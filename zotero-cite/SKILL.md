---
name: zotero-cite
version: 1.4.0
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

## Pairs with

This skill acquires, verifies, persists a reference and exports the `.bib`; pair it with:
- **academic-writer** -- bidirectional and complementary: zotero-cite acquires/verifies/persists references and exports the `.bib`; academic-writer audits an existing manuscript's citations and style-converts them. (zotero-cite manages, academic-writer audits.)
- **research-writer** -- cite while drafting, resolving its `[CITE NEEDED]` placeholders into `@citekey`s.
- **reproducible-repo** -- supply the repo's reproducible `.bib`.
- **any deep-research / multi-source tool** -- batch-import a found reference set (the section-3 flow below).

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
- Zotero 7+ running, for the local API and connector steps. (Step 3b, zotcurate, does not need it running.) Probe: `curl -s -m5 http://127.0.0.1:23119/connector/ping` (HTTP 200).
- If Zotero is not running, open it yourself before you do anything else. Try twice. Do this only while doing a Zotero task the user asked for in this session. It is the user's own installed program: do not launch it for any other reason.
  0. First check for an existing process (Windows: `tasklist /FI "IMAGENAME eq zotero.exe"`; macOS and Linux: `pgrep -i zotero`). If one is running but the ping fails, do not start another: wait 10 s and probe again with `curl`.
  1. Find the program: `C:\Program Files\Zotero\zotero.exe`, else `%LOCALAPPDATA%\Zotero\zotero.exe`
     (Windows); `open -a Zotero` (macOS); `zotero` on PATH (Linux).
  2. Start it detached (Windows PowerShell: `Start-Process "<path>"`), then poll the ping with `curl` (not
     `Invoke-WebRequest`) every 5 s for up to 60 s.
  3. If the ping is still not 200 and no Zotero process exists, launch it a second time in the same way and poll again.
  4. Only after two failed launches, fall back to the checked-`.bib` approach: verify, write a
     hand-keyed `.bib`, and import later. Tell the user that Zotero did not start and that the
     import is still to do.
- Use the **local API** to READ and EXPORT: `GET http://127.0.0.1:23119/api/users/0/collections`
  lists collections and `GET .../collections/<key>/items?format=biblatex` exports. Zotero 7+ adds
  local-API write support, but on older builds a `POST` to the local API returns "Endpoint does not
  support method", so the **connector import endpoint is the documented default write path** here.
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
For each reference, confirm it exists and collect full metadata + DOI (search the web /
fetch the page; resolve PMCID/PMID/DOI). Run academic-writer's citation-check discipline. Mark
anything unconfirmable and ask before adding.

### 2. Make the collection and add items
The local API cannot write, so use one of:

- **Local (connector/import):** simplest, no API key. For collection placement, have the user create the
  target collection in the Zotero UI and click it (so it is the selected collection), then import the
  verified BibTeX:
  ```
  curl -s -X POST "http://127.0.0.1:23119/connector/import" \
    -H "Content-Type: text/plain" -H "Zotero-Allowed-Request: true" --data-binary @verified.bib
  ```
  The `Zotero-Allowed-Request: true` header is REQUIRED on current builds. Items land in the selected
  collection (else My Library); collection placement is by UI selection, not controllable from the request.
  Then proceed to step 4 to export the canonical `.bib`.
- **Web API:** full control, needs an API key. Create the collection, capture its key, then post items:
  ```
  curl -s -X POST "https://api.zotero.org/users/<ID>/collections" -H "Zotero-API-Key: <KEY>" \
    -H "Content-Type: application/json" -d '[{"name":"<NAME>"}]'        # -> successful.0.key
  curl -s "https://api.zotero.org/items/new?itemType=journalArticle"    # template
  # fill creators[], title, publicationTitle, volume, issue, pages, date, DOI, url, "collections":["<KEY>"]
  curl -s -X POST "https://api.zotero.org/users/<ID>/items" -H "Zotero-API-Key: <KEY>" \
    -H "Content-Type: application/json" -d '[<filled item json>]'
  ```
  creators use `{"creatorType":"author","firstName":"...","lastName":"..."}`; check `successful`/`failed`.

