"""Seed questions from NotebookLM suggested topics."""

from notebooklm import NotebookLMClient


async def seed_questions_from_nlm(notebook_id: str) -> list[tuple[str, str]]:
    """Get suggested questions from a NotebookLM notebook.

    Args:
        notebook_id: The notebook ID.

    Returns:
        List of (question, prompt) tuples from notebook's suggested topics.
    """
    async with await NotebookLMClient.from_storage(timeout=60) as client:
        desc = await client.notebooks.get_description(notebook_id)
    return [(t.question, t.prompt or t.question) for t in desc.suggested_topics]
