---
name: publishing-research-compendium
description: >
  Use when packaging a finished analysis (code + data + manuscript) into a
  public, citable, reproducible repository and archiving it for a DOI — e.g.
  "set up a repo for this paper", "make this reproducible", "get a Zenodo DOI",
  "prepare for medRxiv/journal submission", "code and data availability". Covers
  repos with non-redistributable source data, large spatial/binary files,
  CITATION.cff, Zenodo, and Quarto manuscript front-matter.
version: 1.0.0
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Publishing a Research Compendium

## Overview
Turn an analysis pipeline into a repository a stranger can clone and reproduce, and that a paper can cite with a stable DOI. **Core principle: ship the smallest self-contained thing that reproduces the results, and verify it actually does before you publish.**

The high-level workflow (provenance/derived split, Zenodo, concept vs version DOI, CITATION.cff) is mostly intuitive. This skill exists for the parts that are NOT, where capable people still go wrong (see Common Mistakes).

## Pairs with

This is the terminal, packaging step of the research lifecycle. Upstream skills feed it:
- **research-writer** and **academic-writer** -- the manuscript (drafting/structural revision, then humanizing) that the compendium ships.
- **zotero-cite** -- the reproducible `.bib` that the manuscript points at.
- **time-series** and **qual-researcher** -- the temporal and qualitative analysis the repo packages.
- **peer-reviewer** -- the pre-submission review whose reproducibility comments this skill addresses.

## Repo layout (research-compendium convention)
```
code/   numbered scripts; 00_setup.R defines here()-based paths, packages, seed
data/   derived analytic objects that figures/tables consume (shareable)
files/  geometry + lookups (spatial layers, crosswalks)
out/    result tables (CSV) + figures behind the paper
paper/  manuscript + supplement (.qmd) + .bib   (source only)
README.md  CITATION.cff  LICENSE  .gitignore
```
README MUST contain a **script→output map** (table: each script → what it reads → what it writes) and a two-tier reproduction path (quick-start vs full rebuild).

## Non-redistributable raw data → provenance/quick-start split
When raw data can't be shared (programme-governed, patient-level):
- Ship the **derived district/area-level aggregates** the figures actually use — no row-level/identifiable cells. Confirm aggregation is contractually permitted before anything goes public.
- The shipped aggregates are the **quick-start entry point**: scripts downstream of them reproduce every output.
- Keep the raw→aggregate scripts as **documented provenance**, guarded so they fail loudly without the private source: `if (!nzchar(Sys.getenv("SOURCE_ROOT"))) stop("provenance step; use shipped data/…")`. Mirror the "optional Step 1" pattern.

## Large files: simplify-and-verify, don't blindly fetch (the #1 trap)
A >50 MB file in git bloats every clone and the Zenodo archive. Before deciding, ask **is this file a derived product or an unmodified public download?**
- **Unmodified public layer** (GADM/Census/WorldPop as-downloaded): don't commit; add a `get_*.R` that downloads it + a checksum.
- **Derived product** (e.g. boundaries dissolved/edited by the pipeline — has NO public URL): you cannot "link to the source". Instead **simplify it**. For spatial layers, topology-preserving simplification keeps adjacency:
  ```r
  sf_use_s2(FALSE)                                   # planar, match the pipeline
  gs <- rmapshaper::ms_simplify(g, keep = 0.05, keep_shapes = TRUE)
  gs <- sf::st_make_valid(gs)                        # repair self-touching loops
  ```
  Then **VERIFY the analysis-relevant structure survived** before swapping — don't trust the file size alone:
  ```r
  # contiguity graph must be unchanged if you run Moran's I / spatial models on it
  identical(sum(spdep::card(spdep::poly2nb(gs))), sum(spdep::card(spdep::poly2nb(g))))
  ```
  73 MB → ~4.6 MB with an identical queen-contiguity graph is typical at keep=0.05.
- **If the big blob is already committed:** removing the file in a new commit leaves it in history. Re-`init` (unpushed repo) or rewrite history so the blob never ships.

## DOI workflow (ordering is load-bearing)
1. Finish repo, README, LICENSE, CITATION.cff. 2. On Zenodo → GitHub settings, **flip the repo toggle ON FIRST** (releases created before this are NOT archived). 3. Cut a GitHub release (`v1.0.0`). 4. Zenodo mints **two** DOIs — cite the **concept DOI** (all-versions) in the manuscript, never the version DOI, so later releases don't break the citation. Add the DOI badge to the README.

## CITATION.cff
Add `cff-version: 1.2.0`, the software `authors` (with ORCIDs), `version`, top-level `doi:` (the Zenodo concept DOI), and a `preferred-citation:` block for the article itself. Enables GitHub's "Cite this repository" and keeps Zenodo metadata in sync. **Validate it parses** (`yaml::read_yaml()`).

Copy-paste template (replace every `<...>` placeholder; do not ship placeholder values):
```yaml
cff-version: 1.2.0
message: "If you use this software or data, please cite both the software (below) and the article (preferred-citation)."
title: "<Project / compendium title>"
authors:
  - family-names: "<Family>"
    given-names: "<Given>"
    orcid: "https://orcid.org/<your-orcid>"
  - family-names: "<Family2>"
    given-names: "<Given2>"
    orcid: "https://orcid.org/<coauthor-orcid>"
version: 1.0.0
date-released: "2026-01-31"
doi: 10.5281/zenodo.<concept-doi>     # Zenodo CONCEPT (all-versions) DOI
repository-code: "https://github.com/<owner>/<repo>"
url: "https://github.com/<owner>/<repo>"
license: MIT
keywords:
  - reproducible-research
  - <topic-keyword>
  - <method-keyword>
preferred-citation:
  type: article
  authors:
    - family-names: "<Family>"
      given-names: "<Given>"
      orcid: "https://orcid.org/<your-orcid>"
  title: "<Article title as published>"
  journal: "<Journal name>"
  year: 2026
  doi: 10.<publisher-prefix>/<article-doi>
```

