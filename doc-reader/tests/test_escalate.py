import pymupdf
import pytest

from docread import convert, escalate, extract, outline
from docread.extract import PageText


def _pages(spec):
    """spec: list of (chars, images)"""
    return [PageText(i + 1, "x" * c, None, 0, [], images=im) for i, (c, im) in enumerate(spec)]


def test_cover_page_not_scan():
    pages = _pages([(58, 2)] + [(2000, 0)] * 5)
    assert escalate.scan_pages(pages) == []


def test_image_only_pages_detected():
    pages = _pages([(2000, 0), (2000, 0), (0, 1), (10, 1), (2000, 0), (2000, 0)])
    assert escalate.scan_pages(pages) == [3, 4]


def test_all_image_pdf_flags_all_pages():
    pages = _pages([(0, 1)] * 6)
    assert escalate.scan_pages(pages) == [1, 2, 3, 4, 5, 6]


def test_text_pages_with_figures_not_scan():
    assert escalate.scan_pages(_pages([(1500, 3)] * 6)) == []


def _scan_pdf(tmp_path, text_pages, scan_pages, total, name="scan.pdf"):
    """A PDF where `scan_pages` (1-based) hold only a picture of text."""
    d = pymupdf.open()
    for n in range(1, total + 1):
        label = f"page {n} " + "word " * 120
        if n in scan_pages:
            tmp = pymupdf.open()
            tmp.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 780), label, fontsize=12)
            pix = tmp[0].get_pixmap(dpi=100)
            pg = d.new_page()
            pg.insert_image(pg.rect, pixmap=pix)
        else:
            d.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 780), label + f" real{n}", fontsize=10)
    out = tmp_path / name
    d.save(out)
    return out


def test_extract_counts_images(tmp_path):
    pdf = _scan_pdf(tmp_path, [], {2}, 3)
    pages = extract.extract_pages(pdf)
    assert pages[1].images >= 1 and len(pages[1].text.strip()) < 100
    assert pages[0].images == 0


def test_convert_ocrs_only_scan_pages(tmp_path, monkeypatch):
    pdf = _scan_pdf(tmp_path, [], {3, 4}, 6)
    calls = {"ensure": 0, "ocr": None}
    monkeypatch.setattr(escalate, "ensure_docling", lambda: calls.__setitem__("ensure", 1))
    monkeypatch.setattr(escalate, "ocr_pages",
                        lambda p, pgs: calls.__setitem__("ocr", list(pgs)) or {n: f"OCRTEXT{n}" for n in pgs})
    meta = convert.convert(pdf)
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert calls["ocr"] == [3, 4] and calls["ensure"] == 1
    assert "<!-- page 3 ocr -->" in doc and "OCRTEXT3" in doc and "OCRTEXT4" in doc
    assert outline._MARK.match("<!-- page 3 ocr -->")


def test_convert_cover_page_never_installs_docling(tmp_path, monkeypatch):
    d = pymupdf.open()
    cover = d.new_page()
    cover.insert_text((50, 50), "Cover title")
    pix = pymupdf.open()
    pix.new_page().insert_text((50, 50), "logo")
    cover.insert_image(pymupdf.Rect(0, 100, 100, 200), pixmap=pix[0].get_pixmap(dpi=50))
    for n in range(2, 7):
        d.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 780), "body " * 200, fontsize=10)
    out = tmp_path / "cover.pdf"
    d.save(out)
    called = []
    monkeypatch.setattr(escalate, "ensure_docling", lambda: called.append(1))
    convert.convert(out)
    assert called == []


def test_ocr_failure_keeps_page_and_warns(tmp_path, monkeypatch):
    pdf = _scan_pdf(tmp_path, [], {2}, 4)
    monkeypatch.setattr(escalate, "ensure_docling", lambda: (_ for _ in ()).throw(RuntimeError("no net")))
    meta = convert.convert(pdf)
    assert any("p2" in w and "OCR" in w for w in meta["warnings"])


@pytest.mark.slow
def test_ocr_pages_returns_text(tmp_path, sample):
    src = pymupdf.open(sample("hta_cervical_policy.pdf"))
    pix = src[0].get_pixmap(dpi=150)
    d = pymupdf.open()
    pg = d.new_page(width=pix.width, height=pix.height)
    pg.insert_image(pg.rect, pixmap=pix)
    out = tmp_path / "scan1.pdf"
    d.save(out)
    escalate.ensure_docling()
    text = escalate.ocr_pages(out, [1])[1].lower()
    assert "cervical" in text
