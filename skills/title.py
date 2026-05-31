"""YouTube Title Generation Skill — generates YouTube titles for video concepts.

Usage:
    python -m skills.title "video concept string"
    python -m skills.title --outline-file path/to/outline.md

Output:
    Prints the path to the written vault file.
"""

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv
from skills.utils.ai import generate
from skills.brief_loader import load_brief

load_dotenv(PROJECT_ROOT / ".env")

VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "07-Titles"
TITLES_DATA = PROJECT_ROOT / "skills" / "data" / "competitor_titles.json"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "title.md"


async def generate_titles(concept: str) -> str:
    """Generate YouTube titles for a concept using the AI cascade.

    Returns the generated titles text.
    Raises RuntimeError on failure.
    """
    with open(TITLES_DATA, "r", encoding="utf-8") as f:
        all_titles = json.load(f)

    top_30 = all_titles[:30]
    formatted_list = "\n".join(
        f"{i}. \"{entry['title']}\" — {entry['view_count']:,} views (@{entry['channel']})"
        for i, entry in enumerate(top_30, start=1)
    )

    prompt_template = PROMPT_PATH.read_text(encoding="utf-8")
    prompt_text = prompt_template.replace("{competitor_titles}", formatted_list).replace("{concept}", concept)

    # Import the generate function with custom cascade fallback
    from skills.utils.ai import generate
    result = await generate(prompt_text, cascade=["claude", "nim", "ollama"])
    if not result["success"] or not result["text"].strip():
        raise RuntimeError(f"Title generation failed: {result.get('error', 'Empty response')}")
    return result["text"].strip()


def write_vault(concept: str, output: str) -> Path:
    """Write generated titles to the vault."""
    slug = re.sub(r"[^a-z0-9]+", "-", concept.lower()).strip("-")[:50]
    date_str = datetime.now().strftime("%Y-%m-%d")
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    path = VAULT_DIR / f"{date_str}_{slug}.md"
    path.write_text(f"---\nconcept: {concept}\ndate: {date_str}\n---\n\n{output}\n", encoding="utf-8")
    return path


def _load_outline_context(outline_file: str) -> tuple[str, str]:
    path = Path(outline_file)
    content = path.read_text(encoding="utf-8", errors="replace")
    label = path.stem.replace("_", " ").replace("-", " ").strip() or "outline"
    return label, content


async def _main() -> None:
    parser = argparse.ArgumentParser(description="Generate YouTube titles for a video concept or outline file")
    parser.add_argument("concept", nargs="?", default="", help="Video concept string")
    parser.add_argument("--outline-file", default="", help="Existing outline markdown file to use as title context")
    args = parser.parse_args()

    if not args.concept and not args.outline_file:
        parser.error("provide a concept or --outline-file")

    concept_label = args.concept
    concept_context = args.concept
    if args.outline_file:
        outline_label, outline_content = _load_outline_context(args.outline_file)
        concept_label = args.concept or outline_label
        concept_context = (
            f"Video concept: {args.concept}\n\nOutline:\n{outline_content}"
            if args.concept
            else f"Outline:\n{outline_content}"
        )

    try:
        output = await generate_titles(concept_context)
        path = write_vault(concept_label, output)
        print(str(path))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    main()
