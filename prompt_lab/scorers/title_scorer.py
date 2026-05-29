"""Title Scorer — Evaluates titles via pairwise head-to-head LLM-judge.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {win_rate_pct: float (0-100)}
Pairwise comparison against baseline titles over fixture topics.
Each topic: judge votes for variant A or B. Win-rate = % of topics where variant wins.
"""

import re
from prompt_lab.scorers._judge import call_judge


def score_title_output(
    output: str,
    baseline_output: str = None,
    **kwargs
) -> dict[str, float]:
    """
    Score title batch via pairwise head-to-head against baseline.

    Args:
        output: The title markdown from the title skill (10+ candidate titles).
        baseline_output: Optional baseline titles to compare against.
                        If None, scoring uses internal heuristics (fallback).
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {win_rate_pct: float (0-100)} — percentage of tests where variant beat baseline.
        100% = variant wins all comparisons; 0% = baseline wins all.
    """
    if not output:
        return {"win_rate_pct": 0.0}

    # If no baseline provided, use fallback scoring (internal heuristics)
    if not baseline_output:
        return _score_titles_intrinsic(output)

    # Pairwise comparison mode
    win_rate = _judge_titles_pairwise(output, baseline_output)
    return {"win_rate_pct": float(win_rate)}


def _score_titles_intrinsic(titles: str) -> dict:
    """
    Fallback: score titles intrinsically (without baseline comparison).
    Uses LLM to assess title quality on CTR principles.

    Returns: {win_rate_pct: float} — rescaled to 0-100 for consistency.
    """
    rubric = """You are evaluating YouTube video titles for click-through rate potential.

Score 0-10 on these axes:

**Hook Strength (0-10):** Does the title make you WANT to click?
- 10: Impossible not to click — curiosity loop or strong benefit implied
- 7: Strong title; makes you curious
- 4: Decent title but competition might be better
- 1: Weak title; low click appeal
- 0: Repulsive or confusing title

**Clarity (0-10):** Is it immediately clear what the video is about?
- 10: Crystal clear; no ambiguity
- 7: Pretty clear; minor ambiguity
- 4: Somewhat clear; needs inference
- 1: Vague; could mean multiple things
- 0: Incomprehensible

**Specificity (0-10):** Does it use specific numbers, claims, or unique angles?
- 10: Specific claim/number + angle ("3 Ways to..." or "The X Mistake Everyone...")
- 7: Mostly specific with one generic word
- 4: Mix of specific and generic
- 1: Generic title (e.g., "How to Get Better at X")
- 0: Zero specificity

Return ONLY JSON: {"avg_score": <0-10 average>}
Then I'll rescale to 0-100 for win_rate_pct compatibility.

---

TITLES TO EVALUATE:

{titles}"""

    rubric_filled = rubric.format(titles=titles[:3000])
    result = call_judge(rubric_filled, timeout_sec=90)

    if not result["success"]:
        return {"win_rate_pct": 0.0}

    try:
        scores = result["scores"]
        avg_score = float(scores.get("avg_score", 0.0))
        # Rescale 0-10 to 0-100 for consistency
        win_rate = (avg_score / 10.0) * 100.0
        return {"win_rate_pct": max(0.0, min(100.0, win_rate))}
    except (KeyError, ValueError, TypeError):
        return {"win_rate_pct": 0.0}


def _judge_titles_pairwise(variant_titles: str, baseline_titles: str) -> float:
    """
    Pairwise head-to-head: judge votes for variant or baseline on each topic.

    Args:
        variant_titles: The new/variant title batch.
        baseline_titles: The baseline/control title batch.

    Returns:
        win_rate_pct (float 0-100) — percentage of topics where variant wins.
    """
    # Extract title lists (simple heuristic: lines starting with "- " or "1." etc.)
    variant_list = _extract_titles(variant_titles)
    baseline_list = _extract_titles(baseline_titles)

    if not variant_list or not baseline_list:
        # Can't do pairwise comparison; fallback to intrinsic scoring
        return 50.0  # Neutral if we can't extract titles

    # Limit to min of both (usually fixture has same # of test cases)
    num_comparisons = min(len(variant_list), len(baseline_list))

    rubric = """You are judging YouTube titles for click-through potential. For each pair, pick the one more likely to get clicked.

Criteria:
1. Hook Strength — curiosity, benefit, urgency
2. Clarity — immediately understandable
3. Specificity — numbers, claims, unique angles
4. Viewer Intent Match — does it match what viewers actually search/want?

Format your response as JSON:
{"winner_votes": [1, 2, 1, 2, ...]} where 1 = variant, 2 = baseline

For each position (Title 1, Title 2, etc.), vote 1 (prefer variant) or 2 (prefer baseline).

---

"""

    # Build comparison tuples
    pairs = []
    for i in range(num_comparisons):
        variant = variant_list[i]
        baseline = baseline_list[i]
        pairs.append((i + 1, variant, baseline))

    for idx, variant, baseline in pairs:
        rubric += f"\nComparison {idx}:\n- VARIANT:  {variant}\n- BASELINE: {baseline}\n"

    result = call_judge(rubric, timeout_sec=120)

    if not result["success"]:
        return 50.0  # Neutral on judge failure

    try:
        scores = result["scores"]
        votes = scores.get("winner_votes", [])
        if not votes or not isinstance(votes, list):
            return 50.0
        variant_wins = sum(1 for vote in votes if vote == 1)
        win_rate = (variant_wins / len(votes)) * 100.0 if votes else 50.0
        return max(0.0, min(100.0, win_rate))
    except (KeyError, ValueError, TypeError):
        return 50.0


def _extract_titles(text: str) -> list[str]:
    """Extract individual titles from a markdown/text block."""
    # Look for lines starting with "- ", "* ", or "N. " (common list formats)
    titles = re.findall(r"^[\s]*[-*]?\s*(?:\d+\.\s+)?(.+)$", text, re.MULTILINE)
    # Filter out empty lines and common noise
    cleaned = [t.strip() for t in titles if t.strip() and len(t.strip()) > 5]
    return cleaned[:10]  # Return first 10 titles (reasonable batch size)
