---
name: district-risk-tiers
version: 0.1.0
description: >
  Use when ranking districts or sub-districts into High, Moderate and Low tiers from hazard and vulnerability scores,
  or when asked to test, audit or explain such tiers. Covers a rule fixed before results, percentile ranks, what-if
  stability runs, logged deviations, a coverage check and an independent rebuild.
allowed-tools: Read, Write, Edit, Bash
---

# District risk tiers

Policy documents rank areas into High, Moderate and Low and then act on the ranking. This skill makes that ranking defensible. The rule is written and dated before any result is seen. Every change after that is logged. A fresh agent rebuilds the tiers from the written rule alone.

Core principle: the rule comes first, the results second, and every change after results is a logged deviation.

A tier is a relative rank from a screen. It is not a forecast and not a level of danger. Say so wherever tiers appear.

## Pairs with

- numbers-audit: this skill writes the files (tiers, stability, counts). Add one numbers key per headline count, then hand the draft to numbers-audit.
- health-policy-brief: wording for officials. This skill sets the constraint (stability beside every High, "consistent" and "less certain" labels). Then hand the document over.
- peer-reviewer: reviews the method as a manuscript, after this skill.
- spatial-epidemiology (if installed): point-in-polygon assignment, contiguity, small-area models. Upstream of this skill.
- survey-analysis (if installed): design-based survey estimates (strata, PSU, weights) for vulnerability inputs. Upstream.
- targets-workflow (if installed): where functions live, and how to invalidate a stale figure target.
- dataviz or ggplot-publication (if installed): colour and style. The only colour rule kept here is one colour family per quantity.

## When to use

- A document ranks districts, blocks or mandals and acts on the tiers.
- Someone asks "is this ranking robust?", "audit these tiers", or "why is X High?".
- A tier map must show hazard, vulnerability and risk side by side.

