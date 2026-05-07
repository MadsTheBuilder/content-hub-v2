---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/memory.py"
category: "Content Hub Source Code"
---

# memory.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
from backend.database import get_supabase


async def update_publication_memory(workflow_id: str, published_item: dict):
    sb = get_supabase()
    memory = sb.table("content_publication_memory").select("*").eq("workflow_id", workflow_id).single().execute().data
    if not memory:
        # Cold start: create initial row so this publish event is not lost
        sb.table("content_publication_memory").insert({
            "workflow_id": workflow_id,
            "published_count": 0,
            "content_type_distribution": {},
            "avg_script_length": {},
            "preferred_hook_styles": {},
            "topics_published": [],
            "platform_content_map": {},
        }).execute()
        memory = sb.table("content_publication_memory").select("*").eq("workflow_id", workflow_id).single().execute().data
        if not memory:
            return  # DB error — bail gracefully

    new_count = (memory.get("published_count") or 0) + 1
    type_dist = memory.get("content_type_distribution") or {}
    ct = published_item.get("content_type", "unknown")
    for key in type_dist:
        type_dist[key] = type_dist[key] * (new_count - 1) / new_count
    type_dist[ct] = type_dist.get(ct, 0) + (1 / new_count)

    avg_lengths = memory.get("avg_script_length") or {}
    script = published_item.get("script_text", "")
    word_count = len(script.split())
    if ct in avg_lengths:
        avg_lengths[ct] = int((avg_lengths[ct] * (new_count - 1) + word_count) / new_count)
    else:
        avg_lengths[ct] = word_count

    hook_styles = memory.get("preferred_hook_styles") or {}
    detected_hook = _detect_hook_style(script)
    for key in hook_styles:
        hook_styles[key] = hook_styles[key] * (new_count - 1) / new_count
    hook_styles[detected_hook] = hook_styles.get(detected_hook, 0) + (1 / new_count)

    topics = memory.get("topics_published") or []
    topics.insert(0, published_item.get("title", ""))
    topics = topics[:30]

    platform_map = memory.get("platform_content_map") or {}
    platform = published_item.get("platform", "")
    if platform:
        platform_map[platform] = ct

    sb.table("content_publication_memory").update({
        "published_count": new_count,
        "content_type_distribution": type_dist,
        "avg_script_length": avg_lengths,
        "preferred_hook_styles": hook_styles,
        "topics_published": topics,
        "platform_content_map": platform_map,
    }).eq("workflow_id", workflow_id).execute()


def _detect_hook_style(script: str) -> str:
    first_line = script.strip().split("\n")[0].lower() if script else ""
    if "?" in first_line:
        return "question"
    if any(c.isdigit() for c in first_line) and ("%" in first_line or "x" in first_line):
        return "stat"
    if any(word in first_line for word in ["i ", "my ", "when i", "last year", "story"]):
        return "story"
    if any(word in first_line for word in ["stop", "don't", "never", "mistake"]):
        return "contrarian"
    return "statement"


async def update_selection_memory(workflow_id: str, selected_post_ids: list[str]) -> None:
    """Track which hook/content styles the user selects to refine future strategy."""
    sb = get_supabase()
    posts = sb.table("trending_content").select("content_analysis").in_("id", selected_post_ids).execute().data or []

    hook_counts: dict[str, int] = {}
    style_counts: dict[str, int] = {}
    for post in posts:
        analysis = post.get("content_analysis") or {}
        hook = analysis.get("hook_type", "")
        style = analysis.get("content_style", "")
        if hook:
            hook_counts[hook] = hook_counts.get(hook, 0) + 1
        if style:
            style_counts[style] = style_counts.get(style, 0) + 1

    if not hook_counts and not style_counts:
        return

    weight = 0.3 / max(len(selected_post_ids), 1)
    
    # Use Postgres RPC for atomic upsert and update, preventing cold-start loss and JSON race conditions
    sb.rpc("increment_selection_memory", {
        "target_workflow_id": workflow_id,
        "hook_updates": hook_counts,
        "style_updates": style_counts,
        "weight": weight
    }).execute()


async def check_topic_overlap(workflow_id: str, topic: str) -> dict | None:
    sb = get_supabase()
    memory = sb.table("content_publication_memory").select("topics_published").eq("workflow_id", workflow_id).single().execute().data
    if not memory:
        return None
    topics = memory.get("topics_published") or []
    topic_lower = topic.lower()
    for i, past_topic in enumerate(topics):
        if past_topic and _topics_similar(topic_lower, past_topic.lower()):
            return {"similar_topic": past_topic, "position": i}
    return None


def _topics_similar(a: str, b: str) -> bool:
    words_a = set(a.split())
    words_b = set(b.split())
    if not words_a or not words_b:
        return False
    overlap = len(words_a & words_b) / min(len(words_a), len(words_b))
    return overlap > 0.5

```
