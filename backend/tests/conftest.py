"""Shared test fixtures — forces mock mode, no real API calls."""
import pytest


@pytest.fixture(autouse=True)
def mock_supabase(monkeypatch):
    """Every test gets a fresh MockSupabaseClient — no real DB calls."""
    import backend.database as db_mod
    from backend.database import MockSupabaseClient
    client = MockSupabaseClient()
    monkeypatch.setattr(db_mod, "_client", client)
    yield client
    monkeypatch.setattr(db_mod, "_client", None)


@pytest.fixture(autouse=True)
def reset_genai_clients(monkeypatch):
    """Reset all lazy-init Gemini singletons so no real API keys are used."""
    modules = []
    try:
        import backend.intelligence.synthesis as syn
        modules.append(syn)
    except ImportError:
        pass
    try:
        import backend.content.scripting as scr
        modules.append(scr)
    except ImportError:
        pass
    try:
        import backend.intelligence.voice as vc
        modules.append(vc)
    except ImportError:
        pass
    try:
        import backend.research.rag as rag
        modules.append(rag)
    except ImportError:
        pass
    try:
        import backend.research.research_service as rs
        modules.append(rs)
    except ImportError:
        pass

    for mod in modules:
        monkeypatch.setattr(mod, "_genai_client", None)
        monkeypatch.setattr(mod, "_client_init_failed", True)  # Force no-API path
    yield
    for mod in modules:
        monkeypatch.setattr(mod, "_genai_client", None)
        monkeypatch.setattr(mod, "_client_init_failed", False)


@pytest.fixture
def sample_posts():
    """Realistic enriched trending posts with content_analysis."""
    return [
        {
            "id": "post-001",
            "title": "5 home workouts that burn fat faster than the gym",
            "description": "No equipment needed. Science-backed routines.",
            "platform": "tiktok",
            "author_username": "fitguru",
            "view_count": 125_000,
            "like_count": 8_500,
            "comment_count": 420,
            "share_count": 1_200,
            "organic_score": 92_000,
            "content_age_days": 3,
            "post_url": "https://tiktok.com/@fitguru/1",
            "thumbnail_url": "https://example.com/thumb1.jpg",
            "content_analysis": {
                "hook_type": "number",
                "content_style": "educational",
                "pacing": "fast",
                "engagement_drivers": ["curiosity gap", "save-worthy"],
                "why_it_works": "Number-based listicle creates curiosity.",
                "applicable_techniques": ["number hook", "quick cuts", "text overlay"],
            },
        },
        {
            "id": "post-002",
            "title": "I quit the gym for 30 days — here's what happened",
            "description": "My home workout transformation journey.",
            "platform": "tiktok",
            "author_username": "alexfitness",
            "view_count": 89_000,
            "like_count": 6_200,
            "comment_count": 310,
            "share_count": 800,
            "organic_score": 65_000,
            "content_age_days": 7,
            "post_url": "https://tiktok.com/@alexfitness/2",
            "thumbnail_url": None,
            "content_analysis": {
                "hook_type": "story",
                "content_style": "motivational",
                "pacing": "medium",
                "engagement_drivers": ["personal story", "transformation"],
                "why_it_works": "Personal transformation story drives empathy.",
                "applicable_techniques": ["story hook", "before/after"],
            },
        },
        {
            "id": "post-003",
            "title": "Stop doing crunches if you want abs",
            "description": "The exercises that actually work.",
            "platform": "instagram",
            "author_username": "abscoach",
            "view_count": 201_000,
            "like_count": 15_000,
            "comment_count": 890,
            "share_count": 3_400,
            "organic_score": 180_000,
            "content_age_days": 1,
            "post_url": "https://instagram.com/p/abc",
            "thumbnail_url": "https://example.com/thumb3.jpg",
            "content_analysis": {
                "hook_type": "contrarian",
                "content_style": "educational",
                "pacing": "fast",
                "engagement_drivers": ["contrarian take", "myth busting"],
                "why_it_works": "Contrarian hook challenges common belief.",
                "applicable_techniques": ["contrarian hook", "myth busting", "text overlay"],
            },
        },
    ]


@pytest.fixture
def sample_brand_profile():
    """Realistic brand profile dict."""
    return {
        "tone": "motivational but grounded in science",
        "audience_interests": ["home workouts", "fitness", "nutrition"],
        "content_preferences": ["educational", "science-based"],
        "core_problem": "People think they need a gym to get fit",
        "differentiators": ["science-backed", "no-equipment focus"],
        "customer_language": ["gains", "no excuses", "home gym"],
    }


@pytest.fixture
def sample_memory():
    """Realistic publication memory dict."""
    return {
        "published_count": 5,
        "content_type_distribution": {"short_form": 0.6, "slides": 0.4},
        "avg_script_length": {"short_form": 150, "slides": 80},
        "preferred_hook_styles": {"question": 0.5, "number": 0.3, "story": 0.2},
        "topics_published": ["morning routine", "meal prep basics", "HIIT cardio"],
        "platform_content_map": {"tiktok": "short_form"},
        "recurring_notes": ["use personal photos", "cite studies"],
    }
