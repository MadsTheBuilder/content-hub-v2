"""
Apify live test — runs ONE real scrape per platform and prints the raw and
normalised output so you can validate field mappings without touching .env
or writing anything to the database.

Usage:
    python apify_live_test.py

The script forces ENVIRONMENT=production for its own process only.
Nothing is written to Supabase.
"""

import asyncio
import json
import os
import sys

# Force UTF-8 output on Windows so unicode chars don't crash
if sys.stdout.encoding != "utf-8":
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1)

# Force production mode so apify_client.py calls the real API
os.environ["ENVIRONMENT"] = "production"

import httpx
from dotenv import load_dotenv

load_dotenv()

APIFY_API_KEY = os.environ.get("APIFY_API_KEY") or os.environ.get("APIFY_API_TOKEN", "")
APIFY_BASE = "https://api.apify.com/v2"

ACTOR_MAP = {
    "tiktok": "clockworks~free-tiktok-scraper",
    "youtube": "streamers~youtube-scraper",
    "instagram": "apify~instagram-hashtag-scraper",
}

ACTOR_INPUTS = {
    "tiktok": {"hashtags": ["softwaredevelopment"], "resultsPerPage": 3},
    "youtube": {"searchKeywords": ["software development tips"], "maxResults": 3},
    "instagram": {"hashtags": ["softwaredevelopment"], "resultsLimit": 3},
}

SEPARATOR = "-" * 70


def _normalize_tiktok(item: dict) -> dict:
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
        "thumbnail_url": item.get("videoMeta", {}).get("coverUrl", "") or item.get("covers", {}).get("default", ""),
    }


def _normalize_youtube(item: dict) -> dict:
    video_id = item.get("id", "")
    return {
        "post_url": f"https://youtube.com/watch?v={video_id}",
        "author_username": item.get("channelName", ""),
        "author_followers": item.get("subscriberCount", 0),
        "title": item.get("title", "")[:200],
        "description": item.get("description", "")[:500],
        "hashtags": item.get("hashtags", []),
        "view_count": item.get("viewCount", 0),
        "like_count": item.get("likeCount", 0),
        "comment_count": item.get("commentCount", 0),
        "thumbnail_url": item.get("thumbnailUrl", "") or (f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else ""),
    }


def _normalize_instagram(item: dict) -> dict:
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
        "thumbnail_url": item.get("displayUrl", "") or item.get("thumbnailUrl", ""),
    }


NORMALIZERS = {
    "tiktok": _normalize_tiktok,
    "youtube": _normalize_youtube,
    "instagram": _normalize_instagram,
}


def _check_field(label: str, value, expected_type=None, required=True):
    present = value is not None and value != "" and value != 0
    status = "OK" if present else ("MISSING" if required else "empty")
    type_ok = isinstance(value, expected_type) if expected_type and value is not None else True
    type_status = "" if type_ok else f"  TYPE MISMATCH: got {type(value).__name__}"
    mark = "OK" if present else "XX"
    print(f"  [{mark}] {label}: {repr(value)[:80]}{type_status}  [{status}]")


async def test_platform(platform: str):
    print(f"\n{SEPARATOR}")
    print(f"PLATFORM: {platform.upper()}")
    print(SEPARATOR)

    actor_id = ACTOR_MAP[platform]
    actor_input = ACTOR_INPUTS[platform]

    async with httpx.AsyncClient(timeout=120) as client:
        print(f"  Starting actor run: {actor_id}")
        run_resp = await client.post(
            f"{APIFY_BASE}/acts/{actor_id}/runs",
            params={"token": APIFY_API_KEY},
            json=actor_input,
        )

        if run_resp.status_code != 201:
            print(f"  ERROR: Actor run failed with status {run_resp.status_code}")
            print(f"  Response: {run_resp.text[:500]}")
            return

        run_data = run_resp.json().get("data", {})
        dataset_id = run_data.get("defaultDatasetId")
        run_id = run_data.get("id")
        print(f"  Run ID: {run_id}")
        print(f"  Dataset ID: {dataset_id}")

        if not dataset_id:
            print("  ERROR: No dataset ID returned")
            return

        # Poll for completion (max 90s)
        for attempt in range(18):
            await asyncio.sleep(5)
            status_resp = await client.get(
                f"{APIFY_BASE}/acts/{actor_id}/runs/{run_id}",
                params={"token": APIFY_API_KEY},
            )
            run_status = status_resp.json().get("data", {}).get("status", "")
            print(f"  Polling... status={run_status} (attempt {attempt + 1}/18)")
            if run_status in ("SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"):
                break

        if run_status != "SUCCEEDED":
            print(f"  ERROR: Run ended with status={run_status}")
            return

        items_resp = await client.get(
            f"{APIFY_BASE}/datasets/{dataset_id}/items",
            params={"token": APIFY_API_KEY},
        )
        raw_items = items_resp.json()

    if not raw_items:
        print("  WARNING: Dataset returned 0 items")
        return

    print(f"\n  Got {len(raw_items)} raw item(s). Showing first item:")
    print(f"\n  --- RAW PAYLOAD (first item) ---")
    print(json.dumps(raw_items[0], indent=2, default=str)[:2000])

    normalizer = NORMALIZERS[platform]
    normalized = normalizer(raw_items[0])

    print(f"\n  --- NORMALISED OUTPUT ---")
    _check_field("post_url", normalized.get("post_url"), str)
    _check_field("author_username", normalized.get("author_username"), str)
    _check_field("author_followers", normalized.get("author_followers"), int)
    _check_field("title", normalized.get("title"), str)
    _check_field("description", normalized.get("description"), str)
    _check_field("hashtags", normalized.get("hashtags"), list)
    _check_field("view_count", normalized.get("view_count"), int)
    _check_field("like_count", normalized.get("like_count"), int)
    _check_field("comment_count", normalized.get("comment_count"), int)
    _check_field("thumbnail_url", normalized.get("thumbnail_url"), str, required=False)

    missing = [k for k, v in normalized.items() if v is None or v == ""]
    if missing:
        print(f"\n  FIELDS WITH NO VALUE: {missing}")
    else:
        print(f"\n  All fields populated.")


async def main():
    if not APIFY_API_KEY:
        print("ERROR: APIFY_API_KEY / APIFY_API_TOKEN not set in .env")
        return

    print(f"Apify live field-mapping test")
    print(f"API key: {APIFY_API_KEY[:12]}...")
    print(f"Testing 3 platforms with minimal result counts (3 items each)")
    print(f"Nothing is written to the database.\n")

    for platform in ["youtube", "tiktok", "instagram"]:
        try:
            await test_platform(platform)
        except Exception as e:
            print(f"\n  EXCEPTION for {platform}: {e}")

    print(f"\n{SEPARATOR}")
    print("Done. Review MISSING / TYPE MISMATCH lines above.")
    print("Any field shown as MISSING needs a fallback added to _normalize_post() in apify_client.py")
    print(SEPARATOR)


if __name__ == "__main__":
    asyncio.run(main())
