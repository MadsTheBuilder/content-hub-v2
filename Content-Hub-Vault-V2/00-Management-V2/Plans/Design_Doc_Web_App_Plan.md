---
status: Approved (corrected after Claude/Opus review; reconciled with prototype updates 2026-05-22)
date: "2026-05-22"
date_approved: "2026-05-22"
updated: "2026-05-22"
type: Build Plan
description: "Build plan to wire the Design-doc React prototype into a fully working Content Hub V2 web app: Vite+React frontend + FastAPI subprocess orchestrator for the 8 pipeline skills."
tags:
  - plan
  - web-app
  - design-doc
  - vite
  - react
  - fastapi
  - pipeline
  - mvp
supersedes:
  - "[[Content_Hub_Web_Design_Spec]]"
  - "[[Wrapper_Plan]]"
implements: "[[Local_First_Skill_Engine_Plan]]"
modifies:
  - "[[Design-doc]]"
references:
  - "[[researcher]]"
  - "[[ideation]]"
  - "[[hook]]"
  - "[[outline]]"
  - "[[title]]"
  - "[[cascade]]"
  - "[[short-form]]"
  - "[[voice-cleanup]]"
  - "[[2026-05-22_Codex_Plan_Reviewer_Webapp]]"
  - "[[2026-05-22_Codex_Webapp_Brainstorm]]"
  - "[[Codex_Webapp_Brainstorm_Handoff]]"
---

# Design-doc Web App Build Plan

## Context

`Design-doc/Content Hub/` contains a complete React 18 (CDN + Babel Standalone) prototype with all UI surfaces designed: sidebar nav, dashboard, 5 stage workspaces, Knowledge Brain workspace, tweaks panel, particle background. It is pixel-finished but every output is hardcoded demo content — nothing is wired to the actual pipeline.

Meanwhile, the 8 pipeline skills ([[researcher]], [[ideation]], [[hook]], [[outline]], [[title]], [[cascade]], [[short-form]], [[voice-cleanup]]) already work as runnable Python modules via `python -m skills.<name>`. Each writes Markdown into a specific `Content-Hub-Vault-V2/` folder.

**Goal:** Make Design-doc a fully working web app where every button actually runs its corresponding skill against the local pipeline, streams logs live, and renders the resulting vault artifact in the UI.

**Conflict resolved:** The earlier [[Content_Hub_Web_Design_Spec]] and [[Wrapper_Plan]] scope a Streamlit dashboard. The Design-doc/ prototype is React, and the user has chosen to continue on that path. **This plan supersedes both Streamlit planning docs.**

**Locked decisions (from user, 2026-05-22):**
1. **Frontend:** Vite + React (JavaScript, no TypeScript). Port `.jsx` files into a real Vite project.
2. **Pipeline mapping:** Compress — Distribution becomes a multi-tab workspace holding Outline / Title / Cascade / Short-form / Voice-cleanup tabs. Sidebar stays at 5 items.
3. **v1 scope:** Functional MVP — every stage runs its skill, streams logs, and renders normalized output metadata from the backend.
4. **Result contract:** No single `vault_path` assumption. Jobs return `{result_type, primary_path, outputs[]}` where v1 emits `file` or `bundle`; `file_set` is reserved for future multi-file outputs that are not directory bundles.
5. **Outline flow:** Research feeds Ideation and Hooks; Outline derives downstream from topic/hook context. Do not send `research_file` to `skills.outline` unless that skill is explicitly changed.
6. **Runtime:** The FastAPI wrapper runs in the repo's existing Python environment for v1. Do not create a separate minimal `Design-doc/server/.venv`.
7. **Vault/Supabase stance:** The vault remains the execution-layer source of truth. The web UI should read normalized backend metadata; Supabase, if added, stores web app state/job/output metadata above the vault, not instead of it.
8. **Brain v1:** Ship pasted-text analysis only. Remove URL chips and file-drop controls from the ported Brain UI for v1; revisit URL/file ingestion in v2.

**Runtime note (2026-05-22, post-Phase-1):** The Vite project bootstrapped in Phase 1 ships React 19.2.6 / react-dom 19.2.6 — newer than the prototype's CDN React 18 ([Content Hub.html](../../../Design-doc/Content%20Hub/Content%20Hub.html) loads `react@18.3.1`). This is the default for `npm create vite@latest` as of 2026-05-22. No code in this plan depends on React-18-only APIs; the ported components run unchanged.

