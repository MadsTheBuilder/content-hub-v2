---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/renderer_video.py"
category: "Content Hub Source Code"
---

# renderer_video.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
import httpx
from backend.config import settings


async def render_video(storyboard: dict, user_id: str, workflow_id: str) -> str:
    async with httpx.AsyncClient(timeout=180) as client:
        response = await client.post(
            f"{settings.remotion_url}/render",
            json={
                "storyboard": storyboard,
                "user_id": user_id,
                "workflow_id": workflow_id,
                "output_format": "mp4",
                "width": 1080,
                "height": 1920,
            },
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("asset_url", "")
        else:
            raise Exception(f"Remotion render failed: {response.status_code} {response.text}")

```
