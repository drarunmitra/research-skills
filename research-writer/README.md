# research-writer

A Claude Code skill: an academic research writing assistant for public health and
medical research. Drafts, revises, structures, and polishes research writing of any
kind (theses, journal manuscripts, grant proposals, reports), and aggressively
removes AI-generated bloat: em-dashes (a hard rule), significance language, and
filler.

## Install on another machine

This skill is a single self-contained `SKILL.md` with no external dependencies.

```bash
# Clone into your Claude Code skills directory
git clone <this-repo-url> ~/.claude/skills/research-writer
```

Or, if the folder already exists and you just want updates:

```bash
cd ~/.claude/skills/research-writer && git pull
```

Claude Code auto-discovers anything under `~/.claude/skills/`. Invoke it with
`/research-writer` or just describe a research-writing task.

## Update workflow

Edit `SKILL.md`, then `git commit` and `git push`. On other machines, `git pull`.
