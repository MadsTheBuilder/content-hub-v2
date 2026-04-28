# Plan: Add Views Count Feature to Content Hub

**Date**: 2026-04-22  
**Task**: Add a `views_count` column to `content_items` table to track content access, increment count on backend access, and display on frontend library page.

---

## Overview

This feature requires changes across three layers:
1. **Database**: Add `views_count` column migration
2. **Backend**: Increment count on content access endpoint(s)
3. **Frontend**: Display count on library page cards and detail page

---

## Phase 1: Database Schema Changes

### 1.1 Create Migration: `007_add_views_count_column.sql`

**File**: `supabase/migrations/007_add_views_count_column.sql`

**Changes**:
- Add `views_count` column to `content_items` table
- Type: `bigint` (to match other count columns like `view_count` in `trending_content`)
- Default value: `0`
- Add index on `views_count` for sorting/filtering queries
- No NOT NULL constraint needed (allows null initially, defaults to 0)

**SQL to add**:
```sql
-- Add views_count column to content_items
ALTER TABLE public.content_items ADD COLUMN views_count bigint DEFAULT 0;

-- Add index for efficient sorting/filtering by views
CREATE INDEX idx_content_items_views ON public.content_items(views_count DESC);
```

**Rationale**: 
- Follows existing pattern (bigint for counts)
- Matches `trending_content.view_count` naming convention from existing schema
- Index enables fast sorting (popular content first)
- Default 0 avoids null handling in application code

---

## Phase 2: Backend API Changes

### 2.1 Update TypeScript Types

**File**: `frontend/lib/types.ts`

**Change**: Add `views_count` field to `ContentItem` interface

**Current**:
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
  rejection_flag: boolean;
  generation_metadata: Record<string, unknown>;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}
```

**Updated**:
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
  rejection_flag: boolean;
  generation_metadata: Record<string, unknown>;
  error_message: string | null;
  views_count: number;  // NEW
  created_at: string;
  updated_at: string;
}
```

**Rationale**: Ensures frontend type safety and matches database schema.

### 2.2 Update Backend Content Router - Increment on Access

**File**: `backend/content/router.py`

**Changes**:

#### 2.2a: Update `get_content()` endpoint (line 287-291)
- **Current**: Reads content by ID
- **Action**: Increment `views_count` in the database before returning

**New logic**:
```python
@router.get("/{content_id}")
async def get_content(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    # Increment views count for this item
    sb.table("content_items").update({"views_count": sb.raw("views_count + 1")}).eq("id", content_id).eq("user_id", str(user.id)).execute()
    # Fetch updated content
    result = sb.table("content_items").select("*").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    return {"item": result.data}
```

**Rationale**: 
- The `/content/{content_id}` endpoint is called when user views the detail page
- Increment happens after auth check and user ownership verification
- Use raw SQL to safely increment (`views_count + 1`)
- Increment before fetch to ensure returned item includes the new count

#### 2.2b: Update `library()` endpoint (line 257-270)
- **Current**: Returns list of content items (no view increment needed)
- **Action**: No changes - viewing the library list doesn't constitute accessing a piece of content
- **Rationale**: Only individual content detail views should increment

### 2.3 Update Backend Content Models (If needed)

**File**: `backend/content/models.py`

**Check**: Verify request/response models don't need views_count field explicitly defined.

**Current state**: 
- Request models (`ContentGenerateRequest`, `ContentEditRequest`, etc.) don't return content data
- Response models use Supabase table data directly
- No changes needed - the `views_count` field will flow through from database

---

## Phase 3: Frontend Display Changes

### 3.1 Update Library Page to Display Views Count

**File**: `frontend/app/content/library/page.tsx`

**Changes**: Add views count display to the content card

**Current card structure** (lines 177-219):
- Top row: status badge + platform badge
- Title (center)
- Bottom row: content_type badge + date + chevron

**New addition**:
Add views count to bottom row, between content_type and date.

**Visual placement**: 
```
[Content Type Badge] | 👁 123 views | [Date] [Chevron]
```

**Implementation**:
1. Keep the bottom row flex layout
2. Add view count display: `<Eye className="w-3 h-3" /> {item.views_count}`
3. Use same text styling as date (`text-gray-500 text-xs`)
4. Icon from lucide-react: `Eye`

**Code to update** (inside card, bottom row, line 208-215):
```typescript
{/* Bottom row: content_type + views_count + date + chevron */}
<div className="flex items-center justify-between pt-3 border-t border-[#334155]/50">
  <span className="text-[10px] font-black uppercase tracking-widest px-2.5 py-1 rounded-full bg-[#0F172A] border border-[#1E293B] text-gray-500 capitalize">
    {item.content_type.replace("_", " ")}
  </span>
  <div className="flex items-center gap-2 text-gray-500 text-xs">
    <div className="flex items-center gap-1">
      <Eye className="w-3 h-3" />
      <span>{item.views_count}</span>
    </div>
    <span>{new Date(item.created_at).toLocaleDateString()}</span>
    <ChevronRight className="w-3.5 h-3.5 group-hover:text-white group-hover:translate-x-0.5 transition-all" />
  </div>
</div>
```

**Icon import**: Add `Eye` to imports at top (line 8):
```typescript
import { Library, PlusCircle, ChevronRight, Search, Eye } from "lucide-react";
```

**Rationale**:
- Views count is useful metadata on library cards
- Eye icon makes the meaning immediately clear
- Consistent with existing design language
- Non-intrusive placement in bottom row

