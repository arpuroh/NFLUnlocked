/* NFL Unlocked · The Rivalry Index.
   Renders data/rivalries.json (built by scripts/build_rivalries.py): every head-to-head game since
   2011, by manager. The hottest rivalries (heat = volume x closeness x drama x balance), the full
   head-to-head grid, who owns whom, a head-to-head finder with every game on record, each manager's
   file, this week's grudge matches and the all-time series records. Median games are not rivalries
   and are not counted. Uses NU.stamps / NU.wireStamps from app.js. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const f1 = (n) => (Math.round(n * 10) / 10).toFixed(1);
  const f2 = (n) => Number(n).toFixed(2);
  const hasNU = () => typeof NU !== "undefined" && NU && NU.stamps;
  const stamps = (id) => (hasNU() ? NU.stamps(id, {}, { min: 3 }) : "");
  const slug = (m) => m.toLowerCase().replace(/[()]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const KIND = { final: "Title game", third: "3rd place", playoff: "Playoffs" };

  let D, PK, MG, ACTIVE;
  const pairOf = (x, y) => PK[[x, y].sort().join("|")];
  // a pair seen from x's side
  const side = (p, x) => x === p.a
    ? { me: p.a, op: p.b, w: p.aw, l: p.bw, pf: p.apf, pa: p.bpf, po_w: p.po_aw, po_l: p.po_bw }
    : { me: p.b, op: p.a, w: p.bw, l: p.aw, pf: p.bpf, pa: p.apf, po_w: p.po_bw, po_l: p.po_aw };
  const rec = (w, l, t) => `${w}-${l}${t ? "-" + t : ""}`;
  const logo = (m, cls = "sm") => D.logos[m] ? `<img class="tlogo ${cls}" src="${esc(D.logos[m])}" alt="" loading="lazy">` : "";

  function leader(p) {
    if (p.aw === p.bw) return `Series tied ${rec(p.aw, p.bw, p.t)}`;
    const [w, l, who] = p.aw > p.bw ? [p.aw, p.bw, p.a] : [p.bw, p.aw, p.b];
    return `${who} leads ${rec(w, l, p.t)}`;
  }
  function streakTxt(p) {
    if (!p.streak.who || p.streak.n < 2) return p.streak.who ? `${p.streak.who} won the last one` : "Last one was a tie";
    return `${p.streak.who} has won ${p.streak.n} straight`;
  }
  // longest run by either side, from the game log
  function longest(p) {
    let best = { who: null, n: 0 }, cur = { who: null, n: 0 };
    p.log.forEach((g) => {
      const w = g.pa > g.pb ? p.a : g.pb > g.pa ? p.b : null;
      if (w && w === cur.who) cur.n++; else cur = { who: w, n: w ? 1 : 0 };
      if (cur.n > best.n) best = { ...cur };
    });
    return best;
  }

  function splitBar(p) {
    const n = p.games, a = (100 * p.aw / n).toFixed(1), t = (100 * p.t / n).toFixed(1);
    return `<div class="rv-split" title="${esc(p.a)} ${p.aw} · ${esc(p.b)} ${p.bw}${p.t ? " · ties " + p.t : ""}">
      <i class="a${p.aw >= p.bw ? " lead" : ""}" style="width:${a}%"></i>${p.t ? `<i class="t" style="width:${t}%"></i>` : ""}<i class="b${p.bw >= p.aw ? " lead" : ""}"></i></div>`;
  }

  function gameLog(p, x) {
    const s = x || p.a;
    return `<div class="rv-log">
      <div class="rv-log-hd"><span>Season</span><span>Wk</span><span>${esc(s)}</span><span></span><span>${esc(s === p.a ? p.b : p.a)}</span><span>Margin</span></div>
      ${p.log.slice().reverse().map((g) => {
        const [mine, theirs, mn, tn] = s === p.a ? [g.pa, g.pb, g.an, g.bn] : [g.pb, g.pa, g.bn, g.an];
        const won = mine > theirs, tie = mine === theirs;
        return `<div class="rv-log-r ${won ? "w" : tie ? "t" : "l"}${g.kind !== "reg" ? " po" : ""}">
          <span class="y">${g.y}</span><span class="wk">${g.w}${g.kind !== "reg" ? `<em>${KIND[g.kind]}</em>` : ""}</span>
          <span class="s"><b>${f2(mine)}</b><small>${esc(mn)}</small></span>
          <span class="r">${won ? "W" : tie ? "T" : "L"}</span>
          <span class="s"><b>${f2(theirs)}</b><small>${esc(tn)}</small></span>
          <span class="m">${won ? "+" : tie ? "" : "−"}${f2(Math.abs(mine - theirs))}</span>
        </div>`;
      }).join("")}
    </div>`;
  }

  /* ── hero ─────────────────────────────────────────────── */
  function hero(ranked) {
    const top = ranked[0], T = D.totals;
    const closeAll = D.pairs.reduce((a, p) => a + p.close, 0);
    const most = [...D.pairs].sort((a, b) => b.games - a.games)[0];
    const owned = ranked.filter((p) => p.games >= 10).sort((a, b) => (1 - b.balance) - (1 - a.balance) || b.games - a.games)[0];
    const [ow, ol, ob, ov] = owned.aw > owned.bw ? [owned.aw, owned.bw, owned.a, owned.b] : [owned.bw, owned.aw, owned.b, owned.a];
    return `
      <section class="dark roast-hero rv-hero">
        <div class="hero-grid">
          <div>
            <div class="filed"><span class="tag-red">The Rivalry Index</span>
              <span class="eyebrow">${D.first}–${D.last} · ${T.games} head-to-head games · ${T.managers} managers</span></div>
            <h1 class="display">${esc(top.a)} vs ${esc(top.b)}.
              <span class="kick">The hottest feud in the league: ${rec(Math.max(top.aw, top.bw), Math.min(top.aw, top.bw), top.t)} over ${top.games} games, ${top.changes} lead changes.</span></h1>
            <p class="lede">Every matchup since ${D.first}, by manager, through every team rename. Ranked by heat: how often they
              meet, how close it is, how often the lead has flipped and whether it ever mattered in January.
              ${esc(most.a)} and ${esc(most.b)} have played more than anyone (${most.games} times). ${esc(ob)} owns ${esc(ov)} ${ow}-${ol}.</p>
            <div class="hero-actions">
              <a class="btn-red" href="#hot">The hottest rivalries →</a>
              <a class="btn-ghost" href="#grid">The grid →</a>
              <a class="btn-ghost" href="#finder">Look up a matchup →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">Heat index · Top 5</div>
            ${ranked.slice(0, 5).map((p, i) => `<a class="board-row" href="#r-${i}" data-pair="${esc(p.a)}|${esc(p.b)}">
              <span class="bn">${i + 1}</span>
              <span class="bt">${esc(p.a)} vs ${esc(p.b)}<small>${esc(leader(p))} · ${p.games} games</small></span>
              <span class="bm">${Math.round(p.heat)}</span></a>`).join("")}
            <a class="see-all" href="#hot">Top 12 →</a>
          </div>
        </div>
      </section>
      <section class="statbug">
        <div class="cell"><div class="eyebrow">Head-to-head games</div><div class="v">${T.games.toLocaleString("en-US")}</div><div class="s">${D.first} to Week ${D.through_week} of ${D.last}</div></div>
        <div class="cell"><div class="eyebrow">One-score games</div><div class="v red">${closeAll}</div><div class="s">decided by under ${D.close} points</div></div>
        <div class="cell"><div class="eyebrow">Playoff meetings</div><div class="v">${T.playoff}</div><div class="s">bracket games, title games included</div></div>
        <div class="cell"><div class="eyebrow">Most-played series</div><div class="v">${most.games}</div><div class="s">${esc(most.a)} vs ${esc(most.b)} · ${esc(leader(most))}</div></div>
      </section>`;
  }

  /* ── the hottest rivalries ────────────────────────────── */
  function hot(ranked) {
    return `<section class="rv-sec" id="hot">
      <div class="sec-top"><h2 class="h-sec">The Hottest Rivalries</h2><span class="note">Ranked by heat · ${D.min_games}+ meetings</span></div>
      <hr class="rule-h">
      <p class="rv-lede">Heat rewards volume, one-score games, playoff meetings and series lead changes, then discounts it all when
        one side has been winning every time. A long, even, bitter series beats a short lopsided one. Open a card for every game.</p>
      <div class="rv-cards">${ranked.slice(0, 12).map((p, i) => {
        const L = longest(p), last = p.log[p.log.length - 1];
        const lastW = last.pa > last.pb ? p.a : last.pb > last.pa ? p.b : null;
        return `<details class="rv-card${i === 0 ? " lead" : ""}" id="r-${i}">
          <summary>
            <div class="rc-top"><span class="rc-n">${i + 1}</span>
              <span class="rc-names">${logo(p.a)}<b>${esc(p.a)}</b><i>vs</i><b>${esc(p.b)}</b>${logo(p.b)}</span>
              <span class="rc-heat"><b>${Math.round(p.heat)}</b><small>Heat</small></span></div>
            <div class="rc-rec"><span class="${p.aw > p.bw ? "lead" : ""}">${p.aw}</span>${splitBar(p)}<span class="${p.bw > p.aw ? "lead" : ""}">${p.bw}</span></div>
            <div class="rc-line">${esc(leader(p))}. ${esc(streakTxt(p))}.</div>
            <div class="rc-facts">
              <span><b>${p.games}</b> games</span><span><b>${p.close}</b> one-score</span>
              <span><b>${p.changes}</b> lead changes</span><span><b>${p.playoff}</b> playoff${p.finals ? ` · ${p.finals} title` : ""}</span>
              <span>Longest run <b>${L.n}</b> (${esc(L.who || "")})</span>
              <span>Last: ${last.y} Wk ${last.w}, ${esc(lastW || "tie")} ${f1(Math.abs(last.pa - last.pb))}</span>
            </div>
            <span class="rc-open">Every game ▸</span>
          </summary>
          <div class="rc-body">${gameLog(p)}<div class="rc-foot">${stamps("riv-" + slug(p.a) + "-" + slug(p.b))}</div></div>
        </details>`;
      }).join("")}</div>
    </section>`;
  }

  /* ── the grid ─────────────────────────────────────────── */
  function grid() {
    const ms = ACTIVE.map((m) => m.manager);
    return `<section class="rv-sec" id="grid">
      <div class="sec-top"><h2 class="h-sec">The Grid</h2><span class="note">Read across: the row manager's record against each column</span></div>
      <hr class="rule-h">
      <p class="rv-lede">Every active manager against every other, all time. <b class="rd">Red</b> means the row manager owns that
        series, <b>gray</b> means he is owned, white is close to even. Click any cell for the full series.</p>
      <div class="rv-grid-wrap"><table class="rv-grid">
        <thead><tr><th></th>${ms.map((m) => `<th><span>${esc(m)}</span></th>`).join("")}<th class="tot">All</th></tr></thead>
        <tbody>${ms.map((r) => `<tr><th>${esc(r)}</th>${ms.map((c) => {
          if (r === c) return `<td class="self"></td>`;
          const p = pairOf(r, c);
          if (!p) return `<td class="none">–</td>`;
          const s = side(p, r), pct = (s.w + 0.5 * p.t) / p.games;
          const d = pct - 0.5, cls = d > 0.04 ? "up" : d < -0.04 ? "dn" : "ev";
          const a = Math.min(1, Math.abs(d) * 2.2).toFixed(2);
          return `<td class="${cls}" style="--a:${a}" data-pair="${esc(r)}|${esc(c)}" title="${esc(r)} vs ${esc(c)}: ${rec(s.w, s.l, p.t)}">${s.w}-${s.l}</td>`;
        }).join("")}<td class="tot">${(() => { const m = MG[r]; return `${m.w}-${m.l}`; })()}</td></tr>`).join("")}</tbody>
      </table></div>
    </section>`;
  }

  /* ── who owns whom ────────────────────────────────────── */
  function owns() {
    const list = D.pairs.filter((p) => p.games >= D.min_games && p.aw !== p.bw).map((p) => {
      const [w, l, o, v] = p.aw > p.bw ? [p.aw, p.bw, p.a, p.b] : [p.bw, p.aw, p.b, p.a];
      return { p, w, l, o, v, pct: w / (w + l) };
    }).sort((x, y) => y.pct - x.pct || y.w - x.w).slice(0, 10);
    return `<div class="rv-mod">
      <h3 class="rv-h3">Who Owns Whom</h3><hr class="rule-h">
      <p class="rv-small">The most one-sided series with ${D.min_games}+ meetings. Landlord on the left.</p>
      ${list.map((x, i) => `<a class="ow-r" href="#finder" data-pair="${esc(x.o)}|${esc(x.v)}">
        <span class="n">${i + 1}</span><span class="who"><b>${esc(x.o)}</b> owns ${esc(x.v)}<small>${x.p.games} games · ${x.p.first}–${x.p.last}${x.p.active ? "" : " · closed"}</small></span>
        <span class="r">${x.w}-${x.l}</span></a>`).join("")}
    </div>`;
  }

  /* ── records ──────────────────────────────────────────── */
  function records() {
    const all = D.pairs.flatMap((p) => p.log.map((g) => ({ p, g, m: Math.abs(g.pa - g.pb) })));
    const blow = all.slice().sort((a, b) => b.m - a.m)[0];
    const tight = all.filter((x) => x.m > 0).sort((a, b) => a.m - b.m)[0];
    const ties = all.filter((x) => x.m === 0).length;
    const runs = D.pairs.map((p) => ({ p, L: longest(p) })).sort((a, b) => b.L.n - a.L.n)[0];
    const po = D.pairs.slice().sort((a, b) => b.playoff - a.playoff || b.finals - a.finals)[0];
    const flips = D.pairs.slice().sort((a, b) => b.changes - a.changes)[0];
    const W = (x) => x.g.pa > x.g.pb ? [x.p.a, x.p.b, x.g.pa, x.g.pb] : [x.p.b, x.p.a, x.g.pb, x.g.pa];
    const [bw, bl, bs1, bs2] = W(blow), [tw, tl, ts1, ts2] = W(tight);
    const R = [
      ["Biggest beatdown", `${f1(blow.m)}`, `${bw} over ${bl}, ${f2(bs1)} to ${f2(bs2)} · ${blow.g.y} Wk ${blow.g.w}`],
      ["Closest finish", f2(tight.m), `${tw} over ${tl}, ${f2(ts1)} to ${f2(ts2)} · ${tight.g.y} Wk ${tight.g.w}`],
      ["Longest run in a series", runs.L.n, `${runs.L.who} over ${runs.L.who === runs.p.a ? runs.p.b : runs.p.a}`],
      ["Most playoff meetings", po.playoff, `${po.a} and ${po.b} · ${po.a} ${po.po_aw}, ${po.b} ${po.po_bw}`],
      ["Most lead changes", flips.changes, `${flips.a} and ${flips.b} · ${leader(flips)}`],
    ];
    if (ties) R.push(["Ties on record", ties, "Every one of them a refund nobody asked for"]);
    return `<div class="rv-mod">
      <h3 class="rv-h3">Series Records</h3><hr class="rule-h">
      ${R.map(([k, v, s]) => `<div class="sr-r"><span class="k">${esc(k)}</span><b>${esc(v)}</b><small>${esc(s)}</small></div>`).join("")}
    </div>`;
  }

  /* ── this week's grudge matches ───────────────────────── */
  function grudge() {
    if (!D.next.length) return "";
    return `<section class="rv-sec" id="grudge">
      <div class="sec-top"><h2 class="h-sec">Week ${D.next_week} Grudge Matches</h2><span class="note">The history behind this week's games</span></div>
      <hr class="rule-h">
      <div class="gm-grid">${D.next.map((g) => {
        const p = pairOf(g.ma, g.mb);
        if (!p) return `<div class="gm first">
          <div class="gm-hd"><span class="t">${logo(g.ma)}<span><b>${esc(g.ma)}</b><small>${esc(g.ta)}</small></span></span>
            <span class="rr"><b>0-0</b><small>all time</small></span>
            <span class="t r"><span><b>${esc(g.mb)}</b><small>${esc(g.tb)}</small></span>${logo(g.mb)}</span></div>
          <div class="rv-split"></div>
          <p class="gm-first">First meeting ever. Whoever wins Sunday owns this series until further notice.</p>
        </div>`;
        const s = side(p, g.ma), ranked = RANK.indexOf(p);
        return `<div class="gm" data-pair="${esc(g.ma)}|${esc(g.mb)}">
          <div class="gm-hd"><span class="t">${logo(g.ma)}<span><b>${esc(g.ma)}</b><small>${esc(g.ta)}</small></span></span>
            <span class="rr"><b>${s.w}-${s.l}${p.t ? "-" + p.t : ""}</b><small>all time</small></span>
            <span class="t r"><span><b>${esc(g.mb)}</b><small>${esc(g.tb)}</small></span>${logo(g.mb)}</span></div>
          ${splitBar(p.a === g.ma ? p : { ...p, aw: p.bw, bw: p.aw })}
          <p>${esc(streakTxt(p))}. ${p.close} of ${p.games} decided by one score${p.playoff ? `, ${p.playoff} in the playoffs` : ""}.${ranked >= 0 && ranked < 25 ? ` Heat rank ${ranked + 1}.` : ""}</p>
        </div>`;
      }).join("")}</div>
    </section>`;
  }

  /* ── head-to-head finder ──────────────────────────────── */
  function finder() {
    const opts = (sel) => D.managers.map((m) => `<option value="${esc(m.manager)}"${m.manager === sel ? " selected" : ""}>${esc(m.manager)}${m.active ? "" : " (former)"}</option>`).join("");
    const [a, b] = [RANK[0].a, RANK[0].b];
    return `<section class="rv-sec" id="finder">
      <div class="sec-top"><h2 class="h-sec">Head to Head</h2><span class="note">Any two managers, every game</span></div>
      <hr class="rule-h">
      <div class="hf-tools">
        <select id="hf-a" aria-label="First manager">${opts(a)}</select><span class="vs">vs</span>
        <select id="hf-b" aria-label="Second manager">${opts(b)}</select>
        <button type="button" id="hf-swap" class="hf-swap" aria-label="Swap">⇄</button>
      </div>
      <div id="hf-out"></div>
    </section>`;
  }
  function finderOut(a, b) {
    const box = $("#hf-out");
    if (a === b) { box.innerHTML = `<p class="rv-small">Pick two different managers.</p>`; return; }
    const p = pairOf(a, b);
    if (!p) { box.innerHTML = `<p class="rv-small">${esc(a)} and ${esc(b)} have never played each other.</p>`; return; }
    const s = side(p, a), rank = RANK.indexOf(p), L = longest(p);
    const mov = (s.pf - s.pa) / p.games;
    box.innerHTML = `<div class="hf">
      <div class="hf-score">
        <div class="hs ${s.w > s.l ? "lead" : ""}">${logo(a, "lg")}<b>${esc(a)}</b><span>${s.w}</span></div>
        <div class="hm">${p.t ? `<small>${p.t} tie${p.t > 1 ? "s" : ""}</small>` : ""}<i>–</i></div>
        <div class="hs r ${s.l > s.w ? "lead" : ""}"><span>${s.l}</span><b>${esc(b)}</b>${logo(b, "lg")}</div>
      </div>
      ${splitBar(p.a === a ? p : { ...p, aw: p.bw, bw: p.aw })}
      <div class="hf-facts">
        <span>Games <b>${p.games}</b></span><span>Since <b>${p.first}</b></span>
        <span>Points <b>${f1(s.pf)}–${f1(s.pa)}</b></span><span>Avg margin <b>${mov >= 0 ? "+" : "−"}${f1(Math.abs(mov))}</b> ${esc(a)}</span>
        <span>One-score <b>${p.close}</b></span><span>Lead changes <b>${p.changes}</b></span>
        <span>Playoffs <b>${s.po_w}-${s.po_l}</b></span><span>Longest run <b>${L.n}</b> ${esc(L.who || "")}</span>
        <span>Heat <b>${Math.round(p.heat)}</b>${p.games >= D.min_games && rank >= 0 ? ` (rank ${D.pairs.filter((x) => x.games >= D.min_games).indexOf(p) + 1})` : ""}</span>
      </div>
      <p class="hf-line">${esc(streakTxt(p))}. Biggest win: ${esc((p.biggest.pa > p.biggest.pb) ? p.a : p.b)} by ${f1(Math.abs(p.biggest.pa - p.biggest.pb))} in ${p.biggest.y}.
        Closest: ${f2(Math.abs(p.closest.pa - p.closest.pb))} in ${p.closest.y} Week ${p.closest.w}.</p>
      ${gameLog(p, a)}
    </div>`;
  }

  /* ── manager files ────────────────────────────────────── */
  function files() {
    return `<section class="rv-sec" id="files">
      <div class="sec-top"><h2 class="h-sec">Manager Files</h2><span class="note">Pick a manager</span></div>
      <hr class="rule-h">
      <div class="mf-chips">${ACTIVE.map((m, i) => `<button type="button" class="mf-chip${i === 0 ? " on" : ""}" data-m="${esc(m.manager)}">${esc(m.manager)}</button>`).join("")}</div>
      <div id="mf-out"></div>
    </section>`;
  }
  function fileOut(name) {
    const m = MG[name];
    const max = Math.max(...m.vs.map((v) => v.g));
    const vs = m.vs.slice().sort((a, b) => ((b.w - b.l) - (a.w - a.l)) || b.g - a.g);
    const pw = m.vs.reduce((a, v) => a + v.po_w, 0), pl = m.vs.reduce((a, v) => a + v.po_l, 0);
    $("#mf-out").innerHTML = `<div class="mf">
      <div class="mf-hd">${logo(name, "lg")}<div><b>${esc(name)}</b><small>${esc(D.teams26[name] || "")}</small></div>
        <div class="mf-k"><span>All-time H2H <b>${rec(m.w, m.l, m.t)}</b></span><span>Win pct <b>${(m.pct * 100).toFixed(1)}</b></span>
          <span>Playoffs <b>${pw}-${pl}</b></span>
          ${m.nemesis ? `<span>Nemesis <b class="rd">${esc(m.nemesis)}</b></span>` : ""}${m.victim ? `<span>Favorite victim <b>${esc(m.victim)}</b></span>` : ""}</div></div>
      <div class="mf-list">${vs.map((v) => {
        const d = v.w - v.l;
        return `<a class="mf-r${d > 0 ? " up" : d < 0 ? " dn" : ""}${MG[v.op] && MG[v.op].active ? "" : " old"}" href="#finder" data-pair="${esc(name)}|${esc(v.op)}">
          <span class="op">${esc(v.op)}${MG[v.op] && MG[v.op].active ? "" : " <small>former</small>"}</span>
          <span class="bar"><i class="w" style="width:${(100 * v.w / max).toFixed(1)}%"></i></span>
          <span class="rc">${rec(v.w, v.l, v.t)}</span>
          <span class="bar l"><i class="l" style="width:${(100 * v.l / max).toFixed(1)}%"></i></span>
          <span class="df">${d > 0 ? "+" + d : d < 0 ? "−" + Math.abs(d) : "even"}</span></a>`;
      }).join("")}</div>
    </div>`;
  }

  /* ── method ───────────────────────────────────────────── */
  function method() {
    const m = D.method;
    return `<section class="rv-method" id="method">
      <h2 class="h-sec">How the Index Works</h2><hr class="rule-h">
      <dl><dt>The games</dt><dd>${esc(m.games)}</dd><dt>Managers</dt><dd>${esc(m.manager)}</dd><dt>Heat</dt><dd>${esc(m.heat)}</dd></dl>
    </section>
    <section class="rv-band">
      <h2 class="display">Records reset every September. Grudges don't.</h2>
      <div class="meta"><div>${D.first}–${D.last}</div><div>${D.totals.games.toLocaleString("en-US")} games · ${D.totals.pairs} series</div><div>Through Week ${D.through_week}</div></div>
    </section>`;
  }

  /* ── wiring ───────────────────────────────────────────── */
  let RANK;
  function showPair(a, b, scroll = true) {
    $("#hf-a").value = a; $("#hf-b").value = b;
    finderOut(a, b);
    if (scroll) $("#finder").scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function wire() {
    $("#hf-a").addEventListener("change", () => finderOut($("#hf-a").value, $("#hf-b").value));
    $("#hf-b").addEventListener("change", () => finderOut($("#hf-a").value, $("#hf-b").value));
    $("#hf-swap").addEventListener("click", () => showPair($("#hf-b").value, $("#hf-a").value, false));
    $$(".mf-chip").forEach((c) => c.addEventListener("click", () => {
      $$(".mf-chip").forEach((x) => x.classList.toggle("on", x === c));
      fileOut(c.dataset.m);
    }));
    document.addEventListener("click", (e) => {
      const t = e.target.closest("[data-pair]");
      if (!t || t.closest("summary")) return;
      e.preventDefault();
      const [a, b] = t.dataset.pair.split("|");
      showPair(a, b);
    });
    if (hasNU()) NU.wireStamps(document);
    const h = decodeURIComponent(location.hash.slice(1));
    if (h.startsWith("vs=")) { const [a, b] = h.slice(3).split(","); if (MG[a] && MG[b]) setTimeout(() => showPair(a, b), 60); }
    else if (h) { const el = document.getElementById(h); if (el) setTimeout(() => el.scrollIntoView(), 60); }
  }

  function render(db) {
    D = db;
    PK = Object.fromEntries(db.pairs.map((p) => [[p.a, p.b].sort().join("|"), p]));
    MG = Object.fromEntries(db.managers.map((m) => [m.manager, m]));
    ACTIVE = db.managers.filter((m) => m.active && D.logos[m.manager] !== undefined).sort((a, b) => b.w - a.w || b.pct - a.pct);
    if (!ACTIVE.length) ACTIVE = db.managers.filter((m) => m.active);
    RANK = db.pairs.filter((p) => p.games >= db.min_games);
    $("#app").innerHTML = `<div class="rv">
      ${hero(RANK)}${hot(RANK)}${grudge()}${grid()}${finder()}
      <section class="rv-sec rv-two">${owns()}${records()}</section>
      ${files()}${method()}
    </div>`;
    finderOut(RANK[0].a, RANK[0].b);
    fileOut(ACTIVE[0].manager);
    wire();
  }

  fetch("data/rivalries.json", { cache: "no-store" })
    .then((r) => r.json())
    .then(render)
    .catch((e) => {
      console.error("rivalry index render failed:", e);
      const el = $("#app");
      if (el) el.innerHTML = `<div class="pad" style="padding:30px"><p class="empty">Rivalry data unavailable. Everyone is getting along, for once.</p></div>`;
    });
})();
