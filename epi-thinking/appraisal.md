# Appraising a study you are reading

**Core principle:** it is easy to criticise an epidemiological study. **Perfect epidemiological studies do not exist.** The emphasis should not be on preparing a list of possible biases. It should be on assessing the **likely strength and direction** of each, and whether they **taken together could explain the observed association**.

> Mechanistic risk-of-bias assessments focus on whether specific biases are present but fail to give insight into the **direction, magnitude and relative importance** of individual biases. Instead, focus on identifying a small number of the most likely influential sources of bias, classify each study by how effectively it addressed each one, and determine whether results differ across studies in relation to susceptibility to each hypothesised source.

This is a study you are **reading**, to decide what to believe and whether it applies to your population. Judging a manuscript as a reviewer or author is `peer-reviewer`.

## Output contract

Produce, in this order:

**1. The appraisal table.**

| Row | |
|---|---|
| Research question of interest | |
| Study population / cohort definition | |
| Exposure, and method of assessment | |
| Outcome and method of assessment | |
| Follow-up | |
| Analytical approach (incl. covariates considered) | |
| Key findings | |
| Summary of strengths and limitations | |

**2. Ranked threats; at most five, one marked decisive, each with a direction.** The cap is a ceiling, not a target. A good study gets a short list. A poor study has more than five real problems: **group by root cause** (immortal time, prevalent users and an undefined time zero are one threat), and put anything left over in one line headed "Also noted", unranked. For calibration, a full worked answer to a case-control appraisal reduced to: *strengths; population-based; quality of diagnosis; response rate. Weaknesses; exposure assessment; selective report; small numbers.*

**3. A verdict, in the first person.** Do I believe this estimate? Does it apply to my population? What would change my mind?

Filling the table is the working, not the deliverable.

## The two questions

### Q1. What is the magnitude and precision of the effect estimate?

Significance testing tries to reach a decision from a single study. What matters is the **strength and precision** of the estimate and whether it is **consistent with previous studies**.

The possibility that a non-significant result is due to lack of power is addressed by looking at the **confidence interval**, not by post-hoc power calculations. This skill does not compute post-hoc power. → `power-sample-size`.

**Count events, not participants.** A cohort of 9,000 with 14 anxiety cases is a study of 14 events.

### Q2. What are the likely strengths and directions of possible biases?

**Confounding.** Have all potential confounders been controlled or assessed? If not, judge the strength and direction of what remains.

> It is unreasonable to simply assume that a strong association could be due to confounding by unknown risk factors, since to be a strong confounder a factor must be a very strong risk factor **as well as** being strongly associated with exposure.

A relative risk of 2.0 in an occupational study is highly unlikely to be smoking confounding. Relative risks of 0.7–1.5, as in many dietary studies, are not hard to explain by imperfect confounder control. Sign it positive or negative → `validity.md`.

**Selection bias.**

> It is unreasonable to dismiss the findings of a study because of possible selection bias without at least attempting to assess **which direction** it would have been in, and **how strong** it might have been.

**Information bias.** The key question is whether misclassification is likely **differential or non-differential**. If non-differential, the direction is usually known; towards the null. **If a study has yielded a positive finding, it is not valid to dismiss it because of the possibility of non-differential misclassification.**

### Q3. Is the effect big enough to matter?

A third pillar, independent of bias and precision, and the one most often skipped.

> Continuous outcomes are often well-powered, meaning you can detect tiny effects as "statistically significant". The important thing is being able to tell if they matter for policy or practice.

A 1-point difference on a 0–45 depression scale whose mean is 7 and SD nearly 6 may be statistically unambiguous and practically negligible. **Demand a translation**; onto the outcome's own scale, into absolute risk, into number needed to treat, into something a reader can act on. If the authors did not provide one, say so, and say that in the situation where these are highly marginal differences, the "significant" findings may be almost redundant.

## Six moves

**1. Reach a verdict.** Name the decisive threat, give its direction, say what would change your mind.

**2. Cap and rank.** At most five threats, ordered, one marked decisive.

