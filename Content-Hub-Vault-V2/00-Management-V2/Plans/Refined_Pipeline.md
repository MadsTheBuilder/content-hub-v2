---
date: 2026-05-19
type: plan
status: approved — pending implementation
description: Refined NLM-driven content pipeline replacing hardcoded question injection. Approved by user 2026-05-19. Implementation not yet started.
tags: [plan, architecture, nlm, pipeline, refactor, approved]
---

# Refined Pipeline — NLM-Driven Content Engine v1

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[2026-05-19_NLM_Driven_Questions_Architecture]] | [[2026-05-08_Researcher_Fix_Verified]] | [[2026-05-08_YT_Pipeline_Friction_Repair]]
Modifies (pending): [[skills/researcher.py]] | [[skills/yt_pipeline.py]] | [[skills/pipeline.py]] | [[skills/cascade.py]] | [[skills/utils/ai.py]]
Adds (pending): [[skills/studio.py]] | [[skills/helpers/nlm_seed.py]] | [[skills/helpers/nim_picker.py]]

---

## Context

The current pipeline injects hardcoded research questions into NotebookLM (an 8-question list in `researcher.py` + a 12-question prompts file in `yt_pipeline.py`). The most recent eval run (`Content-Hub-Vault-V2/NIM test run/EVAL_REPORT.md`) showed `yt_pipeline.py`'s regex collapses all 12 questions into a single blob — that whole mechanism is brittle and the upstream content drifts every time we touch it.

This refactor stops Claude/yaml from picking the questions. NotebookLM decides what to ask based on the sources it has loaded; NIM picks Studio report formats from NLM's own suggestions; cascade outputs get re-injected into the same notebook to produce slide decks and a LinkedIn video as the terminal step.

**New pipeline order** (voice-cleanup runs as a per-step hook on every text-producing step):
```
/researcher (15 NLM-driven chat queries)
  → NLM Studio: explainer + technical reports   ↳ voice-cleanup (per report)
  → /ideation                                    ↳ voice-cleanup
  → /hook                                        ↳ voice-cleanup
  → /outline                                     ↳ voice-cleanup
  → /title                                       ↳ voice-cleanup
  → /short-form (30s / 60s / 90s)                ↳ voice-cleanup (per script)
  → /cascade (Blog + Instagram + LinkedIn)       ↳ voice-cleanup (per channel)
  → re-inject CLEANED cascade outputs into NLM notebook
  → NLM Studio: 3 slide decks (all channels) + 1 video (LinkedIn only)
```
Twitter is dropped from cascade; replaced with Instagram. Slide decks generated for all 3 channels; video for LinkedIn only.

## Decisions locked with the user

- Stop condition: hard budget = **15** chat queries. No methodology checklist.
- Question seed: `notebooks.get_description().suggested_topics` (static list). When seed yields < 15, extend via existing `generate_followups()` (NIM→Gemini cascade in `skills/research_plan.py`).
- Source discovery (`DISCOVER_SOURCES` RPC): **deferred** — that RPC is stubbed in `notebooklm-py`. v1 ships with seed sources only. ChatReference citations in answers stay preserved in artifacts.
- Reports: call `studio.get_suggested_reports()` first; NIM picks "explainer-like" + "technical-like" from the returned list. Fallback = two `ReportFormat.CUSTOM` reports with hardcoded prompts.
- Cascade: **replace Twitter thread with Instagram**. Slides generated for all 3 channels. Video for LinkedIn only.
- All NLM Studio output (reports, decks, video) generated from the **same notebook** used during research — cascade markdown files are added back as sources before the slides/video step.

---

## Files to modify

### 1. `skills/researcher.py`
- **Archive, don't delete:** move `_RESEARCH_QUESTIONS` (lines 121–153) and `_ANGLE_BATTERY` (lines 156–169) to `archive/2026-05-19_pre-nlm-driven/researcher_legacy_questions.md` (with timestamp + source-of-truth note), then remove from the file.
- **Remove** the two for-loops in `research_one()` (lines ~492–516).
- **Replace** with a single loop driven by `QuestionPlan`:
  - Seed via `seed_questions_from_nlm(notebook_id)` (new helper).
  - Wrap seed in `QuestionPlan(seed, budget=15)`.
  - Loop: `next_question()` → `client.chat.ask()` → `generate_followups(heading, q, answer)` → `plan.add_followup(...)` until queue exhausts or budget hits 15.
