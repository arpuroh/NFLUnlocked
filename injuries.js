/* NFL Unlocked · The Injury Index.
   Renders data/injuries.json (built by scripts/build_injuries.py): every game a rostered
   player missed hurt, charged to whoever held him that week and priced in what he cost them.
   The Injury Bill = dollars paid x games missed. Traded players carry their auction price.
   Sections: hero, the index (sortable, expandable), awards, bill vs standings, the ward
   calendar, the most expensive injuries, where it hurts, the trade clinic, this week's ward,
   ghost starts and phantom stashes, method. Uses NU.stamps / NU.wireStamps from app.js. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const fmt = (n) => Math.round(Number(n) || 0).toLocaleString("en-US");
  const money = (n) => "$" + fmt(n);
  const pl = (n, w, p) => `${n} ${n === 1 ? w : (p || w + "s")}`;
  const hasNU = () => typeof NU !== "undefined" && NU && NU.stamps;
  const stamps = (id) => (hasNU() ? NU.stamps(id, {}, { min: 3 }) : "");
  const clean = (n) => String(n || "").replace(/[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}\u{200D}]/gu, "").replace(/\s+/g, " ").trim();
  const logo = (t, cls = "sm") => t && t.logo ? `<img class="tlogo ${cls}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  const pos = (p) => `<span class="ix-pp pos-${esc(String(p || "").toLowerCase())}">${esc(p)}</span>`;
  const ord = (i) => { const s = ["th", "st", "nd", "rd"], v = i % 100; return i + (s[(v - 20) % 10] || s[v] || s[0]); };
  const HOW = { draft: "Drafted", trade: "Traded for", waivers: "Waivers" };
  const SEV = { "IR": "ir", "IR (return)": "ir", "PUP": "ir", "NFI": "ir", "Out": "out", "Doubtful": "dbt", "Questionable": "q" };
  const SHORT = { "IR (return)": "IR-R", "Doubtful": "Dbt", "Questionable": "Q" };
  const statusChip = (s) => `<span class="ix-st ${SEV[s] || "q"}" title="${esc(s)}">${esc(SHORT[s] || s)}</span>`;

  let D, TM, NOW;

  /* ── little building blocks ───────────────────────────── */
  const dots = (weeks, W) => `<span class="ix-dots" aria-label="missed weeks ${weeks.join(", ")}">${
    Array.from({ length: W }, (_, i) => `<i class="${weeks.includes(i + 1) ? "on" : ""}" title="Week ${i + 1}"></i>`).join("")}</span>`;

  function teamLine(t) {
    if (!t.injured) return "Not one game lost to injury. Either the healthiest roster in the league or nobody here plays.";
    const top = t.ledger[0];
    let s;
    if (top.dg > 0) {
      const via = top.how === "trade" ? " after trading for him" : top.how === "waivers" ? ` after a ${money(top.paid)} claim` : "";
      s = `${top.name} (${money(top.paid)}) has sat ${pl(top.games, "game")}${via}, a ${fmt(top.dg)} bill on his own.`;
      if (t.ledger.length > 1 && t.ledger[1].dg > 0) s += ` ${t.ledger[1].name} adds ${fmt(t.ledger[1].dg)}.`;
    } else {
      s = `${pl(t.injured, "player")} hurt and ${pl(t.games, "game")} missed, every one of them on a player who cost nothing. Volume, no price tag.`;
    }
    if (t.now) {
      const big = NOW.filter((n) => n.team_id === t.team_id && n.status !== "Questionable").sort((a, b) => b.cost - a.cost)[0];
      s += ` ${t.now} in the ward for Week ${D.report_week}${t.due ? `, ${money(t.due)} of roster on the shelf` : ""}`;
      s += big && big.cost >= 10 ? `, led by ${big.name} (${big.status}).` : ".";
    }
    return s;
  }

  /* ── hero ─────────────────────────────────────────────── */
  function hero() {
    const T = D.totals, top = D.teams[0], clean_ = D.teams[D.teams.length - 1];
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
            <h1 class="display">The league's injury bill: ${fmt(T.dollar_games)}.
              <span class="kick">${esc(clean(top.name))} is on the hook for ${fmt(top.dollar_games)} of it.</span></h1>
            <p class="lede">Every game a rostered player sat out hurt, charged to whoever had him that week and priced at
              what he cost them. ${esc(worst.name)} alone has run up ${fmt(worst.dollar_games)}. ${esc(clean(most.name))}
              has lost ${pl(most.injured, "player")} to the infirmary, and ${esc(clean(clean_.name))} has barely noticed
              there is one.</p>
            <div class="hero-actions">
              <a class="btn-red" href="#index">The Index →</a>
              <a class="btn-ghost" href="#ward">This week's ward →</a>
              <a class="btn-ghost" href="#clinic">Trade clinic →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">Injury Bill · Top 5</div>
            ${D.teams.slice(0, 5).map((t, i) => `<a class="board-row" href="#t-${esc(t.team_id)}" data-open="${esc(t.team_id)}">
              <span class="bn">${i + 1}</span>
              <span class="bt">${esc(clean(t.name))}<small>${esc(t.manager)} · ${pl(t.injured, "player")} · ${t.games} gm</small></span>
              <span class="bm">${fmt(t.dollar_games)}</span></a>`).join("")}
            <a class="see-all" href="#index">All 14 teams →</a>
          </div>
        </div>
      </section>
      <section class="statbug">
        <div class="cell"><div class="eyebrow">Players hurt</div><div class="v">${T.injured}</div>
          <div class="s">missed at least one game on a roster</div></div>
        <div class="cell"><div class="eyebrow">Games missed</div><div class="v">${T.games}</div>
          <div class="s">${fmt(T.points)} points on the shelf</div></div>
        <div class="cell"><div class="eyebrow">League injury bill</div><div class="v red">${fmt(T.dollar_games)}</div>
          <div class="s">dollars paid × games missed</div></div>
        <div class="cell"><div class="eyebrow">In the ward now</div><div class="v">${T.now}</div>
          <div class="s">IR or ruled out, Week ${D.report_week} report</div></div>
      </section>
      <div class="ix-scale">
        <span class="k">How the bill works</span>
        <span>Dollars paid × games missed. A $45 receiver out six weeks is a <b>270</b> bill.</span>
        <span>Drafted: auction price. Traded for: his auction price comes with him. Waivers: the FAAB bid.</span>
        <a href="#method" class="go">Full method ↓</a>
      </div>`;
  }

  /* ── the index ────────────────────────────────────────── */
  const COLS = [
    ["injured", "Hurt", "Players who missed a game on your roster"],
    ["games", "Games", "Player-games missed"],
    ["dollar_games", "Bill", "Dollars paid × games missed"],
    ["per_week", "$/wk", "Average dollars sidelined per week"],
    ["points", "Shelf", "Points on the shelf: games missed × healthy average"],
    ["due", "Due", "Dollars already ruled out for next week"],
  ];
  let sortKey = "dollar_games";

  function indexRows() {
    const rows = [...D.teams].sort((a, b) => (b[sortKey] - a[sortKey]) || (b.dollar_games - a.dollar_games) || (b.games - a.games));
    return rows.map((t, i) => `<details class="ix-row" id="t-${esc(t.team_id)}" data-id="${esc(t.team_id)}">
      <summary>
        <span class="ix-n">${i + 1}</span>
        <span class="ix-team">${logo(t)}<span><b>${esc(t.name)}</b><small>${esc(t.manager)} · ${esc(t.record)}</small></span></span>
        ${COLS.map(([k]) => `<span class="ix-c${k === sortKey ? " on" : ""}${k === "dollar_games" ? " big" : ""}" data-k="${k}">${
          k === "per_week" ? money(t[k]) : k === "due" ? (t.due ? money(t.due) : "–") : fmt(t[k])}</span>`).join("")}
        <span class="ix-sub">${t.injured} hurt · ${t.games} games · ${t.now} in the ward</span>
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
        <span>Bill <b>${fmt(t.dollar_games)}</b></span><span>Rank by bill <b>${t.rank} of 14</b></span>
        <span>Players hurt <b>${t.injured}</b></span><span>Games <b>${t.games}</b></span>
        <span>Points on the shelf <b>${fmt(t.points)}</b></span><span>IR slot used <b>${pl(t.ir_weeks, "week")}</b></span>
      </div>
      ${t.ledger.length ? `<div class="ix-led">
        <div class="ix-led-hd"><span>Player</span><span>How</span><span>Paid</span><span>Missed (wk 1–${W})</span><span>Injury</span><span>Bill</span></div>
        ${t.ledger.map((p) => `<div class="ix-led-r">
          <span class="nm">${pos(p.pos)} <b>${esc(p.name)}</b></span>
          <span class="how ${p.how}">${HOW[p.how]}</span>
          <span class="paid">${money(p.paid)}</span>
          <span class="wk">${dots(p.weeks, W)} <i>${p.games}</i></span>
          <span class="inj">${esc(p.part || "Not disclosed")}</span>
          <span class="bill${p.dg ? "" : " z"}">${fmt(p.dg)}</span>
        </div>`).join("")}
      </div>` : ""}
      ${ghosts}
      ${ward.length ? `<div class="ix-ward-mini"><span class="k">Week ${D.report_week} report</span>${ward.map((n) =>
        `<span>${statusChip(n.status)} ${esc(n.name)}</span>`).join("")}</div>` : ""}
      <div class="ix-foot">${stamps("inj-" + t.team_id)}</div>`;
  }

  function index() {
    return `<section class="ix-sec" id="index">
      <div class="sec-top"><h2 class="h-sec">The Index</h2><span class="note">Click a column to re-rank · click a team for the ledger</span></div>
      <hr class="rule-h">
      <p class="ix-lede">The <b>Bill</b> is the headline number: what each injured player cost the team that held him, times the games
        he sat. <b>Hurt</b> is the raw count of players. <b>Shelf</b> is the points those players would have scored at their healthy
        average. <b>Due</b> is what is already ruled out for Week ${D.report_week}.</p>
      <div class="ix-table">
        <div class="ix-hd">
          <span>#</span><span>Team</span>
          ${COLS.map(([k, l, tip]) => `<button type="button" class="ix-sort${k === sortKey ? " on" : ""}" data-k="${k}" title="${esc(k === "due" ? `Dollars ruled out for Week ${D.report_week}` : tip)}">${l}</button>`).join("")}
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
    const iron = by((a, b) => a.dollar_games - b.dollar_games || a.games - b.games);
    const due = by((a, b) => b.due - a.due);
    const cheap = [...T].filter((t) => t.games >= 10).sort((a, b) => (a.dollar_games / a.games) - (b.dollar_games / b.games))[0];
    const worst = D.players[0];
    const wTeam = TM[worst.owners[0].team_id];
    const shelf = by((a, b) => b.points - a.points);
    const A = [
      { k: "The Mash Unit", who: T[0], v: fmt(T[0].dollar_games), u: "bill",
        s: `Biggest injury bill in the league. ${T[0].ledger[0].name} and ${T[0].ledger.length > 1 ? T[0].ledger[1].name : "friends"} did most of the damage.` },
      { k: "Body Count", who: bodies, v: bodies.injured, u: "players",
        s: tiedBodies.length > 1 ? `Tied with ${tiedBodies.filter((t) => t !== bodies).map((t) => clean(t.name)).join(" and ")} for the most players lost.` : `Most players lost to injury. ${bodies.games} games missed between them.` },
      { k: "Iron Man", who: iron, v: fmt(iron.dollar_games), u: "bill",
        s: `Smallest bill in the league, and a ${iron.record} record. Health is a skill until it isn't.` },
      { k: "Clearance Rack", who: cheap, v: (cheap.dollar_games / cheap.games).toFixed(1), u: "$ per game lost",
        s: `${cheap.games} games missed and almost none of them cost anything. Only bargain-bin players get hurt here.` },
      { k: "Most Expensive Injury", who: wTeam, v: fmt(worst.dollar_games), u: "bill",
        s: `${worst.name}: ${money(worst.cost)} at the draft, ${pl(worst.games, "game")} missed, ${(worst.part || "undisclosed").toLowerCase()}.` },
      { k: "Bill Due", who: due, v: money(due.due), u: `out for wk ${D.report_week}`,
        s: `The most money already ruled out for Week ${D.report_week}: ${NOW.filter((n) => n.team_id === due.team_id && n.status !== "Questionable").map((n) => n.name).join(", ")}.` },
      { k: "Points on the Shelf", who: shelf, v: fmt(shelf.points), u: "points",
        s: `More healthy-average points sitting in street clothes than anyone else.` },
    ];
    // The team named after the injured reserve list gets its own line if it earned one
    const ir = T.find((t) => /injured reserved/i.test(t.name));
    if (ir) {
      const gr = [...T].sort((a, b) => b.games - a.games).findIndex((t) => t === ir) + 1;
      A.push({ k: "Nominative Determinism", who: ir, v: ir.games, u: "games missed",
        s: gr === 1 ? `The team named The Injured Reserved has missed more games than anyone. ${ir.rank === 14 ? "" : `Its bill ranks ${ord(ir.rank)} because it only ever loses the cheap guys.`}`
                    : `Named for the IR, ranked ${gr} in games missed. Living up to it.` });
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
    const xs = T.map((t) => t.dollar_games), ys = T.map((t) => t.wins);
    const { r, a, b } = corr(xs, ys);
    const W = 640, H = 330, L = 44, R = 18, Tp = 16, B = 40;
    const xmax = Math.ceil(Math.max(...xs) / 100) * 100;
    const X = (v) => L + (v / xmax) * (W - L - R), Y = (v) => Tp + (1 - v / G) * (H - Tp - B);
    const ticks = []; for (let v = 0; v <= xmax; v += 100) ticks.push(v);
    const yt = []; for (let v = 0; v <= G; v += 3) yt.push(v);
    // label placement: nudge labels so neighbours do not collide
    const pts = T.map((t) => ({ t, x: X(t.dollar_games), y: Y(t.wins) })).sort((p, q) => p.y - q.y || p.x - q.x);
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
    const verdict = r < -0.6 ? "a strong link" : r < -0.35 ? "a real link, but a loose one" : r < -0.15 ? "a weak link" : "next to no link";
    return `<section class="ix-sec" id="standings">
      <div class="sec-top"><h2 class="h-sec">Does It Explain the Standings?</h2><span class="note">r = ${r.toFixed(2).replace("-", "−")}</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Injury bill against wins, median game included. The correlation is ${r.toFixed(2).replace("-", "−")}: ${verdict}.
        Every 100 points of bill is worth about ${Math.abs(b * 100).toFixed(1)} wins the wrong way. Teams above the line are winning
        through it; teams below it have no excuse in the trainer's room.</p>
      <div class="ix-chart">
        <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Injury bill against wins for all 14 teams">
          ${ticks.map((v) => `<line x1="${X(v)}" x2="${X(v)}" y1="${Tp}" y2="${H - B}" class="g"/><text x="${X(v)}" y="${H - B + 16}" class="tx" text-anchor="middle">${v}</text>`).join("")}
          ${yt.map((v) => `<line x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}" class="g"/><text x="${L - 8}" y="${Y(v) + 4}" class="tx" text-anchor="end">${v}</text>`).join("")}
          <line x1="${X(0)}" y1="${Y(a)}" x2="${X(xmax)}" y2="${Y(a + b * xmax)}" class="fit"/>
          <text x="${(L + W - R) / 2}" y="${H - 6}" class="ax" text-anchor="middle">INJURY BILL →</text>
          <text x="12" y="${(Tp + H - B) / 2}" class="ax" text-anchor="middle" transform="rotate(-90 12 ${(Tp + H - B) / 2})">WINS →</text>
          ${pts.map((p) => `<g class="pt${p.t.rank <= 3 ? " hot" : ""}"><title>${esc(clean(p.t.name))}: bill ${fmt(p.t.dollar_games)}, ${esc(p.t.record)}</title>
            <rect x="${p.x - 5}" y="${p.y - 5}" width="10" height="10"/>
            <text x="${p.lx}" y="${p.ly + 4}" text-anchor="${p.side}" class="lb">${esc(p.t.manager)}</text></g>`).join("")}
        </svg>
      </div>
    </section>`;
  }

  /* ── the ward calendar (heatmap) ──────────────────────── */
  function calendar() {
    const W = D.through_week;
    const max = Math.max(1, ...D.teams.flatMap((t) => t.weekly.map((w) => w.dollars)));
    const lw = D.league_weekly;
    const lmax = Math.max(...lw.map((w) => w.dollars));
    return `<section class="ix-sec" id="calendar">
      <div class="sec-top"><h2 class="h-sec">The Ward Calendar</h2><span class="note">Dollars sidelined, team by week</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Each cell is what that team had in street clothes that week. Darker red, more money on the shelf. A gray cell
        means bodies were missing but none of them cost anything. Hover a cell for the names.</p>
      <div class="ix-heat" style="--w:${W}">
        <div class="hh"><span></span>${Array.from({ length: W }, (_, i) => `<span>W${i + 1}</span>`).join("")}<span>Bill</span></div>
        ${D.teams.map((t) => `<div class="hr">
          <span class="ht">${logo(t)}<b>${esc(clean(t.name))}</b></span>
          ${t.weekly.map((w) => {
            const a = w.dollars ? 0.16 + 0.84 * (w.dollars / max) : 0;
            const cls = w.dollars ? (a > 0.55 ? " dk" : "") : w.games ? " free" : " none";
            return `<span class="hc${cls}" style="${w.dollars ? `--a:${a.toFixed(3)}` : ""}" title="${esc(`Week ${w.week}: ${w.games ? w.who.join(", ") : "nobody hurt"}${w.dollars ? ` (${money(w.dollars)})` : ""}`)}">${w.dollars ? fmt(w.dollars) : w.games ? w.games + "×" : ""}</span>`;
          }).join("")}
          <span class="hb">${fmt(t.dollar_games)}</span>
        </div>`).join("")}
        <div class="hr tot"><span class="ht"><b>League</b></span>${lw.map((w) => `<span class="hc lg" title="Week ${w.week}: ${w.games} games missed">
          <i style="height:${Math.round(100 * w.dollars / lmax)}%"></i><em>${fmt(w.dollars)}</em></span>`).join("")}<span class="hb">${fmt(D.totals.dollar_games)}</span></div>
      </div>
    </section>`;
  }

  /* ── the most expensive injuries ──────────────────────── */
  function expensive() {
    const W = D.through_week;
    const list = D.players.slice(0, 12);
    return `<section class="ix-sec" id="players">
      <div class="sec-top"><h2 class="h-sec">The Most Expensive Injuries</h2><span class="note">Bill = what he cost × games missed</span></div>
      <hr class="rule-h">
      <div class="ix-pg">${list.map((p, i) => {
        const owners = p.owners.map((o) => `${esc(clean(TM[o.team_id].name))}${p.owners.length > 1 ? ` (${o.games})` : ""}`).join(", ");
        const now = NOW.find((n) => n.name === p.name);
        return `<article class="pc${i === 0 ? " lead" : ""}">
          <div class="pc-top"><span class="pc-n">${i + 1}</span>${pos(p.pos)}<b class="pc-name">${esc(p.name)}</b>${now ? statusChip(now.status) : ""}</div>
          <div class="pc-math"><span>${money(p.cost)}</span><i>×</i><span>${p.games} gm</span><i>=</i><b>${fmt(p.dollar_games)}</b></div>
          <div class="pc-wk">${dots(p.weeks, W)}</div>
          <div class="pc-meta"><span>${esc(p.part || "Not disclosed")}</span><span>${owners}</span></div>
          <div class="pc-meta"><span>Healthy avg ${p.ppg.toFixed(1)}</span><span>${fmt(p.points)} pts on the shelf</span></div>
        </article>`;
      }).join("")}</div>
      <details class="ix-all">
        <summary>All ${D.players.length} injured players</summary>
        <div class="ix-led all">
          <div class="ix-led-hd"><span>Player</span><span>Held by</span><span>Draft $</span><span>Missed</span><span>Injury</span><span>Bill</span></div>
          ${D.players.map((p) => `<div class="ix-led-r">
            <span class="nm">${pos(p.pos)} <b>${esc(p.name)}</b></span>
            <span class="how">${p.owners.map((o) => esc(TM[o.team_id].manager)).join(", ")}</span>
            <span class="paid">${p.cost ? money(p.cost) : "–"}</span>
            <span class="wk">${dots(p.weeks, W)} <i>${p.games}</i></span>
            <span class="inj">${esc(p.part || "Not disclosed")}</span>
            <span class="bill${p.dollar_games ? "" : " z"}">${fmt(p.dollar_games)}</span>
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
            return `<li>${pos(p.pos)}<span class="pn"><b>${esc(p.name)}</b><small>${money(p.cost)} · missed ${p.missed_before} before the deal, ${p.missed_after} since</small></span>${now ? statusChip(now.status) : `<span class="ix-st ok">Healthy</span>`}</li>`;
          }).join("")}</ul>
        </div>`;
      });
      // the line: who bought a player that is now hurt
      const bad = [];
      tr.sides.forEach((s) => s.got.forEach((p) => {
        const now = NOW.find((n) => n.name === p.name);
        if (now && now.status !== "Questionable") bad.push({ team: TM[s.team_id], p, now });
      }));
      const note = bad.length
        ? bad.map((x) => `${x.team.manager} traded for ${x.p.name} in Week ${tr.week}. ${x.now.status === "Out" || x.now.status === "Doubtful" ? `He is ${x.now.status.toLowerCase()} for Week ${D.report_week}` : `He is on ${x.now.status} for Week ${D.report_week}`}${x.now.part ? ` (${x.now.part.toLowerCase()})` : ""}, which makes him ${money(x.p.cost)} of injury bill every week he sits from here.`).join(" ")
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
      <p class="ix-lede">A traded player's draft price travels with him, so his missed games bill whoever holds him that week. Games he
        missed before the deal stay on the seller's tab. The full trade verdicts live in <a href="trades.html">Trade Court</a>.</p>
      <div class="cl-grid">${cards}</div>
    </section>`;
  }

  /* ── this week's ward ─────────────────────────────────── */
  function ward() {
    const by = {};
    NOW.forEach((n) => (by[n.team_id] = by[n.team_id] || []).push(n));
    const teams = [...D.teams].sort((a, b) => b.due - a.due || b.now - a.now || (by[b.team_id] || []).length - (by[a.team_id] || []).length);
    return `<section class="ix-sec" id="ward">
      <div class="sec-top"><h2 class="h-sec">This Week's Ward</h2><span class="note">Week ${D.report_week} injury report</span></div>
      <hr class="rule-h">
      <p class="ix-lede">Everyone on a Week ${D.through_week} roster who is on injured reserve or carries a game status for Week ${D.report_week}.
        <span class="ix-st ir">IR</span> and <span class="ix-st out">Out</span> are already on the bill;
        <span class="ix-st dbt">Dbt</span> (doubtful) almost certainly will be; <span class="ix-st q">Q</span> (questionable) is a coin flip.</p>
      <div class="wd-grid">${teams.map((t) => {
        const list = by[t.team_id] || [];
        return `<div class="wd${t.due ? " hot" : ""}">
          <div class="wd-hd">${logo(t)}<span><b>${esc(clean(t.name))}</b><small>${esc(t.manager)}</small></span>
            <span class="wd-due">${t.due ? money(t.due) : "–"}<small>out</small></span></div>
          ${list.length ? `<ul>${list.map((n) => `<li>${statusChip(n.status)}<span class="pn">${esc(n.name)}<small>${esc(n.pos)} · ${esc(n.part || "undisclosed")}${n.cost ? ` · ${money(n.cost)}` : ""}</small></span></li>`).join("")}</ul>`
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
        <dt>On the shelf</dt><dd>${esc(m.points)}</dd>
        <dt>Source</dt><dd>${esc(m.source)}</dd>
      </dl>
    </section>
    <section class="ix-band">
      <h2 class="display">Draft day is a promise. The trainer's room is the bill.</h2>
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
