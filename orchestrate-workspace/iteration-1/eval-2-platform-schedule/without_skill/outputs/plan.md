# Platform-Specific Posting Time Recommendations — Implementation Plan

**Status:** Plan Document  
**Date:** 2026-04-22  
**Scope:** Store preferred posting hours per platform in brand config, compute optimal hours using the intelligence layer, and surface recommendations on the content calendar page.

---

## Overview

The task requires implementing three integrated layers:
1. **Persistence Layer:** Add `preferred_post_hours` field to store per-platform posting hour preferences in `brand_configs` table
2. **Intelligence Layer:** Create a recommendation engine that computes optimal posting times based on historical performance and user preferences
3. **UI Layer:** Display posting time recommendations on the content calendar page

---

## Technical Context

### Current State
- **Database:** Supabase PostgreSQL with `brand_configs` table (stores visual branding, fonts, templates)
- **Backend:** FastAPI at `/backend/main.py`; brand endpoints in `/backend/brand/router.py`
- **Intelligence:** Existing suggestion system in `/backend/intelligence/suggestions.py` generates trending content suggestions enriched with user preferences
- **Frontend:** React+Next.js 15; calendar page at `/frontend/app/content/calendar/page.tsx`
- **API Communication:** TypeScript types in `/frontend/lib/types.ts`; API methods in `/frontend/lib/api.ts`

### Key Architecture Patterns
- **Service Role Bypass:** Backend uses Supabase service role key for administrative writes (MVP approach)
- **JSONB for Flexible Data:** Prefer JSONB columns for configuration that varies per platform
- **Memory System:** `content_publication_memory` table tracks publishing patterns (hook styles, content types, platforms)
- **Suggestions Module:** Existing `/backend/intelligence/suggestions.py` is the pattern for generating ranked, personalized recommendations

---

## Change Summary

| Layer | Component | Change Type | File(s) |
|-------|-----------|-------------|---------|
| **Database** | Schema Migration | Add `preferred_post_hours` JSONB column to `brand_configs` | `supabase/migrations/007_posting_hours.sql` (NEW) |
| **Backend/Brand** | Data Model | Add `preferred_post_hours` field to `BrandUpdate` Pydantic model | `backend/brand/models.py` |
| **Backend/Intelligence** | New Module | Create posting time recommendation engine | `backend/intelligence/posting_recommendations.py` (NEW) |
| **Backend/Brand** | Router Endpoint | Expose GET/PUT endpoints for managing preferred posting hours | `backend/brand/router.py` (modify) |
| **Backend/Content** | Calendar Endpoint | Augment `/content/calendar` response to include posting time recommendations per item | `backend/content/router.py` (modify) |
| **Frontend/Types** | TypeScript Interfaces | Extend `BrandConfig` interface with `preferred_post_hours`; add `PostingRecommendation` type | `frontend/lib/types.ts` |
| **Frontend/API** | API Client | Add endpoints to manage posting hours configuration | `frontend/lib/api.ts` |
| **Frontend/Calendar** | UI Component | Display posting time recommendations alongside content items | `frontend/app/content/calendar/page.tsx` |

---

## Detailed Change Plan

### 1. Database Schema Migration (NEW FILE)
**File:** `supabase/migrations/007_posting_hours.sql`

**Purpose:** Add JSONB column to store per-platform preferred posting hours.

**Structure:**
```sql
-- Add preferred_post_hours to brand_configs
-- Format: { "tiktok": { "hours": [7, 8, 19, 20], "timezone": "UTC" }, 
--           "instagram": { "hours": [6, 9, 20], "timezone": "UTC" }, ... }

alter table public.brand_configs
  add column if not exists preferred_post_hours jsonb default '{}'::jsonb;
```

**Logic:**
- JSONB keyed by platform (tiktok, instagram, youtube, linkedin)
- Each platform has `hours` (array of integers 0-23) and optional `timezone`
- Defaults to empty object (no preferences set initially)
- No validation constraint; application layer validates

---

### 2. Backend Brand Data Model
**File:** `backend/brand/models.py`

**Change:**
```python
# Add to BrandUpdate class:
preferred_post_hours: Optional[dict[str, dict]] = None
# Example: {"tiktok": {"hours": [7, 8, 19, 20], "timezone": "UTC"}}
```

**Rationale:** Expose the new column through the Pydantic model so users can update posting hour preferences.

---

### 3. Backend Posting Recommendations Module (NEW FILE)
**File:** `backend/intelligence/posting_recommendations.py`

**Purpose:** Compute optimal posting hours based on:
1. Historical performance data from `content_publication_memory` (publish count, platform engagement)
2. User's stored `preferred_post_hours` in brand config
3. Trending content patterns for each platform

