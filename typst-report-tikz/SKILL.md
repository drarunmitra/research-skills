---
name: typst-report-tikz
version: 1.1.0
allowed-tools: Read, Write, Edit, Bash
description: Build a polished PDF report from Quarto with a custom Typst template and TikZ diagrams (xelatex to SVG). Use when a report PDF must look designed, not default, on Windows with Quarto, Typst and MiKTeX.
---

# Quarto + Typst report with TikZ figures

1. Template: put `typst-template.typ` and `typst-show.typ` next to the .qmd and set `format: typst: template-partials: [typst-template.typ, typst-show.typ]`. Do not use `toc: true`; place `#contents()` with a raw typst block.
2. Fonts: use static fonts only (variable fonts such as Bahnschrift warn in Typst and break dvipdfmx). Check that the fonts you name are installed before rendering (for example Source Serif Pro and Source Sans Pro).
3. Raw typst in qmd: wrap markdown between two raw blocks, for example a block with `#keypoints[`, the markdown list, then a block with `]`.
4. Metadata strings are markdown-escaped, so file names with underscores break (use `cover.png`, not `fig_cover.png`).
5. TikZ: write `tikz/*.tex` (standalone class, `\input{preamble.tex}`), build with `bash scripts/build_tikz.sh` (xelatex, then `pdftocairo -svg`). MiKTeX fails if PATH lists a file as a folder; the script drops entries ending in `.exe`. Include with a raw typst `#figure(image("figures/x.svg", width: 100%), caption: [...], kind: "quarto-float-fig", supplement: [Figure])`.
6. PDF locked by a viewer: render under a new file name.
7. Check: render with `keep-md: true`, then run the project's number checker on the `.typst.md` body (strip `@citekey` tokens first).
8. Prose: no em dashes, no bold in running prose, no AI vocabulary (see academic-writer skill).
9. Metadata keys: `logo` is a Quarto reserved key and renders as `true`. Use your own key (for example `institutionmark`) and read it in `typst-show.typ` with `$if(institutionmark)$`.
10. Compile failures: `error: failed to write PDF` means a viewer holds the file. If Quarto leaves the `.typ`, run `quarto typst compile report.typ report_v2.pdf`. The `.typ` exists only after a failed render.
11. References: add `citeproc: true` under `format: typst` and put `::: {#refs}` where the list should go. Without it, Quarto appends a native bibliography at the very end, after any annex pages. With citeproc, protect proper nouns in `.bib` titles with double braces (`title = {{ENSO Diagnostic Discussion}}`), or titles come out lower-case.
12. Full-page plates: a `#page(margin: 0pt, header: none, footer: none)[...]` page still advances the page counter and leaves a gap in the footer numbers. Put `#counter(page).update(n => n - 1)` as the first item inside it. Plates after the references (district sheets) need no fix.
13. Layout: a figure set to `breakable: false` that is taller than the space left jumps to the next page and leaves a near-empty page behind. Shrink it (`out-width`) or move the text around it. Look at every page as an image (`gs -sDEVICE=png16m -r36`, then a contact sheet) before you call the layout done.
14. Cross-references: give chunks `#| label: fig-x` or the chunk name `fig-x` and write `@fig-x` in the text. A raw typst figure cannot be referenced; use markdown `![caption](figures/x.svg){#fig-x}` instead. Put a line of text between a figure and the next table.
15. Spacing in raw typst: `#v(1.6em)` between blocks. Tell the number checker to ignore it.
16. Tables: pipe tables take column widths from the dash counts in the separator row. Write the separator yourself when columns overlap. Keep headers short.

## Pairs with

- numbers-audit: run it on the rendered `.typst.md` body.
- academic-writer: run it last on the prose.
- health-policy-brief: the document rules for policy reports built with this template.

## Platform compatibility

Environment-dependent. Needs Quarto with Typst, and for TikZ figures a LaTeX install (MiKTeX or TeX Live with xelatex) and `pdftocairo`. Written and tested on Windows; the PATH note in rule 5 is MiKTeX-specific.
