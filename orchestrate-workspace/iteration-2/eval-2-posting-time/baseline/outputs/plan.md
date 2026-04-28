# Implementation Plan: Platform-Specific Posting Time Recommendations

## Overview
Implement a feature that recommends optimal posting times for each platform based on historical performance data. The system will:
1. Store preferred posting hours per platform in brand config
2. Compute optimal hours by analyzing when previously published content performed best
3. Surface recommendations on the content calendar page

## Architecture

### Data Model
```
Brand Config (existing table):
├── preferred_post_hours: {
│   "tiktok": [14, 16, 19],    # hours when content typically performs well
│   "instagram": [18, 20, 21],
│   "youtube": [14, 16],
│   "linkedin": [9, 12]
├── posting_time_analysis_confidence: 0.0-1.0
└── last_posting_time_refresh: timestamp

Content Publication Memory (existing table):
├── posted_at_hours: {
│   "tiktok": [14, 15, 14, 19, 16, 18...],  # raw hours when items were posted
│   ...
└── posting_performance_by_hour: {
│   "tiktok": {
│       "14": {views: 45000, avg_engage: 0.082},
│       "16": {views: 52000, avg_engage: 0.095},
│       ...
│   }
}
```

### Three-Layer Implementation

## Phase 1: Brand Config & Database
**Domain**: db-agent, brand-agent
**Files**: 
- New migration: `supabase/migrations/007_posting_time_config.sql`
- Backend models: `backend/brand/models.py`
- Backend router: `backend/brand/router.py`

### Tasks

#### Task 1.1: Create Database Migration
**File**: `supabase/migrations/007_posting_time_config.sql`

```sql
-- Add posting time configuration to brand_configs
alter table public.brand_configs
  add column if not exists preferred_post_hours jsonb default '{"default": []}'::jsonb,
  add column if not exists posting_time_analysis_confidence float default 0.0,
  add column if not exists last_posting_time_refresh timestamptz default null;

-- Extend content_publication_memory to track posting times
alter table public.content_publication_memory
  add column if not exists posted_at_hours jsonb default '{}'::jsonb,
  add column if not exists posting_performance_by_hour jsonb default '{}'::jsonb;

-- Add check constraint for confidence score
alter table public.brand_configs
  add constraint brand_configs_posting_confidence_check
  check (posting_time_analysis_confidence >= 0.0 and posting_time_analysis_confidence <= 1.0);
```

**Verification**:
- Migration applies without errors
- New columns appear in brand_configs and content_publication_memory
- Default values are correct (empty objects/0.0)

---

#### Task 1.2: Extend BrandUpdate Model
**File**: `backend/brand/models.py`

Add fields to BrandUpdate pydantic model:
```python
class BrandUpdate(BaseModel):
    # ... existing fields ...
    preferred_post_hours: Optional[dict[str, list[int]]] = None  # {platform: [hours]}
    posting_time_analysis_confidence: Optional[float] = None
    # DO NOT include last_posting_time_refresh (backend-managed only)
```

**Verification**:
- Model serializes/deserializes without validation errors
- Confidence field rejects values < 0 or > 1
- preferred_post_hours accepts dict of platform → int array

---

#### Task 1.3: Extend Brand Router
**File**: `backend/brand/router.py`

Modify `update_brand()` endpoint to:
- Accept new fields from BrandUpdate
- Validate preferred_post_hours keys are recognized platforms
- Validate hour values are 0-23
- Return updated fields in response

Add new endpoint `GET /{workflow_id}/posting-recommendations` that returns:
```json
{
  "preferred_post_hours": {...},
  "analysis_confidence": 0.75,
  "recommendation_summary": "Based on 12 published posts..."
}
```

**Verification**:
- PUT endpoint accepts preferred_post_hours and stores correctly
- GET endpoint returns current config with confidence score
- Invalid platform names are rejected with 400
- Invalid hours (>23 or <0) are rejected with 400

---

