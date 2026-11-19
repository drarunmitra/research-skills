---
name: epi-thinking
description: Use when deciding what study design actually answers a question, choosing or interpreting a measure of disease occurrence or effect, judging how large and in which direction a bias is, working out what a routine or programme dataset can and cannot support, or appraising a study you are reading to decide what to believe and whether it applies to your population. Covers source population and risk period, case definitions, cohort / case-control / cross-sectional / ecological / trial / outbreak-investigation choice, control sampling and what the odds ratio estimates, matching and overmatching, prevalence vs risk vs rate vs attack rate, person-time, denominators, notification versus incidence, attributable measures, target vs operationalised exposure and measurement error, selection and information bias, direction of confounding, effect modification on additive vs multiplicative scales, clustering and design effect, causal vs predictive modelling strategy, and triangulation across studies. Triggers include "design a study", "what study design", "cohort or case-control", "what does this odds ratio estimate", "is prevalence the right measure", "attack rate", "outbreak", "epidemic curve", "surveillance data", "programme data", "routine data", "notification register", "is X rising", "is this a real increase", "what is the denominator", "case definition", "historical cohort", "retrospective cohort", "loss to follow-up", "healthy worker effect", "recall bias", "selection bias", "direction of confounding", "overmatching", "person-time", "design effect", "attributable fraction", "number needed to treat", "Bradford Hill", "triangulation", "should I believe this study", "critical appraisal", "is this effect big enough to matter". NOT for choosing an adjustment set or drawing a DAG (that is causal-inference), and NOT for judging a manuscript as a reviewer (that is peer-reviewer).
---

# Epidemiological thinking

**Core principle: never list biases. Always sign and size them.**

> "The important issue is not whether such biases are likely to have occurred (since they will almost always be present to some extent), but rather **what their direction and strength is likely to be, and whether they taken together could explain the observed association**." Pearce, *A Short Introduction to Epidemiology*, ch. 13

Everything else follows from two frames.

**One frame for all designs.** All epidemiological studies are based on a particular population (the **source population**) followed over a particular period of time (the **risk period**). Designs differ only in *how the source population is defined and how information is drawn from it*. They are sampling schemes on one underlying picture, not a hierarchy.

**One map for all biases.**

| Gap | Bias |
|---|---|
| Target population → source population | (lack of) generalisability / transportability |
| Source population → study population | **selection bias** |
| Within the study population | **information bias** (misclassification of exposure, confounder or disease) |
| Within the source population | **confounding** (non-exchangeability of exposed and non-exposed) |

## When to use

- Choosing a design, or working out what design a study actually is
- Deciding what to measure, in what denominator, over what risk period
- Interpreting a risk, rate, odds, prevalence or attributable measure
- Judging the direction and size of a bias, yours or someone else's
- Appraising a study you are reading, to decide what to believe
- Writing epidemiological framing into teaching material

**Not for:** drawing a DAG or choosing an adjustment set (`causal-inference`) · feedback loops (`thinking-in-systems`) · how many participants (`power-sample-size`) · a dataset in hand needing objectives and table shells (`data-to-report`) · whether the data are usable at all (`data-quality-report`) · judging a manuscript as a reviewer or author (`peer-reviewer`) · qualitative designs (`qual-researcher`).

Two seams matter most:

> Appraising a manuscript you are reviewing or about to submit is `peer-reviewer`; that skill produces an editorial recommendation against a reporting guideline. **This skill appraises a study you are reading**, to decide what to believe and whether it applies to your population.

> `causal-inference` decides **which** variables belong in the model. This skill decides **what the study is**, **what the numbers mean**, **how big the biases are**, and **how to build, defend and report the model**.

**Mandatory handoff.** When asked what to adjust for, which covariates to include, or whether a particular variable is a confounder, **say that the formal adjustment set belongs to `causal-inference` and route it there; then supply the epidemiological content of that DAG**: which candidates are confounders, which are mediators, which are colliders, which cannot be measured at all, and the expected **direction** of each. Do not silently answer the adjustment-set question yourself.

## Three lanes

**Lane A: design a study.** Before any method is chosen.

