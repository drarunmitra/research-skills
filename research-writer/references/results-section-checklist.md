# Results section: conventions checklist

Source: MRU Workshop on Manuscript Preparation and Research Communication, Day 2 "Writing the Results Section: Text, Tables & Figures" (Dr Arun Mitra, AIIMS Bibinagar; github.com/drarunmitra/MRU_Workshop_Results). Use alongside the main skill patterns 10-12 and 23.

## Three load-bearing principles
1. **Methods-Results mirror.** The Results section mirrors the Methods paragraph-for-paragraph: participant flow first (screened → eligible → enrolled → analysed), then outcomes in the same order the Methods named the variables. A reader should be able to verify that what was planned was what was executed.
2. **The complete statistical result has four components:** direction, magnitude (effect size), precision (95% CI), and the exact p-value. "OR was 2.1" is incomplete; "OR 2.1 (95% CI 1.3-3.4)" is minimally acceptable; "OR 2.1 (95% CI 1.3-3.4; P = 0.003)" is complete.
3. **One home per finding.** Each finding lives in exactly one place (text, table, or figure), cross-referenced elsewhere. Numbers to read precisely → table. Patterns to see instantly → figure. Headlines and context → text. Nothing lives in two homes.

## Text vs table vs figure (decision framework)
| Scenario | Home |
|---|---|
| Single key number (one prevalence) | Text |
| Baseline characteristics across groups | Table |
| Participant flow | Flow diagram (CONSORT/STROBE/STARD/PRISMA) |
| Multiple point estimates with CIs | Table |
| Subgroup effect sizes | Forest plot |
| Survival / time-to-event | Kaplan-Meier curve (+ risk table) |
| Diagnostic performance across thresholds | ROC curve (+ 2x2) |
| Distribution of a continuous variable (small n) | Dot or box plot, never a bar chart |

## Prose style (Results report observations, not interpretation)
- Begin with participant accounting (denominators for everything that follows; losses/exclusions with reasons).
- Forbidden in Results: "because", "suggesting", "due to", "important", mechanisms, clinical significance, implications. These belong in Discussion.
- Forbidden: Methods in Results ("we used a chi-square test to..."). Report the finding, not the test.
- No data dump: do not narrate every table row. Give the headline, point to the table. "Participants had a mean age of 42 years and were predominantly male (58%); comorbidity was common (Table 1)."
- Introduce every table/figure in one sentence naming its purpose, then cross-reference by number, in numerical order. Never leave a display uncited.
- Internal consistency: text n = table n = flow-diagram n; percentages sum to 100 (note rounding). Reviewers check arithmetic first.

## Statistical reporting
- Exact p-values, never thresholds ("P = 0.003", not "P < 0.05"). Only exception: "P < 0.001" for very small. Never "P = 0.000" (software artifact). AMA style drops the leading zero ("P = .003").
- A point estimate without a CI is incomplete.
- Report absolute AND relative effects between groups: "reduced infection by 6.2 percentage points (12.1% vs 18.3%; RR 0.66, 95% CI 0.48-0.91; P = 0.01)."
- Report ALL pre-specified outcomes, significant or not (selective reporting is bias).

### Design-specific measures
- **Cross-sectional:** prevalence with 95% CI (weighted + design effect if complex sampling); adjusted ORs; "associated with", never "caused".
- **Case-control:** odds ratios only (never risk ratios); conditional logistic if matched; exposure distribution by case/control.
- **Cohort:** person-time, median follow-up (IQR), % lost; incidence rates; hazard ratios with CIs; KM curves with risk tables; competing risks if relevant.
- **Diagnostic:** explicit 2x2 (TP/FP/TN/FN); sensitivity/specificity/PPV/NPV/LR+/LR- all with 95% CIs; ROC + AUC; STARD flow for indeterminates; accuracy by disease spectrum.
- **RCT:** CONSORT flow + registry number (CTRI in India); intention-to-treat primary, per-protocol as sensitivity; absolute + relative effects; NNT/NNH; NO baseline p-values in Table 1; harms table even if it "worked".

## Table 1 (baseline characteristics)
- Title ABOVE the table, stating population, setting, period.
- Continuous: mean ± SD (symmetric) or median (IQR) (skewed); always label which.
- Categorical: n (%) with explicit denominator.
- Consistent decimals; horizontal rules only (top, below header, bottom); NO vertical rules.
- Abbreviation footnote. Self-contained: title, headers, units, n, summary-measure definition, abbreviation key.
- **Baseline p-values:** RCT → none (randomisation makes them meaningless; CONSORT discourages). Observational → SMD column or group-comparison p as a balance measure, not a hypothesis test.

## Figures
- Maximise data-ink: remove 3-D, heavy gridlines, borders, redundant legends.
- The squint test: blur your eyes; if the main message disappears, it is too busy.
- Direct labelling over external legends where space permits.
- Resolution: 300 dpi halftone/colour; 600-1200 dpi line art; TIFF/EPS; embed fonts; readable at column width. Confirm journal Instructions for Authors.
- Figure legend goes BELOW the figure (table titles go above).
- Flow diagrams: use official EQUATOR templates; show numbers at every decision point.
- Forest plot: estimates as squares/diamonds, CIs as horizontal lines, a vertical null line (OR/RR/HR = 1), ordered by effect or pre-specified priority, pooled estimate at bottom.
- KM curve: confidence bands, risk table below, log-rank p in the legend.
- ROC: AUC + 95% CI in legend, optimal operating point marked, supplement with the 2x2.
- Continuous data small n: plot individual points (jittered) with median/box overlay; never bar-and-error-bar.

## Workflow
1. List findings in Methods order (mirror). 2. Build displays (Table 1, outcome tables, figures) BEFORE prose. 3. Identify the 1-2 messages each display carries. 4. Write prose: flow first, then one paragraph per major finding pointing to its display. 5. Check the universal checklist below.

## Universal Results checklist
- First paragraph accounts for all participants (screened → analysed).
- Every finding has one home; every estimate has effect size + 95% CI + exact P.
- P as exact values, not thresholds. All pre-specified outcomes reported.
- Every table/figure cited in numerical order; all self-contained.
- No interpretation/causation/implications; no Methods description.
- Internal consistency: text n = table n = flow n.

## Coloured/complex tables
Colour-coded or heatmap tables (gt `data_color`): build in R with `gt`/`gtExtras`, export PNG (`gtsave(..., expand = 20)`), include with a `#tbl-` label. Plain summary/comparison tables: raw LaTeX booktabs + tabularx. See main skill Pattern 23.
