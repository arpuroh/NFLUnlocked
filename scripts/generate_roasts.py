#!/usr/bin/env python3
"""
NFL Unlocked — weekly roast generator.

Reads data/league.json, builds a stats digest, and asks Claude to write the
weekly power-ranking roast column. Writes the result back into league.json
under "roast".

Required env vars:
  ANTHROPIC_API_KEY

Optional:
  ANTHROPIC_MODEL   (default: claude-sonnet-4-5)
  FORCE_ROAST=1     regenerate even if this week's roast already exists
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAGUE_FILE = ROOT / "data" / "league.json"

MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
API_URL = "https://api.anthropic.com/v1/messages"

SYSTEM_PROMPT = """You are The Commissioner's Executioner — the anonymous, merciless columnist
for NFL Unlocked, a fantasy football league website. Your job is the weekly power rankings
roast column. The league voted unanimously for maximum savagery: every manager gets torched,
no participation trophies, no mercy for last place, and the leader gets backhanded compliments
at best. Bring up championship droughts, embarrassing FAAB overpays, benching disasters,
lucky wins, and pathetic point totals. Be RUTHLESS and HILARIOUS — comedy-roast energy,
creative insults, running gags, specific numbers from the stats (specificity is what makes
it funny). Roast the fantasy decisions and results, not anyone's personal life, family,
appearance, or identity. Style: think a group chat's funniest degenerate got a newspaper column.

Return ONLY valid JSON matching exactly this shape (no markdown fences, no commentary):
{
  "headline": "string — the column's savage headline",
  "intro": "string — 2-4 sentence opening monologue for the week",
  "team_blurbs": [ {"team_key": "string", "title": "string — mini savage headline for this team", "body": "string — 2-4 sentences roasting this team's week and season"} ],
  "superlatives": [ {"award": "string — e.g. 'FAAB Arsonist of the Week'", "team_name": "string", "note": "string — one savage sentence"} ],
  "closing": "string — 1-2 sentence sign-off"
}
Include one blurb for EVERY team, ordered by power ranking. 3-5 superlatives."""


def build_digest(league: dict) -> str:
    meta = league["meta"]
    teams = {t["team_key"]: t for t in league["teams"]}
    lines = [
        f"League: {meta['name']} | Season {meta['season']} | Current week: {meta['current_week']}",
        f"FAAB budget: ${meta.get('faab_budget', 100)}",
        "",
        "POWER RANKINGS (rank. team | manager | record | PF/PA | all-play | luck | streak | FAAB left | moves):",
    ]
    for r in league["power_rankings"]:
        t = teams.get(r["team_key"], {})
        move = f"({'+' if r['movement'] > 0 else ''}{r['movement']})" if r.get("movement") else "(–)"
        luck = r.get("luck_index", 0)
        luck_s = "LUCKY" if luck > 0.08 else ("ROBBED" if luck < -0.08 else "fair")
        lines.append(
            f"{r['rank']}. {move} {t.get('name')} | {t.get('manager')} | "
            f"{t.get('wins')}-{t.get('losses')}-{t.get('ties')} | "
            f"PF {t.get('points_for')} PA {t.get('points_against')} | "
            f"all-play {r.get('all_play')} ({luck_s}) | streak {t.get('streak') or '-'} | "
            f"FAAB ${t.get('faab_balance')} | {t.get('moves')} moves"
        )

    cw = meta["current_week"]
    recent = [m for m in league.get("matchups", []) if m.get("status") == "postevent" and m["week"] >= cw - 1]
    if recent:
        lines += ["", "RECENT MATCHUP RESULTS:"]
        for m in recent[-12:]:
            a, b = m["teams"]
            lines.append(f"Week {m['week']}: {a['name']} {a['points']} vs {b['name']} {b['points']}")

    top_bids = league.get("faab", {}).get("top_bids", [])
    if top_bids:
        lines += ["", "BIGGEST FAAB BIDS OF THE SEASON:"]
        for b in top_bids[:8]:
            lines.append(f"${b['bid']} — {b['team_name']} on {b['player']}")

    txns = league.get("transactions", [])[:15]
    if txns:
        lines += ["", "RECENT TRANSACTIONS:"]
        for tx in txns:
            adds = ", ".join(f"+{a['player']} ({a['position']})" for a in tx["adds"])
            drops = ", ".join(f"-{d['player']}" for d in tx["drops"])
            bid = f" [${tx['faab_bid']} FAAB]" if tx.get("faab_bid", -1) > 0 else ""
            who = (tx["adds"] or tx["drops"] or [{}])[0].get("team_name", "")
            lines.append(f"{who}: {adds} {drops}{bid}".strip())

    return "\n".join(lines)


def call_claude(digest: str, week: int) -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("Missing ANTHROPIC_API_KEY")

    payload = {
        "model": MODEL,
        "max_tokens": 4000,
        "system": SYSTEM_PROMPT,
        "messages": [{
            "role": "user",
            "content": f"Write the Week {week} roast column. Here is the full league stats digest:\n\n{digest}",
        }],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
    text = "".join(b.get("text", "") for b in data.get("content", []))

    # tolerate accidental markdown fences
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def main() -> None:
    if not LEAGUE_FILE.exists():
        sys.exit("data/league.json not found — run fetch_yahoo.py first.")
    league = json.loads(LEAGUE_FILE.read_text())
    meta = league["meta"]

    if meta.get("demo"):
        print("Demo data — skipping roast generation.")
        return

    # Roast the most recently COMPLETED week
    completed_weeks = sorted({m["week"] for m in league.get("matchups", []) if m.get("status") == "postevent"})
    if not completed_weeks:
        print("No completed weeks yet — season hasn't started. Skipping roast.")
        return
    week = completed_weeks[-1]

    existing = league.get("roast", {})
    if existing.get("week") == week and not os.environ.get("FORCE_ROAST"):
        print(f"Week {week} roast already exists — skipping (set FORCE_ROAST=1 to regenerate).")
        return

    print(f"Generating week {week} roast with {MODEL} ...")
    digest = build_digest(league)
    roast = call_claude(digest, week)
    roast["week"] = week
    roast["generated_at"] = datetime.now(timezone.utc).isoformat()

    league["roast"] = roast
    LEAGUE_FILE.write_text(json.dumps(league, indent=1))
    print(f"Roast written: “{roast.get('headline', '')}”")


if __name__ == "__main__":
    main()
