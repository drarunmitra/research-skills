# doc-reader Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `doc-reader` Claude skill: convert PDFs once, cache them, and let Claude read a map, one section, a page range, or keyword hits instead of the whole file.

**Architecture:** One CLI (`scripts/docread.py`) over small modules in `scripts/docread/`. A private venv holds PyMuPDF4LLM (pdfplumber fallback). Docling is installed only when a scan is first seen. Full text goes to a disk cache; every command prints short output.

**Tech Stack:** Python 3.11, pymupdf4llm, pdfplumber, pytest, Docling (opt-in, CPU torch).

**Spec:** `docs/superpowers/specs/2026-11-17-doc-reader-skill-design.md` (section "Revised v1 scope" governs where it conflicts with earlier sections).

## Global Constraints

- Skill folder: `C:\Users\Arun\code\research-skills\doc-reader\`. Symlink into `~/.claude/skills` only after Task 7 passes.
- Windows 11, Python 3.11 (miniconda). Venv at `%LOCALAPPDATA%\doc-reader\venv`; call `venv\Scripts\python.exe` explicitly. Cache at `%LOCALAPPDATA%\doc-reader\cache\<sha256>\`. Env var `DOCREAD_HOME` overrides the root (tests use it).
- `import fitz` fails in the miniconda env. Never use the system Python for extraction; always the venv.
- UTF-8 everywhere: `sys.stdout.reconfigure(encoding="utf-8")`, `open(..., encoding="utf-8")`.
- Token estimate = `len(text) // 4`. Size gate: under 5,000 tokens, no map, read whole.
- Cache key = SHA-256 of file bytes. Page markers in `doc.md`: `<!-- page N -->` (PDF page), with `<!-- page N label L -->` when the printed label differs.
- Headers/footers are stripped only for documents of 10 or more pages.
- No em dashes or bold in SKILL.md prose (house style). Frontmatter: `name`, `description`, `version`, `allowed-tools`. Add "Pairs with" and "Platform compatibility" blocks per CONTRIBUTING.md.
- Test PDFs in `doc-reader-fixtures/dl/` are never committed. Add `doc-reader-fixtures/` to `.gitignore` in Task 0.
- Public repo: do not vendor PyMuPDF (AGPL). The skill only pip-installs it for the user.
- Out of v1: MarkItDown, Office files, `pages.json`, table and figure sidecar files, `upgrade`, `clean`.

## Review Focus

1. Password-protected or corrupt PDF: print one clear line and exit code 2, no traceback.
2. Non-PDF input (docx, xlsx): print "Office files are not supported in v1" and exit 2.
3. Telugu or symbol text (U+25CF): no `UnicodeEncodeError` on a cp1252 console.
4. Page range outside the document, or `grep` with no hits or regex characters in the query: short message, no crash.
5. Cover page with under 100 characters: never triggers the Docling install.

Each line above has its test in the task that owns the code (noted in the task).

---

### Task 0: Scaffold, venv bootstrap, test fixtures

**Files:**
- Create: `doc-reader/scripts/docread.py`, `doc-reader/scripts/docread/__init__.py`, `doc-reader/scripts/docread/env.py`, `doc-reader/tests/conftest.py`, `doc-reader/tests/test_env.py`
- Modify: `.gitignore`

**Interfaces:**
- Produces: `env.home() -> Path` (honours `DOCREAD_HOME`), `env.venv_python() -> Path`, `env.setup() -> None` (creates venv, installs `pymupdf4llm pdfplumber pytest`), `docread.py setup` subcommand. `conftest.py` provides fixtures `make_pdf(pages: list[str], path) -> Path` (builds a text PDF with PyMuPDF), `sample(name) -> Path` (skips the test if the sample file is missing).

- [ ] **Step 1: Write failing test** `test_home_honours_env`: with `DOCREAD_HOME=tmp`, `env.home() == Path(tmp)`; `test_venv_python_is_scripts_exe`: path ends with `venv/Scripts/python.exe`.
- [ ] **Step 2: Run** `python -m pytest doc-reader/tests/test_env.py -v`. Expected: FAIL (module missing).
- [ ] **Step 3: Implement** `env.py`; `setup()` uses `python -m venv` then `venv\Scripts\python.exe -m pip install pymupdf4llm pdfplumber pytest`, printing one line per step. Add `doc-reader-fixtures/` to `.gitignore`.
- [ ] **Step 4: Run `python doc-reader/scripts/docread.py setup`**, then `venv\Scripts\python.exe -c "import pymupdf4llm, pdfplumber"`. Expected: exit 0. Then rerun the tests inside the venv: PASS.
- [ ] **Step 5: Commit** `feat(doc-reader): scaffold and venv bootstrap`.

### Task 1: Extract, clean, cache (`convert`)

**Files:**
- Create: `scripts/docread/cache.py`, `extract.py`, `clean.py`, `convert.py`; `tests/test_convert.py`

