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

`Humanize` (default) · `Tighten` · `Claim-check` · `Citation-check` · `Style-convert`. See `SKILL.md` for the full pattern catalogue (28 patterns / 5 categories), IRON RULES, voice calibration, and the citation-verification protocol.

## Attribution

Structure adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT). Mode and citation-verification ideas from [Imbad0202/academic-research-skills](https://github.com/imbad0202/academic-research-skills) (CC-BY-NC 4.0). Pattern basis: *Wikipedia: Signs of AI writing*; academic-integrity layer per EQUATOR (STROBE/CONSORT/PRISMA) and ICMJE. Original content.
