# Plan: Phase 3 Loose Ends Audit & Remediation

**Status:** Ready for review  
**Date:** 2026-04-15  
**Branch:** `feature/phase3-loose-ends` (new, from `phase-2-production-tasks`)  
**Timeline:** Flexible — comprehensive execution with full testing  
**Execution:** `/orchestrate` via `tools/orchestrator.py` after plan approval

---

## Context

The previous session (2026-04-15) marked Phase 3 as **"100% COMPLETE"** across all 6 tasks. Comprehensive code audit reveals **6 critical/high-severity failures** and **2 medium issues** that block production readiness.

**Root cause:** Multi-agent parallel execution completed features at the model/UI layer but left gaps in database schema, pipeline wiring, security validation, and test coverage. Session verification relied on code existence rather than end-to-end data flow testing.

---

## Findings Summary

|#|Issue|Severity|Task|Impact|
|---|---|---|---|---|
|1|Supabase schema missing 4 brand_configs columns|CRITICAL|T3.1|Data silently dropped — style features non-functional|
|2|reference_creators field unused in pipeline|CRITICAL|T3.1|Users configure creators → ignored by video rendering|
|3|A/B Testing is advisory-only, no experiment execution|HIGH|T2.3|No way to run, track, or conclude experiments|
|4|Remotion auth conditional — allows bypass|HIGH|T2.1|Unauthenticated renders possible if secret unset|
|5|Mock mode auth too permissive in production|HIGH|T1.2|All users share DummyUser if JWT_SECRET missing|
|6|General trending job never integration tested|MEDIUM-HIGH|T3.2|First scheduled run could fail silently|
|7|Library search only on title field (ILIKE)|MEDIUM|T2.2|Works but shallow — no full-text search|
|8|ErrorBoundary/Toast not wired to all error paths|MEDIUM|T2.3.2|Users have limited error visibility|

---

## Detailed Findings & Fixes

### CRITICAL #1: Supabase Schema Missing Brand Fields

**Evidence:** `supabase/migrations/001_initial_schema.sql` lines 120-133 — `brand_configs` table has only: `primary_color`, `secondary_color`, `accent_color`, `font_family`, `logo_url`, `watermark_enabled`, `watermark_text`. No migration (001-004) adds the Phase 3 fields.

**Meanwhile:** `backend/brand/models.py` defines `transition_style`, `reference_creators`, `custom_font`, `slide_template`. Frontend UI at `frontend/app/brand/[workflowId]/page.tsx` lines 264-300 renders all 4 fields. `backend/brand/router.py` line 21 calls `model_dump()` which includes them.

**Result:** User saves style markers → backend sends to Supabase → columns don't exist → silently dropped or error.

**Fix:** Create migration `supabase/migrations/005_phase3_brand_fields.sql`:

```sql
ALTER TABLE public.brand_configs
ADD COLUMN IF NOT EXISTS custom_font text DEFAULT NULL,
ADD COLUMN IF NOT EXISTS slide_template text DEFAULT 'default',
ADD COLUMN IF NOT EXISTS transition_style text DEFAULT 'dynamic',
ADD COLUMN IF NOT EXISTS reference_creators jsonb DEFAULT '[]'::jsonb;
```

**Files:** Supabase migration only. Backend/frontend already correct.

---

### CRITICAL #2: reference_creators Unused in Pipeline

**Evidence:**

- Defined in `backend/intelligence/voice.py` line 43: `reference_creators: list[str] = field(default_factory=list)` ✅
- UI accepts input at `frontend/app/brand/[workflowId]/page.tsx` line 289 ✅
- **NOT extracted** in `backend/content/storyboard.py` — only `transition_style` extracted at line 83, `reference_creators` absent
- **NOT passed** in `backend/content/renderer_video.py` payload (lines 5-27)
- **NOT in** `remotion-service/src/compositions/HookBodyCTAComposition.tsx` HookBodyCTAProps interface (lines 4-20)

**Fix:**

1. `backend/content/storyboard.py` — Extract `reference_creators` from brand dict, include in storyboard frame metadata
2. `remotion-service/src/compositions/HookBodyCTAComposition.tsx` — Add `reference_creators?: string[]` to HookBodyCTAProps brand interface
3. Remotion composition can use creators for style cue text overlays or metadata (MVP: pass through, display as attribution)

---

### HIGH #3: A/B Testing — Full Pipeline Required

**Current state:** Only "Hypothesis Framework" section loaded from `ab-testing.md` into `synthesis.py:_generate_alternatives()` at line 465. Strategy suggestions include hypothesis text. No execution infrastructure exists.

