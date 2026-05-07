---
date: 2026-05-07
session: Phase 0a — Twitter Data Layer
status: complete
---

# Session: Phase 0a — Twitter Data Layer

Implements: [[Phase 0a Twitter Data Layer]]
References: [[Local_First_Skill_Engine_Plan]]

## What changed

### 1. `backend/research/apify_client.py` — appended (lines ~405–610)
- Added `scrape_twitter(keywords, accounts, max_results=60)` function
- Tries `quacker~twitter-scraper` first, falls back to `apify~twitter-scraper`
- Normalizes to 9-field schema: tweet_id, text, author_username, author_followers, like_count, reply_count, retweet_count, created_at (ISO 8601), url
- Returns `[]` + `logger.error` if both actors fail — no exception raised
- Added `_build_twitter_input_quacker`, `_build_twitter_input_apify`, `_normalize_twitter`, `_safe_int` helpers

### 2. `skills/data/twitter_config.json` — created (new file + new directory)
- Config for Twitter scout: 4 keywords, 2 accounts, max_results=60, min_composite_score=0.5

### 3. Supabase migration applied (project: fuvtjsivfngzrmyxeuug)
- `tweets` table: 16 columns, tweet_id PK, float score columns, seen_at/actioned defaults
- `tweet_actions` table: 4 columns, FK → tweets.tweet_id ON DELETE CASCADE, gen_random_uuid() PK
- Both tables verified empty (SELECT COUNT(*) = 0)

## Bugs found and fixed post-dispatch

| Bug | Fix |
|-----|-----|
| Integer fields not cast — `item.get("like_count")` could return string `"42"` → type error on DB insert | Added `_safe_int(val)` helper; all 4 int fields now cast through it |
| `status` variable referenced after polling loop without guaranteed assignment | Added `status = "UNKNOWN"` before the loop as defensive guard |

## Test results
- `python -m py_compile backend/research/apify_client.py` → SYNTAX OK
- Live test with max_results=10: `quacker~twitter-scraper` returned HTTP 403, `apify~twitter-scraper` returned HTTP 404 — external blocker, logged correctly, returned `[]` without raising
- `_safe_int` edge cases (None, 0, "0", "123", "not-a-number", "") → all pass
- `_normalize_twitter` with int tweet_id, @ prefix, string integers, None, Unix timestamp → all pass

## Open items
- Both Twitter actors currently unreachable (403/404). Need to verify actor slugs or purchase access to `quacker~twitter-scraper`. This is an external dependency, not a code issue.
- Score columns (velocity_score, authority_score, opportunity_score, replyability_score, composite_score) are NULL-able — scorer not yet implemented (Phase 0b).

## Files touched
- `backend/research/apify_client.py` (append + 2 post-dispatch fixes)
- `skills/data/twitter_config.json` (new)
- Supabase DB (migration via MCP)
- `Content-Hub-Vault-V2/00-Management-V2/Orchestrations/2026-05-07_phase0a-twitter-data-layer.md` (state file)
