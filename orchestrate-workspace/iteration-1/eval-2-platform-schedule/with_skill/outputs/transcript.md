# Orchestration Transcript — Platform-Specific Posting Time Recommendations

## Session Start (2026-04-22)

**Model**: Haiku 4.5  
**Task**: Implement platform-specific posting time recommendations  
**Goal**: Store preferred_post_hours per platform in brand config, compute optimal hours using intelligence layer based on historical performance, surface recommendations on content calendar

---

## Phase 1: Recon

### Step 1: Announce
"I'm using orchestrated-execution to decompose and dispatch this task."

### Step 2: Load Workflow
- Read: `/SKILL.md` (orchestrate skill definition)
- Read: `/Superpowers/orchestrated-execution.md` (authoritative 6-phase workflow)
- Read: `/Plans/AGENTS.md` (specialist agent definitions)

**Workflow confirmed**: 6-phase process with state file recovery mechanism.

### Step 3: Scan Codebase

#### Brand Config Layer
- **File**: `backend/brand/models.py`
  - Current fields: primary_color, secondary_color, accent_color, font_family, logo_url, watermark_enabled, watermark_text, custom_font, slide_template, transition_style, reference_creators
  - Missing: preferred_post_hours (per-platform time slots)
  - Structure: Pydantic BaseModel (BrandUpdate)
  
- **File**: `backend/brand/router.py`
  - GET/PUT endpoints for brand config
  - Uses Supabase service_role key
  - Updates brand_configs table directly

- **Database**: `supabase/migrations/005_phase3_brand_fields.sql`
  - brand_configs table has: custom_font, slide_template, transition_style, reference_creators
  - Need to add: preferred_post_hours (JSONB field mapping platform → hours array)

#### Intelligence Layer
- **Files**: 
  - `backend/intelligence/memory.py` — publication memory tracking
  - `backend/intelligence/suggestions.py` — daily suggestions (trending posts ranked by user preferences)
  - `backend/intelligence/triggers.py` — trend spike detection
  - `backend/scheduler/jobs.py` — APScheduler job registration

- **Current patterns**:
  - Publication memory already tracks: published_count, content_type_distribution, hook_styles, topics_published, platform_content_map
  - Suggestions engine already ranks by user preferences (hook style, content style)
  - No time-based learning loop yet (only content + voice + trends)

- **Historical data availability**:
  - content_items table has: platform, status (including "posted"), created_at, updated_at
  - content_publication_memory has: platform_content_map (which platform → content_type)
  - Could derive: publish times from posted items if updated_at is used as proxy

#### Frontend Calendar
- **File**: `frontend/app/content/calendar/page.tsx`
  - Currently displays: items grouped by month, sorted newest-first
  - Status badges: generating, scripting, rendering, ready, failed, posted
  - Uses `content.calendar()` API endpoint
  - Platform + content_type displayed as badges

- **API Interface**: `frontend/lib/api.ts`
  - `content.calendar()` endpoint exists → must return items list
  - Brand API: `brand.get(workflowId)` and `brand.update(workflowId, data)`
  - No existing endpoint for posting time recommendations

- **Types**: `frontend/lib/types.ts`
  - BrandConfig interface: includes all current brand fields
  - Missing: preferred_post_hours field
  - Suggestion interface exists but doesn't have posting time data

#### Database Schema
- **Tables relevant to task**:
  - brand_configs: stores all brand settings (need to add preferred_post_hours JSONB)
  - content_items: has platform, status, created_at, updated_at (historical data source)
  - content_publication_memory: has platform_content_map (platform preferences)

---

## Recon Findings Summary

### 1. Brand Config Integration Point
- **Location**: backend/brand/models.py (Pydantic) + supabase schema
- **Current state**: Color, font, watermark, template, transition settings exist
- **Gap**: No preferred_post_hours field
- **Required change**: Add JSONB field mapping platform → time slots (e.g., { "LinkedIn": [9, 17], "Twitter": [14, 19] })

### 2. Intelligence Layer Computation Point
- **Location**: backend/intelligence/ (memory.py + suggestions.py)
- **Current pattern**: Learning loops track publication choices + trends
- **Gap**: No time-based learning (engagement_at_time_of_post not tracked)
- **Required change**: New function to analyze historical publish times + engagement → optimal hours per platform

### 3. Historical Performance Data Source
- **Available**: content_items table with platform + status + timestamps
- **Challenge**: Need to correlate publish time → engagement (but trending_content has organic_score, not tied to publish time)
- **Strategy**: Could compute from published items' timestamps OR derive recommendations based on platform norms

### 4. Calendar UI Integration Point
- **Location**: frontend/app/content/calendar/page.tsx
- **Current rendering**: Month groups with content items + status badges
- **Gap**: No posting time recommendations displayed
- **Required change**: Fetch recommended hours from brand config + display as inline hint or tooltip

### 5. File Ownership (Domain Assignment)
- **Brand Config**: brand-agent (backend/brand/*)
- **Intelligence Computation**: intelligence-agent (backend/intelligence/*)
- **Database Schema**: db-agent (supabase/migrations/*)
- **Frontend UI**: frontend-agent (frontend/app/content/*)
- **API Types**: frontend-agent (frontend/lib/types.ts)

---

## Key Dependencies
1. **Database migration** must run before backend can store/fetch preferred_post_hours
2. **Brand config model** must be updated before router can handle new field
3. **Intelligence function** can read from brand config but also needs to compute dynamically
4. **Frontend types** must be updated before calendar page can display recommendations
5. **Calendar page** should fetch brand config + display recommendations alongside items

---

## No blockers identified. Ready for Phase 2 decomposition.
