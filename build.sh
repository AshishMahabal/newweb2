#!/usr/bin/env bash
# Render _gen/*.md (written by scripts/generate.py) into site/ with pandoc.
#
# BASEURL is the path prefix the site is served under:
#   ""        local preview (python3 -m http.server from site/)
#   /~aam     Caltech
#   /newweb2  GitHub Pages
# SITE_URL is the origin only (https://sites.astro.caltech.edu); it is used for
# canonical and og:url. Left empty locally.
set -euo pipefail

BASEURL_META="${BASEURL:-}"
BASEURL_META="/${BASEURL_META#/}"
BASEURL_META="${BASEURL_META%/}"
if [ "$BASEURL_META" = "/" ]; then BASEURL_META=""; fi

SITE_ORIGIN="${SITE_URL:-}"
SITE_ORIGIN="${SITE_ORIGIN%/}"
ABS_PREFIX="${SITE_ORIGIN}${BASEURL_META}"

ROOT="$(cd "$(dirname "$0")" && pwd)"
SITE="$ROOT/site"
GEN="$ROOT/_gen"
TEMPLATE="$ROOT/assets/template.html"
FILTER="$ROOT/scripts/baseurl.lua"

[ -d "$GEN" ] || { echo "Missing _gen/: run python3 scripts/generate.py first"; exit 1; }

rm -rf "$SITE"
mkdir -p "$SITE"
cp -R "$ROOT/assets" "$SITE/assets"
rm -f "$SITE/assets/template.html"

# _gen/index.md -> site/index.html, _gen/<name>.md -> site/<name>/index.html,
# so URLs look like /~aam/research/ (the old Hugo site used the same style).
render_one() {
  local md="$1" name="$2"
  local out rel section
  case "$name" in
    index) out="$SITE/index.html"; rel="" ;;
    404)   out="$SITE/404.html";   rel="404.html" ;;
    *)     out="$SITE/$name/index.html"; rel="$name/" ;;
  esac
  section="$name"
  mkdir -p "$(dirname "$out")"
  pandoc "$md" \
    --standalone \
    --template="$TEMPLATE" \
    --lua-filter="$FILTER" \
    -M baseurl="$BASEURL_META" \
    -M og_url="$ABS_PREFIX/$rel" \
    -M year="$(date +%Y)" \
    -M "active_$section=1" \
    -o "$out"
}

for md in "$GEN"/*.md; do
  render_one "$md" "$(basename "${md%.md}")"
done

echo "Built HTML into: $SITE"
