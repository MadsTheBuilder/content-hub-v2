"""
Integration test: Happy-path E2E pipeline.

Exercises: Workflow fetch -> Synthesis -> Script generation -> Storyboard -> Render check
All using MockSupabaseClient and placeholder/fallback paths (no real API keys).
"""
import pytest
from backend.intelligence.synthesis import (
    extract_common_patterns,
    generate_strategy_document,
    StrategyDocument,
)
from backend.content.scripting import generate_script
from backend.content.storyboard import script_to_storyboard


class TestHappyPathPipeline:

    @pytest.mark.asyncio
    async def test_full_pipeline_slides(self, sample_posts, sample_brand_profile, sample_memory):
        """Workflow -> extract patterns -> strategy -> script -> storyboard (slides)."""

        # Step 1: Extract patterns from selected posts
        patterns = extract_common_patterns(sample_posts)
        assert patterns["pattern_confidence"] > 0
        assert patterns["dominant_hook_type"] != "unknown"

        # Step 2: Generate strategy (will use fallback path since Gemini is disabled)
        strategy = await generate_strategy_document(
            selected_posts=sample_posts,
            brand_profile=sample_brand_profile,
            content_pillars=["fitness", "home workouts"],
            platform="tiktok",
            memory=sample_memory,
        )
        assert isinstance(strategy, StrategyDocument)
        assert strategy.target_platform == "tiktok"
        # Fallback path builds strategy from first post
        assert strategy.content_angle != ""

        # Step 3: Generate script (will use placeholder since all LLMs disabled)
        strategy_dict = strategy.to_dict()
        script_result = await generate_script(
            content_type="slides",
            topic=strategy.content_angle,
            brand_voice="energetic and educational",
            content_pillars=["fitness"],
            research_context={},
            memory=sample_memory,
            platform="tiktok",
            strategy=strategy_dict,
        )
        assert script_result["success"] is True
        assert script_result["model_used"] == "placeholder"
        assert len(script_result["script"]) > 0

        # Step 4: Convert script to storyboard
        storyboard = script_to_storyboard(
            script_result["script"],
            "slides",
            {"secondary_color": "#1E293B", "primary_color": "#C9A96E"},
        )
        assert storyboard["type"] == "slides"
        assert len(storyboard["frames"]) > 0
        # Verify required frame fields per AGENTS.md contract
        for frame in storyboard["frames"]:
            assert "bg_gradient" in frame
            assert "accent_color" in frame
            assert "headline" in frame
            assert "body" in frame
            assert "slide_number" in frame

    @pytest.mark.asyncio
    async def test_full_pipeline_short_form(self, sample_posts, sample_brand_profile, sample_memory):
        """Pipeline for short_form content type."""

        strategy = await generate_strategy_document(
            selected_posts=sample_posts,
            brand_profile=sample_brand_profile,
            content_pillars=["fitness"],
            platform="tiktok",
            memory=sample_memory,
        )

        script_result = await generate_script(
            content_type="short_form",
            topic=strategy.content_angle or "Test topic",
            brand_voice="motivational",
            content_pillars=["fitness"],
            research_context={},
            memory={},
            platform="tiktok",
            strategy=strategy.to_dict(),
        )
        assert script_result["success"] is True

        storyboard = script_to_storyboard(script_result["script"], "short_form", {})
        assert storyboard["type"] == "short_form"
        assert len(storyboard["scenes"]) == 3
        # Verify enriched storyboard fields
        for scene in storyboard["scenes"]:
            assert "timing_marker" in scene
            assert "transition" in scene
            assert "text_overlay" in scene
            assert "audio_cues" in scene

    @pytest.mark.asyncio
    async def test_full_pipeline_talking_head(self, sample_posts, sample_brand_profile, sample_memory):
        """Pipeline for talking_head content type."""

        script_result = await generate_script(
            content_type="talking_head",
            topic="Home workout myths",
            brand_voice="casual but informative",
            content_pillars=["fitness"],
            research_context={},
            memory={},
            platform="youtube",
        )
        assert script_result["success"] is True

        storyboard = script_to_storyboard(script_result["script"], "talking_head", {})
        assert storyboard["type"] == "talking_head"
        assert "script" in storyboard["sections"]
        assert "shot_list" in storyboard["sections"]

    @pytest.mark.asyncio
    async def test_strategy_with_rejection_notes(self, sample_posts, sample_brand_profile, sample_memory):
        """Revise-strategy loop with rejection notes."""

        strategy = await generate_strategy_document(
            selected_posts=sample_posts,
            brand_profile=sample_brand_profile,
            content_pillars=["fitness"],
            platform="tiktok",
            memory=sample_memory,
            rejection_notes="Too generic, needs more personal angle",
        )
        # Even fallback path should return a valid StrategyDocument
        assert isinstance(strategy, StrategyDocument)
        assert strategy.content_angle != ""

    @pytest.mark.asyncio
    async def test_empty_inputs_pipeline_no_crash(self):
        """Pipeline should handle empty inputs gracefully."""
        strategy = await generate_strategy_document(
            selected_posts=[],
            brand_profile={},
            content_pillars=[],
            platform="tiktok",
            memory={},
        )
        assert isinstance(strategy, StrategyDocument)

        script_result = await generate_script(
            content_type="slides",
            topic="",
            brand_voice="",
            content_pillars=[],
            research_context={},
            memory={},
            platform="",
        )
        assert script_result["success"] is True

    @pytest.mark.asyncio
    async def test_pattern_to_strategy_data_flow(self, sample_posts, sample_brand_profile):
        """Verify extract_common_patterns output feeds correctly into strategy generation."""

        patterns = extract_common_patterns(sample_posts)

        # Patterns should reflect the sample data
        assert patterns["dominant_hook_type"] in ("number", "contrarian", "story")
        assert patterns["dominant_content_style"] == "educational"
        assert patterns["dominant_pacing"] == "fast"
        assert len(patterns["top_techniques"]) > 0

        # Strategy generation should not crash when receiving posts with analysis
        strategy = await generate_strategy_document(
            selected_posts=sample_posts,
            brand_profile=sample_brand_profile,
            content_pillars=["fitness"],
            platform="instagram",
            memory={},
        )
        assert strategy.target_platform == "instagram"
