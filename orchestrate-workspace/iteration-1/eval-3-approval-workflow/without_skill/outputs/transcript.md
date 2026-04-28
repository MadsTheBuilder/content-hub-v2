# Content Approval Workflow — Planning Session Transcript

**Date:** 2026-04-22  
**Task:** Create plan for adding content approval workflow (no code changes)  
**Model:** Claude Haiku 4.5  

---

## Session Steps

### Step 1: Read Project Context Files
**Tools Used:** `Read` (3 calls)

Read the following files to understand project structure and conventions:
- `C:\Users\madhu\Claude cowork\Content Hub\CLAUDE.md` — Project guidelines and guardrails
- `Content-Hub-Vault/00-Management/Plans/CLAUDE.md` — Stack, architecture, DB config
- `Content-Hub-Vault/00-Management/Memory/context.md` — User context and current state

**Key Findings:**
- Stack: FastAPI (port 8000) + Next.js 15 (port 3003) + Supabase PostgreSQL
- Project status: ~95% complete, Phase 3 refinement underway
- Database uses 9 tables + pgvector for RAG
- No multi-user auth needed (single-user MVP, service role bypass for admin ops)
- Convention: plain uuid columns for user_id (no FK to public.users), RLS policies exist

### Step 2: Locate Backend Python Files
**Tools Used:** `Glob` (1 call)

Searched for all Python backend files using pattern `backend/**/*.py`

**Key Files Identified:**
- Content router: `backend/content/router.py` (existing endpoints)
- Content models: `backend/content/models.py` (Pydantic request/response models)
- Database module: `backend/database.py`
- Authentication: `backend/auth/` (dependencies, router)
- Main app: `backend/main.py`

### Step 3: Locate Frontend TypeScript Files
**Tools Used:** `Glob` (1 call)

Searched for all TypeScript frontend files using pattern `frontend/**/*.ts*`

**Key Files Identified:**
- Content detail page: `frontend/app/content/[id]/page.tsx` (where UI changes needed)
- Content library: `frontend/app/content/library/page.tsx` (optional filter enhancement)
- API client: `frontend/lib/api.ts` (all HTTP calls)
- Types: `frontend/lib/types.ts` (TypeScript interfaces)

### Step 4: Examine Backend Content Router
**Tools Used:** `Read` (1 call, full file)

Read `backend/content/router.py` (403 lines):

**Current Endpoints:**
- `POST /content/generate` — Trigger content generation
- `POST /content/synthesize` — Create strategy from trending posts
- `POST /content/generate-from-strategy` — Generate from approved strategy
- `POST /content/revise-strategy` — Re-generate with rejection notes
- `POST /content/{id}/regenerate` — Re-trigger generation for existing item
- `GET /content/library` — List content items (with filters)
- `GET /content/calendar` — Get all content items for calendar view
- `GET /content/status/{id}` — Get generation status
- `GET /content/{id}` — Get single item details
- `GET /content/{id}/download` — Download asset URLs
- `PUT /content/{id}/edit` — Edit script with diff tracking
- `PUT /content/{id}/publish` — Mark as posted and update embeddings
- `DELETE /content/{id}` — Delete with cleanup
- `GET /content/{id}/edit-history` — Get all edits

**Current Model Structure:** Content items have `status` field with values: generating, scripting, rendering, ready, failed, posted

**Publishing Logic (Line 335-358):** 
- Updates status to "posted"
- Stores published_script
- Calls update_publication_memory for learning loop
- Embeds for RAG
- **No approval check exists**

### Step 5: Examine Backend Content Models
**Tools Used:** `Read` (1 call, full file)

Read `backend/content/models.py` (36 lines):

**Current Models:**
- `ContentGenerateRequest` — topic-based generation
- `ContentEditRequest` — script edit
- `SynthesizeRequest` — strategy from posts
- `StrategyGenerateRequest` — generate from strategy
- `ReviseStrategyRequest` — revise strategy with notes

**Analysis:** Models are Pydantic, simple and minimal. New models for approval will follow same pattern.

### Step 6: Examine Frontend Types
**Tools Used:** `Read` (1 call, partial)

Read `frontend/lib/types.ts` (first 40 lines):

**Current ContentItem Interface (Lines 23-40):**
```typescript
export interface ContentItem {
  id: string;
  workflow_id: string;
  user_id: string;
  content_type: "slides" | "topic" | "short_form" | "talking_head";
  platform: string;
  title: string;
  script_text: string;
  published_script: string | null;
  storyboard: Record<string, unknown> | null;
  asset_urls: string[];
  status: "generating" | "scripting" | "refining" | "rendering" | "ready" | "failed" | "posted";
  rejection_flag: boolean;
  generation_metadata: Record<string, unknown>;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}
```

