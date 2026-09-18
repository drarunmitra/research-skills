#!/usr/bin/env bash
# Ban-list check for the playbook-instructions house style.
# Usage: check.sh file1.qmd file2.md ...
# Exit 0 = clean. Exit 1 = at least one banned pattern found. Exit 2 = usage.
#
# Prose in this repo is hard-wrapped at ~80 columns, so a banned phrase can
# fall across a single line break (e.g. "you have\nwon." in
# prelude/data.qmd). Each line is checked alone, and each adjacent pair of
# lines is also checked joined together - but a joined-pair hit is only
# reported when NEITHER line in the pair already matched on its own.
# Without that guard, a phrase sitting entirely on one line would be
# reported again for the pair on each side of it, tripling one real
# violation. This keeps one real violation to one reported line.
#
# Known residual gap: this only reunites a phrase split across ONE line
# break (two physical lines). A phrase split across three or more physical
# lines is not detected. No banned phrase currently in this repo is wrapped
# that far, but exit 0 from this script means "no known-shaped hit found",
# not an absolute guarantee of clean prose - a human skim of new text is
# still worthwhile.
#
# Matching uses grep -E throughout (not awk regex) because the patterns
# below rely on \b word-boundary matching, which GNU awk's regex engine
# does not implement the same way GNU grep does. To stay fast on a slow
# process-spawn platform (Windows/Git Bash), each file gets at most two
# grep calls per pattern - one for the single-line pass, one for every
# adjacent-line pair at once - rather than one grep call per line.
#
# style-exempt marker: a line reading (or ending with)
#   <!-- style-exempt: <reason> -->
# exempts itself, or the line immediately after it, from ALL FOUR
# categories below. Use it for example academic prose (an abstract, a
# Methods template, a demo manuscript) that participants copy or read as a
# model of correct academic writing, where the digit rule and the other
# categories should not apply, rather than for anything a reader is
# instructed to do. The reason after the colon is mandatory and must be
# non-empty; a marker with no reason exempts nothing. Every suppressed hit
# is printed to stderr as "SUPPRESSED file:line: <reason>: <matched line
# text>" - the matched text is included so an auditor can see what was
# suppressed without opening the file - so exemptions
# stay visible rather than silently disappearing, and a suppressed hit
# never affects the exit code.
#
# Fence extension: an HTML comment placed INSIDE a fenced code block is
# not actually invisible - Pandoc renders it as literal escaped text
# (confirmed empirically: it shows up in the built HTML with a comment
# CSS class, but as real visible text). So a marker cannot go on the line
# immediately before a target that is itself deep inside a multi-line
# fence without becoming visible. To keep the marker genuinely invisible
# in that case, place it on the line immediately before the fence OPENS;
# the exemption then extends through every line of that fenced block, up
# to and including its matching closing fence. This still only chains off
# one same-line-or-immediately-preceding marker per exemption, it just
# recognises that "the next line" can itself open a multi-line block.
#
# RULING R25: {webr} fence contents are out of scope, not exempt. SKILL.md's
# own never-touch list forbids editing anything inside a ```{webr} fence
# (the code, and - in the primers - the #| check: true grader messages,
# which are ordinary R string literals inside that fence). A checker that
# flagged those strings would be demanding an edit its own rules forbid, so
# this script never scans inside a {webr} fence at all: every line from the
# opening ```{webr} delimiter through its matching closing fence, inclusive,
# is skipped before any pattern is matched. This is NOT the style-exempt
# mechanism - nothing is suppressed or printed to stderr for these lines,
# because there was never a hit to suppress; the content simply never enters
# scanning. See webr_blank_file, below.
set -uo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: check.sh <file> [file...]" >&2
  exit 2
fi

