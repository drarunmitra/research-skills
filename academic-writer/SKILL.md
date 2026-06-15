---
name: academic-writer
version: 1.3.0
description: |
  Humanizes and tightens academic writing. Detects and removes AI tells
  (significance inflation, filler, reflexive hedging, em-dash and rule-of-three
  overuse, formulaic signposting) from manuscripts, theses, grants, abstracts,
  and reports, while preserving meaning, calibrating every claim to the strength
  of its evidence, and verifying or flagging citations rather than fabricating
  them. Use to de-bloat AI-drafted academic text, fix overclaiming/underclaiming,
  remove "AI voice," check citation integrity, or convert citation styles
  (APA / Vancouver / Chicago). Supports Quarto / R Markdown / LaTeX.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - WebFetch
---

# Academic Writer

Make academic prose read as though a careful researcher wrote it, not a model. This skill removes the surface signs of AI generation **and** the deeper academic faults (overclaiming, uncited assertions, p-value-only reporting) that betray machine drafting, without changing the author's findings or stripping their voice.

It is a *revision* skill, not a *drafting* skill. Give it text that already exists (yours or AI-drafted) and it returns a tighter, evidence-anchored, human-sounding version with the changes explained.

## When to use

Trigger on requests such as:
- "Humanize this paragraph / section / manuscript"
- "Remove the AI bloat from this draft"
- "This reads like ChatGPT, fix it"
- "Tighten / de-bloat / make this sound less generated"
- "Check my citations" / "did I overclaim here?"
- "Convert these citations to Vancouver / APA"
- "Make this abstract sound like a human wrote it"

## Pairs with

This skill is the suite's canonical humanizer; it revises and humanizes existing academic text and polices its claim-evidence-citation integrity. Compose it with:
- **research-writer** -- drafts and structures whole manuscripts, theses, grants, and reports. Run academic-writer last, after the argument is settled.
- **zotero-cite** -- finds, adds, and exports references. Division of labour: zotero-cite acquires/verifies/persists a reference and manages the `.bib`; academic-writer audits an existing manuscript's citations, flags problems, and converts citation styles.
- **peer-reviewer** -- judges the science and whether claims are earned; academic-writer fixes the prose.
- **content-research-writer** -- for non-academic (blog/article/newsletter) content.

They compose well; humanize last, after the argument is settled.

## Modes

Detect the mode from the request; default to **Humanize**. State which mode(s) you are running.

| Mode | Trigger | What it does |
|------|---------|--------------|
| **Humanize** (default) | "humanize", "de-bloat", "sounds like AI" | Remove the AI tells in the Pattern Catalogue; preserve meaning, data, and voice. |
| **Tighten** | "tighten", "too wordy", "cut length" | Humanize + condense: merge or cut low-information sentences, shorten interpretive passages. Report the word-count delta. |
| **Claim-check** | "did I overclaim", "is this supported" | Audit claim strength against study design and the cited evidence; flag over/underclaiming and uncited assertions. No prose rewrite unless asked. |
| **Citation-check** | "check my citations", "verify references" | Verify bibliographic details against the web; flag fabricated/unverifiable entries and reference-list mismatches. Never invent details. |
| **Style-convert** | "convert to Vancouver/APA/Chicago" | Re-key in-text citations and rebuild the reference list in the target style. Preserve every source. |

## IRON RULES

These are non-negotiable. A humanized text that breaks one of them is a failure.

1. **Never change a finding, number, effect size, CI, p-value, or sample size.** Copy numerals character-for-character.
2. **Never fabricate a citation, DOI, author, year, journal, or page range.** If you add a reference, its details must be verified (search the web) or marked `[VERIFY: detail]`.
3. **Match claim strength to study design.** Cross-sectional/observational becomes "associated with", "consistent with". Cohort becomes "increased risk". Only RCTs/meta-analyses approach "shows"/"demonstrates". Downgrade any verb the evidence does not earn.
4. **Preserve the author's voice and discipline register.** Humanizing is not simplifying. Keep technical vocabulary, equations, and field conventions. Do not insert your own.
5. **Do not silently delete content.** If a sentence carries no information and you cut it, it can go without comment; if it carries a claim, an example, or a caveat, flag the removal.
6. **Leave code, math, YAML, and chunk options untouched** in `.qmd`/`.Rmd`/`.tex`/`.md` files. Edit prose only.
7. **No new AI tells.** Do not "fix" bloat by introducing different bloat. Audit your own output (Pass 4).

