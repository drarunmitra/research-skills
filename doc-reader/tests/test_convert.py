import os
import subprocess
import sys
from pathlib import Path

import pytest

from docread import clean, convert, extract
from docread.extract import DocError, PageText

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "docread.py"


WORDS = "alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo lima".split()


def _body(i):
    w = WORDS[i - 1]
    return "\n\n".join(f"Paragraph {k} about {w} {w[::-1]} {w.upper()}-{k}x." for k in "abcdefgh")


def _twelve_pages(make_pdf):
    pages = [
        f"Guidelines India-2026\n\n{_body(i)}\n\nUnique closing sentence {WORDS[i-1]}-qq.\n\n{i} | Page"
        for i in range(1, 13)
    ]
    return make_pdf(pages)


def test_convert_writes_cache_and_marks_pages(make_pdf):
    pdf = make_pdf(["alpha one", "beta two", "gamma three"])
    meta = convert.convert(pdf)
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert "<!-- page 1 -->" in doc and "<!-- page 3 -->" in doc
    assert meta["pages"] == 3


def test_second_convert_hits_cache(make_pdf, monkeypatch):
    pdf = make_pdf(["alpha one", "beta two"])
    convert.convert(pdf)
    calls = []
    monkeypatch.setattr(extract, "extract_pages", lambda p: calls.append(p) or [])
    convert.convert(pdf)
    assert calls == []


def test_strip_running_removes_header_footer_on_12_page_pdf(make_pdf):
    meta = convert.convert(_twelve_pages(make_pdf))
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert "Guidelines India-2026" not in doc
    assert "| Page" not in doc
    assert "golf-qq" in doc


def test_short_doc_keeps_headers(make_pdf):
    pdf = make_pdf(["Guidelines India-2026\n\nbody a", "Guidelines India-2026\n\nbody b"])
    meta = convert.convert(pdf)
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert doc.count("Guidelines India-2026") == 2


def test_printed_labels_recorded_in_marker(make_pdf):
    pages = [f"Running title\n\n{_body(i)}\n\n{i + 10} | Page" for i in range(1, 13)]
    meta = convert.convert(make_pdf(pages))
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert "<!-- page 3 label 13 -->" in doc


def test_page_labels_only_when_different():
    pages = [PageText(1, "x\n1 | Page", None, 0, []), PageText(2, "x\n12 | Page", None, 0, [])]
    assert clean.page_labels(pages) == {2: "12"}


def test_password_pdf_raises_docerror(tmp_path):
    import pymupdf

    d = pymupdf.open()
    d.new_page().insert_text((50, 50), "secret")
    out = tmp_path / "locked.pdf"
    d.save(out, encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="u", owner_pw="o")
    with pytest.raises(DocError, match="password"):
        convert.convert(out)


def test_non_pdf_raises_docerror_with_office_message(tmp_path):
    f = tmp_path / "a.docx"
    f.write_bytes(b"PK")
    with pytest.raises(DocError, match="Office files are not supported in v1"):
        convert.convert(f)


def test_corrupt_pdf_raises_docerror(tmp_path):
    f = tmp_path / "bad.pdf"
    f.write_bytes(b"not a pdf at all")
    with pytest.raises(DocError):
        convert.convert(f)


def test_cli_prints_utf8_on_cp1252_console(make_pdf):
    pdf = make_pdf(["hello world"], name="ప్ర_●.pdf")
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "convert", str(pdf)], capture_output=True, env=env
    )
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    assert "1 pages" in r.stdout.decode("utf-8")


def test_cli_docerror_exit_2_one_line(tmp_path):
    f = tmp_path / "a.docx"
    f.write_bytes(b"PK")
    r = subprocess.run([sys.executable, str(SCRIPT), "convert", str(f)], capture_output=True)
    assert r.returncode == 2
    assert b"Traceback" not in r.stdout + r.stderr
