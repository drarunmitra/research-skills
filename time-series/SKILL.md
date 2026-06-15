---
name: time-series
version: 1.0.0
description: |
  Analyse and forecast time series in R using the tidyverts ecosystem
  (tsibble, feasts, fable). Covers the full workflow: indexing and gap-filling,
  decomposition and feature extraction, exploratory graphics, model fitting
  (ETS, ARIMA, dynamic regression, TSLM, NNETAR, Prophet, VAR, baselines),
  distributional forecasting, time-series cross-validation, accuracy and
  residual diagnostics, and hierarchical/grouped reconciliation. Adds a
  statistical-foundations layer (stationarity, ACF/PACF, spectral analysis,
  state-space/Kalman, point processes) and a public-health/epidemiology layer
  (surveillance, aberration/outbreak detection, interrupted time series,
  count-data models, seasonality, nowcasting) plus a healthcare-ML layer
  (irregular sampling, informative missingness, longitudinal survival,
  treatment effects). Use to explore, model, forecast, evaluate, or write up
  any temporal data, especially epidemiological surveillance and notification
  series.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - WebSearch
  - WebFetch
---

# Time Series

Build, evaluate, and write up time-series analyses the way a careful applied
forecaster would. The default toolchain is the **tidyverts** stack
(`tsibble` + `feasts` + `fable`), the workflow taught in Hyndman &
Athanasopoulos, *Forecasting: Principles and Practice* (3rd ed). Where a
question needs deeper statistical machinery or a clinical-ML method that
`fable` does not cover, this skill points to the right tool and the right
reference file instead of forcing everything through one package.

This is an *analysis* skill, not just a code generator. It enforces a
disciplined workflow (look at the data first, hold out a test set, evaluate
distributions not just point forecasts, check residuals) and matches the
method to the data-generating process rather than reaching for one model.

## When to use

Trigger on requests such as:
- "Forecast these case counts / notifications / admissions for the next N periods"
- "Is there a trend / seasonality / change point in this series?"
- "Decompose this series" / "extract time-series features" / "cluster these series"
- "Which forecasting model should I use here?" / "ETS or ARIMA?"
- "Evaluate / back-test my forecasts" / "set up time-series cross-validation"
- "Detect an outbreak / aberration / anomaly in this surveillance series"
- "Did the intervention change the trend?" (interrupted time series)
- "Reconcile forecasts across districts / age groups / a hierarchy"
- "Handle irregular sampling / informative missingness in clinical time series"
- Anything involving `ts`, `tsibble`, `fable`, `forecast`, `prophet`, ARIMA, ETS, STL

For the user's own work this most often means **TB notification / surveillance
series from Nikshay**: monthly or weekly counts at TU / district / state level,
where seasonality, count distributions, denominators, and spatial-temporal
hierarchy all matter. Lean into that context.

## The five sources this skill distils

1. **fpp3** (otexts.com/fpp3) — the canonical tidyverts workflow and the spine of this skill: graphics, decomposition, features, the forecaster's toolbox, ETS, ARIMA, dynamic regression, hierarchical reconciliation, evaluation.
2. **fable.tidyverts.org** — package-level API for model specification, `forecast()`, `accuracy()`, `reconcile()`, distributional forecasts.
3. **rleripio / R for Economic Research** (book.rleripio.com) — applied, workflow-first philosophy: reproducible pipeline (`renv`), rolling/lagged transforms, seasonal adjustment, HP filter, scenario and analogy forecasting, state-space (time-varying coefficients, dynamic factor, mixed frequency). The guiding line: traditional statistical methods, well-validated, usually beat exotic ones.
4. **Peng, *Time Series Analysis*** (bookdown.org/rdpeng/timeseriesbook) — the statistical-foundations layer: temporal data structure, stationarity, frequency/spectral analysis (Fourier, FFT, filters), time-series regression and temporal confounding, state-space and the Kalman filter, MLE for AR models, point processes (Poisson, conditional intensity). Biomedical/public-health framing throughout.
5. **van der Schaar Lab, Time Series in Healthcare** — the clinical-ML layer: disease-trajectory forecasting from sparse irregular data, longitudinal survival with competing risks (Dynamic-DeepHit), attentive state-space phenotyping, active sensing (Deep Sensing), synthetic generation (TimeGAN), explainability (DynaMask). The core lesson: in clinical series, *missingness is informative* and true states are unobserved, so static modelling assumptions break.

