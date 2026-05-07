---
slug: phase0a-twitter-scout
created: 2026-05-07
status: complete
current_group: null
groups_complete: []
specialists_involved: [research-agent, intelligence-agent]
---

# Orchestration: Phase 0a — Twitter Scout Application Layer

## Recon summary

- `skills/` exists with 10 Python modules (`researcher.py`, `yt_pipeline.py`, etc.) — all use `PROJECT_ROOT = Path(__file__).parent.parent` pattern
- `scripts/` does NOT exist — must be created
- `backend/research/apify_client.py` exists and is off-limits; `scrape_twitter()` is assumed present with the given return schema
- `backend/database.py` exposes `get_supabase()` — handles real/mock Supabase transparently; module path is `backend.database`
- `backend/config.py` uses pydantic_settings with `extra="ignore"` — TELEGRAM vars should be loaded via `os.getenv()` directly, not through Settings
- `.env.example` exists but has NO Telegram vars — needs `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` added
- `requirements.txt` has `httpx==0.27.0` already — use httpx for Telegram Bot API calls (no new dependency needed)
- `.claude/skills/` directory exists; `twitter-scout/` subdirectory does not yet exist
- `twitter_config.json` does not exist — must be created as part of this build

## Execution plan

### Group 1 (parallel)

- [research-agent | EASY] Create `skills/twitter_scorer.py`
  Files: `skills/twitter_scorer.py`
  Criteria:
  1. Five functions present: velocity_score, authority_score, timing_score, opportunity_score, replyability_score
  2. All return float in [0.0, 1.0]
  3. velocity_score: like_count / max(hours, 0.1) / 100, capped at 1.0
  4. authority_score: log10(min(followers, 1_000_000)) / log10(1_000_000), returns 0.0 for ≤0 followers
  5. timing_score: max(0.0, 1.0 - hours/24.0)
  6. opportunity_score: like_count / (reply_count+1) / 500, capped at 1.0
  7. replyability_score: 1.0 if "?" in text; 0.8 if trigger words present; else 0.3
  8. composite_score(tweet: dict) → simple average of all five
  9. softmax_select(tweets, temperature=1.0) → one tweet dict sampled via random.choices(weights=softmax probs)

- [research-agent | EASY] Create `twitter_config.json` + update `.env.example`
  Files: `twitter_config.json`, `.env.example`
  Criteria:
  1. `twitter_config.json` has `min_composite_score`, `temperature`, `search_config` fields
  2. `.env.example` gains two new lines: `TELEGRAM_BOT_TOKEN=your-telegram-bot-token` and `TELEGRAM_CHAT_ID=your-telegram-chat-id`
  3. No other lines in `.env.example` changed

### Group 2 (depends on Group 1)

- [research-agent | MEDIUM] Create `skills/twitter_scout.py`
  Files: `skills/twitter_scout.py`
  Read for context: `skills/twitter_scorer.py`, `backend/database.py`, `backend/config.py`, `twitter_config.json`
  Criteria:
  1. `run_scout()` loads `twitter_config.json` from PROJECT_ROOT
  2. Calls `scrape_twitter(search_config)` — handles both sync and async (use asyncio.run if awaitable)
  3. Attaches `hours_since_post` and `composite_score` to each tweet dict
  4. Upserts ALL scraped tweets to `tweets` table (fields matching schema: tweet_id, text, author_username, author_followers, like_count, reply_count, retweet_count, created_at, url)
  5. Fetches existing tweet_ids from DB BEFORE upsert; filters candidates to those not already seen AND score >= min_composite_score
  6. softmax_select from candidates; if no candidates, prints message and returns
  7. Sends Telegram message with exact format specified in task (via httpx POST to Bot API)
  8. Logs to `tweet_actions` table: {tweet_id, action_type: "sent_to_telegram"}
  9. `if __name__ == "__main__"` block with basicConfig logging and calls run_scout()
  10. Uses `os.getenv()` for TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID (not backend.config)

### Group 3 (parallel, depends on Group 2)

- [intelligence-agent | EASY] Create `scripts/twitter_scheduler.py`
  Files: `scripts/twitter_scheduler.py`
  Criteria:
  1. Inserts PROJECT_ROOT into sys.path so `from skills.twitter_scout import run_scout` works
  2. while-True loop: calls run_scout(), catches all exceptions with logging, then sleeps random.randint(2400, 3000)
  3. Entry guard: `if __name__ == "__main__"` with basicConfig logging

- [research-agent | EASY] Create `.claude/skills/twitter-scout/SKILL.md`
  Files: `.claude/skills/twitter-scout/SKILL.md`
  Criteria:
  1. Has name, description, usage/trigger section
  2. Command: `python skills/twitter_scout.py`
  3. Expected output described: tweet sent to Telegram + tweet_id logged to tweet_actions

