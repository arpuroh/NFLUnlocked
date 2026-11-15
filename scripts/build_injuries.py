#!/usr/bin/env python3
"""The Injury Index: every game a rostered player missed hurt, priced in draft dollars.

Inputs
  data/weeks/<season>-wk<NN>-rosters.json   who held whom, week by week (Yahoo box scores)
  data/weeks/<season>-transactions.json     adds, so a roster move can be told apart from a trade
  data/draft.json                           auction price = draft capital
  data/projections.json                     preseason ppg, for players who never played a snap
  nflverse release assets, cached in data/raw/nflverse/ (gitignored):
    weekly_rosters/roster_weekly_<y>.csv    NFL roster status by week (RES = injured reserve, PUP, NFI)
    injuries/injuries_<y>.csv               the official game-status report (Out / Doubtful / Questionable)
    snap_counts/snap_counts_<y>.csv         who actually played
    schedules/games.csv                     byes

A game counts as MISSED HURT when the player's NFL team played, he took no snap, and either he was
on a reserve list (IR, IR-return, PUP, NFI) or the injury report had him Out or Doubtful, or he was
listed Questionable and then went inactive. Healthy scratches, suspensions and free agents never count.

Every missed game belongs to the fantasy team that rostered the player that week, so a player who was
traded is charged to whoever held him when he sat. His draft capital travels with him.

  python3 scripts/build_injuries.py            # uses the cache
  python3 scripts/build_injuries.py --refresh  # re-downloads the nflverse files
"""
import argparse
import collections
import datetime as dt
import glob
import json
import os
import re
import sys
import urllib.request

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "raw", "nflverse")
NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download/"
sys.path.insert(0, HERE)
from build_week import MANAGERS, RENAMED, norm  # noqa: E402

INJURY_RES = {"R01", "R04", "R05", "R40", "R48", "A01"}   # RES/A01 shows up mid-transition onto IR
RES_LABEL = {"R01": "IR", "R48": "IR (return)", "R04": "PUP", "R05": "NFI", "R40": "IR", "A01": "IR"}
YAHOO_TEAM = {"LAR": "LA", "JAC": "JAX", "WSH": "WAS"}
IDP = {"LB", "DB", "DL", "CB", "S", "DE", "DT", "ILB", "OLB", "MLB", "SS", "FS", "EDGE", "NT", "D"}

# Body parts, folded into buckets a reader recognizes
BODY = [
    ("Hamstring", r"hamstring"), ("Knee", r"knee|acl|mcl|pcl|meniscus|patella"),
    ("Ankle", r"ankle"), ("Foot & toe", r"foot|toe|heel|plantar|lisfranc|turf"),
    ("Achilles & calf", r"achilles|calf|shin|lower leg|fibula|tibia|leg"),
    ("Head", r"concussion|head"), ("Shoulder", r"shoulder|collarbone|clavicle|pec|chest"),
    ("Back & core", r"back|oblique|abdom|rib|core|hip|groin|quad|thigh|pelvis|glute"),
    ("Hand & arm", r"hand|wrist|finger|thumb|elbow|arm|forearm|bicep|tricep"),
    ("Neck", r"neck|stinger|spine"), ("Illness", r"illness|personal|not injury"),
]


def body(s):
    s = str(s or "").lower()
    if not s or s == "nan":
        return "Undisclosed"
    for label, rx in BODY:
        if re.search(rx, s):
            return label
    return "Other"


def nflverse(path, refresh=False):
    dest = os.path.join(CACHE, path)
    if refresh or not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        print("download", path)
        urllib.request.urlretrieve(NFLVERSE + path, dest)
    return dest


