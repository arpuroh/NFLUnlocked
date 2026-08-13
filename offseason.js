/* NFL Unlocked — offseason mode.

   Between the final whistle and Week 1 there are no matchups, so the live
   pages have nothing to render: the roast hero, the weekly stat bug and the
   all-play column all bottom out at "—". Rather than show an empty live page
   (or a stale sample column), this takes over the This Week and Rankings pages
   and renders the completed season instead: final standings, season superlatives,
   the champion, and the countdown to the draft.

   It activates only when the league data has no completed matchups, so the
   moment Week 1 kicks off the normal live pages come back with no changes. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const ord = (i) => {
    const s = ["th", "st", "nd", "rd"], v = i % 100;
    return i + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  // Draft night, per the league's Yahoo settings page.
  const DRAFT = new Date("2026-09-08T21:00:00Z");

  function countdown() {
    const ms = DRAFT - new Date();
    if (ms <= 0) return { v: "Live", s: "Draft is underway" };
    const d = Math.floor(ms / 86400000);
    const h = Math.floor((ms % 86400000) / 3600000);
    return { v: d > 0 ? d + "d " + h + "h" : h + "h", s: "Tue Sep 8 · 5:00pm ET" };
  }

  function seasonView(db, rows, year) {
    const byRank = rows.slice().sort((a, b) => a.rank - b.rank);
    // The Sacco is not last place. It is the loser of the three-team Sacco Bowl,
    // resolved in the database; the standings table only decides the seeding.
    const season = (db.seasons || []).find((s) => s.year === year) || {};
    const champ = byRank.find((r) => r.place === 1) || byRank[0];
    const second = byRank.find((r) => r.place === 2);
    const third = byRank.find((r) => r.place === 3);
    // Regular-season order: record first, then points. Yahoo re-ranks the teams
    // that miss the playoffs by how the consolation bracket went, which is not a
    // standing anybody in this league recognises — and it hides the seeding that
    // sends three teams to the Sacco Bowl. This is the order the season was played in.
    const seeded = rows.slice().sort((a, b) =>
      b.wins - a.wins || b.points_for - a.points_for);
    seeded.forEach((r, i) => { r.seed = i + 1; });
    const FIELD = seeded.length >= 14 ? 6 : 4;
    const playoff = seeded.slice(0, FIELD).sort((a, b) => a.rank - b.rank);
    const last = byRank.find((r) => r.team === season.toilet) || byRank[byRank.length - 1];
    const bottom = seeded[seeded.length - 1];
    const hi = rows.slice().sort((a, b) => b.points_for - a.points_for)[0];
    const lo = rows.slice().sort((a, b) => a.points_for - b.points_for)[0];
    const bestRec = rows.slice().sort((a, b) =>
      (b.wins / (b.wins + b.losses)) - (a.wins / (a.wins + a.losses)))[0];
    const busiest = rows.slice().sort((a, b) => b.moves - a.moves)[0];
    const cd = countdown();

    // Robbed: most points, no title.
    const robbed = rows.slice().sort((a, b) => b.points_for - a.points_for)
      .find((r) => r.place !== 1);

    const champions = (db.people || []).filter((p) => p.display && p.rings);
    const repeat = champions.filter((p) => p.rings > 1).sort(byRecency);
    const once = champions.filter((p) => p.rings === 1).sort(byRecency);

    const tableRow = (r, n, cls) => `<div class="row${cls || ""}">
      <span class="rk">${n}</span>
      <span class="tm">${esc(r.team)}</span>
      <span class="mg">${esc(r.manager)}</span>
      <span class="c">${r.wins}-${r.losses}</span>
      <span class="c b">${r.points_for.toFixed(1)}</span>
      <span class="c dim">${r.points_against.toFixed(1)}</span>
      <span class="c dim">${r.moves}</span>
    </div>`;

    const stat = (label, v, s, red) => `<div class="cell">
      <div class="eyebrow">${esc(label)}</div>
      <div class="v${red ? " red" : ""}">${esc(v)}</div>
      <div class="s">${esc(s)}</div></div>`;

    return `
      <section class="dark roast-hero os-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">Offseason</span>
              <span class="eyebrow">${year} season complete · ${rows.length} teams · next kickoff September</span>
            </div>
            <h1 class="display">The ${year} Season Is In The Books
              <span class="kick">(and the receipts are permanent)</span></h1>
            <p class="lede">${esc(champ.manager)} takes the ${year} title with ${esc(champ.team)}.
              ${robbed && robbed !== champ
                ? `${esc(robbed.manager)} scored more points than anybody (${robbed.points_for.toFixed(1)}) and has nothing to show for it.`
                : ""}
              ${last ? `${esc(last.manager)} lost the Sacco Bowl from the ${ord(last.seed || last.rank)} seed and owns the Sacco until further notice.` : ""}
              Full autopsy in the season review; fifteen years of history in the Trophy Room.</p>
            <div class="hero-actions">
              <a class="btn-red" href="hall.html">Read the season review →</a>
              <a class="btn-ghost" href="trophy.html">Trophy Room →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">${year} Podium</div>
            ${[[champ, "\u{1F3C6}"], [second, "\u{1F948}"], [third, "\u{1F949}"]].filter(([r]) => r).map(([r, m]) => `
              <div class="board-row">
                <span class="bn">${m}</span>
                <span class="bt">${esc(r.team)}</span>
                <span class="bm">${esc(r.manager)}</span>
              </div>`).join("")}
            ${last ? `<div class="board-row">
              <span class="bn">\u{1F6BD}</span><span class="bt">${esc(last.team)}</span>
              <span class="bm">${esc(last.manager)}</span></div>` : ""}
            <a class="see-all" href="trophy.html">All ${db.completed_seasons || 15} seasons →</a>
          </div>
        </div>
      </section>

      <section class="statbug">
        ${stat("Most points, " + year, hi.points_for.toFixed(1), hi.team)}
        ${stat("Fewest points, " + year, lo.points_for.toFixed(1), lo.team, true)}
        ${stat("Best record, " + year, bestRec.wins + "-" + bestRec.losses, bestRec.team)}
        ${stat("Draft night", cd.v, cd.s)}
      </section>

      <div class="body-grid">
        <div class="col-main">
          <div class="sec-top"><h2 class="h-sec">${year} Playoffs</h2>
            <span class="note">How the bracket finished</span></div>
          <hr class="rule-h">
          <div class="os-table">
            <div class="row hd"><span>#</span><span>Team</span><span>Manager</span>
              <span class="c">Record</span><span class="c">Pts For</span><span class="c">Pts Agst</span><span class="c">Moves</span></div>
            ${playoff.map((r) => tableRow(r, r.place === 1 ? "\u{1F3C6}" : ord(r.rank), r.place === 1 ? " champ" : "")).join("")}
          </div>

          <div class="sec-top" style="margin-top:26px"><h2 class="h-sec">${year} Regular Season</h2>
            <span class="note">Seeded by record, then points</span></div>
          <hr class="rule-h">
          <div class="os-table">
            <div class="row hd"><span>Seed</span><span>Team</span><span>Manager</span>
              <span class="c">Record</span><span class="c">Pts For</span><span class="c">Pts Agst</span><span class="c">Moves</span></div>
            ${seeded.map((r) => tableRow(r, r.seed,
              (r === last ? " last" : "") + (r.seed <= FIELD ? " made" : "") +
              (r.seed > seeded.length - 3 ? " bowl" : ""))).join("")}
          </div>
          <p class="os-note">Top ${FIELD} seeds make the playoffs. The bottom three go to the Sacco
          Bowl: the ${seeded.length - 2} and ${seeded.length - 1} seeds play in playoff week one, the
          loser meets the ${seeded.length} seed for the next two weeks, and the lower two-week total
          takes the Sacco. Everything between is just the season.</p>
        </div>

        <div class="col-side">
          <div class="mod">
            <h2 class="h-sec">${year} Awards</h2><hr class="rule-h">
            <div class="sup"><div class="award">Champion</div>
              <div class="who">${esc(champ.team)}</div>
              <div class="note">${esc(champ.manager)} · ${champ.wins}-${champ.losses} · ${champ.points_for.toFixed(1)} PF</div></div>
            ${robbed && robbed !== champ ? `<div class="sup"><div class="award">Most points, no ring</div>
              <div class="who">${esc(robbed.team)}</div>
              <div class="note">${esc(robbed.manager)} led the league at ${robbed.points_for.toFixed(1)} and finished ${ord(robbed.rank)}.</div></div>` : ""}
            <div class="sup"><div class="award">Busiest manager</div>
              <div class="who">${esc(busiest.team)}</div>
              <div class="note">${busiest.moves} roster moves. Nothing was ever good enough.</div></div>
            ${last ? `<div class="sup"><div class="award">The Sacco</div>
              <div class="who">${esc(last.team)}</div>
              <div class="note">${esc(last.manager)} · ${last.wins}-${last.losses}. Lost the Sacco Bowl${
                season.sacco_bowl ? ` ${Math.min(season.sacco_bowl.final.a.total, season.sacco_bowl.final.b.total).toFixed(2)}–${Math.max(season.sacco_bowl.final.a.total, season.sacco_bowl.final.b.total).toFixed(2)}` : ""}. It is engraved.</div></div>` : ""}
            ${bottom && bottom !== last ? `<div class="sup"><div class="award">Worst record</div>
              <div class="who">${esc(bottom.team)}</div>
              <div class="note">${esc(bottom.manager)} · ${bottom.wins}-${bottom.losses} and still did not take the Sacco home.</div></div>` : ""}
          </div>
          <div class="mod">
            <h2 class="h-sec">The Long View</h2><hr class="rule-h">
            ${repeat.map((p) => `<div class="clown-row">
                <span class="r">${p.rings}×</span>
                <span>${esc(p.manager)}</span>
                <span class="c">${esc(p.titles.join(", "))}</span></div>`).join("")}
            <p class="vote-foot" style="margin-top:12px">Repeat champions since ${db.first_season || 2011}.${
              once.length ? ` One apiece, most recent first: ${
                once.map((p) => `${esc(p.manager)} (${Math.max(...p.titles)})`).join(", ")}.` : ""}
              <a href="trophy.html">Full career table →</a></p>
          </div>
        </div>
      </div>`;
  }

  /* The Long View: repeat champions only. The old version sliced the first four
     people off trophy.json's own ordering, which handed the fourth slot to the
     oldest single title in the book. One-time winners now get a line of their
     own instead, newest first. */
  const byRecency = (a, b) => b.rings - a.rings || Math.max(...b.titles) - Math.max(...a.titles);

  async function run() {
    const page = document.body.dataset.page;
    if (page !== "home" && page !== "ranks") return;

    let league = {}, db = {}, ledger = {};
    try {
      [league, db, ledger] = await Promise.all([
        fetch("data/league.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({})),
        fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()),
        fetch("data/ledger.json", { cache: "no-store" }).then((r) => r.json()),
      ]);
    } catch { return; }

    // Live season? Leave the normal pages alone.
    const played = (league.matchups || []).filter((m) => m.status === "postevent");
    if (played.length) return;

    const done = (db.seasons || []).filter((s) => !s.in_progress && s.champion);
    const latest = done[done.length - 1];
    if (!latest) return;
    const raw = ledger[String(latest.year)] || [];
    if (!raw.length) return;
    const rows = raw.map((a) => ({
      team: a[0], manager: a[1], rank: a[2], place: a[3],
      wins: a[4], losses: a[5], points_for: a[6], points_against: a[7], moves: a[8],
    }));

    const paint = () => {
      const app = $("#app");
      if (!app) return false;
      app.innerHTML = seasonView(db, rows, latest.year);
      const chip = document.querySelector(".masthead .badge-live");
      if (chip) { chip.textContent = "Offseason"; chip.classList.add("os-badge"); }
      return true;
    };

    // app.js renders asynchronously; take over once it has painted.
    setTimeout(paint, 60);
    setTimeout(paint, 400);
    setTimeout(paint, 1200);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
