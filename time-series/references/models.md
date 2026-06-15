# Model catalogue and decision guide

Every entry: what it is, when to use it, the `fable` call, and the gotchas.
Always fit alongside the baselines (IRON RULE 4).

## Baselines (always include)

```r
fit <- train |> model(
  mean   = MEAN(y),              # average of history
  naive  = NAIVE(y),            # last value (random walk)
  snaive = SNAIVE(y),          # last value from same season
  drift  = RW(y ~ drift())     # last value + average trend
)
```

`SNAIVE` is the bar to beat for any seasonal series; `NAIVE`/drift for
non-seasonal. If your model loses to these out-of-sample, ship the baseline.

## ETS (exponential smoothing, innovations state space)

What: weighted averages of past observations with weights decaying
geometrically; the modern formulation is a state-space model with Error /
Trend / Seasonal components, each None / Additive / Multiplicative (+ damped
trend). `ETS()` selects the (E,T,S) form by AICc.

When: the robust default for series with trend and/or seasonality and no
external drivers. Often the best off-the-shelf seasonal forecaster.

```r
ETS(y)                                   # auto-select
ETS(y ~ error("M") + trend("Ad") + season("M"))   # multiplicative, damped
ETS(log(y))                              # log for variance growing with level
```

Gotchas: ETS handles one seasonal period only; multiplicative needs strictly
positive data; damped trend (`"Ad"`) usually forecasts long horizons more
safely than additive. Compare ETS vs ARIMA by out-of-sample accuracy, not AICc
(different likelihoods, not comparable across families).

## ARIMA

What: AutoRegressive Integrated Moving Average. `ARIMA(p,d,q)(P,D,Q)[m]`:
differencing (d, D) to reach stationarity, AR terms (p, P), MA terms (q, Q),
at non-seasonal and seasonal lags. `ARIMA()` does a stepwise AICc search over
orders and differencing.

When: autocorrelation structure is the story; you want differencing to handle
trend/unit roots; or you need to add regressors (dynamic regression below).

```r
ARIMA(y)                                  # auto (stepwise)
ARIMA(y, stepwise = FALSE, approximation = FALSE)   # fuller, slower search
ARIMA(y ~ pdq(1,1,1) + PDQ(0,1,1))       # fix orders
report(fit)                               # read the chosen orders + coefficients
```

Manual order ID (when you want to understand, not just auto-fit):
- Differencing: `unitroot_ndiffs`, `unitroot_nsdiffs`; KPSS via `features(y, unitroot_kpss)`. Difference until stationary, no more (over-differencing inflates variance).
- After differencing, read ACF/PACF: AR(p) → PACF cuts off at p, ACF tails; MA(q) → ACF cuts off at q, PACF tails.

Gotchas: `ARIMA()` defaults to a fast stepwise search that can miss the best
model, widen it for final models. The chosen model depends on the
transformation, so set it inside the formula. Confidence intervals assume the
orders are known (they ignore order-selection uncertainty).

## Dynamic regression (regression with ARIMA errors)

What: a regression on covariates where the errors follow an ARIMA process.
Separates the explained part (covariates) from the autocorrelated noise. This
is the engine for interrupted time series and for forecasting with drivers.

```r
ARIMA(y ~ x1 + x2)                        # auto ARIMA on the residuals
ARIMA(y ~ step + ramp)                    # interrupted TS: level + slope change
```

When: you have meaningful covariates (calendar effects, a policy intervention,
lagged predictors, temperature) and OLS residuals are autocorrelated (so plain
`TSLM` intervals would be wrong).

Gotchas: to forecast you must supply future covariate values (`new_data`); the
forecast inherits their uncertainty (IRON RULE 8). Coefficients are interpreted
on the regression part; the ARIMA part is nuisance structure.

## Dynamic harmonic regression (complex/long seasonality)

What: model seasonality with Fourier terms and let ARIMA handle the rest.
Smooth, parsimonious for long or multiple seasonal periods where a seasonal
ARIMA would need huge orders.

```r
ARIMA(y ~ fourier(K = 3) + PDQ(0,0,0))                 # one seasonality
# multiple seasonality (e.g. weekly + annual on daily data):
ARIMA(y ~ fourier(period = "week", K = 3) +
          fourier(period = "year", K = 10) + PDQ(0,0,0))
```

