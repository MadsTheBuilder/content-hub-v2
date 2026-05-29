"""Short-Form Scorer — Evaluates short-form variants via programmatic stage detection.

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {stage_presence_count: int (0-3)}
Count of Dopamine Ladder stages present: hook, promise/solution, payoff/proof.
Programmatic (regex/keyword detection) — no LLM judge for this metric.
Rationale: it's a count of presence, not a quality judgment; cheaper and more reliable.
"""

import re


def score_short_form_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score short-form scripts by detecting key stages.

    Args:
        output: The short-form markdown from the short_form skill.
                Expected: 3 length variants (30s, 60s, 90s) with Dopamine Ladder stages.
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {stage_presence_count: int (0-3)}
        0 = no stages detected; 3 = all three stages present.
    """
    if not output:
        return {"stage_presence_count": 0}

    count = _detect_stages(output)
    return {"stage_presence_count": int(count)}


def _detect_stages(script: str) -> int:
    """
    Detect presence of three Dopamine Ladder stages in short-form script.

    Returns: int count (0-3) of stages present.
    """
    stages = {
        "hook": False,
        "promise": False,
        "payoff": False,
    }

    # Normalize to lowercase for keyword matching
    script_lower = script.lower()

    # Stage 1: Hook — look for hook-specific keywords
    hook_patterns = [
        r"hook\b|scroll\s+stop|first\s+\d+\s*sec",
        r"open|curiosity|attention|grab",
    ]
    if any(re.search(pattern, script_lower) for pattern in hook_patterns):
        stages["hook"] = True

    # Stage 2: Promise/Solution — look for promise-specific keywords
    promise_patterns = [
        r"promise|solution|here\'?s\s+(?:how|why|what)",
        r"reveal|show|explain|teach",
    ]
    if any(re.search(pattern, script_lower) for pattern in promise_patterns):
        stages["promise"] = True

    # Stage 3: Payoff/Proof — look for payoff-specific keywords
    payoff_patterns = [
        r"payoff|proof|result|outcome|example",
        r"delivered|proven|shown|demonstrated",
    ]
    if any(re.search(pattern, script_lower) for pattern in payoff_patterns):
        stages["payoff"] = True

    # Count stages present
    return sum(1 for present in stages.values() if present)
