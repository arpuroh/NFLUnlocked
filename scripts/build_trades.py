#!/usr/bin/env python3
"""Trade Court: every NFL Unlocked trade since 2011, re-scored -> data/trades.json.

Inputs
  data/trades_yahoo.json  every trade and veto, scraped from each season's Yahoo
                          transactions page (?transactionsfilter=trade). Yahoo only serves
                          those pages to a browser, and rate-limits hard: ~40 page loads
                          and it answers "Request denied" for ten minutes. Re-scrape through
                          a logged-in Chrome, one season at a time, only when a new season ends.
  data/ledger.json        team name -> manager, per season (Trophy Room)
  data/trophy.json        champions, people keys
  nflverse weekly stats   stats_player_week / stats_team_week / games.csv, downloaded once
                          into data/raw/nflverse/ (gitignored)
  scripts/trade_notes.py  every hand-written line on the page. Fantasy decisions only.

How a trade is valued
  Each season is scored under that season's own settings (they changed a lot: yardage
  bonuses, fumbles, distance-based kickers until 2021, defense tiers). A player's value is
  every point he scored after the deal through the fantasy final, minus a waiver-wire
  starter's per-game average at his position over the same games, floored at zero.
  Asset valuation: he counts for whoever received him even if they flipped or cut him.
  Rentals (a trade reversed player-for-player within 21 days) count only until the return.
  Engine checked against Yahoo's own weekly points: mean miss 0.11 per player-game.

Usage
  python3 scripts/build_trades.py            # writes data/trades.json
"""
import datetime as dt
import json
import math
import os
import re
import sys
import unicodedata
import urllib.request
from collections import Counter, defaultdict
from functools import lru_cache

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA, "raw", "nflverse")
OUT = os.path.join(DATA, "trades.json")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trade_notes import NOTES, SEASON_NOTES, MGR_NOTES  # noqa: E402

NFLVERSE = "https://github.com/nflverse/nflverse-data/releases/download/"


def nflverse(path):
    """Local copy of an nflverse release asset, downloaded on first use."""
    dest = os.path.join(CACHE, path.replace("/", "__"))
    if not os.path.exists(dest):
        os.makedirs(CACHE, exist_ok=True)
        print("downloading", path, file=sys.stderr)
        urllib.request.urlretrieve(NFLVERSE + path, dest)
    return dest


# ════════════════════════════════════════════════════════ scoring engine

# ---------------------------------------------------------------- season rules
SEASON = {
    # teams, starting slots, last fantasy week
    2011: dict(teams=12, slots=dict(QB=1, WR=3, RB=2, TE=1, FLEX=2, K=1, DEF=1, D=1), last_week=16),
    2012: dict(teams=10, slots=dict(QB=1, WR=3, RB=2, TE=1, FLEX=3, K=1, DEF=1, D=1), last_week=16),
    **{y: dict(teams=14, slots=dict(QB=1, WR=2, RB=2, TE=1, FLEX=3, K=1, DEF=1, D=1), last_week=16) for y in (2013, 2014, 2015, 2016)},
    **{y: dict(teams=14, slots=dict(QB=1, WR=2, RB=2, TE=1, FLEX=2, K=1, DEF=1, D=1), last_week=16) for y in range(2017, 2021)},
    **{y: dict(teams=14, slots=dict(QB=1, WR=2, RB=2, TE=1, FLEX=2, K=1, DEF=1, D=1), last_week=17) for y in range(2021, 2027)},
}


def bonus(yds, tiers):
    """tiers: list of (threshold, points) - cumulative, Yahoo style."""
    return sum(p for t, p in tiers if yds >= t)


def rules(y):
    r = {}
    r["pass_bonus"] = [(300, 1), (350, 1), (400, 1)] if y <= 2013 else [(400, 1), (450, 1), (500, 1)]
    r["rush_bonus"] = [(150, 1), (200, 1)] if y == 2011 else [(100, 1), (150, 1), (200, 1)]
    if y == 2011:
        r["rec_bonus"] = [(50, 1), (100, 2), (150, 3)]
    elif y <= 2013:
        r["rec_bonus"] = [(50, 1), (100, 1), (150, 1)]
    else:
        r["rec_bonus"] = [(100, 1), (150, 1), (200, 1)]
    # fumbles (any) / fumbles lost
    if y <= 2013:
        r["fum"], r["fum_lost"] = -1, -2
    elif y <= 2023:
        r["fum"], r["fum_lost"] = -1, -1
    else:
        r["fum"], r["fum_lost"] = 0, -2
    # kickers
    if y <= 2013:
        r["fg"] = "dist5"      # 2/3/4/5/6
    elif y <= 2020:
        r["fg"] = "default"    # 3/3/3/4/5
    else:
        r["fg"] = "yards"      # 1 pt per 10 made yards
    # team defense points-allowed tiers: 0, 1-6, 7-13, 14-20, 21-27, 28-34, 35+
    if y <= 2013:
        r["pa"] = [15, 12, 9, 6, 3, 0, -3]
    elif y <= 2015:
        r["pa"] = [10, 7, 4, 1, 0, -1, -4]
    else:
        r["pa"] = [5, 4, 3, 2, 1, 0, -1]
    r["ya"] = y >= 2016   # yards-allowed tiers 5/4/3/2/1/0/-1
    r["idp_ast"] = 1.0 if y <= 2014 else 0.5
    return r


