# research-skills

A collection of research-workflow skills for Claude, ChatGPT, and Gemini, focused on public-health and academic research. The suite spans the full lifecycle: data analysis, drafting and revising academic writing, peer review, citation management, reproducibility and archiving, teaching slides, and a separate track for non-academic content. Each skill is a portable Markdown brief (a SKILL.md) that you load into an assistant; some are pure reasoning and run on any chat model, while others drive local command-line tools and need an agent or CLI tier.

## The research lifecycle

```
  qual-researcher ┐
                  ├─► research-writer ─► academic-writer ─► peer-reviewer ─┐
  time-series ────┘     (draft)           (humanize)         (review)       │
                            ▲                                               │
                            └─────────────── revise loop ◄─────────────────┘
  zotero-cite ........... citations throughout (acquire / verify / export .bib)
  publishing-research-compendium ........ package + Zenodo DOI
  slides-creator-skill .................. present results
  content-research-writer ............... separate non-academic track
```

## Skills

### Analysis
- time-series: analyse and forecast time series in R with the tidyverts stack (tsibble, feasts, fable), including surveillance and outbreak detection.
- qual-researcher: qualitative analysis from transcript cleaning through coding, thematic analysis, framework mapping, and COREQ/SRQR reporting.

### Writing and review
- research-writer: draft, structure, and revise academic writing of any kind (thesis, manuscript, grant, report).
- academic-writer: revise and humanize academic prose, calibrate claims to evidence, verify citations, and convert citation styles.
- peer-reviewer: review a manuscript as a journal editor and peer reviewer, with reporting-guideline and statistics critique.

### Citations and reproducibility
- zotero-cite: find and verify references, manage Zotero, export a .bib, and cite with @citekey.
- publishing-research-compendium: package code, data, and manuscript into a reproducible repository with a Zenodo DOI.

### Teaching
- slides-creator-skill: build minimal Quarto Reveal.js teaching decks.

### Non-academic content
- content-research-writer: write non-academic content such as blogs, newsletters, and thought leadership.

## Compatibility

Skills fall into two classes. Pure-reasoning skills run on any LLM, including browser chat. Environment-dependent skills also reason but expect a CLI or agent tier with access to local tools.

| Skill | Class | ChatGPT | Claude | Gemini | Requires |
|---|---|---|---|---|---|
| research-writer | Pure-reasoning | Yes | Yes | Yes | none |
| academic-writer | Pure-reasoning | Yes | Yes | Yes | none |
| content-research-writer | Pure-reasoning | Yes | Yes | Yes | none |
| peer-reviewer | Pure-reasoning | Yes | Yes | Yes | none |
| qual-researcher | Pure-reasoning | Yes | Yes | Yes | none |
| time-series | Environment-dependent | Yes (CLI/agent) | Yes (CLI/agent) | Yes (CLI/agent) | R with tidyverts (tsibble, feasts, fable) |
| publishing-research-compendium | Environment-dependent | Yes (CLI/agent) | Yes (CLI/agent) | Yes (CLI/agent) | git, Quarto, R |
| zotero-cite | Environment-dependent | Yes (CLI/agent) | Yes (CLI/agent) | Yes (CLI/agent) | shell, Zotero with Better BibTeX on local API port 23119 |
| slides-creator-skill | Environment-dependent | Yes (CLI/agent) | Yes (CLI/agent) | Yes (CLI/agent) | Quarto, git |

## Install

Each skill lives in its own folder with a SKILL.md. Load a skill by making that brief available to your assistant.

- Claude Code: clone or symlink each skill folder into `~/.claude/skills/`. The skill is then available by name.
- claude.ai Project: paste a skill's SKILL.md body into the Project instructions.
- ChatGPT: paste a skill's SKILL.md body into a Custom GPT or a Project. Tooled (environment-dependent) skills need Codex or agent mode to run their local tools.
- Gemini: create a Gem from the SKILL.md body, or use the Gemini CLI. Tooled skills need the CLI.

## License

Content is licensed CC BY 4.0. See LICENSE.
