# Validity: selection, information, confounding, chance

**Core principle: there is no statistical method that can determine the causal story from the data alone.**

Two tables of identical numbers:

|  | Drug | No drug |
|---|---|---|
| Men | 81/87 (93%) | 234/270 (87%) |
| Women | 192/263 (73%) | 55/80 (69%) |
| **Combined** | 273/350 (78%) | 289/350 (83%) |

|  | Drug | No drug |
|---|---|---|
| Low BP | 81/87 (93%) | 234/270 (87%) |
| High BP | 192/263 (73%) | 55/80 (69%) |
| **Combined** | 273/350 (78%) | 289/350 (83%) |

In the first, sex is a **confounder**, so the stratified result is correct. In the second, the drug works by lowering blood pressure, so BP is a **mediator** and the combined result is correct. The numbers cannot tell you which. Only the causal story can.

## The map

| Gap | Bias | Definition |
|---|---|---|
| Target → source population | generalisability / transportability |; |
| Source → study population | **selection bias** | systematic error due to differences between the source population and the study population |
| Within the study population | **information bias** | systematic error due to misclassification of exposure, confounders or disease |
| Within the source population | **confounding** | non-exchangeability of the exposed and non-exposed |

Random error is separate: it is reflected in the confidence interval and shrinks as the study grows. Systematic error does not shrink with sample size.

## Selection bias

Any bias arising from the way study participants are selected, or select themselves, from the source population. In DAG terms it is **collider bias where the collider is participation in the study**. (Hernán uses "selection bias" for all collider bias; this course reserves it for selection.)

In an incidence or prevalence study, selection bias **will not occur with a 100% response rate**. It occurs when, for example, cases are more likely to participate than non-cases **and** this is related to exposure. In a case-control study it occurs when control sampling is related to exposure status; when controls are not representative of exposure in the source population.

### Named selection biases

| Bias | Mechanism | Usual direction |
|---|---|---|
| **Healthy-worker effect** | the employed are healthier than the general population | towards the null, or protective, for occupational exposures vs general-population rates |
| **Volunteer / self-selection** | participants differ systematically from non-participants | either; depends on whether selection relates to exposure |
| **Non-response** | response rate varies with exposure or outcome | either; **control determinants of response as confounders** |
| **Loss to follow-up** | attrition related to exposure, outcome, or both | either; differential attrition is the dangerous case |
| **Neyman / prevalence-incidence** | prevalent cases exclude those who died or recovered quickly | survivors are atypical; distorts exposure-disease association |
| **Referral / admission-rate (Berkson)** | hospitalisation depends on both exposure and disease | conditioning on admission creates association |
| **Exclusion of deceased cases** | fatal cases unavailable for interview | depends on whether exposure relates to fatality |

### Solutions

1. Achieve a 100% response rate, and in a case-control study sample controls at random from the source population.
2. **Control the determinants of selection as confounders in the analysis**; if response rates vary by social class, adjust for social class.
3. Assess the likely **size and direction** of the bias.

**The one case where it cannot be removed:** "other disease" controls where the other diseases are themselves directly caused by the exposure of interest.

**Worked generalisability case.** UK Biobank sent letters to 9.2 million people and recruited 500,000; a **5.5% response rate**. Low response reduces generalisability and creates potential for selection bias, though it does not automatically invalidate internal comparisons. (Fry et al., *IJE* 2017 analyses this.)

**Attrition needs a mechanism, not a label.** "Loss to follow-up was 55%" is not a finding. "Continued participation is strongly determined by outcome status, because people with worsening mental health stop responding" is. Then ask the concrete question: **how did those lost differ from those retained?**

## Information bias

Misclassification of exposure or disease. If misclassification of exposure is unrelated to disease (or of disease unrelated to exposure) it is **non-differential**; if related, **differential**.

**Non-differential → bias towards the null.** If you find an association despite non-differential misclassification, the true relative risk is **stronger** than observed. Therefore: *a positive finding cannot be dismissed by invoking non-differential misclassification.* Non-differential information bias cannot usually produce a false positive.

### Four documented exceptions to "towards the null"

1. **Specificity 100%, sensitivity < 100%** in case ascertainment: the **risk difference** is biased towards the null but the **relative risk is not**. (Identify only 50% of deaths, at random, and the ratio survives.)
2. **Multiple exposure categories**: bias may be *away* from the null for some categories.
3. **Misclassification of a positive confounder**: adjustment then only partially removes confounding, so the adjusted estimate is biased **away from the null** relative to what full control would give. Worked: paracetamol and asthma, crude OR 1.76, confounder-adjusted 1.41; where perfect confounder data might have given something nearer 1.0.
4. Other special structures.

**Differential → any direction.** Hence the design rule: *it is usually desirable to ensure information bias is non-differential, even if that means not using some information on one group.* Collect information the same way in the groups being compared.

