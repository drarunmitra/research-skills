# -*- coding: utf-8 -*-
"""
Run every {webr} cell in every primer, in page order, in one R session.

This is the only test that runs what the reader actually runs.

Why it is needed: `quarto render` never executes a `{webr}` cell. It parses the
page and ships the code to the browser. So a primer can render perfectly, deploy
green, and still fail at the first cell the learner presses Run on.

What it models:
  - quarto-live installs AND attaches every package named in `webr: packages:`
    before the first cell runs, so the script attaches them first.
  - quarto-live starts one webR worker per page, so all cells on a page share one
    global environment. Each page should build its data once, in its first cell;
    the later cells use it.

An `object not found` here is a page the reader cannot work through.

Usage:   python tools/run_cells.py
Needs:   Rscript on PATH, with the packages the primers declare.
Exit:    0 if every page runs clean, 1 otherwise. Safe to wire into CI.

Adjust PAGE_DIR and PAGE_PREFIX if your primers live elsewhere.
"""
import io, os, re, subprocess, sys, tempfile

PAGE_DIR = "prelude"
PAGE_PREFIX = "primer-"

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = tempfile.mkdtemp(prefix="cells_")

CELL = re.compile(r"```\{webr\}\n(.*?)\n```", re.S)
PKG = re.compile(r"^\s+- (\w+)$", re.M)

# Noise every tidyverse attach prints; not a failure.
NOISE = ("Warning", "masked", "Attaching", "The following", "conflict")

if not os.path.isdir(PAGE_DIR):
    print("no %s/ directory here; set PAGE_DIR" % PAGE_DIR)
    sys.exit(2)

fails = checked = 0
for f in sorted(os.listdir(PAGE_DIR)):
    if not (f.startswith(PAGE_PREFIX) and f.endswith(".qmd")):
        continue
    p = os.path.join(PAGE_DIR, f)
    s = io.open(p, encoding="utf-8").read()
    pkgs = PKG.findall(s.split("---")[1])
    cells = [m.group(1) for m in CELL.finditer(s)]
    if not cells:
        continue
    checked += 1

    script = ["# quarto-live attaches every declared package before cell 1 runs",
              "suppressPackageStartupMessages({"]
    script += ["  library(%s)" % pk for pk in pkgs]
    script.append("})")
    for i, c in enumerate(cells, 1):
        script.append('\ncat("---- cell %d ----\\n")' % i)
        script.append(c)

    rf = os.path.join(OUT, "cells_%s.R" % f[:-4])
    io.open(rf, "w", encoding="utf-8").write("\n".join(script) + "\n")

    r = subprocess.run(["Rscript", rf], capture_output=True, text=True)
    bad = [l for l in r.stderr.strip().split("\n")
           if l.strip() and not any(n in l for n in NOISE)]
    ok = r.returncode == 0 and not bad
    fails += 0 if ok else 1
    print("%s %-46s %2d cells, pkgs=%s"
          % ("OK  " if ok else "FAIL", p, len(cells), pkgs or "[]"))
    for l in bad[:6]:
        print("        ", l[:140])

print("\npages checked: %d   failing: %d" % (checked, fails))
sys.exit(1 if fails else 0)
