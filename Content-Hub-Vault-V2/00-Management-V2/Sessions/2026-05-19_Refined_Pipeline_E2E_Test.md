---
status: Completed
date: 2026-05-19
type: session_summary
description: End-to-end test of the Refined_Pipeline plan against the multica-ai/andrej-karpathy-skills repo. 3 of 9 steps shipped artifacts (research, Studio reports, cascade); 6 failed on provider timeouts, CLI arg mismatch, and slug mismatch — all bugs documented as outstanding.
tags: [e2e, pipeline, nim, claude-cli, ollama, regression]
---

# Session: Refined Pipeline E2E Test — Karpathy skills repo

Implements: [[Refined_Pipeline]]
References: [[2026-05-19_NLM_Driven_Questions_Architecture]]
Modifies: [[skills/utils/ai.py]] | [[skills/title.py]] | [[skills/research_plan.py]] | [[skills/research_sources.py]]

## What Was Done

Ran the full 9-step E2E test from [[Refined_Pipeline]] using `https://github.com/multica-ai/andrej-karpathy-skills` as input.

Command:
```
python -m skills.pipeline "Andrej Karpathy skills" "https://github.com/multica-ai/andrej-karpathy-skills"
```

### Pre-run fixes
1. `notebooklm-py` was not installed in the active `.venv` — `from notebooklm import ...` raised `ModuleNotFoundError` and the first pipeline run aborted on import of `skills/studio.py`. Fix: `pip install -e notebooklm-py`.
2. Gemini was returning HTTP 503 (high-demand) on every call. Per user direction, replaced Gemini with Claude in every cascade list:
   - `DEFAULT_CASCADE`, `draft()`, `polish()` in `skills/utils/ai.py` → `["nim", "claude", "ollama"]`
   - `skills/title.py:54` → same
   - `skills/research_plan.py:123` → `["nim", "claude"]`
   - `skills/research_sources.py:82` → `["nim", "claude"]`

### Result per step

| #   | Step                  | Status     | Notes                                                                                                                                                                                                                                                                                 |
| --- | --------------------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Research              | ✅          | `10-Research/2026-05-19_andrej_karpathy_skills/research.md`. Notebook `a954c76e-c3b9-47fa-82f3-f70e13407821`. Ran many follow-ups beyond 15 — budget enforcement looks soft.                                                                                                          |
| 2   | Studio reports        | ✅          | `11-Reports/andrej_karpathy_skills/{explainer,technical}_report.md`. NIM picker failed (ReadTimeout) → fell back to hardcoded CUSTOM prompts as designed. Technical report hit "API rate limit or quota exceeded" once but eventually succeeded.                                      |
| 3   | Ideation              | ❌          | `ideation.py` requires `--topic` but `pipeline.py:120` passes `--title`. CLI arg mismatch.                                                                                                                                                                                            |
| 4   | Hook                  | ❌          | All three providers failed: NIM ReadTimeout → Claude CLI `exit code 1` → Ollama `All connection attempts failed`.                                                                                                                                                                     |
| 5   | Outline               | ❌          | Same triple-fail pattern.                                                                                                                                                                                                                                                             |
| 6   | Title                 | ❌          | Same.                                                                                                                                                                                                                                                                                 |
| 7   | Short-form            | ⚠️ partial | NIM occasionally returned 200 OK, occasionally timed out. Script self-reported "❌ One or more generations failed". No `.md` files written to `09-Shorts/`.                                                                                                                            |
| 8   | Cascade               | ✅          | `08-Distribution/2026-05-19_andrej-karpathy-skills/{blog_post,instagram_post,linkedin_post,README}.md`. Claude CLI worked **here** even though it failed in steps 4–6 — needs investigation.                                                                                          |
| 9   | Studio slides + video | ❌          | Pipeline computed `cascade_dir = .../2026-05-19_andrej_karpathy_skills` (underscores from `_slug()`) but `cascade.py` wrote `2026-05-19_andrej-karpathy-skills` (hyphens). Step 9 short-circuited on "cascade directory not found". Would have hit the same Studio rate limit anyway. |

## Files Changed

- `skills/utils/ai.py` — `DEFAULT_CASCADE`, `draft()`, `polish()` swapped Gemini → Claude
- `skills/title.py` — cascade list updated
- `skills/research_plan.py` — `generate_followups()` cascade updated
- `skills/research_sources.py` — primary-source picker cascade updated
- New session log: this file

## Bugs Surfaced (Outstanding)

1. **NIM ReadTimeout dominant.** ~80% of NIM calls time out (60s httpx default). When NIM works it returns 200 OK quickly; when it fails it consumes the full 60s. Need to either lower timeout, add retry, or accept NIM as effectively unavailable in this network.
2. **Claude CLI fails with `exit code 1` from subprocess in steps 4–6 but works in step 8.** Same code path (`_claude_generate` in `ai.py`). Difference might be prompt size or stdin encoding. Needs `stderr` capture to diagnose — current logger swallows it as just `"exit code 1"`.
3. **Ollama not running.** `localhost:11434` connection refused. Cascade's terminal fallback is unavailable.
4. **`ideation.py` CLI contract mismatch.** `pipeline.py:120` calls `--title`; script declares `--topic`. One-line fix in either file.
5. **Slug mismatch between cascade and pipeline.** `pipeline.py:_slug()` returns underscores (`andrej_karpathy_skills`); `cascade.py` writes hyphens (`andrej-karpathy-skills`). Either align slug logic or have pipeline glob the actual cascade dir before step 9.
6. **Research follow-up budget.** Plan says hard cap = 15. Log shows research ran 30+ Q&A pairs. Either `QuestionPlan(budget=15)` isn't being enforced or budget was raised at the call site.
7. **NLM Studio rate limit.** Hit "API rate limit or quota exceeded" during technical report generation. With step 9's planned 3 slide decks + 1 video on the same notebook, this will recur.

## Outstanding

- File a separate hardening pass for items 1–6 above before declaring the refactor "done".
- Re-run E2E once Ollama is running and Claude-CLI failure mode is understood.
- Item 5 is the only one blocking a clean second run — fix it first.
