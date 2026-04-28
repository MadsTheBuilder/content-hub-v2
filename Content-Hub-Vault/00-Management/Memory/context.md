---
status: Active
last_updated: "2026-04-23"
description: "Master project context for session warm-up."
---

# Project Context: Content Hub

## Current State

The project is a solo-creator content intelligence engine. **Phase 3 remediation is complete** as of 2026-04-23. A/B experiments feature is fully wired (DB → backend → frontend → tests → learning-loop feedback).

**Completion:**
- Phase 1 (MVP Days 1–4): ✅ Complete
- Phase 2 (Video, Intelligence, UX, Testing): ✅ Complete (2 partial items flagged)
- Phase 3 (Refinement + Remediation): ✅ Complete (98 pytest + 14 vitest green)

## Critical Decisions
- **Unified Logic**: Backend (FastAPI) handles all heavy lifting; Frontend (Next.js) is the UI layer.
- **Service Role Bypass**: Backend writes use Supabase service role to bypass RLS for administrative simplicity in the MVP. *Auth hardening is a Phase 3 task.*
- **RAG-First**: PostgreSQL pgvector is the source of truth for all content embeddings.
- **Agentic Second Brain**: The project uses this Obsidian Vault (`Content-Hub-Vault`) for all non-code intelligence and planning.
- **Mock Mode**: If Supabase URL is a placeholder, backend falls back to in-memory dicts. Sidebar shows a mock-mode banner.

## What's Partial (Marked done but incomplete)

- **Remotion Auth (2.1.3):** `REMOTION_URL` is configured in `backend/config.py`, but `remotion-service/src/index.ts` POST `/render` still needs auth middleware review. Partial hardening in Phase 3.
- **Library Search (2.3.1):** Client-side text filter in `frontend/app/content/library/page.tsx`. Backend `/content/library` has no `?search=` parameter — only workflow/type/platform filters. *[Deferred]*
- **A/B Testing:** ✅ Full pipeline complete (2026-04-23): `ab_experiments` table + 6 REST endpoints + 3 frontend pages + `/conclude` wired to `update_experiment_learnings` + `_generate_alternatives` injects past winners into Gemini context.

## What's Not in Git (CRITICAL)

Large amounts of work exist on disk but are untracked:
- `backend/tests/` (87 tests across 6 suites)
- `frontend/__tests__/` (14 tests)
- `frontend/components/ErrorBoundary.tsx`, `Toast.tsx`
- `remotion-service/src/compositions/`
- `backend/prompts/skills/ab-testing.md`
- `pytest.ini`, `frontend/vitest.config.ts`

## Active Work

Phase 3 final completion. Full task list at `Content-Hub-Vault/00-Management/Tasks/Final_Implementation_Plan.md`.

## Recent Milestones
- **2026-04-23:** Phase 3 remediation completed via orchestration — A/B experiments feature shipped end-to-end, `/conclude` wired to learning loop, 2 new test suites (test_general_trending, test_experiments) — 112 tests passing (98 backend + 14 frontend). See [[2026-04-23_Phase_3_Completion_Orchestration]].
- **2026-04-14:** Phase 2.5 test infrastructure built and audited — 101 tests passing (87 backend + 14 frontend)
- **2026-04-14:** Full cross-codebase verification audit completed — verified all Phase 2 checkboxes against actual code
- **2026-04-13 (Day 4):** APScheduler (5 jobs), fallback chains, mock mode — all hardened and documented
- **2026-04-12 (Day 3):** Frontend polish — thumbnail cards, accent color picker, calendar grouping
- **2026-04-11 (Day 2):** Platform strategy rules, learning loops, all 6 marketing skills integrated
- **2026-04-09 (Day 1):** E2E pipeline smoke test — scrape → enrich → synthesize → generate → publish

---
[[Current_Sprint]] | [[00-INDEX]]