### Differential ascertainment by data collector

A named information bias that field studies generate and almost never check for. Outcome ascertainment can depend on **who did the interviewing**, which clinic recorded it, or which site enrolled; and that varies with geography, cadre, training and workload.

The test is cheap and it belongs in every appraisal of primary field data: **tabulate the outcome rate by data collector, site or interviewer, within a single exposure stratum.** If it moves, you have found it. In one real gastroenteritis survey the attack rate among users of a single implicated water supply ran from 30.8% to 4.5% across five interviewer cadres; a six-fold spread inside one exposure group, with two wards recording zero cases in 256 people.

Direction: often **not signable without adjustment**, because the collectors are not randomly allocated to exposure groups; under-ascertaining cadres may cover the exposed areas, the unexposed areas, or both. That is exactly when it becomes the decisive threat: a bias you cannot sign is worse than one you can. Remedy: put collector in the model, report crude and adjusted side by side, and if the estimate is stable you have disarmed the largest objection to the study.

### Named information biases

| Bias | Mechanism | Direction |
|---|---|---|
| **Recall bias** | cases recall exposure differently from controls | usually away from the null. Cancer patients recall brief pesticide exposures from years ago; healthy controls do not |
| **Interviewer bias** | interviewer knows case status | usually away from the null; blind the interviewer |
| **Surveillance / detection bias** | the more-investigated group has more disease found | **raises the outcome in the more-surveilled group**: away from the null if that group is the exposed one and the exposure is harmful, **towards the null** if the exposure is protective (statin users who attend clinics more and so get more dementia coded) |
| **Lead-time bias** | earlier detection lengthens measured survival without changing death | apparent benefit of screening |
| **Length-time bias** | screening preferentially detects slow-progressing disease | apparent benefit of screening |
| **Regression dilution** | random error in a continuous exposure | towards the null |
| **Missing-indicator method** | a "missing" category for a confounder | leaves **residual confounding even under MCAR** |

## Confounding

Occurs when the exposed and non-exposed groups in the source population are not comparable because of inherent differences in background disease risk. Equivalently: **the exposure and the outcome have common causes**, and a confounder is a variable that can be used to block a backdoor path. Confounding can also be *introduced* by selection factors or by misclassification.

### The three criteria; necessary but not sufficient

A factor is a confounder if it is:

1. a risk factor for the disease **among the non-exposed**;
2. associated with the exposure **in the source population**;
3. **not** an intermediate step on the causal pathway.

Two ways to identify one, both used in practice:

- **Empirically**; stratify or adjust, and compare with the crude estimate (collapsibility).
- **By checking the conditions against the data, each in its correct subgroup**; the confounder–exposure association **among the controls**, and the confounder–outcome association **among the unexposed**.

### There is no statistical test for confounding

> The LRT or Wald test from a regression model tests whether a variable is a **risk factor**. It does not test whether the variable is a **confounder**. It tests only the first of the three criteria.

> It is **invalid** to use significance testing to decide whether a factor is a confounder; an important confounder may not be statistically significant, and vice versa.

Worked proof. Crude RR for the main exposure 1.36; adjusted for sex, 1.00; clear confounding. Yet sex itself, as a risk factor, gives RR 2.0 with 95% CI 0.94–4.26, **p = 0.07**. A stepwise procedure would have dropped it.

Judge the **magnitude of the change**: 4.5 → 2.0 matters; 4.5 → 4.3 does not.

### Biases in treatment-effect studies

| Bias | Mechanism | Direction |
|---|---|---|
| **Healthy-user / healthy-adherer** | people who take preventive drugs also do other healthy things | towards apparent protection |
| **Confounding by indication** | the drug goes to those at higher (or lower) baseline risk | either way; name who gets the drug and why |
| **Protopathic bias / reverse causation** | early, undiagnosed disease changes who is prescribed or who adheres | towards apparent protection for a preventive drug |
| **Prevalent-user bias** | people already on a drug are survivors of its early harms | towards apparent protection |

### When biases point in opposite directions

Give each its own sign and say so. Do not average them. Then say which you judge to dominate and why, and what single piece of data would settle it (a negative-control outcome, a lag, a validation sample). If you cannot rank them, say "net direction not signable from the paper" and treat that as a finding. It is not a licence to skip the signing.

### Sizing a bias from the paper alone

When no bias analysis is reported, give an order of magnitude with its reasoning, not "large". Examples: immortal time scales with the share of follow-up spent before the exposure is defined; for an unmeasured confounder, ask what risk ratio it would need with both exposure and outcome to move the estimate to the null (the E-value idea), then ask whether any known factor is that strong.

### Direction of confounding

