"""Tests for backend.intelligence.memory — pure helper functions."""
import pytest
from backend.intelligence.memory import _detect_hook_style, _topics_similar


class TestDetectHookStyle:
    def test_question_hook(self):
        assert _detect_hook_style("Did you know this about fitness?") == "question"

    def test_stat_hook_with_percent(self):
        assert _detect_hook_style("80% of people fail at this") == "stat"

    def test_stat_hook_with_x(self):
        assert _detect_hook_style("3x more effective than the gym") == "stat"

    def test_story_hook(self):
        assert _detect_hook_style("When I first started my journey") == "story"

    def test_story_hook_with_my(self):
        assert _detect_hook_style("My transformation took 6 months") == "story"

    def test_contrarian_hook_stop(self):
        assert _detect_hook_style("Stop doing crunches right now") == "contrarian"

    def test_contrarian_hook_never(self):
        assert _detect_hook_style("Never eat these 5 foods") == "contrarian"

    def test_contrarian_hook_dont(self):
        assert _detect_hook_style("Don't do this exercise anymore") == "contrarian"

    def test_statement_fallback(self):
        assert _detect_hook_style("The best workout for beginners") == "statement"

    def test_empty_string(self):
        assert _detect_hook_style("") == "statement"

    def test_multiline_uses_first_line(self):
        assert _detect_hook_style("Is this effective?\nBody text here") == "question"


class TestTopicsSimilar:
    def test_identical_topics(self):
        assert _topics_similar("home workouts", "home workouts") is True

    def test_high_overlap(self):
        assert _topics_similar("home workout routine", "home workout tips") is True

    def test_no_overlap(self):
        assert _topics_similar("cooking pasta", "quantum physics") is False

    def test_partial_overlap_below_threshold(self):
        # 1 out of 3 words match = 33% < 50%
        assert _topics_similar("home workout routine", "home cooking tips") is False

    def test_empty_strings(self):
        assert _topics_similar("", "") is False
        assert _topics_similar("something", "") is False

    def test_single_word_match(self):
        assert _topics_similar("fitness", "fitness") is True

    def test_case_already_lowered(self):
        # Function expects pre-lowered input from caller
        assert _topics_similar("home workouts", "home workouts") is True
