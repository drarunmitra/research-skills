import pymupdf

from docread import extract
from docread.extract import PageText, accept_table

PAGE = (600.0, 800.0)
MD = "| a | b |\n|---|---|\n| 1 | 2 |"


def test_full_page_grid_rejected():
    cells = [["x", "y"], ["z", "w"]]
    assert accept_table((0, 0, 570, 780), PAGE, cells) is False


def test_small_filled_table_accepted():
    cells = [["a", "b"], ["1", "2"]]
    assert accept_table((50, 50, 300, 150), PAGE, cells) is True


def test_sparse_table_rejected():
    cells = [["a", None, None], [None, None, None], [None, "b", None]]
    assert accept_table((50, 50, 300, 150), PAGE, cells) is False


def _grid_pdf(tmp_path, x1, y1, rows, cols, fill):
    d = pymupdf.open()
    pg = d.new_page(width=600, height=800)
    x0, y0 = 20, 20
    cw, ch = (x1 - x0) / cols, (y1 - y0) / rows
    for r in range(rows + 1):
        pg.draw_line((x0, y0 + r * ch), (x1, y0 + r * ch))
    for c in range(cols + 1):
        pg.draw_line((x0 + c * cw, y0), (x0 + c * cw, y1))
    for r in range(rows):
        for c in range(cols):
            if fill(r, c):
                pg.insert_text((x0 + c * cw + 3, y0 + r * ch + ch / 2), f"v{r}{c}", fontsize=8)
    out = tmp_path / "g.pdf"
    d.save(out)
    return out


def test_rule_rejects_page_wide_sparse_grid(tmp_path):
    pdf = _grid_pdf(tmp_path, 580, 780, 8, 8, lambda r, c: r == 0 and c == 0)
    pages = [PageText(1, MD, None, 1, [])]
    extract.apply_table_rule(pdf, pages)
    assert pages[0].tables_md == 0
    assert "|---" not in pages[0].text
    assert "p1: table layout not reliable, raw text kept" in pages[0].warnings


def test_rule_keeps_small_filled_table(tmp_path):
    pdf = _grid_pdf(tmp_path, 260, 120, 3, 3, lambda r, c: True)
    pages = [PageText(1, MD, None, 1, [])]
    extract.apply_table_rule(pdf, pages)
    assert pages[0].tables_md == 1
    assert pages[0].text == MD
    assert pages[0].warnings == []


def test_hta_brief_emits_no_bogus_markdown_table(sample):
    pages = extract.extract_pages(sample("hta_hemoglobinometer_policy.pdf"))
    assert all("|---" not in p.text for p in pages)