**3. Ask whether the authors' fix actually fixes it.** A stated remedy is a claim to be tested, not a box ticked. In the Hardell study, self-reported occupational exposure was supplemented by contacting companies; and the verdict was that this *"does not solve the possible underreporting by controls"*, because the underreporting is on the control side and company records do not reach it.

**4. Treat absence of reporting as a finding.** *"Not mentioned if validated."* *"Completeness not described."* *"Not clear who is in the cohort and how selected initially."* *"Residence of controls in the same regions as the cases is not mentioned."* *"Details on measurement devices, validation, calibration, maintenance and protocols not given in paper."* Record silence; do not assume it benign.

**5. Ask what the analysis actually buys.** A within-person fixed-effect model removes **all time-invariant** confounding, past life experiences, family predisposition, personality, living situation, which is a great deal. It does **not** remove time-varying confounding, and if it does not respect temporal order then reverse causation remains open until you judge it implausible on substantive grounds. An inverse-probability-weighted analysis re-weights the sample so that the probability of exposure is balanced; the estimate reads like an adjusted mean difference, and residual confounding remains.

**6. Ask for crude alongside adjusted**, so the reader can see whether adjustment changed anything. And ask whether a subgroup split was **pre-specified**: *"I do wonder if they always intended to analyse by with/without limitations, as if these categories were pooled together, a more logical fit to the question, the effects might cancel to reveal little overall association."*

**Reporting guideline as a prompt for silence.** Match the design to its checklist (STROBE, RECORD for routine data, CONSORT, STARD, PRISMA) and record each item the paper skips as a finding, per move 4. The checklist is a list of places to look; it is not a quality score, and it does not size any bias. Formal compliance review belongs to `peer-reviewer`.

## Two checks on the design itself

**The known-causes check.** Before believing what a design *found*, ask whether it can recover what is already known. Run it on two or three exposures with solid evidence from other designs. If a district-level analysis returns null or wrong-signed coefficients for women's schooling, antenatal care and institutional delivery, all of which have individual-level and trial evidence behind them, that is a statement about the **design**, not about those interventions.

> A design that cannot recover the causes we already know should not be trusted to discover new ones.

This is the constructive form of a negative control, and it is cheap, because you already have the data. Report it either way. A design that *does* recover the known causes has earned real credibility for its novel finding.

**Regression to the mean, in any change score.** Whenever you compare two rounds, two measurements or two time points, the units that looked worst first will appear to improve most, purely from noise. The diagnostic is one line: **correlate the baseline value with the change.** A strong negative correlation is the fingerprint.

Then size it. If each round's estimate has standard error `s`, their difference has SE `s√2`; compare that against the observed spread of the changes. In one real two-round district comparison the baseline–change correlation was −0.52 for stunting and −0.65 for wasting, and noise alone accounted for roughly a third of the between-district variation in "change" before any real trend. Ranking units by improvement, or targeting those that deteriorated, is then largely ranking noise.

## Calibration: neither credulous nor nihilistic

Given a real case-control study and five candidate conclusions, the defensible answer is the third:

| Candidate conclusion | Verdict |
|---|---|
| (a) demonstrates that the exposure is a cause | **clearly wrong** |
| (b) strong evidence of cause, needs animal confirmation | **clearly wrong** |
| (c) **generates an interesting hypothesis needing confirmation by other epidemiological studies** | **acceptable** |
| (d) provides little information because of the small number exposed | acceptable; some prefer this, or a combination of (c) and (d) |
| (e) not informative because of poor methodology | **probably too strong** |

That is the floor. Perfect studies do not exist, and that is not a licence to dismiss.

**Cohort-study equivalent.** Given a registry cohort claiming a drug prevents a disease, the defensible conclusion is that it **generates a hypothesis needing a cleaner design** (new-user, time-varying exposure, competing risks handled). Claiming the drug protects is wrong. Saying the study is uninformative is usually too strong unless the exposure definition itself is broken.

**No absolute risk reported?** Say so; do not back-calculate silently. If a baseline risk is stated or can be read off, NNT is about 1 / (baseline risk × (1 − RR)); name the baseline you assumed.

