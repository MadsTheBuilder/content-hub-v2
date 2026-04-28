# Content Approval Workflow Implementation Plan

**Date:** 2026-04-22  
**Scope:** Add approval status field, backend approval endpoint, and frontend approve/reject buttons  
**Priority:** Phase 3 refinement feature  

---

## Overview

Add a content approval workflow to the Content Hub, allowing users to review content items with an explicit approval status (draft → pending → approved/rejected) before publishing. This prevents accidental publishing and enables content review governance.

---

## Success Criteria

1. **Database:** Content items have an `approval_status` field with values: `draft`, `pending`, `approved`, `rejected`
2. **Backend:** New endpoint `PUT /api/v1/content/{id}/approve` accepts `{decision: "approved"|"rejected", notes?: string}`
3. **Frontend:** Content detail page displays approval status and shows approve/reject buttons (visible when status is "ready" or "pending")
4. **State Machine:** Publishing only allowed when `approval_status = "approved"`
5. **Backward Compatibility:** Existing content items default to `approval_status = "draft"` (migration)

---

## Architecture Decisions

- **Field Placement:** `approval_status` in `public.content_items` table alongside existing `status` field
  - `status`: generation pipeline state (generating → scripting → rendering → ready → posted)
  - `approval_status`: governance state (draft → pending → approved/rejected)
- **Separation:** These are orthogonal — you can have `status="ready"` and `approval_status="pending"`
- **Publishing Rule:** `PUT /content/{id}/publish` should check `if approval_status != "approved" then 403 Forbidden`
- **No New Table:** Reuse `content_edit_history` pattern — approval decisions logged in-row via metadata (simple, no joins)

---

## Files to Change

### 1. Database Migration (New)
**File:** `supabase/migrations/007_approval_workflow.sql`

```sql
-- Add approval_status column to content_items
ALTER TABLE public.content_items 
ADD COLUMN approval_status TEXT DEFAULT 'draft' 
CHECK (approval_status IN ('draft', 'pending', 'approved', 'rejected'));

-- Index for filtering by approval status
CREATE INDEX idx_content_items_approval ON public.content_items(workflow_id, approval_status);

-- Add approval_notes column to store reviewer feedback
ALTER TABLE public.content_items 
ADD COLUMN approval_notes TEXT DEFAULT NULL;

-- Create audit log table for approval decisions
CREATE TABLE public.content_approval_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content_item_id UUID NOT NULL REFERENCES public.content_items(id) ON DELETE CASCADE,
    workflow_id UUID NOT NULL REFERENCES public.workflows(id) ON DELETE CASCADE,
    decision TEXT NOT NULL CHECK (decision IN ('approved', 'rejected', 'pending')),
    notes TEXT DEFAULT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

ALTER TABLE public.content_approval_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can CRUD own approval logs" ON public.content_approval_log FOR ALL
    USING (workflow_id IN (SELECT id FROM public.workflows WHERE user_id = auth.uid()));

-- Index for audit trail
CREATE INDEX idx_approval_log_content ON public.content_approval_log(content_item_id, created_at DESC);
CREATE INDEX idx_approval_log_workflow ON public.content_approval_log(workflow_id, created_at DESC);
```

**Status:** Create new file (no existing migration to modify)

### 2. Frontend Types
**File:** `frontend/lib/types.ts`

**Change:** Update `ContentItem` interface to include approval fields:

```typescript
export interface ContentItem {
  // ... existing fields ...
  approval_status: "draft" | "pending" | "approved" | "rejected";
  approval_notes?: string;
}
```

**Lines affected:** Add 2 new properties to the existing `ContentItem` interface

### 3. Backend Pydantic Model
**File:** `backend/content/models.py`

**Changes:** Add new request/response models:

```python
class ApproveContentRequest(BaseModel):
    decision: str  # "approved" or "rejected"
    notes: str = ""

class ApprovalResponse(BaseModel):
    content_id: str
    approval_status: str
    notes: str | None
    timestamp: str
```

**Lines affected:** Add 2 new model classes (≈10 lines)

### 4. Backend Content Router
**File:** `backend/content/router.py`

**New Endpoint:** Add after existing endpoints:

```python
@router.put("/{content_id}/approve")
async def approve_content(
    content_id: str, 
    req: ApproveContentRequest, 
    user=Depends(get_current_user)
):
    """Approve or reject a content item. Only callable when status='ready'."""
    # Validate: user owns content
    # Validate: status == 'ready'
    # Validate: decision in ['approved', 'rejected']
    # Update approval_status
    # Log decision in content_approval_log
    # Return updated approval status + notes
```

**Lines affected:** Add 1 new endpoint (≈20 lines)

**Modified Endpoint:** Update `publish` endpoint to enforce approval check:

```python
@router.put("/{content_id}/publish")
async def publish(content_id: str, user=Depends(get_current_user)):
    # Existing code...
    # NEW: Check if approval_status == 'approved', else raise HTTPException 403
    if item["approval_status"] != "approved":
        raise HTTPException(status_code=403, detail="Content must be approved before publishing")
    # ... rest of existing publish logic
```

