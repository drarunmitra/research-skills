# Design options

**Core principle:** all epidemiological studies are based on a particular population (the **source population**) followed over a particular period of time (the **risk period**). Designs differ only in how the source population is defined and how information is drawn from it. If you cannot name the source population and the risk period, you do not yet have a study.

## The taxonomy

Two axes only: is the outcome **incidence or prevalence**, and is sampling **on the outcome or not**.

|  | Not sampled on outcome | Sampled on outcome |
|---|---|---|
| **Incidence** | incidence studies (cohort, follow-up) | incidence case-control studies |
| **Prevalence** | prevalence studies | prevalence case-control studies |

Extended by cross-sectional and longitudinal studies with **continuous** outcomes, and by descriptive and ecological comparisons.

**Directionality is explicitly rejected as a classifying feature.** Prospective vs retrospective, and "from exposure to outcome vs from outcome to exposure", do not distinguish designs.

## Naming discipline: historical, not retrospective

Say **historical cohort study**. Never "retrospective cohort". Four reasons, all of them design insights rather than style:

1. **"Retrospective" describes the investigator, not the study.** Such studies *"use historical information that was collected prospectively but abstracted retrospectively by the investigator."* A 1970 employment register was written in 1970, by a clerk blind to who would later become a case. Exposure recorded before the outcome by someone who could not know the outcome is the strongest property a cohort can have. "Retrospective" conceals it; "historical" preserves it.
2. **The word already names something real, and it is not a design.** *"Recall bias arises from the retrospective collection of exposure information, irrespective of whether the study is an incidence, incidence case-control, prevalence, or prevalence case-control study."* Spend the word on a design label and you lose it for the thing that actually causes bias.
3. **A historical cohort still runs forwards**, exposure then outcome. The label implies backwards reasoning and echoes the reverse-causality misconception attacked below.
4. **It is an unearned demotion**, the same move as the false hierarchy of designs; *"an unfortunate aspect of some discussions of the merits of case-control studies is that they have often been labelled as 'retrospective' studies, when this is in fact not an inherent part of their design."*

No free pass, though: information bias is of most concern *"in historical cohort studies or case-control studies when information is obtained by personal interview"*. The concern attaches to the **method**, not the label; which is the point. Watch for EHR and record-linkage studies titled "retrospective" that are straightforward cohort studies: exposure was defined for everyone at baseline from records generated at that time, then everyone was followed for incident outcomes.

## Choosing a design

There is **no best design and rarely a single definitive study**. Pearce's satirical league table, RCTs in the Premier League, causal inference and Mendelian randomisation in the Championship, cohorts in Division 1, case-control in Division 2, cross-sectional in the Vauxhall Conference, ecological studies as amateurs, is there to be rejected, not applied.

| Design | Reasons to choose it |
|---|---|
| Cohort | incident outcomes; population rates; rare exposures; multiple outcomes; less biased exposure measurement; temporal sequence |
| Case-control | rare disease; long induction time; a smaller study permits richer exposure information for the money; source population hard to enumerate (registry-based) |
| Cross-sectional / prevalence | burden of disease and health-service need; comparing prevalence between populations; trends over time. Especially valuable for non-fatal disease, degenerative disease with no clear onset, and physiological variables such as blood pressure, lung function, liver enzymes |
| Ecological / geographical | low cost; measurement limitations of individual-level studies (diet, air pollution); **design limitations; lack of exposure variation**; interest in ecologic effects; simplicity |
| Trial | randomisation is ethical and feasible, and a concurrent control is obtainable |

**Why not just do a trial?** Ethics (pregnancy, harmful exposures); logistics (exposure cannot be controlled, outcomes too rare); and long-term effects.

## Population-level studies are not a lesser thing

A difference between populations shows both that there is a public health problem to solve **and** that there is a scientific question that can be solved. Comparisons between populations can: reveal "new" risk factors; provide a reality check on "established" individual-level risk factors; enable triangulation; and give aetiological clues precisely when population-level and individual-level findings disagree.