## Core workflow (tidyverts)

Every analysis runs this pipeline. Do not skip step 1 or step 5.

```
1. tsibble   →  index + key; fix gaps; transform           (look at the data)
2. feasts    →  decompose (STL), plot (gg_season etc.), ACF, features
3. fable     →  specify competing models in one model() call
4. forecast  →  h-step distributional forecasts
5. evaluate  →  train/test + time-series CV; accuracy(); residual diagnostics
6. (reconcile / report / write up)
```

```r
library(fpp3)   # loads tsibble, feasts, fable, dplyr, ggplot2, lubridate, tidyr

# 1. Make a tsibble: index = time column, key = series identifier(s)
notif <- raw |>
  mutate(month = yearmonth(date)) |>
  as_tsibble(index = month, key = c(state, tu_id)) |>
  fill_gaps(cases = 0L)            # implicit missings -> explicit (counts often 0)

# 2. Explore
notif |> filter(tu_id == "X") |> autoplot(cases)
notif |> filter(tu_id == "X") |> gg_season(cases)
notif |> filter(tu_id == "X") |> model(STL(cases)) |> components() |> autoplot()

# 3-4. Fit competing models on a training set, forecast the horizon
train <- notif |> filter(month <= yearmonth("2024 Dec"))
fit <- train |>
  model(
    snaive = SNAIVE(cases),
    ets    = ETS(cases),
    arima  = ARIMA(cases),
    harmonic = ARIMA(cases ~ fourier(K = 2) + PDQ(0,0,0))
  )
fc <- fit |> forecast(h = "12 months")

# 5. Evaluate against the held-out test set
fc |> accuracy(notif)
fit |> augment() |> features(.innov, ljung_box, lag = 24)  # residual whiteness
```

See `references/workflow-fable.md` for the full annotated recipe (transforms,
`fill_gaps`, `stretch_tsibble` CV, `hilo()` intervals, `glance`/`tidy`/`report`).

## Task modes

Detect the mode from the request; most jobs combine a few. State which you are running.

| Mode | Trigger | What it does | Reference |
|------|---------|--------------|-----------|
| **Explore** | "look at", "is there a trend/season", "decompose", "features" | tsibble + feasts: time/season/subseries/lag plots, ACF, STL, `features()` | `workflow-fable.md` |
| **Forecast** | "forecast", "predict the next N" | fit competing models, distributional `forecast(h=)`, intervals | `models.md`, `workflow-fable.md` |
| **Choose-model** | "ETS or ARIMA?", "which model" | decision guide by series properties + always-include baselines | `models.md` |
| **Evaluate** | "back-test", "cross-validate", "is it any good" | train/test split, `stretch_tsibble` CV, accuracy metrics, residual + distributional diagnostics | `evaluation.md` |
| **Reconcile** | "across districts/ages", "hierarchy", "bottom-up vs top-down" | `aggregate_key`, `reconcile(min_trace())`, coherent forecasts | `models.md` |
| **Surveillance** | "outbreak", "aberration", "anomaly", "interrupted time series", "Rt", "nowcast", "count data" | epi-specific methods beyond/around fable | `epi-surveillance.md` |
| **Clinical-ML** | "irregular sampling", "missingness", "patient trajectory", "longitudinal survival", "treatment effect over time" | when fable is the wrong tool; van der Schaar methods + R/Python options | `healthcare-ml.md` |
| **Foundations** | "stationarity", "spectral/Fourier", "Kalman", "state space", "point process", "convergence", "sigma/beta", "inequality over time", theory | the statistical machinery and when it matters | `foundations.md` |

## Choosing a model (quick guide)

Full version with code and tie-breakers in `references/models.md`. First principles:

