---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/renderer_talking_head.py"
category: "Content Hub Source Code"
---

# renderer_talking_head.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
import io
import zipfile
import json
from backend.storage.client import upload_file


async def package_talking_head(storyboard: dict, content_item: dict, user_id: str, workflow_id: str) -> str:
    sections = storyboard.get("sections", {})

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("script.txt", sections.get("script", ""))
        zf.writestr("shot_list.txt", sections.get("shot_list", ""))
        zf.writestr("onscreen_text.txt", sections.get("onscreen_text", ""))
        zf.writestr("metadata.json", json.dumps({
            "title": content_item.get("title", ""),
            "content_type": "talking_head",
            "platform": content_item.get("platform", ""),
            "created_at": content_item.get("created_at", ""),
        }, indent=2))

    zip_buffer.seek(0)
    url = await upload_file(user_id, workflow_id, zip_buffer.read(), "talking_head_package.zip", "application/zip")
    return url

```
