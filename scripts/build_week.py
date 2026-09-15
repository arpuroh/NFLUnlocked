#!/usr/bin/env python3
"""
Build data/week<N>.json — the weekly recap the site reads.

Input:
  data/weeks/<season>-wk<NN>-rosters.json   raw Yahoo box scores, one entry per team,
                                            scraped through a logged-in browser (Yahoo
                                            gives a logged-out visitor only the current
                                            week, and there is no API — see CLAUDE.md).
                                            Keys are whatever Yahoo's mid1/mid2 happened
                                            to be; teams are re-identified by matching
                                            each starter total to points_for in
                                            data/league.json, which is unambiguous.
  data/league.json        standings, PF/PA, FAAB, move counts
  data/draft.json         auction price and real position for every drafted player
  data/projections.json   the preseason model (see scripts/project_draft.py)

Output: data/week<N>.json — numbers plus every line of prose, which lives in
        scripts/week_notes.py so a re-run never clobbers the writing.

Usage:  python3 scripts/build_week.py --week 1
"""
import argparse, json, os, re, unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, "data", *p)

SLOT_ORDER = ["QB", "RB", "WR", "TE", "W/R/T", "K", "DEF", "D"]
IDP_POS = {"LB", "DB", "DE", "DT", "CB", "S"}

MANAGERS = {
    "Hail Mary": "Andrew", "ShakeNBake": "Abhishek", "A dad": "Barrett",
    "FreeGucci": "Nishil", "Kim Jong Nate": "Nathan", "Mac Daddy": "Maclane",
    "The Injured Reserved": "Greg (IR)", "Miley 💨LEO 5K Speedo Fan Club": "Greg (Miley)",
    "Bend The Knee 🐲🔥": "Darrius", "Talk Darty to Me 🎯": "Anuj", "Poop Squad 💩": "Anuj",
    "Good Will Hunting": "Will", "Leo the Cleo": "Chris",
    "The Asshouse Always Wins": "Tom", "Fwamming Gwaggon": "Jon",
}
# teams that renamed after the draft; draft.json still carries the old spelling
RENAMED = {"Poop Squad 💩": "Talk Darty to Me 🎯"}


def norm(n):
    n = unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower()
    n = n.replace(".", "").replace("'", "").replace("-", " ")
    n = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", n)
    return re.sub(r"\s+", " ", n).strip()


def lookup(table, name):
    """Exact first, then a prefix match either way (Yahoo and Yahoo's own draft page
    disagree about suffixes: 'Kenneth Walker' vs 'Kenneth Walker III')."""
    n = norm(name)
    if n in table:
        return table[n]
    hits = [v for k, v in table.items() if k.startswith(n) or n.startswith(k)]
    return hits[0] if len(hits) == 1 else (hits[0] if hits else None)


def eligible(pos, slot, pl):
    if slot == "QB":    return pos == "QB"
    if slot == "RB":    return pos == "RB"
    if slot == "WR":    return pos == "WR"
    if slot == "TE":    return pos == "TE"
    if slot == "W/R/T": return pos in ("RB", "WR", "TE")
    if slot == "K":     return pos == "K"
    if slot == "DEF":   return pos == "DEF"
    if slot == "D":
        raw = str(pl.get("pos", ""))
        return pl.get("slot") == "D" or any(p in IDP_POS for p in raw.split(","))
    return False


