"""
Platform Adapter — platform rules knowledge base + voice adaptation.

Provides:
- PLATFORM_RULES: static, per-platform best practices and content conventions
- get_platform_rules(platform): lookup function for any platform
- adapt_voice_to_platform(): Gemini-powered voice adaptation for each platform
- adapt_for_platform(): caption/hashtag adapter for publishing
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Static knowledge base
# ---------------------------------------------------------------------------

PLATFORM_RULES: dict[str, dict[str, Any]] = {
    "tiktok": {
        "ideal_length": "15-60s",
        "hook_window": "0-3s",
        "format": "vertical 9:16",
        "best_practices": [
            "hook in first 3 seconds — user scrolls past if no grab",
            "text overlay on key points for silent viewers",
            "trending audio when possible for algorithmic boost",
            "fast cuts (1-2s per clip) to maintain retention",
            "3-5 targeted hashtags",
        ],
        "content_types": ["short_form", "talking_head"],
        "posting_windows": ["6-9am", "12-3pm", "7-11pm"],
        "tone": "casual, energetic, trend-aware, conversational",
        "cta_style": "save + follow",
        "script_style": (
            "Open with bold, pattern-interrupting hook. "
            "Fast-paced payoff in the body. "
            "End with explicit, low-friction CTA."
        ),
    },
    "instagram": {
        "ideal_length": "15-90s (Reels) or 5-10 slides (carousel)",
        "hook_window": "0-3s",
        "format": "1:1 square or 9:16 Reels",
        "best_practices": [
            "high-quality visuals — aesthetic first impression",
            "strong, curiosity-driving first frame",
            "carousel for educational or list-style content",
            "10-20 relevant hashtags in caption",
            "Stories for daily engagement",
        ],
        "content_types": ["slides", "short_form", "talking_head"],
        "posting_windows": ["8-10am", "3-5pm", "7-9pm"],
        "tone": "aspirational, polished, community-focused",
        "cta_style": "save + share",
        "script_style": (
            "Visual-first storytelling. "
            "Clear value proposition on each slide. "
            "Final slide = CTA with a specific action."
        ),
    },
    "youtube": {
        "ideal_length": "8-15 min (long-form) or 30-60s (Shorts)",
        "hook_window": "0-5s",
        "format": "16:9 landscape (long-form) or 9:16 Shorts",
        "best_practices": [
            "strong thumbnail concept — 50% of clicks",
            "chapters for long-form navigation",
            "pattern interrupt in first 5 seconds",
            "end screen + cards for watch time",
            "SEO-optimized title and description",
        ],
        "content_types": ["slides", "talking_head", "topic"],
        "posting_windows": ["2-4pm weekdays"],
        "tone": "authoritative, educational, trust-building, in-depth",
        "cta_style": "subscribe + comment",
        "script_style": (
            "Strong open that delivers on the title promise. "
            "Structured payoff with depth and examples. "
            "Strong close with clear next-step CTA."
        ),
    },
    "youtube_shorts": {
        "ideal_length": "30-60s",
        "hook_window": "0-3s",
        "format": "vertical 9:16",
        "best_practices": [
            "hook in first 3 seconds",
            "loop-friendly ending to extend watch time",
            "captions for silent viewers",
        ],
        "content_types": ["short_form", "talking_head"],
        "posting_windows": ["2-4pm weekdays", "7-9pm weekends"],
        "tone": "punchy, high-energy, instant value",
        "cta_style": "subscribe",
        "script_style": (
            "One idea, fast delivery, loop naturally back to beginning."
        ),
    },
    "linkedin": {
        "ideal_length": "1-3 min (video) or 5-8 slides (carousel)",
        "hook_window": "0-5s (video) or first line (text post)",
        "format": "16:9 or 1:1",
        "best_practices": [
            "professional but personable tone",
            "data, research, and insights over opinions alone",
            "thought leadership angle",
            "first comment for links/resources (keeps reach high)",
            "3-5 hyper-relevant hashtags",
        ],
        "content_types": ["slides", "talking_head", "topic"],
        "posting_windows": ["7-9am weekdays", "12-1pm weekdays"],
        "tone": "professional, insightful, data-driven, authentically human",
        "cta_style": "comment + share",
        "script_style": (
            "Lead with a sharp insight or counterintuitive statement. "
            "Back it with data or a real example. "
            "Close with an open question to drive comments."
        ),
    },
    "twitter": {
        "ideal_length": "30-60s (video)",
        "hook_window": "0-3s",
        "format": "16:9 or 1:1",
        "best_practices": [
            "punchy, opinionated copy",
            "controversy or strong point of view — safe content is ignored",
            "thread format for complex topics",
            "1-2 hashtags max — overuse kills reach",
        ],
        "content_types": ["short_form", "slides"],
        "posting_windows": ["8-10am", "12-1pm", "5-6pm"],
        "tone": "conversational, opinionated, direct, witty",
        "cta_style": "retweet + comment",
        "script_style": (
            "Hot take or contrarian angle as hook. "
            "Short punchy body. "
            "End with a polarizing question or call to reply."
        ),
    },
    "facebook": {
        "ideal_length": "1-3 min",
        "hook_window": "0-3s",
        "format": "9:16 or 16:9",
        "best_practices": [
            "subtitles/captions required — 85% watch muted",
            "emotional storytelling outperforms pure information",
            "longer captions with storytelling hooks",
            "community questions to drive comments algorithm",
        ],
        "content_types": ["short_form", "talking_head"],
        "posting_windows": ["1-3pm weekdays", "12-1pm weekends"],
        "tone": "warm, community-focused, personal storytelling",
        "cta_style": "comment + share",
        "script_style": (
            "Personal story hook to build connection. "
            "Emotional arc with relatable conflict. "
            "Community invitation at the end."
        ),
    },
}


PLATFORM_GROUPS = {
    "short_form": ["tiktok", "instagram", "facebook", "youtube_shorts"],
    "professional": ["linkedin", "twitter"],
}

PLATFORM_LIMITS = {
    "tiktok": {"caption_length": 300, "hashtag_count": 5, "aspect_ratio": "9:16"},
    "instagram": {"caption_length": 2200, "hashtag_count": 30, "aspect_ratio": "1:1"},
    "youtube_shorts": {"caption_length": 100, "hashtag_count": 3, "aspect_ratio": "9:16"},
    "linkedin": {"caption_length": 3000, "hashtag_count": 5, "aspect_ratio": "1:1"},
    "twitter": {"caption_length": 280, "hashtag_count": 3, "aspect_ratio": "16:9"},
    "facebook": {"caption_length": 500, "hashtag_count": 5, "aspect_ratio": "9:16"},
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_platform_rules(platform: str) -> dict[str, Any]:
    """Return platform-specific best practices and content rules.

    Keys in the returned dict:
        ideal_length, hook_window, format, best_practices,
        content_types, posting_windows, tone, cta_style, script_style.

    Falls back to Instagram rules when platform is unknown.
    """
    return PLATFORM_RULES.get(platform.lower(), PLATFORM_RULES.get("instagram", {}))


async def adapt_voice_to_platform(
    brand_voice: str,
    platform: str,
    google_ai_studio_key: str | None = None,
) -> str:
    """Use Gemini to adapt a brand voice for a specific platform's conventions.

    Returns an adapted voice description string, or the original on failure.
    If *google_ai_studio_key* is not provided, returns a rule-appended string.

    **Design Note (2A-3):** The original plan specified static string composition
    to avoid double LLM latency. The Gemini path was added because it produces
    noticeably higher-quality platform-native voice descriptions, especially for
    platforms with very different conventions (e.g., TikTok vs LinkedIn).
    However, ``_build_prompt()`` in ``scripting.py`` intentionally uses the
    **static path** (no API key) to avoid the latency hit during script
    generation. The Gemini path is available for standalone pre-computation
    (e.g., in a brand setup flow where latency is acceptable).
    """
    if not brand_voice:
        return brand_voice

    rules = get_platform_rules(platform)

    if not google_ai_studio_key:
        # Lightweight adaptation without Gemini: append platform cues
        tone = rules.get("tone", "")
        script_style = rules.get("script_style", "")
        suffix_parts = []
        if tone:
            suffix_parts.append(f"Tone for {platform}: {tone}.")
        if script_style:
            suffix_parts.append(f"Script style: {script_style}")
        if suffix_parts:
            return f"{brand_voice}\n\n{' '.join(suffix_parts)}"
        return brand_voice

    try:
        from google import genai  # lazy import to avoid hard dep at import time

        client = genai.Client(api_key=google_ai_studio_key)
        prompt = (
            f"Adapt this brand voice for {platform.upper()}:\n\n"
            f"Original brand voice:\n{brand_voice}\n\n"
            f"Platform requirements:\n"
            f"- Platform tone: {rules.get('tone', 'engaging')}\n"
            f"- Ideal content length: {rules.get('ideal_length', '')}\n"
            f"- Script style guide: {rules.get('script_style', '')}\n"
            f"- Key best practices: {', '.join(rules.get('best_practices', []))}\n\n"
            f"Write a 2-3 sentence platform-adapted voice description that preserves "
            f"the core brand identity while conforming to {platform}'s conventions. "
            f"Return ONLY the adapted description — no labels, no explanations."
        )
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        adapted = response.text.strip()
        if adapted:
            return adapted
    except Exception:
        logger.warning(
            "adapt_voice_to_platform: Gemini call failed; returning original.",
            exc_info=True,
        )

    return brand_voice


def get_platform_group(platform: str) -> str:
    for group, platforms in PLATFORM_GROUPS.items():
        if platform in platforms:
            return group
    return "short_form"


def adapt_for_platform(script: str, source_platform: str, target_platform: str) -> dict:
    limits = PLATFORM_LIMITS.get(target_platform, PLATFORM_LIMITS["instagram"])
    caption = script[: limits["caption_length"]]
    return {
        "platform": target_platform,
        "adapted_caption": caption,
        "hashtag_limit": limits["hashtag_count"],
        "aspect_ratio": limits["aspect_ratio"],
    }


def get_secondary_platforms(primary_platform: str, workflow_platforms: list[str]) -> list[str]:
    group = get_platform_group(primary_platform)
    return [p for p in workflow_platforms if p != primary_platform and p in PLATFORM_GROUPS.get(group, [])]
