---
slug: platform-posting-schedule
created: 2026-04-22
status: abandoned
current_group: null
groups_complete: []
specialists_involved: [db-agent, brand-agent, intelligence-agent, frontend-agent]
---

# Orchestration: Platform-Specific Posting Time Recommendations

## Recon Summary

The task requires a three-layer implementation:

1. **Brand Config Storage**: Add `preferred_post_hours` field (JSONB) to store per-platform optimal posting times, e.g., `{ "LinkedIn": [9, 17], "Twitter": [14, 19] }`

2. **Intelligence Computation**: Build a function in the intelligence layer that analyzes historical publication data to compute optimal posting hours per platform using engagement metrics from published content.

3. **Calendar UI Display**: Surface posting time recommendations on the content calendar page alongside content items, and allow users to view/edit preferred hours.

### Relevant Files Identified
- **Brand config schema**: `supabase/migrations/005_phase3_brand_fields.sql` (extend)
- **Brand Pydantic model**: `backend/brand/models.py` (add preferred_post_hours field)
- **Brand API**: `backend/brand/router.py` (already handles GET/PUT, no changes needed if schema-compatible)
- **Intelligence layer**: `backend/intelligence/memory.py` + `backend/intelligence/suggestions.py` (new function)
- **Frontend types**: `frontend/lib/types.ts` (add preferred_post_hours to BrandConfig interface)
- **Calendar page**: `frontend/app/content/calendar/page.tsx` (render recommendations)
- **API integration**: `frontend/lib/api.ts` (already has brand.get/update, no changes needed)

### Key Constraints
- `preferred_post_hours` must be JSONB: `{ "platform": [hour1, hour2, ...] }`
- Historical data available from content_items (platform, created_at/updated_at) but engagement metrics (likes, views) only on trending_content
- Calendar should display recommendations without breaking existing layout
- Brand config schema migration must precede model + backend changes

---

## Execution Plan

**Tasks:** 7 across 4 groups  
**Specialists:** db-agent, brand-agent, intelligence-agent, frontend-agent

### Group 1 (Database & Schema) — parallel

- **[db-agent | EASY]** Create migration to add preferred_post_hours field to brand_configs
  - Files: `supabase/migrations/007_preferred_post_hours.sql` (create)
  - Criteria: 
    1. Migration file created with valid SQL
    2. Adds preferred_post_hours JSONB column with default '{}'::jsonb
    3. Includes comment explaining field structure (e.g., mapping platform → hour array)

### Group 2 (Backend Model & Computation) — depends on Group 1

- **[brand-agent | EASY]** Add preferred_post_hours field to BrandConfig model
  - Files: `backend/brand/models.py` (modify)
  - Criteria:
    1. BrandUpdate model includes `preferred_post_hours: Optional[dict[str, list[int]]] = None`
    2. Field validates that each platform maps to a list of hours (0-23)
    3. No changes to router.py needed (PUT/GET already generic)

- **[intelligence-agent | MEDIUM]** Create compute_optimal_posting_hours function
  - Files: `backend/intelligence/posting_times.py` (create)
  - Read: `backend/database.py`, `backend/intelligence/memory.py` (for patterns)
  - Criteria:
    1. New module `backend/intelligence/posting_times.py` with async function: `compute_optimal_posting_hours(workflow_id: str) -> dict[str, list[int]]`
    2. Function queries published content (status='posted') grouped by platform
    3. For each platform, analyzes publish times (hour from created_at/updated_at) vs engagement (organic_score if available, or count)
    4. Returns top 2-3 hours per platform as recommendations
    5. Falls back to platform defaults if insufficient data (LinkedIn: 9-17, Twitter: 14, Instagram: 19, TikTok: 20)
    6. No database writes — pure computation for now (can be called on-demand)

### Group 3 (Frontend Types & API) — depends on Group 2

