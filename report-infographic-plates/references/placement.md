# Placing plates in a Typst / Quarto report

Needs the typst-report-tikz skill for the template. This file covers only how a plate page goes in.

## Full-page plate (a poster after the contents)

```
```{=typst}
#pagebreak()
#page(margin: 0pt, header: none, footer: none)[#counter(page).update(n => n - 1)#image("infographics/plate1_poster.png", width: 100%, height: 100%, fit: "cover")]
```
```

The page counter still steps on this page and the footer is hidden, so the printed numbers would skip one. The `counter(page).update(n => n - 1)` keeps the footer numbers in order. Check the contents list against the footer numbers on the rendered PDF.

## A plate as a figure in the text

```
@fig-cost shows where the cost goes.

```{r fig-cost}
#| fig-cap: "Where the Phase 1 cost goes."
#| out-width: "100%"
knitr::include_graphics("infographics/plate2_cost.png")
```

The table below gives the same costs by group.
```

- Name every figure in the text (`@fig-x`).
- Put a line of text between a plate and the next table or figure.
- Keep the caption short and do not repeat the plate's headline.

## One sheet per area (after the references)

Use `citeproc: true` so the reference list sits where you put `::: {#refs}`. Then emit one full-page raw block per sheet:

```r
fence <- strrep("`", 3); q <- intToUtf8(34)
for (d in areas) cat(fence, "{=typst}\n#page(margin: 0pt, header: none, footer: none)[#image(", q, "infographics/sheet_", d, ".png", q,
                     ", width: 100%, height: 100%, fit: ", q, "contain", q, ")]\n", fence, "\n\n", sep = "")
```

(Chunk option `results="asis"`.) Sheets after the references need no counter fix.

## Checks on the rendered PDF

- Every contents entry matches the footer number of its page.
- No page is nearly empty because a tall figure jumped over a page break. Shrink it with `out-width`.
- Look at the pages as images (a contact sheet is enough).
- A locked PDF: compile to a new file name.
