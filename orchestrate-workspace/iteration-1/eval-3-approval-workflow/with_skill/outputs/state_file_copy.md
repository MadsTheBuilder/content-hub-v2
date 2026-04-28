---
slug: approval-workflow
created: 2026-04-22
status: awaiting-approval
current_group: null
groups_complete: []
specialists_involved: [db-agent, pipeline-agent, frontend-agent]
---

# Orchestration: Content Approval Workflow

## Recon Summary

Phase 1 scan identified the following key areas:

- **Database schema**: `supabase/migrations/001_initial_schema.sql` defines `content_items` table with a `status` column (currently: 'generating', 'scripting', 'rendering', 'ready', 'failed', 'posted'). No approval-related status or field exists yet.
- **Backend models**: `backend/content/models.py` defines request models (ContentGenerateRequest, ContentEditRequest, etc.). No approval request model exists.
- **Backend router**: `backend/content/router.py` handles content generation, synthesis, editing, publishing, deletion. No approval endpoints exist.
- **Frontend types**: `frontend/lib/types.ts` defines `ContentItem` interface with `status` (union of 6 statuses), `rejection_flag`, and other fields. No `approval_status` field.
- **Frontend API client**: `frontend/lib/api.ts` defines content API methods (generate, status, get, library, calendar, download, edit, publish, delete, editHistory). No approve/reject methods.
- **Content detail page**: `frontend/app/content/[id]/page.tsx` displays content with status badge, publish button, edit, regenerate, delete buttons. No approval buttons.
- **Task scope**: Feature adds approval workflow for content items before they are published.
  - New field: `approval_status` (enum: draft, pending, approved, rejected)
  - New backend endpoints: POST `/api/v1/content/{id}/approve` and `/api/v1/content/{id}/reject`
  - New frontend buttons: "Approve" and "Reject" on content detail page
  - Database migration: Add `approval_status` column to `content_items` table

## Execution Plan

**Tasks:** 3 across 3 groups  
**Specialists:** db-agent, pipeline-agent, frontend-agent  
**Complexity:** EASY/MEDIUM. All tasks are straightforward: single schema migration, two API endpoints, two UI buttons.

### Group 1 (parallel)
- [db-agent | EASY] Add approval_status column to content_items table
  Files: supabase/migrations/007_approval_workflow.sql (new)
  Criteria: Migration creates column with 4 enum states, default 'draft', applies to all existing rows

### Group 2 (depends on Group 1)
- [pipeline-agent | EASY] Add approval endpoints (approve / reject)
  Files: backend/content/models.py (modify), backend/content/router.py (modify)
  Criteria: Two new endpoints at /content/{id}/approve and /content/{id}/reject; both return updated content_item; validation ensures only draft/pending items can be approved/rejected

### Group 3 (depends on Group 2)
- [frontend-agent | MEDIUM] Add approval buttons and wire approval API calls
  Files: frontend/lib/api.ts (modify), frontend/lib/types.ts (modify), frontend/app/content/[id]/page.tsx (modify)
  Criteria: Add approve/reject methods to content API client; update ContentItem type; add Approve/Reject buttons on detail page conditional on approval_status; wire onClick handlers; update status badges to include approval_status

## Agent Prompts

### Task: db-agent: Add approval_status column to content_items table
- description: "db-agent: Add approval_status column to content_items table"
- model: haiku
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new database migration that adds an `approval_status` column to the `content_items` table.

    The column should:
    - Be a text enum with 4 possible values: 'draft', 'pending', 'approved', 'rejected'
    - Default to 'draft' for all new items
    - Update all existing content_items to have approval_status = 'draft'

    This migration enables the content approval workflow feature.

    ## Scope
    Read for context: supabase/migrations/001_initial_schema.sql, supabase/migrations/006_ab_experiments.sql
    Create: supabase/migrations/007_approval_workflow.sql
    Modify: (none)

    IMPORTANT: Only touch the files listed above. Other agents are working on other
    files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. Migration file created at supabase/migrations/007_approval_workflow.sql
    2. Column approval_status created as CHECK constraint with values: 'draft', 'pending', 'approved', 'rejected'
    3. Default value is 'draft'
    4. All existing content_items rows are set to approval_status = 'draft'
    5. Migration syntax is valid PostgreSQL/Supabase

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: pipeline-agent: Add approval endpoints (approve / reject)
- description: "pipeline-agent: Add approval endpoints (approve / reject)"
- model: haiku
- prompt: |
    You are the pipeline-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Add two new endpoints to the content router:
    1. POST /api/v1/content/{id}/approve — marks content as approved
    2. POST /api/v1/content/{id}/reject — marks content as rejected

    Both endpoints should:
    - Accept the content ID as path parameter
    - Only work if current approval_status is 'draft' or 'pending'
    - Return the updated content_item
    - Update the content's approval_status to 'approved' or 'rejected'
    - Preserve all other fields unchanged

    Also add a request model `ApprovalRequest` if needed, or reuse existing patterns.

    ## Scope
    Read for context: backend/content/router.py, backend/content/models.py
    Modify: backend/content/router.py, backend/content/models.py
    Create: (none)

    IMPORTANT: Only touch the files listed above. Other agents are working on other
    files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. POST /api/v1/content/{id}/approve endpoint created
    2. POST /api/v1/content/{id}/reject endpoint created
    3. Both endpoints validate that current approval_status is 'draft' or 'pending'
    4. Both endpoints update the approval_status and return updated content_item
    5. Backend requires current user owns the content (via get_current_user)
    6. Code follows existing router patterns (same style as /publish, /edit, /delete endpoints)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: frontend-agent: Add approval buttons and wire approval API calls
- description: "frontend-agent: Add approval buttons and wire approval API calls"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Add approval/rejection workflow UI to the content detail page:

    1. Update `frontend/lib/types.ts` to add `approval_status` field to `ContentItem` interface (enum: 'draft' | 'pending' | 'approved' | 'rejected')
    2. Update `frontend/lib/api.ts` to add two methods to the `content` object:
       - `approve(id: string)` → POST /api/v1/content/{id}/approve
       - `reject(id: string)` → POST /api/v1/content/{id}/reject
    3. Update `frontend/app/content/[id]/page.tsx` to:
       - Add "Approve" button (green) visible when approval_status is 'draft' or 'pending'
       - Add "Reject" button (red) visible when approval_status is 'draft' or 'pending'
       - Update status badge to show approval_status in addition to (or instead of) status
       - Wire click handlers to call approve/reject API methods
       - Show loading state while request is in flight
       - Update item state on success and show toast notification
       - Handle errors gracefully

    Status badge should show both status and approval_status, e.g. "ready · approved" or "ready · pending approval"

    ## Scope
    Read for context: frontend/app/content/[id]/page.tsx, frontend/lib/api.ts, frontend/lib/types.ts
    Modify: frontend/lib/api.ts, frontend/lib/types.ts, frontend/app/content/[id]/page.tsx
    Create: (none)

    IMPORTANT: Only touch the files listed above. Other agents are working on other
    files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. ContentItem type includes approval_status field (typed enum)
    2. content.approve() and content.reject() methods exist in API client
    3. Content detail page shows Approve and Reject buttons when appropriate
    4. Buttons update approval_status on success
    5. Toast notifications appear on success or error
    6. Loading state shown while request is in flight
    7. Buttons styled consistently with existing UI (dark theme, #C9A96E accent)
    8. Buttons hidden when approval_status is already 'approved' or 'rejected'

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

## Status Log
- 2026-04-22 14:30 created, status=awaiting-approval