**Analysis:** No approval_status field currently. rejection_flag is boolean but not used for approval workflow.

### Step 7: Examine Frontend Content Detail Page
**Tools Used:** `Read` (1 call, full file)

Read `frontend/app/content/[id]/page.tsx` (267 lines):

**Current UI Elements:**
- Status badge (shows generation status: ready, posted, generating, etc.)
- Publish button (enabled when status !== "posted")
- Download button
- Edit button
- Regenerate button (visible only when status === "ready")
- Delete button
- Asset display section

**Current Handlers:**
- `handlePublish()` — Calls API, updates status to "posted"
- `handleDownload()` — Opens download URLs
- `handleDelete()` — Confirms and deletes
- `handleRegenerate()` — Prompts for notes, re-runs generation

**Analysis:** Button visibility is status-dependent. Will add approval status badge and approve/reject buttons following same pattern.

### Step 8: Examine Frontend API Client
**Tools Used:** `Read` (2 calls, partial)

Read `frontend/lib/api.ts` (lines 1-129):

**API Client Structure:**
- `fetchAPI()` helper — Common fetch with token, error handling
- `auth` object — signup, login, logout, me
- `workflows` object — CRUD + scrape + trending + suggestions
- `content` object (lines 101-129) — Covers all content operations

**Current Content Methods:**
- `generate()`, `status()`, `get()`, `library()`, `calendar()`
- `download()`, `edit()`, `publish()`, `delete()`, `editHistory()`
- `synthesize()`, `generateFromStrategy()`, `reviseStrategy()`, `regenerate()`

**Analysis:** Will add `approve()` method following same pattern (fetchAPI with PUT method).

### Step 9: Check Database Migrations
**Tools Used:** `Bash` (1 call)

Located migration files:
- `001_initial_schema.sql` — Core 9 tables + RLS + pgvector
- `002_multimodal_embeddings.sql` — Slide image embeddings
- `003_evolution_columns.sql` — Schema updates
- `004_memory_rpc.sql` — Learning system RPC
- `005_phase3_brand_fields.sql` — Brand customization fields
- `006_ab_experiments.sql` — A/B testing table

### Step 10: Examine Initial Schema Migration
**Tools Used:** `Read` (1 call, partial)

Read `Content-Hub-Vault/supabase/migrations/001_initial_schema.sql.md` (first 65 lines):

**Content Items Table Structure (Lines 44-64):**
```sql
create table public.content_items (
    id uuid primary key default gen_random_uuid(),
    workflow_id uuid not null references public.workflows(id) on delete cascade,
    user_id uuid not null,
    content_type text not null check (content_type in (...)),
    platform text not null,
    title text default '',
    script_text text default '',
    published_script text default null,
    storyboard jsonb default null,
    asset_urls jsonb default '[]'::jsonb,
    status text not null default 'generating' check (status in ('generating', 'scripting', 'rendering', 'ready', 'failed', 'posted')),
    rejection_flag boolean default false,
    generation_metadata jsonb default '{}'::jsonb,
    error_message text default null,
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);
```

**Analysis:** Will add `approval_status` column (similar to status but separate concern) and `approval_notes` column in new migration.

### Step 11: Verify Output Directory
**Tools Used:** `Bash` (2 calls)

Created output directory:
- Confirmed path: `C:\Users\madhu\Claude cowork\Content Hub\orchestrate-workspace\iteration-1\eval-3-approval-workflow\without_skill\outputs`

---

## Key Architectural Insights

### Design Decision: Two Independent State Machines

The current `status` field tracks **generation pipeline state**:
```
generating → scripting → refining → rendering → ready → [posted or failed]
```

The new `approval_status` field will track **governance state** (independent):
```
draft → [pending →] approved OR rejected
```

These are **orthogonal**:
- A content item can be `status="ready"` (generation complete) and `approval_status="rejected"` (approval failed)
- Publishing will require `status="ready"` AND `approval_status="approved"`

### Why Not Use rejection_flag?

The existing `rejection_flag` is a boolean and doesn't capture:
1. Rejection vs approval (only negative)
2. Pending state (under review)
3. Audit trail (when rejected, by whom, why)

The new field is richer and enables approval workflows.

### API Endpoint Design

New endpoint: `PUT /content/{id}/approve`
- Input: `{decision: "approved"|"rejected", notes?: string}`
- Output: `{content_id, approval_status, notes, timestamp}`
- Permission: User can only approve own content
- Precondition: `status` must be "ready" (generation complete)
- Side Effect: Log decision to audit table

