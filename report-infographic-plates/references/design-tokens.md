# Design tokens and the page helper

One token set for every plate. Change the values per project, once. Do not change them per plate.

The example below is the "editorial" language used in a health policy report: white page, one red accent, a serif display face and a sans body face. The rules that matter are the structure, not the colours: one background, one accent, one type pair, spacing from a scale, no texture.

```python
import html, os

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@400;900&family=Libre+Franklin:wght@400;500;600&display=swap" rel="stylesheet">')
# Offline builds fall back to the generic families. Say so in the report notes, or bundle the fonts.

CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
svg { display: block; }
:root {
  --bg:#FFFFFF; --surface:#F2F2F2; --surface-2:#DEDEDE; --ink:#20242C; --ink-muted:#6B6F76;
  --accent:#A32035; --chart-1:#A32035; --chart-2:#0D7F63; --chart-3:#B07C1F; --chart-4:#20242C;
  --font-display:'Fraunces',serif; --font-body:'Libre Franklin',sans-serif;
  --space-1:8px; --space-2:16px; --space-3:24px; --space-4:48px; --space-5:72px;
  --rule-hair:1px solid var(--ink); --rule-heavy:3px solid var(--ink);
}
html, body { background: var(--bg); }
body { font-family: var(--font-body); color: var(--ink); width: var(--w); }
.canvas { position: relative; width: var(--w); height: var(--h); overflow: hidden; background: #FFFFFF; }
.abs { position: absolute; }
h1, .display { font-family: var(--font-display); font-weight: 900; line-height: .95; letter-spacing: -0.015em; }
.standfirst { font: italic 400 24px/1.4 var(--font-display); }
.folio { display:flex; justify-content:space-between; font: 600 14px/1 var(--font-body); letter-spacing:.1em; color: var(--ink-muted);
  border-top: var(--rule-hair); border-bottom: var(--rule-hair); padding: 10px 0; }
.cap { font: 400 14px/1.4 var(--font-body); color: var(--ink-muted); }
.src { font: 400 13px/1.4 var(--font-body); color: var(--ink-muted); }
"""

def page(name, w, h, comment, body, out_dir, extra_css=""):
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(name)}</title>{FONTS}'
           f'<style>:root{{--w:{w}px;--h:{h}px}}{CSS}{extra_css}</style></head><body>\n<!-- composition: {comment} -->\n'
           f'<div class="canvas">{body}</div></body></html>')
    os.makedirs(out_dir, exist_ok=True)
    p = os.path.join(out_dir, name + ".html")
    open(p, "w", encoding="utf-8").write(doc)
    return p

def fmt(n):            # 12345 -> "12,345"
    return f"{int(round(n)):,}"
```

Rules:
- White page on every plate. No grain, no gradient, no off-white. (A textured page was built first in the source project and rebuilt on white.)
- Every number in `body` comes from the data feed (`D[...]`), never typed. Format with `fmt()` and friends.
- Text never wears the data colour. The mark carries the colour.
- A drawing that is not data carries the word "illustrative". A proposal carries the word "proposal".
- Fonts below 13 px are a preflight warning. Keep a footer source line at 13 px or more.
- For the design of one plate (hero element, composition, chart type), use the epic-infographics skill steps. This file only fixes what must be the same across the set.
