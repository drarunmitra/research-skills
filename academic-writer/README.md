# Academic Writer

A global Claude Code skill that **humanizes and tightens academic writing**: it removes the surface signs of AI generation (significance inflation, filler, reflexive hedging, em-dash and rule-of-three overuse, formulaic signposting) *and* the deeper academic faults (overclaiming, uncited assertions, p-value-only reporting), without altering findings, numbers, or the author's voice.

Built for manuscripts, theses, grants, abstracts, and reports in Quarto / R Markdown / LaTeX / Markdown.

## Install

It lives in the global skills directory, so it is available in every project:

```
~/.claude/skills/academic-writer/SKILL.md
```

(On this machine: `C:\Users\Arun\.claude\skills\academic-writer\`.) Restart the Claude Code session if it doesn't yet appear in the skill list.

## Use

Invoke explicitly with `/academic-writer`, or just ask in context:

- "Humanize this discussion section."
- "Remove the AI bloat from this draft."
- "Did I overclaim in this paragraph?"
- "Check my references."
- "Convert these citations to Vancouver."

## Modes

`Humanize` (default) · `Tighten` · `Claim-check` · `Citation-check` · `Style-convert`. See `SKILL.md` for the full pattern catalogue (28 patterns / 5 categories), IRON RULES, voice calibration, journal profiles, and the citation-verification protocol.

## Journal profiles

A profile sets house conventions only: spelling, units, headings, how numbers and percentages are set. The default is `generic` (ICMJE plus the matching EQUATOR guideline). Say "for IJMR" to switch to the `ijmr` profile.

A profile never touches the IRON RULES, claim-strength matching, the citation protocol, or the requirement for effect size and 95% CI ahead of the P value. Where a journal's own published papers violate one of those, the rule still wins.

- `references/journal-profiles.md`: the comparison table and the switch rule.
- `references/ijmr-language.md`: the IJMR rules, each with the published excerpt that warrants it.

## Grounding

The `ijmr` profile and the `Evidence:` warrants on the pattern catalogue are built from a corpus of **14 open-access *Indian Journal of Medical Research* articles published before 2019**, read in full text from PubMed Central. The set spans original articles, brief communications, reviews, editorials, clinical images and correspondence. Every article is listed with its DOI or PMID at the top of `references/ijmr-language.md`.

Two things this buys:

1. **Checkable rules.** Each language rule prints the sentence that justifies it, so a user can verify it against the published paper rather than take the skill's word.
2. **Descriptive separated from prescriptive.** The corpus reports bare P values with no confidence intervals, folds limitations into subordinate clauses, and omits participant flow. Part 4 of `references/ijmr-language.md` marks these as defects and the skill keeps flagging them. Grounding the register does not mean importing the reporting faults.

There is also a matching Claude Code output style at `~/.claude/output-styles/IJMR.md`, for drafting directly in the register.

## Attribution

Structure adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT). Mode and citation-verification ideas from [Imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) (CC-BY-NC 4.0). Pattern basis: *Wikipedia: Signs of AI writing*; academic-integrity layer per EQUATOR (STROBE/CONSORT/PRISMA) and ICMJE. Original content.
