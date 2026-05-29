---
status: Completed
date: 2026-05-22
type: session_summary
description: "Added autoCompactEnabled + autoCompactWindow to project settings.json."
tags: [session, settings, config]
---

# Session: Auto-Compact Settings

Modifies: [[.claude/settings.json]]
References: [[Current_Sprint]]

## What Was Done

Added two keys to `.claude/settings.json` (project-scoped, applies to all sessions):

```json
"autoCompactEnabled": true,
"autoCompactWindow": 100000
```

- `autoCompactEnabled` — turns on automatic context compaction
- `autoCompactWindow: 100000` — triggers at 100k tokens (schema minimum; ~50% of a 200k context window)

## Files Changed

- `.claude/settings.json` — 2 keys added

## Outstanding

None. Takes effect from the next session start.
