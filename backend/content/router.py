import logging
import asyncio

from fastapi import APIRouter, Depends, BackgroundTasks, Body
from typing import Optional
from backend.auth.dependencies import get_current_user
from backend.content.models import ContentGenerateRequest, ContentEditRequest, SynthesizeRequest, StrategyGenerateRequest, ReviseStrategyRequest
from backend.database import get_supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/content", tags=["content"])


@router.post("/generate")
async def generate(req: ContentGenerateRequest, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    sb = get_supabase()
    sb.table("workflows").select("id").eq("id", req.workflow_id).eq("user_id", str(user.id)).single().execute()

    item = sb.table("content_items").insert({
        "workflow_id": req.workflow_id,
        "user_id": str(user.id),
        "content_type": req.content_type,
        "platform": req.platform,
        "title": req.topic,
        "status": "generating",
        "generation_metadata": req.model_dump(),
    }).execute().data[0]

    background_tasks.add_task(_run_generation, str(user.id), req.workflow_id, req.content_type, req.platform, req.topic, item["id"], skip_refinement=req.skip_refinement)
    return {"content_id": item["id"], "status": "generating"}


@router.post("/synthesize")
async def synthesize(req: SynthesizeRequest, user=Depends(get_current_user)):
    sb = get_supabase()
    workflow = sb.table("workflows").select("*").eq("id", req.workflow_id).eq("user_id", str(user.id)).single().execute().data or {}
    # Cap processing to top 10 relevant posts to prevent Gemini token overload
    selected_post_ids = req.selected_post_ids[:10]
    selected_posts = sb.table("trending_content").select("*").in_("id", selected_post_ids).execute().data or []
    memory_row = sb.table("content_publication_memory").select("*").eq("workflow_id", req.workflow_id).single().execute()
    memory = memory_row.data if memory_row.data else {}

    from backend.intelligence.synthesis import generate_strategy_document
    strategy_doc = await generate_strategy_document(
        selected_posts=selected_posts,
        brand_profile=workflow.get("brand_profile") or {},
        content_pillars=workflow.get("content_pillars") or [],
        platform=req.platform,
        memory=memory,
        user_id=str(user.id),
    )
    return {"strategy": strategy_doc.to_dict()}


@router.post("/generate-from-strategy")
async def generate_from_strategy(req: StrategyGenerateRequest, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    sb = get_supabase()
    sb.table("workflows").select("id").eq("id", req.workflow_id).eq("user_id", str(user.id)).single().execute()

    strategy = dict(req.strategy)
    if req.user_notes:
        strategy["user_notes"] = req.user_notes
    platform = strategy.get("target_platform", "tiktok")
    topic = strategy.get("content_angle", "Content")

    item = sb.table("content_items").insert({
        "workflow_id": req.workflow_id,
        "user_id": str(user.id),
        "content_type": req.content_type,
        "platform": platform,
        "title": topic,
        "status": "generating",
        "generation_metadata": {
            **req.model_dump(),
            "strategy": strategy,
            "original_strategy": req.original_strategy,  # AI's raw proposal before user edits
        },
    }).execute().data[0]

    background_tasks.add_task(
        _run_generation,
        str(user.id), req.workflow_id, req.content_type, platform, topic, item["id"],
        strategy=strategy, skip_refinement=req.skip_refinement,
    )

    # Learning loop: capture strategy feedback signal (original AI proposal vs user-approved)
    if req.original_strategy:
        background_tasks.add_task(
            _record_strategy_feedback,
            req.workflow_id,
            dict(req.original_strategy),
            strategy,
            req.user_notes or "",
        )

    return {"content_id": item["id"], "status": "generating"}


@router.post("/revise-strategy")
async def revise_strategy(req: ReviseStrategyRequest, user=Depends(get_current_user)):
    """Re-run strategy generation with rejection notes to produce a different angle."""
    sb = get_supabase()
    workflow = sb.table("workflows").select("*").eq("id", req.workflow_id).eq("user_id", str(user.id)).single().execute().data or {}

    selected_posts = []
    if req.selected_post_ids:
        selected_posts = sb.table("trending_content").select("*").in_("id", req.selected_post_ids[:10]).execute().data or []

    memory_row = sb.table("content_publication_memory").select("*").eq("workflow_id", req.workflow_id).single().execute()
    memory = memory_row.data if memory_row.data else {}

    from backend.intelligence.synthesis import generate_strategy_document
    strategy_doc = await generate_strategy_document(
        selected_posts=selected_posts,
        brand_profile=workflow.get("brand_profile") or {},
        content_pillars=workflow.get("content_pillars") or [],
        platform=req.current_strategy.get("target_platform", "tiktok"),
        memory=memory,
        rejection_notes=req.rejection_notes,
        user_id=str(user.id),
    )
    return {"strategy": strategy_doc.to_dict()}


@router.post("/{content_id}/regenerate")
async def regenerate_content(content_id: str, background_tasks: BackgroundTasks, user=Depends(get_current_user), notes: str = Body(default="")):
    """Re-trigger _run_generation for an existing content item without restarting the workflow."""
    sb = get_supabase()
    item = sb.table("content_items").select("*").eq("id", content_id).eq("user_id", str(user.id)).single().execute().data
    if not item:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Content item not found")

    # Reset status and inject any new user notes into generation_metadata
    gen_metadata = item.get("generation_metadata") or {}
    if notes:
        gen_metadata["regeneration_notes"] = notes
    sb.table("content_items").update({"status": "generating", "generation_metadata": gen_metadata, "error_message": None}).eq("id", content_id).execute()

    strategy = gen_metadata.get("strategy")
    background_tasks.add_task(
        _run_generation,
        str(user.id), item["workflow_id"], item["content_type"], item["platform"], item["title"], content_id,
        strategy=strategy,
    )
    return {"content_id": content_id, "status": "generating"}


async def _record_strategy_feedback(
    workflow_id: str,
    original_strategy: dict,
    final_strategy: dict,
    user_notes: str,
) -> None:
    """Background task: store strategy review learning signals."""
    try:
        from backend.intelligence.memory import update_strategy_feedback
        await update_strategy_feedback(workflow_id, original_strategy, final_strategy, user_notes)
    except Exception:
        logger.warning("_record_strategy_feedback failed for workflow %s", workflow_id, exc_info=True)


async def _run_generation(user_id: str, workflow_id: str, content_type: str, platform: str, topic: str, item_id: str, strategy: dict = None, skip_refinement: bool = False):
    sb = get_supabase()
    try:
        workflow = sb.table("workflows").select("*").eq("id", workflow_id).single().execute().data or {}
        brand = sb.table("brand_configs").select("*").eq("workflow_id", workflow_id).single().execute().data or {}
        memory_row = sb.table("content_publication_memory").select("*").eq("workflow_id", workflow_id).single().execute()
        memory = memory_row.data if memory_row.data else {}

        from backend.content.scripting import generate_script, refine_script
        from backend.content.storyboard import script_to_storyboard
        from backend.content.renderer_slides import render_slides
        from backend.content.renderer_video import render_video
        from backend.content.renderer_talking_head import package_talking_head
        from backend.research.research_service import get_full_research_context

        sb.table("content_items").update({"status": "scripting"}).eq("id", item_id).execute()
        research = await get_full_research_context(workflow_id, topic, content_type)
        script_result = await generate_script(content_type, topic, workflow.get("brand_voice", ""), workflow.get("content_pillars", []), research, research.get("memory", memory), platform, strategy=strategy)
        script_text = script_result["script"]

        # Post-generation quality pass (copy-editing sweeps)
        if not skip_refinement:
            sb.table("content_items").update({"status": "refining"}).eq("id", item_id).execute()
            refined = await refine_script(script_text, content_type, workflow.get("brand_voice", ""), platform)
            script_text = refined["script"]

        sb.table("content_items").update({"script_text": script_text, "status": "rendering"}).eq("id", item_id).execute()
        storyboard = script_to_storyboard(script_text, content_type, brand or {})

        asset_urls = []
        if content_type in ("slides", "topic"):
            watermark = brand.get("watermark_text") or workflow.get("name", "")
            asset_urls = await render_slides(storyboard, user_id, workflow_id, watermark=watermark)
        elif content_type == "short_form":
            try:
                from backend.config import settings as _cfg
                if not _cfg.remotion_url:
                    raise ValueError("REMOTION_URL not configured — video rendering disabled")
                # Retry up to 3 times with exponential backoff; 300s timeout per attempt
                _last_exc: Exception = RuntimeError("render never attempted")
                for _attempt in range(3):
                    try:
                        url = await asyncio.wait_for(
                            render_video(storyboard, user_id, workflow_id),
                            timeout=300,
                        )
                        asset_urls = [url]
                        _last_exc = None
                        break
                    except asyncio.TimeoutError:
                        _last_exc = TimeoutError("Render timeout after 300s")
                        logger.warning("Video render attempt %d timed out for %s", _attempt + 1, item_id)
                    except Exception as _exc:
                        _last_exc = _exc
                        logger.warning("Video render attempt %d failed for %s: %s", _attempt + 1, item_id, _exc)
                    if _attempt < 2:
                        await asyncio.sleep(2 ** _attempt)  # 1s, 2s
                if _last_exc is not None:
                    logger.error("All video render attempts failed for %s: %s", item_id, _last_exc)
                    asset_urls = []
            except ValueError as ve:
                logger.warning("Video render skipped for %s: %s", item_id, ve)
                asset_urls = []
        elif content_type == "talking_head":
            url = await package_talking_head(storyboard, {"title": topic, "platform": platform}, user_id, workflow_id)
            asset_urls = [url]

        sb.table("content_items").update({"status": "ready", "asset_urls": asset_urls, "storyboard": storyboard}).eq("id", item_id).execute()

        # Embed slide PNGs for multimodal RAG (non-blocking)
        if asset_urls and content_type in ("slides", "topic"):
            try:
                import httpx
                from backend.research.rag import embed_and_store_image
                async with httpx.AsyncClient(timeout=30) as http:
                    for i, url in enumerate(asset_urls):
                        try:
                            resp = await http.get(url)
                            if resp.status_code == 200:
                                await embed_and_store_image(
                                    workflow_id=workflow_id,
                                    source_type="slide_image",
                                    source_id=f"{item_id}_slide_{i}",
                                    image_bytes=resp.content,
                                    description=f"Slide {i+1} for: {topic}",
                                    metadata={"content_id": item_id, "slide_number": i + 1, "platform": platform},
                                )
                        except Exception:
                            logger.warning("Failed to embed slide %d for %s", i, item_id)
            except Exception:
                logger.warning("Slide embedding failed for %s", item_id)
    except Exception as e:
        sb.table("content_items").update({"status": "failed", "error_message": str(e)}).eq("id", item_id).execute()


@router.get("/library")
async def library(user=Depends(get_current_user), workflow_id: str = None, content_type: str = None, platform: str = None, search: Optional[str] = None):
    sb = get_supabase()
    query = sb.table("content_items").select("*").eq("user_id", str(user.id))
    if workflow_id:
        query = query.eq("workflow_id", workflow_id)
    if content_type:
        query = query.eq("content_type", content_type)
    if platform:
        query = query.eq("platform", platform)
    if search:
        query = query.ilike("title", f"%{search}%")
    result = query.order("created_at", desc=True).execute()
    return {"items": result.data}


@router.get("/calendar")
async def calendar(user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("content_items").select("id, title, content_type, platform, status, created_at, updated_at").eq("user_id", str(user.id)).order("created_at", desc=True).execute()
    return {"items": result.data}


@router.get("/status/{content_id}")
async def get_status(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("content_items").select("id, status, error_message").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    return result.data


@router.get("/{content_id}")
async def get_content(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("content_items").select("*").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    return {"item": result.data}


@router.get("/{content_id}/download")
async def download(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    item = sb.table("content_items").select("asset_urls, title, content_type").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    return {"download_urls": item.data.get("asset_urls", []), "title": item.data.get("title")}


@router.put("/{content_id}/edit")
async def edit_content(content_id: str, req: ContentEditRequest, user=Depends(get_current_user)):
    sb = get_supabase()
    item = sb.table("content_items").select("script_text, workflow_id").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    original = item.data["script_text"]

    sb.table("content_edit_history").insert({
        "content_item_id": content_id,
        "workflow_id": item.data["workflow_id"],
        "original_text": original,
        "edited_text": req.edited_script,
        "diff_summary": _compute_diff_summary(original, req.edited_script),
    }).execute()

    sb.table("content_items").update({"script_text": req.edited_script}).eq("id", content_id).execute()

    # Learning loop: capture edit signal (length preference + hook style rewrite)
    try:
        from backend.intelligence.memory import update_edit_feedback
        item_data = item.data or {}
        workflow_id = item_data.get("workflow_id", "")
        content_type_row = sb.table("content_items").select("content_type").eq("id", content_id).single().execute().data or {}
        await update_edit_feedback(
            workflow_id=workflow_id,
            content_type=content_type_row.get("content_type", ""),
            original_script=original,
            edited_script=req.edited_script,
        )
    except Exception:
        logger.warning("update_edit_feedback failed for content %s", content_id, exc_info=True)

    return {"updated": True}


@router.put("/{content_id}/publish")
async def publish(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    item = sb.table("content_items").select("*").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    content = item.data

    sb.table("content_items").update({
        "status": "posted",
        "published_script": content["script_text"],
    }).eq("id", content_id).execute()

    from backend.intelligence.memory import update_publication_memory
    await update_publication_memory(content["workflow_id"], content)

    from backend.research.rag import embed_and_store
    await embed_and_store(
        workflow_id=content["workflow_id"],
        source_type="published_script",
        source_id=content_id,
        text=content["script_text"],
        metadata={"content_type": content["content_type"], "platform": content["platform"], "title": content["title"]},
    )

    return {"published": True}


@router.delete("/{content_id}")
async def delete_content(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()

    # Fetch first so we have asset_urls before the row is gone
    item = sb.table("content_items").select("asset_urls, workflow_id").eq("id", content_id).eq("user_id", str(user.id)).single().execute()
    asset_urls = (item.data or {}).get("asset_urls") or []
    workflow_id = (item.data or {}).get("workflow_id")

    # Remove slide PNGs from Supabase Storage
    from backend.storage.client import delete_files
    delete_files(asset_urls)

    # Remove associated embeddings (slide_image + published_script for this item)
    if workflow_id:
        try:
            sb.table("content_embeddings").delete().eq("workflow_id", workflow_id).like("source_id", f"{content_id}%").execute()
            sb.table("content_embeddings").delete().eq("source_id", content_id).execute()
        except Exception:
            logger.warning("Embedding cleanup failed for content_id=%s", content_id)

    sb.table("content_items").delete().eq("id", content_id).eq("user_id", str(user.id)).execute()
    return {"deleted": True}


@router.get("/{content_id}/edit-history")
async def edit_history(content_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("content_edit_history").select("*").eq("content_item_id", content_id).order("created_at", desc=True).execute()
    return {"history": result.data}


def _compute_diff_summary(original: str, edited: str) -> str:
    orig_words = len(original.split())
    edit_words = len(edited.split())
    diff = edit_words - orig_words
    if abs(diff) < 3:
        return f"Minor edit ({edit_words} words)"
    elif diff < 0:
        return f"Shortened by {abs(diff)} words ({orig_words} -> {edit_words})"
    else:
        return f"Expanded by {diff} words ({orig_words} -> {edit_words})"
