"""
Vault — reads knowledge files from the vault/ directory.

Simple file reader that loads markdown files and makes them available
for injection into LLM prompts.
"""

from pathlib import Path

VAULT_DIR = Path(__file__).parent.parent.parent / "Content-Hub-Vault" / "Exoskeleton"
SKILLS_DIR = Path(__file__).parent.parent.parent / "backend" / "prompts" / "skills"


def read_vault(filename: str) -> str:
    """Read a vault knowledge file. Returns empty string if not found."""
    path = VAULT_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def read_skill(filename: str) -> str:
    """Read a marketing skill file from backend/prompts/skills/. Returns empty string if not found."""
    path = SKILLS_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def get_niche_context() -> str:
    """Load the niche context file."""
    return read_vault("niche_context.md")


def get_kallaway() -> str:
    """Load the Kallaway masterclass notes."""
    return read_vault("kallaway_masterclass.md")


def get_all_vault_context() -> str:
    """Load all vault files concatenated for full context injection."""
    parts = []
    for md_file in sorted(VAULT_DIR.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        if content.strip() and "_TODO:" not in content[:200]:  # skip empty placeholders
            parts.append(f"--- {md_file.stem} ---\n{content}")
    return "\n\n".join(parts)
