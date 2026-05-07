---
date: 2026-04-29
type: session-log
---

# Vault Separation Fix

Implements: [[Vault Knowledge Graph]]
Modifies: [[CLAUDE.md]], [[Memory System]]

## What changed

- Root cause: Claude's memory incorrectly pointed to V1 vault (`Content Hub\Content-Hub-Vault`) as the write target. Every session log, sprint update, and knowledge file was being written there — invisible in the user's Obsidian which opened the V2 vault.
- Reconciled the two diverged `00-Management-V2/` copies (V1-vault vs V2-repo), pulling newer V1 files into V2-repo.
- Deleted V1-vault's stale `00-Management-V2/` stub — V2 is now the single home.
- Removed stray `01-Knowledge/marketing_brain.md` that was written to V1 vault by a prior session.
- User renamed `Content-Hub-Vault/` → `Content-Hub-Vault-V2/` in File Explorer for clarity.
- Updated all `Content-Hub-Vault/` path references in [[CLAUDE.md]] → `Content-Hub-Vault-V2/`.
- Updated auto-memory to record correct V2 vault path.

## Files touched

- `CLAUDE.md` — all vault paths updated
- `.claude/projects/.../memory/feedback_vault_reference.md` — corrected vault path + rule
- `Content-Hub-Vault-V2/00-Management-V2/Sessions/` — reconciled missing sessions from V1

## Open items

- User needs to update the Obsidian vault entry to point at `Content-Hub-Vault-V2` (folder was renamed)
- Remove the stale "00-Management-V2" vault entry from Obsidian vault switcher
