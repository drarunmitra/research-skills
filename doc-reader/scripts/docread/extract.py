"""Page-wise text extraction (pymupdf4llm, pdfplumber fallback)."""
import contextlib
import io
import re
from dataclasses import dataclass, field
from pathlib import Path

# pymupdf4llm prints banners ("RapidOCR is missing") on import and first use.
# They cost tokens when Claude reads the output, so every import and call is silenced.
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    try:
        import pymupdf
        import pymupdf4llm
    except ImportError:  # setup not run; docread.py reports it
        pymupdf = pymupdf4llm = None


class DocError(Exception):
    """A user-facing problem with the input file. Message is one line."""


@dataclass
class PageText:
    page: int
    text: str
    label: str | None = None
    tables_md: int = 0
    warnings: list[str] = field(default_factory=list)
    images: int = 0
    image_cover: float = 0.0  # share of the page covered by images, 0 to 1
    ocr: bool = False
    stripped: int = 0


OFFICE = {".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"}
ENGINE = {"name": "pymupdf4llm"}


def check_input(path: Path) -> None:
    if not path.exists():
        raise DocError(f"file not found: {path}")
    if path.suffix.lower() in OFFICE:
        raise DocError("Office files are not supported in v1")
    if path.suffix.lower() != ".pdf":
        raise DocError(f"unsupported file type: {path.suffix or '(none)'}")


def _count_md_tables(text: str) -> int:
    n, inside = 0, False
    for line in text.splitlines():
        is_row = line.lstrip().startswith("|") and line.rstrip().endswith("|")
        if is_row and not inside:
            n += 1
        inside = is_row
    return n


MAX_TABLE_AREA = 0.8
MIN_FILLED = 0.6


def table_fits_page(bbox, page_size) -> bool:
    """False when the table box covers most of the page (a layout grid, not data)."""
    x0, top, x1, bottom = bbox
    w, h = page_size
    return (x1 - x0) * (bottom - top) < MAX_TABLE_AREA * w * h


def table_filled(cells) -> bool:
    """True when at least MIN_FILLED of the cells hold text."""
    flat = [c for row in cells for c in row]
    if not flat:
        return False
    return sum(1 for c in flat if c and str(c).strip()) / len(flat) >= MIN_FILLED


def accept_table(bbox, page_size, cells) -> bool:
    """True when a detected table looks like data: not page-wide, mostly filled."""
    return table_fits_page(bbox, page_size) and table_filled(cells)


_SEP = re.compile(r"^\|[\s:|-]+\|$")


def md_table_row_counts(text: str) -> list[int]:
    """Rows (header included, separator excluded) of each Markdown table in the text."""
    counts, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cur = 0 if cur is None else cur
            if not _SEP.match(s):
                cur += 1
        elif cur is not None:
            counts.append(cur)
            cur = None
    if cur is not None:
        counts.append(cur)
    return counts


def md_table_cells(text: str) -> list[list[list[str]]]:
    """Cells of every row of every Markdown table (separator rows dropped)."""
    tables, cur = [], None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            if cur is None:
                cur = []
            if not _SEP.match(s):
                cur.append([c.strip() for c in s.strip("|").split("|")])
        elif cur is not None:
            tables.append(cur)
            cur = None
    if cur is not None:
        tables.append(cur)
    return tables


def apply_table_rule(pdf: Path, pages: list["PageText"]) -> None:
    """Judge the Markdown tables the extractor emitted.

    Raw text replaces a page when a table box covers most of the page (a layout grid)
    or when a Markdown table is mostly empty. A table with more Markdown rows than the
    PDF grid is kept but flagged, because wrapped cells were probably split across rows.
    pdfplumber cell text is not trusted: it reads many real cells as empty.
    """
    import pdfplumber

    with pdfplumber.open(pdf) as doc:
        for p in pages:
            if p.tables_md == 0:
                continue
            pg = doc.pages[p.page - 1]
            size = (float(pg.width), float(pg.height))
            grids = pg.find_tables()
            too_big = any(not table_fits_page(t.bbox, size) for t in grids)
            md = md_table_cells(p.text)
            sparse = any(not table_filled([r for r in tbl]) for tbl in md)
            if too_big or sparse:
                p.text = pg.extract_text() or ""
                p.tables_md = 0
                p.warnings.append(f"p{p.page}: table layout not reliable, raw text kept")
            elif len(md) == len(grids) and any(len(m) > len(g.rows) for m, g in zip(md, grids)):
                p.warnings.append(
                    f"p{p.page}: table rows may be split across lines, check page-image")


def _with_pymupdf4llm(path: Path) -> list[PageText]:
    doc = pymupdf.open(path)
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        chunks = pymupdf4llm.to_markdown(
            doc, page_chunks=True, ignore_images=True, show_progress=False,
            use_ocr=False,  # one OCR owner: Docling escalation, same result on every machine
        )
    return [
        PageText(i + 1, c["text"], None, _count_md_tables(c["text"]))
        for i, c in enumerate(chunks)
    ]


def _with_pdfplumber(path: Path) -> list[PageText]:
    import pdfplumber

    with pdfplumber.open(path) as pdf:
        return [PageText(i + 1, p.extract_text() or "") for i, p in enumerate(pdf.pages)]


def read_toc(pdf: Path) -> list[list]:
    """PDF bookmarks as [level, title, page]; empty when the PDF has none."""
    try:
        return [[lv, str(t), pg] for lv, t, pg in pymupdf.open(pdf).get_toc() if pg >= 1]
    except Exception:
        return []


def extract_pages(pdf: Path) -> list[PageText]:
    check_input(pdf)
    try:
        probe = pymupdf.open(pdf)
    except Exception as e:  # corrupt file
        raise DocError(f"cannot open PDF: {e}") from None
    if probe.needs_pass:
        raise DocError("PDF is password protected")
    probe.close()
    try:
        pages = _with_pymupdf4llm(pdf)
        ENGINE["name"] = "pymupdf4llm"
    except Exception:
        try:
            pages = _with_pdfplumber(pdf)
            ENGINE["name"] = "pdfplumber"
        except Exception as e:
            raise DocError(f"cannot read PDF: {e}") from None
    if not pages:
        raise DocError("PDF has no pages")
    try:
        apply_table_rule(pdf, pages)
    except Exception:
        pass  # table check is advisory; never block extraction
    try:
        doc = pymupdf.open(pdf)
        for p in pages:
            pg = doc[p.page - 1]
            p.images = len(pg.get_images())
            area = pg.rect.get_area() or 1.0
            covered = sum((pymupdf.Rect(i["bbox"]) & pg.rect).get_area() for i in pg.get_image_info())
            p.image_cover = min(1.0, covered / area)
    except Exception:
        pass  # image counts only feed scan detection
    return pages
