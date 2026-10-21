#!/usr/bin/env bash
# Render _gen/*.md (written by scripts/generate.py) into site/ with pandoc.
#
# BASEURL is the path prefix the site is served under:
#   ""        local preview (python3 -m http.server from site/)
#   /~aam     Caltech
#   /newweb2  GitHub Pages
# SITE_DIR sets the output folder (default site/).
# CANONICAL_URL overrides the canonical/og:url base (default: the Caltech ~aam URL).
set -euo pipefail

BASEURL_META="${BASEURL:-}"
BASEURL_META="/${BASEURL_META#/}"
BASEURL_META="${BASEURL_META%/}"
if [ "$BASEURL_META" = "/" ]; then BASEURL_META=""; fi

# The Caltech copy is the official one: every build (GitHub Pages included) names
# it as canonical, so search engines index ~aam and treat the other copy as a mirror.
CANONICAL="${CANONICAL_URL:-https://sites.astro.caltech.edu/~aam}"
CANONICAL="${CANONICAL%/}"

ROOT="$(cd "$(dirname "$0")" && pwd)"
SITE="${SITE_DIR:-$ROOT/site}"
GEN="$ROOT/_gen"
TEMPLATE="$ROOT/assets/template.html"
FILTER="$ROOT/scripts/baseurl.lua"

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
  local out rel section
  case "$name" in
    index)   out="$SITE/index.html"; rel="" ;;
    404)     out="$SITE/404.html";   rel="404.html" ;;
    */index) out="$SITE/$name.html"; rel="${name%index}" ;;
    *)       out="$SITE/$name/index.html"; rel="$name/" ;;
  esac
  section="${name%%/*}"
  mkdir -p "$(dirname "$out")"
  pandoc "$md" \
    --standalone \
    --template="$TEMPLATE" \
    --lua-filter="$FILTER" \
    -M baseurl="$BASEURL_META" \
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

# Apache (the Caltech server): send every missing page under the base path to our
# 404 page, which forwards old addresses to the nearest new page. Other hosts
# ignore this file and use 404.html directly.
echo "ErrorDocument 404 $BASEURL_META/404.html" > "$SITE/.htaccess"

echo "Built HTML into: $SITE"