## Question sets

### Cohort study

The eight-row table above, then three plenary questions:

1. How has the cohort data been **analysed differently** across studies of the same question?
2. What about **generalisability and representativeness**? Is **loss to follow-up** a concern?
3. To what extent are we worried about **confounding** in this body of evidence; i.e. what are the **alternative explanations** for the associations?

Specific things to check: **when does follow-up start, and when is exposure defined?** If exposure is defined by anything that happens after time zero (a drug fill, a landmark reached), suspect immortal-time bias first (`validity.md`); are prevalent users handled; stack the selection fractions (50% baseline non-response, then 55% lost, leaves 43% of the original cohort); is the outcome genuinely **incident**, or could participants already have had it at baseline, unmeasured; and give attrition a mechanism, *continued participation is strongly determined by outcome status*, then ask how those lost differed from those retained.

### Case-control study

1. **Which of the five candidate conclusions do you agree with, or disagree with least?** (See calibration above.)
2. **What is the source population?** State it precisely; e.g. *men aged 30–75 during 1989–92 resident in middle and northern Sweden*.
3. **Comment on possible sources of bias:**
   - 3.1 selection of cases from the source population; *e.g. possible bias from exclusion of deceased cases*
   - 3.2 comparability of cases and controls; *e.g. residence of controls in the same regions is not mentioned*
   - 3.3 response rate; *e.g. relatively high, however 11% of potential controls could not be contacted*
   - 3.4 collection of information and assessment of exposure; *and does the authors' remedy actually fix it?*
4. **Were potential confounders controlled? Which, and how?**; *e.g. age in the analysis, testicular disease by restriction, others not controlled.*
5. **Comment on the presentation of results:**
   - 5.1 selection of exposures for analysis and report; *e.g. only plastics-industry exposures are included and this selection is not well justified; possibility of chance results due to multiple comparisons*
   - 5.2 dose-response; *e.g. limited data owing to small numbers, but results compatible with a dose-relationship*
   - 5.3 subgroup analysis; *e.g. analysis by histological type is important because of heterogeneity of tumour types, but limited by small numbers of non-seminomas*
6. **Main strengths and weaknesses**, three each.

Also worth discussing: how to conduct a population-based case-control study in countries without a cancer registry or complete population registries; alternative methods of exposure assessment; incorporation of biomarkers.

### Exposure measurement

Four columns; **target exposure**, **how it was operationalised**, **approaches to ensure measurement validity**, **potential issues and shortcomings**. → `exposure-measurement.md` for the underlying framework.

Moves the answer keys make:

- **The target exposure is usually unstated and must be inferred**, and naming the candidates *is* the finding: *"acute inflammation; or it could be naturally occurring common infections and vaccinations."* They imply different questions.
- **The exposure window is a modelling assumption** requiring justification against the mechanism. An exposed period of 91 days, split 1–3 / 4–7 / 8–14 / 15–28 / 29–91 days, needs a rationale: *"reason for length of exposed period and how it relates to target exposure of acute inflammation is not clearly explained."*
- **Arbitrary cut-points block appraisal**: moderate-to-vigorous activity defined as >1952 counts per minute, sedentary as <100, and *"unclear what counts represent and therefore hard to judge method."*
- **Protocol adherence is a validity question**: accelerometers posted to participants, *"not known whether they wore them correctly."*
- **Device heterogeneity and cross-calibration**: several device models combined, adjusted for; but *"were devices of the same type calibrated to each other?"*
- **Measurement reactivity**: *"possibility that being in the study (wearing an accelerometer) affected behaviour."*
- **No within-study repeatability or validation**; recorded as a finding in its own right.
- **The contrast you choose determines what you can separate.** Using within-city daily variation makes carbon monoxide necessarily highly correlated with NO₂ in each city, because they share a source; a between-city contrast would break that correlation. The design choice, not the analysis, decided what was identifiable.
- **Short-term effect versus total effect**: a study of next-day mortality leaves the total effect, the thing public health needs, unknown, and raises **harvesting** (mortality displacement) as a rival explanation.

