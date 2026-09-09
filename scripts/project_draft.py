#!/usr/bin/env python3
"""
NFL Unlocked — preseason projections for the drafted rosters.

Power rankings should answer one question: how many points is this team going to
put on the board each week? So that is what this computes.

  1. Pull 2026 season projections (Sleeper's public feed, no key required).
  2. Re-score every projected stat line under THIS league's rules, which are not
     standard: half PPR, 4-point passing touchdowns, kickers paid by total field
     goal yardage, and an IDP slot that rewards tackle volume.
  3. Match every drafted player to his projection.
  4. Build each team's best legal lineup and work out its expected weekly points,
     counting the bench for exactly as much as it is worth: starters miss byes and
     games, and when they do, the next man up plays. A team with real depth loses
     less on those weeks than a team whose bench is a row of dollar bills.
  5. Anybody undrafted is the waiver wire, which is the floor every team falls
     back to when they have nothing better.

Writes data/projections.json.

Usage:  python scripts/project_draft.py [--refresh]
"""

import argparse
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = DATA / "raw" / "sleeper"
SEASON = 2026
POSITIONS = ["QB", "RB", "WR", "TE", "K", "DEF", "LB", "DB", "DL"]
FEED = ("https://api.sleeper.app/projections/nfl/{season}"
        "?season_type=regular&position[]={pos}&order_by=pts_half_ppr")

# ---------------------------------------------------------------- league rules
#
# Taken verbatim from the league's own settings page, which is public at
# football.fantasysports.yahoo.com/f1/675504/settings. Do not guess these. The
# ones that differ from every default scoring system are the four-point passing
# touchdown, kickers paid only by total field goal yardage, an IDP slot paid on
# tackle volume, and defensive tiers compressed to roughly half of Yahoo's.
SCORING = {
    "pass_yd": 0.04, "pass_td": 4.0, "pass_int": -1.0, "pass_2pt": 2.0,
    "rush_yd": 0.1, "rush_td": 6.0, "rush_2pt": 2.0,
    "rec": 0.5, "rec_yd": 0.1, "rec_td": 6.0, "rec_2pt": 2.0,
    "fum_lost": -2.0,
    "fgm_yds": 0.1, "xpm": 1.0,
    "idp_tkl_solo": 1.0, "idp_tkl_ast": 0.5, "idp_sack": 2.0,
    "idp_int": 3.0, "idp_ff": 2.0, "idp_fum_rec": 2.0, "idp_td": 6.0,
    "sack": 1.0, "int": 2.0, "fum_rec": 2.0, "def_td": 6.0,
    "def_st_td": 6.0, "def_kr_td": 6.0, "def_pr_td": 6.0, "def_fum_td": 6.0,
    "pr_td": 6.0, "safe": 2.0, "blk_kick": 2.0,
}

# Yahoo also pays a bonus point for a big game: 100, 150 and 200 rushing or
# receiving yards, and 400, 450 and 500 passing. Projections come as season
# totals, so the bonus has to be estimated rather than counted. Game-level
# yardage is roughly lognormal, so a player's per-game average plus a position's
# usual spread gives how often he should clear each line. It is worth a couple of
# points a week across a lineup, and it quietly rewards the workhorses.
BONUS = {
    "rush_yd": ([100, 150, 200], 0.60),
    "rec_yd": ([100, 150, 200], 0.70),
    "pass_yd": ([400, 450, 500], 0.35),
}

# The defensive tiers are worth about three points a game to an average unit,
# points allowed and yards allowed combined, under this league's compressed
# table. No projection source publishes a defense's points or yards allowed, so
# every defense gets the league-average value rather than an invented one. It is
# the same for all fourteen teams, so it moves nobody up or down; it is here so
# the weekly totals are honest rather than three points light.
DEF_TIER_BASELINE = 2.9

# Two settings are left out because nothing projects them: an IDP's passes
# defended (1 point each) and offensive return yardage (1 point per 25). Both are
# small, and both are disclosed on the site so the number is not oversold.

WEEKS = 17          # NFL regular season
BYE = 1             # every player sits one of them

# Share of the remaining weeks a starter is expected to be available. Running
# backs get hurt, quarterbacks mostly do not, and a defense never misses a snap.
AVAILABILITY = {"QB": 0.90, "RB": 0.80, "WR": 0.86, "TE": 0.87,
                "K": 0.96, "DEF": 1.0, "IDP": 0.88}

LINEUP = [("QB", 1), ("RB", 2), ("WR", 2), ("TE", 1), ("FLEX", 2),
          ("K", 1), ("DEF", 1), ("IDP", 1)]
FLEX_OK = ("RB", "WR", "TE")
IDP_POS = ("LB", "DB", "DL", "CB", "S", "DE", "DT")


# ---------------------------------------------------------------- projections

