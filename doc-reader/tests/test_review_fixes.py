import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor

import pymupdf
import pytest

from docread import cache, clean, convert, env, escalate, extract, outline, readcmd
from docread.extract import PageText


def _uniq(i, n=90):
    rnd = random.Random(i)
    return " ".join(
        "".join(rnd.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rnd.randint(3, 9)))
        for _ in range(n))


def _pdf(tmp_path, pages, name="r.pdf"):
    d = pymupdf.open()
    for t in pages:
        d.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 780), t, fontsize=10)
    out = tmp_path / name
    d.save(out)
    return out


# 1 (critical): numeric table rows must survive header/footer stripping
def test_strip_running_keeps_numeric_table_rows():
    rows = "|Year|Value|\n|---|---|\n|1900|64.5|\n"
    tail = "\n|1999|3.1|\n|2000|4.2|\n|2001|5.3|"
    pages = [PageText(i, rows + _uniq(i, 30) + tail) for i in range(1, 15)]
    before = [p.text for p in pages]
    clean.strip_running(pages)
    assert [p.text for p in pages] == before


def test_strip_running_does_not_collapse_lines_that_differ_only_by_digits():
    pages = [PageText(i, f"Total {1900 + i} births\n" + _uniq(i, 30) + f"\nTotal {2000 + i} deaths")
             for i in range(1, 15)]
    before = [p.text for p in pages]
    clean.strip_running(pages)
    assert [p.text for p in pages] == before


def test_convert_records_stripped_line_count(tmp_path):
    pages = [f"Guidelines India-2026\n\n{_uniq(i)}\n\nUnique close {chr(97 + i)}{chr(98 + i)}-qq.\n\n{i + 1} | Page"
             for i in range(12)]
    meta = convert.convert(_pdf(tmp_path, pages))
    assert meta["stripped_lines"] >= 12


# 2: every flagged page is visible to Claude
def test_map_lists_all_flagged_pages(tmp_path):
    meta = convert.convert(_pdf(tmp_path, [_uniq(i) for i in range(12)]))
    warns = [f"p{n}: table rows may be split across lines, check page-image" for n in range(2, 11)]
    big = dict(meta, small=False, warnings=warns)
    text = outline.render_map(outline.build_map(meta["sha"]), big)
    assert "p10" in text.split("Flagged")[1] and "p2" in text.split("Flagged")[1]


def test_read_pages_shows_warnings_for_returned_pages(tmp_path):
    meta = convert.convert(_pdf(tmp_path, [_uniq(i) for i in range(3)]))
    path = cache.entry_dir(meta["sha"]) / "meta.json"
    m = json.loads(path.read_text(encoding="utf-8"))
    m["warnings"] = ["p2: table rows may be split across lines, check page-image"]
    path.write_text(json.dumps(m), encoding="utf-8")
    assert "p2: table rows may be split" in readcmd.read_pages(meta["sha"], 1, 2)
    assert "p2: table rows may be split" not in readcmd.read_pages(meta["sha"], 3, 3)


# 3: long conversions print a heartbeat
def test_convert_prints_heartbeat_when_slow(tmp_path, monkeypatch, capsys):
    import time

    real = extract.extract_pages
    monkeypatch.setattr(convert, "HEARTBEAT_SECONDS", 0.05)
    monkeypatch.setattr(extract, "extract_pages", lambda p: (time.sleep(0.4), real(p))[1])
    convert.convert(_pdf(tmp_path, [_uniq(0)]))
    assert "still converting" in capsys.readouterr().out


# 4: grep shows the match even deep inside a long line
def test_grep_centres_snippet_on_match(tmp_path):
    long_line = ("filler " * 120) + "needleword" + (" tail" * 40)
    meta = convert.convert(_pdf(tmp_path, [long_line]))
    out = readcmd.grep(meta["sha"], "needleword")
    assert "needleword" in out and len(out) < 600


