	# Content Hub — Completion Plan (Week of Apr 9–13, 2026)

## Context

The Content Hub project has been migrated to a new directory and a vault-based "Agentic Second Brain" workflow has been established. The user wants an honest assessment of where the project stands against the intended architecture (`Content-Hub-Vault/00-Management/Program-Architecture/intended_generation_tree.md`) and a concrete plan to reach MVP completion within this week.

---

## Status Report: Where We Actually Are

### Realistic Completion: **85%**

The CLAUDE.md claim of "~95% complete" is misleading. The individual files exist and contain real code (~2,500 lines of backend logic, full frontend page set), but completion means the **intended architecture works end-to-end**, not just that files exist. Here's the gap analysis:

| System | Architecture Spec | What's Built | Gap | % Done |
|--------|------------------|-------------|-----|--------|
| **Voice Configuration** | Active pipeline: parse competitors → scrape configs, extract audience signals via Gemini, expand pillars into search terms | Fully implemented in `voice.py` (~150 lines). Gemini-powered persona extraction, pillar expansion, competitor parsing. Triggered on workflow creation. | Minor: no style marker extraction beyond tone/energy | **90%** |
| **Platform Strategy** | Platform-specific rules knowledge base, voice adaptation per platform, scrape weights per pillar/platform | Basic `platform_adapter.py` (~25 lines): caption truncation, platform limits, grouping. No knowledge base, no voice adaptation, no scrape weights. | Major: this is a stub compared to the spec | **30%** |
| **Trending Intelligence** | Competitor profile + keyword + general scraping → enrich with thumbnails + "why it works" analysis + weighted relevance → YouTube-style card grid | Backend: profile + hashtag scraping works (`apify_client.py`), enrichment + relevance scoring works (`synthesis.py`). Frontend: card grid with multi-select + "why it works" expandable. Missing: thumbnail fetching/display, side-panel detail view. | Medium: thumbnails are the visible gap | **80%** |
| **Content Synthesis** | Generate strategy document from selections → user reviews/edits/approves → system learns from modifications → approve or revise loop | Backend: fully implemented (`synthesis.py`, ~310 lines, 3-angle output). Frontend: fully implemented (`content/synthesize/page.tsx`, editable fields, alternatives, notes). | Minor: learning from strategy edits is shallow | **90%** |
| **Script Generation** | Enriched prompts from strategy + voice + memory + research + few-shot + platform rules. Multi-model fallback. Copy-editing refinement pass. | Fully implemented (`scripting.py`, ~265 lines). Builds rich prompts with all intended inputs. Gemini → Claude fallback. Refinement pass with copy-editing skill. | Minor: uses heavy copy-editing skill instead of quick version | **90%** |
| **Asset Rendering** | Slides via Playwright, video via Remotion, talking head as packaged ZIP | Slides: working (`renderer_slides.py`). Talking head: working (`renderer_talking_head.py`). Video: thin wrapper around Remotion (`renderer_video.py`, ~20 lines) — external service dependency, untested. | Medium: Remotion video is the gap | **60%** |
| **Learning Loop** | 4 signal sources (selection, strategy mods, script edits, publish/reject) → memory tracks hook prefs, format prefs, rejection patterns, topics, style notes → improves trending/synthesis/scripting | Selection memory: works. Publication memory: works. Hook style detection: works (regex heuristic). Topic overlap: works. Rejection: basic flag + count. **Missing:** strategy edit feedback not wired to memory, script edit diffs stored but not fed back into prompts, style notes not accumulated. | Significant: feedback loops are half-connected | **55%** |
| **Marketing Skills** | 7 skill files loaded contextually throughout pipeline | Only 3 of 7 skills actively used. `copy-editing.md` in refinement (heavy version), `marketing-psychology.md` partially in synthesis (2/20 sections), `social-content.md` in scripting (2/4 content types only). `content-strategy.md`, `copywriting.md`, `SKILL.md` (A/B testing) unused. | Significant: most skills are decorative | **40%** |
| **Frontend Polish** | Thumbnail cards, proper calendar, complete brand editor, search in library | Thumbnails: not rendered. Calendar: timeline, not real calendar. Brand editor: missing accent color + logo upload. Library: no search. Error boundaries: none. | Medium: visual completeness gaps | **70%** |
| **E2E Integration** | Full pipeline: create workflow → scrape → trending → select → synthesize → generate → render → view → edit → publish | **Unknown.** No evidence the full pipeline has ever been run end-to-end. Individual components work in isolation, but integration is unverified. | Critical: this is the single biggest risk | **???** |