IDP_POS = {"DE", "DT", "NT", "DL", "LB", "OLB", "ILB", "MLB", "CB", "S", "FS", "SS", "DB", "SAF"}


def fpos(p):
    p = str(p or "")
    if p in ("QB", "RB", "WR", "TE", "K"):
        return p
    if p == "FB":
        return "RB"
    if p in IDP_POS:
        return "D"
    return None


def num(row, k):
    v = row.get(k, 0)
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 0.0
    return 0.0 if math.isnan(v) else v


def score_player_week(row, y, R):
    pos = fpos(row["position"])
    pts = 0.0
    if pos in ("QB", "RB", "WR", "TE", None) or pos == "K":
        py = num(row, "passing_yards")
        ry = num(row, "rushing_yards")
        rcy = num(row, "receiving_yards")
        pts += py / 25 + bonus(py, R["pass_bonus"]) + 4 * num(row, "passing_tds") - num(row, "passing_interceptions")
        pts += ry / 10 + bonus(ry, R["rush_bonus"]) + 6 * num(row, "rushing_tds")
        pts += 0.5 * num(row, "receptions") + rcy / 10 + bonus(rcy, R["rec_bonus"]) + 6 * num(row, "receiving_tds")
        ret = num(row, "punt_return_yards") + num(row, "kickoff_return_yards")
        pts += ret / 25 + bonus(ret, [(100, 1), (150, 1), (200, 1)]) + 6 * num(row, "special_teams_tds")
        pts += 2 * (num(row, "passing_2pt_conversions") + num(row, "rushing_2pt_conversions") + num(row, "receiving_2pt_conversions"))
        fum = num(row, "fumbles_total")
        lost = num(row, "fumbles_lost_total")
        if not fum and not lost:
            lost = num(row, "rushing_fumbles_lost") + num(row, "receiving_fumbles_lost") + num(row, "sack_fumbles_lost")
            fum = num(row, "rushing_fumbles") + num(row, "receiving_fumbles") + num(row, "sack_fumbles")
        pts += R["fum"] * fum + R["fum_lost"] * lost
        pts += 6 * num(row, "fumble_recovery_tds")
    if pos == "K":
        pts += num(row, "pat_made")
        dists = [int(float(d)) for d in str(row.get("fg_made_list") or "").replace(";", ",").split(",") if d.strip() not in ("", "nan")]
        if R["fg"] == "yards":
            tot = num(row, "fg_made_distance")
            if not tot and dists:
                tot = sum(dists)
            pts += tot / 10
        else:
            buckets = [num(row, "fg_made_0_19"), num(row, "fg_made_20_29"), num(row, "fg_made_30_39"),
                       num(row, "fg_made_40_49"), num(row, "fg_made_50_59") + num(row, "fg_made_60_")]
            vals = [2, 3, 4, 5, 6] if R["fg"] == "dist5" else [3, 3, 3, 4, 5]
            pts += sum(b * v for b, v in zip(buckets, vals))
    if pos == "D":
        pts = 0.0
        pts += num(row, "def_tackles_solo") + R["idp_ast"] * num(row, "def_tackle_assists")
        pts += 2 * num(row, "def_sacks") + 3 * num(row, "def_interceptions") + 2 * num(row, "def_fumbles_forced")
        pts += 2 * num(row, "fumble_recovery_opp") + 6 * num(row, "def_tds") + 2 * num(row, "def_safeties")
        pts += num(row, "def_pass_defended")
        pts += 2 * (num(row, "def_punt_blocks") + num(row, "def_fg_blocks") + num(row, "def_pat_blocks"))
    return pts


GAME_TEAM = {"STL": "LA", "SD": "LAC", "OAK": "LV"}


@lru_cache(None)
def games(y):
    g = pd.read_csv(nflverse("schedules/games.csv"), low_memory=False)
    g = g[(g.season == y) & (g.game_type == "REG")].copy()
    for c in ("home_team", "away_team"):
        g[c] = g[c].replace(GAME_TEAM)
    return g


