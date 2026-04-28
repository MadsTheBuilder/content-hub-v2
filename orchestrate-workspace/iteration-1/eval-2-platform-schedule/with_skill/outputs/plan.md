# Execution Plan: Platform-Specific Posting Time Recommendations

## Summary

**Objective**: Implement platform-specific posting time recommendations for Content Hub by:
1. Storing preferred posting hours per platform in brand config
2. Computing optimal hours via intelligence layer from historical performance data
3. Displaying recommendations on the content calendar page

**Scope**: 5 files modified, 1 file created, 1 migration created  
**Tasks**: 5 across 4 execution groups  
**Specialists**: 4 agents (db-agent, brand-agent, intelligence-agent, frontend-agent)  
**Complexity**: 2 EASY tasks, 2 MEDIUM tasks, 1 EASY migration task

---

## Execution Plan Detail

### Group 1: Database Schema (Parallel)

**Dependency**: None (Phase 1)

#### Task 1.1: [db-agent | EASY] Create Supabase migration for preferred_post_hours

**Purpose**: Add JSONB column to brand_configs table for storing platform-specific optimal posting hours.

**Files to Create**:
- `supabase/migrations/007_preferred_post_hours.sql`

**Acceptance Criteria**:
1. Migration file created with valid SQL syntax
2. ALTER TABLE command adds column: `preferred_post_hours jsonb default '{}'::jsonb`
3. Includes explanatory comment
4. File follows existing migration style
5. SQL is idempotent and properly formatted

**Expected Outcome**: Schema updated with new field ready for model/API usage.

---

### Group 2: Backend Layer (Depends on Group 1)

**Dependency**: Group 1 (schema migration applied)

#### Task 2.1: [brand-agent | EASY] Add preferred_post_hours to BrandUpdate model

**Purpose**: Extend Pydantic model to accept preferred_post_hours field in API requests.

**Files to Modify**:
- `backend/brand/models.py`

**Files to Read**:
- `backend/brand/router.py` (to verify PUT endpoint usage)

**Acceptance Criteria**:
1. BrandUpdate model includes new field: `preferred_post_hours: Optional[dict[str, list[int]]] = None`
2. Field is optional (backward compatible)
3. Type annotation: dict[str, list[int]] where string is platform, list[int] is hours (0-23)
4. File imports/exports correctly with no syntax errors
5. No changes needed to router.py (it already handles arbitrary fields)

**Expected Outcome**: Brand config API can now receive and validate preferred_post_hours updates.

#### Task 2.2: [intelligence-agent | MEDIUM] Create compute_optimal_posting_hours function

**Purpose**: Build computation engine that analyzes historical publication data to recommend optimal posting times.

**Files to Create**:
- `backend/intelligence/posting_times.py`

**Files to Read**:
- `backend/database.py` (for Supabase client pattern)
- `backend/intelligence/memory.py` (for query patterns)
- `supabase/migrations/001_initial_schema.sql` (table schemas)

**Acceptance Criteria**:
1. Module created at `backend/intelligence/posting_times.py`
2. Async function: `async def compute_optimal_posting_hours(workflow_id: str) -> dict[str, list[int]]`
3. Queries content_items table for published content (status='posted')
4. Groups by platform, extracts hour from created_at/updated_at timestamps
5. Returns dict mapping platform → sorted list of top 2-3 hours by frequency
6. Falls back to platform defaults if insufficient published data
7. Platform defaults:
   - LinkedIn: [9, 10, 11, 12, 17, 18]
   - Twitter: [14, 15, 19]
   - Instagram: [19, 20, 21]
   - TikTok: [20, 21, 22]
   - Facebook: [13, 14, 19, 20]
   - YouTube: [10, 14, 18]
8. No database writes (read-only)
9. Graceful error handling (returns {} on failure)
10. Includes docstring explaining logic
11. No syntax errors, imports correctly

**Expected Outcome**: Intelligence layer can compute platform-specific posting recommendations on-demand.

---

### Group 3: Frontend Types (Depends on Group 2)

**Dependency**: Group 2 (model definition finalized)

#### Task 3.1: [frontend-agent | EASY] Update BrandConfig TypeScript interface

**Purpose**: Extend frontend types to include preferred_post_hours field.

**Files to Modify**:
- `frontend/lib/types.ts`

**Acceptance Criteria**:
1. BrandConfig interface includes: `preferred_post_hours?: Record<string, number[]>`
2. Field is optional (? suffix) for backward compatibility
3. Type is Record<string, number[]> (platform name → array of hours)
4. File exports correctly with no TypeScript errors
5. Existing fields unchanged
6. No breaking changes to other types

**Expected Outcome**: Frontend components can type-safely access preferred_post_hours from brand config.

---

### Group 4: Calendar UI Integration (Depends on Group 3)