## Phase 2: Intelligence Layer — Posting Time Analysis
**Domain**: intelligence-agent
**Files**:
- New file: `backend/intelligence/posting_optimizer.py`
- Extend: `backend/intelligence/memory.py`
- Extend: `backend/intelligence/suggestions.py`
- Modify: `backend/scheduler/jobs.py`

### Tasks

#### Task 2.1: Create posting_optimizer.py Module
**File**: `backend/intelligence/posting_optimizer.py`

Create core analysis functions:

**Function 1: `extract_posting_hours(workflow_id: str) -> dict[str, list[int]]`**
- Query all published items (status='posted') for this workflow
- Extract hour from `updated_at` (proxy for posting time)
- Group by platform
- Return: `{"tiktok": [14, 19, 14, 15, ...], ...}`

**Function 2: `compute_performance_by_hour(workflow_id: str, platform: str) -> dict`**
- For each published item on this platform, extract posting hour
- Correlate with `content_items.asset_urls` and view/engagement metrics (if available from trends)
- Aggregate per hour: `{"14": {views: 45000, engagements: 3700}, "19": {views: 52000, ...}}`
- Return ranked hours by average engagement rate

**Function 3: `get_top_posting_hours(workflow_id: str, platform: str, top_n: int = 3) -> tuple[list[int], float]`**
- Call `compute_performance_by_hour()`
- Rank hours by engagement metric
- Return top N hours and a confidence score (0-1 based on sample size)
  - Confidence = min(sample_count / 10, 1.0) (needs at least 10 samples for 1.0 confidence)
- Fallback to platform defaults if no data

**Function 4: `refresh_posting_recommendations(workflow_id: str) -> bool`**
- For each platform in workflow.platforms:
  - Call `get_top_posting_hours()`
  - Update brand_configs with results
  - Update posting_time_analysis_confidence
  - Set last_posting_time_refresh = now()
- Log: "Updated posting recommendations for workflow {id}: {platform_count} platforms"
- Return: True if successful

**Verification**:
- extract_posting_hours() correctly parses hours from timestamps
- compute_performance_by_hour() aggregates data correctly (no nulls, correct math)
- get_top_posting_hours() returns 3 hours max, confidence is 0-1
- refresh_posting_recommendations() updates DB and sets timestamp

---

#### Task 2.2: Extend Memory Update on Publish
**File**: `backend/intelligence/memory.py`

Modify `update_publication_memory()` function to also track posting time:

```python
async def update_publication_memory(workflow_id: str, published_item: dict):
    # ... existing code ...
    
    # NEW: Track posting hour
    posted_at_hours = memory.get("posted_at_hours") or {}
    platform = published_item.get("platform", "")
    if platform:
        posting_hour = int(published_item.get("updated_at", "").split("T")[1].split(":")[0])
        if platform not in posted_at_hours:
            posted_at_hours[platform] = []
        posted_at_hours[platform].append(posting_hour)
        posted_at_hours[platform] = posted_at_hours[platform][-100:]  # Keep last 100
    
    # ... update memory with posted_at_hours ...
```

**Verification**:
- Hours are correctly extracted from ISO timestamps
- posted_at_hours array grows correctly
- Array is limited to 100 entries per platform

---

#### Task 2.3: Add Weekly Refresh Job
**File**: `backend/scheduler/jobs.py`

Add new scheduled job:

```python
async def refresh_posting_time_recommendations():
    """Weekly job: Recompute optimal posting hours for all workflows."""
    from backend.intelligence.posting_optimizer import refresh_posting_recommendations
    
    sb = get_supabase()
    workflows = sb.table("workflows").select("id").execute().data or []
    
    for workflow in workflows:
        try:
            await refresh_posting_recommendations(workflow["id"])
        except Exception as e:
            logger.exception("Failed to refresh posting times for workflow %s", workflow["id"])
    
    logger.info("Posting time recommendation refresh complete")

# Register in APScheduler
# scheduler.add_job(
#     refresh_posting_time_recommendations,
#     'cron',
#     day_of_week='sun',
#     hour=6,  # After voice learning (5 AM) and publication memory (5:30 AM)
#     id='refresh-posting-recommendations'
# )
```