**Prototype updates (2026-05-22):** Since this plan was first written, the prototype gained a new component `Design-doc/Content Hub/sources-panel.jsx` (794 lines, exports `SourcesPanel` + `StackedPanel`, consumed by `brain.jsx:118-120` and `stage-workspace.jsx:159-161`). The component list and Phase 1 / Phase 3 / Phase 4 instructions below have been updated to include it.

---

## Target Directory Structure

```
Design-doc/
├── Content Hub/                    # KEEP — original prototype, untouched as design reference
├── web/                            # NEW — Vite + React app (production frontend)
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js              # proxy /api to backend
│   ├── public/
│   └── src/
│       ├── main.jsx                # Vite entry
│       ├── App.jsx                 # ported from app.jsx
│       ├── styles.css              # ported, unchanged
│       ├── particles.js            # ported, called from App useEffect
│       ├── api.js                  # NEW — fetch helpers + SSE wrapper
│       ├── hooks/
│       │   └── useJobStream.js     # NEW — SSE hook for live logs
│       └── components/
│           ├── Sidebar.jsx
│           ├── Dashboard.jsx
│           ├── StageWorkspace.jsx          # generic 5-stage shell
│           ├── DistributionWorkspace.jsx   # NEW — multi-tab shell
│           ├── DistributionTabs/
│           │   ├── OutlineTab.jsx
│           │   ├── TitleTab.jsx
│           │   ├── CascadeTab.jsx
│           │   ├── ShortFormTab.jsx
│           │   └── VoiceCleanupTab.jsx
│           ├── Brain.jsx                   # wired to a simple Claude analysis call
│           ├── Icons.jsx
│           ├── SourcesPanel.jsx            # exports SourcesPanel + StackedPanel; vault file tree + sources panel — wired to /api/vault/recent in Phase 4
│           ├── TweaksPanel.jsx
│           ├── VaultPicker.jsx             # NEW — dropdown of recent vault files
│           ├── MarkdownViewer.jsx          # NEW — renders vault markdown output
│           └── OutputBrowser.jsx           # NEW — renders file, file_set, and bundle results
└── server/                         # NEW — FastAPI orchestration service
    ├── main.py                     # FastAPI app, port 8765
    ├── pipeline.py                 # per-skill subprocess wrappers
    ├── jobs.py                     # in-memory job registry + SSE event bus
    ├── vault.py                    # recent-artifact scanner + file reader
    ├── brain.py                    # Claude-direct analysis for Brain workspace
    └── runtime.md                  # notes for using the shared repo Python runtime
```

`Design-doc/Content Hub/` stays as the unmodified reference prototype. New work lives in `Design-doc/web/` and `Design-doc/server/`.

---

## Backend (FastAPI, port 8765)

A clean, thin orchestration service. **Does not touch** the existing `backend/main.py` at the project root (that is V1 SaaS scope per [[CLAUDE]] and would conflict with port 8000 + Supabase/auth concerns). For v1, run this service from the repo's existing Python environment so subprocessed skills inherit the same dependency surface as the working local pipeline.

### Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Minimum v1 response: `{status:"ok", backend:"up", capabilities:null}`. Capability checks can be added later without blocking implementation. |
| GET | `/api/vault/recent?folder=10-Research&limit=10` | List recent files in a vault folder, newest first |
| GET | `/api/vault/file?path=...` | Read a vault file's raw markdown (path must resolve inside `Content-Hub-Vault-V2/`) |
| GET | `/api/vault/outputs?path=...` | List readable members for a bundle directory or file set |
| POST | `/api/pipeline/researcher` | Body: `{niche, repos: [], mode}` → `{job_id}` |
| POST | `/api/pipeline/ideation` | Body: `{topic, research_file?, no_trends?}` |
| POST | `/api/pipeline/hook` | Body: `{topic, platform?, audience?, format?, research_file?, no_polish?}` |
| POST | `/api/pipeline/outline` | Body: `{topic, hook_path?, length?, platform?, no_polish?}` |
| POST | `/api/pipeline/title` | Body: `{concept}` |
| POST | `/api/pipeline/cascade` | Body: `{research_file, outline_file, title?}` or `{youtube_url}` |
| POST | `/api/pipeline/short-form` | Body: `{research_file, outline_file, title?}` or `{youtube_url}` |
| POST | `/api/pipeline/voice-cleanup` | Body: `{file_path, inplace?}` |
| POST | `/api/brain/analyze` | Body: `{content}` → triggers Claude analysis job, returns `{job_id}` |
| GET | `/api/jobs/{job_id}` | Returns job metadata: status, started_at, completed_at, result |
| GET | `/api/jobs/{job_id}/stream` | Server-Sent Events: line-by-line stdout/stderr + `done` event with final typed result |

