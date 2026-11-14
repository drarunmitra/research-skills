#!/usr/bin/env Rscript
# check_plate_numbers.R: every number token on a plate must appear in numbers.csv (or in a short, explicit allow list).
# Usage: Rscript check_plate_numbers.R numbers.csv plate_text_dir [allow_file]
#   numbers.csv: columns key, what, value, source (see the numbers-audit skill)
#   plate_text_dir: output of plate_text.py
#   allow_file (optional): one token per line, with a comment after # saying why (dates, named standards)
#   env ALLOW_EXTRA="15,20,25": extra tokens for ONE run (for example axis ticks). Do not widen the pattern.
# Prints "0 unverified" (exit 0) or a table of file, line, tokens and text (exit 1).
# Strongest on multi-digit and decimal tokens. A single digit can pass by accident, so keep the fresh-agent audit.
a <- commandArgs(TRUE); stopifnot(length(a) >= 2)
num <- read.csv(a[1], stringsAsFactors = FALSE)
tok_re <- "[0-9]+(,[0-9]{3})*(\\.[0-9]+)?"
toks <- function(x) { t <- unlist(regmatches(x, gregexpr(tok_re, x))); unique(c(t, gsub(",", "", t))) }
pool <- toks(paste(num$value, collapse = "  "))
allow <- character()
if (length(a) >= 3 && file.exists(a[3])) { l <- sub("#.*$", "", readLines(a[3])); allow <- trimws(l[nzchar(trimws(l))]) }
allow <- c(allow, setdiff(strsplit(Sys.getenv("ALLOW_EXTRA"), ",")[[1]], ""))
miss <- list()
for (f in list.files(a[2], pattern = "\\.txt$", full.names = TRUE)) {
  lines <- readLines(f, warn = FALSE, encoding = "UTF-8")
  for (i in seq_along(lines)) {
    t <- setdiff(toks(lines[i]), c(pool, allow))
    if (length(t)) miss[[length(miss) + 1]] <- data.frame(file = basename(f), line = i, tokens = paste(t, collapse = " "), text = substr(lines[i], 1, 100))
  }
}
if (length(miss)) { m <- do.call(rbind, miss); cat("UNVERIFIED NUMBERS:", nrow(m), "lines\n"); print(m, row.names = FALSE, right = FALSE); quit(status = 1) }
cat("0 unverified\n")
