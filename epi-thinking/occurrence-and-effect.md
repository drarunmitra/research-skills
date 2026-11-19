# Measures of occurrence and effect

**Core principle:** the denominator is the claim. Choose the measure from the question and the follow-up, then say what it does and does not mean.

## Occurrence

Picture the source population over the risk period: lines running from start to finish, some ending in a case, some in death from another cause, some in loss to follow-up.

| Measure | Numerator | Denominator | Notes |
|---|---|---|---|
| **Incidence risk** (incidence proportion, cumulative incidence) | new cases | persons at risk | The probability that a person initially free from, and at risk of, the disease develops it during the observation period. Both numerator and denominator are **numbers of people**. **Cannot be estimated directly when there are significant losses to follow-up.** |
| **Incidence rate** (incidence density) | new cases | **person-time** at risk | The rate of contracting the disease among those still at risk; once a person contracts it they are no longer at risk. Numerator is people, denominator is person-years. |
| **Incidence odds** | cases | non-cases at the end | Has unfortunate statistical properties, particularly **non-collapsibility**, and is difficult to interpret. **Should not be used as an outcome measure in a cohort study.** |
| **Prevalence** | existing cases | population at a point in time | Number or proportion with the disease at a particular moment. |

**Attack rate** is an incidence risk under another name, used in outbreaks: new cases over the population at risk over the outbreak's risk period. Everything above applies. State the denominator (who was enumerated, not who was interviewed) and state the period; and if fieldwork ran over weeks, the risk period differs between households, so either truncate everyone at a common date or use person-time.

The joke that carries the point: *World Death Risk Holding Steady At 100 Percent*. Given long enough follow-up, every cumulative incidence tends to 1. A risk without a stated period is meaningless.

## Effect

| Measure | Definition | Alternative formulation |
|---|---|---|
| Risk ratio | (D₁/N₁) / (D₀/N₀) | (D₁/D₀) / (N₁/N₀) |
| Rate ratio | (D₁/Y₁) / (D₀/Y₀) | (D₁/D₀) / (Y₁/Y₀) |
| Odds ratio | [D₁/(N₁−D₁)] / [D₀/(N₀−D₀)] | (D₁/D₀) / [(N₁−D₁)/(N₀−D₀)] |

**For a rare disease all three are equal for all practical purposes. For a common disease they are different.** Which one a case-control study estimates depends entirely on how controls were sampled → `design-options.md`.

In a 2×2 with cases *a*, *b* and controls *c*, *d*: OR = ad/bc, reachable either as (a/c)/(b/d) or as (a/b)/(c/d). The second form is why a case-control study works: take all the cases and a **sample** of the non-cases, and the ratio survives.

## Prevalence decomposes into incidence and duration

Under steady-state assumptions:

> **P / (1 − P) = I × D**, and therefore **POR = I₁D₁ / I₀D₀**

**A difference in prevalence may be due to a difference in incidence, a difference in duration, or both.** This is the single most important caution about any cross-sectional finding.

Worked case: asthma prevalence is the same in Māori and non-Māori at age 14, but higher in Māori adults. Non-Māori lose the disease as they age and Māori do not. The adult difference reflects **duration**, not incidence.

Consequences for choosing incidence over prevalence: a longer-lasting condition with the same incidence looks more prevalent; the composition of prevalent cases is skewed towards the **less severe**, because those last longer; some conditions are only ever incident (mortality); and directionality of effect is known.

## Attributable measures

| Measure | Formula | Answers |
|---|---|---|
| Attributable risk (risk difference) | R₁ − R₀ | How much extra disease does exposure cause in the exposed? |
| Attributable risk per cent | (R₁ − R₀)/R₁, or (RR−1)/RR | What fraction of disease in the exposed is due to exposure? |
| Population attributable fraction | P(R₁−R₀)/R̄, or p(RR−1)/[1+p(RR−1)] | What fraction of disease in the whole population is due to exposure? |
| Number needed to treat | 1/(R₀ − R₁) | How many must be treated to prevent one case? |

Note that (RR−1)/RR is also the lawyer's **probability of causation**; see the five-stakeholder example in `validity.md`.