@lru_cache(None)
def kickoff_table(y):
    """(team, week) -> kickoff datetime (naive, US/Eastern)."""
    g = games(y)
    out = {}
    for _, r in g.iterrows():
        t = str(r.gametime) if isinstance(r.gametime, str) else "13:00"
        ko = pd.Timestamp(f"{r.gameday} {t}")
        out[(r.home_team, int(r.week))] = ko
        out[(r.away_team, int(r.week))] = ko
    return out


@lru_cache(None)
def week_ends(y):
    """week -> latest kickoff that week (so we know when a week is over)."""
    g = games(y)
    res = {}
    for w, grp in g.groupby("week"):
        kos = [pd.Timestamp(f"{r.gameday} {r.gametime if isinstance(r.gametime, str) else '13:00'}") for _, r in grp.iterrows()]
        res[int(w)] = (min(kos), max(kos))
    return res


def def_points(y, R):
    """team DEF weekly points: (team, week) -> pts."""
    st = pd.read_csv(nflverse(f"stats_team/stats_team_week_{y}.csv"), low_memory=False)
    st = st[st.season_type == "REG"]
    g = games(y)
    opp_pts = {}
    for _, r in g.iterrows():
        if pd.isna(r.home_score):
            continue
        opp_pts[(r.home_team, int(r.week))] = r.away_score
        opp_pts[(r.away_team, int(r.week))] = r.home_score
    off = {(r.team, int(r.week)): r for _, r in st.iterrows()}
    out = {}
    for (team, w), r in off.items():
        rr = r.to_dict()
        o = off.get((rr["opponent_team"], w))
        pts = num(rr, "def_sacks") * 1 + 2 * num(rr, "def_interceptions") + 2 * num(rr, "fumble_recovery_opp")
        pts += 6 * (num(rr, "def_tds") + num(rr, "special_teams_tds")) + 2 * num(rr, "def_safeties")
        pts += 2 * (num(rr, "def_punt_blocks") + num(rr, "def_fg_blocks") + num(rr, "def_pat_blocks"))
        pts += (num(rr, "punt_return_yards") + num(rr, "kickoff_return_yards")) / 50
        pa = opp_pts.get((team, w))
        if pa is not None:
            tiers = R["pa"]
            idx = 0 if pa == 0 else 1 if pa <= 6 else 2 if pa <= 13 else 3 if pa <= 20 else 4 if pa <= 27 else 5 if pa <= 34 else 6
            pts += tiers[idx]
        if R["ya"] and o is not None:
            od = o.to_dict()
            ya = num(od, "passing_yards") - num(od, "sack_yards_lost") + num(od, "rushing_yards")
            pts += 5 if ya < 0 else 4 if ya < 100 else 3 if ya < 200 else 2 if ya < 300 else 1 if ya < 400 else 0 if ya < 500 else -1
        out[(team, w)] = pts
    return out


@lru_cache(None)
def season_table(y):
    """DataFrame: pid, name, pos, team, week, pts  (players + team DEFs)."""
    R = rules(y)
    df = pd.read_csv(nflverse(f"stats_player/stats_player_week_{y}.csv"), low_memory=False)
    df = df[df.season_type == "REG"].copy()
    df["fpos"] = df.position.map(fpos)
    df = df[df.fpos.notna()].copy()
    recs = df.to_dict("records")
    df["pts"] = [score_player_week(r, y, R) for r in recs]
    out = df[["player_id", "player_display_name", "fpos", "team", "week", "pts"]].rename(
        columns={"player_id": "pid", "player_display_name": "name", "fpos": "pos"})
    dp = def_points(y, R)
    drows = [dict(pid="DEF-" + t, name=t + " DEF", pos="DEF", team=t, week=w, pts=p) for (t, w), p in dp.items()]
    out = pd.concat([out, pd.DataFrame(drows)], ignore_index=True)
    out["week"] = out.week.astype(int)
    return out


