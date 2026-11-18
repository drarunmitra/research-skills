"""convert: extract once, clean, cache doc.md + meta.json."""
import json
import os
import shutil
from pathlib import Path

from . import cache, clean, escalate, extract
from .extract import DocError

VERSION = 3
SMALL_TOKENS = 5000


def tokens(text: str) -> int:
    return len(text) // 4


def render_doc(pages, labels: dict[int, str]) -> str:
    parts = []
    for p in pages:
        lab = labels.get(p.page)
        marker = f"<!-- page {p.page}" + (f" label {lab}" if lab else "") + (" ocr" if p.ocr else "") + " -->"
        parts.append(f"{marker}\n{p.text}\n")
    return "\n".join(parts)


def _escalate(path: Path, pages, docling: bool) -> None:
    """OCR scan pages (and table-warning pages when docling=True) with Docling."""
    scans = escalate.scan_pages(pages)
    targets = sorted(set(scans) | ({p.page for p in pages if p.warnings} if docling else set()))
    if not targets:
        return
    try:
        if scans:
            print(f"{len(scans)} scan page(s) found; using Docling OCR", flush=True)
        escalate.ensure_docling()
        texts = escalate.ocr_pages(path, targets)
    except Exception as e:
        for n in targets:
            pages[n - 1].warnings.append(f"p{n}: OCR failed ({e}), page text may be empty")
        return
    for n, t in texts.items():
        pg = pages[n - 1]
        pg.text, pg.ocr, pg.warnings = t, True, []


def convert(path: Path, force: bool = False, docling: bool = False) -> dict:
    path = Path(path)
    extract.check_input(path)
    sha = cache.file_hash(path)
    meta = cache.load_meta(sha)
    if meta and meta.get("v") == VERSION and not force:
        return meta
    pages = extract.extract_pages(path)
    _escalate(path, pages, docling)
    labels = clean.page_labels(pages)
    pages = clean.strip_running(pages)
    doc = render_doc(pages, labels)
    n_tok = tokens(doc)
    meta = {
        "v": VERSION, "sha": sha, "name": path.name, "pages": len(pages),
        "tokens": n_tok, "small": n_tok < SMALL_TOKENS,
        "engine": extract.ENGINE["name"],
        "warnings": [w for p in pages for w in p.warnings],
        "labels": {str(k): v for k, v in labels.items()},
        "toc": extract.read_toc(path),
    }
    final = cache.entry_dir(sha)
    tmp = final.with_name(final.name + ".tmp")
    try:
        shutil.rmtree(tmp, ignore_errors=True)
        tmp.mkdir(parents=True)
        (tmp / "doc.md").write_text(doc, encoding="utf-8")
        (tmp / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
        shutil.rmtree(final, ignore_errors=True)
        os.replace(tmp, final)
    except OSError:
        raise DocError(f"cache dir not writable: {final.parent}") from None
    return meta
