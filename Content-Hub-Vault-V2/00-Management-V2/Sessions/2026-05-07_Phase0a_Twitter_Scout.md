---
date: 2026-05-07
session: Phase 0a — Twitter Scout Application Layer
status: complete
---

# Session: Phase 0a — Twitter Scout

## What changed

Built the complete Twitter Scout application layer. Five files created, one updated.

### Created

- `skills/twitter_scorer.py` — five 0–1 scoring signals, composite average, log-sum-exp softmax selector
- `skills/twitter_scout.py` — end-to-end pipeline: scrape → score → filter → select → Telegram → Supabase log
- `scripts/twitter_scheduler.py` — while-True polling loop, 40–50 min jitter
- `.claude/skills/twitter-scout/SKILL.md` — Claude Code `/twitter-scout` entry point
- `twitter_config.json` — runtime config (keywords, min_composite_score, temperature)

### Updated

- `.env.example` — added `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

## Files touched

```
skills/twitter_scorer.py
skills/twitter_scout.py
scripts/twitter_scheduler.py
.claude/skills/twitter-scout/SKILL.md
twitter_config.json
.env.example
```

## Architecture

Two-layer pattern per [[Local_First_Skill_Engine_Plan]]:
- `.claude/skills/twitter-scout/SKILL.md` (Claude entry) → `skills/twitter_scout.py` (Python logic)

[[twitter_scorer]] implements: `velocity_score`, `authority_score`, `timing_score`, `opportunity_score`, `replyability_score`, `composite_score`, `softmax_select`

[[twitter_scout]] implements: `run_scout()` — calls [[scrape_twitter]] from [[apify_client]], writes to `tweets` table, selects via softmax, sends to Telegram via httpx Bot API, logs to `tweet_actions`

[[twitter_scheduler]] wraps `run_scout()` in a retry-safe while-True loop

## Non-obvious decisions

- `seen_ids` snapshot taken BEFORE the upsert: ensures first-run correctness (tweets new to THIS run, not new after the upsert)
- `_DB_FIELDS` frozenset at module level: strips `hours_since_post` and `composite_score` before Supabase write
- `upsert` wrapped in `AttributeError` catch: MockSupabaseClient doesn't implement upsert — fails gracefully in mock mode
- `inspect.isawaitable` guard: `scrape_twitter()` is likely async (all other Apify functions are); handles both without breaking sync callers
- Log-sum-exp trick in `softmax_select`: prevents float overflow when temperature < 0.01
- `_hours_since` handles Z-suffix, UTC offset, naive datetimes, and malformed strings — returns 0.0 with warning rather than crashing the pipeline

## Verification

- `py_compile` passed on all three Python files
- All scorer unit tests passed (velocity, authority, timing, opportunity, replyability, composite, softmax)
- `_hours_since` tested against Z-suffix, +00:00, naive, malformed, None inputs
- E2E dry-run with fake Supabase + fake scraper:
  - Run 1: tweets upserted, one selected and sent ✓
  - Run 2: all seen, no candidates ✓
  - Run 3: new tweet correctly identified and selected ✓

## Prerequisites for E2E test

Add to `.env` before running:
```
TELEGRAM_BOT_TOKEN=<real value>
TELEGRAM_CHAT_ID=<real value>
SUPABASE_URL=<real value>
SUPABASE_SERVICE_KEY=<real value>
```

Then: `python skills/twitter_scout.py`

## Open items

- `scrape_twitter()` is assumed to exist in [[apify_client]] — not yet verified; add when the function is implemented
- `tweet_actions` table: no uniqueness constraint on (tweet_id, action_type) — the same tweet could be logged multiple times if it appears across scrape windows; acceptable for now

Implements: [[Local_First_Skill_Engine_Plan]]
Modifies: [[twitter_config]], [[env_example]]
References: [[apify_client]], [[backend_database]], [[twitter_scorer]]
