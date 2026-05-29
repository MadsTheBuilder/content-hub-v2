---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 02-outline-tab-agent
task: Create OutlineTab.jsx — topic, optional hook_path picker, length, platform; no research_file.
description: "OutlineTab: topic textarea, VaultPicker 05-Hooks, length number, platform select, posts to /api/pipeline/outline, renders 06-Outlines file via OutputBrowser."
tags: [phase5, outline, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/DistributionTabs/OutlineTab.jsx
verification:
  - Request body contains topic, hook_path, length, platform
  - No research_file field in UI or body
  - Result renders 06-Outlines file
  - No raw fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 02-OutlineTab

## Self-Verification

- [x] Body: `{ topic, hook_path, length, platform }` — no `research_file`.
- [x] `VaultPicker folder="05-Hooks"` for optional hook context.
- [x] `OutputBrowser result={jobResult}` renders `06-Outlines` file on completion.
- [x] No raw `fetch` — uses `runStage('outline', body)` from `api.js`.
- [x] Live SSE log lines shown during loading via `useJobStream`.

## Open Items

None.
