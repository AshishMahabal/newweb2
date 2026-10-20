#!/usr/bin/env python3
"""One-off import of the old ~aam/personal pages into this site, content as is.

    python3 scripts/import_personal.py [mirror_dir]

mirror_dir (default reference/personal_full/personal) is a wget mirror of
https://sites.astro.caltech.edu/~aam/personal/ (see COMMANDS.md). Writes:

    pages/personal/<path>.md   one per page, the old content wrapped in a raw HTML block
    static/personal/<path>     images, MIDI, PostScript, Perl games... copied verbatim

Three kinds of page: Hugo (Wowchemy) pages, from which only the article body is
kept; older hand-written HTML, whose <body> is kept; and plain text (poems,
jokes), shown preformatted. Links are rewritten to the new layout as
site-absolute paths ("/personal/fun/"), which scripts/baseurl.lua prefixes per
host. personal/writings is skipped: the writings site replaces it.
Re-running overwrites pages/personal and static/personal, so restyle pages only
after the import is final.
"""
import json
import os
import re
import shutil
import sys
from html import escape, unescape
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

ROOT = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "reference/personal_full/personal"
PAGES = ROOT / "pages/personal"
STATIC = ROOT / "static/personal"
OLD = "https://sites.astro.caltech.edu/~aam/personal/"
OLD_HOSTS = {"sites.astro.caltech.edu", "www.astro.caltech.edu", "astro.caltech.edu"}
ASSET_EXT = {".gif", ".jpg", ".jpeg", ".png", ".midi", ".mid", ".ps", ".pdf",
             ".pl", ".birdlist", ".txt"}
TOPICS = {"cricket": "Cricket", "familytree": "Family tree", "fun": "Fun", "music": "Music",
          "numismatics": "Numismatics", "ornithology": "Ornithology", "pasadena": "Pasadena",
          "sanskrit": "Sanskrit"}
ATTR = re.compile(r'\b(href|src|background)\s*=\s*("[^"]*"|\'[^\']*\'|[^\s>]+)', re.I)


def kind_of(text):
    if "article-style" in text:
        return "hugo"
    if re.search(r"<(html|body|p|table|h\d|br|a|pre|center|ul)\b", text, re.I):
        return "html"
    return "text"


def scan():
    """Every page: its key (old path, no trailing slash), kind, old URL and new URL."""
    pages = {}
    for dirpath, _, files in os.walk(SRC):
        rel_dir = Path(dirpath).relative_to(SRC).as_posix()
        if rel_dir == "." or rel_dir.split("/")[0] not in TOPICS:
            continue
        for f in files:
            if Path(f).suffix.lower() in ASSET_EXT:
                continue
            text = (Path(dirpath) / f).read_bytes().decode("utf-8", "replace")
            kind = kind_of(text)
            if f in ("index.html", "index"):
                key, old = rel_dir, OLD + rel_dir + "/"
            elif f.endswith(".html"):
                key, old = f"{rel_dir}/{f}", OLD + f"{rel_dir}/{f}"
            else:
                key = f"{rel_dir}/{f}"
                old = OLD + key + ("/" if kind == "hugo" else "")
            new_path = key[:-5] if key.endswith(".html") else key
            pages[key] = {"file": Path(dirpath) / f, "kind": kind, "text": text,
                          "old": old, "new": f"/personal/{new_path}/", "md": new_path}
    return pages


def make_rewriter(pages, page, link_text):
    def rewrite(m):
        attr, val = m.group(1).lower(), m.group(2).strip("'\"")
        if val.startswith(("#", "mailto:", "javascript:")) or not val:
            return m.group(0)
        if "relpermalink" in val:   # an unfilled Hugo template variable
            return f'{attr}="#"'
        u = urlparse(urljoin(page["old"], unescape(val)))
        if u.netloc not in OLD_HOSTS or not u.path.startswith("/~aam"):
            return m.group(0)
        path = unquote(u.path)
        frag = "#" + u.fragment if u.fragment else ""
        # Pre-Hugo pages lived at /~aam/fun/... rather than /~aam/personal/fun/...
        if path.split("/")[2:3] and path.split("/")[2] in TOPICS:
            path = "/~aam/personal" + path[len("/~aam"):]
        if path.startswith("/~aam/personal/writings"):
            new = "https://ashishmahabal.github.io/writings/"
        elif path.startswith("/~aam/personal/"):
            key = re.sub(r"/(index(\.html)?)?$", "", path[len("/~aam/personal/"):])
            if key not in pages and key.endswith(".html") and key[:-5] in pages:
                key = key[:-5]      # the old server had both "games" and "games.html"
            if key not in pages and "." not in key.split("/")[-1] and not (SRC / key).is_file():
                # A folder with no page of its own (a server directory listing): use the
                # nearest page above it.
                while "/" in key and key not in pages:
                    key = key.rsplit("/", 1)[0]
            if key in pages:
                new = pages[key]["new"] + frag
                if attr == "href" and key not in link_text:
                    link_text[key] = page["_last_text"]
            elif key in ("", "index.html"):
                new = "/personal/"
            else:   # an asset (copied to static/), or something long gone
                new = "/personal/" + key
        else:       # the old site outside personal/: the 404 page sorts it out
            new = path[len("/~aam"):] or "/"
        return f'{attr}="{escape(new, quote=True)}"'
    return rewrite


