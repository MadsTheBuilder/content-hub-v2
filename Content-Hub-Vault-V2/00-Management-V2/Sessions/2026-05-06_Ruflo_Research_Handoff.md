---
date: 2026-05-06
type: research-session
topic: ruflo / Claude Code agentic primitives
---

# 2026-05-06 — Ruflo Research Handoff to NotebookLM

## Goal
Heavy research handoff on [[ruvnet/ruflo]] focused on **Claude Code skills, agents (subagents), slash commands, and plugins** — their architecture, differences, and best practices. Outputs requested in 4 formats: PDF (report), slide deck, infographic, mind map.

References: [[Local_First_Skill_Engine_Plan]], [[NotebookLM Automation]]

## What Changed
- Created NotebookLM notebook `Research: ruflo — Skills/Agents/Slash Commands/Plugins` (id `d464de4e-b370-4d41-a875-1bc34f969b32`).
- Seeded with [https://github.com/ruvnet/ruflo](https://github.com/ruvnet/ruflo).
- Kicked off `source add-research --mode deep` covering: ruflo, ruv-FANN, claude-flow, agentic-flow, MCP, skills/agents/slash commands/plugins best practices.
- Deep research returned **109 sources** (45 ready, 64 URL-fetch errors — typical for paywalled/blocked links). The auto-generated synthesis "The Architecture of Autonomous Agency" was imported as a source and seeded the artifact generation.
- Generated 4 artifacts. 3 of 4 succeeded; slide deck hit Google rate limits 3× and was abandoned per `notebooklm` skill guidance ("Audio, video, quiz, flashcards, infographic, and slide deck generation may fail due to Google's rate limits").

## Files Touched

### Research Vault (10-Research)
Created: [[2026-05-06_ruflo_skills_agents_architecture]] — Full structured research: Skills, Agents, Slash Commands, Plugins, MCP comparison matrix, ruflo architecture, ruv-FANN components, mind map, best practices.

### Raw Artifacts (10-Research/2026-05-06_ruflo/)
Created: `report.md` (8.8K) — full NotebookLM briefing doc.
Created: `mindmap.json` (4.2K) — raw hierarchical JSON.
Created: `mindmap.md` — Mermaid-rendered mind map (Obsidian-renderable).
Created: `infographic.png` (4.2M) — portrait, professional style.
Not created: `slides.pdf` — see Open Items.

## Key Findings (from generated report)
References: [[Memory/Research/2026-05-06_ruflo/report.md]]

- **Skills** = procedural SOPs in `.claude/skills/<name>/SKILL.md`. Use for domain-specific knowledge to keep `CLAUDE.md` slim.
- **Agents/Subagents** = isolated context workers in `.claude/agents/`. Built-ins: Explore (Haiku, read-only), Plan, general-purpose (Sonnet). Use for side tasks that would flood main context.
- **Slash commands** = session/context controls. `/init`, `/clear`, `/rewind`, `/agents`, `/plugin`, `/btw`.
- **Plugins** = installable bundles via `/plugin` marketplace; package skills/tools/integrations.
- **ruflo (formerly claude-flow)** = orchestration layer over Claude Code. Self-learning (SONA), 3-tier model routing (~75% API cost reduction claim), AgentDB vector memory, coordinates 100+ specialized agents.
- **MCP** = the connective tissue — JSON-RPC tool registry; LLM-agnostic interface.
- Workflow vs Agent distinction: workflows = predefined paths (predictable), agents = dynamic decision-making (autonomous). Pick by predictability needs.

Modifies: nothing in code. Pure research output.

## Open Items
1. **Slide deck generation failed 3× on rate limit** — task IDs `87c577c6`, `0451c842`, `8b25d99c`. Re-trigger via NotebookLM web UI or rerun `notebooklm generate slide-deck --format detailed -n d464de4e-b370-4d41-a875-1bc34f969b32` after a long cooldown.
2. **PDF of report** — current report is `.md`. If a binary PDF is wanted, run pandoc locally or print-to-PDF in Obsidian.
3. **Mind map visualization** — `mindmap.json` is hierarchical data, not an image. Ingest into a tool like Markmap or Obsidian's mindmap plugin to render.
4. **64 errored research sources** — many would be valuable (Anthropic engineering blog, MCP spec, ruflo USERGUIDE.md). Consider re-adding individually with `source add` if depth needed.
