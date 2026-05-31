---
slug: phase7-launch-e2e-acceptance
date: 2026-05-29
created: 2026-05-29
status: complete
current_group: null
groups_complete: [0, 1, 2, 3, 4, 5]
completed: 2026-05-29
specialists_involved: [webapp-agent, vault-agent]
tags: [orchestration, webapp-sprint, phase7, launch, e2e, verification]
description: "Execution playbook for [[Webapp_sprint]] Phase 7: launcher script, full UI acceptance chain, Brain check, 409 check, and sprint closeout evidence."
---

# Orchestration: Phase 7 Launch + E2E Acceptance - [[Webapp_sprint]]

Implements: [[Webapp_sprint]] Phase 7
References: [[Design_Doc_Web_App_Plan]], [[Current_Sprint]], [[2026-05-29_Phase5_FullChain_Verification]], [[2026-05-24_phase6-dashboard-brain-polish]]
Modifies: [[Design-doc]], [[Webapp_sprint]], [[Current_Sprint]]

## Reader + Action

Reader: Claude acting as the Phase 7 coordinator.

Action after reading: finish Phase 7 of [[Webapp_sprint]] by adding the launch convenience script, running the whole app through the browser-facing acceptance chain, recording evidence, and closing the sprint docs only after the acceptance gate passes.

## Prerequisite Gate

Do not start implementation until these facts are true:

- [[Webapp_sprint]] Phase 5 is complete and [[2026-05-29_Phase5_FullChain_Verification]] exists.
- [[Webapp_sprint]] Phase 6 is complete and [[2026-05-24_phase6-dashboard-brain-polish]] exists.
- `Design-doc/README.md` already contains the current backend and frontend quickstart commands.
- `Design-doc/web/src/api.js` is still the only frontend file using `fetch`.
- `npm run build` and `npm run lint` are clean before the E2E acceptance run begins.

If any item fails, stop and repair the owning earlier phase first. Phase 7 is the final gate, not a place to absorb unfinished Phase 4-6 wiring.

## Definition Of Done

- `Design-doc/start.ps1` launches FastAPI and Vite in separate PowerShell windows from the repo root.
- The launcher uses the repo root `.venv` for FastAPI; it does not create or assume `Design-doc/server/.venv`.
- Both servers are reachable: FastAPI on `http://localhost:8765/api/health`, Vite on `http://localhost:5173`.
- A fresh topic runs through the UI-facing chain: Research -> Ideation -> Hooks -> Distribution tabs in this order: Outline -> Title -> Cascade -> Short-form -> Voice-cleanup.
- Every run shows live SSE log movement and settles without an infinite spinner.
- Every completed stage renders real vault markdown or bundle output through the UI, not demo content.
- Acceptance evidence records the expected Phase 7 surface rows: Trends source, Research, Ideation, Hooks, Outline, Title, Cascade, Short-form, Voice-cleanup.
- Brain returns a real analysis from pasted content through `/api/brain/analyze`.
- A second concurrent run returns a graceful 409 UI state.
- Dashboard recent activity and sidebar status dots reflect the fresh run.
- `Design-doc/web/src/.agent-context/phase7/99-Acceptance.md` captures the evidence.
- [[Webapp_sprint]], [[Current_Sprint]], and the mandatory final session log are updated only after the acceptance gate passes.

## Hard Boundaries

- Do not edit `skills/*.py`, `prompts/*.md`, or the vault pipeline folders during Phase 7 unless an acceptance failure proves the webapp wrapper is blocked by a real pipeline bug.
- Do not redesign UI surfaces. This phase verifies the wired app.
- Do not add a database, auth, publishing automation, or parallel job execution.
- Do not change the single-job constraint. The 409 behavior is part of acceptance.
- Do not mark the sprint complete if browser-facing verification is skipped.
- Do not fabricate evidence. If a manual browser step cannot be run, leave it explicitly open.

## Shared Contract

### Launch Contract

| Item | Contract |
|---|---|
| Script | `Design-doc/start.ps1` |
| Backend command | `.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload` from repo root |
| Frontend command | `npm run dev` from `Design-doc/web/` |
| Windows behavior | Launch backend and frontend in separate PowerShell windows |
| Health check | `GET http://localhost:8765/api/health` returns `{status:"ok", backend:"up", capabilities:null}` |
| App URL | `http://localhost:5173` |

The script should fail early with readable messages if the repo `.venv`, `Design-doc/web/node_modules`, or required directories are missing.

### Acceptance Topic

