#!/usr/bin/env Rscript
# rebuild_check.R: rebuild the tiers from a JSON spec and the input table, and compare with the project's tier file.
# Usage: Rscript rebuild_check.R spec.json inputs.csv project_tiers.csv
# spec.json: {"id":"unit","hazards":{"heat":{"cols":["a","b"],"dir":[1,1]}},"vuln":{"cols":["c","d"],"dir":[1,1]},
#             "wH":0.5,"score_col":"R","tier_col":"tier_overall"}
# This is an independent re-implementation (it does not source tiers_core.R).
# A fresh audit agent may read it. It never replaces the agent.
suppressPackageStartupMessages(library(jsonlite))
a <- commandArgs(TRUE); stopifnot(length(a) == 3)
spec <- fromJSON(a[1], simplifyVector = TRUE)
inp <- read.csv(a[2], check.names = FALSE); proj <- read.csv(a[3], check.names = FALSE)
pr <- function(x, d) { n <- sum(!is.na(x)); (rank(d * x, ties.method = "average", na.last = "keep") - 1) / (n - 1) }
H <- lapply(spec$hazards, function(h) rowMeans(sapply(seq_along(h$cols), function(i) pr(inp[[h$cols[i]]], h$dir[i]))))
V <- rowMeans(sapply(seq_along(spec$vuln$cols), function(i) pr(inp[[spec$vuln$cols[i]]], spec$vuln$dir[i])))
R <- rowMeans(sapply(H, function(h) h^spec$wH * V^(1 - spec$wH)))
id <- inp[[spec$id]]; k <- ceiling(sum(!is.na(R)) / 3)
o <- order(-R, id); r <- integer(length(R)); r[o] <- seq_along(o)
tier <- ifelse(r <= k, "High", ifelse(r <= 2 * k, "Moderate", "Low"))
m <- merge(data.frame(id = id, R = R, tier = tier),
           data.frame(id = proj[[spec$id]], R_p = proj[[spec$score_col]], tier_p = as.character(proj[[spec$tier_col]])), by = "id")
sorted <- sort(R, decreasing = TRUE); cuts <- c(k, 2 * k)
tie_at_cut <- sapply(cuts, function(i) i < length(sorted) && isTRUE(all.equal(sorted[i], sorted[i + 1])))
dmax <- max(abs(m$R - m$R_p), na.rm = TRUE)
cat(sprintf("units compared: %d\n", nrow(m)))
cat(sprintf("score: %s (max abs diff %.2e)\n", if (dmax < 1e-6) "MATCH" else "DIFFERENT", dmax))
d <- m[m$tier != m$tier_p, ]
cat(sprintf("tiers: %s (%d differ)\n", if (nrow(d) == 0) "MATCH" else "DIFFERENT", nrow(d)))
if (nrow(d)) print(d)
cat(sprintf("tied scores at the High cut: %s; at the Moderate cut: %s\n", tie_at_cut[1], tie_at_cut[2]))
cat(sprintf("tied R values in total: %d\n", sum(duplicated(round(R, 12)) & !is.na(R))))
if (any(tie_at_cut) || nrow(d)) cat("RULE GAP: if ties sit at a cut, the rule must say how they break.\n")
