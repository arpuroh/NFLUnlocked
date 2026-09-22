#!/usr/bin/env python3
"""
Build the weekly recaps: data/week<N>.json for every week on file, data/weeks.json
(the index the week picker reads) and data/current.json (the latest week, which every
page merges over the Yahoo scrape).

    python3 scripts/build_week.py              # rebuild every week that has a scrape
    python3 scripts/build_week.py --season 2026

Inputs, all under data/:
  weeks/<season>-wk<NN>-rosters.json   one entry per team, keyed by Yahoo team id:
                                       {team_id, total, starters[], bench[]}. Scraped from
                                       /f1/675504/matchup?week=N&mid1=<id> in a logged-in
                                       browser (no API, and a logged-out visitor only ever
                                       sees the current week). Each page carries both teams.
  weeks/<season>-pairings.json         the real matchups per week, by team id.
  weeks/<season>-transactions.json     every add off the transactions page, with FAAB bids.
  league.json                          the live scrape. Used for names, logos, move counts,
                                       and as the TEST: cumulative records and points must
                                       match it exactly or the build says so loudly.
  draft.json, projections.json         auction prices, positions, the preseason model.

THE MEDIAN GAME. This league plays two games a week: the head-to-head matchup and a game
against the league median score. A weekly record is 2-0, 1-1 or 0-2, never 1-0. With
fourteen teams the median sits between the 7th and 8th scores, nobody can tie it, and the
two teams that set it are the two it decides. Luck is measured on the head-to-head only,
because the median game is decided by your own score and nothing else.

All prose lives in scripts/week_notes.py, keyed by week, so a rebuild never touches it.
"""
import argparse, glob, json, os, re, statistics, sys, unicodedata
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D = lambda *p: os.path.join(ROOT, "data", *p)
sys.path.insert(0, HERE)

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
RENAMED = {"Poop Squad 💩": "Talk Darty to Me 🎯"}   # draft.json keeps the old spelling


def norm(n):
    n = unicodedata.normalize("NFKD", str(n)).encode("ascii", "ignore").decode().lower()
    n = n.replace(".", "").replace("'", "").replace("-", " ")
    n = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", n)
    return re.sub(r"\s+", " ", n).strip()


def lookup(table, name):
    n = norm(name)
    if n in table:
        return table[n]
    hits = [v for k, v in table.items() if k.startswith(n) or n.startswith(k)]
    return hits[0] if hits else None


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
        return pl.get("slot") == "D" or any(p.strip() in IDP_POS for p in raw.split(","))
    return False


def best_lineup(players):
    """Highest-scoring legal lineup out of everyone startable that week. IR does not
    count: an injured star who could not be started is never a lineup mistake."""
    cands = [p for p in players if p.get("slot") != "IR" and not p.get("empty")]
    order = ["QB", "K", "DEF", "D", "TE", "RB", "RB", "WR", "WR", "W/R/T", "W/R/T"]
    best = {"total": -1e9, "picks": []}

    def rec(i, used, picks, tot):
        if i == len(order):
            if tot > best["total"]:
                best.update(total=tot, picks=list(picks))
            return
        slot = order[i]
        opts = sorted((j for j, p in enumerate(cands)
                       if j not in used and eligible(p["_pos"], slot, p)),
                      key=lambda j: -cands[j]["pts"])
        if not opts:
            rec(i + 1, used, picks, tot)
            return
        for j in opts[:6]:
            picks.append((slot, j))
            rec(i + 1, used | {j}, picks, tot + cands[j]["pts"])
            picks.pop()

    rec(0, set(), [], 0)
    return best["total"], [(s, cands[j]) for s, j in best["picks"]]


