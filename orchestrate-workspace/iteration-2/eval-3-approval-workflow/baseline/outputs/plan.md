# Content Approval Workflow — Implementation Plan

## Overview
Add approval workflow to Content Hub. Users can save content as draft, transition to pending approval, then approve/reject with optional rejection notes.

## Current State Analysis

### Content Item Schema (content_items table)
- **Status Field**: Already exists, enum (generating, scripting, rendering, ready, failed, posted)
  - Tracks generation pipeline state, not approval state
  - Cannot be reused for approval workflow
- **Rejection Flag**: Boolean field exists but unused
  - Too coarse-grained for multi-state approval workflow
- **Generated Fields**: generation_metadata (JSONB), error_message (text)

### Publish Flow
- Current: `/content/{content_id}/publish` endpoint directly sets status="posted"
- No approval gate exists
- No rejection tracking

### User Model
- Single-user MVP (auth hardening in Phase 3)
- Service role key used for backend writes (bypasses RLS)
- No distinction between content creator and approver (same user)

## Design Decisions

### 1. New Column: approval_status
Add to `content_items` table:
```sql
approval_status text not null default 'draft' 
  check (approval_status in ('draft', 'pending', 'approved', 'rejected'))
```

**Rationale:**
- Separate from status (which tracks pipeline state)
- Independent state machine: draft → pending → {approved OR rejected}
- Simple enum suitable for single-user MVP
- Allows content to be "ready" (generated) but not yet "approved"

### 2. New Column: approval_notes (optional)
Add to `content_items` table:
```sql
approval_notes text default null
```
- Stores rejection reason or approval context
- nullable; only populated on reject

### 3. Backend Endpoints

#### Endpoint 1: POST /content/{content_id}/approve
- **Purpose**: Approve a content item (pending → approved)
- **Auth**: JWT required (Depends(get_current_user))
- **Request Body**: Optional ApprovalRequest with approval_notes field
- **Response**: {"approved": true, "approval_status": "approved"}
- **Side Effects**: None (publish is separate step)
- **Validations**: 
  - Content must exist and belong to user
  - approval_status must be "pending" (idempotent: already approved is no-op)

#### Endpoint 2: POST /content/{content_id}/reject
- **Purpose**: Reject a content item with optional notes (pending/approved → rejected)
- **Auth**: JWT required
- **Request Body**: RejectRequest with required rejection_notes field
- **Response**: {"rejected": true, "approval_status": "rejected", "approval_notes": <notes>}
- **Side Effects**: None
- **Validations**:
  - Content must exist and belong to user
  - rejection_notes required (non-empty string)
  - approval_status must be "pending" or "approved"

#### Endpoint 3: POST /content/{content_id}/mark-pending (optional helper)
- **Purpose**: Mark content as pending approval (draft → pending)
- **Use case**: User explicitly requests approval review
- **Request/Response**: Simple state transition
- **Note**: May be unnecessary if "pending" is set automatically on generation

### 4. Workflow State Transitions

```
draft (initial)
  ↓
pending (user clicks "Request Approval" OR automatic on generation)
  ├→ approved (user clicks "Approve")
  │   └→ can then publish (separate action)
  │
  └→ rejected (user clicks "Reject", must include notes)
     └→ can edit and re-request approval
```

### 5. UI Changes (Content Detail Page)

#### Status Display
- Rename badge to show both generation status AND approval status
- Layout: "generation-status | approval-status"
- Example: "ready | pending" or "ready | approved" or "ready | rejected"

#### Action Buttons (conditional rendering)
All buttons disabled while status is "generating" / "scripting" / "rendering":

1. **Approve Button**
   - Show only if: approval_status == "pending"
   - Color: Green
   - onClick: POST /content/{content_id}/approve
   - Loading state while pending

2. **Reject Button**
   - Show only if: approval_status in ("pending", "approved")
   - Color: Red
   - onClick: Opens modal/prompt for rejection_notes
   - POST /content/{content_id}/reject with notes
   - Loading state while pending

3. **Request Approval Button** (optional)
   - Show only if: approval_status == "draft"
   - Color: Blue
   - Transitions draft → pending
   - May be auto-triggered on generation instead

4. **Publish Button**
   - Existing behavior
   - May add guard: only show if approval_status == "approved" (design decision TBD)
   - Could allow publishing from any state (no gate)

#### Approval Notes Display
- Show rejection_notes in red banner if approval_status == "rejected"
- Help user understand why content was rejected

### 6. Frontend Type Updates

**Update ContentItem interface in types.ts:**
```typescript
export interface ContentItem {
  id: string;
  workflow_id: string;
  user_id: string;
  content_type: "slides" | "topic" | "short_form" | "talking_head";
  platform: string;
  title: string;
  script_text: string;
  published_script: string | null;
  storyboard: Record<string, unknown> | null;
  asset_urls: string[];
  status: "generating" | "scripting" | "refining" | "rendering" | "ready" | "failed" | "posted";
  approval_status: "draft" | "pending" | "approved" | "rejected";  // NEW
  approval_notes: string | null;  // NEW
  rejection_flag: boolean;
  generation_metadata: Record<string, unknown>;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}
```

**Add Pydantic models in backend/content/models.py:**
```python
class ApprovalRequest(BaseModel):
    approval_notes: Optional[str] = None

class RejectRequest(BaseModel):
    rejection_notes: str  # required
```

### 7. API Client Updates (frontend/lib/api.ts)