**But state the unit of inference, the ecological fallacy, named.** An association between district-level percentages is a statement about districts, not about the people in them. Inferring from the group to the individual is **cross-level bias**, and it is not merely attenuation, **it can reverse sign**. In one real district dataset the coefficient for clean cooking fuel ran +0.023 pooled across states and −0.036 within state. A coefficient that flips on a single specification choice is not an effect estimate. Report pooled and within-group estimates side by side and let the reader see the shrinkage.

The reverse error has a name too: the **atomistic fallacy**, inferring a population-level effect from individual-level data, which misses effects that exist only at population level.

Neither fallacy makes ecological studies illegitimate. They make the **unit of inference** something you must state out loud.

## Routine, programme and surveillance data

Most data you will be handed was created to run a service, not to answer your question. Interrogate it before designing anything.

**A notification is not a case of disease.** It is a reporting event. Counts move with detection effort, active case-finding campaigns, reporting completeness, private-sector engagement and portal behaviour; none of which is incidence. So a rise in notifications can mean more disease *or* better detection, and those have opposite policy meanings. Say which you are claiming.

Questions to put to any routine extract, before analysis:

| Ask | Why it bites |
|---|---|
| **What was this record created for?** | The reason a field exists determines how well it is filled. Fields that drive payment or a clinical action are complete; fields that drive nothing are not |
| **What period does the extract actually cover?** | Read the filter and header rows, not the filename. One real TB extract was filtered to a single month while being named for a year |
| **Which date is the date?** | Notification date, diagnosis date, treatment-start date and entry date are different, and the one you were given may not be the one you need |
| **Who is counted, and where?** | A "current facility" mapping counts people managed here who were diagnosed elsewhere. Right for workload, wrong for local incidence |
| **What is the denominator?** | Usually absent. Without a population there is no rate; only a count |
| **What is the case definition, and did it change?** | A definition change looks exactly like an epidemic |
| **Did the instrument change between rounds?** | So does a device change. A new assay, analyser or cut-off is non-differential *within* a round but a **systematic shift between** rounds; it moves every unit in the same direction at once, which is exactly the structure that manufactures a trend out of nothing. Read the biomarker or methods section of each round before believing any change |
| **Did the fieldwork period change?** | Season, and events. A survey fielded either side of a pandemic, a harvest or a malaria season is measuring two different worlds. If the rounds split cleanly, that split is a **natural experiment** you can exploit rather than a nuisance |
| **Is the outcome administratively censored?** | Recent periods look better or worse simply because outcomes are not yet declared. Check outcome-missingness by period and truncate |
| **Do the registers link, and what does a non-link mean?** | If a non-link is silently read as "exposure absent", you have built misclassification into the dataset |
| **Is a blank a zero?** | Cleaning code that maps missing to "none" converts ignorance into a finding |

A register-based study is usually a **historical cohort** (see the naming discipline above), and often a near-census of its source population rather than a sample from it; which is a genuine strength worth stating.

## Cohort studies: five design questions

Work these in order. Each is illustrated below with one worked study (prediabetes → active TB, Taiwan, *IJE* 2022).

**1. What is the research question?** It must name the **exposure**, the **outcome** and the **target population**; *the population to whom you intend your findings to apply*. → *Does having pre-diabetes increase risk of developing active TB?*

**2. Do you need to collect new data?** Do data on exposure, outcome **and confounders** already exist, in prior studies or routine data? Trade-off: **range and quality of measures** against **time, resources and size**. → *Linkage of a large community diabetes screening programme to national TB and death registers.*

**3. Who are your study population?** At-risk individuals, free of the outcome at baseline. Appropriately representative of the target population; geography, age, occupation. Available and willing (pragmatism). And **when does someone enter the cohort**: a fixed date, or an event such as surgery? → *Adults in the screening programme with no history of TB within 28 days after screening.*

**4. Who are your exposed and comparison groups?** Exposure measurement and validity; sufficient **exposure variation**. Then the key distinction:

| Exposure | Comparison group | Examples |
|---|---|---|
| Rare | **selected by design** | occupational cohorts, matched cohorts |
| Common | **assigned at the analysis stage** | birth cohorts, community cohorts, EHR linkage |

