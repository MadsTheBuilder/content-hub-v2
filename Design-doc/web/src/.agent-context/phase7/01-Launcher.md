---
date: 2026-05-29
type: phase7-agent-note
status: done
agent: 01-launcher-agent
task: create Design-doc/start.ps1 convenience launcher
description: "Group 1 evidence: start.ps1 created — launches FastAPI :8765 and Vite :5173 in separate PowerShell windows from repo root."
tags: [phase7, webapp-sprint, launcher, start-script]
owned_files:
  - Design-doc/start.ps1
verification:
  - script resolves repo root from its own location (Split-Path)
  - checks .venv\Scripts\python.exe; exits with readable message if absent
  - checks Design-doc\web\node_modules; exits with readable message if absent
  - backend uses repo-root .venv per runtime.md locked constraint
  - frontend launched from Design-doc/web/ with npm run dev
  - commands match Design-doc/README.md exactly
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
---

# 01-Launcher Agent

## Mission
Create `Design-doc/start.ps1` that launches FastAPI and Vite in separate PowerShell windows from the repo root.

## Context Read
- `Design-doc/README.md` — canonical quickstart commands
- `Design-doc/server/runtime.md` — locked constraint: repo-root `.venv` only, no `Design-doc/server/.venv`
- `Design-doc/web/package.json` — confirms `npm run dev` script
- `Design-doc/web/src/.agent-context/phase7/00-Contract.md` — launcher command contract

## Changes Made
Created `Design-doc/start.ps1`.

Key decisions:
- `$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path` → resolves repo root dynamically, no hardcoded user path.
- Preflight checks exit with `Write-Error` + `exit 1` on missing `.venv` or `node_modules`.
- Backend: `Start-Process powershell` with `-NoExit` sets working dir to `$repoRoot`, runs uvicorn command.
- Frontend: `Start-Process powershell` with `-NoExit` sets working dir to `$webDir`, runs `npm run dev`.
- Prints health URL and app URL on launch.

## Self-Verification
- Repo-root `.venv\Scripts\python.exe` exists (confirmed by Glob before writing).
- Backend command matches README.md verbatim.
- No hardcoded `C:\Users\madhu\...` path — all paths derived from script location.
- No `Design-doc/server/.venv` reference (per locked constraint).

## Evidence
`Design-doc/start.ps1` created at repo root / `Design-doc/`.

## Open Items
None.
