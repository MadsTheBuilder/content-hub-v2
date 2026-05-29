"""NIM-powered report suggestion picker."""

import logging
from notebooklm.types import ReportSuggestion
from skills.utils.ai import generate

logger = logging.getLogger(__name__)


async def pick_best_report(
    suggestions: list[ReportSuggestion],
    goal: str,
) -> ReportSuggestion | None:
    """Pick the best report suggestion from a list using NIM.

    Args:
        suggestions: List of ReportSuggestion objects from get_suggested_reports.
        goal: Either "explainer" or "technical" — the target report type.

    Returns:
        Best matching ReportSuggestion, or None if no good match found.
    """
    if not suggestions:
        return None

    # Build a prompt listing the suggestions
    suggestion_text = "\n".join(
        f"- {s.title}: {s.description}"
        for s in suggestions
    )

    prompt = f"""Given these report suggestions:

{suggestion_text}

Which one best matches the goal of creating a {goal} report?
Return ONLY the exact title of the best match (no explanation).
If none match well, return "NONE"."""

    result = await generate(prompt, cascade=["nim"])
    if not result.get("success"):
        logger.warning("NIM report picker failed: %s", result.get("error"))
        return None

    best_title = result.get("text", "").strip()
    if best_title == "NONE" or not best_title:
        return None

    # Find and return the matching suggestion
    for suggestion in suggestions:
        if suggestion.title.strip() == best_title:
            return suggestion

    logger.warning("NIM returned title '%s' but no exact match found", best_title)
    return None
