"""Outline Scorer — Evaluates video outline via LLM-judge.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {composite_judge_score: float (0-10), section_count: int}
- composite_judge_score: LLM assessment of structure quality (6 stages, talking points, pacing)
- section_count: Count of major sections (programmatic — exact integer)
"""

import re
from prompt_lab.scorers._judge import call_judge


def score_outline_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score a video outline.

    Args:
        output: The outline markdown from the outline skill (Dopamine Ladder structure).
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {composite_judge_score: float (0-10), section_count: int}
    """
    if not output:
        return {"composite_judge_score": 0.0, "section_count": 0}

    # Count sections programmatically (## headings = major sections)
    section_count = _count_sections(output)

    # Use LLM judge for quality assessment
    judge_result = _judge_outline_quality(output)

    # Return both metrics
    composite_score = judge_result.get("score", 0.0) if judge_result.get("success") else 0.0
    return {
        "composite_judge_score": float(composite_score),
        "section_count": int(section_count),
    }


def _count_sections(outline: str) -> int:
    """Count ## headings (major sections in the outline)."""
    sections = re.findall(r"^##\s+", outline, re.MULTILINE)
    return len(sections)


def _judge_outline_quality(outline: str) -> dict:
    """
    Call Claude to judge outline quality.

    Returns: {"success": bool, "score": float (0-10), "reasoning": str}
    """
    rubric = """You are evaluating a video outline for retention and engagement.

Score 0-10 on these axes:

**Dopamine Ladder Structure (0-10):** Does the outline follow the Dopamine Ladder (6 stages)?
Expected stages: Hook → Problem/Tension → Curiosity → Payoff/Solution → Proof/Examples → Call-to-Action
- 10: All 6 stages present and well-ordered; clear transitions between stages
- 7: 5-6 stages present; mostly logical flow
- 4: 3-4 stages; gaps in the progression
- 1: 1-2 stages only; disjointed flow
- 0: No recognizable Dopamine Ladder structure

**Talking Points Specificity (0-10):** Are the talking points specific and actionable, not generic?
- 10: Every point is concrete, specific, with examples or data implied
- 7: Most points are specific; some generic filler
- 4: Mix of specific and generic; needs refinement
- 1: Mostly generic platitudes
- 0: No actual talking points; just headings

**Pacing & Duration Fit (0-10):** Do section durations seem realistic for a cohesive video?
- 10: Durations are proportional and logical (e.g., hook is brief, body has substance)
- 7: Mostly good pacing; one section feels off
- 4: Pacing inconsistent; some sections too short/long
- 1: Severely unbalanced (e.g., 80% hook, 20% content)
- 0: No timing information; impossible to assess

Return ONLY JSON: {"score": <avg of three axes>, "reasoning": "<1 sentence on strongest axis>"}

---

OUTLINE TO EVALUATE:

{outline}"""

    rubric_filled = rubric.format(outline=outline[:4000])  # Truncate to avoid token bloat
    result = call_judge(rubric_filled, timeout_sec=90)

    if not result["success"]:
        return {"success": False, "score": 0.0, "reasoning": result.get("error", "Judge failed")}

    # Parse result
    try:
        scores = result["scores"]
        score = float(scores.get("score", 0.0))
        reasoning = scores.get("reasoning", "")
        return {"success": True, "score": score, "reasoning": reasoning}
    except (KeyError, ValueError, TypeError) as e:
        return {"success": False, "score": 0.0, "reasoning": f"Parse error: {str(e)[:50]}"}
