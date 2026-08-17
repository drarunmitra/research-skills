# Scaffolding a course

The manifest, the directory tree, and the four config files. Verified against a
shipped Quarto 1.9.36 website project published to GitHub Pages.

## 1. The manifest

One file, `course.yml`, at the project root. It is not read by Quarto. It is read
by you, and everything else is generated from it. Copy `assets/course.yml` and
fill it in with the user.

### Schema

| Key | Required | Notes |
|---|---|---|
| `course.title` | yes | Appears in the navbar, the page footer, every deck footer, and every email subject |
| `course.subtitle` | no | One line, used on the landing page |
| `course.shape` | yes | `workshop`, `semester`, or `single-session` |
| `course.unit_word` | yes | `day`, `week`, or `session`. Drives directory names and headings |
| `course.dates` | yes | ISO dates, one per unit for `workshop`, start and end for `semester` |
| `course.venue` | yes | Or `{{VENUE}}` |
| `course.site_url` | yes | The published URL, with trailing slash. Referenced, never retyped |
| `course.repo_url` | yes | Used for the navbar GitHub icon and `repo-actions` |
| `course.contact` | yes | The address on every email and the help page |
| `course.stack` | yes | `r-quarto`, `python`, or `none`. Selects the optional toolchain module |
| `course.licence` | no | Defaults to CC BY 4.0 for materials, MIT for code |
| `course.palette` | no | `primary` and `accent` hex values. Defaults are in `assets/styles.scss` |
| `units[]` | yes | One entry per day, week, or session |
| `units[].id` | yes | Directory name: `day1`, `week03`. Lowercase, no spaces |
| `units[].title` | yes | Heading text |
| `units[].date` | for `workshop` | Written out in the sidebar title |
| `units[].question` | no | The one question that runs through the unit. Strongly recommended |
| `units[].sessions[]` | yes | Ordered |
| `sessions[].id` | yes | File stem: `s1-fundamentals` |
| `sessions[].number` | yes | Used in the page title as `N · Title` |
| `sessions[].title` | yes | |
| `sessions[].subtitle` | no | |
| `sessions[].teaching` | yes | `HH:MM-HH:MM`. One string, one source of truth |
| `sessions[].handson` | no | Same format. Omit for sessions with no hands-on |
| `sessions[].owner` | yes | Faculty name, or `{{FACULTY}}` |
| `sessions[].slides` | yes | `true` or `false`. See "which sessions get a deck" below |
| `breaks[]` | no | Fixed items in the timetable that are not sessions: registration, tea, lunch |
| `lms` | no | Present only when the course has an LMS. See `lms-kit.md` |

### Placeholders

Anything the user has not decided becomes `{{UPPER_SNAKE}}` and goes into a
tracked list at the bottom of the project `CLAUDE.md` or `README.md`. Never
invent a venue, a date, a faculty name, or a URL. A plausible invention is worse
than a visible gap, because it survives review.

The one placeholder that stays permanently is the mail-merge field, normally
`{{FIRST_NAME}}`. Mark it as such so nobody tries to resolve it.

## 2. What derives from the manifest

Regenerate these; never hand-edit them.

| Derived artefact | Manifest source |
|---|---|
| `_quarto.yml` navbar entries | one per unit, plus Home, Schedule, Resources |
| `_quarto.yml` sidebar, one per unit | `units[].sessions[]`, grouped into `section:` blocks |
| `_quarto.yml` `site-url`, `repo-url` | `course.site_url`, `course.repo_url` |
| `schedule.qmd` tables | `units[]`, `sessions[]`, `breaks[]` |
| `<unit>/index.qmd` arc table | that unit's sessions |
| `.session-meta` strip on each session page | that session's `teaching`, `handson`, `owner`, `slides` |
| Deck front matter footer and date | `course.title`, `units[].date` |
| Every site URL in the LMS kit and the emails | `course.site_url` |

Everything else is prose that the author writes.

When the manifest changes, regenerate all of the above and re-run the checks. A
manifest edit that leaves stale derived files is the exact failure the manifest
exists to prevent.

## 3. Directory layout

### `shape: workshop`

```
course-root/
  course.yml
  _quarto.yml
  index.qmd
  schedule.qmd
  styles.scss
  prelude/          index, install, check-setup, primer, data, pre-reading
  day1/             index.qmd + one qmd per session
  day2/
  slides/
    custom.scss
    day1/           one qmd per session with slides: true
    day2/
  resources/        index, cheatsheet, troubleshooting, glossary, further-reading
  data/             generated, plus a README
  R/  or  py/       dataset generator, worked analysis script
  setup/            install script, check script
  admin/            invitation, reminder, feedback form, timetable source
  lms/              the LMS build kit. NOT in render or resources
  .github/workflows/publish.yml
```

### `shape: semester`

Same, with `week01/` ... `weekNN/` in place of the day directories, and normally
no `prelude/`. Add `assessment/` for assignment briefs and rubrics. The LMS
carries the weekly rhythm, so the site is a reference surface rather than the
spine.

### `shape: single-session`

```
course-root/
  index.qmd        the handout
  slides/
  feedback.md
```

No manifest, no schedule page, no sidebar. Say plainly that this is
`slides-creator-skill` territory with one extra page.

## 4. `_quarto.yml`

Copy `assets/_quarto.yml`. The keys that matter and why:

