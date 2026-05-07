---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/scripting.py"
category: "Content Hub Source Code"
---

# scripting.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
"""
Content scripting module.

Generates platform-specific content scripts by combining a structured prompt
with research context (trending data, few-shot examples, a narrative research
brief, and creator memory / preferences).

The research context is provided by ``backend.research.research_service``.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx
from google import genai

from backend.config import settings

logger = logging.getLogger(__name__)

gemini_client = genai.Client(api_key=settings.google_ai_studio_key)

CONTENT_TYPE_PROMPTS = {
    "slides": (
        "Create a data-driven carousel script with 1-5 slides. Each slide "
        "should have a headline (max 8 words) and body text (max 30 words). "
        "You may optionally provide 'accent_color' (hex) and 'bg_gradient' (CSS gradient) "
        "to match the brand vibe. "
        'Return as JSON array: [{"slide": 1, "headline": "...", "body": "...", "accent_color": "...", "bg_gradient": "..."}]'
    ),
    "topic": (
        "Create an educational carousel script with 3-8 slides. First slide "
        "is the hook. Last slide is the CTA. Each slide: headline + body "
        "(max 40 words). Return as JSON array."
    ),
    "short_form": (
        "Write a short-form video script (15-30 seconds). Include: hook "
        "(first 3 seconds), body, CTA. Format: HOOK: ... BODY: ... CTA: ... "
        "Keep under 180 words total."
    ),
    "talking_head": (
        "Write a talking head video script with: 1) Script (what to say, "
        "with [PAUSE] markers), 2) Shot list (camera angles/movements), "
        "3) On-screen text overlays. Format as sections: SCRIPT: ... "
        "SHOT_LIST: ... ONSCREEN_TEXT: ..."
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate_script(
    content_type: str,
    topic: str,
    brand_voice: str,
    content_pillars: list[str],
    research_context: dict[str, Any],
    memory: dict[str, Any],
    platform: str,
    strategy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a content script using Gemini with Anthropic fallback.

    *research_context* is the dict returned by
    ``research_service.get_full_research_context`` and may include a
    ``research_brief`` key (narrative string).

    Returns a dict with ``script``, ``model_used``, and ``success`` keys.
    """
    prompt = _build_prompt(
        content_type,
        topic,
        brand_voice,
        content_pillars,
        research_context,
        memory,
        platform,
        strategy=strategy,
    )

    # ---- Attempt 1: Gemini 2.0 Flash ----
    try:
        result = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        logger.info("Script generated with gemini-2.5-flash.")
        return {"script": result.text, "model_used": "gemini-2.5-flash", "success": True}
    except Exception:
        logger.warning("gemini-2.5-flash failed; trying fallback.", exc_info=True)

    # ---- Attempt 2: Gemini 1.5 Flash ----
    try:
        result = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        logger.info("Script generated with gemini-2.5-flash-lite.")
        return {"script": result.text, "model_used": "gemini-2.5-flash-lite", "success": True}
    except Exception:
        logger.warning("gemini-2.5-flash-lite failed; trying Anthropic.", exc_info=True)

    # ---- Attempt 3: Anthropic Claude ----
    if settings.anthropic_api_key:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": settings.anthropic_api_key,
                        "anthropic-version": "2023-06-01",
                        "content-type": "application/json",
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 2000,
                        "messages": [{"role": "user", "content": prompt}],
                    },
                    timeout=60,
                )
                data = response.json()
                logger.info("Script generated with claude-sonnet.")
                return {
                    "script": data["content"][0]["text"],
                    "model_used": "claude-sonnet",
                    "success": True,
                }
        except Exception:
            logger.warning("Anthropic fallback failed.", exc_info=True)

    # ---- Last resort: placeholder ----
    logger.warning("All LLM providers failed; returning placeholder script.")
    return {
        "script": _placeholder_script(content_type, topic),
        "model_used": "placeholder",
        "success": True,
    }


# ---------------------------------------------------------------------------
# Post-generation refinement
# ---------------------------------------------------------------------------

