# Execution Plan: Add views_count Column to Content Items

**Created:** 2026-04-22  
**Status:** Awaiting Approval  
**Tasks:** 3 across 2 groups  
**Specialists:** db-agent, pipeline-agent, frontend-agent

---

## Group 1 (Parallel - No Dependencies)

### Task 1.1: db-agent — Add views_count column to content_items table

**Complexity:** EASY  
**Files:**
- Create: `supabase/migrations/007_views_count.sql`

**Description:**  
Add a views_count integer column to the content_items table with default value 0. This migration requires no RLS changes and is purely a schema extension.

**Acceptance Criteria:**
1. New migration file created at `supabase/migrations/007_views_count.sql`
2. Migration adds `views_count integer default 0` column to `content_items` table
3. Migration is valid SQL with proper comments
4. No RLS policy changes needed (existing policies still apply)
5. Migration follows the naming pattern of existing migrations (007_*)

**Dependencies:** None

---

## Group 2 (Parallel - Depends on Group 1)

### Task 2.1: pipeline-agent — Add endpoint to increment views_count when content is accessed

**Complexity:** EASY  
**Files:**
- Modify: `backend/content/router.py`, `backend/content/models.py`
- Read: `backend/database.py`

**Description:**  
Create a new POST endpoint `/api/v1/content/{content_id}/view` that increments the views_count column. This endpoint will be called from the frontend whenever a user accesses content.

**Acceptance Criteria:**
1. New Pydantic model created for request (can be empty body or minimal)
2. New POST endpoint `/api/v1/content/{content_id}/view` implemented
3. Endpoint validates user ownership of the content_item before incrementing
4. Endpoint increments `views_count` by 1 on the content_items row
5. Endpoint returns the updated content_item with new `views_count` value
6. Uses Supabase service role to bypass RLS for the write
7. Proper error handling for missing content_item (404) or unauthorized access (403)

**Dependencies:** Task 1.1 (views_count column must exist)

---

### Task 2.2: frontend-agent — Display views_count on library and wire increment endpoint

**Complexity:** MEDIUM  
**Files:**
- Modify: `frontend/lib/types.ts`, `frontend/lib/api.ts`, `frontend/app/content/library/page.tsx`
- Read: Existing component implementations

**Description:**  
Add the views_count field to the ContentItem TypeScript interface, implement the API client method to call the increment endpoint, and update the library page to display and increment the view count on content cards.

**Acceptance Criteria:**
1. `ContentItem` interface in `frontend/lib/types.ts` includes `views_count: number` field
2. `frontend/lib/api.ts` includes new method `content.view(contentId: string)` that calls `POST /api/v1/content/{id}/view`
3. Library page renders `views_count` on each content card with clear visual treatment (e.g., "📊 1,234 views" or similar badge)
4. When a user clicks to view or interact with a content item, the increment endpoint is called
5. View count updates in real-time or on page refresh
6. Styling is consistent with existing content cards (dark theme #0F172A, accent color #C9A96E, borders #334155)
7. Handles loading state if increment call is async

**Dependencies:** Task 1.1 (views_count column must exist), Task 2.1 (endpoint must exist)

---

## Group Order & Dependencies

```
┌─────────────────────────┐
│   Group 1 (Parallel)    │
│                         │
│  db-agent: Add views    │
│  count column           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────────────────────────────┐
│    Group 2 (Parallel - Depends on Group 1)      │
│                                                 │
│  pipeline-agent: Add increment endpoint         │
│  frontend-agent: Display & wire in UI           │
└─────────────────────────────────────────────────┘
```

## Summary

| Aspect | Value |
|--------|-------|
| Total Tasks | 3 |
| Total Groups | 2 |
| Parallel Tasks | 1 in Group 1; 2 in Group 2 |
| Specialists | 3 (db-agent, pipeline-agent, frontend-agent) |
| Schema Changes | 1 (views_count column) |
| Backend Changes | 1 endpoint + 1 model |
| Frontend Changes | 1 type update + 1 API method + 1 UI component |
| Breaking Changes | None |
| Files Created | 1 (migration) |
| Files Modified | 5 |

## Risk Assessment

**Low Risk:**
- Schema change is purely additive (no column deletions or type changes)
- New endpoint is isolated and doesn't affect existing routes
- Frontend changes are scoped to library page; no other pages affected
- No shared file modifications between agents in same group

**Dependencies are Linear:**
- Group 1 must complete before Group 2 (schema must exist before API and UI can reference it)
- No circular dependencies
- Clear phase ordering: DB → Backend → Frontend

---

## Ready for Approval

This plan is ready for review and approval before execution begins. User may:
- Approve as-is
- Request adjustments to task scope, complexity estimates, or file assignments
- Request additions or removals of tasks
- Request changes to the execution order or grouping
