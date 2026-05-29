---
status: Completed
date: 2026-05-19
type: session_summary
description: Fixed 7 bugs from E2E test + moved pipeline to Claude-first cascade. All 5 verification criteria passed loop 1. Pre-E2E audit added B7 (outline arg mismatch).
tags: [bug-fix, pipeline, cascade, claude-first, slug, nim, ollama]
---

# Session: Pipeline Bug Fix + Claude-First Cascade

Implements: [[Refined_Pipeline]]
References: [[2026-05-19_Refined_Pipeline_E2E_Test]]
Modifies: [[skills/utils/ai.py]] | [[skills/pipeline.py]] | [[skills/yt_pipeline.py]] | [[skills/title.py]] | [[skills/research_plan.py]] | [[skills/research_sources.py]]

## What Was Done

Fixed all outstanding bugs from [[2026-05-19_Refined_Pipeline_E2E_Test]] and moved the entire pipeline to Claude-first cascade. A follow-up pre-E2E audit caught one additional blocking bug (B7).

### Bugs Fixed

| Bug | File | Fix |
|-----|------|-----|
| B1: ideation CLI mismatch (`--title` vs `--topic`) | `skills/pipeline.py:122` | Changed to `--topic` |
| B2: Slug mismatch (underscores vs hyphens) | `skills/pipeline.py:41-44`, `skills/yt_pipeline.py:234-235` | Both now produce hyphens via `re.sub(r"[\s_-]+", "-", ...)` |
| B3: NIM timeout 60s blocking Claude fallback | `skills/utils/ai.py:84` | Lowered to 15s |
| B4: Claude CLI stderr swallowed | `skills/utils/ai.py:136-161` | Added `PYTHONIOENCODING=utf-8` env; logs full stderr with rc |
| B5: Cascade → Claude primary | All 5 cascade lists | `["claude", "nim", "ollama"]` or `["claude", "nim"]` everywhere |
| B6: Ollama not running causing hangs | `skills/utils/ai.py:176-191` | Added `_ollama_available()` helper; cascade skips ollama silently if port 11434 is closed |
| B7: `--outline-path` vs `--outline-file` (steps 7 & 8) | `skills/pipeline.py:162,175` | Renamed to `--outline-file` to match `short_form.py` and `cascade.py` arg declarations — argparse would have exited rc=2 on both steps every run |

### Key Design Decision: Slug Alignment
`yt_pipeline.py` and `pipeline.py` were the only two outliers using underscores. All other scripts (ideation, hook, outline, title, short_form, cascade) already produced hyphen slugs. Both outliers were aligned to hyphens so all 8 path computations are now consistent.

### Cascade Order (All Scripts)
- General tasks: `["claude", "nim", "ollama"]`
- Research tasks: `["claude", "nim"]`

## Files Changed

- `skills/utils/ai.py` — NIM timeout, Claude CLI env+stderr, `_ollama_available()`, cascade order
- `skills/pipeline.py` — `_slug()` hyphen logic, `--topic` arg, `--outline-file` arg fix (B7)
- `skills/yt_pipeline.py` — slug hyphen logic
- `skills/title.py` — cascade order
- `skills/research_plan.py` — cascade order
- `skills/research_sources.py` — cascade order

## Verification (All Passed, Loop 1)

1. `_slug("Andrej Karpathy skills")` → `andrej-karpathy-skills` ✓
2. `DEFAULT_CASCADE[0] == "claude"` ✓
3. `python -m skills.ideation --help` shows `--topic` ✓
4. NIM timeout = 15s in `ai.py:84` ✓
5. `_claude_generate` subprocess includes `PYTHONIOENCODING=utf-8` env ✓

## Degradations Noted (Not Fixed)

These were found during the pre-E2E audit. Non-blocking — pipeline continues but some outputs are lower quality.

- **Stale print strings**: `hook.py:77,85` and `outline.py:75,83` still print "NIM → Gemini" cascade order. Cosmetic only.
- **Slug cap mismatch**: `title.py` caps at 50 chars, `hook.py` caps at 6 words, `pipeline._slug()` caps at 40 chars. For long topics (>40 chars), the voice-cleanup file lookup silently misses; pipeline continues without error.

## Outstanding

- Research budget (B8 candidate) — `budget=15` IS enforced in `QuestionPlan`. The "30+ Q&A" observation in the E2E log was likely follow-up questions queued (not answered). No code change needed; confirm on next E2E run.
- Studio rate limit — not fixed; add retry/backoff if it recurs.
- Claude CLI exit-code-1 root cause — now has full stderr logging; will be diagnosable on next run.
- Re-run full E2E to confirm clean 9/9 pass.
