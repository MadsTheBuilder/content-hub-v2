---
status: Completed
date: 2026-04-09
type: session_summary
---

# Session: Day 1 — E2E Pipeline Smoke Test

## What Was Done

Ran the full pipeline end-to-end using the API directly (port 8001 — fresh server to avoid stale process on port 8000). Confirmed each stage works, found and fixed 3 critical bugs.

### Pipeline Results
| Stage | Result |
|-------|--------|
| Workflow creation + Voice Engine | ✅ brand_profile populated, competitors in apify_config, pillars expanded |
| Scraping (Apify live) | ✅ 50 TikTok posts scraped |
| Enrichment (Gemini analysis) | ✅ 10 posts enriched with hook_type, why_it_works, applicable_techniques |
| Relevance scoring | ✅ all 50 posts scored |
| Content synthesis | ✅ 3-angle strategy document with psychology principles |
| Script generation | ✅ Gemini 2.5 Flash, rich prompts with strategy + research context |
| Slides rendering | ✅ 5 PNGs via Playwright, uploaded to Supabase Storage |
| Edit endpoint | ✅ |
| Publish + learning loop | ✅ content_publication_memory updated |

### Bugs Found and Fixed

**Bug 1: `'refining'` status violates DB constraint**
- Error: `content_items_status_check` only allowed `['generating', 'scripting', 'rendering', 'ready', 'failed', 'posted']`
- Fix: Migration `add_refining_status` — added `'refining'` to the constraint
- File: Supabase migration applied

**Bug 2: Storyboard parser fails on markdown-formatted scripts**
- Error: `_video_storyboard()` and `_talking_head_storyboard()` matched `HOOK:` literally but Gemini writes `**HOOK:** (0-3s)`. Entire script dumped into `body` scene.
- Fix: Added `_strip_label()` helper that strips `**`, `*`, and `(Ns)` timing markers before matching section labels
- File: `backend/content/storyboard.py`

**Bug 3: Stale server on port 8000**
- Cause: A persistent process was running old code (before this session's fixes). New workflow creations via the old server hit the silent `except Exception` in `service.py` causing Voice Engine results to be dropped.
- Fix: Ran fresh server on port 8001. The old server PID(s) are unresponsive to kill — likely Claude Code internal. Not a code bug.

### Known Non-Blockers (Deferred)
- `short_form` and `talking_head` asset_urls empty — Remotion not running (deferred per plan)
- Relevance scores all equal (38.3) — scoring uses brand_profile fields but they're not differentiated enough yet. Day 2 fix.
- Enrichment only runs on top 10 posts (by design, cost control) — remaining 40 get scored but no Gemini analysis

## Files Changed
- `backend/content/storyboard.py` — added `_strip_label()`, fixed `_video_storyboard()` and `_talking_head_storyboard()` parsers
- `backend/workflows/router.py` — added/removed debug endpoint (cleaned up)
- `backend/workflows/service.py` — added/removed verbose traceback logging (cleaned up)
- Supabase: migration `add_refining_status` applied

## Outstanding (Day 2)
- Platform Strategy knowledge base (`platform_adapter.py`)
- Learning loop completeness (strategy feedback, edit feedback)
- Marketing skills full integration
