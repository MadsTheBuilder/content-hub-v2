---
date: 2026-05-24
type: phase5-agent-note
status: done
agent: 08-app-routing-agent
task: Wire App.jsx to DistributionWorkspace; remove standalone title and outline routes.
description: "App.jsx: imports DistributionWorkspace, mounts it for view=distribution, removed standalone title/outline StageWorkspace routes and their TweakSelect jump-list entries."
tags: [phase5, app-routing, distribution, webapp-sprint]
owned_files:
  - Design-doc/web/src/App.jsx
verification:
  - App.jsx no longer routes title or outline as separate screens
  - distribution loads DistributionWorkspace
  - No Phase 4 routes regress
  - No raw fetch
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 08-AppRouting

## Self-Verification

- [x] `import DistributionWorkspace from './DistributionWorkspace.jsx'` added.
- [x] `view === "distribution"` renders `<DistributionWorkspace onBack={() => navigate("dashboard")} />`.
- [x] Standalone `title` (`StageWorkspace stageId="title"`) removed — no longer a route.
- [x] Standalone `outline` (`StageWorkspace stageId="outline"`) removed — no longer a route.
- [x] Fake `initialState` seeds (`runState: "done"`) tied to old title/outline screens removed.
- [x] `TweakSelect` jump-list entries for `title` and `outline` removed.
- [x] `accents` map entries for `title` and `outline` removed.
- [x] `dashboard`, `trends`, `research`, `ideation`, `hooks`, `brain`, `settings` routes intact.
- [x] Build ✅ (193 modules).

## Open Items

None.
