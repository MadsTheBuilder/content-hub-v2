---
status: Active
sprint: "Webapp Sprint"
created: "2026-05-22"
date: "2026-05-22"
type: sprint_plan
description: "Mini-phase task breakdown for wiring the Design-doc React prototype into a fully working Vite+React frontend + FastAPI subprocess orchestrator for the 8 pipeline skills."
implements: "[[Design_Doc_Web_App_Plan]]"
references:
  - "[[Local_First_Skill_Engine_Plan]]"
  - "[[Current_Sprint]]"
  - "[[researcher]]"
  - "[[ideation]]"
  - "[[hook]]"
  - "[[outline]]"
  - "[[title]]"
  - "[[cascade]]"
  - "[[short-form]]"
  - "[[voice-cleanup]]"
tags:
  - sprint
  - web-app
  - vite
  - react
  - fastapi
  - tasks
---

# Webapp Sprint - Design-doc Wiring

> Source of truth: [[Design_Doc_Web_App_Plan]] (`00-Management-V2/Plans/Design_Doc_Web_App_Plan.md`).
> All phases, contracts, and locked decisions come from that document. Do not re-litigate them here.

**Status legend:** `[ ]` not started - `[~]` in progress - `[x]` complete - `[!]` blocked

**Total estimate:** 14-19 hours of focused work across 7 phases.

---

## Status Overview

| # | Phase | Est. | Status |
|---|-------|------|--------|
| 1 | Scaffold - Vite + server skeleton boots | 1-2h | [~] pending browser verify |
| 2 | Backend - FastAPI subprocess orchestrator | 3-4h | [~] implemented; 2.14 verify follow-up remains |
| 3 | Frontend port - CDN React -> Vite | 2-3h | [x] complete |
| 4 | Wire 5 sidebar stages (Trends + 4 skills) | 3-4h | [x] complete |
| 5 | Distribution multi-tab (5 skills) | 2-3h | [x] complete |
| 6 | Dashboard + Brain + polish | 2-3h | [x] complete |
| 7 | Launch convenience + E2E acceptance | 30m | [~] README shipped; launcher + E2E pending |

---

## Phase 1 - Scaffold (1-2h)

**Goal:** Both servers boot, particle background renders, no wiring yet.

- [x] **1.1 Directory init** - `cd Design-doc && mkdir web server`
- [x] **1.2 Vite project** - `cd web && npm create vite@latest . -- --template react`
- [x] **1.3 Frontend deps** - `npm i react-markdown clsx`
- [x] **1.4 Python runtime check** - Shared repo `.venv` confirmed as the locked runtime (Python 3.12.10). Documented in `Design-doc/server/runtime.md`.
- [x] **1.5 Add backend deps to root requirements.txt** - Added `# Design-doc web wrapper` comment + `aiofiles==24.1.0`, then reconciled the shared-runtime pins so the same `.venv` can boot both FastAPI and Streamlit cleanly (`fastapi==0.136.1`, `starlette==1.0.0`). Installed/synced wrapper deps in the shared `.venv`.
- [x] **1.6 Copy reference assets** - `styles.css`, `particles.js`, `Icons.jsx` copied to `web/src/`. `Icons.jsx`: `window.Icon = Icon` -> `export default Icon`. Re-synced 2026-05-22 after prototype updates: `styles.css` refreshed, `Icons.jsx` gained `Type`, `ListTree`, and `Rocket`, and `SourcesPanel.jsx` was ported. See [[2026-05-22_Webapp_Phase1_Resync]].
- [~] **1.7 Boot test** - Both servers boot (FastAPI 200, Vite 200). Vite proxy `/api -> :8765` wired in `vite.config.js`. Pending: user browser verify that particles animate and there are no console errors.

**Verify:** Both servers up simultaneously, particles animate, no console errors.

---

## Phase 2 - Backend (3-4h)

**Goal:** Every pipeline endpoint runs its skill subprocess, streams logs over SSE, returns typed `{result_type, primary_path, outputs[]}`.

### 2A - FastAPI shell
- [x] **2.1 `server/main.py`** - Full router shipped: CORS + `/api/health` + `/api/vault/*` + `/api/jobs/*` + `/api/pipeline/*` + `/api/brain/*`.
- [x] **2.2 `/api/health`** - Returns `{status:"ok", backend:"up", capabilities:null}` (minimum v1 contract). Shipped in `Design-doc/server/main.py`.

### 2B - Job runtime
- [x] **2.3 `server/jobs.py`** - In-memory job registry shipped with per-job `asyncio.Queue` fan-out plus typed `result` metadata.
- [x] **2.4 Single-job constraint** - Second POST while a job is running returns `409 Conflict`; Brain shares the same slot.
- [x] **2.5 `GET /api/jobs/{id}`** - Metadata snapshot endpoint shipped in `server/main.py`.
- [x] **2.6 `GET /api/jobs/{id}/stream`** - SSE stream shipped with `stdout`/`stderr`/`ping`/`done`/`error` events.

