---
slug: phase6-dashboard-brain-polish
date: 2026-05-24
created: 2026-05-24
status: complete
current_group: null
groups_complete: [0, 1, 2, 3, 4]
specialists_involved: [frontend-agent]
tags: [orchestration, webapp-sprint, phase6, frontend, dashboard, brain, polish, verification]
description: "Subagent-driven execution playbook for [[Webapp_sprint]] Phase 6. Each agent owns one task, writes its own memory note, self-verifies, and hands off to a final verification/eval gate."
---

# Orchestration: Phase 6 Dashboard Brain Polish - [[Webapp_sprint]]

Implements: [[Webapp_sprint]]
References: [[Design_Doc_Web_App_Plan]], [[Current_Sprint]], [[2026-05-24_phase5-distribution-multi-tab-5-skills]], [[2026-05-24_Webapp_Phase5_Distribution]]
Modifies: [[Design-doc]]

## Reader + Action

Reader: Claude acting as the coordinator.

Action after reading: complete Phase 6 of [[Webapp_sprint]] using one-task subagents, per-agent memory, self-verification inside each task, and a read-only final eval gate.

## Prerequisite Gate

Do not start Phase 6 until Phase 5 is actually passing.

Minimum evidence before dispatch:

- `Design-doc/web/src/DistributionWorkspace.jsx` exists and owns the five Distribution tabs.
- `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `TitleTab.jsx`, `CascadeTab.jsx`, `ShortFormTab.jsx`, and `VoiceCleanupTab.jsx` already run against the real backend.
- `Design-doc/web/src/api.js` remains the only `fetch` caller in `Design-doc/web/src/`.
- `Design-doc/web/src/hooks/useJobStream.js` exists and settles cleanly for pipeline jobs.
- `Design-doc/web/src/Dashboard.jsx` already routes the Outline card to `#distribution/outline`.
- `npm run build` and `npm run lint` are clean before Phase 6 edits begin.

If any of the above is false, stop and finish Phase 5 first. Phase 6 builds on the existing live wiring; it does not replace it.

## Definition Of Done

- `Design-doc/web/src/Dashboard.jsx` no longer ships hardcoded activity lists for the live cards; each card shows the 3 most recent vault items from its mapped folder.
- Dashboard card header state no longer depends on hardcoded `running` booleans; any running affordance comes from the shared local job snapshot.
- Dashboard card CTA buttons and card clicks navigate to the correct live workspace, with Outline continuing to land on `#distribution/outline`.
- `Design-doc/web/src/Sidebar.jsx` no longer hardcodes `done|running|idle`; status dots derive from current local job activity plus recent vault timestamps.
- Distribution status in the sidebar rolls up `outline`, `title`, `cascade`, `short-form`, and `voice-cleanup` without inventing a new folder.
- A sidebar footer health badge consumes `/api/health` and only surfaces backend reachability in v1.
- `Design-doc/web/src/Brain.jsx` no longer uses a fake `setTimeout` flow or seeded done-state sample output.
- Brain uses `/api/brain/analyze` plus `useJobStream` and renders the real `brain_result` payload fields: `hook_quality`, `structure_score`, `emotional_triggers`, `techniques_to_steal`, and `replication_template`.
- A `409` conflict from a second concurrent submission is handled gracefully in the UI with clear retry-later copy.
- `TweaksPanel` behavior stays intact and localStorage remains the persistence path; no stale `postMessage` path survives in `Design-doc/web/src/`.
- Final eval proves Dashboard recent activity is live, sidebar dots react to real local runs, Brain returns a real analysis payload, `/api/health` is surfaced, and build/lint pass.

## Hard Boundaries

