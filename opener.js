/* NFL Unlocked — the season opener home page.

   Takes over This Week once the draft is in the books and before the first real
   score lands. Four things live here that are not anywhere else on the site:

     1. This week's matchups with a projected score and a win probability
     2. Playoff odds, simulated in the browser, re-runnable
     3. Two league polls with real shared results
     4. The season preview

   Everything is read from data/: projections.json, schedule.json, season.json,
   draft.json, trophy.json. The moment Week 1 scores exist, app.js renders the
   live page instead and this stands down. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  /* Weekly fantasy scores are noisy. A team projected at 106 will put up
     anywhere from 70 to 140 without anything unusual happening. This is the
     spread every probability on the page is built on. */
  const WEEK_SD = 26;
  const SEASON_WEEKS = 14;
  const PLAYOFF_SPOTS = 6;
  const SIMS = 8000;

  const SUPA = "https://zajaumqfompslmgoohxv.supabase.co/rest/v1";
  const SUPA_KEY = "sb_publishable_RlJF7WmTp_IyW2fOS2jwpQ_NnaiaI6u";
  const VOTER_KEY = "nflu_voter_id";

  const getJSON = (p) => fetch(p, { cache: "no-store" })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null);

  /* standard normal CDF, for turning a points gap into a win probability */
  const phi = (z) => 0.5 * (1 + erf(z / Math.SQRT2));
  function erf(x) {
    const s = x < 0 ? -1 : 1; x = Math.abs(x);
    const t = 1 / (1 + 0.3275911 * x);
    const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t
      - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }

  /* one device, one vote, and nothing about a person */
  function voterId() {
    try {
      let v = localStorage.getItem(VOTER_KEY);
      if (!v) {
        v = "v" + Math.random().toString(36).slice(2) + Date.now().toString(36);
        localStorage.setItem(VOTER_KEY, v);
      }
      return v;
    } catch { return "v" + Math.random().toString(36).slice(2) + Date.now().toString(36); }
  }

  /* ── the simulation ───────────────────────────────────────
     Fourteen weeks, everybody scores around their projection, top six make the
     playoffs and the bottom three play for the Sacco. Yahoo only publishes the
     current week's pairings to anybody not logged in, so the rest of the season
     is drawn as a balanced random schedule: over fourteen weeks that is very
     close to what a real one does, and it is stated on the page rather than
     hidden. Ties break on total points, same as the league. */
  function simulate(teams, sims = SIMS) {
    const n = teams.length;
    const proj = teams.map((t) => t.weekly);
    const made = new Array(n).fill(0), sacco = new Array(n).fill(0);
    const wins = new Array(n).fill(0), best = new Array(n).fill(0);
    const order = [...Array(n).keys()];
    for (let s = 0; s < sims; s++) {
      const w = new Array(n).fill(0), pf = new Array(n).fill(0);
      for (let week = 0; week < SEASON_WEEKS; week++) {
        for (let i = n - 1; i > 0; i--) {            // shuffle into pairings
          const j = (Math.random() * (i + 1)) | 0;
          [order[i], order[j]] = [order[j], order[i]];
        }
        const score = proj.map((p) => p + gauss() * WEEK_SD);
        for (let k = 0; k + 1 < n; k += 2) {
          const a = order[k], b = order[k + 1];
          pf[a] += score[a]; pf[b] += score[b];
          if (score[a] >= score[b]) w[a]++; else w[b]++;
        }
      }
      const rank = [...Array(n).keys()].sort((a, b) => w[b] - w[a] || pf[b] - pf[a]);
      rank.forEach((idx, pos) => {
        wins[idx] += w[idx];
        if (pos < PLAYOFF_SPOTS) made[idx]++;
        if (pos === 0) best[idx]++;
        if (pos >= n - 3) sacco[idx]++;
      });
    }
    return teams.map((t, i) => ({
      team: t.team, weekly: t.weekly,
      wins: wins[i] / sims,
      playoffs: made[i] / sims,
      top: best[i] / sims,
      sacco: sacco[i] / sims,
    })).sort((a, b) => b.playoffs - a.playoffs || b.wins - a.wins);
  }

  let spare = null;
  function gauss() {                                  // Box-Muller
    if (spare !== null) { const v = spare; spare = null; return v; }
    let u = 0, v = 0;
    while (u === 0) u = Math.random();
    while (v === 0) v = Math.random();
    const r = Math.sqrt(-2 * Math.log(u));
    spare = r * Math.sin(2 * Math.PI * v);
    return r * Math.cos(2 * Math.PI * v);
  }

  /* ── render ──────────────────────────────────────────────── */
  const pct = (x) => (x >= 0.995 ? ">99" : x <= 0.005 ? "<1" : Math.round(x * 100)) + "%";

  function logoOf(draft, name) {
    const t = (draft.teams || []).find((x) => x.team === name);
    return t && t.logo ? `<img class="tlogo sm" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  }

  // One line under each card. Varies with the margin, and within a margin band
  // it varies by matchup, because seven near-identical sentences read like a form letter.
  const FOOT = {
    flip: [
      "Dead heat. ${x} points is rounding error, not an edge \u2014 whoever benches the wrong flex loses this one.",
      "A coin flip with extra steps. ${x} points apart, which is one bad snap in either direction.",
      "${x} points between them. Whichever one of these two loses is going to blame the projections on this page.",
    ],
    thin: [
      "${F} by ${x}, which is one Sunday-night touchdown. ${D} does not need luck here, just a kicker who shows up.",
      "${F} by ${x}. That is a single busted coverage, so nobody should be printing anything yet.",
    ],
    near: [
      "${F} by ${x} on paper. Close enough that the waiver wire decides it and both managers will claim they were robbed.",
      "${F} by ${x}, a lead thin enough that one Tuesday pickup erases it. Set your lineup on Sunday, not now.",
      "${F} by ${x}. Enough to matter, not enough to relax, which is the worst place to be in Week 1.",
    ],
    real: [
      "${F} by ${x}. A real edge in a league this compressed, but ${D} beats that number any week a tight end remembers he plays football.",
      "${F} by ${x} \u2014 about as clear as Week 1 gets around here. ${D} needs one guy to go nuclear.",
    ],
    wide: [
      "${F} by ${x}, the widest gap on the board. ${D} needs somebody to have a career day.",
      "${F} by ${x}. On paper this is the mismatch of the week, which historically means nothing at all.",
    ],
  };

  // Rotate through a band's lines so two close games never read the same.
  const footUse = {};
  function muFoot(fav, dog, m) {
    const F = esc(fav.team), D = esc(dog.team), x = m.toFixed(1);
    const band = m < 0.75 ? "flip" : m < 2 ? "thin" : m < 3.5 ? "near" : m < 5 ? "real" : "wide";
    const pool = FOOT[band];
    const n = footUse[band] = (footUse[band] || 0);
    footUse[band] = n + 1;
    return pool[n % pool.length].replace(/\$\{F\}/g, F).replace(/\$\{D\}/g, D).replace(/\$\{x\}/g, x);
  }

  function matchupCard(m, byTeam, draft, grades) {
    const a = byTeam[m.home], b = byTeam[m.away];
    if (!a || !b) return "";
    const diff = a.weekly - b.weekly;
    const pa = phi(diff / (WEEK_SD * Math.SQRT2));
    const favA = pa >= 0.5;
    // If both sides round to the same number, nobody gets the red treatment.
    const flip = Math.round(pa * 100) === Math.round((1 - pa) * 100);
    const gr = (t) => (grades && grades.grades && grades.grades[t] ? grades.grades[t].grade : "");
    const side = (t, p, win, home) => `
      <div class="mu-side${home ? "" : " away"}${win ? " fav" : ""}">
        ${logoOf(draft, t.team)}
        <div class="mu-name">${esc(t.team)}<em>${esc(gr(t.team))} · ${t.weekly.toFixed(1)} proj</em></div>
        <div class="mu-pct">${pct(p)}</div>
      </div>`;
    return `<article class="mu">
      ${side(a, pa, !flip && favA, true)}
      <div class="mu-bar${flip ? " even" : favA ? "" : " down"}"><i style="width:${
        Math.round((flip ? 0.5 : favA ? pa : 1 - pa) * 100)}%"></i></div>
      ${side(b, 1 - pa, !flip && !favA, false)}
      <div class="mu-foot">${muFoot(favA ? a : b, favA ? b : a, Math.abs(diff))}</div>
    </article>`;
  }

  function oddsRows(rows, draft) {
    return rows.map((r, i) => `<div class="od-row">
      <span class="od-n">${i + 1}</span>
      ${logoOf(draft, r.team)}
      <span class="od-t">${esc(r.team)}</span>
      <span class="od-bar"><i style="width:${Math.max(1, Math.round(r.playoffs * 100))}%"></i></span>
      <span class="od-v num">${pct(r.playoffs)}</span>
      <span class="od-s">${r.wins.toFixed(1)} wins · ${pct(r.top)} for the one seed · ${pct(r.sacco)} Sacco</span>
    </div>`).join("");
  }

  function pollBlock(poll, teams, draft) {
    return `<div class="poll" data-poll="${esc(poll.id)}">
      <h3 class="poll-q">${esc(poll.question)}</h3>
      <div class="poll-opts">
        ${teams.map((t) => `<button class="poll-opt" type="button" data-choice="${esc(t.team)}">
          ${logoOf(draft, t.team)}
          <span class="po-t">${esc(t.team)}</span>
          <span class="po-bar"><i style="width:0%"></i></span>
          <span class="po-v"></span>
        </button>`).join("")}
      </div>
      <p class="poll-note">${esc(poll.note)} <span class="poll-status"></span></p>
    </div>`;
  }

  async function loadPoll(id, root) {
    const res = await fetch(`${SUPA}/poll_results?select=choice,votes&poll_id=eq.${encodeURIComponent(id)}`,
      { headers: { apikey: SUPA_KEY }, cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).catch(() => null);
    if (!res) { paintPoll(root, null); return; }
    const tally = {};
    res.forEach((r) => { tally[r.choice] = r.votes; });
    paintPoll(root, tally);
  }

  function paintPoll(root, tally) {
    const status = $(".poll-status", root);
    if (!tally) {
      if (status) status.textContent = "Results are offline at the moment. Your vote still counts.";
      return;
    }
    const total = Object.values(tally).reduce((a, b) => a + b, 0);
    const max = Math.max(1, ...Object.values(tally));
    let mine = "";
    try { mine = localStorage.getItem("nflu_vote_" + root.dataset.poll) || ""; } catch {}
    $$(".poll-opt", root).forEach((b) => {
      const v = tally[b.dataset.choice] || 0;
      b.classList.toggle("mine", b.dataset.choice === mine);
      b.classList.toggle("has", v > 0);
      $(".po-bar i", b).style.width = Math.round((v / max) * 100) + "%";
      $(".po-v", b).textContent = total ? (v ? Math.round((v / total) * 100) + "%" : "") : "";
    });
    if (status) {
      status.textContent = total
        ? `${total} vote${total === 1 ? "" : "s"} so far.`
        : "Nobody has voted yet. Go first.";
    }
  }

  async function castVote(id, choice, root) {
    const status = $(".poll-status", root);
    try {
      const r = await fetch(`${SUPA}/poll_votes`, {
        method: "POST",
        headers: { apikey: SUPA_KEY, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify({ poll_id: id, choice, voter: voterId() }),
      });
      if (!r.ok) throw new Error(String(r.status));
      try { localStorage.setItem("nflu_vote_" + id, choice); } catch {}
      await loadPoll(id, root);
    } catch {
      if (status) status.textContent = "That vote did not go through. Try again in a second.";
    }
  }

  /* ── page ─────────────────────────────────────────────────── */
  function view(d) {
    const { season, sched, proj, draft, grades, db } = d;
    const byTeam = Object.fromEntries(proj.teams.map((t) => [t.team, t]));
    const ranked = proj.teams;
    const top = ranked[0], bottom = ranked[ranked.length - 1];
    const champSeason = (db.seasons || []).filter((s) => !s.in_progress && s.champion).pop();
    const odds = simulate(ranked);
    const teamsAZ = ranked.slice().sort((a, b) => a.team.localeCompare(b.team));

    const stat = (label, v, s, red) => `<div class="cell">
      <div class="eyebrow">${esc(label)}</div>
      <div class="v${red ? " red" : ""}">${esc(v)}</div>
      <div class="s">${esc(s)}</div></div>`;

    return `
      <section class="dark roast-hero op-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">Week ${sched.week || season.week}</span>
              <span class="eyebrow">${season.season} season · 14 teams · kickoff ${esc(season.kickoff_label)}</span>
            </div>
            <h1 class="display">${esc(season.headline)} <span class="kick">${esc(season.kicker)}</span></h1>
            <p class="lede">${esc(season.lede)}</p>
            <div class="hero-actions">
              <a class="btn-red" href="#matchups">This week's matchups →</a>
              <a class="btn-ghost" href="#poll">Vote →</a>
              <a class="btn-ghost" href="draft.html">Draft grades →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">Projected, per week</div>
            ${ranked.slice(0, 5).map((t, i) => `<div class="board-row has-logo">
              <span class="bn">${i + 1}</span>
              ${logoOf(draft, t.team)}
              <span class="bt">${esc(t.team)}</span>
              <span class="bm">${t.weekly.toFixed(1)}</span>
            </div>`).join("")}
            <a class="see-all" href="draft.html#rankings">All 14 with grades →</a>
          </div>
        </div>
      </section>

      <section class="statbug">
        ${stat("Projected leader", top.weekly.toFixed(1), `${top.team} · points per week`, true)}
        ${stat("First to last", proj.spread.toFixed(1), "points a week across the whole league")}
        ${stat("League average", proj.avg_weekly.toFixed(1), "a week, on this league's own scoring")}
        ${champSeason ? stat("Defending champion", esc(champSeason.champion_manager),
          `${champSeason.champion} · nobody has repeated since 2015`) : ""}
      </section>

      <div class="body-grid">
        <div class="col-main">
          <div class="sec-top" id="matchups"><h2 class="h-sec">Week ${sched.week} Matchups</h2>
            <span class="note">Projected score and win probability</span></div>
          <hr class="rule-h">
          <div class="op-mus">${(sched.matchups || []).map((m) => matchupCard(m, byTeam, draft, grades)).join("")}</div>
          <p class="os-note">Win probability comes from the two projections and the fact that a fantasy week
            swings about ${WEEK_SD} points in either direction. A team favoured by five wins around 55 percent
            of the time, which is barely a favourite at all.</p>

          <div class="sec-top" style="margin-top:32px" id="preview"><h2 class="h-sec">The Season Ahead</h2>
            <span class="note">Four things to argue about</span></div>
          <hr class="rule-h">
          ${(season.preview || []).map((p) => `<div class="op-story">
            <h3>${esc(p.title)}</h3><p>${esc(p.body)}</p></div>`).join("")}

          <div class="sec-top" style="margin-top:32px" id="poll"><h2 class="h-sec">The League Votes</h2>
            <span class="note">Live, shared, one vote per device</span></div>
          <hr class="rule-h">
          ${(season.polls || []).map((p) => pollBlock(p, teamsAZ, draft)).join("")}
        </div>

        <div class="col-side">
          <div class="mod" id="odds">
            <h2 class="h-sec">Playoff Odds</h2><hr class="rule-h">
            <p class="vote-foot" style="margin:0 0 12px">${SIMS.toLocaleString()} simulated seasons. Everybody scores
              around their projection each week, top six make the playoffs, bottom three go to the Sacco Bowl.</p>
            <div class="od-list">${oddsRows(odds, draft)}</div>
            <button class="dr-toggle" id="resim" type="button">Run it again ↻</button>
            <p class="vote-foot" style="margin-top:10px">Yahoo only publishes the current week's pairings to anybody
              not signed in, so weeks 2 to 14 are drawn as a balanced random schedule. Over fourteen weeks that lands
              very close to a real one. Ties break on points, same as the league.</p>
          </div>

          <div class="mod">
            <h2 class="h-sec">Where To Go</h2><hr class="rule-h">
            <a class="op-link" href="draft.html"><b>Draft grades</b><span>All 14 rosters, every price, the full board</span></a>
            <a class="op-link" href="draft.html#rankings"><b>Power rankings</b><span>Projected points, one to fourteen</span></a>
            <a class="op-link" href="roast.html"><b>Roast Roulette</b><span>Fifteen years of material, dealt at random</span></a>
            <a class="op-link" href="trophy.html"><b>Trophy Room</b><span>Every champion since 2011</span></a>
            <a class="op-link" href="hall.html"><b>Hall of Shame</b><span>The 2025 autopsy, kept permanently</span></a>
          </div>
        </div>
      </div>`;
  }

  function wire(d) {
    const btn = $("#resim");
    if (btn) {
      btn.addEventListener("click", () => {
        btn.disabled = true;
        btn.textContent = "Simulating…";
        setTimeout(() => {
          const rows = simulate(d.proj.teams);
          $(".od-list").innerHTML = oddsRows(rows, d.draft);
          btn.disabled = false;
          btn.textContent = "Run it again ↻";
        }, 30);
      });
    }
    $$(".poll").forEach((root) => {
      const id = root.dataset.poll;
      loadPoll(id, root);
      root.addEventListener("click", (ev) => {
        const b = ev.target.closest(".poll-opt");
        if (b) castVote(id, b.dataset.choice, root);
      });
    });
  }

  async function run() {
    if (document.body.dataset.page !== "home") return;
    const [league, proj, sched, season, draft, grades, db] = await Promise.all([
      getJSON("data/league.json"), getJSON("data/projections.json"),
      getJSON("data/schedule.json"), getJSON("data/season.json"),
      getJSON("data/draft.json"), getJSON("data/draft_grades.json"),
      getJSON("data/trophy.json"),
    ]);
    // Once real scores exist, the live page owns This Week again.
    const played = ((league || {}).matchups || []).filter((m) => m.status === "postevent");
    if (played.length) return;
    if (!proj || !sched || !season || !draft) return;

    const d = { proj, sched, season, draft, grades, db: db || {} };
    const paint = () => {
      const app = $("#app");
      if (!app) return false;
      app.innerHTML = view(d);
      wire(d);
      const chip = $(".masthead .badge-live");
      if (chip) { chip.textContent = `Week ${sched.week}`; chip.style.background = "var(--red)"; }
      return true;
    };
    setTimeout(paint, 60); setTimeout(paint, 400); setTimeout(paint, 1200);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
