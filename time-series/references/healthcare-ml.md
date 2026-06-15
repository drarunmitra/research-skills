# Healthcare / clinical-ML time series

When the data is patient-level longitudinal data rather than an aggregate
surveillance series, the tidyverts assumptions break and you usually leave
fable. This layer distils the van der Schaar Lab's framing: in clinical time
series the sampling is irregular, the missingness is *informative*, the true
state is unobserved, and multiple outcomes compete. Use this file to recognise
when a problem is in that regime and to pick the right method (and language).

## Is this even a fable problem?

fable expects regularly-indexed series with a clean index+key contract. Clinical
EHR/registry data usually is not that:

| Signal | Implication |
|--------|-------------|
| One row per visit/measurement, irregular spacing | not a regular tsibble; do not `fill_gaps` blindly |
| Different patients measured at different times | per-patient series, often very short |
| Missing values that depend on clinical decisions | missingness is a feature, not noise to impute away |
| Goal is per-patient trajectory / risk, not population forecast | longitudinal model, not aggregate forecast |
| Time-to-event with covariates evolving over time | longitudinal survival, not forecasting |

If most of these hold, this is a clinical-ML problem. If you have aggregated to
counts/rates per period (e.g. monthly admissions), it is back to fable.

## The six canonical tasks (van der Schaar)

1. **Disease-trajectory forecasting** from sparse, irregular measurements.
2. **Survival / time-to-event** with competing risks, updated as new
   longitudinal data arrive.
3. **Phenotyping / clustering** by similar *future* outcomes, not current state.
4. **Screening & monitoring**: when and what to measure next (active sensing).
5. **Early diagnosis / onset detection** before clinical manifestation.
6. **Treatment effects over time**: personalised response to interventions.

## Irregular sampling and informative missingness

The central methodological point: *why* a value is missing carries information
(a test ordered because the clinician was worried). Standard fixes that assume
missing-at-random throw this away.

- Encode the missingness: include the measurement mask and time-since-last
  observation as features (the GRU-D idea), do not just impute and forget.
- Imputation choices: last-observation-carried-forward (simple, biased for
  trends), linear/spline interpolation, multiple imputation (`mice` for
  cross-sectional structure), or model-based (Gaussian process, state-space)
  imputation that respects temporal correlation. Always carry imputation
  uncertainty downstream; single imputation understates variance.
- For genuinely irregular series, models that take (value, time) pairs directly
  (Gaussian processes, neural ODEs, attention over timestamps) avoid forcing a
  grid.

## Named methods worth knowing (and their use)

- **Dynamic-DeepHit**: longitudinal + competing-risks survival; updates the
  predicted risk as new measurements arrive. Use for evolving time-to-event
  with several outcomes.
- **Attentive State-Space Models**: learn interpretable disease states with
  attention to capture non-Markovian dynamics; good when you want phenotypes
  with some interpretability.
- **Deep Sensing / active sensing**: decide which measurement to take next given
  cost vs information; for screening/monitoring design.
- **TimeGAN**: generate realistic synthetic time series preserving temporal
  correlation; for augmentation or privacy-preserving sharing.
- **DynaMask** and similar: per-timestep feature-importance explanations for a
  temporal model; for interpretability/audit.

These are research methods, mostly Python. The lab's own libraries:
- **TemporAI** (Python): clinical time-series prediction, time-to-event, and
  treatment-effects-over-time pipelines.
- **Clairvoyance** (Python): end-to-end clinical decision-support pipeline.

## What to do in R vs Python

- **R, classical longitudinal** (often enough, prefer it for inference):
  - Mixed-effects / growth models: `lme4`, `nlme`, `brms` (Bayesian) for
    trajectories with random effects per patient.
  - Joint models (longitudinal + survival): `JM`, `JMbayes2`.
  - Landmarking for dynamic prediction; time-varying-covariate Cox (`survival`).
  - Time-varying treatment effects with confounding: marginal structural models
    / g-methods (`ipw`, `gfoms`, targeted learning `lmtp`).
- **Python, deep/representation learning**: TemporAI, the named architectures
  above, `sktime`/`tslearn` for classification/clustering, when you have many
  patients, long sequences, and prediction (not inference) is the goal.

Default stance: try the classical, interpretable R model first (mixed model,
joint model, MSM). Move to deep methods only when sample size, sequence length,
and a prediction-not-inference goal justify the loss of interpretability, and
validate against a simple baseline (IRON RULE 4 still applies).

## Validation for clinical series

- Split by **patient**, never by row, to avoid leakage across a patient's own
  timeline.
- Use time-aware validation (predict future visits from past) when the use case
  is dynamic prediction.
- Report calibration and discrimination over time (time-dependent AUC,
  Brier score), not just a single number.
- For any clinical prediction model intended for a paper, follow **TRIPOD**
  (and TRIPOD-AI for ML); the `peer-reviewer` skill checks against it.

## Relation to the user's TB work

Most Nikshay work is aggregate surveillance (counts per TU per month), which is
the `epi-surveillance.md` + fable path. This file applies if the project moves
to **patient-level** TB data: treatment trajectories, loss-to-follow-up or
mortality as longitudinal survival, or per-patient outcome prediction. In that
case start from joint/mixed models in R and escalate deliberately.
