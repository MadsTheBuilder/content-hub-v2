---
status: Completed
date: 2026-04-29
type: session_summary
---

# Session: YT Pipeline Skill

Implements: [[Chase_AI_System_Breakdown]] Phase 1
References: [[Architecture_Building]] | [[context]]

## What Was Done

Built the `/yt-pipeline` slash command skill — the core research primitive for the Chase AI content system.

Three files created:

- `prompts/yt_pipeline.md` — 8 NotebookLM analysis questions covering: core argument, frameworks, hook patterns, retention techniques, title formulas, content gaps, best quotes, audience desires
- `skills/yt_pipeline.py` — Python helper with two modes: `search` (yt-dlp YouTube search → numbered list) and `run` (create NLM notebook → add sources → wait → ask 8 questions → write vault markdown)
- `.claude/skills/yt-pipeline/SKILL.md` — slash command entry; handles topic-search mode with user URL approval gate, and direct-URL mode with confirmation gate

Smoke tested `search` mode against "AI agents" — returns 10 results with title, channel, views, URL.

Confirmed pre-conditions:
- `notebooklm` importable from main project Python env
- `yt_dlp` importable from main project Python env
- Callaway ingestion already complete — `marketing_brain.md` verified in `Content-Hub-Vault-V2/01-Knowledge/`
- `Content-Hub-Vault-V2/10-Research/` vault folder confirmed present

## Files Changed

- `prompts/yt_pipeline.md` — created
- `skills/yt_pipeline.py` — created
- `.claude/skills/yt-pipeline/SKILL.md` — created

## Outstanding

- `run` mode not live-tested end-to-end (requires NotebookLM auth + real processing time)
- Callaway ingestion step in sprint can now be marked done (marketing_brain.md already covers it)
- Next: Phase 4a `/cascade` or Phase 4b `/short-form` per sprint priority order
