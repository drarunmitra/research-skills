# Reference: before and after

One worked example. Copy this shape when rewriting any participant-facing
page. The "Before" text is the current `prelude/check-setup.qmd` install
prose, unedited.

## Before

> Open your `meded-conclave-2026` project in RStudio. Paste this into the
> **Console** and press **Enter**. It will take 10-20 minutes on a first
> run. Start it and make tea.

Four actions and a time estimate are packed into two sentences, with a joke
standing in for a success criterion. A reader cannot tell where they are or
whether the paste worked.

## After

```markdown
## Step 2 of 6 — Install the 16 workshop packages

1. Open RStudio.
2. Open your `meded-conclave-2026` project: **File → Open Project**.
3. Click once inside the **Console** pane, at the bottom left.
4. Copy the code box below. Paste it into the Console. Press **Enter**.

**You should see:** lines of text scrolling past, naming each package as it
installs. This takes 10 to 20 minutes the first time. You are finished when
the `>` prompt comes back and stops moving.

**If it does not work:** if R asks
`Do you want to install from sources...?`, type `n` and press **Enter**.
```

## What changed

- Four actions became four numbered steps, one verb each.
- The time estimate moved into **You should see:**, next to the result it
  qualifies, instead of sitting loose in the prose.
- "Start it and make tea" was deleted. It is on the ban list and it did not
  say what a correct run looks like.
- A stopping point was added: the `>` prompt returning is the literal signal
  that the step is done.
- One likely failure got its own **If it does not work:** line, instead of
  being left for the reader to discover.
