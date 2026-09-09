---
date: 2026-06-01
tags: [session, plan-review, obsidian, wikilinks, open-notebook, researcher]
description: "Verified the Obsidian WikiLinks knowledge-base plan against the YouTube transcript, local open-notebook API schema, and researcher code."
---

# Obsidian Wiki Plan Verification

Implements: [[Knowledge Wiki Plan Verification]]
References: [[researcher.py]], [[open_notebook_client.py]], [[open_notebook_seed.py]], [[Local_First_Skill_Engine_Plan]], [[Current_Sprint]], [[2026-06-01_OpenNotebook-Docker-Setup]], [[2026-06-01_CloakBrowser-Research-Notebook-Audit]]
Modifies: [[Sessions]], [[Current_Sprint]]

## Summary

Verified the pasted plan for using an [[Obsidian]] + [[WikiLinks]] knowledge base as a pre-cached web/context layer for the [[researcher]] pipeline.

Used `yt-dlp` via the project `.venv` to fetch captions for `https://www.youtube.com/watch?v=OSZdFnQmgRw`. The transcript confirms the plan's main reading of the video:

- raw sources are staged in a raw folder before wiki synthesis
- generated wiki folders sit under a central wiki directory
- a master index lists sub-wikis
- each sub-wiki has its own index
- Claude Code navigates master index -> topic index -> relevant article
- the system is intentionally not vector RAG and is recommended for solo/small-team scale before moving to true RAG

## Findings

The plan is directionally correct and fits [[Content Hub V2]] well.

Key correction: Path A is not merely hypothetical. The live [[open-notebook]] OpenAPI schema at `http://localhost:5055/openapi.json` exposes `/api/sources/json` with `SourceCreate` fields for `type: text`, `content`, `title`, `notebook_id`, `notebooks`, `embed`, and `async_processing`. That means vault wiki markdown can be added as raw text sources; [[open_notebook_client.py]] only lacks the helper method today.

The current [[open_notebook_client.py]] implements only link sources (`type: link`). [[researcher.py]] therefore still adds only GitHub URL, README raw URL, and discovered primary docs in the open-notebook path. The plan's proposed wiki context injection is not yet implemented.

The cleaner first implementation is still Path B / hybrid: build the vault wiki first, retrieve relevant wiki articles through markdown indexes, inject the selected article text into [[RepoContext]] or the research prompt, and optionally add those same articles to open-notebook as `type: text` sources once `add_text_source()` exists.

## Caveats

- The pasted plan names `skills/open_notebook_seed.py`, but the actual file is `skills/helpers/open_notebook_seed.py`.
- The video emphasizes `raw/` as a human staging area, but also says Claude Code can research and create wiki articles directly. So treating `04-Trends/` as raw input is acceptable, but a dedicated `01-Knowledge/raw/` may still be useful for web clips and source provenance.
- The repo currently has recurring [[researcher.py]] reliability issues from recent audits: context extraction timeouts, seed JSON parse failures, and Claude subprocess contract drift. Wiki context will improve depth, but it will not by itself fix those execution bugs.

## Recommended Next Slice

Create a small `/wiki-gen` vertical slice:

1. Generate `Content-Hub-Vault-V2/01-Knowledge/wiki/_index.md`.
2. Generate one topic folder with `_index.md` and 2-3 wiki articles from existing `04-Trends/` files.
3. Add a `find_relevant_wiki_articles(query)` helper that reads master index first, then topic index, then selected articles.
4. Add `OpenNotebookClient.add_text_source()` using `/api/sources/json`.
5. Wire selected wiki article text into the open-notebook [[researcher.py]] path before question seeding.

## Files Touched

- `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-06-01_Obsidian-Wiki-Plan-Verification.md`
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`

Temporary verification artifacts were written under `.tmp/` during the review and then removed.