### 3. Tags and batch-loading a found reference set (e.g. output from any deep-research / multi-source tool)
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
4. Dedup first (IRON RULE 2): for each candidate, `GET /api/users/<LIBID>/items?q=<DOI or title>` and skip
   if already present, so re-running the load does not create duplicates.
5. Import the whole file in one connector call (with the `Zotero-Allowed-Request: true` header above).
6. Confirm: re-query the local API and count items carrying the project tag
   (`GET /api/users/<LIBID>/items/top?tag=<projecttag>&format=json&limit=100`), and report added vs
   skipped-duplicate vs failed-to-verify.

### 3b. Put items into the right collection with zotcurate (preferred when installed)
The connector import cannot choose a collection, and existing items you dedup against (IRON RULE 2)
stay wherever they already are. zotcurate (`zotc`, https://github.com/jeetsukumaran/zotcurate)
closes both gaps: it reads citation keys from the manuscript itself and makes a Zotero collection
match them, so the user never has to create or click a collection.

What it is and is not:
- It manages collections only. It creates collections (slash paths make parents, e.g.
  `"NFHS/Paper 3"`), adds items, replaces or diffs a collection's contents. It cannot create items,
  tags, notes or metadata. New references still go in via `/connector/import` first (step 2).
- It reads the Better BibTeX SQLite database directly (key -> item key) and writes through the
  Zotero Web API. Zotero does not have to be running, but it needs a Web API key (never
  auto-detected) in `~/.zotc/api-key` or `-k`. Ask the user for the key once; do not invent one.
- Because it writes through the Web API, items just imported locally must first sync to
  zotero.org before `zotc` can see them. BBT also writes its SQLite file with a delay. If `zotc`
  reports unresolved keys right after an import, wait for sync and rerun; do not work around it.
- Every modifying command is a dry run unless you pass `--execute`. Always run it once without
  `--execute`, read the plan, then run it again with `--execute`.

Setup (once; needs Python 3.10+). Ask the user before you install anything or write the API key. Never print the key in output or logs.
```
git clone https://github.com/jeetsukumaran/zotcurate && cd zotcurate && pipx install .
mkdir -p ~/.zotc && echo "<API key from zotero.org/settings/keys>" > ~/.zotc/api-key
zotc config                      # shows the resolved library ID, BBT database and key source
```

The manuscript-to-collection flow:
```
zotc keys extract --keys-only paper.qmd              # every @key the draft cites (no DB, no API)
zotc keys extract paper.qmd                          # resolves keys via BBT; exit code 2 = some unresolved
zotc collection diff   "Project/Paper" paper.qmd     # read-only: what replace would change
zotc collection create "Project/Paper" paper.qmd --on-conflict add            # dry run
zotc collection create "Project/Paper" paper.qmd --on-conflict add --execute  # do it
zotc collection replace "Project/Paper" paper.qmd --execute   # later: keep the collection in step with the draft
```
Use `keys extract` as the quick check that every citation in the draft exists in the library
(unresolved key = a reference that still has to be verified and imported). Prefer `add` over
`replace` unless the user asks for the collection to mirror the draft exactly, because `replace`
removes items the draft no longer cites.

If `zotc` is not installed or there is no API key, fall back to the manual step: the user creates and
selects the collection in the Zotero UI before the connector import, and drags any pre-existing items
into it. Tell the user which items those are.

### 4. Export the collection to .bib
```
curl -s "http://127.0.0.1:23119/api/users/<LIBID>/collections/<COLLKEY>/items?format=biblatex&limit=100" \
  -o references.bib
```
(BBT alternative: `http://127.0.0.1:23119/better-bibtex/export/collection?/<libid>/<collname>.biblatex`,
which gives clean BBT keys and can auto-update. Note: `<collname>` is the BBT collection slug, not the
API collection key.)

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

## Troubleshooting writes

`{"error":"SESSION_EXISTS"}` with HTTP 409 on `/connector/import`. The
connector believes an import session is already open. Retrying is useless -- it
returns 409 every time, and no amount of changing the payload, headers, or file
path helps. The fix is for the user to restart Zotero. You cannot do it for
them, so say so plainly and continue with the rest of the task; a `.bib` you have
already written is a complete artifact and the library sync can happen after.
Re-probe with `curl -s -m5 http://127.0.0.1:23119/connector/ping` (200 means the
server is up, which it will be even while writes are refused -- ping does not
detect this state). After the restart the same request returns HTTP 201 with
a JSON array of the created items; count that array and report added vs skipped.

Ping returns 200 but writes still fail. Local API *reads* and connector
*writes* are different code paths on the same port. A healthy ping tells you
nothing about write availability. Only an actual import call does.

Ping fails in PowerShell but Zotero is up. `Invoke-WebRequest` against port 23119 can fail
with "The underlying connection was closed" even when Zotero is listening. Probe with `curl` (or
`curl.exe`) before deciding that Zotero is down, or you will launch it again for nothing.

Exporting exactly the cited keys. When some cited items live outside the paper's collection
(pre-existing items), export by key instead of by collection, via the BBT JSON-RPC endpoint:
`POST http://127.0.0.1:23119/better-bibtex/json-rpc` with
`{"jsonrpc":"2.0","method":"item.export","params":[["key1","key2"],"Better BibLaTeX"],"id":1}`.
`item.citationkey` with `["1:<ITEMKEY>", ...]` returns the BBT key for items you just imported.

`@references.bib` in PowerShell. `@` is the splatting operator and will
throw a parse error. Use `curl.exe` and quote the argument:
`curl.exe ... --data-binary "@references.bib"`.

Duplicate keys after appending. If you append verified entries to an existing
`.bib`, check for keys already present *before* the append, not after -- a
duplicated key is silently accepted by BibTeX and then resolved unpredictably.
Parse the keys, diff, and drop the later copy.

## Notes
- The local API mirrors the Zotero Web API schema; the same JSON works against api.zotero.org
  with an API key for headless/cloud runs.
- Attachments/PDFs: add via the connector (`/connector/saveItems`) or manually; metadata
  alone is enough for citing.
- Always render the document after wiring citations and report any unresolved `@key`.

## Platform compatibility

- **Class:** Environment-dependent (needs a CLI/agent with a local shell)
- **Requires:** a local shell, plus Zotero running with Better BibTeX (local API on port 23119).
- **Load it on:**
  - Claude: drop into `~/.claude/skills/` (Claude Code), or paste this body into a Project's instructions (claude.ai).
  - ChatGPT: paste this body into a Custom GPT or Project. Needs Codex/agent mode with a connected environment for the shell steps.
  - Gemini: create a Gem from this body, or place it under the Gemini CLI. Needs the Gemini CLI for the shell steps.

## Version history
- 1.4.0 (2026-09-19): Added step 3b, zotcurate (`zotc`) for creating collections and placing
  items (including pre-existing ones) from the manuscript's own citation keys, with its limits
  (collections only, Web API key, sync lag, dry run by default). Added troubleshooting for the
  PowerShell ping false negative and for exporting exactly the cited keys through BBT JSON-RPC.
  Added after a session needed the user to create a collection by hand. This entry also
  rolls up the 1.2.0 and 1.3.0 changes below.
- 1.3.0 (2026-09-19): If Zotero is not running, launch it (two attempts, polling the ping up to
  60 s each) before falling back to the checked-`.bib` approach. Added after a
  session fell back to the `.bib` without trying to open Zotero.
- 1.2.0 (2026-08-28): Added "Troubleshooting writes": the `SESSION_EXISTS` / HTTP
  409 state on `/connector/import` (only a Zotero restart clears it; retrying and
  a healthy `ping` are both misleading), the PowerShell `@file` splatting error,
  and the duplicate-key check when appending to an existing `.bib`. Prompted by
  losing several tool calls to 409 twice in one session.
- 1.1.0 (2026-06-11): Added the `Zotero-Allowed-Request: true` header (required on current connector
  builds) to all connector/import examples; added tagging via the BibTeX `keywords` field (maps to Zotero
  tags, no API key needed); added section 3 "Tags and batch-loading a found reference set" (the
  deep-research / multi-source tool -> Zotero flow: verify -> tagged multi-entry .bib -> one batch import -> dedup + count
  confirmation). Prompted by loading a verified literature-review set into the library with per-theme tags.
- 1.0.0 (2026-06-10): Initial release. Local-API workflow (verify → collection → item →
  biblatex export → cite), BBT detection, citation-key guidance, integrity rules.
