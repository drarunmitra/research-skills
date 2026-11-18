"""Targeted reading: a section, a page range, keyword hits, or one page as an image."""
import re
from pathlib import Path

from . import cache, outline
from .extract import DocError, pymupdf


def _pages_text(sha: str, a: int, b: int, n_pages: int) -> str:
    if a < 1 or b > n_pages or a > b:
        raise DocError(f"pages out of range 1-{n_pages}")
    lines, page_of, _ = outline._load(sha)
    return "\n".join(ln for ln, pg in zip(lines, page_of) if a <= pg <= b)


def read_pages(sha: str, a: int, b: int) -> str:
    meta = cache.load_meta(sha)
    return _pages_text(sha, a, b, meta["pages"])


def read_all(sha: str, meta: dict | None = None, yes: bool = False) -> str:
    meta = meta or cache.load_meta(sha)
    if not meta["small"] and not yes:
        raise DocError(
            f"document is ~{meta['tokens']} tokens; use --section, --pages or grep "
            "(add --yes only if the whole text is really needed)")
    return _pages_text(sha, 1, meta["pages"], meta["pages"])


def read_section(sha: str, query: str) -> str:
    entries = outline.build_map(sha)
    q = query.lower()
    hits = [e for e in entries if q in e.title.lower()]
    exact = [e for e in hits if e.title.lower() == q]
    if len(exact) == 1:
        hits = exact
    if not hits:
        return f"no section matches '{query}'. Run map to see the sections."
    if len(hits) > 1:
        shown = [f"- {e.title} (p{e.page})" for e in hits[:5]]
        more = f"\n...and {len(hits) - 5} more" if len(hits) > 5 else ""
        return f"ambiguous: '{query}' matches:\n" + "\n".join(shown) + more
    e = hits[0]
    lines, _, _ = outline._load(sha)
    return "\n".join(lines[e.start_line:e.end_line])


def grep(sha: str, pattern: str, context: int = 1, max_hits: int = 20) -> str:
    """Literal, case-insensitive search. Each hit is cited as p<PDF page>."""
    lines, page_of, _ = outline._load(sha)
    needle = pattern.lower()
    hits = [i for i, ln in enumerate(lines)
            if needle in ln.lower() and not outline._MARK.match(ln)]
    if not hits:
        return f"no hits for '{pattern}'"
    out = []
    for i in hits[:max_hits]:
        out.append(f"p{page_of[i]}: {lines[i].strip()[:200]}")
        for j in range(max(0, i - context), min(len(lines), i + context + 1)):
            if j != i and lines[j].strip() and not outline._MARK.match(lines[j]):
                out.append(f"    {lines[j].strip()[:120]}")
    if len(hits) > max_hits:
        out.append(f"...and {len(hits) - max_hits} more hits")
    return "\n".join(out)


def page_image(pdf: Path, page: int, out: Path | None = None) -> Path:
    """Render one page to PNG (150 dpi) for Claude to look at."""
    doc = pymupdf.open(pdf)
    if page < 1 or page > len(doc):
        raise DocError(f"pages out of range 1-{len(doc)}")
    if out is None:
        d = cache.entry_dir(cache.file_hash(pdf))
        d.mkdir(parents=True, exist_ok=True)
        out = d / f"page-{page}.png"
    doc[page - 1].get_pixmap(dpi=150).save(out)
    return Path(out)
