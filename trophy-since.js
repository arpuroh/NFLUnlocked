/* Trophy Room — tenure labels.
   The career table already prints a year span for managers who have left.
   This adds the other half: "member since YYYY" for everyone still in the
   league, so the table says at a glance who is active and when they joined.
   Rows are matched by manager name, not row order, so the table is free to
   sort however it likes. */
(() => {
  const css = ".tr-champs .since{margin-top:5px;font-size:10.5px;font-weight:700;"
    + "letter-spacing:.07em;text-transform:uppercase;color:var(--gray-soft)}"
    + ".tr-champs .c.elite .since{color:var(--gray-mid)}";
  const first = (p) => String(p.span || "").split("\u2013")[0];
  const last = (p) => String(p.span || "").split("\u2013")[1];
  const norm = (s) => String(s || "").replace(/\s+/g, " ").trim().toLowerCase();

  fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()).then((db) => {
    const by = new Map();
    (db.people || []).filter((p) => p.display).forEach((p) => by.set(norm(p.manager), p));

    const apply = () => {
      const rows = [...document.querySelectorAll(".tr-table .row:not(.hd) .m")];
      if (!rows.length) return false;

      rows.forEach((el) => {
        if (el.querySelector("i")) return;
        const p = by.get(norm(el.textContent));
        if (!p || !p.active) return;
        const tag = document.createElement("i");
        tag.textContent = " \u00b7 member since " + first(p);
        el.appendChild(tag);
      });

      // On the champions board the only tenure worth printing is a departure —
      // "member since" on a card that already lists title years is noise.
      [...document.querySelectorAll(".tr-champs .c")].forEach((c) => {
        if (c.querySelector(".since")) return;
        const nm = c.querySelector(".nm");
        const p = nm && by.get(norm(nm.textContent));
        if (!p || p.active) return;
        const d = document.createElement("div");
        d.className = "since";
        d.textContent = first(p) + "\u2013" + last(p) + " \u00b7 gone";
        const tm = c.querySelector(".tm");
        if (tm) tm.after(d); else c.appendChild(d);
      });

      const st = document.createElement("style");
      st.textContent = css;
      document.head.appendChild(st);
      return true;
    };

    if (apply()) return;
    let n = 0;
    const t = setInterval(() => { if (apply() || ++n > 24) clearInterval(t); }, 250);
  }).catch(() => {});
})();
