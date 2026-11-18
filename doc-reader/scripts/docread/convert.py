"""convert: extract once, clean, cache doc.md + meta.json."""
import json
import os
import shutil
from pathlib import Path

from . import cache, clean, extract
from .extract import DocError

VERSION = 1
SMALL_TOKENS = 5000


def tokens(text: str) -> int:
    return len(text) // 4


def render_doc(pages, labels: dict[int, str]) -> str:
    parts = []
    for p in pages:
        lab = labels.get(p.page)
        marker = f"<!-- page {p.page} label {lab} -->" if lab else f"<!-- page {p.page} -->"
        parts.append(f"{marker}\n{p.text}\n")
    return "\n".join(parts)


def convert(path: Path, force: bool = False) -> dict:
    path = Path(path)
    extract.check_input(path)
    sha = cache.file_hash(path)
    meta = cache.load_meta(sha)
    if meta and meta.get("v") == VERSION and not force:
        return meta
    pages = extract.extract_pages(path)
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
