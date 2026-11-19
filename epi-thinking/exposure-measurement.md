# Exposure measurement

**Core principle:** three steps, in order. **Define a target exposure → operationalise it → measure the operationalised exposure.** Error enters at both joins, and the first join is a conscious design choice, not an accident.

Two senses of the word. Substantively, an exposure is a disease-causing or preventing agent of interest. Operationally, the exposure is the variable whose causal effect is being estimated in a given analysis. Outcomes in epidemiology are health states; exposures can be almost anything; genetic, biochemical, psychological, behavioural, socio-economic, health-care related, environmental, economic and political.

## Step 1: define the target exposure

Critical, and usually skipped. The choice of metric follows from **the supposed biological mechanism** linking exposure to effect, and from practical and technological constraints. Four questions:

| Question | What to settle | Example |
|---|---|---|
| **Duration and timing** | critical periods, latency, when to measure relative to outcome | toxin exposure in pregnancy may act only in certain trimesters; a long-latency outcome needs the right gap |
| **Relevant dosage** | average, peak, cumulative, threshold | cumulative dose over years for COPD and heart disease; local spikes for asthma exacerbations |
| **Stability** | does it vary naturally, and at what frequency | biological parameters vary through the day; sun exposure varies annually |
| **Relative or absolute** | which quantity is aetiologically relevant | socio-economic position: relative rank, or absolute deprivation? |

**Biomarkers force this choice explicitly.** A biomarker is *"a cellular, biochemical or molecular indicator of exposure; of biological, subclinical, or clinical effects; or of possible susceptibility"* (Porta, *A Dictionary of Epidemiology*, 6th edn). For an environmental agent you can measure anywhere along a ladder:

> environmental level → internal dose → biologically effective dose → early biological effect → altered structure or function

Worked on lead: lead in household paint or occupational air; **blood** lead, reflecting recent months; **bone** lead, reflecting cumulative long-term exposure actually laid down in the body; disrupted heme synthesis as an early biological effect. These are not better and worse measures of one thing; *they are different ways of precisely defining the exposure, corresponding to slightly different research questions and assumptions.*

## Step 2: operationalise it

Why a gap opens between target and operationalised exposure:

- the value **varies over time** (blood pressure, physical activity)
- **experienced exposure varies as people move around**; residence-based environmental measures miss where people actually spend the day
- the **construct is not observable** (stress, self-efficacy, relative socio-economic position)
- **capturing the target is not feasible at scale**; weighed food diaries for years become "how often do you eat oily fish in a week"

Worked examples:

| | Blood pressure → dementia | PM2.5 → dementia |
|---|---|---|
| **Target** | average systolic pressure over the past 5 years | total fine particulate matter inhaled over a lifetime |
| **Operationalised** | brachial systolic BP, once, in clinic, after rest, automated device | predicted average daily PM2.5 in the 1 km² around the house over 10 years |
| **Issues** | BP varies continuously through the day and responds to short-term conditions; how well does arm pressure represent the general concept; how well does the machine estimate true pressure | people spend variable time outside the neighbourhood, and indoors vs outdoors; lung capacity and breathing rate modify inhaled quantity from external concentration; insufficient data for lifetime exposure; predictions more accurate near monitors |

A third, for asset-based socio-economic position: target = current material affluence of a household relative to all households in the country; operationalised = tertiles of a data-derived wealth score from self-reported ownership of eight assets. Issues: are eight assets sufficient to capture material affluence **in this setting**, and is the right comparison population included?

**The trade-off is unavoidable: simpler and easier to measure accurately means further from the true target.** For many natural exposures we cannot operationalise meaningfully and simply do the best we can. This is widely accepted; arguably too widely, since studies often do not acknowledge it at all, or gesture vaguely at "measurement error". The consequence is widespread **underestimation of exposure effects**, and of confounding effects. It matters most for quantifying impact; it is not always the binding constraint for causal reasoning.

## Step 3: measure it

> To measure is to assign numerical values to objects and events according to rules. **Error of measurement** is the difference between the measured and the true value of a variable under given conditions.

Five modalities, each with its own interrogation list.

**1. Factors in the external environment**; community, home or personal monitoring. Fixed-site monitors vs portable personal devices.

**2. Bodily processes**; biomarkers, clinical measurements, images. What stage of the exposure–outcome pathway does it capture? Short-term or long-term (cotinine in blood is short term, in hair long term; fasting vs non-fasting samples)? Lab error, and the consistency of sample collection, transport and analysis, especially across wide geographies or time periods.

