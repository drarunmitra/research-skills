# doc-reader acceptance run (2026-11-18)

Files: KIHT_HEOR.pdf (234 pages) and three HTAIn policy briefs (2-3 pages). Token counts are characters divided by four.

| File | Pages | Tokens after convert | Map |
|---|---|---|---|
| KIHT_HEOR.pdf | 234 | about 116,000 | 23 chapters plus captions, about 900 tokens |
| hta_cervical_policy.pdf | 3 | about 1,800 | small, read whole |
| hta_hemoglobinometer_policy.pdf | 2 | about 1,300 | small, read whole |
| hta_iol_policy.pdf | 3 | about 3,100 | small, read whole |

## One-topic question (KIHT_HEOR: what discount rate does the guideline recommend?)

map (about 890 tokens) + grep "discount rate" (about 535) + read pages 98-99 (about 980) = about 2,400 tokens, against about 116,000 for the whole text. That is 97.9 percent fewer tokens. Bar: at least 85 percent. Met. The answer (3 percent per annum, sensitivity at 0 to 5 percent) is in Table 10 on PDF page 98 (printed page 75).

## Tables checked against page images

| Table | PDF page | Result |
|---|---|---|
| Table 10, key components | 98 | Matches the page image row for row |
| Table 1, target audience | 27 | Kept as Markdown, no warning |
| Table 2, coding standards | 45 | Wrapped cell split across rows; page flagged |
| Table 3, data quality standards | 46 | Header and cells split across rows; page flagged |
| Table 4, caregiver instruments | 61 | Wrapped cell split across rows; page flagged |

Bar: every table matches, or the page says so in the warnings. Met: no table is wrong without a warning. Limit: three of the five tables need the page image to read the row grouping correctly. All words and numbers were present and in the correct column. 16 of 234 KIHT pages carry a table warning.

## Short briefs

All three read whole with `read --all`. Every word of five letters or more in the pdfplumber text is present in the output (0 missing in all three).

## Scan test

Slow test: a rendered image-only copy of a brief page was read through Docling OCR and contained the expected word. Passed (635 seconds, includes the one-time Docling install of about 9.5 minutes).

## Bugs the run found and fixed

1. The table rule judged pdfplumber cell text, which reads many real cells as empty, and threw away good tables. It now judges the Markdown table.
2. Wrapped cells split into extra rows with no warning. Pages where Markdown rows exceed PDF grid rows are now flagged.
3. After Docling is installed, the extractor ran its own OCR and changed scan detection. Its OCR is now off, so Docling is the only OCR path.
4. Library banners leaked into the output. They are silenced.

## Known limits

- First convert of a 234-page file takes about 2 to 3 minutes.
- About 8 running-title lines survive on KIHT (pages where the title sits outside the top three lines).
- Row grouping inside wrapped table cells is not repaired, only flagged.
- Office files are not supported in v1.
