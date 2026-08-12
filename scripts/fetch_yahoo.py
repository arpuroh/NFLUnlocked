#!/usr/bin/env python3
"""
NFL Unlocked — Yahoo Fantasy data fetcher.

Pulls league standings, matchups, transactions, and FAAB data from the
Yahoo Fantasy Sports API using a long-lived refresh token, computes power
rankings, and writes everything to data/league.json for the site.

Required environment variables:
  YAHOO_CLIENT_ID      Yahoo developer app client id
  YAHOO_CLIENT_SECRET  Yahoo developer app client secret
  YAHOO_REFRESH_TOKEN  Refresh token from the one-time OAuth flow (site /setup page)

Optional:
  LEAGUE_ID            Yahoo league id (default: 675504)
  GAME_CODE            Yahoo game code (default: nfl → resolves to current season)
"""

import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LEAGUE_ID = os.environ.get("LEAGUE_ID", "675504")
GAME_CODE = os.environ.get("GAME_CODE", "nfl")
LEAGUE_KEY = f"{GAME_CODE}.l.{LEAGUE_ID}"

API_BASE = "https://fantasysports.yahooapis.com/fantasy/v2"
TOKEN_URL = "https://api.login.yahoo.com/oauth2/get_token"

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"


# ---------------------------------------------------------------- auth

