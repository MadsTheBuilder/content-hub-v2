---
date: 2026-05-29
type: phase7-agent-note
status: done
agent: 00-contract-agent
task: write Phase 7 contract memo so all later workers share the same launcher commands and acceptance matrix
description: "Shared contract for Phase 7 workers: launcher commands, acceptance topic, 11-row stage matrix, and final closeout file names."
tags: [phase7, webapp-sprint, contract, acceptance, launcher]
owned_files:
  - Design-doc/web/src/.agent-context/phase7/00-Contract.md
verification:
  - memo includes launcher commands matching Design-doc/README.md
  - memo includes all Stage Acceptance Matrix rows (Trends through 409)
  - memo names the two final closeout files
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 00-Contract Agent

## Mission
Write a shared contract memo so Groups 1-5 use identical launcher commands, the same acceptance topic, and the same evidence expectations.

## Context Read
- `Design-doc/README.md` — quickstart commands
- `Design-doc/web/package.json` — scripts: dev, build, lint, preview
- `[[Webapp_sprint]]` Phase 7 checklist
- `[[Design_Doc_Web_App_Plan]]` Phase 7 spec
- `[[2026-05-29_phase7-launch-e2e-acceptance]]` orchestration playbook

## Changes Made
Wrote this contract memo only. No production code touched.

## Self-Verification
- Launcher commands below match `Design-doc/README.md` exactly.
- All 11 Stage Acceptance Matrix rows are present.
- Final closeout files are named.

---

## Launcher Command Contract

| Item | Command / Value |
|---|---|
| Script | `Design-doc/start.ps1` |
| Backend (from repo root) | `.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload` |
| Frontend (from `Design-doc/web/`) | `npm run dev` |
| Windows behavior | Backend in one PowerShell window; frontend in another |
| Health check | `GET http://localhost:8765/api/health` → `{status:"ok", backend:"up", capabilities:null}` |
| App URL | `http://localhost:5173` |

The script must use the **repo root `.venv`** — not `Design-doc/server/.venv`.  
It must fail early with readable messages if `.venv\Scripts\python.exe` or `Design-doc/web/node_modules` are absent.

## Acceptance Topic

```
Why local-first AI workbenches are becoming the default for serious creators
```

This is a **fresh-topic full chain** run. All 9 pipeline stages must produce vault artifacts dated 2026-05-29.

## Stage Acceptance Matrix

| Surface | Expected action | Expected evidence |
|---|---|---|
| Trends | Load read-only workspace | Current trends markdown renders from `04-Trends/` |
| Research | Run with niche/topic and repo inputs | New file in `10-Research/`; SSE logs move |
| Ideation | Pick research file, run topic | New file in `02-Ideas/`; rendered in OutputBrowser |
| Hooks | Pick research file, run topic | New file in `05-Hooks/`; rendered in OutputBrowser |
| Outline | Distribution → Outline | New file in `06-Outlines/`; no `research_file` in request body |
| Title | Distribution → Title | New file in `07-Titles/` |
| Cascade | Research + outline or YouTube URL | Bundle in `08-Distribution/`; README opens by default |
| Short-form | Research + outline or YouTube URL | Bundle in `09-Shorts/`; README opens by default |
| Voice-cleanup | Clean one generated markdown file | Cleaned file renders correctly |
| Brain | Paste content → analyze | Real `brain_result` payload: `hook_quality`, `structure_score`, `emotional_triggers`, `techniques_to_steal`, `replication_template` |
| 409 | Start second job while one runs | Human-readable UI copy; no raw stack trace |

## Key Rules

- Brain is **separate** from vault artifacts — it does not write to the vault.
- Final sprint docs ([[Webapp_sprint]], [[Current_Sprint]]) are updated **only after** Group 5 acceptance passes.
- Final closeout files:
  - `Design-doc/web/src/.agent-context/phase7/99-Acceptance.md`
  - `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-29_Design_Doc_Web_App_Wired.md`

## Evidence
Contract memo written and committed to agent-context.

## Open Items
None.
