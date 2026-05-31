---
date: 2026-05-31
type: session-log
description: "Fix researcher skill crashing with ValueError when a direct GitHub URL is passed that isn't present in the github_trending.md trending file."
tags: [bug-fix, researcher, skills]
---

# Session: Researcher Any-URL Fix

Implements: [[researcher.py]]

## What Changed

Researcher skill now accepts any URL as input — GitHub, YouTube, websites, webpages — not just repos present in `[[github_trending.md]]`.

## Root Cause (original bug)

`skills/researcher.py` `run()` filtered every user-supplied repo against `github_trending.md`. Any URL absent from that file → empty list → `ValueError`. GitHub-specific steps (README fetch, doc crawler) also ran unconditionally.

## Full Fix Applied

Modifies: [[researcher.py]]

### 1. New URL helpers (`url_slug`, `source_label`, `is_github_url`)
- `url_slug(url)` — filesystem-safe slug from any URL (GitHub → `owner-repo`, YouTube → `youtube-{id}`, generic → `host-path`)
- `source_label(url)` — human-readable prompt label for any URL
- `is_github_url(url)` — guards GitHub-specific pipeline steps

### 2. `run()` rewrite
- Full URLs (`://`) are used directly, no trending file required
- Bare `owner/repo` slugs still resolve via trending file (lazy — only reads file if bare slugs are present)
- Clear error if neither path yields any URL

### 3. `research_one()` — non-GitHub safety
- README fetch and `discover_primary_docs` wrapped in `if is_github_url(url):`
- `owner_repo` set to `source_label(url)` (generic label) at top of function
- GitHub-specific API path keeps its own `owner_repo_gh` variable

### 4. Prompts de-GitHub-ified
- `synthesize_brief()`, `extract_repo_context()`, verification prompt, chat configure prompt — all removed "GitHub project" language

## Files Touched

- `skills/researcher.py`

## Open Items

None.
