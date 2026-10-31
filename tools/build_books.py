#!/usr/bin/env python3
"""
Build the self-contained book summary pages.

Templates live in tools/templates/ and contain two kinds of placeholders:
  @@CSS@@            -> the contents of tools/templates/style.css
  @@FIG:name.jpg@@   -> a base64 data URI of books/figures/name.jpg

hoffman-complete.html is assembled at build time from the three part templates:
  <!--TOC-->    -> a grouped table of contents (part headings + chapter links)
  <!--PARTS-->  -> each part's part banner followed by its <main> content
Anchors that exist once per part (tldr, cheatsheet, defender, maturity) get a
part prefix (p1-, p2-, p3-) so the combined document has no duplicate ids.

Run from the repository root:
    python3 tools/build_books.py
"""

import base64
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TPL = ROOT / "tools" / "templates"
FIGS = ROOT / "books" / "figures"
OUT = ROOT / "books"

FIG_RE = re.compile(r"@@FIG:([^@]+)@@")


def data_uri(name: str) -> str:
    path = FIGS / name
    if not path.exists():
        sys.exit(f"missing figure: {path}")
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build(template: str, output: str, css: str, html: str | None = None) -> None:
    if html is None:
        html = (TPL / template).read_text(encoding="utf-8")
    used = set()

    def sub(m):
        used.add(m.group(1))
        return data_uri(m.group(1))

    html = FIG_RE.sub(sub, html)
    html = html.replace("@@CSS@@", css)
    if "@@" in html:
        sys.exit(f"unresolved placeholder left in {template}")

    dest = OUT / output
    dest.write_text(html, encoding="utf-8")
    print(f"{dest.relative_to(ROOT)}  {dest.stat().st_size/1e6:.2f} MB  ({len(used)} figures)")


# --- combined edition -------------------------------------------------------

# (id prefix, part banner id, template, TOC group label)
PARTS = [
    ("p1", "part1", "hoffman-part1.html", "Part I · Recon"),
    ("p2", "part2", "hoffman-part2.html", "Part II · Offense"),
    ("p3", "part3", "hoffman-part3.html", "Part III · Defense"),
]

# anchors that occur once per part and would collide when concatenated
PER_PART_IDS = ("tldr", "cheatsheet", "defender", "maturity")


def grab(pattern: str, text: str, where: str) -> str:
    m = re.search(pattern, text, re.S)
    if not m:
        sys.exit(f"could not find {pattern!r} in {where}")
    return m.group(1).strip()


def rename_anchors(html: str, prefix: str) -> str:
    for anchor in PER_PART_IDS:
        html = html.replace(f'id="{anchor}"', f'id="{prefix}-{anchor}"')
        html = html.replace(f'href="#{anchor}"', f'href="#{prefix}-{anchor}"')
    return html


def build_complete(template: str, output: str, css: str) -> None:
    toc, blocks = [], []

    for prefix, banner, part_template, label in PARTS:
        src = (TPL / part_template).read_text(encoding="utf-8")

        title = grab(r"<h1>(.*?)</h1>", src, part_template)          # "Part I: Recon"
        subtitle = grab(r'<p class="subtitle">(.*?)</p>', src, part_template)
        chips = grab(r'<div class="meta">(.*?)</div>', src, part_template)
        part_toc = grab(r'<aside class="toc">\s*<h4>Contents</h4>(.*?)</aside>', src, part_template)
        body = grab(r"<main>(.*?)</main>", src, part_template)

        partnum, _, partname = title.partition(": ")

        toc.append(f'<a class="part" href="#{banner}">{label}</a>')
        toc.append(rename_anchors(part_toc, prefix))

        blocks.append(
            f'<header class="parthead" id="{banner}">\n'
            f'  <div class="partnum">{partnum}</div>\n'
            f'  <h2>{partname or title}</h2>\n'
            f'  <p class="subtitle">{subtitle}</p>\n'
            f'  <div class="meta">{chips}</div>\n'
            f'</header>\n'
            + rename_anchors(body, prefix)
        )

    html = (TPL / template).read_text(encoding="utf-8")
    html = html.replace("<!--TOC-->", "\n".join(toc))
    html = html.replace("<!--PARTS-->", "\n\n".join(blocks))
    build(template, output, css, html=html)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    css = (TPL / "style.css").read_text(encoding="utf-8")
    build("index.html", "index.html", css)
    build("alice.html", "alice-and-bob-learn-secure-coding.html", css)
    build("web-application-security.html", "web-application-security.html", css)
    build("hoffman-part1.html", "web-application-security-part1-recon.html", css)
    build("hoffman-part2.html", "web-application-security-part2-offense.html", css)
    build("hoffman-part3.html", "web-application-security-part3-defense.html", css)
    build_complete("hoffman-complete.html", "web-application-security-complete.html", css)


if __name__ == "__main__":
    main()
