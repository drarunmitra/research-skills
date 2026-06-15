# Figures & code on slides — sizing, reveals, output placement

For decks that compute things live (R chunks) or need crisp, legible plots.
Follows sound R conventions: native pipe `|>`, `here::here()` paths,
`snake_case`, `pak::pak()` installs, tidyverse + ggplot2, and **always seed**
stochastic data (`set.seed(...)`).

Sources: Emil Hvitfeldt's Slidecraft posts on plot sizing and code/output.

---

## 1. Sizing R / ggplot plots (the #1 legibility fix)

**The problem:** Quarto's default `fig-width`/`fig-height` are too large for
slides, so plotted text renders tiny. *Lower* the figure size to make on-plot
text bigger relative to the slide.

Two independent controls:
- **`fig-width` / `fig-height`** — the size the plot is *drawn* at (inches).
  Smaller → larger-looking text. Good starting point: `fig-width: 6`,
  `fig-height: 3.5` for a full slide.
- **`out-width` / `out-height`** — how big the saved image is *displayed*.
  Use to shrink a plot that shouldn't fill the slide (e.g. `out-width: "70%"`).

**Most efficient approach — set the aspect ratio once with `fig-asp`** (height ÷
width), then tune only `fig-width`:
````markdown
```{r}
#| fig-width: 8
#| fig-asp: 0.5      # wide, short — ideal for an epidemic curve
#| fig-align: center
#| echo: false
epi_curve_plot
```
````

Other knobs:
- `fig-dpi: 300` — sharper export (bigger file); raise if a chart looks blurry.
- `fig-align: center` — default is left.

**Interaction with `auto-stretch`:** Reveal shrinks a lone figure to fit the
slide (default `auto-stretch: true`). If your careful `fig-asp` is being
overridden, disable per slide with `## Title {.nostretch}` or globally
`auto-stretch: false`.

**In `.columns`:** a plot in a half-width column needs a *taller* aspect ratio —
re-tune `fig-asp` per slide rather than relying on the global default.

Rule of thumb for a full-slide ggplot during an in-person lecture:
`fig-width: 7–9`, `fig-asp: 0.5–0.65`, theme base_size ≈ 16–20.

---

## 2. Showing code reveal step by step

**Progressive line highlighting** with `code-line-numbers` — walk through a
computation one chunk at a time (each `|`-separated group is one fragment):
````markdown
```{r}
#| echo: true
#| code-line-numbers: "|1|3-4|6"
line_list |>
  filter(ate_chicken) |>
  summarise(ar = mean(ill)) |>           # attack rate in eaters
  mutate(rr = ar / ar_unexposed) |>
  pull(rr)
```
````
- `code-line-numbers: "3,5"` — highlight static lines.
- `code-line-numbers: "|3|5"` — reveal highlight 3, then 5, on click.
- `code-line-numbers: true/false` — just toggle numbering.

Other display options: `echo: true/false` (show source), `eval: true/false`
(run it), `code-copy: true` (copy button), `code-link: true` (linked function
docs), `code-fold: true` (collapsible), `code-block-height: 650px` (avoid
internal scroll on tall blocks).

---

## 3. Placing output relative to code (`output-location`)

Use case: show the code, then *reveal* the plot/table; or put output in a side
column.
````markdown
```{r}
#| echo: true
#| output-location: fragment   # output appears on next click
ggplot(hostel, aes(onset_hour)) + geom_histogram()
```
````
Options:
- `fragment` — output revealed after a click (great for "predict, then show").
- `slide` — output pushed onto its own following slide.
- `column` — code left, output right (side by side).
- `column-fragment` — side by side, but output appears on click.

---

## 4. Long output

Wrap the slide with `{.scrollable}` so a big table/print doesn't overflow:
```markdown
## Model summary {.scrollable}
```
…or keep tables small with `{.smaller}` and `gt`/`DT` sizing.

---

## 5. Worked patterns

**Epidemic curve, drawn live, revealed after the question:**
````markdown
## Read this curve {.smaller}

What source does this shape suggest?

```{r}
#| echo: false
#| output-location: fragment
#| fig-width: 8
#| fig-asp: 0.5
plot_epi_curve(point_source_data)   # single sharp peak
```
````

**Attack-rate table → RR, code then result side by side:**
````markdown
## Finding the vehicle

```{r}
#| echo: true
#| output-location: column-fragment
attack_rates <- food_log |>
  group_by(food, ate) |>
  summarise(ar = mean(ill), .groups = "drop")
attack_rates
```
````

**Reproducible synthetic data (seed!), table with `gt`:**
````markdown
```{r}
#| echo: false
set.seed(18540831)
# ... simulate line list ...
gt::gt(ar_table)
```
````

> For static (pre-rendered) figures, just use `![](images/curve.png){width="80%"}`
> — no R needed at render time, and the deck stays trivially reproducible.
