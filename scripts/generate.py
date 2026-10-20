#!/usr/bin/env python3
"""Turn data/* and pages/*.md into the Markdown that build.sh renders.

    pages/**/*.md     copied to _gen/, with <!-- AUTO:NAME --> markers filled in
    data/projects.yaml  -> _gen/research.md
    data/talks.csv, data/teaching.csv -> _gen/talks.md
    data/ads.json + data/pubs_extra.yaml + data/selected.txt -> _gen/publications.md

Generated HTML goes into ```{=html} blocks so pandoc passes it through as is.
Site-absolute links ("/research/") get the baseurl added by scripts/baseurl.lua.
"""
import csv
import json
import re
import shutil
from collections import Counter
from html import escape
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAGES = ROOT / "pages"
GEN = ROOT / "_gen"

MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def raw(html):
    return "```{=html}\n" + html.strip() + "\n```\n"


def nice_date(d):
    """'2020-02-16' -> 'Feb 16, 2020'; '2026-01' -> 'Jan 2026'; '2025' -> '2025'."""
    parts = d.split("-")
    if len(parts) == 1:
        return d
    m = MONTHS[int(parts[1]) - 1]
    return f"{m} {int(parts[2])}, {parts[0]}" if len(parts) == 3 else f"{m} {parts[0]}"


