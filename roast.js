/* NFL Unlocked — Roast Roulette.
   Spins up a random burn for a random manager from data/roasts.json. No backend,
   no votes, no state to lose: the wheel just holds a shuffled bag per manager and
   deals from it so you never get the same line twice in a row. Mounts itself into
   the Trophy Room after trophy.js has painted. */
(() => {
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  const bags = {};          // key -> indexes not yet dealt this cycle
  let people = [], current = null, last = null;
  let filter = "";          // "" = anybody; otherwise a manager key

  const deal = (p) => {
    if (!bags[p.key] || !bags[p.key].length) {
      bags[p.key] = p.burns.map((_, i) => i);
    }
    const bag = bags[p.key];
    // Avoid repeating the line we just showed, unless there is nothing else.
    let pick = Math.floor(Math.random() * bag.length);
    if (bag.length > 1 && bag[pick] === last) pick = (pick + 1) % bag.length;
    const idx = bag.splice(pick, 1)[0];
    last = idx;
    return p.burns[idx];
  };

  function paint(p, burn) {
    const card = document.querySelector("#rr-card");
    if (!card) return;
    card.classList.remove("spin");
    void card.offsetWidth;                       // restart the animation
    card.classList.add("spin");
    card.innerHTML = `
      <div class="rr-who">
        <span class="rr-nm">${esc(p.name)}</span>
        <span class="rr-tm">${esc(p.team)}</span>
        ${p.tag ? `<span class="rr-tg">${esc(p.tag)}</span>` : ""}
      </div>
      <p class="rr-burn">${esc(burn)}</p>`;
    // The chip that is "on" is the filter, which the spin must not overwrite —
    // otherwise landing on someone silently locks the wheel to them. Where the
    // wheel actually stopped is marked separately.
    document.querySelectorAll(".rr-chip").forEach((c) => {
      c.classList.toggle("on", c.dataset.k === filter);
      c.classList.toggle("hit", !filter && c.dataset.k === p.key);
    });
  }

  function spin(key) {
    const pool = key ? people.filter((p) => p.key === key) : people;
    let p = pool[Math.floor(Math.random() * pool.length)];
    if (!key && people.length > 1 && current && p.key === current.key) {
      p = people[(people.indexOf(p) + 1) % people.length];
    }
    current = p;
    paint(p, deal(p));
  }

  function shell() {
    return `
      <section class="rr">
        <div class="rr-head">
          <div>
            <div class="eyebrow red">Roast Roulette</div>
            <h2 class="rr-h">Pull the lever. Somebody gets it.</h2>
          </div>
          <div class="rr-actions">
            <button class="rr-spin" type="button">\u{1F3B0} Spin</button>
            <button class="rr-copy" type="button">Copy</button>
          </div>
        </div>
        <div class="rr-chips">
          <button class="rr-chip all on" type="button" data-k="">Anybody</button>
          ${people.map((p) => `<button class="rr-chip" type="button" data-k="${esc(p.key)}">${esc(p.name)}</button>`).join("")}
        </div>
        <div class="rr-card" id="rr-card"></div>
        <p class="rr-foot">Every line is written from the league's own record. Nobody is exempt,
        including whoever built this page.</p>
      </section>`;
  }

  function wire(root) {
    root.querySelector(".rr-spin").addEventListener("click", () => spin(filter));
    root.querySelector(".rr-copy").addEventListener("click", async (ev) => {
      const card = root.querySelector("#rr-card");
      if (!card || !current) return;
      const txt = `\u{1F525} NFL Unlocked — ${current.name}: `
        + card.querySelector(".rr-burn").textContent;
      try {
        await navigator.clipboard.writeText(txt);
        ev.target.textContent = "Copied";
        setTimeout(() => { ev.target.textContent = "Copy"; }, 1400);
      } catch { /* clipboard blocked; the text is on screen anyway */ }
    });
    root.querySelector(".rr-chips").addEventListener("click", (ev) => {
      const chip = ev.target.closest(".rr-chip");
      if (!chip) return;
      filter = chip.dataset.k || "";
      spin(filter);
    });
  }

  fetch("data/roasts.json", { cache: "no-store" }).then((r) => r.json()).then((db) => {
    people = (db.managers || []).filter((p) => (p.burns || []).length);
    if (!people.length) return;

    const mount = () => {
      if (document.querySelector(".rr")) return true;
      const anchor = document.querySelector(".tr-hero");
      if (!anchor) return false;
      anchor.insertAdjacentHTML("afterend", shell());
      const root = document.querySelector(".rr");
      wire(root);
      spin("");
      return true;
    };

    if (mount()) return;
    let n = 0;
    const t = setInterval(() => { if (mount() || ++n > 24) clearInterval(t); }, 250);
  }).catch(() => {});
})();