- **[frontend-agent | EASY]** Update BrandConfig TypeScript interface
  - Files: `frontend/lib/types.ts` (modify)
  - Criteria:
    1. BrandConfig interface includes `preferred_post_hours?: Record<string, number[]>`
    2. Optional field (for backward compatibility)

### Group 4 (Calendar UI Integration) — depends on Group 3

- **[frontend-agent | MEDIUM]** Surface posting time recommendations on calendar page
  - Files: `frontend/app/content/calendar/page.tsx` (modify)
  - Read: `frontend/lib/api.ts`, `frontend/lib/types.ts`
  - Criteria:
    1. Calendar page fetches workflow ID from URL/context
    2. On mount, fetches brand config including preferred_post_hours
    3. For each content item, if platform matches a platform in preferred_post_hours, displays a subtle badge or tooltip showing recommended hours (e.g., "Best posted 9–17")
    4. No breakage of existing layout — recommendations appear as secondary info
    5. Handles missing data gracefully (if preferred_post_hours not set, no recommendation shown)

---

## Agent Prompts

### Task: db-agent: Create migration for preferred_post_hours

- description: "db-agent: Create migration to add preferred_post_hours field"
- model: haiku
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new Supabase migration that adds a `preferred_post_hours` JSONB column to the brand_configs table.

    The field should store platform-specific optimal posting times, e.g.:
    ```json
    {
      "LinkedIn": [9, 10, 11, 17],
      "Twitter": [14, 15, 19],
      "Instagram": [19, 20, 21]
    }
    ```

    ## Scope
    Create: `supabase/migrations/007_preferred_post_hours.sql`
    Read for context: `supabase/migrations/005_phase3_brand_fields.sql` (for style reference)

    ## Acceptance Criteria
    1. Migration file created at the correct path with proper naming (007_preferred_post_hours.sql)
    2. SQL adds column: `preferred_post_hours jsonb default '{}'::jsonb`
    3. Includes a brief comment above the ALTER TABLE explaining the field (platform → hour array mapping)
    4. SQL is syntactically valid and idempotent (uses IF NOT EXISTS or similar where appropriate)
    5. File follows the style/structure of existing migrations (comments, formatting)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

---

### Task: brand-agent: Add preferred_post_hours to BrandUpdate model

