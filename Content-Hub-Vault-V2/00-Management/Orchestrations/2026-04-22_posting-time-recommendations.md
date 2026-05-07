---
slug: posting-time-recommendations
created: 2026-04-22
status: abandoned
current_group: null
groups_complete: []
specialists_involved: [db-agent, brand-agent, intelligence-agent, frontend-agent]
---

# Orchestration: Platform-Specific Posting Time Recommendations

## Recon summary

- **Brand config** stored in Supabase `brand_configs` table; model defined in `backend/brand/models.py`; endpoints in `backend/brand/router.py`. Missing `preferred_post_hours` field.
- **Intelligence layer** in `backend/intelligence/` with publication memory tracking platform-content associations and performance data via `content_publication_memory` table.
- **Content calendar** page at `frontend/app/content/calendar/page.tsx` displays items grouped by month; calendar API at `/api/v1/content/calendar`; ready for recommendation integration.
- **Data models** in `frontend/lib/types.ts` define ContentItem, BrandConfig, Workflow; no post-time recommendation types yet.
- **Existing patterns**: Brand fields added via SQL migrations; intelligence recommendations generated via `generate_suggestions()` and surfaced through API; all frontend API calls route through `frontend/lib/api.ts`.

## Execution plan

### Group 1 (Schema) — Parallel
**Dependency:** None

- [db-agent | EASY] Add preferred_post_hours column to brand_configs
  Files: `supabase/migrations/007_posting_time_recommendations.sql`
  Criteria:
  1. New migration file created
  2. Adds JSONB column `preferred_post_hours` to brand_configs (stores {platform: [hours]} map)
  3. Default value is empty JSONB object `{}`
  4. Migration can be applied cleanly

### Group 2 (Backend Schema Models) — Parallel
**Dependency:** Group 1

- [brand-agent | EASY] Extend BrandUpdate model with preferred_post_hours field
  Files: `backend/brand/models.py`
  Criteria:
  1. BrandUpdate model includes: `preferred_post_hours: Optional[dict[str, list[int]]] = None`
  2. Comment explains structure: e.g., {"instagram": [9, 17, 20], "tiktok": [12, 19]}
  3. Existing fields unchanged
  4. Model validates correctly

- [intelligence-agent | EASY] Extend content_publication_memory type hints (documentation)
  Files: `backend/intelligence/memory.py`
  Criteria:
  1. Code comments identify platform_performance data structure
  2. Note platform_content_map extensibility for performance metrics
  3. No migrations or code changes yet

### Group 3 (Intelligence Recommendations) — Sequential
**Dependency:** Group 2

- [intelligence-agent | MEDIUM] Implement compute_posting_time_recommendations() function
  Files: `backend/intelligence/suggestions.py`
  Criteria:
  1. New function `compute_posting_time_recommendations(workflow_id: str, platform: str) -> list[int]`
  2. Queries content_publication_memory and content_items for workflow
  3. Analyzes posted items by platform, extracts posted_at hour, builds frequency histogram
  4. Returns top 3 hours (by frequency) for given platform
  5. Falls back to [9, 12, 18] if < 3 posts on platform
  6. Async function using get_supabase()

- [brand-agent | EASY] Expose posting_time_recommendations via brand router endpoint
  Files: `backend/brand/router.py`
  Criteria:
  1. New endpoint: `GET /api/v1/brand/{workflow_id}/posting-times`
  2. Returns: `{"recommended_hours": {"instagram": [9, 17, 20], "tiktok": [12, 19], ...}}`
  3. Calls compute_posting_time_recommendations() for each platform in workflow
  4. Requires auth (get_current_user dependency)

### Group 4 (Frontend) — Parallel
**Dependency:** Group 3

