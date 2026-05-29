"""Hook Scorer — Evaluates hooks via Kallaway rubric (LLM-judge).

Rubric v0 — expect tuning after first real /prompt-lab runs (see plan §9).

Returns: {scroll_stop_score: float (0-10), curiosity_gap_score: float (0-10), payoff_promise_score: float (0-10)}
Three independent axes from Kallaway's highest-performing framework.
Composite = average of three (internally; caller decides weighting).
"""

from prompt_lab.scorers._judge import call_judge


def score_hook_output(output: str, **kwargs) -> dict[str, float]:
    """
    Score hook variations using the Kallaway rubric.

    The hook output should contain 5 hook variations, each with:
    - Spoken Line (first 3 seconds — stop the scroll)
    - Setup (next 10 seconds — deepen curiosity gap)
    - Promise (next 15 seconds — what they get)

    Args:
        output: The hook markdown from the hook skill (5 variations expected).
        **kwargs: Unused (for compatibility with scorer signature).

    Returns:
        {scroll_stop_score: float (0-10), curiosity_gap_score: float (0-10), payoff_promise_score: float (0-10)}
        Each axis scored independently across all 5 hooks.
    """
    if not output:
        return {
            "scroll_stop_score": 0.0,
            "curiosity_gap_score": 0.0,
            "payoff_promise_score": 0.0,
        }

    # Use LLM judge for Kallaway rubric assessment
    judge_result = _judge_hooks_kallaway(output)

    # Return three independent axes (caller averages if needed)
    if judge_result.get("success"):
        scores = judge_result.get("scores", {})
        return {
            "scroll_stop_score": float(scores.get("scroll_stop", 0.0)),
            "curiosity_gap_score": float(scores.get("curiosity_gap", 0.0)),
            "payoff_promise_score": float(scores.get("payoff_promise", 0.0)),
        }
    else:
        return {
            "scroll_stop_score": 0.0,
            "curiosity_gap_score": 0.0,
            "payoff_promise_score": 0.0,
        }


def _judge_hooks_kallaway(hooks: str) -> dict:
    """
    Call Claude to judge hooks using Kallaway rubric.

    Returns: {"success": bool, "scores": {"scroll_stop": X, "curiosity_gap": Y, "payoff_promise": Z}, "error": str}
    """
    rubric = """You are a YouTube retention expert. Evaluate these 5 hook variations using the Kallaway rubric.

Score EACH AXIS independently 0-10, then average across the 5 hooks for each axis.

**AXIS 1: Scroll Stop (0-10)**
"Would this stop a thumb mid-scroll?"
- 10: First word/image is visually or verbally STUNNING — impossible to keep scrolling
- 7: Strong opening — makes you pause for at least 1 second
- 4: Decent opening but needs work — some pause, then scroll
- 1: Boring opening — would skip in 0.5s
- 0: Negative signal — reader actively wants to scroll away

**AXIS 2: Curiosity Gap (0-10)**
"Does this create an itch that needs scratching?"
- 10: Impossible to know the answer without watching — pure open loop
- 7: Clear question posed; viewer wants to know the answer
- 4: Mild curiosity — some wonder but easily satisfied elsewhere
- 1: No gap; feels complete already
- 0: Anti-gap — viewer knows exactly what comes next

**AXIS 3: Payoff Promise (0-10)**
"Does it imply a clear payoff if I keep watching?"
- 10: Crystal-clear what the viewer will GET by watching (solution, answer, insight, entertainment)
- 7: Payoff implied but could be sharper
- 4: Vague promise — unclear what they're paying attention for
- 1: No payoff implied
- 0: Payoff seems negative (waste of time)

Return ONLY JSON with the average score per axis:
{"scroll_stop": <0-10>, "curiosity_gap": <0-10>, "payoff_promise": <0-10>}

---

HOOKS TO EVALUATE:

{hooks}"""

    rubric_filled = rubric.format(hooks=hooks[:4000])  # Truncate to avoid token bloat
    result = call_judge(rubric_filled, timeout_sec=90)

    if not result["success"]:
        return {
            "success": False,
            "scores": {"scroll_stop": 0.0, "curiosity_gap": 0.0, "payoff_promise": 0.0},
            "error": result.get("error", "Judge failed"),
        }

    # Parse result
    try:
        scores = result["scores"]
        return {
            "success": True,
            "scores": {
                "scroll_stop": float(scores.get("scroll_stop", 0.0)),
                "curiosity_gap": float(scores.get("curiosity_gap", 0.0)),
                "payoff_promise": float(scores.get("payoff_promise", 0.0)),
            },
            "error": "",
        }
    except (KeyError, ValueError, TypeError) as e:
        return {
            "success": False,
            "scores": {"scroll_stop": 0.0, "curiosity_gap": 0.0, "payoff_promise": 0.0},
            "error": f"Parse error: {str(e)[:50]}",
        }
