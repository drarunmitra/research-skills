#!/usr/bin/env python3
"""Check a policy draft (Markdown) against the health-policy-brief rules.

Usage:
    python -I check_text.py DRAFT.md [--numbers numbers.csv] [--allow "2027,2030"]
                                     [--acronyms "PDF,CSV"] [--cabinet]

FAIL (exit 1): sentence over 28 words, em dash, bold in prose, bare
"there is uncertainty", number not in numbers.csv (when given).
FLAG (reported, no exit code): sentence over 25 words, banned causal or
filler wording, acronym used before it is defined, [TO VERIFY] count,
readability. Readability is a flag, not a pass mark.
"""
import argparse
import csv
import re
import sys

FLAG_LONG, FAIL_LONG = 25, 28

CAUSAL = re.compile(
    r"\b(causes?|caused by|leads? to|led to|drives?|driven by|proves?|proven|"
    r"due to|impact of|effect of|no-regret|studies show|research shows|"
    r"it is well known|experts agree)\b", re.I)
BARE_UNCERT = re.compile(
    r"\bthere is (some |considerable |significant |a degree of )?uncertainty\b", re.I)
FILLER = re.compile(
    r"\b(crucial|pivotal|landscape|multifaceted|robust|transformative|"
    r"it is important to note|it is imperative|delve|tapestry|holistic)\b", re.I)
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?%?")
UNIT_AFTER = re.compile(
    r"^\s*(%|crore|lakh|districts?|mandals?|villages?|women|children|deaths?|"
    r"facilities|hostels?|PHCs?|days?|months?|years?)\b", re.I)
MONTH = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*"
DATE_AFTER = re.compile(r"^\s*" + MONTH, re.I)
DATE_BEFORE = re.compile(MONTH + r"\.?\s*$", re.I)
ACRO = re.compile(r"\b[A-Z][A-Z0-9]{1,7}(?:&[A-Z]{1,4})?\b")
DEFAULT_ACRO_OK = {"A4", "PDF", "CSV", "AI", "OK", "US", "UK", "TO", "VERIFY"}


def strip_front_matter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:]
    return text


def prose_lines(text):
    """Yield (lineno, line) for prose lines: not code, tables, headings, rules."""
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not s:
            continue
        if s.startswith("|") or s.startswith("#") or re.fullmatch(r"[-*_=\s]+", s):
            continue
        yield i, line


def clean(line):
    line = re.sub(r"`[^`]*`", " ", line)
    line = re.sub(r"@[A-Za-z][A-Za-z0-9_:.-]*", " ", line)          # citation keys, cross-reference labels
    line = re.sub(r"#v\([^)]*\)", " ", line)                        # layout spacing in raw typst
    line = re.sub(r"https?://\S+", " ", line)
    line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
    line = re.sub(r"^\s*(\d+[.)]|[-*+])\s+", "", line)
    return line


def sentences(text):
    out = []
    for i, line in prose_lines(text):
        c = clean(line)
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(\[])", c):
            part = part.strip()
            if part:
                out.append((i, part))
    return out


def words(s):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'%.,/-]*", s)


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and n > 1:
        n -= 1
    return max(n, 1)


def norm_num(tok):
    return tok.replace(",", "").rstrip("%")


