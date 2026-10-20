/* Filter the publications list in place (topic, refereed, text search).
 *
 * Without JavaScript the page is still the full list, newest first; the
 * controls stay hidden until this runs, so they are never dead.
 */
(function () {
  var list = document.querySelector(".work-list");
  var controls = document.querySelector(".list-controls");
  if (!list || !controls) return;

  var rows = Array.prototype.slice.call(list.querySelectorAll(".work-row"));
  var heads = Array.prototype.slice.call(list.querySelectorAll(".year-head"));
  var tagSel = controls.querySelector(".lc-tag");
  var refBox = controls.querySelector(".lc-ref");
  var query = controls.querySelector(".lc-q");
  var count = controls.querySelector(".lc-count");

  rows.forEach(function (r) { r.__text = r.textContent.toLowerCase(); });

  function matches(row) {
    var tag = tagSel.value;
    if (tag && (row.dataset.tags || "").split(",").indexOf(tag) === -1) return false;
    if (refBox.checked && row.dataset.ref !== "1") return false;
    var words = query.value.toLowerCase().split(/\s+/).filter(Boolean);
    return words.every(function (w) { return row.__text.indexOf(w) !== -1; });
  }

  function render() {
    var shown = 0, visibleYears = {};
    rows.forEach(function (r) {
      var ok = matches(r);
      r.hidden = !ok;
      if (ok) { shown++; visibleYears[r.dataset.year] = true; }
    });
    heads.forEach(function (h) { h.hidden = !visibleYears[h.dataset.year]; });
    count.textContent = shown === rows.length
      ? shown + " papers"
      : shown + " of " + rows.length + " papers";
  }

  tagSel.addEventListener("change", render);
  refBox.addEventListener("change", render);
  query.addEventListener("input", render);

  controls.hidden = false;
  render();
})();
