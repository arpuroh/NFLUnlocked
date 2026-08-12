/* NFL Unlocked — Trophy Room.
   Renders data/trophy.json (+ data/ledger.json): the full league database, 2011
   to now. Every champion, every manager's career line, the record book, and a
   season-by-season ledger you can open. Standalone from app.js so the weekly
   data pipeline can never disturb it. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const n0 = (v) => Math.round(v).toLocaleString();

  const ord = (i) => {
    const s = ["th", "st", "nd", "rd"], v = i % 100;
    return i + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  function ringRow(p) {
    const marks = [];
    for (let i = 0; i < p.rings; i++) marks.push("\u{1F3C6}");
    return marks.join("");
  }

  function render(db) {
    const people = db.people.filter((p) => p.display);
    // Champions board: most rings first, then most recent title. The career
    // table below stays sorted by rings then win percentage.
    const champs = people.filter((p) => p.rings > 0).slice().sort((a, b) =>
      b.rings - a.rings || Math.max(...b.titles) - Math.max(...a.titles));
    const seasons = db.seasons.filter((s) => !s.in_progress).slice().reverse();
    const rec = db.records;

    const recCard = (label, r, fmt) => `<div class="c">
      <div class="eyebrow red">${esc(label)}</div>
      <div class="v">${esc(fmt(r))}</div>
      <div class="s">${esc(r.manager)} · ${esc(r.team)} · ${r.year}</div></div>`;

    $("#app").innerHTML = `
      <section class="tr-hero">
        <div class="eyebrow">${db.first_season}–${db.latest_season} · ${db.completed_seasons} completed seasons · ${people.length} managers · every result on file</div>
        <h1 class="display">Trophy Room</h1>
        <p class="tr-sub">The permanent record of NFL Unlocked. Fifteen seasons of championships,
        collapses and receipts — pulled from the league's own archive, season by season.</p>
      </section>

      <div class="pad">
        <h2 class="h-sec">The Champions</h2><hr class="rule-h">
        <div class="tr-champs">
          ${champs.map((p) => `<div class="c ${p.rings >= 3 ? "elite" : ""}">
            <div class="rings">${ringRow(p)}</div>
            <div class="nm">${esc(p.manager)}</div>
            <div class="tm">${esc(p.current_team)}</div>
            <div class="yrs">${p.titles.join(" · ")}</div>
          </div>`).join("")}
        </div>

        <h2 class="h-sec" style="margin-top:38px">Career Table</h2><hr class="rule-h">
        <p class="tr-note">Sorted by rings, then win percentage. Team names change every year in this
        league — managers are the constant, so everything is tracked by manager.
        Playoffs counts berths made out of seasons played; six of fourteen teams qualify.</p>
        <div class="tr-table">
          <div class="row hd">
            <span>Manager</span><span>Current Team</span><span class="c">Yrs</span>
            <span class="c">Record</span><span class="c">Win%</span><span class="c">Points</span>
            <span class="c">\u{1F3C6}</span><span class="c">\u{1F948}</span><span class="c po">Playoffs</span><span class="c">\u{1F6BD}</span>
          </div>
          ${people.map((p) => `<div class="row ${p.rings ? "won" : ""} ${p.active ? "" : "gone"}">
            <span class="m">${esc(p.manager)}${p.active ? "" : ` <i>· ${esc(p.span)}</i>`}</span>
            <span class="t">${esc(p.current_team)}</span>
            <span class="c" data-k="Seasons">${p.seasons}</span>
            <span class="c" data-k="Record">${p.wins}-${p.losses}${p.ties ? "-" + p.ties : ""}</span>
            <span class="c" data-k="Win%">${p.win_pct.toFixed(3).replace(/^0/, "")}</span>
            <span class="c" data-k="Points">${n0(p.points_for)}</span>
            <span class="c ${p.rings ? "gold" : "dim"}" data-k="Titles">${p.rings || "–"}</span>
            <span class="c dim" data-k="2nd">${p.runner_ups.length || "–"}</span>
            <span class="c po ${p.playoffs ? "" : "dim"}" data-k="Playoffs">${p.playoffs ?? "–"}<i>/${p.seasons}</i></span>
            <span class="c ${p.toilets.length ? "bad" : "dim"}" data-k="Saccos">${p.toilets.length || "–"}</span>
          </div>`).join("")}
        </div>

        <h2 class="h-sec" style="margin-top:38px">The Record Book</h2><hr class="rule-h">
        <div class="tr-records">
          ${recCard("Most points, one season", rec.most_points_season, (r) => n0(r.points_for))}
          ${recCard("Fewest points, one season", rec.fewest_points_season, (r) => n0(r.points_for))}
          ${recCard("Best record", rec.best_record, (r) => `${r.wins}-${r.losses}`)}
          ${recCard("Worst record", rec.worst_record, (r) => `${r.wins}-${r.losses}`)}
          ${recCard("Most roster moves", rec.most_moves, (r) => n0(r.moves))}
        </div>

        <h2 class="h-sec" style="margin-top:38px">Season Ledger</h2><hr class="rule-h">
        <p class="tr-note">Every completed season. Click a year for the full final standings.</p>
        <div class="tr-ledger">
          ${seasons.map((s) => `<details class="yr">
            <summary>
              <span class="y">${s.year}</span>
              <span class="w"><i>\u{1F3C6}</i> ${esc(s.champion)} <b>${esc(s.champion_manager)}</b></span>
              <span class="r"><i>\u{1F948}</i> ${esc(s.runner_up)} <b>${esc(s.runner_up_manager)}</b></span>
              <span class="l"><i>\u{1F6BD}</i> ${esc(s.toilet)} <b>${esc(s.toilet_manager)}</b></span>
              <span class="n">${s.teams} teams</span>
            </summary>
            <div class="full">
              ${!s.standings.length ? `<p class="empty">Standings unavailable.</p>` : `
              <div class="fr hd"><span>#</span><span>Team</span><span>Manager</span>
                <span class="c">Record</span><span class="c">PF</span><span class="c">PA</span><span class="c">Moves</span></div>
              ${s.standings.slice().sort((a, b) => a.rank - b.rank).map((r) => `<div class="fr">
                <span class="rk ${r.place === 1 ? "one" : ""}">${r.place === 1 ? "\u{1F3C6}" : ord(r.rank)}</span>
                <span>${esc(r.team)}</span><span class="mg">${esc(r.manager)}</span>
                <span class="c">${r.wins}-${r.losses}</span>
                <span class="c">${r.points_for.toFixed(1)}</span>
                <span class="c dim">${r.points_against.toFixed(1)}</span>
                <span class="c dim">${r.moves}</span>
              </div>`).join("")}`}
            </div>
          </details>`).join("")}
        </div>
        <p class="tr-foot">Source: the league's own Yahoo archive, one page per season, parsed and
        cross-checked. Two managers named Greg are separated by franchise lineage
        (Miley vs. Injured Reserve). Two 2011 entries and both 2013 Greg teams could not be
        attributed to a person and are excluded from career totals.</p>
      </div>`;
  }

  Promise.all([
    fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()),
    fetch("data/ledger.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({})),
    fetch("data/playoffs.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({})),
  ])
    .then(([db, ledger, playoffs]) => {
      // Playoff berths ship in their own file so the main database does not have
      // to be rewritten to add a column. Whichever source has it wins.
      db.people.forEach((p) => {
        if (p.playoffs == null) p.playoffs = playoffs[p.key] ?? 0;
      });
      // ledger rows are positional to keep the payload small:
      // [team, manager, rank, place, wins, losses, pointsFor, pointsAgainst, moves]
      db.seasons.forEach((s) => {
        s.standings = (ledger[String(s.year)] || []).map((a) => ({
          team: a[0], manager: a[1], rank: a[2], place: a[3],
          wins: a[4], losses: a[5], points_for: a[6], points_against: a[7], moves: a[8],
        }));
      });
      return db;
    })
    .then(render)
    .catch((e) => {
      console.error("trophy render failed:", e);
      const el = $("#app");
      if (el) el.innerHTML = `<div class="pad"><p class="empty">Trophy data unavailable.</p></div>`;
    });
})();