1. State the question as exposure + outcome + **target population** → `design-options.md`
2. Name the **source population** and the **risk period**. If you cannot, stop. → `design-options.md`
3. Choose the design from the question, not from a hierarchy. For a case-control study, derive it: ideal trial → corresponding cohort → corresponding case-control. → `design-options.md`
4. Define the target exposure, then how you will operationalise and measure it → `exposure-measurement.md`
5. Choose the occurrence measure and its denominator → `occurrence-and-effect.md`
6. Anticipate the biases **with directions**, and design against the strongest one → `validity.md`
7. Decide the modelling strategy a priori, and say so → `modelling-strategy.md`
8. Size it → `power-sample-size`

**Lane B: appraise a study you are reading.** → `appraisal.md`, which carries the output contract, the question sets, and the worked calibration example.

**Lane C: put epidemiology back into teaching material.** → `teaching-lane.md`

## Quick reference

**Designs** (Pearce 2012). Directionality is *not* a classifying feature.

|  | Not sampled on outcome | Sampled on outcome |
|---|---|---|
| **Incidence** | incidence (cohort) studies | incidence case-control studies |
| **Prevalence** | prevalence studies | prevalence case-control studies |

Plus cross-sectional and longitudinal studies with continuous outcomes, and descriptive / ecological comparisons.

**Occurrence**

| Measure | Numerator | Denominator | Note |
|---|---|---|---|
| Incidence risk (cumulative incidence) | new cases | persons at risk | cannot be estimated directly with substantial losses |
| Incidence rate | new cases | person-time at risk | cases leave the at-risk pool |
| Incidence odds | cases | non-cases at end | non-collapsible; do not use as a cohort outcome |
| Prevalence | existing cases | population at a point in time | P/(1−P) = I × D |

**What a case-control odds ratio estimates depends on how controls were sampled**; cumulative → odds ratio; case-cohort → risk ratio; density → rate ratio. No rare-disease assumption is needed for any of them.

## The Epi-Reasoning Lint

Run this before presenting anything.

1. Have I named the **source population** and the **risk period**?
2. Is the outcome incidence or prevalence, and does the **denominator match the claim**?
3. For every bias I named, did I give a **direction** and a rough **size**? An unsigned bias is not a finding.
4. Did I name **at most five** threats, rank them, and mark one **decisive**?
5. Did I ask whether the effect is **big enough to matter**, on the outcome's own scale?
6. Where I found confounding, did I sign it **positive or negative relative to the null**, remembering that 0.4 is further from the null than 0.75?
7. Did I check whether the authors' stated **remedies actually address** the biases they name?
8. Did I record what the study **does not report** as a finding, rather than assuming it was fine?
9. Did I check **who collected the data**, and whether the outcome rate varies by collector, site or interviewer? Differential ascertainment hides inside a single exposure stratum.
10. Are the observations **independent**? Households, clusters, repeat episodes and secondary cases all break it; report the design effect rather than ignoring it.
11. Where several studies agree, did I check whether they **share** the bias, and name anything intractable across all of them?
12. Did I use a **p-value to decide whether something is a confounder**? Delete it.
13. Did I say "no association" because a CI crossed the null while the point estimate was substantial? Did I call two studies inconsistent when their point estimates agree?
14. Did I assess **confounding before effect modification**?
15. Have I reached a **verdict**, said what would change it, and said what this estimate does **not** show?

## Output contract

Lane B produces, in this order:

1. The **eight-row appraisal table**: research question · study population / cohort definition · exposure and method of assessment · outcome and method of assessment · follow-up · analytical approach including covariates · key findings · strengths and limitations.
2. **Ranked threats**, at most five, one marked decisive, each with a direction.
3. A **verdict** in the first person: do I believe this estimate, does it apply to my population, and what would change my mind.

Filling the table is the working, not the deliverable. If more than five real problems exist, group by root cause and list the overflow as "Also noted" (see `appraisal.md`). The cap of five is a ceiling, not a target; a good study gets a short list.

## Reference files

