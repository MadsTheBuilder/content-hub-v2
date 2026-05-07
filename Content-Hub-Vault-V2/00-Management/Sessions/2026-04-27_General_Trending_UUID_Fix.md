---
status: Completed
date: 2026-04-27
type: session_summary
---

# Session: General Trending UUID Fix — suggestions endpoint 500

Modifies: [[backend/intelligence/suggestions.py]], [[backend/research/apify_client.py]], [[backend/tests/test_general_trending.py]]
Creates: [[supabase/migrations/008_general_trending_nullable.sql]]

## Root Cause

`GET /api/v1/workflows/{id}/suggestions` was returning 500 on every call:

```
postgrest.exceptions.APIError: {'code': '22P02', 'message': 'invalid input syntax for type uuid: "__general__"'}
```

`trending_content.workflow_id` is `uuid NOT NULL` in the schema. The general trending feature used `"__general__"` as a sentinel string — which PostgreSQL rejects on any query because it cannot cast that to a UUID.

The general trending insert side (`apify_client.py`) had the same bug: it would also fail to persist any general trending posts to the DB for the same reason. The feature was broken at both ends since it shipped.

## Fix

**Schema** (`008_general_trending_nullable.sql`): Dropped `NOT NULL` on `trending_content.workflow_id`. `NULL` now means "general/platform-wide trending". The FK constraint remains valid (NULLs don't violate FK). Service-role backend reads are unaffected by RLS.

**`backend/research/apify_client.py`**: `"workflow_id": "__general__"` → `None` at both insert sites (live scrape result and mock fallback).

**`backend/intelligence/suggestions.py`**: 
- `.eq("workflow_id", "__general__")` → `.is_("workflow_id", "null")`
- `post.get("workflow_id") == "__general__"` → `post.get("workflow_id") is None` (2 occurrences)

**`backend/tests/test_general_trending.py`**: All mock data updated to use `None` for `workflow_id`.

## Test Results

4/4 tests pass after the fix.

## Outstanding

None. The suggestions endpoint now works. General trending inserts will also work correctly when the scheduler runs.