### Interaction

From the same table, reach **both** conclusions and explain why they differ:

| Definition | Pattern | Policy conclusion |
|---|---|---|
| Departure from **multiplicativity** (SMR falls with age, 10.24 → 1.61) | negative interaction | prioritise **younger** patients |
| Departure from **additivity** (excess death rate rises with age, 934 → 10,504 per 100,000) | positive interaction | prioritise **older** patients |

→ `validity.md` for the full treatment and the joint-effects table.

### Trials

**ITT versus per-protocol** maps onto **pragmatic versus explanatory**. Explanatory trials study the effects of treatments as received according to protocol, per-protocol analysis, potentially biased. Pragmatic trials study the consequences of treatment **policies**, recognising that not all patients comply, analysis by intention to treat, all randomised patients in their allocated groups. Most major trials are pragmatic.

**Multiplicity and data dredging.** The Anturane Reinfarction Trial reported: cardiac death at 1 year p=0.17; all cardiac deaths p=0.06; cardiac deaths months 2–7 p=0.02; all sudden deaths p=0.04; sudden deaths months 2–7 p=0.003. Ask which result received the most emphasis, and why.

**Subgroups.** Keep the main emphasis on the overall result. Pre-specify a few key subgroups. View subgroup analyses as **exploratory**. **Use interaction tests, not subgroup p-values.** Subgroup claims are usually exaggerated. Do not over-interpret.

**Reporting.** CONSORT for trials and its extensions, STROBE for observational studies, EQUATOR for the rest, and a pre-specified statistical analysis plan.

## Across studies

**Bradford Hill's nine viewpoints**, strength, consistency, specificity, temporality, biological gradient, plausibility, coherence, experiment, analogy, always with Hill's own caveat:

> What I do not believe is that we can usefully lay down some hard-and-fast rules of evidence that must be obeyed before we can accept cause and effect. **None of my nine viewpoints can bring indisputable evidence for or against the cause-and-effect hypothesis and none can be required as a sine qua non.** What they can do is help us make up our minds on the fundamental question; is there any other way of explaining the set of facts before us, is there any other answer equally, or more, likely than cause and effect?

Pearce's notes on individual viewpoints: **temporality** is crucial, the cause must precede the effect. **Specificity** is much criticised but may be relevant in assessing particular biases. **Consistency** is particularly important when a *variety of designs* is used in different settings, since this reduces the chance that all studies suffer the same bias. **Strength**; a weak association is not thereby non-causal; it just makes alternative explanations harder to exclude. **Dose-response** narrows the range of biases that could explain the relationship.

**Three developments beyond Hill:**

1. **Ruling out alternatives**; twentieth-century lung cancer time trends rule out a gene that causes both smoking and, independently, lung cancer.
2. **Interlocking arguments from different areas of science**; the IARC Monographs integrate human, animal and mechanistic evidence.
3. **Triangulation.**

**Three levels**, which should not be conflated: **causal discovery** (deciding between and ruling out alternatives across a series of studies); **causal inference** (considering all available evidence, not just epidemiological, in a triangulation approach, including investigation of the likelihood of major biases); **causal estimation** (may involve just one or a few high-quality studies).

### Triangulation as a procedure, not a slogan

> Triangulation is the practice of obtaining more reliable answers by integrating results from several different approaches, **where each approach has different key sources of potential bias that are unrelated to each other**. Be explicit about the expected **direction** of bias within each approach, and seek approaches that would be expected to bias the true causal effect **in different directions**.

The procedure: build a grid of **studies × biases**, mark which biases are **shared**, and credit agreement only where a study escapes a bias the others carry.

Worked, on three cohort studies of informal caregiving and mental health using three different analytical approaches and reaching the same answer:

| | Swedish (record linkage) | German (within-person fixed effects) | Australian (IPW) |
|---|---|---|---|
| Confounding by the illness that created the caring need | **shared; intractable** | **shared** | **shared** |
| Time-invariant confounding | partly adjusted | **removed by design** | partly adjusted |
| Outcome-dependent attrition | **escaped** (linked records) | present | present (55% lost) |
| Outcome measurement | objective diagnoses | self-report scale | self-report scale |

