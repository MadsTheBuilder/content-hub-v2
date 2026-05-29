"""Ideation Scorer — Evaluates video idea generation via LLM-judge.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {composite_judge_score: float (0-10), variant_count: int}
- composite_judge_score: LLM assessment of ideas (distinctness, gap reasoning, audience desire)
- variant_count: Count of distinct ideas (programmatic — exact integer)
"""

import re
from prompt_lab.scorers._judge import call_judge


def score_ideation_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score ideation output (9 ranked video ideas).

    Args:
        output: The ideation markdown from the ideation skill (9 ideas expected).
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {composite_judge_score: float (0-10), variant_count: int}
    """
    if not output:
        return {"composite_judge_score": 0.0, "variant_count": 0}

    # Count distinct ideas programmatically (each numbered idea is one variant)
    variant_count = _count_ideas(output)

    # Use LLM judge for quality assessment
    judge_result = _judge_idea_quality(output)

    # Return both metrics
    composite_score = judge_result.get("score", 0.0) if judge_result.get("success") else 0.0
    return {
        "composite_judge_score": float(composite_score),
        "variant_count": int(variant_count),
    }


def _count_ideas(ideation: str) -> int:
    """Count numbered ideas (1., 2., etc.) — rough count of distinct video ideas."""
    # Match numbered list items (1., 2., 3., etc.)
    ideas = re.findall(r"^[\s]*\d+\.", ideation, re.MULTILINE)
    return len(ideas)


def _judge_idea_quality(ideation: str) -> dict:
    """
    Call Claude to judge ideation quality.

    Returns: {"success": bool, "score": float (0-10), "reasoning": str}
    """
    rubric = """You are evaluating a batch of video ideas ranked by originality and audience desire.

Score 0-10 on these axes:

**Distinctness (0-10):** Are the 9 ideas truly distinct from each other and from trending content?
- 10: Each idea has a unique angle; none overlap
- 7: Most ideas distinct; 1-2 overlap slightly
- 4: Several ideas feel similar or incremental
- 1: Ideas are redundant variations on one theme
- 0: All ideas are identical or near-identical

**Gap Reasoning (0-10):** Does each idea explain WHY it's underexplored?
- 10: Each idea has explicit reasoning about market gap or audience need
- 7: Most ideas justify their premise
- 4: Some ideas mention gaps; others are unjustified
- 1: Little to no explanation of why these ideas matter
- 0: No gap analysis

**Audience Desire Mapping (0-10):** Is there evidence that audiences actually want these ideas?
- 10: Each idea maps to specific audience pain point or curiosity loop
- 7: Most ideas connected to audience signals
- 4: Some audience reasoning; mostly generic
- 1: Vague audience assumptions
- 0: No audience signal

Return ONLY JSON: {"score": <avg of three axes>, "reasoning": "<1 sentence on strongest axis>"}

---

IDEAS TO EVALUATE:

{ideation}"""

    rubric_filled = rubric.format(ideation=ideation[:4000])  # Truncate to avoid token bloat
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
