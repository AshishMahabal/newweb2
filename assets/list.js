/* Publications page: filter, sort and chart the list in place.
 *
 * Filters: year (bars of the chart), topic chips, project, refereed, first
 * author, text search; sort newest or most cited. The state is mirrored in the
 * URL (?year=2021&topic=ml&project=ztf&ref=1&first=1&q=...&sort=cited), so a
 * filtered view can be shared; the "Papers" buttons on Research use ?project=.
 *
 * Without JavaScript the page is still the full list, newest first, with a
 * static chart; the controls stay hidden until this runs, so they are never dead.
 */
(function () {
  var list = document.querySelector(".work-list");
  var controls = document.querySelector(".list-controls");
  if (!list || !controls) return;

  var rows = Array.prototype.slice.call(list.querySelectorAll(".work-row"));
  var heads = Array.prototype.slice.call(list.querySelectorAll(".year-head"));
  var bars = Array.prototype.slice.call(document.querySelectorAll(".ybar"));
  var chips = Array.prototype.slice.call(controls.querySelectorAll(".tchip"));
  var projSel = controls.querySelector(".lc-proj");
  var sortSel = controls.querySelector(".lc-sort");
  var refBox = controls.querySelector(".lc-ref");
  var firstBox = controls.querySelector(".lc-first");
  var query = controls.querySelector(".lc-q");
  var clearBtn = controls.querySelector(".lc-clear");
  var count = controls.querySelector(".lc-count");
  var tip = document.querySelector(".ytip");
  var peakLabel = document.querySelector(".ychart-peak");

  var state = { year: "", topic: "", project: "", ref: false, first: false, q: "", sort: "new" };

  rows.forEach(function (r) { r.__text = r.textContent.toLowerCase(); });
  var byDate = rows.slice();
  var byCites = rows.slice().sort(function (a, b) { return b.dataset.cites - a.dataset.cites; });

  function has(list, v) { return (list || "").split(",").indexOf(v) !== -1; }

  // Every filter except the year: the chart shows what the year filter would pick from.
  function passesOthers(r) {
    if (state.topic && !has(r.dataset.tags, state.topic)) return false;
    if (state.project && !has(r.dataset.projects, state.project)) return false;
    if (state.ref && r.dataset.ref !== "1") return false;
    if (state.first && r.dataset.first !== "1") return false;
    var words = state.q.toLowerCase().split(/\s+/).filter(Boolean);
    return words.every(function (w) { return r.__text.indexOf(w) !== -1; });
  }

  function render() {
    var perYear = {}, shown = 0, shownPerYear = {};
    rows.forEach(function (r) {
      var y = r.dataset.year, ok = passesOthers(r);
      if (ok) perYear[y] = (perYear[y] || 0) + 1;
      ok = ok && (!state.year || y === state.year);
      r.hidden = !ok;
      if (ok) { shown++; shownPerYear[y] = (shownPerYear[y] || 0) + 1; }
    });

    // Newest: rows in date order under year heads. Most cited: one flat list.
    var cited = state.sort === "cited";
    var frag = document.createDocumentFragment(), last = null;
    (cited ? byCites : byDate).forEach(function (r) {
      if (!cited && r.dataset.year !== last) {
        last = r.dataset.year;
        var h = heads.filter(function (x) { return x.dataset.year === last; })[0];
        if (h) frag.appendChild(h);
      }
      frag.appendChild(r);
    });
    list.appendChild(frag);
    heads.forEach(function (h) {
      var n = shownPerYear[h.dataset.year] || 0;
      h.hidden = cited || !n;
      h.querySelector(".year-n").textContent = n + (n === 1 ? " paper" : " papers");
    });

    var peak = 0, peakYear = "";
    bars.forEach(function (b) {
      var n = perYear[b.dataset.year] || 0;
      if (n >= peak) { peak = n; peakYear = b.dataset.year; }
    });
    bars.forEach(function (b) {
      var n = perYear[b.dataset.year] || 0;
      b.style.setProperty("--h", peak ? (100 * n / peak) + "%" : "0%");
      b.__n = n;
      b.setAttribute("aria-label", b.dataset.year + ": " + n + (n === 1 ? " paper" : " papers"));
      var on = b.dataset.year === state.year;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.classList.toggle("is-dim", !!state.year && !on);
    });
    if (peakLabel) peakLabel.textContent = peak ? peak + " in " + peakYear : "none";

    chips.forEach(function (c) {
      c.setAttribute("aria-pressed", c.dataset.tag === state.topic ? "true" : "false");
    });

    count.textContent = shown === rows.length
      ? shown + " papers"
      : shown + " of " + rows.length + " papers";
    clearBtn.hidden = !(state.year || state.topic || state.project || state.ref || state.first || state.q);
    writeUrl();
  }

  function readUrl() {
    var p = new URLSearchParams(location.search);
    state.year = p.get("year") || "";
    state.topic = p.get("topic") || "";
    state.project = p.get("project") || "";
    state.ref = p.get("ref") === "1";
    state.first = p.get("first") === "1";
    state.q = p.get("q") || "";
    state.sort = p.get("sort") === "cited" ? "cited" : "new";
    if (!projSel.querySelector('option[value="' + state.project + '"]')) state.project = "";
    projSel.value = state.project;
    sortSel.value = state.sort;
    refBox.checked = state.ref;
    firstBox.checked = state.first;
    query.value = state.q;
  }

  function writeUrl() {
    var p = new URLSearchParams();
    if (state.year) p.set("year", state.year);
    if (state.topic) p.set("topic", state.topic);
    if (state.project) p.set("project", state.project);
    if (state.ref) p.set("ref", "1");
    if (state.first) p.set("first", "1");
    if (state.q) p.set("q", state.q);
    if (state.sort !== "new") p.set("sort", state.sort);
    var qs = p.toString();
    history.replaceState(null, "", location.pathname + (qs ? "?" + qs : "") + location.hash);
  }

  bars.forEach(function (b) {
    b.addEventListener("click", function () {
      state.year = state.year === b.dataset.year ? "" : b.dataset.year;
      render();
    });
    function show() {
      tip.textContent = b.dataset.year + ": " + b.__n + (b.__n === 1 ? " paper" : " papers");
      tip.hidden = false;
      var box = b.getBoundingClientRect(), fig = tip.parentNode.getBoundingClientRect();
      tip.style.left = (box.left + box.width / 2 - fig.left) + "px";
    }
    b.addEventListener("mouseenter", show);
    b.addEventListener("focus", show);
    b.addEventListener("mouseleave", function () { tip.hidden = true; });
    b.addEventListener("blur", function () { tip.hidden = true; });
  });

  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      state.topic = state.topic === c.dataset.tag ? "" : c.dataset.tag;
      render();
    });
  });

  projSel.addEventListener("change", function () { state.project = projSel.value; render(); });
  sortSel.addEventListener("change", function () { state.sort = sortSel.value; render(); });
  refBox.addEventListener("change", function () { state.ref = refBox.checked; render(); });
  firstBox.addEventListener("change", function () { state.first = firstBox.checked; render(); });
  query.addEventListener("input", function () { state.q = query.value.trim(); render(); });
  clearBtn.addEventListener("click", function () {
    state = { year: "", topic: "", project: "", ref: false, first: false, q: "", sort: state.sort };
    projSel.value = ""; refBox.checked = false; firstBox.checked = false; query.value = "";
    render();
  });

  readUrl();
  controls.hidden = false;
  render();
})();
