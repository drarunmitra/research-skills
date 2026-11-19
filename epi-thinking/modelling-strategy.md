# Modelling strategy

**Core principle:** decide first whether you are describing, predicting, or estimating a causal effect. The three have different rules, and almost every modelling error is a rule borrowed from the wrong column.

| Description | Prediction | Causal inference |
|---|---|---|
| Person, place, time | Aim is prediction | Estimate the causal effect of one or more variables |
| | Best predictors explain most of the variation | Requires epidemiological modelling approaches |
| | Want a **parsimonious** model that **fits well** | **Main exposure is always in the model** |
| | Includes standard regression, ML and AI | Control confounding, avoid multicollinearity |
| | | **No need for a parsimonious model** |

## Three lessons before any model is fitted

**1. Variation is not causation.** How much of the population variation in lung cancer would smoking explain if everyone smoked the same amount? None; yet smoking would still cause the same cancers.

| | Population 1 | Population 2 |
|---|---|---|
| Rate ratio | 10.0 | 10.0 |
| Correlation | 0.29 | 0.14 |
| % variance explained | 8.4% | 2.0% |
| PAF | 82% | 89% |

Any standard effect measure should be generalisable and should **not** depend on how much the exposure varies in the population. Therefore **percentage of variance explained, correlation coefficients, standardised regression coefficients and interquartile-range comparisons cannot be used as effect measures in an epidemiological study.**

**2. Prediction is not causation.**

| Predictive and causal | Predictive but not causal |
|---|---|
| smoking and lung cancer | cigarette lighter use and lung cancer |
| gin and liver disease | tonic and liver disease |
| LDL-C and cardiovascular disease | HDL-C and cardiovascular disease |
| vegetable intake and colorectal cancer | vitamin A and colorectal cancer |

More of the same: religious service attendance and lower mortality; antihypertensives and *higher* cardiovascular risk; screening colonoscopy and *higher* colorectal cancer; chemotherapy and more frequent recurrence; surgery and lower survival. Confounding by indication, and by the reason you were selected for the intervention.

HDL-C is the cautionary one: strongly and repeatedly associated with lower CVD risk, confounded by factors including an inverse association with triglycerides, and that confounding is effectively **intractable** by conventional adjustment. Trials and Mendelian randomisation show no effect, possibly harm.

**3. Prediction is not transportability.** Google Flu Trends predicted well, then drifted. **Even very good predictors need continual recalibration over place and time.**

Consequence: for **causal** modelling, ML and AI are in general not appropriate or relevant, except in specific roles such as advanced confounding control. If confounding is intractable, standard methods will not rescue it. For **predictive** modelling they may be appropriate, used carefully, with recalibration.

## Why stepwise regression fails for causal work

1. It makes decisions based on the **amount of variance explained** by each variable, which is directly equivalent to the p-value.
2. **If a variable does not vary much, the model decides it is unimportant**; even if it is causal.
3. **If two variables are highly correlated, it is essentially random which is selected**; smoking or cigarette lighter use.
4. **Stepwise regression does not evaluate confounders.** A strong confounder can be rejected for non-significance; a non-confounder retained for significance. If exposed and non-exposed have the same proportion of smokers, smoking is not a confounder even though it is a strong risk factor.

## Sparse data and the rule of 10

| Design | The count that must be ≥ 10 × number of parameters |
|---|---|
| Cross-sectional or case-control | number of people **with** (or without) the outcome |
| Cohort | number of **events** |

If violated, approximate estimation methods can be biased, and effect estimates are biased **away from the null**.

Only **conditional likelihood** (hypergeometric) and **Mantel-Haenszel** methods remain approximately valid under sparse data. **Unconditional likelihood is invalid.** The extreme case: 100 pair-matched case-control sets means 99 stratum parameters and 100 cases; unconditional logistic regression will produce biased estimates. For matched data the rule applies to the number of **discordant pairs**.

## Confounding versus multicollinearity

Fit a reduced model and a full model. Watch two things: **b₁** (the main exposure coefficient; bias) and **SE(b₁)** (collinearity).

|  | SE unchanged | SE increases |
|---|---|---|
| **b₁ unchanged** | No confounding, no collinearity → **use the full model** (no harm, and you can report having adjusted for all potential confounders) | Collinearity only → revert to the reduced model, or try deleting candidates one at a time |
| **b₁ changes** | Confounding only → **use the full model** | Both → find a reduced model that still controls confounding; if that fails, keep the full model, or use RMSE |

Worked, with asbestos as the exposure and age, sex, smoking forced:

