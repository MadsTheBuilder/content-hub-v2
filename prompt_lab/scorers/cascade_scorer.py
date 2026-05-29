"""Cascade Scorer — Evaluates multi-channel distribution via LLM-judge.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {composite_judge_score: float (0-10)}
Composite assessment across all 3 channels: blog article, Twitter/X thread, LinkedIn post.
"""

from prompt_lab.scorers._judge import call_judge


def score_cascade_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score cascade output (3-channel distribution).

    Args:
        output: The cascade markdown from the cascade skill.
                Expected: blog article + Twitter thread + LinkedIn post.
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {composite_judge_score: float (0-10)}
    """
    if not output:
        return {"composite_judge_score": 0.0}

    # Use LLM judge for cascade quality assessment
    judge_result = _judge_cascade_quality(output)

    # Return composite score
    composite_score = judge_result.get("score", 0.0) if judge_result.get("success") else 0.0
    return {"composite_judge_score": float(composite_score)}


def _judge_cascade_quality(cascade: str) -> dict:
    """
    Call Claude to judge cascade (multi-channel distribution) quality.

    Returns: {"success": bool, "score": float (0-10), "reasoning": str}
    """
    rubric = """You are evaluating content repurposed across three channels: blog, Twitter/X, and LinkedIn.

Score 0-10 on these axes, then average:

**Blog Article Quality (0-10):** Is it substantive, well-structured, and link-worthy?
- 10: Deep insight, well-researched, actionable; 1000+ words; embeddable
- 7: Solid content; good structure; some depth
- 4: Basic content; adequate structure; lacks depth
- 1: Shallow or poorly organized
- 0: Unreadable or off-topic

**Twitter/X Thread Quality (0-10):** Is it punchy, engaging, threadable?
- 10: Grabs attention; each tweet stands alone; clear value
- 7: Good energy; mostly engaging; logical flow
- 4: Decent tweets; some padding or weak linking
- 1: Boring or confusing thread
- 0: Not suited for Twitter

**LinkedIn Post Quality (0-10):** Is it professional, thought-leading, shareable?
- 10: Authentic voice; leadership perspective; insightful hook; professional tone
- 7: Good professional tone; some insight; shareworthy
- 4: Adequate professional tone; generic insight
- 1: Weak or overly salesy
- 0: Tone mismatch or off-brand

**Channel Adaptation (0-10):** Does each version feel native to its platform, not just copy-pasted?
- 10: Each channel uniquely adapted (length, tone, format, CTA appropriate)
- 7: Mostly adapted; minor cross-platform feel
- 4: Some adaptation; still feels repurposed
- 1: Barely adapted; obviously copy-pasted across channels
- 0: Identical content on all channels

Return ONLY JSON: {"score": <avg of four axes>, "reasoning": "<1 sentence on strongest channel>"}

---

CASCADE TO EVALUATE:

{cascade}"""

    rubric_filled = rubric.format(cascade=cascade[:4000])  # Truncate to avoid token bloat
    result = call_judge(rubric_filled, timeout_sec=120)

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
