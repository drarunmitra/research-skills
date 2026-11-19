# Teaching lane: putting epidemiology back into the practicals

**Core principle:** a practical that teaches only R verbs teaches that epidemiology is data manipulation. Every practical should open by saying what study this is, and close by saying what the number does not show.

Scope: the IISc / LSHTM *Concepts and Methods in Epidemiology* short course, 21–25 September 2026. Pairs with `slides-creator-skill` for deck house style.

## The lecture-to-practical bridge

Each evening practical applies that same day's concept. This mapping is not written down anywhere in the repo, which is why the practicals read as a parallel R curriculum rather than as the application of the morning.

| Day | Lectures, in order | Practical | The concept the practical is applying |
|---|---|---|---|
| **1 Mon** | Introduction to epidemiology (Neil) → Study designs + exercise (Neil) → **Exposures + exercise (Poppy)** | **I: Introduction to R** | Source population and risk period; **target → operationalised → measured exposure**, taught two hours earlier |
| **2 Tue** | Overview of bias (Neil) → Confounding + exercise (Neil) → **Cohort studies + exercise (Poppy)** | **II: Cohort study** | Person-time, at-risk definition, and **loss to follow-up as selection bias** |
| **3 Wed** | Cross-sectional (Neil) → Intervention studies (Poppy) → Case-control design (Neil) → **Selection of controls (Neil)** | **III: Case-control study** | **What the OR estimates given how controls were sampled**; confounding and Mantel-Haenszel |
| **4 Thu** | Interaction and effect modification + exercise (Neil) → Causal diagrams + exercise (Poppy) | **IV: Interaction** | Additive vs multiplicative, and the joint-effects table |
| **5 Fri** | Causal inference and p-values (Neil) → Causal and predictive modelling (Neil) | **V: Modelling strategy** | Full model vs change-in-estimate; negative controls |

Two links are especially tight and currently unused. **Practical I runs immediately after the Exposures lecture**, so the exposure framework is fresh and should be applied to real variables. **Practical III runs immediately after "Selection of controls"**, in a hospital-based case-control study, with the hospital identifier in the data.

## Reusable opening block

Put this at the top of every practical, before the first `library()` call. House style: stock Quarto, `::: callout-note`, numbered `1)` tasks, `callout-important` for interpretation, `callout-caution` for traps.

```markdown
::: {.callout-note}
## Before we touch the data

**Research question.** [exposure] → [outcome], in [target population].

**Source population.** [who, where, and how they came to be in this dataset]

**Risk period.** [when, and over what span]

**Measure, and why.** [prevalence / risk / rate / OR]; because [what the
follow-up and the sampling actually allow].

**What this cannot show.** [the honest limit, stated up front]
:::
```

## Reusable closing block

Modelled on the one good instance that already exists, at the end of the Practical 1 deck:

```markdown
::: {.callout-warning}
## What this estimate does not show

**Shows:** [the narrow, defensible claim]

**Does not show:** [the claim a reader will jump to]

[One sentence on the design reason; what came first, what was adjusted for,
who is missing from the denominator.]
:::
```

## Per-practical prescriptions

### Practical I; Introduction to R (APCAPS round 3, prevalence of diagnosed diabetes)

Currently: 692 lines, zero occurrences of bias, confounding, validity, selection or generalisability. It closes by offering a cross-sectional age–prevalence contrast as support for age being a major risk factor.

| Add | Why |
|---|---|
| **Prevalence is not risk.** P/(1−P) = I × D, so an age gradient in prevalence may reflect **duration or survival**, not incidence | The single most important caution about any cross-sectional number → `occurrence-and-effect.md` |
| **`diabetes` is *diagnosed* diabetes.** The variable partly measures healthcare contact | The Cohort lecture makes the same point about EHR outcomes being well recorded for some conditions and not others |
| **State the source population precisely**: children born 1987–90 in 29 defined villages near Hyderabad, plus their parents and siblings; then ask who the findings apply to | Generalisability is the target → source gap, and it is never mentioned |
| **Apply the Exposures lecture from two hours earlier** to `asset_score_quartile`: what is the target exposure, how was it operationalised, what is lost in between | The framework is fresh, the variable is right there, and the connection is currently unmade → `exposure-measurement.md` |
| **Reverse causation and survivorship** as named rivals in the closing block | The existing conclusion leans the wrong way |

### Practical II; Cohort study (APCAPS round 3 → round 4)

Currently: computes loss to follow-up of 34% in men and 42% in women, asks "what might the implications be?", and the solutions file answers only the descriptive half.

