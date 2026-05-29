---
status: Active
last_updated: "2026-04-28"
description: "Master project context for Content Hub V2 — local-first skill engine. Loaded at every session start."
---

# Project Context: Content Hub V2 (Local-First Skill Engine)

## What V2 Is

A **local-first content production engine** that lives at `C:\Users\madhu\Claude cowork\Content Hub V2\`. Modeled on Chase AI's 10M-views workflow. Stops at the script — no automated rendering. Produces **9 deliverables per long-form** via 7 Claude Code slash-commands.

V2 is a **fork** of V1 (the SaaS-stack project at `C:\Users\madhu\Claude cowork\Content Hub\`). V1 is parked. V2 is where all active work happens. Decision logged in [[2026-04-28_V2_Pivot_Local_First_Engine]] (V1 vault).

## Current State — 2026-04-28

**Phase 0 (Cleanup) — not yet started.** V2 currently contains a full clone of V1 and needs SaaS layers stripped before build can begin.

See [[Current_Sprint]] for the live task list.

## Architecture (V2)

Two-layer skill pattern, repeated 7 times:

```
.claude/skills/<name>/SKILL.md   ← Claude Code entry point (/<name> trigger)
skills/<name>.py                 ← Python helper, calls model(s), writes to vault
prompts/<name>.md                ← Single source of truth for prompt text
```

**Cost-aware model routing:**
- **Ollama (local, free)** — first-draft outlines, structural work
- **Claude (paid)** — hooks, titles, voice cleanup, final-30-second polish
- **Gemini** — kept available for any tool that already wires it (research_service.py)

**Knowledge layer:**
- `notebooklm-py` (already cloned in V2) — programmatic NotebookLM access for one-shot Callaway masterclass extraction + ad-hoc deep research
- `Content-Hub-Vault/` (this vault) — human-facing workspace and skill output target
- pgvector RAG (`backend/research/rag.py`) kept available, deprioritized in v1

## The 7 Skills

| # | Skill | Output | Model | Priority |
|---|---|---|---|---|
| 1 | `/researcher` | 5 video ideas → `vault/10-Research/` | notebooklm-py (`add_url` + `research.start` + `chat.ask`) | Phase 4 |
| 2 | `/hook` | 3 hooks → `vault/05-Hooks/` | Ollama draft → Claude polish | Phase 4 (blocked on masterclass) |
| 3 | `/outline` | Section plan → `vault/06-Outlines/` | Ollama draft → Claude polish | Phase 4 |
| 4 | `/title` | 5 Tier-1 + 5 Tier-2 → `vault/07-Titles/` | Pure Claude | Phase 4 |
| 5 | `/cascade` | blog + thread + 3 LinkedIn → `vault/08-Distribution/` | Ollama → Claude | **Phase 3 (highest ROI)** |
| 6 | `/short-form` | 3 vertical scripts → `vault/09-Shorts/` | Claude | **Phase 3 (highest ROI)** |
| 7 | `/voice-cleanup` | Cleaned text | Claude | Phase 3 |

## Critical Decisions (V2)

- **`/researcher` uses notebooklm-py as the web research layer** — trend URLs (GitHub repos, etc.) are added as notebook sources via `add_url`. `research.start` discovers related YouTube videos, blog posts, articles and auto-imports them. `chat.ask` surfaces content gaps. Output is a markdown research brief in `vault/10-Research/`. Gemini is no longer the research driver for this skill. Auth: Google OAuth via Playwright (`~/.notebooklm/storage_state.json`).

- **Stop at the script** — Chase AI playbook: don't automate the part the human's craft owns. No Remotion, no auto-render.
- **Distribution-first build order** — Phase 3 (cascade + short-form + voice-cleanup) ships before Phase 4 (researcher + hook + outline + title) because cascading existing footage delivers value week 1.
- **Prompts are the durable artifact** — when SaaS resumes (in V1), `POST /api/v1/skills/{name}` loads `prompts/{name}.md` and runs the same logic. The two-layer pattern is what makes V2 SaaS-portable later.
- **One vault, two projects** — V1 and V2 share `Content-Hub-Vault/`. V1 management lives in `00-Management/` (parked); V2 management lives in `00-Management-V2/` (active).

## V2 Strip List (planned for Phase 0)

To delete from V2:
- `frontend/`, `remotion-service/`, `supabase/`
- `backend/content/renderer_*.py`, `backend/content/storyboard.py`
- `backend/experiments/` (or move to `archive/` for prompt patterns)
- `frontend/__tests__/`, `tmp/video-bug-report.md`, `tmp/video-notes.md`

To keep in V2:
- `backend/research/` (apify_client, research_service, rag)
- `backend/intelligence/` (synthesis, memory)
- `backend/prompts/skills/` (15 marketing prompts)
- `backend/storage/`, `backend/auth/`, `backend/workflows/`, `backend/brand/`
- `notebooklm-py/`
- `extract_video_knowledge.py` (template for Callaway extractor)
- `.claude/skills/` (existing 6 workflow skills)
- `Content-Hub-Vault/`, `requirements.txt`, `.env`, `pytest.ini`

## Open Inputs (you provide at execution time)

1. **Callaway channel link + 10 specific video URLs** — needed for masterclass extraction (blocks `/hook` and `/outline`).
2. **Voice profile seed** — first version of `Content-Hub-Vault/01-Knowledge/voice_profile.md`. Hand-written initially (10–20 lines on tone/voice/banned phrases).
3. **Ollama model preference** — default `llama3.2` or `mistral`. Confirm what's pulled.
4. **ComfyUI** — deferred to v2 of V2. v1 cascade outputs text only.

## Recent Milestones

- **2026-04-28:** ⚡ V2 fork begins. Plan approved. Phase 0 cleanup queued. See [[2026-04-28_V2_Pivot_Local_First_Engine]] (in V1 sessions folder).

---
[[Current_Sprint]] | [[Local_First_Skill_Engine_Plan]] | [[frontend/README]] (V2 management) | V1 parked: `00-Management/Memory/context.md`
