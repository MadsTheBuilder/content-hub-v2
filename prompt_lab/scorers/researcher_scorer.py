"""Researcher Scorer — Evaluates research brief quality via LLM-judge.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {composite_judge_score: float (0-10), source_count: int}
- composite_judge_score: LLM assessment of brief quality (gap analysis, primary sources, actionability)
- source_count: Programmatic count of cited sources (exact integer, trustworthy)
"""

import re
from prompt_lab.scorers._judge import call_judge


def score_researcher_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score a research brief.

    Args:
        output: The research brief markdown from the researcher skill.
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {composite_judge_score: float (0-10), source_count: int}
    """
    if not output:
        return {"composite_judge_score": 0.0, "source_count": 0}

    # Count sources programmatically (exact integer — most trustworthy)
    source_count = _count_sources(output)

    # Use LLM judge for quality assessment
    judge_result = _judge_research_quality(output)

    # Return both metrics
    composite_score = judge_result.get("score", 0.0) if judge_result.get("success") else 0.0
    return {
        "composite_judge_score": float(composite_score),
        "source_count": int(source_count),
    }


def _count_sources(brief: str) -> int:
    """Count citations in markdown (links, footnotes, explicit "Source:" mentions)."""
    # Count markdown links [text](url)
    link_count = len(re.findall(r"\[.+?\]\(.+?\)", brief))
    # Count Source: prefix lines
    source_mentions = len(re.findall(r"(?:^|\n)\*?\*?Source:", brief, re.MULTILINE | re.IGNORECASE))
    # Count GitHub/URL mentions (rough heuristic)
    url_count = len(re.findall(r"https?://[^\s\)]+", brief))
    # Return unique count (rough dedupe: take max of link/url/source mentions)
    return max(link_count, source_mentions, url_count)


def _judge_research_quality(brief: str) -> dict:
    """
    Call Claude to judge research brief quality.

    Returns: {"success": bool, "score": float (0-10), "reasoning": str}
    """
    rubric = """You are evaluating a research brief for content creation. Score it 0-10 on these axes:

**Gap Analysis (0-10):** Does the brief identify what's missing, underdocumented, or misunderstood? NOT generic summaries.
- 10: Multiple novel insights a viewer cannot find in first Google results
- 7: At least one significant insight beyond surface-level coverage
- 4: Some original observations mixed with generic coverage
- 1: Mostly surface-level summary with little original analysis
- 0: No gap analysis present

**Primary Sources (0-10):** Are findings traceable to GitHub, docs, Twitter, Reddit (flagged), or blogs? Not marketing fluff?
- 10: All major claims cite primary sources; Reddit flagged where used
- 7: Most claims are sourced; minor unsourced claims
- 4: Mix of sourced and unsourced; some marketing language
- 1: Mostly unsourced or thin sourcing
- 0: No sources cited

**Actionability (0-10):** Can a creator use this to write a specific, different video outline?
- 10: Specific angles, audience hooks, and video concepts clearly implied
- 7: Actionable angle with some specificity
- 4: General guidance; needs clarification
- 1: Vague recommendations
- 0: Not actionable

Return ONLY JSON: {{"score": <avg of three axes>, "reasoning": "<1 sentence on strongest aspect>"}}

---

BRIEF TO EVALUATE:

{brief}"""

    rubric_filled = rubric.format(brief=brief[:4000])  # Truncate to avoid token bloat
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