- `synthesize_brief()` (lines 173–219) signature is unchanged. Pass collected Q&A as `raw_qa`; pass `angle_raw=[]` since `_ANGLE_BATTERY` is gone.

### 2. `skills/yt_pipeline.py`
- **Remove** `PROMPTS_FILE` (line 26), `SECTION_PATTERN` (line 28), `_load_questions()` (lines 103–105).
- **Replace** line 210:
  ```python
  plan = QuestionPlan(_load_questions(), budget=12)
  ```
  with:
  ```python
  plan = QuestionPlan(asyncio.run(seed_questions_from_nlm(notebook_id)), budget=15)
  ```
- **Archive `prompts/yt_pipeline.md`** to `archive/2026-05-19_pre-nlm-driven/yt_pipeline.md` (don't delete). Add a header note in the archived file pointing to this plan as the reason for retirement.

### 3. `skills/pipeline.py` (orchestrator)
Current order: Research → Hook → Outline → Short-form → Cascade. Rewrite step list to:

1. Research (yt_pipeline.py) → `10-Research/{topic_slug}/`
2. **Studio reports** (`studio.generate_reports`) → `11-Reports/{topic_slug}/` → voice-cleanup
3. **Ideation** (ideation.py, `--research-file`) → `02-Ideas/{topic_slug}/` → voice-cleanup
4. Hook (hook.py, `--research-file` — **fix the missing arg flagged in EVAL_REPORT**) → `05-Hooks/{topic_slug}/` → voice-cleanup
5. Outline (outline.py, `--hook-path`) → `06-Outlines/{topic_slug}/` → voice-cleanup
6. **Title** (title.py, `--outline-path`) → `07-Titles/{topic_slug}/` → voice-cleanup
7. **Short-form** (short_form.py, `--research-file --outline-path`) → `09-Shorts/{topic_slug}/` → voice-cleanup (per script)
8. Cascade (cascade.py, Blog + Instagram + LinkedIn) → `08-Distribution/{topic_slug}/` → voice-cleanup (per channel)
9. **Studio decks + video** (`studio.inject_cascade_and_generate`, reads CLEANED cascade files) → `12-Slides/{topic_slug}/` + `13-Video/{topic_slug}/`

**Voice-cleanup hook**: implement as a thin orchestrator-level helper invoked after each text-producing step. Calls `python -m skills.voice_cleanup <path> --inplace` for every `.md` file just written. Studio binaries (PDF, MP4) skipped. Failures in voice-cleanup log a warning but don't halt the pipeline.

### 4. `skills/cascade.py` + `prompts/cascade.md`
- Rename the Twitter section in `prompts/cascade.md`: `## TWITTER THREAD PROMPT` → `## INSTAGRAM PROMPT`. Rewrite body for Instagram format (carousel-friendly, hashtag block, no 280-char constraint).
- In `cascade.py`: rename `twitter_tpl` references to `instagram_tpl`; output filename `twitter_thread.md` → `instagram_post.md`.

### 5. `skills/utils/ai.py` (NIM error-log fix — small but ships with this work)
- Lines 88–96: change `logger.warning("NIM %s failed: %s", ...)` to log HTTP status + 500-char body preview. EVAL_REPORT noted 60% silent NIM failures; this unblocks debugging.

---

## New modules

### `skills/helpers/nlm_seed.py` (NEW)
Single helper shared by `researcher.py` and `yt_pipeline.py`:

```python
async def seed_questions_from_nlm(notebook_id: str) -> list[tuple[str, str]]:
    async with await NotebookLMClient.from_storage(timeout=60) as client:
        desc = await client.notebooks.get_description(notebook_id)
    return [(t.question, t.prompt or t.question) for t in desc.suggested_topics]
```

API confirmed at `notebooklm-py/src/notebooklm/_notebooks.py:158-212`. `SuggestedTopic` is `(question, prompt)`.

### `skills/studio.py` (NEW)
Two entry points:

**`generate_reports(notebook_id, slug) -> dict`**
1. `client.studio.get_suggested_reports(notebook_id)` → `list[ReportSuggestion(title, description, prompt)]`.
2. NIM picker (see below) selects best explainer-like + technical-like from suggestions.
3. If picker returns null for either slot → fall back to `ReportFormat.CUSTOM` with the prompts below.
4. Download both via `download_report()`, write to `11-Reports/{topic_slug}/{explainer,technical}_report.md`.

**Explainer report — fallback custom prompt:**
> Write a plain-language explainer for an intelligent but non-technical reader (product manager, founder, marketer who doesn't ship code). Goal: the reader can confidently explain this thing to a colleague in 30 seconds after reading.
>
> Required structure:
> 1. **What it is** — one paragraph, no jargon. Anchor with a one-line analogy to something the reader already knows.
> 2. **Why it matters** — concrete real-world impact. Name the problem it removes and what was painful before.
> 3. **How it works (mental model)** — high-level only. No code, no API names, no version numbers. Use a single sustained metaphor across the section.
> 4. **Who should care** — 3 specific reader profiles, one paragraph each, naming the problem each profile solves with this.
> 5. **Tradeoffs and watch-outs** — honest limitations, what it isn't for, where it breaks down.
>
> Style rules: short paragraphs, no bullet-dumps, no marketing-speak ("revolutionize", "unleash", "empower"), no hedging ("might", "could potentially"). Every section opens with a clear topic sentence. Inline cite the sources. Target length: 1200–1800 words.

**Technical report — fallback custom prompt:**
> Write a deep-dive technical and architecture report for a senior engineer evaluating whether to adopt this in production. Goal: the reader can make a build-vs-buy decision and write an ADR after reading.
>
> Required structure:
> 1. **Architecture overview** — components, responsibilities, control flow. Use a text-based diagram (ASCII or mermaid-style) showing how requests/data move.
> 2. **Data flow** — what moves between components, where state lives, sync vs async boundaries, ownership of mutation.
> 3. **Integration surface** — public APIs, SDK shape, extension points, plugin/middleware model. Include a representative code snippet if sources support one.
> 4. **Performance and scale** — concurrency model, throughput numbers if cited, known bottlenecks, resource footprint.
> 5. **Failure modes and resilience** — what happens when a dependency dies, retry/timeout/fallback semantics, idempotency guarantees.
> 6. **Comparison to alternatives** — side-by-side with named competitors if sources mention them. Be specific about where each one wins.
> 7. **Production readiness** — observability hooks, security model, auth model, deployment story, operational gotchas.
>
> Style rules: precise, terminology-correct, no hedging, no analogies. Schema fragments and pseudo-code welcome where they clarify. Cite sources inline. Target length: 2000–3000 words.

**`inject_cascade_and_generate(cascade_dir, notebook_id, slug) -> dict`**
1. For each of `blog_post.md`, `instagram_post.md`, `linkedin_post.md`: `client.sources.add_text(notebook_id, ...)`.
2. `client.studio.generate_slide_deck(format=DETAILED_DECK, length=DEFAULT)` ×3 (one per channel). Download to `12-Slides/{topic_slug}/{blog,instagram,linkedin}_deck.pdf`.
3. `client.studio.generate_video(format=EXPLAINER, style=AUTO_SELECT)` for LinkedIn only. Download to `13-Video/{topic_slug}/linkedin_video.mp4`.

Studio APIs verified in `notebooklm-py/src/notebooklm/_artifacts.py` — all methods exist with `CREATE_ARTIFACT` RPC.

### `skills/helpers/nim_picker.py` (NEW)
Single function: `pick_best_report(suggestions, goal) -> ReportSuggestion | None`. Builds a prompt listing suggestion titles + descriptions, asks NIM to return the best-matching title for `goal` ("explainer" or "technical"). Returns the matching `ReportSuggestion` object or `None` if NIM returns low confidence / no match. Reuses `skills.utils.ai.generate(cascade=["nim"])`.

---

## Vault layout — every stage folder gets a `{topic_slug}/` subfolder

All artifacts for a single topic live under matching `{topic_slug}` subfolders inside the existing numbered stage folders. No date prefix on the topic folder (slugs are stable per topic; dates live in frontmatter and filenames where useful).

```
Content-Hub-Vault-V2/
  10-Research/{topic_slug}/
    research.md
  11-Reports/{topic_slug}/                  # NEW
    explainer_report.md
    technical_report.md
    README.md (notebook_id, suggestions_used, generated_at)
  02-Ideas/{topic_slug}/
    ideation.md
  05-Hooks/{topic_slug}/
    hooks.md
  06-Outlines/{topic_slug}/
    outline.md
  07-Titles/{topic_slug}/
    titles.md
  09-Shorts/{topic_slug}/
    30s_script.md
    60s_script.md
    90s_script.md
  08-Distribution/{topic_slug}/
    blog_post.md
    instagram_post.md
    linkedin_post.md
  12-Slides/{topic_slug}/                   # NEW
    blog_deck.pdf
    instagram_deck.pdf
    linkedin_deck.pdf
    README.md
  13-Video/{topic_slug}/                    # NEW
    linkedin_video.mp4
    README.md
```

**Migration note**: existing files in stage folders that are NOT yet topic-sub-foldered stay where they are; new pipeline runs write into `{topic_slug}/` subfolders. No bulk move in this PR.

---

## Verification

**Unit-level:**
- `pytest skills/tests/test_research_plan.py` — confirm `QuestionPlan(budget=15)` enforces cap, mutable queue still accepts follow-ups.
- New test: `test_seed_from_nlm` mocks `get_description()` and asserts seed conversion.

**Smoke (cheap):**
- Run `python -m skills.researcher --topic "test" --dry-run` (add `--dry-run` flag that prints planned questions without calling NLM/NIM).

**End-to-end (burns credits — run once when ready):**
1. `python -m skills.pipeline "AI agents" "https://github.com/owner/repo"`
2. Verify outputs exist:
   - `10-Research/{topic_slug}/research.md` (15 Q&A pairs, not 8+3)
   - `11-Reports/{topic_slug}/explainer_report.md` + `technical_report.md`
   - `02-Ideas/{topic_slug}/`, `05-Hooks/{topic_slug}/`, `06-Outlines/{topic_slug}/`, `07-Titles/{topic_slug}/` populated
   - `08-Distribution/{topic_slug}/instagram_post.md` (NOT twitter_thread.md)
   - `12-Slides/{topic_slug}/` has 3 PDFs
   - `13-Video/{topic_slug}/linkedin_video.mp4`
3. Open the NLM notebook in browser — confirm cascade sources got injected.

---

## Out of scope / follow-ups

- **`DISCOVER_SOURCES` wrapper in `notebooklm-py`** — needed for mid-loop NIM-gated source addition. Separate library task. Tracked as v2.
- **NIM retry-with-backoff** — only the log-fix ships with this work; structured retry is a separate hardening task.
- **Per-slide revision via `revise_slide()`** — Studio supports it; not used in v1.
- **Bulk migration of existing vault artifacts into `{topic_slug}/` subfolders** — only new pipeline runs write to the new layout; legacy files stay in place.
- **Edge case**: if `suggested_topics` is small AND `generate_followups` exhausts before 15, the loop stops early. That's acceptable — budget is a cap, not a quota.

---

## Critical files

- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\researcher.py`
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\yt_pipeline.py`
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\pipeline.py`
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\cascade.py`
- `c:\Users\madhu\Claude cowork\Content Hub V2\prompts\cascade.md`
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\utils\ai.py`
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\research_plan.py` (no edits — reused as-is)
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\short_form.py` (no body edits — now invoked by pipeline.py with topic-subfolder output path)
- `c:\Users\madhu\Claude cowork\Content Hub V2\skills\voice_cleanup.py` (no body edits — invoked by pipeline.py per-step hook with `--inplace`)
- New: `skills/helpers/nlm_seed.py`, `skills/helpers/nim_picker.py`, `skills/studio.py`
- New archive: `archive/2026-05-19_pre-nlm-driven/researcher_legacy_questions.md`, `archive/2026-05-19_pre-nlm-driven/yt_pipeline.md`
