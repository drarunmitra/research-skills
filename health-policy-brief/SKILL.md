---
name: health-policy-brief
version: 0.2.0
description: |
  Use when drafting, restructuring or checking a health policy brief, action plan, dossier, Cabinet note, Government Order draft, NHM PIP input note or District Health Action Plan section for district, state or national decision makers in India. Also use when a draft policy document reads half baked, has no clear structure, overclaims, mixes totals, or cites sources that do not support the sentence.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
---

# Health policy brief

Write policy documents that a busy non-specialist can act on. Structure comes from published guides. Wording comes from checked rules. Every number and every citation is traced.

The rules rest on a review of published policy-brief guides and the evidence on how decision makers use them. The reference files hold the reasons.

Be honest about the evidence. No study shows that any brief format leads to better decisions. Graded entry helps understanding. Local data goes with higher stated intent. Page limits, sentence caps and key-points boxes are house style. Say so if asked. Do not claim a format raises uptake.

## Pairs with

- `academic-writer`: AI-tell patterns. Run it last on the prose.
- `numbers-audit`: when numbers come from an analysis pipeline.
- `typst-report-tikz`: PDF build.
- `peer-reviewer`: optional review of a long dossier.

## The five steps

Do them in order. Do not draft before step 2 is done.

### 1. Ask: reader, decision, evidence

Ask the user (skip what they already said):

1. Who reads it: role and level (district, state, national)?
2. What must they decide, by when? (ratify, release money, issue an order, approve a plan) Is it a decision paper that asks for money, or a suggestive document that only offers options? Do not write a money ask, a named decider (a Minister, a Secretary) or a deadline the user did not give.
3. Who briefs them in person, if anyone?
4. What sources and numbers exist? Ask for files. Local data first.
5. Is there a department format or a recent example to follow?

If local data is missing, list it as an open item. Never fill the gap from memory.

### 2. Choose the document and the framework

| Reader needs to | Document | Sections in |
|---|---|---|
| Choose between options and release money | Policy brief | `references/documents.md` section A |
| Sign off a plan with owners, dates, costs | Action plan | section B |
| Hold the full file for staff and decider | Dossier | section C |
| Get Cabinet approval | Cabinet note | section D |
| Issue an order | GO draft | section E |
| Seek NHM funds | PIP input note | section F |
| Plan for one district | DHAP section | section G |
| Choose a technology or package, with cost per QALY | HTA-style evidence brief | section H |
| Turn one study into a programme decision | Institute brief (ICMR style) | section I |
| Size a national problem, or compare states | Policy paper or state factsheet | section J |

Frameworks are in `references/frameworks.md`. The core spine is: problem, options (benefits, harms, cost), implementation, with an equity and fit check. Add GRADE-style option tables, budget impact for money, RE-AIM for monitoring.

Say which structure you chose and why, in one line.

### 3. Draft

Rules:

- Open with a summary box: what the document is, what it is for, who is at risk (places and people), how places were ranked, and the plan. Count the people at risk. With no population data, write "not provided" and list it as an open item.
- Coverage check before you draft: does each score or action cover every group the document names (for example mothers as well as children)? If not, say so in the summary and show the missing group beside it.
- Plain words: keep invented labels out of the text ("tranche", "firm", "re-runs"). Use the user's words. Ask the user to confirm any new term.
- Keep the body clean: no file paths, and no AI-audit lines unless the user asks. Put process and audit detail in a separate audit file.
- Keep to the length the user asked for. Count the main text including tables, excluding annex and front matter. With no length given, a brief is 2 to 4 pages (about 800 to 1,800 words) plus annex. Move option detail, cost lines and method into the annex before you cut the ask, the recommendation or the limits. A brief over 2,000 words in the main text is a dossier: say so, or cut.
- Open with the decision asked, the recommended action and the cost. Background comes after.
- Put one labelled recommendation apart from the evidence. It may not be stronger than the finding.
- Add a "what this means here" line with local data.
- Define each technical term at first use. Expand each acronym at first use.
- Use the wording ladder, causal verb table and basis labels in `references/claims-and-numbers.md`.
- Write forecasts as labelled scenarios with a signpost and a trigger. No bare predictions.
- Put the weakest fact at the point of use. Add one "least certain part" line at the top.
- Language rules are in `references/plain-language.md`.
- Never write scheme names, budget heads, sanction wording or unit costs the user did not give. Mark them `[TO VERIFY]` and list them as open items.
- A local figure derived from a wider rate is allowed only as sourced rate times sourced local quantity. Label it "derived", show the formula, add it to `numbers.csv`, and say the rate is not local. If either part is missing, write "not provided". Never scale a state total to a district by guess.
- Front matter: write "AI audit: pending" until step 5 is done, then name the audit agent and the date.
- Mark every state format as "check against a recent example from this department". Read in full: the central Cabinet note handbook, NHM PIP guidance, the old DHAP framework, two Telangana Finance GOs, HTAIn briefs, ICMR institute briefs, NITI reports. Not found: any Telangana Cabinet note format, any current DHAP template, the HTAIn Process Manual.

### 4. Check

Run the script on the draft:

```
python -I scripts/check_text.py DRAFT.md --numbers numbers.csv
```

It reports: sentences over 25 words (flag) and over 28 (fail), em dashes, bold in prose, banned causal verbs, bare "there is uncertainty", numbers not in the numbers file, acronyms used before they are defined. Fix every fail. Readability scores are a flag, not a pass mark.

