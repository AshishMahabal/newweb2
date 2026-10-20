#!/usr/bin/env python3
"""Check that internal links and #anchors in site/ resolve. Run after a local build."""
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SITE = Path(__file__).resolve().parent.parent / "site"
pages = {p: p.read_text() for p in SITE.rglob("*.html")}
ids = {p: set(re.findall(r'id="([^"]+)"', t)) for p, t in pages.items()}
bad = 0
for page, text in pages.items():
    for url in re.findall(r'(?:href|src)="([^"]+)"', text):
        if re.match(r"[a-z]+:", url) or url.startswith("//"):
            continue
        path, _, frag = unquote(url).partition("#")
        path = path.split("?")[0]
        target = page if not path else (SITE / path.lstrip("/") if path.startswith("/")
                                        else page.parent / path)
        if target.is_dir():
            target = target / "index.html"
        if not target.exists() or (frag and frag not in ids.get(target.resolve(), ids.get(target, set()))):
            print(f"{page.relative_to(SITE)}: broken {url}")
            bad += 1
print(f"{len(pages)} pages checked, {bad} broken links")
sys.exit(1 if bad else 0)
