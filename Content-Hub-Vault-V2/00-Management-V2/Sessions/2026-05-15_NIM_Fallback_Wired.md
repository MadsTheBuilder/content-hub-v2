---
status: Completed
date: 2026-05-15
type: session_summary
description: "Wired NVIDIA NIM (Llama 3.1 70B) as the primary draft fallback in ai.py, replacing local Ollama which was blocked by RAM constraints."
tags: [ai-router, nim, fallback, infrastructure]
---

# Session: NVIDIA NIM Fallback Wired

Implements: [[AI Router]] | Modifies: [[skills/utils/ai.py]], [[backend/config.py]]

## What Was Done

- Investigated Ollama as a local fallback — blocked by RAM (16 GB total, only 2.8 GB free; gemma4:e4b needs 6.7 GB)
- Evaluated alternatives: LM Studio + LM Link (deferred — second PC not available now), Gemini (already wired), NVIDIA NIM, Jarvis Labs (save for TRIBE/batch work)
- Chose NVIDIA NIM: free credits, always-on cloud GPU, OpenAI-compatible API, user has prior experience
- Added `NVIDIA_NIM_API_KEY` to `.env` (user added manually)
- Added `nvidia_nim_api_key` field to `backend/config.py`
- Added `_nim_generate()` provider to `skills/utils/ai.py` — hits `meta/llama-3.1-70b-instruct` via `https://integrate.api.nvidia.com/v1/chat/completions`
- Registered NIM in `PROVIDER_MAP` and updated `DEFAULT_CASCADE` to `nim → gemini → ollama → claude`
- Updated `draft()` convenience wrapper to `nim → gemini → ollama`
- Verified: NIM call returned successfully via `nim/meta/llama-3.1-70b-instruct`

## Files Changed

- `backend/config.py` — added `nvidia_nim_api_key: str = ""`
- `skills/utils/ai.py` — added `_nim_generate()`, updated `PROVIDER_MAP`, `DEFAULT_CASCADE`, `draft()`

## Cascade Now

```
draft()  → NIM (Llama 3.1 70B, free) → Gemini Flash → Ollama
polish() → Claude → Gemini Flash
```

All skills using `draft()` ([[skills/outline.py]], [[skills/cascade.py]], [[skills/hook.py]]) automatically benefit.

## Deferred

- LM Studio + LM Link bridge to second PC — revisit when second PC is available. See [[project_ollama_second_pc]] memory.
- Jarvis Labs credits — reserve for TRIBE v2 fMRI batch scoring or fine-tuning runs.

## Outstanding

- NIM free credits are finite — monitor usage and set up Gemini as the natural fallback (already works).