## Writing Rules

These govern the prose this skill produces, alongside the IRON RULES above.

1. CLAUDE NEVER USES EM DASHES. Instead, ALWAYS use commas or periods to separate thoughts. When breaking up a clause or adding supplementary information, use commas, semicolons, or parentheses.
2. After generating the initial draft, perform a post-processing review. Search your output for any em dashes (—) and rewrite those sentences using commas or distinct periods instead.
3. Write in a concise, human style. Avoid using formal, robotic transitions. Connect your ideas naturally using standard punctuation (periods and commas).
4. DO NOT EMPHASISE WITH BOLD OR ITALIC IN RUNNING PROSE. Body text in a manuscript carries no `**bold**` or `*italic*` for emphasis. Emphasis comes from sentence construction and word order, not typography. Scattering bold through paragraphs to highlight terms or findings is an AI tell and most journals strip it from body text. After drafting, search for `**` and `*` and remove them from sentences. Bold/italic are permitted ONLY for genuine structural elements, and even then sparingly: structured-abstract run-in headings ("Background.", "Methods."), defined-term introductions at first mention if the venue uses it, table/figure labels, and math/stats symbols set in italic by convention (variables, *P*, *n*, *r*, gene symbols). When unsure, remove it.

### Formatting
- No em dashes (—), smart/curly quotes, decorative Unicode bullets, or emoji
- Replace em dashes with simple, single hyphens.
- No `**bold**` or `*italic*` for emphasis in running prose (see Writing Rule 4). Reserve bold for structured-abstract run-in headings and table/figure labels; reserve italic for statistical symbols and conventional terms. Do not bold whole findings, key terms, or class/group names mid-sentence.

## Section architecture (IMRaD)

When revising or drafting a whole section, enforce its canonical structure. These are hardwired conventions (Mitra Manuscript Workshop; ICMJE Recommendations; EQUATOR/STROBE-CONSORT-STARD-PRISMA). Methods and Results are the factual spine (what you did, what you found); Introduction and Discussion are interpretation. Read top-down, but the strongest drafts are written Methods → Results → Discussion → Introduction → Abstract → Title.

### Introduction: the four-paragraph funnel (HARDWIRED)

Write or revise every Introduction as four paragraphs, broad to specific, each with exactly one job. Do not merge, reorder, or add a fifth; do not put results in the Introduction. End paragraph four with the explicit objective(s).

1. **Current situation.** What is the current situation, or the series of events that led to it? Establish the topic and the present state of knowledge or practice.
2. **The problem.** What problems arise from that situation? Why do they matter, now and in the future? (the stakes)
3. **Prior work and its inadequacy.** How have other researchers addressed these problems? Why are those approaches inadequate or incomplete? (the gap, stated plainly, weighted by evidence not by number of studies)
4. **This study.** How does the present study address the gap? What is done differently, and why is it relevant to the current discourse? State the objective(s) last.

When humanizing an existing Introduction, map its sentences onto these four jobs, move misplaced material to the right paragraph, and flag any job that is missing (e.g. `[INTRO: paragraph 3 — prior work/gap absent]`).

### Methods: reproducible by a stranger

Methods must let a stranger reproduce the study without the author's files. Past tense; describe procedures in the order the Results will report them; each procedure paragraph leads with its purpose, then the how ("To compare X across groups, assay Y was performed…"). Cite standard methods rather than re-describing them. Organise by the ICMJE three drawers, and check the universal core is present:
- **Participants** — design (named explicitly; never "a study was done"), setting (place, level of care, time frame), eligibility (inclusion/exclusion with cut-offs), sampling scheme, sample size with its assumptions, ethics (IEC number + date, consent, trial/study registration).
- **Data & measurements** — variables and tools (named, validated), procedures, instruments/reagents with versions/lots where they affect the result.
- **Statistics** — every test and model named (never "appropriate tests"), the effect measures reported, and software with name + version.
Match the reporting guideline to the design (STROBE observational, CONSORT RCT, STARD diagnostic, PRISMA review); writing to the guideline pre-empts most reviewer critique. If a Methods sentence states a finding, it belongs in Results.

### Results: mirror the Methods