### Job execution model

- **Single-job at a time** (matches V2 constraint: shared Claude quota + NotebookLM session). New job submission while another is running returns `409 Conflict` with current job id.
- In-memory job dict (`jobs.py`): `{job_id: {status, started_at, completed_at, result, stdout_buffer, stderr_buffer, subscribers}}`.
- `result` is typed metadata: `{result_type, primary_path, outputs[]}`.
- `result_type=file`: one primary markdown artifact.
- `result_type=file_set`: reserved for a future stage that returns multiple first-class files without a bundle directory; v1 resolvers do not emit it.
- `result_type=bundle`: a generated directory with member files; `primary_path` points to `README.md` if present, otherwise the first useful markdown file or the directory itself.
- Each pipeline POST launches `asyncio.create_subprocess_exec(sys.executable, "-m", "skills.<name>", ...args, cwd=PROJECT_ROOT)` from the shared repo Python environment.
- Stream stdout/stderr to per-job asyncio queues; SSE endpoint reads from queue.
- On exit-0: call the stage-specific output resolver. Do not depend on a generic `"Written to: <path>"` parser or newest-file fallback as the primary contract.
- For `voice_cleanup`, resolve the output directly from submitted `{file_path, inplace}` because in-place edits may not create a new file.
- Brain analysis shares the same single-job slot as pipeline runs for v1. A running researcher/cascade job blocks Brain with the same `409 Conflict` behavior.
- On non-zero exit: mark job `failed`, surface stderr.

### Wrapper: `pipeline.py`

One function per skill that builds the argv list:

```python
import sys

async def run_researcher(niche, repos, mode="deep"):
    args = [sys.executable, "-m", "skills.researcher", "--niche", niche,
            "--repos", *repos, "--mode", mode]
    return await launch_job("researcher", args, resolver=resolve_researcher_outputs)
```

Reuses existing skills exactly as-is — no skill code changes per [[CLAUDE]] § 3 Surgical Changes.

### Stage output resolvers

Normalize at the API boundary instead of changing vault conventions:

| Stage | Result type | Resolver rule | Extraction rule |
|---|---|---|---|
| `researcher` | `file` | Resolve the compiled brief in `10-Research/`. | Parse `Brief written to:\s*(.+\.md)` from stdout. Fallback to `10-Research/{today}_{niche.lower().replace(" ", "-")}_brief.md`; final fallback is newest matching `{today}_*_brief.md` modified after `started_at`. |
| `ideation` | `file` | Resolve `02-Ideas/{date}_{slug}.md`. | Parse `Output:\s*(.+\.md)` from stdout. Fallback to deterministic slug from `skills.ideation.make_output_path`: strip non-word chars, collapse spaces/underscores/hyphens to `-`, trim to 40 chars. |
| `hook` | `file` | Resolve `05-Hooks/{date}_{slug}.md`. | Parse `Hooks written to:\s*(.+\.md)` from stdout. Fallback to `skills.hook.make_slug(topic)`. |
| `outline` | `file` | Resolve `06-Outlines/{date}_{slug}.md`; inputs are topic/hook context, not raw `research_file`. | Parse `Outline written to:\s*(.+\.md)` from stdout. Fallback to `skills.outline.make_slug(topic)`. |
| `title` | `file` | Resolve `07-Titles/{date}_{slug}.md`. | Parse the final stdout line ending in `.md`. Fallback to title slug rule: lower-case concept, replace non-alphanumerics with `-`, trim to 50 chars. |
| `cascade` | `bundle` | Resolve `08-Distribution/{date}_{slug}/`; list markdown members and prefer `README.md` as primary. | Parse the line after `Distribution package written to:`. Fallback to deterministic slug from `skills.cascade.make_output_dir`: strip non-word chars, collapse spaces/underscores/hyphens to `-`, trim to 40 chars. |
| `short-form` | `bundle` | Resolve `09-Shorts/{date}_{slug}/`; list 30s/60s/90s scripts and prefer `README.md` if present. | Parse the line after `Short-form package written to:`. Fallback to deterministic slug from `skills.short_form.make_output_dir`: strip non-word chars, collapse spaces/underscores/hyphens to `-`, trim to 40 chars. |
| `voice-cleanup` | `file` | If `inplace`, return submitted `file_path`; otherwise return the derived cleaned file path. | Do not glob. If `inplace`, return `file_path`; otherwise return sibling path with `_cleaned` before the extension. Optionally verify against `Output:\s*(.+\.md)` from stdout. |

