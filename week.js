/* ══════════════════════════════════════════════════════════════
   WEEK RECAP — reads data/week<N>.json, which scripts/build_week.py
   writes from the week's real box scores. All prose lives in that
   file (authored in scripts/week_notes.py); nothing is written here.
   week.html?w=2 will render Week 2 the moment data/week2.json exists.

   Every block below is a function in SECTIONS. ORDER is the running
   order of the page and RAIL is the sticky nav — to move a section,
   move its name in ORDER and nothing else.
   ══════════════════════════════════════════════════════════════ */
(async function () {
  const { $, $$, esc, endband, stamps, wireStamps } = NU;
  const app = $("#app");
  // data/weeks.json lists every recap on file. No ?w= means the latest one.
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
    app.innerHTML = `<p class="empty pad" style="padding:40px 30px">
      No recap filed for Week ${wk} yet. It lands the Monday after the games.
      ${IDX ? `<a class="see-all" style="color:var(--red)" href="week.html">Latest recap →</a>` : ""}</p>`;
    return;
  }
  const weeksOnFile = IDX ? IDX.weeks : [{ week: W.week, headline: W.headline }];
  const isLatest = !IDX || W.week === IDX.latest;
  document.title = `Week ${W.week} Recap — NFL Unlocked`;

  const n1 = (v) => Number(v || 0).toFixed(1);
  const n2 = (v) => Number(v || 0).toFixed(2);
  const T = Object.fromEntries(W.teams.map((t) => [t.team_id, t]));
  const link = (t) => `team.html?t=${encodeURIComponent(t.team_key)}`;
  const logo = (t, cls) => t && t.logo
    ? `<img class="tlogo${cls ? " " + cls : ""}" src="${esc(t.logo)}" alt="" loading="lazy">` : "";
  const money = (p) => p.fa ? `<span class="cost fa">FA</span>` : `<span class="cost">$${p.cost}</span>`;
  const pos = (p) => `<span class="pos-chip">${esc(p.pos || p.slot || "")}</span>`;
  const sec = (txt) => W.sections[txt] ? `<p class="intro">${esc(W.sections[txt])}</p>` : "";
  const ordinal = (n) => {
    const s = ["th", "st", "nd", "rd"], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  };
  const rankOf = (id) => W.teams.findIndex((t) => t.team_id === id) + 1;

  /* ── derived ────────────────────────────────────────── */
  const M = W.median;
  const medTeam = (id) => (T[id] || {}).name || "";
  const medNames = (ids) => {
    const n = ids.map(medTeam);
    return n.length < 2 ? (n[0] || "") : n.slice(0, -1).join(", ") + " and " + n[n.length - 1];
  };
  const totalRegret = W.teams.reduce((s, t) => s + t.regret, 0);
  const perfect = W.teams.filter((t) => t.efficiency >= 99.95);
  const high = W.teams[0];
  const luckiest = [...W.teams].sort((a, b) => b.luck - a.luck)[0];
  const robbed = [...W.teams].sort((a, b) => a.luck - b.luck)[0];
  const ppRate = (p) => p.cost / p.pts;
  const worstBuy = W.money_pits.filter((p) => p.pts > 0).sort((a, b) => ppRate(b) - ppRate(a))[0];
  const ghosts = W.money_pits.filter((p) => p.pts === 0 && !p.stats);      // never took the field
  const refunds = W.money_pits.filter((p) => p.pts < 0);                   // took it and went backwards
  const biggestCrime = W.bench_crimes[0];
  const crimeTeam = T[biggestCrime.team_id];
  const bestGame = Math.max(...W.games.map((g) => g.winner_points + g.loser_points));
  const marginOf = (id) => n2((W.games.find((g) => g.winner === id || g.loser === id) || {}).margin || 0);

  /* ── page furniture ─────────────────────────────────── */
  // The rail is the sticky sub-nav. Order here follows ORDER below; anything
  // not listed (the receipt, position weather) is an interstitial, not a stop.
  const RAIL = [
    ["awards", "Awards"], ["power", "Power Rankings"], ["median", "The Median"],
    ["standings", "Lineups"], ["bench", "Bench Crimes"], ["faab", "FAAB Audit"],
    ["money", "Money"], ["studs", "Studs &amp; Duds"], ["games", "The Seven"],
  ];
  const num = Object.fromEntries(RAIL.map(([id], i) => [id, String(i + 1).padStart(2, "0")]));
  const head = (id, title, note) => `
    <section class="wk-sec" id="${id}">
      <div class="sec-top">
        <h2 class="h-sec"><span class="secno">${num[id] || ""}</span>${title}</h2>
        <span class="note">${note}</span>
      </div>
      <hr class="rule-h">`;

  /* ══ SECTIONS ══════════════════════════════════════════ */
  const PR = W.power_rankings || [];
  const mvChip = (m) => m > 0 ? `<span class="mv up">▲${m}</span>`
    : m < 0 ? `<span class="mv dn">▼${Math.abs(m)}</span>` : `<span class="mv eq">—</span>`;
  const taxLeader = [...W.teams].filter((t) => t.season)
    .sort((a, b) => (b.season.lineup_tax - a.season.lineup_tax) || (b.season.regret - a.season.regret))[0];
  const audit = W.faab_audit || [];
  const spentWeek = audit.reduce((s, a) => s + (a.bid || 0), 0);
  const paid = audit.filter((a) => a.bid);                  // real FAAB money changed hands
  const freeAgents = audit.filter((a) => a.bid === null);

  const SECTIONS = {

    power: () => !PR.length ? "" : `${head("power", "Power Rankings", W.week === 1 ? "Movement is off the draft model" : "Season to date")}
      ${sec("power")}
    </section>
    <div class="wk-table-wrap">
      <table class="tbl pr-tbl">
        <thead><tr>
          <th>#</th><th>Team</th><th class="r">Record</th><th class="r hide-s">Points</th>
          <th class="r hide-s">All-Play</th><th class="r hide-s">Best Lineup</th><th class="r">Tax</th>
        </tr></thead>
        <tbody>${PR.map((r) => {
          const t = T[r.team_id], s = t.season || {};
          return `<tr>
            <td><span class="rk"><b>${r.rank}</b>${mvChip(r.movement)}</span></td>
            <td><a href="${link(t)}" class="pr-name">${logo(t, "sm")}<span>
              <span class="n">${esc(t.name)}</span>
              <span class="m">${esc(t.manager)}<span class="only-s"> · ${n1(s.points_for || t.points)} pts${
                s.optimal_record ? ` · best lineup ${esc(s.optimal_record)}` : ""}</span></span>
              ${r.blurb ? `<span class="pr-blurb">${esc(r.blurb)}</span>` : ""}</span></a></td>
            <td class="r"><span class="rec">${esc(s.record || t.record)}</span></td>
            <td class="r hide-s"><span class="big">${n1(s.points_for || t.points)}</span></td>
            <td class="r hide-s"><span class="m">${esc(s.all_play || t.all_play)}</span></td>
            <td class="r hide-s"><span class="rec">${esc(s.optimal_record || "")}</span></td>
            <td class="r">${s.lineup_tax ? `<span class="tax">−${s.lineup_tax}</span>` : `<span class="m">0</span>`}</td>
          </tr>`;
        }).join("")}</tbody>
      </table>
    </div>
    ${taxLeader && taxLeader.season.lineup_tax >= 2 ? `<p class="wk-note">Top of the tax table:
      ${esc(taxLeader.name)}, a ${esc(taxLeader.season.record)} team whose best lineup would be
      ${esc(taxLeader.season.optimal_record)}. That is ${taxLeader.season.lineup_tax} wins left on
      the bench, and ${n1(taxLeader.season.regret)} points.</p>` : ""}`,

    faab: () => `${head("faab", "FAAB Audit", spentWeek ? `$${spentWeek} spent this week` : "Snapshot, not advice")}
      ${sec("faab") || sec("waivers")}
    </section>
    ${paid.length ? `<div class="wk-table-wrap">
      <table class="tbl">
        <thead><tr><th class="r">Paid</th><th>Player</th><th>Bought By</th>
          <th class="r">Week ${W.week}</th><th class="hide-s">Used</th></tr></thead>
        <tbody>${paid.map((a) => `<tr>
          <td class="r"><span class="${a.bid ? "cost" : "cost fa"}">${a.bid === null ? "FA" : "$" + a.bid}</span></td>
          <td><span class="pos-chip">${esc(a.pos)}</span><span class="n">${esc(a.player)}</span></td>
          <td><span class="m">${esc(a.team)}</span></td>
          <td class="r">${a.pts === null || a.slot === "IR" ? `<span class="m">—</span>`
            : `<span class="big ${a.started && a.pts >= 10 ? "" : "down"}">${n2(a.pts)}</span>`}</td>
          <td class="hide-s"><span class="stat">${a.pts === null ? "not on the roster by Sunday"
            : a.started ? "started" : a.slot === "IR" ? "on IR" : "benched"}</span></td>
        </tr>`).join("")}</tbody>
      </table>
    </div>` : ""}
    ${freeAgents.length ? `<p class="wk-note">Plus ${freeAgents.length} free-agent pickup${freeAgents.length === 1 ? "" : "s"}
      at no cost. The ones that played for their new team: ${freeAgents.filter((a) => a.pts !== null)
        .sort((a, b) => b.pts - a.pts).slice(0, 6)
        .map((a) => `${esc(a.player)} ${n2(a.pts)} (${esc(a.team)}, ${a.started ? "started" : "benched"})`).join("; ")
        || "none of them"}.</p>` : ""}
    <div class="faab-strip">${[...W.teams].sort((a, b) => a.faab_left - b.faab_left).map((t) => `
      <div class="fs-cell"><span class="fs-v ${t.faab_left < 50 ? "red" : ""}">$${t.faab_left}</span>
        <span class="fs-n">${esc(t.name)}</span></div>`).join("")}</div>
    <p class="wk-note">${esc(W.waiver_note)}</p>`,

    awards: () => `${head("awards", "The Awards", "No trophies, only records")}
      ${sec("awards")}
    </section>
    <div class="wk-awards">${W.awards.map((a) => `<div class="sup">
      <div class="award">${esc(a.title)}</div>
      <div class="who">${esc(a.winner)}</div>
      <div class="note">${esc(a.line)}</div></div>`).join("")}</div>`,

    receipt: () => `
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
            started and never took the field, which is not a rate, it is a donation.` : ""}${
            refunds.length ? ` Also unrankable: ${refunds.map((g) => `${esc(g.name)} ($${g.cost}, ${esc(g.team)}, ${n2(g.pts)})`).join(", ")}
            played and finished below zero, which is not a rate, it is a refund request.` : ""}</div>
        </div>
        <div class="r-cell">
          <div class="r-k">Most expensive seat on a bench</div>
          <div class="r-v">${n2(biggestCrime.pts)}</div>
          <div class="r-s">${esc(biggestCrime.name)} scored it in street clothes for
            ${esc(biggestCrime.team)}, who left ${n2(crimeTeam.regret)} on the bench in total and
            ${crimeTeam.won ? "won by " + marginOf(crimeTeam.team_id) + " anyway"
                            : "lost by " + marginOf(crimeTeam.team_id)}.</div>
        </div>
      </div>
    </section>`,

    standings: () => `${head("standings", `Week ${W.week} Lineups`, "Who started what")}
      ${sec("standings")}
    </section>
    <div class="wk-table-wrap">
      <table class="tbl">
        <thead><tr>
          <th>#</th><th>Team</th><th class="r">Points</th><th class="r">Week</th><th class="r">vs Median</th>
          <th class="r">All-Play</th><th class="r">Lineup Eff.</th><th class="r">Left On Bench</th>
          <th class="r hide-s">Preseason</th><th class="r">Luck</th>
        </tr></thead>
        <tbody>${W.teams.map((t, i) => {
          const clean = t.efficiency >= 99.95;
          const d = (t.pre_rank || 0) - (i + 1);
          return `<tr>
            <td><span class="rk"><b>${i + 1}</b></span></td>
            <td><a href="${link(t)}" style="display:flex;align-items:center;gap:9px">
              ${logo(t, "sm")}<span><span class="n">${esc(t.name)}</span>
              <span class="m">${esc(t.manager)} · ${esc((t.season || {}).record || t.record)} season</span></span></a></td>
            <td class="r"><span class="big">${n2(t.points)}</span></td>
            <td class="r"><span class="rec">${esc(t.record)}</span></td>
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
      ${ordinal(rankOf(luckiest.team_id))} best score in the league, and ${esc(robbed.name)}
      lost one with the ${ordinal(rankOf(robbed.team_id))}. One of those is a fraud and one of
      those got robbed, and neither of them gets to pick which.</p>`,

    median: () => `${head("median", "The Median", `${n2(M.value)} · the second opponent`)}
      ${sec("median")}
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
      ${n2(Math.abs((T[M.closest_below] || {}).vs_median))}. Same number, opposite week.</p>`,

    bench: () => `${head("bench", "Bench Crimes", `${n1(totalRegret)} points, unplayed`)}
      ${sec("bench")}
    </section>
    <div class="wk-table-wrap">
      <table class="tbl">
        <thead><tr><th>Player</th><th>Sat For</th><th class="r">Cost</th>
          <th class="r">Points</th><th class="hide-s">Line</th></tr></thead>
        <tbody>${W.bench_crimes.slice(0, 10).map((p) => `<tr>
          <td>${pos(p)}<span class="n">${esc(p.name)}</span></td>
          <td><span class="m">${esc(p.team)}</span></td>
          <td class="r">${money(p)}</td>
          <td class="r"><span class="big down">${n2(p.pts)}</span></td>
          <td class="hide-s"><span class="stat">${esc(p.stats || "—")}</span></td>
        </tr>`).join("")}</tbody>
      </table>
    </div>`,

    money: () => {
      // From Week 2 on, money is season to date; Week 1 only ever had the one Sunday.
      const season = W.week > 1 && (W.season_money_pits || []).length;
      const pits = season ? W.season_money_pits : W.money_pits;
      const bins = season ? W.season_bargains : W.bargains;
      const title = season ? `Draft Money vs ${W.week} Sundays` : "Draft Money vs One Sunday";
      return `${head("money", title, "Unfair on purpose")}
      ${sec("money")}
    </section>
    <div class="wk-two">
      <section>
        <h3 class="h-sec sub">The Money Pit</h3><hr class="rule-t">
        <div class="wk-list">${pits.slice(0, 8).map((p) => `<div class="wk-li">
          <span><span class="n">${esc(p.name)}</span>
            <span class="m">$${p.cost} · ${esc(p.team)} · ${p.pts > 0
              ? "$" + (p.cost / p.pts).toFixed(2) + " per point" : "no points yet"}${
              season ? ` · ${p.weeks} wk` : ""}</span></span>
          <span class="v bad">${n2(p.pts)}</span></div>`).join("")}</div>
      </section>
      <section>
        <h3 class="h-sec sub">The Bargain Bin</h3><hr class="rule-t">
        <div class="wk-list">${bins.slice(0, 8).map((p) => `<div class="wk-li">
          <span><span class="n">${esc(p.name)}</span>
            <span class="m">$${p.cost} · ${esc(p.team)}${season ? ` · ${p.weeks} wk`
              : ` · ${p.started ? "started" : "on the bench"}`}</span></span>
          <span class="v">${n2(p.pts)}</span></div>`).join("")}</div>
      </section>
    </div>`;
    },

    studs: () => `${head("studs", "Studs &amp; Duds", "Against the projection")}
      ${sec("studs")}
    </section>
    <div class="wk-two">
      <section>
        <h3 class="h-sec sub">Best Starts</h3><hr class="rule-t">
        <div class="wk-list">${W.top_starts.slice(0, 8).map((p) => `<div class="wk-li">
          <span><span class="n">${esc(p.name)}</span>
            <span class="m">${esc(p.team)} · ${p.fa ? "free agent" : "$" + p.cost} ·
              ${p.vs_proj > 0 ? "+" : ""}${n2(p.vs_proj)} vs projection</span></span>
          <span class="v">${n2(p.pts)}</span></div>`).join("")}</div>
      </section>
      <section>
        <h3 class="h-sec sub">Worst Starts</h3><hr class="rule-t">
        <div class="wk-list">${W.worst_starts.slice(0, 8).map((p) => `<div class="wk-li">
          <span><span class="n">${esc(p.name)}</span>
            <span class="m">${esc(p.team)} · ${p.fa ? "free agent" : "$" + p.cost} ·
              ${n2(p.vs_proj)} vs projection</span></span>
          <span class="v bad">${n2(p.pts)}</span></div>`).join("")}</div>
      </section>
    </div>`,

    games: () => `${head("games", "The Seven", "Closest first")}
      ${sec("games")}
    </section>
    <div class="wk-games">
      ${W.games.map((g, i) => {
        const w = T[g.winner], l = T[g.loser];
        const tag = i === 0 ? "Closest game"
          : i === W.games.length - 1 ? "Biggest beating"
          : (g.winner_points + g.loser_points) === bestGame ? "Highest-scoring game"
          : `Game ${i + 1} of ${W.games.length}`;
        return `<article class="wk-game">
          <div class="wk-g-head">
            <span class="wk-g-tag">${esc(tag)}</span>
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
    </div>`,

    weather: () => `
    <section class="wk-sec">
      <div class="sec-top"><h2 class="h-sec sub">Position Weather</h2>
        <span class="note">League-wide starter averages</span></div>
      <hr class="rule-t">
    </section>
    <div class="wk-slots">${Object.entries(W.slot_averages).map(([k, v]) => `
      <div class="wk-slot"><div class="k">${esc(k)}</div>
        <div class="v">${n1(v.avg)}</div>
        <div class="s">${n1(v.high)} hi · ${n1(v.low)} lo</div></div>`).join("")}</div>`,

  };

  // Running order of the page. Move a name here to move the section.
  const ORDER = ["awards", "receipt", "power", "median", "standings", "bench",
                 "faab", "money", "studs", "games", "weather"];

  /* ══ RENDER ════════════════════════════════════════════ */
  app.innerHTML = `
  <section class="dark wk-hero">
    <div class="hero-grid">
      <div>
        <div class="filed">
          <label class="wk-pick"><span class="sr">Choose a week</span>
            <select id="wk-pick">${[...weeksOnFile].sort((a, b) => b.week - a.week).map((x) =>
              `<option value="${x.week}"${x.week === W.week ? " selected" : ""}>Week ${x.week} · Final${
                IDX && x.week === IDX.latest ? " (latest)" : ""}</option>`).join("")}</select>
          </label>
          <span class="eyebrow">${W.season} season · all 14 rosters re-scored</span>
          ${isLatest ? "" : `<a class="tag-red" href="week.html">Latest: Week ${IDX.latest} →</a>`}
        </div>
        <h1 class="display">${esc(W.headline)}<span class="kick">${esc(W.kicker)}</span></h1>
        <p class="wk-lede">${esc(W.lede)}</p>
      </div>
      <div class="board">
        <div class="eyebrow">Final Scores · season records</div>
        ${[...W.games].sort((a, b) => b.winner_points - a.winner_points).map((g) => {
          const w = T[g.winner], l = T[g.loser];
          return `<a class="board-row wk-bd" href="#games">
            <span class="bt">${esc(w.name)} <em>${esc((w.season || {}).record || w.record)}</em></span>
            <span class="bn">${n1(g.winner_points)}</span>
            <span class="bt lost">${esc(l.name)} <em>${esc((l.season || {}).record || l.record)}</em></span>
            <span class="bm">${n1(g.loser_points)}</span>
          </a>`;
        }).join("")}
        <a class="see-all" href="#games">Every game, written up →</a>
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

  <nav class="wk-rail" aria-label="Sections"><div class="rail-inner">
    ${RAIL.map(([id, label], i) => `<a href="#${id}" data-rail="${id}">
      <span class="rn">${String(i + 1).padStart(2, "0")}</span>${label}</a>`).join("")}
  </div></nav>

  ${ORDER.map((k) => SECTIONS[k]()).join("")}

  ${endband({ last_updated: W.built_at })}`;

  wireStamps();

  const pick = $("#wk-pick");
  if (pick) pick.addEventListener("change", () => {
    location.href = `week.html?w=${pick.value}`;
  });

  /* ── sticky rail: highlight the section you are in ───── */
  // Each section element is only its header block (the tables and grids that follow
  // are siblings), so an IntersectionObserver on them goes dark the moment a heading
  // scrolls off. Measure against the headings' offsets instead.
  const links = Object.fromEntries($$("[data-rail]").map((a) => [a.dataset.rail, a]));
  const box = $(".wk-rail .rail-inner");
  const ids = RAIL.map(([id]) => id).filter((id) => document.getElementById(id));
  let current = null, ticking = false;

  function spy() {
    ticking = false;
    const y = window.scrollY + 120;                 // masthead + rail + a little air
    let active = ids[0];
    for (const id of ids) {
      if (document.getElementById(id).offsetTop <= y) active = id; else break;
    }
    if (active === current) return;
    current = active;
    Object.entries(links).forEach(([id, a]) => a.classList.toggle("on", id === active));
    if (box && box.scrollWidth > box.clientWidth) {
      const a = links[active];
      if (a) box.scrollTo({ left: Math.max(0, a.offsetLeft - 16), behavior: "smooth" });
    }
  }
  addEventListener("scroll", () => {
    if (!ticking) { ticking = true; requestAnimationFrame(spy); }
  }, { passive: true });
  addEventListener("resize", spy, { passive: true });
  // lazy-loaded team logos change the offsets under us, so re-measure once they land
  addEventListener("load", spy);
  spy();
})();