Choose K by minimising AICc (more harmonics = wigglier seasonal shape). Set
`PDQ(0,0,0)` so seasonality is captured by the Fourier terms, not seasonal ARIMA.

## TSLM (time series linear model)

What: ordinary linear regression with time-series helpers (`trend()`,
`season()`, `fourier()`). Fast, interpretable, but assumes uncorrelated errors.

```r
TSLM(y ~ trend() + season())
TSLM(y ~ trend() + fourier(K = 2) + holiday + temp)
```

When: a transparent descriptive/explanatory model, or a quick covariate check.
If residuals are autocorrelated (check `ljung_box`), move to `ARIMA(y ~ ...)`
for valid inference and intervals.

## Prophet (fable.prophet)

What: decomposable model (piecewise-linear/logistic trend + Fourier
seasonality + holidays) from Meta. Handles multiple seasonalities, holiday
effects, missing data, and automatic change points; tolerant and fast.

```r
library(fable.prophet)
prophet(y ~ season(period = "year", order = 10) + holiday(holidays_tbl))
```

When: many seasonalities + known holidays/events, analyst-friendly defaults,
business-style series. Often competitive, rarely the single best; treat as a
strong challenger. For epi count series it does not respect count distributions.

## NNETAR (neural network autoregression)

What: a feed-forward neural net with lagged values (and seasonal lags) as
inputs. Nonlinear, single hidden layer; forecasts simulated forward.

```r
set.seed(1)                               # stochastic
NNETAR(y)
NNETAR(sqrt(y) ~ AR(p = 12))
```

When: nonlinearity is plausible and you have enough data. Needs a seed; intervals
come from simulation; prone to overfitting, validate hard. A challenger, not a default.

## VAR (vector autoregression)

What: each of several series regressed on lags of itself and the others;
captures feedback/dynamic interdependence.

```r
VAR(vars(y1, y2) ~ AR(p = 2))
```

When: several series influence each other and you want joint forecasts or
impulse-response/Granger reasoning. Watch parameter explosion (p x k^2).

## THETA, croston, and friends

- `THETA(y)`: simple, strong benchmark, good for M-competition-style series.
- `CROSTON(y)`: intermittent demand (many zeros) via Croston's method, relevant for sparse low-count series.

## Model combinations

Averaging diverse, individually-good models usually lowers error and is robust.

```r
fit |> mutate(combo = (ets + arima) / 2)          # average fitted models
combination_model(ETS(y), ARIMA(y))               # inside model()
```

## Hierarchical and grouped reconciliation

When series nest (TU within district within state) or cross-classify
(district x age x sex), forecast all levels and **reconcile** so they add up
coherently. MinT (minimum trace) reconciliation typically beats bottom-up or
top-down and improves accuracy at every level.

```r
agg <- notif |>
  aggregate_key(state / district / tu_id, cases = sum(cases))    # hierarchy
  # aggregate_key((state/district) * age, cases = sum(cases))    # grouped

fit <- agg |> model(base = ETS(cases)) |>
  reconcile(
    bu   = bottom_up(base),
    ols  = min_trace(base, method = "ols"),
    mint = min_trace(base, method = "mint_shrink")   # usually best
  )

fc <- fit |> forecast(h = "12 months")
fc |> filter(is_aggregated(district)) |> accuracy(agg)
```

Notes: `aggregate_key()` builds all aggregation levels; `is_aggregated()` /
`agg_vec` filter levels; `min_trace(method = "mint_shrink")` is the default
recommendation. Reconciliation is coherent for distributions too
(reconciled prediction intervals).

## Decision summary

| Situation | First choice | Challenger |
|-----------|--------------|------------|
| Trend + one seasonality, no drivers | ETS | ARIMA |
| Autocorrelation is the story / need regressors | ARIMA / dynamic regression | ETS |
| Multiple or long seasonality | dynamic harmonic regression | Prophet, STL+ETS |
| Known holidays/events, many seasons | Prophet | harmonic regression |
| Covariate effect / interrupted TS | ARIMA(y ~ x) or TSLM | — |
| Several interacting series | VAR | per-series ARIMA |
| Counts / many zeros | count model (see epi-surveillance.md) / Croston | log-ETS + bias adj |
| Nested/cross-classified series | base model + min_trace reconcile | bottom-up |
| Nonlinear, lots of data | NNETAR | ARIMA |
| Need a robust ensemble | combination of ETS + ARIMA | — |