- `project.type: website`, `output-dir: _site`.
- `project.execute-dir: project`. Load-bearing. Every code chunk then runs from
  the project root, so a page in `day1/` reads `data/students.csv` with no
  prefix. Without it every data path breaks when a page moves between units.
- `project.render`: use globs, one per unit directory, not a file list. A new
  session file is then picked up with no config edit. List `slides/<unit>/*.qmd`
  separately.
- `project.resources`: paths copied into `_site` verbatim. This is what makes
  "download the script" links work. It is also the leak. Include `data/**` and
  the script directory. Include `admin/**` only if the emails and the feedback
  form are meant to be public. Never include the LMS directory.
- `website.site-url` and `repo-url` from the manifest, `repo-actions: [issue]`
  so readers can report a problem in one click.
- `website.search: {location: navbar, type: overlay}`.
- `website.navbar`: one entry per unit, plus Home, Schedule, Resources on the
  left, and the GitHub icon on the right.
- `website.sidebar`: one block per unit, `style: floating`, `collapse-level: 2`.
  Group sessions under `section:` headings that match the real rhythm of the
  day, normally Morning and Afternoon. A flat list of ten sessions is unreadable.
- `website.page-footer`: attribution, licence, "Built with Quarto".
- `format.html`: one theme pair `light: [cosmo, styles.scss]`, `toc: true` at
  depth 3, `code-copy`, `code-overflow: wrap`, `df-print: paged`,
  `link-external-newwindow`, `anchor-sections`, and default figure dimensions.
  No `revealjs` block here: decks declare their own format, so that a deck and a
  page can differ without either fighting the other.
- `execute.freeze: auto`, and `warning`/`message` off by default. Turn warnings
  back on per chunk where the warning is the lesson.
- `knitr.opts_chunk`: `comment: "#>"`, `collapse: true`, and a narrow
  `R.options.width` so output does not overflow the content column.

## 5. Theme

Copy `assets/styles.scss` and replace the palette with `course.palette`.

Structure is two blocks and nothing else:

- `/*-- scss:defaults --*/` holds only Bootstrap and Quarto variables: the
  palette, body and link colours, font stacks, root font size, heading sizes,
  code block background.
- `/*-- scss:rules --*/` holds the named component classes. Keep this list
  short. The shipped site needed exactly five: `.session-meta` (with
  `.meta-item`, `.meta-label`, `.meta-value`), `.badge-faculty`,
  `table.schedule` (with `tr.break`, `tr.handson`, `td.time`), `.card-grid` with
  `.card-tile`, and a callout-header tint that makes an exercise visually
  distinct from a solution.

If you are about to invent a sixth class, check first whether a native Quarto
callout does the job. This mirrors the rule in `slides-creator-skill`, for the
same reason.

One rule that is not cosmetic: when the course teaches code, disable ligatures
everywhere code is shown.

```scss
code, pre, kbd, samp,
div.sourceCode, .cm-editor, .cm-content, .cm-line {
  font-variant-ligatures: none;
  font-feature-settings: "liga" 0, "clig" 0, "calt" 0;
}
```

JetBrains Mono, Fira Code and Cascadia Code all render `|>` as a single arrow
glyph. A beginner has to be able to copy an operator character by character.
Disabling the feature is font-independent; reordering the font stack is not,
because it depends on what the reader has installed.

The deck theme, `slides/custom.scss`, repeats the palette variables and adds
only deck-specific classes. Keep the two palettes equal, from the manifest.

## 6. `.gitignore`

```
_site/
.quarto/
_freeze/
*_files/
/output/
/site_libs/
/*.html
```

The last two entries are debris rules. When a render aborts part way, Quarto
leaves `site_libs/` and stray `.html` files in the source tree rather than in
`_site`. Without those lines they get committed, and they are tedious to
untangle later.

Do not ignore `data/` if the site links to the datasets. Generated and committed
are not mutually exclusive: commit them so the site renders for anyone who clones
it, and regenerate them in CI so the generator is proven to still work. If you
choose that, say so in `data/README.md`, because "generated, not stored" written
next to committed files is a contradiction a reader will trust and act on.

## 7. CI

Copy `assets/publish.yml` to `.github/workflows/publish.yml`. Pages source must
be set to "GitHub Actions" in the repository settings; this cannot be done from
the workflow file.

Step order is: checkout, set up Quarto, set up the language toolchain, install
dependencies, generate datasets, render, upload artifact, deploy.

Two rules that cost a broken build each:

1. **List transitively-loaded packages explicitly.** A dependency resolver reads
   declared dependencies. A package that another package loads at run time is
   not declared anywhere, so it is not installed, and the render dies on the one
   page that needs it.

2. **Never put a comment inside a literal block scalar.** In a `packages: |`
   block every line is passed through verbatim, so a `#` line is handed to the
   installer as a package name and the step fails with a parse error. Put the
   comment above the key.

Pin the Quarto version to the one the site was verified on, and say in a comment
why. If the `_freeze` cache was built with that version, the pin is load-bearing
rather than cautious.

## 8. Project memory

Write a `CLAUDE.md` at the project root with six sections, in this order: what
this is, non-negotiables, session budget, known issues flagged to the course
lead, build commands with their gotchas, and the placeholder tracker.

The known-issues section is the valuable one. It is where a scheduling conflict,
an untested browser, or a deck with no source file gets recorded rather than
silently absorbed. Record the problem, the mitigation, and what remains
unfixed. Do not quietly rework a timetable that a course lead owns.
