---
date: 2026-05-26
tags: [verification, cleanup, audit, dangling-deps]
description: "Independent audit of the 8GB Shed Cleanup and GitHub Trending Restore sessions. All claimed changes verified. 8 categories of overlooked V1 references still on disk."
---

# Cleanup Verification — 8GB Shed + GitHub Trending Restore

Independent post-hoc audit of [[2026-05-26_8GB_Shed_Cleanup]] and [[2026-05-26_Github_Trending_Restore]]. Goal: confirm every claim in those logs against current disk state, and find dependencies the cleanup may have missed.

## Verification of Claimed Work — All Pass

| Claim | Verified |
|---|---|
| Storage bombs gone: `.venv-tribe/`, `models/tribev2/`, `.venv-py314-backup-20260522/` | ✅ |
| Orphaned dirs gone: `free-claude-code/`, `thinking/`, `tmp_marketingskills/`, `scratch/`, `graphs/`, `archive/`, `cache/`, `output/`, `tools/`, `orchestrate-workspace/` | ✅ |
| Tool dirs gone: `.claude-flow/`, `.hive-mind/`, `.swarm/`, `.agents/`, `.agent/`, `.claire/`, `.gsd/`, `.bg-shell/`, `claude-flow.config.json` | ✅ |
| Root V1 scripts gone (10 files: apify_live_test, checkpoint, copy_skills, debug_browser, push_trends_telegram, research_vault_optimization, setup_safe_hands, smoke_test, sync_vault, undo_changes) | ✅ |
| Test files + excalidraw + logs + run.py + daily.py gone | ✅ |
| `backend/` gone | ✅ |
| Vault V1 folders gone: `Code-Brain/`, `backend/`, `frontend/`, `supabase/`, `00-Management/` | ✅ |
| Twitter removal: `skills/twitter_scout.py`, `skills/twitter_scorer.py`, `.claude/skills/twitter-scout/` gone | ✅ |
| `skills/utils/ai.py` fix: `from backend.config` replaced with `os.getenv` + `load_dotenv` | ✅ (lines 17-30) |
| `github_trending.py` restored | ✅ |
| `run_github_trending.bat` restored | ✅ |
| `github_trending.py` OUTPUT now points at V2 vault | ✅ (line 22) |
| Pipeline skills present (15) + prompts (10) + .claude skills (16) | ✅ |
| Zero `from backend.` imports in live `.py` tree | ✅ (only matches: orchestration logs + the cleanup session log itself) |

## Overlooked Dependencies — Still Tied to V2 But Reference Removed V1

Found 8 categories. Listed in priority order.

### 1. AGENTS.md — entirely V1-stale (HIGHEST)

Every one of the 4 agent definitions points at `backend/...` files that no longer exist:
- `pipeline-agent` owns `backend/content/{scripting,storyboard,renderer_slides,renderer_video,renderer_talking_head,router}.py` — all gone
- `research-agent` owns `backend/research/{apify_client,organic_score,rag,research_service}.py` — all gone
- `intelligence-agent` owns `backend/intelligence/{memory,triggers,suggestions,rejection}.py` + `backend/scheduler/jobs.py` — all gone
- Brand section references `backend/brand/router.py`, `backend/brand/models.py`, `supabase/migrations/001_initial_schema.sql` — all gone

`AGENTS.md` is referenced by [[CLAUDE.md]] § 9 (orchestration auto-trigger uses "specialist domains from AGENTS.md"). Currently it dispatches to ghosts. Needs full rewrite mapping to V2 skills/, or deletion.

### 2. requirements.txt — orphaned V1 packages

Removable (no live consumer in V2):
- `apify_client==1.8.1`, `apify_shared==2.2.0` — Twitter/scraping (twitter_scout removed)
- `supabase==2.10.0`, `supabase-auth==2.28.0`, `supabase-functions==2.28.0`, `supafunc==0.7.0`, `gotrue==2.12.4`, `postgrest==0.18.0`, `realtime==2.5.3`, `storage3==0.9.0` — V1 SaaS DB stack
- `APScheduler==3.10.4` — V1 scheduling (`backend/scheduler/`)
- `gspread==5.12.0`, `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib` — V1 Sheets integration
- `aiosqlite==0.22.1` — V1 local DB

KEEP (still used):
- `fastapi`, `uvicorn`, `starlette`, `python-multipart`, `aiofiles` — confirmed in use by Design-doc webapp (line 146 comment)
- `anthropic`, `google-genai`, `notebooklm-py`, `playwright`, `streamlit`, `httpx`, `dotenv`, `pydantic` — pipeline + skills

### 3. .env — V1 credentials with no live consumer

- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_JWT_SECRET` — nothing in V2 reads these
- Apify section header still present (cleanup removed `APIFY_API_KEY` references but kept the section)

KEEP (still used): `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` (per session log decision), `GOOGLE_AI_STUDIO_KEY`, `NVIDIA_NIM_API_KEY` (`ai.py`), `ANTHROPIC_API_KEY`, `GITHUB_TOKEN` (`github_trending.py`).

### 4. .env.example — placeholder for removed Apify

Line 9: `APIFY_API_KEY=your-apify-api-key` — no live consumer.

### 5. graphify-out/ — 84 MB stale knowledge graph

`manifest.json` (1634 entries) still indexes ~50+ removed files: every deleted root script, `backend/research/apify_client.py`, `free-claude-code/*`, `models/tribev2/*`, `skills/twitter_scout.py`, `skills/twitter_scorer.py`, `scripts/twitter_scheduler.py`, etc.

Per [[CLAUDE.md]] § 6 step 3, every session start tells me to read `GRAPH_REPORT.md` — but it's currently mapping a graph that includes dead nodes. Needs a `graphify --update` rebuild.

### 6. .claude/worktrees/ — 395 MB of agent snapshots

Five agent worktree clones (`agent-a02c8c…`, `agent-a226d2…`, `agent-a574f5…`, `agent-ab89b6…`, `agent-af3ead…`) each containing full copies of removed `backend/`, `skills/twitter_scout.py`, `skills/twitter_scorer.py`, `scripts/twitter_scheduler.py`. Harness ephemeral state from past orchestration runs. Not part of the live pipeline, but ~395 MB of reclaimable space the cleanup did not touch.

### 7. .claude/settings.json — stale Read permissions

Lines 14-15: `"Read(backend/__pycache__/**)"`, `"Read(backend/.venv/**)"` — permissions for a directory that no longer exists. Harmless, but stale.

### 8. .gitignore — moot rule

Line 17: `.venv-tribe/` — entry still present, harmless (no longer matches anything).

## Recommended Order of Cleanup

1. **AGENTS.md** — rewrite or delete (affects orchestration routing now)
2. **graphify rebuild** — refreshes the session-start brain
3. **.env / .env.example** — strip V1 secrets
4. **requirements.txt** — strip V1 packages (test pipeline after)
5. **.claude/worktrees/** — reclaim 395 MB if no active orchestration depends on them
6. **.claude/settings.json + .gitignore** — drop cosmetic stale lines

---

References: [[2026-05-26_8GB_Shed_Cleanup]], [[2026-05-26_Github_Trending_Restore]], [[CLAUDE.md]]
Modifies: (read-only audit — no files changed)
