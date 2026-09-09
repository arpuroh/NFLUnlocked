#!/usr/bin/env python3
"""
NFL Unlocked — this week's matchups.

Yahoo only publishes the pairings for the current week to logged-out visitors:
the league home page carries them as matchup links, and every later week is
behind a login. So this reads whatever week the home page is showing and writes
it to data/schedule.json, and the site renders that. Re-run it every Tuesday.

Usage:  python scripts/fetch_schedule.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen

LEAGUE_ID = "675504"
HOME = f"https://football.fantasysports.yahoo.com/f1/{LEAGUE_ID}"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main() -> int:
    try:
        doc = fetch(HOME)
    except Exception as e:  # noqa: BLE001
        print(f"  could not read the league page: {e}")
        return 1

    # team id -> name, from the links that sit beside every matchup
    names = {}
    for m in re.finditer(r'href="[^"]*/f1/' + LEAGUE_ID + r'/(\d+)"[^>]*>([^<]{1,60})</a>', doc):
        nm = unescape(m.group(2)).strip()
        if nm and not nm.isdigit():
            names.setdefault(m.group(1), nm)

    pairs, week = [], None
    for m in re.finditer(r"matchup\?week=(\d+)&(?:amp;)?mid1=(\d+)&(?:amp;)?mid2=(\d+)", doc):
        week = int(m.group(1))
        a, b = m.group(2), m.group(3)
        if (a, b) not in [(x["home_id"], x["away_id"]) for x in pairs]:
            pairs.append({"home_id": a, "away_id": b,
                          "home": names.get(a, ""), "away": names.get(b, "")})

    if not pairs:
        print("  no matchups found on the league page")
        return 1

    out = {
        "league_id": LEAGUE_ID,
        "week": week,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": HOME,
        "note": "Yahoo only exposes the current week to logged-out visitors.",
        "teams": names,
        "matchups": pairs,
    }
    (DATA / "schedule.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"  week {week}: {len(pairs)} matchups")
    for p in pairs:
        print(f"    {p['home']} vs {p['away']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
