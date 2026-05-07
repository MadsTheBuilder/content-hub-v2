---
date: 2026-05-07
tags: [session, phase3c, title-skill, orchestration]
---

# Session: Phase 3c — Title Skill

Implements: [[Title Skill]]
Orchestration: [[2026-05-07_phase3c-title-skill]]
References: [[Local_First_Skill_Engine_Plan]]

## What changed

Built the `/title` skill end-to-end via orchestrated execution (4 tasks, 3 groups).

### Files created
- `scripts/scrape_competitor_titles.py` — one-off scraper that calls `apify_client.scrape_profiles()` for @nateherk and @Chase-H-AI; writes top-60 videos to `skills/data/competitor_titles.json`
- `skills/data/competitor_titles.json` — 40 entries (20 per channel), `{title, view_count, channel}`, sorted by view_count desc
- `prompts/title.md` — prompt template with `{competitor_titles}` and `{concept}` placeholders; output: 5 Tier-1 (cite competitor pattern) + 5 Tier-2 (A/B risk) + thumbnail text
- `skills/title.py` — runtime module; reads JSON top-30, substitutes into prompt, calls `claude -p -` via subprocess, writes vault file
- `.claude/skills/title/SKILL.md` — Claude Code skill definition for `/title [concept]`

### Files modified
- `skills/title.py` — two post-build patches: `shell=True` (Windows finds `claude.cmd` via shell), `encoding="utf-8"` (fixes em-dash mangling on Windows)

### Vault output
- `Content-Hub-Vault-V2/07-Titles/2026-05-07_how-i-built-a-rag-pipeline-that-actually-works.md` — verified end-to-end test run with 10 titles + thumbnail text

## Open items

- `skills/data/competitor_titles.json` is a static snapshot; no auto-refresh scheduled. Re-run `scripts/scrape_competitor_titles.py` manually to update.
- Scraper returned 40 titles (20 per channel, limited by Apify actor maxResults=20). Top view count in dataset: 361k views.