def get_access_token() -> str:
    cid = os.environ.get("YAHOO_CLIENT_ID")
    secret = os.environ.get("YAHOO_CLIENT_SECRET")
    refresh = os.environ.get("YAHOO_REFRESH_TOKEN")
    if not all([cid, secret, refresh]):
        sys.exit("Missing YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET / YAHOO_REFRESH_TOKEN env vars.")

    body = urllib.parse.urlencode({
        "client_id": cid,
        "client_secret": secret,
        "refresh_token": refresh,
        "grant_type": "refresh_token",
        "redirect_uri": "oob",
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    with urllib.request.urlopen(req) as resp:
        tok = json.loads(resp.read().decode())
    return tok["access_token"]


def api_get(token: str, path: str, retries: int = 3) -> dict:
    url = f"{API_BASE}/{path}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}format=json"
    for attempt in range(retries):
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            print(f"  retrying {path} after error: {e}")
            time.sleep(2 * (attempt + 1))
    return {}


# ------------------------------------------------- yahoo JSON helpers
# Yahoo's JSON is XML translated literally: lists of single-key dicts,
# dicts keyed by "0","1",... with a "count". These helpers flatten it.

def merge_dicts(seq) -> dict:
    """Merge a Yahoo list-of-dicts (or nested lists) into one dict."""
    out = {}
    if isinstance(seq, dict):
        return seq
    if not isinstance(seq, list):
        return out
    for item in seq:
        if isinstance(item, dict):
            out.update(item)
        elif isinstance(item, list):
            out.update(merge_dicts(item))
    return out


def indexed_items(container: dict) -> list:
    """Yield values of a {'0': ..., '1': ..., 'count': n} dict in order."""
    if not isinstance(container, dict):
        return []
    items = []
    for k in sorted(container.keys(), key=lambda x: int(x) if str(x).isdigit() else 10**9):
        if str(k).isdigit():
            items.append(container[k])
    return items


def safe_float(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def safe_int(v, default=0):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return default


# ------------------------------------------------------------ parsing

def parse_team(team_node) -> dict:
    """team_node is Yahoo's team: a list whose first element is the meta list."""
    if isinstance(team_node, dict):
        team_node = team_node.get("team", team_node)
    meta = merge_dicts(team_node[0] if isinstance(team_node, list) else team_node)
    extras = merge_dicts(team_node[1:]) if isinstance(team_node, list) and len(team_node) > 1 else {}

    managers = meta.get("managers", [])
    mgr_names = []
    for m in managers if isinstance(managers, list) else indexed_items(managers):
        mgr = m.get("manager", {}) if isinstance(m, dict) else {}
        if mgr.get("nickname"):
            mgr_names.append(mgr["nickname"])

    logos = meta.get("team_logos", [])
    logo = ""
    if isinstance(logos, list) and logos:
        logo = logos[0].get("team_logo", {}).get("url", "")

    standings = extras.get("team_standings", {}) or meta.get("team_standings", {})
    outcomes = standings.get("outcome_totals", {}) if isinstance(standings, dict) else {}
    streak = standings.get("streak", {}) if isinstance(standings, dict) else {}

    points = extras.get("team_points", {}) or meta.get("team_points", {})

    return {
        "team_key": meta.get("team_key", ""),
        "team_id": meta.get("team_id", ""),
        "name": meta.get("name", "Unknown"),
        "manager": " & ".join(mgr_names) or "Unknown",
        "logo": logo,
        "moves": safe_int(meta.get("number_of_moves")),
        "trades": safe_int(meta.get("number_of_trades")),
        "faab_balance": safe_int(meta.get("faab_balance"), default=-1),
        "clinched_playoffs": bool(safe_int(meta.get("clinched_playoffs"))),
        "rank": safe_int(standings.get("rank")) if isinstance(standings, dict) else 0,
        "wins": safe_int(outcomes.get("wins")),
        "losses": safe_int(outcomes.get("losses")),
        "ties": safe_int(outcomes.get("ties")),
        "win_pct": safe_float(outcomes.get("percentage")),
        "streak": f"{streak.get('type', '')[:1].upper()}{streak.get('value', '')}" if streak else "",
        "points_for": safe_float(standings.get("points_for")) if isinstance(standings, dict) else 0.0,
        "points_against": safe_float(standings.get("points_against")) if isinstance(standings, dict) else 0.0,
        "week_points": safe_float(points.get("total")) if isinstance(points, dict) else 0.0,
    }


def parse_league_meta(league_list) -> dict:
    meta = merge_dicts(league_list[0] if isinstance(league_list, list) else league_list)
    return {
        "league_key": meta.get("league_key", LEAGUE_KEY),
        "name": meta.get("name", "NFL Unlocked"),
        "season": meta.get("season", ""),
        "current_week": safe_int(meta.get("current_week"), 1),
        "start_week": safe_int(meta.get("start_week"), 1),
        "end_week": safe_int(meta.get("end_week"), 17),
        "num_teams": safe_int(meta.get("num_teams")),
        "url": meta.get("url", ""),
        "logo": meta.get("logo_url", "") or "",
        "is_finished": bool(safe_int(meta.get("is_finished"))),
    }


def parse_standings(payload) -> tuple[dict, list]:
    league = payload["fantasy_content"]["league"]
    meta = parse_league_meta(league)
    standings = merge_dicts(league[1:]).get("standings", [])
    teams_container = merge_dicts(standings).get("teams", {})
    teams = [parse_team(t.get("team", t)) for t in indexed_items(teams_container)]
    return meta, teams


def parse_scoreboard(payload) -> list:
    league = payload["fantasy_content"]["league"]
    sb = merge_dicts(league[1:]).get("scoreboard", {})
    sb = merge_dicts(sb) if isinstance(sb, list) else sb
    matchups_container = sb.get("0", sb).get("matchups", {}) if "0" in sb else sb.get("matchups", {})
    matchups = []
    for m in indexed_items(matchups_container):
        mu = merge_dicts(m.get("matchup", m))
        teams_container = mu.get("0", {}).get("teams", {}) or mu.get("teams", {})
        sides = []
        for t in indexed_items(teams_container):
            team = parse_team(t.get("team", t))
            sides.append({
                "team_key": team["team_key"],
                "name": team["name"],
                "points": team["week_points"],
            })
        if len(sides) == 2:
            matchups.append({
                "week": safe_int(mu.get("week")),
                "status": mu.get("status", ""),
                "is_playoffs": bool(safe_int(mu.get("is_playoffs"))),
                "winner_team_key": mu.get("winner_team_key", ""),
                "teams": sides,
            })
    return matchups


def parse_transactions(payload) -> list:
    league = payload["fantasy_content"]["league"]
    container = merge_dicts(league[1:]).get("transactions", {})
    txns = []
    for t in indexed_items(container):
        tx = t.get("transaction", t)
        meta = merge_dicts(tx[0] if isinstance(tx, list) else tx)
        players_container = merge_dicts(tx[1:]).get("players", {}) if isinstance(tx, list) else {}
        adds, drops = [], []
        for p in indexed_items(players_container):
            pl = p.get("player", p)
            pmeta = merge_dicts(pl[0] if isinstance(pl, list) else pl)
            pdata = merge_dicts(pl[1:]) if isinstance(pl, list) else {}
            tdata = merge_dicts(pdata.get("transaction_data", pdata))
            if isinstance(pdata.get("transaction_data"), list):
                tdata = merge_dicts(pdata["transaction_data"])
            entry = {
                "player": (pmeta.get("name", {}) or {}).get("full", "Unknown"),
                "position": pmeta.get("display_position", ""),
                "nfl_team": pmeta.get("editorial_team_abbr", ""),
                "team_name": tdata.get("destination_team_name") or tdata.get("source_team_name") or "",
                "team_key": tdata.get("destination_team_key") or tdata.get("source_team_key") or "",
            }
            if tdata.get("type") == "add":
                adds.append(entry)
            elif tdata.get("type") == "drop":
                drops.append(entry)
        txns.append({
            "id": meta.get("transaction_key", ""),
            "type": meta.get("type", ""),
            "status": meta.get("status", ""),
            "timestamp": safe_int(meta.get("timestamp")),
            "faab_bid": safe_int(meta.get("faab_bid"), default=-1),
            "adds": adds,
            "drops": drops,
        })
    return txns


# ----------------------------------------------------- power rankings

def compute_power_rankings(teams: list, all_matchups: list, current_week: int) -> list:
    """Blend of record, scoring, all-play record, and recent form."""
    if not teams:
        return []

    # Weekly scores per team from completed matchups
    weekly: dict[str, dict[int, float]] = {t["team_key"]: {} for t in teams}
    for mu in all_matchups:
        if mu.get("status") != "postevent":
            continue
        for side in mu["teams"]:
            if side["team_key"] in weekly:
                weekly[side["team_key"]][mu["week"]] = side["points"]

    weeks_played = sorted({w for scores in weekly.values() for w in scores})

    # All-play: each week, how many teams did you outscore?
    all_play_w = {k: 0 for k in weekly}
    all_play_l = {k: 0 for k in weekly}
    for w in weeks_played:
        scores = [(k, s[w]) for k, s in weekly.items() if w in s]
        for k, pts in scores:
            for k2, pts2 in scores:
                if k == k2:
                    continue
                if pts > pts2:
                    all_play_w[k] += 1
                elif pts < pts2:
                    all_play_l[k] += 1

    pf_values = [t["points_for"] for t in teams]
    pf_min, pf_max = (min(pf_values), max(pf_values)) if pf_values else (0, 1)
    pf_range = (pf_max - pf_min) or 1.0

    recent_weeks = weeks_played[-3:]

    ranked = []
    for t in teams:
        k = t["team_key"]
        games = t["wins"] + t["losses"] + t["ties"]
        win_pct = t["win_pct"] if t["win_pct"] else (t["wins"] / games if games else 0.0)
        ap_games = all_play_w[k] + all_play_l[k]
        ap_pct = all_play_w[k] / ap_games if ap_games else 0.0
        pf_norm = (t["points_for"] - pf_min) / pf_range if games else 0.0

        recent_scores = [weekly[k][w] for w in recent_weeks if w in weekly[k]]
        if recent_scores and weeks_played:
            league_recent = [s for kk in weekly for w, s in weekly[kk].items() if w in recent_weeks]
            lo, hi = min(league_recent), max(league_recent)
            rng = (hi - lo) or 1.0
            form = sum((s - lo) / rng for s in recent_scores) / len(recent_scores)
        else:
            form = 0.0

        score = 0.35 * win_pct + 0.30 * pf_norm + 0.20 * ap_pct + 0.15 * form
        ranked.append({
            "team_key": k,
            "score": round(score, 4),
            "all_play": f"{all_play_w[k]}-{all_play_l[k]}",
            "all_play_pct": round(ap_pct, 3),
            "luck_index": round(win_pct - ap_pct, 3),  # + = lucky, - = robbed
            "recent_form": round(form, 3),
        })

    ranked.sort(key=lambda r: r["score"], reverse=True)

    # movement vs. previous run
    prev = {}
    league_file = DATA_DIR / "league.json"
    if league_file.exists():
        try:
            old = json.loads(league_file.read_text())
            prev = {r["team_key"]: r["rank"] for r in old.get("power_rankings", [])}
        except Exception:  # noqa: BLE001
            prev = {}

    for i, r in enumerate(ranked, start=1):
        r["rank"] = i
        r["prev_rank"] = prev.get(r["team_key"], i)
        r["movement"] = r["prev_rank"] - i
    return ranked


# ------------------------------------------------------------- faab

def build_feed(teams: list, rankings: list, transactions: list, matchups: list,
               prev_feed: list) -> list:
    """Assemble The Feed: ranking moves, wire activity, notable scores.

    Existing items are matched by id so their reaction counts survive a refresh.
    """
    by_key = {t["team_key"]: t for t in teams}
    old = {i["id"]: i for i in prev_feed}
    items = []

    def add(item_id, kind, title, body, ts, team_key=""):
        prior = old.get(item_id, {})
        items.append({
            "id": item_id, "kind": kind, "title": title, "body": body,
            "timestamp": ts, "team_key": team_key,
            "reactions": prior.get("reactions", {}),
            "reacted_by": prior.get("reacted_by", 0),
        })

    now = int(time.time())

    # biggest ranking movers
    for r in rankings:
        if abs(r.get("movement", 0)) < 2:
            continue
        t = by_key.get(r["team_key"], {})
        direction = "jumps" if r["movement"] > 0 else "drops"
        add(f"rank-{r['team_key']}-{r['rank']}", "rankings",
            f"{t.get('name','A team')} {direction} {abs(r['movement'])} "
            f"spot{'s' if abs(r['movement']) != 1 else ''} to #{r['rank']}",
            f"All-play {r.get('all_play','')} and a luck index of {r.get('luck_index',0):+.3f}. "
            f"The model {'likes' if r['movement'] > 0 else 'trusts'} them "
            f"{'more' if r['movement'] > 0 else 'less'} than the standings do.",
            now, r["team_key"])

    # notable wire moves
    for tx in transactions[:12]:
        if not tx["adds"]:
            continue
        a = tx["adds"][0]
        team = by_key.get(a.get("team_key", ""), {})
        if tx.get("faab_bid", 0) > 0:
            left = team.get("faab_balance", -1)
            body = (f"Leaves them with ${max(0, left)} for the rest of the season."
                    if left >= 0 else "A bid that will be discussed.")
            add(f"wire-{tx['id']}", "wire",
                f"{a.get('team_name','Someone')} spends ${tx['faab_bid']} on {a['player']}",
                body, tx.get("timestamp", now), a.get("team_key", ""))

    # weekly high and low
    done = [m for m in matchups if m.get("status") == "postevent"]
    if done:
        last = max(m["week"] for m in done)
        sides = [s for m in done if m["week"] == last for s in m["teams"]]
        if sides:
            lo = min(sides, key=lambda s: s["points"])
            hi = max(sides, key=lambda s: s["points"])
            add(f"score-low-{last}", "scores",
                f"{lo['name']} posts {lo['points']:.1f} — lowest score of Week {last}",
                "Somebody should check the starting lineup for players on bye.", now,
                lo["team_key"])
            add(f"score-high-{last}", "scores",
                f"{hi['name']} drops {hi['points']:.1f} on the league in Week {last}",
                "Top score of the week. They will not shut up about it.", now,
                hi["team_key"])

    items.sort(key=lambda i: i["timestamp"], reverse=True)
    return items[:30]


def most_clowned(feed: list, roast: dict, teams: list) -> list:
    """Rank teams by reactions received this week."""
    tally = {t["team_key"]: 0 for t in teams}
    names = {t["team_key"]: t["name"] for t in teams}
    for b in roast.get("team_blurbs", []):
        if b.get("team_key") in tally:
            tally[b["team_key"]] += sum(b.get("reactions", {}).values())
    for item in feed:
        key = item.get("team_key")
        if key in tally:
            tally[key] += sum(item.get("reactions", {}).values())
    out = [{"team_key": k, "team_name": names[k], "count": v}
           for k, v in tally.items() if v > 0]
    out.sort(key=lambda x: x["count"], reverse=True)
    return out[:5]


def faab_stats(teams: list, transactions: list, budget: int) -> dict:
    spent = {t["team_key"]: 0 for t in teams}
    bids = []
    for tx in transactions:
        if tx["faab_bid"] and tx["faab_bid"] > 0 and tx["adds"]:
            key = tx["adds"][0].get("team_key", "")
            if key in spent:
                spent[key] += tx["faab_bid"]
            bids.append({
                "team_key": key,
                "team_name": tx["adds"][0].get("team_name", ""),
                "player": tx["adds"][0].get("player", ""),
                "bid": tx["faab_bid"],
                "timestamp": tx["timestamp"],
            })
    bids.sort(key=lambda b: b["bid"], reverse=True)
    return {"budget": budget, "spent": spent, "top_bids": bids[:10]}


# -------------------------------------------------------------- main

def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    RAW_DIR.mkdir(exist_ok=True)

    print(f"Fetching league {LEAGUE_KEY} ...")
    token = get_access_token()

    standings_raw = api_get(token, f"league/{LEAGUE_KEY}/standings")
    (RAW_DIR / "standings.json").write_text(json.dumps(standings_raw, indent=1))
    meta, teams = parse_standings(standings_raw)
    print(f"  league: {meta['name']} season {meta['season']} week {meta['current_week']}, {len(teams)} teams")

    settings_raw = api_get(token, f"league/{LEAGUE_KEY}/settings")
    (RAW_DIR / "settings.json").write_text(json.dumps(settings_raw, indent=1))
    settings = merge_dicts(merge_dicts(settings_raw["fantasy_content"]["league"][1:]).get("settings", []))
    faab_budget = safe_int(settings.get("waiver_budget"), default=100) or 100
    uses_faab = str(settings.get("uses_faab", "0")) in ("1", "true", "True")

    # scoreboards for every week played so far
    all_matchups = []
    last_week = min(meta["current_week"], meta["end_week"])
    for week in range(meta["start_week"], last_week + 1):
        try:
            sb_raw = api_get(token, f"league/{LEAGUE_KEY}/scoreboard;week={week}")
            wk = parse_scoreboard(sb_raw)
            all_matchups.extend(wk)
            print(f"  week {week}: {len(wk)} matchups")
        except Exception as e:  # noqa: BLE001
            print(f"  week {week}: scoreboard failed ({e})")

    txn_raw = api_get(token, f"league/{LEAGUE_KEY}/transactions")
    (RAW_DIR / "transactions.json").write_text(json.dumps(txn_raw, indent=1))
    transactions = parse_transactions(txn_raw)
    print(f"  transactions: {len(transactions)}")

    rankings = compute_power_rankings(teams, all_matchups, meta["current_week"])
    faab = faab_stats(teams, transactions, faab_budget)

    # Carry forward everything the Yahoo API doesn't own: the roast column,
    # accumulated reactions, the league vote, and season history.
    league_file = DATA_DIR / "league.json"
    prev = {}
    if league_file.exists():
        try:
            prev = json.loads(league_file.read_text())
        except Exception:  # noqa: BLE001
            prev = {}
    roast = prev.get("roast", {})
    history = prev.get("history", {})
    vote = prev.get("vote")

    # reattach reactions to matchups by (week, team keys)
    prev_react = {
        f"{m['week']}-{m['teams'][0]['team_key']}": m.get("reactions", {})
        for m in prev.get("matchups", []) if m.get("teams")
    }
    for m in all_matchups:
        if m.get("teams"):
            m["reactions"] = prev_react.get(f"{m['week']}-{m['teams'][0]['team_key']}", {})

    # trophies from recorded history
    titles, toilets = {}, {}
    for s in history.get("seasons", []):
        titles.setdefault(s.get("champion", ""), []).append(s.get("year"))
        toilets.setdefault(s.get("toilet", ""), []).append(s.get("year"))
    for t in teams:
        marks = [f"Champion '{str(y)[-2:]}" for y in titles.get(t["name"], [])]
        n_toilet = len(toilets.get(t["name"], []))
        if n_toilet == 1:
            marks.append(f"Toilet Bowl '{str(toilets[t['name']][0])[-2:]}")
        elif n_toilet > 1:
            marks.append(f"Toilet Bowl ×{n_toilet}")
        t["trophies"] = marks

    feed = build_feed(teams, rankings, transactions, all_matchups, prev.get("feed", []))

    out = {
        "meta": {
            **meta,
            "uses_faab": uses_faab,
            "faab_budget": faab_budget,
            "demo": False,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "teams": teams,
        "power_rankings": rankings,
        "matchups": all_matchups,
        "transactions": transactions[:60],
        "faab": faab,
        "roast": roast,
        "feed": feed,
        "most_clowned": most_clowned(feed, roast, teams),
        "history": history,
    }
    if vote:
        out["vote"] = vote
    league_file.write_text(json.dumps(out, indent=1))
    print(f"Wrote {league_file}")


if __name__ == "__main__":
    main()
