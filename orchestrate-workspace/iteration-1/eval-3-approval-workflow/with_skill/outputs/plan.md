# Content Approval Workflow — Orchestration Plan

## Executive Summary

Adding a content approval workflow to the Content Hub requires three focused tasks spanning database schema, backend API, and frontend UI. This plan decomposes the work into specialist subtasks with clear dependencies and file ownership to prevent conflicts.

**Total Tasks:** 3  
**Execution Groups:** 3 (sequential due to dependencies)  
**Timeline:** Estimated 45-60 minutes total  
**Complexity:** Low—mechanical schema change, two new endpoints, two UI buttons

---

## Phase 1: Recon Findings

The scan identified the current state:

### Database
- `supabase/migrations/001_initial_schema.sql` defines the `content_items` table
- Current `status` enum: 'generating', 'scripting', 'rendering', 'ready', 'failed', 'posted'
- No approval or rejection fields exist
- Latest migration: `006_ab_experiments.sql`

### Backend
- `backend/content/router.py` handles all content CRUD and lifecycle operations (generate, edit, publish, delete)
- `backend/content/models.py` defines all request/response models
- No approval endpoints currently
- Follows FastAPI patterns with Depends(get_current_user) for auth
- Returns Supabase rows directly

### Frontend
- `frontend/lib/types.ts` defines `ContentItem` interface (23 fields, no approval_status)
- `frontend/lib/api.ts` wraps all API calls; no approve/reject methods
- `frontend/app/content/[id]/page.tsx` displays content detail with buttons (Publish, Download, Edit, Regenerate, Delete)
- No approval-related UI exists
- Uses Framer Motion for animations and Tailwind for styling (dark theme: #0F172A bg, #C9A96E accent)

---

## Execution Plan

### Group 1: Database Schema (parallel, independent)

**[db-agent | EASY] Create migration: Add approval_status column**
- **Files:**
  - Create: `supabase/migrations/007_approval_workflow.sql`
  - Read: `supabase/migrations/001_initial_schema.sql`, `supabase/migrations/006_ab_experiments.sql`
- **Scope:** Database only; no backend or frontend changes yet
- **What to do:**
  - Create migration file numbered 007 (follows 006_ab_experiments)
  - Add `approval_status` column to `content_items` table
  - Type: text with CHECK constraint allowing 'draft', 'pending', 'approved', 'rejected'
  - Default: 'draft' for all new rows
  - Backfill: Set all existing rows to 'draft'
- **Acceptance Criteria:**
  1. Migration file exists at `supabase/migrations/007_approval_workflow.sql`
  2. Column created with correct enum values
  3. Default value is 'draft'
  4. All existing content items backfilled to 'draft'
  5. SQL syntax is valid

---

### Group 2: Backend API Endpoints (depends on Group 1)

**[pipeline-agent | EASY] Add approve and reject endpoints**
- **Files:**
  - Modify: `backend/content/router.py`, `backend/content/models.py`
  - Read: Existing endpoint patterns (publish, edit, delete endpoints for reference)
- **Scope:** Backend only; no database migrations (Group 1 handles schema) or frontend yet
- **What to do:**
  - Add request model (e.g., `ApprovalRequest` or reuse existing pattern)
  - Create endpoint: `POST /api/v1/content/{id}/approve`
    - Path parameter: content item ID
    - Auth: Requires get_current_user dependency
    - Validation: Only allow approval if current approval_status is 'draft' or 'pending'
    - Action: Update content_items.approval_status to 'approved'
    - Response: Return updated content_item
  - Create endpoint: `POST /api/v1/content/{id}/reject`
    - Same pattern as approve but sets approval_status to 'rejected'
  - Error handling: Return 400 if trying to approve/reject when not eligible
- **Acceptance Criteria:**
  1. Both endpoints exist and follow router naming conventions
  2. Both require user authentication (get_current_user)
  3. Both validate ownership (content.user_id == current_user.id)
  4. Both validate approval_status precondition
  5. Both return updated content_item JSON
  6. Code style matches existing endpoints

---

### Group 3: Frontend UI (depends on Group 2)

**[frontend-agent | MEDIUM] Add approval buttons and wire to API**
- **Files:**
  - Modify: `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/app/content/[id]/page.tsx`
  - Read: Existing button patterns (Publish, Delete), existing API methods for reference
- **Scope:** Frontend UI; no backend or database changes
- **What to do:**
  1. Update `frontend/lib/types.ts`:
     - Add `approval_status: 'draft' | 'pending' | 'approved' | 'rejected'` to ContentItem interface
  2. Update `frontend/lib/api.ts`:
     - Add `approve(id: string)` → POST `/api/v1/content/{id}/approve`
     - Add `reject(id: string)` → POST `/api/v1/content/{id}/reject`
     - Follow same pattern as publish, edit, delete (async, return response data)
  3. Update `frontend/app/content/[id]/page.tsx`:
     - Add state: `const [approving, setApproving] = useState(false)`
     - Add state: `const [rejecting, setRejecing] = useState(false)`
     - Add handler: `handleApprove()` — calls contentApi.approve, updates item.approval_status, shows toast
     - Add handler: `handleReject()` — calls contentApi.reject, updates item.approval_status, shows toast
     - Add "Approve" button (visible when approval_status is 'draft' or 'pending')
       - Styling: green badge style (similar to success states), disabled while approving
       - Placement: In action button row, after Publish
     - Add "Reject" button (visible when approval_status is 'draft' or 'pending')
       - Styling: red badge style, disabled while rejecting
       - Placement: In action button row, after Approve
     - Update STATUS_BADGE to include approval_status display (e.g., "ready · approved")
- **Acceptance Criteria:**
  1. ContentItem type has approval_status field
  2. content.approve() and content.reject() methods exist
  3. Approve/Reject buttons visible when appropriate
  4. Buttons are disabled while request is in flight
  5. Toast notifications on success/error
  6. Item state updates on success
  7. Styling matches dark theme (#0F172A bg, #C9A96E accent)
  8. Buttons hidden when approval_status is 'approved' or 'rejected'

---

## File Dependency Matrix

| File | Agent | Change | Depends On |
|------|-------|--------|-----------|
| `supabase/migrations/007_approval_workflow.sql` | db-agent | Create | None (Group 1) |
| `backend/content/models.py` | pipeline-agent | Modify | Group 1 migration |
| `backend/content/router.py` | pipeline-agent | Modify | Group 1 migration |
| `frontend/lib/types.ts` | frontend-agent | Modify | Group 2 endpoints |
| `frontend/lib/api.ts` | frontend-agent | Modify | Group 2 endpoints |
| `frontend/app/content/[id]/page.tsx` | frontend-agent | Modify | Group 2 endpoints |

**Conflict Prevention:**
- db-agent owns schema only
- pipeline-agent owns backend code; no frontend or schema touches
- frontend-agent owns UI layer; no backend or schema touches
- No two agents modify the same file in the same execution group ✓

---

## Specialist Assignments

1. **db-agent** — Database schema specialist
   - Scope: Supabase migrations
   - Task: Create `007_approval_workflow.sql` migration

2. **pipeline-agent** — Content pipeline specialist
   - Scope: `backend/content/*`
   - Task: Add approval endpoints to router and models

3. **frontend-agent** — Next.js UI specialist
   - Scope: `frontend/app/*`, `frontend/lib/*`
   - Task: Add UI buttons and wire approval API calls

---

## Risk & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Column migration fails (invalid SQL) | Low | High | Have db-agent double-check syntax; test locally if possible |
| Approval status not wired in frontend | Low | High | Clear acceptance criteria for types, API, UI in plan |
| Approval buttons blocked by feature flag | Very Low | Low | No feature flags in use; straightforward conditional rendering |
| API response shape mismatch | Very Low | Medium | Agent reads existing endpoints first; copies pattern |

---

## Success Criteria (Post-Execution)

- [ ] Database migration applied; approval_status column exists on content_items
- [ ] Both approve/reject endpoints respond correctly (200 OK, updated JSON)
- [ ] Frontend buttons appear on content detail page
- [ ] Clicking approve/reject updates UI and shows success toast
- [ ] Edge cases handled (cannot approve already-approved items, etc.)
- [ ] All 6 test scenarios pass manually:
  1. Approve draft content → status becomes 'approved'
  2. Reject draft content → status becomes 'rejected'
  3. Approve already-approved content → error toast
  4. Reject already-rejected content → error toast
  5. Cannot approve/reject if status is 'generating'
  6. Buttons hidden when approval_status is terminal (approved/rejected)

---

## Timeline

| Phase | Duration | Notes |
|-------|----------|-------|
| Recon (Phase 1) | 5 min | Scan codebase, identify patterns |
| Plan (Phase 2) | 10 min | Decompose, write state file ← **YOU ARE HERE** |
| Approve (Phase 3) | - | Waiting for user approval (HALTED FOR EVAL) |
| Execute (Phase 4) | 30 min | Dispatch 3 groups sequentially |
| Verify (Phase 6) | 10 min | Test endpoints, check UI, run manual scenarios |

**Total estimated time:** 45-60 minutes (once approved)

