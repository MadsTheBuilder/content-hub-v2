---
date: 2026-05-31
type: session-log
tags: [webapp, full-pipeline, bugfix, frontend]
description: "Fixed 2 of 3 full-pipeline bugs found during live testing. State loss on tab switch resolved; empty ideation slug resolved. Research filename spec pending user clarification."
---

# Session — Full Pipeline Bug Fixes (State Loss + Ideation Name)

**Modifies:** [[FullPipelinePage]], [[App.jsx]]
**References:** [[2026-05-31_Research_Options_Config_Gate]], [[Full Pipeline Page]], [[useJobStream]]

## Bugs Fixed

### Bug 1 — State loss on tab switch

**Root cause:** `App.jsx` used `{view === "full-pipeline" && <FullPipelinePage .../>}` — the conditional render unmounts the component on every tab switch, wiping all `useState` (active step, picks, job streams).

**Fix:** Replaced with a `<div style={{ display: view === "full-pipeline" ? "" : "none" }}>` wrapper so the component stays mounted. CSS hide preserves the React fiber tree and also keeps any live `useJobStream` SSE connections alive across the switch.

**File:** `Design-doc/web/src/App.jsx` — line 100.

---

### Bug 3 — Ideation file named `2026-05-31_.md`

**Root cause:** `approveResearch` sent `topic: seed` to the ideation launcher. `seed` is the top-level "Niche / space" input. If the user left it blank and typed only in the config gate's `research.niche` field, `topic` was `""` → `make_output_path("")` → empty slug → `2026-05-31_.md`.

**Fix:** Changed `approveResearch` in `FullPipelinePage.jsx` to use `research.niche.trim() || seed.trim()`. `research.niche` is guaranteed non-empty by the time `approveResearch` is reachable (research has run and `briefPath` exists), so this is the primary value; `|| seed` is belt-and-suspenders.

**File:** `Design-doc/web/src/FullPipelinePage.jsx` — line 148.

---

## Bug 2 — Research file `2026-05-31_design_brief.md` (pending)

**Reported:** `10-Research/2026-05-31_design_brief` — user considers this "not named properly."

**Root cause candidate:** `researcher.py` line 682 builds the name from niche only (`{date}_{niche_slug}_brief.md`). With niche="design" and repo `Manavarya09/design-extract`, no repo identifier appears in the filename.

**Status:** Awaiting user clarification — the requirement is ambiguous (niche + repo slug? repo name replaces niche? something else?). No change made. See [[Current_Sprint]].

---

### Refresh persistence (2026-06-01 follow-up)

**Request:** Persist Full Pipeline state across page refreshes (not just tab switches).

**Approach:** `localStorage` with a single `"fp_pipeline_v1"` key.

**What's persisted:** `seed`, `activeId`, `phase`, `picks`, `results`, `research`. If the page was refreshed mid-run (`phase === "running"`), it restores to `"review"` so the user can retry from where the job was.

**What's not persisted:** `runningStage`, `stageError`, `jobId`, `refreshKey` — all transient.

**Files changed:**
- `Design-doc/web/src/FullPipelinePage.jsx`
  - Added `STORAGE_KEY` + `readSaved()` module-level helpers
  - 6 `useState` calls use lazy initializers that read from localStorage
  - New `useEffect` writes the 6 fields to localStorage on every change
  - `resetPipeline()` clears localStorage and resets all state to defaults
  - "Start Over" button in header (shown once `activeIndex > 0` or `phase !== "idle"`)

**Lint:** 0 errors, 2 pre-existing warnings (unchanged).

---

### Job recovery after page refresh (2026-06-01 follow-up)

**Problem:** Page refresh drops the SSE `EventSource`. The backend subprocess keeps running, but the frontend lost `jobId` and `runningStage` (both transient), so the step showed as "available" again instead of "waiting on server."

**Why not reconnect SSE:** The pre-refresh SSE generator stays alive up to 30 s (parked in `await queue.get()`). A new `EventSource` would race against it — whichever generator reads the `done` event from the queue wins. If the zombie wins, the new client gets nothing, `onerror` fires, and `useJobStream` sets `status: "failed"` — a lie that blocks the pipeline and burns research credits.

**Fix:** Poll `GET /api/jobs/{id}` every 3 s instead of reconnecting SSE. No queue access, no race.

**Recovery logic (mount-once `useEffect`):**
- Reads `phase` from `fp_pipeline_v1` (localStorage).
- If `"running"`, reads `fp_pipeline_v1_job` (separate key written by `launch()`) for the job ID.
- No saved job ID → `setPhase("review")` (fallback, allow retry).
- Polls `getJobStatus(savedJobId)` every 3 s:
  - `completed` → `clearInterval` + call `handleCompletion` directly (uses `job.result`)
  - `failed/other` → `clearInterval` + show error + `setPhase("review")`
  - `running` → keep polling (shows "Reconnecting to server job…" in log pane)
  - `catch` (404 / server restarted) → show "Server was restarted" error + allow retry
- `return () => clearInterval(...)` cleans up on unmount.

**`handleCompletion(stageId, res, path)` helper:**
Extracted from the old jobStream `useEffect` so both normal flow (SSE) and recovery (polling) share one path. Clears `JOB_KEY`, calls `announceDone`, advances `picks`/`results`/`phase`, sets `runningStage = null`.

**`JOB_KEY = "fp_pipeline_v1_job"`:** Separate from the main storage key.
- Written in `launch()` after `runStage` returns the `job_id`.
- Cleared in `handleCompletion`, in the `failed` branch of the jobStream effect, and in `resetPipeline`.
- Kept separate so the persist effect (which depends on React state) cannot accidentally clobber it.

**Files changed:**
- `Design-doc/web/src/api.js` — added `getJobStatus(jobId)` → `GET /api/jobs/{id}`
- `Design-doc/web/src/FullPipelinePage.jsx`:
  - Import: added `getJobStatus`
  - Added `JOB_KEY` constant
  - Phase initializer: removed "running"→"review" conversion (recovery effect owns that transition now)
  - Added `handleCompletion` function
  - Added recovery `useEffect` (mount-once polling)
  - `launch()`: persists `job_id` to `JOB_KEY`
  - jobStream `useEffect`: refactored to call `handleCompletion`; clears `JOB_KEY` on failure
  - Log pane: shows "Reconnecting to server job…" when `runningStage === null` (recovery in progress)
  - `resetPipeline`: clears `JOB_KEY`

**Lint:** 0 errors, 2 pre-existing warnings (unchanged).

## Open items (carried from previous session)

- Backend restart required to load new `ResearcherBody` fields (uvicorn `--reload`).
- Live run of `--target-length / --tone / --audience / --banned-phrase` still pending.
- Bug 2 research naming pending user answer.
