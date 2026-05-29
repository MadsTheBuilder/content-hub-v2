"""Autoresearch loop — modify → score → keep-or-revert → repeat.

Ported from Karpathy's autoresearch pattern. Optimizes a single prompt file
over N iterations using fixture-based test inputs and skill-specific scorers.

Usage:
    python -m prompt_lab.loop --skill hook --iterations 20 --dry-run
    python -m prompt_lab.loop --skill hook --iterations 20

The loop is the structural orchestrator. Real mutation strategies and skill
invocation are stubbed (TODO) — will be filled in by follow-up sessions.
"""

import argparse
import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path

from skills.pipeline import log_result
from skills.brief_loader import load_brief

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"
FIXTURES_DIR = PROJECT_ROOT / "prompt_lab" / "fixtures"
SCORERS_DIR = PROJECT_ROOT / "prompt_lab" / "scorers"
VAULT = PROJECT_ROOT / "Content-Hub-Vault-V2"
PIPELINE_RESULTS_TSV = VAULT / "00-Management-V2" / "pipeline_results.tsv"

SKILL_CHOICES = [
    "researcher",
    "ideation",
    "hook",
    "outline",
    "title",
    "cascade",
    "short_form",
    "voice_cleanup",
]


def _sha256_short(text: str) -> str:
    """Compute SHA256 hash, return first 16 chars."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _load_prompt(skill: str) -> str:
    """Load prompts/<skill>.md as plaintext."""
    prompt_path = PROMPTS_DIR / f"{skill}.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def _write_prompt(skill: str, content: str) -> None:
    """Write updated prompt to prompts/<skill>.md."""
    prompt_path = PROMPTS_DIR / f"{skill}.md"
    prompt_path.write_text(content, encoding="utf-8")


def _load_prompt_sha(skill: str) -> str:
    """Load current prompt file and hash it."""
    prompt_text = _load_prompt(skill)
    return _sha256_short(prompt_text)


def _load_brief_sha() -> str:
    """Load brief.md, hash its YAML frontmatter."""
    brief = load_brief()
    # Serialize frontmatter to a deterministic string for hashing
    frontmatter_str = json.dumps(brief, sort_keys=True, default=str)
    return _sha256_short(frontmatter_str)


def _load_fixtures(skill: str) -> dict:
    """Load fixture JSON from prompt_lab/fixtures/<skill>_test_topics.json."""
    fixtures_path = FIXTURES_DIR / f"{skill}_test_topics.json"
    if not fixtures_path.exists():
        raise FileNotFoundError(f"Fixtures file not found: {fixtures_path}")
    with open(fixtures_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _mutate_prompt(prompt_text: str) -> str:
    """Mutate the prompt text for the next iteration.

    TODO: Implement real mutation strategy. Currently returns input unchanged.
    Potential strategies:
    - Ask Claude to refactor one section for clarity
    - Swap example order
    - Add/remove constraints
    - Rewrite rubric axes
    - Adjust tone/formality
    """
    # TODO: real mutation strategy
    return prompt_text


def _run_skill_over_fixtures(skill: str, fixtures: dict) -> str:
    """Run the skill over all fixtures and return aggregated output.

    TODO: Implement real skill invocation. Currently returns empty string.
    In real runs, this should:
    - Import or subprocess the skill
    - Run it on each fixture topic
    - Collect outputs
    - Return as single string (or parsed JSON, depending on skill)
    """
    # TODO: real skill invocation over fixtures
    return ""


def _score_output(skill: str, output: str, dry_run: bool = False) -> dict[str, float]:
    """Call the appropriate scorer for this skill.

    Args:
        skill: Skill name (must match a scorer module).
        output: The raw output from running the skill.
        dry_run: If True, return placeholder scores.

    Returns:
        Dictionary of {metric_name: metric_value, ...}
    """
    if dry_run:
        # Placeholder for dry-run: single metric_value=0.0
        return {"metric_value": 0.0}

    # Import the scorer dynamically
    try:
        if skill == "hook":
            from prompt_lab.scorers.hook_scorer import score_hook_output
            result = score_hook_output(output)
        elif skill == "voice_cleanup":
            from prompt_lab.scorers.voice_cleanup_scorer import score_voice_cleanup_output
            result = score_voice_cleanup_output(output)
        # TODO: add importers for remaining scorers (researcher, ideation, outline, title, cascade, short_form)
        else:
            logger.warning("Scorer not yet implemented for skill: %s", skill)
            return {"metric_value": 0.0}

        return result

    except ImportError as e:
        logger.error("Failed to import scorer for skill %s: %s", skill, e)
        return {"metric_value": 0.0}


def _compute_composite(metrics: dict[str, float]) -> float:
    """Compute a single composite score from multiple metrics.

    Strategy: average all metric values.
    TODO: Weight metrics differently if needed (e.g., scroll_stop 1.5x).
    """
    if not metrics:
        return 0.0
    values = [v for v in metrics.values() if isinstance(v, (int, float))]
    return sum(values) / len(values) if values else 0.0


def _run_one_iteration(
    run_id: str,
    skill: str,
    iteration: int,
    prev_composite: float | None,
    dry_run: bool = False,
) -> tuple[float, bool, dict[str, float]]:
    """
    Run one autoresearch iteration: mutate → score → decide.

    Returns:
        (new_composite_score, kept_flag, metrics_dict)
    """
    logger.info("Iteration %d: Starting", iteration)

    # Load current state
    prompt_text = _load_prompt(skill)
    prompt_sha = _load_prompt_sha(skill)
    brief_sha = _load_brief_sha()
    fixtures = _load_fixtures(skill)

    # Save baseline for potential revert
    baseline_prompt = prompt_text

    # Mutate (no-op in dry-run)
    if not dry_run:
        prompt_text = _mutate_prompt(prompt_text)
        _write_prompt(skill, prompt_text)

    # Run skill over fixtures
    if not dry_run:
        output = _run_skill_over_fixtures(skill, fixtures)
    else:
        output = ""

    # Score
    metrics = _score_output(skill, output, dry_run=dry_run)
    new_composite = _compute_composite(metrics)

    # Keep-or-revert decision
    if prev_composite is None:
        # First iteration (baseline)
        kept = True
        logger.info("Iteration %d: Baseline. composite=%.2f. KEPT.", iteration, new_composite)
    elif new_composite > prev_composite:
        # Improved
        kept = True
        logger.info(
            "Iteration %d: Improved. prev=%.2f → new=%.2f. KEPT.",
            iteration,
            prev_composite,
            new_composite,
        )
    else:
        # No improvement, revert
        kept = False
        _write_prompt(skill, baseline_prompt)
        logger.info(
            "Iteration %d: No improvement. prev=%.2f → new=%.2f. REVERTED.",
            iteration,
            prev_composite,
            new_composite,
        )

    # Log all metrics to TSV
    kept_label = "DRYRUN" if dry_run else ("YES" if kept else "NO")
    for metric_name, metric_value in metrics.items():
        log_result(
            run_id=run_id,
            skill=skill,
            metric_name=metric_name,
            metric_value=metric_value,
            model="claude-sonnet-4-6",
            kept=kept_label,
            prompt_sha=prompt_sha,
            brief_sha=brief_sha,
        )

    return new_composite, kept, metrics


def run_loop(
    skill: str,
    iterations: int = 20,
    dry_run: bool = False,
    budget_hours: float = 8.0,
) -> None:
    """
    Main autoresearch loop.

    Args:
        skill: Skill to optimize (researcher, ideation, hook, etc.)
        iterations: Max iterations (default 20)
        dry_run: If True, no real model calls, no prompt writes
        budget_hours: Wall-clock time limit in hours (default 8)
    """
    start_time = time.time()
    budget_seconds = budget_hours * 3600

    # Generate run ID
    run_id = f"autoresearch-{skill}-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"

    logger.info(
        "Starting autoresearch loop: skill=%s, iterations=%d, dry_run=%s, budget=%.1f hours",
        skill,
        iterations,
        dry_run,
        budget_hours,
    )

    # Validate inputs
    if skill not in SKILL_CHOICES:
        raise ValueError(f"Unknown skill: {skill}. Choices: {SKILL_CHOICES}")

    fixtures = _load_fixtures(skill)
    logger.info("Loaded %d fixtures for skill=%s", len(fixtures.get("topics", [])), skill)

    prev_composite = None
    iteration = 0

    while iteration < iterations:
        elapsed = time.time() - start_time
        if elapsed > budget_seconds:
            logger.info("Budget exhausted (%.1f > %.1f). Stopping.", elapsed, budget_seconds)
            break

        iteration += 1

        try:
            new_composite, kept, metrics = _run_one_iteration(
                run_id=run_id,
                skill=skill,
                iteration=iteration,
                prev_composite=prev_composite,
                dry_run=dry_run,
            )
            prev_composite = new_composite if kept else prev_composite

        except Exception as e:
            logger.error("Iteration %d failed: %s", iteration, e, exc_info=True)
            # Log failure and continue
            continue

        time.sleep(0.5)  # Small pause between iterations

    logger.info(
        "Autoresearch loop completed: skill=%s, iterations=%d, elapsed=%.1f sec",
        skill,
        iteration,
        time.time() - start_time,
    )


def main():
    """Parse CLI args and run the loop."""
    parser = argparse.ArgumentParser(
        description="Autoresearch loop - optimize prompts via modify, score, keep-or-revert."
    )
    parser.add_argument(
        "--skill",
        required=True,
        choices=SKILL_CHOICES,
        help="Skill to optimize",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=20,
        help="Max iterations (default 20)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No real model calls, no prompt writes. Structural loop only.",
    )
    parser.add_argument(
        "--budget-hours",
        type=float,
        default=8.0,
        help="Wall-clock time limit in hours (default 8)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default INFO)",
    )

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    # Run the loop
    run_loop(
        skill=args.skill,
        iterations=args.iterations,
        dry_run=args.dry_run,
        budget_hours=args.budget_hours,
    )


if __name__ == "__main__":
    main()
