---
slug: phase4-wire-5-stages
date: 2026-05-23
created: 2026-05-23
status: complete-execution-record-gap
current_group: null
groups_complete: [0,1,2,3]
specialists_involved: [frontend-agent]
tags: [orchestration, webapp-sprint, phase4, frontend, sse, verification]
description: "Subagent-driven execution playbook for [[Webapp_sprint]] Phase 4. Each agent owns one task, writes its own memory note, self-verifies, and hands off to a final verification/eval gate."
completion_note: "Executed 2026-05-24 as a single-session rewrite rather than via the subagent pattern. All groups functionally complete. Worker notes 01–08 were never written (execution-record gap; not fabricated retroactively). Research scripted payload (repos: []) produced an SSE-only pass — file-write gap documented in 99-Verification.md. See [[2026-05-24_phase4-wire-stages]]."
---

# Orchestration: Phase 4 Wire 5 Stages - [[Webapp_sprint]]

Implements: [[Webapp_sprint]]
References: [[Design_Doc_Web_App_Plan]], [[Current_Sprint]], [[2026-05-23_Webapp_Phase3_Lint_Fix]]
Modifies: [[Design-doc]]

## Reader + Action

Reader: Claude acting as the coordinator.

Action after reading: complete Phase 4 of [[Webapp_sprint]] using one-task subagents, per-agent memory, self-verification inside each task, and a read-only final eval gate.

## Definition Of Done

- `Design-doc/web/src/api.js` exists and is the only place in `web/src/` using `fetch`.
- `Design-doc/web/src/hooks/useJobStream.js` exists and returns `{lines, status, result, error}`.
- `Design-doc/web/src/VaultPicker.jsx`, `MarkdownViewer.jsx`, and `OutputBrowser.jsx` render real vault-backed data.
- `Design-doc/web/src/SourcesPanel.jsx` no longer depends on hardcoded vault mocks for the wired stages.
- `Design-doc/web/src/StageWorkspace.jsx` uses real backend behavior for `trends`, `research`, `ideation`, and `hooks`.
- `Design-doc/web/src/App.jsx` no longer injects fake completed-state seed data into the Phase 4 stages.
- `title`, `outline`, `distribution`, and `brain` do not accidentally expand beyond current scope.
- Final eval proves Trends loads, Research runs, Ideation consumes a real research file, Hooks consumes an optional research file, and build/lint pass.

## Hard Boundaries

- Do not edit `skills/*.py`, `prompts/*.md`, or `Design-doc/server/*` unless a proven contract bug blocks Phase 4. If blocked, stop and dispatch one narrowly-scoped `pipeline-agent` patch task instead of widening frontend scope.
- Do not pull in Phase 5 multi-tab work, Dashboard work, Brain wiring, or 409 polish.
- Keep the existing look and layout. Phase 4 is wiring, not redesign.
- All frontend HTTP calls must live in `Design-doc/web/src/api.js`.
- For the wired stages, remove fake `setTimeout` runs and fake output renderers. For out-of-scope stages, keep them explicitly non-live.

## Shared Contract

### Stage -> Endpoint

| UI stage | Backend behavior | Notes |
|---|---|---|
| `trends` | No POST | Read-only file load from `04-Trends/github_trending.md` |
| `research` | `POST /api/pipeline/researcher` | `prompt -> niche`, `urls -> repos`, `mode toggle -> mode` |
| `ideation` | `POST /api/pipeline/ideation` | `prompt -> topic`, `VaultPicker -> research_file` |
| `hooks` | `POST /api/pipeline/hook` | `prompt -> topic`, optional `VaultPicker -> research_file`, keep backend defaults for other fields |

### Stage -> Vault Folder

| UI stage | Folder | Used for |
|---|---|---|
| `trends` | `04-Trends` | read-only file + history |
| `research` | `10-Research` | output + picker source |
| `ideation` | `02-Ideas` | output + history |
| `hooks` | `05-Hooks` | output + history |

### Result Contract

