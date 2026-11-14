# tiers_core.R: rank units (districts, blocks, mandals) into High / Moderate / Low tiers.
# Source this file. Needs dplyr, purrr, tibble. No project data inside.
#
# Spec (a list you write from the rule file, before any result is seen):
#   spec <- list(
#     id = "unit",                                   # name of the id column in `inp`
#     hazards = list(heat = list(cols = c("hot_days", "tmax"), dir = c(1, 1)),
#                    rain = list(cols = c("dry_dep", "mean_rain"), dir = c(-1, -1))),
#     vuln = list(cols = c("stunt", "wast", "st_share"), dir = c(1, 1, 1)),   # or list(given = "V") for a ready value
#     wH = 0.5)                                      # risk = H^wH * V^(1 - wH)
# dir = 1 means a higher value is worse. dir = -1 means a lower value is worse.
suppressPackageStartupMessages({library(dplyr); library(purrr); library(tibble)})

# percentile rank in [0, 1]; NA stays NA
pr <- function(x, dir = 1) {
  n <- sum(!is.na(x)); if (n < 2) return(rep(NA_real_, length(x)))
  (rank(dir * x, ties.method = "average", na.last = "keep") - 1) / (n - 1)
}

# Tier cut into thirds. Tie rule (state it in the rule file): higher score first, then higher stability, then id in alphabetical order.
tier3 <- function(x, id, stability = NULL) {
  n <- sum(!is.na(x)); k <- ceiling(n / 3)
  stab <- if (is.null(stability)) rep(0, length(x)) else stability
  o <- order(-x, -stab, id, na.last = NA); r <- rep(NA_integer_, length(x)); r[o] <- seq_along(o)
  factor(dplyr::case_when(is.na(x) ~ "Data too thin", r <= k ~ "High", r <= 2 * k ~ "Moderate", TRUE ~ "Low"),
         levels = c("High", "Moderate", "Low", "Data too thin"))
}

score_run <- function(inp, spec) {
  id <- inp[[spec$id]]
  H <- map(spec$hazards, function(h) rowMeans(do.call(cbind, map2(h$cols, h$dir, ~ pr(inp[[.x]], .y)))))
  V <- if (!is.null(spec$vuln$given)) inp[[spec$vuln$given]] else {
    m <- do.call(cbind, map2(spec$vuln$cols, spec$vuln$dir, ~ pr(inp[[.x]], .y)))
    v <- rowMeans(m); v[rowSums(is.na(m)) > 0] <- NA; v   # any missing vulnerability input: "Data too thin"
  }
  Rk <- map(H, ~ .x^spec$wH * V^(1 - spec$wH))
  R <- rowMeans(do.call(cbind, Rk))
  out <- tibble(id = id, V = V, R = R)
  for (k in names(H)) out[[paste0("H_", k)]] <- H[[k]]
  for (k in names(Rk)) out[[paste0("R_", k)]] <- Rk[[k]]
  out$tier_overall <- tier3(R, id)
  for (k in names(Rk)) out[[paste0("tier_", k)]] <- tier3(Rk[[k]], id)
  names(out)[1] <- spec$id
  out
}

# What-if runs: each run is a list of overrides merged into the spec with modifyList().
# default_runs() builds drop-one runs and the two weight runs. Add runs that differ in KIND
# (another data source, another weighting), because drop-one runs alone are a weak test.
default_runs <- function(spec) {
  runs <- list()
  if (length(spec$hazards) > 1) for (k in names(spec$hazards))
    runs[[paste0("drop_hazard_", k)]] <- list(hazards = spec$hazards[setdiff(names(spec$hazards), k)])
  if (is.null(spec$vuln$given) && length(spec$vuln$cols) > 1) for (i in seq_along(spec$vuln$cols))
    runs[[paste0("drop_vuln_", spec$vuln$cols[i])]] <- list(vuln = list(cols = spec$vuln$cols[-i], dir = spec$vuln$dir[-i]))
  runs$hazard_x2 <- list(wH = 2 / 3)
  runs$vuln_x2 <- list(wH = 1 / 3)
  runs
}

# Returns list(base = tiers + stability + label, runs = long table of run tiers).
# Stability = share of runs in which the overall tier equals the base tier.
# Label "consistent" if stability >= consistent_at, else "less certain".
# Stability is a robustness check against the listed runs. It is not a confidence interval.
run_all_tiers <- function(inp, spec, runs = default_runs(spec), consistent_at = 0.75) {
  base <- score_run(inp, spec); idc <- spec$id
  rr <- imap_dfr(runs, function(o, nm) score_run(inp, modifyList(spec, o, keep.null = TRUE)) |> mutate(run = nm))
  stab <- rr |> select(all_of(idc), run, tier_run = tier_overall) |>
    left_join(base |> select(all_of(idc), tier_overall), by = idc) |>
    group_by(across(all_of(idc))) |> summarise(stability = mean(tier_run == tier_overall), n_runs = n(), .groups = "drop")
  base <- base |> left_join(stab, by = idc) |> mutate(label = if_else(stability >= consistent_at, "consistent", "less certain"))
  base$tier_overall <- tier3(base$R, base[[idc]], base$stability)   # final tie break uses stability
  list(base = base, runs = rr)
}

# QC: returns a table of checks. Stop on any FALSE before you use the tiers.
qc_tiers <- function(res, inp, spec) {
  b <- res$base; id <- spec$id; cnt <- table(b$tier_overall)
  third <- ceiling(sum(!is.na(b$R)) / 3)
  tibble(
    check = c("one row per unit", "no duplicate ids", "High tier has ceiling(n/3) units", "stability within 0 and 1",
              "no score with a 'Data too thin' tier", "hazard score rises with its risk (Spearman > 0)"),
    pass = c(nrow(b) == nrow(inp), !anyDuplicated(b[[id]]), unname(cnt["High"]) == third,
             all(b$stability >= 0 & b$stability <= 1),
             all(!(b$tier_overall == "Data too thin" & !is.na(b$R))),
             all(map_dbl(names(spec$hazards), ~ cor(b[[paste0("H_", .x)]], b[[paste0("R_", .x)]], method = "spearman", use = "complete.obs")) > 0)),
    detail = c(nrow(b), "", unname(cnt["High"]), paste(round(range(b$stability), 2), collapse = " to "), "", ""))
}
