---
date: 2026-05-31
tags: [session, webapp, debugging, trends, fixed]
description: "Fixed 'Job failed' for Trends stage — asyncio.create_subprocess_exec → run_in_executor. Also added --space argparse to github_trending.py."
---

# Trends Job Fixed — Subprocess on Windows

References: [[2026-05-31_Trends_Job_Failed_Debug_Handoff]]
Modifies: [[pipeline.py]], [[github_trending.py]]

---

## Root Cause

`asyncio.create_subprocess_exec` raises `NotImplementedError` on Windows when uvicorn runs with its default `SelectorEventLoop`. The error was captured by the debug code planted in the previous session:

```
EXC NotImplementedError: NotImplementedError() |
  File "asyncio/base_events.py", line 1756, in subprocess_exec
    transport = await self._make_subprocess_transport(...)
  File "asyncio/base_events.py", line 528, in _make_subprocess_transport
    raise NotImplementedError
```

`SelectorEventLoop._make_subprocess_transport` always raises `NotImplementedError` on Windows — only `ProactorEventLoop` supports subprocesses. Uvicorn uses `SelectorEventLoop` by default.

---

## Fix

**`Design-doc/server/pipeline.py`** — replaced `asyncio.create_subprocess_exec` + async stream draining with `loop.run_in_executor(None, lambda: subprocess.run(...))`.

Key tradeoff: subprocess output now arrives batch-at-completion rather than line-by-line. The SSE queue still receives all stdout/stderr lines — they just arrive simultaneously at the end instead of streaming in real time. Acceptable for correctness; streaming can be improved later if needed.

Also removed the debug code inserted in [[2026-05-31_Trends_Job_Failed_Debug_Handoff]] and restored the clean `fail_job("\n".join(stderr_lines[-30:]))` for the non-zero exit path.

---

## --space Argparse

**`scripts/github_trending.py`** — added `argparse` + `--space` argument. When passed, overrides `AI_TOPICS` to `[space]`, narrowing the GitHub search to that topic. Previously the arg was forwarded by `pipeline.py` but silently ignored.

---

## Verification

Job `d6de36bb` ran for 3m 13s and completed with status `completed`:
- `result_type: "file"`
- `primary_path: Content-Hub-Vault-V2/04-Trends/github_trending.md`
- `error: null`

---

## Files Touched

| File | Change |
|------|--------|
| `Design-doc/server/pipeline.py` | `asyncio.create_subprocess_exec` → `run_in_executor` + `subprocess.run`; debug code removed |
| `scripts/github_trending.py` | `argparse` + `--space` arg wired |

---

## Open Items

- Phase 7 E2E acceptance re-run (all 9 stages) — deferred to next session