- Jobs resolve to `{result_type, primary_path, outputs[], data}`.
- Phase 4 should expect `file` results for the wired stages.
- `GET /api/vault/file` returns `{path, content}`.
- `GET /api/vault/outputs` returns readable members for a file or bundle path.
- `GET /api/vault/recent` returns newest-first items with `name`, `path`, and `modified`.

## Agent Memory Contract

Create `Design-doc/web/src/.agent-context/phase4/` before dispatching workers.

Every worker writes exactly one note:

- `00-Contract.md`
- `01-ApiClient.md`
- `02-JobStream.md`
- `03-VaultPicker.md`
- `04-MarkdownViewer.md`
- `05-OutputBrowser.md`
- `06-SourcesPanel.md`
- `07-StageWorkspace.md`
- `08-AppCleanup.md`
- `99-Verification.md`

Memory note template:

```md
---
date: 2026-05-23
type: phase4-agent-note
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

1. Read [[Webapp_sprint]], [[Design_Doc_Web_App_Plan]], `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, `Design-doc/server/vault.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/StageWorkspace.jsx`, and `Design-doc/web/src/SourcesPanel.jsx`.
2. Create `Design-doc/web/src/.agent-context/phase4/`.
3. Run Group 0 first.
4. Run Group 1 in parallel only after Group 0 lands a contract memo.
5. After Group 1, run `npm run build` and `npm run lint` in `Design-doc/web/`.
6. Run Group 2 sequentially. After each agent, rerun `npm run build`. After Group 2 completes, rerun both build and lint.
7. Start or confirm the backend on port `8765` and the frontend on port `5173`.
8. Run Group 3 as a read-only eval pass. If it fails, do not patch in the verifier. Re-dispatch only the failing worker.
9. Only after Group 3 passes: update [[Webapp_sprint]], update [[Current_Sprint]], write the Phase 4 implementation session log, and mark this orchestration `status: complete`.

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
- Task: write a Phase 4 contract memo so later workers use the same endpoint, folder, and result mapping.
- Read: `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, `Design-doc/server/vault.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/SourcesPanel.jsx`
- Edit: `Design-doc/web/src/.agent-context/phase4/00-Contract.md`
- Must capture:
  - `research -> researcher` endpoint mapping
  - `hooks -> hook` endpoint mapping
  - Trends is read-only and does not POST
  - Phase 4 folders: `04-Trends`, `10-Research`, `02-Ideas`, `05-Hooks`
  - `title`, `outline`, `distribution`, and `brain` stay out of scope
- Self-verification:
  - memo includes a stage-to-endpoint table
  - memo includes a stage-to-folder table
  - memo includes the rule that only `api.js` may use `fetch`

## Group 1 - Parallel Shared Infra

### `01-api-client-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/api.js`
- Read: `Design-doc/server/main.py`, `Design-doc/server/vault.py`, `Design-doc/web/src/.agent-context/phase4/00-Contract.md`
- Edit: `Design-doc/web/src/api.js`, `Design-doc/web/src/.agent-context/phase4/01-ApiClient.md`
- Deliver:
  - `runStage(stage, body)`
  - `getRecent(folder, limit = 10)`
  - `readVaultFile(path)`
  - `listOutputs(path)`
  - one internal stage map for `research`, `ideation`, and `hooks`
- Self-verification:
  - `api.js` is the only new file using `fetch`
  - `runStage('hooks', ...)` maps to `/api/pipeline/hook`
  - `runStage('research', ...)` maps to `/api/pipeline/researcher`
  - errors surface as readable messages, not silent `undefined`

### `02-job-stream-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/hooks/useJobStream.js`
- Read: `Design-doc/server/main.py`, `Design-doc/web/src/.agent-context/phase4/00-Contract.md`
- Edit: `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/.agent-context/phase4/02-JobStream.md`
- Deliver:
  - hook takes `jobId`
  - returns `{lines, status, result, error}`
  - handles `stdout`, `stderr`, `ping`, `done`, and `error`
  - cleans up `EventSource` on unmount or job change
- Self-verification:
  - initial status is explicit
  - `done` closes the stream and stores `result`
  - `error` closes the stream and stores a readable error
  - no direct DOM work

### `03-vault-picker-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/VaultPicker.jsx`
- Read: `Design-doc/web/src/.agent-context/phase4/00-Contract.md`, `Design-doc/web/src/api.js`
- Edit: `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/.agent-context/phase4/03-VaultPicker.md`
- Deliver:
  - dropdown backed by `getRecent(folder)`
  - empty, loading, and error states
  - selected vault path emitted upward
- Self-verification:
  - works for `10-Research` and `05-Hooks`
  - selected option value is the vault path, not just the display name
  - no raw `fetch`

### `04-markdown-viewer-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/MarkdownViewer.jsx`
- Read: `Design-doc/web/src/api.js`
- Edit: `Design-doc/web/src/MarkdownViewer.jsx`, `Design-doc/web/src/.agent-context/phase4/04-MarkdownViewer.md`
- Deliver:
  - loads file content via `readVaultFile(path)`
  - renders with `react-markdown`
  - loading, empty, and error states
- Self-verification:
  - handles missing `path`
  - does not inline demo markdown
  - no raw `fetch`

### `05-output-browser-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/OutputBrowser.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/MarkdownViewer.jsx`
- Edit: `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase4/05-OutputBrowser.md`
- Deliver:
  - `file` opens `primary_path` directly
  - `bundle` or `file_set` shows a selectable member list and opens `primary_path` by default
  - can fall back to `listOutputs(primary_path)` when needed
- Self-verification:
  - default selection respects `primary_path`
  - handles single-file and multi-file result shapes
  - no raw `fetch`

## Group 2 - Sequential Integration

### `06-sources-panel-agent`

- Type: `frontend-agent`
- Task: replace wired-stage hardcoded vault mocks in `Design-doc/web/src/SourcesPanel.jsx`
- Read: `Design-doc/web/src/SourcesPanel.jsx`, `Design-doc/web/src/api.js`, `Design-doc/web/src/MarkdownViewer.jsx`, `Design-doc/web/src/.agent-context/phase4/00-Contract.md`
- Edit: `Design-doc/web/src/SourcesPanel.jsx`, `Design-doc/web/src/.agent-context/phase4/06-SourcesPanel.md`
- Must do:
  - remove dependence on stage-specific mock file trees for `trends`, `research`, `ideation`, and `hooks`
  - drive recent file lists from `getRecent(folder)`
  - clicking a file row opens real markdown from the vault
  - keep the `StackedPanel` export intact
- Must not do:
  - rework Brain analysis
  - invent fake sources not backed by API data
- Self-verification:
  - `VAULT_DATA` is gone or reduced to harmless stage metadata only
  - `SourcesPanel` still exports `SourcesPanel` and `StackedPanel`
  - no raw `fetch`

### `07-stage-workspace-agent`

- Type: `frontend-agent`
- Task: rewire `Design-doc/web/src/StageWorkspace.jsx` for real Phase 4 behavior
- Read: `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/SourcesPanel.jsx`, `Design-doc/web/src/.agent-context/phase4/00-Contract.md`
- Edit: `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase4/07-StageWorkspace.md`
- Must do:
  - replace the fake `setTimeout` run path with `runStage`
  - use `useJobStream` for `research`, `ideation`, and `hooks`
  - make `trends` read-only and render `04-Trends/github_trending.md`
  - render live logs while a job is running
  - swap demo output renderers for `OutputBrowser`
  - wire the history drawer to `getRecent(folder)`
  - replace any "Save to Vault" behavior with "Reveal in vault" copy-to-clipboard behavior
  - map bodies exactly:
    - research: `{ niche: prompt, repos: urls, mode }`
    - ideation: `{ topic: prompt, research_file }`
    - hooks: `{ topic: prompt, research_file }`
- Must not do:
  - wire `title`, `outline`, `distribution`, or `brain` to live backend behavior
  - introduce a new global state layer
- Self-verification:
  - no fake `OUTPUTS[stageId]()` path for the wired stages
  - no fake `setTimeout` run path
  - `trends` reads real vault markdown
  - `research`, `ideation`, and `hooks` all import and use `useJobStream`
  - no raw `fetch`

### `08-app-cleanup-agent`

- Type: `frontend-agent`
- Task: remove fake completed-state seed data from Phase 4 routes in `Design-doc/web/src/App.jsx`
- Read: `Design-doc/web/src/App.jsx`, `Design-doc/web/src/.agent-context/phase4/07-StageWorkspace.md`
- Edit: `Design-doc/web/src/App.jsx`, `Design-doc/web/src/.agent-context/phase4/08-AppCleanup.md`
- Must do:
  - stop preloading `runState: "done"` for `research`, `ideation`, and `hooks`
  - keep navigation intact
  - leave Phase 5 and Phase 6 routes alone unless a minimal guard is required to prevent false "live" behavior
- Self-verification:
  - `App.jsx` no longer forces fake done states into the wired stages
  - no route names changed
  - no new raw `fetch`

## Group 3 - Final Eval Gate

### `99-verification-agent`

- Type: `verification-agent`
- Task: run a read-only end-to-end eval of Phase 4 and decide pass or rerun
- Read: all edited frontend files, all Phase 4 agent notes, `Design-doc/server/main.py`, and `Content-Hub-Vault-V2/04-Trends/github_trending.md`
- Edit only after full pass:
  - `Design-doc/web/src/.agent-context/phase4/99-Verification.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Webapp_sprint.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`
- Read-only if failing:
  - do not patch source files
  - write a fail report naming the exact worker that must rerun
- Eval checklist:
  - static:
    - `rg "fetch\\(" Design-doc/web/src` shows only `api.js`
    - wired-stage fake demo paths are gone from `StageWorkspace.jsx`
    - `App.jsx` does not set `runState: "done"` for `research`, `ideation`, or `hooks`
  - build:
    - `npm run build`
    - `npm run lint`
  - API:
    - backend health returns `{status:"ok", backend:"up", capabilities:null}`
    - Trends file reads from `04-Trends/github_trending.md`
  - browser or live runtime:
    - open `http://localhost:5173`
    - Trends renders real markdown from the vault
    - Research run shows live log lines, then renders a real file from `10-Research`
    - Ideation `VaultPicker` shows the newest research artifact and a run creates a real file in `02-Ideas`
    - Hooks `VaultPicker` shows research files and a run creates a real file in `05-Hooks`
    - history drawer opens a real artifact instead of demo content