- Do not edit `skills/*.py`, `prompts/*.md`, or `Design-doc/server/*` unless a proven contract bug blocks Phase 6. If blocked, stop and dispatch one narrowly scoped `pipeline-agent` patch task instead of widening frontend scope.
- Do not pull in Phase 7 work: `start.ps1`, launch automation, or the full nine-step E2E acceptance chain.
- Do not redesign the Dashboard, Sidebar, or Brain layout. Phase 6 is wiring and polish, not a new visual direction.
- Do not add React Router, Zustand, Redux, or any new global state library. If a tiny shared helper is needed, keep it local to `Design-doc/web/src/`.
- All frontend HTTP calls must continue to live in `Design-doc/web/src/api.js`.
- Brain remains pasted-text only in v1. Do not add URL ingestion, file upload, vault pickers, or history storage for Brain.
- Do not invent new persistence for Dashboard activity, sidebar status, or job history. The vault remains the source of truth for recency; local in-memory state is only for the currently running job in this browser session.
- Do not widen TweaksPanel scope. If localStorage persistence is already correct, treat Phase 6.6 as a verification guard, not a rewrite project.

## Shared Contract

### Dashboard Card -> Vault Folder + Navigation

| Dashboard card | `getRecent` folder | Open target | Notes |
|---|---|---|---|
| `trends` | `04-Trends` | `trends` | Read-only stage; show newest file names only. |
| `research` | `10-Research` | `research` | Activity comes from real vault artifacts, not mock source counts. |
| `ideation` | `02-Ideas` | `ideation` | Activity comes from real idea files, not fake scores. |
| `outline` | `06-Outlines` | `distribution` + hash `#distribution/outline` | Keep the card name `Outline` in Phase 6. Do not explode it into five Distribution cards yet. |

Rules:

- Show at most 3 recent items per card.
- Use returned vault names/paths/timestamps; do not read whole files just to build the activity list.
- Empty folders must render a readable empty state instead of mock content.
- If a card still shows a running affordance in its header, that state must come from the shared local job snapshot rather than a hardcoded boolean.

### Sidebar Stage -> Status Inputs

| Sidebar stage | Running rule | Done rule | Notes |
|---|---|---|---|
| `trends` | never `running` in v1 | `04-Trends` has at least one recent item | Trends is read-only in the webapp. |
| `research` | current local job stage is `research` | `10-Research` has recent items | |
| `ideation` | current local job stage is `ideation` | `02-Ideas` has recent items | |
| `hooks` | current local job stage is `hooks` | `05-Hooks` has recent items | |
| `distribution` | current local job stage is one of `outline`, `title`, `cascade`, `short-form`, `voice-cleanup` | any of `06-Outlines`, `07-Titles`, `08-Distribution`, `09-Shorts` has recent items | Voice-cleanup has no dedicated folder; do not invent one. |

Rules:

- `running` beats `done`, and `done` beats `idle`.
- Status dots should react to jobs started in the current browser session without needing a new backend endpoint.
- A tiny local helper for announcing start/done/fail is allowed if it stays inside `Design-doc/web/src/` and is documented in the agent note.

### Brain Contract

- `POST /api/brain/analyze` accepts `{ content }` and returns `{ job_id }`.
- Brain must use `GET /api/jobs/<job_id>/stream` through `useJobStream`, just like the pipeline stages.
- On success, the `done` event yields a result with:
  - `result_type: "brain_result"`
  - `primary_path: ""`
  - `outputs: []`
  - `data.hook_quality`
  - `data.structure_score`
  - `data.emotional_triggers[]`
  - `data.techniques_to_steal[]`
  - `data.replication_template`
- No other narrative sections are guaranteed by the backend. If the UI wants extra copy, it must derive it from these fields only.

### Health + Conflict + Tweaks Contract

- `GET /api/health` returns `{status, backend, capabilities: null}`.
- Phase 6 only displays backend reachability. Ignore `capabilities` in the UI.
- `409` means another job is already running. The UI must not crash, silently swallow it, or dump an unreadable raw error blob.
- A graceful conflict response can be a toast, inline notice, or clearly styled banner, but it must explain that another run is active and the user should retry after it finishes.
- `TweaksPanel` persistence is already expected to be localStorage-backed. Phase 6 should verify that no `postMessage` path remains; do not replace working localStorage behavior.

