/* Trophy Room — tenure labels.
   The career table already prints a year span for managers who have left.
   This adds the other half: "member since YYYY" for everyone still in the
   league, so the table says at a glance who is active and when they joined.
   Rows render in db.people order, so index alignment is the join key. */
(() => {
  const css = ".tr-champs .since{margin-top:5px;font-size:10.5px;font-weight:700;"
    + "letter-spacing:.07em;text-transform:uppercase;color:var(--gray-soft)}"
    + ".tr-champs .c.elite .since{color:var(--gray-mid)}";
  const first = (p) => String(p.span || "").split("–")[0];
  const last = (p) => String(p.span || "").split("–")[1];

  fetch("data/trophy.json", { cache: "no-store" }).then((r) => r.json()).then((db) => {
    const people = (db.people || []).filter((p) => p.display);
    const champs = people.filter((p) => p.rings > 0);

    const apply = () => {
      const rows = [...document.querySelectorAll(".tr-table .row:not(.hd) .m")];
      if (rows.length !== people.length || !rows.length) return false;

      rows.forEach((el, i) => {
        const p = people[i];
        if (!p || el.querySelector("i")) return;
        const tag = document.createElement("i");
        tag.textContent = " · member since " + first(p);
        el.appendChild(tag);
      });

      [...document.querySelectorAll(".tr-champs .c")].forEach((c, i) => {
        const p = champs[i];
        if (!p || c.querySelector(".since")) return;
        const d = document.createElement("div");
        d.className = "since";
        d.textContent = p.active ? "Member since " + first(p)
          : "Est. " + first(p) + " · left " + last(p);
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