### Where Marketing Skills Fit

**Current usage** (3 checkpoints in the pipeline):
1. `synthesis.py` → `marketing-psychology.md` (2 sections only: Buyers + Persuasion)
2. `scripting.py:_build_prompt()` → `social-content.md` for slides/topic, `copywriting.md` for short_form/talking_head (via `get_scripting_skill()`)
3. `scripting.py:refine_script()` → `copy-editing.md` (full 455-line version)

**What should change:**

| Skill | Current State | Where It Should Be Used |
|-------|--------------|------------------------|
| `content-strategy.md` | **UNUSED** | `synthesis.py` — searchable vs shareable content decisions, pillar matching, prioritization framework |
| `copy-editing-quick.md` | **UNUSED** | Replace `copy-editing.md` in `scripting.py:refine_script()` — lighter, faster, designed for automated passes |
| `copywriting.md` | **UNUSED directly** | `scripting.py:_build_prompt()` — should be loaded for ALL content types as foundational writing principles |
| `marketing-psychology.md` | 2 of 20 sections | Expand to include pricing psychology for monetization content, design models (AIDA, Hick's Law) for conversion content |
| `social-content.md` | slides + topic only | Add for `short_form` and `talking_head` — hook formulas and engagement strategies apply to all social |
| `SKILL.md` (A/B testing) | **UNUSED** | Future: post-generation A/B hypothesis recommendations |

**Key files:**
- `backend/prompts/skill_loader.py` — `load_skill()`, `load_skill_sections()`, `get_scripting_skill()`, `SCRIPTING_SKILL_MAP`
- `backend/content/scripting.py:_build_prompt()` (line ~335) — where scripting skills are injected
- `backend/content/scripting.py:refine_script()` (line ~160) — where copy-editing is loaded
- `backend/intelligence/synthesis.py:_generate_alternatives()` (line ~272) — where psychology is loaded

---

## The Plan: 4 Days to MVP (Apr 10–13)

### Day 1 (Apr 10): E2E Pipeline Smoke Test + Critical Fixes

**Goal:** Answer the most important question — does the pipeline actually work?

**Tasks:**
1. Start backend (`uvicorn backend.main:app --reload --port 8000`)
2. Start frontend (`cd frontend && npm run dev`)
3. Walk the full pipeline manually:
   - Create workflow via `/workflows/new` with real brand voice, competitors, pillars
   - Verify scraping triggers and trending populates
   - View trending cards on `/workflows/[id]`
   - Select posts → synthesize strategy on `/content/synthesize`
   - Approve strategy → generate content
   - View generated content on `/content/[id]`
   - Edit script on `/content/[id]/edit`
   - Publish content
4. Document every failure point
5. Fix critical blockers (anything that prevents the pipeline from completing)

**Files likely touched:** Whatever breaks. This is diagnostic, not planned surgery.

**Exit criteria:** The full pipeline runs from workflow creation to content publication without crashes.

---

### Day 2 (Apr 11): Backend Depth — Platform Strategy + Learning Loop + Skills Integration

**Goal:** Fill the three deepest backend gaps.

#### Task 2A: Platform Strategy Enhancement
Expand `backend/content/platform_adapter.py` from 25 lines to a proper knowledge base:
- Add `get_platform_rules(platform)` → returns ideal_length, hook_window, format, best_practices, content_types, posting_windows (per architecture spec)
- Add `adapt_voice_to_platform(voice_config, platform_rules)` → uses Gemini to adjust tone/style per platform
- Wire into `scripting.py:_build_prompt()` so platform rules inform script generation

#### Task 2B: Learning Loop Completeness
Wire the missing feedback signals:
- `backend/intelligence/memory.py` — add `update_strategy_feedback(workflow_id, original_strategy, user_edits)` to learn from strategy modifications
- `backend/intelligence/memory.py` — add `update_edit_feedback(workflow_id, edit_history)` to extract patterns from script edits and feed back into future prompts
- `backend/content/router.py` — call these new functions from the `/content/edit` and `/content/generate-from-strategy` endpoints
- `backend/intelligence/suggestions.py` — enrich suggestions with learned preferences (hook style, format, topics to avoid)

#### Task 2C: Marketing Skills Full Integration
- `synthesis.py:generate_strategy_document()` — load `content-strategy.md` sections for searchable/shareable decisions and prioritization
- `synthesis.py:_generate_alternatives()` — expand psychology to include pricing + design sections when relevant
- `scripting.py:refine_script()` — switch from `copy-editing.md` to `copy-editing-quick.md`
- `scripting.py:_build_prompt()` — load `copywriting.md` principles for ALL content types alongside existing type-specific skill
- `skill_loader.py:SCRIPTING_SKILL_MAP` — add `social-content.md` for `short_form` and `talking_head` in addition to copywriting

**Files:**
- `backend/content/platform_adapter.py`
- `backend/intelligence/memory.py`
- `backend/intelligence/suggestions.py`
- `backend/content/router.py`
- `backend/intelligence/synthesis.py`
- `backend/content/scripting.py`
- `backend/prompts/skill_loader.py`

**Exit criteria:** Backend serves enriched platform rules, all 4 feedback signals flow to memory, all 6 active skills are loaded at appropriate pipeline stages.

---

### Day 3 (Apr 12): Frontend Polish + Re-integration

**Goal:** Close the visible UX gaps.

#### Task 3A: Trending Card Thumbnails
- `frontend/app/workflows/[id]/page.tsx` — render `thumbnail_url` from `TrendingContent` in card UI
- Backend: add thumbnail extraction in `research/apify_client.py:_normalize_post()` (Apify returns thumbnail data for TikTok/YouTube/Instagram — extract and store the URL)

#### Task 3B: Brand Editor Completeness
- `frontend/app/brand/[workflowId]/page.tsx` — add accent color picker input (field exists in types and backend, just missing from UI form)
- Consider: logo upload can be deferred (requires Supabase Storage integration)

#### Task 3C: Calendar Improvement
- `frontend/app/content/calendar/page.tsx` — group by scheduled/published date instead of created_at if available; at minimum add month headers

#### Task 3D: Re-test E2E
- Run the full pipeline again with Day 2's backend changes
- Verify marketing skills appear in generated scripts (check prompt construction)
- Verify platform rules influence output
- Verify learning signals accumulate in memory

**Files:**
- `frontend/app/workflows/[id]/page.tsx`
- `frontend/app/brand/[workflowId]/page.tsx`
- `frontend/app/content/calendar/page.tsx`
- `backend/research/apify_client.py`

**Exit criteria:** Trending cards show thumbnails, brand editor has all color inputs, calendar groups properly, E2E pipeline passes with enriched backend.

---

### Day 4 (Apr 13): Final Verification + Hardening + Documentation

**Goal:** Verify everything works, harden edge cases, update project state.

#### Task 4A: Scheduler Verification
- Verify APScheduler jobs in `backend/scheduler/jobs.py` actually trigger
- Test: do recurring scrapes fire? Do trend spike detections run?

#### Task 4B: Edge Case Hardening
- Test with no trending data (empty scrape results)
- Test with Gemini API down (verify fallback chain works)
- Test with mock mode vs live mode

#### Task 4C: Update Project Documentation
- Update `CLAUDE.md` with accurate completion state
- Update `Content-Hub-Vault/00-Management/Tasks/Current_Sprint.md`
- Write final session log

**Exit criteria:** Scheduler runs, fallbacks work, documentation matches reality.

---

## What's Explicitly Deferred (Post-Week)

- Remotion video rendering (external service, optional per Tasks.md)
- A/B testing skill integration
- Library search functionality
- Error boundaries on frontend
- Multi-user auth enforcement
- Logo upload in brand editor

---

## Verification Plan

After each day, run this checklist:

1. **Backend health:** `GET /api/v1/status` returns 200 with `mock_mode: false`
2. **Workflow creation:** POST a workflow → verify Voice Engine logs show competitor + pillar parsing
3. **Scraping:** POST scrape → verify trending_content table populates
4. **Trending view:** GET trending → verify enrichment data (content_analysis, relevance_score) present
5. **Synthesis:** POST synthesize with selected post IDs → verify strategy document returns 3 angles
6. **Generation:** POST generate-from-strategy → poll status until ready → verify asset_urls populated
7. **Learning:** Check content_publication_memory table after publish → verify hook_style, topics, content_type_distribution updated
8. **Skills in prompts:** Add temporary logging in `_build_prompt()` to confirm skills are loaded (remove after verification)
