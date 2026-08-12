/* NFL Unlocked — Hall of Shame: Season in Review layer.
   Loads data/history.json and injects the season review + real ledger into the
   hall page after the core app renders. Kept separate from app.js so the weekly
   data pipeline never touches it. */
(() => {
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const medal = (p) => p === 1 ? "\u{1F3C6} Champion" : p === 2 ? "\u{1F948} Runner-Up" : "\u{1F949} Third Place";

  function reviewHtml(rv) {
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
            <div class="pl">\u{1F6BD} Toilet Bowl</div>
            <div class="nm">${esc(rv.toilet.team)}</div>
            <div class="mg">${esc(rv.toilet.manager)} · ${esc(rv.toilet.record)}</div>
            <p>${esc(rv.toilet.note)}</p></div>
        </div>
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
      </div>`;
  }

  function fillCore(hist) {
    const hero = document.querySelector(".hall-hero .eyebrow");
    if (hero) hero.textContent =
      `Est. ${hist.established || "—"} · ${(hist.seasons || []).length} season${(hist.seasons || []).length === 1 ? "" : "s"} on record · Zero forgiveness`;

    const cells = document.querySelectorAll(".hall-stats .c");
    const put = (i, v, s) => {
      if (!cells[i]) return;
      const vEl = cells[i].querySelector(".v"), sEl = cells[i].querySelector(".s");
      if (vEl) vEl.textContent = v;
      if (sEl) sEl.textContent = s;
    };
    if (hist.most_titles) put(0, hist.most_titles.count, hist.most_titles.team);
    if (hist.most_toilets) put(1, hist.most_toilets.count, hist.most_toilets.team);
    if (hist.career_faab) put(2, "$" + hist.career_faab.amount, hist.career_faab.team);

    const secs = [...document.querySelectorAll(".pad .h-sec")];
    const ledgerSec = secs.find((h) => /the ledger/i.test(h.textContent));
    if (ledgerSec && (hist.seasons || []).length) {
      let n = ledgerSec.nextElementSibling && ledgerSec.nextElementSibling.nextElementSibling;
      const rows = hist.seasons.map((s) => `<div class="ledger-row">
        <span class="yr">${esc(s.year)}</span>
        <span><span class="eyebrow">Champion</span><div class="nm">${esc(s.champion)}${s.champion_manager ? " (" + esc(s.champion_manager) + ")" : ""}</div></span>
        <span><span class="eyebrow red">Toilet Bowl</span><div class="nm bad">${esc(s.toilet)}${s.toilet_manager ? " (" + esc(s.toilet_manager) + ")" : ""}</div></span>
        <span><span class="eyebrow">Title Game</span><div class="sc">${esc(s.title_game || "")}</div></span>
      </div>`).join("");
      if (n && (n.classList.contains("empty") || n.classList.contains("ledger-row"))) {
        const trash = [];
        let cur = n;
        while (cur && (cur.classList.contains("empty") || cur.classList.contains("ledger-row"))) { trash.push(cur); cur = cur.nextElementSibling; }
        trash.slice(1).forEach((el) => el.remove());
        trash[0].outerHTML = rows;
      }
    }
    const lowsSec = secs.find((h) => /all-time lows/i.test(h.textContent));
    if (lowsSec && (hist.lows || []).length) {
      const n = lowsSec.nextElementSibling && lowsSec.nextElementSibling.nextElementSibling;
      if (n) n.outerHTML = `<div class="lows">${hist.lows.map((x) => `<div class="c">
        <div class="eyebrow red">${esc(x.label)}</div>
        <div class="v">${esc(x.value)}</div>
        <div class="s">${esc(x.detail)}</div></div>`).join("")}</div>`;
    }
  }

  async function run() {
    let hist;
    try {
      hist = await fetch("data/history.json", { cache: "no-store" }).then((r) => r.json());
    } catch { return; }
    const inject = () => {
      const hero = document.querySelector(".hall-hero");
      if (!hero) return false;
      fillCore(hist);
      if (hist.review && !document.querySelector(".rv")) {
        hero.insertAdjacentHTML("afterend", reviewHtml(hist.review));
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