async def refine_script(
    script_text: str,
    content_type: str,
    brand_voice: str,
    platform: str,
) -> dict[str, Any]:
    """Apply copy-editing quality pass to a generated script.

    Uses condensed Seven Sweeps (Clarity, Voice/Tone, So What, Heightened
    Emotion) + quick-pass word/sentence checks. Returns the refined script
    or the original on failure.
    """
    from backend.prompts.skill_loader import load_skill

    editing_guide = load_skill("copy_editing")
    if not editing_guide:
        return {"script": script_text, "refined": False}

    prompt = (
        f"You are a copy editor reviewing a {content_type} script for {platform}.\n"
        f"Brand voice: {brand_voice}\n\n"
        f"Apply these editing passes to improve the script:\n\n"
        f"{editing_guide}\n\n"
        f"---\n\n"
        f"SCRIPT TO EDIT:\n{script_text}\n\n"
        f"Return ONLY the improved script in the exact same format. "
        f"Do not add commentary, labels, or explanations. "
        f"Do not change the structure or format. "
        f"Only improve clarity, voice consistency, emotional impact, and word choice."
    )

    # Attempt 1: Gemini Flash
    try:
        result = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        logger.info("Script refined with gemini-2.5-flash.")
        return {"script": result.text, "refined": True}
    except Exception:
        logger.warning("Refinement gemini-2.5-flash failed; trying lite.", exc_info=True)

    # Attempt 2: Gemini Flash Lite
    try:
        result = gemini_client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
        )
        logger.info("Script refined with gemini-2.5-flash-lite.")
        return {"script": result.text, "refined": True}
    except Exception:
        logger.warning("Refinement failed; returning original script.", exc_info=True)

    return {"script": script_text, "refined": False}


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def _build_prompt(
    content_type: str,
    topic: str,
    brand_voice: str,
    pillars: list[str],
    research: dict[str, Any],
    memory: dict[str, Any],
    platform: str,
    strategy: dict[str, Any] | None = None,
) -> str:
    """Assemble the full LLM prompt from all available context."""

    sections: list[str] = [
        f"You are a content creation expert. Generate {content_type} content.",
        f"\n## Topic\n{topic}",
    ]

    # -- Approved content strategy (from synthesis step) ----------------------
    if strategy:
        angle = strategy.get("content_angle", "")
        why = strategy.get("why_this_angle", "")
        diff = strategy.get("differentiation", "")
        fmt = strategy.get("recommended_format", {})
        inspired = strategy.get("inspired_by", [])
        user_notes = strategy.get("user_notes", "")
        strategy_lines = ["\n## Approved Content Strategy"]
        if angle:
            strategy_lines.append(f"Content angle: {angle}")
        if why:
            strategy_lines.append(f"Why this works: {why}")
        if diff:
            strategy_lines.append(f"Differentiation: {diff}")
        if fmt:
            strategy_lines.append(
                f"Format: {fmt.get('type', content_type)}, {fmt.get('length', '')}, "
                f"hook={fmt.get('hook_style', '')}, pacing={fmt.get('pacing', '')}, "
                f"cta={fmt.get('cta_style', '')}"
            )
        if inspired:
            techniques = "; ".join(f"{i.get('technique_borrowed', '')}" for i in inspired[:3])
            strategy_lines.append(f"Techniques to use: {techniques}")
        if user_notes:
            strategy_lines.append(f"User notes: {user_notes}")
        strategy_lines.append("Follow this strategy closely.")
        sections.append("\n".join(strategy_lines))

    if brand_voice:
        sections.append(f"\n## Brand Voice\n{brand_voice}")

    # -- Brand Positioning (enriched fields from Voice Engine) ----------------
    brand_profile = research.get("brand_profile") or {}
    positioning_lines = []
    if brand_profile.get("core_problem"):
        positioning_lines.append(f"Core problem we solve: {brand_profile['core_problem']}")
    if brand_profile.get("differentiators"):
        positioning_lines.append(f"What makes us different: {', '.join(brand_profile['differentiators'])}")
    if brand_profile.get("customer_language"):
        positioning_lines.append(f"Language our audience uses: {', '.join(brand_profile['customer_language'])}")
    if positioning_lines:
        sections.append("\n## Brand Positioning\n" + "\n".join(positioning_lines))

    if pillars:
        sections.append(f"\n## Content Pillars\n{', '.join(pillars)}")

    sections.append(f"\n## Target Platform\n{platform}")

    # -- Research brief (narrative, from Gemini analysis of trends) ----------
    research_brief = research.get("research_brief")
    if research_brief:
        sections.append(
            f"\n## Research Brief (analyst summary of this week's landscape)\n"
            f"{research_brief}"
        )

    # -- Trending context (specific items from vector search) ----------------
    trending = research.get("trending_context")
    if trending:
        trending_text = "\n".join(
            f"- {t.get('content_text', t.get('title', ''))[:150]}"
            for t in trending[:5]
        )
        sections.append(
            f"\n## What's Trending in This Niche Right Now\n{trending_text}"
        )

    # -- Few-shot examples (published scripts that matched) -----------------
    examples = research.get("few_shot_examples")
    if examples:
        examples_text = "\n---\n".join(
            t.get("content_text", "")[:500] for t in examples[:3]
        )
        sections.append(
            f"\n## Examples of Content This Creator Has Published "
            f"(match this style)\n{examples_text}"
        )

    # -- Memory-driven personalisation --------------------------------------
    if memory.get("preferred_hook_styles"):
        hooks = memory["preferred_hook_styles"]
        top_hook = max(hooks, key=hooks.get) if hooks else "question"
        sections.append(
            f"\n## Style Preference\n"
            f"This creator prefers '{top_hook}' style hooks. "
            f"Prioritize this format."
        )

    if memory.get("avg_script_length", {}).get(content_type):
        avg_len = memory["avg_script_length"][content_type]
        sections.append(
            f"\n## Length Preference\nTarget approximately {avg_len} words."
        )

    # -- Topics to avoid (from memory) --------------------------------------
    topics_published = memory.get("topics_published", [])
    if topics_published:
        avoid_text = ", ".join(topics_published[:10])
        sections.append(
            f"\n## Topics Already Covered (avoid repeating)\n{avoid_text}"
        )

    # -- Format instructions ------------------------------------------------
    sections.append(
        f"\n## Format Instructions\n"
        f"{CONTENT_TYPE_PROMPTS.get(content_type, '')}"
    )

    # -- Expert Marketing Skills --------------------------------------------
    from backend.prompts.skill_loader import get_scripting_skill
    skill_text = get_scripting_skill(content_type)
    if skill_text:
        sections.append(f"\n## Expert Copywriting / Content Instructions\n{skill_text}")

    return "\n".join(s for s in sections if s)


# ---------------------------------------------------------------------------
# Placeholder fallback
# ---------------------------------------------------------------------------

def _placeholder_script(content_type: str, topic: str) -> str:
    """Return a minimal placeholder when no LLM is available."""
    if content_type == "slides":
        return (
            '[{"slide": 1, "headline": "' + topic + '", '
            '"body": "Key insight about this topic"}, '
            '{"slide": 2, "headline": "The Data", '
            '"body": "Supporting evidence goes here"}, '
            '{"slide": 3, "headline": "Take Action", '
            '"body": "What to do next"}]'
        )
    if content_type == "short_form":
        return (
            f"HOOK: Did you know this about {topic}?\n"
            f"BODY: Here's what most people get wrong...\n"
            f"CTA: Follow for more insights."
        )
    if content_type == "talking_head":
        return (
            f"SCRIPT: Hey everyone, today we're talking about {topic}. "
            f"[PAUSE] Here's what you need to know...\n"
            f"SHOT_LIST: Medium shot, eye level\n"
            f"ONSCREEN_TEXT: {topic}"
        )
    return f"[{topic}] - Content placeholder. Replace with generated content."

```