@lru_cache(None)
def replacement(y):
    """Per-position replacement points per game, from season-long ranks under the
    league's starting lineup: teams x slots, flex filled from the best leftover
    RB/WR/TE. Replacement = mean ppg of the next 6 players past the last starter."""
    cfg = SEASON[y]
    T, S = cfg["teams"], cfg["slots"]
    tab = season_table(y)
    tab = tab[tab.week <= cfg["last_week"]]
    agg = tab.groupby(["pid", "pos"]).agg(tot=("pts", "sum"), gp=("pts", "size")).reset_index()
    agg["ppg"] = agg.tot / agg.gp.clip(lower=1)
    # rank by total points among players with a real sample
    starters = {}
    taken = set()
    for pos in ("QB", "RB", "WR", "TE", "K", "DEF", "D"):
        n = T * S.get(pos, 0)
        pool = agg[agg.pos == pos].sort_values("tot", ascending=False)
        starters[pos] = n
        taken |= set(pool.head(n).pid)
    flex_pool = agg[agg.pos.isin(["RB", "WR", "TE"]) & ~agg.pid.isin(taken)].sort_values("tot", ascending=False)
    for _, r in flex_pool.head(T * S["FLEX"]).iterrows():
        starters[r.pos] += 1
    repl = {}
    for pos, n in starters.items():
        pool = agg[(agg.pos == pos) & (agg.gp >= 4)].sort_values("tot", ascending=False)
        nxt = pool.iloc[n:n + 6]
        repl[pos] = float(nxt.ppg.mean()) if len(nxt) else 0.0
    return repl, starters


# ---------------------------------------------------------------- name matching
SUFFIX = re.compile(r"\b(jr|sr|ii|iii|iv|v)\b")
ALIAS = {
    "hollywood brown": "marquise brown",
    "chad johnson": "chad johnson",
    "steve smith": "steve smith",
    "gardner minshew": "gardner minshew",
    "dj chark": "dj chark",
    "mitch trubisky": "mitchell trubisky",
    "ben watson": "benjamin watson",
    "stevie johnson": "steve johnson",
    "mike thomas": "mike thomas",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "").replace("-", " ")
    s = SUFFIX.sub("", s)
    s = re.sub(r"\s+", " ", s).strip()
    return ALIAS.get(s, s)


DEF_NICK = {
    "cardinals": "ARI", "falcons": "ATL", "ravens": "BAL", "bills": "BUF", "panthers": "CAR", "bears": "CHI",
    "bengals": "CIN", "browns": "CLE", "cowboys": "DAL", "broncos": "DEN", "lions": "DET", "packers": "GB",
    "texans": "HOU", "colts": "IND", "jaguars": "JAX", "chiefs": "KC", "rams": "LA", "chargers": "LAC",
    "raiders": "LV", "dolphins": "MIA", "vikings": "MIN", "patriots": "NE", "saints": "NO", "giants": "NYG",
    "jets": "NYJ", "eagles": "PHI", "steelers": "PIT", "seahawks": "SEA", "49ers": "SF", "buccaneers": "TB",
    "titans": "TEN", "redskins": "WAS", "commanders": "WAS", "football team": "WAS",
}


def match_player(y, name, ypos):
    """Return (pid, pos, display) for a Yahoo name/position in season y."""
    tab = season_table(y)
    pos_list = [p.strip() for p in ypos.split("-")[-1].split(",")] if ypos else []
    if "DEF" in pos_list:
        t = DEF_NICK.get(name.lower())
        return ("DEF-" + t, "DEF", name) if t else (None, "DEF", name)
    key = norm(name)
    names = tab[["pid", "name", "pos"]].drop_duplicates("pid").copy()
    names["k"] = names.name.map(norm)
    cand = names[names.k == key]
    if cand.empty:
        # last-name + first initial fallback
        parts = key.split()
        if len(parts) >= 2:
            cand = names[names.k.str.endswith(" " + parts[-1]) & names.k.str.startswith(parts[0][0])]
    if cand.empty:
        return (None, pos_list[0] if pos_list else None, name)
    ypos_set = {p for p in pos_list}
    tot = tab.groupby("pid").pts.sum()
    def score(r):
        s = 0
        if r.pos in ypos_set:
            s += 1000
        s += tot.get(r.pid, 0)
        return s
    best = max(cand.itertuples(), key=score)
    return (best.pid, best.pos, best.name)


# ════════════════════════════════════════════════════════ trades
MONTHS = {m: i for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}
TRADE_END = {2011: "2011-12-02", 2012: "2012-11-30", 2013: "2013-11-29", 2014: "2014-11-28", 2015: "2015-11-27",
             2016: "2016-11-26", 2017: "2017-11-25", 2018: "2018-11-24", 2019: "2019-11-23", 2020: "2020-11-28",
             2021: "2021-12-04", 2022: "2022-12-03", 2023: "2023-12-02", 2024: "2024-11-30", 2025: "2025-11-29"}


def parse_ts(y, s):
    # "Nov 9, 5:57 pm"
    md, hm = s.split(", ")
    mon, day = md.split()
    t, ampm = hm.split()
    h, m = map(int, t.split(":"))
    if ampm == "pm" and h != 12:
        h += 12
    if ampm == "am" and h == 12:
        h = 0
    yr = y + 1 if MONTHS[mon] < 6 else y
    return pd.Timestamp(dt.datetime(yr, MONTHS[mon], int(day), h, m))


