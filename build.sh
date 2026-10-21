#!/usr/bin/env bash
# Render _gen/*.md (written by scripts/generate.py) into site/ with pandoc.
#
# Internal links are written relative to each page ("../research/"), so one build
# works at any path: local preview (/), Caltech (/~aam/), GitHub Pages (/newweb2/)
# and ashishmahabal.net (/). The 404 page is the exception: the server shows it at
# whatever address was missing, so it finds its base path in the browser instead.
# SITE_DIR sets the output folder (default site/).
# CANONICAL_URL overrides the canonical/og:url base (default: the Caltech ~aam URL).
set -euo pipefail

# The Caltech copy is the official one: every build (GitHub Pages included) names
# it as canonical, so search engines index ~aam and treat the other copy as a mirror.
CANONICAL="${CANONICAL_URL:-https://sites.astro.caltech.edu/~aam}"
CANONICAL="${CANONICAL%/}"

ROOT="$(cd "$(dirname "$0")" && pwd)"
SITE="${SITE_DIR:-$ROOT/site}"
GEN="$ROOT/_gen"
TEMPLATE="$ROOT/assets/template.html"
FILTER="$ROOT/scripts/baseurl.lua"
# Added to the CSS/JS URLs so browsers and caches fetch them again after a change.
ASSET_V="$(cat "$ROOT"/assets/*.css "$ROOT"/assets/*.js | cksum | cut -d' ' -f1)"

[ -d "$GEN" ] || { echo "Missing _gen/: run python3 scripts/generate.py first"; exit 1; }

rm -rf "$SITE"
mkdir -p "$SITE"
cp -R "$ROOT/assets" "$SITE/assets"
rm -f "$SITE/assets/template.html"

# _gen/index.md -> site/index.html, _gen/<name>.md -> site/<name>/index.html,
# _gen/<dir>/index.md -> site/<dir>/index.html, so URLs look like /~aam/research/
# (the old Hugo site used the same style). Nested pages (personal/...) work the same.
render_one() {
  local md="$1" name="$2"
  local out rel section root is404=""
  case "$name" in
    index)   out="$SITE/index.html"; rel="" ;;
    404)     out="$SITE/404.html";   rel="404.html"; is404=1 ;;
    */index) out="$SITE/$name.html"; rel="${name%index}" ;;
    *)       out="$SITE/$name/index.html"; rel="$name/" ;;
  esac
  section="${name%%/*}"
  # Path from this page back to the site root: "." for the home page, ".." for
  # research/, "../.." for personal/fun/, ... (404.html sits at the root).
  root="$(echo "${rel%404.html}" | sed -e 's#[^/]*/#../#g' -e 's#/$##')"
  root="${root:-.}"
  mkdir -p "$(dirname "$out")"
  pandoc "$md" \
    --standalone \
    --template="$TEMPLATE" \
    --lua-filter="$FILTER" \
    -M baseurl="$root" \
    -M asset_v="$ASSET_V" \
    ${is404:+-M is404=1} \
    -M og_url="$CANONICAL/$rel" \
    -M site_url="$CANONICAL" \
    -M year="$(date +%Y)" \
    -M "active_$section=1" \
    -o "$out"
}

while IFS= read -r -d '' md; do
  name="${md#$GEN/}"
  render_one "$md" "${name%.md}"
done < <(find "$GEN" -name '*.md' -print0)

# Files served as they are (images, MIDI, PDFs of the personal pages).
[ -d "$ROOT/static" ] && cp -R "$ROOT/static/." "$SITE/"

# Apache (the Caltech server, the only host that reads this file): send every
# missing page under /~aam to our 404 page, which forwards old addresses to the
# nearest new page. Other hosts ignore this file and use 404.html directly.
echo "ErrorDocument 404 /~aam/404.html" > "$SITE/.htaccess"

echo "Built HTML into: $SITE"