## Agent Memory Contract

Create `Design-doc/web/src/.agent-context/phase6/` before dispatching workers.

Every worker writes exactly one note:

- `00-Contract.md`
- `01-Phase6Api.md`
- `02-PipelineSnapshot.md`
- `03-Dashboard.md`
- `04-Sidebar.md`
- `05-Brain.md`
- `06-RunFeedback.md`
- `99-Verification.md`

Memory note template:

```md
---
date: 2026-05-24
type: phase6-agent-note
status: done
agent: <name>
task: <single task>
owned_files:
  - <path>
verification:
  - <check>
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# <Agent Name>

## Mission
## Context Read
## Changes Made
## Self-Verification
## Open Items
```

Rules:

- One agent, one task, one note.
- If blocked, set `status: blocked`, document the blocker, and stop. Do not absorb adjacent work.
- Each agent must self-verify before returning `DONE`.
- The coordinator reads the note before advancing the group.

## Coordinator Protocol

1. Read [[Webapp_sprint]], [[Design_Doc_Web_App_Plan]], [[2026-05-24_phase5-distribution-multi-tab-5-skills]], `Design-doc/server/main.py`, `Design-doc/server/brain.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/DistributionWorkspace.jsx`, and `Design-doc/web/src/TweaksPanel.jsx`.
2. Confirm the Phase 5 prerequisite gate is genuinely satisfied.
3. Run `rg "postMessage" Design-doc/web/src` before dispatch. If it returns nothing, record in the coordinator notes that Phase 6.6 is already satisfied and should stay a verification guard only.
4. Create `Design-doc/web/src/.agent-context/phase6/`.
5. Run Group 0 first.
6. Run Group 1 sequentially after Group 0 lands the contract memo.
7. Run Group 2 in parallel only after Group 1 lands the shared API and snapshot contract.
8. After Group 2, run `npm run build` and `npm run lint` in `Design-doc/web/`.
9. Run Group 3 sequentially. After the worker lands, rerun `npm run build`. After Group 3 completes, rerun both build and lint.
10. Start or confirm the backend on port `8765` and the frontend on port `5173`.
11. Run Group 4 as a read-only eval pass. If it fails, do not patch in the verifier. Re-dispatch only the failing worker.
12. Only after Group 4 passes: update [[Webapp_sprint]], update [[Current_Sprint]], write the Phase 6 implementation session log, and mark this orchestration `status: complete`.

## Worker Prompt Scaffold

Use this scaffold for every worker and fill in the task-specific section below.

```text
You are the <agent-type> for Content Hub V2.

Do one task only.
Stay inside the listed file scope.
Do not fix unrelated issues.
Write your memory note to <memory-note-path> before returning.
Self-verify inside your own scope before returning.

Return one of:
- DONE
- DONE_WITH_CONCERNS
- STUCK

Include:
- files changed
- verification performed
- open concerns
```

## Group 0 - Contract Memo

### `00-contract-agent`

- Type: `frontend-agent`
- Task: write a Phase 6 contract memo so later workers use the same Dashboard mappings, sidebar status rules, Brain payload contract, and Phase 6 guardrails.
- Read: `Design-doc/server/main.py`, `Design-doc/server/brain.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/TweaksPanel.jsx`
- Edit: `Design-doc/web/src/.agent-context/phase6/00-Contract.md`
- Must capture:
  - Dashboard card folder mapping for `trends`, `research`, `ideation`, and `outline`
  - Outline card still routes to `#distribution/outline`
  - Distribution status rolls up `outline`, `title`, `cascade`, `short-form`, and `voice-cleanup`
  - Brain is job-based, not direct JSON response in the initial POST
  - `/api/health` only drives backend reachability in v1
  - TweaksPanel localStorage guard stays in scope, but no `postMessage` rewrite should be invented if none exists
  - only `api.js` may use `fetch`
