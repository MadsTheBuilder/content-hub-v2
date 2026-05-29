---
date: 2026-05-19
status: completed
type: session_summary
tags: [refined-pipeline, nlm-migration, refactor, implementation]
description: Implementation of Refined_Pipeline.md refactor — migrated from hardcoded questions to NLM-driven question seeding, renamed Twitter to Instagram, reorganized 9-step pipeline with voice-cleanup hooks.
---

# Session: Refined Pipeline Implementation

Implements: [[Refined_Pipeline.md]] | [[Local_First_Skill_Engine_Plan]]  
References: [[2026-05-19_NLM_Driven_Questions_Architecture]]

---

## What Was Done

Complete implementation of the approved Refined_Pipeline.md specification across 9 files created and 5 files modified:

### Files Created (9)

**New helpers module:**
- `skills/helpers/__init__.py` — empty module init
- `skills/helpers/nlm_seed.py` — `seed_questions_from_nlm()` async helper using NotebookLM's `get_description().suggested_topics`
- `skills/helpers/nim_picker.py` — `pick_best_report()` NIM-powered suggestion picker for explainer/technical reports

**New studio module:**
- `skills/studio.py` — two entry points:
  - `generate_reports(notebook_id, slug)` — suggest reports, pick via NIM, fallback to CUSTOM with hardcoded prompts
  - `inject_cascade_and_generate(cascade_dir, notebook_id, slug)` — inject cascade markdown as sources, generate 3 slide decks + 1 LinkedIn video

**Archive:**
- `archive/2026-05-19_pre-nlm-driven/researcher_legacy_questions.md` — archived `_RESEARCH_QUESTIONS` + `_ANGLE_BATTERY` with source-of-truth note
- `archive/2026-05-19_pre-nlm-driven/yt_pipeline.md` — archived 12-question prompt battery with retirement header

### Files Modified (5)

**prompts/cascade.md**
- Renamed `## TWITTER THREAD PROMPT` → `## INSTAGRAM PROMPT`
- Rewrote body for Instagram carousel format (no 280-char limit, hashtag block, swipeable slides)
- Added YAML frontmatter with date, type, description, and wikilinks

**skills/cascade.py**
- Renamed `load_prompts()` to parse for `## INSTAGRAM PROMPT` instead of `## TWITTER THREAD PROMPT`
- Renamed all `twitter_tpl` → `instagram_tpl`
- Renamed output file `twitter_thread.md` → `instagram_post.md`
- Updated console messages and README generation for Instagram

**skills/researcher.py**
- Removed hardcoded `_RESEARCH_QUESTIONS` (8 questions) and `_ANGLE_BATTERY` (3 questions)
- Added imports: `seed_questions_from_nlm`, `QuestionPlan`, `generate_followups`
- Replaced two for-loops in `research_one()` with single NLM-driven loop:
  - Seed from `await seed_questions_from_nlm(notebook_id)`
  - Wrap in `QuestionPlan(seed, budget=15)` (15-question hard cap)
  - Loop: `next_question()` → `client.chat.ask()` → `generate_followups()` → `plan.add_followup()` until budget/queue exhausts
