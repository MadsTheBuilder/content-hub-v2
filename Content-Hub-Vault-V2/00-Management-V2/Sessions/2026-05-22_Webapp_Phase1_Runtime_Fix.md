---
status: Completed
date: "2026-05-22"
type: session_summary
tags: [session, web-app, runtime, dependencies, fastapi, streamlit]
description: "Phase 1 runtime remediation — shared .venv rebuilt on Python 3.12.10, wrapper deps synced, and invalid requirement pins corrected."
references:
  - "[[Webapp_sprint]]"
  - "[[Design_Doc_Web_App_Plan]]"
  - "[[2026-05-22_Webapp_Phase1_Scaffold]]"
---

# Session: Webapp Phase 1 Runtime Fix

## What changed

- Rebuilt the shared repo `.venv` on **Python 3.12.10** after verifying the pinned requirements do not cleanly install on Python 3.14.
- Installed the full pinned `requirements.txt` set into the rebuilt `.venv`.
- Added `streamlit==1.57.0` to `requirements.txt` so the shared runtime is reproducible from the manifest, not manual installs.
- Corrected the FastAPI/Streamlit compatibility pins:
  - `fastapi==0.136.1`
  - `starlette==1.0.0`
- Corrected the invalid linter pin:
  - `ruff==0.8.6` (replacing nonexistent `0.8.7`)
- Added `Design-doc/README.md` quickstart and updated `Design-doc/server/runtime.md` with the required install command.

## Backup kept

- Previous Python 3.14 environment preserved at:
  - `C:\Users\madhu\Claude cowork\Content Hub V2\.venv-py314-backup-20260522`

## Verification

- `.venv\Scripts\python.exe -m pip check` → no broken requirements
- `Design-doc/server/main.py` health route verified via `TestClient`:
  - `GET /api/health` → `200 {"status":"ok","backend":"up","capabilities":null}`

## Note

- A broader import check of `backend.main` now gets past the dependency layer but still reveals a pre-existing code issue: `backend.workflows.service` imports `backend.intelligence.voice`, and that package is not present in the current tree. This is outside the Design-doc Phase 1 scaffold scope but is now clearly separated from environment problems.
