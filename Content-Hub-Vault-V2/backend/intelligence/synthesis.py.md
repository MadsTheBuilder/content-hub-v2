---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/synthesis.py"
category: "Content Hub Source Code"
---

# synthesis.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
"""
Content Synthesis module.

Two responsibilities:
1. Post enrichment -- analyze trending posts with Gemini ("why it works")
2. Strategy generation -- synthesize selected posts + brand context into a
   StrategyDocument for user review before script generation.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from typing import Any

from backend.config import settings
from backend.database import get_supabase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class StrategyDocument:
    content_angle: str = ""
    why_this_angle: str = ""
    target_platform: str = ""
    recommended_format: dict = field(default_factory=lambda: {
        "type": "short_form",
        "length": "30-60s",
        "hook_style": "question",
        "pacing": "fast",
        "cta_style": "follow",
    })
    inspired_by: list[dict] = field(default_factory=list)
    differentiation: str = ""
    user_notes: str = ""
    alternatives: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# Gemini client (lazy init)
# ---------------------------------------------------------------------------

_genai_client = None
_client_init_failed = False


def _get_genai_client():
    global _genai_client, _client_init_failed
    if _genai_client is not None:
        return _genai_client
    if _client_init_failed:
        return None
    if not settings.google_ai_studio_key:
        logger.warning("google_ai_studio_key not set -- synthesis will use defaults.")
        _client_init_failed = True
        return None
    try:
        from google import genai
        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        return _genai_client
    except Exception:
        logger.exception("Failed to create GenAI client for synthesis.")
        _client_init_failed = True
        return None


async def _gemini_json(prompt: str, fallback: Any = None) -> Any:
    """Call Gemini Flash -> Flash-Lite, parse JSON response."""
    client = _get_genai_client()
    if client is None:
        return fallback

    for model_name in ("gemini-2.5-flash", "gemini-2.5-flash-lite"):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            text = response.text.strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
            return json.loads(text)
        except Exception:
            logger.warning("Synthesis: %s failed, trying next.", model_name)
            continue

    logger.error("Synthesis: all Gemini models failed.")
    return fallback


# ---------------------------------------------------------------------------
# Post enrichment ("why it works" analysis)
# ---------------------------------------------------------------------------

async def enrich_trending_posts(
    posts: list[dict],
    brand_profile: dict,
    limit: int = 10,
) -> list[dict]:
    """Analyze top trending posts with Gemini to explain why they work.

    Updates each post dict in-place with a 'content_analysis' key.
    Returns the enriched posts.
    """
    to_analyze = posts[:limit]
    if not to_analyze:
        return posts

    audience_ctx = ""
    if brand_profile:
        interests = brand_profile.get("audience_interests", [])
        if interests:
            audience_ctx = f"Target audience interests: {', '.join(interests)}. "
        tone = brand_profile.get("tone", "")
        if tone:
            audience_ctx += f"Brand tone: {tone}. "

    for post in to_analyze:
        title = post.get("title", "")[:200]
        description = post.get("description", "")[:300]
        metrics = (
            f"Views: {post.get('view_count', 0)}, "
            f"Likes: {post.get('like_count', 0)}, "
            f"Comments: {post.get('comment_count', 0)}, "
            f"Shares: {post.get('share_count', 0)}"
        )
        platform = post.get("platform", "")

        prompt = f"""Analyze this trending {platform} post and explain why it performs well.
{audience_ctx}
Post title: "{title}"
Description: "{description}"
Metrics: {metrics}

