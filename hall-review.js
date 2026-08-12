/* NFL Unlocked — Hall of Shame: Season in Review layer.
   Loads data/history.json (the 2025 review narrative) and data/trophy.json (the
   league database) and fills the hall page after the core app renders. Kept
   separate from app.js so the weekly data pipeline never touches it. */
(() => {
  // The league renamed the Toilet Bowl to the Sacco. The stored review prose
  // predates that, so the rename is applied on the way out as well as in the labels.
  const esc = (s) => String(s ?? "").replace(/Toilet Bowl/g, "Sacco")
    .replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const medal = (p) => p === 1 ? "\u{1F3C6} Champion" : p === 2 ? "\u{1F948} Runner-Up" : "\u{1F949} Third Place";

  /* The Sacco Bowl. Yahoo drops the bottom two seeds out of every bracket, so
     none of this is in the standings — it is replayed from the weekly lineup
     scores and stored on each season in data/trophy.json. */
  function saccoHtml(rules, bowl) {
    if (!rules && !bowl) return "";
    const side = (t, label, score, sub, loser) => `<div class="c${loser ? " loser" : ""}">
      <div class="pl">${esc(label)}</div>
      <div class="nm">${esc(t.team)}</div>
      <div class="mg">${esc(t.manager)}</div>
      <div class="sc">${score}</div>
      <div class="sub">${esc(sub)}</div></div>`;

    let receipts = "";
    if (bowl) {
      const pi = bowl.play_in, f = bowl.final;
      const piLoser = pi.a.pts < pi.b.pts ? "a" : "b";
      const bowlLoser = f.a.total < f.b.total ? "a" : "b";
      const wk = (t) => (t.weekly || []).map((v) => v.toFixed(2)).join("  +  ");
      receipts = `
        <div class="sb-leg">
          <div class="sb-hd">Play-in · Week ${esc(pi.week)}<i>Loser drops into the bowl</i></div>
          <div class="sb-pair">
            ${side(pi.a, "12 seed", pi.a.pts.toFixed(2), piLoser === "a" ? "Into the bowl" : "Safe", piLoser === "a")}
            ${side(pi.b, "13 seed", pi.b.pts.toFixed(2), piLoser === "b" ? "Into the bowl" : "Safe", piLoser === "b")}
          </div>
        </div>
        <div class="sb-leg">
          <div class="sb-hd">The Bowl · Weeks ${esc(bowl.weeks[1])}–${esc(bowl.weeks[2])}<i>Lower two-week total takes it</i></div>
          <div class="sb-pair">
            ${side(f.a, "Play-in loser", f.a.total.toFixed(2), wk(f.a), bowlLoser === "a")}
            ${side(f.b, "14 seed", f.b.total.toFixed(2), wk(f.b), bowlLoser === "b")}
          </div>
        </div>`;
    }
    return `
      <h2 class="h-sec" style="margin-top:36px">${esc(rules?.headline || "The Sacco Bowl")}</h2><hr class="rule-h">
      ${rules?.body ? `<p class="rv-p">${esc(rules.body)}</p>` : ""}
      <div class="sacco-bowl">${receipts}</div>
      ${rules?.footnote ? `<p class="sb-foot">${esc(rules.footnote)}</p>` : ""}`;
  }

  function reviewHtml(rv, hist, db) {
    const season = ((db || {}).seasons || []).find((s) => s.year === rv.year) || {};
    const wr = rv.worst_record;
    return `
      <div class="pad rv">
        <div class="eyebrow red">Season in Review · ${esc(rv.year)}</div>
        <h2 class="rv-head">${esc(rv.headline)}</h2>
        <p class="rv-deck">${esc(rv.deck)}</p>
        <div class="rv-podium">
          ${rv.podium.map((p) => `<div class="c p${p.place}">
            <div class="pl">${medal(p.place)}</div>
            <div class="nm">${esc(p.team)}</div>
            <div class="mg">${esc(p.manager)} · ${esc(p.record)} · ${p.pf} PF</div>
            <p>${esc(p.note)}</p></div>`).join("")}
          <div class="c toilet">
            <div class="pl">\u{1F6BD} The Sacco</div>
            <div class="nm">${esc(rv.toilet.team)}</div>
            <div class="mg">${esc(rv.toilet.manager)} · ${esc(rv.toilet.record)}</div>
            <p>${esc(rv.toilet.note)}</p></div>
          ${wr ? `<div class="c worst">
            <div class="pl">\u{1F4C9} Worst Record</div>
            <div class="nm">${esc(wr.team)}</div>
            <div class="mg">${esc(wr.manager)} · ${esc(wr.record)} · ${wr.pf} PF</div>
            <p>${esc(wr.note)}</p></div>` : ""}
        </div>
        <h2 class="h-sec" style="margin-top:36px">${esc(rv.farewells.headline)}</h2><hr class="rule-h">
        <p class="rv-p">${esc(rv.farewells.intro)}</p>
        <div class="rv-toasts">
          ${rv.farewells.people.map((f) => `<div class="c">
            <div class="eyebrow red">${esc(f.title)}</div>
            <div class="nm">${esc(f.name)} <span class="tm">· ${esc(f.team)}</span></div>
            <p>${esc(f.toast)}</p>
            <div class="cheers">\u{1F942} Gone, but roasted forever.</div></div>`).join("")}
        </div>
        <div class="rv-arrivals">
          <div class="eyebrow">${esc(rv.arrivals.headline)}</div>
          <p>${esc(rv.arrivals.body)}</p>
        </div>
        ${saccoHtml(hist.sacco_rules, season.sacco_bowl)}
        <h2 class="h-sec" style="margin-top:36px">How It Happened</h2><hr class="rule-h">
        ${rv.story.map((p) => `<p class="rv-p">${esc(p)}</p>`).join("")}
        <h2 class="h-sec" style="margin-top:36px">The Draft, Audited</h2><hr class="rule-h">
        <p class="rv-p">${esc(rv.draft.intro)}</p>
        <div class="rv-draft">
          <div class="row hd"><span>Team</span><span>The Board</span><span>Finish</span><span>Grade</span></div>
          ${rv.draft.rows.map((r) => `<div class="row">
            <span class="t"><b>${esc(r.team)}</b><i>${esc(r.manager)} · spent $${r.spent}</i></span>
            <span class="b">${esc(r.board)}<i>${esc(r.verdict)}</i></span>
            <span class="f">${esc(r.finish)}</span>
            <span class="g ${r.grade[0] === "A" ? "good" : (r.grade[0] === "D" || r.grade[0] === "F") ? "bad" : ""}">${esc(r.grade)}</span>
          </div>`).join("")}
        </div>
      </div>`;
  }

  function fillCore(hist, db) {
    const people = (db.people || []).filter((p) => p.display);
    const top = (fn) => {
      const best = Math.max(0, ...people.map(fn));
      return { n: best, who: people.filter((p) => fn(p) === best).map((p) => p.manager) };
    };
    const titles = top((p) => p.rings);
    const toilets = top((p) => p.toilets.length);
    const seconds = top((p) => p.runner_ups.length);

    const hero = document.querySelector(".hall-hero .eyebrow");
    if (hero) hero.textContent =
      `Est. ${db.first_season} · ${db.completed_seasons} seasons on record · ${people.length} managers · Zero forgiveness`;

    const cells = document.querySelectorAll(".hall-stats .c");
    const put = (i, label, v, s) => {
      if (!cells[i]) return;
      const eEl = cells[i].querySelector(".eyebrow");
      const vEl = cells[i].querySelector(".v"), sEl = cells[i].querySelector(".s");
      if (eEl && label) eEl.textContent = label;
      if (vEl) vEl.textContent = v;
      if (sEl) sEl.textContent = s;
    };
    put(0, "Most Titles", titles.n, titles.who.join(" & "));
    put(1, "Most Saccos", toilets.n, toilets.who.join(" & "));
    put(2, "Most Times Runner-Up", seconds.n, seconds.who.join(" & "));

    // The season-by-season ledger lives in the Trophy Room now; this page keeps
    // the superlatives and the review.
    const secs = [...document.querySelectorAll(".pad .h-sec")];
    const lowsSec = secs.find((h) => /all-time lows/i.test(h.textContent));
    const rec = db.records || {};
    const lows = [
      rec.fewest_points_season && { label: "Fewest points, one season",
        value: Math.round(rec.fewest_points_season.points_for).toLocaleString(),
        detail: `${rec.fewest_points_season.manager} · ${rec.fewest_points_season.team} · ${rec.fewest_points_season.year}` },
      rec.worst_record && { label: "Worst record", value: `${rec.worst_record.wins}-${rec.worst_record.losses}`,
        detail: `${rec.worst_record.manager} · ${rec.worst_record.team} · ${rec.worst_record.year}` },
      rec.best_record && { label: "Best record, still no ring", value: `${rec.best_record.wins}-${rec.best_record.losses}`,
        detail: `${rec.best_record.manager} · ${rec.best_record.team} · ${rec.best_record.year} — lost the final` },
      rec.most_moves && { label: "Most roster moves", value: rec.most_moves.moves,
        detail: `${rec.most_moves.manager} · ${rec.most_moves.team} · ${rec.most_moves.year}` },
    ].filter(Boolean);
    if (lowsSec && lows.length) {
      const n = lowsSec.nextElementSibling && lowsSec.nextElementSibling.nextElementSibling;
      if (n) n.outerHTML = `<div class="lows">${lows.map((x) => `<div class="c">
        <div class="eyebrow red">${esc(x.label)}</div>
        <div class="v">${esc(x.value)}</div>
        <div class="s">${esc(x.detail)}</div></div>`).join("")}</div>`;
    }
  }

  async function run() {
    let hist, db;
    try {
      [hist, db] = await Promise.all([
        fetch("data/history.json", { cache: "no-store" }).then((r) => r.json()),
        fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({})),
      ]);
    } catch { return; }
    const inject = () => {
      const hero = document.querySelector(".hall-hero");
      if (!hero) return false;
      fillCore(hist, db || {});
      if (hist.review && !document.querySelector(".rv")) {
        hero.insertAdjacentHTML("afterend", reviewHtml(hist.review, hist, db || {}));
      }
      return true;
    };
    if (inject()) return;
    const mo = new MutationObserver(() => { if (inject()) mo.disconnect(); });
    mo.observe(document.getElementById("app") || document.body, { childList: true, subtree: true });
    setTimeout(() => mo.disconnect(), 15000);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run);
  else run();
})();