Future hardening can add a `--json` completion mode to skills, but v1 should not rewrite the vault artifact layout to make the web wrapper easier.

### Critical existing files referenced (do not modify)

- `skills/researcher.py` — invoked via `python -m skills.researcher`
- `skills/ideation.py`
- `skills/hook.py`
- `skills/outline.py`
- `skills/title.py`
- `skills/cascade.py`
- `skills/short_form.py`
- `skills/voice_cleanup.py`
- `skills/utils/ai.py` — used transparently by skills for Claude-first cascade (see [[2026-05-19_Pipeline_Bug_Fix_Claude_First]])
- `Content-Hub-Vault-V2/04-Trends/github_trending.md` — researcher prerequisite

---

## Frontend (Vite + React JS)

### Port from `Content Hub/` → `web/src/`

1. **`Content Hub.html` → `web/index.html`**: strip the CDN React / Babel / Lucide `<script>` tags and the inline `<script src="particles.js">` tag — Vite injects the bundle from `main.jsx` and the particles module is imported by `App.jsx`. Keep only the `<div id="root">` mount point. **Do not add a `<canvas>` element**: `particles.js` creates its own `<canvas id="__particles">` dynamically on mount (the prototype HTML has no canvas either; the canvas appears at runtime).
2. **`app.jsx` → `App.jsx`**: add explicit React imports (`import { useState, useEffect, useCallback } from 'react'`). Wrap component exports with `export default`. The CDN version relied on global `React`.
3. **`dashboard.jsx`, `stage-workspace.jsx`, `brain.jsx`, `sidebar.jsx`, `icons.jsx`, `tweaks-panel.jsx`, `sources-panel.jsx`**: same treatment — add imports, export default. **Replace the hardcoded demo data with state filled by API responses**: `OUTPUTS[stageId]` inside `stage-workspace.jsx`, and the `VAULT_DATA` constant inside `sources-panel.jsx` (per-stage `tree` and `sources` blocks) — both should be driven by `getRecent(<stage folder>)` once the API is wired in Phase 4. The `sources-panel.jsx` port additionally needs the CDN-globals fix (`window.SourcesPanel = …` → `export { SourcesPanel, StackedPanel }`) plus a `import { useState } from 'react'`.
4. **`styles.css`**: copy as-is, import from `main.jsx`.
5. **`particles.js`**: copy as-is; instantiate inside `App`'s `useEffect` (replacing the inline IIFE in the original HTML).

### New components

**`api.js`** — single source of truth for HTTP calls:
```js
export async function runStage(stage, body) { /* POST /api/pipeline/<stage> → {job_id} */ }
export async function getRecent(folder, limit=10) { /* GET /api/vault/recent */ }
export async function readVaultFile(path) { /* GET /api/vault/file */ }
export async function listOutputs(path) { /* GET /api/vault/outputs */ }
```

**`useJobStream.js`** — SSE hook returning `{lines, status, result, error}` for live log + final typed result.

**`VaultPicker.jsx`** — dropdown driven by `getRecent(folder)`; used in stages that need prior artifacts:
- Ideation → picks from `10-Research/`
- Hook → optional pick from `10-Research/`
- Outline → picks from `05-Hooks/`; research influence is upstream through Ideation/Hook context
- Cascade / Short-form → picks both `10-Research/` and `06-Outlines/`
- Voice-cleanup → picks from any output folder

**`MarkdownViewer.jsx`** — renders vault file content. Use `react-markdown` (small, well-supported). Pass through the OutputZone slot.

