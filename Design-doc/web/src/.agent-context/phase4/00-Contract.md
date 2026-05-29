---
date: 2026-05-24
type: phase4-agent-note
status: done
agent: 00-contract-agent
task: Write Phase 4 contract memo — endpoint, folder, result mapping
description: "Canonical mapping of UI stage → endpoint → vault folder → result shape for Phase 4 wiring. Single source of truth for all parallel workers."
tags: [phase4, contract, webapp-sprint, frontend]
owned_files:
  - Design-doc/web/src/.agent-context/phase4/00-Contract.md
verification:
  - memo includes stage-to-endpoint table
  - memo includes stage-to-folder table
  - memo includes rule that only api.js may use fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# Phase 4 Contract Memo

## Mission
Establish the canonical mapping from UI stage → backend endpoint → vault folder → result shape,
so all parallel workers use identical assumptions.

## Stage → Endpoint

| UI stage    | Method | Endpoint                      | Body fields                          |
|-------------|--------|-------------------------------|--------------------------------------|
| `trends`    | —      | *(no POST; read-only)*        | —                                    |
| `research`  | POST   | `/api/pipeline/researcher`    | `{ niche, repos[], mode }`           |
| `ideation`  | POST   | `/api/pipeline/ideation`      | `{ topic, research_file }`           |
| `hooks`     | POST   | `/api/pipeline/hook`          | `{ topic, research_file }`           |

`title`, `outline`, `distribution`, `brain` are **out of scope for Phase 4** — do not wire them.

Notes:
- `research` endpoint is `/api/pipeline/researcher` (not `/api/pipeline/research`).
- `hooks` endpoint is `/api/pipeline/hook` (not `/api/pipeline/hooks`).
- All bodies are JSON; `Content-Type: application/json` required.
- Every POST returns `{ job_id: string }` immediately (non-blocking).

## Stage → Vault Folder

| UI stage    | Vault folder   | Role                                     |
|-------------|----------------|------------------------------------------|
| `trends`    | `04-Trends`    | read-only file load + history            |
| `research`  | `10-Research`  | output + VaultPicker source for ideation |
| `ideation`  | `02-Ideas`     | output + history                         |
| `hooks`     | `05-Hooks`     | output + history                         |

Trends file to load on mount: `04-Trends/github_trending.md`

## Job Lifecycle (SSE)

1. POST endpoint → returns `{ job_id }`
2. Connect `EventSource` to `GET /api/jobs/{job_id}/stream`
3. Events:
   - `{ type: "stdout", line }` — append to log
   - `{ type: "stderr", line }` — append to log
   - `{ type: "ping" }` — keepalive, ignore
   - `{ type: "done", result }` — job complete; close stream; store result
   - `{ type: "error", error }` — job failed; close stream; store error
4. On component unmount or jobId change: close EventSource

## Result Shape

```json
{
  "result_type": "file",
  "primary_path": "/abs/path/to/output.md",
  "outputs": ["/abs/path/to/output.md"],
  "data": null
}
```

Phase 4 wired stages produce `result_type: "file"`. `OutputBrowser` must handle this correctly.

## Vault API

| Operation           | Endpoint                              | Returns                              |
|---------------------|---------------------------------------|--------------------------------------|
| Recent files        | `GET /api/vault/recent?folder=X&limit=N` | `[{ name, path, modified }]`      |
| Read file content   | `GET /api/vault/file?path=X`          | `{ path, content }`                  |
| List bundle members | `GET /api/vault/outputs?path=X`       | `[{ name, path }]`                   |

## fetch Rule

**Only `Design-doc/web/src/api.js` may call `fetch`.**

All other components import and call the exported functions:
- `runStage(stage, body)` → `{ job_id }`
- `getRecent(folder, limit?)` → `[{ name, path, modified }]`
- `readVaultFile(path)` → `{ path, content }`
- `listOutputs(path)` → `[{ name, path }]`

## Self-Verification

- [x] Table includes `research → /api/pipeline/researcher`
- [x] Table includes `hooks → /api/pipeline/hook`
- [x] Trends is marked read-only with no POST
- [x] Phase 4 vault folders listed: `04-Trends`, `10-Research`, `02-Ideas`, `05-Hooks`
- [x] `title`, `outline`, `distribution`, `brain` explicitly out of scope
- [x] `fetch` rule stated

## Open Items

None.
