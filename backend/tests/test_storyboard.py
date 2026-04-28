"""Tests for backend.content.storyboard — script to frame conversion."""
import json
import pytest
from backend.content.storyboard import script_to_storyboard, _strip_label


class TestStripLabel:
    def test_removes_bold_markers(self):
        assert _strip_label("**HOOK:**") == "HOOK:"

    def test_removes_timing_markers(self):
        # _strip_label strips timing but space before parens stays: "Hook :" after .strip()
        assert _strip_label("Hook (0-3s):") == "Hook :"

    def test_strips_whitespace(self):
        assert _strip_label("  Body  ") == "Body"

    def test_combined_markers(self):
        # Bold removed, timing removed, space before parens stays
        assert _strip_label("**Body** (3-17s):") == "Body :"


class TestSlidesStoryboard:
    def test_parses_valid_json_slides(self):
        script = json.dumps([
            {"slide": 1, "headline": "Title", "body": "Content"},
            {"slide": 2, "headline": "Data", "body": "Numbers"},
        ])
        brand = {"secondary_color": "#1E293B", "primary_color": "#C9A96E"}
        result = script_to_storyboard(script, "slides", brand)
        assert result["type"] == "slides"
        assert len(result["frames"]) == 2
        assert result["frames"][0]["headline"] == "Title"
        assert result["frames"][0]["slide_number"] == 1
        assert "bg_gradient" in result["frames"][0]
        assert "accent_color" in result["frames"][0]

    def test_invalid_json_falls_back(self):
        result = script_to_storyboard("not json at all", "slides", {})
        assert result["type"] == "slides"
        assert len(result["frames"]) == 1
        assert result["frames"][0]["body"] == "not json at all"[:100]

    def test_brand_colors_flow_through(self):
        script = json.dumps([{"slide": 1, "headline": "H", "body": "B"}])
        brand = {"secondary_color": "#FF0000", "accent_color": "#00FF00"}
        result = script_to_storyboard(script, "slides", brand)
        assert "#FF0000" in result["frames"][0]["bg_gradient"]
        assert result["frames"][0]["accent_color"] == "#00FF00"

    def test_slide_level_color_overrides(self):
        script = json.dumps([
            {"slide": 1, "headline": "H", "body": "B",
             "accent_color": "#CUSTOM", "bg_gradient": "linear-gradient(red, blue)"},
        ])
        result = script_to_storyboard(script, "slides", {})
        assert result["frames"][0]["accent_color"] == "#CUSTOM"
        assert result["frames"][0]["bg_gradient"] == "linear-gradient(red, blue)"

    def test_topic_type_uses_slides_storyboard(self):
        script = json.dumps([{"slide": 1, "headline": "H", "body": "B"}])
        result = script_to_storyboard(script, "topic", {})
        assert result["type"] == "slides"

    def test_slide_template_from_brand(self):
        script = json.dumps([{"slide": 1, "headline": "H", "body": "B"}])
        brand = {"slide_template": "dark_minimalist"}
        result = script_to_storyboard(script, "slides", brand)
        assert result["frames"][0]["template"] == "dark_minimalist"

    def test_default_template(self):
        script = json.dumps([{"slide": 1, "headline": "H", "body": "B"}])
        result = script_to_storyboard(script, "slides", {})
        assert result["frames"][0]["template"] == "default"

    def test_frame_contract_fields(self):
        """Verify AGENTS.md contract: every frame has bg_gradient, accent_color, headline, body, slide_number."""
        script = json.dumps([{"slide": 1, "headline": "H", "body": "B"}])
        result = script_to_storyboard(script, "slides", {})
        frame = result["frames"][0]
        for key in ("bg_gradient", "accent_color", "headline", "body", "slide_number"):
            assert key in frame, f"Missing required field: {key}"


class TestVideoStoryboard:
    def test_parses_hook_body_cta(self):
        script = "HOOK: Did you know?\nBODY: Here's the truth.\nCTA: Follow me!"
        result = script_to_storyboard(script, "short_form", {})
        assert result["type"] == "short_form"
        assert len(result["scenes"]) == 3
        assert "Did you know?" in result["scenes"][0]["text"]
        assert "Follow me!" in result["scenes"][2]["text"]

    def test_enriched_storyboard_fields(self):
        script = "HOOK: Test\nBODY: Content\nCTA: Act now"
        result = script_to_storyboard(script, "short_form", {})
        hook = result["scenes"][0]
        assert hook["timing_marker"] == "0-3s"
        assert hook["transition"] == "zoom_in"
        assert "text_overlay" in hook
        assert "audio_cues" in hook
        assert result["duration_seconds"] == 20

    def test_body_continuation_lines(self):
        script = "HOOK: Start\nBODY: First line\nMore body content\nCTA: End"
        result = script_to_storyboard(script, "short_form", {})
        assert "More body content" in result["scenes"][1]["text"]

    def test_scene_durations_sum_to_total(self):
        script = "HOOK: H\nBODY: B\nCTA: C"
        result = script_to_storyboard(script, "short_form", {})
        total = sum(s["duration"] for s in result["scenes"])
        assert total == result["duration_seconds"]


class TestTalkingHeadStoryboard:
    def test_parses_all_sections(self):
        script = "SCRIPT: Hello everyone.\nSHOT_LIST: Medium shot\nONSCREEN_TEXT: Title"
        result = script_to_storyboard(script, "talking_head", {})
        assert result["type"] == "talking_head"
        assert "Hello everyone" in result["sections"]["script"]
        assert "Medium shot" in result["sections"]["shot_list"]
        assert "Title" in result["sections"]["onscreen_text"]

    def test_alternative_section_names(self):
        script = "SCRIPT: Hello.\nSHOT LIST: Wide shot\nONSCREEN TEXT: Overlay"
        result = script_to_storyboard(script, "talking_head", {})
        assert "Wide shot" in result["sections"]["shot_list"]
        assert "Overlay" in result["sections"]["onscreen_text"]


class TestUnknownContentType:
    def test_returns_empty_frames(self):
        result = script_to_storyboard("anything", "unknown_type", {})
        assert result == {"frames": []}
