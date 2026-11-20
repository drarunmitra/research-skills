# doc-reader skill: design

Date: 2026-11-17. Status: draft for approval.

## Intent and why
Claude reads PDFs and other documents badly and expensively. Raw PDFs cost many tokens and lose table structure. Arun reads journal papers, government reports, and reference documents with figures and tables. He wants one skill that converts these once, keeps tables correct, and lets Claude read only what it needs. Goal: lowest token use with no loss of facts.

Key finding from comparing MarkItDown, Docling, LiteDoc, and pdf-to-markdown: all four only convert. None cut tokens after conversion. The savings come from a page map, section-by-section reading, and figures kept as files.

## Goals
- Convert PDF, DOCX, PPTX, XLSX, HTML to Markdown, locally.
- Cache each conversion. Convert a file once.
- Make a small "map" file first: headings with line ranges, table list, figure list with captions, page count, low-confidence pages.
- Let Claude read one section, one table, or a page range, not the whole file.
- Keep tables as Markdown tables. Keep figures as image files with the caption in text.
- Flag pages the tool doubts (little text, garbled text, scan).

## Non-goals
- No cloud services. No uploads.
- No audio, video, or YouTube.
- No GUI or browser tool.
- No full OCR training or model tuning.

## Anti-goals (failure even if it works)
- Claude reads the whole converted file by default.
- Wrong table numbers with no warning.
- A heavy install that blocks first use.
- Figure images pulled into context without a request.