Comparability can be handled at the design stage or the analysis stage. → *Prediabetic vs normal on screening FPG.*

**5. How will you follow up for outcomes?** Outcome definition, ascertainment and validity; define the ICD-10 codes, then ask how accurate that recording actually is in this setting. EHR data is better for some outcomes than others: major stroke is well recorded, common mental health conditions are under-diagnosed. Ongoing follow-up vs repeat surveys. Duration and interval, set by the natural history of the condition. Criteria for leaving the cohort, including death from other causes. Whether someone can recover and become at risk again. **Loss to follow-up can be a major source of bias and must be minimised.**

**Follow-up mode determines the available measure:**

| Data collection | Measure | Analysis |
|---|---|---|
| Ongoing follow-up | incidence rate (person-time) | time-to-event, time series |
| Repeat surveys | continuous traits; means, changes | linear, multilevel growth models |
| Repeat surveys | incidence proportion | logistic regression, risk prediction |

**Sizing a cohort:** meaningful exposure variation, sufficient cases occurring during follow-up, a realistically detectable effect size; therefore power calculations early in planning. → `power-sample-size`.

**Other features with analysis consequences:** multiple observations per person → correlation within individuals, handle with multilevel models. Exposures, confounders or eligibility changing during the study → careful design and time-varying methods; if the time-varying confounder is itself affected by exposure, g-methods are needed (→ `causal-inference`). Loss to follow-up and censoring → minimise by design; weighting or imputation at analysis; competing risks.

**Disadvantages, stated plainly:** expensive and slow; inefficient for rare outcomes; misclassification of exposure and outcome when relying on routine data; and bias from loss to follow-up and confounding.

## Beware: blurred lines

- Data from a "cohort study" analysed **cross-sectionally** (baseline only, or all waves pooled) is a cross-sectional analysis.
- **Trial datasets analysed as cohort studies**; a secondary analysis where the exposure of interest was measured, not randomised.
- **Case-control studies nested within cohorts**; efficient and robust; see control sampling below.
- **"Retrospective"** misapplied to EHR and record linkage. See the naming discipline above.

Disambiguation: *prospective study*, *incidence study*, *cohort study*, *longitudinal study*, *repeated measures* (psychology), *panel survey* (economics) and *follow-up study* all name the same design across disciplines.

## Case-control studies

**Derive the design, do not reach for it.**

1. Design the ideal randomised trial you would really like to do.
2. Design the cohort study that corresponds to that trial, except that exposure has not been randomised.
3. Design the case-control study that corresponds to that cohort study.

A case-control study involves all of the potential biases of the full cohort study, **plus** the additional biases involved in sampling controls. Information bias is *not* an inherent feature of the design.

### Control sampling determines what the odds ratio estimates

This is the single most important technical point in the course.

| Scheme | Controls drawn from | Estimates | Nested CC | Population-based CC |
|---|---|---|---|---|
| **Cumulative** (exclusive); Cornfield 1951 | survivors, i.e. non-cases at end of follow-up | **odds ratio** | No | No |
| **Case-cohort** (inclusive); Thomas 1972, Prentice 1986 | the entire source population at the start | **risk ratio** | Yes | No |
| **Density** (concurrent); Sheehe 1962, Miettinen 1976 | person-time; the risk set at the time each case occurs | **rate ratio** | Yes | Yes |

**None of these requires a rare-disease assumption.** For prevalence case-control studies: exclusive sampling → prevalence odds ratio; inclusive → prevalence ratio.

In density sampling the "time" variable can be survival time (proportional hazards), age (nested) or calendar time (nested or population-based).

### Four misconceptions to attack

1. That it is a fundamentally different design proceeding from disease to exposure, i.e. reverse causality.
2. That it is inherently less valid or more biased than a cohort study.
3. That it requires a rare-disease assumption.
4. That the odds ratio only *approximates* the rate ratio or risk ratio.

### Finding the source population

For registry- or hospital-based cases, ask the question directly. Cases are all lung cancers at the main hospitals in London; what is the source population?

