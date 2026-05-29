---
slug: phase5-distribution-multi-tab-5-skills
date: 2026-05-24
created: 2026-05-24
status: implemented-verification-deferred
current_group: null
groups_complete: [0,1,2,3,4]
specialists_involved: [frontend-agent]
tags: [orchestration, webapp-sprint, phase5, frontend, distribution, verification]
description: "Subagent-driven execution playbook for [[Webapp_sprint]] Phase 5. Each agent owns one task, writes its own memory note, self-verifies, and hands off to a final verification/eval gate."
verification_gap: "Group 4 static/build/lint/health checks passed. Group 4 browser/runtime checks (Outline runtime, Title runtime, Cascade runtime, Short-form runtime, Voice-cleanup runtime) were NOT run — deferred per user instruction to avoid burning real skill credits. Full-chain acceptance test required before status can be upgraded to complete. See [[2026-05-24_Webapp_Phase5_Distribution]] and phase5/99-Verification.md."
---

# Orchestration: Phase 5 Distribution Multi-Tab - [[Webapp_sprint]]

Implements: [[Webapp_sprint]]
References: [[Design_Doc_Web_App_Plan]], [[Current_Sprint]], [[2026-05-23_phase4-wire-5-stages]]
Modifies: [[Design-doc]]

## Reader + Action

Reader: Claude acting as the coordinator.

Action after reading: complete Phase 5 of [[Webapp_sprint]] using one-task subagents, per-agent memory, self-verification inside each task, and a read-only final eval gate.

## Prerequisite Gate

Do not start Phase 5 until Phase 4 is actually passing.

Minimum evidence before dispatch:

- `Design-doc/web/src/api.js` exists and is the only `fetch` caller in `Design-doc/web/src/`.
- `Design-doc/web/src/hooks/useJobStream.js` exists and settles cleanly.
- `Design-doc/web/src/VaultPicker.jsx`, `MarkdownViewer.jsx`, and `OutputBrowser.jsx` exist and are already in use by the wired Phase 4 stages.
- `research`, `ideation`, and `hooks` already run against the real backend.
- `trends` already renders the real vault markdown file.

If any of the above is false, stop and finish Phase 4 first. Phase 5 reuses that shared frontend infrastructure; it does not replace it.

## Definition Of Done

- `Design-doc/web/src/DistributionWorkspace.jsx` exists and owns Distribution tab routing through `#distribution/<tab>`.
- `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `TitleTab.jsx`, `CascadeTab.jsx`, `ShortFormTab.jsx`, and `VoiceCleanupTab.jsx` exist.
- The sidebar no longer exposes `title` and `outline` as standalone top-level pipeline views; Distribution is the single entry point for all five skills.
- `Design-doc/web/src/App.jsx` mounts `DistributionWorkspace` for `view === "distribution"` and no longer routes users into fake standalone Title or Outline workspaces.
- `Design-doc/web/src/Dashboard.jsx` sends the Outline card and CTA to `#distribution/outline`.
- Outline runs real backend behavior through `/api/pipeline/outline` and renders a real `06-Outlines` file.
- Title runs real backend behavior through `/api/pipeline/title` and renders a real `07-Titles` file.
- Cascade runs real backend behavior through `/api/pipeline/cascade` and renders a real `08-Distribution` bundle.
- Short-form runs real backend behavior through `/api/pipeline/short-form` and renders a real `09-Shorts` bundle.
- Voice-cleanup runs real backend behavior through `/api/pipeline/voice-cleanup` and returns either the original path (`inplace`) or a derived `_cleaned` sibling file.
- Phase 4 stages keep working; Phase 5 does not regress `trends`, `research`, `ideation`, or `hooks`.
- Final eval proves the full Distribution chain works from real vault inputs and `npm run build` plus `npm run lint` pass.

## Hard Boundaries