**Full pipeline design:**

#### Database — `supabase/migrations/006_ab_experiments.sql`

```sql
create table public.ab_experiments (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    user_id uuid not null,
    name text not null,
    hypothesis text not null,
    metric text not null check (metric in ('engagement_rate','views','shares','comments','saves','ctr')),
    variant_a_content_id uuid not null references public.content_items(id) on delete cascade,
    variant_b_content_id uuid not null references public.content_items(id) on delete cascade,
    status text not null default 'draft' check (status in ('draft','running','concluded','archived')),
    results_a jsonb default '{"views":0,"engagement_rate":0,"shares":0,"comments":0,"saves":0,"sample_size":0}'::jsonb,
    results_b jsonb default '{"views":0,"engagement_rate":0,"shares":0,"comments":0,"saves":0,"sample_size":0}'::jsonb,
    winner text check (winner in ('a','b',null)),
    winner_confidence_percent float default null,
    started_at timestamptz default null,
    concluded_at timestamptz default null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
alter table public.ab_experiments enable row level security;
create policy "Users can CRUD own experiments" on public.ab_experiments for all using (auth.uid() = user_id);
create index idx_experiments_workflow on public.ab_experiments(workflow_id, status);
```

#### Backend — New router `backend/experiments/`

- `backend/experiments/__init__.py`
- `backend/experiments/models.py` — ExperimentCreateRequest, ResultsSubmissionRequest, ConcludeExperimentRequest
- `backend/experiments/router.py` — 6 endpoints:
    - `POST /api/v1/experiments` — Create experiment (2 content items + hypothesis + metric)
    - `GET /api/v1/experiments?workflow_id=&status=` — List experiments
    - `GET /api/v1/experiments/{id}` — Get details + results
    - `PUT /api/v1/experiments/{id}/start` — Mark running
    - `PUT /api/v1/experiments/{id}/results` — Record results for variant
    - `PUT /api/v1/experiments/{id}/conclude` — Determine winner, feed to memory
- Register in `backend/main.py`: `app.include_router(experiments_router, prefix="/api/v1")`

#### Memory Integration — `backend/intelligence/memory.py`

- New function `update_experiment_learnings(experiment_id, winner, hypothesis, metric)`
- Stores winning patterns in `content_publication_memory.experiment_winners` (jsonb)
- Called as background task on experiment conclusion

#### Synthesis Enhancement — `backend/intelligence/synthesis.py`

- In `_generate_alternatives()`, load past experiment winners from memory
- Inject proven patterns into prompt: "Past experiments showed [angle] won on [metric]"

#### Frontend — 3 new pages

- `frontend/app/content/experiments/page.tsx` — List with Draft/Running/Concluded tabs
- `frontend/app/content/experiments/new/page.tsx` — Creation wizard (select 2 content items, hypothesis, metric)
- `frontend/app/content/experiments/[id]/page.tsx` — Detail view, results submission, conclude

#### Types & API

- `frontend/lib/types.ts` — Add `ABExperiment`, `ExperimentResults` interfaces
- `frontend/lib/api.ts` — Add `experiments` API client object
- `frontend/components/Sidebar.tsx` — Add "Experiments" nav link

---

### HIGH #4: Remotion Auth Conditional Bypass

**Evidence:** `remotion-service/src/index.ts` lines 32-40:

```typescript
const remotionSecret = process.env.REMOTION_SECRET;
if (remotionSecret && remotionSecret.trim()) { // CONDITIONAL
    // validate header
}
// If not set → NO VALIDATION
```

**Fix:** Add startup validation in `backend/main.py` lifespan:

```python
if settings.environment == "production" and not settings.remotion_secret:
    raise RuntimeError("FATAL: REMOTION_SECRET must be set in production")
```

**Files:** `backend/main.py` (add to lifespan startup)

---

### HIGH #5: Mock Mode Auth Too Permissive

**Evidence:** `backend/auth/dependencies.py` lines 28-31:

```python
if not settings.supabase_jwt_secret:
    return DummyUser()  # All requests share one UUID
```

**Fix:** Add to same startup validation:

```python
if settings.environment == "production":
    if not settings.supabase_jwt_secret:
        raise RuntimeError("FATAL: SUPABASE_JWT_SECRET must be set in production")
```

**Files:** `backend/main.py` (same validation block)

---

### HIGH #6: General Trending Job Untested