| Crude | Adjusted (both strata) | Direction |
|---|---|---|
| 3.0 | 1.6 | away from the null; **positive** |
| 0.4 | 0.75 | away from the null; **positive** |
| 3.0 | 4.1 | towards the null; **negative** (masking) |
| 0.4 | 0.25 | towards the null; **negative** (masking) |

**The trap: positive does not mean the crude estimate is numerically higher.** 0.4 is further from the null than 0.75, so that row is positive confounding. Always reason relative to 1.0.

- **Positive confounding is more common**, because risk factors tend to cluster together.
- Positive confounding risks a **false positive**; negative risks a **false negative**. Which error you would rather make depends on the public health question.
- **The rule worth keeping:** confounders are themselves measured with error, so adjustment is always incomplete. You should therefore be **more reassured that a surviving association is real when the confounding you found was negative.**

Worked case: oral contraceptives and myocardial infarction, crude OR 1.49, but stratum-specific ORs of 2.82 (age < 40) and 2.65 (age ≥ 40). Age was **masking** a strong association; negative confounding.

### Control and assessment

Control: **randomisation**, **restriction**, **matching** (see `design-options.md`; it buys precision, not validity), and **control in the analysis** (stratify, estimate within strata, summarise across strata → `occurrence-and-effect.md`).

When you cannot control it directly: adjust for **surrogates** such as social class; obtain confounder information on a **subgroup** and assess confounding there; and **bound the likely size**.

**Confounding is usually weaker than feared.** In 16 studies of lung cancer and occupation, crude and smoking-adjusted relative risks barely differ (1.5 vs 1.6; 2.2 vs 1.9; 5.1 vs 8.9; 2.8 vs 2.3). It is unreasonable to assume a strong association could be explained by an unknown confounder, because to be a strong confounder a factor must be **both** a very strong risk factor **and** strongly associated with exposure.

### Conditioning can induce bias, not only remove it

Adjusting for a baseline covariate can open a path rather than block one. In the worked case, adjusting for alcohol intake, a collider between unmeasured allergies and unmeasured risky behaviour, turns a null association between green vegetables and stomach cancer into an apparent protective effect.

But keep the honest caveat, because it is the seam with `causal-inference`:

> It is rare to find situations as simple as this in which adjusting for a variable is clearly harmful. More typically, adjusting may be beneficial for blocking some paths whilst **simultaneously opening others**. In these cases, a judgement about the **relative strengths of these paths** may be required.

That is sign-and-size applied to a diagram. Two further consequences: a DAG tells you **what data to go and collect** (here, allergies); and DAGs are *"not a get out of jail free card"* but a tool for making reasoning hygienic and transparent to others.

**Data can arbitrate between candidate DAGs.** In a case-control study with true exposure E, reported exposure E\* and disease D: conditional on E there should be **no** association between E\* and D unless an arrow D→E\* exists. If one is observed, recall bias is present, the no-recall-bias diagram is ruled out, and the **crude** analysis (OR 1.73) is correct while adjusting for E\* distorts it.

### What DAGs are and are not good for

| Good at representing | Not good at representing |
|---|---|
| confounding | **non-differential** information bias |
| collider bias, including selection bias | **effect modification** |
| **differential** information bias | **the likelihood, direction and strength of the possible biases** |
| mediators | sampling variation |

Limitations named in the course: model complexity; drawing the "right" DAG is an artform; magnitude and direction are not represented; "collider anxiety"; "analysis paralysis".

## Effect modification

**Confounding and effect modification are completely separate phenomena. You can have one, the other, both, or neither.**

| | Confounding | Effect modification |
|---|---|---|
| How to assess | compare **crude with adjusted** | compare **stratum-specific estimates with each other** |
| Status | a nuisance to be removed | may be of interest in its own right, with policy implications |
| Statistical test | **none exists** | one exists, but with low power and a high false-positive rate |

**Order of operations; against most textbooks.** Assess confounding and obtain summary effect measures **first**, then assess a-priori effect modifiers.

> Many textbooks and courses recommend the opposite approach; consider effect modification first, and present summary estimates only if there is no significant modification. However, this approach, which is more consistent with predictive modelling than with causal modelling, leads to many problems including **false-positive tests for interaction**.

A summary adjusted estimate is always calculable and represents the **average** effect in the study population. But if an exposure has no effect in one subgroup and increases or decreases risk in another, present the strata. When the direction is the same in all subgroups, whether to present strata is a judgement.

### It depends what you mean by "effect"

Lung cancer rates per 1000:

|  | Asbestos exposed | Asbestos non-exposed |
|---|---|---|
| Smokers | 35 | 10 |
| Non-smokers | 5 | 1 |

| Who | Measure | Exposed | Non-exposed | Modification? |
|---|---|---|---|---|
| Biostatistician 1 | risk ratio | 7.0 | 10.0 | Yes, **negative** |
| Biostatistician 2 | risk difference | 30/1000 | 9/1000 | Yes, **positive** |
| Clinician | risk to patient (RD) | 30/1000 | 9/1000 | Yes, positive |
| Public health | risk to population (RD) | 30/1000 | 9/1000 | Yes, positive |
| Lawyer | probability of causation, (RR−1)/RR | 86% | 90% | Yes, negative |