**Exported Function:**
```python
async def compute_posting_recommendation(
    workflow_id: str,
    platform: str,
    content_type: str,
    brand_config: dict,
) -> dict:
    """
    Return optimal posting hour(s) for a specific platform + content type.
    
    Returns:
    {
        "platform": "tiktok",
        "recommended_hours": [7, 8, 19, 20],
        "confidence": 0.75,
        "reason": "Best performance on Tuesday-Thursday mornings (7-8 UTC) and evenings (19-20 UTC)",
        "data_source": "user_preferences",  # or "historical_data" or "trending_signals"
    }
    """
```

**Algorithm:**
1. Check if user has `preferred_post_hours[platform]` defined in brand config → use those with confidence 0.9
2. If not, query `content_publication_memory` for engagement patterns per platform
3. If no memory exists, use platform-wide trending patterns from `trending_content` table
4. Return ranked hours with confidence score and explanation

**Complexity Level:** Medium
- Requires reading from 3 tables: `brand_configs`, `content_publication_memory`, `trending_content`
- Scoring logic: weighted blend of user prefs (50%), historical perf (35%), trending (15%)
- No external APIs; all computation in-band

---

### 4. Backend Brand Router Endpoint
**File:** `backend/brand/router.py`

**New Endpoints:**

**PUT /api/v1/brand/{workflow_id}/posting-hours**
- Accept `{ "platform": "tiktok", "hours": [7, 8, 19, 20], "timezone": "UTC" }`
- Update `brand_configs.preferred_post_hours[platform]`
- Return updated brand config

**GET /api/v1/brand/{workflow_id}/posting-hours**
- Return current `preferred_post_hours` for all platforms
- Example: `{ "tiktok": { "hours": [7, 8, 19, 20], "timezone": "UTC" }, ... }`

**Modifications to existing GET /api/v1/brand/{workflow_id}**
- No change to structure; `preferred_post_hours` already returned via `BrandUpdate` serialization

---

### 5. Backend Calendar Endpoint Enhancement
**File:** `backend/content/router.py`

**Modify:** `@router.get("/calendar")` endpoint

**Current:** Returns list of content items with minimal fields (id, title, content_type, platform, status, created_at, updated_at)

**Enhanced Response:**
```python
{
  "items": [
    {
      "id": "uuid",
      "title": "string",
      "content_type": "slides",
      "platform": "tiktok",
      "status": "ready",
      "created_at": "iso-string",
      "updated_at": "iso-string",
      # NEW FIELD:
      "posting_recommendation": {
        "recommended_hours": [7, 8, 19, 20],
        "confidence": 0.75,
        "reason": "Based on historical performance",
        "timezone": "UTC"
      }
    }
  ]
}
```

**Implementation:**
```python
# Inside calendar endpoint:
for item in result.data:
    brand_config = sb.table("brand_configs").select("*").eq("workflow_id", item["workflow_id"]).single().execute().data or {}
    
    from backend.intelligence.posting_recommendations import compute_posting_recommendation
    recommendation = await compute_posting_recommendation(
        workflow_id=item["workflow_id"],
        platform=item["platform"],
        content_type=item["content_type"],
        brand_config=brand_config,
    )
    item["posting_recommendation"] = recommendation
```

**Note:** Add field only if recommendation exists; nullable if computation fails gracefully.

---

### 6. Frontend TypeScript Types
**File:** `frontend/lib/types.ts`

**Additions:**

```typescript
// Extend BrandConfig interface
export interface BrandConfig {
  // ... existing fields ...
  preferred_post_hours?: Record<string, { hours: number[]; timezone?: string }>;
}

// New interface for posting recommendations
export interface PostingRecommendation {
  platform: string;
  recommended_hours: number[];
  confidence: number;
  reason: string;
  timezone?: string;
}

// Extend ContentItem interface
export interface ContentItem {
  // ... existing fields ...
  posting_recommendation?: PostingRecommendation;
}
```

---

### 7. Frontend API Client
**File:** `frontend/lib/api.ts`

**Add to `brand` export:**
```typescript
export const brand = {
  // ... existing methods ...
  
  getPostingHours: (workflowId: string) =>
    fetchAPI(`/brand/${workflowId}/posting-hours`),
  
  updatePostingHours: (workflowId: string, data: { platform: string; hours: number[]; timezone?: string }) =>
    fetchAPI(`/brand/${workflowId}/posting-hours`, { method: "PUT", body: JSON.stringify(data) }),
};
```

---

### 8. Frontend Calendar UI Enhancement
**File:** `frontend/app/content/calendar/page.tsx`

**Modifications:**

**Add visual indicator section in the calendar item card:**
- Display recommended hours inline below platform/content-type badges
- Show as a small chip with hours list (e.g., "Post at 7–8 AM or 7–8 PM")
- Color highlight based on confidence (gold/accent color for high confidence)
- Tooltip on hover showing reason and data source

**Rendering Logic:**
```tsx
{item.posting_recommendation && (
  <div className="text-[9px] font-medium text-[#C9A96E] mt-1">
    💡 Best time: {formatHours(item.posting_recommendation.recommended_hours)}
  </div>
)}
```

