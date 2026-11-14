# inherit_tiers.R: tiers for sub-areas (for example mandals in districts) that have hazard data of their own
# but share the vulnerability value of their parent. Source tiers_core.R first.
#
# sub: one row per sub-area. Columns: the id, `parent`, and the hazard columns named in spec$hazards.
# parent_V: named numeric vector (names = parent ids) with the PARENT vulnerability score on the 0 to 1 scale,
#           taken from run_all_tiers()$base$V.
# Same rule, one scale across all sub-areas. Every sub-area tier is provisional: sub-areas in one parent differ only by hazard.
inherit_tiers <- function(sub, parent_V, spec, runs = NULL, shared_cell_col = NULL, consistent_at = 0.75) {
  stopifnot("parent" %in% names(sub), all(sub$parent %in% names(parent_V)))
  sub$V_parent <- unname(parent_V[sub$parent])
  spec$vuln <- list(given = "V_parent")
  runs <- if (is.null(runs)) default_runs(spec) else runs
  res <- run_all_tiers(sub, spec, runs, consistent_at)
  res$base$provisional <- TRUE
  if (!is.null(shared_cell_col)) res$base$shares_cell <- sub[[shared_cell_col]]
  cat("Tier counts:\n"); print(table(res$base$tier_overall))
  cat("Provisional flags:", sum(res$base$provisional), "of", nrow(res$base), "\n")
  res
}
