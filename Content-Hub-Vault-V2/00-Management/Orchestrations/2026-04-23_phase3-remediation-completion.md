---
slug: phase3-remediation-completion
created: 2026-04-23
status: complete
current_group: null
groups_complete: [1, 2, 3]
specialists_involved: [intelligence-agent, frontend-agent]
---

# Orchestration: Phase 3 Remediation — Completion (Experiments Feature + Tests + Docs)

## Recon summary

- `backend/experiments/` router + models + __init__ exist and are registered in `backend/main.py`. 6 endpoints live: list, create, get, start, record-result, conclude.
- `backend/intelligence/memory.py:300-378` — `update_experiment_learnings(experiment_id)` already implemented (single-arg signature; fetches winner/variant from the row itself — cleaner than the task-spec 4-arg shape). **BUT** the `/conclude` endpoint (`backend/experiments/router.py:93-115`) does NOT call it. Wiring gap.
- `backend/intelligence/synthesis.py:448-529` — `_generate_alternatives()` already loads past experiment winners (lines 470–480) and injects them into the Gemini prompt. No change needed; task checkbox just needs to be flipped.
- `supabase/migrations/006_ab_experiments.sql` applied; table has user_id, name, variant_a/b jsonb, status enum (draft/active/concluded), winner, metrics jsonb, RLS = `auth.uid() = user_id`.
- Frontend patterns: `frontend/lib/api.ts` uses namespaced objects (`workflows`, `content`, `brand`, `auth`); pages use `'use client'`, Framer Motion, gold accent `#C9A96E`; `Sidebar.tsx` has `NAV_ITEMS` array at top.
- Test conventions: `conftest.py` monkeypatches Supabase via `MockSupabaseClient` + resets genai clients. Test files use classes grouping `test_<scenario>` methods. No `test_general_trending.py` yet; `job_general_trending()` lives in `backend/scheduler/jobs.py:75-86`.

## Execution plan

**Tasks:** 5 across 3 groups
**Specialists:** intelligence-agent, frontend-agent

### Group 1 (parallel — 2 tasks)

- **[intelligence-agent | MEDIUM] Wire `update_experiment_learnings` into the `/conclude` endpoint + verify synthesis integration**
  - Files (modify): `backend/experiments/router.py`, `backend/intelligence/memory.py` (verify only), `backend/intelligence/synthesis.py` (verify only)
  - Criteria: `/conclude` calls `update_experiment_learnings(experiment_id)` AFTER the status update succeeds, wrapped in try/except so a learning-memory failure doesn't break the conclude response. Verify memory.py function handles mock mode (no-op when sb client is mock). Verify synthesis.py experiment-winner loading is intact.

- **[frontend-agent | EASY] Shared frontend plumbing — types, API client, sidebar nav**
  - Files (modify): `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/components/Sidebar.tsx`
  - Criteria: `ABExperiment` and `ExperimentResults` interfaces exported from types.ts. `experiments` namespace exported from api.ts with `list()`, `get(id)`, `create(data)`, `start(id)`, `recordResult(id, data)`, `conclude(id, winner)`. Sidebar has new nav link `{ href: "/experiments", label: "Experiments", icon: <lucide icon> }` inserted after Calendar, before workflows section.

### Group 2 (1 task, depends on Group 1)

- **[frontend-agent | MEDIUM] Build 3 experiments pages**
  - Files (create): `frontend/app/experiments/page.tsx`, `frontend/app/experiments/new/page.tsx`, `frontend/app/experiments/[id]/page.tsx`
  - Criteria:
    - `page.tsx` — list view: shows all user experiments as cards with name, status badge (draft/active/concluded), winner if concluded. Link to detail page.
    - `new/page.tsx` — create form: name + variant_a JSON + variant_b JSON (simple textareas with parse validation). POST to `experiments.create`, redirect to detail.
    - `[id]/page.tsx` — detail view: shows variants, metrics table, status. Actions: Start (if draft), Record Result (form: variant a/b, metric_name, metric_value), Conclude (radio: winner a/b, submit). Use existing pages as styling reference.
  - Uses existing `'use client'`, Framer Motion, gold-accent dark theme, api client namespace. No direct fetch calls.

### Group 3 (parallel — 2 tasks, depends on Group 1 backend wiring)

- **[intelligence-agent | MEDIUM] Write `test_general_trending.py`**
  - Files (create): `backend/tests/test_general_trending.py`
  - Criteria: Tests `job_general_trending()` from `backend/scheduler/jobs.py`. Mocks `scrape_general_trending()` to return fake rows per platform. Verifies each of tiktok/instagram/youtube produces a `trending_content` insert tagged appropriately. Handles failure path (one platform raising — job continues to next).