Do not use it to choose indicators or weights for the user (record the user's choice), to fetch or clean hazard or survey data (upstream), or to check numbers in prose (numbers-audit).

## Iron rules

1. Write the rule file and date it before any tier is computed. Mark every assistant choice "my call".
2. Hazard and risk are different words. A tier built from hazard times vulnerability is a risk tier. Never label it hazard.
3. Every High shown to a reader carries its stability label next to it.
4. A change to the rule after any result is seen is a deviation. Log what, why and what changed.
5. The audit agent gets the rule file and the input files only. It does not read the project code.
6. State how ties break before you cut into thirds. Default: higher score, then higher stability, then name. A project may choose another rule, but must write it down.
7. State what the score is not (not a forecast, not tested against outcomes) wherever it is shown.
8. A score may be called "children and mothers" only if it has indicators for both.
9. Stability is a robustness check against the listed runs. It is not a confidence interval. Say so.

## Order of steps

1. Ask: the unit of analysis, the groups the document names, the hazards available, the vulnerability indicators available, and the tier cut. Thirds is the default. Fixed thresholds (for example official forecast classes) are also valid: then replace `tier3()`, and say so in the rule.
2. Write the rule file from `references/rule-template.md`. Get approval. Record the date.
3. Run the coverage check (`references/coverage-check.md`) on the planned vulnerability score. Add the missing indicators, or narrow the claim, before you compute.
4. Compute: `source("scripts/tiers_core.R")`, write a spec, call `run_all_tiers()`, then `qc_tiers()`. Stop on any failed check.
5. Read the stability. Choose runs that differ in kind (another data source, another weighting), not only drop-one runs. List what each run changes.
6. For sub-areas with their own hazard data, call `inherit_tiers()` (`scripts/inherit_tiers.R`). They take the parent vulnerability. Mark them provisional.
7. Make the maps with `scripts/biv_map.R`. One colour family per quantity. Show the hazard-only map beside the risk map.
8. Independent audit: spawn a fresh agent with `references/audit-prompt.md`. Optional cross-check: `Rscript scripts/rebuild_check.R spec.json inputs.csv tiers.csv`. This does not replace the agent.
9. Log deviations and add a "notes after the audit" section to the rule file. Fix rule gaps (ties are the usual one).
10. Hand the headline counts to numbers-audit.

## The score

- Percentile rank of each input across the units (0 lowest concern, 1 highest). `dir = -1` flips a measure where lower is worse.
- Hazard score: mean of the ranks of its inputs. Vulnerability score: mean of the ranks of its inputs. A unit with a missing vulnerability input is "Data too thin".
- Risk for each hazard: geometric mean `H^w * V^(1 - w)`, default `w = 0.5`. Both must be high for risk to be high. This is a choice: say so.
- Overall risk: mean of the hazard risks. Tiers: top third High, middle third Moderate, last third Low.
- Exposure (people or births) can order units inside a tier. Keep it out of the score unless the rule says otherwise.

## Stability runs

- Each run changes one choice and reruns the tiers. Stability is the share of runs in which a unit keeps its base tier.
- Label: "consistent" if stability is at least 0.75, else "less certain". Show these words to readers. Keep the data values unchanged.
- Useful runs: another data source for a hazard, another weighting of hazard against vulnerability, vulnerability without one indicator, hazard from one metric only.
- A warning: drop-one runs are not independent and some change no tier. Report "consistent under these runs", not "confident".
- Name the runs and the number of runs next to the label. "8 of 10 what-if runs" reads better than "80%".

## Inheritance

When sub-areas have no vulnerability data of their own, they take the parent value. Use one scale across all sub-areas. Sub-areas of one parent then differ only by hazard, so their tiers are provisional. Flag sub-areas that share a grid cell with a neighbour, and units whose boundary file does not match the official list.

## Red flags

| Thought or sign | Fix |
|---|---|
| The map says hazard but the input column is `tier_*` or `R_*` | Those are risk tiers. Build from `H_*` scores or relabel. `biv_map()` stops on this. |
| Two risk maps look alike | Mandals in one district share a vulnerability value. Show the hazard-only map beside the risk map. |
| Two panels, one colour family | One family per quantity. |
| The rule is silent on ties | Add the tie rule and rerun. A fresh auditor finds this first. |
| The run in the code is not the run in the rule (for example a "5 km buffer" run that drops clusters) | Rename the run or log a deviation. |
| Stability looks like a confidence level | It is a check against listed runs. Say so. |
| The document names a group the score does not cover | Run the coverage check. Add indicators or narrow the claim. |
| A count of "two or more sources" is claimed for a hazard | Check each hazard against its input list. |
| Caveats in the rule differ from the text shown with the tiers | Copy the limits list wherever tiers appear. |
| A figure did not change after a code change (`targets` says "skipped") | Invalidate the figure target, then rebuild. |
| Readers meet "firm", "borderline" or "re-runs" | Show "consistent", "less certain", "what-if runs". |

## What the audit must report

The fresh agent rebuilds the tiers, the stability and the counts from the rule and the input files. It reports MATCH or DIFFERENT for each check, lists every gap in the rule (ties, undefined thresholds, runs the rule does not describe), and lists claims in the document that the files do not support. See `references/audit-prompt.md`.

## Common mistakes

- Trying several weightings and calling the best match "the rule". Record extra weightings as what-if runs.
- Calling a score "mothers and children" with child indicators only.
- Showing a High with no stability label.
- Letting file order decide a tie.
- Fixing the rule after the map looks wrong, with no log entry.

## Platform compatibility

Environment-dependent. The scripts need R (dplyr, purrr, tibble; jsonlite for `rebuild_check.R`; sf, ggplot2 and patchwork for `biv_map.R`). The method and the audit prompt run on any chat model. Claude Code: place this folder under `~/.claude/skills/`. Other assistants: paste SKILL.md and the reference files, and run the scripts locally.

## Version history

- 0.1.0 (2026-11-14): First release. Built from a health policy report that ranked 33 districts and 632 mandals. Tested on synthetic data.
