# Feature Plan: Add views_count Column to content_items

## Overview
Add view tracking to content items so the system records how many times each piece of content has been viewed. This involves three integrated layers:
1. **Database**: Add `views_count` column to `content_items` table
2. **Backend**: Increment count when content is accessed
3. **Frontend**: Display view count on library page cards

---

## Database Layer (db-agent)

### Changes
1. **Create migration** `002_add_views_count.sql`
   - Add `views_count BIGINT DEFAULT 0` column to `public.content_items`
   - Add index on `views_count` for efficient sorting (future feature)
   - **Why**: Simple BigInt default tracks views safely; zero-based for new items

2. **RLS Policy**: No change needed
   - Existing `"Users can CRUD own content"` policy on `content_items` covers reads/updates

3. **Apply via Supabase MCP**
   - Use `apply_migration` tool to execute the SQL

### Schema After
```sql
-- In public.content_items table:
views_count bigint default 0,  -- NEW
```

---

## Backend Layer (db-agent + relevant router owner)

### Changes

1. **Update `backend/content/router.py` → GET `/content/{content_id}`**
   - After fetching content, increment `views_count` by 1
   - Single-line update: `sb.table("content_items").update({"views_count": content.views_count + 1}).eq("id", content_id).execute()`
   - **Why**: Simplest point to track — whenever the detail view is accessed, count it

2. **Optional: Also track in GET `/content/library`**
   - Backend already returns list; no increment needed (list view != detailed view)
   - Recommendation: Only increment on single-item access (detail page) to avoid double-counting

3. **No model changes needed**
   - `content/models.py` only defines request/response schemas, not the full item model
   - `views_count` will be returned by the database in all subsequent queries automatically

### Implementation Points
- **Endpoint**: `GET /content/{content_id}` (line 288-291 in router.py)
- **Action**: Add one-line update after read
- **Transaction**: Single atomic update; no rollback risk (view count is non-critical)

---

## Frontend Layer (frontend-agent)

### Changes

1. **Update `frontend/lib/types.ts` → ContentItem interface**
   - Add `views_count: number` field to interface
   - This tells TypeScript that content items have a views_count property

2. **Update `frontend/app/content/library/page.tsx` → Content Card**
   - Add views badge to card bottom-right area (where created_at currently is)
   - Display format: `"1.2K views"` for 1200+, `"42 views"` for under 1000
   - Placement: Next to or above the date in the bottom row
   - Styling: Match existing gray badge style with icon (e.g., Eye icon from lucide)

3. **Update the card structure**
   - Current: `[content_type badge] [date] [chevron]`
   - New: `[content_type badge] [views] [date] [chevron]`
   - Use flexible layout to prevent overflow on mobile

### Implementation Details
- Import `Eye` icon from lucide-react (already imported)
- Create small helper function `formatViewCount(count: number)` to display "1.2K", "42", etc.
- No API changes needed (views_count comes through automatically)
- Library page already fetches full items, so field is available

---

## Verification Checklist

### Database
- [ ] Migration file created and applied
- [ ] `views_count` column exists on `content_items`
- [ ] New content items start with `views_count = 0`
- [ ] Index exists for future optimization

### Backend
- [ ] GET `/content/{content_id}` increments views_count on each access
- [ ] Increment is atomic (no race conditions on concurrent reads)
- [ ] Response includes views_count in returned item

### Frontend
- [ ] TypeScript compiles (views_count added to interface)
- [ ] Library page loads without errors
- [ ] View count displays on each card
- [ ] Mobile layout doesn't break with new badge
- [ ] Format is human-readable (1.2K vs 1200)

---

## Affected Files (Summary)

| Layer | File | Change Type |
|-------|------|-------------|
| DB | `supabase/migrations/002_add_views_count.sql` | CREATE |
| Backend | `backend/content/router.py` | EDIT (1 line in GET /{content_id}) |
| Frontend | `frontend/lib/types.ts` | EDIT (1 field in interface) |
| Frontend | `frontend/app/content/library/page.tsx` | EDIT (icon + badge display) |

---

## Edge Cases & Decisions

1. **Who sees view counts?**
   - Currently: Only the owner (auth.uid() = user_id via RLS)
   - Recommendation: Keep private (don't expose via public API)

2. **Should library list also increment?**
   - **NO** — only detail view (single-item access) increments
   - Rationale: Listing != viewing; prevents artificial inflation

3. **Concurrent view race condition?**
   - **Acceptable risk** — content views are non-critical analytics
   - If strict consistency required, add Postgres CHECK constraint or trigger (future refinement)

4. **Reset views_count ever?**
   - **Not in this feature** — always append-only
   - Could add admin feature later to reset/recalculate

---

## Work Breakdown

### Phase 1: Database (minimal, ~5 min)
- Write migration SQL
- Apply via Supabase MCP

### Phase 2: Backend (minimal, ~5 min)
- Add 1-line update in router.py GET /{content_id}
- Verify response includes new field

### Phase 3: Frontend (moderate, ~15 min)
- Add type to interface
- Add icon + badge to card
- Test mobile responsiveness
- Format number display

**Total estimated effort: ~25 minutes of execution**

---

## Dependencies & Blockers

- **None** — feature is self-contained
- No breaking changes to existing APIs (views_count is additive)
- No new permissions or RLS policies needed
- No changes to business logic (pure analytics)

---

## Success Criteria

1. ✅ Database migration applied successfully
2. ✅ Backend increments views_count on GET /{content_id}
3. ✅ Frontend displays formatted view count on library cards
4. ✅ No TypeScript errors
5. ✅ Mobile layout remains responsive
6. ✅ View count starts at 0 for new items, increments on first access