### 3.2 Update Content Detail Page (Optional - for completeness)

**File**: `frontend/app/content/[id]/page.tsx`

**Change**: Display views count somewhere on the detail page header or stats section

**Suggested placement**: Near status badge or in a stats bar

**Note**: Read first to determine exact placement based on existing layout.

---

## Implementation Order

**Order matters** for safe rollout:

1. **Database Migration First** (007_add_views_count_column.sql)
   - Run Supabase migration to add column
   - Verify column exists with default 0

2. **Type Definitions** (frontend/lib/types.ts)
   - Update TypeScript interface
   - No functional changes, enables type checking

3. **Backend Increment Logic** (backend/content/router.py)
   - Update `get_content()` to increment views_count
   - Test: make GET request, verify count increments
   - Verify RLS permissions don't block increment

4. **Frontend Library Display** (frontend/app/content/library/page.tsx)
   - Add Eye icon import
   - Update card UI to display views_count
   - Test: verify count displays correctly from API response

5. **Frontend Detail Page** (frontend/app/content/[id]/page.tsx)
   - Optional: Add views display to detail page header
   - Test: verify views increment when visiting detail

---

## Key Implementation Details

### Database Increment Strategy
- Use Supabase's raw SQL support: `{"views_count": sb.raw("views_count + 1")}`
- Safer than read-modify-write pattern
- Atomic operation at database level
- Prevents race conditions

### RLS Considerations
- Backend uses `service_role_key` which bypasses RLS
- Increment happens server-side after auth check
- No permission issues expected

### Empty State Handling
- Existing content items will have views_count = 0 (default)
- No migration of old data needed
- Gradual accumulation as users view content

### Mock Mode Compatibility
- Mock client returns empty data by default
- views_count will not increment in mock mode
- This is acceptable for development/demo purposes

---

## Testing Strategy

### Unit Tests to Add

1. **Backend Increment Test** (`backend/tests/test_content.py`)
   - Test GET `/content/{id}` increments views_count
   - Test unauthorized user cannot increment others' content
   - Test multiple views accumulate correctly

2. **API Contract Test**
   - Verify ContentItem response includes views_count field
   - Verify type is number, not string

3. **Frontend Component Test**
   - Verify Eye icon renders
   - Verify views_count displays correctly
   - Verify display format (no decimals, clean number)

### Manual Testing

1. Create a workflow and generate content
2. View the library - should show views_count = 0
3. Click to view content detail - views_count should increment
4. Return to library - should show updated count
5. Refresh detail page multiple times - count should continue incrementing
6. Create new content - should have views_count = 0

---

## Files to Change

| File | Type | Purpose |
|------|------|---------|
| `supabase/migrations/007_add_views_count_column.sql` | NEW | Database schema |
| `frontend/lib/types.ts` | EDIT | Type definitions |
| `backend/content/router.py` | EDIT | Increment logic |
| `frontend/app/content/library/page.tsx` | EDIT | UI display |
| `frontend/app/content/[id]/page.tsx` | EDIT (optional) | Detail page display |

---

## Success Criteria

- [ ] Migration runs without errors
- [ ] New `views_count` column exists in database with default 0
- [ ] TypeScript types compile without errors
- [ ] GET `/content/{id}` increments views_count by 1
- [ ] Increment respects RLS (user can only view own content)
- [ ] Library page displays views_count correctly
- [ ] Detail page shows incremented count after viewing
- [ ] Multiple views accumulate (e.g., 3 views = 3, not capped)
- [ ] Empty state (views_count = 0) displays cleanly ("0 views")

---

## Dependencies & Constraints

- **Supabase project** must be set up with migration support
- **Backend** uses service_role key (already configured)
- **Frontend** uses existing API pattern (no new endpoints)
- **Database** uses PostgreSQL (supports raw SQL increment)
- **No breaking changes** to existing APIs or types

---

## Notes for Implementation

1. **Raw SQL in Supabase**: The increment syntax may vary. If `sb.raw("views_count + 1")` doesn't work, use:
   - Check Supabase-py docs for proper increment syntax
   - Alternative: fetch current value, increment in Python, update back (less ideal but safe)

2. **Icon Import**: Eye icon is part of lucide-react (already a dependency)

3. **Backward Compatibility**: Existing content won't have views tracked historically, but will start from 0

4. **Performance**: Single new index on views_count is minimal overhead

---

## Optional Enhancements (Out of Scope)

- Sort library by views (most viewed first)
- Analytics dashboard showing view trends
- Per-platform view breakdown
- Export view statistics
- View history/audit log
- Reset views counter

These can be added later as separate tasks.

---

## Session Notes

**Explored**:
- Database schema (`supabase/migrations/001_initial_schema.sql`)
- Content router endpoints (`backend/content/router.py`)
- Content types (`backend/content/models.py`)
- TypeScript types (`frontend/lib/types.ts`)
- Library page UI (`frontend/app/content/library/page.tsx`)
- Detail page structure (`frontend/app/content/[id]/page.tsx`)
- API client (`frontend/lib/api.ts`)
- Database client (`backend/database.py`)

**Key Findings**:
- Library page already receives full ContentItem objects from API
- Backend uses service_role bypass (simplifies permissions)
- Icon library (lucide-react) already supports Eye icon
- RLS enabled on content_items but bypassed by backend service role key
- No tests exist yet for this feature (new test files needed)
