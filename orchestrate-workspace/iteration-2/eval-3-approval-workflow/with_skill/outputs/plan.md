# Execution Plan: Content Approval Workflow

**Tasks:** 3 across 3 groups  
**Specialists:** db-agent, pipeline-agent, frontend-agent

## Overview

This orchestration implements a content approval workflow that allows users to approve or reject content items before publishing. The feature spans database schema, backend API endpoints, and frontend UI.

## Execution Plan

### Group 1 (parallel — Database Migration)
- **[db-agent | EASY]** Add approval_status column to content_items table
  - **Files:** `supabase/migrations/007_approval_workflow.sql` (new)
  - **Acceptance Criteria:**
    1. Migration file created at `supabase/migrations/007_approval_workflow.sql`
    2. Column `approval_status` created with CHECK constraint for values: 'draft', 'pending', 'approved', 'rejected'
    3. Default value is 'draft'
    4. All existing content_items rows set to approval_status = 'draft'
    5. Migration syntax is valid PostgreSQL/Supabase

### Group 2 (depends on Group 1 — Backend API Endpoints)
- **[pipeline-agent | EASY]** Add approval endpoints (approve / reject)
  - **Files:** `backend/content/models.py` (modify), `backend/content/router.py` (modify)
  - **Acceptance Criteria:**
    1. POST `/api/v1/content/{id}/approve` endpoint created
    2. POST `/api/v1/content/{id}/reject` endpoint created
    3. Both endpoints validate that current approval_status is 'draft' or 'pending'
    4. Both endpoints update the approval_status and return updated content_item
    5. Backend requires current user owns the content (via get_current_user)
    6. Code follows existing router patterns (same style as /publish, /edit, /delete endpoints)

### Group 3 (depends on Group 2 — Frontend UI and API Integration)
- **[frontend-agent | MEDIUM]** Add approval buttons and wire approval API calls
  - **Files:** `frontend/lib/types.ts` (modify), `frontend/lib/api.ts` (modify), `frontend/app/content/[id]/page.tsx` (modify)
  - **Acceptance Criteria:**
    1. ContentItem type includes approval_status field (typed enum: 'draft' | 'pending' | 'approved' | 'rejected')
    2. `content.approve(id: string)` and `content.reject(id: string)` methods exist in API client
    3. Content detail page shows Approve and Reject buttons when appropriate
    4. Buttons update approval_status on success
    5. Toast notifications appear on success or error
    6. Loading state shown while request is in flight
    7. Buttons styled consistently with existing UI (dark theme, #C9A96E accent)
    8. Buttons hidden when approval_status is already 'approved' or 'rejected'

## Technical Notes

- **Database Migration:** Use standard Supabase migration naming and PostgreSQL syntax. See `supabase/migrations/006_ab_experiments.sql` for reference pattern.
- **Backend Validation:** Both endpoints should only allow status transitions from 'draft' or 'pending' to 'approved' or 'rejected'. Reject other states.
- **Frontend State Management:** Update local item state on success to immediately reflect approval_status change. Reuse existing polling pattern if regenerating.
- **UI Consistency:** Follow existing color scheme: dark background (#0F172A), accent (#C9A96E), borders (#334155). Use existing badge styling.

## Specialist Definitions

The following specialists will be involved:

- **db-agent:** Database schema and migrations specialist (Supabase)
- **pipeline-agent:** Content generation API specialist (FastAPI backend)
- **frontend-agent:** Next.js UI specialist (React, TypeScript, API client)

## Phase Gate

**This plan is awaiting user approval before execution begins.** 

User should review:
1. Are the 3 groups in the right order (sequential dependencies)?
2. Are the file assignments correct and non-conflicting?
3. Does the scope make sense for each specialist?
4. Are the acceptance criteria clear and testable?
