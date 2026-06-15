---
name: publishing-research-compendium
description: >
  Use when packaging a finished analysis (code + data + manuscript) into a
  public, citable, reproducible repository and archiving it for a DOI — e.g.
  "set up a repo for this paper", "make this reproducible", "get a Zenodo DOI",
  "prepare for medRxiv/journal submission", "code and data availability". Covers
  repos with non-redistributable source data, large spatial/binary files,
  CITATION.cff, Zenodo, and Quarto manuscript front-matter.
---

# Publishing a Research Compendium

## Overview
Turn an analysis pipeline into a repository a stranger can clone and reproduce, and that a paper can cite with a stable DOI. **Core principle: ship the smallest self-contained thing that reproduces the results, and verify it actually does before you publish.**

The high-level workflow (provenance/derived split, Zenodo, concept vs version DOI, CITATION.cff) is mostly intuitive. This skill exists for the parts that are NOT, where capable people still go wrong (see Common Mistakes).

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