def load_numbers(path):
    vals = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            v = (row.get("value") or "").strip()
            for t in NUM.findall(v):
                vals.add(norm_num(t))
            if v:
                vals.add(norm_num(v))
    return vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--numbers")
    ap.add_argument("--allow", default="")
    ap.add_argument("--acronyms", default="")
    ap.add_argument("--cabinet", action="store_true",
                    help="Cabinet note: bullets are not allowed")
    a = ap.parse_args()

    with open(a.draft, encoding="utf-8") as f:
        raw = f.read()
    text = strip_front_matter(raw)

    fails, flags = [], []

    # sentence length
    sents = sentences(text)
    wc = []
    for ln, s in sents:
        n = len(words(s))
        wc.append(n)
        if n > FAIL_LONG:
            fails.append(f"line {ln}: sentence of {n} words (over {FAIL_LONG}): {s[:70]}...")
        elif n > FLAG_LONG:
            flags.append(f"line {ln}: sentence of {n} words (over {FLAG_LONG}): {s[:70]}...")

    # per-line checks
    for ln, line in prose_lines(text):
        c = clean(line)
        if "—" in line or " -- " in line:
            fails.append(f"line {ln}: em dash")
        if re.search(r"\*\*[A-Za-z0-9][^*]*\*\*|__[A-Za-z0-9][^_]*__", line):
            fails.append(f"line {ln}: bold in prose")
        if BARE_UNCERT.search(c):
            fails.append(f"line {ln}: 'there is uncertainty' with no number")
        for m in CAUSAL.finditer(c):
            flags.append(f"line {ln}: check wording '{m.group(0)}' against the causal verb table")
        for m in FILLER.finditer(c):
            flags.append(f"line {ln}: filler word '{m.group(0)}'")
        if a.cabinet and re.match(r"\s*[-*+]\s+", line):
            flags.append(f"line {ln}: bullet in a Cabinet note (use numbered paragraphs)")

    # acronyms: first use must be defined
    ok = set(DEFAULT_ACRO_OK) | {x.strip() for x in a.acronyms.split(",") if x.strip()}
    seen = {}
    for ln, line in prose_lines(text):
        c = clean(line)
        for m in ACRO.finditer(c):
            t = m.group(0)
            if t in ok or t in seen or re.fullmatch(r"[A-Z]\d+", t):
                continue
            before = c[:m.start()].rstrip()
            after = c[m.end():].lstrip()
            defined = (before.endswith("(") and after.startswith(")")) or after.startswith("(")
            seen[t] = (ln, defined)
    for t, (ln, defined) in seen.items():
        if not defined:
            flags.append(f"line {ln}: acronym {t} used before it is defined")

    # numbers
    unver = []
    if a.numbers:
        known = load_numbers(a.numbers)
        allow = {norm_num(x.strip()) for x in a.allow.split(",") if x.strip()}
        for ln, line in prose_lines(text):
            c = clean(line)
            for m in NUM.finditer(c):
                tok = norm_num(m.group(0))
                if tok in known or tok in allow:
                    continue
                if re.fullmatch(r"(19|20)\d\d", tok):
                    continue
                if DATE_AFTER.match(c[m.end():]) or DATE_BEFORE.search(c[:m.start()]):
                    continue
                single = len(tok.replace(".", "")) == 1
                if single and not UNIT_AFTER.match(c[m.end():] if not m.group(0).endswith("%") else "%"):
                    continue
                unver.append((ln, m.group(0)))
        # tables too: numbers in tables must also trace
        for i, line in enumerate(text.splitlines(), 1):
            if line.strip().startswith("|") and not re.fullmatch(r"[|\-:\s]+", line.strip()):
                for m in NUM.finditer(clean(line)):
                    tok = norm_num(m.group(0))
                    if tok in known or tok in allow or re.fullmatch(r"(19|20)\d\d", tok):
                        continue
                    if len(tok.replace(".", "")) == 1:
                        continue
                    cl = clean(line)
                    if DATE_AFTER.match(cl[m.end():]) or DATE_BEFORE.search(cl[:m.start()]):
                        continue
                    unver.append((i, m.group(0)))
        for ln, tok in sorted(set(unver)):
            fails.append(f"line {ln}: number {tok} not in {a.numbers}")

    tv = len(re.findall(r"\[TO VERIFY\]", raw))
    if tv:
        flags.append(f"{tv} [TO VERIFY] marks left. Clear them or list them as open items.")

    # readability (flag only)
    allw = [w for _, s in sents for w in words(s)]
    if sents and allw:
        avg = sum(wc) / len(wc)
        syl = sum(syllables(w) for w in allw)
        flesch = 206.835 - 1.015 * avg - 84.6 * (syl / len(allw))
        flags.append(f"readability: {len(sents)} sentences, average {avg:.1f} words, "
                     f"Flesch about {flesch:.0f} (flag only; target near 15 words, Flesch near 60)")

    print(f"FAIL: {len(fails)}")
    for x in fails:
        print("  " + x)
    print(f"FLAG: {len(flags)}")
    for x in flags:
        print("  " + x)
    if not a.numbers:
        print("NOTE: no --numbers file given, so numbers were not traced.")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
