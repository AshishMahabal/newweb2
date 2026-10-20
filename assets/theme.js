/* Light/dark switch: cycles Auto -> Light -> Dark. "Auto" follows the system
 * setting; a manual choice is kept in localStorage and applied by the inline
 * script in <head> before the page paints.
 */
(function () {
  var btn = document.querySelector(".theme-toggle");
  if (!btn) return;
  var order = ["auto", "light", "dark"];
  var labels = { auto: "◐", light: "☀", dark: "☾" };

  function current() { return document.documentElement.dataset.theme || "auto"; }

  function apply(t) {
    if (t === "auto") delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = t;
    try {
      if (t === "auto") localStorage.removeItem("theme");
      else localStorage.setItem("theme", t);
    } catch (e) {}
    btn.textContent = labels[t];
    btn.title = "Colour theme: " + t + " (click to change)";
  }

  btn.addEventListener("click", function () {
    apply(order[(order.indexOf(current()) + 1) % order.length]);
  });
  apply(current());
  btn.hidden = false;
})();