**Interfaces:**
- Consumes: Task 0 `env.home`, fixtures.
- Produces:
  - `cache.file_hash(path: Path) -> str`; `cache.entry_dir(sha: str) -> Path`
  - `extract.PageText` dataclass `(page: int, text: str, label: str | None, tables_md: int, warnings: list[str])`
  - `extract.extract_pages(pdf: Path) -> list[PageText]` (pymupdf4llm per page; pdfplumber if it raises; raises `DocError` for password or corrupt files)
  - `clean.strip_running(pages: list[PageText]) -> list[PageText]` (no-op under 10 pages; removes lines repeating on at least 40% of pages after replacing digits with `#`)
  - `clean.page_labels(pages) -> dict[int, str]` (printed number found in footer or header lines, else none)
  - `convert.convert(path: Path, force: bool = False) -> dict` writes `doc.md` and `meta.json` `{sha, name, pages, tokens, small, engine, warnings, labels}`; returns meta. `DocError(Exception)` lives in `extract.py`.
- CLI: `docread.py convert FILE` prints one line: `<name>: <pages> pages, ~<tokens> tokens, <small|mapped>, cache <sha[:8]>`.

- [ ] **Step 1: Failing tests:** `test_convert_writes_cache_and_marks_pages` (3-page synthetic PDF: `doc.md` has `<!-- page 1 -->` and `<!-- page 3 -->`; meta pages == 3); `test_second_convert_hits_cache` (second call does not call `extract_pages`, use monkeypatch counter); `test_strip_running_removes_header_footer_on_12_page_pdf` (header "Guidelines India-2026" and footer "# | Page" gone, body kept); `test_short_doc_keeps_headers`; `test_password_pdf_raises_docerror`; `test_non_pdf_raises_docerror_with_office_message`; `test_cli_prints_utf8_on_cp1252_console` (page text with U+25CF and Telugu, run via subprocess with `PYTHONIOENCODING=cp1252`, exit 0).
- [ ] **Step 2: Run** `venv\Scripts\python.exe -m pytest doc-reader/tests/test_convert.py -v`. Expected: FAIL.
- [ ] **Step 3: Implement** the modules above. Cache writes are atomic (write temp, rename). Unwritable cache dir: `DocError("cache dir not writable: <path>")`.
- [ ] **Step 4: Run tests.** Expected: PASS. Then `docread.py convert doc-reader-fixtures/dl/KIHT_HEOR.pdf`; expected one line, about 100k tokens, header and footer absent from `doc.md` (grep count 0 for "Page" footer pattern).
- [ ] **Step 5: Commit** `feat(doc-reader): convert with cache, header/footer strip`.

### Task 2: Tables rule

**Files:**
- Modify: `scripts/docread/extract.py`; Create: `tests/test_tables.py`

**Interfaces:**
- Produces: `extract.accept_table(bbox: tuple, page_size: tuple, cells: list[list[str | None]]) -> bool` True only when bbox area is under 80% of page area and at least 60% of cells are non-empty. Accepted tables render as Markdown inside page text; rejected ones leave raw text and add warning `"p<N>: table layout not reliable, raw text kept"`.

- [ ] **Step 1: Failing tests:** `test_full_page_grid_rejected` (bbox 95% of page: False); `test_small_filled_table_accepted`; `test_sparse_table_rejected` (30% filled). Plus `test_hemoglobinometer_p1_warns` (sample file; the 7-column page-wide grid yields a warning and no Markdown table from it).
- [ ] **Step 2: Run, expect FAIL.** **Step 3: Implement** using pdfplumber `find_tables()` boxes mapped onto the page. **Step 4: Run, expect PASS.** **Step 5: Commit** `feat(doc-reader): conservative table rule`.

### Task 3: Map and size gate (`map`)

**Files:**
- Create: `scripts/docread/outline.py`, `tests/test_outline.py`

**Interfaces:**
- Consumes: Task 1 `meta.json`, `doc.md`.
- Produces: `outline.Entry` dataclass `(level: int, title: str, page: int, end_page: int, tokens: int)`; `outline.build_map(sha: str) -> list[Entry]` (order: PDF bookmarks, else heading lines from pymupdf4llm `#` markers plus regex `^(Chapter|Section|\d+(\.\d+)*)\s+\S` and ALL CAPS lines under 80 chars, else 5-page windows titled `pages A-B`); `outline.render_map(entries, meta) -> str` (also lists `Figure N`/`Table N` captions with page numbers, and pages with warnings). `docread.py map FILE` prints the map; for `small` documents prints `small document (~N tokens): read whole with: docread.py read FILE --all`.
- Map output budget: at most 2,000 tokens; deeper levels are collapsed when over budget.

- [ ] **Step 1: Failing tests:** `test_bookmarks_used_first` (synthetic PDF with `set_toc`); `test_regex_fallback_finds_numbered_headings`; `test_window_fallback_when_no_headings` (12 pages, expect entries `pages 1-5`, `6-10`, `11-12`); `test_small_doc_gate`; `test_map_under_2000_tokens_for_kiht` (sample); `test_captions_listed`.
- [ ] **Step 2: Run, expect FAIL.** **Step 3: Implement.** **Step 4: Run; PASS.** On KIHT also print the map and eyeball that chapter titles appear. **Step 5: Commit** `feat(doc-reader): outline map with size gate`.

