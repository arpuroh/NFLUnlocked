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
  YAHOO_REDIRECT_URI   Callback URL the refresh token was granted against
"""

import hashlib
import json
import os
import sys
import time
import urllib.error
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

def _refresh(cid: str, secret: str, refresh: str, redirect_uri: str) -> dict:
    body = urllib.parse.urlencode({
        "client_id": cid,
        "client_secret": secret,
        "refresh_token": refresh,
        "grant_type": "refresh_token",
        "redirect_uri": redirect_uri,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        detail = " ".join((e.read().decode("utf-8", "replace") or "").split())[:300]
        raise RuntimeError(f"HTTP {e.code} :: {detail}") from None


def get_access_token() -> str:
    """Mint an access token that the Fantasy API will actually accept.

    Yahoo hands back a perfectly valid-looking access token on refresh even when
    the grant behind it carries no fantasy scope; the failure only shows up later
    as a 403 on the first data call. So refresh, then probe, and only return a
    token that has been proven to work. `redirect_uri` on the refresh call is the
    variable worth testing: Yahoo is documented as `oob`, but a grant created
    against a real callback URL does not always honour that.
    """
    cid = os.environ.get("YAHOO_CLIENT_ID")
    secret = os.environ.get("YAHOO_CLIENT_SECRET")
    refresh = os.environ.get("YAHOO_REFRESH_TOKEN")
    if not all([cid, secret, refresh]):
        sys.exit("Missing YAHOO_CLIENT_ID / YAHOO_CLIENT_SECRET / YAHOO_REFRESH_TOKEN env vars.")

    # Identify which Yahoo app these secrets belong to without ever printing them.
    # Actions masks secret values in logs, so a hash is the only way to tell the
    # right app from the wrong one — and hashes are safe to publish.
    print("  credential fingerprints (sha256, first 10):")
    for label, val in (("client_id", cid), ("client_secret", secret), ("refresh_token", refresh)):
        print(f"    {label:<14} {hashlib.sha256(val.encode()).hexdigest()[:10]}  len={len(val)}")

    candidates = [
        os.environ.get("YAHOO_REDIRECT_URI", "https://www.nflunlocked.com/api/auth-callback"),
        "https://nflunlocked.com/api/auth-callback",
        "oob",
    ]
    last = ""
    for ru in candidates:
        try:
            tok = _refresh(cid, secret, refresh, ru)
        except Exception as e:  # noqa: BLE001
            print(f"  refresh(redirect_uri={ru}) failed: {e}")
            last = str(e)
            continue
        access = tok.get("access_token", "")
        try:
            api_get(access, "users;use_login=1/games", retries=1)
        except Exception as e:  # noqa: BLE001
            print(f"  refresh(redirect_uri={ru}) ok, but fantasy probe rejected it: {str(e)[:220]}")
            last = str(e)
            continue
        print(f"  fantasy access confirmed using redirect_uri={ru} (expires_in={tok.get('expires_in')})")
        return access

    print(
        "  no refresh variant produced a token the Fantasy API accepts.\n"
        f"  last response: {last[:300]}\n"
        "  ('not authorized' = the Yahoo app lacks Fantasy API approval; apply at\n"
        "  https://sports.yahoo.com/developer/). Falling back to the public league page."
    )
    return ""


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
        except urllib.error.HTTPError as e:
            # Yahoo puts the real reason in the body; the status alone is useless.
            try:
                body = e.read().decode("utf-8", "replace")
            except Exception:  # noqa: BLE001
                body = ""
            body = " ".join(body.split())[:500]
            if attempt == retries - 1:
                raise RuntimeError(f"HTTP {e.code} on {path} :: {body}") from None
            print(f"  retrying {path} after HTTP {e.code}: {body}")
            time.sleep(2 * (attempt + 1))
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            print(f"  retrying {path} after error: {e}")
            time.sleep(2 * (attempt + 1))
    return {}


def discover_leagues(token: str) -> list:
    """Every NFL league this Yahoo account has ever joined, newest season first.

    League ids are re-issued every season, so a hardcoded `nfl.l.<id>` key silently
    points at a stranger's league whenever the game alias rolls over — Yahoo answers
    that with a 403, not a 404. Asking Yahoo which leagues the token actually owns
    removes the guesswork, and doubles as the season chain for league history.
    """
    raw = api_get(token, "users;use_login=1/games;game_codes=nfl/leagues")
    found = []
    for u in indexed_items(raw.get("fantasy_content", {}).get("users", {})):
        user = merge_dicts(u.get("user", []))
        for g in indexed_items(user.get("games", {})):
            game = merge_dicts(g.get("game", []))
            season = safe_int(game.get("season"))
            for l in indexed_items(game.get("leagues", {})):
                lg = merge_dicts(l.get("league", []))
                if not lg.get("league_key"):
                    continue
                found.append({
                    "season": season or safe_int(lg.get("season")),
                    "league_key": lg.get("league_key"),
                    "league_id": str(lg.get("league_id") or ""),
                    "name": lg.get("name") or "",
                    "num_teams": safe_int(lg.get("num_teams")),
                })
    found.sort(key=lambda x: x["season"], reverse=True)
    return found


def resolve_league_key(token: str) -> str:
    """Pick the live league key, preferring an exact LEAGUE_ID hit, newest season."""
    try:
        leagues = discover_leagues(token)
    except Exception as e:  # noqa: BLE001
        print(f"  league discovery failed ({e}); falling back to {LEAGUE_KEY}")
        return LEAGUE_KEY

    if not leagues:
        print(f"  no leagues visible to this token; falling back to {LEAGUE_KEY}")
        return LEAGUE_KEY

    print(f"  this token can see {len(leagues)} NFL league(s):")
    for lg in leagues:
        print(f"    {lg['season']}  {lg['league_key']:<18} id={lg['league_id']:<8} "
              f"{lg['num_teams']:>2} teams  {lg['name']}")

    exact = [lg for lg in leagues if lg["league_id"] == str(LEAGUE_ID)]
    if exact:
        pick = exact[0]
        print(f"  matched LEAGUE_ID {LEAGUE_ID} -> {pick['league_key']} ({pick['season']})")
        return pick["league_key"]

    pick = leagues[0]
    print(f"  LEAGUE_ID {LEAGUE_ID} not in this account's leagues; "
          f"using newest instead -> {pick['league_key']} ({pick['season']}, {pick['name']})")
    return pick["league_key"]


# ------------------------------------------------------- page scrape
# Yahoo's Fantasy API is approval-gated, but this league is publicly viewable,
# so everything the site needs is sitting in server-rendered HTML. The scrape
# path keeps the site live while (or instead of) waiting on API approval.

from html.parser import HTMLParser  # noqa: E402

SITE_BASE = f"https://football.fantasysports.yahoo.com/f1/{LEAGUE_ID}"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


class TableGrab(HTMLParser):
    """Collect every <table> as rows of cells; each cell keeps text, links, imgs."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self._t, self._r, self._c = [], None, None, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._t = {"id": a.get("id", ""), "class": a.get("class", ""), "rows": []}
        elif tag == "tr" and self._t is not None:
            self._r = []
        elif tag in ("td", "th") and self._r is not None:
            self._c = {"text": "", "links": [], "imgs": []}
        elif self._c is not None and tag == "a" and a.get("href"):
            self._c["links"].append(a["href"])
        elif self._c is not None and tag == "img" and a.get("src"):
            self._c["imgs"].append(a["src"])

    def handle_data(self, data):
        if self._c is not None:
            self._c["text"] += data

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._c is not None:
            self._c["text"] = " ".join(self._c["text"].split())
            self._r.append(self._c)
            self._c = None
        elif tag == "tr" and self._r is not None:
            if self._r:
                self._t["rows"].append(self._r)
            self._r = None
        elif tag == "table" and self._t is not None:
            self.tables.append(self._t)
            self._t = None


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Accept", "text/html")
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8", "replace")


