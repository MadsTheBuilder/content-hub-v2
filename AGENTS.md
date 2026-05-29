# Content Hub V2 — Agent Definitions

Specialist agents for V2 (local-first skill engine). When Claude Code delegates work, pick the agent whose domain matches the task. Referenced by [[CLAUDE.md]] § 9 for `/orchestrate` auto-triggering.

V2 is a 7-stage content pipeline: `researcher → ideation → hook → outline → cascade → short-form → voice-cleanup` (+ `title` and `yt-pipeline` as one-shots). Two-layer skill pattern: `.claude/skills/<name>/SKILL.md` (Claude Code entry) + `skills/<name>.py` (helper) + `prompts/<name>.md` (prompt source of truth).

---

## pipeline-agent
**Role:** Core content pipeline specialist
**When to use:** Any work touching the 7 long-form skills — script generation, prompts, AI routing, stage chaining.

**Owns:**
- `skills/researcher.py`, `skills/ideation.py`, `skills/hook.py`, `skills/outline.py`, `skills/cascade.py`, `skills/short_form.py`, `skills/voice_cleanup.py` — the 7 pipeline stages
- `skills/title.py`, `skills/yt_pipeline.py` — one-shot helpers
- `skills/pipeline.py` — chained execution of all 7 stages
- `skills/utils/ai.py` — AI router (Gemini → Ollama → Claude)
- `skills/utils/transcript.py` — YouTube transcript extraction
- `prompts/*.md` — single source of truth for prompt text

**Key contract:** Each stage reads from the previous stage's vault output folder and writes to its own. `skills/utils/ai.py` is the only place model providers are selected — never call Anthropic / Gemini / Ollama SDKs directly from a stage skill.

**Cost-aware routing:** Ollama (free) for drafts → Claude (paid) for polish and hooks. Gemini still available where wired (research).

**Tools needed:** Read, Edit, Bash (`python -m skills.<name>`)

---

## research-agent
**Role:** Research + trend discovery specialist
**When to use:** Work on trending repo scraping, NotebookLM research, or the brief assembly that feeds `/researcher`.

**Owns:**
- `scripts/github_trending.py` — daily GitHub AI trending pull, writes to `Content-Hub-Vault-V2/04-Trends/github_trending.md`
- `bin/run_github_trending.bat` — Windows Task Scheduler entry point
- `skills/researcher.py` — primary research brief assembly
- `skills/researcher_crawler.py` — repo deep-dive crawler
- `skills/research_plan.py`, `skills/research_sources.py` — plan + source curation helpers
- `notebooklm-py/` — programmatic NotebookLM access (one-shot extractions + ad-hoc deep research)

**Key facts:**
- Trend file at `Content-Hub-Vault-V2/04-Trends/github_trending.md` is step 1 of every `/researcher` run.
- NotebookLM: one question at a time (batching causes failures); always go deep into cited sources, not just the surface response.
- Per-repo deep dives land in `Content-Hub-Vault-V2/04-Trends/<owner>_<repo>/`.

**Tools needed:** Read, Edit, Bash (`python scripts/github_trending.py`)

---

## webapp-agent
**Role:** Design-doc webapp specialist (React + FastAPI shell)
**When to use:** UI work on the webapp wrapper that surfaces the 7-stage pipeline — pages, stage workspaces, server endpoints.

**Owns:**
- `Design-doc/web/src/` — React frontend (JSX + components, including `StageWorkspace.jsx`)
- `Design-doc/server/` — Python server layer (FastAPI; aiofiles + python-multipart)
- Stage routing: each pipeline stage gets an InputZone + OutputZone + workspace tab

**Key rules:**
- Stage outputs are read directly from the V2 vault folders (`04-Trends/`, `05-Hooks/`, etc.), not from a database.
- Trends workspace is read-only (`OutputZone` always shows `MarkdownViewer`; `InputZone` shows read-only notice).
- FastAPI + uvicorn + starlette in `requirements.txt` exist for this webapp — do not strip them.

**Tools needed:** Read, Edit, Bash (`npm run dev` / `uvicorn`)

---

## app-agent
**Role:** Control room and entry-point specialist
**When to use:** Work on the local launchers, vault index, or `.bat` shells.

**Owns:**
- `app/control_room.py` — main launcher dispatching to skills and scripts
- `app/runner.py` — pipeline runner
- `app/vault_index.py` — vault index helper
- `bin/run_control_room.bat`, `bin/run_github_trending.bat` — Windows shells
- `scripts/` — one-off scripts callable from control_room

**Key rules:**
- Path constants in `app/` and `scripts/` use `Path(__file__).resolve().parent.parent` to climb up to project root (these files live one level deep).
- Subprocess calls in `control_room.py` reference `scripts/github_trending.py` — keep paths consistent if files move.

**Tools needed:** Read, Edit, Bash

---

## vault-agent
**Role:** Vault knowledge graph specialist
**When to use:** Session logs, sprint task updates, vault structure, graphify rebuilds, anything in `Content-Hub-Vault-V2/00-Management-V2/`.

**Owns:**
- `Content-Hub-Vault-V2/00-Management-V2/Memory/` — persistent project context (`context.md`, etc.)
- `Content-Hub-Vault-V2/00-Management-V2/Sessions/` — session logs (mandatory `[[WikiLinks]]` + semantic edges)
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/` — `Current_Sprint.md`, `Architecture_Building.md`, `Webapp_sprint.md`
- `Content-Hub-Vault-V2/00-Management-V2/Plans/` — `Local_First_Skill_Engine_Plan.md`, this CLAUDE.md
- `Content-Hub-Vault-V2/00-Management-V2/Orchestrations/` — state files for `/orchestrate` runs
- `graphify-out/` — knowledge graph artefacts; regenerate via `/graphify --update`
- `.claude/skills/*/SKILL.md` — slash-command entry points

**Key rules:**
- Every significant task ends with a session log at `Sessions/YYYY-MM-DD_Short_Description.md` written BEFORE the final response (per [[CLAUDE.md]] § 7).
- Logs MUST use explicit `[[WikiLinks]]` and semantic edges (`Implements:`, `References:`, `Modifies:`).
- Rebuild graphify-out after structural changes — `GRAPH_REPORT.md` is read at every session start.

**Tools needed:** Read, Edit, Write

---

## Routing notes for /orchestrate

- Single-skill or single-file work → act directly, do not orchestrate.
- Two-domain work (e.g. add a new pipeline stage + webapp tab + vault session log) → orchestrate across `pipeline-agent` + `webapp-agent` + `vault-agent`.
- Source of truth for orchestrated execution: `Content-Hub-Vault-V2/00-Management-V2/Superpowers/orchestrated-execution.md` (overrides skill files if they conflict).
