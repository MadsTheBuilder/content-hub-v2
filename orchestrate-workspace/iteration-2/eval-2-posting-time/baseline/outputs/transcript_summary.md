# Transcript Summary: Posting Time Recommendations Planning

## Date
2026-04-22

## Task
Implement platform-specific posting time recommendations. Store preferred_post_hours per platform in brand config, compute optimal hours using the intelligence layer based on historical performance data, and surface recommendations on the content calendar page.

## Context Gathering Phase

### 1. Project Architecture Review
- Read `CLAUDE.md` (main guidelines)
- Read `Content-Hub-Vault/00-Management/Memory/context.md` (user context)
- Read `Content-Hub-Vault/00-Management/Plans/CLAUDE.md` (project state)
- Reviewed graph report to understand core abstractions
- Reviewed `AGENTS.md` to understand domain specialization

### 2. Database Schema Analysis
- Examined `supabase/migrations/001_initial_schema.sql` - 9 tables including:
  - `brand_configs` (exists, has visual properties but no posting time fields)
  - `content_publication_memory` (exists, tracks published content metadata)
  - `content_items` (exists, tracks generated/published content)
  - `trending_content` (exists, tracks organic performance)
- Reviewed `005_phase3_brand_fields.sql` - shows recent brand config extensions

### 3. Backend Layer Analysis
- **Brand Module**: `backend/brand/models.py` and `backend/brand/router.py`
  - Currently handles visual identity (colors, fonts, logos, watermarks)
  - BrandUpdate model has no posting time fields
  - GET/PUT endpoints for brand config exist
- **Intelligence Layer**: `backend/intelligence/`
  - `suggestions.py`: Generates personalized content suggestions with memory-based scoring
  - `memory.py`: Tracks publication metrics (content type, hook styles, topics)
  - No existing posting time analysis
- **Content Router**: Has calendar endpoint (`/calendar`) and status endpoints
- **Scheduler**: `backend/scheduler/jobs.py` manages APScheduler jobs

### 4. Frontend Layer Analysis
- Calendar page at `frontend/app/content/calendar/page.tsx`
  - Groups content by month, shows status badges
  - No posting time recommendations currently displayed
- API client at `frontend/lib/api.ts` has:
  - Brand GET/PUT endpoints
  - Calendar endpoint
  - Suggestions endpoint
- Types at `frontend/lib/types.ts`:
  - BrandConfig interface exists
  - No PostingRecommendation type currently defined

### 5. Key Architectural Observations
- **Service role bypass pattern**: Backend uses service role to write to trending_content
- **Memory-based learning**: Publication memory (content_publication_memory table) already tracks metrics
- **No existing time analysis**: No code analyzes when content was posted vs. performance
- **API-first design**: All updates flow through typed endpoints
- **Separation of concerns**: Brand config, intelligence, and content generation are distinct modules

## Key Decisions Made
1. **No schema changes needed**: Can store `preferred_post_hours` as JSONB in brand_configs (existing table)
2. **Intelligence layer ownership**: Posting time analysis belongs in `backend/intelligence/` not brand module
3. **Recommendations pattern**: Follow existing suggestions.py pattern for computing and ranking
4. **Frontend display**: Calendar page is ideal location for recommendations (shows scheduled content)
5. **Data source**: trending_content table already has timestamps; can correlate with organic_score
6. **Learning loop integration**: Tie posting time learning to publication memory refresh schedule

## Constraints & Tradeoffs
- **Historical data limitation**: Only recommendations from newly captured trends will have posting times
- **Platform variance**: Different platforms have different optimal posting times (TikTok vs LinkedIn)
- **Sample size**: Need sufficient volume of published items to detect patterns
- **User education**: Users must understand these are probabilistic recommendations, not guarantees

## Plan Outline (See detailed plan.md)
The implementation spans three major phases:
1. **Database & Brand Config** (db-agent + brand-agent)
2. **Intelligence Layer** (intelligence-agent)
3. **Frontend UI** (frontend-agent)

Each phase has clear entry/exit criteria and is independently testable.

## Tools & References Used
- Glob for file pattern matching
- Grep for code search
- Read for file examination
- AGENTS.md for domain definitions
- graph report for architecture verification
