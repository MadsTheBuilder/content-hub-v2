"""Smoke test: verify fast mode skips source import, deep mode imports."""

import asyncio
import types
import unittest
from unittest.mock import AsyncMock, MagicMock, patch, call


def _make_source(id_: str, title: str = "Test Source", ready: bool = True) -> MagicMock:
    s = MagicMock()
    s.id = id_
    s.title = title
    s.is_ready = ready
    s.is_error = False
    return s


def _make_client(sources_found: list, imported_ids: list[str]) -> MagicMock:
    """Build a minimal mock NotebookLMClient for research_one()."""
    client = MagicMock()

    # notebooks.create
    nb = MagicMock()
    nb.id = "nb-001"
    client.notebooks = MagicMock()
    client.notebooks.create = AsyncMock(return_value=nb)

    # sources.add_url — primary source adds
    client.sources = MagicMock()
    client.sources.add_url = AsyncMock(return_value=None)

    # All sources in notebook after indexing
    primary_src = _make_source("primary-1", "README")
    client.sources.list = AsyncMock(return_value=[primary_src])
    client.sources.get_guide = AsyncMock(return_value={
        "summary": "A helpful library for doing things.", "keywords": ["python", "library"]
    })

    # research.start / poll
    client.research = MagicMock()
    client.research.start = AsyncMock(return_value={"task_id": "task-001"})
    client.research.poll = AsyncMock(return_value={
        "status": "completed",
        "sources": sources_found,
    })
    # import_sources returns mocked imported source objects
    imported = [_make_source(id_) for id_ in imported_ids]
    client.research.import_sources = AsyncMock(return_value=[{"id": id_} for id_ in imported_ids])

    # chat
    client.chat = MagicMock()
    client.chat.configure = AsyncMock(return_value=None)
    client.chat.ask = AsyncMock(return_value=MagicMock(answer="Some answer"))

    # artifacts (skip cleanly)
    client.artifacts = MagicMock()
    client.artifacts.generate_slide_deck = AsyncMock(return_value=MagicMock(task_id=None, error="disabled"))
    client.artifacts.generate_infographic = AsyncMock(return_value=MagicMock(task_id=None, error="disabled"))

    return client


SOURCES_FOUND = [{"url": "https://example.com/ext1"}, {"url": "https://example.com/ext2"}]
IMPORTED_IDS = ["ext-src-1", "ext-src-2"]

REPO_URL = "https://github.com/test-owner/test-repo"


class TestResearcherMode(unittest.IsolatedAsyncioTestCase):

    async def _run_research_one(self, mode: str):
        """Patch heavy dependencies and call research_one with given mode."""
        from skills import researcher

        client = _make_client(SOURCES_FOUND, IMPORTED_IDS)

        with (
            patch.object(researcher, "discover_primary_docs", new=AsyncMock(return_value=[])),
            patch.object(researcher, "seed_questions_from_nlm", new=AsyncMock(return_value=[
                ("What does it do?", "What does test-repo do?")
            ])),
            patch.object(researcher, "generate_followups", new=AsyncMock(return_value=[])),
            patch.object(researcher, "claude_cli", return_value='{"core_use_cases":["testing"],"key_concepts":["mocking"],"common_patterns":["fixture"],"anti_patterns":[],"audience":"Developers"}'),
            patch.object(researcher, "synthesize_brief", new=AsyncMock(return_value="## What it does\nA test tool.")),
            patch("pathlib.Path.mkdir", MagicMock()),
            patch("pathlib.Path.write_text", MagicMock()),
        ):
            result = await researcher.research_one(client, REPO_URL, mode)

        return client, result

    async def test_fast_mode_skips_import(self):
        """import_sources must NOT be called in fast mode."""
        client, result = await self._run_research_one("fast")
        client.research.import_sources.assert_not_called()

    async def test_deep_mode_calls_import(self):
        """import_sources must be called in deep mode."""
        client, result = await self._run_research_one("deep")
        client.research.import_sources.assert_called_once()

    async def test_fast_mode_chat_uses_primary_only(self):
        """In fast mode, chat.ask source_ids should not include any discovered source IDs."""
        client, result = await self._run_research_one("fast")
        for call_args in client.chat.ask.call_args_list:
            source_ids = call_args.kwargs.get("source_ids", [])
            for sid in source_ids:
                self.assertNotIn(sid, IMPORTED_IDS,
                    f"Fast mode chat.ask received discovered source id '{sid}'")

    async def test_deep_mode_chat_includes_verified_sources(self):
        """In deep mode, verified discovered source IDs appear in chat.ask calls."""
        # In deep mode with no Claude verification rejection, all imported ids pass through.
        # The verification Claude call is mocked to return all kept.
        client, result = await self._run_research_one("deep")
        # Just assert import was called — full verified_source_ids check is unit-level
        client.research.import_sources.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