**Dependency**: Group 3 (types updated)

#### Task 4.1: [frontend-agent | MEDIUM] Display posting time recommendations on calendar

**Purpose**: Surface recommended posting hours alongside calendar items, helping users understand optimal publication windows.

**Files to Modify**:
- `frontend/app/content/calendar/page.tsx`

**Files to Read**:
- `frontend/lib/api.ts` (to verify brand.get usage)
- `frontend/lib/types.ts` (to understand BrandConfig structure)

**Acceptance Criteria**:
1. Calendar page fetches workflow_id from URL/context/props
2. On mount, fetches brand config using `brand.get(workflow_id)`
3. Extracts preferred_post_hours from response
4. For each content item displayed, checks if item.platform exists in preferred_post_hours
5. If match found, displays recommendation UI (badge or tooltip) e.g., "Optimal: 9–17"
6. If no recommendation exists for platform, no recommendation shown (clean, not cluttered)
7. Handles loading state gracefully (doesn't block calendar while brand config loads)
8. Handles errors gracefully (if brand.get fails, calendar still renders)
9. UI styling consistent with dark theme (bg-[#0F172A], accent-[#C9A96E], borders-[#334155])
10. Framer Motion animations preserved (no nested motion divs causing deadlock)
11. No breaking changes to existing calendar layout, grouping, or sorting
12. Recommendation appears as secondary info (not overwhelming existing badges)

**Recommendation UI Placement Options**:
- As an additional small badge in the existing badge row (next to platform/content_type/status)
- As a tooltip on hover over the platform badge
- As subtle text below the item title
- Recommendation: badge approach for consistency with existing design

**Expected Outcome**: Users see posting time recommendations on calendar, enabling better scheduling decisions.

---

## Task Dependencies Graph

```
Group 1: Schema
    ↓
Group 2: Backend (Brand Model + Intelligence Computation)
    ├─ Task 2.1 (Brand Model) ──→ 
    └─ Task 2.2 (Intelligence)
        ↓
Group 3: Frontend Types
    ↓
Group 4: Calendar UI
```

All tasks within a group can execute in parallel. Groups must be completed sequentially due to dependencies.

---

## Risk Assessment

### Low Risk
- **Task 1.1 (Migration)**: Simple schema addition, standard Supabase pattern
- **Task 2.1 (Brand Model)**: Straightforward Pydantic field addition
- **Task 3.1 (Types)**: TypeScript interface extension, no logic

### Medium Risk
- **Task 2.2 (Computation)**: Requires understanding Supabase query API + hour extraction logic. Fallback to platform defaults mitigates data scarcity risk.
- **Task 4.1 (Calendar UI)**: Requires fetching additional data (brand config) on calendar page. Risk: async loading complexity. Mitigation: error handling + graceful degradation.

### No Breaking Changes
- All new fields are optional (backward compatible)
- Existing APIs unchanged (brand router already generic)
- Calendar page layout preserved (recommendations are additive)

---

## File Manifest

### Files to Create
1. `supabase/migrations/007_preferred_post_hours.sql`
2. `backend/intelligence/posting_times.py`

### Files to Modify
1. `backend/brand/models.py` (add field)
2. `frontend/lib/types.ts` (add field)
3. `frontend/app/content/calendar/page.tsx` (add recommendation display)

### Files to Read (no changes)
1. `backend/brand/router.py`
2. `backend/database.py`
3. `backend/intelligence/memory.py`
4. `frontend/lib/api.ts`
5. `supabase/migrations/001_initial_schema.sql`
6. `supabase/migrations/005_phase3_brand_fields.sql`

---

## Success Criteria (Phase 6 Verification)

After all tasks complete:

1. **Schema**: New column exists in brand_configs with correct type and default
2. **Backend**: 
   - BrandUpdate model accepts preferred_post_hours without errors
   - compute_optimal_posting_hours function callable and returns correct shape
   - No syntax errors or import failures
3. **Frontend**:
   - BrandConfig interface includes preferred_post_hours field
   - Calendar page displays recommendations without breaking
   - No TypeScript compilation errors
4. **Integration**:
   - Calendar can fetch brand config and display recommendations
   - Graceful handling of missing/invalid data
   - No regression in existing calendar functionality

---

## Notes

- **Historical Data Strategy**: compute_optimal_posting_hours reads from published content (content_items table with status='posted'). If insufficient data, falls back to platform industry-standard defaults.
- **Extensibility**: compute_optimal_posting_hours is read-only and on-demand — can be called whenever recommendations are needed without modifying brand config. Future: could be scheduled to auto-update recommendations.
- **UI Subtlety**: Recommendation badges kept subtle to avoid overwhelming existing calendar design. They are secondary info supporting user decision-making.
- **Backend API**: No new API endpoints needed — brand.get() already returns preferred_post_hours once model is updated.