## .zenodo.json (archive metadata, alternative/supplement to CITATION.cff)
A `.zenodo.json` file at the repo root lets you control the deposited record's metadata directly, instead of relying only on the GitHub→Zenodo toggle's inference from CITATION.cff. Use it when you need precise control of creators, affiliations, license, or keywords on the archive. Minimal example (replace placeholders):
```json
{
  "title": "<Project / compendium title>",
  "upload_type": "software",
  "creators": [
    {
      "name": "<Family>, <Given>",
      "orcid": "<your-orcid>",
      "affiliation": "<Your institution>"
    },
    {
      "name": "<Family2>, <Given2>",
      "orcid": "<coauthor-orcid>",
      "affiliation": "<Coauthor institution>"
    }
  ],
  "license": "MIT",
  "keywords": ["reproducible-research", "<topic-keyword>", "<method-keyword>"]
}
```
Note: `.zenodo.json` overrides the metadata Zenodo would otherwise harvest. Keep its `title`, creators, and `license` consistent with CITATION.cff so the archive and the "Cite this repository" widget agree.

## License the code and the data separately
A compendium ships two different kinds of work that need two different licenses; a single software license does not cleanly cover data, and a data license does not cover code.
- **Code** (scripts, functions, notebooks): use a software license — **MIT** (permissive, simplest), **Apache-2.0** (permissive + explicit patent grant), or **GPL-3.0** (copyleft). Put it in `LICENSE` at the repo root.
- **Data** (shipped derived aggregates, lookups): use a data license — **CC-BY-4.0** (attribution required) or **CC0-1.0** (public-domain dedication, no attribution required). Put it in `LICENSE-data` (or a short `data/LICENSE` / note in the data README) and state in the top-level README which license governs which paths.
- **Why:** software licenses are written around copyright in source code and warranty disclaimers; Creative Commons licenses are written for content/datasets. Mixing them (e.g. MIT on a dataset, or CC-BY on code) creates ambiguity for reusers about what they may legally do. Naming both explicitly removes that ambiguity and satisfies journal "code and data availability" requirements.

## Resources
- The Turing Way — guide to reproducible, ethical, collaborative research: https://book.the-turing-way.org/
- rrtools — research-compendium structure/convention for R: https://github.com/benmarwick/rrtools
- Zenodo documentation (GitHub integration, DOIs, metadata): https://help.zenodo.org/
- Citation File Format (CITATION.cff) spec: https://citation-file-format.github.io/

## Manuscript pairing (Quarto)
- **Authors:** structured YAML — a top-level `affiliations:` list with `id`s, each author `- name:` with `orcid`, `email`, `corresponding: true`, and `affiliations: [{ref: …}]`. Reorder authorship by moving whole blocks.
- **Availability statement:** say what is shareable vs governed, give the repo URL + concept DOI.
- **Ethics statement:** institutional committee + approval/exemption number.
- **Preprint PDF:** add a `pdf:` format. If headings are manually numbered ("## 2. Methods"), set `number-sections: false` or you get double numbering. Set `geometry`, `fontsize`, `linestretch: 1.5`.

## Verify before you publish
- Syntax-check every reorganized script (`parse(file=...)`), don't assume a path-rewrite worked.
- Render the manuscript/supplement **from inside the repo** to confirm relative paths (`../out`, `../files`) resolve self-contained.
- Format tiny p-values in tables as `<0.001`, not `0.0e+00`.
- Quarto on Windows may grab the wrong R — set `$env:QUARTO_R` to the correct R before `quarto render`.

## Publishing handoff (you often can't push)
Creating/pushing to GitHub may be blocked (no `gh`, no token, MCP "Bad credentials"). Don't fake it. Build the repo locally, set the branch + remote, then hand the user ONE authenticated command (`git -C <repo> push -u origin main`) and the manual release/Zenodo-toggle steps. Verify after: `git ls-remote origin HEAD` == local HEAD.

## Common Mistakes
| Mistake | Reality |
|---|---|
| "Link to the source / fetch the big file" | Only works for unmodified public downloads. A pipeline-derived layer has no URL — simplify + verify instead. |
| Simplify by file size, ship it | Verify the analysis structure (contiguity graph, areas) is preserved first; non-topology `st_simplify` breaks adjacency. |
| `git rm` the big blob, commit | Blob stays in history and still ships. Rewrite history / re-init. |
| Trust the path-rewrite / merged scripts | Parse every script; render the paper from inside the repo. |
| Cite the version DOI | Cite the concept (all-versions) DOI. |
| Cut the release, then enable Zenodo | Toggle Zenodo ON before the release or it isn't archived. |
| "I'll just push it" | You likely can't authenticate. Set up locally, hand off one command, verify the remote HEAD. |

## Platform compatibility

- **Class:** Environment-dependent (needs a CLI/agent with a local shell)
- **Requires:** git, quarto, R.
- **Load it on:**
  - Claude: drop into `~/.claude/skills/` (Claude Code), or paste this body into a Project's instructions (claude.ai).
  - ChatGPT: paste this body into a Custom GPT or Project. Needs Codex/agent mode with a connected environment for the shell steps.
  - Gemini: create a Gem from this body, or place it under the Gemini CLI. Needs the Gemini CLI for the shell steps.
