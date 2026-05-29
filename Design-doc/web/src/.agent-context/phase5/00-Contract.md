---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 00-contract-agent
task: Write Phase 5 contract memo so all workers share the same tab order, endpoint mapping, hash routing, folder rules, and out-of-scope boundaries.
description: "Shared contract for Phase 5 Distribution multi-tab: tab order, endpoint mapping, hash routing, picker sources, vault folders, api.js rule, and Phase 6 boundaries."
tags: [phase5, contract, webapp-sprint, distribution]
owned_files:
  - Design-doc/web/src/.agent-context/phase5/00-Contract.md
verification:
  - Memo includes tab-to-endpoint table
  - Memo includes picker/folder table
  - Memo includes Phase 6 out-of-scope rule
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 00-Contract — Phase 5 Distribution Multi-Tab

## Mission

Establish the shared contract all Phase 5 workers must follow. Workers read this memo before touching any file.

## Context Read

Read: `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/StageWorkspace.jsx`.

## Contract

### Tab Order (fixed, do not deviate)

```
outline → title → cascade → short-form → voice-cleanup
```

### URL Hash Format

```
#distribution/<tab>
```

Valid tab slugs: `outline`, `title`, `cascade`, `short-form`, `voice-cleanup`.

Invalid or missing hash → fall back to `outline`.

Tab choice persists across navigation and page refresh (hash stays in URL).

### Tab → Endpoint Table

| Tab | Endpoint | HTTP method |
|---|---|---|
| `outline` | `/api/pipeline/outline` | POST |
| `title` | `/api/pipeline/title` | POST |
| `cascade` | `/api/pipeline/cascade` | POST |
| `short-form` | `/api/pipeline/short-form` | POST |
| `voice-cleanup` | `/api/pipeline/voice-cleanup` | POST |

### Request Body Shapes

| Tab | Body fields |
|---|---|
| `outline` | `{ topic, hook_path, length, platform }` — **no `research_file`** (locked decision #5) |
| `title` | `{ concept }` |
| `cascade` | `{ research_file, outline_file }` OR `{ youtube_url }` |
| `short-form` | `{ research_file, outline_file }` OR `{ youtube_url }` |
| `voice-cleanup` | `{ file_path, inplace }` |

### Vault Output Folders

| Tab | Vault folder | result_type |
|---|---|---|
| `outline` | `06-Outlines` | `file` |
| `title` | `07-Titles` | `file` |
| `cascade` | `08-Distribution` | `bundle` |
| `short-form` | `09-Shorts` | `bundle` |
| `voice-cleanup` | original path or `_cleaned` sibling | `file` |

### Picker Sources

| UI surface | Source folder(s) |
|---|---|
| Outline — hook picker (optional) | `05-Hooks` |
| Cascade — research picker | `10-Research` |
| Cascade — outline picker | `06-Outlines` |
| Short-form — research picker | `10-Research` |
| Short-form — outline picker | `06-Outlines` |
| Voice-cleanup — file picker | `02-Ideas`, `05-Hooks`, `06-Outlines`, `07-Titles`, `08-Distribution`, `09-Shorts`, `10-Research` |

### Result Contract

- `outline`, `title`, `voice-cleanup` → `result_type: "file"` → `OutputBrowser` renders a single markdown file.
- `cascade`, `short-form` → `result_type: "bundle"` → `OutputBrowser` opens `primary_path` by default; all bundle members are selectable.
- API shapes: `GET /api/vault/file` → `{path, content}` · `GET /api/vault/outputs` → `[{name, path}]` · `GET /api/vault/recent` → `[{name, path, modified}]`.

### Sidebar Nav Collapse

- Remove top-level `title` and `outline` entries from `PIPELINE` in `Sidebar.jsx`.
- `distribution` remains as the single top-level entry for all five skills.
- Order for earlier stages: `trends → research → ideation → hooks → distribution`.

### App Routing Changes

- Mount `<DistributionWorkspace />` for `view === "distribution"`.
- Remove standalone `title` and `outline` routes from `App.jsx`.
- Remove `TweakSelect` jump-list entries for `title` and `outline`.
- Remove the fake `initialState` seeds (`runState: "done"`) tied to the old Title and Outline standalone screens.
- Keep: `dashboard`, `trends`, `research`, `ideation`, `hooks`, `distribution`, `brain`, `settings`.

### api.js Extension

- Add `outline`, `title`, `cascade`, `short-form`, `voice-cleanup` to `STAGE_ENDPOINTS`.
- No other file may call `fetch` directly.

### Phase 6 Out-of-Scope (do not pull in)

- Dashboard recent-activity wiring from real vault.
- Sidebar status dots from real job state.
- Brain wiring.
- Health badge.
- TweaksPanel `localStorage` persistence.
- 409 toast / graceful UX polish.
- Any change to `skills/*.py` or `prompts/*.md`.

## Changes Made

Wrote this contract memo only. No source files touched.

## Self-Verification

- [x] Tab-to-endpoint table present and covers all 5 tabs.
- [x] Picker/folder table present and covers all picker surfaces.
- [x] Phase 6 out-of-scope list is explicit.
- [x] No `research_file` on Outline — locked decision #5 captured.
- [x] `fetch` rule stated: only `api.js` may call `fetch`.

## Open Items

None.
