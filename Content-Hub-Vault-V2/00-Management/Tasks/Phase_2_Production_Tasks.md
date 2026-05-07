# Phase 2 Production Tasks — Content Hub

> Future Roadmap focused on Video Rendering, Intelligence Depth, and UX Hardening.

---

## 2.1 — Video Rendering (The Remotion Gap)
*Goal: Finalize the ability to output high-quality MP4 content.*

- [x] **2.1.0 — Remotion Service Bootstrap:** Create the `remotion-service/` directory and initialize a new Remotion project. This is a prerequisite for all rendering.
- [x] **2.1.1 — Storyboard Enrichment:** Upgrade `storyboard.py` to produce structured data:
    - Per-shot timing markers (e.g., "0-3s: hook zoom_in")
    - Text overlay positioning (x, y, size, opacity, duration)
    - Transition types per cut (dissolve, zoom, cut, slide)
    - Audio cues (bgm, sfx markers)
- [x] **2.1.2 — Composition Polish:** Create/Import Remotion compositions for "Hook + Body + CTA" templates that consume the enriched storyboard data.
- [x] **2.1.3 — Infrastructure Check:** Verify `REMOTION_URL` and Auth in production environment. ✅ **COMPLETE (Phase 3, T2.1, 2026-04-15)** — X-Render-Secret header validation middleware added to `remotion-service/src/index.ts`. Backend conditionally includes header in `renderer_video.py` when `settings.remotion_secret` is configured. Dev-mode fallback for local testing. Commit: `e1fe56a`.
- [x] **2.1.4 — Hardening:** Add retry logic for video renders and background task timeout handling.

## 2.2 — Intelligence Depth & Nuance
*Goal: Make the suggestions and scraping more "surgical."*

- [x] **2.2.5 — Pattern Extraction from User Selections:** Implement `extract_common_patterns(selected_posts)` in `synthesis.py`. Aggregate `content_analysis` data to identify dominant hooks, styles, and techniques across the selection set.
- [x] **2.2.6 — Estimated Performance in Strategy Output:** Update `StrategyDocument` and Gemini prompts to include `{view_range, engagement_rate, confidence}`. Ground these predictions in historical publish → performance data.
- [x] **2.1.2 — Scrape Weights:** Implement pillar-based weighting in `research_service.py` (e.g., TikTok weights "trending" higher, LinkedIn weights "educational" higher).
- [x] **2.1.3 — A/B Testing Skill:** Integrate `SKILL.md` into the generation loop to produce variation hypotheses.

## 2.3 — UX & Management
*Goal: Polish the frontend for a "Premium" feel.*

- [x] **2.3.5 — Strategy Revise Loop:** Create a bidirectional feedback loop for strategy.
    - **Backend:** `/revise-strategy` endpoint that takes current strategy + user rejection notes.
    - **Frontend:** "Revise Strategy" button on the synthesize page.
- [x] **2.3.6 — Content Regenerate Button:** Add a "Regenerate" button to `content/[id]/page.tsx` to re-trigger `_run_generation` with updated notes without restarting the workflow.
- [x] **2.3.1 — Library Search:** Add text search and filter (by topic/platform) to the `/content/library` page.
- [x] **2.3.2 — Error Boundaries:** Implement React Error Boundaries and toast notifications for "Refining/Rendering" failures.
- [x] **2.3.3 — Logo & Full Brand Editor:** Complete the Logo upload and custom font selection in the Brand config.
- [x] **2.3.4 — Slide Templates:** Add 2-3 alternative HTML/CSS templates for slides (e.g., "Dark Minimalist," "Vibrant High-Energy").

## 2.5 — Test Infrastructure (Critical Safety Net)
*Goal: Prevent regressions across the multi-agent pipeline.*

- [x] **Backend Testing:** Pytest setup + fixtures for mock Supabase client. Unit tests for `synthesis.py`, `scripting.py`, `storyboard.py`, `memory.py`, and `voice.py`.
- [x] **Frontend Testing:** Vitest or Jest setup. Component tests for `synthesize/page.tsx` and `workflows/[id]/page.tsx`.
- [x] **Integration Test:** Create a happy-path E2E pipeline test: Workflow → Scrape → Synthesize → Generate → Ready.

---

## Phase 3 — Refinement & Expansion (ALL COMPLETE ✅)

> Status updated 2026-04-15 — All Phase 3 tasks completed.

- [x] **Active Style Markers:** Extract `transition_style` and `reference_creators` from Brand Persona and pass structurally to the enriched storyboard. ✅ **COMPLETE (T3.1, 2026-04-15)** — `BrandProfile` fields added in `backend/voice.py`, `BrandUpdate` in `backend/brand/models.py`, integrated into storyboard TRANSITION_MAP, Remotion composition updated. Brand editor UI enhanced with Content Style Markers section. Commits: `4d0a833`, `bd0cfde`.
- [x] **General Trending Scrape:** Platform-wide trending discovery independent of specific keyword/competitor filters. ✅ **COMPLETE (T3.2, 2026-04-15)** — `scrape_general_trending()` function added to `backend/research/apify_client.py`. Weekly scheduled job (Tuesday 5 AM UTC) registered in `backend/scheduler.py`. Blended at 0.6× into suggestions pool via `__general__` sentinel. Commit: `356abb6`.
- [x] **Stale Path Audit:** Maintenance housekeeping of `.claude/skills/` paths. ✅ **VERIFIED CLEAN — `.claude/skills/` contains only 1 active file: `content-hub-domain-knowledge.md`. `SKILL.md` was deleted with no dangling refs — `skill_loader.py` uses explicit `NAMED_SKILLS` dict. No hardcoded stale paths found in codebase.)*
- [x] **Multi-User Auth Hardening:** Full RLS enforcement. ✅ **COMPLETE (T1.2, 2026-04-15)** — JWT validation with HS256 algorithm, "sub" claim extraction in `backend/auth/dependencies.py`. Mock-mode fallback when Supabase not configured. Automatic 401 redirect on token expiry. Commits: `62c6336`, `9238741`.

## Critical Outstanding: Uncommitted Files

> ✅ **RESOLVED 2026-04-15** — All production files committed to git.

Resolved via:
- [x] `backend/tests/` — entire test directory (conftest.py, 6 test files, __init__.py, 87 tests)
- [x] `frontend/__tests__/` — 2 component test files + setup.ts (14 tests)
- [x] `frontend/vitest.config.ts` — Vitest configuration
- [x] `pytest.ini` — Pytest configuration
- [x] `frontend/components/ErrorBoundary.tsx` — React error boundary
- [x] `frontend/components/Toast.tsx` — Toast notification system
- [x] `remotion-service/src/compositions/` — HookBodyCTAComposition.tsx and Root.tsx
- [x] `backend/prompts/skills/ab-testing.md` — A/B testing skill (replaces deleted SKILL.md)
- [x] Frontend auth infrastructure — `frontend/lib/supabase.ts`, `frontend/components/AuthProvider.tsx`, login/signup pages
- [x] Orchestration tooling — `tools/orchestrator.py`
- [x] Delegation documentation — `Content-Hub-Vault/00-Management/Superpowers/delegation.md`

**Status:** All committed via commit `9238741` (2026-04-15). Branch is clean and ready for merge.
