"""Brief loader — reads per-run constraints from brief.md frontmatter.

Part of Opportunity 3 (Self-Improvement Loop). Skills call load_brief() at startup
to learn run-specific tone, audience, banned phrases, etc.

Usage:
    from skills.brief_loader import load_brief, apply_cli_overrides
    import argparse

    brief = load_brief()  # reads Content-Hub-Vault-V2/00-Management-V2/brief.md
    parser = argparse.ArgumentParser()
    parser.add_argument("--tone", default=None)  # optional override
    args = parser.parse_args()
    brief = apply_cli_overrides(brief, args)

    # Use brief['tone'], brief['audience'], etc. in prompts
"""

import argparse
import logging
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

logger = logging.getLogger(__name__)

# Discover project root and vault location
PROJECT_ROOT = Path(__file__).parent.parent
BRIEF_PATH = PROJECT_ROOT / "Content-Hub-Vault-V2" / "00-Management-V2" / "brief.md"

# Default brief when file is missing
DEFAULT_BRIEF = {
    "tone": None,
    "audience": None,
    "banned_phrases": [],
    "target_length_minutes": None,
    "must_include": [],
    "must_avoid": [],
    "optimize_for": None,
}


def load_brief(path: Path | None = None) -> dict:
    """Load brief.md frontmatter + body. Returns empty dict (graceful) if file missing.

    Args:
        path: Optional override path to brief.md. Defaults to vault location.

    Returns:
        Dictionary with keys: tone, audience, banned_phrases, target_length_minutes,
        must_include, must_avoid, optimize_for. All present even if file missing (defaults).
    """
    if path is None:
        path = BRIEF_PATH

    if not path.exists():
        logger.debug("brief.md not found at %s — using defaults", path)
        return DEFAULT_BRIEF.copy()

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning("Failed to read brief.md (%s) — using defaults", e)
        return DEFAULT_BRIEF.copy()

    # Parse YAML frontmatter (---\n...\n---)
    if not content.startswith("---"):
        logger.warning("brief.md has no frontmatter — using defaults")
        return DEFAULT_BRIEF.copy()

    parts = content.split("---", 2)
    if len(parts) < 3:
        logger.warning("brief.md frontmatter malformed — using defaults")
        return DEFAULT_BRIEF.copy()

    frontmatter_text = parts[1].strip()

    # Parse YAML
    if yaml is None:
        logger.warning("PyYAML not available — using defaults")
        return DEFAULT_BRIEF.copy()

    try:
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except Exception as e:
        logger.warning("Failed to parse brief.md YAML (%s) — using defaults", e)
        return DEFAULT_BRIEF.copy()

    # Merge with defaults (frontmatter wins, missing keys get defaults)
    result = DEFAULT_BRIEF.copy()
    result.update(frontmatter)

    logger.debug("Loaded brief from %s", path)
    return result


def apply_cli_overrides(brief: dict, cli_args: argparse.Namespace) -> dict:
    """Overlay CLI flags on top of brief. CLI values win if present.

    Args:
        brief: Dictionary from load_brief()
        cli_args: argparse.Namespace from parser.parse_args()

    Returns:
        Updated brief dict with CLI overrides applied.
    """
    result = brief.copy()

    # List of brief keys that can be overridden via CLI
    overrideable_keys = [
        "tone",
        "audience",
        "target_length_minutes",
        "optimize_for",
    ]

    for key in overrideable_keys:
        if hasattr(cli_args, key):
            cli_value = getattr(cli_args, key, None)
            if cli_value is not None:
                result[key] = cli_value
                logger.debug("CLI override: %s = %s", key, cli_value)

    # Special handling for banned_phrases (repeatable flag)
    if hasattr(cli_args, "banned_phrase") and cli_args.banned_phrase:
        # CLI banned_phrases extend (not replace) brief's list
        result["banned_phrases"] = result.get("banned_phrases", []) + cli_args.banned_phrase
        logger.debug("Added CLI banned phrases: %s", cli_args.banned_phrase)

    return result