# 5: a chapter divider or a certificate is not a scan
def test_small_picture_page_is_not_scan():
    divider = PageText(3, "Chapter 2", None, 0, [], images=1, image_cover=0.05)
    body = [PageText(n, "x" * 2000) for n in (1, 2, 4, 5, 6)]
    assert escalate.scan_pages(sorted(body + [divider], key=lambda p: p.page)) == []


def test_full_page_picture_is_scan():
    scan = PageText(3, "", None, 0, [], images=1, image_cover=0.9)
    body = [PageText(n, "x" * 2000) for n in (1, 2, 4, 5, 6)]
    assert escalate.scan_pages(sorted(body + [scan], key=lambda p: p.page)) == [3]


# 6: concurrent converts do not clobber each other
def test_convert_keeps_cache_written_by_another_process(tmp_path, monkeypatch):
    pdf = _pdf(tmp_path, [_uniq(0), _uniq(1)])
    sha = cache.file_hash(pdf)
    real = extract.extract_pages

    def slow_then_other_wins(p):
        pages = real(p)
        d = cache.entry_dir(sha)  # another process finishes first
        d.mkdir(parents=True, exist_ok=True)
        (d / "doc.md").write_text("<!-- page 1 -->\nx", encoding="utf-8")
        (d / "meta.json").write_text(json.dumps({"v": convert.VERSION, "sha": sha, "name": "r.pdf",
                                                 "pages": 2, "tokens": 1, "small": True, "warnings": []}),
                                     encoding="utf-8")
        (d / "page-1.png").write_bytes(b"png")
        return pages

    monkeypatch.setattr(extract, "extract_pages", slow_then_other_wins)
    convert.convert(pdf)
    assert (cache.entry_dir(sha) / "page-1.png").exists()


def test_parallel_converts_all_succeed(tmp_path):
    pdf = _pdf(tmp_path, [_uniq(i) for i in range(6)])
    gate = threading.Barrier(6)

    def go(_):
        gate.wait()
        return convert.convert(pdf)["sha"]

    with ThreadPoolExecutor(6) as ex:
        assert len(set(ex.map(go, range(6)))) == 1


# 7: a failed OCR or install is retried, not cached forever
def test_failed_ocr_is_not_cached(tmp_path, monkeypatch):
    d = pymupdf.open()
    for n in range(4):
        pg = d.new_page()
        if n == 1:
            src = pymupdf.open()
            src.new_page().insert_text((50, 50), "scan text " * 20)
            pg.insert_image(pg.rect, pixmap=src[0].get_pixmap(dpi=60))
        else:
            pg.insert_textbox(pymupdf.Rect(50, 50, 550, 780), _uniq(n), fontsize=10)
    pdf = tmp_path / "s.pdf"
    d.save(pdf)
    monkeypatch.setattr(escalate, "ensure_docling",
                        lambda: (_ for _ in ()).throw(RuntimeError("offline")))
    assert convert.convert(pdf)["incomplete"] is True
    calls = []
    real = extract.extract_pages
    monkeypatch.setattr(extract, "extract_pages", lambda p: calls.append(1) or real(p))
    convert.convert(pdf)
    assert calls == [1]  # tried again


# 8: pinned dependencies, fallback is announced
def test_packages_pinned_and_pytest_is_dev_only():
    assert not any(p.startswith("pytest") for p in env.packages())
    assert any(p.startswith("pytest") for p in env.packages(dev=True))
    assert all(">=" in p for p in env.packages())


def test_fallback_engine_is_announced(tmp_path, monkeypatch):
    monkeypatch.setattr(extract, "_with_pymupdf4llm", lambda p: (_ for _ in ()).throw(ValueError("x")))
    meta = convert.convert(_pdf(tmp_path, [_uniq(0)]))
    assert meta["engine"] == "pdfplumber"
    assert any("fallback" in w for w in meta["warnings"])
