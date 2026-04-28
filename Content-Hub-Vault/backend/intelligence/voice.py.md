---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/voice.py"
category: "Content Hub Source Code"
---

# voice.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
"""
Voice Engine -- parses raw workflow inputs into actionable intelligence.

Transforms:
 - Competitors (raw handles) -> platform-specific scrape targets
 - Brand persona (raw text) -> structured BrandProfile via Gemini
 - Content pillars (raw labels) -> expanded search terms via Gemini

The resulting VoiceConfig feeds into apify_search_config (scraping)
and brand_profile (scripting/synthesis).
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field, asdict
from typing import Any

from backend.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class BrandProfile:
    audience_age_range: str = ""
    audience_interests: list[str] = field(default_factory=list)
    content_preferences: list[str] = field(default_factory=list)
    energy: str = "medium"
    tone: str = ""
    mentioned_accounts: list[str] = field(default_factory=list)
    # Enriched fields (from product-marketing-context template)
    core_problem: str = ""
    differentiators: list[str] = field(default_factory=list)
    customer_language: list[str] = field(default_factory=list)
    objections: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CompetitorConfig:
    profiles: dict[str, list[str]] = field(default_factory=dict)
    # {"tiktok": ["alexfitness", "yogawithserena"], "youtube": [...]}


@dataclass
class PillarConfig:
    pillars: list[str] = field(default_factory=list)
    expanded_terms: dict[str, list[str]] = field(default_factory=dict)
    scrape_config: dict[str, dict] = field(default_factory=dict)


@dataclass
class VoiceConfig:
    competitor_config: CompetitorConfig = field(default_factory=CompetitorConfig)
    brand_profile: BrandProfile = field(default_factory=BrandProfile)
    pillar_config: PillarConfig = field(default_factory=PillarConfig)


# ---------------------------------------------------------------------------
# Gemini client (lazy init, same pattern as research_service.py)
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
        logger.warning("google_ai_studio_key not set -- Voice Engine will use defaults.")
        _client_init_failed = True
        return None
    try:
        from google import genai
        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        return _genai_client
    except Exception:
        logger.exception("Failed to create GenAI client for Voice Engine.")
        _client_init_failed = True
        return None


async def _gemini_json(prompt: str, fallback: Any = None) -> Any:
    """Call Gemini with Flash -> Flash-Lite fallback, parse JSON response."""
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
            # Strip markdown code fences if present
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*", "", text)
                text = re.sub(r"\s*```$", "", text)
            return json.loads(text)
        except Exception:
            logger.warning("Voice Engine: %s failed, trying next model.", model_name)
            continue

    logger.error("Voice Engine: all Gemini models failed, returning fallback.")
    return fallback


# ---------------------------------------------------------------------------
# Competitor parsing (no Gemini needed -- string parsing)
# ---------------------------------------------------------------------------

HANDLE_PATTERN = re.compile(r"@([\w.]+)")


def parse_competitors(competitors: list[str], platforms: list[str]) -> CompetitorConfig:
    """Extract usernames from competitor list and assign to each platform.

    Input can be: ["@alexfitness", "yogawithserena", "GymShark"]
    Strips @ prefix, assigns each username to every selected platform.
    """
    usernames: list[str] = []
    for entry in competitors:
        entry = entry.strip()
        if not entry:
            continue
        # Extract @handle or use the raw string
        match = HANDLE_PATTERN.search(entry)
        if match:
            usernames.append(match.group(1))
        else:
            # Clean up: lowercase, strip whitespace
            cleaned = entry.lstrip("@").strip()
            if cleaned:
                usernames.append(cleaned)

    # Deduplicate preserving order
    seen = set()
    unique = []
    for u in usernames:
        lower = u.lower()
        if lower not in seen:
            seen.add(lower)
            unique.append(u)

    profiles = {p: list(unique) for p in platforms}
    return CompetitorConfig(profiles=profiles)


# ---------------------------------------------------------------------------
# Brand persona parsing (Gemini)
# ---------------------------------------------------------------------------

async def parse_brand_persona(brand_voice: str) -> BrandProfile:
    """Use Gemini to extract structured audience/style signals from persona text.
    Falls back to regex-only extraction if Gemini unavailable."""

    # Always extract @mentions via regex
    mentioned = HANDLE_PATTERN.findall(brand_voice)

    if not brand_voice.strip():
        return BrandProfile(mentioned_accounts=[f"@{m}" for m in mentioned])

    prompt = f"""Analyze this brand persona description and extract structured data.