- Self-verification:
  - memo includes a Dashboard card table
  - memo includes a sidebar status table
  - memo names the exact Brain payload keys
  - memo explicitly keeps Phase 7 work out of scope

## Group 1 - Shared Infra

### `01-phase6-api-agent`

- Type: `frontend-agent`
- Task: extend the shared frontend API module for Phase 6
- Read: `Design-doc/server/main.py`, `Design-doc/server/brain.py`, `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`
- Edit: `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase6/01-Phase6Api.md`
- Deliver:
  - `runBrainAnalysis(content)` posting to `/api/brain/analyze`
  - `getHealth()`
  - normalized error handling so `409` can be distinguished in the UI without duplicating fetch logic elsewhere
  - existing stage helpers stay intact
- Self-verification:
  - `fetch(` still appears only in `api.js`
  - `runBrainAnalysis` returns `{ job_id }`
  - `getHealth()` returns `{status, backend, capabilities}`
  - conflict errors preserve readable text and an inspectable `status === 409`

### `02-pipeline-snapshot-agent`

- Type: `frontend-agent`
- Task: create the shared Phase 6 recency + local running-status helper
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/DistributionWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`, `Design-doc/web/src/.agent-context/phase6/01-Phase6Api.md`
- Edit: `Design-doc/web/src/hooks/usePipelineSnapshot.js`, `Design-doc/web/src/jobActivity.js`, `Design-doc/web/src/.agent-context/phase6/02-PipelineSnapshot.md`
- Deliver:
  - one shared source for Dashboard recents and sidebar status derivation
  - stage/folder mappings for Dashboard cards and sidebar stages
  - local current-job signals for `start`, `done`, and `fail` in the current browser session
  - refresh behavior on mount, on window focus, and after a local job settles
- Must not do:
  - add a new dependency
  - add a backend polling endpoint
  - turn this into a generic app store
- Self-verification:
  - no raw `fetch`
  - Distribution running state rolls up the five child stage ids
  - Dashboard recents expose only the four approved cards
  - Trends remains read-only and never fabricates a fake running job

## Group 2 - Parallel Feature Workers

### `03-dashboard-agent`

- Type: `frontend-agent`
- Task: replace Dashboard mock activity with live vault recency while preserving current navigation behavior
- Read: `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/hooks/usePipelineSnapshot.js`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`, `Design-doc/web/src/.agent-context/phase6/02-PipelineSnapshot.md`
- Edit: `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/styles.css`, `Design-doc/web/src/.agent-context/phase6/03-Dashboard.md`
- Must do:
  - remove hardcoded activity arrays for the wired cards
  - show up to 3 recent items from the mapped vault folder on each card
  - replace any hardcoded card-level `running` booleans with shared local job state
  - keep card clicks and CTA buttons navigating to the correct workspace
  - keep Outline pointing to Distribution with hash `#distribution/outline`
  - render empty activity states cleanly when a folder has no artifacts yet
- Must not do:
  - add more dashboard cards
  - widen this into Phase 7 full-chain tracking
  - disturb the Brain banner
- Self-verification:
  - no mock score badges, source-count badges, or fake time labels remain on the wired cards
  - no hardcoded `running` booleans remain for the wired cards
  - Outline still lands on `#distribution/outline`
  - cards render readable fallback copy if recents are empty
  - no raw `fetch`

### `04-sidebar-agent`

- Type: `frontend-agent`
- Task: replace hardcoded sidebar statuses and add the v1 backend health badge
- Read: `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/hooks/usePipelineSnapshot.js`, `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`, `Design-doc/web/src/.agent-context/phase6/02-PipelineSnapshot.md`
- Edit: `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/styles.css`, `Design-doc/web/src/.agent-context/phase6/04-Sidebar.md`
- Must do:
  - remove hardcoded `status` values from the sidebar pipeline definition
  - drive each dot from current local running job + recent vault evidence
  - roll up Distribution correctly across Outline, Title, Cascade, Short-form, and Voice-cleanup
  - add a footer health badge using `/api/health`
  - keep the collapse control, Brain nav, and Settings nav intact
