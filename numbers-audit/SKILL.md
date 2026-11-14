---
name: numbers-audit
version: 1.1.0
allowed-tools: Read, Grep, Glob, Bash
description: >
  Use when a manuscript, report, abstract, or slide deck quotes numbers produced
  by an analysis pipeline, and those numbers must be provably correct, e.g.
  "check the numbers in this paper", "does every figure in the draft come from
  the analysis", "I reran the model, is the manuscript stale", "verify the
  results section", "build a claim-to-source table". Enforces that every result
  number in a document traces to a file the pipeline wrote, and catches numbers
  quoted from memory, invented, or gone stale after a rerun.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Auditing the Numbers in a Manuscript

## Overview

Proofreading catches prose errors. It does not catch a number that is internally
consistent, plausible, well-formatted, and wrong. Those come from three places:

1. **Memory.** You wrote the sentence from what you remembered the model said.
2. **Invention.** A number that sounds like a result but was never computed.
3. **Staleness.** You reran the analysis, an estimate shifted, and the draft
   still carries the old value.

All three survive rereading, co-author review, and usually peer review, because
nothing about them looks wrong.

**Core principle: every result number in the document must trace to a file the
pipeline wrote. Enforce it mechanically, not by reading.**

This is a *different* check from citation verification (does this reference
exist) and from claim-evidence audit (is this claim supported). Run all three;
they catch disjoint sets of errors.

## Pairs with

- **academic-writer** -- verifies citations; this skill verifies numbers. Adjacent, non-overlapping.
- **peer-reviewer** -- audits claims against evidence; this audits figures against files.
- **research-writer** / **thesis-writer** -- run this before handing a draft on.
- **reproducible-repo** -- the numbers table is itself a compendium artifact worth shipping.

## The two-script architecture

Do not try to do this in one pass or by hand.

```
build_numbers.R   reads the pipeline's OUTPUT FILES  ->  numbers.csv
check_draft.R     reads numbers.csv + the DRAFT      ->  pass / list of orphans
```

`numbers.csv` has four columns:

| column | meaning |
|---|---|
| `key` | short stable id, e.g. `scm.var.shared` |
| `what` | one line a human can read, e.g. "shared spatial variance with 95% CrI" |
| `value` | the number **as a formatted string**, e.g. `0.316 (0.230 to 0.440)` |
| `source` | the file it came from, e.g. `shared_component.rds` |

The builder never hardcodes a value. It reads the stored model object or CSV and
formats it. If a number cannot be produced by reading a file, it does not belong
in the paper.

### Builder sketch

```r
NUM <- list()
add <- function(key, what, value, source)
  NUM[[key]] <<- data.frame(key, what, value = as.character(value), source)

m <- readRDS("out/model.rds")
p <- m$summary.hyperpar["Precision for area", ]
add("var.area", "area variance with 95% CrI",
    sprintf("%.3f (%.3f to %.3f)", 1/p$mean, 1/p$`0.975quant`, 1/p$`0.025quant`),
    "model.rds")

readr::write_csv(do.call(rbind, NUM), "numbers.csv")
```

### Checker sketch