- Do not edit `skills/*.py`, `prompts/*.md`, or `Design-doc/server/*` unless a proven contract bug blocks Phase 5. If blocked, stop and dispatch one narrowly scoped `pipeline-agent` patch task instead of widening frontend scope.
- Do not pull in Phase 6 work: Dashboard recent-activity wiring, sidebar status dots, Brain wiring, health badge, TweaksPanel persistence changes, or 409 UX polish.
- Keep the existing visual language and layout. Phase 5 is wiring and compression, not redesign.
- Do not add a new router library or a new global state layer. Use the existing app view state plus URL hash behavior only where Phase 5 requires it.
- All frontend HTTP calls must continue to live in `Design-doc/web/src/api.js`.
- Reuse Phase 4 shared components and hooks instead of cloning parallel versions.
- Do not invent extra form fields just because the backend supports them. Backend-only optional fields such as `title` on Cascade/Short-form and `no_polish` on Outline stay out of scope unless a minimal field is clearly needed and does not widen the sprint.
- Do not leave dead top-level `title` or `outline` routes behind in the UI after Distribution becomes the single entry point.

## Shared Contract

### Distribution Tab -> Endpoint

| Distribution tab | Backend behavior | Notes |
|---|---|---|
| `outline` | `POST /api/pipeline/outline` | Body is `{ topic, hook_path, length, platform }`. No `research_file` field in the UI. |
| `title` | `POST /api/pipeline/title` | Body is `{ concept }`. |
| `cascade` | `POST /api/pipeline/cascade` | UI supports either vault inputs (`research_file`, `outline_file`) or `youtube_url`. Backend also allows optional `title`, but Phase 5 may omit it. |
| `short-form` | `POST /api/pipeline/short-form` | Same body shape as Cascade. |
| `voice-cleanup` | `POST /api/pipeline/voice-cleanup` | Body is `{ file_path, inplace }`. |

### Distribution Tab -> Vault Folder

| Distribution tab | Folder | Used for |
|---|---|---|
| `outline` | `06-Outlines` | output + history |
| `title` | `07-Titles` | output + history |
| `cascade` | `08-Distribution` | bundle output + history |
| `short-form` | `09-Shorts` | bundle output + history |
| `voice-cleanup` | selected output folder | returns either the same file path (`inplace`) or a sibling `_cleaned` file |

### Picker Sources

| UI surface | Source folder(s) | Notes |
|---|---|---|
| Outline hook picker | `05-Hooks` | optional hook context |
| Cascade research picker | `10-Research` | real research artifact only |
| Cascade outline picker | `06-Outlines` | created by Outline or existing vault history |
| Short-form research picker | `10-Research` | real research artifact only |
| Short-form outline picker | `06-Outlines` | created by Outline or existing vault history |
| Voice-cleanup file picker | readable markdown outputs across `02-Ideas`, `05-Hooks`, `06-Outlines`, `07-Titles`, `08-Distribution`, `09-Shorts`, `10-Research` | submit one concrete file path; for bundles, choose a member markdown file such as `README.md` |

### Result Contract

- Outline, Title, and Voice-cleanup resolve to `{result_type, primary_path, outputs[], data}` with `result_type: "file"`.
- Cascade and Short-form resolve to `result_type: "bundle"` and should open `primary_path` by default while still exposing other markdown members.
- `GET /api/vault/file` returns `{path, content}`.
- `GET /api/vault/outputs` returns readable members for a file or bundle path.
- `GET /api/vault/recent` returns newest-first items with `name`, `path`, and `modified`.
- The backend still enforces one active job at a time. Phase 5 should not break on a `409`; full UX polish for that stays in Phase 6.

## Agent Memory Contract

Create `Design-doc/web/src/.agent-context/phase5/` before dispatching workers.

Every worker writes exactly one note:

- `00-Contract.md`
- `01-DistributionShell.md`
- `02-OutlineTab.md`
- `03-TitleTab.md`
- `04-CascadeTab.md`
- `05-ShortFormTab.md`
- `06-VoiceCleanupTab.md`
- `07-SidebarNav.md`
- `08-AppRouting.md`
- `09-DashboardLink.md`
- `99-Verification.md`

Memory note template:

```md
---
date: 2026-05-24
type: phase5-agent-note
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

1. Read [[Webapp_sprint]], [[Design_Doc_Web_App_Plan]], [[2026-05-23_phase4-wire-5-stages]], `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/Dashboard.jsx`, and `Design-doc/web/src/StageWorkspace.jsx`.
2. Confirm the Phase 4 prerequisite gate is genuinely satisfied.
3. Create `Design-doc/web/src/.agent-context/phase5/`.
4. Run Group 0 first.
5. Run Group 1 only after Group 0 lands a contract memo.
6. Run Group 2 in parallel only after Group 1 lands the tab-shell and hash-routing contract.
7. After Group 2, run `npm run build` and `npm run lint` in `Design-doc/web/`.
8. Run Group 3 sequentially. After each agent, rerun `npm run build`. After Group 3 completes, rerun both build and lint.
9. Start or confirm the backend on port `8765` and the frontend on port `5173`.
10. Run Group 4 as a read-only eval pass. If it fails, do not patch in the verifier. Re-dispatch only the failing worker.
11. Only after Group 4 passes: update [[Webapp_sprint]], update [[Current_Sprint]], write the Phase 5 implementation session log, and mark this orchestration `status: complete`.

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
- Task: write a Phase 5 contract memo so later workers use the same tab ordering, endpoint mapping, hash routing, and folder rules.
- Read: `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/StageWorkspace.jsx`
- Edit: `Design-doc/web/src/.agent-context/phase5/00-Contract.md`
- Must capture:
  - Distribution tab order is `outline -> title -> cascade -> short-form -> voice-cleanup`
  - URL hash format is `#distribution/<tab>`
  - top-level `title` and `outline` views leave the sidebar and fold into Distribution
  - Outline does not expose `research_file`
  - the allowed Phase 5 folders are `06-Outlines`, `07-Titles`, `08-Distribution`, `09-Shorts`, plus concrete picked file paths for Voice-cleanup
  - only `api.js` may use `fetch`
- Self-verification:
  - memo includes a tab-to-endpoint table
  - memo includes a picker/folder table
  - memo includes the rule that Phase 6 work stays out of scope

## Group 1 - Distribution Shell

### `01-distribution-shell-agent`

- Type: `frontend-agent`
- Task: create the Distribution workspace shell and hash-routing behavior
- Read: `Design-doc/web/src/App.jsx`, `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/StageWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`
- Edit: `Design-doc/web/src/DistributionWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Deliver:
  - tab bar in this exact order: `Outline`, `Title`, `Cascade`, `Short-form`, `Voice-cleanup`
  - active tab derived from `#distribution/<tab>`
  - invalid or missing Distribution hash falls back to `outline`
  - tab choice persists on refresh and when re-entering the Distribution view
  - each tab mounts its own component from `Design-doc/web/src/DistributionTabs/`
- Self-verification:
  - `#distribution/title` selects the Title tab
  - `#distribution/not-real` falls back to Outline
  - no raw `fetch`
  - shell does not absorb the per-tab form and job logic owned by later workers

## Group 2 - Parallel Tab Workers

### `02-outline-tab-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/DistributionTabs/OutlineTab.jsx`, `Design-doc/web/src/.agent-context/phase5/02-OutlineTab.md`
- Deliver:
  - collects `topic`, optional `hook_path`, `length`, and `platform`
  - uses `VaultPicker` against `05-Hooks`
  - posts exact body shape for Outline
  - shows live logs while the job runs
  - renders the final file result through `OutputBrowser`
- Must not do:
  - add `research_file`
  - widen the form with extra advanced toggles
- Self-verification:
  - request body contains `topic`, `hook_path`, `length`, and `platform`
  - no `research_file` field appears in the UI or request body
  - result renders a real `06-Outlines` file
  - no raw `fetch`

### `03-title-tab-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/DistributionTabs/TitleTab.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/DistributionTabs/TitleTab.jsx`, `Design-doc/web/src/.agent-context/phase5/03-TitleTab.md`
- Deliver:
  - collects `concept` only
  - posts exact body shape for Title
  - shows live logs while the job runs
  - renders the final file result through `OutputBrowser`
- Self-verification:
  - no hook, research, outline, or URL fields appear
  - request body is `{ concept }`
  - result renders a real `07-Titles` file
  - no raw `fetch`

### `04-cascade-tab-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/DistributionTabs/CascadeTab.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/DistributionTabs/CascadeTab.jsx`, `Design-doc/web/src/.agent-context/phase5/04-CascadeTab.md`
- Deliver:
  - supports vault-input mode with `research_file` plus `outline_file`
  - supports alternate URL mode with `youtube_url`
  - reuses Phase 4 output browsing for bundle results
  - shows live logs while the job runs
- Must not do:
  - require users to fill both picker mode and URL mode at the same time
  - widen scope into dashboard or sidebar work
- Self-verification:
  - bundle output opens `primary_path` by default
  - request body is valid in picker mode and URL mode
  - result resolves to a real `08-Distribution` bundle
  - no raw `fetch`