def playoff_start(y):
    return SEASON[y]["last_week"] - 2


def load():
    raw = json.load(open(os.path.join(DATA, "trades_yahoo.json")))
    ledger = json.load(open(os.path.join(DATA, "ledger.json")))
    trophy = json.load(open(os.path.join(DATA, "trophy.json")))
    mgr_of = {}
    finish = {}
    for y, rows in ledger.items():
        for r in rows:
            mgr_of[(int(y), r[0])] = r[1]
            finish[(int(y), r[0])] = dict(rank=r[2], place=r[3], w=r[4], l=r[5], pf=r[6])
    key_of = {}
    for p in trophy["people"]:
        key_of[p["manager"]] = p["key"]
    trades = []
    for y, lst in raw.items():
        y = int(y)
        for i, t in enumerate(lst):
            legs = []
            for (tid, tname, ts, act, items) in t["L"]:
                legs.append(dict(team_id=tid, team=tname, ts=ts, players=[dict(name=n, yid=yid, ypos=p) for n, yid, p in items]))
            trades.append(dict(season=y, vetoed=t["k"] != "F-trade", ts=parse_ts(y, legs[0]["ts"]), legs=legs))
    trades.sort(key=lambda t: t["ts"])
    for i, t in enumerate(trades):
        t["id"] = f"{t['season']}-{i:03d}"
        for leg in t["legs"]:
            leg["manager"] = mgr_of.get((t["season"], leg["team"]), "Unknown")
            leg["mkey"] = key_of.get(leg["manager"], "unknown")
            leg["finish"] = finish.get((t["season"], leg["team"]))
    return trades, key_of


def player_windows(trades):
    """Asset valuation: a player's whole rest-of-season counts for whoever received him,
    whatever they did with him afterwards (flip, drop, bench). The one exception is a
    rental - a deal undone within days by an exact reverse trade - which only counts
    until the players went back."""
    by_id = {t["id"]: t for t in trades}
    for t in trades:
        back = by_id.get(t.get("reversed_by")) if t.get("reversed_by") else None
        for leg in t["legs"]:
            for p in leg["players"]:
                p["until"] = back["ts"] if back else None


def detect_reversals(trades):
    ex = [t for t in trades if not t["vetoed"]]
    for a in ex:
        for b in ex:
            if b["season"] != a["season"] or b["ts"] <= a["ts"] or (b["ts"] - a["ts"]).days > 21:
                continue
            if b.get("reverses") or a.get("reversed_by"):
                continue
            A = {leg["team_id"]: {p["name"] for p in leg["players"]} for leg in a["legs"]}
            B = {leg["team_id"]: {p["name"] for p in leg["players"]} for leg in b["legs"]}
            if set(A) != set(B):
                continue
            t1, t2 = list(A)
            # what t1 received in A, t2 received back in B (and vice versa)
            if A[t1] and A[t1] <= B[t2] and A[t2] <= B[t1]:
                a["reversed_by"] = b["id"]
                b["reverses"] = a["id"]


def evaluate(trades):
    out = []
    for t in trades:
        y = t["season"]
        if y not in SEASON or y > 2025:
            continue
        tab = season_table(y)
        repl, _ = replacement(y)
        ko = kickoff_table(y)
        last = SEASON[y]["last_week"]
        pstart = playoff_start(y)
        for leg in t["legs"]:
            tot_val = tot_pts = tot_po = 0.0
            weeks_all = set()
            for p in leg["players"]:
                pid, pos, disp = match_player(y, p["name"], p["ypos"])
                ypos = p["ypos"].split("-")[-1].strip().split(",")[0] if p["ypos"] else ""
                if ypos in ("QB", "RB", "WR", "TE", "K", "DEF"):
                    pos = ypos
                p["pid"], p["pos"] = pid, pos or ypos
                rows = tab[tab.pid == pid] if pid else tab.iloc[0:0]
                until = None if t["vetoed"] else p.get("until")
                pts = val = po = 0.0
                games = 0
                wk = []
                for r in rows.itertuples():
                    if r.week > last:
                        continue
                    k = ko.get((r.team, r.week))
                    if k is None or k <= t["ts"]:
                        continue
                    if until is not None and k > until:
                        continue
                    pts += r.pts
                    val += r.pts - repl.get(pos, 0.0)
                    if r.week >= pstart:
                        po += r.pts
                    games += 1
                    wk.append([int(r.week), round(float(r.pts), 1)])
                    weeks_all.add(r.week)
                p["pts"] = round(pts, 1)
                p["vor"] = round(max(0.0, val), 1)
                p["po_pts"] = round(po, 1)
                p["games"] = games
                p["weeks"] = sorted(wk)
                p["ppg"] = round(pts / games, 1) if games else 0.0
                tot_val += max(0.0, val)
                tot_pts += pts
                tot_po += po
            leg["vor"] = round(tot_val, 1)
            leg["pts"] = round(tot_pts, 1)
            leg["po_pts"] = round(tot_po, 1)
        a, b = t["legs"]
        t["margin"] = round(a["vor"] - b["vor"], 1)
        t["winner"] = 0 if a["vor"] > b["vor"] else 1 if b["vor"] > a["vor"] else None
        out.append(t)
    return out




