---
status: Completed
date: 2026-04-29
type: session_summary
---

# Session: GitHub Trending Script (Phase 0b)

Implements: [[GitHub Trending Script (Phase 0b — Fountainhead #2)]]
References: [[Chase AI Content System — Detailed Breakdown]] | [[Local_First_Skill_Engine_Plan]]
Modifies: [[Current_Sprint]]

## What Was Done

Built `github_trending.py` — the daily Fountainhead #2 script. Writes a markdown report to `Content-Hub-Vault/04-Trends/github_trending.md`, which the future `/researcher` skill reads for topic discovery.

**Script behaviour:**
- Queries GitHub Search API (`/search/repositories`) for AI repos using topic filters: `llm`, `ai`, `machine-learning`, `deep-learning`, `generative-ai`, `rag`, `transformer`
- 7-day window → top 10 repos sorted by star count; computes star velocity (stars ÷ age in days)
- 30-day window → top 5 repos, excluding anything already in the 7-day list
- Single Claude API call (`claude-sonnet-4-6`) picks 1 repo from each window with 1–2 sentence reasoning
- Output overwrites `04-Trends/github_trending.md` daily

**No auth required for first run** — GitHub public API allows 60 req/hr unauthenticated. `GITHUB_TOKEN` env var improves limit to 5000/hr.

## Files Created

- `github_trending.py` — main script (project root)
- `run_github_trending.bat` — Windows Task Scheduler wrapper, logs to `logs/github_trending.log`
- `Content-Hub-Vault/04-Trends/` — new vault folder (created by script on first run)

## Outstanding

- [ ] Schedule `run_github_trending.bat` via Windows Task Scheduler (daily 08:00)
- [ ] Add `GITHUB_TOKEN` to `.env` for higher rate limits (optional but recommended)
- [ ] Next: Phase 0a Twitter scraping web app, OR jump to Phase 1 infrastructure (`skills/runner.py`)