- Added `--dry-run` flag: prints planned questions, exits without calling NLM/NIM
- Updated `synthesize_brief()` to accept optional `angle_raw=None` (NLM loop doesn't produce angle battery anymore)

**skills/yt_pipeline.py**
- Removed `PROMPTS_FILE` constant, `SECTION_PATTERN` regex, `_load_questions()` function
- Added imports: `seed_questions_from_nlm`, `QuestionPlan`, `generate_followups`
- Replaced line 210: `plan = QuestionPlan(_load_questions(), budget=12)` with NLM-driven:
  ```python
  seed_qs = asyncio.run(seed_questions_from_nlm(notebook_id))
  plan = QuestionPlan(seed_qs, budget=15)
  ```

**skills/utils/ai.py**
- Enhanced NIM error logging (lines 90-98):
  - Log HTTP status code + 500-char response body preview (was: silent failure)
  - Unify exception logging to include full error message (up to 500 chars)
  - Goal: unblock debugging of 60% silent NIM failures noted in EVAL_REPORT

**skills/pipeline.py** (complete rewrite)
- Rewrote as 9-step orchestrator (was: 5-step)
- New order:
  1. Research (yt_pipeline.py) → 10-Research/{slug}/
  2. Studio reports (TODO: integrate studio.generate_reports) → 11-Reports/{slug}/ + voice-cleanup
  3. Ideation → 02-Ideas/{slug}/ + voice-cleanup
  4. Hook (with `--research-file` arg) → 05-Hooks/{slug}/ + voice-cleanup
  5. Outline → 06-Outlines/{slug}/ + voice-cleanup
  6. Title → 07-Titles/{slug}/ + voice-cleanup
  7. Short-form → 09-Shorts/{slug}/ + voice-cleanup (per script)
  8. Cascade → 08-Distribution/{slug}/ + voice-cleanup (per channel)
  9. Studio slides + video (TODO: integrate inject_cascade_and_generate) → 12-Slides/{slug}/ + 13-Video/{slug}/
- Added `run_voice_cleanup()` helper to invoke voice_cleanup.py --inplace per text-producing step
- Pipeline-level orchestration only; studio methods exist but not yet wired (TODO placeholders)

---

## Files Changed Summary

| File | Type | Change |
|------|------|--------|
| `skills/helpers/nlm_seed.py` | NEW | Question seeding from NLM |
| `skills/helpers/nim_picker.py` | NEW | NIM-powered report picker |
| `skills/studio.py` | NEW | Report + slide + video generation |
| `archive/2026-05-19_pre-nlm-driven/researcher_legacy_questions.md` | NEW | Archived constants |
| `archive/2026-05-19_pre-nlm-driven/yt_pipeline.md` | NEW | Archived prompt battery |
| `prompts/cascade.md` | MOD | Twitter → Instagram |
| `skills/cascade.py` | MOD | Renamed twitter_tpl → instagram_tpl, output files |
| `skills/researcher.py` | MOD | Removed constants, NLM-driven loop, --dry-run flag |
| `skills/yt_pipeline.py` | MOD | Removed _load_questions, use seed_questions_from_nlm |
| `skills/utils/ai.py` | MOD | Enhanced NIM error logging |
| `skills/pipeline.py` | MOD | Complete rewrite: 5→9 steps + voice-cleanup hooks |

---

## Verification Notes

### Code Conformance
- All new files follow existing style (async/await patterns, error handling, logging)
- API calls verified against notebooklm-py:
  - `NotebookLMClient.from_storage()` ✓
  - `client.notebooks.get_description()` → `SuggestedTopic(question, prompt)` ✓
  - `client.artifacts.suggest_reports()` → `list[ReportSuggestion]` ✓
  - `client.artifacts.generate_report(ReportFormat.CUSTOM, custom_prompt=...)` ✓
  - `client.artifacts.generate_slide_deck(SlideDeckFormat, SlideDeckLength)` ✓
  - `client.artifacts.generate_video(VideoFormat, VideoStyle)` ✓
  - `client.artifacts.wait_for_completion()` ✓
  - `client.artifacts.download_*()` ✓

### Deviations from Plan
None. Plan was executed as specified.

### Iteration 2 Fixes (4-agent review loop)

A 4-agent parallel review loop (Validator + Smoke Tester + Verifier) ran against Iteration 1 and found 2 gaps + 1 style issue. All were resolved in Iteration 2.

**Gaps fixed:**
1. `pipeline.py` step 2 — wired `studio.generate_reports(notebook_id, slug)`: reads `notebook_id` from `research.md` YAML frontmatter, calls studio, runs voice-cleanup on reports; graceful skip if `notebook_id` missing
2. `pipeline.py` step 9 — wired `studio.inject_cascade_and_generate(cascade_dir, notebook_id, slug)`: uses `notebook_id` from step 2 scope, determines cascade_dir from step 8 output; graceful skip if unavailable
3. `yt_pipeline.py` — duplicate inline imports consolidated to module level

**Confirmed:** `yt_pipeline.py` writes `notebook_id:` to `research.md` frontmatter (line 243) — both studio steps will execute at runtime.

**Final review verdict (Iteration 2):** ALL CLEAR across all 3 agents.

### TODOs / Follow-ups

1. **Test coverage:**
   - New test needed: `test_seed_from_nlm()` mocking `get_description()` and verifying seed conversion
   - New test needed: `test_nim_picker()` verifying report selection logic

2. **End-to-end (costly — next session):**
   - Full pipeline run on a real repo (burns NotebookLM + NIM credits)
   - Verify all 9 outputs exist with correct folder structure
   - Verify cascade sources injected into notebook before slides/video generation

---

## Outstanding Items

Pipeline is implementation-complete and verified. E2E run deferred to next session (user's explicit instruction).