## Agent prompts

### Task: research-agent: Create skills/twitter_scorer.py

- description: "research-agent: Create skills/twitter_scorer.py"
- model: haiku
- prompt: |
    You are the research-agent for the Content Hub V2 project.

    **Role:** Research layer and RAG specialist
    **When to use:** Work on trending content scraping, embedding, retrieval, or the research brief assembly.

    **Owns:**
    - `backend/research/apify_client.py` — Apify actor runs + polling
    - `backend/research/organic_score.py` — view × retention scoring
    - `backend/research/rag.py` — embed_and_store, similarity search, weekly refresh
    - `backend/research/research_service.py` — ResearchBrief assembly

    **Key facts:**
    - Embedding model: text-embedding-004 (Gemini), 768 dimensions
    - pgvector search via match_embeddings RPC in Supabase
    - Mock mode: sb.rpc() returns empty result

    ## Your Task

    Create `skills/twitter_scorer.py` with five 0.0–1.0 scoring functions, a composite scorer, and a softmax selector.

    Look at `skills/researcher.py` first to understand the module style (no class, just module-level functions, PROJECT_ROOT pattern).

    ## Scope
    Read for context: `skills/researcher.py`
    Create: `skills/twitter_scorer.py`

    IMPORTANT: Only touch the files listed above.

    ## Exact specification

    ```python
    # skills/twitter_scorer.py
    import math
    import random

    def velocity_score(like_count: int, hours_since_post: float) -> float:
        """Likes-per-hour normalized to 0–1 (100 lph = 1.0)."""
        hours = max(hours_since_post, 0.1)
        return min(like_count / hours / 100.0, 1.0)

    def authority_score(author_followers: int) -> float:
        """Log10 scale: 0 followers=0.0, 1M followers=1.0."""
        if author_followers <= 0:
            return 0.0
        return math.log10(min(author_followers, 1_000_000)) / math.log10(1_000_000)

    def timing_score(hours_since_post: float) -> float:
        """Linear decay: 0h=1.0, 24h=0.0."""
        return max(0.0, 1.0 - hours_since_post / 24.0)

    def opportunity_score(reply_count: int, like_count: int) -> float:
        """Low replies on popular tweet = high gap (ratio/500, capped 1.0)."""
        return min(like_count / (reply_count + 1) / 500.0, 1.0)

    _REPLYABILITY_WORDS = {"thoughts", "agree", "disagree", "opinion", "think", "unpopular", "hot take"}

    def replyability_score(text: str) -> float:
        """Heuristic: question mark=1.0, trigger words=0.8, else 0.3."""
        if "?" in text:
            return 1.0
        if any(w in text.lower() for w in _REPLYABILITY_WORDS):
            return 0.8
        return 0.3

    def composite_score(tweet: dict) -> float:
        """Simple average of all five scores. tweet must have hours_since_post."""
        h = tweet.get("hours_since_post", 0.0)
        scores = [
            velocity_score(tweet["like_count"], h),
            authority_score(tweet["author_followers"]),
            timing_score(h),
            opportunity_score(tweet["reply_count"], tweet["like_count"]),
            replyability_score(tweet["text"]),
        ]
        return sum(scores) / len(scores)

    def softmax_select(tweets: list[dict], temperature: float = 1.0) -> dict:
        """Probabilistic selection weighted by softmax of composite_score."""
        scores = [t["composite_score"] for t in tweets]
        exp_scores = [math.exp(s / temperature) for s in scores]
        total = sum(exp_scores)
        weights = [e / total for e in exp_scores]
        return random.choices(tweets, weights=weights, k=1)[0]
    ```

    Write that file exactly as shown. No modifications.

    ## Acceptance Criteria
    1. File exists at `skills/twitter_scorer.py`
    2. All seven functions present with correct signatures
    3. velocity_score, authority_score, opportunity_score capped at 1.0
    4. timing_score returns 0.0 for hours >= 24
    5. softmax_select uses random.choices

    ## When done
    Report: DONE or STUCK. Include what you created.

### Task: research-agent: Create twitter_config.json and update .env.example

- description: "research-agent: Create twitter_config.json + update .env.example"
- model: haiku
- prompt: |
    You are the research-agent for the Content Hub V2 project.

    ## Your Task

    1. Create `twitter_config.json` at the project root with reasonable defaults.
    2. Append two new lines to `.env.example` (do NOT change any existing lines).

    ## Scope
    Read for context: `.env.example`
    Create: `twitter_config.json`
    Edit: `.env.example`

    IMPORTANT: Only touch the files listed above.

    ## Exact content

    `twitter_config.json`:
    ```json
    {
      "search_config": {
        "keywords": ["AI", "SaaS", "founder", "product"],
        "max_results": 50
      },
      "min_composite_score": 0.3,
      "temperature": 1.0
    }
    ```

    `.env.example` — append these two lines at the end (preserve all existing lines exactly):
    ```
    TELEGRAM_BOT_TOKEN=your-telegram-bot-token
    TELEGRAM_CHAT_ID=your-telegram-chat-id
    ```

    ## Acceptance Criteria
    1. `twitter_config.json` exists with min_composite_score, temperature, search_config
    2. `.env.example` has TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID at the end
    3. No other lines in `.env.example` changed

    ## When done
    Report: DONE or STUCK.