Same numbers, opposite conclusions.

**Formal position:** effect modification should be assessed as departure from **additivity** (a risk difference measure). However it is generally preferable to *use* a relative risk measure; better statistical properties, easier to report, often less modification across strata, and easier to assess confounding and other biases. **Resolution: print the joint-effects table** so readers can apply whichever definition of effect they need. The four joint categories can be estimated by fitting an interaction term, or by making a single four-level variable with the doubly-unexposed as reference.

### Scale choice can reverse a policy conclusion

Standardised mortality ratios for people with diabetes, by age at diagnosis:

| Age | SMR | Excess death rate per 100,000 |
|---|---|---|
| < 40 | 10.24 | 934 |
| 40–49 | 7.12 | 3,007 |
| 50–59 | 5.00 | 4,854 |
| 60–69 | 3.65 | 7,996 |
| 70–79 | 2.42 | 10,814 |
| 80+ | 1.61 | 10,504 |

On the **multiplicative** scale the effect shrinks with age (negative interaction) → prioritise the young. On the **additive** scale the excess death rate rises (positive interaction) → prioritise the old. Same table, opposite policy. Report both.

(The declining SMR itself has a rival explanation: **depletion of susceptibles**; heterogeneity in frailty means later age groups are on average less frail.)

## Time-related and missing-data biases

Sign and size each one. These are the ones a reader most often meets in cohort and routine-data studies.

### Immortal-time bias

Exposure is defined by something that happens after follow-up starts (a prescription filled, a landmark survived). The time before that event is counted as exposed, yet the outcome could not have happened in it. **Direction: away from the null, towards a spurious protective effect of the exposure.** Size grows with the length of the immortal stretch relative to total follow-up. Fix: start the clock at exposure (new-user design), treat exposure as time-varying, or use a landmark analysis. A "target trial" framing (eligibility, treatment assignment and time zero all aligned) prevents it by design; the formal emulation machinery belongs to `causal-inference`.

### Competing risks

When death from another cause removes people from the at-risk pool, treating it as censoring makes Kaplan-Meier risk **too high** (it assumes those people could still have the event). Use cumulative incidence with the competitor named. Ask which question is wanted: the rate among those still at risk (cause-specific hazard) or the absolute risk in the real population (cumulative incidence). They can point in different directions.

### Missing data

Name the **mechanism** (completely at random, at random given observed variables, or not at random) and the **fraction**. Complete-case analysis is unbiased only when missingness is unrelated to the outcome given the model covariates. If missingness depends on outcome status, give the direction by asking who is missing: sicker people missing from follow-up usually bias risk **downwards**. Imputation helps for "at random" only. Report the amount missing per variable, and a sensitivity analysis under a plausible "not at random" scenario.

## Chance

**The purpose of significance testing is to reach a decision on the basis of a single study. Decisions should be based on information from all available studies**, and should also involve non-statistical considerations such as plausibility and coherence with current knowledge.

P-values and confidence intervals **do not** account for mis-specification of the statistical model, nor for uncertainty due to selection bias, information bias or residual confounding. They address random error only.

### The named errors

- an almost complete focus on the p-value rather than the point estimate and interval
- describing associations as "strong" or "weak" based on the p-value rather than the estimate
- using a likelihood-ratio test to assess confounding instead of looking at the change in the estimate
- thinking an association has "disappeared" because adjustment produced a small change and the interval now includes the null
- saying "there was no association" when there is a substantial one with a non-significant p-value
- saying two studies are inconsistent when they have similar point estimates but one interval crosses the null

Worked case: Brown et al., *JAMA* 2017; antidepressants in pregnancy and autism. Cox adjusted HR 1.59 (1.17–2.17); after IPTW, 1.61 (**0.997**–2.59). Reported as "not associated", despite a near-identical point estimate and two meta-analyses around 1.7.

### Alternatives

- **The confidence interval**; though in practice people merely check whether it crosses the null.
- **The p-value function**; the whole curve rather than one point.
- **The s-value**, s = −log₂(p): the number of heads in a row from a fair coin carrying the same surprise. p = 0.10 → s = 3.3; p = 0.01 → s = 6.6. Useful because it makes the evidential weight of a p-value feel as modest as it is.

## Design is always a compromise

Better exposure information may reduce information bias but **increase random error** if it shrinks the study. Summary:

- reduce random error by making the study as large as possible and through appropriate design
- minimise selection bias with a good response rate and appropriate control selection
- ensure information bias is **non-differential** and keep it small
- minimise confounding by design and control for it in the analysis
