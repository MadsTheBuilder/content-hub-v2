---
name: fixture-01-minimal
description: Minimal 3-task 2-group orchestration fixture for the manual eval harness
---

# Fixture 01 — Minimal

A tiny cross-domain task that exercises all six phases of the orchestrate skill without doing real production work. Exists so the harness has something safe to drive.

## User request (paste this after `/orchestrate`)

> Add a `GET /api/v1/ping` endpoint that returns `{"pong": true}`. Also add a `PING_ENDPOINT` constant to the frontend API client, and add a "Ping" link to the sidebar nav that points to a new `/ping` page which calls the endpoint and displays the response.

## Expected Phase 2 decomposition

3 tasks across 2 groups.

### Group 1 (parallel — independent files)

- **[pipeline-agent | EASY]** Add `GET /api/v1/ping` endpoint
  - Files to modify: `backend/main.py` (or wherever the FastAPI app lives) — add one route
  - Acceptance: `curl http://localhost:8000/api/v1/ping` returns `{"pong": true}`

- **[frontend-agent | EASY]** Add `PING_ENDPOINT` constant + ping call to API client
  - Files to modify: `frontend/lib/api.ts` — add const + export a `ping()` method
  - Acceptance: `api.ping()` exists and calls `GET /api/v1/ping`

### Group 2 (depends on Group 1 — frontend page wires to both)

- **[frontend-agent | EASY]** Add `/ping` page + sidebar link
  - Files to modify: `frontend/app/ping/page.tsx` (new), `frontend/components/Sidebar.tsx`
  - Acceptance: Page renders, calls `api.ping()`, displays the response; sidebar shows "Ping" link

## Expected file writes (exhaustive)

Any file NOT in this list that gets modified during the run is a scope violation — **FAIL the harness**.

- `backend/main.py` — one new route
- `frontend/lib/api.ts` — one new const + one new method
- `frontend/app/ping/page.tsx` — new file
- `frontend/components/Sidebar.tsx` — one new nav item

## Expected state file fields

After Phase 6:
```yaml
slug: add-ping-endpoint   # or similar
status: complete
current_group: 2
groups_complete: [1, 2]
specialists_involved: [pipeline-agent, frontend-agent]
```

## Cleanup after the run

Since this is a throwaway fixture, revert all four files to their pre-run state:

```bash
git checkout -- backend/main.py frontend/lib/api.ts frontend/components/Sidebar.tsx
rm -f frontend/app/ping/page.tsx
rmdir frontend/app/ping 2>/dev/null || true
```

Also delete the state file created by the run from `Content-Hub-Vault/00-Management/Orchestrations/`.

## Why this fixture is good

- **Covers all 3 domains** the orchestrate skill is designed for: backend route, API client, UI page. Exercises the domain boundaries from AGENTS.md.
- **Two groups** — exercises the dependency-ordering logic (Group 2 depends on Group 1).
- **Small files** — cheap to run, easy to revert.
- **Deterministic expected output** — pass/fail is unambiguous.
- **No real production impact** — the `/ping` endpoint has no side effects; easy to remove.