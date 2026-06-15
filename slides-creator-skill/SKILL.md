---
name: slides-creator-skill
version: 1.0.0
description: |
  Builds and publishes Dr Arun Mitra's teaching slide decks as Quarto
  Reveal.js presentations in his house style: stock Quarto defaults plus a
  tiny style.css — NEVER imported display fonts, colour-variable palettes,
  custom themes, gradient boxes, or bordered headings. Structure comes from
  native Quarto constructs (callouts, columns, panel-tabset, .smaller,
  fragments, .important). Use when asked to create, draft, restyle, or
  de-fancify a lecture/seminar/CME slide deck, or to render and publish one
  to GitHub Pages. Supports AIIMS Bibinagar Community Medicine teaching.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# Slides Creator (house style)

Create teaching decks the way Dr Arun Mitra actually builds them: **stock Quarto
Reveal.js with at most a tiny `style.css`.** The pedagogy and visual interest
come from *native Quarto features*, not bespoke CSS.

This rule was learned the hard way: a deck authored with imported serif display
fonts (Spectral/Playfair), a `:root` colour palette, `theme: simple`,
gold-underlined headings, and gradient `.ask`/`.park` boxes was rejected as too
"fancy." The fix was to delete all of it and lean on native constructs.

## When to use

- "Make slides / a deck / a presentation for <topic>"
- "Create a Quarto Reveal.js lecture / seminar / CME"
- "This deck looks too fancy — match my usual style"
- "Render and publish these slides to GitHub Pages"

## The house style — non-negotiable

**DO**
- Start from stock Quarto `revealjs` (the default theme — do not set `theme:`).
- Keep the front matter minimal (see template below).
- Use a **tiny `style.css`**: logo placement + `.important` (maroon) +
  `.inverse` headings (white). That's the whole sheet. Copy
  `assets/style.css` from this skill verbatim.
- Build structure with **native Quarto**:
  - `::: {.callout-note}` / `.callout-tip` / `.callout-important` /
    `.callout-warning` — for answers, asides, key points, "ask the class"
    prompts (use `appearance="simple"` for an understated look).
  - `:::: {.columns}` + `::: {.column width="50%"}` for two-up layouts.
  - `::: {.panel-tabset}` with `###` tabs for compare/contrast.
  - `{.smaller}` on the slide heading for dense slides (it is built in).
  - `. . .` to reveal content incrementally; `{.fragment}` on elements.
  - `[text]{.important}` for inline maroon emphasis, or `::: {.important}`
    to colour a whole label/line.
- Dark divider/section slides: `# Section title {.inverse background-color="#1f5560"}`
  (the `.inverse` rule turns headings/text white so they stay readable).
- Diagrams: native ```` ```{mermaid} ```` blocks (no external image needed).
- Keep `self-contained: true` + `embed-resources: true` so the `.html` is a
  single portable file (good for sharing and GitHub Pages).

**DON'T**
- No `@import url(...fonts...)` / Google Fonts / display typefaces.
- No `:root { --custom: ... }` colour-variable palettes.
- No `theme: simple` (or any non-default theme) unless explicitly asked.
- No gradient/border "boxes" — use native callouts instead.
- No bordered/underlined headings, custom `transition:`, etc.
- Don't invent bespoke classes (`.ask`, `.park`, `.stat-box`, …). If you
  catch yourself writing a new CSS class, replace it with a native callout
  or `.important`.

> Reference: this mirrors his `management_sem9` (tiny style.css), `Okinawa_Diet`
> (zero CSS), and `STH_Lecture_Slides` (stock default theme) decks.

## Standard front matter

```yaml
---
title: "<Deck title>"
subtitle: "<optional one-line subtitle>"
author: "Dr Arun Mitra"
institute: "Dept of Community and Family Medicine, AIIMS, Bibinagar"
date: today
format:
  revealjs:
    slide-number: true
    logo: aiims_bibinagar_logo.png
    css: style.css
    self-contained: true
    embed-resources: true
---
```

Copy `aiims_bibinagar_logo.png` into the deck folder (it lives alongside every
existing deck). Copy `assets/style.css` next to the `.qmd`.

## Workflow

1. **Scaffold** the deck folder: `<topic>/index.qmd` (or
   `<topic>_slides.qmd`), `style.css`, `aiims_bibinagar_logo.png`, and an
   `images/` subfolder for figures.
2. **Draft** content from the standard front matter + `assets/template.qmd` as
   a starting skeleton. One idea per slide; lean on callouts/columns/tabsets.
3. **Figures**: prefer pre-rendered PNGs in `images/`, or generate them in R
   following his conventions — native pipe `|>`, `here::here()` paths,
   `snake_case`, `pak::pak()` installs, tidyverse + ggplot2, and **seed all
   stochastic data** (`set.seed(...)`) for reproducibility.
4. **Render**: `quarto render <file>.qmd` (produces a self-contained `.html`).
   No R is needed if the deck only uses mermaid + pre-made images.
5. **Review** against the DO/DON'T list — grep the rendered `.html` to confirm
   no font imports leaked in: `grep -c "Playfair\|Spectral\|@import" file.html`.

## Publishing to GitHub Pages (optional)

When asked to publish (see the `outbreak_investigation` deploy as the worked
example):
- The repo holds **HTML only** — `index.html` (the deck) + any extra pages +
  a `.nojekyll` file. Source qmd/css/images stay out of the Pages repo.
- `gh` CLI / GitHub MCP are typically **not** authenticated; push with **git
  over HTTPS** — the Windows Credential Manager (`credential.helper=manager-core`)
  supplies the token.
- Stage in a temp dir **outside Dropbox** so no `.git` syncs into the teaching
  folder (e.g. `%LocalAppData%\Temp\ghpages_<name>`).
- Rename the main deck's HTML to `index.html` in the staging dir.
- Enable Pages via the REST API only with the user's go-ahead (it requires
  reading their stored token via `git credential fill`); otherwise have them
  flip Settings → Pages → source `main` / root.
- Update flow: re-render → copy HTML to `index.html` in the stage →
  `git add/commit/push origin main` → Pages auto-rebuilds.

## Recipes & deeper reference

When a slide needs more than the basics, consult these cookbooks (all examples
are teaching-oriented and, unless flagged, pure-native = on-brand):

- `references/revealjs-cookbook.md` — native features by use case: step reveals
  & fragments, building a figure in layers with `.r-stack` (e.g. the Snow spot
  map), columns, fit/stretch/absolute layout, overflow, backgrounds, speaker
  notes, vertical navigation, transitions, and built-in plugins (chalkboard,
  menu). **Start here.**
- `references/figures-and-code.md` — sizing R/ggplot plots for legibility
  (`fig-width`/`fig-asp`/`auto-stretch`), progressive code reveals
  (`code-line-numbers`), and output placement (`output-location:
  fragment/slide/column`). For analytic slides (attack-rate tables, RR, curves).
- `references/advanced-and-extensions.md` — auto-animate (morph state→state),
  fragment-triggered JavaScript, and opt-in extensions (quarto-timeline,
  quarto-revealjs-animate for SVG/OR visuals, quarto-revealjs-editable for live
  editing). Extensions need `quarto add` — confirm with the user first.

## Assets in this skill

- `assets/style.css` — the complete house stylesheet. Copy as-is.
- `assets/template.qmd` — a minimal skeleton deck demonstrating every
  approved native construct. Start here and replace the content.
