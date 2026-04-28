---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/suggestions.py"
category: "Content Hub Source Code"
---

# suggestions.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
from backend.database import get_supabase
from backend.intelligence.memory import check_topic_overlap


async def generate_suggestions(workflow_id: str) -> list[dict]:
    sb = get_supabase()
    trending = sb.table("trending_content").select("*").eq("workflow_id", workflow_id).order("organic_score", desc=True).limit(10).execute().data
    memory = sb.table("content_publication_memory").select("*").eq("workflow_id", workflow_id).single().execute()
    memory_data = memory.data if memory.data else {}

    suggestions = []
    for item in trending[:5]:
        topic = item.get("title", "")[:100]
        overlap = await check_topic_overlap(workflow_id, topic)

        suggestion = {
            "type": "trending_topic",
            "topic": topic,
            "platform": item.get("platform", ""),
            "organic_score": item.get("organic_score", 0),
            "source_url": item.get("post_url", ""),
        }

        if overlap:
            suggestion["warning"] = f"Similar to '{overlap['similar_topic']}' published recently"

        type_dist = memory_data.get("content_type_distribution", {})
        if type_dist:
            suggestion["recommended_type"] = max(type_dist, key=type_dist.get)
        else:
            suggestion["recommended_type"] = "short_form"

        suggestions.append(suggestion)

    return suggestions

```
