---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/auth/dependencies.py"
category: "Content Hub Source Code"
---

# dependencies.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
from fastapi import Depends, HTTPException, Header
from typing import Optional


class DummyUser:
    """Dummy user for single-user MVP mode (no Supabase auth)."""
    id = "00000000-0000-0000-0000-000000000000"
    email = "local@contenthub.dev"


async def get_current_user(authorization: Optional[str] = Header(None)):
    """MVP: bypass auth, return dummy user. Replace with Supabase auth when connected."""
    return DummyUser()

```
