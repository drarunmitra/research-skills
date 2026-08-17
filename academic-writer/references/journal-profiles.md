# Journal profiles

A profile sets **house conventions only**: spelling, units, headings, how
numbers and percentages are set. Nothing else.

The default profile is `generic`. Announce which profile you used, in your
report.

## What a profile never touches

These are profile-independent. No profile can weaken them, and any future
profile added to this file inherits them unchanged.

- The five IRON RULES in `SKILL.md`.
- Claim strength matched to study design (IRON RULE 3).
- The citation-verification protocol. No fabricated references, ever.
- Pattern 26: effect size and 95% confidence interval before the P value.
- Pattern 23: uncited empirical claims get `[CITE NEEDED]`.
- The four Writing Rules: no em dashes, no bold or italic for emphasis in
  running prose.

If a journal's own published papers violate one of these, the rule still wins.
See Part 4 of `ijmr-language.md` for a worked example: IJMR reports bare P
values, and the skill still flags them.

## Choosing a profile

Use `ijmr` when any of these hold:

1. The user says "IJMR", "Indian Journal of Medical Research", or "ICMR style".
2. The manuscript's front matter, target-journal field, or cover letter names
   the journal.
3. The existing text already carries two or more IJMR markers: `per cent` in
   running prose, `Material & Methods`, `yr` as a unit, `Interpretation &
   conclusions`.

Otherwise use `generic`. When a document is mixed, follow the document's
dominant existing convention and say so rather than imposing either profile.

## Comparison

| Convention | `generic` (default) | `ijmr` |
|---|---|---|
| Percentages in running prose | `35%` | `35 per cent` |
| Percentages after a count | `162 (33.5%)` | `162 (33.5%)` |
| `and` in titles and headings | `and` | `&` |
| Years | `35.0 years`, `35.0 yr` if the journal abbreviates | `35.0 yr` |
| Weeks, hours | `weeks`, `hours` | `wk`, `h` in ranges and parentheses; spelled out in narrative |
| Methods heading | `Methods` | `Material & Methods` (singular *Material*) |
| Short-paper merge | `Results` and `Discussion` separate | `Results & Discussion` permitted |
| Structured abstract | `Background`, `Methods`, `Results`, `Conclusions` | `Background & objectives`, `Methods`, `Results`, `Interpretation & conclusions` |
| Spelling | follow the document | British `-ae-/-oe-/-our` with Oxford `-ize` |
| Mean and SD | `35.0 (SD 15.0)` or per journal | `35.01±14.96 yr`, closed up |
| Median | `14.0 (IQR 9.0-18.5)` | `14.0 (9.0-18.5)` |
| Ranges | en dash or hyphen per journal | plain hyphen: `8-52 wk` |
| Sentence-initial numbers | spell out | spell out; rest of series stays numeric |
| Citations | per document: Vancouver, APA or Chicago | Vancouver superscript numerals, by first appearance |
| Prior work in text | named author or named design | named author, place or design; never "studies show" |
| Software and reagents | name plus version | name, version, vendor, city, country |

## `generic`

ICMJE Recommendations plus the EQUATOR guideline matching the design
(STROBE, CONSORT, STARD, PRISMA). Follow the document's own existing spelling
and citation style. Do not impose British or American forms on a consistent
document.

## `ijmr`

Full rules, each with the published excerpt that warrants it, in
`references/ijmr-language.md`. Read that file before applying this profile.

Grounded in 14 open-access IJMR articles published before 2019, read in full
text from PubMed Central. The corpus and its identifiers are listed at the top
of `ijmr-language.md`.

Note on scope: IJMR moved publisher in 2023 and its current instructions to
authors differ. This profile describes the pre-2019 house style, which is what
the corpus attests. Say so if a user is submitting today.

## Adding a profile

One row per convention in the table above, one section of worked excerpts in a
companion reference file, and a corpus of real published articles behind it.
A profile without excerpts is an assertion, and this skill does not ship
assertions.
