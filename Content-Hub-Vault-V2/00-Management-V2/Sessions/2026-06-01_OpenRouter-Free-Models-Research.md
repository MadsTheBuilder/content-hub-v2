---
date: 2026-06-01
type: session-log
status: complete
tags: [openrouter, model-routing, free-models, pipeline]
description: "Research session identifying best OpenRouter free models for the content pipeline — DeepSeek V4 Flash, Nemotron 120B, Gemma 4 31B — with rate limit findings and integration plan."
---

# Session Log: OpenRouter Free Models Research
Date: 2026-06-01
Status: Research complete, integration not yet built

## What Happened

Researched OpenRouter's free model tier to find zero-cost replacements for the paid Claude calls in the [[Local_First_Skill_Engine_Plan]] pipeline. Goal: run the full 8-step pipeline without spending money on most steps.

## Key Findings

### Free Models Selected for Pipeline
Three models chosen from the 26 available free models on OpenRouter:

| Model ID | Use In Pipeline |
|---|---|
| `deepseek/deepseek-v4-flash:free` | `/researcher`, `/ideation`, `/outline`, `/cascade` |
| `nvidia/nemotron-3-super-120b-a12b:free` | `/hook`, `/title`, `/short-form` |
| `google/gemma-4-31b-it:free` | `/voice-cleanup` (structured edits) |

Keep Claude paid only for final voice polish where Kallaway tone quality matters.

### Rate Limits (Confirmed)
- **50 req/day** (no credits) — per account, not per API key. Creating extra keys does not help.
- **1,000 req/day** — unlocked by adding $10 credits once (credits won't be spent since pipeline uses free models)
- **20 req/min** — applies regardless of credit level
- A full pipeline run = ~10–16 requests → 3–5 runs/day free, ~60+ runs/day with $10 unlock

### Compute
No local compute needed. OpenRouter hosts all models on their own infrastructure and routes to available providers automatically.

### Integration Path
OpenRouter uses the OpenAI-compatible API — no new packages needed. Project already has `openai==1.6.1` in `requirements.txt`. Plan is to upgrade to latest openai SDK and add `OPENROUTER_API_KEY` to `.env`.

Fallback chain proposed: DeepSeek V4 Flash → Nemotron 120B → Gemma 4 31B (handles 429s from provider-side rate limiting during peak hours).

## Files Touched
None — research session only. No code written yet.

## Open Items
- [ ] Upgrade `openai` package: `.venv\Scripts\pip install --upgrade openai python-dotenv`
- [ ] Add `OPENROUTER_API_KEY` to `.env`
- [ ] Build `openrouter_client.py` with fallback chain logic
- [ ] Wire client into pipeline skills — swap Ollama calls on `/researcher`, `/ideation`, `/outline`, `/cascade`; swap paid Claude calls on `/hook`, `/title`, `/short-form`

## References
- Implements: [[Local_First_Skill_Engine_Plan]]
- Modifies: [[Current_Sprint]]
- Related: [[project_cascade_gemini_to_claude_swap]] (prior model routing decision)
