---
slug: phase3-orchestration-code-review
created: 2026-04-27
status: complete
current_group: 4
groups_complete: [1, 2, 3, 4]
specialists_involved: [pipeline-agent, intelligence-agent, frontend-agent, db-agent]
---

# Orchestration: Code Review of Phase 3 Remediation Orchestration

## Recon summary

- **Target orchestration:** `Phase 3 Remediation — Completion (2026-04-23)`, status `complete` per its state file. Shipped A/B experiments end-to-end (commit `7b31ce2`) plus brand-field plumbing (commit `3060ccc`) on branch `feature/phase3-loose-ends`.
- **18 production files touched across 4 subsystems.** Backend experiments module (3 new files), backend integrations (storyboard, main, intelligence/memory, intelligence/synthesis), 2 new test files, 4 frontend files (3 new pages + types/api/sidebar), 2 new migrations (005 brand fields, 006 ab_experiments), 1 Remotion composition.
- **Prior orchestration verification claimed:** pytest 98 passed, vitest 14 passed, spot-checks. We are auditing whether those green checks hide bugs the agents didn't test for.
- **Known loose ends called out by recon (pre-existing, not from this orchestration):** `datetime.utcnow()` deprecation in `backend/experiments/router.py:113`; missing `@supabase/supabase-js` in `frontend/node_modules`; `content_calendar` RLS disabled. These will be inputs to the review, not auto-targets — reviewers will assess whether they fall into scope.
- **Two un-executed orchestrations exist** (`approval-workflow`, `views-count-feature`) — both `awaiting-approval`. Out of scope for this review.
- **Clean domain split possible:** every file maps to exactly one of pipeline-agent / intelligence-agent / frontend-agent / db-agent. Reviewers can run fully parallel with zero file overlap.

## Execution plan

**Loop semantics (per user instruction):** Group 1 → Group 2 → Group 3 → Group 4. If Group 4 finds residual bugs, loop back to Group 3 with a fresh fix batch. The loop terminates only when Group 4 reports clean (no new bugs, tests green, spot-check clean). The user pre-authorized this loop, so we do not pause for re-approval between iterations — only the initial plan needs approval.

### Group 1 — Parallel code review (read-only, no edits)

All four reviewers run in parallel. Each produces a structured bug report. **Reviewers do not modify any files.**

- **[pipeline-agent | MEDIUM] Review pipeline-side changes**
  Files (read-only): `backend/content/storyboard.py`, `backend/main.py`, `remotion-service/src/compositions/HookBodyCTAComposition.tsx`
  Criteria: Audit `reference_creators` extraction → Remotion payload flow; verify experiments router registration in `main.py` doesn't shadow other routers or drop CORS/auth middleware; check that the Remotion prop addition doesn't break existing prop typing or default rendering. Output: numbered bug list with severity (BLOCKER / HIGH / MEDIUM / LOW / NIT) and file:line refs.

- **[intelligence-agent | HARD] Review experiments module + intelligence integration + tests**
  Files (read-only): `backend/experiments/__init__.py`, `backend/experiments/models.py`, `backend/experiments/router.py`, `backend/intelligence/memory.py` (focus `update_experiment_learnings`), `backend/intelligence/synthesis.py` (focus lines 470–498), `backend/tests/test_experiments.py`, `backend/tests/test_general_trending.py`
  Criteria: Audit the 6 experiment endpoints for input validation, status-transition correctness, race conditions, and the try/except around the memory hook (does it swallow real errors?); verify the synthesis past-winner injection prompt format is parseable; review the two new test files for false-positive risk (mocks too permissive, assertions too weak, async spy correctness). Output: numbered bug list with severity + file:line refs.

- **[frontend-agent | MEDIUM] Review frontend experiments feature**
  Files (read-only): `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/components/Sidebar.tsx`, `frontend/app/experiments/page.tsx`, `frontend/app/experiments/new/page.tsx`, `frontend/app/experiments/[id]/page.tsx`
  Criteria: Audit type-vs-DB-schema field alignment; API path correctness against backend routes; JSON validation UX in the new-experiment form; conditional action rendering on the detail page (stale state on concurrent record-result + conclude); error handling when fetches fail; sidebar integration. Output: numbered bug list with severity + file:line refs.

