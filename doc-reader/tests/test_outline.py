import os
import random

import pymupdf

from docread import convert, outline

WORDS = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima".split()
FILL = " ".join(["lorem ipsum dolor sit amet"] * 12)


def _uniq(i):
    rnd = random.Random(i)
    return " ".join(
        "".join(rnd.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rnd.randint(3, 9)))
        for _ in range(90))


def _pdf(tmp_path, pages, toc=None, name="o.pdf"):
    d = pymupdf.open()
    for text in pages:
        d.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 780), text, fontsize=10)
    if toc:
        d.set_toc(toc)
    out = tmp_path / name
    d.save(out)
    return out


def test_bookmarks_used_first(tmp_path):
    pdf = _pdf(tmp_path, [FILL] * 4, toc=[[1, "Intro", 1], [1, "Methods", 3]])
    meta = convert.convert(pdf)
    entries = outline.build_map(meta["sha"])
    assert [e.title for e in entries] == ["Intro", "Methods"]
    assert (entries[0].page, entries[0].end_page) == (1, 2)
    assert entries[1].end_page == 4


def test_regex_fallback_finds_numbered_headings(tmp_path):
    pages = [f"1. Introduction\n\n{FILL}", f"1.1 Background\n\n{FILL}", f"2. Methods\n\n{FILL}"]
    meta = convert.convert(_pdf(tmp_path, pages))
    entries = outline.build_map(meta["sha"])
    assert [(e.level, e.title, e.page) for e in entries] == [
        (1, "1. Introduction", 1), (2, "1.1 Background", 2), (1, "2. Methods", 3)]


def test_window_fallback_when_no_headings(tmp_path):
    meta = convert.convert(_pdf(tmp_path, [_uniq(i) for i in range(12)]))
    entries = outline.build_map(meta["sha"])
    assert [e.title for e in entries] == ["pages 1-5", "pages 6-10", "pages 11-12"]


def test_small_doc_gate(tmp_path):
    meta = convert.convert(_pdf(tmp_path, ["short text"]))
    text = outline.render_map(outline.build_map(meta["sha"]), meta)
    assert text.startswith("small document")
    assert "read FILE --all" in text


def test_captions_listed(tmp_path):
    pages = [f"1. Intro\n\n{_uniq(0)}\n\nFigure 1: Flow of studies",
             f"2. Methods\n\n{_uniq(1)}\n\nTable 2: Coding standards"]
    pages += [_uniq(i) for i in range(2, 12)]
    meta = convert.convert(_pdf(tmp_path, pages))
    meta = dict(meta, small=False)  # force the big-document view
    text = outline.render_map(outline.build_map(meta["sha"]), meta)
    assert "Figure 1 p1" in text and "Flow of studies" in text
    assert "Table 2 p2" in text


def test_map_under_2000_tokens_for_kiht(sample, monkeypatch):
    real = os.path.expandvars(r"%LOCALAPPDATA%\doc-reader")
    monkeypatch.setenv("DOCREAD_HOME", real)
    meta = convert.convert(sample("KIHT_HEOR.pdf"))
    text = outline.render_map(outline.build_map(meta["sha"]), meta)
    assert len(text) // 4 <= 2000
    assert "Introduction" in text and "Data Sources and Quality" in text


def test_cli_map_prints_gate_for_small_doc(tmp_path):
    import subprocess
    import sys
    from pathlib import Path

    script = Path(__file__).resolve().parents[1] / "scripts" / "docread.py"
    pdf = _pdf(tmp_path, ["short text"])
    r = subprocess.run([sys.executable, str(script), "map", str(pdf)], capture_output=True)
    assert r.returncode == 0, r.stderr
    assert r.stdout.decode("utf-8").startswith("small document")
