"""Tests for backend.intelligence.voice — competitor parsing + data structures."""
import pytest
from backend.intelligence.voice import (
    parse_competitors,
    CompetitorConfig,
    BrandProfile,
    PillarConfig,
    VoiceConfig,
)


class TestParseCompetitors:
    def test_strips_at_symbol(self):
        result = parse_competitors(["@alexfitness", "@yogawithserena"], ["tiktok"])
        assert "alexfitness" in result.profiles["tiktok"]
        assert "yogawithserena" in result.profiles["tiktok"]

    def test_handles_raw_names(self):
        result = parse_competitors(["GymShark", "fitpro"], ["youtube"])
        assert "GymShark" in result.profiles["youtube"]
        assert "fitpro" in result.profiles["youtube"]

    def test_assigns_to_all_platforms(self):
        result = parse_competitors(["@user1"], ["tiktok", "youtube", "instagram"])
        assert "user1" in result.profiles["tiktok"]
        assert "user1" in result.profiles["youtube"]
        assert "user1" in result.profiles["instagram"]

    def test_deduplicates(self):
        result = parse_competitors(["@user1", "user1", "@USER1"], ["tiktok"])
        # Case-insensitive dedup
        assert len(result.profiles["tiktok"]) == 1

    def test_empty_list(self):
        result = parse_competitors([], ["tiktok"])
        assert result.profiles["tiktok"] == []

    def test_empty_entries_skipped(self):
        result = parse_competitors(["", "  ", "@valid"], ["tiktok"])
        assert len(result.profiles["tiktok"]) == 1
        assert "valid" in result.profiles["tiktok"]

    def test_mixed_formats(self):
        result = parse_competitors(
            ["@alex", "raw_user", "  @spaced  ", "noat"],
            ["tiktok"],
        )
        usernames = result.profiles["tiktok"]
        assert len(usernames) == 4
        assert "alex" in usernames
        assert "raw_user" in usernames
        assert "spaced" in usernames
        assert "noat" in usernames

    def test_no_platforms(self):
        result = parse_competitors(["@user"], [])
        assert result.profiles == {}


class TestDataStructures:
    def test_brand_profile_to_dict(self):
        bp = BrandProfile(tone="energetic", audience_interests=["fitness"])
        d = bp.to_dict()
        assert d["tone"] == "energetic"
        assert d["audience_interests"] == ["fitness"]
        assert "core_problem" in d
        assert "differentiators" in d
        assert "customer_language" in d

    def test_brand_profile_defaults(self):
        bp = BrandProfile()
        assert bp.energy == "medium"
        assert bp.tone == ""
        assert bp.mentioned_accounts == []
        assert bp.objections == []

    def test_voice_config_defaults(self):
        vc = VoiceConfig()
        assert isinstance(vc.competitor_config, CompetitorConfig)
        assert isinstance(vc.brand_profile, BrandProfile)
        assert isinstance(vc.pillar_config, PillarConfig)

    def test_pillar_config_defaults(self):
        pc = PillarConfig()
        assert pc.pillars == []
        assert pc.expanded_terms == {}
        assert pc.scrape_config == {}
