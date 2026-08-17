---
name: academic-course-creator
version: 1.0.0
description: >
  Builds a complete academic course as a Quarto website plus its supporting kit:
  unit and session pages with worked examples and graded exercises, a slide deck
  per session, generated teaching datasets, participant emails and a feedback
  form, and a Moodle build kit with question banks. Everything derives from one
  course manifest, so the timetable and the site URL are authored once rather
  than copied into every page. Use when asked to set up, scaffold, plan or
  extend a workshop, short course, semester course or CME, or to add a session
  to one that already exists. Also use when a course site has drifted: session
  times disagree between pages, a URL change means editing dozens of files, or
  answers or admin files are being published that should not be.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Building an academic course

A course is not a pile of pages. It is one timetable, one research question, and
one set of participants, expressed in a website, a slide deck, a dataset, an
inbox and a learning management system. Author the shared facts once, in a
manifest, and derive every appearance of them.

Every rule below came from a shipped two-day workshop site (Quarto 1.9.36,
GitHub Pages, Moodle 4.x): 35 pages, 10 session pages, 8 decks, 4 generated
datasets, 30 questions in 6 banks. Where a rule exists because something broke,
the damage is stated.

## When to use

- "Set up a site for my workshop / short course / CME"
- "Scaffold a two-day course on <topic>"
- "Add session 6 to the course"
- "Build the Moodle course for the pre-work"
- "The times on the schedule page and the session pages disagree"
- "We renamed the repo and now every link is wrong"

## When NOT to

Do not use this for a single lecture, a conference talk, or a seminar with no
participants to email and no timetable to keep consistent. Reach for
`slides-creator-skill` and stop there.

The manifest earns its cost only when a fact appears in more than one place. One
deck has one title and one date, written once. A course has a session that
appears in the navbar, the sidebar, the schedule page, the unit index table, its
own page header, the invitation email and the LMS. That is seven copies of one
start time, and keeping them equal by hand is the observed default failure, not
a hypothetical one.

If you are unsure, count the appearances. Fewer than three, write it by hand.

## Pairs with

- `slides-creator-skill`: hands off to it for every deck. This skill decides
  which sessions get a deck and writes the front matter; that skill writes the
  slides.
- `webr-workshop`: for pre-course pages a participant must run before installing
  anything. Use it whenever the manifest sets `stack: r-quarto` and the course
  has a prelude.
- `research-writer`: for the prose of a pre-reading page or a course rationale.
- `academic-writer`: mandatory before publishing. Run its humanize pass over
  every file a participant reads. See step 5 of the workflow.
- `reproducible-repo`: after the course, to archive the materials and mint a
  DOI.

## Task modes

| Mode | Trigger | What it does | Reference |
|---|---|---|---|
| Scaffold | "set up", "start", "scaffold a course" | Writes `course.yml` with the user, then generates the directory tree, config, CI, and a stub page per session | `references/scaffold.md` |
| Author | "add a session", "write the hands-on for s4", "draft the invitation" | Fills one page, one dataset, or one LMS activity into a course that already exists | `references/teaching-pages.md`, `references/course-materials.md`, `references/lms-kit.md` |
| Audit | "the times disagree", "check before publishing" | Finds drift between the manifest and the pages, and finds material published that should not be | This file, Verification below |

Ask which mode applies if the request is ambiguous. Scaffolding over an existing
course overwrites work.

## The three course shapes

`shape` in the manifest selects the vocabulary and which parts of the kit apply.

| shape | Unit word | Directories | Prelude | LMS kit | Typical size |
|---|---|---|---|---|---|
| `workshop` | day | `day1/`, `day2/` | Yes | Yes | 1 to 3 days, 4 to 6 sessions per day |
| `semester` | week | `week01/` ... `week14/` | Optional | Yes, and it carries more weight than the site | 10 to 16 weeks |
| `single-session` | session | none, pages sit at the root | No | No | one deck, one handout, one feedback form |