def side(pos):
    return "D" if str(pos).upper() in IDP else "O"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    y = a.season

    # ── fantasy side ───────────────────────────────────────
    files = sorted(glob.glob(os.path.join(DATA, "weeks", f"{y}-wk*-rosters.json")))
    weeks = {int(re.search(r"wk(\d+)", f).group(1)): json.load(open(f)) for f in files}
    W = max(weeks)
    cur = json.load(open(os.path.join(DATA, f"week{W}.json")))
    tmeta = {t["team_id"]: t for t in cur["teams"]}
    draft = json.load(open(os.path.join(DATA, "draft.json")))
    cost = {}
    drafter = {}
    for t in draft["teams"]:
        for p in t["picks"]:
            if p["pos"] == "DEF":
                continue
            cost[norm(p["player"])] = p["cost"]
            drafter[norm(p["player"])] = RENAMED.get(t["team"], t["team"])
    proj = {}
    for t in json.load(open(os.path.join(DATA, "projections.json")))["teams"]:
        for row in t.get("lineup", []) + t.get("bench", []):
            n = row.get("player")
            if n and row.get("ppg") is not None:
                proj[norm(n)] = row["ppg"]
    adds = json.load(open(os.path.join(DATA, "weeks", f"{y}-transactions.json")))["adds"]
    added = collections.defaultdict(list)
    for x in adds:
        added[norm(x["player"])].append((x["week"], x["team_id"], x.get("bid")))

    # ── NFL side ───────────────────────────────────────────
    R = pd.read_csv(nflverse(f"weekly_rosters/roster_weekly_{y}.csv", a.refresh), low_memory=False)
    I = pd.read_csv(nflverse(f"injuries/injuries_{y}.csv", a.refresh), low_memory=False)
    S = pd.read_csv(nflverse(f"snap_counts/snap_counts_{y}.csv", a.refresh), low_memory=False)
    G = pd.read_csv(nflverse("schedules/games.csv", a.refresh), low_memory=False)
    R = R[R.game_type == "REG"]
    I = I[I.game_type == "REG"]
    G = G[(G.season == y) & (G.game_type == "REG")]
    plays = collections.defaultdict(set)   # (team, week) -> played that week
    for _, g in G.iterrows():
        plays[g.home_team].add(int(g.week))
        plays[g.away_team].add(int(g.week))
    snaps = set()
    S["tot"] = S[["offense_snaps", "defense_snaps", "st_snaps"]].fillna(0).sum(axis=1)
    for _, s in S[S.tot > 0].iterrows():
        snaps.add((s.pfr_player_id, int(s.week)))
    roster = {}       # (gsis, week) -> row
    for r in R.itertuples():
        roster[(r.gsis_id, int(r.week))] = r
    rep = {}
    for r in I.itertuples():
        rep[(r.gsis_id, int(r.week))] = r

    by_name = collections.defaultdict(set)
    for r in R[["gsis_id", "full_name", "football_name", "first_name", "last_name", "team", "position"]].drop_duplicates().itertuples():
        for nm in {norm(r.full_name), norm(f"{r.football_name if isinstance(r.football_name, str) else r.first_name} {r.last_name}")}:
            by_name[nm].add((r.gsis_id, r.team, side(r.position)))
        by_name["init:" + norm(f"{str(r.first_name)[:1]} {r.last_name}")].add((r.gsis_id, r.team, side(r.position)))

    def gsis(name, team, pos):
        nn = norm(name)
        c = by_name.get(nn) or set()
        if not c and re.match(r"^[A-Za-z]\. ", name):
            c = by_name.get("init:" + nn) or set()
        c = {x for x in c if x[2] == side(pos)} or c
        if len(c) > 1:
            t = YAHOO_TEAM.get(team.upper(), team.upper())
            c = {x for x in c if x[1] == t} or c
        ids = {x[0] for x in c}
        return ids.pop() if len(ids) == 1 else None

    # ── walk every rostered player-week ────────────────────
    ids = {}
    held = collections.defaultdict(dict)       # pkey -> week -> team_id
    slot = collections.defaultdict(dict)       # pkey -> week -> slot
    info = {}
    yahoo_pts = collections.defaultdict(dict)  # pkey -> week -> pts
    yahoo_line = collections.defaultdict(dict) # pkey -> week -> stat line ("" when he did nothing)
    for w, teams in weeks.items():
        for tid, t in teams.items():
            for p in t["starters"] + t["bench"]:
                if p.get("empty") or p["name"] == "(Empty)" or p["pos"] == "DEF":
                    continue
                k = norm(p["name"])
                held[k][w] = tid
                slot[k][w] = p["slot"]
                yahoo_pts[k][w] = p["pts"]
                yahoo_line[k][w] = (p.get("stats") or "").strip()
                info[k] = {"name": p["name"], "pos": p["pos"], "nfl": p["nflTeam"]}
                if k not in ids:
                    ids[k] = gsis(p["name"], p["nflTeam"], p["pos"])

    unmatched = sorted(info[k]["name"] for k in info if not ids[k])
    pfr = {r.gsis_id: r.pfr_id for r in R[["gsis_id", "pfr_id"]].drop_duplicates("gsis_id").itertuples()}

    def where(g, w):
        """The injury on file for player g in week w: this week's report, then the practice
        report, then the nearest earlier report, then the next one filed."""
        order = [w] + list(range(w - 1, 0, -1)) + list(range(w + 1, W + 3))
        for b in order:
            r = rep.get((g, b))
            if r is None:
                continue
            for col in ("report_primary_injury", "practice_primary_injury"):
                v = getattr(r, col)
                if isinstance(v, str) and not v.lower().startswith("not injury"):
                    return v
        return None

    def status(k, w):
        """('played'|'bye'|'hurt'|'dnp'|'nfa', detail dict) for player k in week w."""
        g = ids.get(k)
        if not g:
            return "nfa", {}
        r = roster.get((g, w))
        if r is None:
            return "nfa", {}
        team = r.team
        if w not in plays[team]:
            return "bye", {"team": team}
        if (pfr.get(g), w) in snaps or yahoo_line[k].get(w) or yahoo_pts[k].get(w):
            return "played", {"team": team}   # a Yahoo stat line beats a missing snap count
        ir = rep.get((g, w))
        rs = ir.report_status if ir is not None and isinstance(ir.report_status, str) else None
        pp = ir.practice_primary_injury if ir is not None and isinstance(ir.practice_primary_injury, str) else None
        if pp and pp.lower().startswith("not injury"):
            pp = None
        part = where(g, w)
        if r.status == "RES" and r.status_description_abbr in INJURY_RES:
            return "hurt", {"team": team, "why": RES_LABEL.get(r.status_description_abbr, "IR"), "part": part}
        if rs in ("Out", "Doubtful", "Questionable") or (pp and ir.practice_status != "Full Participation in Practice"):
            return "hurt", {"team": team, "why": rs or "Did not play", "part": part}
        return "dnp", {"team": team, "why": r.status}

    # healthy ppg: Yahoo points in weeks he took a snap, whoever held him
    def ppg(k):
        pts = [yahoo_pts[k][w] for w in yahoo_pts[k] if status(k, w)[0] == "played"]
        if len(pts) >= 2:
            return round(sum(pts) / len(pts), 2), "season"
        if k in proj:
            return proj[k], "preseason"
        if pts:
            return round(pts[0], 2), "season"
        return 0.0, "none"

    # ── trades: a player changes fantasy team without an add to explain it ──
    trades = collections.defaultdict(lambda: {"week": None, "sides": collections.defaultdict(list)})
    moved = {}
    for k, ws in held.items():
        prev = None
        for w in sorted(ws):
            tid = ws[w]
            if prev and prev[1] != tid and not any(t == tid and prev[0] < aw <= w for aw, t, _ in added.get(k, [])):
                pair = tuple(sorted((prev[1], tid)))
                tr = trades[(w, pair)]
                tr["week"] = w
                tr["sides"][tid].append(k)
                moved.setdefault(k, []).append({"week": w, "from": prev[1], "to": tid})
            prev = (w, tid)

    name_of = {tid: m["name"] for tid, m in tmeta.items()}

    def how(k, tid):
        if any(mv["to"] == tid for mv in moved.get(k, [])):
            return "trade"
        if drafter.get(k) == name_of[tid]:
            return "draft"
        return "waivers"

    def capital(k, tid, w):
        """What the player cost the team holding him: his auction price if they drafted him or
        traded for him (the price travels with the player), the FAAB bid if they claimed him."""
        h = how(k, tid)
        if h in ("draft", "trade"):
            return cost.get(k, 0)
        bids = [b for aw, t, b in added.get(k, []) if t == tid and aw <= w]
        return (bids[-1] or 0) if bids else 0

    # ── tally ──────────────────────────────────────────────
    T = {tid: {"team_id": tid, "players": set(), "games": 0, "dollar_games": 0, "points": 0.0,
               "weekly": collections.defaultdict(lambda: {"dollars": 0, "games": 0, "who": []}),
               "ghosts": [], "byes": [], "ir_weeks": 0, "parts": collections.Counter(),
               "drafted_dollars": 0}
         for tid in tmeta}
    P = {}
    parts = collections.Counter()
    league_week = collections.defaultdict(lambda: {"dollars": 0, "games": 0, "players": 0})
    for k, ws in held.items():
        val, src = ppg(k)
        rec = P.setdefault(k, {"name": info[k]["name"], "pos": info[k]["pos"], "nfl": info[k]["nfl"],
                               "cost": cost.get(k, 0), "drafted_by": drafter.get(k), "ppg": val, "ppg_src": src,
                               "missed": [], "owners": collections.Counter(), "dollar_games": 0,
                               "traded": moved.get(k, [])})
        for w, tid in ws.items():
            st, d = status(k, w)
            sl = slot[k][w]
            if sl == "IR":
                T[tid]["ir_weeks"] += 1
            started = sl not in ("BN", "IR")
            if started and st in ("hurt", "dnp", "nfa"):
                T[tid]["ghosts"].append({"week": w, "name": info[k]["name"], "pos": info[k]["pos"],
                                         "why": d.get("why", "no team") if st != "hurt" else (d.get("why") or "Out"),
                                         "hurt": st == "hurt", "pts": yahoo_pts[k][w]})
            if started and st == "bye":
                T[tid]["byes"].append({"week": w, "name": info[k]["name"], "pos": info[k]["pos"]})
            if st != "hurt":
                continue
            c = capital(k, tid, w)
            part = body(d.get("part"))
            rec["missed"].append({"week": w, "team_id": tid, "why": d.get("why"), "part": d.get("part") or None,
                                  "body": part, "slot": sl, "capital": c})
            rec["owners"][tid] += 1
            rec.setdefault("owner_dg", collections.Counter())[tid] += c
            rec["dollar_games"] += c
            tt = T[tid]
            tt["players"].add(k)
            tt["games"] += 1
            tt["dollar_games"] += c
            tt["points"] += val
            tt["parts"][part] += 1
            tt["weekly"][w]["dollars"] += c
            tt["weekly"][w]["games"] += 1
            tt["weekly"][w]["who"].append(info[k]["name"])
            parts[part] += 1
            league_week[w]["dollars"] += c
            league_week[w]["games"] += 1

    # who is hurt right now: the most recent injury report, against the latest rosters
    nxt = W + 1 if (I.week == W + 1).any() else W
    now = []
    for tid, t in weeks[W].items():
        for p in t["starters"] + t["bench"]:
            if p.get("empty") or p["pos"] == "DEF" or p["name"] == "(Empty)":
                continue
            k = norm(p["name"])
            g = ids.get(k)
            r = roster.get((g, nxt)) if g else None
            ir = rep.get((g, nxt)) if g else None
            tag = None
            if r is not None and r.status == "RES" and r.status_description_abbr in INJURY_RES:
                tag = RES_LABEL.get(r.status_description_abbr, "IR")
            elif ir is not None and isinstance(ir.report_status, str):
                tag = ir.report_status
            if not tag:
                continue
            part = where(g, nxt)
            now.append({"team_id": tid, "name": p["name"], "pos": p["pos"], "nfl": p["nflTeam"],
                        "status": tag, "part": part, "cost": capital(k, tid, W), "slot": p["slot"],
                        "missed": len(P.get(k, {}).get("missed", []))})
    order = {"IR": 0, "IR (return)": 1, "PUP": 2, "NFI": 3, "Out": 4, "Doubtful": 5, "Questionable": 6}
    now.sort(key=lambda x: (order.get(x["status"], 9), -x["cost"]))

    # ── output ─────────────────────────────────────────────
    teams = []
    for tid, t in T.items():
        m = tmeta[tid]
        spent = sum(p["cost"] for dt_ in draft["teams"] if RENAMED.get(dt_["team"], dt_["team"]) == m["name"] or dt_["team"] == m["name"] for p in dt_["picks"])
        teams.append({
            "team_id": tid, "name": m["name"], "manager": m.get("manager") or MANAGERS.get(m["name"], ""),
            "logo": m.get("logo", ""), "record": m["season"]["record"], "wins": m["season"]["wins"],
            "points_for": m["season"]["points_for"], "power_rank": m.get("power_rank"),
            "injured": len(t["players"]), "games": t["games"], "dollar_games": t["dollar_games"],
            "per_week": round(t["dollar_games"] / W, 1), "points": round(t["points"], 1),
            "ir_weeks": t["ir_weeks"],
            "now": sum(1 for x in now if x["team_id"] == tid and x["status"] not in ("Questionable",)),
            "due": sum(x["cost"] for x in now if x["team_id"] == tid and x["status"] not in ("Questionable",)),
            "weekly": [{"week": w, **t["weekly"][w]} for w in range(1, W + 1)],
            "ghosts": sorted(t["ghosts"], key=lambda g: g["week"]),
            "byes": sorted(t["byes"], key=lambda g: g["week"]),
            "parts": t["parts"].most_common(),
            "ledger": sorted(({"name": P[k]["name"], "pos": P[k]["pos"], "nfl": P[k]["nfl"], "cost": P[k]["cost"],
                               "games": P[k]["owners"][tid], "dg": P[k]["owner_dg"][tid],
                               "paid": max((m["capital"] for m in P[k]["missed"] if m["team_id"] == tid), default=0),
                               "weeks": [m["week"] for m in P[k]["missed"] if m["team_id"] == tid],
                               "part": next((m["part"] for m in reversed(P[k]["missed"]) if m["part"]), None),
                               "how": how(k, tid)}
                              for k in t["players"]), key=lambda x: (-x["dg"], -x["games"], x["name"])),
            "draft_spent": spent,
        })
    teams.sort(key=lambda x: (-x["dollar_games"], -x["games"]))
    for i, t in enumerate(teams):
        t["rank"] = i + 1

    players = []
    for k, p in P.items():
        if not p["missed"]:
            continue
        bodies = collections.Counter(m["body"] for m in p["missed"])
        last = next((m["part"] for m in reversed(p["missed"]) if m["part"]), None)
        players.append({"name": p["name"], "pos": p["pos"], "nfl": p["nfl"], "cost": p["cost"],
                        "drafted_by": p["drafted_by"], "games": len(p["missed"]),
                        "dollar_games": p["dollar_games"], "ppg": p["ppg"], "ppg_src": p["ppg_src"],
                        "points": round(p["ppg"] * len(p["missed"]), 1),
                        "part": last, "body": bodies.most_common(1)[0][0],
                        "weeks": [m["week"] for m in p["missed"]],
                        "owners": [{"team_id": t, "games": n, "dg": p["owner_dg"][t]} for t, n in p["owners"].most_common()],
                        "traded": p["traded"]})
    players.sort(key=lambda x: (-x["dollar_games"], -x["games"], -x["points"]))

    trade_out = []
    for (w, pair), tr in sorted(trades.items()):
        sides = []
        for tid in pair:
            got = []
            for k in tr["sides"].get(tid, []):
                before = sum(1 for m in P[k]["missed"] if m["week"] < w)
                after = sum(1 for m in P[k]["missed"] if m["week"] >= w and m["team_id"] == tid)
                got.append({"name": info[k]["name"], "pos": info[k]["pos"], "cost": cost.get(k, 0),
                            "missed_before": before, "missed_after": after,
                            "dg_after": sum(m["capital"] for m in P[k]["missed"] if m["week"] >= w and m["team_id"] == tid)})
            sides.append({"team_id": tid, "got": got})
        trade_out.append({"week": w, "sides": sides})

    stashes = []
    for k in info:
        if ids.get(k):
            continue
        ws = held[k]
        by = collections.Counter(ws.values()).most_common(1)[0][0]
        stashes.append({"name": info[k]["name"], "pos": info[k]["pos"], "nfl": info[k]["nfl"],
                        "team_id": by, "weeks": len(ws), "cost": cost.get(k, 0)})
    stashes.sort(key=lambda s: -s["weeks"])

    tot_dg = sum(t["dollar_games"] for t in teams)
    out = {
        "season": y, "through_week": W, "report_week": nxt,
        "built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": {"injured": len(players), "games": sum(t["games"] for t in teams),
                   "dollar_games": tot_dg, "points": round(sum(t["points"] for t in teams), 1),
                   "ghosts": sum(len(t["ghosts"]) for t in teams), "byes": sum(len(t["byes"]) for t in teams),
                   "now": len([x for x in now if x["status"] != "Questionable"])},
        "teams": teams,
        "players": players,
        "parts": parts.most_common(),
        "league_weekly": [{"week": w, "dollars": league_week[w]["dollars"], "games": league_week[w]["games"]}
                          for w in range(1, W + 1)],
        "now": now,
        "trades": trade_out,
        "stashes": stashes,
        "unmatched": unmatched,
        "method": {
            "hurt": "A game counts when the player's NFL team played, he took no snap, and he was on injured reserve, PUP or NFI, listed Out or Doubtful on the official injury report, or listed Questionable and then inactive. Byes, healthy scratches, suspensions and unsigned players never count.",
            "owner": "Each missed game is charged to whoever had the player on their Yahoo roster that week. Traded players carry their draft price to the new team. Drop a hurt player and he stops costing you.",
            "bill": "The Injury Bill is what a player cost you times the games he missed: a $40 player out three weeks is a 120 bill. Drafted players cost their auction price. Traded-for players bring their auction price with them, so the buyer inherits it. Waiver and free-agent pickups cost their FAAB bid, usually next to nothing, so they count toward the injured-player tally while adding little to the bill.",
            "points": "Points on the shelf: games missed times the player's healthy average this season (Yahoo points in the games he played), or his preseason projection if he has fewer than two games.",
            "source": "Injury reports, NFL roster status and snap counts from nflverse. Rosters from the league's Yahoo box scores. Draft prices from the 2026 auction.",
        },
    }
    dest = os.path.join(DATA, "injuries.json")
    try:   # leave the file alone when only the timestamp would change (the cron runs daily)
        old = json.load(open(dest))
        old.pop("built_at", None)
        same = old == json.loads(json.dumps({k: v for k, v in out.items() if k != "built_at"}, ensure_ascii=False))
    except (OSError, ValueError):
        same = False
    if not same:
        with open(dest, "w") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    else:
        print("no change")
    print(f"through week {W}: {out['totals']['injured']} injured players, {out['totals']['games']} games, "
          f"bill {tot_dg}, {len(trade_out)} trades, unmatched {unmatched}")
    for t in teams:
        print(f"{t['rank']:>2} {t['name'][:24]:<24} inj {t['injured']:>2} gm {t['games']:>3} bill {t['dollar_games']:>4} "
              f"pts {t['points']:>6} ghosts {len(t['ghosts'])} byes {len(t['byes'])} {t['record']}")


if __name__ == "__main__":
    main()
