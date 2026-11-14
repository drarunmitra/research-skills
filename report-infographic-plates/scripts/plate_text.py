#!/usr/bin/env python3
"""Extract the visible text of each plate (HTML) into one text file per plate, one text node per line,
so the number checker can test every number on every plate.

Usage: python plate_text.py [html_dir] [text_dir]
Defaults: report/infographics/html  report/infographics/plate_text
Prints: "N files". Skips <style>, <script> and <title>.
"""
import os
import sys
import glob
from html.parser import HTMLParser

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join("report", "infographics", "html")
DST = sys.argv[2] if len(sys.argv) > 2 else os.path.join("report", "infographics", "plate_text")
os.makedirs(DST, exist_ok=True)


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.out = []

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "title"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("style", "script", "title") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        t = " ".join(data.split())
        if t and not self.skip:
            self.out.append(t)


files = sorted(glob.glob(os.path.join(SRC, "*.html")))
for f in files:
    p = P()
    p.feed(open(f, encoding="utf-8").read())
    out = os.path.join(DST, os.path.basename(f).replace(".html", ".txt"))
    open(out, "w", encoding="utf-8").write("\n".join(p.out) + "\n")
print(len(files), "files")
