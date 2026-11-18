"""Document map: headings (bookmarks, markdown, regex, or page windows) plus captions."""
import re
from dataclasses import dataclass

from . import cache

MAP_BUDGET_TOKENS = 2000
WINDOW = 5
_MARK = re.compile(r"^<!-- page (\d+)(?: label (\S+))?(?: ocr)? -->$")
_MD_HEAD = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
_NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)[.)]?\s+[A-Z]\S")
_CHAPTER = re.compile(r"^(Chapter|Section|Part)\s+(\d+|[IVX]+)\b", re.I)
_CAPS = re.compile(r"^[A-Z][A-Z0-9 ,&:\-]{3,78}$")
_CAPTION = re.compile(r"^(Figure|Fig\.|Table|Box|Chart)\s*0*(\d+)\s*[:.\-–]\s*(.+)$", re.I)
_CAPTION_START = re.compile(r"^(Figure|Fig\.|Table|Box|Chart)\s*0*\d+", re.I)


@dataclass
class Entry:
    level: int
    title: str
    page: int
    end_page: int
    tokens: int
    start_line: int = 0
    end_line: int = 0


def _clean(s: str) -> str:
    s = re.sub(r"</?mark>", "", s)
    return re.sub(r"[*_#]", "", s).strip()


def _load(sha: str):
    d = cache.entry_dir(sha)
    lines = (d / "doc.md").read_text(encoding="utf-8").splitlines()
    page_of, cur = [], 1
    marks: dict[int, int] = {}
    for i, ln in enumerate(lines):
        m = _MARK.match(ln)
        if m:
            cur = int(m.group(1))
            marks[cur] = i
        page_of.append(cur)
    return lines, page_of, marks


def _depth(title: str) -> int | None:
    m = re.match(r"^(\d+(?:\.\d+)*)", title)
    return len(m.group(1).split(".")) if m else None


def _md_candidates(lines):
    out = []
    for i, ln in enumerate(lines):
        m = _MD_HEAD.match(ln)
        if not m:
            continue
        title = _clean(m.group(2))
        if not title or len(title) > 150 or _CAPTION_START.match(title):
            continue
        depth = _depth(title)
        level = depth if depth else (1 if len(m.group(1)) <= 2 else 2)
        out.append((i, level, title))
    return out


def _regex_candidates(lines):
    out = []
    for i, ln in enumerate(lines):
        s = _clean(ln)
        if not s or len(s) > 100 or _MARK.match(ln) or _CAPTION_START.match(s):
            continue
        if i > 0 and lines[i - 1].strip() and not _MARK.match(lines[i - 1]):
            continue  # headings stand alone after a blank line or page marker
        if _NUMBERED.match(s):
            out.append((i, _depth(s) or 1, s))
        elif _CHAPTER.match(s):
            out.append((i, 1, s))
        elif _CAPS.match(s) and sum(c.isalpha() for c in s) >= 4:
            out.append((i, 1, s))
    return out


def _toc_candidates(toc, lines, page_of, marks):
    out = []
    for lv, title, pg in toc:
        start = marks.get(pg, 0)
        for i in range(start, len(lines)):
            if page_of[i] != pg:
                break
            if title.lower() in lines[i].lower():
                start = i
                break
        out.append((start, lv, title))
    return out


def _window_candidates(meta, marks):
    n, out = meta["pages"], []
    for a in range(1, n + 1, WINDOW):
        b = min(a + WINDOW - 1, n)
        out.append((marks.get(a, 0), 1, f"pages {a}-{b}"))
    return out


def _to_entries(cands, lines, page_of):
    cands = sorted(cands, key=lambda c: c[0])
    entries = []
    for k, (start, level, title) in enumerate(cands):
        end = len(lines)
        for nxt in cands[k + 1:]:
            if nxt[1] <= level and nxt[0] > start:
                end = nxt[0]
                break
        body = "\n".join(lines[start:end])
        last = max(start, end - 1)
        entries.append(Entry(level, title, page_of[start], page_of[last],
                             len(body) // 4, start, end))
    return entries


def build_map(sha: str) -> list[Entry]:
    meta = cache.load_meta(sha)
    lines, page_of, marks = _load(sha)
    cands = _toc_candidates(meta.get("toc") or [], lines, page_of, marks)
    if not cands:
        cands = _md_candidates(lines)
    if len(cands) < 3:
        cands = _regex_candidates(lines) if len(_regex_candidates(lines)) >= 3 else cands
    if len(cands) < 3 and not meta.get("toc"):
        cands = _window_candidates(meta, marks)
    return _to_entries(cands, lines, page_of)


def _captions(sha: str, limit: int = 30) -> list[str]:
    lines, page_of, _ = _load(sha)
    seen, out = set(), []
    for i, ln in enumerate(lines):
        m = _CAPTION.match(_clean(ln))
        if not m:
            continue
        label = f"{m.group(1).title().rstrip('.')} {int(m.group(2))}"
        if label in seen:
            continue
        seen.add(label)
        out.append(f"{label} p{page_of[i]}: {m.group(3)[:70]}")
    more = len(out) - limit
    out = out[:limit]
    if more > 0:
        out.append(f"...and {more} more captions (use grep)")
    return out


def _render(entries, meta, cap: int, caps: list[str]) -> str:
    out = [f"{meta['name']}: {meta['pages']} pages, ~{meta['tokens']} tokens. "
           "Page numbers are PDF pages."]
    if meta.get("labels"):
        k, v = next(iter(meta["labels"].items()))
        out.append(f"(printed page labels differ, e.g. PDF page {k} = printed {v})")
    out.append("Sections: level, pages, ~tokens, title")
    for e in entries:
        if e.level <= cap:
            span = f"p{e.page}" if e.page == e.end_page else f"p{e.page}-{e.end_page}"
            out.append(f"{'  ' * (e.level - 1)}{span} ~{e.tokens} {e.title}")
    if caps:
        out.append("Figures and tables:")
        out.extend(caps)
    if meta.get("warnings"):
        out.append("Warnings: " + "; ".join(meta["warnings"][:5]))
    return "\n".join(out)


def render_map(entries, meta) -> str:
    if meta["small"]:
        return (f"small document (~{meta['tokens']} tokens): "
                "read whole with: docread.py read FILE --all")
    caps = _captions(meta["sha"])
    text = ""
    for cap in (4, 3, 2, 1):
        text = _render(entries, meta, cap, caps)
        if len(text) // 4 <= MAP_BUDGET_TOKENS:
            return text
    return text[: MAP_BUDGET_TOKENS * 4] + "\n...map truncated; use grep"
