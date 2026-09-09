# NFL Unlocked

Static site for a 14-team Yahoo fantasy football league. Live at **nflunlocked.com**
(Vercel, git-connected to `main` — push to `main` and it is live in ~30s).

No build step. No framework. Plain HTML + one CSS file per feature + vanilla JS.
Do not introduce a bundler, a framework, or a package.json without being asked.

## Layout

| Path | What it is |
|---|---|
| `index.html` | This Week |
| `rankings.html` `scoreboard.html` `team.html` `feed.html` | league pages (`team.html?t=<team_key>`) |
| `hall.html` `trophy.html` | Hall of Shame, Trophy Room |
| `roast.html` + `roast.js` + `roast.css` | Roast Roulette, incl. the suggestion box |
| `draft.html` + `draft.js` + `draft.css` | Draft Central: auction ledger, grades, preseason rankings. Three states from data alone: pending / complete / graded |
| `app.js` `styles.css` | shared shell: masthead, nav, formatting helpers |
| `data/*.json` | all content. `league.json` is machine-written; the rest are hand-authored |
| `scripts/fetch_yahoo.py` | Actions cron → rewrites `data/league.json` |
| `scripts/generate_roasts.py` | Claude API → weekly roast headline |
| `scripts/fetch_draft.py` | public Yahoo draft-results page → `data/draft.json` (no OAuth; the league is public). `--fixture` rebuilds `data/draft_2025.json` from `data/draft_2025.txt` |
| `scripts/project_draft.py` | Sleeper 2026 projections re-scored under this league's rules → `data/projections.json`. **This is what the power rankings are built on.** `--refresh` re-downloads the feed |
| `scripts/generate_draft_grades.py` | `data/draft.json` → `data/draft_grades.json` via the Claude API. Grades live apart from the ledger so a re-scrape never clobbers the writing |
| `.github/workflows/draft.yml` | polls the draft page every 15 min on draft night; `workflow_dispatch` any time |
| `.github/workflows/update.yml` | the cron |

Each page is a thin shell: `<header class="masthead">` + `<main id="app">`, filled in by JS
that fetches from `data/`. Follow that pattern for new pages rather than writing static markup.

## Design system — non-negotiable

Modernist sports tabloid. Archivo (self-hosted in `fonts/`, **never** add a Google Fonts link),
compressed at newspaper scale, hard 2px rules, **zero border radius anywhere**.

```
ink #201E1D   ink-2 #444141   gray #605D5D    gray-mid #7D7979
gray-soft #9B9797   gray-faint #BAB6B6   rule #D7D3D3
fill #EAE9E9   paper #F3F2F2   page #EFEDE8
red #EC3013   red-bright (on dark only) #FF563C   red-deep #AE1800
```

Dark blocks are reserved for "something is happening": the roast hero, the stat-bug strip,
the live scoreboard, the roast callout on team pages, the suggestion box. Do not make a
section dark just for variety.

Form controls on dark: `#2B2928` fill, `#4A4645` 2px border, red-bright focus ring,
and **16px font on phones** so iOS does not zoom on focus. `.rr-form` in `roast.css` is
the reference implementation.

## Roast tone

Full savage, but **fantasy decisions only** — drafts, trades, lineups, waiver crimes.
Never anybody's real life, job, family or appearance. This applies to generated roasts,
to `data/roasts.json`, and to anything promoted out of the suggestion box.

## Suggestion box → Supabase

`roast.js` posts to Supabase project `nfl-unlocked` (`zajaumqfompslmgoohxv`).
The `sb_publishable_…` key in the source is **meant to be public**. Safety lives in the
database, not the key: `anon` has INSERT on four columns only (`target_key`, `target_name`,
`joke`, `author`) — no SELECT, no UPDATE, no DELETE, and `status` is not grantable so nobody
can approve their own line. A BEFORE INSERT trigger rejects a 21st row in any minute and
exact duplicate jokes inside 10 minutes.

Read submissions in the Supabase dashboard → table `roast_suggestions`. Promoting an
approved line into `data/roasts.json` is currently manual.

**If you add another shared-state feature (reactions, votes), copy this pattern:**
column-level GRANT + RLS insert-only + a trigger, and `revoke execute` on the trigger
function or the security advisor flags it as a callable RPC.

## Known broken — do not assume these work

1. **`update.yml` never generates roasts.** It runs `fetch_yahoo.py` only;
   `generate_roasts.py` has its own `main()` and is never invoked, so the marquee headline
   freezes while scores keep moving. Needs a second step plus an `ANTHROPIC_API_KEY` secret.
2. **Yahoo OAuth is failing silently.** `main()` falls back to `scrape_league()` when the
   token refresh fails, and the scrape path hardcodes `"week": 0` on every matchup. That
   makes recent-form rankings meaningless and makes the roast generator fire exactly once,
   ever. `data/league.json` showing `league_key: "scrape.l.675504"` is the tell.
   Consider gating the fallback behind an explicit `ALLOW_SCRAPE=1` so a broken refresh
   turns the build red instead of green.

## Power rankings: projected points, not dollars

`scripts/project_draft.py` is the model. It pulls Sleeper's public 2026 season projections
(no key needed), re-scores every stat line under this league's actual rules (half PPR, 4-point
passing TDs, kickers paid 1 pt per 10 yards of made FGs, IDP paid on tackles), fits each roster's
best legal lineup, and computes expected points per week. Two rules keep it honest:

1. **Every slot is floored at the waiver wire.** Undrafted players are the free-agent pool, so a
   missing kicker or a starter worse than what is sitting unowned costs nothing. Nobody is
   penalized for a slot they can fill on Tuesday.
2. **Starters miss weeks.** Byes plus position-specific injury rates decide how often, and the
   best bench player at that position covers. That is exactly what depth is worth, no more.

Never rank on money spent. Earlier versions did and were wrong twice: dollar-based ranking had
Hail Mary 14th (projections: 3rd) and Leo the Cleo 12th (projections: 2nd).

## Draft data

`data/draft.json` is machine-written (never hand-edit); `data/draft_grades.json` is the writing,
keyed by team name exactly as Yahoo spells it. `draft.js` carries the team → manager map
(`MANAGERS`) because the public page has team names only; update it when a team renames.
The offseason home page (`offseason.js`) swaps its hero to the draft grades once
`draft.json.status === "complete"`, and links the draft-night stat cell to `draft.html` before that.
Draft time lives in two places: `offseason.js` and `draft.js` (`DRAFT_AT`), both 2026-09-08T23:00Z.

## Testing

There is no test suite. Before pushing a JS change, serve the folder and click it:

```
python3 -m http.server 8000     # then open http://localhost:8000/roast.html
```

Check the console is clean, and check it at 390px wide as well as desktop — most of the
league reads this on a phone.