**`OutputBrowser.jsx`** — receives `{result_type, primary_path, outputs[]}`. For `file`, delegate to `MarkdownViewer` for `primary_path`. For `file_set` and `bundle`, render a selectable output list with `primary_path` opened by default, then delegate the selected markdown file to `MarkdownViewer`.

**`DistributionWorkspace.jsx`** — replaces the single Distribution view with a tab bar across the top: **Outline | Title | Cascade | Short-form | Voice-cleanup**. Each tab mounts its own input+output panel reusing `StageWorkspace`'s patterns. Active tab persists in URL hash (`#distribution/outline`) so it survives nav.

### Wiring the existing components

- **Sidebar status dots**: replace hardcoded `status: "done|running|idle"` with state derived from the current job and the most recent vault file timestamps.
- **Dashboard cards**: each card's activity list comes from `getRecent(<folder>)` — show 3 most recent file slugs. Dashboard "Outline" card links to `#distribution/outline`.
- **Run button** (in StageWorkspace InputZone): on click, calls `runStage(stageId, body)`, switches OutputZone to live-log view via `useJobStream`, then swaps in `OutputBrowser` rendering the typed result returned by the backend.
- **Save to Vault action**: no-op for v1 (skills already write to the vault directly). Replace with a "Reveal in vault" button that copies the path to clipboard.
- **History drawer**: list of recent normalized outputs for the stage, newest first. File rows open in `MarkdownViewer`; bundle rows open in `OutputBrowser`.
- **SourcesPanel** (the `StackedPanel` "back" of every stage, including Brain): replace the hardcoded `VAULT_DATA[stageId]` constants with state from `getRecent(<stage folder>)`; render the file tree and "Sources" list from API data. Clicking a file row opens it via `MarkdownViewer`. Per-stage folder mapping mirrors the same conventions used by `VaultPicker`.
- **TweaksPanel**: keep as-is, persists to `localStorage` instead of postMessage (simpler in a single-app context).

### Brain workspace

V1 ships pasted-text analysis only. During the frontend port, remove the prototype's URL chips and file-drop affordances from `Brain.jsx` so no visible controls ship without backend behavior.

The remaining textarea flow is wired to `POST /api/brain/analyze`. Backend `brain.py` calls Anthropic SDK directly with a fixed analysis prompt that produces the JSON structure the UI expects (hook quality score, structure score, emotional triggers list, techniques to steal, replication template). This is the only **new** AI invocation outside the 8 existing skills — necessary because Brain is not a pipeline skill but the user wants the full app working.

### Vite proxy config

```js
// vite.config.js
export default {
  server: {
    proxy: {
      '/api': 'http://localhost:8765'
    }
  }
}
```

---

## Pipeline-to-UI Action Mapping (complete coverage of all 8 skills)

| UI Surface | Triggers | Inputs collected | Normalized result |
|---|---|---|---|
| Sidebar **Trends** workspace | (no skill) — displays current `04-Trends/github_trending.md` + lets user refresh externally | — | `file` from `04-Trends/` |
| Sidebar **Research** workspace | `python -m skills.researcher` | niche (text), repos (chip input), mode (deep/fast) | `file` from `10-Research/` |
| Sidebar **Ideation** workspace | `python -m skills.ideation` | topic (text), research_file (VaultPicker `10-Research/`) | `file` from `02-Ideas/` |
| Sidebar **Hooks** workspace | `python -m skills.hook` | topic, platform, audience, format, research_file? | `file` from `05-Hooks/` |
| Sidebar **Distribution** → **Outline** tab | `python -m skills.outline` | topic, hook_path (VaultPicker `05-Hooks/`), length, platform | `file` from `06-Outlines/`; no direct `research_file` |
| Distribution → **Title** tab | `python -m skills.title` | concept (text) | `file` from `07-Titles/` |
| Distribution → **Cascade** tab | `python -m skills.cascade` | research_file, outline_file, title? OR youtube_url | `bundle` from `08-Distribution/` |
| Distribution → **Short-form** tab | `python -m skills.short_form` | research_file, outline_file, title? OR youtube_url | `bundle` from `09-Shorts/` |
| Distribution → **Voice-cleanup** tab | `python -m skills.voice_cleanup` | file_path (VaultPicker any output folder), inplace? | `file`; original path if `inplace`, cleaned path otherwise |
| Sidebar **Knowledge Brain** | direct Claude call via `/api/brain/analyze` | pasted content only | not written to vault in v1 |

