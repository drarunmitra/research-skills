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


def _is_table_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def _key(line: str) -> str:
    """Comparison key. Digits are ignored only on page-number lines; any other
    line must repeat exactly, so rows that differ only by their numbers survive."""
    s = _plain(line)
    if any(rx.match(s) for rx in _LABEL):
        return re.sub(r"\d+", "#", s)
    return s


def _zone_indexes(lines: list[str]) -> list[int]:
    idx = [i for i, ln in enumerate(lines) if ln.strip()]
    return sorted(set(idx[:ZONE] + idx[-ZONE:]))


def _candidates(lines: list[str]) -> list[int]:
    """Zone lines that may be running text. Table rows are never candidates."""
    return [i for i in _zone_indexes(lines) if not _is_table_row(lines[i])]


def strip_running(pages: list[PageText]) -> list[PageText]:
    if len(pages) < MIN_PAGES:
        return pages
    counts: dict[str, int] = {}
    for p in pages:
        lines = p.text.splitlines()
        for k in {_key(lines[i]) for i in _candidates(lines)}:
            counts[k] = counts.get(k, 0) + 1
    running = {k for k, c in counts.items() if k and c / len(pages) >= REPEAT_SHARE}
    for p in pages:
        lines = p.text.splitlines()
        drop = {i for i in _candidates(lines) if _key(lines[i]) in running}
        p.stripped = len(drop)
        p.text = "\n".join(ln for i, ln in enumerate(lines) if i not in drop).strip("\n")
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
