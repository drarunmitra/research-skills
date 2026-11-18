import random
import subprocess
import sys
from pathlib import Path

import pytest

from docread import convert, readcmd
from docread.extract import DocError

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "docread.py"


def _uniq(i, n=60):
    rnd = random.Random(i)
    return " ".join(
        "".join(rnd.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rnd.randint(3, 9)))
        for _ in range(n))


def _doc(make_pdf, heads=("1. Intro", "2. Methods", "3. Results")):
    pages = [f"{h}\n\n{_uniq(i)} body{'xyz'[i]}end" for i, h in enumerate(heads)]
    pdf = make_pdf(pages)
    return pdf, convert.convert(pdf)["sha"]


def test_read_pages_inclusive(make_pdf):
    pdf = make_pdf([f"{_uniq(i)} pg{'abcde'[i]}tag" for i in range(5)])
    sha = convert.convert(pdf)["sha"]
    out = readcmd.read_pages(sha, 2, 3)
    assert "pgbtag" in out and "pgctag" in out
    assert "pgatag" not in out and "pgdtag" not in out


def test_read_pages_out_of_range_message(make_pdf):
    sha = convert.convert(make_pdf(["a b c", "d e f"]))["sha"]
    with pytest.raises(DocError, match="pages out of range 1-2"):
        readcmd.read_pages(sha, 1, 99)


def test_read_section_returns_only_that_section(make_pdf):
    _, sha = _doc(make_pdf)
    out = readcmd.read_section(sha, "methods")
    assert "bodyyend" in out and "bodyxend" not in out and "bodyzend" not in out


def test_read_section_ambiguous_lists_candidates(make_pdf):
    _, sha = _doc(make_pdf, heads=("1. Intro", "2. Methods A", "3. Methods B"))
    out = readcmd.read_section(sha, "methods")
    assert out.startswith("ambiguous")
    assert "2. Methods A" in out and "3. Methods B" in out


def test_read_section_no_match(make_pdf):
    _, sha = _doc(make_pdf)
    assert readcmd.read_section(sha, "zzz").startswith("no section matches 'zzz'")


def test_grep_literal_special_chars(make_pdf):
    sha = convert.convert(make_pdf(["intro text here", "we found (p<0.05) in arm B", "end"]))["sha"]
    out = readcmd.grep(sha, "(p<0.05)")
    assert out.startswith("p2:") and "(p<0.05)" in out


def test_grep_no_hits_message(make_pdf):
    sha = convert.convert(make_pdf(["nothing relevant"]))["sha"]
    assert readcmd.grep(sha, "x") != "" and readcmd.grep(sha, "qqq") == "no hits for 'qqq'"


def test_page_image_writes_png(make_pdf):
    pdf = make_pdf(["hello", "world"])
    out = readcmd.page_image(pdf, 2)
    assert out.read_bytes()[:4] == b"\x89PNG"
    with pytest.raises(DocError, match="pages out of range 1-2"):
        readcmd.page_image(pdf, 9)


def test_read_all_refuses_large_doc_without_yes(make_pdf):
    pdf = make_pdf([_uniq(i, 400) for i in range(12)])  # about 5k+ tokens
    meta = convert.convert(pdf)
    assert not meta["small"]
    with pytest.raises(DocError, match="use --section, --pages or grep"):
        readcmd.read_all(meta["sha"], meta)
    assert len(readcmd.read_all(meta["sha"], meta, yes=True)) > 1000


def test_cli_read_pages_and_grep(make_pdf):
    pdf = make_pdf(["alpha line", "beta needle line"])
    r = subprocess.run([sys.executable, str(SCRIPT), "read", str(pdf), "--pages", "2-2"],
                       capture_output=True)
    assert r.returncode == 0 and b"needle" in r.stdout
    g = subprocess.run([sys.executable, str(SCRIPT), "grep", str(pdf), "needle"],
                       capture_output=True)
    assert g.returncode == 0 and g.stdout.decode().startswith("p2:")