Add methods to content object:
```typescript
approve: (id: string, notes?: string) =>
  fetchAPI(`/content/${id}/approve`, { 
    method: "POST", 
    body: JSON.stringify({ approval_notes: notes }) 
  }),

reject: (id: string, notes: string) =>
  fetchAPI(`/content/${id}/reject`, { 
    method: "POST", 
    body: JSON.stringify({ rejection_notes: notes }) 
  }),
```

## Implementation Sequence

### Phase 1: Database (db-agent)
1. Create migration file: `supabase/migrations/007_content_approval.sql`
2. Add approval_status column with default 'draft' and check constraint
3. Add approval_notes column (nullable)
4. Create indexes on (workflow_id, approval_status) for list filtering
5. Update existing content_items to approval_status='draft' (data migration)

### Phase 2: Backend API (pipeline-agent or core team)
1. Update `backend/content/models.py` — add ApprovalRequest, RejectRequest
2. Update `backend/content/router.py`:
   - Add POST /content/{content_id}/approve endpoint
   - Add POST /content/{content_id}/reject endpoint
   - Optional: Add POST /content/{content_id}/mark-pending endpoint
   - Add validation: user owns content, state is valid
3. Test with curl/Postman before frontend integration

### Phase 3: Frontend Types (frontend-agent)
1. Update `frontend/lib/types.ts` — add approval_status, approval_notes to ContentItem
2. Update `frontend/lib/api.ts` — add approve() and reject() methods

### Phase 4: Frontend UI (frontend-agent)
1. Update `frontend/app/content/[id]/page.tsx`:
   - Modify status badge to show approval_status alongside status
   - Add approve button (green, conditional)
   - Add reject button (red, conditional) with modal for notes
   - Add rejection_notes banner if rejected
   - Wire button handlers to new API methods
   - Add loading/error states
2. Optional: Update `frontend/app/content/library/page.tsx` to show approval_status in list view

## Design Decisions Still Open

1. **Publish Gate**: Should publish endpoint require approval_status=="approved"?
   - Option A: Yes (enforce approval before publishing)
   - Option B: No (publish allowed from any state)
   - Current assumption: Option B (user can bypass approval in MVP)

2. **Auto-pending**: Should content auto-transition to "pending" when generation completes?
   - Option A: Yes (ready content immediately requests approval)
   - Option B: No (user explicitly clicks "Request Approval" button)
   - Current assumption: Option B (manual control)

3. **Rejection Behavior**: When rejected, can user:
   - Edit and re-request approval? (assume yes)
   - Regenerate? (assume yes)
   - Publish anyway? (assume yes, no gate)

4. **Single-User Assumption**: 
   - Current design assumes single approver (same user who created)
   - No "assigned reviewer" or queue concept
   - Sufficient for MVP but would need redesign for multi-user

## Files Modified

| File | Changes | Owner |
|------|---------|-------|
| `supabase/migrations/007_content_approval.sql` | NEW — Add columns + constraints | db-agent |
| `backend/content/models.py` | Add ApprovalRequest, RejectRequest | pipeline-agent |
| `backend/content/router.py` | Add approve, reject endpoints | pipeline-agent |
| `frontend/lib/types.ts` | Add approval_status, approval_notes to ContentItem | frontend-agent |
| `frontend/lib/api.ts` | Add approve(), reject() methods | frontend-agent |
| `frontend/app/content/[id]/page.tsx` | Add buttons, conditionals, badge updates | frontend-agent |
| `frontend/app/content/library/page.tsx` | Optional: show approval_status in list | frontend-agent |

## Testing Strategy

### Database
- Verify column creation and default values with direct query
- Verify check constraint rejects invalid values

### Backend
- POST /content/{content_id}/approve with valid/invalid states
- POST /content/{content_id}/reject with/without notes
- Verify state transitions are idempotent where appropriate
- Verify auth: user can only approve own content

### Frontend
- Render detail page with different approval_status values
- Verify buttons show/hide based on approval_status
- Click approve → verify POST call and state update
- Click reject → modal appears, POST on submit
- Rejection notes display when status is "rejected"

## Assumptions & Risks

### Assumptions
1. Single-user MVP (no multi-user approval queue needed)
2. User can approve their own content (no supervisor role)
3. Approval is advisory/recordkeeping, not a publish gate
4. No audit trail needed (approval_status changes not logged)

### Risks
1. **Breaking Change**: Adding NOT NULL column requires data migration
   - Mitigation: Set default 'draft' in migration
2. **No Audit Trail**: Can't see who approved or when
   - Mitigation: Could add approval_timestamp, approved_by fields later
3. **No Notification**: No alert when content is rejected
   - Mitigation: Could add to learning loop or scheduler later
4. **No Rollback Path**: No easy way to revert "approved" → "draft" if needed
   - Mitigation: Add endpoint if needed

## Success Criteria

- Approval workflow UI renders with correct buttons for each approval_status
- Approve endpoint updates approval_status to "approved"
- Reject endpoint requires notes and updates both approval_status and approval_notes
- Buttons are disabled during generation/rendering pipeline
- Frontend displays rejection notes prominently when status=="rejected"
- All existing functionality continues to work (backward compatibility)

## Estimated Effort

- Database: ~30 min (migration + testing)
- Backend: ~45 min (2 endpoints + models + validation)
- Frontend: ~1.5 hours (types, api, component updates, conditional rendering)
- **Total: ~2.5–3 hours** (including testing, debugging, refinement)