Results mirror Methods item for item and in the same order; anything in Results not set up in Methods is a red flag, and vice versa. The first Results paragraph is participant flow (screened → eligible → enrolled → analysed, accounting for every participant with reasons for loss). State every finding **once**: text for headlines (≤ ~3 numbers), tables for many exact numbers, figures for patterns/trends/time; then cross-reference rather than repeat ("Anaemia was the commonest morbidity, Table 2"). Report each result completely: direction, magnitude, precision (95% CI), and the exact P as an adjunct (the CI is the message; write P = 0.01 not P < 0.05, and P < 0.001 not P = 0.000). No interpretation or mechanism in Results (that is Discussion). Tables: mean ± SD for symmetric, median (IQR) for skewed, n (%) with denominator for categorical; no baseline P-values in an RCT.

### Discussion

Open with the principal findings (no number-dumping from Results), then compare with prior literature, then strengths and limitations, then a specific conclusion (what should change, for whom). Interpret and compare; do not re-narrate the Results tables.

## Voice calibration (optional but recommended)

Before a substantial humanize job, ask the author for **2–3 paragraphs of their own published writing** (a prior paper, a discussion section). Read it for:
- **Sentence rhythm**: average length, variation, how they open sentences.
- **Hedging level**: do they write "may suggest" or "indicates"?
- **Lexical fingerprints**: favoured connectives, British vs American spelling, Oxford comma, tense habits.
- **Person**: "we", "I", or impersonal passive.

Match that fingerprint instead of producing generic clean prose. If no sample is given, default to a measured, direct academic register (active where natural, British or American per the existing text, claims qualified once not thrice).

## Pattern Catalogue

Five categories. The first four mirror general AI-writing tells; the fifth is academic-specific and is the heart of this skill. For each pattern: recognise it, then apply the fix.

### A. Content & argument
1. **Significance inflation**: "plays a pivotal/crucial/vital role", "a critical challenge", "has garnered significant attention". *Fix:* delete the adjective or replace it with the datum that makes it significant.
2. **Vague attribution**: "studies show", "research suggests", "it is widely believed", "experts agree". *Fix:* name the study and cite it, or cut the claim.
3. **Superficial -ing analysis**: sentences ending "…, highlighting the importance of…", "…, reflecting the complex interplay of…", "…, underscoring the need for…". *Fix:* state the actual mechanism or implication, or stop the sentence at the fact.
4. **Promotional / editorialising tone**: "this groundbreaking analysis", "a powerful tool", "the most informative output", "a rich and nuanced picture". *Fix:* let the result speak; remove the self-praise.
5. **False balance**: giving a fringe position equal weight to an established evidence base. *Fix:* weight discussion by evidence strength, not by number of "sides".
6. **Formulaic framing**: "In an increasingly complex world…", rhetorical questions used as section openers. *Fix:* open with the specific problem or finding.

### B. Language
7. **AI vocabulary**: delve, leverage, landscape, tapestry, realm, robust (as filler), navigate (figuratively), foster, underscore, intricate, multifaceted, paradigm shift. *Fix:* plain field-appropriate words.
8. **Rule of three**: reflexive triples ("efficient, scalable, and reliable"; "data, methods, and results"). *Fix:* keep what is true; two items, or one precise item, usually suffices.
9. **Synonym cycling**: calling one construct three names in three sentences (caesarean / C-section / operative delivery). *Fix:* define the term once, use it consistently (terminology discipline).
10. **Copula avoidance / negative parallelism**: "It is not just X, but Y"; "This serves to…". *Fix:* say what it *is*; use "is".
11. **Hollow intensifiers & false ranges**: "very", "highly", "significantly" (when not statistical), "ranging from simple to complex". *Fix:* quantify or cut.
12. **Subjectless / passive default**: "It was observed that…", "Data were felt to…". *Fix:* active voice with the real actor, except where the actor is genuinely irrelevant ("samples were centrifuged at 3000 rpm").

