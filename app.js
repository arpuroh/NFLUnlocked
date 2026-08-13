/* ══════════════════════════════════════════════════════════════
   NFL UNLOCKED — shared runtime
   Loads data/league.json, paints chrome, renders whichever page
   is declared via <body data-page="...">.
   ══════════════════════════════════════════════════════════════ */

const NU = (() => {
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) =>
    String(s ?? "").replace(/[&<>"']/g, (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const NAV = [
    ["index.html",     "This Week",     "home"],
    ["rankings.html",  "Rankings",      "ranks"],
    ["scoreboard.html","Scoreboard",    "scores"],
    ["team.html",      "Teams",         "team"],
    ["feed.html",      "The Feed",      "feed"],
    ["hall.html",      "Hall of Shame", "hall"],
  ];
  const REACTIONS = ["🤡", "🔥", "💀", "😂"];

  /* ── initials for the striped placeholder avatars ─────────── */
  const initials = (name) =>
    String(name || "?")
      .replace(/[^A-Za-z0-9 ]/g, " ")
      .split(/\s+/).filter(Boolean)
      .slice(0, 3).map((w) => w[0].toUpperCase()).join("") || "?";

  const avatar = (t, dark) =>
    `<span class="avatar${dark ? " dark-a" : ""}">${
      t && t.logo ? `<img src="${esc(t.logo)}" alt="">` : `<span>${esc(initials(t && t.name))}</span>`
    }</span>`;

  const ago = (ts) => {
    if (!ts) return "";
    const d = (Date.now() / 1000) - ts;
    if (d < 3600) return `${Math.max(1, Math.round(d / 60))} min ago`;
    if (d < 86400) return `${Math.round(d / 3600)} hrs ago`;
    return new Date(ts * 1000).toLocaleDateString(undefined, { month: "short", day: "numeric" });
  };

  /* ── reaction stamps ────────────────────────────────
     Counts ship in the data file. A click is recorded locally so the
     UI responds instantly; a shared backend can replace `mine()` later
     without touching any of the rendering below.                     */
  const KEY = "nu_reactions_v1";
  const mine = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const setMine = (m) => { try { localStorage.setItem(KEY, JSON.stringify(m)); } catch {} };

  function stamps(id, seed = {}, opts = {}) {
    const m = mine()[id] || {};
    const keys = [...new Set([...Object.keys(seed), ...Object.keys(m)])]
      .filter((k) => (seed[k] || 0) + (m[k] ? 1 : 0) > 0)
      .sort((a, b) => (seed[b] || 0) - (seed[a] || 0));
    const shown = keys.length ? keys : REACTIONS.slice(0, opts.min || 0);
    return `<span class="stamps" data-react="${esc(id)}">${
      shown.map((k) => {
        const n = (seed[k] || 0) + (m[k] ? 1 : 0);
        return `<button class="stamp${m[k] ? " on" : ""}" data-e="${esc(k)}">
                  <span class="e">${k}</span><span class="n">${n}</span></button>`;
      }).join("")
    }<button class="stamp-add" data-add="1">+</button></span>`;
  }

  function wireStamps(root = document) {
    $$(".stamps", root).forEach((box) => {
      if (box.dataset.wired) return;
      box.dataset.wired = "1";
      box.addEventListener("click", (ev) => {
        const add = ev.target.closest("[data-add]");
        const btn = ev.target.closest(".stamp");
        const id = box.dataset.react;
        const m = mine();
        m[id] = m[id] || {};

        if (add) {
          const used = new Set($$(".stamp .e", box).map((e) => e.textContent));
          const next = REACTIONS.find((r) => !used.has(r));
          if (!next) return;
          m[id][next] = 1; setMine(m);
          const b = document.createElement("button");
          b.className = "stamp on";
          b.dataset.e = next;
          b.innerHTML = `<span class="e">${next}</span><span class="n">1</span>`;
          box.insertBefore(b, box.querySelector("[data-add]"));
          return;
        }
        if (!btn) return;
        const e = btn.dataset.e;
        const nEl = btn.querySelector(".n");
        const n = parseInt(nEl.textContent, 10) || 0;
        if (m[id][e]) { delete m[id][e]; btn.classList.remove("on"); nEl.textContent = Math.max(0, n - 1); }
        else { m[id][e] = 1; btn.classList.add("on"); nEl.textContent = n + 1; }
        setMine(m);
      });
    });
  }

  /* ── page chrome ──────────────────────────────────── */
  function chrome(meta, page) {
    const live = meta.current_week ? `Week ${meta.current_week} · Live` : "Preseason";
    $("#masthead").innerHTML = `
      <div class="inner">
        <a class="wordmark" href="index.html">NFL Unlocked <i></i></a>
        <nav class="mnav">${NAV.map(([h, l, k]) =>
          `<a href="${h}" class="${k === page ? "on" : ""}">${l}</a>`).join("")}</nav>
        <div class="mhead-right">
          <span class="league-id">Yahoo · ${esc(meta.league_id || "675504")}</span>
          <span class="badge-live">${esc(live)}</span>
        </div>
      </div>`;

    // The masthead nav is hidden under 900px, so this bar is the only way around
    // the site on a phone — the Trophy Room and the Hall of Shame belong in it.
    const tabs = [["index.html","Home","home"],["rankings.html","Ranks","ranks"],
                  ["scoreboard.html","Scores","scores"],["feed.html","Feed","feed"],
                  ["trophy.html","Trophy","trophy"],["hall.html","Shame","hall"]];
    const mt = document.createElement("nav");
    mt.className = "mobile-tabs";
    mt.innerHTML = tabs.map(([h, l, k]) =>
      `<a href="${h}" class="${k === page ? "on" : ""}">${l}</a>`).join("");
    document.body.appendChild(mt);

    if (meta.demo) {
      const bar = document.createElement("div");
      bar.className = "demo-bar";
      bar.innerHTML = `Demo data — <a href="setup.html">connect the Yahoo league</a> to go live`;
      document.body.insertBefore(bar, document.body.firstChild);
    }
  }

  function endband(meta) {
    const upd = meta.last_updated ? new Date(meta.last_updated) : null;
    return `<section class="endband">
      <h2 class="display">No one asked for a permanent record of your bad decisions. You got one anyway.</h2>
      <div class="meta">
        <div>Updated ${upd ? esc(ago(upd.getTime() / 1000)) : "—"}</div>
        <div>Auto-pulled from Yahoo Fantasy</div>
        <div>Roasts by AI · Grudges by you</div>
        <div><a href="setup.html">Commissioner setup</a></div>
      </div>
    </section>`;
  }

  /* ── derived helpers ────────────────────────────────── */
  function derive(L) {
    const teams = Object.fromEntries((L.teams || []).map((t) => [t.team_key, t]));
    const played = (L.matchups || []).filter((m) => m.status === "postevent");
    const weekly = {};
    played.forEach((m) => m.teams.forEach((s) => {
      (weekly[s.team_key] = weekly[s.team_key] || []).push({
        w: m.week, p: s.points, win: m.winner_team_key === s.team_key,
      });
    }));
    Object.values(weekly).forEach((a) => a.sort((x, y) => x.w - y.w));
    const lastWeek = played.length ? Math.max(...played.map((m) => m.week)) : null;
    return { teams, played, weekly, lastWeek };
  }

  async function load() {
    const resp = await fetch("data/league.json", { cache: "no-store" });
    return resp.json();
  }

  return { $, $$, esc, avatar, initials, ago, stamps, wireStamps, chrome,
           endband, derive, load, NAV, REACTIONS };
})();

