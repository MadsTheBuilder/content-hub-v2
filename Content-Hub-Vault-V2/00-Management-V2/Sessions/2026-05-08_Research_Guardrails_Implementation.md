---
date: 2026-05-08
session_type: implementation
status: complete
---

# 2026-05-08 — Research Guardrails Implementation (4.5→9/10)

Implements: [[Local_First_Skill_Engine_Plan]]
Modifies: [[yt_pipeline]], [[researcher]], [[ideation]]

## What Changed

Implemented all 5 research guardrails from the OpenMythos audit plan to bring default research quality from 4.5/10 to 9/10.

### Files Created

- `skills/research_sources.py` — `collect_primary_sources(topic, seed_urls)` async function. Scrapes yt-dlp descriptions for arxiv/GitHub/PDF/official-doc URLs, falls back to Gemini prompt backstop if < 5 found. Returns `(urls, metadata)`.
- `skills/research_plan.py` — `QuestionPlan` class with word-overlap dedup (60% threshold), budget enforcement (default 12 turns), follow-up queue. `generate_followups()` async function that calls Gemini → Claude cascade on each answer.
- `prompts/research_followups.md` — 6-trigger drill-down prompt (numeric claims without source, named entities, comparison claims, pronoun ambiguity, unverified community claims, stability claims). Limits output to 0-2 follow-ups per answer.

### Files Modified

- `prompts/researcher.md` — Added Lens 7.5 (Competitive Landscape) between Lens 7 and Lens 8. Added `Content Angle Battery` to Output Format.
- `prompts/yt_pipeline.md` — Added Q8 (Competitive Landscape), renamed old Q8 → Q9 (Audience Desires), added Q10-Q12 (Angle Battery: counterintuitive claim, emotional hook, non-technical summary).
- `skills/yt_pipeline.py` — Primary-source pre-flight after seed URL addition. Replaced `for heading, question in questions` loop with `QuestionPlan` loop. Added `asyncio.run(generate_followups(...))` per answer. Frontmatter now includes: `primary_sources_found`, `secondary_sources_added`, `questions_asked`, `questions_deduped`, `followups_generated`, `budget_remaining`.
- `skills/researcher.py` — Primary-source pre-flight adds raw GitHub README (tries `main` then `master` branch). Added `_ANGLE_BATTERY` constant (3 questions). Angle Battery asked after main `chat.ask()`. Result dict carries `angle_battery` and `primary_sources_found`. Brief frontmatter includes `primary_sources_found`. Section output includes `## Content Angle Battery` block.
- `skills/ideation.py` — Reads `primary_sources_found` from research frontmatter, warns if 0.

## Guardrail Coverage

| # | Guardrail | Where implemented |
|---|---|---|
| 1 | Primary-source pre-flight | `research_sources.py` + wired in `yt_pipeline.py` + `researcher.py` |
| 2 | Question dedup | `QuestionPlan.is_duplicate()` in `research_plan.py` |
| 3 | Adaptive follow-up drilling | `generate_followups()` in `research_plan.py`, called per turn |
| 4 | Competitive landscape question | Q8 in `yt_pipeline.md`, Lens 7.5 in `researcher.md` |
| 5 | Content-angle questions | Q10-Q12 in `yt_pipeline.md`, Angle Battery in `researcher.md` and `researcher.py` |

## Open Items

- Verify end-to-end on a live topic (suggested: re-run OpenMythos — see audit plan verification checklist)
- `research_sources.py` Gemini backstop uses training-data URLs, not live search; quality depends on how well-known the topic is
- `QuestionPlan` dedup is word-overlap only (no semantic embedding); may miss paraphrases that share few words
