# MVP Completion Tasks — Content Hub

> Canonical task checklist for the Completion Plan (Apr 10–13, 2026).
> Reference: [[MVP_Completion_Plan]]

---

## Day 1 — E2E Pipeline Smoke Test + Critical Fixes (Apr 9 ✅)

- [x] Start backend on port 8000 (already running, used port 8001 for fresh instance)
- [x] Create workflow via API with real brand voice, competitors, pillars
- [x] Verify Voice Engine triggers — competitor profiles + expanded pillar terms in apify_config ✅
- [x] Trigger scrape — 48/50 posts scraped from TikTok ✅
- [x] Enrich + relevance score all posts — 10 enriched with Gemini analysis, all 50 scored ✅
- [x] Synthesise strategy — 3-angle strategy document returned with psychology principles ✅
- [x] Generate content (slides) — Playwright rendered 5 PNGs, uploaded to Supabase Storage ✅
- [x] Edit script endpoint — works with `edited_script` field ✅
- [x] Publish content — `content_publication_memory` updated (published_count, topics, hook_styles) ✅
- [x] Document and fix all critical blockers (3 bugs found and fixed — see session log)

---

## Day 2 — Backend Depth (Apr 11)

### 2A: Platform Strategy Enhancement
- [x] Add `get_platform_rules(platform)` to `platform_adapter.py` (knowledge base)
- [x] Add `adapt_voice_to_platform()` using Gemini
- [x] Wire platform rules into `scripting.py:_build_prompt()`

### 2B: Learning Loop Completeness
- [x] Add `update_strategy_feedback()` to `memory.py`
- [x] Add `update_edit_feedback()` to `memory.py`
- [x] Wire strategy feedback from `/content/generate-from-strategy` endpoint
- [x] Wire edit feedback from `/content/edit` endpoint
- [x] Enrich `suggestions.py` with learned preferences

### 2C: Marketing Skills Full Integration
- [x] Load `content-strategy.md` in `synthesis.py:generate_strategy_document()`
- [x] Expand psychology sections in `synthesis.py:generate_strategy_document()` (corrected: was `_generate_alternatives()`, completed 2026-04-13)
- [x] Switch `refine_script()` from `copy-editing.md` to `copy-editing-quick.md` ✅ (was already done)
- [x] Load `copywriting.md` for ALL content types in `_build_prompt()`
- [x] Add `social-content.md` for `short_form` + `talking_head` in `SCRIPTING_SKILL_MAP`

---

## Day 3 — Frontend Polish + Re-integration (Apr 12 ✅)
2026-04-12T20:51:53Z
- [x] Render `thumbnail_url` in trending cards (`workflows/[id]/page.tsx`)
- [x] Add thumbnail extraction in `apify_client.py:_normalize_post()` (Already existed, verified)
- [x] Add accent color picker to brand editor (`brand/[workflowId]/page.tsx`)
- [x] Improve calendar grouping (`content/calendar/page.tsx`)
- [x] Re-test full E2E pipeline with Day 2 backend changes
- [x] Verify marketing skills appear in generated script prompts
- [x] Verify platform rules influence script output
- [x] Verify learning signals accumulate in memory tables

---

## Day 4 — Final Verification + Hardening (Apr 13 ✅)
2026-04-13T15:14:00Z

- [x] Verify APScheduler jobs trigger — all 5 jobs verified via test script: scrape_organic, detect_trends, generate_suggestions, weekly_embed, flag_rejections ✅
- [x] Test with empty trending data — graceful fallback confirmed: StrategyDocument always returned, _build_prompt() skips empty sections safely ✅
- [x] Test with Gemini API down — 4-level fallback in scripting (Flash→Flash-Lite→Claude→placeholder), 3-level in synthesis (Flash→Flash-Lite→StrategyDocument default) ✅
- [x] Test mock mode vs live mode — dual toggle documented: Supabase (_is_placeholder()) + Apify (apify_api_key check), independent and correct ✅
- [x] Update `CLAUDE.md` with accurate completion state ✅
- [x] Update `Current_Sprint.md` to reflect final state ✅
- [x] Write final session log in vault → `2026-04-13_Day4_Final_Hardening.md` ✅

---

## Deferred (Post-Week)

> Status updated 2026-04-14 via code verification audit. `[x]` = verified complete in codebase, `[~]` = partial implementation exists, `[ ]` = not yet implemented.

- [x] Remotion video rendering *(Completed in Phase 2.1 — `remotion-service/` bootstrapped, `HookBodyCTAComposition.tsx` created, `renderer_video.py` wired with retry logic + 300s timeout. Commit: `d5bc28d`.)*
- [x] A/B testing skill integration — **Advisory complete** *(`backend/prompts/skills/ab-testing.md` loaded via `skill_loader.py` into strategy generation in `synthesis.py`. Skill informs strategy angles with hypothesis fields. Full experiment execution pipeline is deferred post-launch — no DB table, endpoint, or UI needed for current scope.)*
- [x] Library search functionality *(Completed in Phase 3 (T2.2, 2026-04-15) — Server-side PostgreSQL ILIKE search on title column. Client-side 200ms debounce in `frontend/app/content/library/page.tsx` prevents excessive API calls. Backend `/content/library?search=` parameter filters results server-side. Commit: `7d26e7c`.)*
- [x] Frontend error boundaries *(Completed in Phase 2.3.2 — `frontend/components/ErrorBoundary.tsx` (React class component with retry UI) and `frontend/components/Toast.tsx` (context provider, auto-dismiss 5s, error/success/info types) both exist and are wired into `frontend/app/layout.tsx`.)*
- [x] Multi-user auth enforcement *(Completed in Phase 3 (T1.2, 2026-04-15) — JWT validation with HS256, "sub" claim extraction in `backend/auth/dependencies.py`. Mock-mode fallback when Supabase not configured. Automatic 401 redirect on token expiry. Commits: `62c6336`, `9238741`.)*
- [x] Logo upload in brand editor *(Completed in Phase 2.3.3 — `frontend/app/brand/[workflowId]/page.tsx` has upload UI with preview, `backend/brand/router.py` has `POST /{workflow_id}/logo` endpoint, uploads to Supabase Storage `brand-assets` bucket and stores URL in `brand_configs.logo_url`.)*
