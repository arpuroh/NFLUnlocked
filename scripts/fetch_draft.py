#!/usr/bin/env python3
"""
NFL Unlocked — draft results fetcher.

Reads the league's PUBLIC Yahoo draft-results page (no OAuth needed; the league
is publicly viewable) and writes data/draft.json: every pick with its auction
price, per-team rosters and spend, and the league-wide ledger the draft page
renders (biggest buys, position markets, $1 counts, last year's price for the
same player when we have it).

Grades are NOT written here. They live in data/draft_grades.json, keyed by team
name, and are produced by scripts/generate_draft_grades.py (or by hand). Keeping
them apart means re-running this scraper never clobbers the writing.

Usage:
  python scripts/fetch_draft.py                      # scrape the live league page
  python scripts/fetch_draft.py --fixture data/draft_2025.txt --season 2025 \
      --out data/draft_2025.json                     # build from a saved pick list

Exit codes: 0 wrote a file (status may still be "pending" if the draft has not
happened yet), 1 the page could not be read at all.
"""

import argparse
import json
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

LEAGUE_ID = "675504"
PAGE = f"https://football.fantasysports.yahoo.com/f1/{LEAGUE_ID}/draftresults"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# Yahoo lists a player as "Name (Team - POS)"; IDPs carry two slots ("DB,CB").
# Fantasy-relevant bucket for the ledger and the position markets.
def bucket(pos: str) -> str:
    p = pos.split(",")[0].strip().upper()
    if p in ("QB", "RB", "WR", "TE", "K", "DEF"):
        return p
    return "IDP"


# ---------------------------------------------------------------- parsing

