/* Adds the Trophy Room entry to the masthead nav.
   Kept out of app.js so the nav can gain pages without reshipping the runtime. */
(() => {
  const add = () => {
    const nav = document.querySelector(".masthead nav") ||
                document.querySelector(".masthead ul") ||
                document.querySelector(".masthead");
    if (!nav) return false;
    const links = [...nav.querySelectorAll("a")];
    if (!links.length) return false;
    if (links.some((a) => (a.getAttribute("href") || "").includes("trophy"))) return true;

    const hall = links.find((a) => (a.getAttribute("href") || "").includes("hall"));
    const model = hall || links[links.length - 1];
    const a = model.cloneNode(true);
    a.setAttribute("href", "trophy.html");
    a.textContent = "Trophy Room";
    a.classList.remove("on", "active", "current");
    if (document.body.dataset.page === "trophy") {
      a.classList.add(...[...model.classList].filter((c) => /on|active|current/.test(c)));
    }
    model.after(a);
    return true;
  };

  if (!add()) {
    const mo = new MutationObserver(() => { if (add()) mo.disconnect(); });
    mo.observe(document.body, { childList: true, subtree: true });
    setTimeout(() => mo.disconnect(), 10000);
  }

  // The masthead badge is built from meta.current_week, which is 1 all through
  // the offseason - so every page claimed "Week 1 - Live" with no games on the
  // board. Correct it site-wide from the same signal offseason.js uses.
  fetch("data/league.json", { cache: "no-store" })
    .then((r) => r.json())
    .then((L) => {
      const played = (L.matchups || []).filter((m) => m.status === "postevent");
      if (played.length) return;
      const stamp = () => {
        const chip = document.querySelector(".masthead .badge-live");
        if (!chip || /offseason/i.test(chip.textContent)) return !!chip;
        chip.textContent = "Offseason";
        chip.style.background = "var(--gray-mid)";
        return true;
      };
      if (stamp()) return;
      let n = 0;
      const t = setInterval(() => { if (stamp() || ++n > 20) clearInterval(t); }, 200);
    })
    .catch(() => {});
})();
