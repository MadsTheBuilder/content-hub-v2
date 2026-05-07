---
status: Synced
last_sync: "2026-04-09 23:47"
original_path: "CLAUDE.md"
---
# CLAUDE.md

# Content Hub — Claude Code Context

## Obsidian Vault — Session Start Protocol

At the start of every session:
1. Read `Content-Hub-Vault/00-Management/Memory/context.md` for persistent user context
2. Read `Content-Hub-Vault/00-Management/Plans/CLAUDE.md` for project context
3. Follow all rules in `Content-Hub-Vault/00-Management/Plans/AGENTS.md`

## Task Completion Protocol

After completing any significant task (feature, fix, refactor, config change, investigation):
1. Write a session log to `Content-Hub-Vault/00-Management/Sessions/` named `YYYY-MM-DD_Short_Description.md`
2. Use this format:
   ```
   ---
   status: Completed
   date: YYYY-MM-DD
   type: session_summary
   ---
   # Session: <Short Description>
   ## What Was Done
   ## Files Changed
   ## Outstanding
   ```
3. Do this BEFORE giving the final response to the user — the log is part of completing the task, not an afterthought
4. Keep it factual and brief — what changed, which files, what's still open

## What this is
A solo-creator content intelligence engine. Connects to Apify for trend scraping, Gemini for AI scripting, Playwright for slide rendering, and Remotion for video. Single-user MVP — no multi-tenancy needed.

## Stack
- **Frontend**: Next.js 15 (App Router), Tailwind, Framer Motion — port 3003
- **Backend**: FastAPI (Python) — port 8000, proxied via Next.js rewrites
- **Database**: Supabase (PostgreSQL + pgvector + RLS)
- **Storage**: Supabase Storage (`content-hub` bucket)
- **AI**: Google Gemini (via `google-generativeai`) for scripting
- **Scraping**: Apify for TikTok/Instagram/YouTube/LinkedIn trending content
- **Rendering**: Playwright (slides → PNG), Remotion (video — port 3100)

## Current state: ~95% complete

### ✅ Done
- Full backend (FastAPI): `backend/main.py`, auth, workflows, content, brand, research, intelligence, scheduler, storage
- All frontend pages: dashboard, workflows/new, workflows/[id], brand/[workflowId], content/new, content/library, content/[id], content/[id]/edit, content/calendar
- Sidebar with mock-mode banner (`frontend/components/Sidebar.tsx`)
- `frontend/lib/api.ts` — all API methods wired
- `frontend/lib/types.ts` — all TypeScript types
- Supabase project created: `fuvtjsivfngzrmyxeuug` (ap-southeast-1)
- Database migration applied: 9 tables + pgvector + RLS + `match_embeddings` RPC
- Storage bucket `content-hub` created with user-scoped policy
- `.env` updated with SUPABASE_URL + SUPABASE_ANON_KEY

### ⏳ Remaining
See `Content-Hub-Vault/00-Management/Tasks/Current_Sprint.md` for the canonical task list.

## Key architecture decisions (already made, don't re-debate)
- **No `public.users` table** — `auth.users` is the source of truth. `workflows.user_id` and `content_items.user_id` are plain `uuid` columns (no FK constraint). Backend uses service_role key → bypasses RLS entirely.
- **Mock mode** — if Supabase URL is a placeholder, backend falls back to in-memory dicts. The Sidebar shows a mock-mode banner.
- **Single-user MVP** — auth is technically wired but bypassed. Service role key = full access.
- **RAG over NotebookLM** — `content_embeddings` table + `match_embeddings` RPC + `backend/research/rag.py`
- **Few-shot + edit-diff learning** — `content_edit_history` + `content_publication_memory` tables feed the intelligence loop

## Supabase project
- **Project ID**: `fuvtjsivfngzrmyxeuug`
- **URL**: `https://fuvtjsivfngzrmyxeuug.supabase.co`
- **Anon key**: already in `.env`
- **Service role key**: user must add manually (never commit to git)


