"""convert: extract once, clean, cache doc.md + meta.json."""
import contextlib
import json
import os
import shutil
import sys
import threading
import time
from pathlib import Path

from . import cache, clean, escalate, extract
from .extract import DocError

VERSION = 4  # 4: table rows are never stripped as running text
SMALL_TOKENS = 5000
HEARTBEAT_SECONDS = 30


def tokens(text: str) -> int:
    return len(text) // 4


def render_doc(pages, labels: dict[int, str]) -> str:
    parts = []
    for p in pages:
        lab = labels.get(p.page)
        marker = f"<!-- page {p.page}" + (f" label {lab}" if lab else "") + (" ocr" if p.ocr else "") + " -->"
        parts.append(f"{marker}\n{p.text}\n")
    return "\n".join(parts)


@contextlib.contextmanager
def _heartbeat(name: str):
    """Print a line every HEARTBEAT_SECONDS so a long convert is not silent."""
    out, t0, stop = sys.stdout, time.time(), threading.Event()

    def run():
        while not stop.wait(HEARTBEAT_SECONDS):
            print(f"still converting {name} ({int(time.time() - t0)} s)", file=out, flush=True)

    th = threading.Thread(target=run, daemon=True)
    th.start()
    try:
        yield
    finally:
        stop.set()


def _escalate(path: Path, pages, docling: bool) -> bool:
    """OCR scan pages (and table-warning pages when docling=True) with Docling.
    Returns True when the escalation failed."""
    scans = escalate.scan_pages(pages)
    targets = sorted(set(scans) | ({p.page for p in pages if p.warnings} if docling else set()))
    if not targets:
        return False
    try:
        if scans:
            print(f"{len(scans)} scan page(s) found; using Docling OCR", flush=True)
        escalate.ensure_docling()
        texts = escalate.ocr_pages(path, targets)
    except Exception as e:
        for n in targets:
            pages[n - 1].warnings.append(f"p{n}: OCR failed ({e}), page text may be empty")
        return True
    for n, t in texts.items():
        pg = pages[n - 1]
        pg.text, pg.ocr, pg.warnings = t, True, []
    return False


def _usable(meta: dict | None) -> bool:
    return bool(meta) and meta.get("v") == VERSION and not meta.get("incomplete")


def convert(path: Path, force: bool = False, docling: bool = False) -> dict:
    path = Path(path)
    extract.check_input(path)
    sha = cache.file_hash(path)
    meta = cache.load_meta(sha)
    if _usable(meta) and not force:
        return meta
    with _heartbeat(path.name):
        pages = extract.extract_pages(path)
        failed = _escalate(path, pages, docling)
    labels = clean.page_labels(pages)
    pages = clean.strip_running(pages)
    doc = render_doc(pages, labels)
    n_tok = tokens(doc)
    warnings = [w for p in pages for w in p.warnings]
    if extract.ENGINE["name"] != "pymupdf4llm":
        warnings.append(f"engine: {extract.ENGINE['name']} fallback used, headings and tables are poor")
    meta = {
        "v": VERSION, "sha": sha, "name": path.name, "pages": len(pages),
        "tokens": n_tok, "small": n_tok < SMALL_TOKENS,
        "engine": extract.ENGINE["name"], "incomplete": failed,
        "stripped_lines": sum(p.stripped for p in pages),
        "warnings": warnings,
        "labels": {str(k): v for k, v in labels.items()},
        "toc": extract.read_toc(path),
    }
    final = cache.entry_dir(sha)
    tmp = final.with_name(f"{final.name}.tmp{os.getpid()}_{threading.get_ident()}")
    try:
        tmp.mkdir(parents=True)
        (tmp / "doc.md").write_text(doc, encoding="utf-8")
        (tmp / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        other = cache.load_meta(sha)
        if _usable(other) and not force:  # another process finished first: keep its entry
            return other
        if final.exists():
            for png in final.glob("page-*.png"):
                shutil.copy2(png, tmp / png.name)
            shutil.rmtree(final, ignore_errors=True)
        try:
            os.replace(tmp, final)
        except OSError:
            other = cache.load_meta(sha)
            if _usable(other):
                return other
            raise
    except OSError:
        raise DocError(f"cache dir not writable: {final.parent}") from None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return meta
