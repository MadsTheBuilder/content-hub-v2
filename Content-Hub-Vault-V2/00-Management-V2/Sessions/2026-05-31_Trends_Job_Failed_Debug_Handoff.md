---
date: 2026-05-31
tags: [session, handoff, webapp, debugging, trends]
description: "Handoff: Trends 'Job failed' root cause still unresolved. Debug trap is set — next session picks up with a clean curl test."
---

# Handoff: Trends "Job failed" — Root Cause Unknown

References: [[2026-05-31_Trends_UI_Fix_404_Resolved]]
Modifies: [[pipeline.py]], [[main.py]]

---

## Status

**Blocked.** Clicking "Run Trends" in the webapp returns `Error: Job failed` in the UI. Root cause not yet identified.

---

## What Is Working

- UI renders correctly — textarea, file drop, Run Trends button
- POST `/api/pipeline/trends` returns a `job_id` (no 404, no 409)
- `scripts/github_trending.py` runs successfully when launched directly from terminal (exit 0, full output)
- `scripts/github_trending.py` runs successfully when launched via `asyncio.create_subprocess_exec` in a standalone test (exit 0, 18 stdout lines, 0 stderr lines)
- GitHub API is not rate-limited (tested 2026-05-31, returns results with token)

---

## What Is Broken

Job fails in ~14ms with `error: ""` (empty string). The UI fallback `err || "Job failed"` fires because `data.error` is blank.

The `type: "error"` SSE event IS being sent — so `fail_job()` IS being called. But with an empty string.

The original `fail_job` call (before debug edits) was:
```python
fail_job(job.job_id, "\n".join(stderr_lines[-30:]))
```
Empty error = `stderr_lines` was empty when the job failed.

14ms is too fast for the subprocess to start, run real work, and exit. Something is failing at or immediately after subprocess launch.

---

## Current State of pipeline.py

Debug code is **already in place** in `Design-doc/server/pipeline.py`. The failure paths now write verbose info into the error field:

```python
# Non-zero returncode path (lines ~171-172):
_debug = f"rc={proc.returncode} stdout={len(stdout_lines)} stderr={len(stderr_lines)} | STDOUT: {stdout_lines[-3:]} | STDERR: {stderr_lines[-3:]}"
fail_job(job.job_id, _debug)

# Exception path (lines ~173-175):
import traceback as _tb
fail_job(job.job_id, f"EXC {type(exc).__name__}: {exc!r} | {_tb.format_exc()[-500:]}")
```

This means the NEXT job that fails will have a readable error string in `job.error` instead of `""`.

---

## Why Debugging Has Been Stuck

The server runs with `--reload`. Every edit to `pipeline.py` caused uvicorn to restart, clearing the in-memory `_jobs` dict. So every time we added debug code and triggered a job, the job vanished before we could read it back (`{"detail": "Job not found"}`).

The debug code is now committed to disk. The server should be stable (no pending edits). No more reloads expected.

---

## Next Action — Do This First

**Step 1:** Confirm server is running and stable:
```bash
curl -s http://localhost:8765/api/health
```
Expected: `{"status": "ok", ...}`

**Step 2:** Trigger a trends job AND immediately poll for the error (server must not be restarting):
```bash
JOB=$(curl -s -X POST http://localhost:8765/api/pipeline/trends \
  -H "Content-Type: application/json" \
  -d "{\"space\":\"\"}" | python -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "JOB=$JOB"
sleep 2
curl -s "http://localhost:8765/api/jobs/$JOB"
```

**Step 3:** Read `job.error` in the response. It will now contain one of:
- `rc=<N> stdout=<N> stderr=<N> | STDOUT: [...] | STDERR: [...]` → subprocess exited non-zero
- `EXC <ExceptionType>: <message> | <traceback>` → exception before or during subprocess

That string tells us the actual root cause.

---

## Leading Hypotheses (ranked)

1. **`asyncio.CancelledError` cancels the task before it finishes** — uvicorn's lifespan may be cancelling pending tasks. `CancelledError` is a `BaseException` (not `Exception`) in Python 3.8+, so the `except Exception` block does NOT catch it. Job stays "running" forever in that case. But we're seeing "failed"... so this might not be it unless there's another code path.

2. **Claude CLI not on PATH inside uvicorn's subprocess env** — `github_trending.py` calls `subprocess.run("claude", shell=True)`. If uvicorn's worker process has a different PATH (e.g., npm bin not in it), the `claude` command fails silently inside the script and the script exits non-zero. `where claude` works in the terminal but may not work in the spawned process.

3. **Windows pipe buffering or asyncio ProactorEventLoop edge case** — subprocess starts but its stdout/stderr pipes close before the drain coroutines read data. Subprocess exits with rc!=0 but stderr is captured as empty.

4. **Rate limit / network error in GitHub API** — unlikely (tested clean today), but possible if enough runs happen in quick succession (10 req/min unauthenticated; authenticated limit is much higher, token is present).

---

## Key Files

| File | Role |
|------|------|
| `Design-doc/server/pipeline.py` | Job launcher — debug code already in here |
| `Design-doc/server/main.py` | FastAPI routes — `POST /api/pipeline/trends` |
| `Design-doc/server/jobs.py` | In-memory job registry + `fail_job()` |
| `scripts/github_trending.py` | The script that actually does the work |
| `Design-doc/web/src/hooks/useJobStream.js` | UI SSE consumer — `err \|\| "Job failed"` is line 37 |

---

## After Root Cause Is Found

1. Fix the actual issue
2. Remove debug code from `pipeline.py` (restore original `fail_job(job.job_id, "\n".join(stderr_lines[-30:]))` in the non-zero path, clean up the exception handler)
3. Re-run Phase 7 E2E acceptance
4. Add `--space` argparse to `scripts/github_trending.py` (open item from previous session — the arg is passed but silently ignored by the script)
