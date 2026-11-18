---
name: doc-reader
version: 1.0.0
allowed-tools: Read, Grep, Glob, Bash
description: >
  Use when you need to read a PDF (journal paper, government report, guideline,
  reference document with tables and figures) and want to spend as few tokens as
  possible, e.g. "read this PDF", "what does chapter 6 of this report say",
  "find the discount rate in this guideline", "summarise this paper", "get the
  table on page 45". Converts the PDF once to cached Markdown, strips repeated
  headers and footers, builds a short map, and lets you read one section, a page
  range, or keyword hits instead of the whole file. Scanned pages are read with
  Docling OCR. Use it before opening any PDF longer than a few pages.
---

# doc-reader

Read long documents by map first, then by section. Never load the whole file when a section answers the question.

## Pairs with

- zotero-cite: use doc-reader to read a paper, then zotero-cite to add and cite it.
- numbers-audit: use doc-reader to pull a number from a source report, then numbers-audit to trace it into the manuscript.
- health-policy-brief and research-writer: read the source documents with doc-reader before drafting.
- qual-researcher: transcripts and reports can be read in sections before coding.

## Platform compatibility

Environment-dependent. Needs Python 3.10 or later and a shell. A private virtual environment is created by the setup step. PyMuPDF is AGPL licensed; this skill installs it on the user's machine and does not ship it. Docling (MIT) is installed only when a scanned page is first met (about 2 GB, roughly 10 minutes, one time). Office files (docx, pptx, xlsx) are not supported in v1.

## Setup

Run once: `python scripts/docread.py setup` from the skill folder. It creates a venv under `%LOCALAPPDATA%\doc-reader\venv` (or `~/.local/share/doc-reader` on other systems) and installs pymupdf4llm and pdfplumber. All later commands start from `python scripts/docread.py` and re-run themselves inside that venv.

## Rules for Claude

1. Run `convert FILE` first, then `map FILE`. The first convert of a long document is slow: a 234-page report took 2 to 3 minutes, and a scanned document takes longer. Run it in the background, or with a shell timeout of at least 10 minutes, because a killed convert caches nothing. It prints a "still converting" line every 30 seconds. Later calls use the cache and return at once. Every command other than `convert` also converts on first use.
2. Read the map before anything else. Never open the cached Markdown file directly.
3. A document under about 5,000 tokens is marked small. For those, run `read FILE --all` and skip the map.
4. For a question about one topic, run `read FILE --section TEXT`. If the answer says the match is ambiguous, pick one title from the list and run again.
5. For a fact, number, or term, run `grep FILE TEXT`. Hits are cited as `p<PDF page>`. Then read the section or the page range around the hit.
6. Use `read FILE --pages A-B` when you know the pages. Page numbers are PDF pages. The printed page number can differ (the map says when it does).
7. Do not run `read FILE --all --yes` on a large document unless the whole text is truly needed. The command refuses without `--yes` on purpose.
8. If a table or figure looks wrong in the text, or the convert output has a warning for that page, run `page-image FILE N` and open the PNG path it prints. This costs fewer tokens than reading the whole PDF natively.
9. Say which pages an answer came from. Quote numbers exactly as printed. The map ends with the list of flagged pages, and `read` and `grep` print the warnings for the pages they return. Check a flagged page with `page-image` before relying on a number from its table.
10. Do not ask the user to install Docling. It installs itself when a scanned page is found, and prints progress.

## Commands

See references/commands.md for flags and output formats. In short: `convert`, `map`, `read` (with `--section`, `--pages`, `--all`), `grep`, `page-image`, `setup`.

## Limits to state when relevant

- Token counts are characters divided by four. They under-count Telugu and other non-Latin scripts.
- Tables are kept as Markdown only when the detected table looks like data. Otherwise the page keeps raw text and carries a warning.
- Multi-column and designed layouts (policy briefs, posters) can interleave lines. Check the page image when a passage reads oddly.
- Figures are not extracted. The map lists figure and table captions with page numbers. Use `page-image` to look at one.
- Headings come from PDF bookmarks, then from the extractor, then from numbering patterns, then from 5-page windows. A map built from windows means the document had no usable structure.