**Lines affected:** Modify existing endpoint (≈3 lines added for check)

### 5. Frontend Content Detail Page
**File:** `frontend/app/content/[id]/page.tsx`

**Changes:**

1. **Display approval status** — Add a second badge showing approval_status (similar to status badge)
2. **Approve/Reject buttons** — Show only when `status === "ready"` (before Publish button)
3. **Approval notes display** — Show approval_notes if rejection reason provided
4. **API calls** — Add new `content.approve(id, decision, notes)` method to `frontend/lib/api.ts`

**Lines affected:**
- ~30 lines for new badge and buttons (JSX)
- ~15 lines for approval decision handler
- ~10 lines in `api.ts` for new method

### 6. Frontend API Client
**File:** `frontend/lib/api.ts`

**New Methods:** Add to `content` object:

```typescript
approve: (id: string, decision: "approved" | "rejected", notes: string = "") =>
    fetchAPI(`/content/${id}/approve`, { 
      method: "PUT", 
      body: JSON.stringify({ decision, notes }) 
    }),
```

**Lines affected:** Add 1 method (≈3 lines)

### 7. Frontend Content Library Page (Optional, but Recommended)
**File:** `frontend/app/content/library/page.tsx`

**Enhancement:** Add filtering by `approval_status` to help users see pending approvals. This is **optional** but improves UX.

**Lines affected:** ~10 lines for filter toggle

---

## Implementation Order

1. **Database Migration** (1st)
   - Run migration to add `approval_status`, `approval_notes`, and audit table
   - Existing content defaults to `draft`

2. **Backend Models** (2nd)
   - Add `ApproveContentRequest` and `ApprovalResponse` models

3. **Backend Router** (3rd)
   - Add new `/approve` endpoint
   - Modify `/publish` to enforce approval check

4. **Frontend Types** (4th)
   - Update `ContentItem` interface with new fields

5. **Frontend API Client** (5th)
   - Add `approve()` method

6. **Frontend Content Detail Page** (6th)
   - Add approval status badge
   - Add approve/reject buttons and handlers
   - Add approval notes display

7. **Frontend Content Library** (7th, Optional)
   - Add approval status filter if desired

---

## Testing Strategy

### Backend Tests
- `test_approve_content_success`: POST approval, verify status updated in DB
- `test_approve_unauthorized`: Different user cannot approve others' content
- `test_publish_without_approval`: Publishing without approval → 403 error
- `test_publish_with_approval`: Publishing after approval → succeeds

### Frontend Tests
- Approve/reject buttons visible only when `status === "ready"`
- Clicking approve shows confirmation, updates UI
- Rejection with notes persists notes
- Publishing disabled if not approved

### Manual E2E
1. Generate content → status: ready, approval_status: draft
2. Click "Approve" → approval_status: approved
3. Click "Publish" → succeeds
4. Retry flow: Generate → Reject with notes → status: ready, approval_status: rejected
5. Verify notes shown in detail page

---

## Risk Mitigation

1. **Backward Compatibility:** Default `approval_status = 'draft'` allows existing workflows to continue
2. **Approval Bypass:** Publish endpoint enforces check — cannot be circumvented via API
3. **Audit Trail:** All decisions logged to `content_approval_log` for transparency
4. **UI Clarity:** Status badges and buttons clearly indicate what's required before publishing

---

## Known Constraints

- **Single User MVP:** No role-based approval (e.g., manager approving content creator's work). All approval logic applies to the content owner.
- **No Notifications:** No approval reminders or notifications — Phase 3 scope limited.
- **No Bulk Approval:** Cannot approve multiple items at once — single-item endpoint only.

---

## Summary of Changes by File

| File | Type | Change | LOC |
|------|------|--------|-----|
| `supabase/migrations/007_approval_workflow.sql` | New | DB schema + audit table | ~40 |
| `frontend/lib/types.ts` | Modify | Add 2 fields to ContentItem | +2 |
| `backend/content/models.py` | Modify | Add 2 Pydantic models | +10 |
| `backend/content/router.py` | Modify | Add 1 endpoint, modify 1 endpoint | +25 |
| `frontend/lib/api.ts` | Modify | Add 1 method | +3 |
| `frontend/app/content/[id]/page.tsx` | Modify | UI: badges, buttons, handlers | +55 |
| `frontend/app/content/library/page.tsx` | Modify (optional) | Filter by approval_status | ~10 |

**Total LOC:** ~145 lines of changes across 7 files

---

## Glossary

- **approval_status**: Governance state of a content item (draft/pending/approved/rejected)
- **status**: Generation pipeline state (generating/scripting/rendering/ready/failed/posted)
- **Orthogonal Fields**: These two state machines are independent — a content can be "ready" (generation done) and "rejected" (approval failed) simultaneously
- **Audit Log**: Permanent record of all approval decisions for compliance/transparency