### Task: research-agent: Create skills/twitter_scout.py

- description: "research-agent: Create skills/twitter_scout.py"
- model: sonnet
- prompt: |
    You are the research-agent for the Content Hub V2 project.

    **Role:** Research layer and RAG specialist — trending content scraping and research brief assembly.

    ## Your Task

    Create `skills/twitter_scout.py`. This is the main entry point for the Twitter Scout feature.

    ## Scope
    Read for context: `skills/twitter_scorer.py`, `backend/database.py`, `backend/config.py`, `twitter_config.json`, `skills/researcher.py`
    Create: `skills/twitter_scout.py`

    IMPORTANT: Only touch `skills/twitter_scout.py`. Do NOT touch `backend/research/apify_client.py`.

    ## Exact specification

    The file must implement `run_scout()` as follows:

    ```python
    """twitter_scout — Find high-opportunity tweets and send to Telegram."""
    import asyncio
    import inspect
    import json
    import logging
    import os
    import sys
    from datetime import datetime, timezone
    from pathlib import Path

    import httpx
    from dotenv import load_dotenv

    PROJECT_ROOT = Path(__file__).parent.parent
    load_dotenv(PROJECT_ROOT / ".env")
    sys.path.insert(0, str(PROJECT_ROOT))

    from backend.database import get_supabase
    from backend.research.apify_client import scrape_twitter
    from skills.twitter_scorer import (
        authority_score,
        composite_score,
        opportunity_score,
        softmax_select,
        velocity_score,
    )

    logger = logging.getLogger(__name__)

    CONFIG_FILE = PROJECT_ROOT / "twitter_config.json"


    def _hours_since(created_at: str) -> float:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0


    def _send_telegram(tweet: dict) -> None:
        token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHAT_ID"]
        h = tweet["hours_since_post"]
        message = (
            f"🎯 Tweet Scout\n\n"
            f"@{tweet['author_username']} ({tweet['author_followers']:,} followers)\n"
            f"\"{tweet['text']}\"\n\n"
            f"Velocity: {velocity_score(tweet['like_count'], h):.2f} | "
            f"Authority: {authority_score(tweet['author_followers']):.2f}\n"
            f"Opportunity: {opportunity_score(tweet['reply_count'], tweet['like_count']):.2f} | "
            f"Composite: {tweet['composite_score']:.2f}\n\n"
            f"{tweet['url']}"
        )
        resp = httpx.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": message},
            timeout=10,
        )
        resp.raise_for_status()


    def run_scout() -> None:
        config = json.loads(CONFIG_FILE.read_text())
        min_score: float = config.get("min_composite_score", 0.3)
        temperature: float = config.get("temperature", 1.0)
        search_config: dict = config.get("search_config", {})

        raw = scrape_twitter(search_config)
        tweets: list[dict] = asyncio.run(raw) if inspect.isawaitable(raw) else raw

        sb = get_supabase()

        existing = sb.table("tweets").select("tweet_id").execute()
        seen_ids = {row["tweet_id"] for row in (existing.data or [])}

        for tweet in tweets:
            tweet["hours_since_post"] = _hours_since(tweet["created_at"])
            tweet["composite_score"] = composite_score(tweet)

        if tweets:
            rows = [
                {k: v for k, v in t.items() if k not in ("hours_since_post", "composite_score")}
                for t in tweets
            ]
            sb.table("tweets").upsert(rows, on_conflict="tweet_id").execute()
            logger.info("Upserted %d tweets to Supabase", len(tweets))

        candidates = [
            t for t in tweets
            if t["composite_score"] >= min_score and t["tweet_id"] not in seen_ids
        ]

        if not candidates:
            print("No new candidates above score threshold.")
            return

        selected = softmax_select(candidates, temperature=temperature)
        _send_telegram(selected)
        print(f"Sent tweet {selected['tweet_id']} to Telegram (score: {selected['composite_score']:.2f})")

        sb.table("tweet_actions").insert({
            "tweet_id": selected["tweet_id"],
            "action_type": "sent_to_telegram",
        }).execute()
        logger.info("Logged tweet_action for %s", selected["tweet_id"])


    if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        run_scout()
    ```

    Write that file exactly as shown.

    ## Acceptance Criteria
    1. File exists at `skills/twitter_scout.py`
    2. run_scout() loads twitter_config.json from PROJECT_ROOT
    3. Handles both sync and async scrape_twitter() via inspect.isawaitable
    4. Fetches seen_ids BEFORE upsert
    5. Upserts all tweets (stripping hours_since_post and composite_score)
    6. Filters by score threshold AND not in seen_ids
    7. Telegram message uses the exact format specified
    8. Logs to tweet_actions with action_type='sent_to_telegram'
    9. Uses os.environ for Telegram credentials (not backend.config)

    ## When done
    Report: DONE or STUCK. Include what you created.

