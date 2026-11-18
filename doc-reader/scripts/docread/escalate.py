"""Docling escalation: OCR for scanned pages, installed only when first needed."""
import contextlib
import importlib
import importlib.util
import io
import subprocess
import sys
import time

from . import env
from .extract import PageText

MIN_TEXT = 100
MIN_COVER = 0.5  # a scan is mostly picture; a divider or logo page is not
CPU_INDEX = "https://download.pytorch.org/whl/cpu"


def scan_pages(pages: list[PageText]) -> list[int]:
    """Pages with almost no text but an image. A cover page is not a scan."""
    cand = [p.page for p in pages
            if len(p.text.strip()) < MIN_TEXT and p.images > 0 and p.image_cover >= MIN_COVER]
    if len(cand) > len(pages) / 2:
        return cand
    last = pages[-1].page if pages else 0
    return [n for n in cand if n not in (1, last)]


def docling_installed() -> bool:
    return importlib.util.find_spec("docling") is not None


def ensure_docling() -> None:
    """pip install docling (CPU torch) into this venv, with a progress line every 10 s."""
    if docling_installed():
        return
    print("Installing Docling: about 2 GB, one time, several minutes.", flush=True)
    log = env.home() / "docling-install.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "pip", "install", "-q", "docling",
           "--extra-index-url", CPU_INDEX]
    start = time.time()
    with open(log, "w", encoding="utf-8") as fh:
        proc = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT)
        while True:
            try:
                proc.wait(timeout=10)
                break
            except subprocess.TimeoutExpired:
                print(f"  still installing Docling ({int(time.time() - start)} s)", flush=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Docling install failed, see {log}")
    importlib.invalidate_caches()
    print("Docling installed.", flush=True)


def ocr_pages(pdf, pages: list[int]) -> dict[int, str]:
    """Markdown text for each requested 1-based page, via Docling with OCR on."""
    sink = io.StringIO()
    with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.document_converter import DocumentConverter, PdfFormatOption

        opts = PdfPipelineOptions()
        opts.do_ocr = True
        conv = DocumentConverter(
            format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opts)})
        out = {}
        for n in pages:
            res = conv.convert(str(pdf), page_range=(n, n))
            out[n] = res.document.export_to_markdown()
    return out