### `05-short-form-tab-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/DistributionTabs/ShortFormTab.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/DistributionTabs/ShortFormTab.jsx`, `Design-doc/web/src/.agent-context/phase5/05-ShortFormTab.md`
- Deliver:
  - same input modes as Cascade
  - bundle output rendered through `OutputBrowser`
  - clear support for the generated short-form markdown members
  - shows live logs while the job runs
- Self-verification:
  - request body is valid in picker mode and URL mode
  - result resolves to a real `09-Shorts` bundle
  - `primary_path` opens first
  - no raw `fetch`

### `06-voice-cleanup-tab-agent`

- Type: `frontend-agent`
- Task: create `Design-doc/web/src/DistributionTabs/VoiceCleanupTab.jsx`
- Read: `Design-doc/web/src/api.js`, `Design-doc/web/src/hooks/useJobStream.js`, `Design-doc/web/src/VaultPicker.jsx`, `Design-doc/web/src/OutputBrowser.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/DistributionTabs/VoiceCleanupTab.jsx`, `Design-doc/web/src/.agent-context/phase5/06-VoiceCleanupTab.md`
- Deliver:
  - file picker for readable markdown outputs across the approved source folders
  - `inplace` toggle
  - exact `voice-cleanup` body mapping
  - result rendered through `OutputBrowser`
- Must do:
  - support selecting a concrete markdown file from a bundle
  - handle both `inplace: true` and `inplace: false`
- Self-verification:
  - request body is `{ file_path, inplace }`
  - `inplace` returns the original path
  - non-inplace returns a `_cleaned` sibling file path or the stdout-reported path
  - no raw `fetch`

## Group 3 - Sequential Integration

### `07-sidebar-nav-agent`

- Type: `frontend-agent`
- Task: collapse Title and Outline into the single Distribution sidebar entry
- Read: `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/.agent-context/phase5/00-Contract.md`
- Edit: `Design-doc/web/src/Sidebar.jsx`, `Design-doc/web/src/.agent-context/phase5/07-SidebarNav.md`
- Must do:
  - remove top-level `title` and `outline` pipeline items
  - keep Distribution as the single top-level entry for the five skills
  - preserve the earlier stage order for `trends`, `research`, `ideation`, and `hooks`
- Self-verification:
  - no dead `title` or `outline` nav buttons remain
  - `distribution` still navigates correctly
  - no unrelated Brain or Settings changes

### `08-app-routing-agent`

- Type: `frontend-agent`
- Task: wire `App.jsx` to the new Distribution workspace and remove dead standalone routes
- Read: `Design-doc/web/src/App.jsx`, `Design-doc/web/src/DistributionWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/App.jsx`, `Design-doc/web/src/.agent-context/phase5/08-AppRouting.md`
- Must do:
  - mount `DistributionWorkspace` for `view === "distribution"`
  - remove standalone Title and Outline workspace routes
  - remove fake completed-state seed data tied to the old Title and Outline views
  - keep `dashboard`, `trends`, `research`, `ideation`, `hooks`, `distribution`, `brain`, and `settings` navigation intact
  - update any jump-list or view-select options so users are not sent to removed standalone screens
- Self-verification:
  - `App.jsx` no longer routes `title` or `outline` as separate screens
  - `distribution` loads the shell
  - no Phase 4 routes regress
  - no raw `fetch`

### `09-dashboard-link-agent`

- Type: `frontend-agent`
- Task: point the Dashboard Outline card to the Outline tab inside Distribution
- Read: `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/DistributionWorkspace.jsx`, `Design-doc/web/src/.agent-context/phase5/01-DistributionShell.md`
- Edit: `Design-doc/web/src/Dashboard.jsx`, `Design-doc/web/src/.agent-context/phase5/09-DashboardLink.md`
- Must do:
  - card click opens Distribution with hash `#distribution/outline`
  - CTA button does the same
  - leave the rest of the Dashboard activity mocks alone for now
- Self-verification:
  - Outline card click and CTA both land on the Outline tab
  - non-Outline cards keep their current behavior
  - no Phase 6 recent-activity work slips in

## Group 4 - Final Eval Gate

### `99-verification-agent`

