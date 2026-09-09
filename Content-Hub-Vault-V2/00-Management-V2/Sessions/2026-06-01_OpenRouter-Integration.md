---
date: 2026-06-01
type: session-log
status: complete
tags: [openrouter, model-routing, free-models, pipeline, ai-router]
description: "Integrated OpenRouter free tier into the full pipeline cascade — Gemma 4 31B as default, Claude CLI demoted to fallback."
---

# Session Log: OpenRouter Integration
Date: 2026-06-01
Status: Complete — live and smoke-tested

## What Happened

Wired OpenRouter into the AI cascade in [[skills/utils/ai.py]] so every pipeline step
tries OpenRouter first before touching Claude CLI. Zero Claude Pro consumption on routine
generation runs going forward.

Continues: [[2026-06-01_OpenRouter-Free-Models-Research]]

## Changes Made

### `skills/utils/ai.py`
- Added `_openrouter_generate()` — `httpx`-based, OpenAI-compatible, reads `OPENROUTER_API_KEY` and `OPENROUTER_DEFAULT_MODEL` from `.env`
- Registered `"openrouter"` in `PROVIDER_MAP`
- Updated `DEFAULT_CASCADE`: `["claude", "nim", "ollama"]` → `["openrouter", "claude", "nim", "ollama"]`
- Updated `draft()` and `polish()` wrappers to match

### `.env`
- Added `OPENROUTER_API_KEY=sk-or-v1-...`
- Added `OPENROUTER_DEFAULT_MODEL=google/gemma-4-31b-it:free`

## Model Selected

`google/gemma-4-31b-it:free` — free tier, no cost, hosted by OpenRouter.
To swap: change `OPENROUTER_DEFAULT_MODEL` in `.env`. No code changes needed.

## Verified

Smoke test passed:
```
{'text': "Hello, I hope you're well.", 'success': True, 'provider': 'openrouter/google/gemma-4-31b-it:free'}
```

Fallback confirmed: with key unset, cascade falls through to `claude/cli` cleanly.

## Pipeline Coverage

All 8 steps now route through OpenRouter:
`/researcher` → `/ideation` → `/hook` → `/outline` → `/title` → `/cascade` → `/short-form` → `/voice-cleanup`

Claude CLI fires only on OpenRouter failure.

## Open Items
- [ ] Per-skill model routing (future optimization) — see [[2026-06-01_OpenRouter-Free-Models-Research]] for the recommended model-per-step table

## References
- Implements: [[Local_First_Skill_Engine_Plan]]
- Modifies: [[skills/utils/ai.py]]
- Continues: [[2026-06-01_OpenRouter-Free-Models-Research]]
- Related: [[project_cascade_gemini_to_claude_swap]]
