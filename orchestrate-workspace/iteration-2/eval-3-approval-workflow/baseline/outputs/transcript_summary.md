# Transcript Summary: Approval Workflow Planning Session

## Date
2026-04-22

## Task
Add a content approval workflow to Content Hub. Content items need an `approval_status` field (draft/pending/approved/rejected). Add a backend endpoint to approve or reject content items, and add approve/reject buttons to the content detail page.

## Investigation Process

### 1. Context Files Read (Session Start Protocol)
- **context.md**: Learned project is at ~95% completion, Phase 2 done, Phase 3 in progress
- **CLAUDE.md**: Stack overview (Next.js 15, FastAPI, Supabase PostgreSQL + pgvector, RLS policies)
- **GRAPH_REPORT.md**: Verified no special abstractions needed for this task
- **AGENTS.md**: Identified relevant specialist roles (db-agent, pipeline-agent, frontend-agent)

### 2. Database Schema Exploration
- Examined migration file: `supabase/migrations/001_initial_schema.sql`
- Found `content_items` table with fields: id, workflow_id, user_id, content_type, platform, title, script_text, published_script, storyboard, asset_urls, **status**, rejection_flag, generation_metadata, error_message, created_at, updated_at
- Note: `rejection_flag` boolean exists but is unused; `status` enum has values: (generating, scripting, rendering, ready, failed, posted)
- Identified that content_items uses RLS policy: "Users can CRUD own content"

### 3. Backend API Structure
- Examined `backend/content/router.py` for existing endpoints
- Found existing endpoints: /generate, /synthesize, /generate-from-strategy, /revise-strategy, /{content_id}/regenerate, /library, /calendar, /status/{content_id}, /{content_id}, /{content_id}/download, /{content_id}/edit, /{content_id}/publish, /{content_id}
- Publish flow: sets status="posted" and stores published_script
- Auth pattern: all endpoints use `Depends(get_current_user)` for JWT verification

### 4. Frontend Type Definitions
- Examined `frontend/lib/types.ts` ContentItem interface
- Current status field enum: "generating" | "scripting" | "refining" | "rendering" | "ready" | "failed" | "posted"
- No approval_status field currently defined

### 5. Frontend API Client
- Examined `frontend/lib/api.ts`
- Pattern: all methods use `fetchAPI()` helper with JWT auth
- Content methods: generate, status, get, library, calendar, download, edit, publish, delete, editHistory, synthesize, generateFromStrategy, reviseStrategy, regenerate

### 6. Content Detail Page
- Examined `frontend/app/content/[id]/page.tsx`
- Current UI shows status badge, publish button, delete button, download button, regenerate button
- Status displays in badge with color-coding (ready=blue, posted=green, generating=blue, scripting=purple, rendering=yellow, failed=red)

## Key Observations

1. **Existing Rejection Infrastructure**: `rejection_flag` exists in schema but is unused and boolean-only; unsuitable for approval_status workflow
2. **Status Field Overloaded**: Current `status` field tracks generation pipeline state, not approval state
3. **Publish Endpoint**: Currently directly transitions content to "posted" without approval gate
4. **No Approval Role**: No concept of "admin" or "approver" user — single-user MVP (auth hardening is Phase 3 task)
5. **Service Role Pattern**: Backend uses Supabase service_role key for writes, bypassing RLS

## Scope Understanding
The task requires:
1. Add `approval_status` column to `content_items` table with enum (draft/pending/approved/rejected)
2. Add backend endpoint(s) to transition approval_status (approve/reject)
3. Add UI buttons to content detail page for approve/reject actions
4. Integration point: publish endpoint may need to check approval_status (blocked design decision)

## Files That Will Need Changes (Identified)
1. `supabase/migrations/007_content_approval.sql` (NEW) — Add column + check constraint
2. `backend/content/router.py` — Add approve/reject endpoints
3. `backend/content/models.py` — Add ApprovalRequest Pydantic model (if needed)
4. `frontend/lib/types.ts` — Add approval_status to ContentItem interface
5. `frontend/lib/api.ts` — Add approve/reject methods to content object
6. `frontend/app/content/[id]/page.tsx` — Add approve/reject buttons + conditional rendering

## Stopping Point
Task instructions: "Stop before actually executing any code changes — just produce a plan"

This investigation was completed WITHOUT reading orchestrated-execution.md or any skill files, as instructed.
