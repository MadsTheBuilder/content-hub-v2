---
date: 2026-05-14
type: session-log
description: "Integration of obsidian-mind lifecycle hooks into Content Hub V2 — auto context injection, PreCompact transcript backup, § 7 stop checklist, and Content Hub-specific classify signals."
tags: [hooks, obsidian-mind, context-management, session-tracking]
---

# Session: Obsidian Mind Integration

## What Changed

Integrated [obsidian-mind](https://github.com/breferrari/obsidian-mind) lifecycle hooks into Content Hub V2's `.claude/` setup. This replaces the manual § 6 session-start ceremony with automated context injection.

## Files Touched

- `.claude/settings.json` — Added 5 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, PreCompact, Stop)
- `.claude/scripts/` — Copied obsidian-mind's TypeScript hook scripts (zero runtime deps, runs via `node --experimental-strip-types`)
- `.claude/scripts/session-start.ts` — **Adapted** for Content Hub V2 vault paths: loads `context.md`, god nodes, `Current_Sprint.md` instead of obsidian-mind's `brain/` structure
- `.claude/scripts/lib/signals.ts` — **Replaced** generic corporate signals with Content Hub V2-specific routing: GOD NODE WARNING, SKILL BUILD, SPRINT UPDATE, CONTENT PIPELINE, GRAPH UPDATE
- `.claude/scripts/stop-checklist.ts` — **Adapted** checklist to § 7 requirements (session log, sprint update, wikilinks)
- `.claude/commands/` — Added all obsidian-mind slash commands (`/om-standup`, `/om-dump`, `/om-wrap-up`, etc.)
- `thinking/session-logs/` — Created for PreCompact transcript backups

## What Each Hook Does

| Hook | Trigger | Effect |
|------|---------|--------|
| SessionStart | startup/resume/clear/compact | Injects: date, context.md excerpt, god nodes, current sprint, git changes |
| UserPromptSubmit | every message | Classifies message against 7 Content Hub signals, injects routing hints |
| PostToolUse | Write/Edit | Validates markdown frontmatter + wikilinks in vault notes |
| PreCompact | before compaction | Backs up transcript JSONL to `thinking/session-logs/` (30-file retention) |
| Stop | session end | Shows § 7 checklist: session log, sprint update, wikilinks |

## Why

obsidian-mind solves the "AI forgets between sessions" problem with structured hooks that automate what was previously manual (§ 6 reads, § 7 session logs). Key benefits:
- Session context auto-injected — no manual file reads at start
- PreCompact backup — no more lost context on `/compact`
- Stop hook enforces § 7 discipline without relying on memory
- Classify hook catches when decisions/architecture/god-node edits need documenting

Implements: [[Local-First Skill Engine Build Plan]]
Modifies: [[Content Hub V2 Claude Code Context]] (settings.json)
References: [[2026-05-14_Graphify_Update]], [[Current Sprint]]
