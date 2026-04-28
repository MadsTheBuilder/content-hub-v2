---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/triggers.py"
category: "Content Hub Source Code"
---

# triggers.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
from backend.database import get_supabase


async def detect_trend_spikes(workflow_id: str):
    sb = get_supabase()
    recent = sb.table("trending_content").select("*").eq("workflow_id", workflow_id).order("scraped_at", desc=True).limit(100).execute().data
    if not recent:
        return []

    scores = [r["organic_score"] for r in recent if r["organic_score"] > 0]
    if not scores:
        return []
    baseline = sum(scores) / len(scores)

    triggers = []
    for item in recent[:20]:
        if item["organic_score"] > baseline * 3:
            trigger = {
                "workflow_id": workflow_id,
                "trigger_type": "trend_spike",
                "title": f"Trending: {item['title'][:100]}",
                "description": f"Organic score {item['organic_score']:.0f} is {item['organic_score']/baseline:.1f}x above baseline ({baseline:.0f})",
                "source_data": {"trending_content_id": item["id"], "organic_score": item["organic_score"], "platform": item["platform"]},
            }
            triggers.append(trigger)

    if triggers:
        sb.table("content_triggers").insert(triggers).execute()
    return triggers

```
