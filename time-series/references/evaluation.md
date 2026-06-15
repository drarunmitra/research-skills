# Evaluation: splitting, cross-validation, accuracy, diagnostics

The half of forecasting that decides whether anything you built is trustworthy.
Out-of-sample, always (IRON RULE 3).

## Train/test split (never random)

Hold out the **most recent** block, the test set must be the future relative to
the training set. Test length ≈ the forecast horizon you care about.

```r
train <- notif |> filter(month <= yearmonth("2024 Dec"))
test  <- notif |> filter(month >  yearmonth("2024 Dec"))

fit <- train |> model(ets = ETS(cases), arima = ARIMA(cases), snaive = SNAIVE(cases))
fc  <- fit |> forecast(h = nrow(test) / n_keys(notif))   # or h = "12 months"
fc |> accuracy(notif)                                     # compares to held-out actuals
```

A single split is high-variance, it depends on which window you happened to
hold out. Use it for a quick look; use cross-validation for the real verdict.

## Time-series cross-validation (the real evaluation)

`stretch_tsibble()` builds an expanding-window set of training origins; forecast
h steps from each origin and pool the errors. This is "evaluation on a rolling
forecasting origin".

```r
cv <- notif |>
  stretch_tsibble(.init = 36, .step = 1)        # start with 36 obs, grow by 1

fc <- cv |>
  model(ets = ETS(cases), arima = ARIMA(cases), snaive = SNAIVE(cases)) |>
  forecast(h = 12)

fc |> accuracy(notif)                            # averaged over all origins
# accuracy by horizon (does error grow with h?):
fc |> mutate(h = ...) |> accuracy(notif, by = c("h", ".model"))
```

`slide_tsibble()` gives a fixed (rolling) window instead of expanding. Choose
`.init` long enough to fit the most complex model and capture full seasonal
cycles. CV is the gold standard but costs one fit per origin; for many series or
slow models, subsample origins or use a coarser `.step`.

## Point accuracy measures

`accuracy()` reports ME, RMSE, MAE, MPE, MAPE, MASE, RMSSE, ACF1 by default.

- **MAE / RMSE**: scale-dependent (same units as the data). RMSE penalises large
  errors more; optimising RMSE targets the mean, MAE targets the median. Good
  for comparing models on **one** series.
- **MAPE**: percentage error. Familiar but flawed: undefined/explosive near
  zero (fatal for low counts and any series with zeros), and asymmetric
  (penalises over-forecasts more). Avoid for count/surveillance data.
- **MASE / RMSSE** (preferred for cross-series comparison): error scaled by the
  in-sample one-step naive (seasonal naive for seasonal data). MASE < 1 means
  you beat the naive on average; > 1 means you lost (IRON RULE 4 in a number).
  Scale-free, defined at zero, comparable across series of different magnitudes.

Default recommendation: report **MASE** (or RMSSE) plus one scale-dependent
measure (RMSE or MAE), and always the baseline's value next to the model's.

## Distributional / interval accuracy (IRON RULE 5)

A point forecast hides the uncertainty. When intervals are the deliverable
(most surveillance and planning use cases), score the distribution:

```r
fc |> accuracy(notif, measures = list(
  crps    = CRPS,                       # continuous ranked probability score
  winkler = winkler_score,              # interval score at a given level
  cover   = list(coverage = ...),       # empirical coverage of the nominal level
  pinball = quantile_score
))
fc |> accuracy(notif, measures = interval_accuracy_measures, level = 95)
fc |> accuracy(notif, measures = distribution_accuracy_measures)
```

- **CRPS**: proper scoring rule on the whole predictive distribution; lower is
  better; reduces to MAE for a point mass. The default distributional metric.
- **Winkler score**: penalises a (1-α) interval for width plus a penalty when the
  actual falls outside. Rewards sharp, well-calibrated intervals.
- **Pinball / quantile loss**: for specific quantiles (e.g. a 90th-percentile
  surge planning bound).
- **Coverage**: does a nominal 95% interval actually contain ~95% of actuals?
  Under-coverage means overconfident intervals, common and dangerous.

## Residual (innovation) diagnostics (IRON RULE 6)

Good residuals: uncorrelated, zero-mean, constant variance, ~normal (the last
two for valid intervals). The first two are requirements; the rest improve
interval quality.

```r
fit |> select(arima) |> gg_tsresiduals()        # residual plot + ACF + histogram

# Ljung-Box: H0 = residuals are white noise. Want a LARGE p-value.
fit |> augment() |> features(.innov, ljung_box, lag = 24, dof = ...)
#   set dof = number of estimated AR/MA params; lag ~ 2*m (seasonal) or 10 (non-seasonal)
```

Autocorrelated residuals → the model missed structure (add terms, change orders,
add a covariate); the point forecast may still be ok but the intervals are too
narrow. Non-zero mean → bias; correct it. Changing variance → transform or model
the variance (GARCH/INGARCH).

## Comparing models, honestly

- Compare by **out-of-sample** accuracy (CV-averaged), not in-sample fit.
- AICc/BIC compare models **within the same family and likelihood** only (ARIMA
  vs ARIMA, ETS vs ETS). Never use AICc to choose ETS vs ARIMA vs regression.
- Beware selecting on the test set: if you tune many models against one test
  split, that split becomes training. Keep a final untouched holdout, or nest CV.
- A small accuracy edge is often within noise; prefer the simpler, more stable,
  more interpretable model when differences are marginal. Report uncertainty in
  the comparison (e.g. error distribution across CV origins), not just the mean.

## Practical issues (fpp3 ch. 13)

- **Short series**: limited data → favour simple models (ETS, low-order ARIMA);
  CV with small `.init`; do not fit high-order seasonal models.
- **Long/high-frequency series**: complex seasonality → harmonic regression /
  Prophet / STL; CV is expensive, subsample origins.
- **Outliers & missing**: identify before modelling; STL remainder or
  `tsoutliers()`-style checks; decide replace vs model vs leave; document it.
- **Forecasts within limits**: forecast on a transformed scale (log to keep
  positive; scaled logit to bound between known limits) and back-transform.
- **Aggregated intervals**: the interval for a sum of horizons is not the sum of
  intervals; simulate or use the reconciliation machinery.