- description: "brand-agent: Add preferred_post_hours field to BrandConfig model"
- model: haiku
- prompt: |
    You are the brand-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Update the BrandUpdate Pydantic model to include the `preferred_post_hours` field, allowing clients to store and update platform-specific optimal posting times.

    ## Scope
    Read for context: `backend/brand/router.py` (to understand how BrandUpdate is used)
    Modify: `backend/brand/models.py`

    ## Acceptance Criteria
    1. BrandUpdate model includes new field: `preferred_post_hours: Optional[dict[str, list[int]]] = None`
    2. Field is optional (so existing updates don't break)
    3. Type hint uses dict[str, list[int]] where key is platform name (string), value is list of hours (0-23)
    4. No validation required beyond type checking (hours validation can be client-side or added later)
    5. File still imports correctly and has no syntax errors

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

---

### Task: intelligence-agent: Create compute_optimal_posting_hours function

- description: "intelligence-agent: Implement compute_optimal_posting_hours function"
- model: sonnet
- prompt: |
    You are the intelligence-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new module `backend/intelligence/posting_times.py` with an async function that computes optimal posting hours per platform based on historical publication and engagement data.

    The function should:
    1. Query published content (status='posted') for the given workflow
    2. Group by platform
    3. Extract publish hour (from created_at or updated_at)
    4. Correlate with engagement metrics if available (from trending_content.organic_score or similar)
    5. Return top 2-3 hours per platform as recommendations
    6. Fall back to platform defaults if insufficient data

    Example output:
    ```python
    {
        "LinkedIn": [9, 10, 17],
        "Twitter": [14, 15, 19],
        "Instagram": [19, 20, 21],
        "TikTok": [20, 21, 22]
    }
    ```

    ## Scope
    Create: `backend/intelligence/posting_times.py`
    Read for context: 
    - `backend/database.py` (for get_supabase pattern)
    - `backend/intelligence/memory.py` (for workflow querying patterns)
    - `supabase/migrations/001_initial_schema.sql` (content_items, trending_content table schemas)

    Modify: None (this is a new module, no other files touched)

    ## Acceptance Criteria
    1. File created at `backend/intelligence/posting_times.py`
    2. Async function signature: `async def compute_optimal_posting_hours(workflow_id: str) -> dict[str, list[int]]`
    3. Function queries content_items table for workflow_id with status='posted'
    4. Extracts hour from published timestamps (datetime → hour extraction)
    5. Groups hours by platform
    6. Returns dict mapping platform → sorted list of top hours (max 3 per platform)
    7. If no published data exists for a platform, returns platform defaults (fallback dict)
    8. No database writes — pure read + computation
    9. Error handling: if query fails or workflow not found, returns empty dict {}
    10. Module imports correctly and has no syntax errors
    11. Includes a docstring explaining the function and return format

    **Platform defaults (fallback):**
    - LinkedIn: [9, 10, 11, 12, 17, 18]
    - Twitter: [14, 15, 19]
    - Instagram: [19, 20, 21]
    - TikTok: [20, 21, 22]
    - Facebook: [13, 14, 19, 20]
    - YouTube: [10, 14, 18]

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

---

### Task: frontend-agent: Update BrandConfig interface

- description: "frontend-agent: Add preferred_post_hours to BrandConfig TypeScript interface"
- model: haiku
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Update the BrandConfig TypeScript interface to include the new `preferred_post_hours` field.

    ## Scope
    Modify: `frontend/lib/types.ts`

    ## Acceptance Criteria
    1. BrandConfig interface includes: `preferred_post_hours?: Record<string, number[]>`
    2. Field is optional (?) for backward compatibility
    3. Type is Record<string, number[]> — platform name → array of hours
    4. File imports/exports correctly, no TypeScript errors
    5. Existing fields unchanged

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

---

### Task: frontend-agent: Surface posting time recommendations on calendar

- description: "frontend-agent: Display posting time recommendations on content calendar"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Modify the content calendar page to fetch and display posting time recommendations for each content item based on the brand's preferred_post_hours configuration.

    The recommendations should appear as a subtle UI element (badge, tooltip, or inline text) showing the optimal posting hours for that platform, e.g., "Best posted 9–17".

    ## Scope
    Read for context:
    - `frontend/lib/api.ts` (for API patterns)
    - `frontend/lib/types.ts` (BrandConfig structure)
    
    Modify: `frontend/app/content/calendar/page.tsx`

    ## Acceptance Criteria
    1. Calendar page fetches workflow_id from route/context (assume it's available via props or URL)
    2. On component mount, fetches brand config using `brand.get(workflow_id)`
    3. Extracts preferred_post_hours from brand config
    4. For each calendar item, checks if its platform exists in preferred_post_hours
    5. If match found, displays recommendation badge/text (e.g., "Optimal: 9–17" or tooltip on hover)
    6. If no recommendation exists for that platform, no recommendation shown
    7. Handles loading state gracefully (doesn't block calendar rendering if brand fetch is slow)
    8. Handles errors gracefully (if brand.get fails, calendar still renders without recommendations)
    9. Styling consistent with existing dark theme (bg-[#0F172A], accent-[#C9A96E], borders-[#334155])
    10. Framer Motion animations preserved (no deadlock from nested motion divs)
    11. No breaking changes to existing calendar layout or functionality

    **UI Location Suggestion:**
    - Could appear as a small badge next to platform/content_type badges
    - Or as a subtle tooltip on hover over the platform badge
    - Keep it secondary info (don't overwhelm existing badge row)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

---

## Status Log

- 2026-04-22 11:30 created, status=awaiting-approval
