---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/intelligence/rejection.py"
category: "Content Hub Source Code"
---

# rejection.py

**Description:** Automated learning systems, publication memory loops, and trend intelligence.

---

```py
from backend.database import get_supabase
from datetime import datetime, timedelta


async def flag_rejected_content():
    sb = get_supabase()
    cutoff = (datetime.utcnow() - timedelta(days=7)).isoformat()
    sb.table("content_items").update({"rejection_flag": True}).eq("status", "ready").eq("rejection_flag", False).lt("created_at", cutoff).execute()


async def update_rejection_patterns(workflow_id: str):
    sb = get_supabase()
    rejected = sb.table("content_items").select("content_type, platform, generation_metadata").eq("workflow_id", workflow_id).eq("rejection_flag", True).execute().data
    if not rejected:
        return
    patterns = {}
    for item in rejected:
        ct = item.get("content_type", "unknown")
        patterns[ct] = patterns.get(ct, 0) + 1
    sb.table("content_publication_memory").update({"rejection_patterns": patterns}).eq("workflow_id", workflow_id).execute()

```