Reading it: agreement across all three is *not* strong evidence, because the decisive confounder, household sickness or disability, which creates the need for care **and** independently harms mental health, operates in all three and is *"a fairly intractable issue"*. What **is** informative is that the one study escaping outcome-dependent attrition agrees with the others. Name the intractable common cause explicitly rather than burying it in a limitations list.

**The counterweight:** before explaining disagreement between studies by bias, consider **genuine effect heterogeneity**. Different populations, settings and age groups may simply have different effects, and there is no reason to expect them all to behave the same way.

### Meta-analysis

Pooling increases the numbers and therefore reduces **random** error. It does **not** necessarily reduce systematic error, and may increase it through publication bias. Its real value:

> A careful meta-analysis will enable various possible biases to be addressed, **using actual data from specific studies** rather than hypothetical examples.

Compare studies that had smoking data with those that did not. Compare general-population controls with other-cancer controls to test recall bias. That is the meta-analysis worth doing.

### The false hierarchy

Reject it. There is no "best" study design and rarely a single definitive study. When RCTs go bad they go bad badly: MRFIT, the largest and most expensive trial of its type, found a small *increase* in lung cancer in the smoking-cessation arm, explained away as chance, with a major problem of intervention spillover; drop the randomisation and the estimates resemble the observational literature.

## Worked calibration example: fenoterol and asthma mortality

This is what the skill should sound like. Every move is on the record.

**The problem.** Asthma mortality epidemics in the 1960s, and a second epidemic in New Zealand from the late 1970s.

**Rival explanations enumerated first**, before any data: increased prevalence; increased case fatality; increased severity; environmental factors; **inappropriate medical management**.

**Descriptive and ecological evidence.** Countries with and without epidemics differed in use of isoprenaline-forte. National asthma mortality tracked beta-agonist sales, then fenoterol market share.

**A case-control study, with the control source justified from prior evidence.** Cases: all 125 asthma deaths aged 5–45 in New Zealand, Aug 1981 – Jul 1983, from the National Asthma Mortality Survey. Controls: hospital admissions for asthma, chosen because Rea et al. had shown that asthma deaths and asthma admissions were similar with respect to markers of chronic severity; *"asthmatic patients who are admitted to hospital and those who die appear to come from a similar portion of the asthmatic population."* Matched on age, ethnicity, district, date. Result: fenoterol OR 1.6 (1.0–2.3); salbutamol 0.7 (0.5–1.1).

**The obvious objection, and the answer.** Critics argued confounding by chronic asthma severity; sicker patients get fenoterol and also die. So stratify by severity markers. The odds ratio **rose**:

| Severity subgroup | OR | 95% CI |
|---|---|---|
| Prior admission in past year | 2.2 | 1.1–4.1 |
| 3+ categories of asthma drugs | 2.2 | 1.3–3.9 |
| Oral steroids | 6.5 | 2.7–15.3 |
| Admission in past year + oral steroids | 13.3 | 3.5–51.2 |

The confounding ran **opposite** to the direction critics claimed. That is signing a bias rather than naming it.

**A second study designed against the strongest remaining objection.** Restrict to patients with a prior asthma admission, so cases and controls are severity-comparable by design; take drug therapy from hospital records relating to the previous admission; and **assess it blind**, killing information bias. Result: fenoterol OR 2.0 (1.1–2.6), rising to 9.8 in the most severe subgroup. Salbutamol again null.

**The natural experiment.** The drug was withdrawn. The epidemic ended.

**What makes this exemplary:** rival explanations listed before the analysis; the source population and risk period named; the control source **justified by evidence** rather than convenience; the main objection answered by **signing and sizing** the suspected confounding; the next study **designed against the objection**; blinding used deliberately to make information bias non-differential; and causation reached through a **body of evidence**, ecological, time-trend, two case-control studies with different control sources and different biases, mechanistic evidence on cardiac effects, and a withdrawal experiment, rather than from a single p-value.