def content_of(page):
    t = page["text"]
    if page["kind"] == "hugo":
        title = re.search(r'docs-article-container">\s*<h1[^>]*>(.*?)</h1>', t, re.S)
        body = t.split('<div class="article-style">', 1)[1]
        ends = [body.find(e) for e in ('<div class="article-widget">', '<div class="body-footer">',
                                       '</article>', '<div class="share-box">', '<div class="page-footer">',
                                       '<footer', '<script src=', '<div class="media author-card') if e in body]
        body = body[:min(ends)] if ends else body
        body = re.sub(r"(\s*</div>)+\s*$", "", body.strip())
        updated = re.search(r"Last updated on ([^<]+)<", t)
        return (unescape(title.group(1)).strip() if title else None, body,
                updated.group(1).strip() if updated else None)
    if page["kind"] == "html":
        m = re.search(r"<body[^>]*>(.*?)(</body>|$)", t, re.S | re.I)
        body = m.group(1) if m else re.sub(r"(?is)<head>.*?</head>|</?html[^>]*>", "", t)
        title = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
        return (unescape(title.group(1)).strip() if title else None, body, None)
    return None, f'<pre class="legacy-text">{escape(t)}</pre>', None


def crumbs(key, pages):
    """Personal > Topic > ... links back up, skipping folders that have no page."""
    parts = key.split("/")
    out = ['<a href="/personal/">Personal</a>']
    for i in range(1, len(parts)):
        sub = "/".join(parts[:i])
        if sub in pages:
            label = TOPICS.get(sub) or pages[sub].get("title") or parts[i - 1]
            out.append(f'<a href="/personal/{sub}/">{escape(label)}</a>')
    return '<p class="back-link">' + " › ".join(out) + "</p>"


def main():
    pages = scan()
    link_text = {}
    # First pass: rewrite links, and learn link texts (titles for the text pages).
    anchor = re.compile(r"(<a\b[^>]*>)(.*?)</a>", re.S | re.I)
    for key, page in pages.items():
        title, body, updated = content_of(page)

        def per_anchor(m, page=page):
            page["_last_text"] = re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
            return ATTR.sub(make_rewriter(pages, page, link_text), m.group(1)) + m.group(2) + "</a>"
        body = anchor.sub(per_anchor, body)
        page["_last_text"] = ""
        body = ATTR.sub(make_rewriter(pages, page, link_text), body)
        page.update(title=title, body=body, updated=updated)

    shutil.rmtree(PAGES, ignore_errors=True)
    shutil.rmtree(STATIC, ignore_errors=True)
    for key, page in pages.items():
        title = (page["title"] or link_text.get(key) or TOPICS.get(key)
                 or key.split("/")[-1].replace("_", " "))
        title = re.sub(r"\s*\|\s*aschig.*$", "", title).strip().strip("'\"") or key
        fence = "````" if "```" in page["body"] else "```"
        lines = ["---", f"title: {json.dumps(title, ensure_ascii=False)}", "---", "",
                 fence + "{=html}", crumbs(key, pages)]
        if page["kind"] != "html":   # old HTML pages carry their own heading
            lines.append(f"<h1>{escape(title)}</h1>")
        lines += ['<div class="legacy">', page["body"].strip(), "</div>"]
        if page["updated"]:
            lines.append(f'<p class="meta">Last updated on {escape(page["updated"])}.</p>')
        lines.append(fence)
        name = page["md"] + ("/index" if (SRC / page["md"]).is_dir() and
                             page["file"].name in ("index.html", "index") else "")
        out = PAGES / (name + ".md")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n")

    n_assets = 0
    for dirpath, _, files in os.walk(SRC):
        rel_dir = Path(dirpath).relative_to(SRC)
        if rel_dir.parts[:1] and rel_dir.parts[0] in TOPICS:
            for f in files:
                if Path(f).suffix.lower() in ASSET_EXT:
                    (STATIC / rel_dir).mkdir(parents=True, exist_ok=True)
                    shutil.copy2(Path(dirpath) / f, STATIC / rel_dir / f)
                    n_assets += 1
    kinds = {k: sum(p["kind"] == k for p in pages.values()) for k in ("hugo", "html", "text")}
    print(f"{len(pages)} pages {kinds}, {n_assets} assets")


if __name__ == "__main__":
    main()
