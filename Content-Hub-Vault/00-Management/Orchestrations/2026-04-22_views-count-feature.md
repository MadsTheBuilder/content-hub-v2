---
slug: views-count-feature
created: 2026-04-22
status: abandoned
current_group: null
groups_complete: []
specialists_involved: [db-agent, pipeline-agent, frontend-agent]
---

# Orchestration: Add views_count Tracking to Content Items

## Recon summary

- **content_items table** currently has 15 columns; no views_count column exists
- **Content access endpoints**: GET /api/v1/content/library, GET /api/v1/content/{content_id}, GET /api/v1/content/calendar currently do not track view counts
- **Frontend ContentItem type** has 15 properties but no views_count field
- **Content library page** displays content cards but no views display
- **Schema history**: Latest migration is 006_ab_experiments.sql; next migration is 007
- **No existing view tracking patterns** in the codebase

## Execution plan

**Tasks:** 3 across 3 groups  
**Specialists:** db-agent, pipeline-agent, frontend-agent

### Group 1 (parallel)

- [db-agent | EASY] Create migration to add views_count column
  - Files: supabase/migrations/007_add_views_count.sql
  - Criteria: Column added with default value 0, indexed for performance

### Group 2 (depends on Group 1)

- [pipeline-agent | MEDIUM] Add view increment logic to content endpoints
  - Files: backend/content/router.py
  - Criteria: GET /content/{content_id} increments views_count; response includes count

### Group 3 (depends on Group 2)

- [frontend-agent | MEDIUM] Add views_count to types and display on library page
  - Files: frontend/lib/types.ts, frontend/app/content/library/page.tsx
  - Criteria: ContentItem type includes views_count, library page displays count on cards

## Status log

- 2026-04-22 14:32 created, status=awaiting-approval