**Evidence:** `backend/scheduler/jobs.py` lines 75-87 registers `job_general_trending()` with Tuesday 5AM cron. No test exists in `backend/tests/` for this job or the 0.6x blending in `suggestions.py` lines 111-117.

**Fix:** Create `backend/tests/test_general_trending.py`:

- Test `job_general_trending()` with mock Apify
- Test `__general__` entries created correctly
- Test 0.6x blending weight in suggestions
- Test graceful handling of empty results

**Files:** New test file

---

### MEDIUM #7 & #8: Library Search & Error Handling

**Defer to post-launch.** Current implementations are functional:

- Library search works via ILIKE on title — good enough for MVP content volume
- ErrorBoundary and Toast exist at root level — catches critical errors

---

## Execution Plan

### Phase 1: Branch & Schema (10 min)

1. Create branch `feature/phase3-loose-ends` from `phase-2-production-tasks`
2. Apply migration `005_phase3_brand_fields.sql` to Supabase
3. Verify columns exist via `list_tables` / `execute_sql`

### Phase 2: Pipeline Wiring — reference_creators (30 min)

1. Update `backend/content/storyboard.py` — extract and include reference_creators
2. Update `remotion-service/src/compositions/HookBodyCTAComposition.tsx` — add prop
3. Test: brand config → storyboard → Remotion payload includes creators

### Phase 3: Security Hardening (15 min)

1. Add production startup validation to `backend/main.py`
2. Update `.env.example` with `SUPABASE_JWT_SECRET` and `REMOTION_SECRET`
3. Test: app refuses to start without secrets when `ENVIRONMENT=production`

### Phase 4: A/B Testing Full Pipeline (2-3 hours)

1. Apply migration `006_ab_experiments.sql`
2. Create `backend/experiments/` module (models + router)
3. Register router in `backend/main.py`
4. Extend `backend/intelligence/memory.py` with experiment learnings
5. Enhance `backend/intelligence/synthesis.py` to reference past winners
6. Create 3 frontend pages (list, create, detail)
7. Extend `frontend/lib/types.ts` and `frontend/lib/api.ts`
8. Add sidebar navigation link

### Phase 5: Testing (45 min)

1. Create `backend/tests/test_general_trending.py`
2. Create `backend/tests/test_experiments.py`
3. Run full test suite: `pytest backend/tests/`
4. Run frontend tests: `npx vitest run`

### Phase 6: Verification & Documentation (20 min)

1. Full E2E smoke test per verification-before-completion superpower
2. Update `context.md` with accurate state
3. Update task lists
4. Write session log
5. Commit all changes

---

## Files to Create

- `supabase/migrations/005_phase3_brand_fields.sql`
- `supabase/migrations/006_ab_experiments.sql`
- `backend/experiments/__init__.py`
- `backend/experiments/models.py`
- `backend/experiments/router.py`
- `backend/tests/test_general_trending.py`
- `backend/tests/test_experiments.py`
- `frontend/app/content/experiments/page.tsx`
- `frontend/app/content/experiments/new/page.tsx`
- `frontend/app/content/experiments/[id]/page.tsx`

## Files to Modify

- `backend/main.py` — Startup validation + register experiments router
- `backend/content/storyboard.py` — Extract reference_creators
- `backend/intelligence/memory.py` — Add update_experiment_learnings()
- `backend/intelligence/synthesis.py` — Reference past winners
- `remotion-service/src/compositions/HookBodyCTAComposition.tsx` — Add prop
- `frontend/lib/types.ts` — ABExperiment interface
- `frontend/lib/api.ts` — experiments API client
- `frontend/components/Sidebar.tsx` — Navigation link
- `.env.example` — Document new env vars
- `Content-Hub-Vault/00-Management/Memory/context.md` — Update state

## Verification Criteria (Iron Law: Evidence Before Claims)

- [ ]  `SELECT column_name FROM information_schema.columns WHERE table_name='brand_configs'` shows all 4 new columns
- [ ]  `SELECT * FROM ab_experiments LIMIT 1` — table exists
- [ ]  Brand save → DB → API response round-trips all style fields
- [ ]  reference_creators appears in storyboard payload (log or test)
- [ ]  App crashes on startup with `ENVIRONMENT=production` and empty secrets
- [ ]  App starts normally with `ENVIRONMENT=development` and empty secrets
- [ ]  `pytest backend/tests/` — all tests pass including new ones
- [ ]  `npx vitest run` — all frontend tests pass
- [ ]  Full experiment lifecycle: create → start → submit results → conclude → verify memory updated