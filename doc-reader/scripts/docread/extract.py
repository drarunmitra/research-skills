"""Page-wise text extraction (pymupdf4llm, pdfplumber fallback)."""
import contextlib
import io
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


def accept_table(bbox, page_size, cells) -> bool:
    """True when a detected table looks like data: not page-wide, mostly filled."""
    x0, top, x1, bottom = bbox
    w, h = page_size
    if (x1 - x0) * (bottom - top) >= MAX_TABLE_AREA * w * h:
        return False
    flat = [c for row in cells for c in row]
    if not flat:
        return False
    filled = sum(1 for c in flat if c and str(c).strip())
    return filled / len(flat) >= MIN_FILLED


def apply_table_rule(pdf: Path, pages: list["PageText"]) -> None:
    """Pages whose Markdown tables fail the check fall back to raw text plus a warning."""
    import pdfplumber

    with pdfplumber.open(pdf) as doc:
        for p in pages:
            if p.tables_md == 0:
                continue
            pg = doc.pages[p.page - 1]
            size = (float(pg.width), float(pg.height))
            bad = False
            for t in pg.find_tables():
                if not accept_table(t.bbox, size, t.extract()):
                    bad = True
                    break
            if bad:
                p.text = pg.extract_text() or ""
                p.tables_md = 0
                p.warnings.append(f"p{p.page}: table layout not reliable, raw text kept")


def _with_pymupdf4llm(path: Path) -> list[PageText]:
    doc = pymupdf.open(path)
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        chunks = pymupdf4llm.to_markdown(
            doc, page_chunks=True, ignore_images=True, show_progress=False
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
    return pages
