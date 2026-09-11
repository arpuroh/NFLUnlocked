/* NFL Unlocked — Trade Court.
   Renders data/trades.json: every trade in league history (2011 to now), re-scored with
   what the players did after the deal. The robberies, the trader rankings, the title
   trades, the veto files, the rental era and a filterable archive of every deal.
   All numbers are built offline (see the method block at the bottom of the page);
   this file only lays them out. Standalone from app.js apart from NU.esc and stamps. */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const r0 = (v) => Math.round(Number(v) || 0);
  const signed = (v) => { const n = r0(v); return n > 0 ? "+" + n : n < 0 ? "−" + Math.abs(n) : "0"; };
  const ord = (i) => { const s = ["th", "st", "nd", "rd"], v = i % 100; return i + (s[(v - 20) % 10] || s[v] || s[0]); };
  const VCLS = { "Grand Larceny": "larceny", "Robbery": "robbery", "Clear Win": "clear", "Slight Edge": "edge", "Wash": "wash" };
  const chip = (label, cls) => `<span class="vchip ${cls || VCLS[label] || "wash"}">${esc(label)}</span>`;
  const pos = (p) => `<span class="pp pos-${esc(String(p || "").toLowerCase())}">${esc(p === "D" ? "IDP" : p)}</span>`;
  const p0 = (v) => (r0(v) > 0 ? "+" + r0(v) : "0");
  const hasNU = () => typeof NU !== "undefined" && NU && NU.stamps;
  const stamps = (id) => (hasNU() ? NU.stamps(id, {}, { min: 3 }) : "");
  // Two 2011 teams have no known manager, and both 2013 Greg teams are unattributed: name the team instead.
  const who = (s) => (s.manager === "Unknown" || s.manager === "Greg (unmatched)" ? s.team : s.manager);
  const span = (m) => { const [a, b] = String(m.span || "").split(/[–-]/); return a && a === b ? a + " only" : m.span; };

  let DB, BY, MG;

  const finish = (s) => !s.rank ? "" : s.place === 1 ? "won the title" : s.place === 2 ? "lost the final"
    : `finished ${ord(s.rank)}`;
  // Winner on the left; a push keeps Yahoo's order.
  const ordered = (t) => (t.win === 1 ? [t.sides[1], t.sides[0]] : [t.sides[0], t.sides[1]]);
  const byVal = (a, b) => b.val - a.val || b.pts - a.pts;
  const names = (s, n = 3) => {
    const g = s.got.slice().sort(byVal);
    const head = g.slice(0, n).map((p) => p.n).join(", ");
    return g.length > n ? `${head} +${g.length - n}` : head;
  };
  const whoLine = (s) => s.manager === "Unknown" ? "manager unknown" : s.manager;

  /* ── the trade card ─────────────────────────────────── */
  function tradeCard(t, o = {}) {
    const [a, b] = ordered(t);
    const decided = t.win !== null && t.win !== undefined;
    const side = (s, won) => `<div class="tc-side ${decided ? (won ? "won" : "lost") : ""}">
        <div class="tc-team"><div><b${s.team.length > 16 ? ' class="long"' : ""}>${esc(s.team)}</b>
          <small>${esc(whoLine(s))}${finish(s) ? " · " + esc(finish(s)) : ""}</small></div>
          ${decided ? `<span class="tc-flag">${won ? "Won" : "Lost"}</span>` : ""}</div>
        <div class="tc-lbl">Received · pts after · value</div>
        <ul class="tc-pl">${s.got.slice().sort(byVal).map((p) => `<li>${pos(p.p)}
          <span class="pn">${esc(p.n)}</span>
          <span class="pv">${r0(p.pts)} pts <b class="${r0(p.val) > 0 ? "" : "z"}">${p0(p.val)}</b></span></li>`).join("")}</ul>
        <div class="tc-sum"><span>Value received</span><b>${p0(s.val)}</b></div>
      </div>`;
    return `<article class="tc${o.feature ? " feature" : ""}${o.more ? " more" : ""}"${o.anchor ? ` id="c-${esc(t.id)}"` : ""}>
      <div class="tc-bar">
        ${o.rank ? `<span class="tc-rank">${o.rank}</span>` : ""}
        ${o.chip || chip(t.verdict)}
        <span class="tc-when">${t.season} · Wk ${esc(t.week ?? "?")} · ${esc(t.when)}</span>
        ${decided ? `<span class="tc-m"><b>+${r0(t.margin)}</b><small>Point gap</small></span>` : ""}
      </div>
      <div class="tc-sides">${side(a, true)}${side(b, false)}</div>
      ${t.note ? `<p class="tc-note">${esc(t.note)}</p>` : ""}
      ${o.stamps ? `<div class="tc-foot">${stamps("trade-" + t.id)}</div>` : ""}
    </article>`;
  }
  /* ── hero + stat bug ────────────────────────────────── */
  function hero() {
    const T = DB.totals, M = DB.managers;
    const top = BY[DB.lists.robberies[0]];
    const tw = top.sides[top.win], tl = top.sides[1 - top.win];
    const king = M[0], donor = M[M.length - 1];
    return `
      <section class="dark roast-hero td-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">Trade Court</span>
              <span class="eyebrow">${DB.first}–${DB.last} · ${T.trades} trades · ${T.players} players moved · ${T.vetoes} vetoed</span>
            </div>
            <h1 class="display">Every trade since ${DB.first}. <span class="kick">Re-scored.</span></h1>
            <p class="lede">${T.trades} deals across fifteen seasons, each one judged by what the players
              actually did after the handshake, under that season's own scoring. ${esc(king.manager)} is up
              ${r0(king.net)} points. ${esc(donor.manager)} has donated ${Math.abs(r0(donor.net))}. The rest of
              you are somewhere in between, and the receipts are below.</p>
            <div class="hero-actions">
              <a class="btn-red" href="#robberies">The robberies →</a>
              <a class="btn-ghost" href="#rankings">Trader rankings →</a>
              <a class="btn-ghost" href="#archive">Find your trades →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">Trade kings · career net</div>
            ${M.slice(0, 5).map((m, i) => `<a class="board-row" href="#m-${esc(m.key)}" data-open="${esc(m.key)}">
              <span class="bn">${i + 1}</span>
              <span class="bt">${esc(m.manager)}<small>${m.trades} trade${m.trades === 1 ? "" : "s"} · ${m.w}-${m.l}-${m.p}</small></span>
              <span class="bm">${signed(m.net)}</span></a>`).join("")}
            <a class="see-all" href="#rankings">All ${M.length} traders →</a>
          </div>
        </div>
      </section>
      <section class="statbug">
        <div class="cell"><div class="eyebrow">Trades on file</div><div class="v">${T.trades}</div>
          <div class="s">plus ${T.vetoes} the league vetoed</div></div>
        <div class="cell"><div class="eyebrow">Biggest robbery</div><div class="v red">+${r0(top.margin)}</div>
          <div class="s">${esc(tw.team)} over ${esc(who(tl))} · ${top.season}</div></div>
        <div class="cell"><div class="eyebrow">Trade king</div><div class="v">${signed(king.net)}</div>
          <div class="s">${esc(king.manager)} · ${king.trades} trades, ${king.w}-${king.l}-${king.p}</div></div>
        <div class="cell"><div class="eyebrow">Most generous</div><div class="v red">${signed(donor.net)}</div>
          <div class="s">${esc(donor.manager)} · ${donor.trades} trades, ${donor.w}-${donor.l}-${donor.p}</div></div>
      </section>
      <div class="td-scale">
        <span class="k">How a trade is judged</span>
        <span>Value = rest-of-season points over a waiver-wire starter. The gap between the two sides is the verdict:</span>
        ${DB.method.verdicts.map((v) => `<span class="sc">${chip(v.label)}<i>${v.min ? v.min + "+" : "under 12"}</i></span>`).join("")}
        <a href="#method" class="sc" style="font-weight:800;color:var(--red)">Full method ↓</a>
      </div>`;
  }

  /* ── the robberies ──────────────────────────────────── */
  function robberies() {
    const ids = DB.lists.robberies;
    return `<section class="td-sec" id="robberies">
      <div class="sec-top"><h2 class="h-sec">The Robberies</h2><span class="note">The ${ids.length} most lopsided trades ever made</span></div>
      <hr class="rule-h">
      <p class="td-lede">Ranked by the point gap between what each side received, counted from the day the deal
        went through to the fantasy championship. A player counts for whoever got him, whatever that manager did with him next.</p>
      <div class="tc-grid collapsed" id="rob-grid">${ids.map((id, i) => tradeCard(BY[id], { rank: i + 1, feature: i === 0, stamps: true, anchor: true, more: i >= 5 })).join("")}</div>
      <button type="button" class="td-more" id="rob-more">Show all ${ids.length} robberies</button>
    </section>`;
  }

  /* ── trader rankings ────────────────────────────────── */
  function rankings() {
    const rows = DB.managers.map((m, i) => {
      const best = m.best && BY[m.best.id];
      const bestVs = best ? best.sides.find((s) => s.mkey !== m.key) : null;
      return `<details class="rk-row" id="m-${esc(m.key)}" data-key="${esc(m.key)}">
        <summary>
          <span class="rk-n">${i + 1}</span>
          <span class="rk-m"><b>${esc(m.manager)}</b><span class="t">${esc(m.team)}${m.active ? "" : ` · ${esc(span(m))}`}</span></span>
          <span class="rk-c">${m.trades}</span>
          <span class="rk-c">${m.w}-${m.l}-${m.p}</span>
          <span class="rk-c big ${m.net > 0 ? "pos" : m.net < 0 ? "neg" : ""}">${signed(m.net)}</span>
          <span class="rk-c dim">${signed(m.per)}</span>
          <span class="rk-best">${best && m.best.d > 0 ? `<b>${signed(m.best.d)}</b> vs ${esc(who(bestVs))} '${String(best.season).slice(2)}` : "no wins yet"}</span>
          <span class="rk-caret">▶</span>
          <span class="rk-sub">${m.trades} trade${m.trades === 1 ? "" : "s"} · ${m.w}-${m.l}-${m.p} · ${signed(m.per)} a trade</span>
        </summary>
        <div class="rk-body" data-lazy="1"></div>
      </details>`;
    }).join("");
    return `<div class="body-grid" id="rankings">
      <div class="col-main">
        <div class="sec-top"><h2 class="h-sec">The Trader Rankings</h2><span class="note">Career net, every trade</span></div>
        <p class="td-lede" style="margin-top:4px">Net is everything a manager received minus everything he gave away, in
          points over the waiver wire. A trade is a win only by 5 or more. Rentals count at what they were worth while
          they lasted; vetoed deals do not count. Tap anyone for the full ledger.</p>
        <div class="rk-table">
          <div class="rk-hd"><span>#</span><span>Manager</span><span class="rk-c">Trades</span><span class="rk-c">W-L-P</span>
            <span class="rk-c">Net</span><span class="rk-c">Per</span><span class="rk-best">Best deal</span><span></span></div>
          ${rows}
        </div>
      </div>
      <div class="col-side">${partners()}${flyers()}${never()}</div>
    </div>`;
  }

  function managerBody(m) {
    const mine = DB.trades.filter((t) => t.kind !== "return" && t.sides.some((s) => s.mkey === m.key))
      .sort((a, b) => a.date.localeCompare(b.date));
    const facts = [
      m.fav ? `Favorite partner <b>${esc(m.fav.name)}</b> (${m.fav.n})` : "",
      m.victim ? `Biggest mark <b>${esc(m.victim.name)}</b> (${signed(m.victim.d)})` : "",
      m.nemesis ? `Nemesis <b>${esc(m.nemesis.name)}</b> (${signed(m.nemesis.d)})` : "",
      `Received <b>${r0(m.got)}</b> · gave <b>${r0(m.gave)}</b>`,
      m.loans ? `Rentals <b>${m.loans}</b>` : "",
      m.vetoed ? `Vetoed <b>${m.vetoed}</b>` : "",
    ].filter(Boolean).map((f) => `<span>${f}</span>`).join("");
    return `${m.note ? `<p class="rk-note">${esc(m.note)}</p>` : ""}
      <div class="rk-facts">${facts}</div>
      <div class="rk-list">${mine.map((t) => {
        const me = t.sides.find((s) => s.mkey === m.key), them = t.sides.find((s) => s !== me);
        const d = me.val - them.val;
        const veto = t.kind === "veto";
        return `<div class="rk-tr ${t.kind === "loan" ? "tag-loan" : ""}">
          <span class="y">${t.season}</span>
          <span class="g"><i>${veto ? "Vetoed · would have got" : "Got"}</i>${esc(names(me, 4))}</span>
          <span class="o"><i>${veto ? "would have sent" : "Sent"} to ${esc(who(them))}</i>${esc(names(them, 4))}</span>
          <span class="d ${veto ? "dim" : d >= 5 ? "pos" : d <= -5 ? "neg" : ""}">${veto ? "veto" : signed(d)}</span>
        </div>`;
      }).join("")}</div>
      <p style="margin:12px 0 0"><a href="#archive" class="see-all" style="color:var(--red)" data-filter="${esc(m.key)}">Show ${esc(m.manager)}'s trades in the archive →</a></p>`;
  }

  function partners() {
    const P = DB.pairs.slice(0, 6);
    return `<div class="mod">
      <h2 class="h-sec">Favorite Partners</h2><hr class="rule-h">
      ${P.map((p) => {
        const up = p.d >= 0 ? p.an : p.bn;
        return `<div class="pair-row"><span class="who">${esc(p.an)} &amp; ${esc(p.bn)}</span>
          <span class="n">${p.n}</span>
          <span class="s">${Math.abs(p.d) < 5 ? "Dead even across the lot." : `${esc(up)} is up ${Math.abs(r0(p.d))} across the ${p.n} deals.`}</span></div>`;
      }).join("")}
    </div>`;
  }

  function flyers() {
    const F = DB.flyers.slice(0, 8);
    return `<div class="mod">
      <h2 class="h-sec">Frequent Flyers</h2><hr class="rule-h">
      ${F.map((f) => `<div class="fly-row"><span class="who">${pos(f.pos)}<span>${esc(f.n)}</span></span>
        <span class="n">${f.times}×</span>
        <span class="s">${f.seasons.join(", ")} · ${f.owners} different buyers</span></div>`).join("")}
    </div>`;
  }

  function never() {
    const N = DB.never;
    const nishil = DB.managers.find((m) => m.key === "nishil");
    return `<div class="mod">
      <h2 class="h-sec">Never Traded</h2><hr class="rule-h">
      <p class="never">${N.length ? `${N.map((n) => `<b>${esc(n.manager)}</b>`).join(" and ")} (${esc(span(N[0]))}) never made a trade.
        Everybody else has.` : "Everybody has made at least one trade."}
        ${nishil ? `<b>Nishil</b> has made ${nishil.trades} in fifteen seasons, lost none of them, and owns three titles. Draw your own conclusions.` : ""}</p>
    </div>`;
  }

  /* ── traded for a ring ──────────────────────────────── */
  function rings() {
    const L = DB.lists.title;
    const nt = DB.lists.no_trade_champs.filter((c) => c.year >= 2017);
    const recent = DB.seasons.filter((s) => s.year >= 2017 && s.champ).length;
    const tally = {};
    nt.forEach((c) => { tally[c.champ] = (tally[c.champ] || 0) + 1; });
    const times = (n) => (n === 1 ? "once" : n === 2 ? "twice" : n === 3 ? "three times" : n + " times");
    return `<section class="td-sec" id="titles">
      <div class="sec-top"><h2 class="h-sec">Traded for a Ring</h2><span class="note">What the champions bought</span></div>
      <hr class="rule-h">
      <p class="td-lede">The deal each champion made that paid off most in the fantasy playoffs. Winning the trade and
        winning the league are different skills. Jordan proved it twice.</p>
      <div class="ring-grid">${L.map((r) => {
        const t = BY[r.id], me = t.sides[r.side];
        return `<div class="ring">
          <div class="yr"><b>${t.season}</b><span>${esc(t.when)} · Wk ${esc(t.week)}${t.deadline ? " · deadline" : ""}</span></div>
          <div class="who"><b>${esc(me.manager)}</b> · ${esc(me.team)}</div>
          <div class="got">${esc(me.got.slice().sort((a, b) => b.po - a.po).map((p) => p.n).join(", "))}</div>
          <div class="po"><b>${r0(r.po)}</b><span>pts in the fantasy playoffs<br>${r.d >= 5 ? `won the trade by ${r0(r.d)}` : r.d <= -5 ? `lost the trade by ${Math.abs(r0(r.d))}` : "trade was a wash"}</span></div>
          ${t.note ? `<p>${esc(t.note)}</p>` : ""}
        </div>`;
      }).join("")}</div>
      <p class="ring-foot">And the other way to win: <b>${nt.length} of the last ${recent} champions made zero trades</b> that season
        (${Object.entries(tally).map(([k, v]) => `${esc(k)} ${times(v)}`).join(", ")}).</p>
    </section>`;
  }

  /* ── veto files + rental era ────────────────────────── */
  function vetoes() {
    const V = DB.lists.vetoes.map((id) => BY[id]);
    const approved = (v) => DB.trades.find((t) => t.kind === "trade" && t.season === v.season && t.date >= v.date &&
      (new Date(t.date) - new Date(v.date)) / 864e5 <= 4 &&
      t.sides.map((s) => s.mkey + s.team).sort().join() === v.sides.map((s) => s.mkey + s.team).sort().join());
    return `<div class="body-grid" id="vetoes">
      <div class="col-main">
        <div class="sec-top"><h2 class="h-sec">The Veto Files</h2><span class="note">${V.length} deals the league blocked</span></div>
        <hr class="rule-h">
        <p class="td-lede">Scored as if they had gone through. Sometimes the league saved a man from himself. Sometimes it
          just made him try again.</p>
        ${V.map((v) => {
          const [a, b] = ordered(v);
          const ok = approved(v);
          return `<div class="veto">
            <div class="veto-top">${chip("Vetoed", "vetoed")}<span class="tc-when">${v.season} · Wk ${esc(v.week)} · ${esc(v.when)}</span>
              ${v.win !== null && v.win !== undefined ? `<span class="would">Would have been ${chip(v.verdict)} <b>+${r0(v.margin)}</b> ${esc(who(a))}</span>` : `<span class="would">Would have been a wash</span>`}</div>
            <div class="veto-sides">${[a, b].map((s) => `<div class="vs">
              <div class="hd"><b>${esc(s.team)}</b>${s.manager !== "Unknown" ? " · " + esc(s.manager) : ""} would have got</div>
              <div class="pl">${s.got.slice().sort(byVal).map((p) => `${esc(p.n)} <span>${r0(p.pts)}</span>`).join(", ")}</div></div>`).join("")}</div>
            ${v.note ? `<p>${esc(v.note)}</p>` : ""}
            ${ok ? `<p style="font-weight:700;color:var(--ink)">Approved ${ok.date === v.date ? "the same day" : "later"} in a new version: <a href="#a-${esc(ok.id)}" class="red" data-jump="${esc(ok.id)}">see ${esc(ok.when)}, ${ok.season} →</a></p>` : ""}
          </div>`;
        }).join("")}
      </div>
      <div class="col-side">${rentals()}</div>
    </div>`;
  }

  function rentals() {
    const R = DB.lists.rentals.map(([a, b]) => [BY[a], BY[b]]);
    const days = (x, y) => Math.max(0, Math.round((new Date(y.date) - new Date(x.date)) / 864e5));
    return `<div class="mod" id="rentals">
      <h2 class="h-sec">The Rental Era</h2><hr class="rule-h">
      <p class="never" style="margin:10px 0 6px">In 2015 and 2016 the league discovered that a trade can be undone.
        ${R.length} deals were reversed player-for-player within days. They count here only for the games played on loan.</p>
      ${R.map(([l, r]) => `<div class="rent-row">
        <span class="d">${esc(l.when)} '${String(l.season).slice(2)}<small>${days(l, r) ? days(l, r) + (days(l, r) === 1 ? " day" : " days") : "same day"}</small></span>
        <span class="x"><b>${esc(l.sides[0].manager)} ⇄ ${esc(l.sides[1].manager)}</b>
          <span>${l.sides.map((s) => `${esc(s.manager)} got ${esc(names(s, 3))}`).join(" · ")}</span></span>
      </div>`).join("")}
    </div>`;
  }

  /* ── fair fights ────────────────────────────────────── */
  function fair() {
    const ids = DB.lists.winwin.slice(0, 4);
    if (!ids.length) return "";
    return `<section class="td-sec" id="fair">
      <div class="sec-top"><h2 class="h-sec">Fair Fights</h2><span class="note">Both sides got real players</span></div>
      <hr class="rule-h">
      <p class="td-lede">Trades where both teams walked away with at least 35 points of value and the gap stayed under 30.
        Rare. Worth studying.</p>
      <div class="tc-grid">${ids.map((id) => tradeCard(BY[id])).join("")}</div>
    </section>`;
  }

  /* ── archive ────────────────────────────────────────── */
  function archiveRow(t) {
    const [a, b] = ordered(t);
    const decided = t.win !== null && t.win !== undefined;
    const side = (s, won) => `<div class="ar-s ${decided && won && t.kind !== "return" ? "won" : ""}">
      <div class="t">${esc(s.team)} <i>${esc(s.manager)}</i></div>
      <div class="p">${s.got.slice().sort(byVal).map((p) => `${esc(p.n)} ${r0(p.val) > 0 ? `<em>+${r0(p.val)}</em>` : `<em class="z">${r0(p.pts)} pts</em>`}`).join(", ")}</div></div>`;
    let v;
    if (t.kind === "veto") v = `${chip("Vetoed", "vetoed")}<small>${decided ? `would have been +${r0(t.margin)}` : "would have been even"}</small>`;
    else if (t.kind === "return") v = `${chip("Sent back", "back")}<small>undoes ${esc(BY[t.pair] ? BY[t.pair].when : "")}</small>`;
    else if (t.kind === "loan") {
      const back = BY[t.pair];
      const d = back ? Math.round((new Date(back.date) - new Date(t.date)) / 864e5) : 0;
      v = `${chip("Rental", "rental")}<small>sent back ${d ? `in ${d} day${d === 1 ? "" : "s"}` : "the same day"}</small>${decided ? `<b>+${r0(t.margin)}</b>` : ""}`;
    } else v = `${chip(t.verdict)}${decided ? `<b>+${r0(t.margin)}</b>` : `<small>even</small>`}${t.deadline ? "<small>deadline deal</small>" : ""}`;
    const keys = t.sides.map((s) => s.mkey).join(" ");
    return `<div class="ar-row k-${t.kind}" id="a-${esc(t.id)}" data-m="${esc(keys)}">
      <div class="w">${esc(t.when)}<span>Wk ${esc(t.week ?? "?")}</span></div>
      ${side(a, true)}${side(b, false)}
      <div class="ar-v">${v}</div>
      ${t.note && t.kind !== "veto" ? `<p class="ar-note">${esc(t.note)}</p>` : ""}
    </div>`;
  }

  function archive() {
    const S = DB.seasons.slice().reverse();
    const maxN = Math.max(...DB.seasons.map((s) => s.trades));
    const opts = DB.managers.slice().sort((a, b) => a.manager.localeCompare(b.manager));
    return `<section class="td-sec" id="archive">
      <div class="sec-top"><h2 class="h-sec">Every Trade</h2><span class="note">${DB.totals.trades} deals · ${DB.first} to ${DB.last}</span></div>
      <hr class="rule-h">
      <div class="ar-chart" role="img" aria-label="Trades per season, ${DB.first} to ${DB.last}">
        ${DB.seasons.map((s) => {
          const rent = s.loans * 2;
          const h = (s.trades / maxN) * 100;
          return `<button type="button" data-year="${s.year}" title="${s.year}: ${s.trades} trades${rent ? `, ${rent} of them rental round-trips` : ""}${s.vetoes ? `, ${s.vetoes} vetoed` : ""}">
            <span class="v">${s.trades}</span>
            <span class="bar" style="height:${h}%">${rent ? `<i style="height:${(rent / s.trades) * 100}%"></i>` : ""}</span>
          </button>`;
        }).join("")}
      </div>
      <div class="ar-yrs">${DB.seasons.map((s) => `<span>'${String(s.year).slice(2)}</span>`).join("")}</div>
      <div class="ar-key"><span><i></i>Trades</span><span><i class="l"></i>Rentals and their returns</span><span>Tap a year to open it</span></div>

      <div class="ar-tools">
        <label for="ar-m">Manager</label>
        <select id="ar-m"><option value="">All ${DB.managers.length} managers</option>
          ${opts.map((m) => `<option value="${esc(m.key)}">${esc(m.manager)} (${m.trades})</option>`).join("")}</select>
        <span class="cnt" id="ar-cnt"></span>
        <button type="button" class="clear" id="ar-clear" hidden>Clear</button>
      </div>

      <div class="ar" id="ar">
        ${S.map((s, i) => {
          const rows = DB.trades.filter((t) => t.season === s.year).sort((a, b) => b.date.localeCompare(a.date) || b.id.localeCompare(a.id));
          const top = s.top ? BY[s.top] : null;
          const tw = top ? top.sides[top.win] : null, tl = top ? top.sides[1 - top.win] : null;
          return `<details class="ar-yr" id="y-${s.year}" data-year="${s.year}" ${i === 0 ? "open" : ""}>
            <summary><span class="y">${s.year}</span>
              <span class="n">${s.trades} trade${s.trades === 1 ? "" : "s"}${s.vetoes ? ` · ${s.vetoes} vetoed` : ""}</span>
              <span class="dim">🏆 ${esc(s.champ || "")}${s.busy ? ` · busiest: ${esc(s.busy.manager)} (${s.busy.n})` : ""}</span>
              <span class="dim">${top ? `Top deal: <b>${esc(who(tw))} +${r0(top.margin)}</b> over ${esc(who(tl))}` : ""}</span>
            </summary>
            <div class="ar-body">
              ${s.note ? `<p class="ar-dek">${esc(s.note)}</p>` : ""}
              ${rows.map(archiveRow).join("")}
              <p class="ar-empty" hidden>No trades for this manager in ${s.year}.</p>
            </div>
          </details>`;
        }).join("")}
      </div>
    </section>`;
  }

  /* ── method + band ──────────────────────────────────── */
  function method() {
    const m = DB.method;
    const last = DB.replacement[String(DB.last)] || {};
    const lab = { QB: "QB", RB: "RB", WR: "WR", TE: "TE", K: "K", DEF: "DEF", D: "IDP" };
    return `<section class="td-method" id="method">
      <h2 class="h-sec">How the Court Works</h2><hr class="rule-h">
      <dl>
        <dt>Value</dt><dd>${esc(m.value)}</dd>
        <dt>Window</dt><dd>${esc(m.window)}</dd>
        <dt>Scoring</dt><dd>${esc(m.scoring)} 2011 paid receivers bonuses from 50 yards. Kickers were paid by distance
          until 2021. Team defenses got 15 points for a shutout through 2013.</dd>
        <dt>Waiver line, ${DB.last}</dt><dd><span class="rep">${Object.entries(last).map(([k, v]) => `<span>${lab[k] || k} ${v}</span>`).join("")}</span>
          Points per game from the first players past the last starter at each position, given ${DB.last}'s lineup of 14 teams.
          Every season has its own line.</dd>
        <dt>Verdicts</dt><dd>A side wins by ${m.push} or more. ${m.verdicts.map((v) => `${v.label} ${v.min ? v.min + "+" : "under 12"}`).join(" · ")}.</dd>
        <dt>Source</dt><dd>${esc(m.source)}</dd>
      </dl>
    </section>
    <section class="td-band">
      <h2 class="display">Every trade is final. The receipts are forever.</h2>
      <div class="meta"><div>${DB.totals.trades} trades · ${DB.first}–${DB.last}</div><div>Re-scored under each season's rules</div><div>Updated ${esc(DB.generated)}</div></div>
    </section>`;
  }

  /* ── wiring ─────────────────────────────────────────── */
  function applyFilter(key) {
    const sel = $("#ar-m");
    if (sel.value !== key) sel.value = key;
    let n = 0;
    $$(".ar-yr").forEach((yr) => {
      let k = 0;
      $$(".ar-row", yr).forEach((row) => {
        const show = !key || row.dataset.m.split(" ").includes(key);
        row.hidden = !show;
        if (show && !row.classList.contains("k-veto") && !row.classList.contains("k-return")) k++;
      });
      n += k;
      const any = $$(".ar-row", yr).some((r) => !r.hidden);
      yr.hidden = key ? !any : false;
      if (key && any) yr.open = true;
    });
    const m = MG[key];
    $("#ar-cnt").textContent = key && m ? `${n} trade${n === 1 ? "" : "s"} involving ${m.manager}` : "";
    $("#ar-clear").hidden = !key;
    try { history.replaceState(null, "", key ? `#m=${key}` : location.pathname); } catch {}
  }

  function jumpTo(id) {
    const row = document.getElementById("a-" + id);
    if (!row) return;
    const yr = row.closest(".ar-yr");
    if ($("#ar-m").value && row.hidden) applyFilter("");
    if (yr) yr.open = true;
    $$(".ar-row.hl").forEach((r) => r.classList.remove("hl"));
    row.classList.add("hl");
    row.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  function wire() {
    $("#ar-m").addEventListener("change", (e) => applyFilter(e.target.value));
    $("#rob-more").addEventListener("click", (e) => { $("#rob-grid").classList.remove("collapsed"); e.currentTarget.hidden = true; });
    $("#ar-clear").addEventListener("click", () => applyFilter(""));
    $$(".ar-chart button").forEach((b) => b.addEventListener("click", () => {
      const yr = $("#y-" + b.dataset.year);
      if (!yr) return;
      if (yr.hidden) applyFilter("");
      yr.open = true;
      yr.scrollIntoView({ behavior: "smooth", block: "start" });
    }));
    // lazy ledger per manager
    $$(".rk-row").forEach((d) => d.addEventListener("toggle", () => {
      const body = $(".rk-body", d);
      if (d.open && body.dataset.lazy) { body.innerHTML = managerBody(MG[d.dataset.key]); delete body.dataset.lazy; }
    }));
    document.addEventListener("click", (e) => {
      const f = e.target.closest("[data-filter]");
      if (f) { e.preventDefault(); applyFilter(f.dataset.filter); $("#archive").scrollIntoView({ behavior: "smooth" }); return; }
      const j = e.target.closest("[data-jump]");
      if (j) { e.preventDefault(); jumpTo(j.dataset.jump); return; }
      const o = e.target.closest("[data-open]");
      if (o) {
        const d = document.getElementById("m-" + o.dataset.open);
        if (d) { e.preventDefault(); d.open = true; d.scrollIntoView({ behavior: "smooth", block: "start" }); }
      }
    });
    if (hasNU()) NU.wireStamps(document);
    // deep links: #m=varun filters the archive, #a-<id> opens a trade
    const h = decodeURIComponent(location.hash.slice(1));
    if (h.startsWith("m=") && MG[h.slice(2)]) {
      applyFilter(h.slice(2));
      setTimeout(() => $("#archive").scrollIntoView(), 60);
    } else if (h.startsWith("a-")) setTimeout(() => jumpTo(h.slice(2)), 60);
    else if (h.startsWith("m-") && MG[h.slice(2)]) {
      const d = document.getElementById(h);
      if (d) { d.open = true; setTimeout(() => d.scrollIntoView(), 60); }
    } else if (h) {
      const el = document.getElementById(h);
      if (el) setTimeout(() => el.scrollIntoView(), 60);
    }
  }

  function render(db) {
    DB = db;
    BY = Object.fromEntries(db.trades.map((t) => [t.id, t]));
    MG = Object.fromEntries(db.managers.map((m) => [m.key, m]));
    $("#app").innerHTML = `<div class="td">
      ${hero()}${robberies()}${rankings()}${rings()}${vetoes()}${fair()}${archive()}${method()}
    </div>`;
    wire();
  }

  fetch("data/trades.json", { cache: "no-store" })
    .then((r) => r.json())
    .then(render)
    .catch((e) => {
      console.error("trade court render failed:", e);
      const el = $("#app");
      if (el) el.innerHTML = `<div class="pad" style="padding:30px"><p class="empty">Trade data unavailable. The court is in recess.</p></div>`;
    });
})();
