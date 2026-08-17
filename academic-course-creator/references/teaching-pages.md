# Teaching pages

The session page template, the exercise grammar, the unit index, the resources
pages, and the handoff to slides. The template below held across all 10 session
pages of the shipped workshop; deviations were deliberate and are noted.

## 1. The session page, ten parts in order

### 1. Front matter

Two keys only.

```yaml
---
title: "3 · Introduction to data visualisation"
subtitle: "The grammar of graphics"
---
```

The number comes from `sessions[].number`. The middle dot reads better than a
hyphen and sorts cleanly in the sidebar. Everything else about the page format
is inherited from `_quarto.yml`.

### 2. The session-meta strip

Generated from the manifest. Four items, in this order.

```markdown
::: {.session-meta}
::: {.meta-item}
[Teaching]{.meta-label}[11:15 – 12:00]{.meta-value}
:::
::: {.meta-item}
[Hands-on]{.meta-label}[12:00 – 13:00]{.meta-value}
:::
::: {.meta-item}
[Faculty]{.meta-label}[Name]{.meta-value}
:::
::: {.meta-item}
[Slides]{.meta-label}[[Open deck ↗](../slides/day1/s3.html){target="_blank"}]{.meta-value}
:::
:::
```

Drop the Hands-on item when `handson` is absent, and the Slides item when
`slides: false`. Never type a time here. It comes from the manifest or it is a
bug.

### 3. Hidden setup chunk

```r
#| include: false
```

Loads the stack, sets a plot theme, reads the datasets. It exists so the visible
chunks later can show only the line being taught. Present on every page that
runs code, absent otherwise.

### 4. Learning objectives

`## Learning objectives`, a numbered list of about five, each starting with a
verb the participant can do at the end. Not "understand". Present on teaching
sessions; skip it on activity sessions such as live coding or a group brief,
where the brief itself is the objective.

### 5. Teaching body

One `##` per concept. Inside each: the worked example first, then the prose that
explains what just happened. Not the reverse. A beginner reads the output and
then wants to know why; explaining before showing gives them nothing to attach
the explanation to.

This is the non-negotiable from the source project: every concept gets a worked
example before any exercise asks for it.

### 6. Interleaved callouts

Use a callout when a trap deserves to stop the reader. Write its title as a `##`
heading on the first line inside the div.

```markdown
::: {.callout-important}
## That warning is the point
`Removed 11 rows containing non-finite values`. Eleven students have no
post-test score. Real analyses die here.
:::
```

Observed density on a mature 300-line session page: five or six notes, four or
five tips, one important. If a page has none, the material is probably being
presented as friction-free when it is not.

### 7. The hands-on boundary

```markdown
# Hands-on {#hands-on}
```

Level one, with an explicit anchor. The anchor is what lets the schedule page
deep-link `day1/s3.qmd#hands-on`, so a participant arriving at 12:00 lands on
the exercises rather than the top of a long page. Open the section with the
clock time and what the room should do.

### 8. Exercises and solutions, strictly alternating

```markdown
::: {.callout-note title="Exercise 1: Distribution of post-test scores"}
**Time:** 5 minutes

Draw a histogram of `posttest`. Choose a binwidth that shows the shape
without inventing detail.
:::

::: {.callout-tip title="Solution 1" collapse="true"}
```r
ggplot(students, aes(x = posttest)) +
  geom_histogram(binwidth = 5)
```

The distribution is close to symmetric, so a mean is a fair summary here.
The warning about 11 removed rows is the same 11 students as before.
:::
```

Rules:

- Exercise in `callout-note`, solution in `callout-tip collapse="true"`. Always.
  The callout-header tint in the stylesheet is what makes the two readable at a
  glance while scrolling.
- Every exercise carries a `**Time:**` line. Without it a facilitator cannot pace
  the room, and the sum of the times is the only honest check that the hands-on
  fits its slot.
- A solution carries interpretation, not just code. Code answers "what do I
  type". The participant came for "what does it mean".
- Write at least one exercise whose honest answer is that there is no effect.
  Every exercise finding a clean result teaches that analysis always finds
  something, which is the opposite of the lesson.

The exception to the callout rule is an interactive page where a checker
provides its own hint and solution controls. Use the native controls there
rather than maintaining every answer twice. See `webr-workshop`.

### 9. Key takeaways

`## Key takeaways`, a `{.callout-note appearance="minimal"}` holding three to
five bullets. Each one is a sentence the participant could say out loud, not a
topic name.

