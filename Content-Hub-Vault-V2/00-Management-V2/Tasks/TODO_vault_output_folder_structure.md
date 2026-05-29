---
date: 2026-05-27
tags: [todo, refactor, vault, voice-cleanup, cascade]
status: pending
priority: medium
description: "Refactor cascade and voice-cleanup output paths so raw AI drafts land in raw/ and cleaned publish-ready files land in cleaned/ subfolders inside each distribution slug."
---

# TODO — Separate Raw and Cleaned Output Folders

## Problem

Raw `/cascade` output and `/voice-cleanup` output currently land in the same distribution folder, mixed together:

```
08-Distribution/2026-05-27_<slug>/
  blog_post.md          ← raw AI output
  blog_post_cleaned.md  ← voice-cleaned version
  twitter_thread.md
  twitter_thread_cleaned.md
  linkedin_post.md
  linkedin_post_cleaned.md
```

This makes it unclear which file is publish-ready when browsing the vault in Obsidian.

## Desired State

```
08-Distribution/2026-05-27_<slug>/
  raw/
    blog_post.md
    twitter_thread.md
    linkedin_post.md
  cleaned/
    blog_post.md
    twitter_thread.md
    linkedin_post.md
```

`cleaned/` = publish candidate. `raw/` = AI draft kept for reference.

## Files to Change

- [ ] [[cascade|skills/cascade.py]] — write output to `<slug>/raw/` instead of `<slug>/`
- [ ] [[voice_cleanup|skills/voice_cleanup.py]] — write cleaned output to `<slug>/cleaned/<original_filename>` instead of `<slug>/<stem>_cleaned.md`
- [ ] `.claude/skills/cascade/SKILL.md` — update documented output paths
- [ ] `.claude/skills/voice-cleanup/SKILL.md` — update documented output paths
- [ ] `app/vault_index.py` — check if any listing functions need updating for new subfolder paths
- [ ] `server/vault.py` (web app) — check if output resolvers are path-sensitive

## Notes

- The `--inplace` flag in voice_cleanup.py should still work as-is (overwrites the file in place wherever it is)
- Existing vault folders (pre-change) won't be migrated — they stay as-is
- Related memory: [[project_vault_output_folder_structure]]