/* ══════════════════════════════════════════════════════════════
   Page renderers
   ══════════════════════════════════════════════════════════════ */
(async function () {
  const { $, esc, avatar, ago, stamps, wireStamps, chrome, endband, derive, load } = NU;
  const page = document.body.dataset.page;
  let L;
  try { L = await load(); }
  catch { document.getElementById("app").innerHTML =
    `<p class="empty pad">Could not load league data. Poke the commissioner.</p>`; return; }

  const meta = L.meta || {};
  meta.league_id = (meta.league_key || "").split(".").pop() || "675504";
  const { teams, played, weekly, lastWeek } = derive(L);
  const ranks = L.power_rankings || [];
  const roast = L.roast || {};
  const rankOf = Object.fromEntries(ranks.map((r) => [r.team_key, r]));

  chrome(meta, page);

  const teamLink = (k) => `team.html?t=${encodeURIComponent(k)}`;
  const mvChip = (m) =>
    m > 0 ? `<span class="mv up">▲${m}</span>`
    : m < 0 ? `<span class="mv dn">▼${Math.abs(m)}</span>`
    : `<span class="mv eq">—</span>`;

  /* ─────────────────────────── HOME ───────────────────────── */
  if (page === "home") {
    const top5 = ranks.slice(0, 5);
    const allPts = played.flatMap((m) => m.teams.map((s) => s.points));
    const hi = played.flatMap((m) => m.teams).sort((a, b) => b.points - a.points)[0];
    const lo = played.flatMap((m) => m.teams).sort((a, b) => a.points - b.points)[0];
    const topBid = (L.faab?.top_bids || [])[0];
    const fraud = [...ranks].sort((a, b) => (b.luck_index || 0) - (a.luck_index || 0))[0];
    const maxScore = Math.max(1, ...ranks.map((r) => r.score || 0));

    const results = played.filter((m) => m.week === lastWeek);

    $("#app").innerHTML = `
      <section class="dark roast-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">The Roast · Wk ${esc(roast.week ?? "—")}</span>
              <span class="eyebrow">${roast.generated_at
                ? `Filed ${esc(new Date(roast.generated_at).toLocaleString(undefined,{weekday:"short",hour:"numeric",minute:"2-digit"}))} by the Executioner`
                : "Awaiting the Executioner"}</span>
            </div>
            <h1 class="display">${roast.headline
              ? esc(roast.headline).replace(/\(([^)]+)\)/, '<span class="kick">($1)</span>')
              : "The season has not started. Enjoy the silence."}</h1>
            <p class="lede">${esc(roast.intro || "Once the Yahoo league is connected, a fresh column lands here every Tuesday morning.")}</p>
            <div class="hero-actions">
              <a class="btn-red" href="feed.html">Read the full column →</a>
              ${stamps("roast-" + (roast.week ?? 0), roast.reactions || {}, { min: 3 })}
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">The Board · Top 5</div>
            ${top5.map((r) => {
              const t = teams[r.team_key] || {};
              return `<a class="board-row" href="${teamLink(r.team_key)}">
                <span class="bn">${r.rank}</span>
                <span class="bt">${esc(t.name || "")}</span>
                <span class="bm ${r.movement > 0 ? "up" : r.movement < 0 ? "dn" : ""}">${
                  r.movement > 0 ? "▲ " + r.movement : r.movement < 0 ? "▼ " + Math.abs(r.movement) : "—"}</span>
              </a>`;
            }).join("") || `<p class="empty">Rankings land after Week 1.</p>`}
            <a class="see-all" href="rankings.html">See all ${(L.teams || []).length} →</a>
          </div>
        </div>
      </section>

      <section class="statbug">
        <div class="cell"><div class="eyebrow">Highest Wk ${esc(lastWeek ?? "—")}</div>
          <div class="v">${hi ? hi.points.toFixed(1) : "—"}</div><div class="s">${esc(hi?.name || "")}</div></div>
        <div class="cell"><div class="eyebrow">Lowest Wk ${esc(lastWeek ?? "—")}</div>
          <div class="v red">${lo ? lo.points.toFixed(1) : "—"}</div><div class="s">${esc(lo?.name || "")}</div></div>
        <div class="cell"><div class="eyebrow">Biggest FAAB Burn</div>
          <div class="v">${topBid ? "$" + topBid.bid : "—"}</div><div class="s">${esc(topBid?.team_name || "")}</div></div>
        <div class="cell"><div class="eyebrow">Luckiest Fraud</div>
          <div class="v">${fraud ? (fraud.luck_index > 0 ? "+" : "") + fraud.luck_index.toFixed(3) : "—"}</div>
          <div class="s">${esc(teams[fraud?.team_key]?.name || "")}</div></div>
      </section>

      <div class="body-grid">
        <div class="col-main">
          <div class="sec-top"><h2 class="h-sec">Power Rankings</h2>
            <span class="note">Not the standings — the truth</span></div>
          <hr class="rule-h">
          ${ranks.map((r) => {
            const t = teams[r.team_key] || {};
            return `<a class="pr-row" href="${teamLink(r.team_key)}">
              <span class="pr-rank"><b>${r.rank}</b>${mvChip(r.movement)}</span>
              ${avatar(t)}
              <span class="pr-team">
                <span class="nm">${esc(t.name || "")}</span>
                <span class="mg">${esc(t.manager || "")} · ${t.wins}-${t.losses}${t.ties ? "-" + t.ties : ""} · ${esc(t.streak || "—")}</span>
              </span>
              <span class="pr-stats">
                <span class="stat-cell"><span class="k">Pts For</span><span class="v">${Number(t.points_for || 0).toFixed(1)}</span></span>
                <span class="stat-cell"><span class="k">All-Play</span><span class="v">${esc(r.all_play || "—")}</span></span>
                <span class="stat-cell"><span class="k">Power</span>
                  <span class="power-bar"><i style="width:${((r.score || 0) / maxScore * 100).toFixed(1)}%"></i></span></span>
              </span>
            </a>`;
          }).join("") || `<p class="empty">No rankings yet.</p>`}

          <div class="sec-top" style="margin-top:30px"><h2 class="h-sec">Week ${esc(lastWeek ?? "—")} Results</h2>
            <span class="note">Final</span></div>
          <hr class="rule-h">
          ${results.length ? `<div class="results-grid">${results.map((m) => {
            const [a, b] = [...m.teams].sort((x, y) => y.points - x.points);
            return `<div class="mu-cell">
              <div class="mu-side"><span class="n">${esc(a.name)}</span><span class="p">${a.points.toFixed(1)}</span></div>
              <div class="mu-side lost"><span class="n">${esc(b.name)}</span><span class="p">${b.points.toFixed(1)}</span></div>
              <div class="margin">Margin ${(a.points - b.points).toFixed(1)}</div>
            </div>`;
          }).join("")}</div>` : `<p class="empty">No completed matchups yet.</p>`}
        </div>

        <div class="col-side">
          <div class="mod">
            <h2 class="h-sec">Superlatives</h2><hr class="rule-h">
            ${(roast.superlatives || []).map((s) => `<div class="sup">
              <div class="award">${esc(s.award)}</div>
              <div class="who">${esc(s.team_name)}</div>
              <div class="note">${esc(s.note)}</div></div>`).join("")
              || `<p class="empty">Awards drop with the column.</p>`}
          </div>

          ${L.vote ? `<div class="mod">
            <h2 class="h-sec">League Vote</h2><hr class="rule-h">
            <div class="vote-q">${esc(L.vote.question)}</div>
            ${(() => {
              const tot = L.vote.options.reduce((s, o) => s + o.votes, 0) || 1;
              const lead = Math.max(...L.vote.options.map((o) => o.votes));
              return L.vote.options.map((o) => {
                const pct = Math.round(o.votes / tot * 100);
                return `<div class="vote-opt ${o.votes === lead ? "lead" : ""}">
                  <div class="lbl"><span>${esc(o.label)}</span><span>${pct}%</span></div>
                  <div class="vote-track"><i style="width:${pct}%"></i></div></div>`;
              }).join("");
            })()}
            <div class="vote-foot">${esc(L.vote.footnote || "")}</div>
          </div>` : ""}

          <div class="mod">
            <h2 class="h-sec">The Wire</h2><hr class="rule-h">
            ${(L.transactions || []).slice(0, 6).map((tx) => {
              const add = tx.adds[0], drop = tx.drops[0];
              const who = (add || drop || {}).team_name || "";
              return `<div class="wire-row">
                <span class="bid ${tx.faab_bid > 0 ? "" : "zero"}">${tx.faab_bid > 0 ? "$" + tx.faab_bid : "$0"}</span>
                <span>
                  <span class="mv-txt">${add ? "+ " + esc(add.player) + (add.position ? ` (${esc(add.position)}${add.nfl_team ? ", " + esc(add.nfl_team) : ""})` : "")
                    : "− " + esc(drop?.player || "")}</span>
                  <span class="meta">${esc(who)} · ${esc(ago(tx.timestamp))}</span>
                </span></div>`;
            }).join("") || `<p class="empty">No moves yet. Everyone still believes in their draft.</p>`}
          </div>
        </div>
      </div>
      ${endband(meta)}`;
  }

  /* ──────────────────────── RANKINGS ──────────────────────── */
  if (page === "ranks") {
    const maxLuck = Math.max(0.05, ...ranks.map((r) => Math.abs(r.luck_index || 0)));
    $("#app").innerHTML = `
      <section class="dark pr-head">
        <div class="eyebrow">Week ${esc(meta.current_week)} · Model v3 · Updated ${esc(meta.last_updated ? ago(new Date(meta.last_updated).getTime()/1000) : "—")}</div>
        <h1 class="display">Power Rankings</h1>
        <p class="lede">Record, scoring, all-play and recent form — weighted, with luck fully exposed. Your schedule cannot hide you here.</p>
        <div class="weights">
          <div class="w"><div class="eyebrow">Record</div><div class="v">35%</div></div>
          <div class="w"><div class="eyebrow">Scoring</div><div class="v">30%</div></div>
          <div class="w"><div class="eyebrow">All-Play</div><div class="v">20%</div></div>
          <div class="w"><div class="eyebrow">Recent Form</div><div class="v">15%</div></div>
        </div>
      </section>
      <table class="tbl">
        <thead><tr><th>Rk</th><th>Team</th><th>Record</th><th>Pts For</th>
          <th class="hide-s">All-Play</th><th>Luck Index</th></tr></thead>
        <tbody>${ranks.map((r) => {
          const t = teams[r.team_key] || {};
          const v = r.luck_index || 0;
          const w = Math.abs(v) / maxLuck * 50;
          const st = (t.streak || "").toUpperCase();
          return `<tr onclick="location.href='${teamLink(r.team_key)}'" style="cursor:pointer">
            <td><span class="rk"><b>${r.rank}</b>${mvChip(r.movement)}</span></td>
            <td><div style="display:flex;align-items:center;gap:11px">${avatar(t)}
              <div><div class="n">${esc(t.name || "")}</div><div class="m">${esc(t.manager || "")}</div></div></div></td>
            <td><span class="rec">${t.wins}-${t.losses}${t.ties ? "-" + t.ties : ""}</span>
              <span class="strk ${st.startsWith("L") ? "l" : "w"}">${esc(t.streak || "")}</span></td>
            <td><span class="big">${Number(t.points_for || 0).toFixed(1)}</span></td>
            <td class="hide-s"><span class="big">${esc(r.all_play || "—")}</span></td>
            <td><div class="luck">
              <div class="luck-track"><div class="luck-fill ${v >= 0 ? "fraud" : "robbed"}" style="width:${w}%"></div></div>
              <div class="luck-lbl">${v >= 0 ? "+" : ""}${v.toFixed(3)} ${v >= 0.02 ? "fraud" : v <= -0.02 ? "robbed" : "fair"}</div>
            </div></td></tr>`;
        }).join("")}</tbody>
      </table>
      ${endband(meta)}`;
  }

  /* ─────────────────────── SCOREBOARD ─────────────────────── */
  if (page === "scores") {
    const wk = meta.current_week;
    let games = (L.matchups || []).filter((m) => m.week === wk);
    let label = `Week ${wk} Scoreboard`;
    if (!games.length && lastWeek) { games = played.filter((m) => m.week === lastWeek); label = `Week ${lastWeek} Scoreboard`; }
    const anyLive = games.some((m) => m.status && m.status !== "postevent");

    document.body.classList.add("dark");
    $("#app").innerHTML = `
      <section class="dark">
        <div class="sb-head">
          <div>
            <div class="${anyLive ? "live-dot" : "eyebrow"}">${anyLive
              ? `Live · ${esc(new Date().toLocaleString(undefined,{weekday:"short",hour:"numeric",minute:"2-digit"}))}`
              : "Final"}</div>
            <h1 class="display">${esc(label)}</h1>
          </div>
          <div class="sb-meta">
            <div>${games.length} matchups</div>
            <div>Auto-refresh · 60s</div>
          </div>
        </div>
        ${games.map((m, i) => {
          const [a, b] = m.teams;
          const ta = teams[a.team_key] || {}, tb = teams[b.team_key] || {};
          const tot = (a.points + b.points) || 1;
          const diff = Math.abs(a.points - b.points);
          const done = m.status === "postevent";
          const state = done ? "Final"
            : diff < 8 ? "Too close"
            : `${esc((a.points > b.points ? a : b).name.split(" ")[0])} +${diff.toFixed(1)}`;
          return `<div class="sb-game">
            <div class="sb-line">
              <div class="sb-team">${avatar(ta, 1)}
                <div><div class="nm">${esc(a.name)}</div>
                  <div class="sub">${done ? "Final" : "In progress"}</div></div></div>
              <div class="sb-score">
                <div class="pts">${a.points.toFixed(1)} — ${b.points.toFixed(1)}</div>
                <div class="state ${done ? "neutral" : ""}">${state}</div>
              </div>
              <div class="sb-team right">
                <div><div class="nm">${esc(b.name)}</div>
                  <div class="sub">${done ? "Final" : "In progress"}</div></div>${avatar(tb, 1)}</div>
            </div>
            <div class="sb-bar">
              <span class="winprob"><i style="width:${(a.points / tot * 100).toFixed(1)}%"></i></span>
              ${stamps(`mu-${m.week}-${i}`, m.reactions || {}, { min: 3 })}
            </div>
          </div>`;
        }).join("") || `<p class="empty pad">No matchups scheduled yet.</p>`}
        <div class="sb-strip">
          <span>${games.length ? "Biggest swing — " + esc([...games].sort((x,y)=>
            Math.abs(y.teams[0].points-y.teams[1].points)-Math.abs(x.teams[0].points-x.teams[1].points))[0].teams[0].name) : "Season pending"}</span>
          <span>Updated ${esc(meta.last_updated ? ago(new Date(meta.last_updated).getTime()/1000) : "—")}</span>
        </div>
      </section>`;
  }

  /* ─────────────────────────── TEAM ───────────────────────── */
  if (page === "team") {
    const q = new URLSearchParams(location.search).get("t");
    const key = q && teams[q] ? q : (ranks[0]?.team_key || (L.teams || [])[0]?.team_key);
    const t = teams[key];
    if (!t) { $("#app").innerHTML = `<p class="empty pad">No teams yet.</p>`; return; }
    const r = rankOf[key] || {};
    const trace = weekly[key] || [];
    // Scale against the league's own range, not zero — otherwise every week
    // looks identical. Floor at 14% so the worst week still reads as a bar.
    const leaguePts = played.flatMap((m) => m.teams.map((s) => s.points));
    const loP = Math.min(...leaguePts, Infinity);
    const hiP = Math.max(...leaguePts, 1);
    const barH = (p) => 14 + 86 * ((p - loP) / ((hiP - loP) || 1));
    const myTx = (L.transactions || []).filter((tx) =>
      [...tx.adds, ...tx.drops].some((p) => p.team_key === key));
    const blurb = (roast.team_blurbs || []).find((b) => b.team_key === key);
    const h2h = {};
    played.forEach((m) => {
      const me = m.teams.find((s) => s.team_key === key);
      const opp = m.teams.find((s) => s.team_key !== key);
      if (!me || !opp) return;
      const o = (h2h[opp.team_key] = h2h[opp.team_key] || { name: opp.name, w: 0, l: 0 });
      m.winner_team_key === key ? o.w++ : o.l++;
    });

    $("#app").innerHTML = `
      <section class="dark team-hero">
        <div class="team-shot">Manager<br>headshot<br>B&amp;W · 1:1</div>
        <div class="body">
          <div class="eyebrow red">Rank ${r.rank ?? "—"} of ${(L.teams||[]).length} · ${
            r.movement > 0 ? "▲" + r.movement : r.movement < 0 ? "▼" + Math.abs(r.movement) : "no move"
          } this week · Manager: ${esc(t.manager || "")}</div>
          <h1 class="display">${esc(t.name)}</h1>
          <div class="team-stats">
            <div class="c"><div class="eyebrow">Record</div><div class="v">${t.wins}-${t.losses}${t.ties ? "-" + t.ties : ""}</div></div>
            <div class="c"><div class="eyebrow">Pts For</div><div class="v">${Number(t.points_for||0).toFixed(1)}</div></div>
            <div class="c"><div class="eyebrow">Streak</div><div class="v ${String(t.streak||"").startsWith("L") ? "red" : ""}">${esc(t.streak || "—")}</div></div>
            <div class="c"><div class="eyebrow">Moves</div><div class="v">${t.moves ?? 0}</div></div>
            <div class="c"><div class="eyebrow">FAAB Left</div><div class="v ${(t.faab_balance ?? 0) <= 10 ? "red" : ""}">$${Math.max(0, t.faab_balance ?? 0)}</div></div>
          </div>
        </div>
      </section>

      <div class="body-grid">
        <div class="col-main">
          <h2 class="h-sec">Season Trace</h2><hr class="rule-h">
          ${trace.length ? `<div class="trace">${trace.map((x) => `
            <div class="b ${x.win ? "" : "loss"}">
              <div class="val">${Math.round(x.p)}</div>
              <div class="bar" style="height:${barH(x.p).toFixed(1)}%"></div>
              <div class="wl">${x.win ? "W" : "L"}</div>
            </div>`).join("")}</div>` : `<p class="empty">No games played yet.</p>`}

          <h2 class="h-sec" style="margin-top:30px">Transaction Rap Sheet</h2><hr class="rule-h">
          ${myTx.length ? myTx.slice(0, 10).map((tx) => {
            const add = tx.adds.find((p) => p.team_key === key);
            const drop = tx.drops.find((p) => p.team_key === key);
            return `<div class="rap-row">
              <span class="amt ${tx.faab_bid > 0 ? "" : "zero"}">$${Math.max(0, tx.faab_bid)}</span>
              <span><span class="t">${add ? "Added " + esc(add.player) + (add.position ? ` (${esc(add.position)}${add.nfl_team ? ", " + esc(add.nfl_team) : ""})` : "") : "Dropped " + esc(drop?.player || "")}</span>
                <span class="s">${add && drop ? "Dropped " + esc(drop.player) : "No replacement claimed"}</span></span>
              <span class="when">${esc(ago(tx.timestamp))}</span></div>`;
          }).join("") : `<p class="empty">A clean sheet. Suspicious.</p>`}
        </div>

        <div class="col-side">
          ${blurb ? `<div class="callout mod">
            <div class="eyebrow red">What the Executioner said · Wk ${esc(roast.week)}</div>
            <h3>${esc(blurb.title)}</h3>
            <p>${esc(blurb.body)}</p>
            ${stamps("blurb-" + key, blurb.reactions || {}, { min: 3 })}
          </div>` : ""}

          <div class="mod">
            <h2 class="h-sec">Head to Head</h2><hr class="rule-h">
            ${Object.values(h2h).length ? Object.values(h2h).map((o) => `
              <div class="h2h-row"><span>${esc(o.name)}</span>
                <span class="r ${o.w < o.l ? "bad" : ""}">${o.w}-${o.l}</span></div>`).join("")
              : `<p class="empty">No history yet.</p>`}
          </div>

          <div class="mod">
            <h2 class="h-sec">Trophy Case</h2><hr class="rule-h">
            <div class="trophies">
              ${(t.trophies || []).map((x) => `<span class="trophy">${esc(x)}</span>`).join("")}
              ${(r.rank === (L.teams||[]).length) ? `<span class="trophy bad">Current Basement</span>` : ""}
              ${(t.faab_balance ?? 100) <= 10 ? `<span class="trophy bad">FAAB Arsonist</span>` : ""}
              ${!(t.trophies||[]).length && (r.rank !== (L.teams||[]).length) && (t.faab_balance ?? 100) > 10
                ? `<span class="trophy">Nothing yet</span>` : ""}
            </div>
          </div>

          <div class="mod">
            <h2 class="h-sec">Switch Team</h2><hr class="rule-h">
            ${ranks.map((x) => `<div class="h2h-row"><a href="${teamLink(x.team_key)}">${esc(teams[x.team_key]?.name || "")}</a>
              <span class="r">#${x.rank}</span></div>`).join("")}
          </div>
        </div>
      </div>
      ${endband(meta)}`;
  }

  /* ─────────────────────────── FEED ───────────────────────── */
  if (page === "feed") {
    const items = L.feed || [];
    const clown = L.most_clowned || [];
    const render = (filter) => items
      .filter((i) => filter === "all" || i.kind === filter)
      .map((i, n) => `<div class="feed-item">
        <div class="top"><span class="${i.kind === "wire" ? "tag-red" : "tag-ink"}">${esc(i.kind)}</span>
          <span class="when">${esc(ago(i.timestamp))}</span></div>
        <h3>${esc(i.title)}</h3>
        <p>${esc(i.body || "")}</p>
        <div class="foot">${stamps("feed-" + (i.id || n), i.reactions || {}, { min: 3 })}
          <span class="reacted">${i.reacted_by ? esc(i.reacted_by) + " of " + (L.teams||[]).length + " reacted" : ""}</span></div>
      </div>`).join("") || `<p class="empty">Nothing has happened yet. Give it a week.</p>`;

    $("#app").innerHTML = `
      <section class="feed-head">
        <div><div class="eyebrow red">No posting. Only judgement.</div>
          <h1 class="display">The Feed</h1></div>
        <div class="chips">${["all","rankings","wire","roast","scores"].map((c, i) =>
          `<button class="chip ${i === 0 ? "on" : ""}" data-f="${c}">${c}</button>`).join("")}</div>
      </section>
      <div class="body-grid">
        <div class="col-main" id="feed-list">${render("all")}</div>
        <div class="col-side">
          <div class="mod">
            <h2 class="h-sec">Most Clowned</h2><hr class="rule-h">
            ${clown.map((c, i) => `<div class="clown-row"><span class="r">${i + 1}</span>
              <span>${esc(c.team_name)}</span><span class="c">${c.count}</span></div>`).join("")
              || `<p class="empty">Nobody has been clowned yet.</p>`}
            <p class="vote-foot" style="margin-top:12px">Reactions received this week. Resets Tuesday when the column drops.</p>
          </div>
          ${clown[0] ? `<div class="stamp-week">
            <div class="eyebrow red">Stamp of the week</div>
            <div class="big"><span class="e">🤡</span><span class="n">${clown.reduce((s,c)=>s+c.count,0)}</span></div>
            <p>The clown got more use in seven days than the fire did in the whole first half of the season.</p>
          </div>` : ""}
        </div>
      </div>
      ${endband(meta)}`;

    document.querySelector(".chips").addEventListener("click", (e) => {
      const b = e.target.closest(".chip"); if (!b) return;
      document.querySelectorAll(".chip").forEach((c) => c.classList.remove("on"));
      b.classList.add("on");
      $("#feed-list").innerHTML = render(b.dataset.f);
      wireStamps();
    });
  }

  /* ──────────────────── HALL OF SHAME ───────────────────────── */
  if (page === "hall") {
    // Every number on this page now comes out of the league database
    // (data/trophy.json, via hall-review.js). This is just the shell it fills.
    $("#app").innerHTML = `
      <section class="hall-hero">
        <div class="eyebrow">Loading the permanent record…</div>
        <h1 class="display">Hall of Shame</h1>
      </section>
      <div class="hall-stats">
        <div class="c"><div class="eyebrow">Most Saccos</div>
          <div class="v red">—</div><div class="s">&nbsp;</div></div>
        <div class="c"><div class="eyebrow">Most Times Runner-Up</div>
          <div class="v">—</div><div class="s">&nbsp;</div></div>
      </div>
      <div class="pad" style="padding-top:26px;padding-bottom:34px">
        <h2 class="h-sec">All-Time Lows</h2><hr class="rule-h">
        <p class="empty">Reading the archive…</p>
      </div>
      ${endband(meta)}`;
  }

  wireStamps();
})();
