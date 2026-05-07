---
name: twitter-scout
description: Scout Twitter for high-opportunity tweets to reply to, score them across five signals, and send the best probabilistic pick to Telegram
trigger: /twitter-scout
---

# Twitter Scout

Runs the Twitter scoring and selection pipeline. Scrapes recent tweets, scores each
tweet on five 0–1 signals (velocity, authority, timing, opportunity, replyability),
then sends the top probabilistic pick to Telegram and logs the action to Supabase.

## Usage

```
/twitter-scout
```

No arguments.

## What it does

1. Loads `twitter_config.json` from the project root (min score, temperature, search config)
2. Calls `scrape_twitter(search_config)` via `backend/research/apify_client.py`
3. Scores every tweet with five 0–1 signals → composite score (simple average)
4. Upserts all scraped tweets to the Supabase `tweets` table
5. Filters out tweets already seen (present in `tweets` table before this run)
6. Softmax-selects one tweet probabilistically (not always the top scorer)
7. Sends the scout summary to Telegram
8. Logs `action_type='sent_to_telegram'` to the `tweet_actions` table

## Invocation

```bash
python skills/twitter_scout.py
```

## Expected output

```
INFO: Upserted N tweets to Supabase
Sent tweet <tweet_id> to Telegram (score: 0.XX)
INFO: Logged tweet_action for <tweet_id>
```

Telegram receives a message formatted as:

```
🎯 Tweet Scout

@username (N,NNN followers)
"tweet text"

Velocity: 0.XX | Authority: 0.XX
Opportunity: 0.XX | Composite: 0.XX

https://twitter.com/...
```

## Prerequisites

- `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`
- `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in `.env` (real values, not placeholders)
- Supabase tables `tweets` (tweet_id PK) and `tweet_actions` must exist

## To run on a schedule (40-50 min interval)

```bash
python scripts/twitter_scheduler.py
```

## Scoring signals

| Signal | Description |
|---|---|
| velocity | Likes-per-hour (100 lph = 1.0) |
| authority | Log10 follower count (1M followers = 1.0) |
| timing | Linear decay 0–24 h (fresh = 1.0) |
| opportunity | Like/reply ratio (low replies on popular = gap) |
| replyability | Question mark or trigger words present |
