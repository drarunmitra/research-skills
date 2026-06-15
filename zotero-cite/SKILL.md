---
name: zotero-cite
version: 1.0.0
description: |
  Find/verify a reference, add it to a Zotero collection via the Zotero local
  API, export the collection to a BibTeX/BibLaTeX file, and cite it from a
  Quarto/R Markdown/LaTeX document with @citekey. Use when the user wants to
  "add this paper to Zotero and cite it", build a paper's bibliography in
  Zotero, keep a .bib in sync with a Zotero collection, or set up reproducible
  citing for a manuscript. Pairs with academic-writer's citation-check.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - WebSearch
  - WebFetch
---

# zotero-cite

Bridge Zotero and a Quarto/LaTeX manuscript: verify a reference, store it in a Zotero
collection (the user's library), export that collection to a `.bib`, and cite it with
`@citekey`. The Zotero collection is the source of truth; the `.bib` is a generated
artifact the document points at.

## IRON RULES
1. Never fabricate bibliographic detail. Verify authors/year/journal/volume/pages/DOI on
   the web (PubMed, Crossref, publisher, PMC) before adding. A DOI must resolve to the
   stated title. If a field can't be confirmed, leave it empty rather than guessing.
2. Never duplicate. Before adding, search the library for the DOI/title; skip if present.
3. Don't reorganise the user's existing library. Create or write only inside the named
   collection for this task.
4. Keep the `.bib` a generated file: regenerate it from Zotero, don't hand-edit it (hand
   edits are lost on the next export). If Better BibTeX is absent, see "Citation keys".

## Preconditions
- Zotero 7+ running. Probe: `curl -s -m5 http://127.0.0.1:23119/connector/ping` (HTTP 200).
- The **local API is READ-ONLY** on current builds: `GET http://127.0.0.1:23119/api/users/0/collections`
  lists collections and `GET .../collections/<key>/items?format=biblatex` exports, but `POST` to it
  returns "Endpoint does not support method". So use it to READ and EXPORT, not to write.
- **Writes** go through the **connector** server (same port) or the **Web API**:
  - `POST http://127.0.0.1:23119/connector/import` with `Content-Type: text/plain` and a BibTeX/RIS body
    creates items in the user's library (in the collection currently selected in the Zotero UI, else
    "My Library"). This is the simplest local write path. Current Zotero builds require an anti-CSRF
    header on connector writes: add `-H "Zotero-Allowed-Request: true"` or the import is rejected.
    A multi-entry BibTeX body imports all entries in one call (batch). Each entry's `keywords = {a, b}`
    field is imported as Zotero TAGS, so tagging needs no API key, put the tags in the bib.
  - `POST .../connector/saveItems` with Zotero-JSON also works but needs a session.
  - For programmatic collection creation + precise placement, use the **Web API** `https://api.zotero.org`
    with an API key (`POST /users/<id>/collections`, then `POST /users/<id>/items` with the collection key).
    Ask the user for an API key if collection control is required headlessly.
- Better BibTeX (BBT) gives stable pinned keys + auto-export; detect with
  `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:23119/better-bibtex/cayw?probe=probe` (200 = present).
  If absent (404), export via the native local API (`format=biblatex`); keys are Zotero-generated (see
  "Citation keys"), or keep a hand-keyed `.bib` as the document bibliography and mirror items into Zotero.

## Workflow

### 1. Verify (always)
For each reference, confirm it exists and collect full metadata + DOI (use WebSearch /
WebFetch; resolve PMCID/PMID/DOI). Run academic-writer's citation-check discipline. Mark
anything unconfirmable and ask before adding.

### 2. Make the collection and add items
The local API cannot write, so use one of:

- **Local (connector/import)** — simplest, no API key. For collection placement, have the user create the
  target collection in the Zotero UI and click it (so it is the selected collection), then import the
  verified BibTeX:
  ```
  curl -s -X POST "http://127.0.0.1:23119/connector/import" \
    -H "Content-Type: text/plain" -H "Zotero-Allowed-Request: true" --data-binary @verified.bib
  ```
  The `Zotero-Allowed-Request: true` header is REQUIRED on current builds. Items land in the selected
  collection (else My Library); collection placement is by UI selection, not controllable from the request.
  Then proceed to step 4 to export the canonical `.bib`.
