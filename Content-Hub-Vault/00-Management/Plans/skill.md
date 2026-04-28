# Content Hub — Skills Reference

## check-db
**When to use:** Before any DB-related work. Verify tables exist and RLS is correct.

```bash
# In Claude Code, run these to check the DB state:
# 1. List tables via Supabase MCP → list_tables (project: fuvtjsivfngzrmyxeuug)
# 2. Check migration status → list_migrations
# 3. Expected tables: workflows, content_items, trending_content, content_triggers,
#    content_style_profiles, content_edit_history, brand_configs,
#    content_publication_memory, content_embeddings
```

**Quick sanity:** If any of the 9 tables are missing, re-apply `supabase/migrations/001_initial_schema.sql` via Supabase MCP → apply_migration.

---

## boot
**When to use:** Starting the full dev stack.

```bash
# Terminal 1 — Backend (from Content Hub root)
# Cwd: c:\Users\madhu\Claude cowork\Content Hub
uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend
# Cwd: c:\Users\madhu\Claude cowork\Content Hub\frontend
npm run dev   # port 3003

# Terminal 3 — Remotion (only needed for short_form video)
# Cwd: c:\Users\madhu\Claude cowork\Content Hub\remotion
npm start     # port 3100
```

**Check mock vs live:** Backend logs `MOCK MODE` or `LIVE MODE` on startup. If mock mode, add SUPABASE_SERVICE_ROLE_KEY to `.env`.

---

## test-generation
**When to use:** End-to-end smoke test after any backend change.

```
1. POST /api/v1/workflows → create "Test Fitness" workflow
2. POST /api/v1/content/generate → {workflow_id, content_type: "slides", platform: "linkedin", topic: "3 training principles"}
3. Poll GET /api/v1/content/status/{id} until status = "ready"
4. GET /api/v1/content/{id} → verify asset_urls populated
5. PUT /api/v1/content/{id}/publish → verify content_publication_memory updated
```

Expected pipeline states: `generating → scripting → rendering → ready`

---

## fix-rendering
**When to use:** Slides not rendering / PNG files missing.

```bash
# Install Playwright browsers (one-time)
# Cwd: c:\Users\madhu\Claude cowork\Content Hub
playwright install chromium

# Check Supabase Storage bucket exists
# → Supabase MCP → execute_sql: SELECT * FROM storage.buckets WHERE id = 'content-hub';
# If missing: create via Supabase dashboard → Storage → New bucket → 'content-hub' (public)
```

**Storyboard→renderer contract:** Frame dicts must have `bg_gradient`, `accent_color`, `headline`, `body`, `slide_number`. If slides are blank, check `backend/content/storyboard.py` output matches `backend/content/renderer_slides.py` expectations.

---

## evolve-claude-md
**When to use:** After completing a significant feature or fixing a major bug.

1. Read current `CLAUDE.md`
2. Update the `✅ Done` section with what was completed
3. Update the `⏳ Remaining` section — remove done items, add new blockers
4. Update any architecture decisions that changed
5. Never add speculative content — only facts about the current state

---

## add-content-type
**When to use:** Adding a new content type (e.g., newsletter, thread).

Files to touch (in order):
1. `backend/content/models.py` → add to `ContentType` enum
2. `backend/content/scripting.py` → add prompt template for the type
3. `backend/content/storyboard.py` → add `_new_type_storyboard()` function
4. `backend/content/router.py` → add elif branch in `_run_generation()`
5. `frontend/app/content/new/page.tsx` → add to content type selector
6. Update `CLAUDE.md` to reflect the new type

---

## learning-cycle
**When to use:** Debugging why the intelligence layer isn't improving output.

```
Loop A: Publication memory → backend/intelligence/memory.py → update_publication_memory()
Loop B: Voice learning   → backend/intelligence/memory.py → weekly edit diff analysis
Loop C: Trend detection  → backend/intelligence/triggers.py → detect_trend_spikes()

Check: GET /api/v1/workflows/{id}/suggestions → should return 3 suggestions
Check: content_publication_memory table → published_count should increment on publish
```

---

## model-cascade
**When to use:** Scripting fails or produces poor output.

Cascade order (defined in `backend/content/scripting.py`):
1. Gemini 2.0 Flash (Google AI Studio key)
2. Gemini 1.5 Pro (fallback)
3. Claude Sonnet (Anthropic key)
4. Placeholder script (never blocks pipeline)

If Gemini fails: check `GOOGLE_AI_STUDIO_KEY` in `.env`. Test: `python3 -c "import google.generativeai as genai; genai.configure(api_key='KEY'); [print(m.name) for m in genai.list_models()]"`