**Verification**:
- Job runs without blocking other scheduler tasks
- Handles missing workflows gracefully
- Logs success and failures separately

---

#### Task 2.4: Extend Suggestions with Posting Time
**File**: `backend/intelligence/suggestions.py`

Modify `generate_suggestions()` to include posting time guidance:

```python
# After building each suggestion dict:
# Get recommended posting hours from brand config
brand_config = sb.table("brand_configs").select("preferred_post_hours").eq("workflow_id", workflow_id).single().execute().data
if brand_config and item.get("platform") in brand_config.get("preferred_post_hours", {}):
    suggestion["recommended_posting_hours"] = brand_config["preferred_post_hours"][item["platform"]]
    suggestion["posting_time_note"] = f"Optimal times: {', '.join(map(str, suggestion['recommended_posting_hours']))} (confidence: 0.75)"
```

**Verification**:
- Posting hours are included in suggestion response (when available)
- Works correctly when no posting data exists (graceful fallback)
- Confidence score is included in note

---

## Phase 3: Frontend — Calendar Display
**Domain**: frontend-agent
**Files**:
- Extend: `frontend/lib/types.ts`
- Extend: `frontend/lib/api.ts`
- Extend: `frontend/app/content/calendar/page.tsx`
- New component (optional): `frontend/components/PostingTimeCard.tsx`

### Tasks

#### Task 3.1: Update Types
**File**: `frontend/lib/types.ts`

Add new types:

```typescript
export interface PostingRecommendation {
  platform: string;
  preferred_hours: number[];
  confidence: number; // 0-1
  sample_size: number;
  analysis_summary: string;
}

export interface BrandConfig {
  // ... existing fields ...
  preferred_post_hours?: Record<string, number[]>;
  posting_time_analysis_confidence?: number;
  last_posting_time_refresh?: string;
}
```

**Verification**:
- Types compile without errors
- Interfaces are exported from types.ts

---

#### Task 3.2: Extend API Client
**File**: `frontend/lib/api.ts`

Add to brand API methods:

```typescript
export const brand = {
  get: (workflow_id: string) => fetchAPI(`/brand/${workflow_id}`),
  update: (workflow_id: string, data: Partial<BrandConfig>) =>
    fetchAPI(`/brand/${workflow_id}`, { method: "PUT", body: JSON.stringify(data) }),
  getPostingRecommendations: (workflow_id: string) =>  // NEW
    fetchAPI(`/brand/${workflow_id}/posting-recommendations`),
  // ... existing methods ...
};
```

**Verification**:
- getPostingRecommendations endpoint matches backend URL
- Returns data in expected format
- Error handling works (graceful fallback if endpoint fails)

---

#### Task 3.3: Update Calendar Page
**File**: `frontend/app/content/calendar/page.tsx`

Add posting time recommendations display:

**Change 1: Import and fetch data**
```typescript
import { brand as brandApi } from "@/lib/api";
// ... in useEffect ...
const recs = await brandApi.getPostingRecommendations(workflow_id);
setPostingRecommendations(recs);
```

**Change 2: Add state**
```typescript
const [postingRecommendations, setPostingRecommendations] = useState<Record<string, any> | null>(null);
```

**Change 3: Display above calendar header**
```typescript
{postingRecommendations && (
  <motion.div className="p-4 rounded-lg bg-blue-500/10 border border-blue-500/20 mb-6">
    <p className="text-sm text-blue-300">
      📅 <strong>Posting time tips:</strong> TikTok performs best at {postingRecommendations.preferred_post_hours?.tiktok?.join(":00, ")}.
      (Based on {postingRecommendations.analysis_confidence * 100}% confidence)
    </p>
  </motion.div>
)}
```

**Change 4: Add posting time hint to item cards (optional)**
```typescript
// In the item card, add a hint for next to item's platform badge
{item.platform && postingRecommendations?.preferred_post_hours?.[item.platform] && (
  <span title={`Recommended posting hours: ${postingRecommendations.preferred_post_hours[item.platform].join(":00, ")}`}>
    ⏰
  </span>
)}
```