`numbers.csv` has the columns `key,what,value,source`. Build it from the user's data files. If no file exists, build one with the user and note each number's source.

Derived numbers (sums, differences, shares) go into `numbers.csv` as new rows, with source "derived: [formula and the rows used]". Do not hide them with `--allow`. Use `--allow` only for one-off dated or named-source tokens. Dates next to a month name and four-digit years are ignored by the script.

Then check the rendered PDF, not only the text:

- Contents at the top. Page numbers run in order (full-page plates must not leave a gap). Every table and figure is named in the text.
- No tall figure that leaves a near-empty page behind it. Look at every page as an image.
- A figure and a table never sit side by side without one or two lines of text between them.
- With citeproc, protect proper nouns in `.bib` titles with double braces, and put the reference list before any annex of plates or sheets.

Then check by hand:

- Scope match: do the decision, the recommended option, the headline cost and the draft order all cover the same set (same districts, same institutions, same phase)? If the headline leaves out a decided add-on, give both figures together.
- Total or increment: is each "added" figure the extra cost, or the total of a larger set that already contains the base? Say which. Do not subtract ranges.
- Who decided: is each decision attributed to the right body (the government, the plan lead, a committee)? A proposal is not a decision.
- Owner level: can the named owner really do the action? A Collector cannot issue a state order. Name one accountable owner per action, with partners listed separately. Split a state action from the district action that follows it.
- Test scope: does each strength claim say what was tested? "Firm" for the overall tier is not "firm" for each hazard. Name the measure and the level it applies to.
- Complete money ask: every line in the cost table has a figure with a low, planning and high value, or an explicit "not provided" with the missing input named. Do not ask for sign-off on a total with blank lines you could compute from the given rules.
- Action table: every action has what, who, when and how much. Count the actions that fail any of the four and fix them.
- Excluded places: name the districts, mandals or sites that fall outside the plan and say why.
- Promise match: does every sentence in the objective, key messages and outputs ("every site is protected") match what the action table delivers, site type by site type? Narrow the sentence, or add the action.
- Action and budget match: does each action's frequency and scope match what the cost line pays for (monthly refills versus one-time stock; all sites versus some)?
- Page 1 and body match: is each total on page 1 on the same basis as the same total in the body? Label the base wherever a share or comparison is made.
- "No data" claims: before you write "the files give no X", search the files for X. Say where you looked.
- Cross-references: every "see action A2" or "annex item 6" points at the right item.
- Authority by action part: when an action splits across departments (health sites and anganwadi centres), name the owner of each part. Do not name the authors or their institute as accountable owner. Make them advisers.
- Source conflicts: when two sources disagree (for example 1 to 2 C versus about 1 C), use the more cautious one, state both, and say which you used.
- Triggers with no sourced threshold: use a date or a named event as the trigger and write "threshold not provided". Do not invent a number.
- Unratified source plans: if the plan you draw from is a draft by the same authors, say so. Do not write as if an official plan exists.
- Counts: does "none of N" use the placed count? State how many are unplaced.
- Does every citation support the exact sentence it sits on? Cite at the point of use. An annex list is not enough.
- Does every total say what it counts and what it leaves out?
- Do the key messages agree with the limits section?
- Is every selected set (districts, facilities) defined?
- Are assumptions marked, with a line asking the officer to confirm?

### 5. Audit with a fresh agent

Spawn a fresh agent with `references/audit-prompt.md`. Do not give it your conclusions. Give it only the draft and the source files. Fix what it finds. Name it in the front matter as an AI audit agent.

Then run `academic-writer` for AI tells. Then the user reads it.

## Iron rules

1. Ask the reader and the decision first.
2. No number without a source in a file. No source from memory.
3. No total without a basis label. Write "basis not provided" and list it as an open item.
4. No recommendation stronger than the finding.
5. No forecast without a scenario label, range and trigger.
6. No em dashes. No bold in running prose. Sentence case headings.
7. Paraphrase sources. Short quotes only.
8. Mark every unverified item `[TO VERIFY]` in the draft. A brief goes out only when the register is empty or the user accepts the open items.
9. Label proposals as proposals. A draft order says "draft, not issued".
10. Say plainly that a brief informs an open decision. It works best with a short oral briefing.

## Red flags: stop and fix

| Thought | Fix |
|---|---|
| "The evidence is strong enough to say it will work" | Use the ladder. Name the study design and certainty. |
| "I remember the scheme budget head" | Ask for the source. Mark `[TO VERIFY]`. |
| "Phase 1 and Phase 2 totals are close, I will compare" | Put both on one basis, or label each. |
| "A long sentence is fine, the content is rich" | Split at 25 words. |
| "I will add a limits section at the end only" | Put the weakest fact where it is used, and one line at the top. |
| "The reader is an expert" | Define the term anyway. Ministers and Collectors are not health specialists. |
| "A table of studies shows it" | Count the studies. Name sample size and place. |

## What this skill cannot do

- It has no tested format for Indian officials. Transfer from other groups is an assumption.
- It does not know your state's current GO or Cabinet note format. Ask for a recent example.
- It does not replace a subject expert reading the final text.

## Platform compatibility

- Class: environment-dependent for the checker (`scripts/check_text.py` needs Python 3). The drafting rules run on any chat model.
- Claude Code: place this folder under `~/.claude/skills/`. Other assistants: paste SKILL.md and the reference files you need into the project instructions, and run the checker locally.
