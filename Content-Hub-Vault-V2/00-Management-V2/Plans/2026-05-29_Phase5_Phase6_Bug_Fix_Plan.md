---
date: 2026-05-29
status: ready
tags: [plan, webapp-sprint, phase6, bugfix, verification]
description: "Bug-fixing plan for Phase 5/6 verification findings before Phase 7 E2E acceptance."
---

# Phase 5 + Phase 6 Bug Fix Plan

Implements: [[Webapp_sprint]] repair pass
References: [[2026-05-29_Phase5_Phase6_Verification_Audit]], [[2026-05-24_Webapp_Phase5_Distribution]], [[2026-05-24_phase6-dashboard-brain-polish]], [[2026-05-29_phase7-launch-e2e-acceptance]], [[Design_Doc_Web_App_Plan]]
Modifies: [[Design-doc]]

## Goal

Repair the confirmed Phase 6 runtime bugs and polish debt before running Phase 7 browser-facing E2E acceptance. Phase 5 API/vault artifact verification is already complete via [[2026-05-29_Phase5_FullChain_Verification]], but Phase 5 still needs the browser visual/SSE spot-check during Phase 7.

## Do Not Widen Scope

- Do not redesign the webapp UI.
- Do not edit `skills/*.py`, `prompts/*.md`, or server pipeline wrappers unless a browser acceptance failure proves a wrapper bug.
- Do not add a database, persistent job store, React Router, Redux/Zustand, auth, or publishing automation.
- Do not mark [[Webapp_sprint]] complete until Phase 7 acceptance passes in the browser.

## Fix Order

### 1. Fix Brain Result Rendering

**Problem:** Backend Brain jobs return the five payload fields under `result.data`, but `Brain.jsx` reads them from the top-level result object.

**Files:**

- `Design-doc/web/src/Brain.jsx`

**Implementation:**

- In `BrainResults`, normalize the payload:
  - If `result.result_type === "brain_result"`, read `const data = result.data || {}`.
  - Keep a defensive fallback for direct payloads only if useful for old local state.
- Render:
  - `data.hook_quality`
  - `data.structure_score`
  - `data.emotional_triggers`
  - `data.techniques_to_steal`
  - `data.replication_template`
- Render a readable empty/error state if a completed Brain job has missing `data`.

**Acceptance:**

- A mocked `/api/brain/analyze` job returns `result.data` and the UI-visible result component receives all five fields.
- No fake Brain sample prose is reintroduced.
- `npm.cmd run lint` stays clean.

### 2. Refresh Dashboard/Sidebar Snapshot After Jobs

**Problem:** `usePipelineSnapshot` loads recents/status once on mount. After a job completes, `runningSet` updates but vault recents and done statuses can stay stale until reload.

**Files:**

- `Design-doc/web/src/hooks/usePipelineSnapshot.js`
- `Design-doc/web/src/jobActivity.js` only if the hook needs event metadata beyond the current `Set`

**Implementation:**

- Extract `loadSnapshot()` inside `usePipelineSnapshot`.
- Run `loadSnapshot()`:
  - on mount
  - on `window.focus`
  - after a local job settles (`announceDone` or `announceFail`)
- Keep the implementation local and simple. A small event version counter in `jobActivity` is acceptable; a global store is not.
- Avoid polling.

**Acceptance:**

- Starting a job sets the relevant running dot immediately.
- Completing a job clears running and refreshes Dashboard recents/status without full page reload.
- Window focus refreshes stale recents.
- `fetch(` remains isolated to `api.js`.

### 3. Correct Distribution Status Rollup

**Problem:** Distribution done status currently checks only `06-Outlines`; the contract requires a rollup across the Distribution child outputs.

**Files:**

- `Design-doc/web/src/hooks/usePipelineSnapshot.js`

**Implementation:**

- Replace single-folder status mapping with stage-to-folders mapping.
- Distribution done folders:
  - `06-Outlines`
  - `07-Titles`
  - `08-Distribution`
  - `09-Shorts`
- Running status remains `runningSet.has("distribution")` for current tab implementation.
- Preserve Trends read-only behavior.

**Acceptance:**

- If any Distribution output folder has at least one item, sidebar Distribution status becomes `done`.
- Running still beats done.
- Empty folders with no running job render `idle`.

### 4. Remove Misleading Dashboard Prototype Stats

**Problem:** Dashboard still shows hardcoded "last run 12 minutes ago" and Brain banner stats (`142`, `8.1`, `37`). They are not tied to backend/vault state.

**Files:**

- `Design-doc/web/src/Dashboard.jsx`

**Implementation Options:**

- Preferred: replace hardcoded subtitle with a neutral live summary based on loaded recents, such as `4 active stages`.
- Preferred: replace Brain stats with non-numeric labels or remove that stat strip until Brain history exists.
- Do not invent Brain history persistence.

**Acceptance:**

- No misleading fixed recency copy remains.
- No fake Brain totals/scores remain.
- Dashboard remains visually balanced.

### 5. Reassess Static SourcesPanel Demo Data

**Problem:** `SourcesPanel.jsx` still contains static demo data for `distribution`, `brain`, `title`, and `outline`. Current live Distribution tabs do not use that path, but the dead demo data can confuse future verification.

**Files:**

- `Design-doc/web/src/SourcesPanel.jsx`
- Possibly `Design-doc/web/src/StageWorkspace.jsx` if old non-live stage branches are now unreachable

**Implementation Options:**

- Minimal: document that static fallback is legacy/unreachable for current navigation and leave it until Phase 7.
- Better: remove static fallback entries for live/current routes and render a plain "No live source panel for this workspace" message for unsupported stage IDs.

**Acceptance:**

- No visible current route exposes fake vault/source data.
- Existing Trends/Research/Ideation/Hooks source panels still load live vault recents.

## Verification Gate

Run these after fixes:

1. `rg -n "fetch\\(" Design-doc/web/src` shows only `api.js`.
2. `rg -n "postMessage" Design-doc/web/src` has no matches.
3. `npm.cmd run build` in `Design-doc/web` passes.
4. `npm.cmd run lint` in `Design-doc/web` passes.
5. FastAPI TestClient mocked Brain job confirms:
   - `/api/health` returns `{status:"ok", backend:"up", capabilities:null}`.
   - `/api/brain/analyze` returns `{job_id}`.
   - completed job result has five fields under `result.data`.
6. Browser check at `http://localhost:5173` confirms:
   - Brain renders all five fields after a completed analysis.
   - Dashboard recents refresh after at least one completed run.
   - Sidebar status dots flip running -> done/idle.
   - A second concurrent submission shows the friendly 409 notice.
   - Distribution tab navigation and SSE log movement are visible.

## Phase 7 Gate After Repair

After the repair verification passes, resume [[2026-05-29_phase7-launch-e2e-acceptance]]:

- Use the launcher/servers contract from Phase 7.
- Run the full UI chain: Research -> Ideation -> Hooks -> Distribution tabs.
- Verify Brain and 409 in the browser.
- Only then update [[Webapp_sprint]], [[Current_Sprint]], and the final wired-app session log.

## Repair Checklist

- [ ] Fix Brain `result.data` rendering.
- [ ] Add snapshot refresh on focus and job settle.
- [ ] Roll up Distribution done status across all output folders.
- [ ] Remove misleading Dashboard prototype stats.
- [ ] Decide whether to remove or quarantine static `SourcesPanel` fallback data.
- [ ] Run static/build/lint/backend verification.
- [ ] Run browser-facing acceptance checks.
- [ ] Update sprint docs only after acceptance passes.