**3. Reported by participants or informants**, questionnaires, interviews, diaries. Current or recalled? Any biases or interests at play; is blinding possible? Validated instruments, construct validity, criterion validity, reliability. Appropriate for **this** population: children, cultural context. Mode: interviewer, CAPI, self-completed, online.

**4. Records gathered elsewhere for other purposes**, EHR, social security, education, spending. **Why and how were these records originally created?** What was the reason for the exposure to be recorded at all? Completeness, quality, exclusions. Validity of the measure and quality of recording, is there a validation study? Duration, e.g. full occupational histories. And **linkage**: methods, quality, transparency; are all records expected to link, or is a non-link being silently treated as absence of exposure?

**5. Modelling**; land-use regression for air pollution; modelled strain composition for infections; heart rate plus motion sensors plus location for physical activity; risk scores such as QRISK and eGFR combining biomarkers with sociodemographics.

## Quantifying measurement error

You need a group of people on whom you have **both** the error-prone measure and a "true" or best measure.

**Continuous.** Plot measure 1 against measure 2 and look for a 1:1 relationship. Better: plot the **difference against the mean**, and look for an even spread above and below zero. (Cuff vs arterial-line blood pressure is the worked case.)

**Binary or categorical.** Tabulate agreement against true status.

|  | True: exposed | True: not exposed | Total |
|---|---|---|---|
| **Measured: exposed** | 28 | 23 | 51 |
| **Measured: not exposed** | 4 | 45 | 49 |
| **Total** | 32 | 68 | 100 |

| Statistic | Definition | Here |
|---|---|---|
| Accuracy | total proportion correct | (28+45)/100 = 0.73 |
| Sensitivity | true positives correctly identified | 28/32 = 0.88 |
| Specificity | true negatives correctly identified | 45/68 = 0.66 |
| Positive predictive value | test-positives that were true positives | 28/51 = 0.55 |
| Negative predictive value | test-negatives that were true negatives | 45/49 = 0.92 |

**PPV and NPV condition on the test result, so they depend on the prevalence of the exposure, not on the validity of the measure alone.** Sensitivity and specificity are properties of the instrument; predictive values are properties of the instrument *in that population*.

Reliability, getting the same answer on repeated measurement, is a related but distinct question from validity.

## What measurement error does

Three separate consequences, not one:

1. **Increases the variance** of continuous measures. Random error in blood pressure readings inflates the standard deviation.
2. **Over- or under-estimates exposure prevalence.** If sensitivity < 1, not everyone truly exposed is identified, so exposure is under-counted.
3. **May bias the exposure–outcome association.**

For the third:

|  | Continuous exposure | Categorical exposure |
|---|---|---|
| **Non-differential** (e.g. random) | bias **towards the null** | usually null, but exceptions occur with multiple exposure categories |
| **Differential** | **anything could happen**; think it through carefully | anything could happen |

**"Differential" means something precise:** the error in the exposure is **causally affected by the outcome** (knowing you have cancer changes how you recall a toxin), **or** the errors in exposure and outcome **share a common cause** (both asked on one questionnaire, and some people over-report everything).

The documented exceptions to "non-differential biases towards the null" are in `validity.md`. Regression dilution is the continuous-exposure case (Hutcheon, Chiolero & Hanley, *BMJ* 2010;340:c2289).

## What to do about it

**At design and conduct**; this is where the leverage is:

- choice of how the exposure is operationalised, including newer tools: continuous physiological monitoring, wearables
- pre-testing and validation, especially for questionnaires
- data collection discipline: SOPs, QA procedures, training, re-training
- QC procedures and repeatability, especially for assays

> **A bigger sample will not help here. It makes you more precisely wrong.**

**At analysis**; only if you have external information on the extent of the error, or a true measure on a sub-sample: statistical adjustment for measurement error, and **sensitivity analysis**.

Sensitivity analyses are thought experiments: how much error or bias would be needed to substantially alter the conclusion? A usable rule of thumb; under certain assumptions, to *completely* explain an association, having the outcome would need to increase the odds of self-reporting the exposure by at least the value of the observed odds ratio. If low social support in pregnancy carries 1.51 times the odds of post-partum depression, and both are self-reported afterwards, then women with depression would have to over-report low social support by a factor of 1.51 for the finding to be entirely artefactual. State that, and let the reader judge whether it is plausible.
