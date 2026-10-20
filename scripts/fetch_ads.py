#!/usr/bin/env python3
"""Fetch Ashish Mahabal's papers from NASA ADS into data/ads.json.

Run locally; the result is committed so CI needs no token.
Token: ADS_API_TOKEN env var, else ~/.ads/dev_key (the ads package convention).
The token is never printed.

    python3 scripts/fetch_ads.py
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "ads.json"

QUERY = 'author:("Mahabal, A" OR "Mahabal, Ashish") year:1990-2100'
FIELDS = ["bibcode", "title", "author", "author_count", "year", "pubdate", "pub",
          "volume", "page", "doi", "identifier", "property", "doctype",
          "citation_count", "abstract"]   # abstract: only for matching papers to projects
ROWS = 200


def token():
    t = os.environ.get("ADS_API_TOKEN", "").strip()
    if not t:
        f = Path.home() / ".ads" / "dev_key"
        if f.exists():
            t = f.read_text().strip()
    if not t:
        sys.exit("No ADS token: set ADS_API_TOKEN (or create ~/.ads/dev_key).")
    return t


def fetch_all(tok):
    docs, start = [], 0
    while True:
        params = urllib.parse.urlencode({
            "q": QUERY, "fl": ",".join(FIELDS), "rows": ROWS, "start": start,
            "sort": "date desc"})
        req = urllib.request.Request(
            "https://api.adsabs.harvard.edu/v1/search/query?" + params,
            headers={"Authorization": "Bearer " + tok})
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.load(r)["response"]
        docs += resp["docs"]
        start += ROWS
        if start >= resp["numFound"]:
            return docs


def main():
    docs = fetch_all(token())
    for d in docs:
        # Keep the first few authors only: the full lists run to hundreds.
        # Remember where Mahabal sits so a long list can still show him.
        authors = d.get("author", [])
        d["mahabal_pos"] = next((i for i, a in enumerate(authors)
                                 if a.lower().startswith("mahabal")), None)
        d["author"] = authors[:12]
    OUT.write_text(json.dumps(docs, indent=1, ensure_ascii=False) + "\n")
    print(f"Wrote {len(docs)} records to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