**Placement:** Between status badge and chevron-right icon on each calendar item card.

---

## Execution Order & Verification Checklist

### Phase 1: Database & Models (Prerequisite)
- [ ] Create migration file `007_posting_hours.sql`
- [ ] Apply migration to Supabase (manual step; not code)
- [ ] Update `BrandUpdate` Pydantic model with `preferred_post_hours` field
- [ ] **Verify:** `brand_configs` table has new JSONB column; Pydantic model reflects it

### Phase 2: Intelligence Layer
- [ ] Create `posting_recommendations.py` module with `compute_posting_recommendation()` function
- [ ] Implement scoring logic (user prefs 50%, historical 35%, trending 15%)
- [ ] Test with mock data to ensure it returns valid recommendation objects
- [ ] **Verify:** Function returns dict with `recommended_hours`, `confidence`, `reason`, `timezone`

### Phase 3: Backend API
- [ ] Add `PUT /brand/{workflow_id}/posting-hours` endpoint
- [ ] Add `GET /brand/{workflow_id}/posting-hours` endpoint
- [ ] Modify `/content/calendar` to call `compute_posting_recommendation()` for each item
- [ ] **Verify:** Calendar endpoint returns items with `posting_recommendation` field populated

### Phase 4: Frontend Types & API
- [ ] Extend `BrandConfig` and `ContentItem` TypeScript interfaces
- [ ] Add `PostingRecommendation` interface
- [ ] Add `getPostingHours` and `updatePostingHours` methods to `brand` API object
- [ ] **Verify:** TypeScript compilation succeeds; types are exported

### Phase 5: Frontend UI
- [ ] Update calendar page component to render posting recommendations
- [ ] Style the recommendation chip to match design system (gold/accent color, small text)
- [ ] Test rendering on calendar with sample data
- [ ] **Verify:** Calendar displays "Best time: 7–8 AM, 7–8 PM" (or similar) under each item

### Phase 6: Integration & End-to-End Testing
- [ ] Call brand API to set posting hours for a platform
- [ ] Verify hours are persisted and returned on GET
- [ ] Generate a content item for that platform
- [ ] Check calendar page; verify recommendation appears
- [ ] Edit posting hours; verify calendar updates reflect new recommendation
- [ ] **Verify:** Full flow works without errors; UI is responsive

---

## Assumptions & Decisions

### Assumptions
1. **No Multi-Timezone Complexity (MVP):** Recommendations use a single timezone; user can optionally override in preferences
2. **Platform List is Static:** Hardcoded list (tiktok, instagram, youtube, linkedin) matches existing `platform` enum
3. **Historical Data Sparse Initially:** System gracefully falls back to trending patterns if user has few published items
4. **Offline Recommendation Logic:** No real-time data feed; recommendations computed at request time from snapshot data

### Design Decisions
1. **JSONB Over Dedicated Table:** `preferred_post_hours` stored as JSONB in `brand_configs` for flexibility; easier to add new platforms later
2. **No Database Constraint:** Platform/hours validation in Python (Pydantic + application logic) rather than database constraints
3. **Async Computation:** `compute_posting_recommendation()` is async to allow future DB queries; currently they're not awaited but structure allows it
4. **Confidence Score:** Float 0.0–1.0 allows frontend to vary visual emphasis (high confidence = brighter/bolder)
5. **Data Source Attribution:** Include `data_source` field ("user_preferences", "historical_data", "trending_signals") to explain recommendation basis

---

## Known Gaps & Future Work

1. **A/B Testing:** No tracking of whether users actually post at recommended times; future enhancement could measure conversion
2. **Timezone Handling:** Current implementation treats all as UTC; support for per-platform timezones deferred
3. **Weekday Insights:** Recommendations don't distinguish Monday vs. Friday; future could include day-of-week patterns
4. **External Integrations:** No connection to platform APIs (e.g., TikTok Creator Center analytics); future enhancement
5. **Scheduled Publishing:** No automatic scheduling; UI recommends times but user must publish manually

---

## Files to Create
1. `supabase/migrations/007_posting_hours.sql`
2. `backend/intelligence/posting_recommendations.py`

## Files to Modify
1. `backend/brand/models.py`
2. `backend/brand/router.py`
3. `backend/content/router.py`
4. `frontend/lib/types.ts`
5. `frontend/lib/api.ts`
6. `frontend/app/content/calendar/page.tsx`

## Total Impact
- **Database:** 1 new column
- **Backend:** 2 new endpoints, 1 new module with ~100 lines of logic
- **Frontend:** 3 TypeScript interface updates, 6–8 API method additions, ~15 lines of UI rendering

---

## Success Criteria
- ✅ Users can set preferred posting hours per platform via API
- ✅ Calendar page displays posting time recommendations for each content item
- ✅ Recommendations blend user preferences, historical performance, and trending patterns
- ✅ All changes are backward compatible (recommendations optional; calendar works without them)
- ✅ No breaking changes to existing endpoints
