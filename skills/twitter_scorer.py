"""twitter_scorer — Five 0.0–1.0 scoring signals for tweet opportunity selection."""
import math
import random


def velocity_score(like_count: int, hours_since_post: float) -> float:
    """Likes-per-hour normalised to 0–1. 100 lph = 1.0."""
    hours = max(hours_since_post, 0.1)  # floor to avoid division by zero on brand-new tweets
    return min(like_count / hours / 100.0, 1.0)


def authority_score(author_followers: int) -> float:
    """Log10 scale: 0 followers → 0.0, 1 M followers → 1.0, capped at 1 M."""
    if author_followers <= 0:
        return 0.0
    return math.log10(min(author_followers, 1_000_000)) / math.log10(1_000_000)


def timing_score(hours_since_post: float) -> float:
    """Linear decay: 0 h → 1.0, 24 h → 0.0. Clamped to [0, 1]."""
    return max(0.0, 1.0 - hours_since_post / 24.0)


def opportunity_score(reply_count: int, like_count: int) -> float:
    """Low replies on a popular tweet signals an unanswered conversation gap.
    Ratio = likes / (replies+1); normalised so 500 = 1.0."""
    return min(like_count / (reply_count + 1) / 500.0, 1.0)


_REPLYABILITY_WORDS = frozenset({
    "thoughts", "agree", "disagree", "opinion", "think",
    "unpopular", "hot take", "what do you", "your take",
})


def replyability_score(text: str) -> float:
    """Heuristic: question mark → 1.0; trigger words → 0.8; else 0.3."""
    if "?" in text:
        return 1.0
    lower = text.lower()
    if any(w in lower for w in _REPLYABILITY_WORDS):
        return 0.8
    return 0.3


def composite_score(tweet: dict) -> float:
    """Simple average of all five signals.
    tweet dict must already have 'hours_since_post' attached by the caller."""
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
    """Probabilistic selection weighted by softmax of composite_score.

    Uses temperature to control spread:
    - temperature → 0 : approaches argmax (always picks best)
    - temperature → ∞ : approaches uniform random

    Raises ValueError if tweets is empty.
    """
    if not tweets:
        raise ValueError("softmax_select requires a non-empty list")

    # Guard against degenerate temperatures that cause exp overflow or div-by-zero
    t = max(temperature, 1e-3)

    scores = [tw["composite_score"] for tw in tweets]

    # Subtract max for numerical stability (standard log-sum-exp trick)
    max_score = max(scores)
    exp_scores = [math.exp((s - max_score) / t) for s in scores]

    total = sum(exp_scores)
    weights = [e / total for e in exp_scores]
    return random.choices(tweets, weights=weights, k=1)[0]