- Type: `verification-agent`
- Task: run a read-only end-to-end eval of Phase 5 and decide pass or rerun
- Read: all edited Distribution files, all Phase 5 agent notes, `Design-doc/server/main.py`, `Design-doc/server/pipeline.py`, and any Phase 4 shared frontend infra the Distribution tabs depend on
- Edit only after full pass:
  - `Design-doc/web/src/.agent-context/phase5/99-Verification.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Webapp_sprint.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`
- Read-only if failing:
  - do not patch source files
  - write a fail report naming the exact worker that must rerun
- Eval checklist:
  - static:
    - `rg "fetch\\(" Design-doc/web/src` shows only `api.js`
    - `Sidebar.jsx` no longer exposes top-level `title` or `outline`
    - `App.jsx` mounts `DistributionWorkspace` and no longer routes standalone Title or Outline screens
    - `DistributionWorkspace.jsx` recognizes all 5 tabs and falls back invalid hashes to Outline
    - Outline UI does not expose `research_file`
  - build:
    - `npm run build`
    - `npm run lint`
  - API:
    - backend health returns `{status:"ok", backend:"up", capabilities:null}`
    - Outline, Title, Cascade, Short-form, and Voice-cleanup endpoints all return `{job_id}`
  - browser or live runtime:
    - open `http://localhost:5173`
    - navigate to Distribution and confirm the tab bar order
    - Dashboard Outline card lands on `#distribution/outline`
    - Outline run shows live log lines, then renders a real file from `06-Outlines`
    - Title run shows live log lines, then renders a real file from `07-Titles`
    - Cascade run renders a real bundle from `08-Distribution`
    - Short-form run renders a real bundle from `09-Shorts`
    - Voice-cleanup run works against a real markdown artifact and renders the returned file path
- Pass rule:
  - every check above passes
  - only then mark Phase 5 items complete in [[Webapp_sprint]]
  - only then update [[Current_Sprint]] so Phase 6 becomes the next step

## Exact Verification Payloads

Use small repeatable payloads so the eval stays deterministic:

- Preconditions:
  - newest `10-Research` file exists from a real Phase 4 research run
  - newest `05-Hooks` file exists from a real Phase 4 hooks run
- Outline:
  - `topic`: `Why open-source design tools are suddenly worth watching`
  - `hook_path`: newest `05-Hooks` file
  - `length`: `8`
  - `platform`: `yt-long`
- Title:
  - `concept`: `Why open-source design tools are suddenly worth watching`
- Cascade:
  - picker mode first
  - `research_file`: newest `10-Research` file
  - `outline_file`: outline output created above
  - `youtube_url`: empty
- Short-form:
  - `research_file`: same research brief path
  - `outline_file`: same outline path
  - `youtube_url`: empty
- Voice-cleanup:
  - `file_path`: `README.md` from the Cascade bundle if present, otherwise the first readable markdown member from the Short-form bundle
  - `inplace`: `false`

## Failure Routing

- If hash routing or tab fallback is wrong: rerun `01-distribution-shell-agent`
- If Outline payloads or picker wiring are wrong: rerun `02-outline-tab-agent`
- If Title payloads or rendering are wrong: rerun `03-title-tab-agent`
- If Cascade mode switching or bundle rendering is wrong: rerun `04-cascade-tab-agent`
- If Short-form mode switching or bundle rendering is wrong: rerun `05-short-form-tab-agent`
- If Voice-cleanup path selection or return-path handling is wrong: rerun `06-voice-cleanup-tab-agent`
- If top-level nav collapse is wrong: rerun `07-sidebar-nav-agent`
- If Distribution routing or removed standalone routes are wrong: rerun `08-app-routing-agent`
- If the Dashboard link target is wrong: rerun `09-dashboard-link-agent`
- If the backend contract is actually wrong: dispatch one `pipeline-agent` patch task with a separate note, then rerun the blocked frontend worker

## Closeout

After pass:

1. Update this orchestration frontmatter:
   - `status: complete`
   - `groups_complete: [0, 1, 2, 3, 4]`
   - `current_group: null`
2. Update [[Webapp_sprint]] Phase 5 items to reflect what really passed.
3. Update [[Current_Sprint]] so Phase 6 becomes the next step.
4. Write a session log in `00-Management-V2/Sessions/` linking back to this orchestration, [[Webapp_sprint]], and [[Design_Doc_Web_App_Plan]].
5. Keep all Phase 5 agent notes. They are the local memory for the next Claude session.
