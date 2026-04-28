import asyncio
import logging

from backend.config import settings
from backend.research.organic_score import is_organic, compute_organic_score
from backend.database import get_supabase

logger = logging.getLogger(__name__)

APIFY_BASE = "https://api.apify.com/v2"

ACTOR_MAP = {
    "tiktok": "clockworks~free-tiktok-scraper",
    "youtube": "streamers~youtube-scraper",
    "instagram": "apify~instagram-hashtag-scraper",
}

# Profile scraping uses same or different actors with profile-specific inputs
PROFILE_ACTOR_MAP = {
    "tiktok": "clockworks~free-tiktok-scraper",
    "youtube": "streamers~youtube-scraper",
    "instagram": "apify~instagram-profile-scraper",
}


async def scrape_platform(workflow_id: str, platform: str, search_config: dict) -> list[dict]:
    if not settings.apify_api_key:
        return _mock_results(platform, workflow_id)

    actor_id = ACTOR_MAP.get(platform)
    if not actor_id:
        return []

    import httpx
    async with httpx.AsyncClient(timeout=300) as client:
        run_response = await client.post(
            f"{APIFY_BASE}/acts/{actor_id}/runs",
            params={"token": settings.apify_api_key},
            json=_build_actor_input(platform, search_config),
        )
        run_data = run_response.json()["data"]
        run_id = run_data.get("id")
        dataset_id = run_data.get("defaultDatasetId")
        if not dataset_id or not run_id:
            return []

        # Poll until the actor run finishes
        for _ in range(60):  # up to ~5 minutes
            await asyncio.sleep(5)
            status_resp = await client.get(
                f"{APIFY_BASE}/actor-runs/{run_id}",
                params={"token": settings.apify_api_key},
            )
            status = status_resp.json()["data"]["status"]
            logger.info("Apify run %s [%s]: %s", run_id, platform, status)
            if status == "SUCCEEDED":
                break
            if status in ("FAILED", "ABORTED", "TIMED-OUT"):
                logger.error("Apify run %s failed with status: %s", run_id, status)
                return []
        else:
            logger.error("Apify run %s timed out after polling", run_id)
            return []

        items_response = await client.get(
            f"{APIFY_BASE}/datasets/{dataset_id}/items",
            params={"token": settings.apify_api_key},
        )
        raw_items = items_response.json()

    results = []
    for item in raw_items:
        post = _normalize_post(item, platform)
        if is_organic(post):
            post["organic_score"] = compute_organic_score(post, platform)
            post["workflow_id"] = workflow_id
            post["platform"] = platform
            results.append(post)

    results.sort(key=lambda x: x["organic_score"], reverse=True)
    return results[:50]


async def scrape_profiles(workflow_id: str, platform: str, usernames: list[str]) -> list[dict]:
    """Scrape recent posts from specific creator profiles."""
    if not settings.apify_api_key or not usernames:
        return []

    actor_id = PROFILE_ACTOR_MAP.get(platform)
    if not actor_id:
        return []

    actor_input = _build_profile_input(platform, usernames)
    if not actor_input:
        return []

    import httpx
    async with httpx.AsyncClient(timeout=300) as client:
        run_response = await client.post(
            f"{APIFY_BASE}/acts/{actor_id}/runs",
            params={"token": settings.apify_api_key},
            json=actor_input,
        )
        run_data = run_response.json()["data"]
        run_id = run_data.get("id")
        dataset_id = run_data.get("defaultDatasetId")
        if not dataset_id or not run_id:
            return []

        for _ in range(60):
            await asyncio.sleep(5)
            status_resp = await client.get(
                f"{APIFY_BASE}/actor-runs/{run_id}",
                params={"token": settings.apify_api_key},
            )
            status = status_resp.json()["data"]["status"]
            logger.info("Apify profile run %s [%s]: %s", run_id, platform, status)
            if status == "SUCCEEDED":
                break
            if status in ("FAILED", "ABORTED", "TIMED-OUT"):
                logger.error("Apify profile run %s failed: %s", run_id, status)
                return []
        else:
            logger.error("Apify profile run %s timed out", run_id)
            return []

        items_response = await client.get(
            f"{APIFY_BASE}/datasets/{dataset_id}/items",
            params={"token": settings.apify_api_key},
        )
        raw_items = items_response.json()

    results = []
    for item in raw_items:
        post = _normalize_post(item, platform)
        if is_organic(post):
            post["organic_score"] = compute_organic_score(post, platform)
            post["workflow_id"] = workflow_id
            post["platform"] = platform
            results.append(post)

    results.sort(key=lambda x: x["organic_score"], reverse=True)
    return results[:30]


