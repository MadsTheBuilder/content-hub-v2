---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/research/rag.py"
category: "Content Hub Source Code"
---

# rag.py

**Description:** Research layer, web scraping integrations (Apify), and RAG/pgvector operations.

---

```py
"""
RAG module for Content Hub.

Handles embedding generation, vector storage, similarity search, and
embedding lifecycle management using Gemini text-embedding-004 and
Supabase pgvector.
"""

from __future__ import annotations

import asyncio
import hashlib
import logging
import time
from typing import Any

from backend.config import settings
from backend.database import get_supabase

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Gemini client (lazy, so the module can be imported even without a key)
# ---------------------------------------------------------------------------

_genai_client = None
_client_init_failed = False

EMBEDDING_MODEL = "gemini-embedding-2-preview"
EMBEDDING_DIMENSION = 1536

# Gemini free-tier rate limits (requests per minute / per day)
_RATE_LIMIT_RPM = 1500
_RATE_LIMIT_BATCH_SIZE = 20
_RATE_LIMIT_DELAY_SECONDS = 1.5  # pause between batches to stay safe


def _get_genai_client():
    """Return the Google GenAI client, creating it on first call.

    Returns None (and logs a warning once) when the API key is missing or
    the import fails.
    """
    global _genai_client, _client_init_failed

    if _genai_client is not None:
        return _genai_client

    if _client_init_failed:
        return None

    if not settings.google_ai_studio_key:
        logger.warning(
            "google_ai_studio_key is not configured -- embedding features "
            "are disabled. Set the key in .env or backend/config.py."
        )
        _client_init_failed = True
        return None

    try:
        from google import genai  # noqa: WPS433 (nested import is intentional)
        _genai_client = genai.Client(api_key=settings.google_ai_studio_key)
        logger.info("Google GenAI client initialised successfully.")
        return _genai_client
    except Exception:
        logger.exception("Failed to initialise Google GenAI client.")
        _client_init_failed = True
        return None


# ---------------------------------------------------------------------------
# Low-level embedding helpers
# ---------------------------------------------------------------------------

async def embed_text(
    text: str, task_type: str = "RETRIEVAL_DOCUMENT"
) -> list[float]:
    """Embed a single text string. Returns a 1536-dim vector.

    Raises ``RuntimeError`` if the GenAI client is unavailable.
    """
    client = _get_genai_client()
    if client is None:
        raise RuntimeError(
            "Google AI Studio key is missing or invalid -- cannot generate "
            "embeddings."
        )

    try:
        from google.genai import types

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[text],
            config=types.EmbedContentConfig(
                task_type=task_type,
                output_dimensionality=EMBEDDING_DIMENSION,
            ),
        )
        return response.embeddings[0].values
    except Exception:
        logger.exception("embed_text failed for text (len=%d)", len(text))
        raise


async def embed_image(
    image_bytes: bytes, mime_type: str = "image/png"
) -> list[float]:
    """Embed an image. Returns a 1536-dim vector in the same space as text.

    Raises ``RuntimeError`` if the GenAI client is unavailable.
    """
    client = _get_genai_client()
    if client is None:
        raise RuntimeError(
            "Google AI Studio key is missing or invalid -- cannot generate "
            "embeddings."
        )

    try:
        from google.genai import types

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=types.Content(
                parts=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type)]
            ),
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIMENSION,
            ),
        )
        return response.embeddings[0].values
    except Exception:
        logger.exception("embed_image failed (size=%d bytes)", len(image_bytes))
        raise


async def embed_texts_batch(
    texts: list[str],
    *,
    batch_size: int = _RATE_LIMIT_BATCH_SIZE,
    delay: float = _RATE_LIMIT_DELAY_SECONDS,
) -> list[list[float]]:
    """Embed multiple texts with automatic batching and rate limiting.

    Returns a list of embedding vectors in the same order as *texts*.
    """
    client = _get_genai_client()
    if client is None:
        raise RuntimeError(
            "Google AI Studio key is missing or invalid -- cannot generate "
            "embeddings."
        )

    all_embeddings: list[list[float]] = []
    total = len(texts)

    for start in range(0, total, batch_size):
        batch = texts[start : start + batch_size]
        batch_num = start // batch_size + 1
        total_batches = (total + batch_size - 1) // batch_size
        logger.debug(
            "Embedding batch %d/%d (%d texts)", batch_num, total_batches, len(batch)
        )

        try:
            from google.genai import types

            response = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=EMBEDDING_DIMENSION,
                ),
            )
            all_embeddings.extend(emb.values for emb in response.embeddings)
        except Exception:
            logger.exception(
                "Batch embedding failed (batch %d/%d). Falling back to "
                "one-by-one embedding for this batch.",
                batch_num,
                total_batches,
            )
            for text in batch:
                try:
                    single = await embed_text(text)
                    all_embeddings.append(single)
                except Exception:
                    logger.error(
                        "Single-text embedding failed; inserting zero vector "
                        "as placeholder."
                    )
                    all_embeddings.append([0.0] * EMBEDDING_DIMENSION)

        # Rate-limit pause between batches (skip after the last batch)
        if start + batch_size < total:
            await asyncio.sleep(delay)

    return all_embeddings


# ---------------------------------------------------------------------------
# Content hash for deduplication
# ---------------------------------------------------------------------------

def _content_hash(text: str) -> str:
    """Return a stable SHA-256 hex digest for *text*."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Storage: embed + upsert
# ---------------------------------------------------------------------------

async def embed_and_store(
    workflow_id: str,
    source_type: str,
    source_id: str,
    text: str,
    metadata: dict[str, Any] | None = None,
) -> bool:
    """Embed *text* and store it in the ``content_embeddings`` table.

    Skips re-embedding if the exact same content (by hash) is already stored
    for this *source_id*.  Returns ``True`` if a new row was inserted,
    ``False`` if it was already present.
    """
    if metadata is None:
        metadata = {}

    sb = get_supabase()
    content_text = text[:2000]
    text_hash = _content_hash(content_text)

    # ---- cache check: skip if already embedded with identical content ----
    try:
        existing = (
            sb.table("content_embeddings")
            .select("id, metadata")
            .eq("source_id", source_id)
            .eq("source_type", source_type)
            .execute()
        )
        if existing.data:
            stored_hash = (existing.data[0].get("metadata") or {}).get(
                "content_hash"
            )
            if stored_hash == text_hash:
                logger.debug(
                    "Skipping re-embed for source_id=%s (content unchanged).",
                    source_id,
                )
                return False
            # Content changed -- delete old row so we can insert fresh
            sb.table("content_embeddings").delete().eq(
                "id", existing.data[0]["id"]
            ).execute()
            logger.info(
                "Content changed for source_id=%s; re-embedding.", source_id
            )
    except Exception:
        logger.exception(
            "Cache check failed for source_id=%s; will embed anyway.",
            source_id,
        )

    # ---- embed and insert ----
    try:
        embedding = await embed_text(content_text)
    except RuntimeError:
        logger.warning(
            "Embedding unavailable -- skipping storage for source_id=%s.",
            source_id,
        )
        return False

    metadata["content_hash"] = text_hash

    sb.table("content_embeddings").insert(
        {
            "workflow_id": workflow_id,
            "source_type": source_type,
            "source_id": source_id,
            "embedding": embedding,
            "content_text": content_text,
            "metadata": metadata,
        }
    ).execute()

    logger.debug("Stored embedding for source_id=%s.", source_id)
    return True


async def embed_and_store_image(
    workflow_id: str,
    source_type: str,
    source_id: str,
    image_bytes: bytes,
    mime_type: str = "image/png",
    description: str = "",
    metadata: dict[str, Any] | None = None,
) -> bool:
    """Embed an image and store in ``content_embeddings``.

    *description* is stored as ``content_text`` for hybrid search fallback.
    Returns ``True`` if a new row was inserted.
    """
    if metadata is None:
        metadata = {}

    sb = get_supabase()
    content_hash = _content_hash(description or str(len(image_bytes)))

    # ---- cache check ----
    try:
        existing = (
            sb.table("content_embeddings")
            .select("id, metadata")
            .eq("source_id", source_id)
            .eq("source_type", source_type)
            .execute()
        )
        if existing.data:
            stored_hash = (existing.data[0].get("metadata") or {}).get(
                "content_hash"
            )
            if stored_hash == content_hash:
                return False
            sb.table("content_embeddings").delete().eq(
                "id", existing.data[0]["id"]
            ).execute()
    except Exception:
        logger.exception(
            "Image cache check failed for source_id=%s.", source_id
        )

    # ---- embed and insert ----
    try:
        embedding = await embed_image(image_bytes, mime_type=mime_type)
    except RuntimeError:
        logger.warning(
            "Embedding unavailable -- skipping image for source_id=%s.",
            source_id,
        )
        return False

    metadata["content_hash"] = content_hash

    sb.table("content_embeddings").insert(
        {
            "workflow_id": workflow_id,
            "source_type": source_type,
            "source_id": source_id,
            "embedding": embedding,
            "content_text": description[:2000],
            "metadata": metadata,
        }
    ).execute()

    logger.debug("Stored image embedding for source_id=%s.", source_id)
    return True


# ---------------------------------------------------------------------------
# Batch embedding of trending content
# ---------------------------------------------------------------------------

async def embed_trending_batch(workflow_id: str) -> int:
    """Embed the top trending content for a workflow.

    Returns the number of *new* embeddings inserted.
    """
    sb = get_supabase()
    trending = (
        sb.table("trending_content")
        .select("*")
        .eq("workflow_id", workflow_id)
        .order("organic_score", desc=True)
        .limit(50)
        .execute()
    )

    if not trending.data:
        logger.info("No trending content to embed for workflow %s.", workflow_id)
        return 0

    # ---- Filter out already-embedded items with unchanged content ----
    items_to_embed: list[dict] = []
    for item in trending.data:
        text = f"{item['title']} {item.get('description', '')}"
        content_text = text[:2000]
        text_hash = _content_hash(content_text)

        try:
            existing = (
                sb.table("content_embeddings")
                .select("id, metadata")
                .eq("source_id", item["id"])
                .eq("source_type", "trending_content")
                .execute()
            )
            if existing.data:
                stored_hash = (existing.data[0].get("metadata") or {}).get(
                    "content_hash"
                )
                if stored_hash == text_hash:
                    continue  # already embedded, skip
                # Content changed -- delete old row
                sb.table("content_embeddings").delete().eq(
                    "id", existing.data[0]["id"]
                ).execute()
        except Exception:
            logger.exception(
                "Cache check failed for trending item %s.", item["id"]
            )

        items_to_embed.append(
            {
                "item": item,
                "content_text": content_text,
                "text_hash": text_hash,
            }
        )

    if not items_to_embed:
        logger.info(
            "All trending content already embedded for workflow %s.",
            workflow_id,
        )
        return 0

    # ---- Batch embed ----
    texts = [entry["content_text"] for entry in items_to_embed]
    try:
        embeddings = await embed_texts_batch(texts)
    except RuntimeError:
        logger.warning(
            "Embedding unavailable -- skipping trending batch for workflow %s.",
            workflow_id,
        )
        return 0

    # ---- Insert rows ----
    inserted = 0
    for entry, embedding in zip(items_to_embed, embeddings):
        item = entry["item"]
        try:
            sb.table("content_embeddings").insert(
                {
                    "workflow_id": workflow_id,
                    "source_type": "trending_content",
                    "source_id": item["id"],
                    "embedding": embedding,
                    "content_text": entry["content_text"],
                    "metadata": {
                        "platform": item.get("platform"),
                        "organic_score": item.get("organic_score"),
                        "post_url": item.get("post_url"),
                        "content_hash": entry["text_hash"],
                    },
                }
            ).execute()
            inserted += 1
        except Exception:
            logger.exception(
                "Failed to insert embedding for trending item %s.", item["id"]
            )

    logger.info(
        "Embedded %d/%d trending items for workflow %s.",
        inserted,
        len(items_to_embed),
        workflow_id,
    )
    return inserted


# ---------------------------------------------------------------------------
# Similarity search
# ---------------------------------------------------------------------------

async def search_similar(
    workflow_id: str,
    query: str,
    source_type: str | None = None,
    limit: int = 5,
) -> list[dict]:
    """Find the most similar embeddings for *query* via Supabase RPC.

    Returns an empty list (instead of raising) when embeddings are
    unavailable.
    """
    try:
        query_embedding = await embed_text(query, task_type="RETRIEVAL_QUERY")
    except RuntimeError:
        logger.warning(
            "Embedding unavailable -- returning empty search results."
        )
        return []

    sb = get_supabase()
    params: dict[str, Any] = {
        "query_embedding": query_embedding,
        "match_workflow_id": workflow_id,
        "match_count": limit,
    }
    if source_type:
        params["match_source_type"] = source_type

    try:
        result = sb.rpc("match_embeddings", params).execute()
        return result.data or []
    except Exception:
        logger.exception("match_embeddings RPC failed.")
        return []


# ---------------------------------------------------------------------------
# Research context (consumed by research_service / scripting)
# ---------------------------------------------------------------------------

async def get_research_context(
    workflow_id: str, topic: str, content_type: str
) -> dict:
    """Build a research context dict with trending + few-shot data.

    Falls back to a raw DB query when vector search yields too few results.
    """
    trending_results = await search_similar(
        workflow_id, topic, source_type="trending_content", limit=5
    )
    few_shot_results = await search_similar(
        workflow_id,
        f"{content_type} {topic}",
        source_type="published_script",
        limit=3,
    )

    # Fallback when vector search returns sparse results
    if len(trending_results) < 3:
        try:
            sb = get_supabase()
            fallback = (
                sb.table("trending_content")
                .select("*")
                .eq("workflow_id", workflow_id)
                .order("organic_score", desc=True)
                .limit(10)
                .execute()
            )
            trending_results = fallback.data or []
        except Exception:
            logger.exception("Fallback trending query failed.")

    return {
        "trending_context": trending_results,
        "few_shot_examples": few_shot_results,
    }


# ---------------------------------------------------------------------------
# Weekly embedding refresh (called by scheduler)
# ---------------------------------------------------------------------------

async def refresh_workflow_embeddings(workflow_id: str) -> dict[str, int]:
    """Full refresh of embeddings for a workflow.

    1. Re-embed trending content (new + changed).
    2. Re-embed published scripts that are missing or stale.
    3. Clean up orphaned embeddings whose source rows no longer exist.

    Returns a summary dict with counts.
    """
    sb = get_supabase()
    summary = {"trending_embedded": 0, "scripts_embedded": 0, "orphans_removed": 0}

    # ---- 1. Trending content ----
    summary["trending_embedded"] = await embed_trending_batch(workflow_id)

    # ---- 2. Published scripts ----
    try:
        published = (
            sb.table("content_items")
            .select("id, script_text, content_type, platform, title")
            .eq("workflow_id", workflow_id)
            .eq("status", "posted")
            .execute()
        )
        for item in published.data or []:
            if not item.get("script_text"):
                continue
            was_new = await embed_and_store(
                workflow_id=workflow_id,
                source_type="published_script",
                source_id=item["id"],
                text=item["script_text"],
                metadata={
                    "content_type": item.get("content_type"),
                    "platform": item.get("platform"),
                    "title": item.get("title"),
                },
            )
            if was_new:
                summary["scripts_embedded"] += 1
    except Exception:
        logger.exception(
            "Published-script re-embedding failed for workflow %s.",
            workflow_id,
        )

    # ---- 3. Orphan cleanup ----
    try:
        all_embeddings = (
            sb.table("content_embeddings")
            .select("id, source_type, source_id")
            .eq("workflow_id", workflow_id)
            .execute()
        )
        for row in all_embeddings.data or []:
            source_exists = True
            if row["source_type"] == "trending_content":
                check = (
                    sb.table("trending_content")
                    .select("id")
                    .eq("id", row["source_id"])
                    .execute()
                )
                source_exists = bool(check.data)
            elif row["source_type"] == "published_script":
                check = (
                    sb.table("content_items")
                    .select("id")
                    .eq("id", row["source_id"])
                    .execute()
                )
                source_exists = bool(check.data)

            if not source_exists:
                sb.table("content_embeddings").delete().eq(
                    "id", row["id"]
                ).execute()
                summary["orphans_removed"] += 1
    except Exception:
        logger.exception(
            "Orphan cleanup failed for workflow %s.", workflow_id
        )

    logger.info(
        "Embedding refresh for workflow %s: %s", workflow_id, summary
    )
    return summary

```
