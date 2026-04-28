---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/scheduler/jobs.py"
category: "Content Hub Source Code"
---

# jobs.py

**Description:** Python backend service, scripting module, or execution logic.

---

```py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from backend.database import get_supabase
from backend.research.apify_client import scrape_workflow
from backend.research.rag import embed_trending_batch, refresh_workflow_embeddings
from backend.intelligence.triggers import detect_trend_spikes
from backend.intelligence.suggestions import generate_suggestions
from backend.intelligence.rejection import flag_rejected_content, update_rejection_patterns
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler(job_defaults={"misfire_grace_time": 600})


async def _get_active_workflows() -> list[dict]:
    sb = get_supabase()
    result = sb.table("workflows").select("id, apify_search_config").eq("is_active", True).execute()
    return result.data


async def job_scrape_organic():
    logger.info("Running organic scrape job")
    workflows = await _get_active_workflows()
    for wf in workflows:
        try:
            count = await scrape_workflow(wf["id"], wf["apify_search_config"])
            await embed_trending_batch(wf["id"])
            logger.info(f"Scraped {count} items for workflow {wf['id']}")
        except Exception as e:
            logger.error(f"Scrape failed for {wf['id']}: {e}")


async def job_detect_trends():
    logger.info("Running trend detection job")
    workflows = await _get_active_workflows()
    for wf in workflows:
        try:
            await detect_trend_spikes(wf["id"])
        except Exception as e:
            logger.error(f"Trend detection failed for {wf['id']}: {e}")


async def job_generate_suggestions():
    logger.info("Running suggestion generation job")
    workflows = await _get_active_workflows()
    for wf in workflows:
        try:
            await generate_suggestions(wf["id"])
        except Exception as e:
            logger.error(f"Suggestions failed for {wf['id']}: {e}")


async def job_weekly_embed_refresh():
    logger.info("Running weekly embed refresh")
    workflows = await _get_active_workflows()
    for wf in workflows:
        try:
            summary = await refresh_workflow_embeddings(wf["id"])
            logger.info(f"Embed refresh for {wf['id']}: {summary}")
        except Exception as e:
            logger.error(f"Embed refresh failed for {wf['id']}: {e}")


async def job_flag_rejections():
    logger.info("Running rejection flagging job")
    await flag_rejected_content()
    workflows = await _get_active_workflows()
    for wf in workflows:
        try:
            await update_rejection_patterns(wf["id"])
        except Exception as e:
            logger.error(f"Rejection update failed for {wf['id']}: {e}")


def start_scheduler():
    scheduler.add_job(job_scrape_organic, CronTrigger(day="*/3", hour=5, minute=30), id="scrape_organic")
    scheduler.add_job(job_detect_trends, CronTrigger(day="*/3", hour=6, minute=0), id="detect_trends")
    scheduler.add_job(job_generate_suggestions, CronTrigger(hour=6, minute=30), id="generate_suggestions")
    scheduler.add_job(job_weekly_embed_refresh, CronTrigger(day_of_week="sun", hour=4, minute=0), id="weekly_embed")
    scheduler.add_job(job_flag_rejections, CronTrigger(day_of_week="sun", hour=6, minute=0), id="flag_rejections")
    scheduler.start()
    logger.info("Scheduler started with 5 jobs")

```
