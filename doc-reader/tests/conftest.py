import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

SAMPLES = Path(__file__).resolve().parents[2] / "doc-reader-fixtures" / "dl"


@pytest.fixture(autouse=True)
def docread_home(tmp_path, monkeypatch):
    monkeypatch.setenv("DOCREAD_HOME", str(tmp_path / "home"))
    return tmp_path / "home"


@pytest.fixture
def make_pdf(tmp_path):
    def _make(pages, name="t.pdf"):
        import pymupdf  # venv only; imported lazily

        doc = pymupdf.open()
        for text in pages:
            page = doc.new_page()
            page.insert_textbox(pymupdf.Rect(50, 50, 550, 780), text, fontsize=10)
        out = tmp_path / name
        doc.save(out)
        return out

    return _make


@pytest.fixture
def sample():
    def _sample(name):
        p = SAMPLES / name
        if not p.exists():
            pytest.skip(f"sample missing: {name}")
        return p

    return _sample