| File | What is inside |
|---|---|
| `design-options.md` | Source population and risk period; the design taxonomy; deriving a case-control study; control sampling and what the OR estimates; matching and overmatching; cohort design in five questions; trials; ecological and descriptive studies; why "historical cohort", never "retrospective cohort" |
| `occurrence-and-effect.md` | Risk vs rate vs odds vs prevalence and their denominators; P/(1−P)=I×D; RR, rate ratio, OR; attributable measures and PAF and NNT; pooling vs standardisation vs maximum likelihood; matched analysis arithmetic |
| `exposure-measurement.md` | Define target → operationalise → measure; the four target-exposure questions; biomarker ladders; five measurement modalities; quantifying measurement error with sensitivity, specificity, PPV and NPV; direction of measurement bias |
| `validity.md` | The three-population map; immortal-time, competing-risk and missing-data biases with directions; named selection and information biases with directions; confounding criteria, the no-statistical-test doctrine, and the direction taxonomy; effect modification and scale; chance and p-values; when conditioning induces bias |
| `modelling-strategy.md` | Description vs prediction vs causal inference; why stepwise fails; sparse data and the rule of 10; the confounding-vs-multicollinearity 2×2; RMSE; the four-model algorithm; where p-values legitimately belong; reporting |
| `appraisal.md` | The two-question interpretation framework; the magnitude question; appraisal question sets for cohort, case-control, exposure and interaction; triangulation as a procedure; Bradford Hill; the fenoterol worked example |
| `teaching-lane.md` | Lecture-to-practical bridge; reusable framing and closing blocks; per-practical prescriptions for the IISc/LSHTM R practicals |

## Common mistakes

| Mistake | Why it's wrong | Fix |
|---|---|---|
| Listing biases | A list has no direction and no size, so it cannot change a conclusion | Sign and size at most five, rank them, mark one decisive |
| "Retrospective cohort" | Describes when the investigator arrived, not the design; the data were usually collected prospectively | Say **historical cohort**; reserve "retrospective" for retrospective *collection* of exposure information |
| Using a p-value to test for confounding | Tests only whether the variable is a risk factor, which is one of three criteria | Compare crude with adjusted and judge the change |
| "No association" when the CI crosses the null | The point estimate may be substantial and consistent with prior studies | Report the estimate and interval; compare with previous evidence, not with the null |
| Treating the OR as needing a rare-disease assumption | What it estimates depends on how controls were sampled | Name the sampling scheme, then name what it estimates |
| Assessing effect modification before confounding | Predictive logic; produces false-positive interactions | Confound first, summarise, then test a-priori modifiers |
| Reporting only one scale for a joint effect | Multiplicative and additive can give opposite policy conclusions | Print the joint-effects table and let the reader choose |
| Calling a significant result important | Continuous outcomes are often well-powered; tiny effects reach significance | Translate onto the outcome's own scale or into absolute risk |
| Trusting agreement across studies | They may share the decisive bias | Tabulate studies × biases; credit only where biases differ |
| Matching to remove confounding | It does not; it can introduce confounding | Match for precision only, then adjust for what you matched on |

## Related skills

`causal-inference` (DAGs, adjustment sets, g-methods) · `thinking-in-systems` (feedback loops) · `power-sample-size` (sizing) · `data-to-report` (analysis plan from a dataset in hand) · `data-quality-report` (is the data usable) · `peer-reviewer` (manuscript judgement) · `qual-researcher` (qualitative designs) · `slides-creator-skill` (deck house style, for Lane C).

## Provenance

Distilled from the IISc / LSHTM short course *Concepts and Methods in Epidemiology* (Neil Pearce and Poppy Mallinson), read slide by slide including speaker notes, together with all seven exercise answer keys, and Pearce N, *A Short Introduction to Epidemiology*, 2nd edn, Centre for Public Health Research, Massey University, 2005. Where the course takes a position against mainstream teaching, assess confounding before effect modification; no statistical test for confounding, ever; matching buys precision not validity; the odds ratio needs no rare-disease assumption; percentage of variance explained is not an effect measure; there is no hierarchy of study designs, this skill keeps the course's position and says why.

Two of Mallinson's decks were rewritten for 2026 and the newer versions are the authority here: *Exposures* (34 slides, restructured around define → operationalise → measure, with a new section on quantifying measurement error) and *Cohort studies* (51 slides, restructured around five design questions).

**What these sources do not cover**, so the skill does not either: screening programme evaluation as a discipline; formal surveillance-system attributes; survival analysis mechanics; Bayesian methods; and the g-methods themselves, which are named but routed to `causal-inference`.

**Outbreak investigation is in scope**, though the course does not teach it directly. Tested against a real gastroenteritis investigation, the general machinery transferred without modification; source population and risk period, attack rate as a cumulative incidence with a stated denominator, exposures measured after the outcome, differential ascertainment by data collector, household clustering, risk ratios in place of odds ratios, and joint effects on both scales. Use it, and say plainly that the epidemic-curve and microbiological limbs of an investigation sit outside what this skill supplies.
