# Plate checklist and red flags

## Before you render
- Every number comes from `data.json`. Search the generator for digits in strings.
- Each plate has one sentence: what the reader should remember.
- Each total names its scope (what it includes, what it leaves out).
- Each drawing that is not data says "illustrative".
- Each proposal says "proposal". Each unverified item says so.

## After you render
- The build printed "all plates passed" (a non-zero exit means a plate failed).
- `plate_text.py` then `check_plate_numbers.R` printed "0 unverified".
- You made a contact sheet of the whole set after this build and looked at it.
- You looked at each new or changed plate at full size, and re-looked at the unchanged plates.
- The PDF page numbers run in order.
- A fresh agent audited the plates and every must-fix is closed.

## Red flags from the project this skill came from

| What went wrong | Fix |
|---|---|
| A source line said "all prices" but one source gave 83% of the money | Check each rate's source before you write "all". |
| A total on a plate had no scope, and the report defined the same word with more in it | Name the scope on the plate. |
| The plate title total differed from the sum of its bars (contingency was in a separate box) | Say "subtotal", or show the remainder. |
| A caption said all places were labelled but five were not | Count labels against the data. |
| A dashed line from the last measured point to a text box read as a forecast, on a plate headed "not a forecast" | Use a text callout, not a line. |
| A bar or date had no source in the report text | Source it or mark it as assumed. |
| An unverified item appeared as fact | Show "to be confirmed". |
| One footnote covered two weightings | One note per weighting. |
| The same column name meant a total in one file and a part in another | Rename or document it. |
| A credit appeared with no map | Match credits to content. |
| Plates were first built on a textured, off-white page | White page, grain off. |
| A summary sheet of 33 rows was counted as 33 records | Compare parsed counts with the file's own total. |
| A name alias was wrong, so a unit vanished from a join | Print unmatched names. |
| Single-digit numbers passed the number check by accident | The checker is strong on multi-digit numbers. Keep the fresh-agent audit. |
| The build script printed "PREFLIGHT ERRORS" and carried on, with exit status 0 | Use `build_plates.sh`, which counts failures and exits 1. |