- **[intelligence-agent | MEDIUM] Write `test_experiments.py`**
  - Files (create): `backend/tests/test_experiments.py`
  - Criteria: Full lifecycle test using FastAPI `TestClient`:
    1. Create experiment → assert 200 + experiment has id + status=draft.
    2. Start → status transitions to active.
    3. Record result for variant a (some metric) — twice; verify metrics jsonb appended.
    4. Record result for variant b (same metric).
    5. Conclude with winner=a → status=concluded, winner=a.
    6. Assert `update_experiment_learnings` side-effect landed: `content_publication_memory.recurring_notes` contains a new entry mentioning the winner/experiment name. (Mock-mode friendly — if memory call is no-op in mock, assert at least the call happens and doesn't raise.)
    - Include negative cases: conclude with invalid winner, start an already-active experiment, 404 on unknown id.

### Verification (performed by advisor, not dispatched)

- Run `pytest backend/tests/` — expect all existing tests + 2 new suites green.
- Run `npx vitest run` (from `frontend/`) — expect all existing frontend tests green (no frontend tests added in this orchestration).
- Spot-check: read `backend/experiments/router.py` to confirm wiring; read one experiments page to confirm patterns.
- Update `Content-Hub-Vault/00-Management/Memory/context.md` — flip Phase 3 status to complete.
- Flip Phase_3_Remediation_Tasks.md checkboxes for all completed items.
- Write session log `Content-Hub-Vault/00-Management/Sessions/2026-04-23_Phase_3_Completion_Orchestration.md`.
- Commit.

---

## Agent prompts

### Task: intelligence-agent: Wire update_experiment_learnings into /conclude + verify synthesis
- description: "intelligence-agent: wire experiment learnings into conclude endpoint"
- model: sonnet
- prompt: |
    You are the **intelligence-agent** for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Close a wiring gap: the `/conclude` endpoint in `backend/experiments/router.py` does not call `update_experiment_learnings()` from `backend/intelligence/memory.py`. It must, so concluded experiments feed back into the learning loop. Also verify (read-only) that `synthesis.py _generate_alternatives` still loads past experiment winners correctly.

    ## Scope
    Read for context:
      - backend/intelligence/memory.py (esp. lines 300–378, `update_experiment_learnings`)
      - backend/intelligence/synthesis.py (esp. `_generate_alternatives`, lines ~440–530 — verify experiment-winner loading block is present and intact)
      - backend/experiments/router.py (the full file)
      - backend/database.py (for MockSupabaseClient behavior if needed)
    Modify:
      - backend/experiments/router.py — add the memory call after successful conclude
      - backend/intelligence/memory.py — ONLY if you find a bug or mock-mode gap; otherwise leave alone
    Create: none

    IMPORTANT: Only touch the files listed above. Other agents are working on frontend files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. `/conclude` endpoint calls `update_experiment_learnings(experiment_id)` AFTER the DB update succeeds. Wrap the call in try/except logging.exception so a memory failure does not 500 the conclude response.
    2. Import path is clean (`from backend.intelligence.memory import update_experiment_learnings`).
    3. `update_experiment_learnings` handles mock mode gracefully — if `sb.table(...).execute()` returns empty `.data`, it returns early without raising.
    4. `synthesis.py _generate_alternatives` still loads up to 5 concluded experiments and formats them into the Gemini context block. Report its current shape verbatim.
    5. Zero changes to any file outside the scope list.

    ## When done
    Report your status (DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT) with a summary of what you changed and the verbatim diff snippet for router.py.

### Task: frontend-agent: Shared plumbing (types + api client + sidebar)
- description: "frontend-agent: shared experiments plumbing"
- model: sonnet
- prompt: |
    You are the **frontend-agent** for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Set up the shared frontend scaffolding for the new Experiments feature: TypeScript types, API client namespace, and Sidebar navigation link. Three subsequent page agents depend on these contracts.

    ## Scope
    Read for context:
      - frontend/lib/types.ts (see existing interfaces like Workflow, ContentItem for shape patterns)
      - frontend/lib/api.ts (see existing namespaces: workflows, content, brand, auth)
      - frontend/components/Sidebar.tsx (see NAV_ITEMS array structure)
      - backend/experiments/models.py (authoritative backend contract — match field names exactly)
      - backend/experiments/router.py (authoritative endpoints + response shapes)
    Modify:
      - frontend/lib/types.ts
      - frontend/lib/api.ts
      - frontend/components/Sidebar.tsx
    Create: none

    IMPORTANT: Only touch the three files listed above. Other agents are working on backend files in parallel. Modifying anything else WILL cause conflicts.

    ## Acceptance Criteria
    1. `frontend/lib/types.ts` exports two new interfaces:
       - `ABExperiment` — id, user_id, name, variant_a (Record<string, unknown>), variant_b (Record<string, unknown>), status ('draft' | 'active' | 'concluded'), winner?: 'a' | 'b' | null, metrics?: Record<string, Record<string, number[]>> | null, created_at, updated_at.
       - `ExperimentResults` — shape that mirrors the `metrics` jsonb (variant → metric_name → number[]), plus computed summary fields if helpful (e.g., `avgA: Record<string, number>`, `avgB: Record<string, number>`).
    2. `frontend/lib/api.ts` exports a new `experiments` namespace with:
       - `list(): Promise<{ experiments: ABExperiment[] }>`
       - `get(id: string): Promise<{ experiment: ABExperiment }>`
       - `create(data: { name: string; variant_a: Record<string, unknown>; variant_b: Record<string, unknown> }): Promise<{ experiment: ABExperiment }>`
       - `start(id: string): Promise<{ experiment: ABExperiment }>`
       - `recordResult(id: string, data: { variant: 'a' | 'b'; metric_name: string; metric_value: number }): Promise<{ experiment: ABExperiment }>`
       - `conclude(id: string, winner: 'a' | 'b'): Promise<{ experiment: ABExperiment }>`
       Use the same `fetchAPI` helper and namespace pattern as `workflows` / `content`. Paths: `/api/v1/experiments` etc. If `fetchAPI` already prefixes `/api/v1`, don't double-prefix — match the existing namespaces.
    3. `frontend/components/Sidebar.tsx` gets a new nav item `{ href: "/experiments", label: "Experiments", icon: FlaskConical }` (or any available lucide-react beaker/flask icon) inserted after "Calendar". Import the icon at the top.
    4. No edits to any other file.

    ## When done
    Report your status (DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT) with a summary of the exact exports added and the Sidebar insertion point.

### Task: frontend-agent: Build experiments list + new + detail pages
- description: "frontend-agent: build 3 experiments pages"
- model: sonnet
- prompt: |
    You are the **frontend-agent** for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Build three new pages that expose the A/B experiments feature to the user. The shared types, API client, and sidebar link have already been added in a previous orchestration group — use them as given.

    ## Scope
    Read for context:
      - frontend/lib/types.ts (ABExperiment, ExperimentResults — already added)
      - frontend/lib/api.ts (experiments namespace — already added)
      - frontend/app/content/library/page.tsx (pattern reference for list views)
      - frontend/app/content/new/page.tsx (pattern reference for create/wizard)
      - frontend/app/content/[id]/page.tsx (pattern reference for detail pages)
      - frontend/components/Sidebar.tsx (confirm nav link exists)
    Modify: none
    Create:
      - frontend/app/experiments/page.tsx
      - frontend/app/experiments/new/page.tsx
      - frontend/app/experiments/[id]/page.tsx

    IMPORTANT: Only CREATE the three files listed above. Do not modify types.ts, api.ts, or Sidebar.tsx — they are already done. Do not touch any other page. Modifying anything outside your create list WILL cause conflicts.

    ## Acceptance Criteria
    1. All three files start with `'use client';` and use the project styling (dark bg `#080F1A`, gold accent `#C9A96E`, slate borders `#334155`).
    2. List page (`experiments/page.tsx`):
       - Fetches experiments via `experiments.list()` in a `useEffect`.
       - Renders cards in a grid: name, status badge (colored by status), winner indicator if concluded.
       - "New experiment" button top-right links to `/experiments/new`.
       - Each card links to `/experiments/{id}`.
       - Loading + empty states.
    3. New page (`experiments/new/page.tsx`):
       - Form: name (text), variant_a (textarea, JSON), variant_b (textarea, JSON).
       - On submit: parse JSON, call `experiments.create`, router.push to `/experiments/{id}` on success.
       - Client-side JSON parse error handling (don't submit if invalid).
    4. Detail page (`experiments/[id]/page.tsx`):
       - Fetches via `experiments.get(id)`.
       - Displays: name, status, variant_a JSON, variant_b JSON, metrics table (grouped by variant → metric → values).
       - Actions section (conditional on status):
         - If `status === 'draft'`: "Start experiment" button → `experiments.start(id)` → refresh.
         - If `status === 'active'`: two sub-forms —
           - Record result: variant (a/b radio), metric_name (text), metric_value (number) → `experiments.recordResult`.
           - Conclude: winner (a/b radio) → `experiments.conclude`.
         - If `status === 'concluded'`: display winner + final metrics, no actions.
       - After each action: refetch to show new state.
    5. Use Framer Motion sparingly (e.g., list card entry, status transitions) — match existing pages, don't nest motion divs.
    6. No raw `fetch()` calls — all API access through the `experiments` namespace.

    ## When done
    Report your status (DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT) with a summary of the 3 files created and any style/pattern decisions worth flagging.

### Task: intelligence-agent: Write test_general_trending.py
- description: "intelligence-agent: test general trending job"
- model: sonnet
- prompt: |
    You are the **intelligence-agent** for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Add integration tests for the scheduled general-trending job. The job is untested end-to-end; we need to prove it loops all platforms and writes to `trending_content`.

    ## Scope
    Read for context:
      - backend/scheduler/jobs.py (esp. `job_general_trending` at ~lines 75–86)
      - backend/research/apify_client.py (for `scrape_general_trending` signature + shape)
      - backend/tests/conftest.py (fixtures + mock-Supabase pattern)
      - backend/tests/test_memory.py (as a terse test-style reference)
    Modify: none
    Create:
      - backend/tests/test_general_trending.py

    IMPORTANT: Only create the one test file. Do not modify scheduler/jobs.py, apify_client.py, or conftest.py. Modifying anything outside WILL cause conflicts.

    ## Acceptance Criteria
    1. Test file uses pytest, imports `job_general_trending` directly, monkeypatches `scrape_general_trending` (module-level patch at the import site used inside jobs.py).
    2. Test case: happy path — mock returns 2 rows per platform for tiktok/instagram/youtube. After `await job_general_trending()`, assert the mock Supabase client has received 3 insert calls to `trending_content` (or 6 if rows inserted individually — match actual implementation).
    3. Test case: failure resilience — mock raises on one platform; job continues to remaining platforms and logs the error (assert via caplog if the job logs, else assert remaining platforms still get inserts).
    4. Test runs under `pytest backend/tests/test_general_trending.py` without touching network.
    5. Style matches existing tests (class-grouped, `test_<scenario>` methods, plain asserts).

    ## When done
    Report your status (DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT) with a summary of test cases and any implementation details (e.g., how insert counting is done on MockSupabaseClient) worth flagging for the verification phase.

### Task: intelligence-agent: Write test_experiments.py
- description: "intelligence-agent: test experiment lifecycle"
- model: sonnet
- prompt: |
    You are the **intelligence-agent** for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Add a full-lifecycle integration test for the A/B experiments feature, including verification that `update_experiment_learnings` is invoked on conclude (the wiring gap that Group 1 closes).

    ## Scope
    Read for context:
      - backend/experiments/router.py (all 6 endpoints)
      - backend/experiments/models.py
      - backend/intelligence/memory.py (`update_experiment_learnings`)
      - backend/tests/conftest.py
      - backend/tests/test_integration_pipeline.py (pattern for TestClient-based flows)
    Modify: none
    Create:
      - backend/tests/test_experiments.py

    IMPORTANT: Only create the one test file. Do not modify router.py, models.py, or memory.py. Modifying anything outside WILL cause conflicts.

    ## Acceptance Criteria
    1. Uses FastAPI `TestClient` (or httpx AsyncClient per existing test-integration pattern) against `backend.main.app`.
    2. Auth: follow the existing test pattern to stub `get_current_user` (see conftest.py or other integration tests for how auth is bypassed in the test suite).
    3. Lifecycle test (single test, stepwise assertions):
       - POST `/api/v1/experiments` with a sample body → 200, response has `experiment.id`, status='draft'.
       - POST `/experiments/{id}/start` → status='active'.
       - POST `/experiments/{id}/record-result` (variant=a, metric_name='ctr', metric_value=0.12) → metrics.a.ctr = [0.12].
       - Repeat record-result for a second value and for variant b.
       - POST `/experiments/{id}/conclude` with `{"winner": "a"}` → status='concluded', winner='a'.
       - Assert `update_experiment_learnings` was invoked (use monkeypatch to spy on it OR verify the side effect — mock-mode-safe: if memory writes are no-ops under mock Supabase, asserting the function is called is sufficient).
    4. Negative cases: conclude with invalid winner 'c' → 400; start an already-active experiment → 400; get/conclude/record on unknown id → 404.
    5. Test runs under `pytest backend/tests/test_experiments.py` offline.

    ## When done
    Report your status (DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT) with a summary of test cases, the auth-stub approach used, and how update_experiment_learnings was asserted (spy vs side-effect).

## Status log
- 2026-04-23 created, status=awaiting-approval
- 2026-04-23 approved (resumed) — model routing: medium→sonnet, easy→haiku
- 2026-04-23 phase 4 dispatch begin — Group 1 (parallel)
- 2026-04-23 Group 1 complete (both DONE) — dispatching Group 2
- 2026-04-23 Group 2 complete (DONE) — dispatching Group 3 (parallel tests)
- 2026-04-23 Group 3 complete (both DONE) — entering Phase 6 verification
- 2026-04-23 verification green (pytest 98 ✓, vitest 14 ✓); docs + session log written; status=complete
