---
title: Phase 6 API Agent — Memory Note
type: agent-context
date: 2026-05-24
tags: [phase6, webapp, api, agent-context]
description: What was done in Group 1a (api.js) and Group 1b (usePipelineSnapshot + jobActivity). Contracts for downstream agents.
---

# Group 1 — Completed

Related: [[2026-05-24_phase6-dashboard-brain-polish]] | [[00-Contract]]

## api.js changes

- Added `ConflictError` class (exported): `this.status = 409`
- `runStage` now throws `ConflictError` on 409 instead of plain Error
- Added `runBrainAnalysis(content)` → POST `/api/brain/analyze` → `{job_id}`; throws `ConflictError` on 409
- Added `getHealth()` → GET `/api/health` → `{status, backend, capabilities}`; returns `{status:"error"}` on failure

## jobActivity.js (new file — `src/jobActivity.js`)

- Module-scope `Set` for running stageIds, resets on page reload
- `announceStart(stageId)`, `announceDone(stageId)`, `announceFail(stageId)`
- `subscribe(fn)` returns unsubscribe fn; `isRunning(stageId)` for point checks

## usePipelineSnapshot.js (new file — `src/hooks/usePipelineSnapshot.js`)

- `usePipelineSnapshot()` → `{ recents, runningSet, sidebarStatuses }`
- `recents`: `{ trends, research, ideation, outline }` each `[{name,path,modified}]` (limit 3)
- `runningSet`: live Set from jobActivity subscribe
- `sidebarStatuses`: `{ trends, research, ideation, hooks, distribution }` each `"running"|"done"|"idle"`
  - `distribution` maps to `06-Outlines` folder presence

## Contracts for downstream agents

- Dashboard agent (03): import `usePipelineSnapshot`, use `recents[cardId]` for activity list
- Sidebar agent (04): import `usePipelineSnapshot`, use `sidebarStatuses[stageId]`
- Brain agent (05): import `runBrainAnalysis` from `../api.js`, `announceStart/Done/Fail` from `../jobActivity.js`
- RunFeedback agent (06): import `announceStart/Done/Fail` into StageWorkspace + Distribution tabs
