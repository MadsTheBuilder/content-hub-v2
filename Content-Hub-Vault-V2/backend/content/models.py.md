---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/models.py"
category: "Content Hub Source Code"
---

# models.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
from pydantic import BaseModel


class ContentGenerateRequest(BaseModel):
    workflow_id: str
    content_type: str
    platform: str
    topic: str
    skip_refinement: bool = False


class ContentEditRequest(BaseModel):
    edited_script: str


class SynthesizeRequest(BaseModel):
    workflow_id: str
    selected_post_ids: list[str]
    platform: str


class StrategyGenerateRequest(BaseModel):
    workflow_id: str
    strategy: dict
    original_strategy: dict | None = None
    user_notes: str = ""
    content_type: str = "short_form"
    skip_refinement: bool = False

```
