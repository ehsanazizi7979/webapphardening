# webapphardening

Study notes for the two books in this repository:

- **Alice & Bob Learn Secure Coding** — Tanya Janca (Wiley, 2025)
- **Web Application Security: Exploitation and Countermeasures** — Andrew Hoffman (O'Reilly, 2nd ed. 2024)

## What is in here

| Path | What it is |
|---|---|
| `books/index.html` | Landing page: what each book covers and how they differ |
| `books/alice-and-bob-learn-secure-coding.html` | Plain-language summary of all 15 chapters + 5 figures from the book |
| `books/web-application-security.html` | Plain-language summary of all 37 chapters + 42 figures from the book |
| `books/web-application-security-part1-recon.html` | Deep dive on Part I (Recon, chapters 2–8): 16 figures + the book's recon code |
| `books/web-application-security-part2-offense.html` | Deep dive on Part II (Offense, chapters 9–19): 19 figures + the book's attack code and payloads |
| `books/web-application-security-part3-defense.html` | Deep dive on Part III (Defense, chapters 20–37): 17 figures + the book's mitigations and secure-coding guidance |
| `books/web-application-security-complete.html` | All three deep dives concatenated in book order (chapters 2–37, 52 figures) with one grouped table of contents |
| `books/figures/` | The extracted figure images (JPEG) |
| `tools/templates/` | Editable HTML templates and the shared stylesheet |
| `tools/build_books.py` | Builds the seven pages in `books/` from the templates |

Open `books/index.html` in any browser — no server needed. Every page is a single,
self-contained file: the stylesheet is inlined and every image is embedded as a
base64 data URI, so the summaries can be copied, e-mailed or printed on their own.

## Rebuilding after an edit

Edit `tools/templates/*.html` or `tools/templates/style.css`, then:

```bash
python3 tools/build_books.py
```

Templates use two placeholders: `@@CSS@@` (the stylesheet) and
`@@FIG:name.jpg@@` (an image from `books/figures/`, inlined as a data URI).

## Notes

The figures are reproduced from the books for personal study; the captions
explaining each figure were written for these notes. Page/PDF sources are the two
PDF files in the repository root.
