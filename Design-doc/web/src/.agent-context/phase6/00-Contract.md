---
title: Phase 6 Contract Memo
type: agent-context
date: 2026-05-24
tags: [phase6, webapp, agent-context]
description: Shared contracts for Phase 6 execution — vault folder mappings, sidebar status rules, Brain payload keys, 409 handling, and jobActivity signals.
---

# Phase 6 Contract Memo

Related: [[2026-05-24_phase6-dashboard-brain-polish]]

## Dashboard Card → Vault Folder Mapping

| Card ID  | Vault Folder   | Activity display                          |
|----------|----------------|-------------------------------------------|
| trends   | 04-Trends      | filename + modified timestamp             |
| research | 10-Research    | filename + modified timestamp             |
| ideation | 02-Ideas       | filename + modified timestamp             |
| outline  | 06-Outlines    | filename + modified timestamp             |

- Source: `getRecent(folder, limit=3)` → `[{name, path, modified}]`
- `running` state comes from `jobActivity.js` (in-session only), NOT vault
- No `badge`, `score`, or `status` chip derivation from vault — show name + time only
- Hardcoded mock arrays in Dashboard.jsx are deleted entirely

## Sidebar Status Derivation Rules

| Stage       | Vault folder(s) checked          | Running signal   |
|-------------|----------------------------------|------------------|
| trends      | 04-Trends                        | jobActivity      |
| research    | 10-Research                      | jobActivity      |
| ideation    | 02-Ideas                         | jobActivity      |
| hooks       | 05-Hooks                         | jobActivity      |
| distribution| 06-Outlines (any output present) | jobActivity      |

- Priority: `running` > `done` > `idle`
- `done` = vault folder has ≥1 file
- `idle` = vault folder empty AND not running
- No polling — one-shot on mount (refresh happens on next page load)
- Footer health badge: `GET /api/health` → green dot if `status === "ok"`, red dot otherwise

## Brain Payload Keys (from `/api/brain/analyze` SSE → `done` event)

```json
{
  "hook_quality": "string",
  "structure_score": "string",
  "emotional_triggers": ["string"],
  "techniques_to_steal": ["string"],
  "replication_template": "string"
}
```

- Render exactly these 5 fields — no invented sections
- Fake 6-section structure in Brain.jsx is deleted entirely
- `runState` initial value must be `"idle"` (not `"done"`)
- No setTimeout fake analysis

## 409 Conflict Handling

- `api.js` exports `ConflictError` class with `.status = 409`
- `runStage`, `runBrainAnalysis` throw `ConflictError` on 409 response
- UI shows inline notice: "A job is already running — wait for it to finish"
- Does NOT show generic error toast for 409

## jobActivity.js Signals

- `announceStart(stageId)` — called when any job begins
- `announceDone(stageId)` — called on SSE `done` event
- `announceFail(stageId)` — called on SSE `error` or catch
- Backed by `Map` in module scope (not localStorage — session only)
- `subscribe(fn)` / `unsubscribe(fn)` for reactive listeners

## Phase 7 Out of Scope (do not implement)

- Vault write-back (auto-save skill output to vault)
- Notification toasts / push notifications
- Pagination on vault recency lists
- Persistent job history across sessions
- Any new routes or views
