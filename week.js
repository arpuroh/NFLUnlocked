/* ══════════════════════════════════════════════════════════════
   WEEK RECAP — reads data/week<N>.json, which scripts/build_week.py
   writes from the week's real box scores. All prose lives in that
   file (authored in scripts/week_notes.py); nothing is written here.
   week.html?w=2 will render Week 2 the moment data/week2.json exists.
   ══════════════════════════════════════════════════════════════ */
(async function () {
  const { $, esc, chrome, endband, stamps, wireStamps } = NU;
  const app = $("#app");
  const wk = Math.max(1, parseInt(new URLSearchParams(location.search).get("w"), 10) || 1);

  let W;
  try {
    const r = await fetch(`data/week${wk}.json`, { cache: "no-store" });
    if (!r.ok) throw new Error("no file");
    W = await r.json();
  } catch {
    app.innerHTML = `<p class="empty pad" style="padding:40px 30px">
      No recap filed for Week ${wk} yet. It lands the Monday after the games.</p>`;
    return;
  }

  const n1 = (v) => Number(v || 0).toFixed(1);
  const n2 = (v) => Number(v || 0).toFixed(2);
  const T = Object.fromEntries(W.teams.map((t) => [t.team_id, t]));
  const link = (t) => `team.html?t=${encodeURIComponent(t.team_key)}`;
  const logo = (t, cls) => t && t.logo
    ? `<img class="tlogo${cls ? " " + cls : ""}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  const money = (p) => p.fa ? `<span class="cost fa">FA</span>` : `<span class="cost">$${p.cost}</span>`;
  const pos = (p) => `<span class="pos-chip">${esc(p.pos || p.slot || "")}</span>`;

  /* ── derived headline numbers ───────────────────────── */
  const totalRegret = W.teams.reduce((s, t) => s + t.regret, 0);
  const perfect = W.teams.filter((t) => t.efficiency >= 99.95);
  const high = W.teams[0];
  const low = W.teams[W.teams.length - 1];
  const luckiest = [...W.teams].sort((a, b) => b.luck - a.luck)[0];
  const robbed = [...W.teams].sort((a, b) => a.luck - b.luck)[0];
  // Dollars per point only means anything above zero points; a player who never
  // took the field is its own, worse category and gets named on the same line.
  const ppRate = (p) => p.cost / p.pts;
  const worstBuy = W.money_pits.filter((p) => p.pts > 0).sort((a, b) => ppRate(b) - ppRate(a))[0];
  const ghosts = W.money_pits.filter((p) => p.pts <= 0);
  const biggestCrime = W.bench_crimes[0];
  const crimeTeam = T[biggestCrime.team_id];
  const M = W.median;
  const medTeam = (id) => (T[id] || {}).name || "";
  const medNames = (ids) => {
    const n = ids.map(medTeam);
    return n.length < 2 ? (n[0] || "") : n.slice(0, -1).join(", ") + " and " + n[n.length - 1];
  };
  const combined = W.games.map((g) => g.winner_points + g.loser_points);
  const bestGame = Math.max(...combined);

  const tagFor = (g, i) =>
    i === 0 ? "Closest game"
    : i === W.games.length - 1 ? "Biggest beating"
    : (g.winner_points + g.loser_points) === bestGame ? "Highest-scoring game"
    : `Game ${i + 1} of ${W.games.length}`;

  /* ── build ──────────────────────────────────────────── */
  app.innerHTML = `
  <section class="dark wk-hero">
    <div class="hero-grid">
      <div>
        <div class="filed">
          <span class="tag-red">Week ${W.week} · Final</span>
          <span class="eyebrow">${W.season} season · all 14 rosters re-scored</span>
        </div>
        <h1 class="display">${esc(W.headline)}<span class="kick">${esc(W.kicker)}</span></h1>
        <p class="wk-lede">${esc(W.lede)}</p>
        <nav class="wk-jump">
          <a href="#games">The Seven</a>
          <a href="#median">The Median</a>
          <a href="#standings">Standings &amp; Efficiency</a>
          <a href="#bench">Bench Crimes</a>
          <a href="#money">Draft Money</a>
          <a href="#studs">Studs &amp; Duds</a>
          <a href="#awards">Awards</a>
          <a href="#wire">The Wire</a>
        </nav>
      </div>
      <div class="board">
        <div class="eyebrow">Final Scores</div>
        ${[...W.games].sort((a, b) => b.winner_points - a.winner_points).map((g) => {
          const w = T[g.winner], l = T[g.loser];
          return `<a class="board-row wk-bd" href="#games">
            <span class="bt">${esc(w.name)} <em>${esc(w.record)}</em></span>
            <span class="bn">${n1(g.winner_points)}</span>
            <span class="bt lost">${esc(l.name)} <em>${esc(l.record)}</em></span>
            <span class="bm">${n1(g.loser_points)}</span>
          </a>`;
        }).join("")}
        <a class="see-all" href="#standings">Full standings and efficiency →</a>
      </div>
    </div>
  </section>

  <section class="statbug wk-bug5">
    <div class="cell"><div class="eyebrow">The Median</div>
      <div class="v">${n2(M.value)}</div><div class="s">${M.beat} of 14 cleared it</div></div>
    <div class="cell"><div class="eyebrow">League Average</div>
      <div class="v">${n2(W.league_average)}</div><div class="s">model said 105.99 a week</div></div>
    <div class="cell"><div class="eyebrow">Highest Score</div>
      <div class="v">${n2(high.points)}</div><div class="s">${esc(high.name)}</div></div>
    <div class="cell"><div class="eyebrow">Left On Benches</div>
      <div class="v red">${n1(totalRegret)}</div><div class="s">across all 14 teams</div></div>
    <div class="cell"><div class="eyebrow">Perfect Lineups</div>
      <div class="v">${perfect.length}</div>
      <div class="s">${perfect.length ? esc(perfect.map((t) => t.name).join(", ")) : "nobody"}</div></div>
  </section>

  <section class="wk-sec" id="games">
    <div class="sec-top"><h2 class="h-sec">The Seven</h2><span class="note">Closest first</span></div>
    <hr class="rule-h">
  </section>
  <div class="wk-games">
    ${W.games.map((g, i) => {
      const w = T[g.winner], l = T[g.loser];
      return `<article class="wk-game">
        <div class="wk-g-head">
          <span class="wk-g-tag">${esc(tagFor(g, i))}</span>
          <span class="wk-g-margin">Margin ${n2(g.margin)} · ${n1(g.winner_points + g.loser_points)} combined</span>
        </div>
        <div class="wk-g-line">
          <a class="wk-side" href="${link(w)}">${logo(w)}
            <span class="who"><span class="n">${esc(w.name)}</span>
            <span class="m">${esc(w.manager)} · ${esc(w.record)} · ${w.efficiency}% of his own roster</span></span></a>
          <span class="wk-g-score"><b>${n2(g.winner_points)}</b><i>–</i><b class="lose">${n2(g.loser_points)}</b></span>
          <a class="wk-side right lose" href="${link(l)}">${logo(l)}
            <span class="who"><span class="n">${esc(l.name)}</span>
            <span class="m">${esc(l.manager)} · ${esc(l.record)} · left ${n2(l.regret)} on the bench</span></span></a>
        </div>
        <p class="wk-g-note">${esc(g.note)}</p>
        ${stamps(`wk${W.week}-g${i}`, {}, { min: 3 })}
      </article>`;
    }).join("")}
  </div>

  <section class="dark wk-receipt">
    <div class="eyebrow">Receipt of the week</div>
    <h2 class="h-sec">Filed, stamped, permanent.</h2>
    <div class="rcpt">
      <div class="r-cell">
        <div class="r-k">Worst dollar per point</div>
        <div class="r-v">$${ppRate(worstBuy).toFixed(2)}</div>
        <div class="r-s">${esc(worstBuy.name)} cost $${worstBuy.cost} at the auction and
          returned ${n2(worstBuy.pts)} points in ${esc(worstBuy.team)}'s starting lineup.${
          ghosts.length ? ` Unrankable: ${ghosts.map((g) => `${esc(g.name)} ($${g.cost}, ${esc(g.team)})`).join(", ")}
          started and never took the field, which is not a rate, it is a donation.` : ""}</div>
      </div>
      <div class="r-cell">
        <div class="r-k">Most expensive seat on a bench</div>
        <div class="r-v">${n2(biggestCrime.pts)}</div>
        <div class="r-s">${esc(biggestCrime.name)} scored it in street clothes for
          ${esc(biggestCrime.team)}, who left ${n2(crimeTeam.regret)} on the bench in total and
          ${crimeTeam.won
            ? "won by " + n2((W.games.find((g) => g.winner === crimeTeam.team_id) || {}).margin || 0) + " anyway"
            : "lost by " + n2((W.games.find((g) => g.loser === crimeTeam.team_id) || {}).margin || 0)}.</div>
      </div>
    </div>
  </section>

  <section class="wk-sec" id="median">
    <div class="sec-top"><h2 class="h-sec">The Median</h2>
      <span class="note">${n2(M.value)} · the second opponent</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.median)}</p>
  </section>
  <div class="med-cards">
    <div class="med-card"><div class="k">Swept the week</div>
      <div class="v">${M.sweeps.length}</div>
      <div class="s">${esc(medNames(M.sweeps))} went 2-0.</div></div>
    <div class="med-card"><div class="k">Saved by the median</div>
      <div class="v">${M.saved_by_median.length}</div>
      <div class="s">${M.saved_by_median.length
        ? esc(medNames(M.saved_by_median)) + " lost the matchup and cleared the line anyway, so 1-1."
        : "nobody"}</div></div>
    <div class="med-card"><div class="k">Sunk by the median</div>
      <div class="v red">${M.sunk_by_median.length}</div>
      <div class="s">${M.sunk_by_median.length
        ? esc(medNames(M.sunk_by_median)) + " won the matchup and still went 1-1."
        : "nobody"}</div></div>
    <div class="med-card"><div class="k">Swept out</div>
      <div class="v red">${M.swept.length}</div>
      <div class="s">${esc(medNames(M.swept))} went 0-2.</div></div>
  </div>
  <div class="med-chart">
    ${(() => {
      const mx = Math.max(...W.teams.map((t) => Math.abs(t.vs_median))) || 1;
      return W.teams.map((t) => {
        const w = Math.abs(t.vs_median) / mx * 48;
        return `<a class="med-row" href="${link(t)}">
          <span class="med-team">${logo(t, "sm")}<span><span class="n">${esc(t.name)}</span>
            <span class="m">${esc(t.record)} · ${n2(t.points)}</span></span></span>
          <span class="med-track"><i class="${t.beat_median ? "over" : "under"}"
            style="${t.beat_median ? `left:50%;width:${w}%` : `right:50%;width:${w}%`}"></i></span>
          <span class="med-v ${t.beat_median ? "over" : "under"}">${
            t.vs_median > 0 ? "+" : ""}${n2(t.vs_median)}</span>
        </a>`;
      }).join("");
    })()}
  </div>
  <p class="wk-note">With fourteen teams the line sits between the 7th and 8th scores, so
    nobody ties it and the two teams that set it are the two it decides.
    ${esc(medTeam(M.closest_above))} cleared it by
    ${n2(Math.abs((T[M.closest_above] || {}).vs_median))} and
    ${esc(medTeam(M.closest_below))} missed it by
    ${n2(Math.abs((T[M.closest_below] || {}).vs_median))}. Same number, opposite week.</p>

  <section class="wk-sec" id="standings">
    <div class="sec-top"><h2 class="h-sec">Standings &amp; Efficiency</h2>
      <span class="note">One week of evidence</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.standings)}</p>
  </section>
  <div class="wk-table-wrap">
    <table class="tbl">
      <thead><tr>
        <th>#</th><th>Team</th><th class="r">Points</th><th class="r">vs Median</th><th class="r">All-Play</th>
        <th class="r">Lineup Eff.</th><th class="r">Left On Bench</th>
        <th class="r hide-s">Preseason</th><th class="r">Luck</th>
      </tr></thead>
      <tbody>${W.teams.map((t, i) => {
        const clean = t.efficiency >= 99.95;
        const d = (t.pre_rank || 0) - (i + 1);
        return `<tr>
          <td><span class="rk"><b>${i + 1}</b></span></td>
          <td><a href="${link(t)}" style="display:flex;align-items:center;gap:9px">
            ${logo(t, "sm")}<span><span class="n">${esc(t.name)}</span>
            <span class="m">${esc(t.manager)} · ${esc(t.record)}</span></span></a></td>
          <td class="r"><span class="big">${n2(t.points)}</span></td>
          <td class="r"><span class="${t.beat_median ? "up" : "down"}">${
            t.vs_median > 0 ? "+" : ""}${n2(t.vs_median)}</span></td>
          <td class="r"><span class="rec">${esc(t.all_play)}</span></td>
          <td class="r"><span class="big">${t.efficiency}%</span>
            <span class="eff-bar" style="margin-left:auto"><i class="${clean ? "clean" : ""}" style="width:${t.efficiency}%"></i></span></td>
          <td class="r"><span class="${t.regret > 20 ? "down" : "up"}">${n2(t.regret)}</span></td>
          <td class="r hide-s"><span class="m">#${t.pre_rank} · ${n1(t.pre_ppg)}/wk</span><br>
            <span class="${d > 0 ? "up" : d < 0 ? "down" : "m"}">${d > 0 ? "▲" + d : d < 0 ? "▼" + Math.abs(d) : "—"}</span></td>
          <td class="r"><span class="luck">
            <span class="luck-track">${t.luck === 0 ? "" :
              `<span class="luck-fill ${t.luck > 0 ? "fraud" : "robbed"}" style="width:${Math.abs(t.luck) * 50}%"></span>`}</span>
            <span class="luck-lbl">${t.luck > 0 ? "+" : ""}${t.luck.toFixed(3)}</span></span></td>
        </tr>`;
      }).join("")}</tbody>
    </table>
  </div>
  <p class="wk-note">Luck is measured on the head-to-head only, because the median game is
    decided by your own score and nothing else: half this league's weekly schedule luck does
    not exist. On the half that does, ${esc(luckiest.name)} won a matchup with the
    ${ordinal(W.teams.findIndex((t) => t.team_id === luckiest.team_id) + 1)} best score in the
    league, and ${esc(robbed.name)} lost one with the
    ${ordinal(W.teams.findIndex((t) => t.team_id === robbed.team_id) + 1)}. One of those is a
    fraud and one of those got robbed, and neither of them gets to pick which.</p>

  <section class="wk-sec" id="bench">
    <div class="sec-top"><h2 class="h-sec">Bench Crimes</h2>
      <span class="note">${n1(totalRegret)} points, unplayed</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.bench)}</p>
  </section>
  <div class="wk-table-wrap">
    <table class="tbl">
      <thead><tr><th>Player</th><th>Sat For</th><th class="r">Cost</th>
        <th class="r">Points</th><th class="hide-s">Line</th></tr></thead>
      <tbody>${W.bench_crimes.map((p) => `<tr>
        <td>${pos(p)}<span class="n">${esc(p.name)}</span></td>
        <td><span class="m">${esc(p.team)}</span></td>
        <td class="r">${money(p)}</td>
        <td class="r"><span class="big down">${n2(p.pts)}</span></td>
        <td class="hide-s"><span class="stat">${esc(p.stats || "—")}</span></td>
      </tr>`).join("")}</tbody>
    </table>
  </div>

  <section class="wk-sec" id="money">
    <div class="sec-top"><h2 class="h-sec">Draft Money vs One Sunday</h2>
      <span class="note">Unfair on purpose</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.money)}</p>
  </section>
  <div class="wk-two">
    <section>
      <h3 class="h-sec" style="font-size:19px">The Money Pit</h3><hr class="rule-t">
      <div class="wk-list">${W.money_pits.slice(0, 8).map((p) => `<div class="wk-li">
        <span><span class="n">${esc(p.name)}</span>
          <span class="m">$${p.cost} · ${esc(p.team)} · ${p.pts > 0
            ? "$" + (p.cost / p.pts).toFixed(2) + " per point" : "did not play"}</span></span>
        <span class="v bad">${n2(p.pts)}</span></div>`).join("")}</div>
    </section>
    <section>
      <h3 class="h-sec" style="font-size:19px">The Bargain Bin</h3><hr class="rule-t">
      <div class="wk-list">${W.bargains.slice(0, 8).map((p) => `<div class="wk-li">
        <span><span class="n">${esc(p.name)}</span>
          <span class="m">$${p.cost} · ${esc(p.team)} · ${p.started ? "started" : "on the bench"}</span></span>
        <span class="v">${n2(p.pts)}</span></div>`).join("")}</div>
    </section>
  </div>

  <section class="wk-sec" id="studs">
    <div class="sec-top"><h2 class="h-sec">Studs &amp; Duds</h2>
      <span class="note">Against the projection</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.studs)}</p>
  </section>
  <div class="wk-two">
    <section>
      <h3 class="h-sec" style="font-size:19px">Best Starts</h3><hr class="rule-t">
      <div class="wk-list">${W.top_starts.slice(0, 10).map((p) => `<div class="wk-li">
        <span><span class="n">${esc(p.name)}</span>
          <span class="m">${esc(p.team)} · ${p.fa ? "free agent" : "$" + p.cost} ·
            ${p.vs_proj > 0 ? "+" : ""}${n2(p.vs_proj)} vs projection</span></span>
        <span class="v">${n2(p.pts)}</span></div>`).join("")}</div>
    </section>
    <section>
      <h3 class="h-sec" style="font-size:19px">Worst Starts</h3><hr class="rule-t">
      <div class="wk-list">${W.worst_starts.slice(0, 10).map((p) => `<div class="wk-li">
        <span><span class="n">${esc(p.name)}</span>
          <span class="m">${esc(p.team)} · ${p.fa ? "free agent" : "$" + p.cost} ·
            ${n2(p.vs_proj)} vs projection</span></span>
        <span class="v bad">${n2(p.pts)}</span></div>`).join("")}</div>
    </section>
  </div>

  <section class="wk-sec">
    <div class="sec-top"><h2 class="h-sec">Position Weather</h2>
      <span class="note">League-wide starter averages</span></div>
    <hr class="rule-h">
  </section>
  <div class="wk-slots">${Object.entries(W.slot_averages).map(([k, v]) => `
    <div class="wk-slot"><div class="k">${esc(k)}</div>
      <div class="v">${n1(v.avg)}</div>
      <div class="s">${n1(v.high)} hi · ${n1(v.low)} lo</div></div>`).join("")}</div>

  <section class="wk-sec" id="awards">
    <div class="sec-top"><h2 class="h-sec">The Week 1 Awards</h2>
      <span class="note">No trophies, only records</span></div>
    <hr class="rule-h">
  </section>
  <div class="wk-awards">${W.awards.map((a) => `<div class="sup">
    <div class="award">${esc(a.title)}</div>
    <div class="who">${esc(a.winner)}</div>
    <div class="note">${esc(a.line)}</div></div>`).join("")}</div>

  <section class="wk-sec" id="wire">
    <div class="sec-top"><h2 class="h-sec">The Wire</h2>
      <span class="note">Snapshot, not advice</span></div>
    <hr class="rule-h">
    <p class="intro">${esc(W.sections.waivers)}</p>
  </section>
  <div class="wk-table-wrap">
    <table class="tbl">
      <thead><tr><th>Team</th><th class="r">Moves</th><th class="r">FAAB Left</th>
        <th class="r">FAAB Spent</th><th class="hide-s">Best unowned-at-draft starter</th></tr></thead>
      <tbody>${[...W.teams].sort((a, b) => b.moves - a.moves || b.faab_left - a.faab_left)
        .map((t) => {
          const fa = [...t.starters, ...t.bench].filter((p) => p.fa)
            .sort((a, b) => b.pts - a.pts)[0];
          return `<tr>
            <td><a href="${link(t)}" style="display:flex;align-items:center;gap:9px">
              ${logo(t, "sm")}<span><span class="n">${esc(t.name)}</span>
              <span class="m">${esc(t.manager)}</span></span></a></td>
            <td class="r"><span class="big">${t.moves}</span></td>
            <td class="r"><span class="rec">$${t.faab_left}</span></td>
            <td class="r"><span class="${100 - t.faab_left ? "down" : "m"}">$${100 - t.faab_left}</span></td>
            <td class="hide-s"><span class="stat">${fa
              ? esc(fa.name) + " · " + n2(fa.pts) : "none"}</span></td>
          </tr>`;
        }).join("")}</tbody>
    </table>
  </div>
  <p class="wk-note">${esc(W.waiver_note)}</p>

  ${endband({ last_updated: W.built_at })}`;

  function ordinal(n) {
    const s = ["th", "st", "nd", "rd"], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }

  wireStamps();
})();