def streak(weekly):
    if not weekly or weekly[-1] == 1:
        return ""
    k = weekly[-1]
    n = 0
    for w in reversed(weekly):
        if w != k:
            break
        n += 2
    return ("W" if k == 2 else "L") + str(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--season", type=int, default=2026)
    ap.add_argument("--week", type=int, help="ignored; every week on file is rebuilt")
    args = ap.parse_args()
    season = args.season

    from week_notes import NOTES

    league = json.load(open(D("league.json")))
    draft = json.load(open(D("draft.json")))
    proj = json.load(open(D("projections.json")))
    pairings = json.load(open(D("weeks", f"{season}-pairings.json")))
    tx_path = D("weeks", f"{season}-transactions.json")
    adds = json.load(open(tx_path))["adds"] if os.path.exists(tx_path) else []

    files = sorted(glob.glob(D("weeks", f"{season}-wk*-rosters.json")))
    weeks = sorted(int(re.search(r"wk(\d+)", f).group(1)) for f in files)
    if not weeks:
        raise SystemExit("no roster scrapes in data/weeks/")
    latest = max(weeks)

    by_id = {t["team_id"]: t for t in league["teams"]}
    ids = list(by_id)

    price, pos_of = {}, {}
    for t in draft["teams"]:
        for p in t["picks"]:
            k = norm(p["player"])
            price[k], pos_of[k] = p["cost"], p["pos"]

    pre = sorted(proj["teams"], key=lambda t: -t["weekly"])
    pre_rank_by_name = {RENAMED.get(t["team"], t["team"]): i + 1 for i, t in enumerate(pre)}
    pre_ppg_by_name = {RENAMED.get(t["team"], t["team"]): t["weekly"] for t in proj["teams"]}

    season_tot = {tid: dict(wins=0, losses=0, pf=0.0, pa=0.0, ap_w=0, ap_l=0,
                            h2h_w=0, med_w=0, luck=0.0, scores=[], opt_w=0, regret=0.0, weekly_w=[])
                  for tid in ids}
    player_season = {}          # norm(name) -> {name, pts, weeks, cost, team_id (latest)}
    prev_rank = {by_id[t]["team_id"]: pre_rank_by_name.get(by_id[t]["name"]) for t in ids}
    index = []

    for wk in weeks:
        raw = json.load(open(D("weeks", f"{season}-wk{wk:02d}-rosters.json")))
        notes = NOTES.get(wk, {})
        pairs = pairings[f"{season}-wk{wk:02d}"]
        old_path = D(f"week{wk}.json")
        old = json.load(open(old_path)) if os.path.exists(old_path) else {}
        old_moves = {t["team_id"]: t.get("moves") for t in old.get("teams", [])}

        # ── per team ────────────────────────────────────────────
        teams = {}
        for tid, v in raw.items():
            meta = by_id[tid]
            squad = v["starters"] + [p for p in v["bench"] if not p.get("empty")]
            for p in squad:
                p["cost"] = lookup(price, p["name"])
                known = lookup(pos_of, p["name"])
                raw_pos = str(p.get("pos") or "")
                p["_pos"] = known or (raw_pos if raw_pos in ("QB", "RB", "WR", "TE", "K", "DEF")
                                      else ("D" if any(x.strip() in IDP_POS for x in raw_pos.split(",")) else p["slot"]))
                p["fa"] = p["cost"] is None
            actual = round(sum(p["pts"] for p in v["starters"]), 2)
            opt, opt_lineup = best_lineup(squad)
            started = {id(p) for p in v["starters"]}
            teams[tid] = {
                "team_id": tid, "team_key": meta["team_key"], "name": meta["name"],
                "manager": MANAGERS.get(meta["name"], ""), "logo": meta.get("logo", ""),
                "points": actual, "optimal": round(opt, 2), "regret": round(opt - actual, 2),
                "efficiency": round(100 * actual / opt, 1) if opt else 0,
                "projected": round(sum(p.get("proj") or 0 for p in v["starters"]), 2),
                "bench_points": round(sum(p["pts"] for p in v["bench"]
                                          if p.get("slot") == "BN" and not p.get("empty")), 2),
                # moves is a live counter on Yahoo; a past week keeps the number it shipped with
                "moves": meta.get("moves", 0) if wk == latest else (old_moves.get(tid) or 0),
                "faab_left": 100 - sum(a["bid"] or 0 for a in adds
                                       if a["team_id"] == tid and a["week"] <= wk),
                "faab_spent_week": sum(a["bid"] or 0 for a in adds
                                       if a["team_id"] == tid and a["week"] == wk),
                "adds_week": sum(1 for a in adds if a["team_id"] == tid and a["week"] == wk),
                "pre_rank": pre_rank_by_name.get(meta["name"]),
                "pre_ppg": pre_ppg_by_name.get(meta["name"]),
                "starters": [{"slot": p["slot"], "name": p["name"], "pos": p["_pos"],
                              "pts": p["pts"], "proj": p.get("proj"), "cost": p["cost"],
                              "fa": p["fa"], "stats": p.get("stats", "")} for p in v["starters"]],
                "bench": [{"slot": p["slot"], "name": p["name"], "pos": p["_pos"],
                           "pts": p["pts"], "proj": p.get("proj"), "cost": p["cost"],
                           "fa": p["fa"], "stats": p.get("stats", "")}
                          for p in v["bench"] if not p.get("empty")],
                "best_lineup": [{"slot": s, "name": p["name"], "pts": p["pts"],
                                 "benched": id(p) not in started} for s, p in opt_lineup],
            }
            for p in squad:
                k = norm(p["name"])
                ps = player_season.setdefault(k, {"name": p["name"], "pts": 0.0, "weeks": 0,
                                                  "cost": p["cost"], "pos": p["_pos"]})
                ps["pts"] = round(ps["pts"] + p["pts"], 2)
                ps["weeks"] += 1
                ps["team_id"] = tid

        # ── games, median, all-play, luck ───────────────────────
        games = []
        for a, b in pairs:
            w, l = (a, b) if teams[a]["points"] > teams[b]["points"] else (b, a)
            games.append({"winner": w, "loser": l,
                          "winner_points": teams[w]["points"], "loser_points": teams[l]["points"],
                          "margin": round(teams[w]["points"] - teams[l]["points"], 2),
                          "note": notes.get("games", {}).get(int(w), "")})
        games.sort(key=lambda g: g["margin"])
        scores = {tid: t["points"] for tid, t in teams.items()}
        median = round(statistics.median(scores.values()), 2)
        opp = {}
        for g in games:
            opp[g["winner"]], opp[g["loser"]] = g["loser"], g["winner"]

        for tid, t in teams.items():
            s = scores[tid]
            apw = sum(1 for o, v in scores.items() if o != tid and s > v)
            h2h = any(g["winner"] == tid for g in games)
            beat = s > median
            w = int(h2h) + int(beat)
            t.update(all_play=f"{apw}-{len(scores) - 1 - apw}", all_play_wins=apw,
                     won=h2h, beat_median=beat, vs_median=round(s - median, 2),
                     wins=w, losses=2 - w, record=f"{w}-{2 - w}",
                     luck=round(int(h2h) - apw / (len(scores) - 1), 3),
                     opponent=opp[tid], points_against=scores[opp[tid]])
            st = season_tot[tid]
            st["wins"] += w; st["losses"] += 2 - w
            st["pf"] = round(st["pf"] + s, 2); st["pa"] = round(st["pa"] + scores[opp[tid]], 2)
            st["ap_w"] += apw; st["ap_l"] += len(scores) - 1 - apw
            st["h2h_w"] += int(h2h); st["med_w"] += int(beat)
            st["luck"] = round(st["luck"] + t["luck"], 3)
            st["scores"].append(s)
            st["weekly_w"].append(w)

            # The record the best lineup would have earned, everyone else as played.
            # The median is recomputed with this team's best score in place of its real one.
            o = t["optimal"]
            med_o = statistics.median([o if x == tid else v for x, v in scores.items()])
            ow = int(o > scores[opp[tid]]) + int(o > med_o)
            t["optimal_wins"] = ow
            t["optimal_record"] = f"{ow}-{2 - ow}"
            t["lineup_tax"] = ow - w          # wins left on the bench this week
            st["opt_w"] += ow
            st["regret"] = round(st["regret"] + t["regret"], 2)

        for tid, t in teams.items():
            st = season_tot[tid]
            t["season"] = {"wins": st["wins"], "losses": st["losses"],
                           "record": f"{st['wins']}-{st['losses']}",
                           "points_for": st["pf"], "points_against": st["pa"],
                           "all_play": f"{st['ap_w']}-{st['ap_l']}",
                           "h2h": f"{st['h2h_w']}-{wk - st['h2h_w']}",
                           "vs_median": f"{st['med_w']}-{wk - st['med_w']}",
                           "luck": st["luck"],
                           "optimal_record": f"{st['opt_w']}-{2 * wk - st['opt_w']}",
                           "lineup_tax": st["opt_w"] - st["wins"],
                           "regret": st["regret"]}

        # ── power rankings as of this week ───────────────────────
        pfs = [season_tot[t]["pf"] for t in ids]
        lo_pf, hi_pf = min(pfs), max(pfs)
        lo_s, hi_s = min(scores.values()), max(scores.values())
        power = []
        for tid in ids:
            st = season_tot[tid]
            games_played = st["wins"] + st["losses"]
            ap = st["ap_w"] / max(1, st["ap_w"] + st["ap_l"])
            scoring = (st["pf"] - lo_pf) / ((hi_pf - lo_pf) or 1)
            form = (scores[tid] - lo_s) / ((hi_s - lo_s) or 1)
            power.append({"team_id": tid, "team_key": teams[tid]["team_key"],
                          "score": round(0.35 * st["wins"] / max(1, games_played)
                                         + 0.30 * scoring + 0.20 * ap + 0.15 * form, 4),
                          "all_play": f"{st['ap_w']}-{st['ap_l']}", "all_play_pct": round(ap, 4),
                          "luck_index": st["luck"], "recent_form": round(form, 4),
                          "efficiency": teams[tid]["efficiency"], "regret": teams[tid]["regret"],
                          "prev_rank": prev_rank.get(tid)})
        power.sort(key=lambda r: (-r["score"], -season_tot[r["team_id"]]["pf"]))
        for i, r in enumerate(power):
            r["rank"] = i + 1
            r["movement"] = (r["prev_rank"] - r["rank"]) if r["prev_rank"] else 0
            r["blurb"] = notes.get("blurbs", {}).get(int(r["team_id"]), "")
        for r in power:
            teams[r["team_id"]]["power_rank"] = r["rank"]
            teams[r["team_id"]]["power_move"] = r["movement"]
        prev_rank = {r["team_id"]: r["rank"] for r in power}

        # ── leaderboards ────────────────────────────────────────
        everyone = []
        for tid, t in teams.items():
            everyone += [{**p, "team": t["name"], "team_id": tid, "started": True} for p in t["starters"]]
            everyone += [{**p, "team": t["name"], "team_id": tid, "started": False}
                         for p in t["bench"] if p["slot"] == "BN"]
        for p in everyone:
            p["vs_proj"] = round(p["pts"] - (p["proj"] or 0), 2)
        starters = [p for p in everyone if p["started"]]
        benched = [p for p in everyone if not p["started"]]

        # draft money, season to date (every point the player scored, started or not)
        money = [dict(v, team=teams.get(v["team_id"], {}).get("name", ""))
                 for v in player_season.values() if v.get("cost")]
        for m in money:
            m["per_point"] = round(m["cost"] / m["pts"], 2) if m["pts"] > 0 else None

        # the FAAB audit: what each purchase this week actually returned this week
        where = {}
        for tid, t in teams.items():
            for p in t["starters"]:
                where[norm(p["name"])] = (tid, True, p["pts"], p["slot"])
            for p in t["bench"]:
                where.setdefault(norm(p["name"]), (tid, False, p["pts"], p["slot"]))
        audit = []
        for a in adds:
            if a["week"] != wk:
                continue
            got = where.get(norm(a["player"]))
            audit.append({**a, "team": by_id[a["team_id"]]["name"],
                          "pts": got[2] if got and got[0] == a["team_id"] else None,
                          "started": bool(got and got[0] == a["team_id"] and got[1]),
                          "slot": got[3] if got and got[0] == a["team_id"] else None})
        audit.sort(key=lambda a: (-(a["bid"] or 0), a["when"]))

        out = {
            "season": season, "week": wk,
            "built_at": datetime.now(timezone.utc).isoformat(),
            "league_average": round(sum(scores.values()) / len(scores), 2),
            "median": {
                "value": median,
                "beat": sum(1 for t in teams.values() if t["beat_median"]),
                "closest_above": min((t for t in teams.values() if t["beat_median"]),
                                     key=lambda t: t["vs_median"])["team_id"],
                "closest_below": max((t for t in teams.values() if not t["beat_median"]),
                                     key=lambda t: t["vs_median"])["team_id"],
                "saved_by_median": [t["team_id"] for t in sorted(teams.values(), key=lambda t: -t["points"])
                                    if not t["won"] and t["beat_median"]],
                "sunk_by_median": [t["team_id"] for t in sorted(teams.values(), key=lambda t: -t["points"])
                                   if t["won"] and not t["beat_median"]],
                "sweeps": [t["team_id"] for t in sorted(teams.values(), key=lambda t: -t["points"]) if t["wins"] == 2],
                "swept": [t["team_id"] for t in sorted(teams.values(), key=lambda t: -t["points"]) if t["wins"] == 0],
            },
            "headline": notes.get("headline", f"Week {wk}"),
            "kicker": notes.get("kicker", ""),
            "lede": notes.get("lede", ""),
            "sections": notes.get("sections", {}),
            "awards": notes.get("awards", []),
            "waiver_note": notes.get("waiver_note", ""),
            "teams": sorted(teams.values(), key=lambda t: -t["points"]),
            "power_rankings": power,
            "games": games,
            "top_starts": sorted(starters, key=lambda p: -p["pts"])[:12],
            "worst_starts": sorted([p for p in starters if p["proj"]], key=lambda p: p["vs_proj"])[:12],
            "bench_crimes": sorted(benched, key=lambda p: -p["pts"])[:12],
            # this week, priced (the first week's view)
            "money_pits": sorted([p for p in everyone if p["cost"] and p["cost"] >= 18 and p["started"]],
                                 key=lambda p: p["pts"])[:12],
            "bargains": sorted([p for p in everyone if p["cost"] and p["cost"] <= 3 and p["pts"] >= 12],
                               key=lambda p: -p["pts"])[:12],
            # season to date, priced
            "season_money_pits": sorted([m for m in money if m["cost"] >= 18],
                                        key=lambda m: (m["pts"] / max(1, m["weeks"])))[:10],
            "season_bargains": sorted([m for m in money if m["cost"] <= 3],
                                      key=lambda m: -m["pts"])[:10],
            "faab_audit": audit,
            "free_agents": sorted([p for p in everyone if p["fa"] and p["pts"] >= 8],
                                  key=lambda p: -p["pts"])[:10],
            "slot_averages": {s: {"n": len(v), "avg": round(sum(v) / len(v), 2),
                                  "high": max(v), "low": min(v)}
                              for s in SLOT_ORDER
                              for v in [[p["pts"] for p in starters if p["slot"] == s]] if v},
        }
        # The page never reads the rosters (the raw scrape keeps them), so the published
        # file drops them and ships compact: half the bytes on a phone.
        for t in out["teams"]:
            for k in ("starters", "bench", "best_lineup"):
                t.pop(k, None)
        out.pop("free_agents", None)
        json.dump(out, open(D(f"week{wk}.json"), "w"), ensure_ascii=False, separators=(",", ":"))
        index.append({"week": wk, "headline": out["headline"], "median": median,
                      "high": out["teams"][0]["name"], "high_points": out["teams"][0]["points"]})
        print(f"week {wk}: median {median}, average {out['league_average']}, "
              f"{len(audit)} adds, high {out['teams'][0]['name']} {out['teams'][0]['points']}")

    # ── the test: cumulative records and points against the live scrape ──
    bad = []
    for tid, t in by_id.items():
        st = season_tot[tid]
        if (st["wins"], st["losses"]) != (t["wins"], t["losses"]) or abs(st["pf"] - t["points_for"]) > 0.01:
            bad.append(f"  {t['name']}: built {st['wins']}-{st['losses']} {st['pf']}  "
                       f"yahoo {t['wins']}-{t['losses']} {t['points_for']}")
    if bad:
        print("!! MISMATCH against league.json (stat correction? missing week?):\n" + "\n".join(bad))
    else:
        print(f"checked: all {len(by_id)} season records and points match league.json")

    # ── data/weeks.json and data/current.json ───────────────────
    json.dump({"season": season, "latest": latest, "weeks": index},
              open(D("weeks.json"), "w"), ensure_ascii=False, separators=(",", ":"))

    W = json.load(open(D(f"week{latest}.json")))
    standings = []
    for r in W["power_rankings"]:
        tid = r["team_id"]; t = next(x for x in W["teams"] if x["team_id"] == tid)
        st = season_tot[tid]
        standings.append({
            "team_key": t["team_key"], "team_id": tid, "name": t["name"],
            "manager": t["manager"], "logo": t["logo"],
            "wins": st["wins"], "losses": st["losses"], "ties": 0,
            "win_pct": round(st["wins"] / max(1, st["wins"] + st["losses"]), 3),
            # Two games a week and Yahoo never says which came first, so a streak only
            # exists across whole sweeps: 2-0, 2-0 is W4; anything after a 1-1 is unknowable.
            "streak": streak(st["weekly_w"]),
            "points_for": st["pf"], "points_against": st["pa"],
            "week_points": t["points"], "moves": t["moves"], "faab_balance": t["faab_left"],
            "rank": r["rank"],
        })
    matchups = []
    for wk in weeks:
        Wk = json.load(open(D(f"week{wk}.json")))
        T = {t["team_id"]: t for t in Wk["teams"]}
        for g in Wk["games"]:
            matchups.append({
                "week": wk, "status": "postevent",
                "winner_team_key": T[g["winner"]]["team_key"],
                "teams": [{"team_key": T[x]["team_key"], "name": T[x]["name"],
                           "points": T[x]["points"], "projected": T[x]["projected"]}
                          for x in (g["winner"], g["loser"])],
            })
    cur = {
        "season": season, "week": latest, "status": "final",
        "label": f"Week {latest} · Final", "recap": f"week.html?w={latest}",
        "built_at": W["built_at"], "headline": W["headline"], "kicker": W["kicker"],
        "lede": W["lede"], "league_average": W["league_average"], "median": W["median"]["value"],
        "weeks": weeks, "teams": standings, "power_rankings": W["power_rankings"],
        "matchups": matchups,
    }
    json.dump(cur, open(D("current.json"), "w"), ensure_ascii=False, separators=(",", ":"))
    print(f"wrote current.json (week {latest}) and weeks.json ({len(weeks)} weeks)")


if __name__ == "__main__":
    main()