BANNED_PHRASES='make tea|you have won|on Tuesdays|the room that actually turns up|lies to you|when the words have referents|break them on purpose|and that is the point'
BANNED_WORDS='\bsimply\b|\bjust\b|\bobviously\b|\bof course\b|\bmerely\b|\bclearly\b'
BANNED_IDIOM='\bhit \b|\bgrab \b|fire up|spin up'
SPELLED_COUNTS='\b(three|four|five|six|seven|eight|nine|ten|eleven|twelve|sixteen|twenty|forty) (packages|files|datasets|rows|students|questions|minutes|sections|steps|panes|pane|boxes|box|windows|window|primers|primer|colleges|arms|stations|quizzes|attempts|papers)\b'

# EXEMPT_REASON["file:lineno"] -> reason text, for every line exempted by a
# style-exempt marker (populated once per file by build_exempt_map, below).
declare -A EXEMPT_REASON

# BLANKED_FILE["file"] -> path of a scratch copy of "file" with every
# {webr}-fenced line replaced by an empty line (populated once per file by
# webr_blank_file, below, and cleaned up on exit by cleanup_blanked). All
# pattern matching reads from this scratch copy instead of the real file,
# so {webr} fence contents can never match - see RULING R25 above. Line
# numbers are preserved exactly (blank lines occupy the same slot as the
# fence lines they stand in for), so reported line numbers still point at
# the right line in the real file.
declare -A BLANKED_FILE

cleanup_blanked() {
  local f
  for f in "${!BLANKED_FILE[@]}"; do
    rm -f "${BLANKED_FILE[$f]}" 2>/dev/null
  done
}
trap cleanup_blanked EXIT