Return ONLY a JSON object:
{{
  "hook_type": "question/number/story/contrarian/statement/curiosity_gap",
  "content_style": "educational/entertaining/motivational/practical/controversial",
  "pacing": "fast/medium/slow",
  "engagement_drivers": ["list of 2-3 reasons it gets engagement"],
  "why_it_works": "1-2 sentence explanation",
  "applicable_techniques": ["2-3 techniques the user could borrow"]
}}"""

        analysis = await _gemini_json(prompt, fallback=None)
        if analysis and isinstance(analysis, dict):
            post["content_analysis"] = analysis
        else:
            post["content_analysis"] = {
                "hook_type": "unknown",
                "content_style": "unknown",
                "pacing": "unknown",
                "engagement_drivers": [],
                "why_it_works": "",
                "applicable_techniques": [],
            }

    return posts


# ---------------------------------------------------------------------------
# Relevance scoring (pure computation, no Gemini)
# ---------------------------------------------------------------------------

def compute_relevance_score(
    post: dict,
    brand_profile: dict,
    pillars: list[str],
) -> float:
    """Weighted relevance: 40% pillar match, 30% organic, 20% audience, 10% recency."""

    # 1. Pillar match (40%) -- keyword overlap between post text and pillars
    post_text = f"{post.get('title', '')} {post.get('description', '')}".lower()
    pillar_terms = [p.lower() for p in pillars]
    pillar_matches = sum(1 for term in pillar_terms if term in post_text)
    pillar_score = min(pillar_matches / max(len(pillar_terms), 1), 1.0) * 40

    # 2. Organic engagement (30%) -- normalize organic_score to 0-30
    organic = post.get("organic_score", 0)
    # Log-scale normalization (most scores are 0-1M range)
    import math
    organic_norm = min(math.log10(max(organic, 1)) / 6, 1.0) * 30

    # 3. Audience overlap (20%) -- check if post content matches audience interests
    audience_interests = brand_profile.get("audience_interests", []) if brand_profile else []
    interest_matches = sum(1 for interest in audience_interests if interest.lower() in post_text)
    audience_score = min(interest_matches / max(len(audience_interests), 1), 1.0) * 20

    # 4. Recency (10%) -- newer is better
    age_days = post.get("content_age_days", 30)
    recency_score = max(0, (30 - min(age_days, 30)) / 30) * 10

    return round(pillar_score + organic_norm + audience_score + recency_score, 2)


# ---------------------------------------------------------------------------
# Strategy document generation
# ---------------------------------------------------------------------------

async def generate_strategy_document(
    selected_posts: list[dict],
    brand_profile: dict,
    content_pillars: list[str],
    platform: str,
    memory: dict,
) -> StrategyDocument:
    """Synthesize selected trending posts + brand context into a content strategy."""

    # Build context from selected posts
    posts_summary = []
    for i, post in enumerate(selected_posts[:5], 1):
        analysis = post.get("content_analysis", {})
        posts_summary.append(
            f"{i}. \"{post.get('title', '')[:100]}\" by @{post.get('author_username', '')}\n"
            f"   Views: {post.get('view_count', 0):,} | "
            f"Hook: {analysis.get('hook_type', 'unknown')} | "
            f"Style: {analysis.get('content_style', 'unknown')}\n"
            f"   Why it works: {analysis.get('why_it_works', 'N/A')}"
        )

    posts_text = "\n".join(posts_summary)

    # Brand context
    brand_ctx = ""
    if brand_profile:
        tone = brand_profile.get("tone", "")
        interests = brand_profile.get("audience_interests", [])
        prefs = brand_profile.get("content_preferences", [])
        if tone:
            brand_ctx += f"Brand tone: {tone}\n"
        if interests:
            brand_ctx += f"Audience interests: {', '.join(interests)}\n"
        if prefs:
            brand_ctx += f"Content style preferences: {', '.join(prefs)}\n"
        core_problem = brand_profile.get("core_problem", "")
        if core_problem:
            brand_ctx += f"Core problem we solve: {core_problem}\n"
        differentiators = brand_profile.get("differentiators", [])
        if differentiators:
            brand_ctx += f"What makes us different: {', '.join(differentiators)}\n"
        customer_lang = brand_profile.get("customer_language", [])
        if customer_lang:
            brand_ctx += f"Language our audience uses: {', '.join(customer_lang)}\n"

    pillars_text = ", ".join(content_pillars) if content_pillars else "General"

    # Memory context (learning signals)
    memory_ctx = ""
    if memory:
        hook_prefs = memory.get("preferred_hook_styles", {})
        if hook_prefs:
            top_hook = max(hook_prefs, key=hook_prefs.get)
            memory_ctx += f"User's preferred hook style: {top_hook}\n"
        topics = memory.get("topics_published", [])
        if topics:
            memory_ctx += f"Topics to avoid (already covered): {', '.join(topics[:5])}\n"
        notes = memory.get("recurring_notes", [])
        if notes:
            memory_ctx += f"User's recurring notes: {', '.join(notes[:3])}\n"

    # Load targeted psychology sections (not the full 455-line file)
    from backend.prompts.skill_loader import load_skill_sections
    psychology_skill = load_skill_sections("psychology", [
        "Understanding Buyers & Human Psychology",
        "Influencing Behavior & Persuasion",
    ])

    prompt = f"""You are a master content strategist. Based on the user's selected trending posts and brand context, create a content strategy.