> *"All those who would have come to the main hospitals in London for treatment if they had developed lung cancer."*

**The symmetry rule:** restrictions that apply to one group, having a telephone, being on the Electoral Roll, having health insurance, **must also be applied to the other**. If cases were restricted to residents, restrict controls to residents, and exclude cases who travelled in for treatment.

### "Other disease" controls

Three variants: all other diseases; all other diseases except those known to be related to the exposure; a disease known to be unrelated to the exposure.

| | General population controls | "Other disease" controls |
|---|---|---|
| Represents source population | Yes | Only if those diseases are unrelated to exposure |
| Recall | May be more prone to recall bias if cases recall better | Equal motivation and recall |
| Interviewer | Hard to keep blind; interviewer bias | Easier to keep blind |
| Selection bias | Lower | Higher, and **irremovable** if the other diseases are caused by the exposure |

## Matching

Every claim here is demonstrated numerically in the course.

**Matching does not remove confounding.** In the worked example, the unmatched study gives crude OR 1.76 and adjusted 5.00; the matched study gives crude 2.06 and adjusted 5.00. Neither crude analysis is right; both adjusted analyses are. **You must still adjust for what you matched on.**

**Matching introduces confounding even where none existed.** Making cases and controls identical on the matching factor makes them similar on everything associated with it. Match on cigarette lighter use in a study of smoking and lung cancer, and you have equalised smoking too.

**It buys precision, not validity.** The adjusted estimate is the same either way; only the confidence interval narrows. The sole exception is when matching enables control of **unmeasured** confounding; siblings, neighbours.

**You cannot estimate the independent effect of a matching factor.** Matching distorts its association with the outcome. So never match on something whose own effect you want to report.

**Overmatching.** Matching on a factor strongly associated with the exposure but only weakly a risk factor destroys discordant pairs: you throw away data, lose precision, and bias towards the null.

**The rule.** Only match on factors that are (i) not of intrinsic interest in themselves, (ii) strong risk factors for the disease, and (iii) not too difficult to match on. Age and sex qualify. If you match, you must control for it; though not necessarily with a pair-matched analysis; see `occurrence-and-effect.md`.

**Reasons to match anyway:** practical efficiency (a control admitted the same day; siblings; same general practice) and statistical efficiency (random general-population controls in a lung cancer study would be mostly young while cases are mostly old, leaving thin strata).

## Intervention studies

| Type | What it is |
|---|---|
| Uncontrolled | everyone receives the intervention; compared with before, or historical controls |
| Non-randomised controlled | individuals allocated by a non-random procedure |
| Randomised controlled trial | participants randomly allocated to intervention or control |

**Why a control group is required.** Without one you cannot separate the treatment effect from: **natural improvement over time**, **regression to the mean**, and **placebo or other care**. Those three are the standing rival explanations for any uncontrolled before-and-after result.

**Randomisation** gives a fair comparison, makes treatment unpredictable in advance, and helps balance groups at baseline. Prerequisites: the question is of value and the answer is not already known; the trial is well designed; consent; and **clinical equipoise**.

**Blinding is not allocation concealment.** Single blind: the patient does not know. Double blind: those treating and evaluating do not know either. Blinding is often impossible, surgery, but **allocation concealment**, not knowing in advance which treatment will be allocated, is crucial regardless, and blinded outcome evaluation usually remains possible via an independent event validation committee.

**Size depends on six things:** the primary outcome measure; the significance level; the degree of certainty wanted (power); expected loss to follow-up; the expected control-group event rate; and the smallest treatment difference worth detecting. → `power-sample-size`. A large p-value in a small trial does not mean no difference exists.

**Other designs:** individual or cluster randomised; superiority or non-inferiority/equivalence; parallel group or crossover; more than two groups; factorial; adaptive.

For analysis, reporting, ITT vs per-protocol and subgroup rules, see `appraisal.md`.

> Clinical trials: hard to do, easy-ish to analyse and interpret. Observational studies: easy-ish to do, hard to analyse and interpret.