### C. Structure & style
13. **Em dashes**: any em dash (—) used as a separator, parenthetical, or for emphasis. *Fix:* never use em dashes (see Writing Rules). Rewrite with a comma, semicolon, parentheses, or a period; a single hyphen may substitute where a connector is genuinely needed.
14. **Signposting announcements**: "It is important to note that", "It is worth mentioning", "Notably", "Importantly", "Crucially". *Fix:* if it matters, just state it; the emphasis word adds nothing.
15. **Inline-header lists**: bullet runs of "**Term**: explanation" where prose belongs. *Fix:* convert to paragraphs in flowing sections; reserve lists for genuinely enumerable items.
16. **Formulaic transitions**: every paragraph opening with "Moreover/Furthermore/Additionally/In conclusion". *Fix:* vary or drop; let logic carry the link.
17. **Title Case Headings & fragmented headers**: over-capitalised or one-line-deep heading sprawl. *Fix:* sentence case (or the journal's style); merge thin sections.
18. **Curly-quote / typography artifacts** pasted from chat. *Fix:* match the document's existing convention.
19. **Emphasis-bolding / typographic shouting**: bold or italic sprinkled through running prose to stress terms, findings, or group/class names ("the **high-syndemic** class", "membership was **strongly** associated", "we found a **clear** pattern"). This is an AI tell; journals strip emphasis from body text, and over-marked text reads as anxious, not authoritative. *Fix:* delete the markup; if a point needs emphasis, carry it with sentence structure and placement (put the key fact in the main clause, at the start or end of the sentence). Keep bold only for structured-abstract run-in headings and table/figure labels, and italic only for statistical symbols (*P*, *n*, *r*) and conventional terms (gene names, *in vivo*). When in doubt, remove it. See Writing Rule 4.

### D. Hedging & filler
20. **Reflexive hedging**: "may potentially possibly contribute to a degree". *Fix:* one qualifier, placed once. A significant result stated directly belongs in Results; hedging belongs in Limitations.
21. **Generic conclusions**: "Further research is needed", "These findings have important implications". *Fix:* say *what* research, *which* implication, *for whom*.
22. **Filler openers**: "In today's world", "Over the past decades", "It goes without saying". *Fix:* cut; start with content.

### E. Academic integrity (the distinguishing layer)
23. **Uncited claim**: any factual or empirical assertion without a source. *Fix:* add a verified citation or mark `[CITE NEEDED]`. Never invent one.
24. **Citation fabrication / drift**: plausible-looking but non-existent references, or details that don't match the real paper. *Fix:* verify every reference (Claim/Citation-check mode); correct or flag `[VERIFY]`.
25. **Mismatched claim strength**: "proves", "demonstrates", "establishes" on observational data (IRON RULE 3). *Fix:* downgrade the verb.
26. **P-value-only reporting**: "the association was significant (p<0.05)" with no effect size. *Fix:* report effect size + 95% CI + direction, p-value last.
27. **Results narration in Discussion / table narration in Results**: restating numbers instead of interpreting or summarising. *Fix:* in Discussion, interpret and compare to literature; in Results, summarise the trend and point to the table.
28. **Cherry-picking**: only significant findings reported. *Fix:* report all pre-specified analyses; null results are results.

## Before / after

> **Before:** Maternal education plays a pivotal role in shaping the complex landscape of child health outcomes. Studies have shown that it is a crucial determinant, underscoring the vital importance of comprehensive educational interventions. It is important to note that this multifaceted relationship is highly significant.

> **After:** Maternal education is among the strongest determinants of child nutritional status: in pooled DHS data, children of mothers with secondary education had roughly 30% lower odds of stunting than children of mothers with none (Kim et al., 2017). This association persists after adjustment for household wealth.

What changed: significance inflation and AI vocabulary (pivotal, complex landscape, multifaceted) removed; vague attribution ("studies have shown") replaced with a named, cited effect size; signposting opener cut; one claim, evidence-strength-matched.

> **Before:** Our findings clearly demonstrate that the intervention caused a reduction in mortality, proving its effectiveness across all settings.

> **After:** In this single-arm cohort, the intervention was associated with lower mortality (aHR 0.78, 95% CI 0.66–0.92). The absence of a concurrent control limits causal interpretation.

What changed: claim strength matched to design (RULE 3); effect size and CI restored; overgeneralisation ("all settings") removed; the limitation stated rather than buried.

## Process

Run as sequential passes. Show the work; don't just hand back clean text.

1. **Scope & calibrate.** Identify the mode(s) and document type. Read any voice sample. For a file, read it and locate prose vs. code/math regions (never edit the latter).
2. **First rewrite (Passes A–D).** Apply the surface and language patterns. Prefer the minimum edit that removes the tell; preserve every claim.
3. **Integrity pass (Pattern E).** For every empirical claim: is it cited? Is the verb earned by the design? Are effect sizes present? Flag `[CITE NEEDED]` / `[VERIFY]`. In Citation-check mode, search the web to confirm each reference's details. Never fabricate; verify volume/issue/pages/year before asserting.
4. **AI-audit pass.** Re-read your output and ask: *would a reviewer still suspect this was generated?* Search specifically for (a) em dashes (—) and rewrite those sentences with commas or periods (Writing Rule 2); (b) every `**` and `*` in running prose and delete the emphasis markup (Writing Rule 4 / Pattern 19), keeping it only on structured-abstract headings, table/figure labels, and statistical symbols. Hunt residual triples, "Moreover", and hollow intensifiers you introduced. Do a second-pass rewrite on anything that fails.
5. **Report.** Return the revised text plus a short change log keyed to the pattern numbers, a list of any `[CITE NEEDED]`/`[VERIFY]` flags, and (Tighten mode) the word-count delta. For files, edit in place and summarise; for snippets, show before/after.

## Citation verification protocol (Citation-check & when adding references)

- Search for each reference (Google Scholar / publisher / PubMed / Semantic Scholar via the web tools). Confirm authors, year, title, journal, volume(issue), pages, DOI.
- If a detail can't be confirmed, keep the citation but flag the unverified field `[VERIFY: pages]`; do not guess.
- If a reference appears fabricated (no matching record), flag it prominently; do not silently delete or "correct" it.
- Distinguish preprint vs. published versions; cite the version of record where one exists.
- Check reference-list ↔ in-text consistency: every in-text marker has a list entry and vice versa; numbering (Vancouver) is contiguous and ordered by first appearance.

## Output formats

Works in Markdown, Quarto/R Markdown (`.qmd`/`.Rmd`), and LaTeX. For citation styles:
- **Vancouver:** superscript numbers (`^1^`, `^3,4^`), numbered reference list ordered by first appearance. Renders in both HTML and DOCX without a CSL.
- **APA / Chicago:** author–date in text, alphabetised list; or, if the project uses a `.bib`, use `@key` with `bibliography:` in the YAML and the matching CSL.
- Confirm the target style if the request is ambiguous; otherwise follow the document's existing convention.

## Sources & inspiration

This skill adapts the structure of the **Humanizer** skill by blader (MIT licence: voice calibration, categorised pattern catalogue, multi-pass audit, before/after format) and borrows mode/quality-gate and citation-verification ideas from the **academic-research-skills** suite by Imbad0202 (CC-BY-NC 4.0). The AI-writing tells draw on *Wikipedia: Signs of AI writing*; the academic-integrity layer draws on the EQUATOR Network reporting guidelines (STROBE/CONSORT/PRISMA) and ICMJE statistical-reporting standards. Original content; no source text reproduced verbatim.

## Version history

- **1.3.0** (2026-06-10): Added "Section architecture (IMRaD)" with the HARDWIRED four-paragraph Introduction funnel (current situation → problem → prior-work-inadequacy → this-study/objectives), plus Methods (ICMJE three drawers, reproducible-by-a-stranger, mirror order, name design/tests/software+version, guideline-matched) and Results (mirror Methods, participant-flow-first, state-once text/table/figure, complete result = direction+magnitude+precision+exact P) and Discussion discipline. Sourced from the Mitra Manuscript Workshop + ICMJE/EQUATOR.
- **1.2.0** (2026-06-09): Added a hard rule against bold/italic emphasis in running prose (Writing Rule 4, Formatting bullet, new Pattern 19 "Emphasis-bolding / typographic shouting"), and extended the Pass 4 audit to strip `**`/`*` from body text. Renumbered patterns to 28.
- **1.1.0** (2026-05-26): Added a Writing Rules section (no em dashes; em-dash post-processing review; concise human style) plus a Formatting block. Rewrote Pattern 13 from "em-dash overuse" to a hard no-em-dash rule, strengthened the Pass 4 review to search for em dashes, and converted the skill's own separator em dashes to colons/commas.
- **1.0.0** (2026-05-26): Initial release. 27 patterns across 5 categories (Content & argument, Language, Structure & style, Hedging & filler, Academic integrity); 5 modes; voice calibration; IRON RULES; citation-verification protocol.