**Verification**:
- Calendar page loads without errors (recommendations are optional)
- Recommendations display when data exists
- Gracefully handles missing or null recommendations
- Mobile responsive
- No layout shift when recommendations load

---

## Success Criteria

### Phase 1 (Brand Config & DB)
- [ ] Migration applies successfully
- [ ] New columns exist in brand_configs and content_publication_memory
- [ ] BrandUpdate model accepts preferred_post_hours
- [ ] PUT /brand/{id} accepts and stores posting config
- [ ] GET /brand/{id}/posting-recommendations returns correct structure
- [ ] Invalid platforms/hours are rejected with 400

### Phase 2 (Intelligence Layer)
- [ ] posting_optimizer.py exports all 4 functions
- [ ] extract_posting_hours() correctly parses timestamps
- [ ] compute_performance_by_hour() aggregates metrics correctly
- [ ] get_top_posting_hours() returns 3 hours and 0-1 confidence
- [ ] refresh_posting_recommendations() updates DB without errors
- [ ] publication memory tracks posted_at_hours
- [ ] Weekly scheduler job registers and runs
- [ ] Suggestions include posting_time_note when available

### Phase 3 (Frontend)
- [ ] PostingRecommendation and updated BrandConfig types compile
- [ ] API client has getPostingRecommendations() method
- [ ] Calendar page fetches and displays recommendations
- [ ] Works gracefully when recommendations are missing
- [ ] Mobile layout not affected
- [ ] No console errors in browser dev tools

## Testing Strategy

### Unit Tests
- `test_extract_posting_hours()`: Mock content_items with various timestamps
- `test_compute_performance_by_hour()`: Mock engagement metrics and verify aggregation
- `test_get_top_posting_hours()`: Verify confidence scoring with different sample sizes

### Integration Tests
- Full workflow: publish item → update memory → run refresh → check brand config updated
- Frontend load calendar with recommendations → verify display

### Manual Testing
- Publish 5+ items across different hours/platforms
- Run refresh job manually
- Verify brand config updated in Supabase Dashboard
- Open calendar, check recommendations displayed
- Verify responsive on mobile

## Rollback Plan
1. Revert Phase 3 (frontend) — calendar gracefully handles missing recommendations
2. Disable scheduler job in APScheduler
3. Revert Phase 2 (intelligence layer) — suggestions work without posting times
4. Revert Phase 1 (migration) — only if new columns must be removed

## Known Limitations
1. **Historical data**: Only future published content will be analyzed. Existing content will not retroactively populate posting times unless backfill job is added.
2. **Time zone assumptions**: Uses UTC for all timestamps. Platform-local recommendations would require timezone metadata.
3. **Sample size**: Recommendations start appearing after ~5-10 published items per platform.
4. **External factors**: Analysis doesn't account for content quality, topic, hashtags, audience size—only posting hour.

## Dependencies & Ordering
- Phase 1 must complete before Phase 2 (new DB columns needed)
- Phase 2 must complete before Phase 3 (API endpoint must exist)
- Phases can be reviewed/tested in parallel but deployed sequentially

## File Summary
```
supabase/migrations/
  └── 007_posting_time_config.sql (NEW)

backend/brand/
  └── models.py (EXTEND)
  └── router.py (EXTEND)

backend/intelligence/
  ├── posting_optimizer.py (NEW)
  ├── memory.py (EXTEND)
  ├── suggestions.py (EXTEND)
  └── ../scheduler/jobs.py (EXTEND)

frontend/lib/
  ├── types.ts (EXTEND)
  └── api.ts (EXTEND)

frontend/app/
  └── content/calendar/page.tsx (EXTEND)
```

Total: 7 files (3 new, 4 extended) + 1 new component (optional)

---

## Next Steps (Not in Plan)
1. **Backfill existing content**: Create migration to analyze already-posted items
2. **Time zone support**: Add workflow.timezone field and localize recommendations
3. **Advanced analytics**: Consider content quality, topic, audience size in scoring
4. **A/B testing**: Support testing different posting times and automatic recommendation adjustment
5. **User feedback loop**: Let users mark recommendations as "helpful" or "wrong" to refine algorithm