async def scrape_general_trending(platform: str) -> list[dict]:
    """Scrape platform-wide trending content without keyword/competitor filter.

    Results are tagged with workflow_id='__general__' for downstream blending.
    Runs weekly — less aggressive than keyword scraping.
    """
    if not settings.apify_api_key:
        return _mock_general_results(platform)

    actor_id = ACTOR_MAP.get(platform)
    if not actor_id:
        return []

    actor_input = _build_general_trending_input(platform)
    if not actor_input:
        return []

    import httpx
    async with httpx.AsyncClient(timeout=300) as client:
        run_response = await client.post(
            f"{APIFY_BASE}/acts/{actor_id}/runs",
            params={"token": settings.apify_api_key},
            json=actor_input,
        )
        run_data = run_response.json()["data"]
        run_id = run_data.get("id")
        dataset_id = run_data.get("defaultDatasetId")
        if not dataset_id or not run_id:
            return []

        for _ in range(60):
            await asyncio.sleep(5)
            status_resp = await client.get(
                f"{APIFY_BASE}/actor-runs/{run_id}",
                params={"token": settings.apify_api_key},
            )
            status = status_resp.json()["data"]["status"]
            logger.info("General trending run %s [%s]: %s", run_id, platform, status)
            if status == "SUCCEEDED":
                break
            if status in ("FAILED", "ABORTED", "TIMED-OUT"):
                logger.error("General trending run %s failed: %s", run_id, status)
                return []
        else:
            logger.error("General trending run %s timed out", run_id)
            return []

        items_response = await client.get(
            f"{APIFY_BASE}/datasets/{dataset_id}/items",
            params={"token": settings.apify_api_key},
        )
        raw_items = items_response.json()

    results = []
    for item in raw_items:
        post = _normalize_post(item, platform)
        if is_organic(post):
            post["organic_score"] = compute_organic_score(post, platform)
            post["workflow_id"] = None
            post["platform"] = platform
            results.append(post)

    results.sort(key=lambda x: x["organic_score"], reverse=True)
    return results[:30]


async def scrape_workflow(workflow_id: str, apify_config: dict) -> int:
    sb = get_supabase()
    total = 0
    seen_urls: set[str] = set()

    for platform, config in apify_config.items():
        # 1. Hashtag/keyword scraping (existing)
        try:
            results = await scrape_platform(workflow_id, platform, config)
            if results:
                # Deduplicate
                new_results = []
                for r in results:
                    if r.get("post_url") and r["post_url"] not in seen_urls:
                        seen_urls.add(r["post_url"])
                        new_results.append(r)
                if new_results:
                    sb.table("trending_content").insert(new_results).execute()
                    total += len(new_results)
        except Exception:
            logger.exception("Scrape failed for platform %s, continuing with others", platform)

        # 2. Profile scraping (new — competitor accounts)
        profiles = config.get("profiles", [])
        if profiles:
            try:
                profile_results = await scrape_profiles(workflow_id, platform, profiles)
                if profile_results:
                    new_results = []
                    for r in profile_results:
                        if r.get("post_url") and r["post_url"] not in seen_urls:
                            seen_urls.add(r["post_url"])
                            new_results.append(r)
                    if new_results:
                        sb.table("trending_content").insert(new_results).execute()
                        total += len(new_results)
            except Exception:
                logger.exception("Profile scrape failed for %s/%s", platform, profiles)

    return total


def _build_actor_input(platform: str, config: dict) -> dict:
    if platform == "tiktok":
        return {"hashtags": config.get("hashtags", []), "resultsPerPage": 30}
    elif platform == "youtube":
        keywords = config.get("keywords", [])
        start_urls = [
            {"url": f"https://www.youtube.com/results?search_query={'+'.join(k.split())}"}
            for k in keywords[:5]
        ]
        if not start_urls:
            start_urls = [{"url": "https://www.youtube.com/results?search_query=trending"}]
        return {"startUrls": start_urls, "maxResults": 30}
    elif platform == "instagram":
        return {"hashtags": config.get("hashtags", []), "resultsLimit": 30}
    return {}


def _build_general_trending_input(platform: str) -> dict:
    """Build Apify actor input for general trending (no keyword filter)."""
    if platform == "tiktok":
        # Broad trending hashtags — not user-specific keywords
        return {"hashtags": ["trending", "viral", "fyp", "foryou"], "resultsPerPage": 30}
    elif platform == "youtube":
        return {
            "startUrls": [
                {"url": "https://www.youtube.com/results?search_query=AI+tools+2025"},
                {"url": "https://www.youtube.com/results?search_query=AI+workflow+automation"},
                {"url": "https://www.youtube.com/results?search_query=build+in+public+AI"},
            ],
            "maxResults": 30,
        }
    elif platform == "instagram":
        return {"hashtags": ["trending", "viral", "explore", "reels"], "resultsLimit": 30}
    return {}