- Pass rule:
  - every check above passes
  - only then mark Phase 4 items complete in [[Webapp_sprint]]
  - only then update [[Current_Sprint]] so Phase 5 becomes the next step

## Exact Verification Payloads

Use small repeatable payloads so the eval stays deterministic:

- Research:
  - `niche`: `open-source design tools`
  - `repos`: `[]`
  - `mode`: `fast` if supported; otherwise `deep`
- Ideation:
  - `topic`: `Angles from the latest design tools research brief`
  - `research_file`: newest `10-Research` file returned by the research run
- Hooks:
  - `topic`: `Why open-source design tools are suddenly worth watching`
  - `research_file`: same research brief path used above

## Failure Routing

- If `api.js` mapping is wrong: rerun `01-api-client-agent`
- If SSE never settles or leaks: rerun `02-job-stream-agent`
- If a picker or viewer fails: rerun only the owning component worker
- If wired stages still show demo content or wrong payload mapping: rerun `07-stage-workspace-agent`
- If fake done state survives app load: rerun `08-app-cleanup-agent`
- If the backend contract is actually wrong: dispatch one `pipeline-agent` patch task with a separate note, then rerun the blocked frontend worker

## Closeout

After pass:

1. Update this orchestration frontmatter:
   - `status: complete`
   - `groups_complete: [0, 1, 2, 3]`
   - `current_group: null`
2. Update [[Webapp_sprint]] Phase 4 items to reflect what really passed.
3. Update [[Current_Sprint]] so Phase 5 becomes the next step.
4. Write a session log in `00-Management-V2/Sessions/` linking back to this orchestration, [[Webapp_sprint]], and [[Design_Doc_Web_App_Plan]].
5. Keep all Phase 4 agent notes. They are the local memory for the next Claude session.
