# Contributing

This repo holds research-workflow skills. A skill is a portable Markdown brief that an assistant loads and follows. Contributions should keep skills portable, evidence-bound, and consistent in voice.

## Skill anatomy

Each skill is a folder containing a SKILL.md with two parts.

1. Frontmatter (YAML): `name`, `description`, `version`, and `allowed-tools`. The description should state what the skill does and when to use it, since assistants route on it.
2. Body (Markdown): a portable set of instructions that works regardless of platform. The body should include:
   - A "Pairs with" block naming related skills in the suite and how they hand off to each other.
   - A "Platform compatibility" block stating the capability class (pure-reasoning or environment-dependent) and any local tools the skill needs.

Keep the body self-contained. Avoid hard dependencies on a specific assistant or file layout unless the skill is explicitly environment-dependent.

## House style

All skills and prose in this repo follow one house style:

- No em dashes. Use a comma, a colon, parentheses, or a new sentence.
- No emoji.
- No bold for emphasis in running prose. Use sentence structure to carry weight.
- Match every claim to its evidence. Do not overstate certainty, and do not invent citations.

## Testing a skill in Claude Code

1. Place the skill folder under `~/.claude/skills/`, for example `~/.claude/skills/my-skill/SKILL.md`.
2. Start Claude Code in any project and invoke the skill, either by name or by a prompt that matches its description.
3. Confirm the skill loads and behaves as written. For environment-dependent skills, confirm the required local tools are installed and reachable first.
