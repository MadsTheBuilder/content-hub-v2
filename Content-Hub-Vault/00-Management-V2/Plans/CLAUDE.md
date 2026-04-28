---
status: Active
created: "2026-04-28"
description: "Claude Code project context for Content Hub V2 — local-first skill engine."
---

# CLAUDE.md — Content Hub V2

> Active project: `C:\Users\madhu\Claude cowork\Content Hub V2\`
> Vault management: `Content-Hub-Vault/00-Management-V2/`
> V1 (`Content Hub/`) is parked as SaaS reservation. Do not edit V1 unless explicitly asked.

## Session Start Protocol (V2)

1. Read [[context]] (`00-Management-V2/Memory/context.md`) — project context.
2. Read this file (`00-Management-V2/Plans/CLAUDE.md`) — project rules.
3. Read [[Local_First_Skill_Engine_Plan]] (`00-Management-V2/Plans/`) — full build plan.
4. Read [[Current_Sprint]] (`00-Management-V2/Tasks/`) — what to do next.
5. Plan before acting — ask 1–3 focused questions if anything is ambiguous, then wait.

## Task Completion Protocol

After completing any significant V2 task:
1. Write a session log to `00-Management-V2/Sessions/` named `YYYY-MM-DD_Short_Description.md`.
2. Use the standard frontmatter format:
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
3. Use explicit `[[WikiLinks]]` for any V2 component, prior session, or architecture node.
4. Edges: `Implements: [[X]]`, `References: [[Y]]`, `Modifies: [[Z]]`.
5. Write the log **before** the final response to the user.

## What V2 Is

A local-first content production engine. 7 Claude Code slash-commands, each backed by a Python helper + a single-source-of-truth prompt file. Produces 9 deliverables per long-form. No Remotion. No frontend. Vault-first output.

## Stack (V2)

- **Runtime**: Python 3.x (existing `requirements.txt`), Claude Code as the UI
- **Local model**: Ollama (default `llama3.2` or `mistral`) — first drafts
- **Premium model**: Claude (Anthropic SDK) — hooks, titles, polish
- **Backup model**: Gemini (already wired in `backend/research/research_service.py`)
- **Knowledge**: `notebooklm-py` (cloned at `notebooklm-py/`) for one-shot extractions
- **Vault**: `Content-Hub-Vault/` — output target for every skill
- **Trending**: existing `backend/research/apify_client.py` + APScheduler job

## Key Architecture Decisions (V2)

- **Two-layer skill pattern**: `.claude/skills/<name>/SKILL.md` (Claude entry) + `skills/<name>.py` (Python helper) + `prompts/<name>.md` (durable prompt).
- **Cost-aware routing**: Ollama for drafts, Claude for polish. Don't burn premium tokens on outline structure.
- **Stop at the script**: Chase AI rule — humans own filming + editing. Skills produce text; no auto-render.
- **Distribution-first build order**: cascade + short-form + voice-cleanup ship before researcher/hook/outline/title because they multiply existing footage.
- **Prompts are durable**: when SaaS resumes (V1), `prompts/{name}.md` ports as-is into FastAPI endpoints.

## Vault Knowledge Graph — Memory System

The vault is the persistent graph brain shared across V1 and V2. After every significant V2 task:
1. Write a session log → `00-Management-V2/Sessions/`
2. Use `[[WikiLinks]]` for components, sessions, decisions
3. Update `00-Management-V2/Tasks/Current_Sprint.md` to reflect progress

## Project Knowledge Map (V2)

| What | Where |
|---|---|
| Project context, stack, decisions | [[context]] (`00-Management-V2/Memory/`) |
| Full build plan | [[Local_First_Skill_Engine_Plan]] (`00-Management-V2/Plans/`) |
| Active sprint | [[Current_Sprint]] (`00-Management-V2/Tasks/`) |
| V2 session history | `00-Management-V2/Sessions/` |
| V1 (parked) reference | `00-Management/` |
| V1 pivot decision | [[2026-04-28_V2_Pivot_Local_First_Engine]] |

## Out of Scope for V2

- Next.js frontend (lives in V1 for SaaS resume)
- Remotion / Playwright rendering (dropped permanently from local-first)
- A/B experiments framework (kept available, not wired)
- ComfyUI image generation (deferred to v2 of V2)
- Auto-publishing to YouTube/Twitter/LinkedIn (manual copy-paste)