### Task 4: Read, grep, page image

**Files:**
- Create: `scripts/docread/readcmd.py`, `tests/test_readcmd.py`

**Interfaces:**
- Consumes: Task 3 `build_map`.
- Produces: `read_section(sha, query: str) -> str` (case-insensitive substring match on map titles; ambiguous match returns the list of candidates, max 5); `read_pages(sha, a: int, b: int) -> str` (inclusive; clamps nothing, raises `DocError("pages out of range 1-N")`); `read_all(sha) -> str`; `grep(sha, pattern: str, context: int = 1, max_hits: int = 20) -> str` (pattern is a literal string, not a regex; each hit `p<N>: <line>`); `page_image(pdf: Path, page: int, out: Path | None = None) -> Path` (150 dpi PNG in the cache dir). CLI: `read FILE [--section Q | --pages A-B | --all]`, `grep FILE TEXT`, `page-image FILE N` (prints the PNG path only).

- [ ] **Step 1: Failing tests:** `test_read_pages_inclusive`; `test_read_pages_out_of_range_message`; `test_grep_literal_special_chars` (query `(p<0.05)` finds the line); `test_grep_no_hits_message` (`no hits for 'x'`); `test_read_section_ambiguous_lists_candidates`; `test_page_image_writes_png`.
- [ ] **Step 2: Run, expect FAIL.** **Step 3: Implement.** **Step 4: Run; PASS.** **Step 5: Commit** `feat(doc-reader): read, grep, page-image`.

### Task 5: Docling escalation for scans and bad tables

**Files:**
- Create: `scripts/docread/escalate.py`, `tests/test_escalate.py`; Modify: `convert.py`

**Interfaces:**
- Produces: `escalate.scan_pages(pages: list[PageText]) -> list[int]` (pages under 100 characters of text that also hold images, excluding page 1 and the last page unless more than half of all pages qualify); `escalate.ensure_docling() -> None` (pip installs `docling` with the CPU torch index into the venv, one progress line per 10 seconds, prints expected size about 2 GB first); `escalate.ocr_pages(pdf: Path, pages: list[int]) -> dict[int, str]`. `convert()` calls these only when `scan_pages` is non-empty or `--docling` is passed; replaced pages get `<!-- page N ocr -->` marker.

- [ ] **Step 1: Failing tests:** `test_cover_page_not_scan` (page 1 with 58 chars and an image: `[]`); `test_image_only_pages_detected` (synthetic 6-page PDF, pages 3-4 image-only: `[3, 4]`); `test_all_image_pdf_flags_all_pages`; `test_ocr_pages_returns_text` (slow, marked `@pytest.mark.slow`, uses a rendered image-only copy of `hta_cervical_policy.pdf` page 1; asserts a known phrase from that page appears).
- [ ] **Step 2: Run non-slow tests, expect FAIL.** **Step 3: Implement.** **Step 4: Run non-slow tests; PASS. Then run the slow test once** (installs Docling; expect a long first run with progress lines; expect PASS). **Step 5: Commit** `feat(doc-reader): docling escalation for scans`.

### Task 6: SKILL.md, references, conventions

**Files:**
- Create: `doc-reader/SKILL.md`, `doc-reader/references/commands.md`
- Modify: `README.md` and any skills index the repo keeps (follow how `learn-from-video` is listed; check `docs/index.html`).

**Interfaces:** SKILL.md rules for Claude, in this order: run `convert` then `map`; never read `doc.md` directly; small documents are read whole; read sections, not the file; use `grep` for facts; use `page-image` only when a table or figure is unreadable; never ask for Docling unless `map` warns about scans. Include a Setup section (`python scripts/docread.py setup`) and the Telugu and non-Latin token warning.

- [ ] **Step 1:** Write SKILL.md and commands.md following CONTRIBUTING.md and the structure of `learn-from-video`.
- [ ] **Step 2:** Check: `grep -c "—" doc-reader/SKILL.md` returns 0.
- [ ] **Step 3: Commit** `docs(doc-reader): SKILL.md and command reference`.

### Task 7: Acceptance run on the real files

**Files:** Create `doc-reader/tests/acceptance.md` (results table, committed; no PDF content copied).

- [ ] **Step 1:** For each of the four fixtures run `convert` and `map`; record pages, tokens, map tokens.
- [ ] **Step 2:** KIHT_HEOR one-topic question (pick a chapter, e.g. discounting): measure tokens of `map` plus `read --section`, divided by tokens of full text. Pass: at least 85% fewer.
- [ ] **Step 3:** Pick 5 tables across the fixtures. Compare each Markdown table with the PDF page (`page-image`) by eye. Pass: 5 of 5 match, or a rejected table says so in the warnings.
- [ ] **Step 4:** Three short briefs: `map` says small, `read --all` returns all text, no loss.
- [ ] **Step 5:** Scan test from Task 5 passes. Record in `acceptance.md`.
- [ ] **Step 6:** Symlink `doc-reader` into `~/.claude/skills`, then run one real session question end to end. Commit `test(doc-reader): acceptance results`.