## Constraints
- Windows 11, Python 3.11 (miniconda), 52 GB free disk. PyMuPDF 1.23.3 and pdfplumber already installed.
- Skill lives in `C:\Users\Arun\code\research-skills\doc-reader\`, symlinked into `~/.claude/skills` (public repo pattern).
- Docling and MarkItDown are optional installs. The skill must work with PyMuPDF alone.
- Scripts must print short output (token cost).

## Approaches considered
- **A (chosen):** new skill. PyMuPDF first pass, Docling only on hard pages, MarkItDown for Office/HTML, cache, map, targeted reads. Most work, most savings.
- **B:** extend aliceisjustplaying/claude-skill-pdf-to-markdown. Faster, but PDF only, stale (Nov 2025), one-person dependency.
- **C:** install Docling alone. Heavy, no token controls. Dropped.

## Design (decided)
Pipeline, in order:
1. `convert` : file in, cache out. Cache key = file hash + tool version. Cache dir `~/.cache/doc-reader/<hash>/`.
2. Router: PDF uses PyMuPDF4LLM. Pages flagged hard (tables with merged cells, scans, low text) are re-run with Docling if installed, else flagged. DOCX/PPTX/XLSX/HTML use MarkItDown.
3. Outputs per document: `doc.md`, `map.md`, `figures/` (PNG + caption sidecar), `tables/` (one Markdown file each), `pages.json` (confidence per page).
4. `read` : prints one section by heading, one table by id, or a page range.
5. SKILL.md tells Claude: always read `map.md` first; never open `doc.md` whole unless under a small size limit; open figure images only when the caption is not enough.

## My calls (not yet confirmed by Arun)
- Name: `doc-reader`.
- Token limit for "small enough to read whole": 4,000 tokens (estimated by characters / 4).
- Hard-page rule: page has a table with no ruling lines, or under 100 characters of text with images (likely scan).
- Scanned pages without Docling or OCR: flag only, no OCR in v1.
- CLI is a single Python script with subcommands `convert`, `map`, `read`.

## Calls added after builder check (my calls, not yet confirmed)
- Table check: cheap generic check on every table. Flag the page if row column counts differ, the table crosses a page break, or table text is much shorter than raw page text. Flag only, no repair.
- `doc.md` has page markers (`<!-- page N -->`). `map.md` gives both line and page ranges. Re-running hard pages with Docling later (`doc-reader upgrade <file>`) rebuilds only flagged pages and the map.
- No headings found: map falls back to 5-page windows, so "never read whole" still works.
- Separate venv at `~/.cache/doc-reader/venv`. Installs pymupdf4llm there. The existing miniconda is not touched. Plain PyMuPDF text is the fallback if pymupdf4llm fails.
- Figures: save embedded images. For vector charts, render the page region above the "Figure N" caption to PNG. No caption: name it "Figure on page N".
- Cache key = SHA-256 of file contents. `doc-reader clean` removes old entries. No automatic cap.
- Token estimate = characters / 4. It under-counts Telugu and other non-Latin text. SKILL.md says so.
- XLSX: each sheet is one section in the map.
- Paths are cross-platform (pathlib), since the repo is public.

## Decided by Arun (2026-11-17)
- Scans: v1 includes OCR through Docling. First scan triggers a Docling install (about 2 GB) in the skill venv. This replaces the earlier "flag only" call and the "no OCR in v1" non-goal.
- Test files, in `C:\Users\Arun\code\research-skills\doc-reader-fixtures\dl\` (do NOT commit; add to .gitignore):
  - `KIHT_HEOR.pdf`: HEOR guidelines, 234 pages, long report with few tables.
  - `hta_cervical_policy.pdf`, `hta_hemoglobinometer_policy.pdf`, `hta_iol_policy.pdf`: HTAIn policy briefs, 2-3 pages each, many tables and images.
  - Source: htain.dhr.gov.in/completed-hta-studies.php. The "outcome report" links on that page returned 404, so I used the policy documents.
- No sample is a real scan. My call: make a test scan by rendering one page of a sample to an image-only PDF.
- Pass bar (my proposal, Arun did not object): 5 tables checked by eye match the original; Claude's reading cost drops at least 70% against reading the raw PDF text.
- Local note: `import fitz` fails on this machine (PyMuPDF 1.23.3 broken). Another reason for the separate venv.

## Review findings (2026-11-17: web search, red-team, token measurement)
Measured on the sample PDFs (chars/4 estimates, pdfplumber):
- KIHT_HEOR: 234 pages, about 113k tokens, no bookmarks, 3.5% running header/footer text, tables only about 7% of text. Heading levels cannot be told from font size alone (23 sizes; body 12.0 pt = 92% of chars).
- The three HTAIn briefs: 1.2k to 2.9k tokens each. A map saves nothing on them.
- Markdown tables cost 5-10% MORE tokens than plain tables. Their value is correct structure, not savings.
- Realistic savings: about 94% on a one-topic question in KIHT, 80-90% on multi-section questions. 0% on short briefs.
- Claude's native PDF reading costs about 2-4x more per page than clean Markdown (secondary sources; check the Read tool's `pages` option on this machine).
Web search:
- Docling: MIT, best table score on one vendor benchmark. Marker/MinerU: heavy, licence limits. olmOCR: needs NVIDIA GPU. All skipped.
- PyMuPDF/PyMuPDF4LLM is AGPL (matters for a public repo; the skill only pip-installs it for the user, it does not ship it). Importing pymupdf4llm silently changes table detection (known bug).
- Best token-saving practice seen elsewhere: outline first, 400-900 token section chunks, keyword search over chunks, write full text to disk and return a short summary, render one page as an image for a bad table or figure.
Red-team:
- A "no ruling lines" hard-page rule fires on nearly every designer-layout HTAIn page, so flags would carry no information.
- Figure captions can be on the next page; multi-panel figures break the "crop above caption" rule; many images are decoration.
- Multi-column text interleaves. A cover page with under 100 chars would trigger a 2 GB install.
- Windows: use `venv\Scripts\python.exe`; set UTF-8 output (cp1252 crashes on Telugu and symbols); `fitz` is broken here.
- Repo conventions: SKILL.md frontmatter (name, description, version, allowed-tools), "Pairs with" and "Platform compatibility" blocks, `scripts/` and `references/` folders. Add the fixtures folder to .gitignore before any commit.

## Revised v1 scope (proposed; replaces conflicting parts above once Arun approves)
Core (must have):
1. One script `scripts/docread.py` with subcommands `convert`, `map`, `read`, `grep`. Output is short. Full text goes to disk.
2. Size gate: under 5k tokens, no map, read whole.
3. Strip running headers and footers (repeat detection on documents of 10+ pages only). Add `<!-- page N -->` markers with both PDF page and printed page label where they differ.
4. Map: headings found by PDF bookmarks, else regex (Chapter, 1.2, ALL CAPS) plus bold/size. Each entry has pages and token count. Fallback: 5-page windows.
5. Read by heading, by page range, or `grep` keyword with page-cited hits.
6. Tables: Markdown only when the table box is under 80% of the page and most cells are filled. Otherwise keep raw text and say so. Warn rather than repair.
7. Figures: not extracted by default. The map lists "Figure N" captions with page numbers. `read --page-image N` renders one page to PNG for Claude to look at.
8. Cache by SHA-256 in `%LOCALAPPDATA%\doc-reader`. UTF-8 everywhere. Separate venv, `Scripts\python.exe`.
9. Engine: PyMuPDF4LLM in the venv for digital PDFs (pdfplumber fallback). Docling is an opt-in escalation, installed on first need.
Docling escalation (kept because Arun chose OCR in v1): scans and bad tables only. Scan test = rendered image-only PDF. Install uses CPU torch and prints progress. Triggered by low text per page on non-cover pages, never by a cover page.
Cut or deferred to v1.1: `pages.json` confidence file, table sidecar files, figure PNG sidecars, `upgrade`, `clean`, MarkItDown (Office files go to Docling escalation or v1.1).
Pass bar: 5 tables checked by eye; at least 85% fewer tokens on a one-topic question in KIHT_HEOR; short briefs read whole with no loss; scan test returns readable text.

## Left to the builder
Exact flag names, map file format details, test PDFs, how to detect a hard table, and the install notes in SKILL.md.