### 2C - Pipeline wrappers (8 skills, exact CLI passthrough)
- [x] **2.7 `server/pipeline.py` - one function per skill** building argv via `[sys.executable, "-m", "skills.<name>", ...]`, spawned with `asyncio.create_subprocess_exec` and `cwd=PROJECT_ROOT`. **Reuse skills as-is; no skill code changes** per [[CLAUDE]] section 3.
  - [x] 2.7.1 `run_researcher(niche, repos, mode)`
  - [x] 2.7.2 `run_ideation(topic, research_file?, no_trends?)`
  - [x] 2.7.3 `run_hook(topic, platform?, audience?, format?, research_file?, no_polish?)`
  - [x] 2.7.4 `run_outline(topic, hook_path?, length?, platform?, no_polish?)` - **does not pass `research_file`** per locked decision #5.
  - [x] 2.7.5 `run_title(concept)`
  - [x] 2.7.6 `run_cascade({research_file, outline_file, title?} | {youtube_url})`
  - [x] 2.7.7 `run_short_form({research_file, outline_file, title?} | {youtube_url})`
  - [x] 2.7.8 `run_voice_cleanup(file_path, inplace?)`

### 2D - Stage output resolvers
- [x] **2.8 Resolver dispatch table** (per plan section "Stage output resolvers"):
  - [x] 2.8.1 `resolve_researcher_outputs` - parses `Brief written to:` with deterministic fallback.
  - [x] 2.8.2 `resolve_ideation_outputs` - parses `Output:` with deterministic fallback.
  - [x] 2.8.3 `resolve_hook_outputs` - parses `Hooks written to:` with deterministic fallback.
  - [x] 2.8.4 `resolve_outline_outputs` - parses `Outline written to:` with deterministic fallback.
  - [x] 2.8.5 `resolve_title_outputs` - parses final stdout `.md` line with title-slug fallback.
  - [x] 2.8.6 `resolve_cascade_outputs` - parses `Distribution package written to:` and returns `bundle` with `README.md` preferred as `primary_path`.
  - [x] 2.8.7 `resolve_short_form_outputs` - parses `Short-form package written to:` and returns `bundle`.
  - [x] 2.8.8 `resolve_voice_cleanup_outputs` - supports `inplace` and `_cleaned` sibling fallback.

### 2E - Vault + Brain
- [x] **2.9 `server/vault.py`** - `recent(folder, limit)`, `read_file(path)`, and `outputs(path)` shipped with path-traversal guard inside `Content-Hub-Vault-V2/`.
- [x] **2.10 `GET /api/vault/recent`, `/api/vault/file`, `/api/vault/outputs`** - wired in `server/main.py`.
- [x] **2.11 `server/brain.py`** - Brain analyzer shipped, but with one implementation drift: Claude CLI via `generate(provider="claude")` instead of the plan's direct Anthropic SDK call. See [[2026-05-22_Webapp_Phase2_Authority_Clarification]].
- [x] **2.12 `POST /api/brain/analyze`** - accepts `{content}`, returns `{job_id}`.

### 2F - Verify
- [x] **2.13 Curl smoke test** - Title endpoint + SSE happy path captured in [[2026-05-22_Webapp_Phase2_Backend]].
- [~] **2.14 Repeat for each of the 8 pipeline endpoints + Brain** at minimum with one happy-path payload. Endpoint surface is shipped, but a full per-endpoint verification matrix is still worth capturing in one place.

---

## Phase 3 - Frontend Port (2-3h)

**Goal:** Vite renders the prototype identically to the original `Content Hub.html`. No wiring, still hardcoded demo data.

