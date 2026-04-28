"""
Skill Loader — cached loading of marketing skill markdown files.

Supports full-file loading and section extraction (by ## heading).
Files are read once per process and cached in memory.
"""

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

_cache: dict[str, str] = {}

SKILL_DIR = Path(__file__).parent / "skills"

# content_type -> type-specific skill for scripting prompts.
# Note: copywriting.md is ALWAYS loaded separately in _build_prompt() for all types.
# This map provides the additional platform/format-specific layer.
SCRIPTING_SKILL_MAP: dict[str, str] = {
    "short_form": "social-content.md",   # video-first social content guidance
    "talking_head": "social-content.md", # video-first social content guidance
    "slides": "social-content.md",       # carousel/slide social content guidance
    "topic": "social-content.md",        # educational carousel guidance
}

# named keys for special-purpose skills
NAMED_SKILLS: dict[str, str] = {
    "psychology": "marketing-psychology.md",
    "copy_editing": "copy-editing-quick.md",
    "social_content": "social-content.md",
    "copywriting": "copywriting.md",
    "content_strategy": "content-strategy.md",
    "ab_testing": "ab-testing.md",
}


def _read_file(filename: str) -> str:
    """Read a skill file and cache it. Returns empty string on failure."""
    if filename in _cache:
        return _cache[filename]

    path = SKILL_DIR / filename
    try:
        if path.exists():
            text = path.read_text(encoding="utf-8")
            _cache[filename] = text
            return text
        else:
            logger.warning("Skill file not found: %s", path)
    except Exception as e:
        logger.warning("Could not load skill file %s: %s", filename, e)

    _cache[filename] = ""
    return ""


def _extract_section(text: str, heading: str) -> str:
    """Extract content under a specific ## heading (case-insensitive).

    Returns everything from the ## heading line to the next ## heading
    or end of file, excluding the heading line itself.
    """
    pattern = rf"^## {re.escape(heading)}\s*$"
    lines = text.split("\n")
    start = None
    for i, line in enumerate(lines):
        if re.match(pattern, line, re.IGNORECASE):
            start = i + 1
            continue
        if start is not None and line.startswith("## "):
            return "\n".join(lines[start:i]).strip()

    if start is not None:
        return "\n".join(lines[start:]).strip()

    return ""


def load_skill(key: str, section: str | None = None) -> str:
    """Load a skill by named key, optionally extracting a single ## section.

    Args:
        key: A key from NAMED_SKILLS (e.g. "psychology", "copy_editing")
        section: Optional ## heading name to extract (e.g. "Understanding Buyers & Human Psychology")

    Returns:
        The skill text (full or section), or empty string on failure.
    """
    filename = NAMED_SKILLS.get(key, key)
    text = _read_file(filename)

    if section and text:
        extracted = _extract_section(text, section)
        if extracted:
            return extracted
        logger.warning("Section '%s' not found in skill '%s', returning full file", section, key)

    return text


def load_skill_sections(key: str, sections: list[str]) -> str:
    """Load multiple ## sections from a skill file, concatenated.

    Args:
        key: A key from NAMED_SKILLS
        sections: List of ## heading names to extract

    Returns:
        Concatenated section contents separated by newlines.
    """
    filename = NAMED_SKILLS.get(key, key)
    text = _read_file(filename)
    if not text:
        return ""

    parts = []
    for heading in sections:
        extracted = _extract_section(text, heading)
        if extracted:
            parts.append(f"## {heading}\n\n{extracted}")

    return "\n\n".join(parts)


def get_scripting_skill(content_type: str) -> str:
    """Return the appropriate full skill file for a content type."""
    filename = SCRIPTING_SKILL_MAP.get(content_type, "social-content.md")
    return _read_file(filename)
