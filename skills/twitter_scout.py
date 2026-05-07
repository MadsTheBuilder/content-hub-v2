"""twitter_scout — Score and surface high-opportunity tweets, forward to Telegram.

Run directly:
    python skills/twitter_scout.py

Or import:
    from skills.twitter_scout import run_scout
"""
import asyncio
import inspect
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Resolve project root regardless of working directory, load .env before any
# backend import so pydantic_settings picks up vars from os.environ.
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv  # noqa: E402 — must come after sys.path
load_dotenv(PROJECT_ROOT / ".env")

import httpx  # noqa: E402

from backend.database import get_supabase  # noqa: E402
from backend.research.apify_client import scrape_twitter  # noqa: E402
from skills.twitter_scorer import (  # noqa: E402
    authority_score,
    composite_score,
    opportunity_score,
    softmax_select,
    velocity_score,
)

logger = logging.getLogger(__name__)

CONFIG_FILE = PROJECT_ROOT / "twitter_config.json"

# Columns that exist in the `tweets` table — strip computed fields before insert.
_DB_FIELDS: frozenset[str] = frozenset({
    "tweet_id", "text", "author_username", "author_followers",
    "like_count", "reply_count", "retweet_count", "created_at", "url",
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hours_since(created_at: str) -> float:
    """Return hours elapsed since created_at (ISO 8601 string).

    Handles:
    - Z-suffix:    '2024-01-15T10:30:00Z'
    - UTC offset:  '2024-01-15T10:30:00+00:00'
    - Naive:       '2024-01-15T10:30:00'  (treated as UTC)
    - Malformed:   returns 0.0 with a warning
    """
    try:
        normalized = created_at.replace("Z", "+00:00")
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).total_seconds() / 3600.0
    except (ValueError, TypeError, AttributeError):
        logger.warning("Could not parse created_at=%r — defaulting to 0 hours", created_at)
        return 0.0


def _send_telegram(tweet: dict) -> None:
    """POST the scout summary to Telegram. Raises on HTTP error or missing creds."""
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


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_scout() -> None:
    """Full pipeline: scrape → score → filter → select → Telegram → log."""
    config = json.loads(CONFIG_FILE.read_text())
    min_score: float = config.get("min_composite_score", 0.3)
    temperature: float = config.get("temperature", 1.0)
    search_config: dict = config.get("search_config", {})

    # Support both sync and async implementations of scrape_twitter.
    raw = scrape_twitter(search_config)
    tweets: list[dict] = asyncio.run(raw) if inspect.isawaitable(raw) else raw

    if not tweets:
        print("No tweets returned from scraper.")
        return

    sb = get_supabase()

    # Snapshot seen IDs BEFORE the upsert so first-run semantics are correct:
    # candidates = tweets new to THIS run, not tweets new after the upsert.
    existing_result = sb.table("tweets").select("tweet_id").execute()
    seen_ids: set[str] = {row["tweet_id"] for row in (existing_result.data or [])}

    # Annotate each tweet with derived fields (not persisted to DB).
    for tweet in tweets:
        tweet["hours_since_post"] = _hours_since(tweet["created_at"])
        tweet["composite_score"] = composite_score(tweet)

    # Persist all scraped tweets — strip the computed fields first.
    rows = [{k: v for k, v in t.items() if k in _DB_FIELDS} for t in tweets]

    try:
        sb.table("tweets").upsert(rows, on_conflict="tweet_id").execute()
        logger.info("Upserted %d tweets to Supabase", len(rows))
    except AttributeError:
        # MockSupabaseClient doesn't implement upsert — skip silently in dev.
        logger.warning("Supabase mock mode active — tweet writes skipped")

    # Filter: new to this run AND above composite score threshold.
    candidates = [
        t for t in tweets
        if t["tweet_id"] not in seen_ids and t["composite_score"] >= min_score
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