Every skill has a home. Every button does real work.

Research still shapes Outline, but indirectly: Research feeds Ideation and Hook generation, then Outline consumes the selected topic/hook context via the current `skills.outline` CLI.

---

## Implementation Phases

### Phase 1 — Scaffold (1-2 hours)
1. `cd Design-doc && mkdir web server`
2. `cd web && npm create vite@latest . -- --template react`
3. Install: `react-markdown`, `clsx`
4. Confirm the repo's existing Python environment can import the current skill stack. Use the repo root `.venv` if present; otherwise use the active interpreter that already runs `python -m skills.title`.
5. Add missing web-wrapper packages to the root `requirements.txt` under a short "Design-doc web wrapper" comment (`fastapi`, `uvicorn`, `aiofiles`, `anthropic`, `python-dotenv`). Do not create `Design-doc/server/requirements.txt` for v1.
6. Add `server/runtime.md` documenting the resolved interpreter path and the shared-runtime rule; do not create `Design-doc/server/.venv`.
7. Copy `Content Hub/styles.css`, `particles.js`, `icons.jsx`, `sources-panel.jsx` into `web/src/` (rename to `Icons.jsx` / `SourcesPanel.jsx`; apply JSX import fixes — CDN globals `window.Icon = Icon` / `window.SourcesPanel = …` replaced with `export default Icon` and `export { SourcesPanel, StackedPanel }`; add `import { useState } from 'react'` to `SourcesPanel.jsx`). `particles.js` and `styles.css` copy unchanged.
8. Boot both servers locally; confirm static UI loads through Vite dev with the particle background working.

### Phase 2 — Backend (3-4 hours)
1. `server/main.py`: FastAPI app, CORS for `http://localhost:5173`, mount routers.
2. `server/jobs.py`: in-memory job registry + per-job asyncio.Queue for SSE + typed `result` metadata.
3. `server/pipeline.py`: one wrapper per skill (8 functions). Each spawns subprocess, streams stdout/stderr into the queue, and calls the stage-specific output resolver on exit.
4. `server/vault.py`: `recent(folder, limit)`, `read_file(path)`, `outputs(path)` with path-traversal guard (must resolve inside `Content-Hub-Vault-V2/`).
5. `server/brain.py`: Anthropic SDK call with fixed analysis prompt.
6. **Verify**: hit each endpoint with `curl` — confirm researcher launches, SSE streams lines, and the job returns `{result_type, primary_path, outputs[]}` on completion.

### Phase 3 — Frontend port (2-3 hours)
1. Port `app.jsx` → `App.jsx` with imports + state hooks intact.
2. Port the 5 remaining prototype component files (`dashboard.jsx`, `stage-workspace.jsx`, `brain.jsx`, `sidebar.jsx`, `tweaks-panel.jsx`). `Icons.jsx` and `SourcesPanel.jsx` were already copied into `web/src/` in Phase 1 — just `import Icon from './Icons.jsx'` and `import { SourcesPanel, StackedPanel } from './SourcesPanel.jsx'` in the consumers (`brain.jsx:118-120` and `stage-workspace.jsx:159-161`). Replace global icon references with imports. In `Brain.jsx`, strip URL chips and file-drop controls for v1 instead of porting dead affordances.
3. Wire `main.jsx` to mount `<App />` and instantiate particles in a useEffect.
4. **Verify**: every screen renders identical to the original prototype with hardcoded demo data still in place.

### Phase 4 — Wire 5 sidebar stages (3-4 hours)
1. Build `api.js` + `useJobStream.js`.
2. Build `VaultPicker.jsx`, `MarkdownViewer.jsx`, and `OutputBrowser.jsx`.
3. Modify `StageWorkspace.jsx`: replace `OUTPUTS[stageId]()` with `<OutputBrowser result={result} />`; replace static loading state with `useJobStream`.
4. Trends workspace: read-only view of `04-Trends/github_trending.md`.
5. **Verify each in turn**: Trends loads file → Research runs end-to-end → Ideation auto-fills research from VaultPicker → Hook runs.

