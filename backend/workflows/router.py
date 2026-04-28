import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.auth.dependencies import get_current_user
from backend.workflows.models import WorkflowCreate, WorkflowUpdate
from backend.workflows.service import create_workflow
from backend.workflows.templates import NICHE_TEMPLATES, GUIDED_QUESTIONNAIRE
from backend.database import get_supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/workflows", tags=["workflows"])


@router.get("/templates")
async def get_templates():
    return {"templates": NICHE_TEMPLATES, "questionnaire": GUIDED_QUESTIONNAIRE}



@router.get("")
async def list_workflows(user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("workflows").select("*").eq("user_id", str(user.id)).order("created_at", desc=True).execute()
    return {"workflows": result.data}


@router.post("")
async def create_workflow_endpoint(data: WorkflowCreate, user=Depends(get_current_user)):
    try:
        workflow = await create_workflow(str(user.id), data.model_dump())
        return {"workflow": workflow}
    except Exception as e:
        logger.exception("Workflow creation failed")
        raise


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("workflows").select("*").eq("id", workflow_id).eq("user_id", str(user.id)).single().execute()
    return {"workflow": result.data}


@router.put("/{workflow_id}")
async def update_workflow(workflow_id: str, data: WorkflowUpdate, user=Depends(get_current_user)):
    sb = get_supabase()
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    result = sb.table("workflows").update(update_data).eq("id", workflow_id).eq("user_id", str(user.id)).execute()
    return {"workflow": result.data[0]}


@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    sb.table("workflows").delete().eq("id", workflow_id).eq("user_id", str(user.id)).execute()
    return {"deleted": True}


@router.post("/{workflow_id}/scrape")
async def trigger_scrape(workflow_id: str, user=Depends(get_current_user)):
    from backend.research.apify_client import scrape_workflow
    from backend.intelligence.synthesis import enrich_trending_posts, compute_relevance_score

    sb = get_supabase()
    workflow = sb.table("workflows").select("apify_search_config, brand_profile, content_pillars").eq("id", workflow_id).eq("user_id", str(user.id)).single().execute()
    wf = workflow.data

    count = await scrape_workflow(workflow_id, wf["apify_search_config"])

    # Post-scrape enrichment: analyze top posts with Gemini + compute relevance scores
    if count > 0:
        try:
            trending = sb.table("trending_content").select("*").eq("workflow_id", workflow_id).order("organic_score", desc=True).limit(50).execute()
            posts = trending.data or []

            brand_profile = wf.get("brand_profile") or {}
            pillars = wf.get("content_pillars") or []

            # Enrich top 10 with "why it works" analysis
            await enrich_trending_posts(posts, brand_profile, limit=10)

            # Compute relevance scores for all
            for post in posts:
                post["relevance_score"] = compute_relevance_score(post, brand_profile, pillars)

            # Update DB with enrichment data
            for post in posts:
                update = {"relevance_score": post["relevance_score"]}
                if post.get("content_analysis"):
                    update["content_analysis"] = post["content_analysis"]
                sb.table("trending_content").update(update).eq("id", post["id"]).execute()

            logger.info("Enriched %d trending posts for workflow %s", len(posts), workflow_id)
        except Exception:
            logger.exception("Post-scrape enrichment failed for workflow %s", workflow_id)

    return {"scraped": count}


@router.get("/{workflow_id}/trending")
async def get_trending(workflow_id: str, user=Depends(get_current_user)):
    sb = get_supabase()
    result = sb.table("trending_content").select("*").eq("workflow_id", workflow_id).order("relevance_score", desc=True).limit(50).execute()
    return {"trending": result.data}


@router.get("/{workflow_id}/suggestions")
async def get_suggestions(workflow_id: str, user=Depends(get_current_user)):
    from backend.intelligence.suggestions import generate_suggestions
    suggestions = await generate_suggestions(workflow_id)
    return {"suggestions": suggestions}


class SelectionRecord(BaseModel):
    selected_post_ids: list[str]


@router.post("/{workflow_id}/selections")
async def record_selections(workflow_id: str, data: SelectionRecord, user=Depends(get_current_user)):
    sb = get_supabase()
    sb.table("workflows").select("id").eq("id", workflow_id).eq("user_id", str(user.id)).single().execute()
    from backend.intelligence.memory import update_selection_memory
    await update_selection_memory(workflow_id, data.selected_post_ids)
    return {"recorded": True}