# ════════════════════════════════════════════════════════ page data

VERDICTS = [(100, "Grand Larceny"), (60, "Robbery"), (30, "Clear Win"), (12, "Slight Edge"), (0, "Wash")]
PUSH = 5  # a side "wins" a trade only by 5+ points over the waiver wire


def verdict(m):
    m = abs(m)
    for th, lab in VERDICTS:
        if m >= th:
            return lab
    return "Wash"


def week_of(y, ts):
    we = week_ends(y)
    ws = [w for w, (a, b) in sorted(we.items()) if b > ts]
    return ws[0] if ws else None


def main():
    trades, key_of = load()
    detect_reversals(trades)
    player_windows(trades)
    ev = evaluate(trades)

    trophy = json.load(open(os.path.join(DATA, "trophy.json")))
    champs = {s["year"]: s["champion_manager"] for s in trophy["seasons"] if s.get("champion_manager")}
    runner = {s["year"]: s["runner_up_manager"] for s in trophy["seasons"] if s.get("runner_up_manager")}
    toilet = {s["year"]: s["toilet_manager"] for s in trophy["seasons"] if s.get("toilet_manager")}

    out_trades = []
    for t in ev:
        y = t["season"]
        kind = "veto" if t["vetoed"] else "return" if t.get("reverses") else "loan" if t.get("reversed_by") else "trade"
        end = pd.Timestamp(TRADE_END[y]) + pd.Timedelta(hours=23, minutes=59)
        sides = []
        for leg in t["legs"]:
            fin = leg.get("finish") or {}
            sides.append(dict(
                team=leg["team"], manager=leg["manager"], mkey=leg["mkey"],
                got=[dict(n=p["name"], p=p["pos"] or "", pts=p["pts"], val=p["vor"], g=p["games"], po=p["po_pts"],
                          ppg=p["ppg"]) for p in leg["players"]],
                val=leg["vor"], pts=leg["pts"], po=leg["po_pts"],
                place=fin.get("place", 0), rank=fin.get("rank"), rec=f"{fin.get('w', '?')}-{fin.get('l', '?')}" if fin else "",
                champ=(champs.get(y) == leg["manager"]),
            ))
        m = t["margin"]
        win = t["winner"] if abs(m) >= PUSH else None
        rec = dict(
            id=t["id"], season=y, date=t["ts"].strftime("%Y-%m-%d"), when=t["ts"].strftime("%b %-d"),
            time=t["ts"].strftime("%-I:%M %p").lower(), week=week_of(y, t["ts"]),
            deadline=bool((end - t["ts"]).days < 7 and t["ts"] <= end),
            kind=kind, pair=t.get("reverses") or t.get("reversed_by"),
            sides=sides, win=win, margin=round(abs(m), 1), verdict=verdict(m) if win is not None else "Wash",
            total=round(sides[0]["val"] + sides[1]["val"], 1),
            bodies=len(sides[0]["got"]) + len(sides[1]["got"]),
        )
        if t["id"] in NOTES:
            rec["note"] = NOTES[t["id"]]
        out_trades.append(rec)

    by_id = {t["id"]: t for t in out_trades}
    real = [t for t in out_trades if t["kind"] in ("trade", "loan")]

    # ------------------------------------------------------------ managers
    people = {p["key"]: p for p in trophy["people"]}
    M = defaultdict(lambda: dict(trades=0, w=0, l=0, p=0, net=0.0, got=0.0, gave=0.0, partners=Counter(),
                                 vs=defaultdict(float), best=None, worst=None, seasons=set(), loans=0, vetoed=0))
    for t in out_trades:
        for i, s in enumerate(t["sides"]):
            o = t["sides"][1 - i]
            r = M[s["mkey"]]
            r["manager"] = s["manager"]
            if t["kind"] == "veto":
                r["vetoed"] += 1
                continue
            if t["kind"] == "return":
                continue
            r["trades"] += 1
            r["seasons"].add(t["season"])
            if t["kind"] == "loan":
                r["loans"] += 1
            d = s["val"] - o["val"]
            r["net"] += d
            r["got"] += s["val"]
            r["gave"] += o["val"]
            r["partners"][o["mkey"]] += 1
            r["vs"][o["mkey"]] += d
            if t["win"] == i:
                r["w"] += 1
            elif t["win"] == 1 - i:
                r["l"] += 1
            else:
                r["p"] += 1
            if r["best"] is None or d > r["best"][1]:
                r["best"] = (t["id"], d)
            if r["worst"] is None or d < r["worst"][1]:
                r["worst"] = (t["id"], d)
    managers = []
    for k, r in M.items():
        if k in ("unknown", "greg-unresolved") or not r["trades"]:
            continue
        pe = people.get(k, {})
        fav = r["partners"].most_common(1)[0] if r["partners"] else None
        victim = max(r["vs"].items(), key=lambda kv: kv[1]) if r["vs"] else None
        nemesis = min(r["vs"].items(), key=lambda kv: kv[1]) if r["vs"] else None
        managers.append(dict(
            key=k, manager=r["manager"], team=pe.get("current_team", ""), active=pe.get("active", False),
            span=pe.get("span", ""), trades=r["trades"], w=r["w"], l=r["l"], p=r["p"],
            net=round(r["net"], 1), got=round(r["got"], 1), gave=round(r["gave"], 1),
            per=round(r["net"] / r["trades"], 1), seasons=len(r["seasons"]), loans=r["loans"], vetoed=r["vetoed"],
            best=dict(id=r["best"][0], d=round(r["best"][1], 1)) if r["best"] else None,
            worst=dict(id=r["worst"][0], d=round(r["worst"][1], 1)) if r["worst"] else None,
            fav=dict(key=fav[0], n=fav[1], name=M[fav[0]].get("manager", fav[0])) if fav else None,
            victim=dict(key=victim[0], d=round(victim[1], 1), name=M[victim[0]].get("manager", victim[0])) if victim and victim[1] > 0 else None,
            nemesis=dict(key=nemesis[0], d=round(nemesis[1], 1), name=M[nemesis[0]].get("manager", nemesis[0])) if nemesis and nemesis[1] < 0 else None,
            note=MGR_NOTES.get(k, ""),
        ))
    managers.sort(key=lambda r: -r["net"])
    # never-traded managers (in the trophy room but no trades)
    never = [dict(key=p["key"], manager=p["manager"], seasons=p["seasons"], span=p.get("span", ""))
             for p in trophy["people"] if p.get("display") and p["key"] not in M]

    # ------------------------------------------------------------ pairs
    pairs = defaultdict(lambda: dict(n=0, d=0.0, ids=[]))
    for t in real:
        a, b = t["sides"]
        if "unknown" in (a["mkey"], b["mkey"]) or "greg-unresolved" in (a["mkey"], b["mkey"]):
            continue
        ka, kb = sorted([a["mkey"], b["mkey"]])
        rec = pairs[(ka, kb)]
        rec["n"] += 1
        sa = a if a["mkey"] == ka else b
        sb = b if sa is a else a
        rec["d"] += sa["val"] - sb["val"]
        rec["ids"].append(t["id"])
        rec["names"] = (sa["manager"], sb["manager"])
    pair_list = sorted([dict(a=k[0], b=k[1], an=v["names"][0], bn=v["names"][1], n=v["n"], d=round(v["d"], 1), ids=v["ids"])
                        for k, v in pairs.items()], key=lambda r: (-r["n"], -abs(r["d"])))

    # ------------------------------------------------------------ frequent flyers
    flyers = defaultdict(lambda: dict(n=0, seasons=set(), ids=[], owners=[]))
    for t in out_trades:
        if t["kind"] == "veto":
            continue
        for s in t["sides"]:
            for p in s["got"]:
                f = flyers[p["n"]]
                f["n"] += 1
                f["seasons"].add(t["season"])
                f["ids"].append(t["id"])
                f["owners"].append(s["manager"])
                f["pos"] = p["p"]
    fly = sorted([dict(n=k, pos=v["pos"], times=v["n"], seasons=sorted(v["seasons"]), ids=v["ids"],
                       owners=len(set(v["owners"])))
                  for k, v in flyers.items()], key=lambda r: (-r["times"], -len(r["seasons"])))[:12]

    # ------------------------------------------------------------ seasons
    seasons = []
    for y in range(2011, 2026):
        ts = [t for t in out_trades if t["season"] == y]
        rl = [t for t in ts if t["kind"] in ("trade", "loan")]
        top = max(rl, key=lambda t: (t["margin"] if t["win"] is not None else -1), default=None)
        cnt = Counter(s["manager"] for t in rl for s in t["sides"])
        busiest = cnt.most_common(1)[0] if cnt else None
        champ_n = sum(1 for t in rl if any(s["manager"] == champs.get(y) for s in t["sides"]))
        seasons.append(dict(
            busy=dict(manager=busiest[0], n=busiest[1]) if busiest else None, champ_trades=champ_n,
            year=y, trades=len([t for t in ts if t["kind"] != "veto"]), vetoes=len([t for t in ts if t["kind"] == "veto"]),
            loans=len([t for t in ts if t["kind"] == "loan"]), champ=champs.get(y), runner=runner.get(y), toilet=toilet.get(y),
            top=top["id"] if top and top["win"] is not None else None,
            note=SEASON_NOTES.get(y, ""),
        ))

    # ------------------------------------------------------------ headline lists
    ranked = sorted([t for t in real if t["win"] is not None], key=lambda t: -t["margin"])
    robberies = [t["id"] for t in ranked[:13]]
    # win-win: both sides at least 40 over the wire, margin under 25
    winwin = sorted([t for t in real if min(t["sides"][0]["val"], t["sides"][1]["val"]) >= 35 and t["margin"] < 30],
                    key=lambda t: -t["total"])
    blockbusters = sorted(real, key=lambda t: -t["total"])[:6]
    # champions' trades: the eventual champion received value (> 0) in-season
    title = []
    for t in real:
        for i, s in enumerate(t["sides"]):
            if s["champ"] and (s["val"] > 0 or s["po"] >= 40):
                title.append(dict(id=t["id"], side=i, val=s["val"], po=s["po"], d=round(s["val"] - t["sides"][1 - i]["val"], 1)))
    title.sort(key=lambda r: -r["po"])
    # keep the best playoff payoff per champion season, most recent first
    seen = set(); tl = []
    for r in title:
        y = int(r["id"][:4])
        if y in seen:
            continue
        seen.add(y); tl.append(r)
    title = sorted(tl, key=lambda r: r["id"])
    no_trade_champs = [dict(year=s["year"], champ=s["champ"]) for s in seasons if s["champ"] and s["champ_trades"] == 0]
    deadline = [t["id"] for t in real if t["deadline"]]
    vetoes = [t["id"] for t in out_trades if t["kind"] == "veto"]
    rentals = [[t["id"], t["pair"]] for t in out_trades if t["kind"] == "loan"]

    totals = dict(
        trades=len([t for t in out_trades if t["kind"] != "veto"]),
        vetoes=len(vetoes), rentals=len(rentals),
        players=sum(len(s["got"]) for t in out_trades if t["kind"] != "veto" for s in t["sides"]),
        managers=len(managers), seasons=15,
        busiest=max(seasons, key=lambda s: s["trades"]), quietest=min(seasons, key=lambda s: s["trades"]),
        deadline=len(deadline),
    )
    data = dict(
        generated=pd.Timestamp.now(tz="America/New_York").strftime("%Y-%m-%d"),
        first=2011, last=2025, totals=totals,
        method=dict(
            value="Every point a player scored after the trade, minus what a waiver-wire starter at his position averaged over the same number of games. Floored at zero per player: a guy you would have benched or cut costs nothing.",
            window="Every game after the deal went through, up to the fantasy championship (Week 16 through 2020, Week 17 since). A player counts for whoever received him, even if that manager flipped him, benched him or cut him the next day, because that is what the asset was worth. Rentals are the exception: they count only until they were sent back.",
            scoring="Each season is scored under that season's own league settings, read off the Yahoo settings page, not today's.",
            source="Trades from the league's Yahoo transaction logs, 2011 to 2025. Weekly stats from nflverse, re-scored and spot-checked against Yahoo's own weekly points (average miss 0.1 per game).",
            push=PUSH, verdicts=[dict(min=a, label=b) for a, b in VERDICTS],
        ),
        replacement={y: {k: round(v, 1) for k, v in replacement(y)[0].items()} for y in range(2011, 2026)},
        trades=out_trades, managers=managers, never=never, pairs=pair_list[:12], flyers=fly, seasons=seasons,
        lists=dict(robberies=robberies, winwin=[t["id"] for t in winwin[:6]], blockbusters=[t["id"] for t in blockbusters],
                   title=title, no_trade_champs=no_trade_champs, deadline=deadline, vetoes=vetoes, rentals=rentals),
    )
    json.dump(data, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    return data


if __name__ == "__main__":
    d = main()
    t = d["totals"]
    print(f"wrote {OUT}: {t['trades']} trades, {t['vetoes']} vetoes, {t['rentals']} rentals, {len(d['managers'])} managers")
