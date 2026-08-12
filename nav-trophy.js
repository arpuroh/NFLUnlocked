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

  if (add()) return;
  const mo = new MutationObserver(() => { if (add()) mo.disconnect(); });
  mo.observe(document.body, { childList: true, subtree: true });
  setTimeout(() => mo.disconnect(), 10000);
})();
