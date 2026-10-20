#!/usr/bin/env bash
# Netlify build: fetch pandoc (not in Netlify's image), then the usual two steps.
# BASEURL is empty: ashishmahabal.net serves the site at the domain root.
set -euo pipefail
PANDOC_VERSION=3.8.3
curl -sSL "https://github.com/jgm/pandoc/releases/download/$PANDOC_VERSION/pandoc-$PANDOC_VERSION-linux-amd64.tar.gz" \
  | tar xz -C /tmp
export PATH="/tmp/pandoc-$PANDOC_VERSION/bin:$PATH"
pip install --quiet pyyaml
python3 scripts/generate.py
BASEURL="" ./build.sh