- [x] **3.1 `Content Hub.html` -> `web/index.html`** - CDN tags stripped; Vite mount point kept. Per the corrected plan, `particles.js` creates its own canvas dynamically, so no static `<canvas>` was added.
- [x] **3.2 `app.jsx` -> `App.jsx`** - add `import { useState, useEffect, useCallback } from 'react'`; `export default App`. Replaces global `React` CDN reliance.
- [x] **3.3 Port `dashboard.jsx`, `stage-workspace.jsx`, `sidebar.jsx`, `icons.jsx`, `tweaks-panel.jsx`** - explicit imports + default exports.
- [x] **3.4 Port `brain.jsx`** - **strip URL chips + file-drop controls** for v1 (locked decision #8). Pasted-text textarea only.
- [x] **3.5 `main.jsx`** - mounts `<App />`; the particle bootstrap side effect shipped early in `App.jsx` during Phase 1 scaffold.
- [x] **3.6 Import `styles.css`** from `main.jsx`.
- [x] **3.7 Visual diff check** - Vite dev server output should be visually identical to the original `Content Hub.html` rendering, hardcoded demo data still in place.

---

## Phase 4 - Wire 5 Sidebar Stages (3-4h)

**Goal:** Trends + Research + Ideation + Hooks + (Brain placeholder) all run real backend, stream logs, render real vault output.
Execution playbook: [[2026-05-23_phase4-wire-5-stages]] (one-task subagents, per-agent memory notes, self-verification, final eval gate).

### 4A - Shared frontend infra
- [x] **4.1 `web/src/api.js`** - `runStage(stage, body)`, `getRecent(folder, limit)`, `readVaultFile(path)`, `listOutputs(path)`.
- [x] **4.2 `web/src/hooks/useJobStream.js`** - SSE hook returning `{lines, status, result, error}`.

### 4B - New shared UI components
- [x] **4.3 `VaultPicker.jsx`** - dropdown driven by `getRecent(folder)`; supports per-stage folder configs (10-Research, 05-Hooks, 06-Outlines, any-output).
- [x] **4.4 `MarkdownViewer.jsx`** - `react-markdown` render of vault file content.
- [x] **4.5 `OutputBrowser.jsx`** - receives `{result_type, primary_path, outputs[]}`. `file` -> delegate to `MarkdownViewer`; `file_set`/`bundle` -> selectable list with `primary_path` opened by default.

### 4C - Generic stage rewire
- [x] **4.6 `StageWorkspace.jsx` rewrite** - replaced `OUTPUTS[stageId]()` demo data with `<OutputBrowser result={result} />`; replaced static loading state with `useJobStream`. Run button -> `runStage(stageId, body)`. Mode state lifted to `StageWorkspace`. `SourcesPanel.jsx` wired to live vault via `LiveSourcesPanel` + `getRecent`. See [[2026-05-24_phase4-wire-stages]].
- [x] **4.7 History drawer** - list `getRecent(<folder>)` newest-first; clicking file row opens `MarkdownViewer` inline inside drawer with back button.
- [x] **4.8 "Save to Vault" -> "Reveal in vault"** - "Copy path" button copies `jobResult.primary_path` to clipboard.

### 4D - Per-stage wiring + verify
- [x] **4.9 Trends workspace** - read-only render of `04-Trends/github_trending.md`. `OutputZone` always shows `MarkdownViewer`; `InputZone` shows read-only notice only; `handleRun` returns early.
- [x] **4.10 Research workspace** - `runStage("research", {niche, repos, mode})` -> SSE stream -> `OutputBrowser`. `App.jsx` `runState:"done"` seed removed. Live verification: SSE fires + done event correct shape; researcher skill requires non-empty `--repos` — playbook payload `repos: []` exits early, no file written (skill CLI gap, not frontend defect).
- [x] **4.11 Ideation workspace** - `VaultPicker folder="10-Research"` replaces URL input; `runStage("ideation", {topic, research_file})` -> SSE -> `OutputBrowser`.
- [x] **4.12 Hook workspace** - `VaultPicker folder="10-Research"` for research file; `runStage("hooks", {topic, research_file})` -> SSE -> `OutputBrowser`. `App.jsx` seed removed.

**Live verification (2026-05-24):** Ideation ✅ real file in `02-Ideas`; Hooks ✅ real file in `05-Hooks`; Trends ✅ reads real vault markdown; Research SSE ✅ (file-write gap: requires non-empty repos). History drawer ✅ returns real artifacts. Build ✅ 187 modules. Lint ✅ stable 0 errors. Full evidence in `Design-doc/web/src/.agent-context/phase4/99-Verification.md`. **Execution-record gap:** agent memory notes 01–08 absent (single-session execution, not subagent pattern).

---

## Phase 5 - Distribution Multi-Tab (2-3h)

**Goal:** Compress 5 skills (Outline, Title, Cascade, Short-form, Voice-cleanup) into one sidebar entry with internal tabs.

- [x] **5.1 `DistributionWorkspace.jsx`** - top tab bar + URL hash routing (`#distribution/<tab>`); active tab persists across nav.
- [x] **5.2 `DistributionTabs/OutlineTab.jsx`** - topic, `hook_path` (`VaultPicker` `05-Hooks/`), length, platform. **No `research_file` field** (locked decision #5).
- [x] **5.3 `DistributionTabs/TitleTab.jsx`** - concept input only.
- [x] **5.4 `DistributionTabs/CascadeTab.jsx`** - `research_file` + `outline_file` pickers OR `youtube_url`; renders `bundle` output.
- [x] **5.5 `DistributionTabs/ShortFormTab.jsx`** - same shape as Cascade; renders `bundle` output (30s/60s/90s scripts).
- [x] **5.6 `DistributionTabs/VoiceCleanupTab.jsx`** - `file_path` (`VaultPicker` any-output folder) + `inplace?` toggle.
- [x] **5.7 Dashboard "Outline" card** - link target switches to `#distribution/outline`.
- [ ] **5.8 Full-chain verify** - from a single new topic, run Outline -> Title -> Cascade -> Short-form -> Voice-cleanup. Confirm all 5 artifacts land in correct vault folders. (deferred to Phase 7 E2E)

---

## Phase 6 - Dashboard + Brain + Polish (2-3h)

Execution: [[2026-05-24_phase6-dashboard-brain-polish]] (inline coordinator, 5 groups). Build ✅ 195 modules. Lint ✅ 0 problems. Evidence in `Design-doc/web/src/.agent-context/phase6/99-Verification.md`.

- [x] **6.1 Dashboard cards** - `usePipelineSnapshot` pulls `getRecent(<folder>, 3)` per card; activity list shows real vault filenames + `formatRelative` timestamps. Hardcoded mock arrays deleted.
- [x] **6.2 Dashboard "Run [Stage]" buttons** - already correct in Phase 5; running state now comes from `jobActivity.js` `runningSet` (live, not hardcoded).
- [x] **6.3 Sidebar status dots** - `usePipelineSnapshot` derives `sidebarStatuses` from vault folder presence + live `jobActivity` running set. Hardcoded `done|running|idle` replaced.
- [x] **6.4 Brain workspace wiring** - `runBrainAnalysis(content)` → `POST /api/brain/analyze` → `useJobStream` SSE → 5 real payload fields rendered. All fake content (6-section BrainResults, ScoreCard, setTimeout) deleted.
- [x] **6.5 Health badge** - `getHealth()` in Sidebar.jsx; green dot "Backend up" / red dot "Backend down" in `sidebar-bottom`.
- [x] **6.6 TweaksPanel** - already `localStorage`-backed via `CustomEvent('tweakchange')`; no `postMessage` in source files. Verified clean.
- [x] **6.7 409 handling** - `ConflictError` (status 409) exported from `api.js`; inline notice "A job is already running — wait for it to finish." wired in StageWorkspace, Brain, and all 5 Distribution tabs.

---

## Phase 7 - Launch Convenience + E2E Acceptance (30m + verify)

- [ ] **7.1 `Design-doc/start.ps1`** - launches Vite + FastAPI in separate PowerShell windows.
- [x] **7.2 `Design-doc/README.md`** - dev quickstart shipped in [[2026-05-22_Webapp_Phase1_Runtime_Fix]].
- [ ] **7.3 E2E acceptance run** - fresh topic, full chain through the UI:
  - [ ] Research -> Ideation -> Hooks -> Distribution (Outline -> Title -> Cascade -> Short-form -> Voice-cleanup).
  - [ ] All SSE log streams live, no spinner stalls.
  - [ ] Every completed run renders real vault markdown/bundle (no demo content).
  - [ ] `Content-Hub-Vault-V2/` contains all 9 deliverables dated today.
  - [ ] Sidebar status dots flip done/running correctly.
  - [ ] Brain returns a real Claude analysis on pasted content.
  - [ ] Dashboard "recent activity" reflects new artifacts.
  - [ ] Second concurrent submission returns 409 gracefully.

---

## Session Log Obligation (mandatory per [[CLAUDE]] section 7)

- [ ] On final phase completion, write `Content-Hub-Vault-V2/00-Management-V2/Sessions/YYYY-MM-DD_Design_Doc_Web_App_Wired.md` linking back to [[Design_Doc_Web_App_Plan]] and to all 8 skill nodes ([[researcher]], [[ideation]], [[hook]], [[outline]], [[title]], [[cascade]], [[short-form]], [[voice-cleanup]]).
- [ ] Update [[Current_Sprint]] to mark wrapper plan superseded and webapp sprint complete.

---

## Out of Scope (do not pull in mid-sprint)

- SQLite/Postgres/Supabase job history (Supabase, if added later, is **app state only** - vault stays execution-layer truth).
- In-app markdown editor (Obsidian owns editing).
- Multi-user auth (add a demo gate only if exposing externally).
- Parallel job execution.
- Publishing automation.
- Any change to `backend/main.py` (V1 SaaS, port 8000).
- Any change to `skills/*.py` or `prompts/*.md` ([[CLAUDE]] section 3 surgical changes - wrapper only).
- TypeScript port (locked decision #1).
- Brain URL/file ingestion (deferred to v2; locked decision #8).

---

## Related Nodes

- Implements: [[Design_Doc_Web_App_Plan]]
- References: [[Local_First_Skill_Engine_Plan]], [[Current_Sprint]]
- Depends on: [[researcher]], [[ideation]], [[hook]], [[outline]], [[title]], [[cascade]], [[short-form]], [[voice-cleanup]]
- Modifies: `Design-doc/` directory tree (new `web/` and `server/` subdirs)
