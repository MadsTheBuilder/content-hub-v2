---
status: Synced
last_sync: "2026-04-09 17:56"
original_path: "AGENTS.md"
---
# AGENTS.md

# Content Hub — Agent Definitions

These are the specialist agents for Content Hub. When Claude Code delegates work, it should pick the right agent based on the task scope.

---

## pipeline-agent
**Role:** Content generation pipeline specialist
**When to use:** Any work touching the generation pipeline — scripting, storyboard, rendering, or the pipeline orchestration in `router.py`.

**Owns:**
- `backend/content/scripting.py` — LLM cascade, prompt construction, model fallback
- `backend/content/storyboard.py` — script → frame dict conversion
- `backend/content/renderer_slides.py` — Playwright PNG rendering
- `backend/content/renderer_video.py` — Remotion MP4 rendering
- `backend/content/renderer_talking_head.py` — ZIP packaging
- `backend/content/router.py` — generation endpoint + background task

**Key contract:** Storyboard frames must always include `bg_gradient`, `accent_color`, `headline`, `body`, `slide_number`. If you change the frame schema, update both storyboard.py AND the renderer.

**Tools needed:** Read, Edit, Bash (to test rendering)

---

## research-agent
**Role:** Research layer and RAG specialist
**When to use:** Work on trending content scraping, embedding, retrieval, or the research brief assembly.

**Owns:**
- `backend/research/apify_client.py` — Apify actor runs + polling
- `backend/research/organic_score.py` — view × retention scoring
- `backend/research/rag.py` — embed_and_store, similarity search, weekly refresh
- `backend/research/research_service.py` — ResearchBrief assembly (RAG + trending + memory → narrative)

**Key facts:**
- Embedding model: `text-embedding-004` (Gemini), 768 dimensions
- pgvector search via `match_embeddings` RPC in Supabase
- Mock mode: `sb.rpc()` returns empty result — don't mistake mock silence for failure

**Tools needed:** Read, Edit, Bash (to test embedding calls)

---

## intelligence-agent
**Role:** Learning system and suggestions specialist
**When to use:** Work on the three learning loops (publication memory, voice learning, trend detection) or the daily suggestions engine.

**Owns:**
- `backend/intelligence/memory.py` — Loop A (publication memory) + Loop B (voice learning)
- `backend/intelligence/triggers.py` — Loop C (trend spike detection)
- `backend/intelligence/suggestions.py` — daily 3-suggestion generator
- `backend/intelligence/rejection.py` — suggestion rejection tracking
- `backend/scheduler/jobs.py` — APScheduler cron job registration

**Learning loop cadence:**
- Continuous: publication memory (on every publish)
- Daily 6 AM: trend detection → content_triggers
- Weekly Sunday 5 AM: voice learning (edit diffs → style profile)
- Weekly Sunday 5:30 AM: batch publication memory refresh

**Tools needed:** Read, Edit

---

## frontend-agent
**Role:** Next.js frontend specialist
**When to use:** Any UI work — pages, components, API wiring, styling.

**Owns:**
- `frontend/app/` — all pages
- `frontend/components/` — Sidebar and UI components
- `frontend/lib/api.ts` — API client (all fetch calls)
- `frontend/lib/types.ts` — TypeScript types

**Key rules:**
- Port 3003 (`npm run dev` in `frontend/`)
- Dark theme: bg `#0F172A`, accent `#C9A96E`, borders `#334155`
- All API calls go through `frontend/lib/api.ts` — never raw fetch in page components
- Framer Motion for animations — single `<motion.div key={step}>` wrapper per animated section; don't nest motion divs or exits deadlock
- `useEffect` deps must be accurate — don't put `router` in deps if the effect doesn't use router state

**Tools needed:** Read, Edit, Bash (npm run dev)

---

## db-agent
**Role:** Supabase schema and RLS specialist
**When to use:** Schema changes, new tables, RLS policy changes, migrations.

**Owns:**
- `supabase/migrations/001_initial_schema.sql` — canonical schema
- All Supabase MCP operations

**Key rules:**
- `workflows.user_id` and `content_items.user_id` are plain `uuid` — NO FK to auth.users (dropped to avoid FK violations with dummy user)
- Service role key bypasses RLS — backend writes use service role
- `trending_content` and `content_embeddings` have SELECT-only RLS policies (service role writes, frontend reads)
- All other tables have ALL (CRUD) policies scoped to `auth.uid() = user_id`
- pgvector extension must be enabled; `match_embeddings` RPC must exist
- Supabase project: `fuvtjsivfngzrmyxeuug` (ap-southeast-1)

**Tools needed:** Supabase MCP tools, Read, Edit

---

## brand-agent
**Role:** Brand config and visual identity specialist
**When to use:** Brand config API, brand colours flowing into rendered content, watermark logic.

**Owns:**
- `backend/brand/router.py` — GET/PUT brand config endpoints
- `backend/brand/models.py` — BrandConfig Pydantic model

**Key contract:** Brand colours must flow through the pipeline:
```
brand_configs table → router.py fetches brand → storyboard.py uses secondary_color + primary_color
→ renderer_slides.py injects bg_gradient + accent_color into HTML → PNG output
```
If slides look wrong (wrong colours, missing watermark), trace this chain from DB to render.

**Tools needed:** Read, Edit

---

## Protocol: General Superpowers
**Role:** Instructional Agentic Workflows
**When to use:** Whenever an agent is tasked with building new features, planning, debugging, or using subagents.

**Key rules:**
- Agents MUST read the relevant skill from `Content-Hub-Vault/00-Management/Superpowers/` before attempting complex actions.
- Utilize the `using-git-worktrees` skill for any branching/development features (the physical `.git` repository might be cleaned up or repurposed to accommodate this).
- Use `writing-plans` for detailed breakdown of work.
- Use `subagent-driven-development` and `dispatching-parallel-agents` when delegating tasks.