Return ONLY a JSON object with these exact keys:
{{
  "audience_age_range": "e.g. 20-35 or empty string if not mentioned",
  "audience_interests": ["list of interests/topics the audience cares about"],
  "content_preferences": ["list of content style preferences e.g. motivational, educational, entertaining"],
  "energy": "low/medium/high",
  "tone": "brief description of the tone e.g. motivational but grounded",
  "core_problem": "the main problem this brand/creator solves for their audience (1 sentence, or empty string)",
  "differentiators": ["2-4 things that make this brand unique vs competitors"],
  "customer_language": ["3-5 phrases or words the target audience actually uses when talking about this topic"],
  "objections": ["2-3 common hesitations or objections the audience might have"]
}}

Brand persona text:
\"\"\"{brand_voice}\"\"\"
"""

    result = await _gemini_json(prompt, fallback=None)

    if result and isinstance(result, dict):
        return BrandProfile(
            audience_age_range=result.get("audience_age_range", ""),
            audience_interests=result.get("audience_interests", []),
            content_preferences=result.get("content_preferences", []),
            energy=result.get("energy", "medium"),
            tone=result.get("tone", ""),
            mentioned_accounts=[f"@{m}" for m in mentioned],
            core_problem=result.get("core_problem", ""),
            differentiators=result.get("differentiators", []),
            customer_language=result.get("customer_language", []),
            objections=result.get("objections", []),
        )

    # Fallback: basic profile from text
    return BrandProfile(
        tone=brand_voice[:100] if brand_voice else "",
        mentioned_accounts=[f"@{m}" for m in mentioned],
    )


# ---------------------------------------------------------------------------
# Content pillar expansion (Gemini)
# ---------------------------------------------------------------------------

async def process_content_pillars(
    pillars: list[str],
    brand_profile: BrandProfile,
    platforms: list[str],
) -> PillarConfig:
    """Expand each pillar into 5-8 search-optimized terms via Gemini."""

    if not pillars:
        return PillarConfig()

    audience_context = ""
    if brand_profile.audience_interests:
        audience_context = f"Target audience interests: {', '.join(brand_profile.audience_interests)}. "
    if brand_profile.tone:
        audience_context += f"Brand tone: {brand_profile.tone}. "

    prompt = f"""You are a social media research assistant.
{audience_context}
For each content pillar below, generate 5-8 search terms that would find trending content on TikTok, Instagram, and YouTube. Include hashtags (without #), keyword phrases, and topic variations.

Return ONLY a JSON object where each key is the pillar name and the value is a list of search terms.

Pillars: {json.dumps(pillars)}
"""

    result = await _gemini_json(prompt, fallback=None)

    expanded_terms: dict[str, list[str]] = {}
    if result and isinstance(result, dict):
        for pillar in pillars:
            # Try exact key match, then case-insensitive
            terms = result.get(pillar)
            if not terms:
                for k, v in result.items():
                    if k.lower() == pillar.lower():
                        terms = v
                        break
            expanded_terms[pillar] = terms if isinstance(terms, list) else [pillar]
    else:
        # Fallback: use raw pillar names as search terms
        for pillar in pillars:
            expanded_terms[pillar] = [pillar.lower()]

    # Build platform-specific scrape config from expanded terms
    all_terms = []
    for terms in expanded_terms.values():
        all_terms.extend(terms)
    # Deduplicate
    all_terms = list(dict.fromkeys(all_terms))

    scrape_config: dict[str, dict] = {}
    for platform in platforms:
        if platform in ("tiktok", "instagram"):
            scrape_config[platform] = {"hashtags": all_terms[:15]}
        elif platform in ("youtube", "linkedin", "twitter"):
            scrape_config[platform] = {"keywords": all_terms[:10]}

    return PillarConfig(
        pillars=pillars,
        expanded_terms=expanded_terms,
        scrape_config=scrape_config,
    )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

async def build_voice_config(
    brand_voice: str,
    competitors: list[str],
    pillars: list[str],
    platforms: list[str],
) -> VoiceConfig:
    """Main entry point -- builds complete VoiceConfig from raw workflow inputs."""

    competitor_config = parse_competitors(competitors, platforms)
    brand_profile = await parse_brand_persona(brand_voice)

    # Add accounts mentioned in persona to competitor scraping
    for account in brand_profile.mentioned_accounts:
        username = account.lstrip("@")
        for platform in platforms:
            if platform in competitor_config.profiles:
                if username not in competitor_config.profiles[platform]:
                    competitor_config.profiles[platform].append(username)
            else:
                competitor_config.profiles[platform] = [username]

    pillar_config = await process_content_pillars(pillars, brand_profile, platforms)

    return VoiceConfig(
        competitor_config=competitor_config,
        brand_profile=brand_profile,
        pillar_config=pillar_config,
    )

```
