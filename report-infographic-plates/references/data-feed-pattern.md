# Data feed pattern

One script reads the files the pipeline wrote and writes one JSON file. The generator reads only that JSON. No result is typed by hand.

Steps (R shown; any language works):

1. Read the outputs: the tier or estimate tables (CSV), the numbers file (`numbers.csv`), and any spatial file for maps.
2. Pull headline values from the numbers file with a strict helper. It stops if the key is missing or appears twice:

```r
tok <- function(key, i = 1) {
  v <- num$value[num$key == key]; stopifnot(length(v) == 1)
  as.numeric(gsub(",", "", regmatches(v, gregexpr("[0-9]+(,[0-9]{3})*(\\.[0-9]+)?", v))[[1]][i]))
}
```

3. Maps: simplify geometry once, project to a fixed SVG viewBox (for example width 1000), and write each unit as an SVG path string with its class (tier, phase) in the JSON. The plate then draws paths and never touches coordinates.

```r
bb <- st_bbox(units); k <- cos(mean(c(bb["ymin"], bb["ymax"])) * pi / 180)
W <- 1000; sx <- W / ((bb["xmax"] - bb["xmin"]) * k); H <- round((bb["ymax"] - bb["ymin"]) * sx)
proj <- function(x, y) cbind(round((x - bb["xmin"]) * k * sx, 1), round((bb["ymax"] - y) * sx, 1))
```

4. Group values the plates need: per-area counts for the sheets, per-group sums for bars, lists of names for labels.
5. Write one file with `jsonlite::write_json(list(...), "data.json", auto_unbox = TRUE, digits = NA)`.
6. At the end, print the key counts (for example "High districts 11, consistent mandals 165") so a person can compare them with the report at a glance.
7. Join by name? Print the unmatched names. A wrong spelling alias once dropped a whole area silently.
8. Compare parsed row counts with the source file's own totals. A summary sheet of 33 district rows was once counted as 33 institutions.
9. A column that is a total in one file and a part in another (same name, different rule) must be renamed or documented before use.

Keep the data script free of design choices. Colours, fonts and layout live in the generator.
