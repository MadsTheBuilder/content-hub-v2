---
date: 2026-05-29
tags: [session, cascade, voice-cleanup, vault]
description: "Baked voice cleanup into /cascade so only polished content lands in the vault."
---

# Session — Cascade: Vault-Only Clean Output

Implements: [[project_vault_output_folder_structure]]
Modifies: [[skills/cascade.py]], [[.claude/skills/cascade/SKILL.md]]

## What changed

`skills/cascade.py` now runs voice cleanup on all three generated pieces (blog, Instagram, LinkedIn) before writing anything to `08-Distribution/`. Raw AI drafts are never persisted to disk.

Two helpers added:
- `_load_voice_cleanup_template()` — reads `prompts/voice_cleanup.md` once per run
- `_voice_clean(text, template)` — calls `polish()` with the cleanup prompt; falls back to raw text if the model call fails (with a logged warning)

Voice cleanup runs sequentially after all three generation calls succeed and before `make_output_dir()` is called. The `README.md` checklist now reads "voice-cleaned, ready to publish".

## Files touched

- `skills/cascade.py` — added `polish` import, two helper functions, three cleanup calls, README copy update
- `.claude/skills/cascade/SKILL.md` — updated description and "Things to know" to document built-in cleanup

## Open items

- `/voice-cleanup` standalone skill still works for one-off file cleanup — no changes needed there.
- The `raw/` + `cleaned/` subfolder design from [[project_vault_output_folder_structure]] is superseded by this approach: no raw files means no need for the split. Memory record should be updated to reflect the final design.
