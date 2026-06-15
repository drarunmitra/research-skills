# Reveal.js cookbook — native features, by use case

Everything here is **native Quarto/Reveal.js** — no custom CSS, no extensions —
so it is fully on-brand for the house style. Reach for these before ever writing
a CSS rule. Examples lean on a teaching domain (epidemiology, public
health, management) but the syntax is general.

Source: <https://quarto.org/docs/presentations/revealjs/> and
<https://quarto.org/docs/presentations/revealjs/advanced.html>

---

## 1. Revealing content step by step

### Pause mid-slide
Use case: show a question, let students answer, then reveal the key point.
```markdown
## It all hinges on the baseline

You cannot call it an outbreak until you know the **expected** count.

. . .

No baseline → no outbreak.
```

### Incremental bullet lists
Use case: walk through reasons/steps one at a time.
```markdown
::: {.incremental}
- Control the current outbreak
- Prevent recurrence
- Identify novel agents
:::
```
Global toggle: `incremental: true` in YAML (then use `.nonincremental` to opt a
list out).

### Fragments (fine-grained reveals + effects)
Use case: emphasise, strike through a wrong answer, highlight the vehicle.
```markdown
::: {.fragment .fade-up}
Slides up as it appears
:::

::: {.fragment .highlight-red}
Chicken curry — RR ≈ 11 (the vehicle)
:::

::: {.fragment .strike}
Paneer (no association)
:::
```
Effect classes: `fade-out`, `fade-up/down/left/right`, `fade-in-then-out`,
`fade-in-then-semi-out`, `semi-fade-out`, `grow`, `shrink`, `strike`,
`highlight-red/green/blue`, `highlight-current-red/green/blue`.

**Order reveals independently of source order** with `fragment-index`:
```markdown
::: {.fragment fragment-index=2}Second::: 
::: {.fragment fragment-index=1}First:::
```

**Nest** for sequential effects on the same element:
```markdown
::: {.fragment .fade-in}
::: {.fragment .highlight-red}
::: {.fragment .semi-fade-out}
Appears → highlights → dims
:::
:::
:::
```

---

## 2. Building a figure layer by layer (`.r-stack`)

Use case: **John Snow spot map revealed one layer at a time**, or an epidemic
curve that gains its label on click — stack images on top of each other and
fragment them in. This replaces the need for separate near-duplicate slides.
```markdown
## The spot map builds up

::: {.r-stack}
![](images/snow_stage1.png){width="700"}
![](images/snow_stage2.png){.fragment width="700"}
![](images/snow_stage3.png){.fragment width="700"}
![](images/snow_stage4.png){.fragment width="700"}
:::
```
Variant — "which curve is which?" reveal the labelled version over the blank one:
```markdown
::: {.r-stack}
![](images/curves_hook_unlabelled.png){width="800"}
![](images/curves_labelled.png){.fragment width="800"}
:::
```

---

## 3. Two-up and multi-column layouts

Use case: figure beside its interpretation; eaters vs non-eaters.
```markdown
:::: {.columns}
::: {.column width="48%"}
![](images/hostel_curve.png){width="100%"}
:::
::: {.column width="52%"}
- Single tight peak → **point source**
- All onsets within ~24–30 h
- Which dish was the vehicle?
:::
::::
```

---

## 4. Filling and fitting the slide

| Goal | Class | Example |
|:--|:--|:--|
| Auto-resize a figure to remaining space | `.r-stretch` | `![](map.png){.r-stretch}` |
| Stop auto-shrinking on a busy slide | `.nostretch` (slide) | `## Title {.nostretch}` |
| Huge headline text | `.r-fit-text` | `::: {.r-fit-text}\n1854\n:::` |
| Vertically centre slide content | `.center` (slide) | `## Key idea {.center}` |
| Free placement | `.absolute` | see below |

Reveal auto-stretches one image per slide by default. Disable globally with
`auto-stretch: false`.

### Absolute positioning
Use case: annotate a diagram, place callouts at exact spots.
```markdown
![](pump.png){.absolute top=120 left=40 width="350"}
![](legend.png){.absolute bottom=30 right=60 width="280"}
```
Attributes: `top left bottom right width height` (px or CSS units).

---

## 5. Handling overflow

```markdown
## Dense slide {.smaller}        <!-- shrink all text on this slide -->
## Long slide {.scrollable}      <!-- add a scrollbar instead of overflowing -->
```
`{.smaller}` is built in — never define your own "small" class. Both can be set
globally (`smaller: true`, `scrollable: true`) but per-slide is usually better.

---

## 6. Slide backgrounds

Use case: section dividers, full-bleed photos, embedded live sites.
```markdown
## {background-color="#222222"}                      <!-- solid; divider colour - set to taste -->
## {background-gradient="linear-gradient(to bottom,#283b95,#17b2c3)"}
## {background-image="soho1854.jpg" background-size="cover" background-opacity="0.6"}
## {background-video="cholera.mp4" background-video-loop="true" background-video-muted="true"}
## {background-iframe="https://ourworldindata.org/..." background-interactive="true"}
```
House note: prefer `.inverse` on dark/coloured dividers so headings stay white:
`# Section {.inverse background-color="#222222"}` (divider colour - set to taste).

Title-slide background (YAML):
```yaml
title-slide-attributes:
  data-background-image: cover.png
  data-background-size: contain
  data-background-opacity: "0.5"
```

---

## 7. Speaker notes, asides, footnotes

```markdown
## Slide

Visible content.

::: {.notes}
Presenter-only reminder. Press **S** for speaker view.
:::

::: aside
A peripheral note shown small at the bottom.
:::

Key claim.^[Snow J. *On the Mode of Communication of Cholera.* 1855.]
```

---

## 8. Per-slide footer / logo control

```markdown
## No footer here {footer=false}

## Custom footer
::: footer
WHO Field Epidemiology, 2018
:::
```
Global: `footer: "..."` and `logo: logo.png` in YAML.

---

## 9. Slide visibility & counting

```markdown
## Backup slide {visibility="hidden"}      <!-- excluded entirely -->
## Optional aside {visibility="uncounted"} <!-- shown, not counted in N -->
```

---

## 10. Vertical (stacked) navigation

Use case: a main thread with optional drill-downs you can skip live.
```yaml
format:
  revealjs:
    navigation-mode: vertical   # linear | vertical | grid
```
```markdown
# Steps            (horizontal)
## Step 4 detail   (press ↓ to reach)
## Step 5 detail
# Examples         (next horizontal)
```

---

## 11. Presentation size & transitions

```yaml
format:
  revealjs:
    width: 1050        # defaults: 1050 x 700
    height: 700
    margin: 0.1
    min-scale: 0.2
    max-scale: 2.0
```
Transitions (default is `none` — only add motion when it aids comprehension):
```yaml
    transition: fade          # none|fade|slide|convex|concave|zoom
    transition-speed: fast
```
Per-slide override: `## Title {transition="zoom"}`.

---

## 12. Built-in plugins (no install needed)

Enable in YAML; all ship with Quarto:
```yaml
format:
  revealjs:
    chalkboard: true   # press 'b' to draw, 'c' for chalkboard — great for live teaching
    menu: true         # slide menu (press 'm')
    multiplex: true    # audience follows your phone/laptop (needs setup)
    pdf-export: true
```
`chalkboard: true` is especially useful for annotating maps/curves during a
lecture and is fully native.

---

## See also
- `references/figures-and-code.md` — sizing R/ggplot plots, code reveals, output placement
- `references/advanced-and-extensions.md` — auto-animate, fragment-triggered JS, timeline/animate/editable extensions
