"""YouTube Title Generation Skill — generates YouTube titles for video concepts.

Usage:
    python -m skills.title "video concept string"

Output:
    Prints the path to the written vault file.
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Load .env to make env vars available
load_dotenv()


def find_project_root() -> Path:
    """Walk up from __file__ until we find a directory with 'skills/' and 'prompts/'."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "skills").exists() and (current / "prompts").exists():
            return current
        current = current.parent
    # Fallback: assume parent of skills/
    return Path(__file__).resolve().parent.parent


def generate_titles(concept: str) -> str:
    """Generate YouTube titles for a concept using Claude.

    Args:
        concept: The video concept string

    Returns:
        The generated titles output from Claude

    Raises:
        RuntimeError: If Claude CLI call fails
    """
    project_root = find_project_root()

    # Load competitor titles
    titles_path = project_root / "skills" / "data" / "competitor_titles.json"
    with open(titles_path, "r", encoding="utf-8") as f:
        all_titles = json.load(f)

    # Take top 30
    top_30 = all_titles[:30]

    # Format as numbered list
    formatted_list = "\n".join(
        f"{i}. \"{entry['title']}\" — {entry['view_count']:,} views (@{entry['channel']})"
        for i, entry in enumerate(top_30, start=1)
    )

    # Load prompt template
    prompt_path = project_root / "prompts" / "title.md"
    prompt_template = prompt_path.read_text(encoding="utf-8")

    # Replace placeholders
    prompt_text = prompt_template.replace("{competitor_titles}", formatted_list).replace("{concept}", concept)

    # Call Claude CLI via subprocess.
    # shell=True lets Windows find claude.cmd (npm wrapper) without needing
    # the npm bin dir explicitly on PATH.
    try:
        result = subprocess.run(
            "claude -p -",
            input=prompt_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=180,
            shell=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Claude CLI failed (exit {result.returncode}): {result.stderr.strip()}")
        output = result.stdout.strip()
        if not output:
            raise RuntimeError("Claude CLI returned empty output")
        return output
    except subprocess.TimeoutExpired:
        raise RuntimeError("Claude CLI call timed out after 180 seconds")


def write_vault(concept: str, output: str) -> Path:
    """Write generated titles to the vault.

    Args:
        concept: The original video concept
        output: The generated titles output

    Returns:
        Path to the written file
    """
    project_root = find_project_root()

    # Create slug from concept
    slug = re.sub(r"[^a-z0-9]+", "-", concept.lower()).strip("-")[:50]

    # Create date string
    date_str = datetime.now().strftime("%Y-%m-%d")

    # Create output directory
    out_dir = project_root / "Content-Hub-Vault-V2" / "07-Titles"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build output path
    path = out_dir / f"{date_str}_{slug}.md"

    # Write file with frontmatter
    content = f"""---
concept: {concept}
date: {date_str}
---

{output}
"""
    path.write_text(content, encoding="utf-8")
    return path


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python -m skills.title \"video concept\"")
        sys.exit(1)

    concept = sys.argv[1]

    try:
        output = generate_titles(concept)
        path = write_vault(concept, output)
        print(str(path))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