- **Web API** — full control, needs an API key. Create the collection, capture its key, then post items:
  ```
  curl -s -X POST "https://api.zotero.org/users/<ID>/collections" -H "Zotero-API-Key: <KEY>" \
    -H "Content-Type: application/json" -d '[{"name":"<NAME>"}]'        # -> successful.0.key
  curl -s "https://api.zotero.org/items/new?itemType=journalArticle"    # template
  # fill creators[], title, publicationTitle, volume, issue, pages, date, DOI, url, "collections":["<KEY>"]
  curl -s -X POST "https://api.zotero.org/users/<ID>/items" -H "Zotero-API-Key: <KEY>" \
    -H "Content-Type: application/json" -d '[<filled item json>]'
  ```
  creators use `{"creatorType":"author","firstName":"...","lastName":"..."}`; check `successful`/`failed`.

### 3. Tags and batch-loading a found reference set (e.g. a deep-research output)
When the task is to load a *set* of found/verified references into the library so the user can manage
them later, tags are the robust mechanism (no API key, survives whether or not a collection is used):

1. Verify every reference (step 1). Drop or flag anything unconfirmable; never import a guessed DOI.
2. Build ONE multi-entry `.bib`. Give every entry a `keywords` field with a shared project tag plus a
   per-theme tag, e.g. `keywords = {TB-notif-seasonality, tb-seasonality}`. Comma-separated keywords
   become separate Zotero tags. Use BBT-style stable keys if BBT is present.
3. (Optional collection) If the user wants a collection, either: they create it in the Zotero UI and
   select it before import; or they supply a Web API key and you create it (step 2, Web API) and post
   items with `"collections":["<KEY>"]`. If neither, rely on the tags alone, the user can drag the
   tagged set into a collection later.
4. Import the whole file in one connector call (with the `Zotero-Allowed-Request: true` header above).
5. Confirm: re-query the local API and count items carrying the project tag
   (`GET /api/users/<LIBID>/items/top?tag=<projecttag>&format=json&limit=100`), and report added vs
   skipped-duplicate vs failed-to-verify.

Dedup first (IRON RULE 2): for each candidate, `GET /api/users/<LIBID>/items?q=<DOI or title>` and skip
if already present, so re-running the load does not create duplicates.

### 4. Export the collection to .bib
```
curl -s "http://127.0.0.1:23119/api/users/<LIBID>/collections/<COLLKEY>/items?format=biblatex&limit=100" \
  -o references.bib
```
(BBT alternative: `http://127.0.0.1:23119/better-bibtex/export/collection?/<libid>/<collkey>.biblatex`,
which gives clean BBT keys and can auto-update.)

### 5. Cite in the document
- Quarto/R Markdown: set `bibliography: references.bib` in the YAML; cite with `@key`,
  `[@key]`, `[@a; @b]`. Render to confirm every `@key` resolves (no "?@key").
- LaTeX: `\addbibresource{references.bib}` (biblatex) and `\autocite{key}`.

## Citation keys
- With BBT: keys are stable (`shewade_trends_2022`); cite those directly.
- Without BBT: the native biblatex export assigns keys; after step 4, read the exported
  keys and either (a) cite those, or (b) if the document already uses chosen keys, keep a
  hand-maintained `references.bib` with those keys as the document's bibliography AND mirror
  the items into Zotero for the user's library (the two are kept consistent by you, not by
  auto-export). State which mode is in use. Recommend installing BBT for the (a) workflow.

## Notes
- The local API mirrors the Zotero Web API schema (write support added in Zotero 7); the
  same JSON works against api.zotear.org with an API key for headless/cloud runs.
- Attachments/PDFs: add via the connector (`/connector/saveItems`) or manually; metadata
  alone is enough for citing.
- Always render the document after wiring citations and report any unresolved `@key`.

## Version history
- 1.1.0 (2026-06-11): Added the `Zotero-Allowed-Request: true` header (required on current connector
  builds) to all connector/import examples; added tagging via the BibTeX `keywords` field (maps to Zotero
  tags, no API key needed); added section 3 "Tags and batch-loading a found reference set" (the
  deep-research -> Zotero flow: verify -> tagged multi-entry .bib -> one batch import -> dedup + count
  confirmation). Prompted by loading a verified literature-review set into the library with per-theme tags.
- 1.0.0 (2026-06-10): Initial release. Local-API workflow (verify → collection → item →
  biblatex export → cite), BBT detection, citation-key guidance, integrity rules.
