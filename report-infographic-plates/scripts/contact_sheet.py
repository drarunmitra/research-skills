#!/usr/bin/env python3
"""One overview image of all plate PNGs, so a person can look at every plate at once before placing them.

Usage: python contact_sheet.py png_dir out.png [glob_pattern]
Default pattern: *.png. Needs Pillow. Prints the output path.
Plates are placed in the shortest of three columns (masonry layout). The file name (without .png) is the label.
"""
import glob
import os
import sys
from PIL import Image, ImageDraw, ImageFont

src, out = sys.argv[1], sys.argv[2]
pat = sys.argv[3] if len(sys.argv) > 3 else "*.png"
files = [f for f in sorted(glob.glob(os.path.join(src, pat))) if os.path.abspath(f) != os.path.abspath(out)]
if not files:
    sys.exit("no PNG files found")
W, cols, gap = 2400, 3, 40
cw = (W - gap * (cols + 1)) // cols
try:
    font = ImageFont.truetype("arial.ttf", 26)
except Exception:
    font = ImageFont.load_default()
colh = [gap] * cols
pos = []
for f in files:
    im = Image.open(f).convert("RGB")
    im = im.resize((cw, int(im.height * cw / im.width)), Image.LANCZOS)
    c = colh.index(min(colh))
    x, y = gap + c * (cw + gap), colh[c]
    pos.append((os.path.basename(f)[:-4], im, x, y))
    colh[c] = y + 40 + im.height + gap
sheet = Image.new("RGB", (W, max(colh)), "#FFFFFF")
d = ImageDraw.Draw(sheet)
for label, im, x, y in pos:
    d.text((x, y), label, fill="#20242C", font=font)
    sheet.paste(im, (x, y + 40))
    d.rectangle([x, y + 40, x + im.width, y + 40 + im.height], outline="#C6BFB0")
sheet.save(out)
print(out)
