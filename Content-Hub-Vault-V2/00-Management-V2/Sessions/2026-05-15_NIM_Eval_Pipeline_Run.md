---
date: 2026-05-15
type: session_log
description: "First NIM full-pipeline eval run against a real YouTube video. Found PYTHONPATH bug and fixed it. Identified 3 pipeline failures via log analysis. Wrote eval report."
tags: [nim, eval, pipeline, bug-report, research]
---

# Session: NIM Eval Pipeline Run

References: [[2026-05-15_NIM_Full_Pipeline_Takeover]] | [[2026-05-15_NIM_Fallback_Wired]]
Modifies: [[skills/pipeline.py]]
Adds: [[NIM test run/EVAL_REPORT.md]]

## What Was Done

Ran the first live eval of the full NIM pipeline against a real YouTube video: *Claude Code Has Evolved* (`https://www.youtube.com/watch?v=d86VCtQ_dN8`).

### 1. Context review

Reviewed the two prior NIM sessions to establish the current routing state:
- [[2026-05-15_NIM_Fallback_Wired]] — wired NIM as primary provider, replacing blocked Ollama
- [[2026-05-15_NIM_Full_Pipeline_Takeover]] — removed Claude from all pipeline content calls; cascade is now `NIM → Gemini → Ollama`

### 2. First run — PYTHONPATH bug

Pipeline failed immediately on step 1 with `ModuleNotFoundError: No module named 'skills'`. `pipeline.py` was spawning `yt_pipeline.py` as a subprocess without setting `PYTHONPATH`, so the child process could not import from the project root.

**Fix applied** — `skills/pipeline.py`:
- Added `_SUBPROCESS_ENV` dict that injects `PYTHONPATH=<PROJECT_ROOT>` and `PYTHONIOENCODING=utf-8` into all subprocess calls
- All 5 pipeline steps now receive the correct import path

### 3. Second run — completed, exit code 0

Pipeline ran to completion. Output written across 5 vault folders:
- `05-Hooks/` — 5 hook variations
- `06-Outlines/` — 8-stage dopamine ladder outline
- `08-Distribution/` — blog post, Twitter thread, LinkedIn post
- `09-Shorts/` — 30s, 60s, 90s scripts
- `10-Research/` — research.md (broken — see failures below)

All outputs moved to `Content-Hub-Vault-V2/NIM test run/` to preserve the eval run separately from production vault content.

### 4. Eval analysis — 3 failures found

Full details in [[NIM test run/EVAL_REPORT.md]]. Summary:

**Failure 1 — Research regex (CRITICAL)**
`SECTION_PATTERN` in `skills/yt_pipeline.py:28` uses `.+` in the heading capture group with `re.DOTALL`. DOTALL makes `.` match newlines, so `.+` greedily consumes the entire prompts file as one match. All 12 questions were collapsed into a single NotebookLM query. NotebookLM returned a generic response ("It appears that your query was left blank"). Research file has no usable answers.

Root cause confirmed by running the regex directly — 1 match vs 12 matches with the fix (`[^\n]+` instead of `.+`).

**Failure 2 — NIM intermittent failures (HIGH)**
NIM succeeded on ~4 of 10 calls and failed silently on the rest, falling back to Gemini each time. Error log showed blank error string — HTTP status code and response body are not captured before the exception handler. Failure pattern is consistent with free-tier per-minute rate limiting, not credit exhaustion.

**Failure 3 — Hooks generated without research (HIGH)**
`pipeline.py` calls `hook.py` with only the topic string — no `--research-file` passed. Every other downstream step (outline, short-form, cascade) receives the research file. Hooks are therefore generated from the topic title alone, producing generic output disconnected from actual video content.

### 5. NIM behaviour summary from this run

| Step | NIM result |
|---|---|
| Research follow-ups | Not reached (research broken before NIM called) |
| Hooks (step 2) | Failed both calls → Gemini fallback |
| Outline (step 3) | Failed both calls → Gemini fallback |
| Short-form (step 4) | Succeeded on call 1, failed on calls 2–3 → Gemini |
| Distribution (step 5) | Failed call 1 (blog), succeeded calls 2–3 (Twitter, LinkedIn) |

## Files Changed

| File | Change |
|---|---|
| `skills/pipeline.py` | Added `_SUBPROCESS_ENV` with `PYTHONPATH` for all subprocess steps |
| `Content-Hub-Vault-V2/NIM test run/EVAL_REPORT.md` | New — full eval report with confirmed root causes and fixes |
| `Content-Hub-Vault-V2/NIM test run/` | New folder — all eval run outputs moved here from production folders |

## Open Items

These three bugs are confirmed and ready to fix:

1. `skills/yt_pipeline.py:28` — change `(Q\d+ — .+)` to `(Q\d+ — [^\n]+)` in SECTION_PATTERN
2. `skills/utils/ai.py:88` — log HTTP status + response body before exception handler in `_nim_generate()`
3. `skills/pipeline.py:64` + `skills/hook.py` — pass `--research-file` to hook step; hook.py needs to accept and use it
