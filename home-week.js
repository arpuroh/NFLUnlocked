/* ══════════════════════════════════════════════════════════════
   HOME — in-season.
   Owns index.html from the moment data/current.json says a week is
   final. Before that, offseason.js / opener.js still own the page,
   so nothing here runs and nothing there needs to change.
   Everything it shows comes from data/current.json (standings,
   rankings, results) and data/week<N>.json (the writing).
   ══════════════════════════════════════════════════════════════ */
(async function () {
  const { $, esc, chrome, endband, stamps, wireStamps } = NU;

  const cur = await fetch("data/current.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  if (!cur || cur.status !== "final") return;          // offseason.js keeps the page

  const [L, W] = await Promise.all([
    fetch("data/league.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({})),
    fetch(`data/week${cur.week}.json`, { cache: "no-store" })
      .then((r) => (r.ok ? r.json() : null)).catch(() => null),
  ]);
  if (!W) return;

  const n1 = (v) => Number(v || 0).toFixed(1);
  const n2 = (v) => Number(v || 0).toFixed(2);
  const T = Object.fromEntries(W.teams.map((t) => [t.team_id, t]));
  const rank = Object.fromEntries(cur.power_rankings.map((r) => [r.team_id, r]));
  const link = (t) => `team.html?t=${encodeURIComponent(t.team_key)}`;
  const logo = (t, cls) => t && t.logo
    ? `<img class="tlogo${cls ? " " + cls : ""}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";

  const high = W.teams[0];
  const low = W.teams[W.teams.length - 1];
  const totalRegret = W.teams.reduce((s, t) => s + t.regret, 0);
  const luckiest = [...W.teams].sort((a, b) => b.luck - a.luck)[0];
  const M = W.median;
  const board = [...cur.power_rankings].sort((a, b) => a.rank - b.rank).slice(0, 5);
  const maxScore = Math.max(1, ...cur.power_rankings.map((r) => r.score || 0));
  const mv = (m) => m > 0 ? `<span class="mv up">▲${m}</span>`
    : m < 0 ? `<span class="mv dn">▼${Math.abs(m)}</span>` : `<span class="mv eq">—</span>`;

  document.body.dataset.page = "home";
  chrome({ ...(L.meta || {}), league_id: "675504", current_week: cur.week,
           week_label: cur.label }, "home");

  $("#app").innerHTML = `
    <section class="dark roast-hero">
      <div class="hero-grid">
        <div>
          <div class="filed">
            <span class="tag-red">Week ${cur.week} · Final</span>
            <span class="eyebrow">Filed ${esc(new Date(cur.built_at).toLocaleDateString(undefined,
              { weekday: "long", month: "long", day: "numeric" }))}</span>
          </div>
          <h1 class="display">${esc(W.headline)}<span class="kick">${esc(W.kicker)}</span></h1>
          <p class="lede">${esc(W.lede)}</p>
          <div class="hero-actions">
            <a class="btn-red" href="${esc(cur.recap)}">Read the full Week ${cur.week} recap →</a>
            ${stamps(`wk${cur.week}-home`, {}, { min: 3 })}
          </div>
        </div>
        <div class="board">
          <div class="eyebrow">The Board · Top 5</div>
          ${board.map((r) => {
            const t = T[r.team_id] || {};
            return `<a class="board-row" href="${link(t)}">
              <span class="bn">${r.rank}</span>
              <span class="bt">${esc(t.name || "")}</span>
              <span class="bm ${r.movement > 0 ? "up" : r.movement < 0 ? "dn" : ""}">${
                r.movement > 0 ? "▲ " + r.movement : r.movement < 0 ? "▼ " + Math.abs(r.movement) : "—"}</span>
            </a>`;
          }).join("")}
          <a class="see-all" href="rankings.html">See all ${W.teams.length} →</a>
        </div>
      </div>
    </section>

    <section class="statbug">
      <div class="cell"><div class="eyebrow">Highest Wk ${cur.week}</div>
        <div class="v">${n1(high.points)}</div><div class="s">${esc(high.name)}</div></div>
      <div class="cell"><div class="eyebrow">Lowest Wk ${cur.week}</div>
        <div class="v red">${n1(low.points)}</div><div class="s">${esc(low.name)}</div></div>
      <div class="cell"><div class="eyebrow">The Median</div>
        <div class="v">${n2(M.value)}</div><div class="s">${M.beat} of 14 cleared it</div></div>
      <div class="cell"><div class="eyebrow">Left On Benches</div>
        <div class="v">${n1(totalRegret)}</div><div class="s">league-wide, unplayed</div></div>
    </section>

    <div class="body-grid">
      <div class="col-main">
        <div class="sec-top"><h2 class="h-sec">Power Rankings</h2>
          <span class="note">Movement is off the draft model</span></div>
        <hr class="rule-h">
        ${cur.power_rankings.map((r) => {
          const t = T[r.team_id] || {};
          return `<a class="pr-row" href="${link(t)}">
            <span class="pr-rank"><b>${r.rank}</b>${mv(r.movement)}</span>
            ${logo(t) || ""}
            <span class="pr-team">
              <span class="nm">${esc(t.name || "")}</span>
              <span class="mg">${esc(t.manager || "")} · ${esc(t.record)} · ${r.efficiency}% efficient</span>
            </span>
            <span class="pr-stats">
              <span class="stat-cell"><span class="k">Pts For</span><span class="v">${n1(t.points)}</span></span>
              <span class="stat-cell"><span class="k">All-Play</span><span class="v">${esc(r.all_play)}</span></span>
              <span class="stat-cell"><span class="k">Power</span>
                <span class="power-bar"><i style="width:${(r.score / maxScore * 100).toFixed(1)}%"></i></span></span>
            </span>
          </a>`;
        }).join("")}

        <div class="sec-top" style="margin-top:30px"><h2 class="h-sec">Week ${cur.week} Results</h2>
          <span class="note">Final</span></div>
        <hr class="rule-h">
        <div class="results-grid">${W.games.map((g) => {
          const w = T[g.winner], l = T[g.loser];
          return `<div class="mu-cell">
            <div class="mu-side"><span class="n">${esc(w.name)}</span><span class="p">${n1(g.winner_points)}</span></div>
            <div class="mu-side lost"><span class="n">${esc(l.name)}</span><span class="p">${n1(g.loser_points)}</span></div>
            <div class="margin">Margin ${n2(g.margin)} · ${esc(w.record)} / ${esc(l.record)}</div>
          </div>`;
        }).join("")}</div>
        <p style="margin:16px 0 0"><a class="see-all" href="${esc(cur.recap)}">
          Every game, every bench crime, every receipt →</a></p>
      </div>

      <div class="col-side">
        <div class="mod">
          <h2 class="h-sec">Superlatives</h2><hr class="rule-h">
          ${W.awards.slice(0, 4).map((a) => `<div class="sup">
            <div class="award">${esc(a.title)}</div>
            <div class="who">${esc(a.winner)}</div>
            <div class="note">${esc(a.line)}</div></div>`).join("")}
          <a class="see-all" href="${esc(cur.recap)}#awards">All ${W.awards.length} awards →</a>
        </div>

        <div class="mod">
          <h2 class="h-sec">Bench Crimes</h2><hr class="rule-h">
          ${W.bench_crimes.slice(0, 6).map((p) => `<div class="wire-row">
            <span class="bid">${n1(p.pts)}</span>
            <span><span class="mv-txt">${esc(p.name)}</span>
              <span class="meta">${esc(p.team)} · ${p.fa ? "free agent" : "$" + p.cost} · did not start</span></span>
          </div>`).join("")}
          <a class="see-all" href="${esc(cur.recap)}#bench">The full charge sheet →</a>
        </div>
      </div>
    </div>
    ${endband({ last_updated: cur.built_at })}`;

  wireStamps();
})();