### Task: intelligence-agent: Create scripts/twitter_scheduler.py

- description: "intelligence-agent: Create scripts/twitter_scheduler.py"
- model: haiku
- prompt: |
    You are the intelligence-agent for the Content Hub V2 project.

    **Role:** Learning system and suggestions specialist — scheduling, learning loops, and trend detection.

    **Owns:** backend/intelligence/, backend/scheduler/jobs.py

    ## Your Task

    Create `scripts/twitter_scheduler.py` — a standalone polling loop that calls run_scout() every 40–50 minutes.

    Note: The `scripts/` directory does not exist yet. The Write tool will create it.

    ## Scope
    Read for context: `skills/twitter_scout.py`
    Create: `scripts/twitter_scheduler.py`

    IMPORTANT: Only touch the file listed above.

    ## Exact content

    ```python
    """twitter_scheduler — Run twitter_scout every 40-50 minutes."""
    import logging
    import random
    import sys
    import time
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).parent.parent))

    from skills.twitter_scout import run_scout

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    logger = logging.getLogger(__name__)

    if __name__ == "__main__":
        logger.info("Twitter scheduler started. Running every 40-50 minutes.")
        while True:
            try:
                run_scout()
            except Exception as exc:
                logger.error("run_scout() failed: %s", exc)
            delay = random.randint(2400, 3000)
            logger.info("Sleeping %d seconds (%.1f min)...", delay, delay / 60)
            time.sleep(delay)
    ```

    Write that file exactly as shown.

    ## Acceptance Criteria
    1. File exists at `scripts/twitter_scheduler.py`
    2. sys.path insert at top so import works from any working directory
    3. while-True loop with try/except wrapping run_scout()
    4. random.randint(2400, 3000) sleep
    5. Proper logging throughout

    ## When done
    Report: DONE or STUCK.

### Task: research-agent: Create .claude/skills/twitter-scout/SKILL.md

- description: "research-agent: Create .claude/skills/twitter-scout/SKILL.md"
- model: haiku
- prompt: |
    You are the research-agent for the Content Hub V2 project.

    ## Your Task

    Create `.claude/skills/twitter-scout/SKILL.md` — the Claude Code skill entry point for /twitter-scout.

    Look at `.claude/skills/` to understand any existing skill structure (there may only be a single `.md` file there, not subdirectories — that's fine, create the subdirectory).

    ## Scope
    Create: `.claude/skills/twitter-scout/SKILL.md`

    IMPORTANT: Only touch the file listed above.

    ## Exact content

    ```markdown
    ---
    name: twitter-scout
    description: Scout Twitter for high-opportunity tweets to reply to and send the best candidate to Telegram
    trigger: /twitter-scout
    ---

    # Twitter Scout

    Runs the Twitter scoring and selection pipeline. Scrapes recent tweets, scores each
    on velocity, authority, timing, opportunity, and replyability, then sends the top
    probabilistic pick to Telegram.

    ## Usage

    /twitter-scout

    (No arguments.)

    ## What it does

    1. Loads `twitter_config.json` from project root
    2. Calls `scrape_twitter()` via `backend/research/apify_client.py`
    3. Scores every tweet with five 0–1 signals → composite score
    4. Filters out tweets already seen (in Supabase `tweets` table)
    5. Softmax-selects one tweet (probabilistic, not always top scorer)
    6. Sends to Telegram in the Scout format
    7. Logs `action_type='sent_to_telegram'` to `tweet_actions` table

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
    🎯 Tweet Scout

    @username (N,NNN followers)
    "tweet text"

    Velocity: 0.XX | Authority: 0.XX
    Opportunity: 0.XX | Composite: 0.XX

    https://twitter.com/...

    ## Prerequisites

    - `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set in `.env`
    - Supabase `tweets` and `tweet_actions` tables exist
    - `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` set in `.env`
    ```

    Write that file exactly as shown.

    ## Acceptance Criteria
    1. File exists at `.claude/skills/twitter-scout/SKILL.md`
    2. Has trigger: /twitter-scout
    3. Documents invocation command
    4. Describes expected Telegram message format

    ## When done
    Report: DONE or STUCK.

## Status log
- 2026-05-07 created, status=awaiting-approval
