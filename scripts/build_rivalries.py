#!/usr/bin/env python3
"""The Rivalry Index: every head-to-head game in league history, by manager.

Inputs
  data/rivalries_yahoo.json   scraped from the league home matchups module, one call per season-week:
                              {"teams": {year: {team_id: name}}, "games": [[year, week, id1, id2, pts1, pts2], ...]}
                              (/<year>/f1/<league_id>?matchup_week=<w>&module=matchups returns JSON)
  data/ledger.json            team name -> manager and final rank, per season
  data/weeks/2026-*.json      the current season, straight from the weekly box scores

Only head-to-head matchups count. The median game (every team also plays the league median since
2023-ish) is nobody's rival. Consolation-bracket games after the regular season are dropped; playoff
games (both teams in the championship bracket) are kept and flagged.

Heat, the number the rivalries are ranked by:
  heat = (meetings + 3 x playoff meetings + 2 x one-score games + 2 x series lead changes)
         x (0.35 + 0.65 x balance)            balance = 1 - |W - L| / games
  A one-score game is decided by fewer than 8 points. Pairs need 8 meetings to be ranked.

  python3 scripts/build_rivalries.py
"""
import collections
import datetime as dt
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
sys.path.insert(0, HERE)
from build_week import MANAGERS, norm  # noqa: E402

CLOSE = 8.0
MIN_GAMES = 8
SKIP = {"Unknown", "Greg (unmatched)", ""}


def key(m):
    return re.sub(r"[^a-z0-9]+", "-", m.lower().replace("(", "").replace(")", "")).strip("-")