Use one fresh topic for the full chain so recents, status dots, and vault outputs can be tied together.

Recommended topic:

```text
Why local-first AI workbenches are becoming the default for serious creators
```

If a stage needs an existing research file to avoid burning extra research credits, record the selected file and mark the run as "E2E with seeded research" instead of "fresh-topic full chain."

### Stage Acceptance Matrix

| Surface | Expected action | Expected evidence |
|---|---|---|
| Trends | Load read-only workspace | Current trends markdown renders from `04-Trends/` |
| Research | Run with niche/topic and repo inputs | New or intentionally seeded research file in `10-Research/`; SSE logs move |
| Ideation | Pick research file, run topic | New file in `02-Ideas/`; rendered in OutputBrowser |
| Hooks | Pick research file, run topic | New file in `05-Hooks/`; rendered in OutputBrowser |
| Outline | Open Distribution -> Outline | New file in `06-Outlines/`; no `research_file` request body |
| Title | Open Distribution -> Title | New file in `07-Titles/` |
| Cascade | Use research + outline or YouTube URL | Bundle in `08-Distribution/`; README opens by default |
| Short-form | Use research + outline or YouTube URL | Bundle in `09-Shorts/`; README opens by default |
| Voice-cleanup | Clean one generated markdown file | Cleaned file or in-place edited file renders correctly |
| Brain | Paste content and analyze | Real `brain_result` payload renders all five fields |
| 409 | Start a second job while one runs | UI explains another job is already running |

## Agent Memory Contract

Create `Design-doc/web/src/.agent-context/phase7/` before dispatching workers.

Every worker writes exactly one note:

- `00-Contract.md`
- `01-Launcher.md`
- `02-Preflight.md`
- `03-FullChainUi.md`
- `04-BrainAndConflict.md`
- `05-CloseoutDocs.md`
- `99-Acceptance.md`

Memory note template:

```md
---
date: 2026-05-29
type: phase7-agent-note
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
## Evidence
## Open Items
```

Rules:

- One agent, one task, one note.
- If blocked, set `status: blocked`, document the blocker, and stop.
- The coordinator reads the note before advancing.
- The final verifier is read-only. If it fails, re-dispatch the owning worker instead of patching inside the verifier.

## Coordinator Protocol

