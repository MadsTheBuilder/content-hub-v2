---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/platform_adapter.py"
category: "Content Hub Source Code"
---

# platform_adapter.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
PLATFORM_GROUPS = {
    "short_form": ["tiktok", "instagram", "facebook", "youtube_shorts"],
    "professional": ["linkedin", "twitter"],
}

PLATFORM_LIMITS = {
    "tiktok": {"caption_length": 300, "hashtag_count": 5, "aspect_ratio": "9:16"},
    "instagram": {"caption_length": 2200, "hashtag_count": 30, "aspect_ratio": "1:1"},
    "youtube_shorts": {"caption_length": 100, "hashtag_count": 3, "aspect_ratio": "9:16"},
    "linkedin": {"caption_length": 3000, "hashtag_count": 5, "aspect_ratio": "1:1"},
    "twitter": {"caption_length": 280, "hashtag_count": 3, "aspect_ratio": "16:9"},
    "facebook": {"caption_length": 500, "hashtag_count": 5, "aspect_ratio": "9:16"},
}


def get_platform_group(platform: str) -> str:
    for group, platforms in PLATFORM_GROUPS.items():
        if platform in platforms:
            return group
    return "short_form"


def adapt_for_platform(script: str, source_platform: str, target_platform: str) -> dict:
    limits = PLATFORM_LIMITS.get(target_platform, PLATFORM_LIMITS["instagram"])
    caption = script[:limits["caption_length"]]
    return {
        "platform": target_platform,
        "adapted_caption": caption,
        "hashtag_limit": limits["hashtag_count"],
        "aspect_ratio": limits["aspect_ratio"],
    }


def get_secondary_platforms(primary_platform: str, workflow_platforms: list[str]) -> list[str]:
    group = get_platform_group(primary_platform)
    return [p for p in workflow_platforms if p != primary_platform and p in PLATFORM_GROUPS.get(group, [])]

```