**The warning that must travel with these.** Two populations, identical rate ratio of 10.0:

| | Population 1 | Population 2 |
|---|---|---|
| Rate ratio | 10.0 | 10.0 |
| Correlation | 0.29 | 0.14 |
| % variance explained | 8.4% | 2.0% |
| PAF | 82% | 89% |

The effect is identical; the attributable fraction and the variance explained are not, because they depend on how much the exposure varies in that population. A factor can account for a large proportion of cases yet explain little of the population variation. Therefore **percentage of variance explained, correlation coefficients, standardised regression coefficients and interquartile-range comparisons are not usable as effect measures** → `modelling-strategy.md`.

## Summarising across strata

Three methods, with different assumptions.

| Method | Weights | Small strata | Assumes constant RR? | Estimates |
|---|---|---|---|---|
| **Pooling (Mantel-Haenszel)** | bᵢcᵢ/Tᵢ | robust | **Yes** | a weighted average of stratum-specific ratios |
| **Standardisation** (e.g. standardised rate ratio) | external or chosen standard | affected | **No** | ratio of weighted-average rates; the average risk |
| **Maximum likelihood** |; | less affected (unconditional), unaffected (conditional) | No | close to the SRR on the data's own stratum distribution |

**Precision (inverse-variance) weights are rejected**: they yield estimates that are unstable and highly affected by small numbers in particular strata.

Mantel-Haenszel weights are very close to statistically optimal and robust provided no stratum has a zero marginal total.

Because maximum likelihood and standardisation estimate an **average** risk, there is no problem presenting a summary estimate even when there is substantial effect modification; though see `validity.md` for when you should also present the strata separately.

**Practical ceiling:** it is usually not practicable to adjust for more than **three or four** potential confounders in a stratified analysis. Beyond that you need a regression model, and you accept the assumptions that models involve.

## Matched analysis

A matched analysis is a special stratified analysis in which **each case-control set is its own stratum**.

If you matched only on general variables such as age and sex, you do **not** need a pair-matched analysis; adjust for them in the usual way (Mantel-Haenszel, regression). If you matched on something specific; siblings, neighbours; retain the sets as strata.

For 1:1 pair matching there are four cell counts: n₁₁ (both exposed), n₁₀ (case exposed only), n₀₁ (control exposed only), n₀₀ (neither). The Mantel-Haenszel odds ratio reduces to:

> **OR = n₁₀ / n₀₁**

Concordant pairs contribute nothing. **We only get useful information from pairs where the case and control differ.** That is exactly why overmatching costs precision → `design-options.md`.

Note the sparse-data trap: 100 pair-matched sets means 99 stratum parameters and 100 cases, so unconditional logistic regression is invalid here. Only conditional likelihood and Mantel-Haenszel remain approximately valid → `modelling-strategy.md`.

## The observations are usually not independent

A risk or a rate assumes independent observations. Most real data breaks that:

| Source of dependence | Where it shows up |
|---|---|
| **Households** | outbreak surveys, cluster surveys, family studies |
| **Clusters** (hamlet, ward, village, school, clinic, TU) | anything sampled or delivered in groups |
| **Repeat episodes per person** | registers where someone can re-enter |
| **Secondary cases** | person-to-person transmission inside a household |

Consequence: the point estimate is usually fine, the **confidence interval is too narrow**. Quantify it rather than ignoring it; report the intracluster correlation and the **design effect** (roughly `1 + (m − 1)ρ` for clusters of size `m`), then widen the interval accordingly, or fit a mixed model or GEE clustered on the real unit. A household ICC of 0.33 with households of about three people inflates the variance by roughly 1.7, which is the difference between a defensible interval and an indefensible one.

Say which unit you clustered on and why. The unit is whatever the **exposure** was delivered to; a piped water scheme is a household-and-hamlet exposure, not an individual one.

## Reporting rules

- State the **period** with every risk, and the **person-time units** with every rate.
- Give the point estimate and confidence interval. Compare with previous studies, not with the null.
- For joint effects of two exposures, **print the full 2×2 table of joint effects**, so readers can apply whichever definition of "effect" they need.
- Say which measure the design could actually estimate, and why.
