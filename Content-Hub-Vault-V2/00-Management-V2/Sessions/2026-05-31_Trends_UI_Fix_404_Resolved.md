---
date: 2026-05-31
tags: [session, webapp, bugfix, trends]
description: "Fixed Trends stage UI (replaced markdown-viewer with standard form) and resolved 404 root cause on Run Trends."
---

# Session: Trends UI Fix + 404 Root Cause

Implements: [[Webapp_sprint]]
Modifies: [[StageWorkspace.jsx]], [[main.py]], [[pipeline.py]]

## What Changed

### 1. Trends InputZone — standard form (was: markdown viewer)

The Trends left panel had a hardcoded `isTrends` early-return in `InputZone` that rendered a `MarkdownViewer` of the current trends file + a bare Run button. Replaced by removing that branch entirely — Trends now falls through to the same standard form every other LIVE_STAGE uses.

Result: textarea ("What space should I trend-scan?"), file drop area, URL paste field, and Run Trends button — matching the approved design.

**Files touched:**
- `Design-doc/web/src/StageWorkspace.jsx`
  - Removed `isTrends` variable and its `if (isTrends) { return ... }` block (~40 lines)
  - `showUrlInput` now includes `trends` (`stage.id === "research" || stage.id === "trends"`)
  - Removed special `if (stageId === "trends") { ... return; }` branch from `handleRun`
  - Added `trends` case to LIVE_STAGES body builder: `{ space: prompt }`

### 2. Backend — TrendsBody model + space param

`/api/pipeline/trends` previously took no body. Updated to accept an optional `TrendsBody` with `space: str = ""` so the form prompt passes through.

**Files touched:**
- `Design-doc/server/main.py` — added `TrendsBody` model; endpoint signature updated to `run_trends(body: TrendsBody = None)`
- `Design-doc/server/pipeline.py` — `run_trends(space: str = "")` now appends `--space <value>` to the subprocess args when provided (non-breaking; `scripts/github_trending.py` may ignore unrecognised flags)

### 3. 404 Root Cause

`Error: trends failed (404): {"detail":"Not Found"}` was caused by uvicorn running the old committed version of `main.py` — the trends route was added to the working-tree version but the server was started before that change and without `--reload`. The Vite proxy and route definitions were both correct.

**Fix (user action):** restart the server:
```bash
.venv/Scripts/python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload
```
Note: use forward slashes in Git Bash.

## Open Items

- `scripts/github_trending.py` does not yet parse `--space` — the arg is passed through but silently ignored. Future work: add argparse to the script and filter trending output by niche.
- Re-run Phase 7 E2E acceptance after server restart to confirm Trends streams correctly.
