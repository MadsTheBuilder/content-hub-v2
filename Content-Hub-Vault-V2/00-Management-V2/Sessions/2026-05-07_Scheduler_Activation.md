---
status: Complete
date: "2026-05-07"
author: Scheduler & Orchestration Agent
title: "Scheduler Activation & Daily Auto-Commit Pipeline"
---

# Scheduler Activation & Auto-Commit Pipeline

## Summary
Activated APScheduler in the Content Hub backend, created a daily auto-commit job that runs at 6 AM, and added CLI flags to `daily.py` for on-demand trigger and dry-run modes.

## Changes Made

### 1. backend/main.py
- **Imports**: Added `apscheduler.schedulers.background.BackgroundScheduler`, `datetime`, and `Path`
- **Scheduler Init**: Created `BackgroundScheduler()` instance at module level
- **setup_scheduled_jobs()**: New function that:
  - Registers the daily auto-commit job at 6:00 AM
  - Job calls `run_auto_commit()` from daily.py
  - Logs all execution results to `logs/scheduler.log` with timestamps
  - Returns list of scheduled jobs with metadata (name, id, next_run_time, last_run_time)
- **Lifespan Context**: Updated `lifespan()` to:
  - Start scheduler on app startup
  - Log all registered jobs to scheduler.log on startup
  - Log all registered jobs to console logger on startup
  - Shutdown scheduler on app shutdown

### 2. daily.py
- **run_auto_commit()**: New helper function that:
  - Stages files in Content-Hub-Vault-V2 using GitManager
  - Runs quality checks (pytest, ruff, mypy) using QualityValidator
  - Commits with message "Daily auto-commit: vault + quality [timestamp]" if all checks pass
  - Returns dict: `{success, files_staged, commit_hash}`
  - Properly handles no-changes scenario (success=True, commit_hash=None)

- **CLI Flags** added to argparse:
  - `--auto-commit`: Manually trigger full auto-commit pipeline
  - `--check-only`: Run quality checks without committing (dry-run mode)
  - Both flags are handled before normal workflow steps

- **Flag Handlers**:
  - `--auto-commit`: Calls `run_auto_commit()`, prints success/failure with commit details
  - `--check-only`: Calls `QualityValidator.run_checks(verbose=True)`, prints full results

## Files Touched
- `/backend/main.py` - APScheduler init, lifespan context, setup_scheduled_jobs()
- `/daily.py` - run_auto_commit() helper, CLI flags --auto-commit and --check-only

## Scheduled Jobs
**Daily Auto-Commit** — runs at 06:00 AM every day
- **Pipeline**: stage vault changes → run quality checks → commit if passing
- **Logging**: All executions logged to `logs/scheduler.log` with timestamps
- **Author**: "Claude + Scheduler" for commit attribution

## CLI Examples
```bash
# Manual trigger (full pipeline)
python daily.py --auto-commit

# Dry-run (checks only, no commit)
python daily.py --check-only

# Normal workflow (unaffected)
python daily.py                           # research + ideas
python daily.py --step script "Title"     # script generation
```

## Dependencies Met
- `backend.git_manager.GitManager` - ✅ exists, provides stage_files() and commit()
- `backend.quality_check.QualityValidator` - ✅ exists, provides run_checks()
- `apscheduler` - ✅ must be in requirements.txt for production
- `PathLib` and `datetime` - ✅ standard library

## Integration Points
- **Scheduler** runs daily auto-commit at 6 AM → logs to `logs/scheduler.log`
- **Manual trigger** via `python daily.py --auto-commit` → same pipeline
- **Dry-run mode** via `python daily.py --check-only` → quality validation only
- **Normal daily workflow** unaffected → still runs research/ideas/script/cascade steps

## References
- Implements: [[APScheduler Integration]]
- Modifies: [[backend/main.py]], [[daily.py]]
- Uses: [[GitManager]], [[QualityValidator]]
- Logging: `logs/scheduler.log`