1. **Always fit baselines.** `NAIVE`, `SNAIVE` (seasonal), `RW(y ~ drift())`, `MEAN`. A model that cannot beat `SNAIVE` out-of-sample is not worth shipping. This is non-negotiable (Iron Rule 4).
2. **Match the structure.**
   - Trend + seasonality, automatic, robust default → **ETS** (exponential smoothing state-space). Multiplicative for variance that grows with level, or log-transform first.
   - Autocorrelation structure / want differencing + AR/MA, or external regressors → **ARIMA** (use `ARIMA()` auto-selection, then inspect).
   - **Complex / multiple / non-integer seasonality** (weekly+annual, daily) → dynamic harmonic regression: `ARIMA(y ~ fourier(period, K) + PDQ(0,0,0))`, or **Prophet** (`fable.prophet`) for many seasonalities + holidays + change points, or STL + ETS on the seasonally adjusted series.
   - **Covariates / interventions** (calendar effects, a policy step, lagged drivers) → `TSLM()` for simple regression, or **dynamic regression** `ARIMA(y ~ xreg)` when residuals are autocorrelated. This is the engine for interrupted time series.
   - **Multivariate / feedback between series** → `VAR()`.
   - **Nonlinear, enough data** → `NNETAR()` (neural net autoregression). Treat as a challenger, not a default.
3. **ETS vs ARIMA**: not nested in general; compare by out-of-sample accuracy (and AICc only within a family). ETS often wins on seasonal business/epi data; ARIMA when autocorrelation is the story or you need regressors.
4. **Counts / rare events** (low TB counts in small TUs, zeros) → Gaussian forecasts can go negative and misstate intervals. Use a log/Box-Cox transform with bias adjustment, model rates with a population offset, or move to count models (INGARCH/`tscount`, Poisson/NegBin GLM with harmonic terms, `glarma`). See `epi-surveillance.md`.
5. **Combine.** Simple averages of good, diverse models (e.g. ETS + ARIMA) frequently beat any single model. `combination_model()` or just average the forecasts.

## IRON RULES

These are non-negotiable. A time-series analysis that breaks one is unreliable.

1. **Plot the series before modelling.** Time plot, seasonal plot, and ACF at minimum. Most modelling errors are visible in the first plot (level shifts, missing seasonality, variance growth, outliers, gaps).
2. **Make implicit missings explicit.** Run `has_gaps()` / `scan_gaps()` and `fill_gaps()` before any model. A `tsibble` with hidden gaps silently corrupts lags, ACF, and seasonal models. For counts, a gap usually means zero, not missing, decide deliberately.
3. **Never evaluate on the training data.** Hold out a test set at the end of the series (never random); prefer `stretch_tsibble()` time-series cross-validation. Report out-of-sample accuracy. In-sample fit (R², AICc) selects within a model family only, it does not validate forecasts.
4. **Always beat a baseline.** Report `SNAIVE`/`NAIVE`/drift alongside every "real" model. If the proposed model does not beat the seasonal naive out-of-sample, say so plainly and prefer the simpler model.
5. **Report uncertainty, not bare points.** For forecasts: prediction intervals, checked for calibration (coverage); a point forecast without an interval is not a forecast, and distributional accuracy measures (CRPS, Winkler) apply when intervals are the deliverable. The same rule binds **descriptive** summaries: any estimated index (a coefficient of variation, Theil/Gini, a seasonal amplitude, a convergence slope) carries sampling error and must be reported with an interval, via a block bootstrap (time-domain quantities) or a unit-resampling bootstrap (cross-sectional inequality), not as a single number whose stability is assumed.
6. **Check residuals.** Residuals (innovations) should be uncorrelated (`ljung_box`), zero-mean, and ideally homoscedastic and near-normal for valid intervals. Autocorrelated residuals mean information is left on the table; report it.
7. **Respect the transformation.** If you fit on a transformed scale (log, Box-Cox, rate per population), back-transform with bias adjustment and state the scale of every reported number. Never let a count forecast or its interval go negative.
8. **Do not extrapolate structure you did not establish.** Long horizons, regime changes, and external shocks are where forecasts fail. State the horizon's credibility and the assumptions (especially for any covariate you must itself forecast).

## Reproducibility

