---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 03-title-tab-agent
task: Create TitleTab.jsx — concept input only; posts { concept } to /api/pipeline/title.
description: "TitleTab: single concept textarea, posts { concept } to /api/pipeline/title, renders 07-Titles file via OutputBrowser."
tags: [phase5, title, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/DistributionTabs/TitleTab.jsx
verification:
  - No hook, research, outline, or URL fields
  - Request body is { concept }
  - Result renders 07-Titles file
  - No raw fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 03-TitleTab

## Self-Verification

- [x] UI: single `concept` textarea only — no hook, research, outline, or URL fields.
- [x] Body: `{ concept: concept.trim() }`.
- [x] `OutputBrowser result={jobResult}` renders `07-Titles` file on completion.
- [x] No raw `fetch` — uses `runStage('title', body)` from `api.js`.

## Open Items

None.