- **[db-agent | EASY] Review migrations**
  Files (read-only): `supabase/migrations/005_phase3_brand_fields.sql`, `supabase/migrations/006_ab_experiments.sql`
  Criteria: Verify column types, defaults, NOT NULL choices, indexes, RLS policy correctness (especially that policies don't lock out the service role); check for naming consistency with existing migrations and idempotency (`IF NOT EXISTS` where appropriate). Output: numbered bug list with severity + file:line refs.

### Group 2 — Advisor synthesis (no dispatch)

The advisor (Opus, this conversation) consolidates the four bug reports into a single ranked fix list, deduplicating overlaps and validating each finding against the actual code (a finding the advisor cannot reproduce in the source is dropped). The consolidated fix plan is written to a follow-up section of this state file. No user re-approval is requested — the loop runs autonomously per the original instruction.

### Group 3 — Parallel fix dispatch

For each confirmed bug, dispatch ONE specialist (the owner of that file) to apply the fix. Parallel dispatch is gated by the one-task-per-file rule: if two findings touch the same file, they merge into one task. Each fix task is given:
- The bug description + severity
- The exact file:line(s) to change
- The acceptance criterion ("after this change, X is true")

If Group 1 returned zero confirmed bugs, Group 3 is skipped and we go straight to Group 4 to confirm clean state.

### Group 4 — Verification

Run by the advisor (with one or more verifier sub-agents for fresh eyes):
1. `pytest backend/tests/` — must be green
2. `npx vitest run` (in `frontend/`) — must be green
3. `tsc --noEmit` (in `frontend/`) — must be clean
4. **Fresh-eyes re-review:** dispatch a Haiku reviewer over the *fixed* files only, scoped to "did the fix introduce new issues or fail to address the original finding?" Each fix gets a pass/fail.
5. If any fix fails verification OR new bugs surface → loop back to Group 3 with the residual list. Loop terminates when Group 4 returns fully clean.

Maximum loop iterations: 3. If iteration 3 still has residuals, the advisor escalates back to the user with the unresolved list rather than spinning indefinitely.

## Agent prompts

### Task: pipeline-agent: Review pipeline-side changes
- description: "pipeline-agent: review storyboard + main.py + Remotion composition"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Code-review the pipeline-side changes from the Phase 3 Remediation orchestration (commit 7b31ce2 and earlier on branch `feature/phase3-loose-ends`). Find every bug, regression risk, contract violation, and integration gap. DO NOT MODIFY ANY FILES — review only.

    Focus on:
    - `reference_creators` extraction in storyboard.py: is the field shape correct? Does it default safely when missing? Does it survive the storyboard → Remotion payload boundary?
    - `backend/main.py`: experiments router registration — does it correctly wire prefix/tags/auth dependency? Does the import order break startup? Did the import of httpx fix from session 2026-04-23 hold?
    - `HookBodyCTAComposition.tsx`: does the new `reference_creators?: string[]` prop have correct defaults, render conditionally, and not break existing renders that lack the field?

    ## Scope
    Read for context: backend/content/storyboard.py, backend/main.py, remotion-service/src/compositions/HookBodyCTAComposition.tsx, backend/content/router.py (for context on how storyboard is called), backend/experiments/router.py (for understanding the experiments router being registered)
    Modify: NONE
    Create: NONE

    IMPORTANT: This is a READ-ONLY review. Do not edit any file. Other reviewers are auditing other domains in parallel.

    ## Acceptance Criteria
    1. Output a numbered bug list. For each bug: severity (BLOCKER / HIGH / MEDIUM / LOW / NIT), file:line range, one-sentence description, why it's a bug, suggested fix.
    2. If you find no bugs in a file, say so explicitly — silence is not acceptance.
    3. Distinguish bugs introduced by the orchestration from pre-existing issues; flag the latter as `[pre-existing]` so they don't get auto-fixed.

    ## When done
    Report your status:
    - DONE: Review complete, bug list attached
    - DONE_WITH_CONCERNS: Review complete but you have doubts about specific findings (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include the full bug list in your summary.

### Task: intelligence-agent: Review experiments module + intelligence integration + tests
- description: "intelligence-agent: review experiments + memory + synthesis + new tests"
- model: sonnet
- prompt: |
    You are the intelligence-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Code-review the experiments module and intelligence-layer integration shipped by the Phase 3 Remediation orchestration. Find every bug, race condition, validation gap, and weak-test issue. DO NOT MODIFY ANY FILES — review only.

    Focus on:
    - `backend/experiments/router.py`: 6 endpoints (list, create, get, start, record-result, conclude). Audit input validation on each, status-transition rules (can a concluded experiment be re-concluded? can record-result happen on a draft?), the try/except around `update_experiment_learnings` (does it swallow real errors? does it log enough?), and `datetime.utcnow()` deprecation if material.
    - `backend/experiments/models.py`: pydantic models — required vs optional fields, default values, validation.
    - `backend/intelligence/memory.py` `update_experiment_learnings`: idempotency, error handling, what happens if the experiment row was deleted between dispatch and execution.
    - `backend/intelligence/synthesis.py` lines ~470–498: past-winner injection — is the prompt format change parseable downstream? does it still work when there are zero past winners?
    - `backend/tests/test_experiments.py` and `backend/tests/test_general_trending.py`: are mocks too permissive? are assertions strong enough to catch regressions? does the async spy on `update_experiment_learnings` actually verify the call happened?

    ## Scope
    Read for context: backend/experiments/__init__.py, backend/experiments/models.py, backend/experiments/router.py, backend/intelligence/memory.py, backend/intelligence/synthesis.py, backend/tests/test_experiments.py, backend/tests/test_general_trending.py, supabase/migrations/006_ab_experiments.sql (for schema cross-check)
    Modify: NONE
    Create: NONE

    IMPORTANT: This is a READ-ONLY review. Do not edit any file. Other reviewers are auditing other domains in parallel.

    ## Acceptance Criteria
    1. Numbered bug list with severity (BLOCKER / HIGH / MEDIUM / LOW / NIT), file:line range, description, root cause, suggested fix.
    2. Specifically validate: does the conclude endpoint correctly fire the memory hook only after a successful DB update? Is the try/except scope appropriate?
    3. Specifically validate: do the new tests fail if the production code is broken? (consider mutation-testing intuition — try to imagine a bug that would slip past each test).
    4. Flag pre-existing issues with `[pre-existing]` so they don't auto-fix.

    ## When done
    Report your status:
    - DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT

    Include the full bug list in your summary.

### Task: frontend-agent: Review frontend experiments feature
- description: "frontend-agent: review experiments pages + types + api client"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Code-review the frontend experiments feature from the Phase 3 Remediation orchestration. Find every bug, type-mismatch, accessibility issue, error-handling gap, and React anti-pattern. DO NOT MODIFY ANY FILES — review only.

    Focus on:
    - `frontend/lib/types.ts`: do `ABExperiment` and `ExperimentResults` field names match the backend models in `backend/experiments/models.py` and the DB schema in `supabase/migrations/006_ab_experiments.sql`? Optional vs required correct?
    - `frontend/lib/api.ts`: do the 6 experiments methods hit the correct backend paths? Are HTTP methods right? Are response types correct?
    - `frontend/app/experiments/page.tsx`: error handling on fetch failure, empty states, loading states.
    - `frontend/app/experiments/new/page.tsx`: JSON validation on the variants field — does invalid JSON give meaningful feedback? Does submit re-enable on error? Does it reset on success?
    - `frontend/app/experiments/[id]/page.tsx`: conditional action rendering based on status — is there a stale-state risk if user clicks record-result then conclude rapidly? Are buttons properly disabled during in-flight requests? Does the page handle a concluded experiment correctly?
    - `frontend/components/Sidebar.tsx`: nav link insertion correct? icon import correct? active state logic intact?

    ## Scope
    Read for context: frontend/lib/types.ts, frontend/lib/api.ts, frontend/components/Sidebar.tsx, frontend/app/experiments/page.tsx, frontend/app/experiments/new/page.tsx, frontend/app/experiments/[id]/page.tsx, backend/experiments/models.py (for cross-check), backend/experiments/router.py (for endpoint cross-check)
    Modify: NONE
    Create: NONE

    IMPORTANT: This is a READ-ONLY review. Do not edit any file. Other reviewers are auditing other domains in parallel.

    ## Acceptance Criteria
    1. Numbered bug list with severity (BLOCKER / HIGH / MEDIUM / LOW / NIT), file:line range, description, root cause, suggested fix.
    2. Explicit table verifying type ↔ backend model ↔ DB column field-by-field.
    3. Explicit table verifying api.ts method ↔ backend route + HTTP verb.
    4. Flag pre-existing issues with `[pre-existing]`.

    ## When done
    Report your status:
    - DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT

    Include the full bug list in your summary.

### Task: db-agent: Review migrations 005 and 006
- description: "db-agent: review brand fields and ab_experiments migrations"
- model: haiku
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Code-review the two migrations shipped by the Phase 3 Remediation orchestration. Find every schema bug, RLS hole, missing index, and compatibility issue. DO NOT MODIFY ANY FILES — review only.

    Focus on:
    - `supabase/migrations/005_phase3_brand_fields.sql`: column types, defaults, NOT NULL choices, idempotency (`IF NOT EXISTS`), naming consistency with `001_initial_schema.sql`.
    - `supabase/migrations/006_ab_experiments.sql`: full table audit — column types, foreign keys, indexes (especially on user_id and status), RLS enablement, RLS policies (do they correctly scope to `auth.uid() = user_id`? does service-role bypass work? is there a SELECT-only or full-CRUD policy mismatch?), check that the migration is forward-compatible with the existing schema and follows project conventions.

    ## Scope
    Read for context: supabase/migrations/005_phase3_brand_fields.sql, supabase/migrations/006_ab_experiments.sql, supabase/migrations/001_initial_schema.sql (for convention reference), backend/experiments/models.py (to verify schema matches model)
    Modify: NONE
    Create: NONE

    IMPORTANT: This is a READ-ONLY review. Do not edit any file.

    ## Acceptance Criteria
    1. Numbered bug list with severity (BLOCKER / HIGH / MEDIUM / LOW / NIT), file:line range, description, root cause, suggested fix.
    2. Explicit RLS table: which roles can do what on `ab_experiments`? Confirm service-role can write.
    3. Schema-vs-model cross-check: every column in `ab_experiments` appears in `backend/experiments/models.py` with matching type.

    ## When done
    Report your status:
    - DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT

    Include the full bug list in your summary.

## Status log
- 2026-04-27 created, status=awaiting-approval
- 2026-04-27 user approved plan, status=approved
- 2026-04-27 dispatching Group 1 (4 parallel reviewers), status=executing
- 2026-04-27 Group 1 returned: 4 BLOCKER candidates, 6 HIGH candidates, ~10 MEDIUM/LOW. Advisor validated against actual code.
- 2026-04-27 Group 2 synthesis complete: 3 BLOCKER + 3 HIGH + 4 MEDIUM = 10 confirmed bugs. Several findings dropped after code-level verification.
- 2026-04-27 dispatching Group 3 (3 parallel fix tasks: frontend, backend-experiments, db-migration), current_group=3
- 2026-04-27 Group 3 fixers all returned DONE: frontend (response-key + id guards, tsc clean), intelligence (8 fixes A–H across router/models/synthesis/content-router, 11/11 tests pass), db (migration 007 applied to Supabase: 3 indexes + 4 per-action RLS policies)
- 2026-04-27 Group 4 verification: pytest 98/98 PASS, vitest 14/14 PASS, tsc --noEmit clean, fresh-eyes Haiku review reports 8/8 PASS with zero residuals
- 2026-04-27 loop terminated on iteration 1 (no residuals); status=complete

## Consolidated fix list (Group 3 input)

### BLOCKER
1. `frontend/app/experiments/new/page.tsx:56` — `data.experiment_id` → `data.experiment.id` (response key mismatch breaks create→navigate)
2. `backend/experiments/router.py:61` — start_experiment UPDATE missing `.eq("user_id", str(user.id))` (authz bypass)
3. `backend/experiments/router.py:79-91` — record_result must reject when status != 'active'

### HIGH
4. `backend/experiments/router.py:90` — record_result UPDATE missing user_id filter
5. `backend/experiments/router.py:114` — conclude UPDATE missing user_id filter
6. `backend/intelligence/synthesis.py:471` — past-winner fetch missing user_id filter (must thread user_id through the call chain)

### MEDIUM
7. `backend/experiments/router.py:113` — replace `datetime.utcnow().isoformat() + "Z"` with `datetime.now(timezone.utc).isoformat()`
8. New `supabase/migrations/007_ab_experiments_hardening.sql` — add indexes (user_id, status, (user_id, created_at DESC)) + explicit WITH CHECK policies
9. `frontend/app/experiments/[id]/page.tsx:31` — guard `typeof id === "string"` before cast
10. `backend/experiments/router.py:95` + `backend/experiments/models.py` — replace `body: dict` with typed `ConcludeRequest(BaseModel)`
