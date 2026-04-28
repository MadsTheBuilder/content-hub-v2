"""Tests for backend.intelligence.synthesis — pure computation functions."""
import pytest
from backend.intelligence.synthesis import (
    extract_common_patterns,
    compute_relevance_score,
    StrategyDocument,
)


class TestExtractCommonPatterns:
    def test_dominant_patterns_from_enriched_posts(self, sample_posts):
        result = extract_common_patterns(sample_posts)
        assert result["pattern_confidence"] == 1.0
        assert result["dominant_content_style"] == "educational"  # 2 of 3
        assert result["dominant_pacing"] == "fast"  # 2 of 3
        assert isinstance(result["top_techniques"], list)
        assert len(result["top_techniques"]) <= 3

    def test_empty_posts_returns_unknowns(self):
        result = extract_common_patterns([])
        assert result["dominant_hook_type"] == "unknown"
        assert result["dominant_content_style"] == "unknown"
        assert result["pattern_confidence"] == 0

    def test_posts_without_analysis_lowers_confidence(self):
        posts = [{"id": "1"}, {"id": "2", "content_analysis": {"hook_type": "question"}}]
        result = extract_common_patterns(posts)
        assert result["pattern_confidence"] == 0.5
        assert result["dominant_hook_type"] == "question"

    def test_none_analysis_is_skipped(self):
        posts = [{"id": "1", "content_analysis": None}]
        result = extract_common_patterns(posts)
        assert result["pattern_confidence"] == 0

    def test_single_post_full_confidence(self):
        posts = [{"id": "1", "content_analysis": {
            "hook_type": "story",
            "content_style": "entertaining",
            "pacing": "slow",
            "applicable_techniques": ["vlog style"],
        }}]
        result = extract_common_patterns(posts)
        assert result["pattern_confidence"] == 1.0
        assert result["dominant_hook_type"] == "story"
        assert result["dominant_content_style"] == "entertaining"
        assert result["dominant_pacing"] == "slow"
        assert "vlog style" in result["top_techniques"]


class TestComputeRelevanceScore:
    def test_perfect_pillar_match_boosts_score(self, sample_brand_profile):
        post = {
            "title": "home workouts for beginners",
            "description": "fitness tips",
            "organic_score": 100_000,
            "content_age_days": 1,
        }
        score = compute_relevance_score(post, sample_brand_profile, ["home workouts", "fitness"])
        assert score > 50  # strong pillar + organic + audience + recency

    def test_no_match_gives_low_score(self):
        post = {
            "title": "cooking show episode 5",
            "description": "making pasta",
            "organic_score": 10,
            "content_age_days": 30,
        }
        score = compute_relevance_score(post, {}, ["blockchain"])
        assert score < 15

    def test_recency_bonus(self, sample_brand_profile):
        recent = {"title": "fitness", "description": "", "organic_score": 100, "content_age_days": 1}
        old = {"title": "fitness", "description": "", "organic_score": 100, "content_age_days": 30}
        score_recent = compute_relevance_score(recent, sample_brand_profile, ["fitness"])
        score_old = compute_relevance_score(old, sample_brand_profile, ["fitness"])
        assert score_recent > score_old

    def test_empty_inputs_no_crash(self):
        score = compute_relevance_score({}, {}, [])
        assert isinstance(score, float)
        assert score >= 0

    def test_high_organic_score_contributes(self):
        low = {"title": "", "description": "", "organic_score": 1, "content_age_days": 15}
        high = {"title": "", "description": "", "organic_score": 1_000_000, "content_age_days": 15}
        score_low = compute_relevance_score(low, {}, [])
        score_high = compute_relevance_score(high, {}, [])
        assert score_high > score_low


class TestStrategyDocument:
    def test_to_dict_returns_all_fields(self):
        doc = StrategyDocument(content_angle="Test angle", target_platform="tiktok")
        d = doc.to_dict()
        assert d["content_angle"] == "Test angle"
        assert d["target_platform"] == "tiktok"
        assert "recommended_format" in d
        assert "estimated_performance" in d
        assert "alternatives" in d

    def test_default_values(self):
        doc = StrategyDocument()
        assert doc.content_angle == ""
        assert doc.recommended_format["type"] == "short_form"
        assert doc.estimated_performance["confidence"] == "low"

    def test_alternatives_default_empty(self):
        doc = StrategyDocument()
        assert doc.alternatives == []

    def test_user_notes_default_empty(self):
        doc = StrategyDocument()
        assert doc.user_notes == ""
