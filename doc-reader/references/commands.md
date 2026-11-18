# doc-reader commands

Run from the skill folder: `python scripts/docread.py <command>`. Exit code 0 means success, 2 means a problem with the input (one line, no traceback).

setup [--dev]
  Creates the private venv and installs pymupdf4llm and pdfplumber (minimum versions are set). Run once. --dev also installs pytest, for running the tests.

convert FILE [--force] [--docling]
  Extracts, cleans, and caches the document. Prints one line:
  `name.pdf: 234 pages, ~116085 tokens, mapped, cache a073ce5f`
  The word is "small" when the document is under 5,000 tokens.
  A line such as `16 warning(s); map lists the flagged pages` follows when pages are flagged. A "still converting" line prints every 30 seconds on long files. A scan or install failure is not cached, so the next call tries again.
  --force rebuilds the cache entry. --docling re-runs pages that carry table warnings through Docling (forces a rebuild).
  Scanned pages (little text, has an image; a cover page does not count) are read with Docling OCR automatically. The first time, Docling is installed and progress prints every 10 seconds.

map FILE
  Prints sections (page range, approximate tokens, title), then figure and table captions, then the flagged pages. At most about 2,000 tokens. Small documents get a one-line message instead.

read FILE --section TEXT
  Case-insensitive match on section titles. One match prints the section. Several matches print up to five candidates.

read FILE --pages A-B
  Prints PDF pages A to B inclusive. `--pages 7` prints one page. An out-of-range request prints the valid range.

read FILE --all [--yes]
  Prints the whole text. Refused for documents that are not small unless --yes is given.

grep FILE TEXT
  Literal, case-insensitive search (no regular expressions). Up to 20 hits, each `p<page>: <line>` with one line of context either side.

page-image FILE N
  Renders PDF page N to a 150 dpi PNG in the cache folder and prints its path.

Cache
  `%LOCALAPPDATA%\doc-reader\cache\<sha256 of the file>\` holds `doc.md` (page markers `<!-- page N -->`, with `label L` when the printed number differs and `ocr` for OCR pages) and `meta.json`. Set `DOCREAD_HOME` to move the whole folder. Delete a cache folder to force a rebuild.