- [frontend-agent | MEDIUM] Add PostingTimeRecommendations component
  Files: `frontend/components/PostingTimeRecommendations.tsx`
  Criteria:
  1. Component accepts: `{workflowId: string, platform: string}`
  2. Displays recommended hours as pill buttons/icons
  3. 12-hour format (e.g., "9 AM", "5 PM")
  4. Dark theme (#0F172A bg, #C9A96E accent)
  5. Framer Motion fade-in animation

- [frontend-agent | MEDIUM] Integrate recommendations into calendar page
  Files: `frontend/app/content/calendar/page.tsx`, `frontend/lib/api.ts`, `frontend/lib/types.ts`
  Criteria:
  1. Calendar fetches posting recommendations on mount
  2. Shows recommended hours for each item's platform
  3. Recommendation panel non-intrusive positioning
  4. API client exports `brand.postingTimes(workflowId)` function
  5. Types.ts includes PostingTimeRecommendations interface

## Agent prompts

### Task: db-agent: Add preferred_post_hours column to brand_configs

- description: "db-agent: Add preferred_post_hours column to brand_configs"
- model: haiku
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Create a new migration file that adds a `preferred_post_hours` column to the `brand_configs` table in Supabase. This column will store preferred posting hours per platform as a JSONB object.

    ## Scope

    Read for context: `supabase/migrations/005_phase3_brand_fields.sql`, `supabase/migrations/001_initial_schema.sql`
    Modify: Create new file `supabase/migrations/007_posting_time_recommendations.sql`

    ## Acceptance Criteria

    1. Migration file follows existing naming and SQL style conventions
    2. Adds JSONB column `preferred_post_hours` with default `'{}'::jsonb`
    3. No other changes to brand_configs table
    4. SQL syntax is correct and idempotent (uses `if not exists` where appropriate)
    5. Migration file is ready to apply via Supabase CLI

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: brand-agent: Extend BrandUpdate model with preferred_post_hours

- description: "brand-agent: Extend BrandUpdate model with preferred_post_hours"
- model: haiku
- prompt: |
    You are the brand-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Extend the `BrandUpdate` Pydantic model in `backend/brand/models.py` to include a new field `preferred_post_hours` that stores recommended posting hours per platform. Structure: `{"instagram": [9, 17, 20], "tiktok": [12, 19]}`

    ## Scope

    Read for context: `backend/brand/models.py` (current state)
    Modify: `backend/brand/models.py`

    ## Acceptance Criteria

    1. BrandUpdate model includes new field: `preferred_post_hours: Optional[dict[str, list[int]]] = None`
    2. Field is documented with a comment explaining the structure and use
    3. Type hint is correct (dict of string platform names to list of hour integers)
    4. All existing fields remain unchanged
    5. Model can be imported and instantiated without errors

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: intelligence-agent: Extend content_publication_memory type hints

- description: "intelligence-agent: Extend content_publication_memory type hints"
- model: haiku
- prompt: |
    You are the intelligence-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Review `backend/intelligence/memory.py` and add code comments documenting how the `content_publication_memory` data structure can be extended to support platform-specific performance tracking. Identify what additional fields or structure might be needed to compute posting time recommendations. Do NOT implement new code yet — just document the structure for future work.

    ## Scope

    Read for context: `backend/intelligence/memory.py`, `supabase/migrations/001_initial_schema.sql`
    Modify: `backend/intelligence/memory.py` (comments only)

    ## Acceptance Criteria

    1. Comments explain platform_content_map structure and extensibility
    2. Notes identify what performance metrics (views, engagement) could be tracked per platform
    3. Comments reference the schema column names and structures
    4. No functional code changes — documentation only

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: intelligence-agent: Implement compute_posting_time_recommendations()

- description: "intelligence-agent: Implement compute_posting_time_recommendations() function"
- model: sonnet
- prompt: |
    You are the intelligence-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Implement a new function `compute_posting_time_recommendations()` in `backend/intelligence/suggestions.py` that analyzes historical posting data per platform and recommends optimal posting hours based on engagement frequency.

    The function should:
    1. Query the workflow's content_items where status='posted'
    2. Group by platform
    3. Extract the hour from each item's `updated_at` timestamp (or creation time)
    4. Build a frequency histogram of hours (0-23)
    5. Return the top 3 hours by frequency
    6. Default to [9, 12, 18] if < 3 posts on that platform exist

    ## Scope

    Read for context: `backend/intelligence/suggestions.py`, `backend/database.py`, database schema
    Modify: `backend/intelligence/suggestions.py` (add new function)

    ## Acceptance Criteria

    1. Function signature: `async def compute_posting_time_recommendations(workflow_id: str, platform: str) -> list[int]:`
    2. Returns list of 3 integers (hours 0-23) in descending order of frequency
    3. Queries content_items WHERE workflow_id = X AND platform = Y AND status = 'posted'
    4. Extracts hour from updated_at (or falls back to created_at)
    5. Falls back to [9, 12, 18] if fewer than 3 posts exist
    6. Uses async/await with get_supabase() for database access
    7. Function is properly documented with docstring

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: brand-agent: Expose posting_time_recommendations via brand router

- description: "brand-agent: Expose posting_time_recommendations via brand router"
- model: sonnet
- prompt: |
    You are the brand-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Add a new GET endpoint to the brand router that exposes posting time recommendations for all platforms in a workflow. The endpoint should call the intelligence layer's `compute_posting_time_recommendations()` function for each platform and return aggregated results.

    ## Scope

    Read for context: `backend/brand/router.py`, `backend/intelligence/suggestions.py` (new function from previous task)
    Modify: `backend/brand/router.py` (add new endpoint)

    ## Acceptance Criteria

    1. New endpoint: `GET /api/v1/brand/{workflow_id}/posting-times`
    2. Requires authentication (uses get_current_user dependency)
    3. Fetches the workflow to get its list of platforms
    4. Calls compute_posting_time_recommendations(workflow_id, platform) for each platform
    5. Returns JSON: `{"recommended_hours": {"instagram": [9, 17, 20], "tiktok": [12, 19], ...}}`
    6. Handles missing workflow gracefully with 404 error
    7. Function is properly documented

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: frontend-agent: Add PostingTimeRecommendations component

- description: "frontend-agent: Add PostingTimeRecommendations component"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Create a new React component `PostingTimeRecommendations.tsx` that displays recommended posting hours for a given platform. The component should present hours in a visually appealing way using the project's dark theme and Framer Motion.

    ## Scope

    Create: `frontend/components/PostingTimeRecommendations.tsx`
    Read for context: `frontend/components/` (existing components for style reference)

    ## Acceptance Criteria

    1. Component exports default function: `PostingTimeRecommendations(props: {workflowId: string, platform: string})`
    2. Displays recommended hours as clickable/interactive pill buttons
    3. Hours shown in 12-hour format (e.g., "9 AM", "5 PM", "12 PM")
    4. Uses dark theme: background #0F172A, accent #C9A96E, borders #334155
    5. Includes Framer Motion fade-in animation on mount (variant: { initial: {opacity: 0}, animate: {opacity: 1} })
    6. Responsive design (works on mobile and desktop)
    7. Exports as `export default PostingTimeRecommendations`

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: frontend-agent: Integrate recommendations into calendar page

- description: "frontend-agent: Integrate recommendations into calendar page"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task

    Integrate posting time recommendations into the content calendar page. The page should fetch recommendations on mount and display them alongside or below each content item's platform.

    ## Scope

    Read for context: `frontend/app/content/calendar/page.tsx`, `frontend/lib/api.ts`, `frontend/lib/types.ts`
    Modify: `frontend/app/content/calendar/page.tsx`, `frontend/lib/api.ts`, `frontend/lib/types.ts`
    Create: New type interface in types.ts if needed

    ## Acceptance Criteria

    1. Calendar page uses `useEffect` to fetch posting recommendations on mount (once per workflow)
    2. API client exports new function: `brand.postingTimes(workflowId: string) -> Promise<{recommended_hours: Record<string, number[]>}>`
    3. For each content item displayed, show recommended hours if available for that item's platform
    4. Recommendation display is non-intrusive (subtle styling, below/beside item)
    5. Uses PostingTimeRecommendations component (from previous task) for display
    6. Types.ts includes interface: `PostingTimeRecommendations: {recommended_hours: Record<string, number[]>}`
    7. Handles loading/error states gracefully

    ## When done

    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

## Status log

- 2026-04-22 18:00 created, status=awaiting-approval
