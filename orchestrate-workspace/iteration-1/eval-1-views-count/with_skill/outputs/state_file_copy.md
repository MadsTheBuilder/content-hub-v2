---
slug: views-count-feature
created: 2026-04-22
status: awaiting-approval
current_group: null
groups_complete: []
specialists_involved: [db-agent, pipeline-agent, frontend-agent]
---

# Orchestration: Add views_count Column to content_items

## Recon summary

- **Database schema**: `content_items` table (001_initial_schema.sql) has 15 columns including id, workflow_id, user_id, content_type, platform, title, script_text, published_script, storyboard, asset_urls, status, rejection_flag, generation_metadata, error_message, created_at, updated_at. **No views_count column exists.**
- **Existing pattern**: `trending_content` table already has `view_count bigint` column; same pattern can be used.
- **Backend API**: `/content/library` endpoint in `backend/content/router.py` retrieves content items with filtering. No view tracking logic currently exists.
- **Frontend display**: `frontend/app/content/library/page.tsx` renders content cards showing status, platform, title, content_type, created_at. **ContentItem type in types.ts does not include views_count.**
- **Architecture**: Backend uses Supabase service_role key for writes; frontend receives data via API. Increment pattern needed when content is accessed (GET endpoint).

## Execution plan

**Tasks:** 3 across 3 groups
**Specialists:** db-agent, pipeline-agent, frontend-agent

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

## Agent prompts

### Task: db-agent: Create migration for views_count column
- description: "db-agent: Create migration for views_count column"
- model: haiku
- prompt: |
    You are the db-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new Supabase migration file to add a `views_count` column to the `content_items` table. This column will track how many times each piece of content has been viewed.

    ## Scope
    Read for context: supabase/migrations/001_initial_schema.sql
    Create: supabase/migrations/007_views_count.sql

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. Migration file `007_views_count.sql` exists at supabase/migrations/
    2. File contains ALTER TABLE public.content_items ADD COLUMN views_count bigint DEFAULT 0;
    3. File includes a performance index: CREATE INDEX idx_content_views on public.content_items(views_count DESC);
    4. File follows the same format/style as existing migrations (comments, clear structure)
    5. File is idempotent (uses IF NOT EXISTS or similar for safety)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: pipeline-agent: Wire views_count increment into content retrieval
- description: "pipeline-agent: Wire views_count increment into content retrieval"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Modify backend endpoints to track and increment views_count when content is accessed. You need to:
    1. Update GET /content/{id} endpoint to increment views_count in the DB
    2. Update GET /content/library endpoint to return views_count in the response
    3. Update the backend ContentItem model to include views_count field
    4. Ensure increments happen atomically via SQL to avoid race conditions

    ## Scope
    Read for context: backend/database.py, backend/content/models.py (current structure)
    Modify: backend/content/router.py, backend/content/models.py

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. ContentItem Pydantic model in backend/content/models.py includes views_count: int field
    2. GET /content/{id} endpoint (likely around line 150+ in router.py) increments views_count via SQL UPDATE before returning the item
    3. GET /content/library endpoint returns views_count for each item in the response
    4. Increment is atomic (single SQL statement) to avoid race conditions
    5. Default views_count is 0 for newly created content items (handled by DB schema migration)
    6. Code passes linting and follows existing patterns in router.py

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

### Task: frontend-agent: Display views_count on library cards
- description: "frontend-agent: Display views_count on library cards"
- model: sonnet
- prompt: |
    You are the frontend-agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Update the frontend to display the views_count from the API on each content card in the library page. You need to:
    1. Add views_count field to ContentItem type in types.ts
    2. Display views_count as a badge/pill on the library cards (similar to status, platform, content_type)
    3. Ensure the display is visually consistent with existing card design (dark theme, [#C9A96E] accent color)

    ## Scope
    Read for context: frontend/app/content/library/page.tsx (current card structure), frontend/lib/api.ts
    Modify: frontend/lib/types.ts, frontend/app/content/library/page.tsx

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. ContentItem interface in frontend/lib/types.ts includes views_count: number field
    2. Library page card displays views_count (e.g., "123 views" or "view count: 123")
    3. View count badge is positioned logically on the card (suggested: near the date, or in a separate row)
    4. Styling matches existing design: dark bg (#1E293B), text color, accent highlights match [#C9A96E]
    5. View count updates immediately when library is refreshed
    6. Code follows existing patterns (Tailwind classes, component structure, motion animations)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you changed and why.

## Status log
- 2026-04-22 14:15 created, status=awaiting-approval