For `single-session` the manifest is close to pointless and this skill is close
to `slides-creator-skill`. Say so, and offer the lighter path.

## Load-bearing facts

1. **Never put a per-document format in the site-wide `format:` block.** In a
   Quarto website project that map applies to every format-less input. Adding
   `live-html` alongside `html` made all 28 other pages render twice to the same
   output path: the build aborted on a rename error, `_site` was left holding 1
   file instead of 35, and about 32 stray `.html` files plus `site_libs/` were
   scattered into the source tree. Per-document formats go in that document's own
   front matter.

2. **Nothing containing answers may sit in a directory listed under
   `resources:`.** Quarto copies those paths into `_site` verbatim, with no
   render step and no way to notice. The LMS kit belongs in neither the render
   list nor the resources list. Check the same way every time: after a render,
   `ls _site/<lms-dir>` must fail.

3. **`resources:` publishes the admin kit too.** If `admin/**` is listed, the
   invitation email, the feedback form and the timetable spreadsheet are served
   publicly. That may be what you want. Decide it deliberately, because the
   default is silent.

4. **Set `execute-dir: project` once.** It is what lets a page in `day1/` write
   `read_csv("data/students.csv")` instead of `../data/...`. Without it every
   path in every session page needs a prefix that changes when the file moves.

5. **Author the timetable once.** In the source workshop the timetable existed
   in five places and the schedule page carried a prose instruction to reconcile
   them by hand. The site URL was hard-coded 42 times across 9 files. Both are
   generation problems solved by the manifest.

6. **Pin the toolchain version in CI.** A different CI version than the one the
   site was verified on is an untested render, and the failure surfaces on the
   published site rather than locally.

7. **Rendering proves nothing.** A site renders happily with the wrong times on
   every page, a leaked answer key, and a dead link. Run the checks in
   Verification.

8. **Course material drafted with an assistant reads like it.** A shipped
   pre-course kit needed 187 em dashes removed from participant-facing prose in
   one pass, along with bold used as decoration, reflexive hedging, and
   rule-of-three padding. Nobody notices while writing; everybody notices while
   reading. The de-bloat is a required step, not a polish step, and it is
   cheaper before the same sentence has been copied into an email, a quiz
   description and a page.

## Workflow

1. **Write the manifest.** Copy `assets/course.yml`. Fill it with the user, one
   section at a time. Do not guess dates, faculty names or a venue. Ask.
   Anything not yet known becomes an explicit `{{PLACEHOLDER}}` and goes on a
   tracked list, never a plausible invention.

2. **Generate the shell.** Directory tree for the shape, `_quarto.yml` (navbar,
   one sidebar per unit, render globs, resources), `styles.scss`, `.gitignore`,
   and `.github/workflows/publish.yml`. All from `assets/`, all values from the
   manifest. See `references/scaffold.md`.

3. **Generate the derived pages.** `index.qmd`, `schedule.qmd`, one
   `index.qmd` per unit, and one stub page per session carrying its
   `.session-meta` strip. Every time in these files comes from the manifest.

4. **Author the content.** Session bodies, exercises and solutions
   (`references/teaching-pages.md`), datasets and setup scripts and admin comms
   (`references/course-materials.md`), the LMS kit (`references/lms-kit.md`).
   Hand each deck to `slides-creator-skill`.

5. **De-bloat the prose.** Before publishing, hand every file a participant
   reads to `academic-writer` for its humanize pass. That surface is wider than
   it looks:

   | Surface | Files |
   |---|---|
   | Site | unit index pages, session pages, prelude pages, resources pages, the landing page |
   | Comms | invitation email, reminder email, feedback form |
   | LMS | activity text, section summaries, announcements, quiz descriptions, question feedback |

   Not included: the manifest, the blueprint, `CLAUDE.md`, design records, and
   anything else only the course team reads. Leave those alone.

   Do it once, near the end, as its own commit, so the diff is reviewable and
   the content change is provably nil. A mechanical em-dash sweep produces comma
   splices; rewrite those individually rather than leaving them.