def best_lineup(players):
    """Highest-scoring legal lineup out of everyone who was startable that week.
    IR does not count: those players could not have been started, so holding an
    injured star is never charged as a lineup mistake."""
    cands = [p for p in players if p.get("slot") != "IR" and not p.get("empty")]
    order = ["QB", "K", "DEF", "D", "TE", "RB", "RB", "WR", "WR", "W/R/T", "W/R/T"]
    best = {"total": -1, "picks": []}

    def rec(i, used, picks, tot):
        if i == len(order):
            if tot > best["total"]:
                best.update(total=tot, picks=list(picks))
            return
        slot = order[i]
        opts = [j for j, p in enumerate(cands)
                if j not in used and eligible(p["_pos"], slot, p)]
        opts.sort(key=lambda j: -cands[j]["pts"])
        if not opts:
            rec(i + 1, used, picks, tot)
            return
        for j in opts[:6]:                     # six deep is far past any real optimum
            picks.append((slot, j))
            rec(i + 1, used | {j}, picks, tot + cands[j]["pts"])
            picks.pop()

    rec(0, set(), [], 0)
    return best["total"], [(s, cands[j]) for s, j in best["picks"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", type=int, required=True)
    ap.add_argument("--season", type=int, default=2026)
    args = ap.parse_args()

    raw = json.load(open(D("weeks", f"{args.season}-wk{args.week:02d}-rosters.json")))
    league = json.load(open(D("league.json")))
    draft = json.load(open(D("draft.json")))
    proj = json.load(open(D("projections.json")))

    import sys
    sys.path.insert(0, HERE)
    from week_notes import NOTES

    by_id = {t["team_id"]: t for t in league["teams"]}
    # re-identify each scraped roster by its starter total
    tot_to_id = {round(t["points_for"], 2): t["team_id"] for t in league["teams"]}
    if len(tot_to_id) != len(league["teams"]):
        raise SystemExit("two teams scored exactly the same — identify rosters by hand")
    rosters = {}
    for v in raw.values():
        tot = round(sum(p["pts"] for p in v["starters"]), 2)
        if tot not in tot_to_id:
            raise SystemExit(f"starter total {tot} matches no team in league.json")
        rosters[tot_to_id[tot]] = v

    price, pos_of, drafted_by = {}, {}, {}
    for t in draft["teams"]:
        for p in t["picks"]:
            k = norm(p["player"])
            price[k], pos_of[k] = p["cost"], p["pos"]
            drafted_by[k] = RENAMED.get(t["team"], t["team"])

    # preseason model rank
    pre = sorted(proj["teams"], key=lambda t: -t["weekly"])
    pre_rank = {RENAMED.get(t["team"], t["team"]): i + 1 for i, t in enumerate(pre)}
    pre_ppg = {RENAMED.get(t["team"], t["team"]): t["weekly"] for t in proj["teams"]}

    # ── per team ────────────────────────────────────────────────
    teams = {}
    for tid, v in rosters.items():
        meta = by_id[tid]
        squad = v["starters"] + [p for p in v["bench"] if not p.get("empty")]
        for p in squad:
            k = norm(p["name"])
            p["cost"] = lookup(price, p["name"])
            p["_pos"] = lookup(pos_of, p["name"]) or (
                p.get("pos") if p.get("pos") in ("QB", "RB", "WR", "TE", "K", "DEF") else p["slot"])
            p["fa"] = p["cost"] is None
        actual = round(sum(p["pts"] for p in v["starters"]), 2)
        opt, opt_lineup = best_lineup(squad)
        started = {id(p) for p in v["starters"]}
        teams[tid] = {
            "team_id": tid,
            "team_key": meta["team_key"],
            "name": meta["name"],
            "manager": MANAGERS.get(meta["name"], ""),
            "logo": meta.get("logo", ""),
            "points": actual,
            "optimal": round(opt, 2),
            "regret": round(opt - actual, 2),
            "efficiency": round(100 * actual / opt, 1) if opt else 0,
            "projected": round(sum(p.get("proj") or 0 for p in v["starters"]), 2),
            "bench_points": round(sum(p["pts"] for p in v["bench"]
                                      if p.get("slot") == "BN" and not p.get("empty")), 2),
            "moves": meta.get("moves", 0),
            "faab_left": meta.get("faab_balance", 100),
            "pre_rank": pre_rank.get(meta["name"]),
            "pre_ppg": pre_ppg.get(meta["name"]),
            "starters": [{"slot": p["slot"], "name": p["name"], "pos": p["_pos"],
                          "nfl": p.get("nflTeam", ""), "pts": p["pts"],
                          "proj": p.get("proj"), "cost": p["cost"], "fa": p["fa"],
                          "stats": p.get("stats", "")} for p in v["starters"]],
            "bench": [{"slot": p["slot"], "name": p["name"], "pos": p["_pos"],
                       "nfl": p.get("nflTeam", ""), "pts": p["pts"], "proj": p.get("proj"),
                       "cost": p["cost"], "fa": p["fa"], "stats": p.get("stats", "")}
                      for p in v["bench"] if not p.get("empty")],
            "best_lineup": [{"slot": s, "name": p["name"], "pts": p["pts"],
                             "benched": id(p) not in started} for s, p in opt_lineup],
        }

    # ── matchups, from the PF/PA mirror (the scrape has no schedule) ──
    games, seen = [], set()
    for t in league["teams"]:
        if t["team_id"] in seen:
            continue
        opp = [o for o in league["teams"]
               if o["team_id"] != t["team_id"]
               and round(o["points_for"], 2) == round(t["points_against"], 2)]
        if len(opp) != 1:
            raise SystemExit(f"cannot pair {t['name']} from points against")
        opp = opp[0]
        seen |= {t["team_id"], opp["team_id"]}
        w, l = (t, opp) if t["points_for"] > opp["points_for"] else (opp, t)
        games.append({
            "winner": w["team_id"], "loser": l["team_id"],
            "winner_points": round(w["points_for"], 2),
            "loser_points": round(l["points_for"], 2),
            "margin": round(w["points_for"] - l["points_for"], 2),
            "note": NOTES["games"].get(int(w["team_id"]), ""),
        })
    games.sort(key=lambda g: g["margin"])

    # ── all-play and luck ───────────────────────────────────────
    scores = {tid: teams[tid]["points"] for tid in teams}
    for tid in teams:
        s = scores[tid]
        wins = sum(1 for o, v in scores.items() if o != tid and s > v)
        teams[tid]["all_play"] = f"{wins}-{len(scores) - 1 - wins}"
        teams[tid]["all_play_wins"] = wins
        won = any(g["winner"] == tid for g in games)
        teams[tid]["won"] = won
        # luck = the gap between the result and what the score deserved
        teams[tid]["luck"] = round((1 if won else 0) - wins / (len(scores) - 1), 3)

    # ── league-wide leaderboards ────────────────────────────────
    everyone = []
    for tid, t in teams.items():
        for p in t["starters"]:
            everyone.append({**p, "team": t["name"], "team_id": tid, "started": True})
        for p in t["bench"]:
            if p["slot"] == "BN":
                everyone.append({**p, "team": t["name"], "team_id": tid, "started": False})
    for p in everyone:
        p["vs_proj"] = round(p["pts"] - (p["proj"] or 0), 2)

    starters = [p for p in everyone if p["started"]]
    benched = [p for p in everyone if not p["started"]]
    drafted = [p for p in everyone if p["cost"]]

    out = {
        "season": args.season,
        "week": args.week,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "league_average": round(sum(scores.values()) / len(scores), 2),
        "headline": NOTES["headline"],
        "kicker": NOTES["kicker"],
        "lede": NOTES["lede"],
        "sections": NOTES["sections"],
        "awards": NOTES["awards"],
        "waiver_note": NOTES["waiver_note"],
        "teams": sorted(teams.values(), key=lambda t: -t["points"]),
        "games": games,
        "top_starts": sorted(starters, key=lambda p: -p["pts"])[:12],
        "worst_starts": sorted([p for p in starters if p["proj"]],
                               key=lambda p: p["vs_proj"])[:12],
        "bench_crimes": sorted(benched, key=lambda p: -p["pts"])[:12],
        "money_pits": sorted([p for p in drafted if p["cost"] >= 18 and p["started"]],
                             key=lambda p: p["pts"])[:12],
        "bargains": sorted([p for p in drafted if p["cost"] <= 3 and p["pts"] >= 12],
                           key=lambda p: -p["pts"])[:12],
        "free_agents": sorted([p for p in everyone if p["fa"] and p["pts"] >= 8],
                              key=lambda p: -p["pts"])[:10],
        "slot_averages": {},
    }
    for slot in SLOT_ORDER:
        vals = [p["pts"] for p in starters if p["slot"] == slot]
        if vals:
            out["slot_averages"][slot] = {
                "n": len(vals), "avg": round(sum(vals) / len(vals), 2),
                "high": max(vals), "low": min(vals),
            }


    # ── data/current.json ────────────────────────────────────────
    # The Yahoo scrape cannot see a schedule (no API, and a logged-out visitor is
    # shown only the current week), so league.json ships with an empty matchup list
    # and doubled win totals. Every page reads league.json through NU.load(), which
    # merges this file over it — so standings, power rankings, the scoreboard and
    # the team pages all come from the same re-derived truth as the recap.
    W = {t["team_id"]: t for t in teams.values()}
    lo = min(t["points"] for t in W.values())
    hi = max(t["points"] for t in W.values())
    span = (hi - lo) or 1

    standings, power = [], []
    for tid, t in W.items():
        won = t["won"]
        g = next(g for g in games if tid in (g["winner"], g["loser"]))
        against = g["loser_points"] if won else g["winner_points"]
        standings.append({
            "team_key": t["team_key"], "team_id": tid, "name": t["name"],
            "manager": t["manager"], "logo": t["logo"],
            "wins": 1 if won else 0, "losses": 0 if won else 1, "ties": 0,
            "win_pct": 1.0 if won else 0.0, "streak": "W1" if won else "L1",
            "points_for": t["points"], "points_against": against,
            "week_points": t["points"], "moves": t["moves"],
            "faab_balance": t["faab_left"],
        })
        ap = t["all_play_wins"] / (len(W) - 1)
        scoring = (t["points"] - lo) / span
        power.append({
            "team_key": t["team_key"], "team_id": tid,
            "score": round(0.35 * (1 if won else 0) + 0.30 * scoring
                           + 0.20 * ap + 0.15 * scoring, 4),
            "all_play": t["all_play"], "all_play_pct": round(ap, 4),
            "luck_index": t["luck"], "recent_form": round(scoring, 4),
            "efficiency": t["efficiency"], "regret": t["regret"],
            "prev_rank": t["pre_rank"],          # movement is measured off the draft model
        })
    power.sort(key=lambda r: -r["score"])
    for i, r in enumerate(power):
        r["rank"] = i + 1
        r["movement"] = (r["prev_rank"] - r["rank"]) if r["prev_rank"] else 0
    rank_of = {r["team_id"]: r["rank"] for r in power}
    for s_ in standings:
        s_["rank"] = rank_of[s_["team_id"]]
    standings.sort(key=lambda s_: s_["rank"])

    matchups = [{
        "week": args.week, "status": "postevent",
        "winner_team_key": W[g["winner"]]["team_key"],
        "teams": [
            {"team_key": W[g["winner"]]["team_key"], "name": W[g["winner"]]["name"],
             "points": g["winner_points"], "projected": W[g["winner"]]["projected"]},
            {"team_key": W[g["loser"]]["team_key"], "name": W[g["loser"]]["name"],
             "points": g["loser_points"], "projected": W[g["loser"]]["projected"]},
        ],
    } for g in games]

    cur = {
        "season": args.season, "week": args.week, "status": "final",
        "label": f"Week {args.week} \u00b7 Final",
        "recap": f"week.html?w={args.week}",
        "built_at": out["built_at"],
        "headline": NOTES["headline"], "kicker": NOTES["kicker"], "lede": NOTES["lede"],
        "league_average": out["league_average"],
        "teams": standings, "power_rankings": power, "matchups": matchups,
    }
    json.dump(cur, open(D("current.json"), "w"), indent=1, ensure_ascii=False)
    print(f"wrote {D('current.json')}: week {args.week} marked final")

    path = D(f"week{args.week}.json")
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {path}: {len(out['teams'])} teams, {len(out['games'])} games, "
          f"league average {out['league_average']}")


if __name__ == "__main__":
    main()
