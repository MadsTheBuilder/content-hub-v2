---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/brand/models.py"
category: "Content Hub Source Code"
---

# models.py

**Description:** Brand configuration API and visual identity state management.

---

```py
from pydantic import BaseModel
from typing import Optional


class BrandUpdate(BaseModel):
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    accent_color: Optional[str] = None
    font_family: Optional[str] = None
    logo_url: Optional[str] = None
    watermark_enabled: Optional[bool] = None
    watermark_text: Optional[str] = None

```