6. **Verify.** Run every check below before telling the user it is done.

## Reference files

| Read this when | File |
|---|---|
| Writing the manifest, laying out directories, or touching `_quarto.yml`, SCSS, `.gitignore` or CI | `references/scaffold.md` |
| Writing a session page, a unit index, an exercise, a solution, or the resources pages | `references/teaching-pages.md` |
| Generating teaching datasets, writing setup or check scripts, or drafting participant emails and the feedback form | `references/course-materials.md` |
| Building the LMS course, writing activity text, or authoring question banks | `references/lms-kit.md` |

## Verification

Run all of these. Report the output, not a summary of it.

1. `quarto render`. It must succeed, and `_site` must hold every page. A partial
   tree is a failure even when the exit code is 0.
2. For every session, the start time in `schedule.qmd`, in its unit index table,
   and in its own `.session-meta` strip must be the same string as the manifest.
3. `ls _site/<lms-dir>` must fail.
4. Grep `_site` for the site URL. Every occurrence must match the manifest value.
5. Grep the source tree for a hard-coded time or URL that is not in the manifest.
6. Every `{{PLACEHOLDER}}` is either resolved or on the tracked list.
7. Open a rendered page in a browser. Confirm the theme applied. An unstyled
   page usually means a theme path resolved relative to the document rather than
   the project root, which fails with a single `WARN` line and no error.
8. Count em dashes in participant-facing prose. The target is zero, and it is
   the fastest single proxy for assistant-drafted text:
   `grep -rc "—" <site pages> <comms> <lms kit>`.
   (That em dash is the search pattern. It is the one in this file that a
   house-style sweep must leave alone.)
   Then read a sample by eye for the tells a grep cannot catch: bold decorating
   rather than structuring, "it is worth noting", three-item lists where two
   items were true, and openers that announce what the paragraph will do.
9. Confirm the de-bloat changed no content. Links, times, byte figures and quiz
   answers must be identical before and after.

## Common mistakes

- Scaffolding before asking for dates and faculty, then inventing them. Ask, or
  use `{{PLACEHOLDER}}`.
- Editing a derived page by hand. The next generation overwrites it. Change the
  manifest.
- Putting the LMS kit inside the admin directory because both are "not the
  site". See fact 2.
- Writing a solution that is only code. A solution carries the interpretation,
  including when the honest interpretation is that the effect is absent.
- Giving every session a deck. Live-coding and group-activity sessions are
  better served by a brief and a screen share.
- Naming a work-in-progress page with a leading underscore. Quarto excludes
  underscore-prefixed files from the project, and then cannot resolve
  `_extensions/`, failing with a misleading message about the extension.
- Treating the render as the test. See fact 7.
- Leaving the prose pass until after the material has been circulated. Once an
  announcement is posted and an email is sent, the published wording and the
  repository wording diverge permanently.
- Running the em-dash sweep mechanically and shipping the comma splices it
  creates. Each one needs the punctuation its sentence actually wanted.

## Platform compatibility

- **Class:** Environment-dependent (needs a CLI/agent with a local shell)
- **Requires:** quarto, git. R only when the manifest sets `stack: r-quarto`.
- **Load it on:**
  - Claude: drop into `~/.claude/skills/` (Claude Code), or paste this body into a Project's instructions (claude.ai).
  - ChatGPT: paste this body into a Custom GPT or Project. Needs Codex/agent mode with a connected environment for the shell steps.
  - Gemini: create a Gem from this body, or place it under the Gemini CLI. Needs the Gemini CLI for the shell steps.

## Version history

- **1.0.0** (2026-08-17): First release. Manifest-driven scaffold, three course
  shapes, LMS kit, derived from a shipped two-day workshop site.