Existing `PUT /content/{id}/publish` will enforce check:
```python
if item["approval_status"] != "approved":
    raise HTTPException(403, "Content must be approved before publishing")
```

### Database Schema

Two new entities:
1. **Columns on content_items:**
   - `approval_status TEXT (draft|pending|approved|rejected)` — main state
   - `approval_notes TEXT NULL` — reviewer feedback
   
2. **New table content_approval_log:**
   - Audit trail of all approval decisions
   - Enables compliance, rollback analysis, decision history
   - Soft delete safety (preserve logs even if content deleted)

---

## Changes by Component

### Backend (Python/FastAPI)
1. **Database:** New migration file (007)
2. **Models:** 2 new Pydantic models (ApproveContentRequest, ApprovalResponse)
3. **Router:** 1 new endpoint + 1 modified endpoint

### Frontend (Next.js/TypeScript)
1. **Types:** 2 new fields in ContentItem interface
2. **API:** 1 new method in content object
3. **UI:** Updated content detail page with approval status badge and buttons

### Database (Supabase/PostgreSQL)
1. 2 new columns on content_items table
2. 1 new table (content_approval_log) with RLS policy
3. 2 new indexes for performance

---

## Files Affected (Summary)

| # | File | Changes | Type |
|---|------|---------|------|
| 1 | `supabase/migrations/007_approval_workflow.sql` | Create | New migration |
| 2 | `backend/content/models.py` | Add 2 models | Code |
| 3 | `backend/content/router.py` | Add 1 endpoint, modify 1 | Code |
| 4 | `frontend/lib/types.ts` | Add 2 fields | Type def |
| 5 | `frontend/lib/api.ts` | Add 1 method | Code |
| 6 | `frontend/app/content/[id]/page.tsx` | Add UI + handlers | Code |
| 7 | `frontend/app/content/library/page.tsx` | Add filter (optional) | Code |

---

## Testing Requirements (Outline)

### Backend Tests (pytest)
- Approval endpoint validates user ownership
- Approval only allowed when status="ready"
- Publish endpoint enforces approval_status="approved"
- Audit log records all decisions
- Rejection notes persist

### Frontend Tests (vitest)
- Approve/reject buttons visible only when status="ready"
- Clicking approve shows confirmation dialog
- Rejection button shows optional notes input
- Publishing blocked if not approved (403 error handling)

### Manual E2E Flow
1. Generate content → status:ready, approval_status:draft
2. View detail page → see "Approve" button
3. Click "Approve" → approval_status:approved
4. Click "Publish" → succeeds, status:posted
5. Verify: Cannot publish without approval

---

## Tool Usage Summary

| Tool | Count | Purpose |
|------|-------|---------|
| Read | 8 | Explore project context, code files, migrations |
| Glob | 2 | Locate Python and TypeScript files |
| Bash | 2 | Verify output directory, list migrations |
| Write | 2 | Create plan.md and this transcript |

**Total Tool Calls:** 14

---

## Next Steps (For Implementation, Not in Scope)

1. **Create migration:** Run `007_approval_workflow.sql` against Supabase
2. **Add backend models:** Update `backend/content/models.py`
3. **Add endpoint:** Update `backend/content/router.py`
4. **Update types:** Update `frontend/lib/types.ts`
5. **Add API method:** Update `frontend/lib/api.ts`
6. **Update UI:** Update `frontend/app/content/[id]/page.tsx`
7. **Test:** Run backend + frontend test suites
8. **Manual verification:** E2E flow testing
9. **Commit & Deploy:** Create PR to main branch

---

## Clarifications & Assumptions

### Assumptions Made (No Ambiguity Found)
1. **Approval Required for Publishing:** Publishing without approval_status="approved" returns 403
2. **Single Decision:** Approve button = one-click approval, Reject button = one-click with optional notes
3. **No Role-Based Access:** Single user MVP — users can only approve own content
4. **No Undo:** Approval decision is permanent (can regenerate and re-approve if needed)
5. **Backward Compatibility:** Existing items default to approval_status="draft" (non-blocking)

### Design Clarity (Confirmed)
- **approval_status vs status:** Two independent state machines ✓
- **Audit Trail:** Essential for compliance, new table recommended ✓
- **Publishing Gate:** Enforce at router level ✓
- **UI Pattern:** Follow existing button/badge patterns ✓

---

## Completion Status

**Planning:** ✓ Complete  
**File Exploration:** ✓ Complete  
**Transcript:** ✓ Complete  
**Plan Document:** ✓ Complete  

**Code Changes:** Not in scope (planning only)  
**Testing:** Not in scope (planning only)  
**Deployment:** Not in scope (planning only)

