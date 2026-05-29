---
date: 2026-05-15
type: session_summary
description: "Redirected all pipeline LLM calls from Claude to NIM. Added standalone pipeline runner and /run-pipeline skill."
tags: [nim, ai-router, pipeline, automation]
---

# Session: NIM Full Pipeline Takeover

Implements: [[AI Router]] | Modifies: [[skills/utils/ai.py]], [[skills/research_sources.py]], [[skills/research_plan.py]]
Adds: [[skills/pipeline.py]], [[.claude/skills/run-pipeline/SKILL.md]]
References: [[2026-05-15_NIM_Fallback_Wired]]

## What Was Done

Redirected every remaining Claude call in the content pipeline to NIM, and added a standalone pipeline runner so the full pipeline can execute without Claude Code involvement.

### LLM routing changes

| File | Change |
|------|--------|
| `skills/utils/ai.py` | `polish()` cascade: `["claude", "gemini"]` → `["nim", "gemini"]` |
| `skills/utils/ai.py` | `DEFAULT_CASCADE`: removed `"claude"` → now `["nim", "gemini", "ollama"]` |
| `skills/research_sources.py` | cascade `["gemini", "claude"]` → `["nim", "gemini"]` |
| `skills/research_plan.py` | cascade `["gemini", "claude"]` → `["nim", "gemini"]` |

### New files

- `skills/pipeline.py` — subprocess chainer: research → hooks → outline → short-form → cascade. Takes `<topic>` and `<url1,url2,...>` as CLI args. Infers all vault output paths from `{today}_{slug}` convention. Non-fatal on individual step failures (warns and continues).
- `.claude/skills/run-pipeline/SKILL.md` — `/run-pipeline` skill that fires `pipeline.py` in background and steps away.

### Cascade state after this session

```
draft()   → NIM → Gemini → Ollama
polish()  → NIM → Gemini
generate() → NIM → Gemini → Ollama   (Claude removed from DEFAULT_CASCADE)
research_sources / research_plan → NIM → Gemini
```

Claude is now **fully out of the pipeline execution path**.

## Rationale

Reserve Claude tokens for code refinement and development. NIM (Llama 3.1 70B, free credits) handles all content generation during pipeline runs.

## Open Items

- First `/run-pipeline` run will be the live smoke test — monitor NIM call success rates.
- NIM free credits are finite; if credits run dry, Gemini Flash is the automatic fallback.
- `pipeline.py` infers output paths from `{today}_{slug}` — if a skill changes its naming convention, paths will need updating.
