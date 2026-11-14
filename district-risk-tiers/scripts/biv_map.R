# biv_map.R: bivariate choropleth (3 x 3 classes) for two tier columns.
# Needs sf, ggplot2, dplyr, patchwork. Refuses a "hazard" label on risk columns
# (a real mistake in the project this came from: risk tiers were captioned as hazard).
suppressPackageStartupMessages({library(ggplot2); library(sf); library(dplyr)})

# Multiply-blend two 3-colour ramps. Cell names run "Low-Low" ... "High-High" (x first, then y).
make_blend <- function(xr, yr) {
  lv <- c("Low", "Moderate", "High"); out <- character(); nm <- character()
  for (j in 1:3) for (i in 1:3) {
    v <- col2rgb(xr[i]) / 255 * col2rgb(yr[j]) / 255
    out <- c(out, rgb(v[1], v[2], v[3])); nm <- c(nm, paste(lv[i], lv[j], sep = "-"))
  }
  setNames(out, nm)
}

# One colour family per quantity, so two panels are not read as the same thing.
BIV_PAL <- list(
  hazard = c("Low-Low" = "#E8E8E8", "Moderate-Low" = "#E4ACAC", "High-Low" = "#C85A5A",
             "Low-Moderate" = "#B0D5DF", "Moderate-Moderate" = "#AD9EA5", "High-Moderate" = "#985356",
             "Low-High" = "#64ACBE", "Moderate-High" = "#627F8C", "High-High" = "#574249"),   # pink and blue
  risk = make_blend(c("#F4F4F4", "#F7CE78", "#EE8A1C"), c("#F4F4F4", "#B4E0D4", "#4FB3A3")),   # amber and teal
  vulnerability = make_blend(c("#F4F4F4", "#C9B8DC", "#6A51A3"), c("#F4F4F4", "#F4B6C2", "#E0457B")))   # purple and magenta

# sf: polygons with a column named by `key`. tab: data frame with `key`, xcol and ycol (values Low, Moderate, High).
# kind "hazard": the two columns must come from hazard scores (H_*). Columns named tier_* or R_* are risk, so the call stops.
biv_map <- function(sf, tab, xcol, ycol, title, kind = c("hazard", "risk", "vulnerability"),
                    xlab = xcol, ylab = ycol, path = NULL, key = "key") {
  kind <- match.arg(kind)
  if (kind == "hazard" && any(grepl("^(tier_|R_)", c(xcol, ycol))))
    stop("Label says hazard but the columns look like risk tiers (tier_* or R_*). Build hazard tiers from H_* scores, or use kind = 'risk'.")
  lv <- c("Low", "Moderate", "High")
  tab$biv <- paste(factor(tab[[xcol]], lv), factor(tab[[ycol]], lv), sep = "-")
  d <- left_join(sf, tab[, c(key, "biv")], by = key); pal <- BIV_PAL[[kind]]
  g <- expand.grid(x = factor(lv, lv), y = factor(lv, lv)); g$biv <- paste(g$x, g$y, sep = "-")
  g$n <- as.integer(table(tab$biv)[g$biv]); g$n[is.na(g$n)] <- 0L
  cat("Class counts (x-y):\n"); print(setNames(g$n, g$biv))
  leg <- ggplot(g, aes(x, y, fill = biv)) + geom_tile(colour = "white", linewidth = 0.8) + geom_text(aes(label = n), size = 2.4) +
    scale_fill_manual(values = pal, guide = "none") + coord_fixed() + labs(x = paste0(xlab, " →"), y = paste0(ylab, " →")) +
    theme_minimal(base_size = 7.5) + theme(panel.grid = element_blank())
  p <- ggplot(d) + geom_sf(aes(fill = biv), colour = "white", linewidth = 0.1) +
    scale_fill_manual(values = pal, guide = "none") + labs(title = title) + theme_void(base_size = 9) +
    theme(plot.title = element_text(face = "bold")) + patchwork::inset_element(leg, 0.7, 0, 1, 0.28)
  if (!is.null(path)) ggsave(path, p, width = 6.5, height = 6.4, dpi = 300, bg = "white")
  p
}
