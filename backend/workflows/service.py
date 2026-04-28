import logging

from backend.database import get_supabase
from backend.workflows.templates import NICHE_TEMPLATES
from backend.intelligence.voice import build_voice_config

logger = logging.getLogger(__name__)


def build_apify_config_from_questionnaire(answers: dict) -> dict:
    search_terms = answers.get("search_terms", "").split(",")
    hashtags = [t.strip().lstrip("#") for t in search_terms if t.strip()]
    platforms = answers.get("platforms", [])
    config = {}
    for platform in platforms:
        p = platform.lower().replace("/x", "").strip()
        if p in ("tiktok", "instagram"):
            config[p] = {"hashtags": hashtags}
        elif p in ("youtube", "linkedin", "twitter"):
            config[p] = {"keywords": hashtags}
    return config


async def create_workflow(user_id: str, data: dict) -> dict:
    sb = get_supabase()
    template = NICHE_TEMPLATES.get(data["template_type"], NICHE_TEMPLATES["custom"])

    brand_voice = data.get("brand_voice", "")
    competitors = data.get("competitors", [])
    pillars = data.get("content_pillars") or template["content_pillars"]
    platforms = data.get("platforms") or template["platform_defaults"]

    # Base apify config from questionnaire or template
    base_apify_config = (
        build_apify_config_from_questionnaire(data["questionnaire_answers"])
        if data.get("questionnaire_answers")
        else dict(template["apify_search_config"])
    )

    # Voice Engine: parse persona, competitors, pillars into actionable intelligence
    brand_profile = {}
    try:
        voice_config = await build_voice_config(brand_voice, competitors, pillars, platforms)
        brand_profile = voice_config.brand_profile.to_dict()

        # Merge expanded pillar terms into apify config
        for platform, config in voice_config.pillar_config.scrape_config.items():
            if platform not in base_apify_config:
                base_apify_config[platform] = config
            else:
                existing = base_apify_config[platform]
                for key in ("hashtags", "keywords"):
                    if key in config:
                        existing_terms = existing.get(key, [])
                        merged = list(dict.fromkeys(existing_terms + config[key]))
                        existing[key] = merged

        # Add competitor profiles to apify config
        for platform, usernames in voice_config.competitor_config.profiles.items():
            if usernames:
                if platform not in base_apify_config:
                    base_apify_config[platform] = {}
                base_apify_config[platform]["profiles"] = usernames

        logger.info("Voice Engine processed workflow: %d competitors, %d pillars expanded",
                     sum(len(v) for v in voice_config.competitor_config.profiles.values()),
                     len(voice_config.pillar_config.expanded_terms))
    except Exception:
        logger.exception("Voice Engine failed, proceeding with defaults.")

    workflow_data = {
        "user_id": user_id,
        "name": data["name"],
        "template_type": data["template_type"],
        "brand_voice": brand_voice,
        "content_pillars": pillars,
        "platforms": platforms,
        "posting_cadence": data.get("posting_cadence", {}),
        "competitors": competitors,
        "questionnaire_answers": data.get("questionnaire_answers"),
        "apify_search_config": base_apify_config,
        "brand_profile": brand_profile,
    }
    result = sb.table("workflows").insert(workflow_data).execute()
    workflow = result.data[0]

    sb.table("brand_configs").insert({"workflow_id": workflow["id"]}).execute()
    sb.table("content_publication_memory").insert({"workflow_id": workflow["id"]}).execute()
    sb.table("content_style_profiles").insert({"workflow_id": workflow["id"]}).execute()

    return workflow
