"""Header/footer stripping and printed page labels."""
import re

from .extract import PageText

MIN_PAGES = 10
ZONE = 3  # lines inspected at the top and bottom of each page
REPEAT_SHARE = 0.4
_LABEL = [
    re.compile(r"^(\d{1,4})\s*\|\s*page$", re.I),
    re.compile(r"^page\s*(\d{1,4})(?:\s*of\s*\d+)?$", re.I),
    re.compile(r"^(\d{1,4})$"),
]


def _plain(line: str) -> str:
    """Drop markdown decoration (bold, headings, list bullets) from a line."""
    s = re.sub(r"[*_#>`]", "", line).strip()
    return re.sub(r"^[-+]\s+", "", s)


def _norm(line: str) -> str:
    return re.sub(r"\d+", "#", _plain(line))


def _zone_indexes(lines: list[str]) -> list[int]:
    idx = [i for i, ln in enumerate(lines) if ln.strip()]
    return sorted(set(idx[:ZONE] + idx[-ZONE:]))


def strip_running(pages: list[PageText]) -> list[PageText]:
    if len(pages) < MIN_PAGES:
        return pages
    counts: dict[str, int] = {}
    for p in pages:
        lines = p.text.splitlines()
        for n in {_norm(lines[i]) for i in _zone_indexes(lines)}:
            counts[n] = counts.get(n, 0) + 1
    running = {n for n, c in counts.items() if n and c / len(pages) >= REPEAT_SHARE}
    for p in pages:
        lines = p.text.splitlines()
        zone = set(_zone_indexes(lines))
        keep = [ln for i, ln in enumerate(lines) if not (i in zone and _norm(ln) in running)]
        p.text = "\n".join(keep).strip("\n")
    return pages


def page_labels(pages: list[PageText]) -> dict[int, str]:
    """Printed page numbers that differ from the PDF page number."""
    out: dict[int, str] = {}
    for p in pages:
        lines = p.text.splitlines()
        found = None
        for i in _zone_indexes(lines):
            s = _plain(lines[i])
            for rx in _LABEL:
                m = rx.match(s)
                if m:
                    found = m.group(1)
                    break
            if found:
                break
        if found and found != str(p.page):
            out[p.page] = found
    return out
