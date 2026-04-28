# Execution Plan: Add views_count Column to content_items

**Tasks:** 3 across 3 groups
**Specialists:** db-agent, pipeline-agent, frontend-agent

## Execution Plan

### Group 1 (parallel)
- [db-agent | EASY] Create migration for views_count column
  Files: supabase/migrations/007_views_count.sql
  Criteria: Migration file created with ALTER TABLE to add views_count bigint column, default 0, with index on (content_item_id, views_count) for library queries

### Group 2 (depends on Group 1)
- [pipeline-agent | MEDIUM] Wire views_count increment into content retrieval endpoints
  Files: backend/content/router.py, backend/content/models.py
  Criteria: GET /content/{id} endpoint increments views_count in DB, /content/library endpoint returns views_count in response

### Group 3 (depends on Group 2)
- [frontend-agent | MEDIUM] Display views_count on library cards
  Files: frontend/lib/types.ts, frontend/app/content/library/page.tsx
  Criteria: ContentItem type includes views_count field, library page renders view count badge on each card

## Recon Summary

### Database Schema
- `content_items` table (supabase/migrations/001_initial_schema.sql) currently has 15 columns
- **No views_count column exists** — needs to be added
- Existing pattern: `trending_content` table already tracks `view_count bigint`
- RLS policy scoped to user_id — service role key bypasses for writes

### Backend API Structure
- Content endpoints in `backend/content/router.py`
- `/content/{id}` — GET endpoint for retrieving single content item
- `/content/library` — GET endpoint for listing filtered content items
- Currently returns content without view tracking
- ContentItem model in `backend/content/models.py` — needs views_count field

### Frontend Architecture
- Library page: `frontend/app/content/library/page.tsx`
- Content cards display: status badge, platform badge, title, content_type, created_at
- API calls: `content.library()` and `content.get()` from `frontend/lib/api.ts`
- ContentItem type in `frontend/lib/types.ts` — **does not include views_count**

## Task Dependencies

1. **Schema migration must complete first** — database column must exist before backend can write to it
2. **Backend endpoints must be wired before frontend displays** — frontend needs the views_count field in API responses
3. **No file conflicts** — each specialist owns distinct files:
   - db-agent: supabase/migrations/007_views_count.sql (new file)
   - pipeline-agent: backend/content/router.py, backend/content/models.py
   - frontend-agent: frontend/lib/types.ts, frontend/app/content/library/page.tsx

## Success Criteria (Phase 6 Verification)

After all groups complete:
1. Migration file exists and follows Supabase conventions
2. Backend models and endpoints handle views_count correctly
3. Views are incremented atomically (single SQL UPDATE)
4. Frontend displays views_count on library cards with consistent styling
5. No scope violations (each agent only modified assigned files)
6. Frontend types match backend API response shape
