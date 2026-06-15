# Statistical foundations

The theory behind the workflow, distilled from Peng, *Time Series Analysis*
(biomedical/public-health framing). Read this when a question is about *why* a
method works, when its assumptions hold, or when you need machinery fable does
not expose (spectral analysis, Kalman filtering, point processes). Not every
analysis needs this, but the IRON RULES rest on it.

## Temporal data structure and stationarity

A time series is observations indexed by time, with dependence between nearby
observations, the dependence is the signal, and it is what breaks ordinary iid
statistics.

- **Strict vs weak (covariance) stationarity.** Weak stationarity: constant
  mean, constant variance, and an autocovariance that depends only on the lag,
  not on time. Most classical methods (ARMA, spectral) assume it.
- **Why it matters.** Non-stationary series (trend, unit root, changing
  variance) give spurious regressions and invalid inference. Achieve
  stationarity by differencing (trend/unit root), seasonal differencing
  (seasonality), or a variance-stabilising transform (log/Box-Cox), then model
  the stationary part.
- **Tests.** KPSS (`unitroot_kpss`, H0 = stationary), ADF/PP (H0 = unit root);
  `unitroot_ndiffs` / `unitroot_nsdiffs` recommend how many differences. Do not
  over-difference (it injects negative autocorrelation and inflates variance).

## Autocorrelation and partial autocorrelation

- **ACF** r_k: correlation between y_t and y_{t-k}. White noise has ACF ≈ 0 at
  all non-zero lags (within ±1.96/√n bands). Slow decay → non-stationary/trend;
  spikes at seasonal lags → seasonality.
- **PACF**: correlation at lag k after removing the effect of intervening lags.
- **Order identification.** AR(p): PACF cuts off after lag p, ACF tails off.
  MA(q): ACF cuts off after lag q, PACF tails off. ARMA: both tail off. This is
  the manual counterpart to `ARIMA()` auto-selection, use it to sanity-check the
  automated orders.
- **Ljung-Box** tests joint whiteness of residual autocorrelations (IRON RULE 6).

## Frequency / spectral analysis

A complementary view: decompose the series into oscillations at different
frequencies. Useful for finding hidden periodicities and for filter design.

- **Fourier transform / DFT, computed by the FFT.** The **spectral density** /
  periodogram shows how variance distributes across frequencies; a peak at
  frequency f means a cycle of period 1/f.
- **Smoothing the periodogram** (it is a noisy estimate of the spectrum) via
  spans/kernels: `spectrum()`, `spec.pgram()` in base R; `astsa` for teaching.
- **Filters.** Low-pass (keep slow movements → trend/seasonal adjustment),
  high-pass (keep fast movements), band-pass. Moving averages are low-pass
  filters; differencing is a high-pass filter. The **Hodrick-Prescott filter**
  separates trend from cycle (common in the rleripio/economics workflow; beware
  its end-point and spurious-cycle issues).
- **Exponential smoothing** can be read as a particular linear filter, linking
  this view to ETS.
- When to use the frequency domain: detecting/confirming periodicity, designing
  seasonal adjustment, analysing physiological signals; less so for short
  business/epi count series where the time-domain ARIMA/ETS path is simpler.

## Time-series regression and temporal confounding

Regression with time-series data, the Peng emphasis on getting standard errors
and confounding right.

- **Residual autocorrelation** breaks OLS standard errors (too small → false
  significance). Fixes: model the error structure (regression with ARIMA
  errors, GLS), or use HAC/Newey-West robust SEs. This is exactly why
  interrupted time series uses ARIMA errors (see `epi-surveillance.md`).
- **Distributed lag models**: effects of a predictor spread over several lags
  (e.g. exposure now affecting outcomes over following weeks); the lag structure
  is the estimand.
- **Temporal confounding**: shared trend or seasonality between exposure and
  outcome creates association with no causal link. Adjust for trend and season
  (splines of time, harmonic terms), or difference, to remove common temporal
  structure before interpreting an effect. Standard in environmental
  epidemiology (air pollution and mortality) and applicable to programme
  evaluation.

## State-space models and the Kalman filter

A unifying framework: an unobserved **state** evolves over time (transition
equation) and generates noisy **observations** (measurement equation). ETS,
ARIMA, structural time-series, dynamic regression, and dynamic factor models are
all special cases.

- **Kalman filter**: recursive optimal (MMSE, exact for linear-Gaussian)
  estimation of the hidden state as each observation arrives; the smoother uses
  all data for in-sample state estimates. Applications in the book: tracking
  position, estimating a rocket's apogee, and biomedical signals.
- **Why use it explicitly.** Time-varying parameters (a regression coefficient
  that drifts), missing observations handled natively, multi-rate / mixed-
  frequency data, and online updating. The rleripio state-space chapter
  (time-varying coefficients, dynamic factor models, mixed frequency) lives here.
- **R tools.** `KFAS`, `dlm`, `bsts` (Bayesian structural time series),
  `MARSS` (multivariate state-space for ecology/biology). fable's ETS/ARIMA use
  state-space internally but do not expose arbitrary custom states; reach for
  these packages when you need a bespoke state equation.

## Maximum likelihood estimation

How AR/ARMA/state-space models are actually fit.

- **AR(1), AR(2)** likelihoods are tractable illustrations: condition on initial
  values (conditional likelihood) or include their distribution (exact/full
  likelihood). Estimates come from numerically maximising the (Gaussian)
  likelihood; the Kalman filter provides the likelihood for state-space models.