- Must not do:
  - expose `capabilities`
  - add a separate Brain status dot
  - redesign the sidebar structure
- Self-verification:
  - no static `done|running|idle` values remain embedded in the pipeline nav data
  - Distribution dot reacts to any of the five child stage runs
  - health badge survives API failure with readable fallback copy
  - no raw `fetch`

### `05-brain-agent`

- Type: `frontend-agent`
- Task: replace Brain's fake analysis flow with the real `/api/brain/analyze` job flow
- Read: `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`, `Design-doc/web/src/.agent-context/phase6/01-Phase6Api.md`
- Edit: `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/styles.css`, `Design-doc/web/src/.agent-context/phase6/05-Brain.md`
- Must do:
  - remove the seeded fake done-state and fake `setTimeout`
  - submit pasted text through `runBrainAnalysis`
  - use `useJobStream(jobId)` to drive loading, done, and error states
  - render score cards and analysis sections from the actual backend payload only
  - keep Brain as pasted-text only
- Must not do:
  - add URL/file ingestion
  - invent backend fields such as a narrative "Why It Works" blob if it does not come from the payload
  - add vault persistence or Brain history storage
- Self-verification:
  - initial Brain state is not a fake completed analysis
  - no fake sample prose survives in the success state
  - result rendering reads only `hook_quality`, `structure_score`, `emotional_triggers`, `techniques_to_steal`, and `replication_template`
  - no raw `fetch`

## Group 3 - Sequential Integration

### `06-run-feedback-agent`

- Type: `frontend-agent`
- Task: wire shared local run feedback and graceful `409` handling across all live-run screens
- Read: `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `Design-doc/web/src/DistributionTabs/TitleTab.jsx`, `Design-doc/web/src/DistributionTabs/CascadeTab.jsx`, `Design-doc/web/src/DistributionTabs/ShortFormTab.jsx`, `Design-doc/web/src/DistributionTabs/VoiceCleanupTab.jsx`, `Design-doc/web/src/jobActivity.js`, `Design-doc/web/src/hooks/usePipelineSnapshot.js`, `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase6/00-Contract.md`, `Design-doc/web/src/.agent-context/phase6/02-PipelineSnapshot.md`
- Edit: `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/Brain.jsx`, `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `Design-doc/web/src/DistributionTabs/TitleTab.jsx`, `Design-doc/web/src/DistributionTabs/CascadeTab.jsx`, `Design-doc/web/src/DistributionTabs/ShortFormTab.jsx`, `Design-doc/web/src/DistributionTabs/VoiceCleanupTab.jsx`, `Design-doc/web/src/styles.css`, `Design-doc/web/src/.agent-context/phase6/06-RunFeedback.md`
- Must do:
  - emit shared local run-activity signals on `start`, `done`, and `fail` for Research, Ideation, Hooks, all five Distribution tabs, and Brain
  - ensure Distribution child stages report themselves so the sidebar rollup can show `running`
  - replace raw ugly conflict text with a clear retry-later notice for `409` responses
  - keep existing per-screen loading states and output rendering intact
  - verify that Phase 6.6 needs no extra TweaksPanel rewrite if `postMessage` is absent
- Must not do:
  - add a new backend endpoint
  - widen this into a full notification framework
  - change successful result contracts
- Self-verification:
  - starting Research marks Research as locally running
  - starting Outline, Title, Cascade, Short-form, or Voice-cleanup marks Distribution as locally running
  - a `409` path produces friendly copy instead of a crash or silent failure
  - `rg "postMessage" Design-doc/web/src` stays empty
  - no raw `fetch`

## Group 4 - Final Eval Gate

