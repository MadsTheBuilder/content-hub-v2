import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from backend.auth.dependencies import get_current_user
from backend.brand.models import BrandUpdate
from backend.database import get_supabase

logger = logging.getLogger(__name__)
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


@router.post("/{workflow_id}/logo")
async def upload_logo(
    workflow_id: str,
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    """Upload a brand logo image to Supabase Storage and update brand_configs.logo_url."""
    sb = get_supabase()

    # Validate file type
    allowed = {"image/png", "image/jpeg", "image/webp", "image/svg+xml"}
    if file.content_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}. Use PNG, JPEG, WEBP, or SVG.")

    ext = (file.filename or "logo").rsplit(".", 1)[-1].lower()
    storage_path = f"brand-assets/{workflow_id}/logo.{ext}"
    file_bytes = await file.read()

    try:
        # Upload to Supabase Storage bucket "brand-assets"
        sb.storage.from_("brand-assets").upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": file.content_type, "upsert": "true"},
        )
        # Build CDN public URL
        public_url_result = sb.storage.from_("brand-assets").get_public_url(storage_path)
        logo_url = public_url_result if isinstance(public_url_result, str) else str(public_url_result)
    except Exception as exc:
        logger.exception("Logo upload failed for workflow %s", workflow_id)
        raise HTTPException(status_code=500, detail=f"Upload failed: {exc}") from exc

    # Persist logo_url into brand_configs
    sb.table("brand_configs").update({"logo_url": logo_url}).eq("workflow_id", workflow_id).execute()

    return {"logo_url": logo_url}
