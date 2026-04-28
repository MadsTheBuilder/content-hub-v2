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

from google import genai

from backend.config import settings

logger = logging.getLogger(__name__)

_genai_client = None
_client_init_failed = False

def _get_genai_client():
    global _genai_client, _client_init_failed
    if _genai_client is not None:
        return _genai_client
    if _client_init_failed:
        return None
    if not settings.google_ai_studio_key:
        logger.warning("google_ai_studio_key not set -- scripting will use fallback.")
        _client_init_failed = True
        return None
    try:
        from google import genai
        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        return _genai_client
    except Exception:
        logger.exception("Failed to create GenAI client for scripting.")
        _client_init_failed = True
        return None

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

    client = _get_genai_client()

    # ---- Attempt 1: Gemini 2.0 Flash ----
    if client is not None:
        try:
            result = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            logger.info("Script generated with gemini-2.5-flash.")
            return {"script": result.text, "model_used": "gemini-2.5-flash", "success": True}
        except Exception:
            logger.warning("gemini-2.5-flash failed; trying fallback.", exc_info=True)

    # ---- Attempt 2: Gemini 1.5 Flash ----
    if client is not None:
        try:
            result = client.models.generate_content(
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
            import httpx
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

    client = _get_genai_client()

    # Attempt 1: Gemini Flash
    if client is not None:
        try:
            result = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            logger.info("Script refined with gemini-2.5-flash.")
            return {"script": result.text, "refined": True}
        except Exception:
            logger.warning("Refinement gemini-2.5-flash failed; trying lite.", exc_info=True)

    # Attempt 2: Gemini Flash Lite
    if client is not None:
        try:
            result = client.models.generate_content(
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
        # Adapt brand voice to platform conventions using static composition.
        # Intentionally NOT using a Gemini call here to avoid double LLM
        # latency — the scripting LLM receives the adapted voice and does
        # the heavy lifting. This mirrors adapt_voice_to_platform()'s
        # no-API-key path (see code review item 2A-4b / 2A-3).
        from backend.content.platform_adapter import get_platform_rules as _get_voice_rules
        _voice_rules = _get_voice_rules(platform)
        _voice_parts = []
        if _voice_rules.get("tone"):
            _voice_parts.append(f"Tone for {platform}: {_voice_rules['tone']}.")
        if _voice_rules.get("script_style"):
            _voice_parts.append(f"Script style: {_voice_rules['script_style']}")
        adapted_voice = (
            f"{brand_voice}\n\n{' '.join(_voice_parts)}"
            if _voice_parts else brand_voice
        )
        sections.append(f"\n## Brand Voice (adapted for {platform})\n{adapted_voice}")

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

    # NOTE: Redundant bare platform label removed (code review item 2A-4).
    # The structured Platform Strategy Rules section below provides platform
    # name plus detailed rules, making a standalone label unnecessary bloat.

    # -- Platform-specific strategy rules (from platform_adapter knowledge base) ---
    from backend.content.platform_adapter import get_platform_rules
    p_rules = get_platform_rules(platform)
    if p_rules:
        rules_lines = ["\n## Platform Strategy Rules"]
        if p_rules.get("ideal_length"):
            rules_lines.append(f"Ideal content length: {p_rules['ideal_length']}")
        if p_rules.get("hook_window"):
            rules_lines.append(f"Hook must land within: {p_rules['hook_window']}")
        if p_rules.get("tone"):
            rules_lines.append(f"Platform tone: {p_rules['tone']}")
        if p_rules.get("cta_style"):
            rules_lines.append(f"CTA style: {p_rules['cta_style']}")
        if p_rules.get("script_style"):
            rules_lines.append(f"Script style guide: {p_rules['script_style']}")
        if p_rules.get("best_practices"):
            rules_lines.append(f"Best practices: {'; '.join(p_rules['best_practices'])}")
        sections.append("\n".join(rules_lines))

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

    # -- Expert Marketing Skills (copywriting always + type-specific social content) --
    from backend.prompts.skill_loader import get_scripting_skill, load_skill_sections

    # 1. Core copywriting principles — applied to ALL content types.
    #    Targeted sections only (~2KB) instead of full file (~7.8KB) to
    #    manage prompt token spend (code review item 2C-3).
    copywriting_text = load_skill_sections("copywriting", [
        "Copywriting Principles",
        "Writing Style Rules",
        "CTA Copy Guidelines",
    ])
    if copywriting_text:
        sections.append(f"\n## Core Copywriting Principles\n{copywriting_text}")

    # 2. Type-specific social content guidance (short_form/talking_head/slides/topic all get social-content.md)
    skill_text = get_scripting_skill(content_type)
    if skill_text and skill_text != copywriting_text:  # avoid duplication if maps align
        sections.append(f"\n## Platform Content Execution Guide\n{skill_text}")

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