### `99-verification-agent`

- Type: `verification-agent`
- Task: run a read-only end-to-end eval of Phase 6 and decide pass or rerun
- Read: all edited Phase 6 files, all Phase 6 agent notes, `Design-doc/server/main.py`, `Design-doc/server/brain.py`, and any shared Phase 4/5 frontend infra used by Dashboard, Sidebar, or Brain
- Edit only after full pass:
  - `Design-doc/web/src/.agent-context/phase6/99-Verification.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Webapp_sprint.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`
- Read-only if failing:
  - do not patch source files
  - write a fail report naming the exact worker that must rerun
- Eval checklist:
  - static:
    - `rg "fetch\\(" Design-doc/web/src` shows only `api.js`
    - `rg "postMessage" Design-doc/web/src` returns nothing
    - `Dashboard.jsx` no longer contains the old mock activity arrays for the wired cards
    - `Sidebar.jsx` no longer hardcodes pipeline statuses
    - `Brain.jsx` no longer seeds `runState: "done"` or uses fake `setTimeout` analysis
  - build:
    - `npm run build`
    - `npm run lint`
  - API:
    - backend health returns `{status:"ok", backend:"up", capabilities:null}`
    - `/api/brain/analyze` returns a `job_id` and settles through SSE
  - browser or live runtime:
    - open `http://localhost:5173`
    - Dashboard cards show real recent vault items for Trends, Research, Ideation, and Outline
    - Dashboard Outline card and CTA both land on `#distribution/outline`
    - Sidebar health badge reflects backend reachability
    - Sidebar dots react to a live local run and settle back to `done` or `idle`
    - Brain accepts pasted text, shows loading, then renders a real analysis payload
    - while one job is running, a second run attempt yields a graceful `409` notice
- Pass rule:
  - every check above passes
  - only then mark Phase 6 complete in [[Webapp_sprint]]
  - only then update [[Current_Sprint]] so Phase 7 becomes the next step

## Exact Verification Payloads

Use small repeatable payloads so the eval stays deterministic and Phase 6 does not turn into a full Phase 7 chain test.

- Brain:
  - `content`:
    - `I built a local RAG that runs on my laptop with no API bill. Watch what happens at 0:23 when the answer comes back from my own codebase instead of the cloud. Most tutorials waste ten minutes on setup, so I opened with the demo and only explained the stack after the payoff.`
- Conflict:
  - first run:
    - stage: `research`
    - `niche`: `phase6 conflict check for AI tutorial hook patterns`
    - `repos`: `[]`
    - `mode`: `deep`
  - second run while the first is still active:
    - stage: `title` or `brain`
    - use any small valid payload

## Failure Routing

- If Brain or health API mapping is wrong: rerun `01-phase6-api-agent`
- If recency data or local running signals are mapped wrong: rerun `02-pipeline-snapshot-agent`
- If Dashboard still shows mock activity or wrong navigation: rerun `03-dashboard-agent`
- If sidebar dots or health badge are wrong: rerun `04-sidebar-agent`
- If Brain still shows fake output or mismatched payload rendering: rerun `05-brain-agent`
- If `409` handling or live run-status feedback is broken: rerun `06-run-feedback-agent`
- If the backend contract is actually wrong: dispatch one `pipeline-agent` patch task with a separate note, then rerun the blocked frontend worker

## Closeout

After pass:

1. Update this orchestration frontmatter:
   - `status: complete`
   - `groups_complete: [0, 1, 2, 3, 4]`
   - `current_group: null`
2. Update [[Webapp_sprint]] Phase 6 items to reflect what really passed.
3. Update [[Current_Sprint]] so Phase 7 becomes the next step.
4. Write a session log in `00-Management-V2/Sessions/` linking back to this orchestration, [[Webapp_sprint]], and [[Design_Doc_Web_App_Plan]].
5. Keep all Phase 6 agent notes. They are the local memory for the next Claude session.