class Tables(HTMLParser):
    """Collects every <table> as {id, cls, rows:[[{text, title, href}]]}."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tables, self._t, self._row, self._cell = [], None, None, None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._t = {"id": a.get("id", ""), "cls": a.get("class", ""), "rows": []}
        elif tag == "tr" and self._t is not None:
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = {"text": "", "title": a.get("title", ""), "href": ""}
        elif tag == "a" and self._cell is not None and not self._cell["href"]:
            self._cell["href"] = a.get("href", "")

    def handle_data(self, data):
        if self._cell is not None:
            self._cell["text"] += data

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._cell["text"] = " ".join(self._cell["text"].split())
            self._row.append(self._cell); self._cell = None
        elif tag == "tr" and self._row is not None:
            if self._row: self._t["rows"].append(self._row)
            self._row = None
        elif tag == "table" and self._t is not None:
            self.tables.append(self._t); self._t = None


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


PLAYER_RE = re.compile(r"^(?P<name>.*?)\s*\((?P<nfl>[^)]*?)\s*-\s*(?P<pos>[^)]*)\)\s*$")


def parse_picks(html: str) -> list:
    """Rows of the Pick | Player | Salary | Team table, in draft order."""
    tp = Tables(); tp.feed(html)
    for t in tp.tables:
        if not t["rows"]:
            continue
        head = [c["text"].lower() for c in t["rows"][0]]
        if "pick" in head and "player" in head and ("salary" in head or "cost" in head):
            picks = []
            for r in t["rows"][1:]:
                cells = dict(zip(head, r))
                pick = int(re.sub(r"\D", "", cells["pick"]["text"]) or 0)
                m = PLAYER_RE.match(cells["player"]["text"])
                name = m.group("name") if m else cells["player"]["text"]
                nfl = m.group("nfl") if m else ""
                pos = m.group("pos") if m else ""
                cost_txt = (cells.get("salary") or cells.get("cost"))["text"]
                cost = int(re.sub(r"[^\d]", "", cost_txt) or 0)
                team = cells["team"]["title"] or cells["team"]["text"]
                picks.append({"pick": pick, "player": name, "nfl": nfl, "pos": pos,
                              "slot": bucket(pos), "cost": cost, "team": team})
            return picks
    return []


def parse_order(html: str) -> list:
    """Nomination-order table: team names + starting budget, present pre- and post-draft."""
    tp = Tables(); tp.feed(html)
    for t in tp.tables:
        if not t["rows"]:
            continue
        head = [c["text"].lower() for c in t["rows"][0]]
        if any("nomination" in h for h in head) and "team" in head:
            out = []
            for r in t["rows"][1:]:
                cells = dict(zip(head, r))
                team = cells["team"]["title"] or cells["team"]["text"]
                if team and team != "-":
                    out.append(team)
            return out
    return []


def parse_fixture(path: Path) -> list:
    picks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        pick, name, tp, cost, team = line.split("~")
        nfl, _, pos = tp.partition(" - ")
        picks.append({"pick": int(pick), "player": name, "nfl": nfl, "pos": pos,
                      "slot": bucket(pos), "cost": int(cost), "team": team})
    return picks


# ---------------------------------------------------------------- analysis

# ---------------------------------------------------------------- lineup model
#
# Only eight roster slots turn money into points: QB, RB, RB, WR, WR, TE and two
# flexes. Kickers, defenses and the IDP cost a dollar and are replacement level by
# definition, so they are left out of the strength number entirely.
#
# An auction price is the whole room's estimate of a player's value over a freely
# available replacement, which is why prices add up the way points do. The one
# place raw price lies is at the bottom: a $3 starter is not worth three dollars of
# production, he is worth roughly nothing, because anybody can claim a $3 player on
# Tuesday. So REPLACEMENT dollars come off every player before the lineup is added
# up. Bench players count at BENCH_WEIGHT because byes and injuries hand them
# roughly a fifth of the season's starts.
FULL_LINEUP = [("QB", 1), ("RB", 2), ("WR", 2), ("TE", 1), ("FLEX", 2), ("K", 1), ("DEF", 1), ("IDP", 1)]
OFFENSE = [("QB", 1), ("RB", 2), ("WR", 2), ("TE", 1), ("FLEX", 2)]
FLEX_OK = ("RB", "WR", "TE")
REPLACEMENT = 4
BENCH_WEIGHT = 0.30


def _fill(pool: list, slots: list) -> tuple:
    used, starters = set(), []
    missing = []
    for slot, n in slots:
        for _ in range(n):
            cand = next((p for p in pool
                         if id(p) not in used
                         and (p["slot"] in FLEX_OK if slot == "FLEX" else p["slot"] == slot)), None)
            if cand is None:
                missing.append(slot)
                continue
            used.add(id(cand))
            starters.append({**cand, "start": slot})
    return starters, used, missing


def fit_lineup(picks: list) -> dict:
    """Whole-roster fit, used for the money map and the waiver-wire shopping list."""
    pool = sorted(picks, key=lambda p: -p["cost"])
    starters, used, missing = _fill(pool, FULL_LINEUP)
    bench = [p for p in pool if id(p) not in used]
    return {
        "starters": starters, "bench": bench, "missing": missing,
        "starter_capital": sum(p["cost"] for p in starters),
        "bench_spend": sum(p["cost"] for p in bench),
        "core_capital": sum(p["cost"] for p in starters if p["slot"] in FLEX_OK),
    }


def lineup_strength(picks: list) -> dict:
    """The number the power rankings are built on: replacement-adjusted starting offense."""
    pool = sorted(picks, key=lambda p: -p["cost"])
    starters, used, _ = _fill(pool, OFFENSE)
    bench = [p for p in pool if id(p) not in used and p["slot"] in ("QB",) + FLEX_OK]
    above = lambda p: max(0, p["cost"] - REPLACEMENT)
    start_value = sum(above(p) for p in starters)
    bench_value = sum(above(p) for p in bench[:5])
    return {
        "offense_starters": [{"start": p["start"], "player": p["player"], "pos": p["pos"],
                              "slot": p["slot"], "cost": p["cost"]} for p in starters],
        "start_paid": sum(p["cost"] for p in starters),
        "start_value": start_value,
        "bench_value": bench_value,
        "lineup_score": round(start_value + BENCH_WEIGHT * bench_value, 1),
        "weak_starters": [p["player"] for p in starters
                          if p["cost"] <= REPLACEMENT and p["slot"] != "QB"],
    }


def build(picks: list, order: list, season: int, budget: int, prev: dict | None) -> dict:
    prev_price = {}
    if prev:
        for p in prev.get("picks", []):
            prev_price[p["player"]] = p["cost"]

    by_team = defaultdict(list)
    for p in picks:
        if prev_price.get(p["player"]) is not None:
            p["last_year"] = prev_price[p["player"]]
        by_team[p["team"]].append(p)

    team_names = list(dict.fromkeys(order + [p["team"] for p in picks]))
    teams = []
    for name in team_names:
        ps = sorted(by_team.get(name, []), key=lambda x: -x["cost"])
        spent = sum(p["cost"] for p in ps)
        top3 = sum(p["cost"] for p in ps[:3])
        pos_spend = defaultdict(int)
        for p in ps:
            pos_spend[p["slot"]] += p["cost"]
        fit = fit_lineup(ps)
        strength = lineup_strength(ps)
        teams.append({
            "team": name,
            "picks": ps,
            "count": len(ps),
            "spent": spent,
            "left": budget - spent,
            "top_buy": ps[0] if ps else None,
            "top3_share": round(top3 / spent, 3) if spent else 0,
            "dollar_players": sum(1 for p in ps if p["cost"] <= 1),
            "avg_cost": round(spent / len(ps), 1) if ps else 0,
            "pos_spend": dict(pos_spend),
            "starters_spend": sum(p["cost"] for p in ps if p["slot"] in ("QB", "RB", "WR", "TE")),
            "starter_capital": fit["starter_capital"],
            "bench_spend": fit["bench_spend"],
            "core_capital": fit["core_capital"],
            "missing": fit["missing"],
            **strength,
        })

    # league-wide ledger
    priced = sorted(picks, key=lambda p: (-p["cost"], p["pick"]))
    pos_market = {}
    for slot in ("QB", "RB", "WR", "TE", "K", "DEF", "IDP"):
        ps = [p for p in picks if p["slot"] == slot]
        if ps:
            pos_market[slot] = {
                "count": len(ps),
                "total": sum(p["cost"] for p in ps),
                "max": max(ps, key=lambda p: p["cost"]),
                "avg": round(sum(p["cost"] for p in ps) / len(ps), 1),
            }
    total_spent = sum(p["cost"] for p in picks)
    inflation = []
    for p in picks:
        if "last_year" in p and p["last_year"] >= 10:
            inflation.append({**p, "delta": p["cost"] - p["last_year"]})
    inflation.sort(key=lambda p: -abs(p["delta"]))

    money_map = [{
        "team": t["team"],
        "starter_capital": t["starter_capital"],
        "bench_spend": t["bench_spend"],
        "pos": {k: t["pos_spend"].get(k, 0) for k in ("QB", "RB", "WR", "TE", "K", "DEF", "IDP")},
    } for t in sorted(teams, key=lambda t: -t["starter_capital"])]

    holes = [{"team": t["team"], "missing": t["missing"]} for t in teams if t["missing"]]

    lineup_board = sorted(
        [{"team": t["team"], "lineup_score": t["lineup_score"], "start_paid": t["start_paid"],
          "start_value": t["start_value"], "bench_value": t["bench_value"],
          "weak_starters": t["weak_starters"]} for t in teams],
        key=lambda x: -x["lineup_score"])

    status = "complete" if picks and len(picks) >= len(team_names) * 14 else \
             "in_progress" if picks else "pending"

    return {
        "season": season,
        "league_id": LEAGUE_ID,
        "status": status,
        "budget": budget,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": PAGE,
        "teams": sorted(teams, key=lambda t: -t["spent"]),
        "picks": picks,
        "ledger": {
            "total_spent": total_spent,
            "total_budget": budget * len(team_names),
            "top_buys": priced[:12],
            "pos_market": pos_market,
            "dollar_count": sum(1 for p in picks if p["cost"] <= 1),
            "first_ten": sorted(picks, key=lambda p: p["pick"])[:10],
            "price_moves": inflation[:12],
            "money_map": money_map,
            "holes": holes,
            "lineup_board": lineup_board,
            "avg_lineup_score": round(sum(t["lineup_score"] for t in teams) / len(teams), 1) if teams else 0,
            "avg_starter_capital": round(sum(t["starter_capital"] for t in teams) / len(teams), 1) if teams else 0,
            "avg_bench_spend": round(sum(t["bench_spend"] for t in teams) / len(teams), 1) if teams else 0,
            "qb_spend": sorted(
                [{"team": t["team"], "spent": t["pos_spend"].get("QB", 0)} for t in teams],
                key=lambda x: -x["spent"]),
        },
    }


# ---------------------------------------------------------------- main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixture", help="pick list (pick~player~Team - POS~cost~team) instead of the live page")
    ap.add_argument("--season", type=int, default=datetime.now(timezone.utc).year)
    ap.add_argument("--budget", type=int, default=200)
    ap.add_argument("--out", default=str(DATA / "draft.json"))
    ap.add_argument("--prev", default=str(DATA / "draft_2025.json"),
                    help="previous season draft.json for year-over-year prices")
    args = ap.parse_args()

    order = []
    if args.fixture:
        picks = parse_fixture(Path(args.fixture))
        print(f"  fixture: {len(picks)} picks")
    else:
        try:
            html = fetch(PAGE)
        except Exception as e:  # noqa: BLE001
            print(f"  could not fetch {PAGE}: {e}")
            return 1
        print(f"  fetched {len(html)} bytes")
        picks = parse_picks(html)
        order = parse_order(html)
        print(f"  picks: {len(picks)}  teams in nomination order: {len(order)}")

    prev = None
    pp = Path(args.prev)
    if pp.exists() and Path(args.out).resolve() != pp.resolve():
        try:
            prev = json.loads(pp.read_text())
        except Exception:  # noqa: BLE001
            prev = None

    out = build(picks, order, args.season, args.budget, prev)
    Path(args.out).write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"  status={out['status']}  wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