# webr_blank_file FILE
# Prints FILE with every line that is part of a ```{webr} ... ``` fence -
# the opening delimiter (which may carry attributes after "{webr"), every
# line of its contents, and its matching closing delimiter - replaced by an
# empty line. Everything else is printed unchanged. The closing delimiter is
# the next line that is nothing but backticks at least as long as the
# opening one, matching CommonMark fence-closing rules. If the file ends
# before a closing fence appears, every remaining line is treated as still
# inside the fence (blanked) rather than left unclosed, so the scan cannot
# hang or error on a truncated file.
webr_blank_file() {
  local f="$1"
  awk '
    {
      raw = $0
      trimmed = raw
      gsub(/\r$/, "", trimmed)
      gsub(/^[ \t]+/, "", trimmed)
      gsub(/[ \t]+$/, "", trimmed)
      if (!inwebr) {
        if (trimmed ~ /^```+\{webr/) {
          bt = trimmed
          sub(/[^`].*/, "", bt)
          flen = length(bt)
          inwebr = 1
          print ""
          next
        }
        print raw
        next
      }
      if (trimmed ~ /^```+$/ && length(trimmed) >= flen) {
        inwebr = 0
      }
      print ""
    }
  ' "$f"
}

# build_exempt_map FILE
# Scans FILE for style-exempt markers and records, for each one found with
# a non-empty reason, every line it exempts: its own line, the line right
# after it (same-line marker and marker-on-the-line-before are both
# supported shapes) - and, if that following line opens a fenced code
# block, every line through the block's matching closing fence too (see
# the "Fence extension" note above).
build_exempt_map() {
  local f="$1"
  local lineno reason
  while IFS=$'\t' read -r lineno reason; do
    [ -z "$lineno" ] && continue
    EXEMPT_REASON["$f:$lineno"]="$reason"
  done < <(awk '
    { gsub(/\r$/, ""); lines[NR] = $0 }
    END {
      for (i = 1; i <= NR; i++) {
        line = lines[i]
        if (!match(line, /<!--[ \t]*style-exempt:[ \t]*[^ \t].*-->/)) continue
        reason = line
        sub(/.*<!--[ \t]*style-exempt:[ \t]*/, "", reason)
        sub(/[ \t]*-->.*/, "", reason)
        if (reason == "") continue
        print i "\t" reason
        nxt = i + 1
        if (nxt > NR) continue
        print nxt "\t" reason
        trimmed = lines[nxt]
        gsub(/^[ \t]+/, "", trimmed)
        gsub(/[ \t]+$/, "", trimmed)
        if (!match(trimmed, /^(```+|~~~+)/)) continue
        fence = substr(trimmed, RSTART, RLENGTH)
        fchar = substr(fence, 1, 1)
        flen = length(fence)
        close_idx = 0
        for (j = nxt + 1; j <= NR; j++) {
          ctrim = lines[j]
          gsub(/^[ \t]+/, "", ctrim)
          gsub(/[ \t]+$/, "", ctrim)
          if (fchar == "`") {
            if (ctrim ~ /^```+$/ && length(ctrim) >= flen) { close_idx = j; break }
          } else {
            if (ctrim ~ /^~~~+$/ && length(ctrim) >= flen) { close_idx = j; break }
          }
        }
        if (close_idx > 0) {
          for (j = nxt; j <= close_idx; j++) print j "\t" reason
        }
      }
    }
  ' "$f")
}

# match_pattern_in_file PATTERN FILE
# Prints "FILE:LINE:text" for every line-level or wrap-spanning hit, each
# real violation reported exactly once. A hit on a line exempted via
# EXEMPT_REASON is not printed to stdout (so it cannot affect the exit
# code) - instead "SUPPRESSED FILE:LINE: reason" goes to stderr. Reads from
# BLANKED_FILE[FILE], not FILE itself, so {webr} fence contents (see
# RULING R25 above) never reach either pass and never appear as a hit or
# as a SUPPRESSED line - they are out of scope, not exempted.
match_pattern_in_file() {
  local pattern="$1" f="$2" bf="${BLANKED_FILE[$2]}"
  local -A matched_lines=()
  local line lineno content startline joined nextline reason

  # Pass 1: one grep call for every line that matches on its own.
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    lineno="${line%%:*}"
    content="${line#*:}"
    matched_lines["$lineno"]=1
    reason="${EXEMPT_REASON["$f:$lineno"]:-}"
    if [ -n "$reason" ]; then
      printf 'SUPPRESSED %s:%s: %s: %s\n' "$f" "$lineno" "$reason" "$content" >&2
    else
      printf '%s:%s:%s\n' "$f" "$lineno" "$content"
    fi
  done < <(grep -niE "$pattern" "$bf" 2>/dev/null)

  # Pass 2: one awk call builds every adjacent-line pair (CRLF-stripped,
  # so a phrase is not broken by a stray \r left at the end of a line on a
  # Windows checkout), then one grep call finds pairs that match only when
  # joined. A pair is reported only if neither of its two lines already
  # matched in Pass 1.
  while IFS=$'\x01' read -r startline joined; do
    [ -z "${startline:-}" ] && continue
    nextline=$((startline + 1))
    if [ -z "${matched_lines[$startline]:-}" ] && [ -z "${matched_lines[$nextline]:-}" ]; then
      reason="${EXEMPT_REASON["$f:$startline"]:-}"
      [ -z "$reason" ] && reason="${EXEMPT_REASON["$f:$nextline"]:-}"
      if [ -n "$reason" ]; then
        printf 'SUPPRESSED %s:%s: %s: %s\n' "$f" "$startline" "$reason" "$joined" >&2
      else
        printf '%s:%s:%s\n' "$f" "$startline" "$joined"
      fi
    fi
  done < <(
    awk '{ gsub(/\r$/, ""); lines[NR] = $0 }
         END { for (i = 1; i < NR; i++) print i "\x01" lines[i] " " lines[i + 1] }' \
      "$bf" | grep -iE "$pattern" 2>/dev/null
  )
}

status=0

for f in "$@"; do
  build_exempt_map "$f"
  BLANKED_FILE["$f"]=$(mktemp)
  webr_blank_file "$f" > "${BLANKED_FILE[$f]}"
done

for pattern_name in BANNED_PHRASES BANNED_WORDS BANNED_IDIOM SPELLED_COUNTS; do
  pattern="${!pattern_name}"
  found=0
  for f in "$@"; do
    hits=$(match_pattern_in_file "$pattern" "$f")
    if [ -n "$hits" ]; then
      printf '%s\n' "$hits"
      found=1
    fi
  done
  if [ "$found" -eq 1 ]; then
    echo "^^ $pattern_name violation" >&2
    status=1
  fi
done

exit "$status"