1. Read [[Webapp_sprint]], [[Design_Doc_Web_App_Plan]], [[2026-05-29_Phase5_FullChain_Verification]], [[2026-05-24_phase6-dashboard-brain-polish]], `Design-doc/README.md`, `Design-doc/server/runtime.md`, and the relevant webapp entry files.
2. Confirm the prerequisite gate.
3. Create `Design-doc/web/src/.agent-context/phase7/`.
4. Run Group 0 first.
5. Run Group 1 to create or fix `Design-doc/start.ps1`.
6. Run Group 2 static/build/preflight verification.
7. Start the app with `Design-doc/start.ps1` and confirm both ports.
8. Run Group 3 full-chain UI acceptance.
9. Run Group 4 Brain and 409 acceptance.
10. Run Group 5 read-only final acceptance. If it fails, route back to the owning group.
11. Only after Group 5 passes: update [[Webapp_sprint]], update [[Current_Sprint]], write `YYYY-MM-DD_Design_Doc_Web_App_Wired.md`, and mark this orchestration `status: complete`.

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
- evidence paths
- open concerns
```

## Group 0 - Contract Memo

### `00-contract-agent`

- Type: `webapp-agent`
- Task: write the Phase 7 contract memo so later workers use the same launcher commands and acceptance matrix.
- Read: `Design-doc/README.md`, `Design-doc/server/runtime.md`, `Design-doc/web/package.json`, [[Webapp_sprint]], [[Design_Doc_Web_App_Plan]]
- Edit: `Design-doc/web/src/.agent-context/phase7/00-Contract.md`
- Must capture:
  - launcher command contract
  - acceptance topic
  - stage acceptance matrix
  - rule that Brain is separate from vault artifacts
  - rule that final docs update only after acceptance passes
- Self-verification:
  - memo includes launcher commands
  - memo includes all Stage Acceptance Matrix rows
  - memo names the final closeout files

## Group 1 - Launch Convenience

### `01-launcher-agent`

- Type: `webapp-agent`
- Task: create `Design-doc/start.ps1`.
- Read: `Design-doc/README.md`, `Design-doc/server/runtime.md`, `Design-doc/web/package.json`, `Design-doc/web/src/.agent-context/phase7/00-Contract.md`
- Edit: `Design-doc/start.ps1`, `Design-doc/web/src/.agent-context/phase7/01-Launcher.md`
- Deliver:
  - validates it is running from the repo root or resolves the repo root from the script path
  - checks `.venv\Scripts\python.exe`
  - checks `Design-doc/web/node_modules`
  - starts backend in one PowerShell window
  - starts frontend in one PowerShell window
  - prints the frontend URL and health URL
- Self-verification:
  - `powershell -NoProfile -ExecutionPolicy Bypass -File Design-doc/start.ps1 -WhatIf` or equivalent dry-run path if implemented
  - commands match `Design-doc/README.md`
  - no hardcoded user-only path beyond resolving from script location

## Group 2 - Preflight

### `02-preflight-agent`

- Type: `webapp-agent`
- Task: prove the app is ready for acceptance before burning full-chain runtime.
- Read: `Design-doc/web/src/.agent-context/phase7/00-Contract.md`, `Design-doc/web/src/.agent-context/phase7/01-Launcher.md`
- Edit: `Design-doc/web/src/.agent-context/phase7/02-Preflight.md`
- Run:
  - `rg "fetch\\(" Design-doc/web/src`
  - `npm run build` in `Design-doc/web/`
  - `npm run lint` in `Design-doc/web/`
  - `GET /api/health` after launching backend
- Self-verification:
  - build passes
  - lint passes
  - `fetch` remains isolated to `api.js`
  - health endpoint returns the v1 contract

## Group 3 - Full-Chain UI Acceptance

### `03-full-chain-ui-agent`

- Type: `webapp-agent`
- Task: run the browser-facing full chain and record evidence.
- Read: `Design-doc/web/src/.agent-context/phase7/00-Contract.md`, `Design-doc/web/src/.agent-context/phase7/02-Preflight.md`
- Edit: `Design-doc/web/src/.agent-context/phase7/03-FullChainUi.md`
- Run through UI:
  - Trends
  - Research
  - Ideation
  - Hooks
  - Distribution -> Outline
  - Distribution -> Title
  - Distribution -> Cascade
  - Distribution -> Short-form
  - Distribution -> Voice-cleanup
- Must capture:
  - topic used
  - exact input files selected
  - output path or bundle path for each completed stage
  - whether SSE lines visibly moved
  - whether OutputBrowser rendered the result
  - dashboard recent activity after the run
  - sidebar status behavior during and after at least one run
- Self-verification:
  - all expected vault artifact rows have evidence
  - no demo output observed
  - no spinner remains after a completed job

## Group 4 - Brain + Conflict Acceptance

### `04-brain-conflict-agent`

- Type: `webapp-agent`
- Task: verify the non-pipeline acceptance items.
- Read: `Design-doc/web/src/.agent-context/phase7/00-Contract.md`, `Design-doc/web/src/.agent-context/phase7/03-FullChainUi.md`
- Edit: `Design-doc/web/src/.agent-context/phase7/04-BrainAndConflict.md`
- Run:
  - paste representative content into Brain and confirm a real `brain_result`
  - start a long enough job, attempt a second submission, and confirm graceful 409 UI copy
- Must capture:
  - Brain input excerpt or source path
  - returned payload fields
  - 409 UI behavior
- Self-verification:
  - Brain renders `hook_quality`, `structure_score`, `emotional_triggers`, `techniques_to_steal`, and `replication_template`
  - 409 is human-readable, not a raw stack trace

## Group 5 - Final Eval + Closeout Docs

### `99-acceptance-agent`

- Type: `vault-agent`
- Task: run a read-only final acceptance pass over all Phase 7 evidence.
- Read: all `Design-doc/web/src/.agent-context/phase7/*.md`, [[Webapp_sprint]], [[Current_Sprint]]
- Edit only after pass: `Design-doc/web/src/.agent-context/phase7/99-Acceptance.md`, [[Webapp_sprint]], [[Current_Sprint]], final session log
- Acceptance:
  - launcher evidence present
  - build/lint/health evidence present
  - all stage rows have output evidence
  - Brain evidence present
  - 409 evidence present
  - dashboard and sidebar evidence present
- If pass:
  - mark Phase 7 complete in [[Webapp_sprint]]
  - mark the webapp sprint complete in [[Current_Sprint]]
  - write `Content-Hub-Vault-V2/00-Management-V2/Sessions/YYYY-MM-DD_Design_Doc_Web_App_Wired.md`
  - mark this orchestration `status: complete`
- If fail:
  - write `99-Acceptance.md` with `status: blocked`
  - do not mark sprint complete
  - name the owning failed group