def main():
    raw = json.load(open(os.path.join(DATA, "rivalries_yahoo.json")))
    ledger = json.load(open(os.path.join(DATA, "ledger.json")))
    trophy = json.load(open(os.path.join(DATA, "trophy.json")))
    active = {p["manager"] for p in trophy["people"] if p.get("active")}

    # ── season by season: who managed which team id, how long the regular season ran ──
    games = []
    for y_s, tmap in sorted(raw["teams"].items()):
        y = int(y_s)
        rows = ledger.get(y_s, [])
        by_name = {norm(r[0]): r for r in rows}

        def find(name):
            n = norm(name)
            if n in by_name:
                return by_name[n]
            hit = [r for k, r in by_name.items() if k.startswith(n) or n.startswith(k)]
            return hit[0] if len(hit) == 1 else None

        info = {}
        for tid, name in tmap.items():
            r = find(name)
            info[tid] = {"name": name, "manager": r[1] if r else "Unknown", "rank": r[2] if r else 99,
                         "gp": (r[4] + r[5]) if r else 0}
        gp = max((v["gp"] for v in info.values()), default=13)
        reg = gp // 2 if gp > 17 else gp           # the median era doubles every record
        wk = [g for g in raw["games"] if g[0] == y]
        last = max((g[1] for g in wk), default=reg)
        rounds = last - reg
        bracket = 4 if rounds <= 2 else 6 if rounds == 3 else 8
        for _, w, a, b, pa, pb in wk:
            A, B = info.get(str(a)), info.get(str(b))
            if not A or not B or (pa == 0 and pb == 0):
                continue
            kind = "reg"
            if w > reg:
                if A["rank"] > bracket or B["rank"] > bracket:
                    continue                                  # consolation bracket
                ranks = {A["rank"], B["rank"]}
                kind = "final" if w == last and ranks == {1, 2} else "third" if w == last and ranks == {3, 4} else "playoff"
            games.append({"y": y, "w": w, "a": A["manager"], "b": B["manager"], "an": A["name"], "bn": B["name"],
                          "pa": pa, "pb": pb, "kind": kind})

    # ── 2026 from the box scores on file ──
    cur = sorted(glob.glob(os.path.join(DATA, "weeks", "2026-wk*-rosters.json")))
    pairs = json.load(open(os.path.join(DATA, "weeks", "2026-pairings.json")))
    W = max(int(re.search(r"wk(\d+)", f).group(1)) for f in cur) if cur else 0
    wk = json.load(open(os.path.join(DATA, f"week{W}.json"))) if W else {"teams": []}
    names26 = {t["team_id"]: t["name"] for t in wk["teams"]}
    mgr26 = {t["team_id"]: t["manager"] for t in wk["teams"]}
    if "2026" not in raw["teams"]:
        for f in cur:
            w = int(re.search(r"wk(\d+)", f).group(1))
            box = json.load(open(f))
            for a, b in pairs.get(f"2026-wk{w:02d}", []):
                games.append({"y": 2026, "w": w, "a": mgr26[a], "b": mgr26[b], "an": names26[a], "bn": names26[b],
                              "pa": box[a]["total"], "pb": box[b]["total"], "kind": "reg"})

    active |= set(mgr26.values())          # this season's managers, new ones included
    games = [g for g in games if g["a"] not in SKIP and g["b"] not in SKIP and g["a"] != g["b"]]
    games.sort(key=lambda g: (g["y"], g["w"]))

    # ── pair the games up ──
    P = {}
    for g in games:
        a, b = sorted((g["a"], g["b"]))
        pa, pb = (g["pa"], g["pb"]) if g["a"] == a else (g["pb"], g["pa"])
        an, bn = (g["an"], g["bn"]) if g["a"] == a else (g["bn"], g["an"])
        p = P.setdefault((a, b), {"a": a, "b": b, "log": []})
        p["log"].append({"y": g["y"], "w": g["w"], "pa": round(pa, 2), "pb": round(pb, 2), "an": an, "bn": bn,
                         "kind": g["kind"]})

    out_pairs = []
    for (a, b), p in P.items():
        L = p["log"]
        aw = sum(1 for x in L if x["pa"] > x["pb"])
        bw = sum(1 for x in L if x["pb"] > x["pa"])
        t = len(L) - aw - bw
        n = len(L)
        close = sum(1 for x in L if abs(x["pa"] - x["pb"]) < CLOSE)
        po = [x for x in L if x["kind"] != "reg"]
        # lead changes and the current streak
        lead, changes, run = 0, 0, 0
        prev_leader = None
        for x in L:
            lead += 1 if x["pa"] > x["pb"] else -1 if x["pb"] > x["pa"] else 0
            leader = "a" if lead > 0 else "b" if lead < 0 else None
            if leader and prev_leader and leader != prev_leader:
                changes += 1
            if leader:
                prev_leader = leader
        last = None
        for x in reversed(L):
            r = "a" if x["pa"] > x["pb"] else "b" if x["pb"] > x["pa"] else "t"
            if last is None:
                last = r
                run = 1
            elif r == last:
                run += 1
            else:
                break
        balance = 1 - abs(aw - bw) / n
        heat = (n + 3 * len(po) + 2 * close + 2 * changes) * (0.35 + 0.65 * balance)
        big = max(L, key=lambda x: abs(x["pa"] - x["pb"]))
        tight = min(L, key=lambda x: abs(x["pa"] - x["pb"]))
        out_pairs.append({
            "a": a, "b": b, "games": n, "aw": aw, "bw": bw, "t": t,
            "apf": round(sum(x["pa"] for x in L), 2), "bpf": round(sum(x["pb"] for x in L), 2),
            "close": close, "playoff": len(po), "finals": sum(1 for x in po if x["kind"] == "final"),
            "po_aw": sum(1 for x in po if x["pa"] > x["pb"]), "po_bw": sum(1 for x in po if x["pb"] > x["pa"]),
            "changes": changes, "streak": {"who": a if last == "a" else b if last == "b" else None, "n": run},
            "balance": round(balance, 3), "heat": round(heat, 1),
            "active": a in active and b in active,
            "seasons": sorted({x["y"] for x in L}),
            "first": L[0]["y"], "last": L[-1]["y"],
            "biggest": big, "closest": tight, "log": L,
        })
    out_pairs.sort(key=lambda p: -p["heat"])

    # ── managers ──
    M = {}
    for p in out_pairs:
        for me, op, w, l, pf, pa in ((p["a"], p["b"], p["aw"], p["bw"], p["apf"], p["bpf"]),
                                      (p["b"], p["a"], p["bw"], p["aw"], p["bpf"], p["apf"])):
            m = M.setdefault(me, {"manager": me, "key": key(me), "active": me in active, "w": 0, "l": 0, "t": 0,
                                  "pf": 0, "pa": 0, "vs": []})
            m["w"] += w
            m["l"] += l
            m["t"] += p["t"]
            m["pf"] += pf
            m["pa"] += pa
            m["vs"].append({"op": op, "w": w, "l": l, "t": p["t"], "g": p["games"], "pf": round(pf, 1), "pa": round(pa, 1),
                            "po_w": p["po_aw"] if me == p["a"] else p["po_bw"],
                            "po_l": p["po_bw"] if me == p["a"] else p["po_aw"]})
    for m in M.values():
        m["g"] = m["w"] + m["l"] + m["t"]
        m["pct"] = round((m["w"] + 0.5 * m["t"]) / m["g"], 3) if m["g"] else 0
        m["pf"] = round(m["pf"], 1)
        m["pa"] = round(m["pa"], 1)
        m["vs"].sort(key=lambda v: (-v["g"], v["op"]))
        q = [v for v in m["vs"] if v["g"] >= 6]
        m["nemesis"] = min(q, key=lambda v: ((v["w"] - v["l"]), -v["g"]))["op"] if q else None
        m["victim"] = max(q, key=lambda v: ((v["w"] - v["l"]), v["g"]))["op"] if q else None
    managers = sorted(M.values(), key=lambda m: (-m["active"], -m["pct"]))

    # this week's grudge matches: the next week's pairings, from the newsletter
    nxt = []
    for a, b, *_ in (wk.get("newsletter", {}) or {}).get("next", []):
        ma, mb = mgr26.get(str(a)), mgr26.get(str(b))
        if ma and mb:
            nxt.append({"a": str(a), "b": str(b), "ma": ma, "mb": mb, "ta": names26[str(a)], "tb": names26[str(b)]})

    out = {
        "built_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "first": min(g["y"] for g in games), "last": max(g["y"] for g in games), "through_week": W,
        "next_week": W + 1, "totals": {"games": len(games), "playoff": sum(1 for g in games if g["kind"] != "reg"),
                                       "pairs": len(out_pairs), "managers": len(M)},
        "min_games": MIN_GAMES, "close": CLOSE,
        "pairs": out_pairs, "managers": managers, "next": nxt,
        "logos": {t["manager"]: t.get("logo", "") for t in wk["teams"]},
        "teams26": {t["manager"]: t["name"] for t in wk["teams"]},
        "method": {
            "games": "Every head-to-head matchup since 2011, read from Yahoo's weekly matchups for each season plus this season's box scores. The weekly game against the league median is not a rivalry and is left out, and so are consolation-bracket games. Playoff and championship games are in, and flagged.",
            "manager": "Records follow the manager, not the team name, so every rename counts as the same franchise. Teams whose manager is unknown are left out.",
            "heat": f"Heat = (meetings + 3 per playoff meeting + 2 per one-score game + 2 per series lead change) x (0.35 + 0.65 x balance), where balance is 1 when the series is even and 0 when one side has won every game. A one-score game is decided by fewer than {CLOSE:.0f} points. A rivalry needs {MIN_GAMES} meetings to be ranked.",
        },
    }
    dest = os.path.join(DATA, "rivalries.json")
    try:   # leave the file alone when only the timestamp would change (the cron runs daily)
        old = json.load(open(dest))
        old.pop("built_at", None)
        same = old == json.loads(json.dumps({k: v for k, v in out.items() if k != "built_at"}, ensure_ascii=False))
    except (OSError, ValueError):
        same = False
    if not same:
        with open(dest, "w") as f:
            json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(games)} games, {len(out_pairs)} pairs, {len(M)} managers")
    for p in [p for p in out_pairs if p["games"] >= MIN_GAMES][:15]:
        print(f"{p['heat']:6} {p['a']:>14} {p['aw']}-{p['bw']}{'-'+str(p['t']) if p['t'] else ''} {p['b']:<14} g{p['games']} po{p['playoff']} close{p['close']} chg{p['changes']}")


if __name__ == "__main__":
    main()