def fetch(refresh: bool) -> list:
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = []
    for pos in POSITIONS:
        f = CACHE / f"{pos}.json"
        if refresh or not f.exists():
            url = FEED.format(season=SEASON, pos=pos)
            req = urllib.request.Request(url, headers={"User-Agent": "nflunlocked/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                f.write_bytes(r.read())
            print(f"  fetched {pos}")
        rows.extend(json.loads(f.read_text()))
    return rows


def _expected_bonus(total_yards: float, games: float, lines: list, cv: float) -> float:
    """Times a player should clear each yardage line over the season, at a point each."""
    if total_yards <= 0 or games <= 0:
        return 0.0
    mu = total_yards / games
    if mu <= 1:
        return 0.0
    sigma2 = math.log(1 + cv * cv)
    sigma = math.sqrt(sigma2)
    med = math.log(mu) - sigma2 / 2          # lognormal median implied by the mean
    out = 0.0
    for line in lines:
        z = (math.log(line) - med) / sigma
        out += games * 0.5 * math.erfc(z / math.sqrt(2))   # games x P(X >= line)
    return out


def score(stats: dict) -> float:
    pts = sum(v * stats.get(k, 0.0) for k, v in SCORING.items())
    games = stats.get("gp", 0.0) or WEEKS
    for key, (lines, cv) in BONUS.items():
        pts += _expected_bonus(stats.get(key, 0.0), games, lines, cv)
    return round(pts, 2)


SUFFIX = re.compile(r"\b(jr|sr|ii|iii|iv|v)\b")


def norm(name: str) -> str:
    n = (name or "").lower().replace("&", "and")
    n = re.sub(r"[.'’`]", "", n)
    n = re.sub(r"[^a-z0-9 ]", " ", n)
    n = SUFFIX.sub(" ", n)
    return " ".join(n.split())


def bucket(pos: str) -> str:
    p = (pos or "").split(",")[0].strip().upper()
    if p in ("QB", "RB", "WR", "TE", "K"):
        return p
    if p in ("DEF", "DST"):
        return "DEF"
    return "IDP"


def build_index(rows: list) -> tuple:
    """name -> {pos: projection}. Team defenses are keyed by nickname."""
    by_name, pool = {}, []
    for r in rows:
        p = r.get("player") or {}
        st = r.get("stats") or {}
        pos = bucket(r.get("position") or p.get("position") or "")
        if pos == "DEF":
            full = p.get("last_name") or p.get("first_name") or ""
        else:
            full = f"{p.get('first_name','')} {p.get('last_name','')}"
        key = norm(full)
        if not key:
            continue
        pts = score(st)
        if pos == "DEF":
            pts += DEF_TIER_BASELINE * WEEKS   # DEF "gp" is 1 in the feed, not a game count
        rec = {"name": full.strip(), "pos": pos, "points": round(pts, 2),
               "team": (p.get("team") or ""), "ppg": round(pts / WEEKS, 2)}
        # keep the best projection under a given name+position
        cur = by_name.get((key, pos))
        if cur is None or pts > cur["points"]:
            by_name[(key, pos)] = rec
        pool.append(rec)
    return by_name, pool


ALIAS = {"hollywood brown": "marquise brown"}


def match(player: str, slot: str, by_name: dict) -> dict | None:
    key = norm(player)
    key = ALIAS.get(key, key)
    hit = by_name.get((key, slot))
    if hit:
        return hit
    # a defense is stored under its nickname; Yahoo writes "Broncos"
    if slot == "DEF":
        for (k, p), v in by_name.items():
            if p == "DEF" and (k.endswith(key) or key.endswith(k)):
                return v
    # IDPs come through Yahoo as DB/CB/S/LB/DL, all of which we bucket as IDP
    for p in ("QB", "RB", "WR", "TE", "K", "DEF", "IDP"):
        hit = by_name.get((key, p))
        if hit and (slot == "IDP" or p == "IDP"):
            return hit
    return None


# ---------------------------------------------------------------- the model

def best_lineup(players: list) -> tuple:
    """Highest-scoring legal lineup, by projected points per game."""
    pool = sorted(players, key=lambda p: -p["ppg"])
    used, starters = set(), []
    for slot, n in LINEUP:
        for _ in range(n):
            cand = next((p for p in pool if id(p) not in used and
                         (p["pos"] in FLEX_OK if slot == "FLEX" else p["pos"] == slot)), None)
            if cand is None:
                starters.append({"slot": slot, "player": None, "ppg": 0.0})
                continue
            used.add(id(cand))
            starters.append({"slot": slot, "player": cand, "ppg": cand["ppg"]})
    bench = [p for p in pool if id(p) not in used]
    return starters, bench


def weekly_projection(starters: list, bench: list, waiver: dict) -> dict:
    """
    Expected points in a normal week.

    Two rules, both of them just describing what managers actually do.

    A slot is never worth less than the waiver wire. If somebody drafted nobody at
    a position, or drafted somebody worse than what is sitting there unowned, he
    picks up the free one in week one and nobody ever mentions it again. So every
    slot is floored at the best realistically available free agent.

    And a starter does not play every week. He has a bye, and he gets hurt, at a
    rate that depends on where he lines up. On those weeks the slot is filled by
    the best replacement that manager actually has, which is where a real bench
    earns its money and a row of dollar bills does not.
    """
    left = list(bench)
    total, detail = 0.0, []
    for s in starters:
        slot = s["slot"]
        pos_ok = FLEX_OK if slot == "FLEX" else (slot,)
        floor = max(waiver.get(p, 0.0) for p in pos_ok)

        starter = s["player"]
        started = max(s["ppg"], floor)
        # who actually covers the bye and the hamstring
        backup = next((p for p in left if p["pos"] in pos_ok), None)
        rep = max(backup["ppg"] if backup else 0.0, floor)
        if backup and backup["ppg"] > floor:
            left.remove(backup)
        else:
            backup = None

        pos = starter["pos"] if starter else pos_ok[0]
        avail = AVAILABILITY.get(pos, 0.85) * (WEEKS - BYE) / WEEKS
        pts = avail * started + (1 - avail) * rep
        total += pts
        detail.append({
            "slot": slot,
            "player": starter["name"] if starter else "(waiver pickup)",
            "ppg": round(s["ppg"], 2),
            "counted": round(started, 2),
            "replaced": bool(starter and s["ppg"] < floor),
            "backup": backup["name"] if backup else "waiver",
            "backup_ppg": round(rep, 2),
            "expected": round(pts, 2),
        })
    return {"weekly": round(total, 2), "slots": detail}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download the projection feed")
    ap.add_argument("--draft", default=str(DATA / "draft.json"))
    ap.add_argument("--out", default=str(DATA / "projections.json"))
    args = ap.parse_args()

    rows = fetch(args.refresh)
    by_name, pool = build_index(rows)
    draft = json.loads(Path(args.draft).read_text())

    drafted_keys = {(norm(p["player"]), bucket(p["pos"])) for p in draft["picks"]}

    teams, misses = [], []
    for t in draft["teams"]:
        roster = []
        for p in t["picks"]:
            slot = bucket(p["pos"])
            m = match(p["player"], slot, by_name)
            if m is None:
                misses.append(f'{p["player"]} ({p["pos"]})')
                m = {"name": p["player"], "pos": slot, "points": 0.0, "ppg": 0.0, "team": p["nfl"]}
            roster.append({**m, "pos": slot, "cost": p["cost"]})
        teams.append((t["team"], roster))

    # the waiver wire: best projection at each slot that nobody drafted
    waiver = {}
    for slot in ("QB", "RB", "WR", "TE", "K", "DEF", "IDP"):
        free = [r for r in pool if r["pos"] == slot
                and (norm(r["name"]), r["pos"]) not in drafted_keys]
        free.sort(key=lambda r: -r["ppg"])
        # not the single best free agent: the one you realistically win, a few deep
        waiver[slot] = round(free[3]["ppg"], 2) if len(free) > 3 else (round(free[0]["ppg"], 2) if free else 0.0)

    out_teams = []
    for name, roster in teams:
        starters, bench = best_lineup(roster)
        proj = weekly_projection(starters, bench, waiver)
        starter_ppg = round(sum(s["counted"] for s in proj["slots"]), 2)
        bench_ppg = round(sum(p["ppg"] for p in bench[:5]), 2)
        out_teams.append({
            "team": name,
            "weekly": proj["weekly"],
            "season": round(proj["weekly"] * WEEKS, 1),
            "lineup_ppg": starter_ppg,
            "depth_cost": round(starter_ppg - proj["weekly"], 2),
            "waiver_slots": [x["slot"] for x in proj["slots"] if x["replaced"] or x["player"] == "(waiver pickup)"],
            "bench_ppg": bench_ppg,
            "lineup": proj["slots"],
            "bench": [{"name": p["name"], "pos": p["pos"], "ppg": p["ppg"], "cost": p["cost"]}
                      for p in bench[:6]],
        })
    out_teams.sort(key=lambda t: -t["weekly"])
    for i, t in enumerate(out_teams, 1):
        t["rank"] = i

    avg = round(sum(t["weekly"] for t in out_teams) / len(out_teams), 2)
    out = {
        "season": SEASON,
        "source": "Sleeper 2026 season projections, re-scored under this league's rules",
        "scoring_note": ("scored on the league's own Yahoo settings: half PPR, 4-point passing "
                         "touchdowns, big-game yardage bonuses, kickers paid 1 point per 10 yards of "
                         "made field goals, IDP on tackle volume, and this league's compressed "
                         "defensive tiers. Passes defended and return yardage are not projected by "
                         "any source and are left out."),
        "waiver_baseline": waiver,
        "avg_weekly": avg,
        "spread": round(out_teams[0]["weekly"] - out_teams[-1]["weekly"], 2),
        "teams": out_teams,
        "unmatched": sorted(set(misses)),
    }
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"  matched {len(draft['picks']) - len(misses)}/{len(draft['picks'])} picks")
    if misses:
        print(f"  unmatched: {sorted(set(misses))}")
    print(f"  league average {avg} pts/week, spread {out['spread']}")
    for t in out_teams:
        print(f"  {t['rank']:>2} {t['team'][:30]:32} {t['weekly']:>7} /wk   lineup {t['lineup_ppg']:>6}   depth cost {t['depth_cost']:>5}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
