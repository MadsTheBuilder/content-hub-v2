---
status: Completed
date: 2026-04-17
type: session_summary
---
# Session: Phase 4 Part 1 — A/B Testing Server Side

## Overview
Built the complete server-side layer of the A/B testing system using orchestrated execution. Three specialist agents (db-agent, pipeline-agent, intelligence-agent) were dispatched across 2 sequential groups. The orchestrator (Opus) planned, dispatched, verified, and fixed a bug caught during the verification phase.

## Orchestration Process

### Phase 1: Recon
An Explore agent scanned the codebase to understand existing patterns before planning:
- `backend/main.py` — 4 routers registered (auth, workflows, content, brand). Import pattern: `from backend.xxx.router import router as xxx_router`.
- `backend/brand/router.py` — Reference FastAPI router using `APIRouter(prefix="/api/v1/brand", tags=["brand"])`, `Depends(get_current_user)`, `get_supabase()`.
- `backend/brand/models.py` — Pydantic pattern: `class XxxUpdate(BaseModel)` with `Optional[...]` fields.
- `backend/intelligence/memory.py` — 293 lines. Async functions, Supabase table operations, cold-start handling.
- `backend/intelligence/synthesis.py` — 516 lines. Confirmed it EXISTS (did not need creation). Has `_generate_alternatives()` at line 448.
- `backend/experiments/` — Did NOT exist yet.
- `supabase/migrations/001_initial_schema.sql` — RLS pattern: `ALTER TABLE ENABLE ROW LEVEL SECURITY` + `CREATE POLICY ... FOR ALL USING (auth.uid() = user_id)`.

### Phase 2: Plan
Decomposed into 3 tasks across 2 groups:
- **Group 1** (sequential): db-agent creates and applies migration
- **Group 2** (parallel): pipeline-agent creates API module + intelligence-agent adds learning functions
- File ownership enforced: no two agents touch the same file

### Phase 3: Approve
User approved the plan.

### Phase 4: Execute

#### Group 1 — db-agent (EASY)
**Task:** Create `ab_experiments` table and apply migration.

Created `supabase/migrations/006_ab_experiments.sql` with:
```sql
create table public.ab_experiments (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null,
    name text not null,
    variant_a jsonb not null default '{}',
    variant_b jsonb not null default '{}',
    status text not null default 'draft'
        check (status in ('draft', 'active', 'concluded')),
    winner text default null,
    metrics jsonb default null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
alter table public.ab_experiments enable row level security;
create policy "Users can CRUD own experiments"
    on public.ab_experiments for all using (auth.uid() = user_id);
```
Applied via Supabase MCP `apply_migration` — returned `{"success": true}`.

#### Group 2a — pipeline-agent (MEDIUM)
**Task:** Create experiments API module and register in main.py.

**`backend/experiments/__init__.py`** — Empty package marker.

**`backend/experiments/models.py`** — 4 Pydantic models:
- `ExperimentCreate(BaseModel)` — `name: str`, `variant_a: dict`, `variant_b: dict`
- `ExperimentUpdate(BaseModel)` — all Optional fields for partial updates
- `ExperimentResult(BaseModel)` — `variant: str` ("a"/"b"), `metric_name: str`, `metric_value: float`
- `ExperimentResponse(BaseModel)` — full response shape with all DB fields

**`backend/experiments/router.py`** — 6 endpoints on `APIRouter(prefix="/api/v1/experiments")`:
1. `POST /experiments` — inserts with `user_id=str(user.id)`, status defaults to 'draft'
2. `GET /experiments` — lists all for user, ordered by `created_at desc`
3. `GET /experiments/{experiment_id}` — single fetch, filtered by id AND user_id, 404 if missing
4. `POST /experiments/{experiment_id}/start` — validates current status is 'draft', transitions to 'active'
5. `POST /experiments/{experiment_id}/record-result` — appends metric to nested dict: `metrics[variant][metric_name] = [values]`
6. `POST /experiments/{experiment_id}/conclude` — validates winner is "a" or "b", sets status to 'concluded'

All endpoints use `Depends(get_current_user)` and filter by `user_id` for row-level isolation.

**`backend/main.py`** — Added import on line 10 and `app.include_router(experiments_router)` on line 70 (after brand_router).

#### Group 2b — intelligence-agent (MEDIUM)
**Task:** Add experiment learnings to memory + synthesis.

**`backend/intelligence/memory.py`** — Added `update_experiment_learnings(experiment_id: str)` after line 293:
- Fetches experiment from `ab_experiments` by ID
- Validates status is "concluded" and winner is "a" or "b"
- Extracts winning variant data (`variant_a` or `variant_b`)
- Looks up user's workflow, then finds their `content_publication_memory` row
- Builds learning note: `[experiment-winner] {name}: variant {A/B} won -- {data_summary}`
- Appends to `recurring_notes` (capped at 10 entries, FIFO)

**`backend/intelligence/synthesis.py`** — Modified `_generate_alternatives()` (line 448+):
- Added DB fetch after skill loader calls: queries `ab_experiments` for 5 most recent concluded experiments
- Builds `experiment_ctx` string with winner summaries (each capped at 200 chars)
- Injected into Gemini prompt as `PAST EXPERIMENT INSIGHTS:` section between brand context and the final instruction

### Phase 5: Handle Results
Both agents reported DONE. Proceeded to verification.

### Phase 6: Verify

**Syntax check:** All 6 Python files pass `py_compile`.

**Scope check:** `git status` confirmed only planned files were touched — no scope violations.

**Bug caught and fixed:** The intelligence-agent's `update_experiment_learnings()` queried `content_publication_memory` with `.eq("user_id", user_id)`, but that table has no `user_id` column — it uses `workflow_id` (FK to `workflows`). Fixed by:
1. Looking up the user's workflow via `workflows` table: `.eq("user_id", user_id).limit(1)`
2. Then querying `content_publication_memory` via the resolved `workflow_id`

## Files Changed

| File | Action | Agent | Details |
|------|--------|-------|---------|
| `supabase/migrations/006_ab_experiments.sql` | Created | db-agent | New table + RLS policy |
| `backend/experiments/__init__.py` | Created | pipeline-agent | Empty package marker |
| `backend/experiments/models.py` | Created | pipeline-agent | 4 Pydantic models (34 lines) |
| `backend/experiments/router.py` | Created | pipeline-agent | 6 FastAPI endpoints (116 lines) |
| `backend/main.py` | Modified | pipeline-agent | +2 lines (import + include_router) |
| `backend/intelligence/memory.py` | Modified | intelligence-agent + orchestrator fix | +80 lines (experiment learnings function) |
| `backend/intelligence/synthesis.py` | Modified | intelligence-agent | +15 lines (experiment winners in prompt) |

## Task Checklist Updated
Updated `Phase_3_Remediation_Tasks.md` Phase 4 section:
- Checked off "Apply migration 006 to Supabase" (was unchecked despite migration being applied)

## Outstanding
- **Pre-existing concern:** `recurring_notes` column on `content_publication_memory` is not tracked in any migration file but is used by existing code (`update_strategy_feedback`, `update_edit_feedback`). Likely added via Supabase dashboard. Not introduced by this session.
- **Phase 4 Part 2 (frontend):** 6 remaining tasks — TypeScript types, API client, sidebar nav, 3 experiment pages
- **Phase 5 (testing):** `test_experiments.py` not yet created
- **Phase 6 (verification):** E2E smoke test for full experiment lifecycle pending
