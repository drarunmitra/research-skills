# Course materials

Teaching datasets, the setup and check scripts, and the participant comms kit.
Conventions generalised from a shipped workshop whose generator produced four
datasets and a codebook from one seed.

## 1. Teaching datasets

### Why generate rather than supply

Real data carries consent, ethics and redistribution problems, and it rarely
contains the specific teaching moments a session needs. Generated data can be
designed so that the lesson is in the data.

Say so on the page, at the top, in a `callout-important`. A participant who
thinks these are real findings will cite them.

### Conventions

1. **One script writes everything**, including its own codebook. If the codebook
   is maintained separately it will disagree with the data within a month.

2. **One seed, set once, equal to the course date.** `set.seed(20260909)`.
   Comment it: change this and every number below changes. A reader who does not
   know that will change it to test something and quietly invalidate every
   number quoted in the teaching prose.

3. **Laptop-sized.** The shipped sizes were 240 rows, 1200 rows and 132 rows.
   Big enough that a summary is worth computing, small enough that a participant
   can print the whole thing and that nothing takes more than a second.

4. **A header comment that is a manifest.** Purpose, the command that runs it,
   and a table of output file, rows, what one row is, and whether it is clean or
   messy. This is the first thing anyone reads when a dataset surprises them.

5. **One clean file, one long file, one deliberately messy file.** The clean one
   teaches the verbs. The long one teaches joins and grouped summaries. The
   messy one is where cleaning is taught, and its mess is engineered and
   enumerated rather than random: spaces in column names, several date formats in
   one column, case-variant categories, spelling variants, numbers stored as
   text, several spellings of yes and no, and more than one sentinel for missing.

6. **A causal chain, not independent columns.** Build the outcome from the
   predictors with explicit coefficients and noise, so that an analysis in a
   later session recovers something that is really there. Independent random
   columns produce exercises whose answers are noise, and a participant cannot
   tell the difference.

7. **Deliberate missingness with a known count.** Inject an exact number of
   missing values, not a probability. Then quote that number in the teaching
   prose. In the source workshop `Removed 11 rows containing non-finite values`
   was the pedagogical centrepiece of a whole session, and it only works because
   the count is fixed.

8. **At least one relationship engineered to be null.** Generate one variable
   from something other than the exposure, so the exercise that tests it
   correctly finds nothing, and the solution says so. See `teaching-pages.md`.

9. **A closing report.** Print each file's dimensions and a line stating the
   seed and that re-running reproduces the files exactly.

10. **A framing that threads the whole course.** A study design, not a table:
    sites, arms, a pre and post measure, a repeated-measures component. One
    research question then runs through every unit.

### Where it lives

`R/00_generate_datasets.R` or `py/00_generate_datasets.py`, writing into
`data/`. Run before render, locally and in CI. Add `data/README.md` stating that
the files are synthetic, how to regenerate them, and whether they are committed.

For `stack: none`, skip this entirely. A course with no code has no datasets to
generate, and a spreadsheet of examples belongs in `resources/`.

## 2. Setup and check scripts

Two scripts, both participant-facing. Only for `stack: r-quarto` or
`stack: python`.

### The install script

- Grouped by purpose with a comment per group, not one flat list.
- Idempotent: compare against what is already installed and install only the
  difference. A participant will run it more than once.
- A post-check that fails loudly if anything did not install, rather than
  finishing quietly with a broken environment.
- A closing message naming the next command to run.

### The check script

This is the one that decides whether the first morning is calm. It prints a tick
or a cross per check and ends with a summary and a block the participant pastes
back to the organisers.

Checks, in order:

1. Language version meets the minimum.
2. A version-gated feature the course actually uses is available.
3. The IDE is present.
4. Quarto is present.
5. Every required package is installed.
6. The core stack actually loads, not just resolves. Installed and importable
   are different failures.
7. The working directory is writable.
8. An end-to-end render of a tiny document succeeds.

Check 8 is the one that matters. The first seven can all pass on a machine that
cannot render, and rendering is what the course asks them to do.

Pair it with a `check-setup` page that mirrors the script: how to run it, what a
healthy result looks like, a table of common results and what each means, and how
to save the evidence. If the LMS has a readiness assignment, that evidence is
what gets uploaded.

## 3. The participant comms kit

Three files in `admin/`, all Markdown, all with a header block above a `---`
rule so the send instructions never get pasted into the message body.

```markdown
**Send:** four weeks before
**To:** all registered participants
**Subject:** Your place on <course title>, <dates>

---

Dear {{FIRST_NAME}},
```

`{{FIRST_NAME}}` is the mail-merge field and stays unresolved forever. Mark it
as permanent in the placeholder tracker so nobody tries to fill it.

| File | Sent | Carries |
|---|---|---|
| `invitation-email.md` | About four weeks before | Dates, venue, what to bring, the site URL, the pre-work deadline, the LMS enrolment link |
| `reminder-email.md` | About five days before | The setup check as the single call to action, the timetable, travel and arrival details, who to contact when stuck |
| `feedback-form.md` | At the end | About you, a per-session rating table, free text on what to keep and what to change |

Every URL in these comes from `course.site_url`. The reminder is a nudge to
complete the setup check, not a second invitation: one action, stated once,
early.

Add `admin/checklist.md` for the organisers if the course has a venue: room
layout, power, wifi capacity, printed handouts, name badges, and who opens the
room.

### Bandwidth

If the course asks participants to download anything on the day, do the
arithmetic and put it in the checklist. Participants times payload divided by the
time available gives the sustained rate the venue must supply. Forty people
pulling 45 MB in the first ten minutes is about 1.8 GB and roughly 25 Mbit/s
sustained, which is more than many teaching rooms provide. Where the payload is
cacheable, tell participants in the reminder email to open the page once before
they travel.

## 4. Publishing decisions

`admin/**` is published if it is listed under `resources:` in `_quarto.yml`. That
means the invitation email, the feedback form and the timetable are on the public
web. Sometimes that is right: participants can re-read the joining instructions.
Sometimes it is not: an internal organiser checklist with phone numbers should
not be.

Split it if in doubt. Keep participant-facing files in `admin/` and put anything
internal in a directory that is in neither the render list nor `resources:`, the
same way the LMS kit is handled.

Never put a real dataset in a published directory to "look at it later". A stray
spreadsheet in `data/` will be uploaded by the next local publish, and because CI
would not upload an untracked file, the exposure is intermittent and easy to
miss.
