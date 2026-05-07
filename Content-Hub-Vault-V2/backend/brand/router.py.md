---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/brand/router.py"
category: "Content Hub Source Code"
---

# router.py

**Description:** Brand configuration API and visual identity state management.

---

```py
from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
from backend.brand.models import BrandUpdate
from backend.database import get_supabase

router = APIRouter(prefix="/api/v1/brand", tags=["brand"])


@router.get("/{workflow_id}")
async def get_brand(workflow_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("brand_configs").select("*").eq("workflow_id", workflow_id).single().execute()
    return {"brand": result.data}


@router.put("/{workflow_id}")
async def update_brand(workflow_id: str, data: BrandUpdate, user=Depends(get_current_user)):
    sb = get_supabase()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = sb.table("brand_configs").update(update_data).eq("workflow_id", workflow_id).execute()
    return {"brand": result.data[0]}

```
