---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/research/research_service.py"
category: "Content Hub Source Code"
---

# research_service.py

**Description:** Research layer, web scraping integrations (Apify), and RAG/pgvector operations.

---

```py
"""
Research service -- orchestration layer that sits between the RAG module and
the content scripting module.

Responsibilities:
 - Combine RAG vector-search results with raw trending data and publication
   memory into a single research context.
 - Generate a narrative *research brief* via Gemini that the scripting prompt
   can consume directly.
 - Provide a one-call entry point (``get_full_research_context``) that content
   generation uses.
"""

from __future__ import annotations

import logging
from typing import Any

from backend.config import settings
from backend.database import get_supabase
from backend.research.rag import get_research_context, search_similar

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini generation client (lazy, same pattern as rag.py)
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
        logger.warning(
            "google_ai_studio_key not set -- research brief generation "
            "will be skipped."
        )
        _client_init_failed = True
        return None

    try:
        from google import genai  # noqa: WPS433

        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        return _genai_client
    except Exception:
        logger.exception("Failed to create GenAI client for research_service.")
        _client_init_failed = True
        return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_memory(workflow_id: str) -> dict[str, Any]:
    """Fetch publication memory for the workflow, returning {} on failure."""
    try:
        sb = get_supabase()
        result = (
            sb.table("content_publication_memory")
            .select("*")
            .eq("workflow_id", workflow_id)
            .single()
            .execute()
        )
        return result.data or {}
    except Exception:
        logger.exception(
            "Failed to load publication memory for workflow %s.", workflow_id
        )
        return {}


def _get_raw_trending(workflow_id: str, limit: int = 20) -> list[dict]:
    """Fetch the top trending rows directly from the DB (no embeddings)."""
    try:
        sb = get_supabase()
        result = (
            sb.table("trending_content")
            .select("*")
            .eq("workflow_id", workflow_id)
            .order("organic_score", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception:
        logger.exception(
            "Failed to load raw trending data for workflow %s.", workflow_id
        )
        return []


def _get_recent_published(workflow_id: str, limit: int = 10) -> list[dict]:
    """Fetch the most recently published scripts for the workflow."""
    try:
        sb = get_supabase()
        result = (
            sb.table("content_items")
            .select("id, title, content_type, platform, script_text, created_at")
            .eq("workflow_id", workflow_id)
            .eq("status", "posted")
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return result.data or []
    except Exception:
        logger.exception(
            "Failed to load published scripts for workflow %s.", workflow_id
        )
        return []


# ---------------------------------------------------------------------------
# Research brief generation
# ---------------------------------------------------------------------------

_BRIEF_SYSTEM_PROMPT = """\
You are a social-media research analyst. Given the raw data below, produce a
concise *research brief* that a content creator can use when scripting their
next piece. The brief MUST include exactly these three sections:

## Top Hooks This Week
List the 3-5 most effective hook patterns you see in the trending content.
For each, give a short label and one concrete example from the data.

## Content Angles Performing Well
List 3-5 content angles / themes that are getting high organic scores.
Explain briefly why each is resonating.

## Topics to Avoid
List topics that this creator has already covered recently OR that show
declining engagement. Explain why each should be avoided for now.

Keep the brief under 600 words. Be specific -- reference actual titles and
scores from the data. Do not invent data that was not provided.
"""


def _build_brief_user_prompt(
    trending: list[dict],
    published: list[dict],
    memory: dict[str, Any],
    topic_hint: str,
    content_type: str,
) -> str:
    """Assemble the user-side prompt for the research brief."""
    sections: list[str] = []

    # Trending data
    if trending:
        lines = []
        for t in trending[:15]:
            title = t.get("content_text", t.get("title", ""))[:120]
            score = t.get("organic_score", t.get("metadata", {}).get("organic_score", "?"))
            platform = t.get("platform", t.get("metadata", {}).get("platform", "?"))
            lines.append(f"- [{platform}] (score {score}) {title}")
        sections.append("### Trending Content\n" + "\n".join(lines))

    # Recently published (what the creator already covered)
    if published:
        lines = []
        for p in published[:10]:
            lines.append(
                f"- [{p.get('platform', '?')}] {p.get('title', '')[:100]} "
                f"({p.get('content_type', '?')})"
            )
        sections.append(
            "### Creator's Recent Publications\n" + "\n".join(lines)
        )

    # Memory insights
    if memory:
        mem_lines = []
        topics_published = memory.get("topics_published", [])
        if topics_published:
            mem_lines.append(
                "Recent topics: " + ", ".join(topics_published[:10])
            )
        hooks = memory.get("preferred_hook_styles", {})
        if hooks:
            top_hooks = sorted(hooks, key=hooks.get, reverse=True)[:3]
            mem_lines.append("Preferred hook styles: " + ", ".join(top_hooks))
        if mem_lines:
            sections.append(
                "### Creator Memory / Preferences\n" + "\n".join(mem_lines)
            )

    # What the creator is thinking about
    if topic_hint:
        sections.append(
            f"### Topic the creator is considering\n{topic_hint} "
            f"(format: {content_type})"
        )

    return "\n\n".join(sections) if sections else "(No data available.)"


async def generate_research_brief(
    workflow_id: str,
    topic: str,
    content_type: str,
    *,
    trending: list[dict] | None = None,
    published: list[dict] | None = None,
    memory: dict[str, Any] | None = None,
) -> str:
    """Generate a narrative research brief using Gemini.

    Returns the brief text, or a short fallback message if generation fails
    (never raises).
    """
    # Gather data if not provided
    if trending is None:
        trending = _get_raw_trending(workflow_id)
    if published is None:
        published = _get_recent_published(workflow_id)
    if memory is None:
        memory = _get_memory(workflow_id)

    user_prompt = _build_brief_user_prompt(
        trending, published, memory, topic, content_type
    )

    client = _get_genai_client()
    if client is None:
        logger.info(
            "GenAI client unavailable; returning minimal research brief."
        )
        return _fallback_brief(trending, published, memory)

    # Try primary model, then fallback
    for model in ("gemini-2.5-flash", "gemini-2.5-flash-lite"):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {"role": "user", "parts": [{"text": _BRIEF_SYSTEM_PROMPT + "\n\n" + user_prompt}]},
                ],
            )
            brief = response.text
            if brief and len(brief.strip()) > 50:
                logger.info(
                    "Research brief generated (%d chars) using %s.",
                    len(brief),
                    model,
                )
                return brief
        except Exception:
            logger.exception(
                "Research brief generation failed with model %s.", model
            )

    logger.warning("All models failed; returning fallback brief.")
    return _fallback_brief(trending, published, memory)


def _fallback_brief(
    trending: list[dict],
    published: list[dict],
    memory: dict[str, Any],
) -> str:
    """Produce a plain-text summary when Gemini is unavailable."""
    parts: list[str] = ["## Research Brief (auto-generated fallback)\n"]

    if trending:
        parts.append("### Top Trending")
        for t in trending[:5]:
            title = t.get("content_text", t.get("title", ""))[:100]
            score = t.get("organic_score", t.get("metadata", {}).get("organic_score", ""))
            parts.append(f"- (score {score}) {title}")

    topics_published = (memory or {}).get("topics_published", [])
    if topics_published:
        parts.append("\n### Recently Covered Topics (consider avoiding)")
        for tp in topics_published[:5]:
            parts.append(f"- {tp}")

    if not trending and not topics_published:
        parts.append(
            "No trending data or publication history available yet. "
            "Run a scrape job first."
        )

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Main entry point for content generation
# ---------------------------------------------------------------------------

async def get_full_research_context(
    workflow_id: str,
    topic: str,
    content_type: str,
) -> dict[str, Any]:
    """One-call entry point consumed by the scripting module.

    Returns a dict with:
      - ``trending_context``:  list of relevant trending items (from RAG)
      - ``few_shot_examples``: list of similar published scripts (from RAG)
      - ``research_brief``:    narrative brief string (from Gemini)
      - ``memory``:            raw publication memory dict
      - ``raw_trending``:      top trending items from DB (un-vectorised)
    """
    # Kick off parallel-ish data fetching (sync DB calls + async RAG)
    memory = _get_memory(workflow_id)
    raw_trending = _get_raw_trending(workflow_id, limit=15)
    published = _get_recent_published(workflow_id, limit=10)

    # RAG vector search
    rag_context = await get_research_context(workflow_id, topic, content_type)

    # Narrative brief
    brief = await generate_research_brief(
        workflow_id,
        topic,
        content_type,
        trending=rag_context.get("trending_context") or raw_trending,
        published=published,
        memory=memory,
    )

    return {
        "trending_context": rag_context.get("trending_context", []),
        "few_shot_examples": rag_context.get("few_shot_examples", []),
        "research_brief": brief,
        "memory": memory,
        "raw_trending": raw_trending,
    }

```