| Model | b₁ | RR | SE(b₁) | Reading |
|---|---|---|---|---|
| exposure + forced | 0.693 | 2.0 | 0.24 | reference |
| + V1…V5 | 0.693 | 2.0 | 0.24 | nothing changed → full model |
| + V1…V5 | 1.099 | 3.0 | 0.24 | **confounding** → full model |
| + V1…V5 | 0.693 | 2.0 | 0.47 | **collinearity** → reduce |
| + V1…V5 | 1.099 | 3.0 | 0.47 | **both** → reduce carefully, or RMSE |

**This decision uses no p-values and no goodness-of-fit statistics. They are irrelevant here.** The only thing that matters is whether the main effect changes when the other variables enter.

## Root mean squared error

When confounding and collinearity conflict, trade bias against variance explicitly.

> MSE(reduced) = (b_reduced − b_full)² + SE²_reduced
> MSE(full) = SE²_full

Worked on sodium and potassium intake at 4 months and blood pressure at 7 years: for sodium, the reduction in SE from deleting potassium is offset by the increase in bias (RMSE 0.294 without vs 0.290 with), so keeping potassium is no worse in accuracy and has smaller bias. For potassium, RMSE is 0.095 with sodium included vs 0.130 without, so include sodium.

## The preference order

> **Using the full model is preferable, provided there are no problems of sparse data and/or multicollinearity.** If we have to find a reduced model, the **change-in-estimate** approach is preferable to using significance testing.

So: **full model > change-in-estimate > stepwise.** Stepwise belongs to prediction, not causation.

**Change-in-estimate has its own limitations**, which must be stated whenever it is used:

- Some effect measures, rate ratios, odds ratios, are **not collapsible**, so the estimate can change on adjustment **even when there is no confounding**. A change is therefore not proof of confounding.
- The change in estimate may be **unstable when there is multicollinearity**.

More sophisticated options exist and are out of scope here: penalisation, using Bayesian shrinkage to partially enter all variables; and machine-learning-based algorithms under development.

## One approach to modelling

1. Decide **a priori** what the main effect variable is and how it will be defined.
2. Decide **a priori** the basic **forced variables** always adjusted for; age, sex, and so on.
3. If there are very many candidates, screen: run "univariate" analyses for each potential confounder, adjusted for the forced variables, and keep those showing strong associations with the outcome (e.g. OR or RR above about 1.5). This produces a shorter list. (It screens only on the outcome relation; an alternative is to try adjusting for each and see whether the main effect changes.)
4. **Think about collinearity a priori, from theory rather than testing.** Some variables are expected to be collinear: smoking and cigarette lighter use; several measures of socio-economic status; age and years in the workforce. Decide from prior knowledge which to include.
5. **Model 1**; main exposure + forced variables.
   **Model 2**; + potential confounders. Check for multicollinearity of the main effect; **if there is none, stop.**
   **Model 3**; + potential confounders minus one. If there is multicollinearity, try to reduce it *without reducing confounder control* by eliminating candidates one at a time. If that fails, return to the full model or use RMSE.
   **Model 4**; **now**, and only now, consider effect modification.

For multiple main exposures the principles are unchanged but you must watch the coefficients of every main exposure simultaneously, which gets hard quickly. Screen harder first.

## Where p-values legitimately belong

**Not** for assessing confounding. Once the confounders are settled, you may reasonably use a p-value:

- to test the statistical significance of the main exposure–outcome association (alongside the estimate and interval);
- to assess evidence for **effect modification**;
- to assess the **form** of the relationship, e.g. linear versus non-linear.

## Mediation

**Traditional:** not adjusting for the mediator gives the **total** effect; adjusting for it blocks that pathway and leaves the **direct** effect.

**Modern:** adjusting for the mediator **opens** the mediator–outcome confounder path, so g-methods (Robins) are required for valid estimates. → `causal-inference`.

A calibrating note: in a worked study of ethnicity and cancer outcomes, traditional and g-method estimates broadly agreed; 87% vs 89% of the risk difference direct for stage, 21% vs 23% for mortality. The sophisticated method is not automatically a different answer.

## Reporting

**A standard set of tables:**

| Table | Content |
|---|---|
| 1 | Characteristics of study participants |
| 2 | "Univariate" analyses, adjusted for the forced variables |
| 3 | Final multiple regression with summary average population effects |
| 4 | Findings in specific subgroups (effect modification) |

And the rule that follows from the course's own complaint that *"it is difficult to tell from most papers what modelling strategy has been used"*:

> **Document the modelling strategy**, whatever it was, so readers can interpret the results in the light of its strengths and weaknesses.

Also: show **crude alongside adjusted**, so the reader can see whether adjustment did anything at all.
