/* NFL Unlocked · The Injury Index.
   Renders data/injuries.json (built by scripts/build_injuries.py): every game a rostered
   player missed hurt, charged to whoever held him that week.
   The Injury Bill = starter points left on the table: each week, the best lineup a team could
   have set with its hurt players against the best it could set without them. A hurt bench guy
   costs nothing. Dead money (draft dollars x games missed) is the secondary, draft-capital view.
   Sections: hero, the index (sortable, expandable), awards, bill vs standings, the ward
   calendar, the most expensive injuries, where it hurts, the trade clinic, this week's ward,
   ghost starts and phantom stashes, method. Uses NU.stamps / NU.wireStamps from app.js. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (n) => Math.round(Number(n) || 0).toLocaleString("en-US");
  const f1 = (n) => (Math.round((Number(n) || 0) * 10) / 10).toFixed(1);
  const money = (n) => "$" + fmt(n);
  const pl = (n, w, p) => `${n} ${n === 1 ? w : (p || w + "s")}`;
  const ord = (i) => { const s = ["th", "st", "nd", "rd"], v = i % 100; return i + (s[(v - 20) % 10] || s[v] || s[0]); };
  const hasNU = () => typeof NU !== "undefined" && NU && NU.stamps;
  const stamps = (id) => (hasNU() ? NU.stamps(id, {}, { min: 3 }) : "");
  const clean = (n) => String(n || "").replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}\u{200D}]/gu, "").replace(/\s+/g, " ").trim();
  const logo = (t, cls = "sm") => t && t.logo ? `<img class="tlogo ${cls}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  const pos = (p) => `<span class="ix-pp pos-${esc(String(p || "").toLowerCase())}">${esc(p)}</span>`;
  const HOW = { draft: "Drafted", trade: "Traded for", waivers: "Waivers" };
  const SEV = { "IR": "ir", "IR (return)": "ir", "PUP": "ir", "NFI": "ir", "Out": "out", "Doubtful": "dbt", "Questionable": "q" };
  const SHORT = { "IR (return)": "IR-R", "Doubtful": "Dbt", "Questionable": "Q" };
  const statusChip = (s) => `<span class="ix-st ${SEV[s] || "q"}" title="${esc(s)}">${esc(SHORT[s] || s)}</span>`;
  const OUT = (s) => s !== "Questionable";

  let D, TM, NOW, PL;
  const who = (tid) => TM[tid] ? `${clean(TM[tid].name)} (${TM[tid].manager})` : "";
  // "(now with Andrew)" when a player has since moved on from the team being described
  const since = (name, tid) => {
    const p = PL[name];
    if (!p || p.now_team === tid) return "";
    const mv = (p.traded || []).find((m) => m.from === tid);
    if (mv) return ` (traded to ${TM[mv.to].manager} in Week ${mv.week})`;
    return p.now_team ? ` (now with ${TM[p.now_team].manager})` : " (since dropped)";
  };

  /* ── little building blocks ───────────────────────────── */
  // a square per week: red = missed and would have started, dark = missed from the bench
  const dots = (weeks, W, starts) => `<span class="ix-dots" aria-label="missed weeks ${weeks.join(", ")}">${
    Array.from({ length: W }, (_, i) => {
      const w = i + 1, on = weeks.includes(w), st = starts && starts.includes(w);
      return `<i class="${on ? (st || !starts ? "on" : "bn") : ""}" title="Week ${w}${on ? (st ? ": would have started" : starts ? ": bench" : "") : ""}"></i>`;
    }).join("")}</span>`;

  function teamLine(t) {
    if (!t.injured) return "Not one game lost to injury. Either the healthiest roster in the league or nobody here plays.";
    const top = t.ledger[0];
    let s;
    if (top.lost > 0.5) {
      const via = top.how === "trade" ? " after the trade" : "";
      s = `${top.name}${since(top.name, t.team_id)} has cost ${f1(top.lost)} starter points${via}: ${pl(top.started, "week")} he would have been in the lineup and wasn't.`;
      if (t.ledger.length > 1 && t.ledger[1].lost > 0.5) s += ` ${t.ledger[1].name} adds ${f1(t.ledger[1].lost)}.`;
    } else {
      s = `${pl(t.injured, "player")} hurt and ${pl(t.games, "game")} missed, and the bench covered almost all of it. Depth pays.`;
    }
    if (t.games >= 8 && t.bill < t.games * 1.2) s += ` ${t.games} games missed for a ${f1(t.bill)}-point bill: the backups did their job.`;
    if (t.now) {
      const big = NOW.filter((n) => n.team_id === t.team_id && OUT(n.status) && n.starter)[0];
      s += ` ${t.now} in the ward for Week ${D.report_week}${t.due_pts ? `, about ${f1(t.due_pts)} starter points out` : ""}`;
      s += big ? `, led by ${big.name} (${big.status}).` : ".";
    }
    return s;
  }

  /* ── hero ─────────────────────────────────────────────── */
  function hero() {
    const T = D.totals, top = D.teams[0], last = D.teams[D.teams.length - 1];
    const worst = D.players[0];
    const most = [...D.teams].sort((a, b) => b.injured - a.injured || b.games - a.games)[0];
    return `
      <section class="dark roast-hero ix-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">The Injury Index</span>
              <span class="eyebrow">${D.season} · Weeks 1–${D.through_week} · ${T.injured} players · ${T.games} games missed</span>
            </div>
            <h1 class="display">${f1(T.bill)} starter points, gone.
              <span class="kick">${esc(clean(top.name))} has lost ${f1(top.bill)} of them.</span></h1>
            <p class="lede">Every week, the best lineup each team could have set with its hurt players against the best it
              could set without them. The gap is the bill. Of ${T.games} games missed, ${T.started} were starters; the rest were
              bench bodies who cost nothing. ${esc(worst.name)} alone has cost ${f1(worst.lost)} points. ${esc(clean(most.name))}
              has lost ${pl(most.injured, "player")} to the infirmary, and ${esc(clean(last.name))} has barely noticed.</p>
            <div class="hero-actions">
              <a class="btn-red" href="#index">The Index →</a>
              <a class="btn-ghost" href="#ward">This week's ward →</a>
              <a class="btn-ghost" href="#clinic">Trade clinic →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">Injury Bill · starter points lost</div>
            ${D.teams.slice(0, 5).map((t, i) => `<a class="board-row" href="#t-${esc(t.team_id)}" data-open="${esc(t.team_id)}">
              <span class="bn">${i + 1}</span>
              <span class="bt">${esc(clean(t.name))}<small>${esc(t.manager)} · ${pl(t.injured, "player")} · ${t.started} starter games</small></span>
              <span class="bm">${f1(t.bill)}</span></a>`).join("")}
            <a class="see-all" href="#index">All 14 teams →</a>
          </div>
        </div>
      </section>
      <section class="statbug">
        <div class="cell"><div class="eyebrow">Players hurt</div><div class="v">${T.injured}</div>
          <div class="s">missed at least one game on a roster</div></div>
        <div class="cell"><div class="eyebrow">Games missed</div><div class="v">${T.games}</div>
          <div class="s">${T.started} of them by would-be starters</div></div>
        <div class="cell"><div class="eyebrow">League injury bill</div><div class="v red">${f1(T.bill)}</div>
          <div class="s">starter points left on the table</div></div>
        <div class="cell"><div class="eyebrow">Out for Week ${D.report_week}</div><div class="v">${f1(T.due_pts)}</div>
          <div class="s">starter points already ruled out · ${T.now} players</div></div>
      </section>
      <div class="ix-scale">
        <span class="k">How the bill works</span>
        <span>Best lineup with your hurt players minus best lineup without them, every week. A hurt starter costs the gap to
          whoever filled in; a hurt bench guy costs <b>0</b>.</span>
        <span>Dead money ($ paid × games missed) is the draft-capital view.</span>
        <a href="#method" class="go">Full method ↓</a>
      </div>`;
  }

  /* ── the index ────────────────────────────────────────── */
  const COLS = [
    ["injured", "Hurt", "Players who missed a game on your roster"],
    ["games", "Games", "Player-games missed"],
    ["started", "Starts", "Missed games by players who would have started"],
    ["bill", "Bill", "Starter points left on the table"],
    ["dollar_games", "Dead $", "Draft dollars × games missed"],
    ["due_pts", "Due", "Starter points already ruled out for next week"],
  ];
  let sortKey = "bill";
  const cell = (t, k) => k === "bill" || k === "due_pts" ? (t[k] ? f1(t[k]) : "–") : fmt(t[k]);

  function indexRows() {
    const rows = [...D.teams].sort((a, b) => (b[sortKey] - a[sortKey]) || (b.bill - a.bill) || (b.games - a.games));
    return rows.map((t, i) => `<details class="ix-row" id="t-${esc(t.team_id)}" data-id="${esc(t.team_id)}">
      <summary>
        <span class="ix-n">${i + 1}</span>
        <span class="ix-team">${logo(t)}<span><b>${esc(t.name)}</b><small>${esc(t.manager)} · ${esc(t.record)}</small></span></span>
        ${COLS.map(([k]) => `<span class="ix-c${k === sortKey ? " on" : ""}${k === "bill" ? " big" : ""}" data-k="${k}">${cell(t, k)}</span>`).join("")}
        <span class="ix-sub">${t.injured} hurt · ${t.games} games (${t.started} starts) · ${money(t.dollar_games)} dead</span>
        <span class="ix-caret">▸</span>
      </summary>
      <div class="ix-body" data-lazy="1"></div>
    </details>`).join("");
  }

  function teamBody(t) {
    const W = D.through_week;
    const ghosts = t.ghosts.length ? `<p class="ix-ghost-line"><b>Started a ghost:</b> ${t.ghosts.map((g) =>
      `${esc(g.name)} in Week ${g.week} (${esc(g.hurt ? g.why : "did not play")})`).join(", ")}.</p>` : "";
    const ward = NOW.filter((n) => n.team_id === t.team_id);
    return `
      <p class="ix-line">${esc(teamLine(t))}</p>
      <div class="ix-facts">
        <span>Bill <b>${f1(t.bill)} pts</b></span><span>Rank <b>${t.rank} of 14</b></span>
        <span>Players hurt <b>${t.injured}</b></span><span>Games <b>${t.games}</b> (${t.started} starts)</span>
        <span>Per game missed <b>${f1(t.per_game)}</b></span><span>Dead money <b>${money(t.dollar_games)}</b></span>
        <span>IR slot used <b>${pl(t.ir_weeks, "week")}</b></span>
      </div>
      ${t.ledger.length ? `<div class="ix-led">
        <div class="ix-led-hd"><span>Player</span><span>How</span><span>Dead $</span><span>Missed · <i class="k-on"></i> start <i class="k-bn"></i> bench</span><span>Injury</span><span>Pts lost</span></div>
        ${t.ledger.map((p) => `<div class="ix-led-r">
          <span class="nm">${pos(p.pos)} <b>${esc(p.name)}</b></span>
          <span class="how ${p.how}" title="${p.cut ? `Cut while hurt: ${p.cut} of these games came after he was dropped` : ""}">${HOW[p.how]}${p.cut ? " · cut" : ""}</span>
          <span class="paid">${p.dg ? money(p.dg) : "–"}</span>
          <span class="wk">${dots(p.weeks, W, p.start_weeks)} <i>${p.started}/${p.games}</i></span>
          <span class="inj">${esc(p.part || "Not disclosed")}</span>
          <span class="bill${p.lost > 0.05 ? "" : " z"}">${f1(p.lost)}</span>
        </div>`).join("")}
      </div>` : ""}
      ${ghosts}
      ${ward.length ? `<div class="ix-ward-mini"><span class="k">Week ${D.report_week} report</span>${ward.map((n) =>
        `<span>${statusChip(n.status)} ${esc(n.name)}${n.starter ? " <em>starter</em>" : ""}</span>`).join("")}</div>` : ""}
      <div class="ix-foot">${stamps("inj-" + t.team_id)}</div>`;
  }

  function index() {
    return `<section class="ix-sec" id="index">
      <div class="sec-top"><h2 class="h-sec">The Index</h2><span class="note">Click a column to re-rank · click a team for the ledger</span></div>
      <hr class="rule-h">
      <p class="ix-lede">The <b>Bill</b> is the headline: starter points left on the table. <b>Hurt</b> is the raw count of
        injured players and <b>Games</b> the games they missed; <b>Starts</b> counts the ones where he would have been in the lineup.
        <b>Dead $</b> is draft dollars times games missed, including players acquired by trade. <b>Due</b> is starter points
        already ruled out for Week ${D.report_week}.</p>
      <div class="ix-table">
        <div class="ix-hd">
          <span>#</span><span>Team</span>
          ${COLS.map(([k, l, tip]) => `<button type="button" class="ix-sort${k === sortKey ? " on" : ""}" data-k="${k}" title="${esc(tip)}">${l}</button>`).join("")}
          <span></span>
        </div>
        <div id="ix-rows">${indexRows()}</div>
      </div>
    </section>`;
  }

  /* ── awards ───────────────────────────────────────────── */
  function awards() {
    const T = D.teams;
    const by = (f) => [...T].sort(f)[0];
    const bodies = by((a, b) => b.injured - a.injured || b.games - a.games);
    const tiedBodies = T.filter((t) => t.injured === bodies.injured);
    const iron = by((a, b) => a.games - b.games || a.bill - b.bill);
    const due = by((a, b) => b.due_pts - a.due_pts);
    const depth = [...T].filter((t) => t.games >= 10 && t !== iron && !/injured reserved/i.test(t.name)).sort((a, b) => a.per_game - b.per_game)[0];
    const dead = by((a, b) => b.dollar_games - a.dollar_games);
    const worst = D.players[0];
    const wTeam = TM[worst.owners[0].team_id];
    const A = [
      { k: "The Mash Unit", who: T[0], v: f1(T[0].bill), u: "pts lost",
        s: `Most starter points lost to injury. ${T[0].ledger[0].name}${since(T[0].ledger[0].name, T[0].team_id)}${T[0].ledger.length > 1 ? ` and ${T[0].ledger[1].name}${since(T[0].ledger[1].name, T[0].team_id)}` : ""} did most of the damage.` },
      { k: "Most Expensive Injury", who: wTeam, v: f1(worst.lost), u: "pts lost",
        s: `${worst.name}: ${pl(worst.started, "week")} he would have started and sat, ${(worst.part || "undisclosed").toLowerCase()}.` },
      { k: "Body Count", who: bodies, v: bodies.injured, u: "players",
        s: tiedBodies.length > 1 ? `Tied with ${tiedBodies.filter((t) => t !== bodies).map((t) => clean(t.name)).join(" and ")} for the most players lost.` : `Most players lost to injury. ${bodies.games} games missed between them.` },
      { k: "Iron Man", who: iron, v: iron.games, u: "games missed",
        s: `Fewest games lost to injury in the league, and a ${iron.record} record. Health is a skill until it isn't.` },
      { k: "Depth Chart", who: depth, v: f1(depth.per_game), u: "pts per game lost",
        s: `${depth.games} games missed and the bench barely noticed. The backups started and the lineup held.` },
      { k: "Dead Money", who: dead, v: money(dead.dollar_games), u: "$ × games",
        s: `The most draft capital in street clothes. ${dead.ledger.slice().sort((a, b) => b.dg - a.dg)[0].name} is most of it.` },
      { k: "Bill Due", who: due, v: f1(due.due_pts), u: `pts out wk ${D.report_week}`,
        s: `The most starter points already ruled out for Week ${D.report_week}: ${NOW.filter((n) => n.team_id === due.team_id && OUT(n.status) && n.starter).map((n) => n.name).join(", ") || "the whole ward"}.` },
    ];
    // the team named after the injured reserve list gets its own line if it earned one
    const ir = T.find((t) => /injured reserved/i.test(t.name));
    if (ir) {
      const gr = [...T].sort((a, b) => b.games - a.games).findIndex((t) => t === ir) + 1;
      A.push({ k: "Nominative Determinism", who: ir, v: ir.games, u: "games missed",
        s: gr === 1 ? (ir.rank === T.length
                      ? `The team named The Injured Reserved has missed more games than anyone and has the smallest bill in the league (${f1(ir.bill)}). It only loses players it can afford to lose.`
                      : `The team named The Injured Reserved has missed more games than anyone. Its bill ranks ${ord(ir.rank)}.`)
                    : `Named for the IR, ${ord(gr)} in games missed. Living up to it.` });
    }
    return `<section class="ix-sec" id="awards">
      <div class="sec-top"><h2 class="h-sec">The Infirmary Awards</h2><span class="note">Through Week ${D.through_week}</span></div>
      <hr class="rule-h">
      <div class="ix-aw">${A.map((a, i) => `<div class="aw${i === 0 ? " lead" : ""}">
        <div class="aw-k">${esc(a.k)}</div>
        <div class="aw-who">${logo(a.who)}<span><b>${esc(clean(a.who.name))}</b><small>${esc(a.who.manager)}</small></span></div>
        <div class="aw-v"><b>${a.v}</b><span>${esc(a.u)}</span></div>
        <p>${esc(a.s)}</p>
      </div>`).join("")}</div>
    </section>`;
  }

  /* ── bill vs standings ────────────────────────────────── */
  function corr(xs, ys) {
    const n = xs.length, mx = xs.reduce((a, b) => a + b) / n, my = ys.reduce((a, b) => a + b) / n;
    let sxy = 0, sxx = 0, syy = 0;
    xs.forEach((x, i) => { sxy += (x - mx) * (ys[i] - my); sxx += (x - mx) ** 2; syy += (ys[i] - my) ** 2; });
    return { r: sxy / Math.sqrt(sxx * syy), b: sxy / sxx, a: my - (sxy / sxx) * mx };
  }

  function scatter() {
    const T = D.teams, games = T.map((t) => t.wins + Number(String(t.record).split("-")[1] || 0));
    const G = Math.max(...games);
    const xs = T.map((t) => t.bill), ys = T.map((t) => t.wins);
    const { r, a, b } = corr(xs, ys);
    const W = 640, H = 330, L = 44, R = 18, Tp = 16, B = 40;
    const step = Math.max(...xs) > 60 ? 20 : 10;
    const xmax = Math.ceil(Math.max(...xs) / step) * step;
    const X = (v) => L + (v / xmax) * (W - L - R), Y = (v) => Tp + (1 - v / G) * (H - Tp - B);
    const ticks = []; for (let v = 0; v <= xmax; v += step) ticks.push(v);
    const yt = []; for (let v = 0; v <= G; v += 3) yt.push(v);
    const pts = T.map((t) => ({ t, x: X(t.bill), y: Y(t.wins) })).sort((p, q) => p.y - q.y || p.x - q.x);
    const placed = [];
    pts.forEach((p) => {
      let dy = -9, side = "start", dx = 9;
      for (let tries = 0; tries < 6; tries++) {
        const hit = placed.some((q) => Math.abs(q.ly - (p.y + dy)) < 12 && Math.abs(q.lx - (p.x + dx)) < 70);
        if (!hit) break;
        dy += 12;
      }
      if (p.x > W - 120) { side = "end"; dx = -9; }
      p.lx = p.x + dx; p.ly = p.y + dy; p.side = side;
      placed.push(p);
    });
    const rr = r.toFixed(2).replace("-", "−");
    const verdict = r < -0.6 ? "a strong link" : r < -0.35 ? "a real link, but a loose one" : r < -0.15 ? "a weak link" : "next to no link";
    return `<section class="ix-sec" id="standings">
      <div class="sec-top"><h2 class="h-sec">Does It Explain the Standings?</h2><span class="note">r = ${rr}</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Injury bill against wins, median game included. The correlation is ${rr}: ${verdict}.
        ${b < 0 ? `Every 10 starter points lost is worth about ${Math.abs(b * 10).toFixed(1)} wins the wrong way.` : "Injuries have not been the story of this season."}
        Teams above the line are winning through it; teams below it have no excuse in the trainer's room.</p>
      <div class="ix-chart">
        <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Injury bill against wins for all 14 teams">
          ${ticks.map((v) => `<line x1="${X(v)}" x2="${X(v)}" y1="${Tp}" y2="${H - B}" class="g"/><text x="${X(v)}" y="${H - B + 16}" class="tx" text-anchor="middle">${v}</text>`).join("")}
          ${yt.map((v) => `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" class="g"/><text x="${L - 8}" y="${Y(v) + 4}" class="tx" text-anchor="end">${v}</text>`).join("")}
          <line x1="${X(0)}" y1="${Y(a)}" x2="${X(xmax)}" y2="${Y(a + b * xmax)}" class="fit"/>
          <text x="${(L + W - R) / 2}" y="${H - 6}" class="ax" text-anchor="middle">STARTER POINTS LOST →</text>
          <text x="12" y="${(Tp + H - B) / 2}" class="ax" text-anchor="middle" transform="rotate(-90 12 ${(Tp + H - B) / 2})">WINS →</text>
          ${pts.map((p) => `<g class="pt${p.t.rank <= 3 ? " hot" : ""}"><title>${esc(clean(p.t.name))}: bill ${f1(p.t.bill)}, ${esc(p.t.record)}</title>
            <rect x="${p.x - 5}" y="${p.y - 5}" width="10" height="10"/>
            <text x="${p.lx}" y="${p.ly + 4}" text-anchor="${p.side}" class="lb">${esc(p.t.manager)}</text></g>`).join("")}
        </svg>
      </div>
    </section>`;
  }

  /* ── the ward calendar (heatmap) ──────────────────────── */
  function calendar() {
    const W = D.through_week;
    const max = Math.max(1, ...D.teams.flatMap((t) => t.weekly.map((w) => w.pts)));
    const lw = D.league_weekly;
    const lmax = Math.max(1, ...lw.map((w) => w.pts));
    return `<section class="ix-sec" id="calendar">
      <div class="sec-top"><h2 class="h-sec">The Ward Calendar</h2><span class="note">Starter points lost, team by week</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Each cell is what injuries cost that team's best lineup that week. Darker red, bigger hit. A gray cell
        means players were hurt but none of them would have started. Hover a cell for the names.</p>
      <div class="ix-heat" style="--w:${W}">
        <div class="hh"><span></span>${Array.from({ length: W }, (_, i) => `<span>W${i + 1}</span>`).join("")}<span>Bill</span></div>
        ${D.teams.map((t) => `<div class="hr">
          <span class="ht">${logo(t)}<b>${esc(clean(t.name))}</b></span>
          ${t.weekly.map((w) => {
            const hit = w.pts >= 0.05;
            const a = hit ? 0.16 + 0.84 * (w.pts / max) : 0;
            const cls = hit ? (a > 0.55 ? " dk" : "") : w.games ? " free" : " none";
            return `<span class="hc${cls}" style="${hit ? `--a:${a.toFixed(3)}` : ""}" title="${esc(`Week ${w.week}: ${w.games ? w.who.join(", ") : "nobody hurt"}${hit ? ` (${f1(w.pts)} starter pts)` : w.games ? " (bench only)" : ""}`)}">${hit ? f1(w.pts) : w.games ? w.games + "×" : ""}</span>`;
          }).join("")}
          <span class="hb">${f1(t.bill)}</span>
        </div>`).join("")}
        <div class="hr tot"><span class="ht"><b>League</b></span>${lw.map((w) => `<span class="hc lg" title="Week ${w.week}: ${w.games} games missed, ${f1(w.pts)} starter points">
          <i style="height:${Math.round(100 * w.pts / lmax)}%"></i><em>${f1(w.pts)}</em></span>`).join("")}<span class="hb">${f1(D.totals.bill)}</span></div>
      </div>
    </section>`;
  }

  /* ── the most expensive injuries ──────────────────────── */
  function expensive() {
    const W = D.through_week;
    const list = D.players.slice(0, 12);
    return `<section class="ix-sec" id="players">
      <div class="sec-top"><h2 class="h-sec">The Most Expensive Injuries</h2><span class="note">Starter points lost · red squares = would have started</span></div>
      <hr class="rule-h">
      <div class="ix-pg">${list.map((p, i) => {
        const span = (ws) => ws.length > 1 && ws[ws.length - 1] - ws[0] === ws.length - 1 ? `Wk ${ws[0]}–${ws[ws.length - 1]}` : `Wk ${ws.join(", ")}`;
        const owners = p.owners.map((o) => `${span(o.weeks)} with ${esc(who(o.team_id))}`).join("; ");
        const nowLine = p.now_team && !p.owners.some((o) => o.team_id === p.now_team) ? `Now on ${esc(who(p.now_team))}` : p.now_team ? `Still on ${esc(who(p.now_team))}` : "Not on a roster now";
        const now = NOW.find((n) => n.name === p.name);
        return `<article class="pc${i === 0 ? " lead" : ""}">
          <div class="pc-top"><span class="pc-n">${i + 1}</span>${pos(p.pos)}<b class="pc-name">${esc(p.name)}</b>${now ? statusChip(now.status) : ""}</div>
          <div class="pc-math"><span>${p.started} of ${p.games} missed as a starter</span><b>${f1(p.lost)}</b></div>
          <div class="pc-wk">${dots(p.weeks, W, p.start_weeks)}</div>
          <div class="pc-own">Missed ${owners}</div>
          <div class="pc-own now">${nowLine}</div>
          <div class="pc-meta"><span>${esc(p.part || "Not disclosed")}</span><span>Dead money ${money(p.dollar_games)}${p.cost ? ` · ${money(p.cost)} at the draft` : ""}</span></div>
        </article>`;
      }).join("")}</div>
      <details class="ix-all">
        <summary>All ${D.players.length} injured players</summary>
        <div class="ix-led all">
          <div class="ix-led-hd"><span>Player</span><span>Held by</span><span>Dead $</span><span>Missed</span><span>Injury</span><span>Pts lost</span></div>
          ${D.players.map((p) => `<div class="ix-led-r">
            <span class="nm">${pos(p.pos)} <b>${esc(p.name)}</b></span>
            <span class="how" title="${esc(p.owners.map((o) => `Wk ${o.weeks.join(", ")}: ${who(o.team_id)}`).join("; "))}">${p.owners.map((o) => esc(TM[o.team_id].manager)).join(", ")}</span>
            <span class="paid">${p.dollar_games ? money(p.dollar_games) : "–"}</span>
            <span class="wk">${dots(p.weeks, W, p.start_weeks)} <i>${p.started}/${p.games}</i></span>
            <span class="inj">${esc(p.part || "Not disclosed")}</span>
            <span class="bill${p.lost > 0.05 ? "" : " z"}">${f1(p.lost)}</span>
          </div>`).join("")}
        </div>
      </details>
    </section>`;
  }

  /* ── where it hurts ───────────────────────────────────── */
  function body() {
    const parts = D.parts.filter(([k]) => k !== "Undisclosed");
    const undis = (D.parts.find(([k]) => k === "Undisclosed") || [0, 0])[1];
    const max = Math.max(...parts.map(([, n]) => n));
    const tot = D.parts.reduce((a, [, n]) => a + n, 0);
    return `<div class="ix-mod" id="body">
      <h3 class="ix-h3">Where It Hurts</h3><hr class="rule-h">
      <p class="ix-small">Games missed, by body part. ${parts[0][0]} leads with ${parts[0][1]} of ${tot}.</p>
      <div class="ix-bars">${parts.map(([k, n], i) => `<div class="bar-r${i === 0 ? " top" : ""}">
        <span class="bl">${esc(k)}</span><span class="bt"><i style="width:${(100 * n / max).toFixed(1)}%"></i></span><span class="bv">${n}</span></div>`).join("")}
      </div>
      ${undis ? `<p class="ix-small">Plus ${undis} games where the team never said what was wrong.</p>` : ""}
    </div>`;
  }

  /* ── the trade clinic ─────────────────────────────────── */
  function clinic() {
    if (!D.trades.length) return "";
    const cards = D.trades.map((tr) => {
      const sides = tr.sides.map((s) => {
        const t = TM[s.team_id];
        return `<div class="cl-side">
          <div class="cl-team">${logo(t)}<span><b>${esc(clean(t.name))}</b><small>${esc(t.manager)} received</small></span></div>
          <ul>${s.got.map((p) => {
            const now = NOW.find((n) => n.name === p.name);
            return `<li>${pos(p.pos)}<span class="pn"><b>${esc(p.name)}</b><small>${money(p.cost)} · missed ${p.missed_before} before the deal, ${p.missed_after} since${p.lost_after ? ` (${f1(p.lost_after)} pts)` : ""}</small></span>${now ? statusChip(now.status) : `<span class="ix-st ok">Healthy</span>`}</li>`;
          }).join("")}</ul>
        </div>`;
      });
      const bad = [];
      tr.sides.forEach((s) => s.got.forEach((p) => {
        const now = NOW.find((n) => n.name === p.name);
        if (now && OUT(now.status)) bad.push({ team: TM[s.team_id], p, now });
      }));
      const note = bad.length
        ? bad.map((x) => `${x.team.manager} traded for ${x.p.name} in Week ${tr.week}. ${x.now.status === "Out" || x.now.status === "Doubtful" ? `He is ${x.now.status.toLowerCase()} for Week ${D.report_week}` : `He is on ${x.now.status} for Week ${D.report_week}`}${x.now.part ? ` (${x.now.part.toLowerCase()})` : ""}${x.now.starter ? ", and he was a starter: that hole goes straight on the bill" : ""}.`).join(" ")
        : `Nobody in this deal has missed a game since. Clean bill of health, for now.`;
      return `<article class="cl">
        <div class="cl-bar"><span class="tc-when">${D.season} · Week ${tr.week}</span></div>
        <div class="cl-sides">${sides.join("")}</div>
        <p class="cl-note">${esc(note)}</p>
      </article>`;
    }).join("");
    return `<section class="ix-sec" id="clinic">
      <div class="sec-top"><h2 class="h-sec">The Trade Clinic</h2><span class="note">${D.season} trades, medically reviewed</span></div>
      <hr class="rule-h">
      <p class="ix-lede">A traded player's missed games go on the bill of whoever holds him that week, and his draft price travels
        with him into dead money. Games he missed before the deal stay on the seller's tab. The full trade verdicts live in
        <a href="trades.html">Trade Court</a>.</p>
      <div class="cl-grid">${cards}</div>
    </section>`;
  }

  /* ── this week's ward ─────────────────────────────────── */
  function ward() {
    const by = {};
    NOW.forEach((n) => (by[n.team_id] = by[n.team_id] || []).push(n));
    const teams = [...D.teams].sort((a, b) => b.due_pts - a.due_pts || b.now - a.now || (by[b.team_id] || []).length - (by[a.team_id] || []).length);
    return `<section class="ix-sec" id="ward">
      <div class="sec-top"><h2 class="h-sec">This Week's Ward</h2><span class="note">Week ${D.report_week} injury report</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Everyone on a Week ${D.through_week} roster who is on injured reserve or carries a game status for Week ${D.report_week}.
        The number is the starter points already ruled out (IR, Out and Doubtful). <span class="ix-st ir">IR</span> and
        <span class="ix-st out">Out</span> are certain; <span class="ix-st dbt">Dbt</span> almost; <span class="ix-st q">Q</span> is a coin flip.
        <em class="wd-tag">Starter</em> marks a player who would be in the best lineup.</p>
      <div class="wd-grid">${teams.map((t) => {
        const list = by[t.team_id] || [];
        return `<div class="wd${t.due_pts >= 0.5 ? " hot" : ""}">
          <div class="wd-hd">${logo(t)}<span><b>${esc(clean(t.name))}</b><small>${esc(t.manager)}</small></span>
            <span class="wd-due">${t.due_pts >= 0.05 ? f1(t.due_pts) : "–"}<small>pts out</small></span></div>
          ${list.length ? `<ul>${list.map((n) => `<li>${statusChip(n.status)}<span class="pn">${esc(n.name)}${n.starter ? ` <em class="wd-tag">Starter</em>` : ""}<small>${esc(n.pos)} · ${esc(n.part || "undisclosed")}${n.cost ? ` · ${money(n.cost)}` : ""}</small></span></li>`).join("")}</ul>`
            : `<p class="wd-none">Nobody on the report. Enjoy it.</p>`}
        </div>`;
      }).join("")}</div>
    </section>`;
  }

  /* ── ghosts + stashes ─────────────────────────────────── */
  function oddities() {
    const ghosts = D.teams.flatMap((t) => t.ghosts.map((g) => ({ ...g, t })));
    return `<section class="ix-sec ix-two">
      <div class="ix-mod">
        <h3 class="ix-h3">Started a Ghost</h3><hr class="rule-h">
        <p class="ix-small">Starters who never took a snap while their NFL team played. A zero in the lineup, on purpose or by neglect.</p>
        ${ghosts.length ? ghosts.sort((a, b) => a.week - b.week).map((g) => `<div class="gh-r">
          <span class="w">Wk ${g.week}</span>
          <span class="x"><b>${esc(clean(g.t.name))}</b> started ${esc(g.name)} <small>${esc(g.hurt ? `listed ${g.why}` : "active, did not play")} · ${g.pts} pts</small></span>
        </div>`).join("") : `<p class="ix-small">Nobody. Impressive.</p>`}
      </div>
      ${body()}
      ${D.stashes.length ? `<div class="ix-mod">
        <h3 class="ix-h3">Phantom Stashes</h3><hr class="rule-h">
        <p class="ix-small">Rostered players who are not on any NFL team. Not injured, just not employed. Not on the bill.</p>
        ${D.stashes.map((s) => `<div class="gh-r"><span class="w">${s.weeks} wk</span>
          <span class="x"><b>${esc(s.name)}</b> <small>held by ${esc(clean(TM[s.team_id].name))}</small></span></div>`).join("")}
      </div>` : ""}
    </section>`;
  }

  /* ── method ───────────────────────────────────────────── */
  function method() {
    const m = D.method;
    const built = new Date(D.built_at);
    return `<section class="ix-method" id="method">
      <h2 class="h-sec">How the Index Works</h2><hr class="rule-h">
      <dl>
        <dt>A missed game</dt><dd>${esc(m.hurt)}</dd>
        <dt>Who pays</dt><dd>${esc(m.owner)}</dd>
        <dt>The bill</dt><dd>${esc(m.bill)}</dd>
        <dt>Player values</dt><dd>${esc(m.points)}</dd>
        <dt>Dead money</dt><dd>${esc(m.dollars)}</dd>
        <dt>Source</dt><dd>${esc(m.source)}</dd>
      </dl>
    </section>
    <section class="ix-band">
      <h2 class="display">Draft day is a promise. The trainer's room sends the bill.</h2>
      <div class="meta"><div>Weeks 1–${D.through_week} · ${D.season}</div><div>${D.totals.injured} players · ${D.totals.games} games</div><div>Built ${esc(built.toLocaleDateString("en-US", { month: "short", day: "numeric", timeZone: "America/New_York" }))}</div></div>
    </section>`;
  }

  /* ── wiring ───────────────────────────────────────────── */
  function wireRows() {
    $$(".ix-row").forEach((d) => d.addEventListener("toggle", () => {
      const b = $(".ix-body", d);
      if (d.open && b.dataset.lazy) {
        b.innerHTML = teamBody(TM[d.dataset.id]);
        delete b.dataset.lazy;
        if (hasNU()) NU.wireStamps(b);
      }
    }));
  }

  function openTeam(id) {
    const d = document.getElementById("t-" + id);
    if (!d) return;
    d.open = true;
    d.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function wire() {
    wireRows();
    $$(".ix-sort").forEach((b) => b.addEventListener("click", () => {
      sortKey = b.dataset.k;
      $$(".ix-sort").forEach((x) => x.classList.toggle("on", x === b));
      $("#ix-rows").innerHTML = indexRows();
      wireRows();
    }));
    document.addEventListener("click", (e) => {
      const o = e.target.closest("[data-open]");
      if (o) { e.preventDefault(); openTeam(o.dataset.open); }
    });
    if (hasNU()) NU.wireStamps(document);
    const h = location.hash.slice(1);
    if (h.startsWith("t-")) setTimeout(() => openTeam(h.slice(2)), 60);
    else if (h) { const el = document.getElementById(h); if (el) setTimeout(() => el.scrollIntoView(), 60); }
  }

  function render(db) {
    D = db;
    TM = Object.fromEntries(db.teams.map((t) => [t.team_id, t]));
    NOW = db.now || [];
    PL = Object.fromEntries(db.players.map((p) => [p.name, p]));
    $("#app").innerHTML = `<div class="ix">
      ${hero()}${index()}${awards()}${scatter()}${calendar()}${expensive()}${clinic()}${ward()}${oddities()}${method()}
    </div>`;
    wire();
  }

  fetch("data/injuries.json", { cache: "no-store" })
    .then((r) => r.json())
    .then(render)
    .catch((e) => {
      console.error("injury index render failed:", e);
      const el = $("#app");
      if (el) el.innerHTML = `<div class="pad" style="padding:30px"><p class="empty">Injury data unavailable. The trainer is on break.</p></div>`;
    });
})();
