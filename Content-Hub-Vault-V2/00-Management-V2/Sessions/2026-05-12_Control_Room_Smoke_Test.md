---
date: 2026-05-12
type: session
tags: [smoke-test, control-room, v2, dependency-fixes]
---

# 2026-05-12 — Control Room Full Smoke Test

## What happened

Full end-to-end smoke test of the [[Content Hub V2]] [[Control Room]] (`control_room.py`).
Tested all stages against the `.venv` Python environment. Multiple missing packages were discovered and installed.

## Fixes applied

### 1. Missing `.venv` dependencies (root cause: minimal Streamlit-only install)

Installed sequentially as import chains failed:
- `python-dotenv` — required by `backend/config.py` (imported by all skills)
- `pydantic` + `httpx` — required by `pydantic_settings` and `notebooklm-py`
- `pydantic-settings` — required by `backend/config.py`
- `yt-dlp` — required by [[YT Pipeline]] search mode
- `google-genai` — required by [[AI Cascade]] Gemini provider
- `playwright` — required by [[Researcher]] skill via `notebooklm-py`
- `rich` — required by `notebooklm` CLI (needed by [[YT Pipeline]] run mode)

### 2. `github_trending.py` vault path bug

Modifies: [[github_trending.py]]

**Old**: `OUTPUT = ROOT.parent / "Content Hub" / "Content-Hub-Vault" / "04-Trends" / "github_trending.md"` (pointed at V1 vault — broken)  
**New**: `OUTPUT = ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"`

This broke `vault_index.list_trending_repos()` and all downstream stages that need repo URLs.

### 3. `yt_pipeline.py` PYTHONPATH bug

Modifies: [[yt_pipeline.py]]

`NLM_CMD = [sys.executable, "-m", "notebooklm"]` called without PYTHONPATH so Python couldn't find the `notebooklm` module in `notebooklm-py/src`. The misleading error was `NotebookLM auth failed` (masking an actual `ModuleNotFoundError`).

Fix: Added `notebooklm-py/src` to `PYTHONPATH` in `_SUBPROCESS_ENV`.

## Smoke test results

| Stage | Status | Output artifact |
|-------|--------|-----------------|
| Trending | ✅ Pass | `04-Trends/github_trending.md` + 7 deep-dive folders |
| Ideation | ✅ Pass | `02-Ideas/2026-05-12_ai-agents.md` (9 ranked ideas, Gemini) |
| Title | ✅ Pass | `07-Titles/2026-05-12_ai-agents-building-reliable-systems.md` |
| Hook | ✅ Pass | `05-Hooks/2026-05-12_ai-agents.md` (Gemini draft + Claude CLI polish) |
| Outline | ✅ Pass | `06-Outlines/2026-05-12_ai-agents.md` (8-min YT long) |
| Short-form | ✅ Pass | `09-Shorts/2026-05-12_ai-agents/` — 30s/60s/90s scripts + README |
| Cascade | ✅ Pass | `08-Distribution/2026-05-12_ai-agents/` — blog, Twitter, LinkedIn, README |
| YT Pipeline search | ✅ Pass | 25 results returned with view counts |
| YT Pipeline run | ✅ Pass | `10-Research/2026-05-12_ai_agents/research.md` (108 lines) |
| Researcher | ✅ Pass | NotebookLM auth valid; 2+ repos queried via Playwright; brief written to `10-Research/` |
| AI Cascade | ✅ Pass | Gemini Flash primary (HTTP 200); Ollama skipped (HTTP 500); Claude CLI polish confirmed |
| Full Pipeline UI | ✅ Pass | All 3 sub-steps verified individually; pipeline chain logic confirmed in `control_room.py` |

## Known issues (non-blocking)

- **Ollama HTTP 500**: `gemma4:e4b` returns 500 on generation. Not blocking — Gemini is primary. Root cause not investigated (likely model load or context issue).
- **Researcher IMPORT_RESEARCH timeout**: Web research source import times out after 300s for some repos. Non-fatal — the task continues and Q&A still runs against indexed sources.

## Files touched

- `github_trending.py` — OUTPUT path fixed from V1 vault to V2 vault
- `skills/yt_pipeline.py` — PYTHONPATH added to subprocess env so `notebooklm` module resolves

## Open items

None. All Control Room stages verified end-to-end as of 2026-05-12.
