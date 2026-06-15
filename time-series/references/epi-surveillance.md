# Public-health & epidemiology time series

The layer that matters most for the user's work: TB notification and
surveillance series (Nikshay), counts at TU/district/state level, where the
data-generating process is discrete, often low-count, seasonal, and tied to a
shifting denominator. fable is the workhorse, but several epi tasks need
methods around or beyond it.

## Counts, not Gaussians

Notification counts are non-negative integers, often small in a single TU, often
with structural zeros. Gaussian forecasts (default ETS/ARIMA) can produce
negative point forecasts and intervals that cross zero, which is meaningless.

Options, in rough order of effort:

1. **Transform + bias-adjust.** Fit `ETS(log(cases + 1))` or a Box-Cox; fable
   back-transforms with bias adjustment and keeps forecasts positive. Cheap,
   often adequate for moderate counts. State the offset.
2. **Model the rate with an offset.** When the denominator (population, eligible
   pop) changes, model the rate, not the count. In a count GLM use
   `offset(log(pop))` so coefficients are on the log-rate scale; forecast the
   count back as rate x pop. (See denominator note below.)
3. **Count regression with seasonality.** Poisson / Negative Binomial GLM with
   harmonic terms (`sin`/`cos` of month) and a trend, plus offset. NegBin for
   overdispersion (almost always present in surveillance counts). Packages:
   base `glm`, `MASS::glm.nb`; `glarma` for GLM with ARMA-type autocorrelation;
   `tscount`/INGARCH for autoregressive count processes with proper count
   distributions and interval coverage.
4. **Intermittent/sparse** (many zeros, small TUs): Croston (`CROSTON()`), or
   aggregate up (to district or to a coarser interval) until counts are stable
   enough to model, then optionally reconcile back down.

Always check coverage of count-model intervals; that is where the count vs
Gaussian choice pays off.

## Aberration / outbreak detection

Detecting when current counts exceed expectation, the classic surveillance task.
Use the `surveillance` R package (and `sts` objects) for the established
algorithms; do not hand-roll these.

- **EARS C1 / C2 / C3** (Early Aberration Reporting System): moving mean+SD over
  a short baseline window; C2 skips a 2-day guardband, C3 sums recent
  statistics. Good for limited history / fast signals.
- **Farrington / improved Farrington (`farringtonFlexible`)**: the European
  standard. Overdispersed Poisson GLM on comparable weeks from previous years,
  with trend and seasonality, downweighting past outbreaks; flags when current
  count exceeds an upper threshold. Best when you have several years of history.
- **CUSUM / GLR**: cumulative-sum control charts for detecting small persistent
  shifts; tunable to a target change size.
- **Bayesian (`boda`, `bodaDelay`)**: handle reporting delay and produce
  probabilistic alarms.

```r
library(surveillance)
sts_obj <- sts(observed = counts_matrix, start = c(2018, 1), frequency = 12)
res <- farringtonFlexible(sts_obj, control = list(
  range = recent_idx, b = 4, w = 3, trend = TRUE,
  pastWeeksNotIncluded = 1, thresholdMethod = "nbPlugin"))
plot(res)   # alarms where observed exceeds the upper bound
```

Pair detection with forecasting: a forecast's prediction interval is itself an
expectation band; an actual above the upper interval is a candidate aberration.

## Interrupted time series (did the intervention change things?)

Quasi-experimental evaluation of a policy/programme change at a known time.
Model level and slope, with a step (immediate level change) and a ramp (slope
change) from the intervention point. Use dynamic regression so autocorrelated
errors do not fake significance.

```r
ds <- series |> mutate(
  step = as.integer(month >= intervention),
  ramp = pmax(0L, as.integer(month - intervention) + 1L)
)
fit <- ds |> model(its = ARIMA(cases ~ step + ramp + fourier(K = 2) + PDQ(0,0,0)))
report(fit)   # step coef = level change; ramp coef = slope change post-intervention
```

Notes: control for seasonality (Fourier/season) and underlying trend; check for
autocorrelation (that is why ARIMA errors, not OLS); consider a counterfactual
forecast (fit pre-intervention, forecast the post period, compare to observed);
for count outcomes use a Poisson/NegBin ITS (segmented regression with offset)
rather than Gaussian. Watch for co-interventions and time-varying confounders.

## Seasonality quantification

- STL `seasonal_strength_year` from `features()` to rank/quantify seasonality
  across many series.
- Seasonal subseries plots (`gg_subseries`) to see the shape and any drift in the
  seasonal pattern.
- For TB specifically, expect and test for an annual cycle (notification dips and
  surges tied to season and to reporting/administrative calendars). Distinguish
  true epidemiological seasonality from reporting-artifact seasonality
  (month-length, quarter-end reporting pushes).

## Effective reproduction number (Rt)

Not a fable task. For renewal-equation Rt estimation from incidence use
`EpiEstim` (Cori method, requires a serial-interval distribution) or
`EpiNow2`/`epinowcast` (Bayesian, jointly handles reporting delay, right
truncation, and Rt with uncertainty). TB's long and variable generation time
makes Rt less standard than for acute infections; prefer trend/forecast framing
unless Rt is specifically requested.

## Nowcasting (correcting for reporting delay)

Recent counts are incomplete because of notification lag, raw recent points
understate the truth and look like a spurious decline. Correct before
forecasting or interpreting trends. Tools: `surveillance::nowcast`,
`epinowcast`, or a reporting-triangle/delay-distribution model. With Nikshay,
characterise the delay distribution (notification date vs entry date) and
nowcast the most recent weeks/months; never read the last few raw points as a
real downturn.

## Denominators (the user's binding constraint)

Rates need a denominator, and at TU level the denominator (crosswalk to
population) is itself a research object in this project. Practical guidance:
- Model **rates** only where the denominator is trustworthy; otherwise model
  counts and report counts, stating the denominator caveat.
- Keep population as a time-varying offset if it changes over the series.
- When forecasting rates, decide whether to hold the denominator fixed or
  project it, and state which (IRON RULE 8).
- Spatial-temporal hierarchy (TU within district within state) is a natural fit
  for `aggregate_key` + `min_trace` reconciliation, see `models.md`; this also
  borrows strength for small, noisy TU series.

## Reporting (epi write-up)

A surveillance/forecasting methods paragraph should state: data source and case
definition; geographic level and time unit; how reporting delay/incompleteness
was handled (nowcasting or exclusion of recent points); the count/rate model and
its distribution; seasonality and trend handling; validation scheme and accuracy
(out-of-sample, with baseline); and software versions. Match TB notification
claims to the evidence and hand the prose to `academic-writer`.