def _build_profile_input(platform: str, usernames: list[str]) -> dict:
    """Build Apify actor input for profile scraping (different from hashtag scraping)."""
    if platform == "tiktok":
        profiles = [f"https://www.tiktok.com/@{u}" for u in usernames[:5]]
        return {"profiles": profiles, "resultsPerPage": 20}
    elif platform == "youtube":
        start_urls = [{"url": f"https://www.youtube.com/@{u}"} for u in usernames[:5]]
        return {"startUrls": start_urls, "maxResults": 20}
    elif platform == "instagram":
        return {"usernames": usernames[:5], "resultsLimit": 20}
    return {}


def _normalize_post(item: dict, platform: str) -> dict:
    if platform == "tiktok":
        return {
            "post_url": item.get("webVideoUrl", ""),
            "author_username": item.get("authorMeta", {}).get("name", ""),
            "author_followers": item.get("authorMeta", {}).get("fans", 0),
            "title": item.get("text", "")[:200],
            "description": item.get("text", ""),
            "hashtags": [h.get("name", "") for h in item.get("hashtags", [])],
            "view_count": item.get("playCount", 0),
            "like_count": item.get("diggCount", 0),
            "comment_count": item.get("commentCount", 0),
            "share_count": item.get("shareCount", 0),
            "save_count": 0,
            "content_age_days": 5,
            "thumbnail_url": item.get("videoMeta", {}).get("coverUrl", "") or item.get("covers", {}).get("default", ""),
        }
    elif platform == "youtube":
        video_id = item.get("id", "")
        return {
            "post_url": item.get("url", "") or (f"https://youtube.com/watch?v={video_id}" if video_id else ""),
            "author_username": item.get("channelName", "") or item.get("channelUsername", ""),
            "author_followers": item.get("numberOfSubscribers", 0) or 0,
            "title": item.get("title", "")[:200],
            "description": (item.get("text", "") or item.get("description", ""))[:500],
            "hashtags": item.get("hashtags", []),
            "view_count": item.get("viewCount", 0) or 0,
            "like_count": item.get("likes", 0) or 0,
            "comment_count": item.get("commentsCount", 0) or 0,
            "share_count": 0,
            "save_count": 0,
            "content_age_days": 5,
            "thumbnail_url": item.get("thumbnailUrl", "") or (f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else ""),
        }
    elif platform == "instagram":
        return {
            "post_url": item.get("url", ""),
            "author_username": item.get("ownerUsername", ""),
            "author_followers": item.get("ownerFollowerCount", 0),
            "title": (item.get("caption", "") or "")[:200],
            "description": item.get("caption", "") or "",
            "hashtags": item.get("hashtags", []),
            "view_count": item.get("videoPlayCount", 0) or item.get("likesCount", 0),
            "like_count": item.get("likesCount", 0),
            "comment_count": item.get("commentsCount", 0),
            "share_count": 0,
            "save_count": 0,
            "content_age_days": 5,
            "thumbnail_url": item.get("displayUrl", "") or item.get("thumbnailUrl", ""),
        }
    return item


def _mock_results(platform: str, workflow_id: str) -> list[dict]:
    return [
        {
            "workflow_id": workflow_id,
            "platform": platform,
            "post_url": f"https://{platform}.com/mock/{i}",
            "author_username": f"creator_{i}",
            "author_followers": 5000 + (i * 1000),
            "title": f"Mock trending post #{i} for {platform}",
            "description": f"This is a mock trending post about the niche topic #{i}",
            "hashtags": ["trending", "viral", platform],
            "view_count": 10000 * (i + 1),
            "like_count": 500 * (i + 1),
            "comment_count": 50 * (i + 1),
            "share_count": 20 * (i + 1),
            "save_count": 10 * (i + 1),
            "organic_score": float(10000 * (i + 1) * (500 + 20 + 50) * (i + 1) / (5000 + i * 1000)),
            "content_age_days": 5,
            "thumbnail_url": "",
        }
        for i in range(10)
    ]


def _mock_general_results(platform: str) -> list[dict]:
    """Mock general trending results for when Apify key is absent."""
    return [
        {
            "workflow_id": None,
            "platform": platform,
            "post_url": f"https://{platform}.com/general_trending/{i}",
            "author_username": f"trending_creator_{i}",
            "author_followers": 50000 + (i * 10000),
            "title": f"Platform-wide trending topic #{i} on {platform}",
            "description": f"General trending content #{i} — not keyword filtered",
            "hashtags": ["trending", "viral", platform],
            "view_count": 100000 * (i + 1),
            "like_count": 5000 * (i + 1),
            "comment_count": 500 * (i + 1),
            "share_count": 200 * (i + 1),
            "save_count": 100 * (i + 1),
            "organic_score": float(100000 * (i + 1)),
            "content_age_days": 2,
            "thumbnail_url": "",
        }
        for i in range(8)
    ]
