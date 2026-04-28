"""Tests for backend.content.scripting — prompt construction + placeholder fallback."""
import pytest
from backend.content.scripting import _build_prompt, _placeholder_script


class TestBuildPrompt:
    def test_includes_topic_and_content_type(self):
        prompt = _build_prompt("slides", "home workouts", "", [], {}, {}, "tiktok")
        assert "home workouts" in prompt
        assert "slides" in prompt

    def test_includes_brand_voice(self):
        prompt = _build_prompt("short_form", "topic", "energetic and fun", [], {}, {}, "tiktok")
        assert "energetic and fun" in prompt

    def test_includes_strategy_angle(self):
        strategy = {
            "content_angle": "5 exercises that replace the gym",
            "why_this_angle": "listicle pattern",
        }
        prompt = _build_prompt(
            "short_form", "topic", "", [], {}, {}, "tiktok", strategy=strategy,
        )
        assert "5 exercises that replace the gym" in prompt
        assert "listicle pattern" in prompt

    def test_includes_strategy_user_notes(self):
        strategy = {
            "content_angle": "Test",
            "user_notes": "Make it more personal",
        }
        prompt = _build_prompt(
            "short_form", "topic", "", [], {}, {}, "tiktok", strategy=strategy,
        )
        assert "Make it more personal" in prompt

    def test_includes_memory_hook_preference(self):
        memory = {"preferred_hook_styles": {"question": 0.8, "story": 0.2}}
        prompt = _build_prompt("short_form", "topic", "", [], {}, memory, "tiktok")
        assert "question" in prompt

    def test_includes_topics_to_avoid(self):
        memory = {"topics_published": ["meal prep", "cardio HIIT"]}
        prompt = _build_prompt("short_form", "topic", "", [], {}, memory, "tiktok")
        assert "meal prep" in prompt
        assert "Already Covered" in prompt

    def test_includes_research_brief(self):
        research = {"research_brief": "This week fitness content is trending upward."}
        prompt = _build_prompt("short_form", "topic", "", [], research, {}, "tiktok")
        assert "trending upward" in prompt

    def test_includes_trending_context(self):
        research = {"trending_context": [{"title": "trending workout post"}]}
        prompt = _build_prompt("short_form", "topic", "", [], research, {}, "tiktok")
        assert "trending workout post" in prompt

    def test_includes_few_shot_examples(self):
        research = {"few_shot_examples": [{"content_text": "Example script: Hook..."}]}
        prompt = _build_prompt("short_form", "topic", "", [], research, {}, "tiktok")
        assert "Example script" in prompt

    def test_includes_brand_positioning(self):
        research = {
            "brand_profile": {
                "core_problem": "People lack confidence",
                "differentiators": ["science-backed"],
                "customer_language": ["gains", "shredded"],
            }
        }
        prompt = _build_prompt("short_form", "topic", "voice", [], research, {}, "tiktok")
        assert "People lack confidence" in prompt
        assert "science-backed" in prompt

    def test_includes_avg_script_length(self):
        memory = {"avg_script_length": {"short_form": 150}}
        prompt = _build_prompt("short_form", "topic", "", [], {}, memory, "tiktok")
        assert "150" in prompt

    def test_empty_inputs_no_crash(self):
        prompt = _build_prompt("short_form", "", "", [], {}, {}, "")
        assert isinstance(prompt, str)
        assert len(prompt) > 0


class TestPlaceholderScript:
    def test_slides_returns_json_array(self):
        result = _placeholder_script("slides", "Test Topic")
        assert "[{" in result
        assert "Test Topic" in result

    def test_short_form_has_hook_body_cta(self):
        result = _placeholder_script("short_form", "Fitness")
        assert "HOOK:" in result
        assert "BODY:" in result
        assert "CTA:" in result
        assert "Fitness" in result

    def test_talking_head_has_sections(self):
        result = _placeholder_script("talking_head", "Yoga")
        assert "SCRIPT:" in result
        assert "SHOT_LIST:" in result
        assert "ONSCREEN_TEXT:" in result

    def test_unknown_type_returns_placeholder(self):
        result = _placeholder_script("unknown", "Topic")
        assert "Topic" in result

    def test_short_form_placeholder_feeds_storyboard(self):
        """Placeholder output must be parseable by storyboard.py."""
        from backend.content.storyboard import script_to_storyboard
        script = _placeholder_script("short_form", "Test")
        storyboard = script_to_storyboard(script, "short_form", {})
        assert storyboard["type"] == "short_form"
        assert len(storyboard["scenes"]) == 3

    def test_slides_placeholder_feeds_storyboard(self):
        """Placeholder output must be parseable by storyboard.py."""
        from backend.content.storyboard import script_to_storyboard
        script = _placeholder_script("slides", "Test")
        storyboard = script_to_storyboard(script, "slides", {})
        assert storyboard["type"] == "slides"
        assert len(storyboard["frames"]) > 0
