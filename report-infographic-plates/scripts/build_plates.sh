#!/usr/bin/env bash
# build_plates.sh: render every plate from HTML to PNG, run the layout preflight on each, and FAIL if any preflight fails.
# Usage: bash build_plates.sh plates.tsv [plate_name ...]
# plates.tsv (use forward slashes in paths): tab-separated, one plate per line, no header: name<TAB>width<TAB>height<TAB>html_dir<TAB>png_dir
#   example:  plate1_poster	1240	1754	report/infographics/html	report/infographics
# Env: EPIC_DIR = folder holding check.mjs and render.mjs (the epic-infographics plugin's scripts folder). Required.
#      Run from the project root. Needs node, Playwright and Chromium (see epic-infographics).
# Output: one preflight line per plate, then "FAILED: n" or "all plates passed". Exit status 1 if any preflight or render failed.
# Windows line endings (CRLF) in plates.tsv are stripped. The png folder is created if it is missing.
set -u
TSV="${1:?plates.tsv required}"; shift
: "${EPIC_DIR:?set EPIC_DIR to the folder with check.mjs and render.mjs}"
ONLY=("$@"); FAIL=0; FAILED=()
CR=$(printf '\r')
while IFS=$'\t' read -r NAME W H HTML_DIR PNG_DIR; do
  NAME="${NAME//$CR/}"; W="${W//$CR/}"; H="${H//$CR/}"; HTML_DIR="${HTML_DIR//$CR/}"; PNG_DIR="${PNG_DIR//$CR/}"
  [ -z "${NAME:-}" ] && continue
  if [ ${#ONLY[@]} -gt 0 ]; then keep=0; for o in "${ONLY[@]}"; do [ "$o" = "$NAME" ] && keep=1; done; [ $keep -eq 0 ] && continue; fi
  mkdir -p "$PNG_DIR"
  if node "$EPIC_DIR/check.mjs" "$HTML_DIR/$NAME.html" --width "$W" --height "$H"; then
    node "$EPIC_DIR/render.mjs" "$HTML_DIR/$NAME.html" "$PNG_DIR/$NAME.png" --width "$W" --height "$H" || { FAIL=$((FAIL+1)); FAILED+=("$NAME (render)"); }
  else
    FAIL=$((FAIL+1)); FAILED+=("$NAME (preflight)")
  fi
done < "$TSV"
if [ $FAIL -gt 0 ]; then echo "FAILED: $FAIL -> ${FAILED[*]}"; exit 1; fi
echo "all plates passed"
