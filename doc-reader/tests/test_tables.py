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


def test_md_table_row_counts_ignores_separator():
    text = "intro\n| a | b |\n|---|---|\n| 1 | 2 |\n\nmid\n| c |\n|---|\n| 3 |\n| 4 |"
    assert extract.md_table_row_counts(text) == [2, 3]


def test_rule_warns_when_markdown_has_more_rows_than_the_pdf_table(tmp_path):
    pdf = _grid_pdf(tmp_path, 260, 120, 3, 2, lambda r, c: True)  # 3 real rows
    split = "| a | b |\n|---|---|\n" + "\n".join(f"| r{i} | x |" for i in range(5))
    pages = [PageText(1, split, None, 1, [])]
    extract.apply_table_rule(pdf, pages)
    assert pages[0].text == split  # flag only, no repair
    assert "p1: table rows may be split across lines, check page-image" in pages[0].warnings


def test_kiht_wrapped_cell_table_is_flagged(sample, monkeypatch):
    import os

    monkeypatch.setenv("DOCREAD_HOME", os.path.expandvars(r"%LOCALAPPDATA%\doc-reader"))
    from docread import convert

    meta = convert.convert(sample("KIHT_HEOR.pdf"))
    assert any(w.startswith("p46:") and "split" in w for w in meta["warnings"])
    assert not any(w.startswith("p98:") for w in meta["warnings"])
    doc = (convert.cache.entry_dir(meta["sha"]) / "doc.md").read_text(encoding="utf-8")
    assert "|**Discount Rate**|3% per annum" in doc  # Table 10 survives as Markdown


def test_rule_judges_the_markdown_not_pdfplumber_cells(tmp_path):
    # pdfplumber sees an almost empty small grid, but the Markdown table is full: keep it
    pdf = _grid_pdf(tmp_path, 260, 120, 3, 3, lambda r, c: r == 0 and c == 0)
    full = "| a | b |\n|---|---|\n| 1 | 2 |"
    pages = [PageText(1, full, None, 1, [])]
    extract.apply_table_rule(pdf, pages)
    assert pages[0].text == full and pages[0].warnings == []


def test_rule_rejects_sparse_markdown_table(tmp_path):
    pdf = _grid_pdf(tmp_path, 260, 120, 3, 3, lambda r, c: True)
    sparse = "| a |  |  |\n|---|---|---|\n|  |  |  |\n|  | z |  |"
    pages = [PageText(1, sparse, None, 1, [])]
    extract.apply_table_rule(pdf, pages)
    assert pages[0].tables_md == 0
    assert "p1: table layout not reliable, raw text kept" in pages[0].warnings
