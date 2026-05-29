---
date: 2026-05-26
tags: [graphify, stale, knowledge-graph]
description: "Graphify graph marked stale after 2026-05-26 cleanup; rebuild via /graphify --update."
---

# Graph Report — STALE (needs rebuild)

**Status:** Stale as of 2026-05-26. The previous graph indexed ~1,634 nodes including ~50+ now-removed paths (`backend/*`, `skills/twitter_*`, root V1 scripts, `models/tribev2/*`, `free-claude-code/*`, agent worktrees, etc.).

**To rebuild:** run `/graphify --update` from project root. The incremental update prunes ghost nodes for deleted files and only re-extracts new/changed files (the May 26 reorg moved scripts into `app/`, `bin/`, `scripts/`).

**Why this wasn't done automatically:** `/graphify --update` dispatches multiple semantic-extraction subagents and is best run interactively when the user is present to confirm corpus scope and review community labels.

**What's safe to read until then:**
- `Content-Hub-Vault-V2/00-Management-V2/Memory/context.md` — project context
- `Content-Hub-Vault-V2/00-Management-V2/Plans/CLAUDE.md` — V2 rules and stack
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md` — active sprint
- `AGENTS.md` — current V2 agent → file mappings (rewritten 2026-05-26)

References: [[2026-05-26_Cleanup_Verification]], [[2026-05-26_8GB_Shed_Cleanup]]