Match the user's environment and habits (see global memory):
- Use **R 4.4.1 explicitly**; the default `Rscript` on PATH is a broken empty 4.0.5.
- The user prefers **DuckDB + duckspatial** for heavy data; pull/aggregate there, model in R.
- For project work, pin packages with `renv` (the rleripio reproducibility stance). Set a seed before any stochastic model (`NNETAR`, bootstrap, MCMC).
- Prefer Quarto/R Markdown for write-ups so figures and numbers regenerate. Pair with the `academic-writer` / `research-writer` skills for the prose and the `peer-reviewer` skill before submission.

## Writing up time-series results

When the deliverable is text (a methods paragraph, a results section), follow the
user's house style (no em dashes; no bold/italic for emphasis in running prose;
claims matched to evidence). A defensible Methods paragraph names: the series and
its index/frequency; gap and transformation handling; the candidate models and
the selection criterion; the train/test or cross-validation scheme; the accuracy
measures; and software with versions. Report forecast accuracy out-of-sample with
an explicit baseline comparison, and give intervals, not just points. Hand the
draft to `academic-writer` for the final humanizing pass.

## Reference files

Load the relevant file before doing substantial work in that mode:

- `references/workflow-fable.md` — full tidyverts recipe: tsibble construction, gaps, transforms, exploratory graphics, `model()`/`forecast()`/`accuracy()`, `stretch_tsibble` CV, `report`/`tidy`/`glance`/`augment`, intervals via `hilo()`.
- `references/models.md` — model catalogue and decision guide: baselines, ETS taxonomy, ARIMA (stationarity, differencing, orders), dynamic regression & harmonic regression, TSLM, Prophet, NNETAR, VAR, combinations, and hierarchical/grouped reconciliation.
- `references/evaluation.md` — splitting, time-series cross-validation, point accuracy (MAE/RMSE/MASE/MAPE and why MASE), distributional accuracy (CRPS, Winkler, pinball, coverage), residual diagnostics, model comparison pitfalls.
- `references/epi-surveillance.md` — public-health methods: count-data models, aberration/outbreak detection (EARS C1-C3, Farrington, CUSUM, `surveillance` pkg), interrupted time series, seasonality quantification, Rt estimation, nowcasting, working with rates and denominators.
- `references/healthcare-ml.md` — clinical time series: irregular sampling and informative missingness, imputation, longitudinal survival (Dynamic-DeepHit), attentive state-space phenotyping, treatment effects over time, when to leave fable for Python/specialised tooling.
- `references/foundations.md` — Peng-style theory: temporal data structure and stationarity, ACF/PACF, frequency/spectral analysis (Fourier, FFT, filters, HP filter), time-series regression and temporal confounding, state-space and the Kalman filter, MLE for AR models, point processes, and convergence / panel time series (sigma vs beta, Galton/regression-to-the-mean bias, inequality-over-time with bootstrap uncertainty).

## Sources & attribution

Distils the tidyverts workflow from Hyndman & Athanasopoulos *Forecasting:
Principles and Practice* 3rd ed (otexts.com/fpp3) and the `fable` documentation;
the applied/reproducible philosophy from *R for Economic Research* (book.rleripio.com);
the statistical foundations from R. Peng *Time Series Analysis* (bookdown.org/rdpeng/timeseriesbook);
and the clinical-ML framing from the van der Schaar Lab's Time Series in Healthcare programme.
Original content; code idioms follow the public package APIs. No source text reproduced verbatim.

## Version history

- **1.1.0** (2026-06-11): Added a "Convergence and panel time series" section to `foundations.md` (sigma vs beta-convergence, Galton/regression-to-the-mean and measurement-error bias, small-area shrinkage before inequality/convergence, bootstrap uncertainty for inequality indices). Generalised IRON RULE 5 to require uncertainty on descriptive indices (CV, Theil/Gini, seasonal amplitude, convergence slope), not only forecasts. Prompted by applying the skill to a TB district-notification convergence manuscript.
- **1.0.0** (2026-06-11): Initial release. tidyverts-first workflow, 8 task modes, model decision guide, 8 IRON RULES, and six reference files (workflow, models, evaluation, epi-surveillance, healthcare-ML, foundations).