| Add | Why |
|---|---|
| **Differential loss to follow-up is selection bias** on the sex-specific rate comparison the students just computed. Give it a **direction** | This is the whole of that morning's bias lecture, sitting unused in the students' own output |
| **Give attrition a mechanism, not a label**; who stops participating, and is it related to the outcome? Then: how did those lost differ from those retained? | "42% were lost" is not a finding |
| **`died_fu` is a competing risk** | It is in the dataset and never mentioned |
| **Say why the rate is the right measure**: with losses this large the incidence proportion **cannot be estimated directly** | Turns a formula choice into a design argument → `occurrence-and-effect.md` |
| Note that the Cohort lecture that morning names **loss to follow-up in the younger age group** as one of APCAPS's three headline limitations | The practical computes the number; the lecture flags the problem; nothing connects them |

### Practical III; Case-control study (COVID-19 vaccine effectiveness, 11 hospitals)

Currently handles confounding by age well. The phrase "selection bias" never appears, and the control-sampling scheme is never named; in a hospital-based study, on the day of the "Selection of controls" lecture, with `hosp_code` in the data.

| Add | Why |
|---|---|
| **What is the source population** for cases drawn from 11 hospitals? Answer in the lecture's own form: *all those who would have come to these hospitals if they had developed severe COVID-19* | The defining question of the design → `design-options.md` |
| **Apply the symmetry rule to `hosp_code`**; restrictions applied to cases must apply to controls | Directly actionable with the data in hand |
| **Name the control-sampling scheme, then name what the OR estimates**; odds ratio, risk ratio or rate ratio | The signature technical point of the course, and free to add |
| **Confounding by indication and by rollout timing** as the live threats in a vaccine-effectiveness study | Task 5 already reasons about the Indian rollout; extend it to name the bias |
| Add **admission-rate (Berkson) bias** as a named candidate | Hospital-based controls are its textbook home → `validity.md` |

### Practical IV; Interaction

Currently handles additive vs multiplicative well. Confounding of the stratum-specific estimates is not revisited, and the joint-effects table is not printed.

| Add | Why |
|---|---|
| **Print the 2×2 of joint effects** with the doubly-unexposed as reference | The lecture explicitly asks for this so readers can use whichever definition of "effect" they need |
| **Revisit confounding within strata** | Confounding and effect modification are separate; stratifying does not settle the first |
| **Make the policy consequence explicit**; who to prioritise for vaccination changes with the scale | Mirrors the Weiderpass exercise done that morning, where the two scales give opposite policy answers |

### Practical V; Modelling strategy

Currently: screens covariates by change-in-estimate, then forward selection, then presents forward-vs-full as a toss-up with the criterion "provides more complete adjustment".

| Add | Why |
|---|---|
| **State the course's preference order: full model first**, change-in-estimate only if sparse data or multicollinearity force a reduction, stepwise never | The lecture the previous morning says exactly this. The practical currently inverts it → `modelling-strategy.md` |
| **Name the change-in-estimate rule's own limitations**; non-collapsibility means the estimate can move without confounding; the change is unstable under multicollinearity | The lecture states both; the practical states neither |
| **Use the confounding-vs-multicollinearity 2×2** explicitly: watch b₁ and SE(b₁), and read the answer off the table | Turns "which model do you prefer?" into a decision with a rule |
| **Frame `vac_source` as a negative control / information-bias probe** | It already is one; naming it connects the task to Day 5's triangulation teaching |
| **Check the rule of 10** against the number of events before fitting the full model | Makes the sparse-data constraint concrete rather than theoretical |
| Flag that "controls for all potential confounders" is **not** a justification for reporting every coefficient | Table 2 fallacy → `causal-inference` |

## House style constraint

Stock Quarto defaults plus the existing 21-line `style.css`, whose own header is the rule:

> Minimal teaching-deck house stylesheet; keep it this small. Do NOT add font imports, colour palettes, themes, or gradient boxes.

Structure comes from native Quarto constructs: `panel-tabset`, callouts, `.smaller`, `. . .` fragments, `{.inverse background-color="#222222"}` section dividers. R conventions in this project: `pacman::p_load()` with an inline comment per package, `here()` for every path, `rio::import()`, `janitor::clean_names()`, native `|>`, `#| label:` and `#| code-summary:` on every chunk, and results quoted back into prose with inline code so the narrative cannot drift from the table.

## A caution on scope

Adding epidemiological framing must not turn a two-hour R practical into a lecture. The opening and closing blocks are **five lines each**. The per-practical additions above are one or two callouts and a sentence in an interpretation, not new tasks. If a point needs more than a callout, it belongs in the lecture, not the practical.
