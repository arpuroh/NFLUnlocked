#!/usr/bin/env python3
"""
NFL Unlocked — draft grades writer.

Turns data/draft.json (the auction ledger) into data/draft_grades.json (the
writing) with the Claude API. Schema the site expects:

{
  "season": 2026,
  "written_at": "...",
  "headline": "...",            # hero, <= 8 words, no trailing period
  "kicker":   "(...)",          # red parenthetical under the headline
  "lede":     "...",            # 2-3 sentences
  "rankings": [ {"rank": 1, "team": "...", "blurb": "one line"} , ... 14 ],
  "awards":   [ {"label": "...", "team": "...", "note": "..."} , ... 4-6 ],
  "grades": {
    "<team name exactly as in draft.json>": {
      "manager": "...", "grade": "B+", "headline": "...",
      "body": ["para", "para"], "best": "...", "worst": "..."
    }, ...
  }
}

Tone: full savage, fantasy decisions only. Never anybody's job, family, body or
real life. The prompt below carries that rule; keep it there.

Usage:
  ANTHROPIC_API_KEY=... python scripts/generate_draft_grades.py
  python scripts/generate_draft_grades.py --dry-run     # print the prompt only
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5")

SYSTEM = """You write the draft-grades column for NFL Unlocked, a 14-team, half-PPR, $200
auction fantasy football league with a 16-man roster: QB, 2 RB, 2 WR, TE, 2 W/R/T flex, K, DEF,
one IDP, 5 bench, 2 IR. Kickers score total FG yards (1 pt / 10 yds), the IDP slot rewards tackle
volume, 4-pt passing TDs. Six of fourteen make the playoffs; the bottom three play the Sacco Bowl
and the loser owns the Sacco for a year.

Voice: modernist sports tabloid. Short declarative sentences. Specific numbers. Dry, mean, funny.
FULL SAVAGE about fantasy decisions only: prices paid, roster shape, positional neglect, panic buys,
money left on the table, $1 bins, last year's results. NEVER about anybody's job, family, body,
health, appearance or real life. No emoji. No exclamation points. No em dashes; use commas,
periods or parentheses.

Grade on: price vs. the room's market for that tier, roster shape against the league's actual
lineup, depth, and whether the money bought points or bought names. Money left unspent is a
crime. Grades range A+ to F and must spread across the league; do not give everyone a B."""


def build_prompt(draft: dict, prev: dict | None, history: str) -> str:
    teams = []
    for t in draft["teams"]:
        picks = ", ".join(f"{p['player']} ({p['pos']}) ${p['cost']}" +
                          (f" [was ${p['last_year']} in {prev['season']}]" if p.get("last_year") is not None and prev else "")
                          for p in t["picks"])
        teams.append(f"### {t['team']} · spent ${t['spent']} / ${draft['budget']} · {t['count']} players · "
                     f"top-3 share {round(t['top3_share'] * 100)}% · ${1} players: {t['dollar_players']}\n"
                     f"By position: {json.dumps(t['pos_spend'])}\n{picks}")
    L = draft["ledger"]
    market = "\n".join(f"{k}: {v['count']} bought, ${v['total']} total, avg ${v['avg']}, top ${v['max']['cost']} {v['max']['player']}"
                       for k, v in L["pos_market"].items())
    return f"""Season {draft['season']} auction. {len(draft['picks'])} picks, ${L['total_spent']} of ${L['total_budget']} spent,
{L['dollar_count']} players went for $1.

POSITION MARKET
{market}

TEN BIGGEST BUYS
{chr(10).join(f"${p['cost']} {p['player']} ({p['pos']}) to {p['team']}" for p in L['top_buys'][:10])}

LEAGUE MEMORY (use it)
{history}

TEAMS
{chr(10).join(teams)}

Write the JSON object described below and nothing else. Team names must match exactly.
{{
 "headline": "<= 8 words", "kicker": "(short parenthetical)", "lede": "2-3 sentences",
 "rankings": [{{"rank": 1, "team": "...", "blurb": "one savage line"}}, ... all {len(draft['teams'])}],
 "awards": [{{"label": "Best Value", "team": "...", "note": "..."}}, {{"label": "Worst Overpay", ...}},
            {{"label": "Most Money Left on the Table", ...}}, {{"label": "Boldest Build", ...}}, {{"label": "Most Boring Draft", ...}}],
 "grades": {{"<team>": {{"manager": "...", "grade": "B+", "headline": "5-9 words",
             "body": ["paragraph of 3-4 sentences", "paragraph of 2-3 sentences"],
             "best": "player, price, one clause why", "worst": "player, price, one clause why"}}, ...}}
}}"""


def call_claude(prompt: str) -> str:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("ANTHROPIC_API_KEY is not set.")
    body = json.dumps({
        "model": MODEL, "max_tokens": 8000, "system": SYSTEM,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, method="POST", headers={
        "x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        out = json.loads(r.read().decode())
    return "".join(b.get("text", "") for b in out["content"])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", default=str(DATA / "draft.json"))
    ap.add_argument("--prev", default=str(DATA / "draft_2025.json"))
    ap.add_argument("--out", default=str(DATA / "draft_grades.json"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    draft = json.loads(Path(args.draft).read_text())
    if draft.get("status") != "complete":
        sys.exit(f"draft.json status is {draft.get('status')!r}; nothing to grade yet.")
    prev = json.loads(Path(args.prev).read_text()) if Path(args.prev).exists() else None

    # Whatever the league remembers: last season's finish per team, if we have it.
    history = ""
    lp = DATA / "ledger.json"
    if lp.exists():
        led = json.loads(lp.read_text())
        yr = str(draft["season"] - 1)
        history = "\n".join(f"{a[0]} ({a[1]}): finished {a[2]}, {a[4]}-{a[5]}, {a[6]} PF" for a in led.get(yr, []))
    prompt = build_prompt(draft, prev, history)
    if args.dry_run:
        print(prompt); return 0

    text = call_claude(prompt)
    text = text[text.find("{"): text.rfind("}") + 1]
    grades = json.loads(text)
    names = {t["team"] for t in draft["teams"]}
    missing = names - set(grades.get("grades", {}))
    if missing:
        print(f"  WARNING: no grade for {missing}")
    grades["season"] = draft["season"]
    grades["written_at"] = datetime.now(timezone.utc).isoformat()
    Path(args.out).write_text(json.dumps(grades, indent=1, ensure_ascii=False))
    print(f"  wrote {args.out}: {len(grades['grades'])} grades")
    return 0


if __name__ == "__main__":
    sys.exit(main())
