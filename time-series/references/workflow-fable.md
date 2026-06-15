# Workflow: the tidyverts pipeline (tsibble → feasts → fable)

The annotated end-to-end recipe. Load with `library(fpp3)`, which attaches
`tsibble`, `feasts`, `fable`, plus `dplyr`, `tidyr`, `ggplot2`, `lubridate`.

## 1. Build a tsibble

A `tsibble` is a tidy data frame with a declared time **index** and one or more
**key** columns that together identify a single series. Index + key must be
unique; that is the contract.

```r
# Index helpers: yearmonth(), yearweek(), yearquarter(), as_date(), date-time
notif <- raw |>
  mutate(month = yearmonth(date)) |>
  as_tsibble(index = month, key = c(state, tu_id))

# Inspect the structure
notif                      # prints [interval] e.g. [1M], and the key
interval(notif)            # detected interval
key(notif); index(notif)
```

Regular interval is inferred from the index. Irregular event data (one row per
event) is a different object: keep it as a data frame or use a point-process /
survival approach (see `foundations.md`, `healthcare-ml.md`), do not force it
into a regular tsibble.

## 2. Gaps: implicit vs explicit missing (IRON RULE 2)

```r
has_gaps(notif)            # per-key: any implicit gaps?
scan_gaps(notif)           # the actual missing index values
count_gaps(notif)          # run lengths of gaps

# Make implicit missings explicit, then decide their value
notif <- notif |> fill_gaps(.full = TRUE)            # NA in the gaps
# For counts, a "missing month" usually means zero notifications:
notif <- notif |> fill_gaps(cases = 0L, .full = TRUE)
```

Decide deliberately: a true zero (no cases reported) is different from a
reporting gap (system down). If genuinely missing, leave `NA` and let the model
or an explicit imputation handle it, do not silently zero-fill reporting holes.

## 3. Transformations

Stabilise variance before modelling when spread grows with the level.

```r
# Box-Cox; lambda via Guerrero
lam <- notif |> features(cases, guerrero) |> pull(lambda_guerrero)
notif |> autoplot(box_cox(cases, lam))

# Common explicit choices
# log:        cases ~ log(cases)            (multiplicative seasonality)
# rate:       model cases with population offset (see epi-surveillance.md)
```

`fable` carries the transformation through `forecast()` and back-transforms with
bias adjustment automatically when you write the transform inside `model()`
(e.g. `ETS(log(cases))`). State the scale of every reported number (IRON RULE 7).

## 4. Explore (feasts)

```r
one <- notif |> filter(tu_id == "X")

one |> autoplot(cases)                 # time plot - always first
one |> gg_season(cases)                # seasonal plot (overlaid years)
one |> gg_subseries(cases)             # subseries by season (mean per month)
one |> gg_lag(cases, geom = "point")   # lag plots
one |> ACF(cases) |> autoplot()        # autocorrelation
one |> ACF(difference(cases)) |> autoplot()
```

### STL decomposition (the default decomposition)

```r
dcmp <- one |> model(STL(cases ~ trend(window = 13) + season(window = "periodic")))
components(dcmp) |> autoplot()
# Seasonally adjusted series = trend + remainder
components(dcmp) |> mutate(sa = cases - season_year) |> autoplot(sa)
```

### Features at scale (the power move for many series)

`features()` collapses each series to a row of numbers, so you can screen,
cluster, or rank hundreds of TUs at once.

```r
feat <- notif |> features(cases, feature_set(pkgs = "feasts"))
# Key ones: trend_strength, seasonal_strength_year, spikiness, linearity,
#           acf1, stl_e_acf1, coef_hurst, ...
feat |> select(tu_id, trend_strength, seasonal_strength_year)

# Cluster or find anomalies among series
library(broom)
pcs <- feat |> select(where(is.numeric)) |> prcomp(scale = TRUE) |> augment(feat)
pcs |> ggplot(aes(.fittedPC1, .fittedPC2)) + geom_point()
```

## 5. Model (fable)

Specify several competing models in **one** `model()` call. Each column is a
fitted model per key.

```r
train <- notif |> filter(month <= yearmonth("2024 Dec"))

fit <- train |> model(
  snaive   = SNAIVE(cases),                          # baseline (IRON RULE 4)
  drift    = RW(cases ~ drift()),
  ets      = ETS(cases),                             # auto ETS
  arima    = ARIMA(cases),                           # auto ARIMA
  harmonic = ARIMA(cases ~ fourier(K = 2) + PDQ(0,0,0)),
  combo    = combination_model(ETS(cases), ARIMA(cases))
)

fit                       # a mable (model table), one row per key
fit |> select(arima) |> report()      # full model summary for one model
fit |> select(arima) |> tidy()        # coefficients
fit |> glance()                        # AICc, BIC, sigma2 per model (within-family compare only)
fit |> select(ets) |> components() |> autoplot()
```

`model()` fits each key independently and tolerates failures (a model that
cannot fit one series returns `NULL` for that cell, with a warning).

## 6. Forecast

```r
fc <- fit |> forecast(h = "12 months")      # or h = 12
fc                          # a fable: distribution column `.mean` + `cases` (distribution)

fc |> filter(tu_id == "X") |> autoplot(notif, level = c(80, 95))

# Pull intervals explicitly
fc |> hilo(level = 95) |> unpack_hilo("95%")
```

`forecast()` returns a **distribution** (`distributional` package), not just a
mean. `.mean` is the point forecast; the `cases` column holds the full
predictive distribution, which is what intervals and CRPS use.

### Forecasting with covariates

If a model uses external regressors, supply their future values via
`new_data`:

```r
future <- new_data(train, 12) |> mutate(temp = forecast_of_temp, holiday = ...)
fit |> forecast(new_data = future)
```

You must forecast (or know) the regressors. A dynamic regression is only as good
as the future covariates (IRON RULE 8). Calendar/Fourier terms are deterministic
and safe; weather or economic drivers are not.

## 7. Evaluate

```r
# Out-of-sample accuracy against the full series
fc |> accuracy(notif)
fc |> accuracy(notif, measures = list(point = point_accuracy_measures,
                                       interval = interval_accuracy_measures,
                                       distr = distribution_accuracy_measures))

# Residual diagnostics
fit |> select(arima) |> gg_tsresiduals()
fit |> augment() |> features(.innov, ljung_box, lag = 24, dof = 0)
```

See `evaluation.md` for cross-validation (`stretch_tsibble`), metric choice
(MASE over MAPE), and distributional scoring.

## 8. Refit / produce final forecasts

Once a model is chosen and evaluated, refit on the **full** series before
forecasting the genuine future:

```r
final_fit <- notif |> model(arima = ARIMA(cases))
final_fc  <- final_fit |> forecast(h = "12 months")
```

## Cheat sheet

| Verb | Package | Returns |
|------|---------|---------|
| `as_tsibble`, `fill_gaps`, `has_gaps` | tsibble | tsibble |
| `gg_season`, `gg_subseries`, `ACF`, `STL`, `features` | feasts | plot / tsibble |
| `model()` | fable | mable (fitted models) |
| `report`, `tidy`, `glance`, `augment`, `components` | fable | summaries |
| `forecast()` | fable | fable (distributions) |
| `accuracy()` | fable | metric table |
| `aggregate_key`, `reconcile` | fabletools | tsibble / mable |
| `stretch_tsibble`, `slide_tsibble` | tsibble | CV folds |