### 10. Next

```markdown
## Next

→ [4 · Introduction to Quarto](s4-quarto.qmd) : write a document that contains
its own code.
```

Link plus a one-line gloss of why they would want to go there. The last session
of a unit ends with `## End of Day 1` and what happens tomorrow.

## 2. The unit index page

Front matter with title and date, then:

- One paragraph: what the participant will be able to do by the end of the unit.
- `## Today's arc`, a three-column table (Time, Session, Faculty) generated from
  the manifest, with session names linked and non-session rows (registration,
  lunch) present but unlinked.
- `## Before the first session`, a short checklist.
- `## The question that runs through today`, as a blockquote. One research
  question that every session attacks a piece of. This is the single strongest
  structural device in the source workshop: it turns five sessions into one
  argument. Name which session does which part.
- `## Ground rules`, on the first unit only. Ask immediately; type the code
  rather than paste it; errors are normal; you will not remember the syntax.

## 3. The resources pages

Four pages, static, no executed code, few or no callouts. The contrast with
session pages is deliberate: this is reference, and reference should look
different from teaching.

| Page | Shape |
|---|---|
| `cheatsheet.qmd` | One `##` per topic, non-executing fenced code, no prose between blocks |
| `troubleshooting.qmd` | One `##` per error message, quoted verbatim as the participant sees it, then cause and fix. Verbatim matters: they arrive by searching the text on their screen |
| `glossary.qmd` | Thematic `##` sections, entries as `**Term**: definition.` One sentence each |
| `further-reading.qmd` | `##` sections, each a two-column table of link and one-line annotation. An unannotated link list is not a reading list |

Plus `resources/index.qmd` as the hub: during-the-course links, downloadable
materials, and the full list of decks.

## 4. Which sessions get a deck

`slides: true` when the session has 30 minutes or more of front-of-room
teaching. `slides: false` for live coding, group activities, and hands-on-only
slots. In the source workshop 8 of 10 sessions had decks, and the two without
were correct to have none: a live-coding session is a screen share, and a group
activity is a brief.

Hand the deck to `slides-creator-skill`. This skill supplies:

- the file path, `slides/<unit>/<session-id>.qmd`
- title, subtitle, author from `sessions[].owner`, date from `units[].date`
- a footer string built from `course.title`
- the shared `../custom.scss`
- the list of concepts from the page's `## Learning objectives`

Write speaker notes as timed stage directions, not as a script.

```markdown
::: {.notes}
3 min. Point out that posttest is dbl with NAs.
STOP on the warning. Ask the room what it means before telling them.
This is the most important 60 seconds of the session.
:::
```

A note that says what to do and when is usable at speed. A note that paraphrases
the slide is not.

## 5. Keeping the page and its script in sync

If a session page reproduces a script that also exists as a file, include it
rather than copying it.

```markdown
{{< include ../R/01_analysis.R >}}
```

In the source workshop a 130-line analysis script was hand-copied into a session
page and the two drifted: the page's copy lost a directory-creation guard and two
`show_col_types` arguments, while the page still described it as the complete
script. Nothing detected this. An include cannot drift.

## 6. Voice

Write it the way you would say it to the room. The failure mode of
assistant-drafted teaching material is not that it is wrong, it is that it is
inflated: every point arrives in threes, every claim is hedged, and every
paragraph opens by announcing itself.

While drafting, four habits prevent most of the later cleanup:

- Punctuate with what the sentence wants. A comma, a colon, parentheses, or a
  new sentence. The em dash is the loudest single tell and it accumulates
  invisibly.
- Use bold to structure, never to emphasise. A bold label at the start of a list
  item is structure. A bold phrase mid-paragraph is decoration.
- Say the thing rather than hedging toward it. "Check the warning", not "it is
  worth checking the warning".
- Let a list be two items when only two are true. Padding to three invents a
  third.

Beginners are the audience, so short sentences and one idea per sentence are
correct here for pedagogical reasons as well as stylistic ones.

The formal pass happens at step 5 of the workflow, using `academic-writer`, over
every participant-facing file. Drafting well does not remove that step, it just
makes the diff small.

## 7. Session budget

State the budget explicitly and check the content against it before declaring a
page done. For a workshop the shipped budget was 45 minutes teaching plus 45 to
60 minutes hands-on.

Sum the `**Time:**` lines. If they exceed the hands-on slot, say so plainly and
propose what to cut. Do not silently write 90 minutes of exercises into a
60-minute slot: the room discovers it, not the author.