def read_csv(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# --- Research -------------------------------------------------------------

def load_projects():
    return yaml.safe_load((DATA / "projects.yaml").read_text())


def project_html(p, n_papers=0):
    years = str(p.get("years") or "")
    years = f"since {years[:-1]}" if years.endswith("-") else years.replace("-", "–")
    meta = [years, p.get("role") or ""]
    meta = " · ".join(m for m in meta if m)
    links = [f'<a class="btn btn-sm" href="{escape(u)}">{escape(t)}</a>'
             for t, u in p.get("links", [])]
    if n_papers:
        links.append(f'<a class="btn btn-sm" href="/publications/?project={p["id"]}#all">'
                     f'Papers ({n_papers})</a>')
    links = " ".join(links)
    out = [f'<section class="project theme-{p["theme"]}" id="{p["id"]}">',
           f'<h3>{escape(p["title"])}</h3>']
    if meta:
        out.append(f'<p class="meta">{escape(meta)}</p>')
    out.append(f'<p>{escape(p["blurb"].strip())}</p>')
    if links:
        out.append(f'<p class="buttons">{links}</p>')
    out.append("</section>")
    return "\n".join(out)


def research_md(d, pubs):
    """Current projects under their themes, then "Dormant", then "Earlier work" (past)."""
    status = lambda p: p.get("status") or "current"
    current = [p for p in d["projects"] if status(p) == "current"]
    extra = [(s, title, [p for p in d["projects"] if status(p) == s])
             for s, title in (("dormant", "Dormant"), ("past", "Earlier work"))]
    extra = [e for e in extra if e[2]]
    themes = [t for t in d["themes"] if any(p["theme"] == t["id"] for p in current)]
    out = ["---", "title: Research", "---", "", "# Research", ""]
    n = Counter(pid for p in pubs for pid in p["projects"])
    html = lambda ps: raw("\n".join(project_html(p, n[p["id"]]) for p in ps))
    out.append(raw('<p class="buttons">' + " ".join(
        f'<a class="btn theme-btn theme-{t["id"]}" href="#{t["id"]}">{escape(t["short"])}</a>'
        for t in themes) + "</p>"))
    if extra:
        out.append(raw('<p class="buttons">' + " ".join(
            f'<a class="btn btn-sm" href="#{s}">{title}</a>' for s, title, _ in extra) + "</p>"))
    for t in themes:
        out += [f"## {t['title']} {{#{t['id']}}}", "", t["blurb"].strip(), ""]
        out.append(html([p for p in current if p["theme"] == t["id"]]))
    for s, title, ps in extra:
        out += [f"## {title} {{#{s}}}", ""]
        out.append(html(ps))
    return "\n".join(out)


def focus_html(d):
    by_id = {p["id"]: p for p in d["projects"]}
    cards = []
    for pid in d.get("focus", []):
        p = by_id[pid]
        role = f'<span class="card-role">{escape(p["role"])}</span>' if p.get("role") else ""
        cards.append(f'<a class="card theme-{p["theme"]}" href="/research/#{pid}">'
                     f'<span class="card-title">{escape(p["title"])}</span>{role}</a>')
    return raw('<div class="cards">\n' + "\n".join(cards) + "\n</div>")


def news_html(n=5):
    rows = sorted(read_csv("news.csv"), key=lambda r: r["date"], reverse=True)[:n]
    items = []
    for r in rows:
        text = escape(r["text"])
        if r["link"]:
            text = f'<a href="{escape(r["link"])}">{text}</a>'
        items.append(f'<li><span class="when">{nice_date(r["date"])}</span> {text}</li>')
    return raw('<ul class="news">\n' + "\n".join(items) + "\n</ul>")


# --- Talks and teaching ---------------------------------------------------

def talks_md():
    talks = sorted(read_csv("talks.csv"), key=lambda r: r["date"], reverse=True)
    teaching = sorted(read_csv("teaching.csv"), key=lambda r: r["date"], reverse=True)
    out = ["---", "title: Talks and teaching", "---", "", "# Talks and teaching", "",
           "## Talks", ""]
    html, year = ['<ul class="plain-list">'], None
    for r in talks:
        y = r["date"][:4]
        if y != year:
            html.append(f'<li class="year-head">{y}</li>')
            year = y
        title = escape(r["title"])
        if r["link"]:
            title = f'<a href="{escape(r["link"])}">{title}</a>'
        where = ", ".join(escape(x) for x in (r["event"], r["place"]) if x)
        html.append(f'<li>{title}<br><span class="meta">{where} · {nice_date(r["date"])}</span></li>')
    html.append("</ul>")
    out.append(raw("\n".join(html)))
    out += ["## Teaching and schools", ""]
    html = ['<ul class="plain-list">']
    for r in teaching:
        title = escape(r["title"])
        if r["link"]:
            title = f'<a href="{escape(r["link"])}">{title}</a>'
        meta = " · ".join(escape(x) for x in (r["place"], r["detail"], nice_date(r["date"])) if x)
        html.append(f'<li>{title}<br><span class="meta">{meta}</span></li>')
    html.append("</ul>")
    out.append(raw("\n".join(html)))
    return "\n".join(out)


# --- Publications ---------------------------------------------------------

KEEP_DOCTYPES = {"article", "eprint", "inproceedings", "inbook", "book",
                 "phdthesis", "techreport", "software", "proceedings"}
# ADS name search also finds other Mahabals.
NOT_ME = re.compile(r"Mahabal, (Abhijit|Anil)\b")
ML_RE = re.compile(r"machine.learn|deep.learn|neural|classif|\bAI\b|artificial intel|"
                   r"data.scien|data.driven|informatics|broker|anomal|bayesian|"
                   r"autoencoder|transformer|statistic|big data", re.I)
BIO_RE = re.compile(r"cancer|biomark|medic|clinic|tumou?r|patient|health|fung|protein", re.I)
TAG_NAMES = {"astro": "Astronomy", "ml": "AI/ML", "bio": "Biomedical", "other": "Other"}


def short_name(a):
    """'Mahabal, Ashish A.' -> 'A. A. Mahabal'."""
    if "," not in a:
        return a
    last, first = [s.strip() for s in a.split(",", 1)]
    initials = " ".join(w[0] + "." for w in re.split(r"[\s.]+", first) if w and w[0].isalpha())
    return f"{initials} {last}".strip()


def authors_html(authors, count, pos):
    names = [short_name(a) for a in authors]
    show = names[:3]
    if count <= 5 and len(names) >= count:   # short list: show everyone
        show = names
    elif pos is not None and pos >= 3:
        show = names[:1] + ["…", "A. A. Mahabal"]
    out = [f"<b>{escape(n)}</b>" if n.lower().endswith("mahabal") else escape(n) for n in show]
    s = ", ".join(out)
    if count > len(show) - show.count("…"):
        s += f" et al. ({count} authors)"
    return s


def arxiv_id(ids):
    for i in ids or []:
        if i.startswith("arXiv:"):
            return i[6:]
    return None


def from_ads(d):
    title = (d.get("title") or ["PhD thesis" if d.get("doctype") == "phdthesis" else "(untitled)"])[0]
    tags = ["astro"]
    if ML_RE.search(title):
        tags.append("ml")
    if BIO_RE.search(title):
        tags.append("bio")
    venue = d.get("pub", "")
    if d.get("volume"):
        venue += f" {d['volume']}"
    if d.get("page"):
        venue += f", {d['page'][0]}"
    return {
        "year": int(d["year"]), "date": d.get("pubdate", d["year"]),
        "title": title, "venue": venue,
        "authors": authors_html(d.get("author", []), d.get("author_count", 0), d.get("mahabal_pos")),
        "doi": (d.get("doi") or [None])[0], "arxiv": arxiv_id(d.get("identifier")),
        "bibcode": d["bibcode"], "tags": tags,
        "text": title + " " + (d.get("abstract") or ""),
        "refereed": "REFEREED" in (d.get("property") or []),
        "preprint": d.get("doctype") == "eprint",
        "cites": d.get("citation_count") or 0, "first": d.get("mahabal_pos") == 0,
    }


def from_extra(e):
    return {
        "year": int(e["year"]), "date": str(e["year"]), "title": e["title"],
        "venue": e.get("venue", ""), "authors": escape(e.get("authors", "")),
        "doi": e.get("doi"), "arxiv": e.get("arxiv"), "bibcode": None, "text": e["title"],
        "tags": e.get("tags", ["other"]), "refereed": not e.get("preprint", False),
        "preprint": e.get("preprint", False), "selected": e.get("selected", False),
        "cites": 0, "first": e.get("first", False),
    }


def mahabal_name(d):
    """The Mahabal author string, or "" when it sits past the authors kept in ads.json."""
    pos = d.get("mahabal_pos")
    return d["author"][pos] if pos is not None and pos < len(d["author"]) else ""


def title_key(p):
    return re.sub(r"\W+", "", p["title"].lower())


def dedupe(pubs):
    """ADS sometimes keeps the arXiv preprint and the published paper as separate
    records. Keep the published one, carrying over the arXiv id."""
    best = {}
    for p in pubs:
        k = title_key(p)
        q = best.get(k)
        if q is None:
            best[k] = p
            continue
        keep, drop = (q, p) if p["preprint"] else (p, q)
        keep["arxiv"] = keep["arxiv"] or drop["arxiv"]
        keep["text"] = max(keep["text"], drop["text"], key=len)
        best[k] = keep
    return list(best.values())


def load_pubs(projects):
    ads_file = DATA / "ads.json"
    ads = json.loads(ads_file.read_text()) if ads_file.exists() else []
    pubs = dedupe([from_ads(d) for d in ads if d.get("doctype") in KEEP_DOCTYPES
                   and not NOT_ME.match(mahabal_name(d))])
    by_doi = {p["doi"].lower(): p for p in pubs if p["doi"]}
    by_title = {title_key(p): p for p in pubs}
    for e in yaml.safe_load((DATA / "pubs_extra.yaml").read_text()) or []:
        x = from_extra(e)
        hit = by_doi.get(str(x["doi"]).lower()) or by_title.get(title_key(x))
        if hit and hit["doi"]:   # ADS has it: keep ADS metadata, take the curated tags/flags
            hit["tags"] = x["tags"]
            hit["selected"] = x["selected"]
        elif hit:   # same title but no DOI in ADS (e.g. a meeting abstract): curated wins
            x["text"] = max(x["text"], hit["text"], key=len)
            pubs[pubs.index(hit)] = x
        else:
            pubs.append(x)
    sel_file = DATA / "selected.txt"
    keys = set()
    if sel_file.exists():
        keys = {l.split("#")[0].strip().lower() for l in sel_file.read_text().splitlines()}
        keys.discard("")
    for p in pubs:
        if (p["bibcode"] or "").lower() in keys or (p["doi"] or "").lower() in keys:
            p["selected"] = True
    pats = [(pr["id"], re.compile(pr["papers"], re.I)) for pr in projects["projects"]
            if pr.get("papers")]
    for p in pubs:
        p["projects"] = [pid for pid, rx in pats if rx.search(p["text"])]
    pubs.sort(key=lambda p: p["date"], reverse=True)
    return pubs, len(ads)


def pub_html(p):
    url = (f"https://ui.adsabs.harvard.edu/abs/{p['bibcode']}/abstract" if p["bibcode"]
           else f"https://doi.org/{p['doi']}" if p["doi"] else "")
    title = escape(p["title"])
    title = f'<a class="pub-title" href="{escape(url)}">{title}</a>' if url else title
    links = []
    if p["arxiv"]:
        links.append(f'<a class="chip" href="https://arxiv.org/abs/{escape(p["arxiv"])}">arXiv</a>')
    if p["doi"] and p["bibcode"]:
        links.append(f'<a class="chip" href="https://doi.org/{escape(p["doi"])}">DOI</a>')
    if p["bibcode"]:
        links.append(f'<a class="chip" href="https://ui.adsabs.harvard.edu/abs/'
                     f'{escape(p["bibcode"])}/exportcitation">BibTeX</a>')
    if p["cites"]:
        links.append(f'<a class="chip chip-cites" href="https://ui.adsabs.harvard.edu/abs/'
                     f'{escape(p["bibcode"])}/citations">cited {p["cites"]}</a>')
    badges = ' <span class="badge">preprint</span>' if p["preprint"] else ""
    meta = " · ".join(x for x in (escape(p["venue"]), str(p["year"])) if x)
    if links:
        meta += " · " + " ".join(links)
    authors = f'<br><span class="pub-authors">{p["authors"]}</span>' if p["authors"] else ""
    return (f'{title}{badges}{authors}<br><span class="meta">{meta}</span>')


def h_index(cites):
    cites = sorted(cites, reverse=True)
    return sum(1 for i, c in enumerate(cites, 1) if c >= i)


def stats_html(pubs):
    tiles = [(len(pubs), "papers"), (sum(p["refereed"] for p in pubs), "refereed"),
             (sum(p["first"] for p in pubs), "first author"),
             (f'{sum(p["cites"] for p in pubs):,}', "citations (ADS)"),
             (h_index(p["cites"] for p in pubs), "h-index (ADS)")]
    return ('<div class="stats">' + "".join(
        f'<div class="stat"><span class="stat-num">{n}</span><span class="stat-label">{l}</span></div>'
        for n, l in tiles) + "</div>")


def year_chart_html(pubs):
    """Papers per year as bars; each bar is a button that filters the list (list.js).
    Heights here are for all papers; list.js recomputes them under the other filters."""
    per = Counter(p["year"] for p in pubs)
    ref = Counter(p["year"] for p in pubs if p["refereed"])
    years = list(range(min(per), max(per) + 1))
    peak = max(per.values())
    peak_year = max(years, key=lambda y: (per[y], y))
    bars, axis = [], []
    for i, y in enumerate(years, 1):
        n = per[y]
        bars.append(f'<button type="button" class="ybar" data-year="{y}" style="--h:{100 * n / peak:.1f}%" '
                    f'aria-label="{y}: {n} papers, {ref[y]} refereed" aria-pressed="false">'
                    f'<span class="ybar-fill"></span></button>')
        # Every fifth year, plus the ends unless a fifth-year label is too close.
        if y % 5 == 0 or (y in (years[0], years[-1]) and min(y % 5, 5 - y % 5) > 2):
            axis.append(f'<span style="grid-column:{i}">{y}</span>')
    return ('<figure class="ychart">'
            f'<figcaption class="meta">Papers per year, peak <span class="ychart-peak">{peak} in {peak_year}</span>. '
            'Click a year to show only that year.</figcaption>'
            f'<div class="ychart-bars" style="--n:{len(years)}">{"".join(bars)}</div>'
            f'<div class="ychart-axis" style="--n:{len(years)}">{"".join(axis)}</div>'
            '<div class="ytip" hidden></div></figure>')


def publications_md(pubs, n_ads, projects):
    counts = Counter(t for p in pubs for t in p["tags"])
    n_proj = Counter(pid for p in pubs for pid in p["projects"])
    per_year = Counter(p["year"] for p in pubs)
    out = ["---", "title: Publications", "---", "", "# Publications", "",
           "Astronomy papers come from "
           "[NASA ADS](https://ui.adsabs.harvard.edu/search/q=author%3A%22Mahabal%2C%20A%22&sort=date%20desc%2C%20bibcode%20desc); "
           "the rest are added by hand. Also on "
           "[Google Scholar](https://scholar.google.com/citations?user=Ww9DSqAAAAAJ).", ""]
    if not n_ads:
        out += ["<!-- data/ads.json missing: run scripts/fetch_ads.py -->", ""]
    out.append(raw(stats_html(pubs)))
    sel = [p for p in pubs if p.get("selected")]
    if sel:
        out += ["## Selected", ""]
        out.append(raw('<ul class="plain-list">\n' +
                       "\n".join(f"<li>{pub_html(p)}</li>" for p in sel) + "\n</ul>"))
    out += ["## All {#all}", ""]
    chips = "".join(f'<button type="button" class="tchip" data-tag="{t}" aria-pressed="false">'
                    f'{TAG_NAMES[t]} <span class="tchip-n">{counts[t]}</span></button>'
                    for t in TAG_NAMES if counts[t])
    controls = (
        '<div class="list-controls" hidden>'
        f'<div class="lc-row lc-chips">{chips}</div>'
        '<div class="lc-row">'
        '<label class="lc-field">Project <select class="lc-proj"><option value="">All</option>'
        + "".join(f'<option value="{pr["id"]}">{escape(pr["title"])} ({n_proj[pr["id"]]})</option>'
                  for pr in projects["projects"] if n_proj[pr["id"]]) + '</select></label>'
        '<label class="lc-field">Sort <select class="lc-sort"><option value="new">Newest</option>'
        '<option value="cited">Most cited</option></select></label>'
        '<label class="lc-field"><input type="checkbox" class="lc-ref"> Refereed</label>'
        '<label class="lc-field"><input type="checkbox" class="lc-first"> First author</label>'
        '</div><div class="lc-row">'
        '<label class="lc-field lc-grow"><input type="search" class="lc-q" placeholder="Search titles, authors"></label>'
        '<button type="button" class="btn btn-sm lc-clear" hidden>Clear filters</button>'
        '<span class="lc-count"></span></div></div>')
    html, year = [year_chart_html(pubs), controls, '<ul class="work-list">'], None
    for p in pubs:
        if p["year"] != year:
            year = p["year"]
            html.append(f'<li class="year-head" data-year="{year}">{year} '
                        f'<span class="year-n">{per_year[year]} papers</span></li>')
        html.append(f'<li class="work-row" data-year="{year}" data-tags="{",".join(p["tags"])}" '
                    f'data-projects="{",".join(p["projects"])}" data-cites="{p["cites"]}" '
                    f'data-first="{1 if p["first"] else 0}" '
                    f'data-ref="{1 if p["refereed"] else 0}">{pub_html(p)}</li>')
    html.append("</ul>")
    out.append(raw("\n".join(html)))
    return "\n".join(out)


# --- Main -----------------------------------------------------------------

def main():
    shutil.rmtree(GEN, ignore_errors=True)
    GEN.mkdir()
    projects = load_projects()
    auto = {"FOCUS": focus_html(projects), "NEWS": news_html()}
    for md in PAGES.rglob("*.md"):
        text = md.read_text()
        for k, v in auto.items():
            text = text.replace(f"<!-- AUTO:{k} -->", v)
        out = GEN / md.relative_to(PAGES)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
    pubs, n_ads = load_pubs(projects)
    (GEN / "research.md").write_text(research_md(projects, pubs))
    (GEN / "talks.md").write_text(talks_md())
    (GEN / "publications.md").write_text(publications_md(pubs, n_ads, projects))
    print(f"Wrote {len(list(GEN.rglob('*.md')))} pages into {GEN.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
