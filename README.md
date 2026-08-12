# 🏈 NFL Unlocked

Auto-updating hub for Yahoo fantasy league [675504](https://football.fantasysports.yahoo.com/f1/675504).
Power rankings, a savage weekly roast column, FAAB forensics, reaction stamps and a permanent
record of every bad decision. Nobody touches anything after setup.

**Live:** https://www.nflunlocked.com

**Design:** modernist sports tabloid — Archivo compressed at newspaper scale, red-on-white,
hard 2px rules, zero radius. Dark blocks are reserved for the moments that matter (the roast
hero, the stat-bug strip, the live scoreboard, the roast callout on team pages), so the site
reads bright and loud and darkness means something is happening.

## Pages

| File | What it is |
|---|---|
| `index.html` | This Week — roast hero, top-5 board, stat bug, power rankings, results |
| `rankings.html` | The receipts — full table with the diverging luck index |
| `scoreboard.html` | Live Sunday scoreboard, dark broadcast mode |
| `team.html?t=<team_key>` | The permanent record — season trace, rap sheet, head-to-head, trophies |
| `feed.html` | Reactions, stamps, Most Clowned board |
| `hall.html` | Season history, the ledger, all-time lows |
| `setup.html` | One-time commissioner wiring |

## How it works

```
Yahoo Fantasy API ──▶ GitHub Actions (cron) ──▶ data/league.json ──▶ Vercel auto-deploy
                                                        ▲
                          Claude (Cowork, weekly) ──────┘  writes the roast column
```

- `scripts/fetch_yahoo.py` — pulls standings, matchups, transactions and FAAB, computes power
  rankings (record 35% / scoring 30% / all-play 20% / recent form 15%) plus a luck index, and
  builds The Feed. Reactions, the league vote and season history carry forward across runs.
- `.github/workflows/update.yml` — hourly during Sunday games, post-MNF Tuesday, daily baseline.
  Commits the data; Vercel redeploys on push.
- The **roast column** is written by a scheduled Claude Cowork task each Tuesday morning, which
  reads the live data file and pushes the column back. No Anthropic API key, no metered billing.
- `api/auth-*.js` — two serverless functions used only for the one-time Yahoo OAuth handshake.

Everything else is static: no build step, no framework, no runtime dependencies.
Archivo is self-hosted in `fonts/` (SIL OFL), so there is no CDN dependency.

## Reactions

Stamps (🤡 🔥 💀 😂) render from counts in `data/league.json` and record a viewer's own taps in
`localStorage` for instant feedback. To make them league-wide and permanent, point
`stamps()` in `app.js` at a shared store (a KV namespace or a tiny serverless endpoint) —
the rendering layer does not change.

## Setup

Full walkthrough on the site: **/setup**

The Yahoo app must have the **Fantasy Sports · Read** permission. Yahoo removed that option from
newly created apps — apps that predate the change still carry it, and newer ones need approval
via https://sports.yahoo.com/developer/access/. Without it, every league endpoint returns 401.

1. Yahoo app redirect URI → `https://www.nflunlocked.com/api/auth-callback`
2. `YAHOO_CLIENT_ID` / `YAHOO_CLIENT_SECRET` as Vercel env vars, then **redeploy**
   (env var edits do not affect existing deployments)
3. Visit `/setup`, click Connect Yahoo League, copy the refresh token
4. Three GitHub Actions secrets: `YAHOO_CLIENT_ID`, `YAHOO_CLIENT_SECRET`, `YAHOO_REFRESH_TOKEN`
5. Actions → Update league data → Run workflow

## Config

`LEAGUE_ID` (default `675504`), `GAME_CODE` (default `nfl`, resolves to the current season).

## Roast policy

Full savage was a unanimous league vote. Complaints go to the waiver wire.