{"MARKETING PSYCHOLOGY FRAMEWORKS (Use these behavioral science principles to explain why this angle works!):" + chr(10) + psychology_skill if psychology_skill else ""}

SELECTED TRENDING POSTS:
{posts_text}

BRAND CONTEXT:
{brand_ctx}
Content pillars: {pillars_text}
Target platform: {platform}

{memory_ctx}

Return ONLY a JSON object:
{{
  "content_angle": "A specific, compelling content angle/title idea",
  "why_this_angle": "1-2 sentences explaining why this angle works based on the selected posts and brand",
  "target_platform": "{platform}",
  "recommended_format": {{
    "type": "short_form/slides/topic/talking_head",
    "length": "e.g. 30-45s or 5 slides",
    "hook_style": "question/number/story/contrarian/statement",
    "pacing": "fast/medium/slow",
    "cta_style": "follow/save/comment/share"
  }},
  "inspired_by": [
    {{"post_title": "title of inspiring post", "technique_borrowed": "what technique to use"}}
  ],
  "differentiation": "1-2 sentences on how to make this unique vs the inspiration"
}}"""

    result = await _gemini_json(prompt, fallback=None)

    if result and isinstance(result, dict):
        strategy = StrategyDocument(
            content_angle=result.get("content_angle", ""),
            why_this_angle=result.get("why_this_angle", ""),
            target_platform=result.get("target_platform", platform),
            recommended_format=result.get("recommended_format", {}),
            inspired_by=result.get("inspired_by", []),
            differentiation=result.get("differentiation", ""),
        )

        # Generate 2 alternative angles
        strategy.alternatives = await _generate_alternatives(strategy, posts_text, brand_ctx, platform)
        return strategy

    # Fallback: build basic strategy from selected posts
    if selected_posts:
        first = selected_posts[0]
        return StrategyDocument(
            content_angle=f"Inspired by: {first.get('title', '')[:80]}",
            why_this_angle="Based on your top-performing trending selection.",
            target_platform=platform,
            differentiation="Add your unique brand perspective.",
        )

    return StrategyDocument(target_platform=platform)


async def _generate_alternatives(
    primary: StrategyDocument,
    posts_text: str,
    brand_ctx: str,
    platform: str,
) -> list[dict]:
    """Generate 2 alternative strategy angles based on the primary strategy."""
    from backend.prompts.skill_loader import load_skill_sections

    content_strategy_ctx = load_skill_sections("content_strategy", [
        "Searchable vs Shareable",
        "Content Types",
    ])

    prompt = f"""Given this primary content strategy:
- Angle: {primary.content_angle}
- Why: {primary.why_this_angle}
- Platform: {platform}

And these trending posts for context:
{posts_text[:1500]}

{f"CONTENT STRATEGY FRAMEWORKS:{chr(10)}{content_strategy_ctx}" if content_strategy_ctx else ""}

{f"BRAND CONTEXT:{chr(10)}{brand_ctx}" if brand_ctx else ""}

Propose exactly 2 alternative content angles that are meaningfully different from the primary.
For each alternative, provide a hypothesis: "Because [observation from the data], we believe [this angle] will [expected outcome]."

Return ONLY a JSON array:
[
  {{
    "content_angle": "A different compelling angle",
    "hypothesis": "Because [observation], we believe [angle] will [outcome]",
    "differentiation": "How this differs from the primary angle"
  }},
  {{
    "content_angle": "Another different angle",
    "hypothesis": "Because [observation], we believe [angle] will [outcome]",
    "differentiation": "How this differs from the primary and first alternative"
  }}
]"""

    result = await _gemini_json(prompt, fallback=None)

    if result and isinstance(result, list):
        return [
            {
                "content_angle": alt.get("content_angle", ""),
                "hypothesis": alt.get("hypothesis", ""),
                "differentiation": alt.get("differentiation", ""),
            }
            for alt in result[:2]
            if isinstance(alt, dict)
        ]

    return []

```
