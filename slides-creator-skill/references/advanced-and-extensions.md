# Advanced motion & extensions

Power-user techniques for when a reveal needs real motion. Ordered from
**most house-friendly** (native, no install) to **opt-in extensions** (need
`quarto add`, an internet fetch at install, and add JS/plugins).

**House-style rule still holds:** keep `style.css` tiny. These add *behaviour*
(animation/interactivity), not decorative CSS. Use them only when the
pedagogical payoff is real; a static `.fragment` reveal is usually enough.

---

## A. Auto-animate (native — no extension)

Reveal automatically tweens matching elements between two consecutive slides
that both carry `auto-animate=true`. Great for **morphing** one state into the
next without a video.

Source: <https://quarto.org/docs/presentations/revealjs/advanced.html>

**Move / grow text:**
```markdown
## {auto-animate=true}
::: {style="margin-top: 100px;"}
Cases in excess of expected
:::

## {auto-animate=true}
::: {style="margin-top: 200px; font-size: 3em; color: maroon;"}
Cases in excess of expected
:::
```

**Match elements explicitly with `data-id`** (when text differs but the object
should be "the same"):
```markdown
## {auto-animate=true}
::: {data-id="box" style="background:#1f5560;width:200px;height:120px;"}
:::

## {auto-animate=true}
::: {data-id="box" style="background:maroon;width:500px;height:300px;"}
:::
```

**Animate code** (lines morph between slides — ideal for building up an analysis):
````markdown
## {auto-animate=true}
```r
ar_exposed <- 0.95
```

## {auto-animate=true}
```r
ar_exposed   <- 0.95
ar_unexposed <- 0.08
rr <- ar_exposed / ar_unexposed   # ≈ 11.4
```
````

Tuning attributes (slide- or element-level, or global YAML):
`auto-animate-easing` (default `ease`), `auto-animate-duration` (s),
`auto-animate-delay`, `auto-animate-unmatched` (fade unmatched, default true),
`auto-animate-id` (only animate between slides sharing an id).

**Use cases:** transform a 2×2 table into a calculated RR; grow a key number;
slide a pump marker onto a map; reveal an equation term by term.

---

## B. Fragment-triggered JavaScript (native + a small script include)

Run arbitrary JS exactly when a fragment is shown/hidden. Lets an "empty"
fragment drive a change elsewhere on the slide.

Source: <https://emilhvitfeldt.com/post/slidecraft-fragment-js/>

**Wire a script in:**
```yaml
format:
  revealjs:
    include-after-body: _script.html
```
`_script.html`:
```html
<script type="text/javascript">
Reveal.on('fragmentshown', (event) => {
  if (event.fragment.classList.contains('color')) {
    const color = event.fragment.dataset.color;
    Reveal.getCurrentSlide().querySelector('h2').style.color = color;
  }
});
Reveal.on('fragmenthidden', (event) => { /* reverse on back-nav */ });
</script>
```
**Trigger markup** — an empty fragment carrying data:
```markdown
## Watch the title change

:::: {.fragment .color data-color="maroon"}
::::
```
Key API: `Reveal.on('fragmentshown'|'fragmenthidden', cb)`,
`event.fragment` (the DOM node), `event.fragment.dataset.*`,
`Reveal.getCurrentSlide()`, then `.querySelector(...)`.

**Use cases:** recolour/annotate a chart on cue; start a CSS/JS animation;
reveal a map layer rendered by another library; play a sound/timer.

---

## C. Extensions (opt-in — require `quarto add`)

Caveats before using any: they must be installed into the project
(`_extensions/` folder), need network access at install time, add a Reveal
plugin and/or Lua filter, and slightly reduce the "one portable self-contained
HTML" simplicity. Confirm with the user before adding a dependency.

### C1. Timeline — `EmilHvitfeldt/quarto-timeline`
A styled, optionally animated timeline. Perfect for **the history of
epidemiology**, the **steps of an outbreak investigation**, or an **outbreak
chronology**.
- Install: `quarto add EmilHvitfeldt/quarto-timeline`
- YAML: `filters: [timeline]`
- Markup:
```markdown
::: {.timeline}
::: {.event data-label="1854" .fragment}
**Broad Street** — Snow's spot map indicts the pump.
:::
::: {.event data-label="1976" .fragment}
**Legionnaires'** — a novel organism found *via* the investigation.
:::
::: {.event data-label="2018" .fragment}
**Nipah, Kerala** — rapid response, One Health.
:::
:::
```
Add `.fragment` to each `.event` to reveal them one by one. Layout/modifier
classes (`.vertical`, `.tl-card`, …) exist for styling; defaults are fine.

### C2. SVG animation — `fradav/quarto-revealjs-animate`
Animates SVG elements with [SVG.js], synced to fragments. Built on rajgoel's
reveal animate plugin. Good for **transmission diagrams, mechanism animations,
and operations-research visuals** (the example gallery shows Monty Hall, linear
programming, simplex, branch-and-bound — directly relevant to the *management /
modern management techniques* deck).
- Install: `quarto install extension fradav/quarto-revealjs-animate`
- YAML:
```yaml
format: { revealjs: default }
revealjs-plugins: [animate]
filters: [animate]
```
- Markup — a fenced block with class `.animate` pointing at an SVG, with
  `setup:` (one-time manipulation) and `animation:` (timed) sections:
````markdown
## Beating heart

```{.animate src="images/heart.svg"}
setup:
  - element: "#heart"
    modifier: function() { this.animate(1500).ease('<>').scale(.9).loop(true,true); }
    parameters: []
```
````
`element` is a CSS selector into the SVG; `modifier` is any SVG.js function;
`parameters` are its args; timing via `duration`/`delay`/`when`. **Fragment
integration:** nest arrays in the `animation:` block — the first array runs on
slide entry, each subsequent array runs on the next fragment click.

### C3. Live-editable slides — `emilhvitfeldt/quarto-revealjs-editable`
Edit slide text/images **during** the talk (fix a typo, move a label, annotate),
with a Save that can write back to the `.qmd`.
- Install: `quarto add emilhvitfeldt/quarto-revealjs-editable`
- YAML:
```yaml
revealjs-plugins: [editable]
filters: [editable]
```
- Usage: either click the **Modify** button live (new mode, no pre-marking), or
  pre-mark elements:
```markdown
![](map.png){.editable}

::: {.editable}
Editable text block — move, resize, retype live.
:::
```
**Use case:** interactive teaching where you annotate/correct in front of the
class; capturing student-suggested edits and saving them.

[SVG.js]: https://svgjs.dev/

---

## Quick decision guide

| Need | Reach for | House-friendly? |
|:--|:--|:--:|
| Reveal items/effects | `.fragment` (cookbook §1) | ✅ native |
| Build a figure in layers | `.r-stack` + `.fragment` | ✅ native |
| Morph state → state | auto-animate (§A) | ✅ native |
| Step through code/output | `code-line-numbers`, `output-location` | ✅ native |
| Draw on slides live | `chalkboard: true` | ✅ native |
| Drive other elements on cue | fragment JS (§B) | ◐ small script |
| Chronology/timeline | quarto-timeline (§C1) | ◐ extension |
| SVG / OR / mechanism animation | quarto-revealjs-animate (§C2) | ◐ extension |
| Edit live during talk | quarto-revealjs-editable (§C3) | ◐ extension |