def grab_tables(html: str) -> list:
    p = TableGrab()
    p.feed(html)
    return p.tables


def _row_lookup(headers: list, row: list) -> dict:
    return {h.lower(): c for h, c in zip(headers, row)}


def scrape_league() -> tuple[dict, list, list, list]:
    """Standings, matchups and transactions straight off the public league pages."""
    print(f"  scraping public league page {SITE_BASE}")
    html = fetch_page(SITE_BASE)
    print(f"  fetched {len(html)} bytes; standingstable present: {'standingstable' in html}")

    tables = grab_tables(html)
    standings = next((t for t in tables if t["id"] == "standingstable"), None)
    if standings is None:
        # fall back to any table whose header row mentions W-L-T
        standings = next(
            (t for t in tables
             if t["rows"] and any("w-l-t" in c["text"].lower() for c in t["rows"][0])),
            None)
    if standings is None:
        raise RuntimeError(
            f"No standings table in the page ({len(tables)} tables seen). "
            "If the league was switched to private, flip 'Make league publicly viewable' "
            "back on in Yahoo league settings.")

    headers = [c["text"] for c in standings["rows"][0]]
    print(f"  standings columns: {headers}")

    teams = []
    for row in standings["rows"][1:]:
        cells = _row_lookup(headers, row)
        team_cell = cells.get("team")
        if not team_cell or not team_cell["text"]:
            continue
        team_href = next((l for l in team_cell["links"] if f"/f1/{LEAGUE_ID}/" in l), "")
        team_id = team_href.rstrip("/").split("/")[-1] if team_href else str(len(teams) + 1)
        wlt = (cells.get("w-l-t", {}) or {}).get("text", "0-0-0")
        parts = [safe_int(x) for x in wlt.split("-")] + [0, 0, 0]
        wins, losses, ties = parts[0], parts[1], parts[2]
        games = wins + losses + ties
        budget_txt = (cells.get("waiver bdgt", {}) or {}).get("text", "")
        streak_txt = (cells.get("streak", {}) or {}).get("text", "")
        teams.append({
            "team_key": f"scrape.l.{LEAGUE_ID}.t.{team_id}",
            "team_id": team_id,
            "name": team_cell["text"],
            "manager": "",
            "logo": (team_cell["imgs"] or [""])[0],
            "moves": safe_int((cells.get("moves", {}) or {}).get("text")),
            "trades": 0,
            "faab_balance": safe_int(budget_txt.replace("$", ""), default=-1) if "$" in budget_txt else -1,
            "clinched_playoffs": "*" in ((cells.get("rank", {}) or {}).get("text", "")),
            "rank": safe_int((cells.get("rank", {}) or {}).get("text", "").replace("*", "")) or len(teams) + 1,
            "wins": wins, "losses": losses, "ties": ties,
            "win_pct": round(wins / games, 3) if games else 0.0,
            "streak": streak_txt.replace("-", ""),
            "points_for": safe_float((cells.get("pf", {}) or {}).get("text")),
            "points_against": safe_float((cells.get("pa", {}) or {}).get("text")),
            "week_points": 0.0,
        })
    print(f"  parsed {len(teams)} teams from standings")

    # matchups: pre-draft the scoreboard is empty; harvest whatever exists
    matchups = []
    by_name = {t["name"]: t["team_key"] for t in teams}
    for t in tables:
        for row in t["rows"]:
            texts = [c["text"] for c in row]
            # matchup rows on the league page look like: name, score, name, score
            if len(texts) >= 4 and texts[0] in by_name and texts[2] in by_name:
                try:
                    p1, p2 = float(texts[1]), float(texts[3])
                except ValueError:
                    continue
                matchups.append({
                    "week": 0, "status": "postevent" if (p1 or p2) else "preevent",
                    "is_playoffs": False,
                    "winner_team_key": by_name[texts[0]] if p1 > p2 else by_name[texts[2]],
                    "teams": [
                        {"team_key": by_name[texts[0]], "name": texts[0], "points": p1},
                        {"team_key": by_name[texts[2]], "name": texts[2], "points": p2},
                    ],
                })

    # transactions page (public): adds/drops with FAAB bids once the season runs
    transactions = []
    try:
        tx_html = fetch_page(f"{SITE_BASE}/transactions")
        for t in grab_tables(tx_html):
            for row in t["rows"]:
                text = " | ".join(c["text"] for c in row if c["text"])
                if not text or "no recent transactions" in text.lower():
                    continue
                low = text.lower()
                if "added" not in low and "dropped" not in low and "trade" not in low:
                    continue
                transactions.append({
                    "id": f"scrape-{len(transactions)}",
                    "type": "add/drop" if "added" in low else "trade",
                    "status": "successful",
                    "timestamp": 0,
                    "faab_bid": safe_int((["0"] + [w.strip("$") for w in text.split() if w.startswith("$")])[-1], 0),
                    "adds": [], "drops": [],
                    "raw": text[:200],
                })
        print(f"  transactions scraped: {len(transactions)}")
    except Exception as e:  # noqa: BLE001
        print(f"  transactions page skipped ({e})")

    season = datetime.now(timezone.utc).year if datetime.now(timezone.utc).month >= 3 else datetime.now(timezone.utc).year - 1
    meta = {
        "league_key": f"scrape.l.{LEAGUE_ID}",
        "name": "NFL Unlocked",
        "season": str(season),
        "current_week": max([m["week"] for m in matchups], default=1) or 1,
        "start_week": 1, "end_week": 17,
        "num_teams": len(teams),
        "url": SITE_BASE,
        "logo": "",
        "is_finished": False,
    }
    return meta, teams, matchups, transactions


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

    global LEAGUE_KEY
    print(f"Fetching league {LEAGUE_KEY} ...")
    token = get_access_token()

    faab_budget, uses_faab = 100, True
    if token:
        LEAGUE_KEY = resolve_league_key(token)

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
    else:
        meta, teams, all_matchups, transactions = scrape_league()
        print(f"  league: {meta['name']} season {meta['season']}, {len(teams)} teams (scraped)")

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
