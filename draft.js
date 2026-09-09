/* NFL Unlocked — Draft Central.

   Reads data/draft.json (written by scripts/fetch_draft.py off the public Yahoo
   draft-results page) and data/draft_grades.json (the writing: grades, awards,
   preseason power rankings). Three states, decided by the data alone:

     pending   — no picks yet: countdown, the field, last year's biggest buys
     complete  — picks in, no grades yet: full auction ledger, grades "in the oven"
     graded    — picks + grades: the real page

   No build step, no state. Reloading is the refresh. */
(() => {
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const $ = (s, r = document) => r.querySelector(s);
  const money = (n) => "$" + (n ?? 0);
  const ord = (i) => {
    const s = ["th", "st", "nd", "rd"], v = i % 100;
    return i + (s[(v - 20) % 10] || s[v] || s[0]);
  };

  // Draft night, per the league's Yahoo settings page. 7:00pm ET.
  const DRAFT_AT = new Date("2026-09-08T23:00:00Z");
  const YAHOO = "https://football.fantasysports.yahoo.com/f1/675504";

  // Team name → manager. Yahoo's public page carries team names only.
  const MANAGERS = {
    "Hail Mary": "Andrew", "Hail Purdy": "Andrew",
    "ShakeNBake": "Abhishek",
    "A dad": "Barrett",
    "FreeGucci": "Nishil",
    "Kim Jong Nate": "Nathan",
    "Mac Daddy": "Maclane",
    "The Injured Reserved": "Greg (IR)",
    "Miley 💨LEO 5K Speedo Fan Club": "Greg (Miley)",
    "Bend The Knee 🐲🔥": "Darrius",
    "Poop Squad 💩": "Anuj",
    "Good Will Hunting": "Will",
    "Leo the Cleo": "Chris",
    "The Asshouse Always Wins": "Tom",
    "Fwamming Gwaggon": "Jon",
    "Shut Up": "Neil", "Bullish": "Mohsin",
  };
  const mgr = (team, grades) =>
    (grades && grades.grades && grades.grades[team] && grades.grades[team].manager) ||
    MANAGERS[team] || "";

  const POS_ORDER = ["QB", "RB", "WR", "TE", "K", "DEF", "IDP"];
  // each manager's own Yahoo avatar, scraped with the draft results
  const tlogo = (t, cls) => t && t.logo
    ? `<img class="tlogo${cls ? " " + cls : ""}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  const posClass = (slot) => "pos-" + String(slot || "").toLowerCase();
  // Stable anchor per team so the index at the top can jump straight to a card.
  const slug = (t) => "t-" + String(t).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

  /* ── data ────────────────────────────────────────────── */
  const getJSON = (p) => fetch(p, { cache: "no-store" }).then((r) => (r.ok ? r.json() : null)).catch(() => null);

  async function run() {
    if (document.body.dataset.page !== "draft") return;
    const [draft, grades, prev, ledger, proj] = await Promise.all([
      getJSON("data/draft.json"), getJSON("data/draft_grades.json"),
      getJSON("data/draft_2025.json"), getJSON("data/ledger.json"),
      getJSON("data/projections.json"),
    ]);
    if (proj && draft) {
      const byTeam = Object.fromEntries((proj.teams || []).map((t) => [t.team, t]));
      (draft.teams || []).forEach((t) => { t.proj = byTeam[t.team] || null; });
      draft.projections = proj;
    }
    const paint = () => {
      const app = $("#app");
      if (!app) return false;
      if (!draft) {
        app.innerHTML = `<p class="empty pad">Draft data has not been published yet. Poke the commissioner.</p>`;
        return true;
      }
      const graded = draft.status === "complete" && grades && grades.grades && Object.keys(grades.grades).length;
      app.innerHTML = draft.status === "pending"
        ? pendingView(draft, prev, ledger)
        : draftView(draft, graded ? grades : null, prev);
      wire();
      const chip = document.querySelector(".masthead .badge-live");
      if (chip) {
        chip.textContent = draft.status === "pending" ? "Draft Night" : "Preseason";
        chip.style.background = draft.status === "pending" ? "var(--red)" : "";
      }
      return true;
    };
    // app.js paints the shell asynchronously; take over once it has.
    setTimeout(paint, 60); setTimeout(paint, 400); setTimeout(paint, 1200);
  }

  /* ── shared bits ─────────────────────────────────────── */
  const stat = (label, v, s, red) => `<div class="cell">
    <div class="eyebrow">${esc(label)}</div>
    <div class="v${red ? " red" : ""}">${esc(v)}</div>
    <div class="s">${esc(s)}</div></div>`;

  const pickLine = (p, opts = {}) => `<div class="dr-pick${opts.cls || ""}">
      <span class="pp ${posClass(p.slot)}">${esc(p.slot === "IDP" ? p.pos.split(",")[0] : p.slot)}</span>
      <span class="pn">${esc(p.player)} <em>${esc(p.nfl)}</em></span>
      ${opts.team ? `<span class="pt">${esc(p.team)}</span>` : ""}
      <span class="pc num">${money(p.cost)}${p.last_year != null && opts.delta
        ? `<i class="${p.cost > p.last_year ? "up" : p.cost < p.last_year ? "dn" : ""}">${
            p.cost === p.last_year ? "=" : (p.cost > p.last_year ? "+" : "−") + Math.abs(p.cost - p.last_year)}</i>` : ""}</span>
    </div>`;

  function countdown() {
    const ms = DRAFT_AT - new Date();
    if (ms <= 0) return { v: "Live", s: "The auction is underway" };
    const h = Math.floor(ms / 3600000), m = Math.floor((ms % 3600000) / 60000);
    return { v: h > 0 ? `${h}h ${m}m` : `${m}m`, s: "Tue Sep 8 · 7:00pm ET" };
  }

  const finishOf = (ledger, year, team) => {
    const rows = (ledger && ledger[String(year)]) || [];
    const r = rows.find((a) => a[0] === team);
    return r ? { rank: r[2], place: r[3], rec: `${r[4]}-${r[5]}` } : null;
  };

  /* ── PENDING: before the first nomination ─────────────── */
  function pendingView(draft, prev, ledger) {
    const cd = countdown();
    const order = (draft.teams || []).map((t) => t.team);
    const pTop = prev ? prev.ledger.top_buys.slice(0, 12) : [];
    const pDollar = prev ? prev.ledger.dollar_count : null;

    return `
      <section class="dark roast-hero dr-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">Draft Night</span>
              <span class="eyebrow">${draft.season} auction · ${order.length || 14} teams · $${draft.budget} each · 16 roster spots</span>
            </div>
            <h1 class="display">Every Dollar Gets Audited
              <span class="kick">(grades drop tonight)</span></h1>
            <p class="lede">Fourteen managers, $${(draft.budget || 200) * (order.length || 14)} in play, one room. The moment the
              last $1 kicker goes off the board this page turns into the receipts: every pick with its price,
              a letter grade for every roster, and the preseason power rankings nobody agrees with.
              Refresh after the draft.</p>
            <div class="hero-actions">
              <a class="btn-red" href="${YAHOO}" target="_blank" rel="noopener">Yahoo draft room →</a>
              <a class="btn-ghost" href="#last-year">Last year's receipts ↓</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">${order.length ? "The field" : "Nomination order"}</div>
            ${order.length ? order.map((t, i) => `<div class="board-row">
                <span class="bn">${i + 1}</span>
                <span class="bt">${esc(t)}</span>
                <span class="bm">${esc(MANAGERS[t] || "")}</span></div>`).join("")
              : `<p class="lede" style="margin-top:8px">Yahoo randomizes it 30 minutes before the draft.</p>`}
            <span class="see-all">Order is randomized 30 min before kickoff</span>
          </div>
        </div>
      </section>

      <section class="statbug">
        ${stat("First nomination in", cd.v, cd.s, true)}
        ${stat("Money on the table", money((draft.budget || 200) * (order.length || 14)), "$1 is reserved for every empty slot")}
        ${prev && pTop[0] ? stat("Last year's top buy", money(pTop[0].cost), `${pTop[0].player} · ${pTop[0].team}`) : stat("Last year's top buy", "—", "")}
        ${pDollar != null ? stat("$1 players last year", pDollar, `of ${prev.picks.length} picks. A third of the league costs a dollar.`) : stat("$1 players", "—", "")}
      </section>

      <div class="dr-solo" id="last-year">
        ${prev ? `
        <div class="sec-top"><h2 class="h-sec">The ${prev.season} Auction, Audited</h2>
          <span class="note">Biggest buys and where they finished</span></div>
        <hr class="rule-h">
        <div class="dr-table">
          <div class="row hd"><span>Pick</span><span>Player</span><span>Bought by</span><span class="c">Price</span><span class="c">Finish</span></div>
          ${pTop.map((p) => {
            const f = finishOf(ledger, prev.season, p.team);
            const fin = f ? (f.place === 1 ? "\u{1F3C6} Champion" : ord(f.rank) + " · " + f.rec) : "—";
            return `<div class="row${f && f.rank >= 12 ? " bad" : ""}${f && f.place === 1 ? " champ" : ""}">
              <span class="rk">${p.pick}</span>
              <span class="tm"><span class="pp ${posClass(p.slot)}">${esc(p.slot)}</span> ${esc(p.player)}</span>
              <span class="mg">${esc(p.team)}</span>
              <span class="c b num">${money(p.cost)}</span>
              <span class="c dim">${esc(fin)}</span></div>`;
          }).join("")}
        </div>
        <p class="os-note">The five biggest buys of ${prev.season} finished 6th, 14th, 8-20, 4th and the Sacco. Not one made
          the final. The champion's most expensive player cost $36. Tonight the same fourteen people
          walk back into the same room with the same $200 and swear it will be different.</p>` : `<p class="empty">No prior draft on file.</p>`}
      </div>`;
  }

  /* ── COMPLETE / GRADED ────────────────────────────────── */
  function draftView(draft, grades, prev) {
    const L = draft.ledger || {};
    const teams = draft.teams || [];
    const G = grades ? grades.grades : null;
    const rankOf = {};
    (grades && grades.rankings || []).forEach((r) => { rankOf[r.team] = r; });
    const BUDGET = draft.budget || 200;

    // Order: by preseason rank when graded, else by starter capital.
    const ordered = teams.slice().sort((a, b) =>
      G ? ((rankOf[a.team] || {}).rank || 99) - ((rankOf[b.team] || {}).rank || 99)
        : b.starter_capital - a.starter_capital);

    const top = L.top_buys ? L.top_buys[0] : null;
    const dollarKing = teams.slice().sort((a, b) => b.dollar_players - a.dollar_players)[0];
    const benchKing = teams.slice().sort((a, b) => b.bench_spend - a.bench_spend)[0];
    const qb = L.pos_market && L.pos_market.QB;
    const totalSpent = L.total_spent || 0;
    const top5 = (grades && grades.rankings || []).slice(0, 5);
    const headline = (grades && grades.headline) || "The Receipts Are In";
    const kicker = (grades && grades.kicker) || "(grades are being written)";
    const lede = (grades && grades.lede) ||
      `${draft.picks.length} picks, ${money(totalSpent)} spent, ${L.dollar_count} of them for a dollar. The full auction
       ledger is below. The letter grades and the preseason power rankings are being written right now;
       refresh in a bit.`;

    /* capital bar: what actually starts vs what sits on the bench */
    const P = draft.projections || {};
    const avgWeek = P.avg_weekly || 0;
    const capitalBar = (t) => `<div class="cap">
      ${t.proj ? `<div class="cap-score">
        <span class="cs-n${t.proj.weekly >= avgWeek ? " up" : " dn"}">${(Math.round(t.proj.weekly * 10) / 10).toFixed(1)}</span>
        <span class="cs-l">Projected points per week<em>${ord(t.proj.rank)} of ${(P.teams || []).length} &middot; league average ${avgWeek}
          &middot; ${(Math.round(t.proj.lineup_ppg * 10) / 10).toFixed(1)} when everybody plays, less ${(Math.round(t.proj.depth_cost * 10) / 10).toFixed(1)} for byes and injuries</em></span>
      </div>` : ""}
      <div class="cap-bar">
        <i class="st" style="width:${Math.round(t.starter_capital / BUDGET * 100)}%"></i>
        <i class="bn" style="width:${Math.round(t.bench_spend / BUDGET * 100)}%"></i>
      </div>
      <div class="cap-lbl">
        <span><b>${money(t.starter_capital)}</b> in the starting eleven</span>
        <span class="${t.bench_spend >= 20 ? "warn" : ""}">${money(t.bench_spend)} on the bench</span>
        ${t.left > 0 ? `<span class="warn">${money(t.left)} never spent</span>` : ""}
      </div>
    </div>`;

    const card = (t, i) => {
      const g = G && G[t.team];
      const r = rankOf[t.team];
      const shown = t.picks.slice(0, 7);
      const rest = t.picks.slice(7);
      const pos = POS_ORDER.filter((k) => t.pos_spend[k]).map((k) =>
        `<span class="ps"><b class="pp ${posClass(k)}">${k}</b> ${money(t.pos_spend[k])}</span>`).join("");
      const gclass = g ? " " + g.grade.replace("+", "p").replace("-", "m").toLowerCase() : "";
      return `<article class="dr-card${g ? "" : " ungraded"}" id="${slug(t.team)}">
        <div class="dr-grade">
          <span class="g${gclass}">${g ? esc(g.grade) : "?"}</span>
          ${r ? `<span class="rk">#${r.rank}<i> preseason</i></span>` : ""}
        </div>
        <div class="dr-body">
          <div class="dr-head">
            <div class="dr-id">
              ${tlogo(t, "lg")}
              <div>
              <h3>${esc(t.team)}</h3>
              <div class="mg">${esc(mgr(t.team, grades))} · ${money(t.spent)} spent · ${t.count} players · top 3 = ${Math.round(t.top3_share * 100)}% of the budget</div>
              </div>
            </div>
            <div class="dr-pos">${pos}</div>
          </div>
          ${(t.missing || []).length ? `<div class="dr-note">Walked out without a ${t.missing.map((m) => esc(m)).join(" or a ")}. Costs a waiver claim on Tuesday and nothing else, which is exactly why nobody spent on them.</div>` : ""}
          ${g ? `<h4 class="dr-hl">${esc(g.headline)}</h4>
                 ${(Array.isArray(g.body) ? g.body : [g.body]).map((p) => `<p class="dr-p">${esc(p)}</p>`).join("")}
                 <div class="dr-verdicts">
                   ${g.best ? `<div class="vd good"><span class="eyebrow">Best buy</span><div>${esc(g.best)}</div></div>` : ""}
                   ${g.worst ? `<div class="vd bad"><span class="eyebrow">Worst buy</span><div>${esc(g.worst)}</div></div>` : ""}
                 </div>` : `<p class="dr-p dim">Grade pending. The roster is final; the verdict is not.</p>`}
          ${capitalBar(t)}
          <div class="dr-roster">
            ${shown.map((p) => pickLine(p, { delta: true })).join("")}
            ${rest.length ? `<div class="dr-more" hidden>${rest.map((p) => pickLine(p, { delta: true })).join("")}</div>
              <button class="dr-toggle" type="button" data-n="${t.picks.length}">Full roster (${t.picks.length}) ↓</button>` : ""}
          </div>
        </div>
      </article>`;
    };

    /* the money map: every team's spend split by position, one stacked bar each */
    const mapRows = (L.money_map || []).map((m) => {
      const segs = POS_ORDER.filter((k) => m.pos[k]).map((k) =>
        `<i class="seg ${posClass(k)}" style="width:${m.pos[k] / BUDGET * 100}%" title="${k} ${money(m.pos[k])}"></i>`).join("");
      const t = teams.find((x) => x.team === m.team) || {};
      return `<div class="mm-row">
        <span class="mm-t">${esc(m.team)}</span>
        <span class="mm-bar">${segs}</span>
        <span class="mm-v num">${money(m.starter_capital)}</span>
      </div>`;
    }).join("");

    const pm = L.pos_market || {};
    const posRows = POS_ORDER.filter((k) => pm[k]).map((k) => `<div class="mk-row">
        <span class="pp ${posClass(k)}">${k}</span>
        <span class="mk-bar"><i style="width:${Math.round(pm[k].total / totalSpent * 100 * 2.2)}%"></i></span>
        <span class="mk-v num">${money(pm[k].total)}</span>
        <span class="mk-s">${pm[k].count} bought · avg ${money(pm[k].avg)} · top ${money(pm[k].max.cost)} ${esc(pm[k].max.player)}</span>
      </div>`).join("");

    /* the board: all 224 picks in nomination order */
    const board = (draft.picks || []).slice().sort((a, b) => a.pick - b.pick);
    const boardRow = (p) => `<div class="bd-row${p.cost >= 40 ? " big" : ""}${p.cost <= 1 ? " buck" : ""}">
      <span class="bd-n">${p.pick}</span>
      <span class="pp ${posClass(p.slot)}">${esc(p.slot === "IDP" ? p.pos.split(",")[0] : p.slot)}</span>
      <span class="bd-p">${esc(p.player)} <em>${esc(p.nfl)}</em></span>
      <span class="bd-t">${esc(p.team)}</span>
      <span class="bd-c num">${money(p.cost)}</span>
    </div>`;

    return `
      <section class="dark roast-hero dr-hero">
        <div class="hero-grid">
          <div>
            <div class="filed">
              <span class="tag-red">${grades ? "Draft Grades" : "Auction Ledger"}</span>
              <span class="eyebrow">${draft.season} auction · ${draft.picks.length} picks · ${money(totalSpent)} spent · ${teams.length} teams</span>
            </div>
            <h1 class="display">${esc(headline)} <span class="kick">${esc(kicker)}</span></h1>
            <p class="lede">${esc(lede)}</p>
            <div class="hero-actions">
              <a class="btn-red" href="#grades">${grades ? "Read the grades →" : "See every pick →"}</a>
              <a class="btn-ghost" href="#rankings">Power rankings →</a>
              <a class="btn-ghost" href="#board">The full board →</a>
            </div>
          </div>
          <div class="board">
            <div class="eyebrow">${top5.length ? "Preseason power rankings" : "Biggest buys"}</div>
            ${top5.length ? top5.map((r) => `<div class="board-row has-logo">
                <span class="bn">${r.rank}</span>
                ${tlogo(teams.find((x) => x.team === r.team), "sm")}
                <span class="bt">${esc(r.team)}</span>
                <span class="bm">${esc(G && G[r.team] ? G[r.team].grade : "")}</span></div>`).join("")
              : (L.top_buys || []).slice(0, 5).map((p) => `<div class="board-row">
                <span class="bn">${money(p.cost)}</span>
                <span class="bt">${esc(p.player)}</span>
                <span class="bm">${esc(p.team)}</span></div>`).join("")}
            <a class="see-all" href="#rankings">${top5.length ? `All ${teams.length} →` : "Full ledger →"}</a>
          </div>
        </div>
      </section>

      <section class="statbug">
        ${top ? stat("Biggest buy", money(top.cost), `${top.player} · ${top.team}`, true) : ""}
        ${stat("Dollar players", L.dollar_count, `of ${draft.picks.length} picks went for a buck`)}
        ${benchKing ? stat("Most money benched", money(benchKing.bench_spend), `${benchKing.team} · league average ${money(Math.round(L.avg_bench_spend))}`, benchKing.bench_spend >= 30) : ""}
        ${qb ? stat("The entire QB market", money(qb.total), `${qb.count} QBs bought. The room paid more for two running backs.`) : ""}
      </section>

      <nav class="dr-index" id="index" aria-label="Jump to a team's grade">
        <div class="ix-head">
          <span class="eyebrow">All ${ordered.length} grades · tap yours to jump straight to it</span>
          <span class="ix-note">${grades ? "Best to worst" : "By starting-lineup capital"}</span>
        </div>
        <div class="ix-grid">
          ${ordered.map((t, i) => {
            const g = G && G[t.team];
            const r = rankOf[t.team];
            const gc = g ? " g" + g.grade.replace("+", "p").replace("-", "m").toLowerCase() : "";
            return `<a class="ix${gc}" href="#${slug(t.team)}">
              <span class="ix-n">${r ? r.rank : i + 1}</span>
              ${tlogo(t, "sm")}
              <span class="ix-t">${esc(t.team)}<em>${esc(mgr(t.team, grades))}</em></span>
              <span class="ix-g">${g ? esc(g.grade) : "—"}</span>
            </a>`;
          }).join("")}
        </div>
      </nav>

      <div class="body-grid">
        <div class="col-main" id="grades">
          <div class="sec-top"><h2 class="h-sec">${grades ? "The Grades" : "Every Roster"}</h2>
            <span class="note">${grades ? "Ordered by preseason rank, best first" : "Ordered by starting-lineup capital"}</span></div>
          <hr class="rule-h">
          <p class="os-note" style="margin-bottom:6px">Every roster below carries its projected points per week, worked out under
            this league's own scoring rules and using the lineup each manager would actually field. Nobody is punished for a slot
            they can fill off the waiver wire. Grades weigh that number against what was paid for it. They are final, unfair, and
            get reprinted in December next to your actual record.</p>
          ${ordered.map(card).join("")}
        </div>

        <div class="col-side">
          ${grades && grades.rankings ? `<div class="mod" id="rankings">
            <h2 class="h-sec">Preseason Power Rankings</h2><hr class="rule-h">
            ${grades.rankings.map((r) => `<div class="dr-rank">
              <span class="n">${r.rank}</span>
              ${tlogo(teams.find((x) => x.team === r.team), "sm")}
              <span class="t"><b>${esc(r.team)}</b><small>${esc(mgr(r.team, grades))}${G && G[r.team] ? " · " + esc(G[r.team].grade) : ""}${
                (teams.find((x) => x.team === r.team) || {}).proj
                  ? " · " + (Math.round(teams.find((x) => x.team === r.team).proj.weekly * 10) / 10).toFixed(1) + " pts/wk" : ""}</small>
                ${r.blurb ? `<span class="bl">${esc(r.blurb)}</span>` : ""}</span>
            </div>`).join("")}
            <p class="vote-foot" style="margin-top:12px"><b>How this is ranked:</b> by projected points, the same way real power
            rankings work. Every drafted player is run through this league's actual scoring rules, which are not standard
            anywhere else: half PPR, four points for a passing touchdown, kickers paid a point per ten yards of made field
            goals, and an IDP slot paid on tackles. Each roster then fields its best legal lineup and we add up what it
            should score in a normal week. Two things stop that from being naive. Nobody is punished for a slot they can
            fill off the wire, so every position is worth at least the best free agent available. And starters miss weeks,
            for byes and for hamstrings, at rates that differ by position, so a real bench earns back the points a row of
            dollar bills does not. Projections are one source and one source is always wrong somewhere. Zero games have
            been played.</p>
          </div>` : `<div class="mod" id="rankings"><h2 class="h-sec">Preseason Power Rankings</h2><hr class="rule-h">
            <p class="empty">Being written. Refresh shortly.</p></div>`}

          ${grades && grades.awards && grades.awards.length ? `<div class="mod">
            <h2 class="h-sec">Draft Night Awards</h2><hr class="rule-h">
            ${grades.awards.map((a) => `<div class="sup"><div class="award">${esc(a.label)}</div>
              <div class="who">${esc(a.team)}</div><div class="note">${esc(a.note)}</div></div>`).join("")}
          </div>` : ""}

          ${(L.holes || []).length ? `<div class="mod">
            <h2 class="h-sec">Tuesday's Shopping List</h2><hr class="rule-h">
            <p class="vote-foot" style="margin:0 0 10px">Nobody drafted a kicker or a defense with real money and nobody should.
              These three skipped one entirely and will pick it up off waivers for a dollar like everybody else does in October.</p>
            ${L.holes.map((h) => `<div class="hole-row">
              <span class="hn">${esc(h.team)}</span>
              <span class="hv">${h.missing.map((m) => `<b>${esc(m)}</b>`).join(" · ")}</span>
            </div>`).join("")}
          </div>` : ""}

          <div class="mod" id="moneymap">
            <h2 class="h-sec">The Money Map</h2><hr class="rule-h">
            <p class="vote-foot" style="margin:0 0 10px">Every budget, split by position. The number on the right is what the
              starting eleven cost. Ordered by that.</p>
            <div class="dr-map">${mapRows}</div>
            <div class="mm-key">${POS_ORDER.map((k) => `<span><i class="seg ${posClass(k)}"></i>${k}</span>`).join("")}</div>
          </div>

          <div class="mod" id="ledger">
            <h2 class="h-sec">Biggest Buys</h2><hr class="rule-h">
            <div class="dr-list">${(L.top_buys || []).map((p) => pickLine(p, { team: true, delta: true })).join("")}</div>
            <p class="vote-foot" style="margin-top:10px">The small number is the move against what this room paid for the same
              player last September.</p>
          </div>

          <div class="mod">
            <h2 class="h-sec">Where the Money Went</h2><hr class="rule-h">
            <div class="dr-market">${posRows}</div>
          </div>

          ${(L.price_moves || []).length ? `<div class="mod">
            <h2 class="h-sec">The Inflation Report</h2><hr class="rule-h">
            <p class="vote-foot" style="margin:0 0 10px">Biggest price moves against ${prev ? prev.season : "last year"}. The market
              has no memory and every year it swears it does.</p>
            <div class="dr-list">${L.price_moves.map((p) => `<div class="dr-pick">
              <span class="pp ${posClass(p.slot)}">${esc(p.slot)}</span>
              <span class="pn">${esc(p.player)} <em>${esc(p.team)}</em></span>
              <span class="pc num">${money(p.last_year)} → ${money(p.cost)} <i class="${p.delta > 0 ? "up" : "dn"}">${p.delta > 0 ? "+" : "−"}${Math.abs(p.delta)}</i></span>
            </div>`).join("")}</div>
          </div>` : ""}

          <div class="mod">
            <h2 class="h-sec">The First Ten Off The Board</h2><hr class="rule-h">
            <div class="dr-list">${(L.first_ten || []).map((p) => pickLine(p, { team: true })).join("")}</div>
            <p class="vote-foot" style="margin-top:10px">Nominated early to drain everyone else's budget, or bought early out of
              nerves. It is almost always the second one.</p>
          </div>
        </div>
      </div>

      <div class="dr-solo" id="board">
        <div class="sec-top"><h2 class="h-sec">The Board</h2>
          <span class="note">All ${board.length} picks in the order they came off</span></div>
        <hr class="rule-h">
        <div class="dr-board">
          <div class="bd-row hd"><span class="bd-n">#</span><span>Pos</span><span class="bd-p">Player</span>
            <span class="bd-t">Bought by</span><span class="bd-c">Price</span></div>
          ${board.slice(0, 40).map(boardRow).join("")}
          <div class="bd-more" hidden>${board.slice(40).map(boardRow).join("")}</div>
        </div>
        <button class="dr-toggle bd-toggle" type="button">Show all ${board.length} picks ↓</button>
      </div>`;
  }

  function wire() {
    document.querySelectorAll(".dr-toggle").forEach((b) => {
      if (b.dataset.wired) return;
      b.dataset.wired = "1";
      const more = b.classList.contains("bd-toggle")
        ? b.previousElementSibling.querySelector(".bd-more")
        : b.previousElementSibling;
      if (!more) return;
      const shut = b.textContent;
      b.addEventListener("click", () => {
        more.hidden = !more.hidden;
        b.textContent = more.hidden ? shut
          : (b.classList.contains("bd-toggle") ? "Collapse the board ↑" : "Hide the bench ↑");
      });
    });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