### Phase 5 — Distribution multi-tab (2-3 hours)
1. Build `DistributionWorkspace.jsx` with tab bar + URL hash routing.
2. Build 5 tab components (Outline/Title/Cascade/ShortForm/VoiceCleanup) — each is a thin shell around StageWorkspace's InputZone+OutputZone with the right form fields.
3. **Verify**: from a single topic, run the full chain in order. Confirm all 9 deliverables land in vault (research brief, 9 ideas, 5 hooks, outline, 10 titles, 3 distribution files, 3 short scripts, voice-cleaned version of any).

### Phase 6 — Dashboard + Brain + polish (2-3 hours)
1. Dashboard cards: replace hardcoded activity with `getRecent` calls. Add "Run [Stage]" buttons that nav to the workspace.
2. Sidebar status dots: derive from current job + recent vault scan.
3. Brain workspace: wire textarea-only analysis to `/api/brain/analyze` with the JSON-returning Claude prompt.
4. Health badge in sidebar footer: consume the minimum `/api/health` contract (`status`, `backend`, `capabilities:null`) and display only backend reachability in v1.

### Phase 7 — Launch convenience (30 min)
1. `Design-doc/start.ps1`: launches both servers in separate windows.
2. `Design-doc/README.md`: 10-line dev quickstart.

**Total estimate:** 14–19 hours of focused work.

---

## Verification

**Component-level (after each phase):**
- Phase 2: `curl -X POST http://localhost:8765/api/pipeline/title -d '{"concept":"test"}'` returns a job_id; `curl http://localhost:8765/api/jobs/<id>/stream` streams lines and ends with a typed `result`.
- Phase 3: visual diff between original `Content Hub.html` rendering and Vite dev server — should be identical.
- Phase 4: pick a known topic with existing vault data, confirm VaultPicker populates, Run button triggers backend, and `OutputBrowser` renders file and bundle results correctly.

**End-to-end (final acceptance):**
1. Start both servers via `start.ps1`.
2. Open `http://localhost:5173`.
3. From a clean slate, run the full chain on a new topic: Research → Ideation → Hooks → Distribution(Outline → Title → Cascade → Short-form → Voice-cleanup).
4. Confirm:
   - SSE log stream is live on each run (no spinner stalls).
   - Each completed run renders the actual vault markdown or bundle member list (not demo content).
   - `Content-Hub-Vault-V2/` contains all 9 deliverables for the topic, dated today.
   - Sidebar status dots flip done/running correctly.
   - Brain workspace returns a real Claude analysis when given pasted content.
   - Dashboard cards show the new artifacts under "recent activity".
5. Confirm constraint: starting a second skill while one is running returns 409 in the UI gracefully (toast or disabled Run button).

**Session log (mandatory per [[CLAUDE]] § 7):**
On completion, write `Content-Hub-Vault-V2/00-Management-V2/Sessions/YYYY-MM-DD_Design_Doc_Web_App_Wired.md` linking back to this plan and to the 8 skill nodes. Update [[Current_Sprint]] to reflect the wrapper plan supersession.

---

## Out of scope for v1 (explicit non-goals)

- No mandatory SQLite/Postgres/Supabase job history for v1. If Supabase is introduced, it stores app state and output metadata only.
- No replacement of the vault as the execution-layer artifact system.
- No in-app markdown editor (Obsidian handles that — design-spec convention).
- No full multi-user authentication system. If exposing a demo externally, add a simple access gate and dedicated demo workspace/output namespace.
- No parallel job execution.
- No publishing automation (manual copy-paste, per V2 plans).
- No changes to `backend/main.py` at project root (V1 SaaS scope, port 8000).
- No changes to any `skills/*.py` or `prompts/*.md` ([[CLAUDE]] § 3 Surgical Changes — wrapper only).
- No TypeScript port (per user decision, 2026-05-22).

---

## Related Nodes

- Implements: [[Local_First_Skill_Engine_Plan]]
- Supersedes: [[Content_Hub_Web_Design_Spec]], [[Wrapper_Plan]]
- References: [[Refined_Pipeline]] (topic_slug vault convention), [[Researcher_Optimisation]], [[2026-05-22_Codex_Plan_Reviewer_Webapp]], [[2026-05-22_Codex_Webapp_Brainstorm]]
- Modifies: `Design-doc/` directory tree
- Depends on: [[researcher]], [[ideation]], [[hook]], [[outline]], [[title]], [[cascade]], [[short-form]], [[voice-cleanup]]
