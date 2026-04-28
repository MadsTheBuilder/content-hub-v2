# Orchestration Plan: Platform-Specific Posting Time Recommendations

## Summary

Implement posting time recommendations by:
1. Adding `preferred_post_hours` JSONB column to brand_configs table
2. Extending BrandUpdate model to accept posting hours per platform
3. Creating intelligence function to compute optimal hours from historical platform performance
4. Exposing recommendations via new brand router endpoint
5. Building calendar UI component to display recommendations

---

## Execution Plan

### Group 1: Database Schema (Parallel)

**Task 1.1: [db-agent | EASY] Create migration for preferred_post_hours**
- Files: `supabase/migrations/007_posting_time_recommendations.sql`
- Add JSONB column `preferred_post_hours` to brand_configs with default `{}`
- Acceptance: Migration applies cleanly, follows existing conventions

---

### Group 2: Backend Models (Parallel, depends on Group 1)

**Task 2.1: [brand-agent | EASY] Extend BrandUpdate with preferred_post_hours**
- Files: `backend/brand/models.py`
- Add field: `preferred_post_hours: Optional[dict[str, list[int]]] = None`
- Document structure: `{"instagram": [9, 17, 20], "tiktok": [12, 19]}`
- Acceptance: Type-correct, documented, validates without errors

**Task 2.2: [intelligence-agent | EASY] Document platform_performance structure**
- Files: `backend/intelligence/memory.py` (comments only)
- Add comments explaining platform_content_map extensibility
- Note performance metrics that could be tracked per platform
- Acceptance: Clear documentation, no code changes

---

### Group 3: Intelligence Recommendations (Sequential, depends on Group 2)

**Task 3.1: [intelligence-agent | MEDIUM] Implement compute_posting_time_recommendations()**
- Files: `backend/intelligence/suggestions.py`
- New function: `async def compute_posting_time_recommendations(workflow_id: str, platform: str) -> list[int]`
- Logic:
  - Query posted content_items by platform
  - Extract hour from updated_at (or created_at fallback)
  - Build frequency histogram of hours (0-23)
  - Return top 3 hours by frequency
  - Default to [9, 12, 18] if < 3 posts
- Acceptance: Async, returns 3-hour list, handles edge cases

**Task 3.2: [brand-agent | EASY] Add posting-times endpoint**
- Files: `backend/brand/router.py`
- New endpoint: `GET /api/v1/brand/{workflow_id}/posting-times`
- Returns: `{"recommended_hours": {"instagram": [9, 17, 20], "tiktok": [12, 19], ...}}`
- Calls compute_posting_time_recommendations() for each platform
- Requires auth, handles missing workflow with 404
- Acceptance: Auth-protected, correct response format, error handling

---

### Group 4: Frontend UI (Parallel, depends on Group 3)

**Task 4.1: [frontend-agent | MEDIUM] Create PostingTimeRecommendations component**
- Files: `frontend/components/PostingTimeRecommendations.tsx`
- Props: `{workflowId: string, platform: string}`
- Display: Pill buttons with hours in 12-hour format ("9 AM", "5 PM")
- Styling: Dark theme (#0F172A, #C9A96E), Framer Motion fade-in
- Acceptance: Responsive, accessible, animated, themed correctly

**Task 4.2: [frontend-agent | MEDIUM] Integrate into calendar page**
- Files: `frontend/app/content/calendar/page.tsx`, `frontend/lib/api.ts`, `frontend/lib/types.ts`
- Features:
  - Fetch recommendations on mount via `brand.postingTimes(workflowId)`
  - Show recommendations below/beside each item's platform
  - Use PostingTimeRecommendations component for display
  - Add PostingTimeRecommendations type interface
- Acceptance: Fetches correctly, displays non-intrusively, types defined, handles errors

---

## Task Summary

| Group | Count | Complexity | Blockers |
|-------|-------|-----------|----------|
| 1 (Schema) | 1 | EASY | None |
| 2 (Models) | 2 | EASY | Group 1 |
| 3 (Intelligence) | 2 | MEDIUM | Group 2 |
| 4 (Frontend) | 2 | MEDIUM | Group 3 |
| **Total** | **7** | **Mixed** | **Ordered** |

---

## Specialist Involvement

- **db-agent**: Migration creation (1 task)
- **brand-agent**: Model extension, router endpoint (2 tasks)
- **intelligence-agent**: Recommendation function, memory docs (2 tasks)
- **frontend-agent**: Component & calendar integration (2 tasks)

---

## Execution Dependencies

```
Group 1 (Schema)
    ↓
Group 2 (Models) — runs in parallel
    ↓
Group 3 (Intelligence) — runs sequentially (Task 3.1 → 3.2)
    ↓
Group 4 (Frontend) — runs in parallel
```

No file conflicts: each task owns distinct files; brand router doesn't conflict with models; calendar page doesn't conflict with component creation.

---

## Scope Summary

**Database:**
- 1 new migration

**Backend changes:**
- 2 models/model extensions
- 2 new functions
- 1 new endpoint

**Frontend additions:**
- 1 new component
- 1 page integration
- 1 API client function
- 1 type interface

**Total files touched:** ~12 (6 modified, 1 created for migration, 1 component, 4 type/API client updates)
