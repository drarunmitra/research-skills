---
name: report-infographic-plates
version: 0.1.0
description: >
  Use when building infographic plates and per-area sheets for a Typst or Quarto PDF report from the project's own
  output files, so every number traces to a numbers file. Covers one white design language, a data feed, a build with
  layout preflight, a text check, page placement and a fresh-agent audit.
allowed-tools: Read, Write, Edit, Bash
---

# Report infographic plates

A report can carry a small set of infographic plates (full-page or half-page images) and one sheet per area. This skill makes the set look like one document and keeps every number traceable.

Core principle: a plate shows numbers. It never owns them.

## Pairs with

- epic-infographics (plugin): owns the design of one plate (brief, pitch, metaphor, design language, preflight, self-review). This skill sits on top for a whole set inside a report. For one plate's design, load epic-infographics. This skill takes over for data, build, text check and placement.
- numbers-audit: owns the numbers builder and the draft checker. This skill feeds it plate text. Hand off for building `numbers.csv` and the allow list.
- typst-report-tikz: owns the template, fonts, locked-PDF handling and `keep-md`. This skill owns only how a plate page is inserted.
- health-policy-brief: reader, tone and plain wording. Run its text checker on the extracted plate text.
- district-risk-tiers: supplies tier counts and the "consistent" and "less certain" labels that plates show.
- dataviz or design critique skills (if installed): optional chart and design review.

## When to use

- A report needs a poster, a few explainer plates and a sheet per district or area, built from the project's own data.
- Plates are being rebuilt after the numbers changed, and the numbers must be re-checked.

Do not use it for one stand-alone infographic (use epic-infographics), for building the report template (typst-report-tikz), or for judging the wording for decision makers (health-policy-brief).

## Iron rules

1. No number is typed into plate HTML. It comes from `data.json`, which comes from files the pipeline wrote.
2. One design language, one CSS token set, and a white page on every plate.
3. The build exits non-zero if any preflight fails, and names the plate.
4. Run the text extractor and the number checker after every rebuild. "0 unverified" is the gate.
5. Look at every PNG, or the contact sheet, before you place it.
6. A drawing that is not data is labelled illustrative. A proposal is labelled a proposal. An unverified item is shown as to be confirmed.
7. A plate that quotes a total names its scope.
8. The audit agent is a fresh agent that reads output files, not the generator.

## Order of steps

1. Ask: which plates, which areas get sheets, the report format and page size, and which numbers file exists.
2. Fix the design tokens once (`references/design-tokens.md`). Write the plate list with one sentence per plate: what the reader should remember.
3. Write the data script (`references/data-feed-pattern.md`). Print the key counts at the end.
4. Write the generator one plate at a time. Use epic-infographics for each plate's design.
5. Write `plates.tsv` and run `EPIC_DIR=<plugin scripts folder> bash scripts/build_plates.sh plates.tsv`. Fix every preflight error. Do not render around an error.
6. Extract the text and check it:
   `python scripts/plate_text.py html_dir text_dir`, then `Rscript scripts/check_plate_numbers.R numbers.csv text_dir allow.txt`.
   Allow structural tokens (axis ticks, dates) with a short allow file or `ALLOW_EXTRA` for one run. Never widen the pattern.
7. Make a contact sheet (`python scripts/contact_sheet.py png_dir sheet.png`) and look at it.
8. Place the plates (`references/placement.md`): full-page plates with the page counter fixed, figure plates with captions and `@fig-` references, area sheets after the references.
9. Render the PDF. Check that the contents numbers match the footer numbers and that no page is nearly empty.
10. Fresh-agent audit (`references/audit-prompt.md`). Fix the must-fix items. Log the rest.
11. If the project keeps a document hub, rebuild it and give the owner the link.

## Design language

One token set for the whole set: white background, one accent, one type pair, spacing from a scale (see `references/design-tokens.md`). Do not mix languages across plates. Do not add texture or grain. Fonts load from a font service at render time, so an offline build falls back to generic fonts. Say so in the build notes, or bundle the fonts.

## Data feed

One script reads the output files and writes one JSON file. A strict helper pulls headline numbers from `numbers.csv` and stops if a key is missing or not unique. Maps become SVG paths in a fixed viewBox. The script prints key counts so a person can compare them with the report. See `references/data-feed-pattern.md`.

## Build and preflight

`scripts/build_plates.sh` reads `plates.tsv` (name, width, height, html folder, png folder). It calls the preflight and the render scripts of epic-infographics (set `EPIC_DIR` to that folder, not a copy, and do not hard-code the plugin version in the path). It counts failures and exits 1 if any plate fails.

## Per-area sheets

One template, one sheet per area. Every sheet shows the same blocks in the same places. Name the same facts, so the sheets can be compared. After the references, one full-page block per sheet.

## Fresh-agent audit

The agent reads the plate text, the PNGs, `numbers.csv`, the output files and the report. It traces numbers, checks geometry against values, checks scope words and dates, and checks status words (illustrative, proposal, to be confirmed). See `references/audit-prompt.md`.

## Red flags

| Thought or sign | Fix |
|---|---|
| "I will type this one number into the HTML" | Add a key to the numbers builder, pass it through the data feed, rebuild. |
| The build said "PREFLIGHT ERRORS" and then "done" | Use `build_plates.sh`. A failed plate stops the build. |
| A total with no scope word | Name what it includes and leaves out. |
| A plate title total differs from the sum of its bars | Say "subtotal" or show the remainder. |
| A caption says "all are labelled" | Count the labels. |
| A line that could read as a forecast | Use a text callout. |
| A date or bar the report text never gives | Source it or mark it assumed. |
| The number check passed, so the plate is fine | Single digits pass by accident. Run the fresh-agent audit. |
| A textured or off-white page | White page, no grain. |
| Contents numbers do not match the footer after a full-page plate | `#counter(page).update(n => n - 1)` inside the plate page. |

The full table is in `references/plate-checklist.md`.

## Common mistakes

- Designing each plate with a different style.
- Pasting the plugin's scripts into the project, then letting them drift from the plugin.
- Rebuilding plates after the numbers changed and not re-running the text check.
- Using the plates in the report before anyone has looked at the contact sheet.

## Platform compatibility

Environment-dependent. Needs node with Playwright and Chromium (installed through epic-infographics), Python 3 with Pillow for the contact sheet, R for the number checker, and Quarto with Typst for the report. Internet is needed at render time for web fonts unless fonts are bundled. Tested on Windows with Git Bash. The method and the audit prompt run on any chat model.

## Version history

- 0.1.0 (2026-11-14): First release. Built from a health policy report with 11 plates and 12 area sheets. Scripts were not run against a live Playwright install in this release, apart from the text and checker scripts.
