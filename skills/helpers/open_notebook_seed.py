"""Seed research questions from README text using OpenRouter."""

import json
import logging

from skills.utils.ai import _openrouter_generate

logger = logging.getLogger(__name__)

_FALLBACK = [
    ("Core Functionality", "What are the main features and capabilities of this project?"),
    ("Getting Started", "What is the fastest path to getting this project running?"),
    ("Common Pitfalls", "What are the most common mistakes developers make with this?"),
    ("Integration Patterns", "How does this integrate with other tools and systems?"),
    ("Performance Trade-offs", "What are the performance characteristics and limitations?"),
    ("Alternatives Comparison", "How does this compare to similar tools in the ecosystem?"),
]


async def seed_questions_from_readme(readme_text: str, owner_repo: str) -> list[tuple[str, str]]:
    """Generate seed research questions from README text using OpenRouter.

    Returns [(heading, question), ...] — same format as nlm_seed.py.
    Falls back to 6 generic questions if OpenRouter fails.
    """
    prompt = (
        f"You are generating research questions for the GitHub project '{owner_repo}'.\n\n"
        f"README:\n{readme_text[:3000]}\n\n"
        f"Generate 6 specific questions a developer would want answered. "
        f"Cover: what it does, how to use it, common pitfalls, integration, performance, alternatives.\n\n"
        f"Return ONLY a JSON array — no markdown, no code fences:\n"
        f'[{{"heading": "short label 3-6 words", "question": "full question"}}, ...]'
    )

    try:
        result = await _openrouter_generate(prompt, model="google/gemma-4-31b-it:free")
        if not result["success"]:
            raise RuntimeError(result.get("error", "OpenRouter failed"))
        raw = result["text"].strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "```"), len(lines))
            raw = "\n".join(lines[1:end])
        items = json.loads(raw)
        return [
            (item["heading"], item["question"])
            for item in items
            if "heading" in item and "question" in item
        ]
    except Exception as e:
        logger.warning("seed_questions_from_readme failed (%s), using fallbacks", e)
        return _FALLBACK
