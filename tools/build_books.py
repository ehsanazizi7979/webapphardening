#!/usr/bin/env python3
"""
Build the self-contained book summary pages.

Templates live in tools/templates/ and contain two kinds of placeholders:
  @@CSS@@            -> the contents of tools/templates/style.css
  @@FIG:name.jpg@@   -> a base64 data URI of books/figures/name.jpg

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


def build(template: str, output: str, css: str) -> None:
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


def main() -> None:
    OUT.mkdir(exist_ok=True)
    css = (TPL / "style.css").read_text(encoding="utf-8")
    build("index.html", "index.html", css)
    build("alice.html", "alice-and-bob-learn-secure-coding.html", css)
    build("web-application-security.html", "web-application-security.html", css)
    build("hoffman-part1.html", "web-application-security-part1-recon.html", css)


if __name__ == "__main__":
    main()