- **Practical consequences.** AICc/BIC for order selection are likelihood-based
  and only comparable within the same likelihood/family (see `evaluation.md`).
  Convergence can fail for near-non-stationary or over-parameterised models;
  simplify or re-difference.

## Point processes (event-time data)

When the data is *times of events* (not counts on a grid), the right object is a
point process, not a tsibble.

- **Poisson process**: events at constant rate λ; inter-event times are
  exponential. Inhomogeneous Poisson: time-varying rate λ(t).
- **Conditional intensity** models: the instantaneous event rate given history;
  self-exciting (Hawkes) processes where past events raise the near-term rate,
  the natural model for clustered events (the book's earthquake example;
  epidemiologically, contagion/clustering of cases).
- **Relevance.** Outbreak clustering, recurrent clinical events, and any
  irregular event stream. R tools: `spatstat` (spatial/spatio-temporal point
  patterns, relevant to the user's spatial-epi work), `hawkes`/`emhawkes`,
  `ppstat`. Aggregate to counts only if the grid is fine enough not to lose the
  clustering you care about.

## Convergence and panel time series (inequality over time)

A recurring epi/economics question: are units (districts, states, countries)
becoming more alike over time, or is the gap between them persisting? Two
distinct quantities answer it, and they are not interchangeable.

- **Sigma-convergence** is the one that actually answers "is the gap closing":
  the dispersion of the cross-section, measured each period and tracked over
  time. Use the SD of log(rate), the population-weighted coefficient of
  variation, the Theil index, or the Gini. Falling dispersion = sigma-
  convergence. This is the primary inequality measure; report it first.
- **Beta-convergence** asks "do initially-low units grow faster?": regress each
  unit's growth (or its fitted per-unit slope) on its baseline level; a negative
  coefficient is catch-up. Beta is **necessary but not sufficient** for sigma
  (Quah): units can catch up on average while the spread stays constant or
  widens, because new dispersion is continually generated. Never conclude "the
  gap is closing" from beta alone.

### The Galton / regression-to-the-mean trap

Beta-convergence regresses change on baseline, and baseline appears (with
opposite sign) on both sides of that relationship. If the baseline is **measured
with error**, this induces a spurious negative beta even when there is no true
convergence (Galton's fallacy; Friedman 1992; Quah 1993). For small-area
epidemiological rates this is acute: a district with few cases has a noisy rate,
and a year that happened to be high by chance is expected to fall back, which
reads as "catch-up". A small negative beta on noisy small-area data is the
default artefact, not evidence.

Defences (use at least one):
- **Shrink the rates first.** Apply Empirical-Bayes (`spdep::EBest`,
  `EBlocal`) or a hierarchical/BYM smoother to each period's small-area rate
  before computing dispersion or fitting beta. Raw small-area CNR inflates
  sigma every period (so a real narrowing is masked) and biases beta negative.
  Use the *same* smoothing the cross-sectional companion analysis uses, an
  inconsistency between a temporal panel on raw rates and a cross-section on
  EB rates is a real defect.
- **Split-sample / instrumented baseline.** Estimate the baseline level from one
  subsample (e.g. odd months) and the growth from another (even months), or
  instrument the baseline, so measurement error does not leak into the
  regressor.
- **Lead with sigma.** Since sigma is the quantity of interest and is less prone
  to this bias, treat beta as supporting evidence only.

### Estimating the per-unit trend

Classifying units as rising/stable/falling, or feeding beta, by **endpoint
change** (last vs first period, e.g. a +/-10% rule) is the noisiest possible
estimator and is hostage to an anomalous endpoint (a recovery year, a lag-
affected final period). Prefer a **fitted slope** per unit (`lm(log(rate) ~
year)` over all periods) with its standard error, and classify on the slope and
its CI, not on two points.

### Uncertainty (IRON RULE 5 for descriptive indices)

A coefficient of variation, Theil/Gini, seasonal amplitude, or convergence slope
is an estimate with sampling error, report an interval. The clean general tool
is the bootstrap, matched to the dependence structure:
- **Cross-sectional inequality** (CV/Theil/Gini in a given period): resample the
  units (districts) with replacement, recompute the index, take percentiles.
- **Time-domain quantities** (a trend slope, a seasonal amplitude from a series):
  use a **block bootstrap** (`tsbootstrap`, `boot::tsboot`, or a moving-block
  resample) so serial dependence is preserved, an iid bootstrap understates the
  variance of anything estimated from an autocorrelated series.
- **Convergence slope**: bootstrap over units; a small beta whose CI spans zero
  is not convergence.

### Tools and scope

Plain `lm` + a bootstrap covers most epi convergence work; `plm` for formal
panel models (fixed/random effects), `spdep`/`spatialreg` when convergence is
spatial (neighbours influence each other). The macro "unit-root panel
convergence" tests (Im-Pesaran-Shin and kin) are usually overkill for short
(<10-period) epi panels, name them only if a reviewer expects them.

## When foundations change the answer

- A "trend" that is a unit root vs a deterministic trend implies different models
  and very different long-horizon forecasts, test, do not assume.
- Significant covariate effects can be artefacts of residual autocorrelation or
  shared seasonality, check residuals and adjust for time.
- A periodicity invisible in the time plot can be obvious in the periodogram.
- Irregular event timing is a point process, forcing it onto a grid discards the
  process you are studying.
