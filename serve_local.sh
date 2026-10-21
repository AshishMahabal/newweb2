#!/usr/bin/env bash
# Build and preview.
#   ./serve_local.sh            local build, served at http://localhost:8002/
#   ./serve_local.sh caltech    same build, served at http://localhost:8002/~aam/
#   ./serve_local.sh gh         same build, served at http://localhost:8002/newweb2/
set -euo pipefail

MODE="${1:-local}"
PORT="${2:-8002}"
ROOT="$(cd "$(dirname "$0")" && pwd)"

case "$MODE" in
  local)   export BASEURL="" ;;
  caltech) export BASEURL="/~aam" ;;
  gh)      export BASEURL="/newweb2" ;;
  *) echo "Unknown mode: $MODE (local | caltech | gh)" >&2; exit 1 ;;
esac

python3 "$ROOT/scripts/generate.py"
"$ROOT/build.sh"

if [ -z "$BASEURL" ]; then
  echo "==> http://localhost:$PORT/"
  cd "$ROOT/site" && exec python3 -m http.server "$PORT"
fi

# Mimic the prefix: serve a temp dir holding <prefix> -> site.
TMP="$(mktemp -d)"
ln -s "$ROOT/site" "$TMP/${BASEURL#/}"
echo "==> http://localhost:$PORT$BASEURL/"
cd "$TMP" && exec python3 -m http.server "$PORT"
