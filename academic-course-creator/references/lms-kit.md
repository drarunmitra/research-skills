# The LMS build kit

A repeatable structure for building the course inside a learning management
system. Written against Moodle 4.x, which was the shipped case; the structure
transfers to any LMS with categories, quizzes and file resources, but the XML
schema in section 5 is Moodle-specific.

## 1. The rule that comes first

The kit contains answer keys. It must be in neither the render list nor the
`resources:` list in `_quarto.yml`.

Do not put it under the admin directory because both are "not the site". If
`admin/**` is published, the kit is published with it, and quiz answers are on
the public web with no error, no warning and no way to notice from the build
output.

Verify after every render: `ls _site/<lms-dir>` must fail.

## 2. Why a build kit rather than direct authoring

An LMS is a live system with a web UI. You cannot version-control it, diff it, or
rebuild it from source. So the kit is a specification that a human executes,
plus the importable files.

This has a consequence worth stating to the user at the start: the live course
will fork from the kit. In the shipped case the course lead rewrote three
section summaries directly in the LMS, and four settings ended up different from
the plan. Nothing detects that drift. The kit records what was intended and what
was actually built, in two clearly separated parts, and the second part is
written after the build, not before.

## 3. The five files

```
lms/
  README.md              entry point: preconditions, build order, verification
  course-blueprint.md    structure and settings, with rationale
  activity-text.md       the exact strings to paste
  announcements.md       dated posts
  questions/
    *.xml                source of truth, one file per category
    gift/*.txt           generated, if the instance imports GIFT more reliably
```

### `README.md`

- A file table saying what each file is for.
- The do-not-move warning from section 1.
- A preconditions table verified against the live instance: which course, which
  role you need, which question formats the instance actually accepts, whether
  file upload is enabled. Verify these before writing anything, not after.
- A build order, numbered. Import question banks before creating the quizzes that
  use them.
- A verification checklist with explicit state markers, so a half-done build is
  visible.
- The placeholder tracker for anything not yet known.

### `course-blueprint.md`

Structure and settings. Two parts, in this order:

1. **As planned.** Section-by-section: what activities exist, in what order, with
   a settings table for each. Under every settings table, a short paragraph
   saying why those settings. A table alone gets copied without thought; the
   rationale is what lets someone deviate correctly later.
2. **As built.** Written after the build. Records what actually happened,
   including every departure from the plan, and who made it. Date it.

Course structure that worked, for a pre-course:

| Section | Purpose |
|---|---|
| 0 | Welcome, how this works, the pre-test |
| 1 | Get set up. A submission that proves readiness, and a help forum |
| 2 | Learn just enough. Links out to the site, one check quiz per topic |
| 3 | Data and reading. What to bring, where to be, when |
| 4 | Reference, open all the time |

Order the sections so that someone who starts at section 2 still has a complete
path. Not everyone reads section 1.

### `activity-text.md`

The exact strings to paste, separated from the structure that describes them. One
heading per activity, grouped by section. Keeping copy separate from structure is
what lets the copy be revised without re-reading the settings tables, and it is
what makes a de-bloating pass over participant-facing prose possible.

### `announcements.md`

One dated post per milestone, written in advance. Typically: course opens, a
nudge at the setup deadline, a nudge at the content deadline, and final joining
details. Each carries one action and one deadline.

## 4. Settings that matter

| Activity | Setting | Why |
|---|---|---|
| Pre-test | One attempt, deferred feedback, review closed until after | It is a measurement. Showing answers destroys it. Say so in the description, plainly, so it does not read as distrust |
| Practice quiz | Unlimited attempts, immediate feedback, highest grade | It is practice |
| Practice quiz | Never reveal the right answer | Unlimited attempts plus per-distractor feedback gets them there. Showing the answer removes the reason to think |
| Practice quiz | Weight zero | Nothing here is a grade. Also hide the gradebook from students |
| Readiness submission | No cut-off date | Late is much better than never |
| Help forum | Optional subscription | Let people choose |
| Link to the site | Open in a pop-up, never embedded | An embedded page is a third-party context. Storage and cache are partitioned, so a large payload is re-downloaded and any saved state is invisible |
| Everything | No completion gating | A participant blocked at 23:00 the night before is a participant who does not arrive |

## 5. Question banks

### File layout

One XML file per category. The first element in the file is a category
declaration, and it is what builds the category tree on import.

```xml
<question type="category">
  <category>
    <text>$course$/top/Prelude/Primer 01 · Objects and vectors</text>
  </category>
  <info format="html">
    <text><![CDATA[<p>Four questions on ... Unlimited attempts, zero weight.</p>]]></text>
  </info>
</question>
```

### Every question carries

| Element | Rule |
|---|---|
| `<name>` | A stable code plus a short description: `P1Q1 Counting with a comparison`. The code is how you refer to it in a commit message or an email |
| `<questiontext>` | HTML in `CDATA`. Entity-escape code inside `<pre><code>`: `&lt;` and `&gt;` |
| `<generalfeedback>` | Teaches the concept regardless of what they answered. This is the highest-value element in the file and the one most often left empty |
| `<answer fraction="100">` | Exactly one |
| `<feedback>` on every distractor | Non-empty, and it names the specific misconception that leads to that option |
| `<single>true</single>`, `<shuffleanswers>true</shuffleanswers>` | |
| `<defaultgrade>`, `<penalty>` | Consistent across the bank |

The distractor feedback is what makes unlimited attempts a teaching mechanism
rather than a guessing game. Write each distractor to be the result of one
specific, nameable error, then say in its feedback what that error was. A
distractor nobody would pick teaches nothing and wastes a slot.

Two things to check when writing questions:

- Every distractor must actually be wrong. In the shipped bank one pre-test
  question had to be replaced entirely because a distractor was, on inspection,
  true.
- If the course lead edits a question in the live course, sync the XML back. The
  XML is the source of truth only if it is kept as one.

See `assets/question-bank.xml` for a complete, correctly shaped example.

### GIFT

Some instances import GIFT more reliably than XML. If you generate GIFT from the
XML, generate it, never hand-edit it, and put a banner at the top of each file
saying so. Two transformations are not cosmetic and must be documented in the
generator:

- Escape `~ = # { } :` and backslash, which are GIFT control characters.
- Convert newlines inside a question to `<br>`. A blank line terminates a GIFT
  question, so an unconverted newline silently truncates it.

Render true/false as a two-option multichoice. GIFT's dedicated true/false
feedback ordering is ambiguously documented, and a two-option multichoice is
unambiguous.

## 6. Linking the LMS to the site

The LMS holds the sequence, the deadlines and the assessment. The site holds the
content. Do not duplicate content into the LMS: link out to it.

Every one of those links uses `course.site_url` from the manifest. In the shipped
case the site URL appeared 19 times in the activity text and 16 times in the
blueprint. Renaming the repository would have meant 35 edits in the LMS kit
alone.

Set link resources to display in a pop-up with the description shown on the
course page, so the one-line instruction is readable without a click.