```r
draft <- readLines("manuscript.md")
num   <- readr::read_csv("numbers.csv")

# every numeric token that appears anywhere in the value column
pool <- unique(unlist(regmatches(num$value, gregexpr("[0-9]+\\.?[0-9]*", num$value))))

# every numeric token in the draft, ignoring code spans and link targets
body <- gsub("`[^`]*`|\\(https?://[^)]*\\)", "", paste(draft, collapse = "\n"))
tok  <- unique(unlist(regmatches(body, gregexpr("[0-9]+\\.?[0-9]*", body))))

allow <- c("1","2","3","4","5","6","10","15","95",           # structural
           as.character(1990:2030))                          # years
miss <- setdiff(tok, c(pool, allow))
```

Print `miss` with the line each token sits on, so the fix is one grep away.
Fail loudly. A checker that prints "done" on failure is worse than no checker.

## What actually goes wrong

These are the traps, in the order you will hit them.

**Rounding mismatch.** The file holds `0.3164`; the draft says `0.316`. Both are
right and the checker flags it. Fix in the *builder*, not the allow-list: emit
both precisions in the value string (`"0.316 / 0.3164 (...)"`). The value column
is matched by substring, so extra formats cost nothing.

**Range tokens.** `75.7–84.6` with an en-dash can tokenize to a stray `75`.
Decide once: either strip en-dashes before tokenizing, or allow-list the
fragments. Do not silently widen the regex until the count reaches zero.

**Structural numbers.** Years, section numbers, "more than 700 districts",
reference thresholds like the WHO 10–15% band. These are prose, not results.
Keep them in a short, explicit `allow` vector, and keep it short. Every entry you
add is a check you have switched off, so add the *specific* token, never a
pattern.

**The staleness trap, and it is the dangerous one.** Rerun a model and estimates
drift — a DIC by 0.2, a variance in the fourth decimal. The draft still reads
plausibly. **The file on disk is the single source of truth; sync the prose to
it, never the other way round.** If the builder and the draft disagree, the
draft is wrong by definition. This is the failure mode that a human reviewer
cannot catch at all.

**Two sources for one quantity.** The same variance computed by the main script
and again by a sensitivity script will differ slightly. Pick one as canonical,
cite it everywhere, and say in the builder which one it is.

## Also worth checking, same pass

Cheap, and they fail for the same reason:

- **Citation orphans.** Every `@key` in the draft is in the `.bib`, and every
  `.bib` entry is cited. Watch for false positives from email addresses
  (`someone@example.com` looks like a citation key).
- **Named examples.** "The fastest-rising districts are X, Y, Z" goes stale
  exactly like a number does. Give named examples their own table with the same
  key/what/value/source shape.
- **Cross-document consistency.** Supporting information, abstract and cover
  letter quote the same numbers as the main text. Run the checker over all of
  them against one `numbers.csv`.
- **Internal arithmetic.** If the text says "A rose from 40 to 55, a gain of
  16", the checker will pass all three tokens and miss the error. Where the
  draft states a derived quantity, compute it in the builder too.

## Verify before you hand it over

- The checker reports **0 unverified**, and you have read the allow-list to
  confirm nothing real is hiding in it.
- The builder runs clean from a fresh session — no objects inherited from the
  console.
- Every number in the abstract and conclusion is in `numbers.csv`. These get
  written last, edited most, and checked least.
- Ship `numbers.csv` with the paper. It is the claim-to-source table a reviewer
  or a reproducibility checker would otherwise have to build by hand.

## Common Mistakes

| Mistake | Reality |
|---|---|
| Check the numbers by reading the draft | The three failure modes all look correct on the page. That is what makes them dangerous. |
| Hardcode the value in the builder | Then the builder agrees with the draft and both are wrong. It must read a file. |
| Widen the regex until orphans hit zero | You have disabled the check, not passed it. Fix the builder or allow-list one specific token. |
| Edit the file to match the manuscript | The pipeline output is canonical. Always sync the prose to the file. |
| `str.replace` the draft and print "patched" | A silent no-op reports success. Use an editor that errors when the target is absent, or assert the match first. |
| Run it once, at the end | Run it after every rerun of any model. That is when staleness enters. |
| Skip the abstract | Most-edited, least-checked section in the paper. |

## Platform compatibility

- **Class:** Environment-dependent (needs a CLI/agent with a local shell)
- **Requires:** a local shell, plus R or Python to run the two scripts.
- **Load it on:**
  - Claude: drop into `~/.claude/skills/` (Claude Code), or paste this body into a Project's instructions (claude.ai).
  - ChatGPT: paste this body into a Custom GPT or Project. Needs Codex/agent mode with a connected environment for the shell steps.
  - Gemini: create a Gem from this body, or place it under the Gemini CLI. Needs the Gemini CLI for the shell steps.

## Notes from a policy report (Nov 2026)

- Check the rendered body (`keep-md: true`, the `.typst.md` file), not the `.qmd`. Tables and inline R only exist after rendering.
- Strip citation keys (`@munoz2021era5land`) and cross-reference labels before you tokenise. The years inside keys look like numbers.
- Layout values (`#v(1.6em)`, `out-width: "76%"`) are not results. Allow them for one run with an explicit, named extra list (for example an `ALLOW_EXTRA` environment variable), never in the permanent allow-list.
- Run the same checker over text pulled from infographic plates (extract the visible text of each plate HTML to a `.txt` file). Plates hold many numbers.
- When a figure function changes and `targets` says "skipped", run `tar_invalidate()` on that target, then `tar_make()`.
- A new number in the text needs a new row in the builder first (`key, what, value, source`). Add derived numbers with the formula in `source`.

## Version history

- 1.0.0 (2026-08-28): Initial release. Two-script builder/checker architecture,
  the four trap classes (rounding, range tokens, structural numbers, staleness),
  and the adjacent checks worth running in the same pass. Written after a
  Bayesian spatiotemporal manuscript where the harness caught four errors that
  had survived rereading: coefficients quoted from memory, a `+6.0` that was
  `+6.7`, an invented pair of percentages, and a stale list of states left over
  from an earlier model run.
- 1.1.0 (2026-11-14): Added notes from a policy report: check the rendered body, strip citation keys and layout tokens, trace plate text, targets invalidation.
