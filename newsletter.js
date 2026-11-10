/* ══════════════════════════════════════════════════════════════
   UNLOCKED & LOADED, the weekly newsletter.
   Reads data/weeks.json + data/week<N>.json (built by scripts/build_week.py).
   Every reader owns one of the fourteen teams, so the core of the issue
   is a card per team, in power-ranking order: rank and movement, the
   week, the season, the roast, the award, and who they play next.
   All prose comes from scripts/week_notes.py; nothing is written here.
   newsletter.html?w=8 shows an older issue.
   ══════════════════════════════════════════════════════════════ */
(async function () {
  const { $, $$, esc, endband } = NU;
  const app = $("#app");
  const IDX = await fetch("data/weeks.json", { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);
  const asked = parseInt(new URLSearchParams(location.search).get("w"), 10);
  const wk = asked > 0 ? asked : (IDX && IDX.latest) || 1;

  let W;
  try {
    const r = await fetch(`data/week${wk}.json`, { cache: "no-store" });
    if (!r.ok) throw new Error("no file");
    W = await r.json();
  } catch {
    app.innerHTML = `<p class="empty pad" style="padding:40px 30px">No issue for Week ${wk} yet.
      <a class="see-all" style="color:var(--red)" href="newsletter.html">Latest issue →</a></p>`;
    return;
  }
  document.title = `Unlocked & Loaded, Week ${W.week} | NFL Unlocked`;

  const n2 = (v) => Number(v || 0).toFixed(2);
  const T = Object.fromEntries(W.teams.map((t) => [t.team_id, t]));
  const NL = W.newsletter || {};
  const byName = {};
  (W.awards || []).forEach((a) => { (byName[a.winner] = byName[a.winner] || []).push(a); });
  const opp = {};
  (NL.next || []).forEach(([a, b, line]) => {
    opp[String(a)] = { id: String(b), line };
    opp[String(b)] = { id: String(a), line };
  });
  const ord = (n) => { const x = ["th", "st", "nd", "rd"], v = n % 100; return n + (x[(v - 20) % 10] || x[v] || x[0]); };
  const scoreRank = (id) => W.teams.findIndex((t) => t.team_id === id) + 1;   // teams ship sorted by points
  const mv = (m) => m > 0 ? `<span class="nl-mv up">▲${m}</span>`
    : m < 0 ? `<span class="nl-mv dn">▼${-m}</span>` : `<span class="nl-mv eq">=</span>`;
  const badge = (t) => `<span class="nl-badge">${t.logo ? `<img src="${esc(t.logo)}" alt="" loading="lazy">`
    : `<b>${esc(NU.initials(t.name))}</b>`}</span>`;

  const games = [...(W.games || [])];
  const closest = games[0], blowout = games[games.length - 1];
  const high = W.teams[0], low = W.teams[W.teams.length - 1];
  const worstBuy = [...(W.faab_audit || [])].filter((a) => a.bid > 0 && a.started)
    .sort((a, b) => (a.pts / a.bid) - (b.pts / b.bid))[0];
  const bench = (W.bench_crimes || [])[0];
  const M = W.median || {};

  const issues = IDX ? IDX.weeks : [{ week: W.week }];
  const SAVE = "nu_my_team";
  const getMine = () => { try { return localStorage.getItem(SAVE) || ""; } catch { return ""; } };
  const setMine = (v) => { try { localStorage.setItem(SAVE, v); } catch {} };

  const card = (r) => {
    const t = T[r.team_id], s = t.season || {};
    const aw = byName[t.name] || [];
    const nx = opp[t.team_id], o = nx && T[nx.id];
    const res = t.wins === 2 ? "win" : t.wins === 0 ? "loss" : "split";
    return `<article class="nl-card" id="t${t.team_id}" data-team="${t.team_id}">
      <div class="nl-rank"><span class="nl-rn">${r.rank}</span>${mv(r.movement)}</div>
      <div class="nl-body">
        <header class="nl-head">${badge(t)}
          <div><h3>${esc(t.name)}</h3><span class="nl-mgr">${esc(t.manager)} · ${esc(s.record)} · ${esc(s.points_for != null ? n2(s.points_for) : "")} PF</span></div>
        </header>
        <div class="nl-week">
          <span class="nl-res ${res}">${esc(t.record)}</span>
          <span><b class="num">${n2(t.points)}</b> pts, ${ord(scoreRank(t.team_id))} of 14</span>
          <span>${t.efficiency.toFixed(1)}% lineup</span>
          <span>${t.vs_median >= 0 ? "+" : ""}${n2(t.vs_median)} vs median</span>
        </div>
        ${r.blurb ? `<p class="nl-roast">${esc(r.blurb)}</p>` : ""}
        ${aw.map((a) => `<div class="nl-award"><span class="tag-red">${esc(a.title)}</span><p>${esc(a.line)}</p></div>`).join("")}
        ${o ? `<div class="nl-next"><span class="eyebrow">Week ${W.week + 1}</span> vs <b>${esc(o.name)}</b> (${esc((o.season || {}).record || "")})</div>` : ""}
      </div>
    </article>`;
  };

  app.innerHTML = `
  <section class="dark nl-hero">
    <div class="nl-flag">
      <span class="nl-name">Unlocked <i>&amp;</i> Loaded</span>
      <span class="nl-issue">The NFL Unlocked weekly · Issue ${W.week}
        ${issues.length > 1 ? `<select id="nl-pick" aria-label="Choose an issue">${issues.slice().reverse().map((x) =>
          `<option value="${x.week}" ${x.week === W.week ? "selected" : ""}>Week ${x.week}</option>`).join("")}</select>` : ""}</span>
    </div>
    <h1 class="display nl-h1">${esc(W.headline)}</h1>
    ${NL.intro ? `<p class="nl-intro">${esc(NL.intro)}</p>` : W.kicker ? `<p class="nl-intro">${esc(W.kicker)}</p>` : ""}
    <div class="nl-cta">
      ${W.video && W.video.src ? `<a class="btn-red" href="week.html?w=${W.week}#reel">▶ Watch the roast (${W.video.seconds || 40}s)</a>` : ""}
      <a class="btn-ghost" href="week.html?w=${W.week}">Full recap →</a>
    </div>
  </section>

  <section class="nl-find" aria-label="Find your team">
    <span class="eyebrow">Find your team</span>
    <div class="nl-chips">${(W.power_rankings || []).map((r) => {
      const t = T[r.team_id];
      return `<a href="#t${t.team_id}" class="nl-chip" data-pick="${t.team_id}">${esc(t.manager)}</a>`;
    }).join("")}</div>
  </section>

  <section class="nl-quick">
    <div><span class="eyebrow">High</span><b class="num">${n2(high.points)}</b><span>${esc(high.name)}</span></div>
    <div><span class="eyebrow">Low</span><b class="num red">${n2(low.points)}</b><span>${esc(low.name)}</span></div>
    <div><span class="eyebrow">Median</span><b class="num">${n2(M.value)}</b><span>${M.beat} of 14 cleared it</span></div>
    ${closest ? `<div><span class="eyebrow">Closest</span><b class="num">${n2(closest.margin)}</b><span>${esc(T[closest.winner].name)} over ${esc(T[closest.loser].name)}</span></div>` : ""}
    ${blowout ? `<div><span class="eyebrow">Blowout</span><b class="num">${n2(blowout.margin)}</b><span>${esc(T[blowout.winner].name)} over ${esc(T[blowout.loser].name)}</span></div>` : ""}
    ${bench ? `<div><span class="eyebrow">Bench crime</span><b class="num red">${n2(bench.pts)}</b><span>${esc(bench.name)}, ${esc(bench.team)}</span></div>` : ""}
    ${worstBuy ? `<div><span class="eyebrow">Worst buy</span><b class="num red">$${worstBuy.bid}</b><span>${esc(worstBuy.player)}: ${n2(worstBuy.pts)} pts</span></div>` : ""}
  </section>

  <section class="nl-sec">
    <h2 class="display">The Fourteen</h2>
    <p class="nl-dek">Power-ranking order. One roast, every award, and who you play next.</p>
    <div class="nl-list">${(W.power_rankings || []).map(card).join("")}</div>
  </section>

  ${(NL.next || []).length ? `<section class="nl-sec">
    <h2 class="display">Week ${W.week + 1}</h2>
    <div class="nl-games">${NL.next.map(([a, b, line]) => {
      const A = T[String(a)], B = T[String(b)];
      return `<div class="nl-game"><div class="nl-vs"><b>${esc(A.name)}</b> <em>${esc((A.season || {}).record)}</em>
        <span>vs</span> <b>${esc(B.name)}</b> <em>${esc((B.season || {}).record)}</em></div>
        <p>${esc(line)}</p></div>`;
    }).join("")}</div>
  </section>` : ""}

  ${W.waiver_note ? `<section class="nl-sec nl-wire"><span class="eyebrow">Waivers</span><p>${esc(W.waiver_note)}</p></section>` : ""}

  ${endband({ last_updated: W.built_at })}`;

  const pick = $("#nl-pick");
  if (pick) pick.addEventListener("change", () => { location.href = `newsletter.html?w=${pick.value}`; });

  // "Find your team": remember the reader's team on this device and mark it.
  const mark = (id) => {
    $$(".nl-card").forEach((c) => c.classList.toggle("mine", c.dataset.team === id));
    $$(".nl-chip").forEach((c) => c.classList.toggle("on", c.dataset.pick === id));
  };
  $$(".nl-chip").forEach((c) => c.addEventListener("click", () => { setMine(c.dataset.pick); mark(c.dataset.pick); }));
  const mine = getMine();
  if (mine && T[mine]) mark(mine);
})();
