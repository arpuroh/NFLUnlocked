/* NFL Unlocked — Roast Roulette.
   Its own page now. Pulls the burns out of data/roasts.json and the career line
   out of data/trophy.json, then deals one at random. No backend and no stored
   state: the wheel holds a shuffled bag per manager and empties it before it
   reshuffles, so a spin never repeats a line you have already seen this visit. */
(() => {
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  let people = [];
  const bags = {};              // key -> burn indexes not yet dealt this cycle
  let current = null;           // whoever the wheel last landed on
  let lastBurn = "";
  let filter = "";              // "" = anybody; otherwise a manager key
  let dealt = 0;
  let spinning = false;

  /* ── dealing ─────────────────────────────────────────── */
  const deal = (p) => {
    if (!bags[p.key] || !bags[p.key].length) bags[p.key] = p.burns.map((_, i) => i);
    const bag = bags[p.key];
    let pick = Math.floor(Math.random() * bag.length);
    if (bag.length > 1 && p.burns[bag[pick]] === lastBurn) pick = (pick + 1) % bag.length;
    const burn = p.burns[bag.splice(pick, 1)[0]];
    lastBurn = burn;
    return burn;
  };

  const pickPerson = (key) => {
    if (key) return people.find((p) => p.key === key);
    let p = people[Math.floor(Math.random() * people.length)];
    // Two spins in a row on the same person reads as a broken wheel, so nudge on.
    if (people.length > 1 && current && p.key === current.key) {
      p = people[(people.indexOf(p) + 1) % people.length];
    }
    return p;
  };

  /* ── the card ────────────────────────────────────────── */
  function line(p) {
    const bits = [];
    if (p.record) bits.push(`<span>${esc(p.record)}</span>`);
    if (p.rings) bits.push(`<span class="gold">${"\u{1F3C6}".repeat(Math.min(p.rings, 4))} ${p.rings} title${p.rings > 1 ? "s" : ""}</span>`);
    if (p.saccos) bits.push(`<span class="bad">\u{1F6BD} ${p.saccos} Sacco${p.saccos > 1 ? "s" : ""}</span>`);
    if (p.seasons) bits.push(`<span class="dim">${p.seasons} season${p.seasons > 1 ? "s" : ""}</span>`);
    return bits.length ? `<div class="rr-line">${bits.join("")}</div>` : "";
  }

  function paint(p, burn) {
    const face = document.querySelector("#rr-face");
    if (!face) return;
    face.innerHTML = `
      <div class="rr-who">
        <div class="rr-nm">${esc(p.name)}</div>
        <div class="rr-meta">
          <span class="rr-tm">${esc(p.team)}</span>
          ${p.tag ? `<span class="rr-tg">${esc(p.tag)}</span>` : ""}
        </div>
      </div>
      ${line(p)}
      <p class="rr-burn">${esc(burn)}</p>`;
    // The lit chip is the *filter*, which a spin must never overwrite — otherwise
    // landing on somebody silently locks the wheel to them. Where the wheel
    // actually stopped is marked separately, in red.
    document.querySelectorAll(".rr-chip").forEach((c) => {
      c.classList.toggle("on", c.dataset.k === filter);
      c.classList.toggle("hit", !filter && c.dataset.k === p.key);
    });
    const n = document.querySelector("#rr-count");
    if (n) n.textContent = `${dealt} pulled · ${people.reduce((a, x) => a + x.burns.length, 0)} on file`;
  }

  /* ── the pull ────────────────────────────────────────── */
  function spin(key) {
    if (spinning) return;
    const target = pickPerson(key);
    if (!target) return;
    spinning = true;
    dealt += 1;

    const machine = document.querySelector("#rr-machine");
    const reel = document.querySelector("#rr-reel");
    machine.classList.add("rolling");

    // A short blur of names before it settles. Purely theatre, and the whole
    // point of a roulette.
    let ticks = 0;
    const total = 11;
    const roll = () => {
      ticks += 1;
      reel.textContent = people[Math.floor(Math.random() * people.length)].name;
      if (ticks < total) {
        setTimeout(roll, 38 + ticks * 9);
      } else {
        reel.textContent = target.name;
        machine.classList.remove("rolling");
        machine.classList.remove("landed");
        void machine.offsetWidth;
        machine.classList.add("landed");
        current = target;
        paint(target, deal(target));
        spinning = false;
      }
    };
    roll();
  }

  /* ── chrome ──────────────────────────────────────────── */
  function shell(db) {
    const burns = people.reduce((a, p) => a + p.burns.length, 0);
    return `
      <section class="rr-hero dark">
        <div class="eyebrow red">Roast Roulette</div>
        <h1 class="display">Pull the lever.<br>Somebody gets it.</h1>
        <p class="rr-sub">${burns} burns on file across ${people.length} managers and fifteen years of
        evidence. Every line is drawn from the league's own record. Nobody is exempt, including
        whoever built this page.</p>
        <div class="rr-stats">
          <div><b>${people.length}</b><span>Managers loaded</span></div>
          <div><b>${burns}</b><span>Burns on file</span></div>
          <div><b>15</b><span>Seasons of evidence</span></div>
          <div><b>0</b><span>Appeals upheld</span></div>
        </div>
      </section>

      <section class="rr-stage">
        <div class="rr-machine" id="rr-machine">
          <div class="rr-top">
            <span class="rr-label">Reel</span>
            <span class="rr-reel" id="rr-reel">—</span>
            <span class="rr-count" id="rr-count"></span>
          </div>
          <div class="rr-face" id="rr-face"></div>
          <div class="rr-controls">
            <button class="rr-spin" type="button">\u{1F3B0} <b>Spin</b></button>
            <button class="rr-copy" type="button">Copy line</button>
            <span class="rr-hint" id="rr-hint">Or aim it at somebody below</span>
          </div>
        </div>

        <div class="rr-target">
          <div class="eyebrow">Aim the wheel</div>
          <div class="rr-chips">
            <button class="rr-chip all on" type="button" data-k="">Anybody</button>
            ${people.map((p) => `<button class="rr-chip" type="button" data-k="${esc(p.key)}"
              title="${esc(p.record || "")}">${esc(p.short || p.name)}</button>`).join("")}
          </div>
          <p class="rr-note">Ordered by career wins, most first. The two rookies have no record to
          stand on yet, so they wait at the end.</p>
        </div>
      </section>`;
  }

  function wire() {
    document.querySelector(".rr-spin").addEventListener("click", () => spin(filter));

    document.querySelector(".rr-copy").addEventListener("click", async (ev) => {
      const burn = document.querySelector(".rr-burn");
      if (!burn || !current) return;
      const txt = `\u{1F525} NFL Unlocked — ${current.name}: ${burn.textContent}`;
      try {
        await navigator.clipboard.writeText(txt);
        ev.target.textContent = "Copied";
        setTimeout(() => { ev.target.textContent = "Copy line"; }, 1400);
      } catch { /* clipboard blocked; the text is on screen anyway */ }
    });

    document.querySelector(".rr-chips").addEventListener("click", (ev) => {
      const chip = ev.target.closest(".rr-chip");
      if (!chip) return;
      filter = chip.dataset.k || "";
      const hint = document.querySelector("#rr-hint");
      const who = people.find((p) => p.key === filter);
      if (hint) hint.textContent = who ? `Locked on ${who.name}` : "Or aim it at somebody below";
      spin(filter);
    });

    // Space bar pulls the lever, because of course it does.
    document.addEventListener("keydown", (ev) => {
      if (ev.code !== "Space" || /^(INPUT|TEXTAREA|BUTTON)$/.test(document.activeElement.tagName)) return;
      ev.preventDefault();
      spin(filter);
    });
  }

  /* ── boot ────────────────────────────────────────────── */
  Promise.all([
    fetch("data/roasts.json", { cache: "no-store" }).then((r) => r.json()),
    fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()).catch(() => ({ people: [] })),
  ]).then(([db, tr]) => {
    // The burns file carries the writing; the trophy database carries the record.
    // Joining them here keeps roasts.json pure content that anybody can edit.
    const rec = Object.fromEntries((tr.people || []).map((p) => [p.key, p]));
    people = (db.managers || []).filter((p) => (p.burns || []).length).map((p) => {
      const r = rec[p.key];
      return !r ? p : Object.assign({}, p, {
        record: `${r.wins}-${r.losses}${r.ties ? "-" + r.ties : ""}`,
        rings: r.rings, saccos: (r.toilets || []).length, seasons: r.seasons,
      });
    });
    if (!people.length) throw new Error("no burns");

    const mount = () => {
      const app = document.querySelector("#app");
      if (!app) return false;
      app.innerHTML = shell(db);
      wire();
      spin("");
      return true;
    };
    if (mount()) return;
    let n = 0;
    const t = setInterval(() => { if (mount() || ++n > 24) clearInterval(t); }, 200);
  }).catch(() => {
    const app = document.querySelector("#app");
    if (app) app.innerHTML = `<div class="pad"><p class="empty">The wheel is jammed. Try again shortly.</p></div>`;
  });
})();
