"""Voice Cleanup — V2 De-AI'ify skill. Rewrites AI-generated content in the creator's authentic voice."""

import asyncio, argparse, logging, sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import polish
from skills.brief_loader import load_brief, apply_cli_overrides
from skills.brief_args import add_brief_args

logger = logging.getLogger(__name__)


def load_prompt_template() -> str:
    return (PROJECT_ROOT / "prompts" / "voice_cleanup.md").read_text(encoding="utf-8")


async def main():
    parser = argparse.ArgumentParser(description="De-AI'ify content — rewrite in the creator's authentic voice")
    parser.add_argument("file", nargs="?", help="Path to a markdown file to clean (omit to read from stdin)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite the original file instead of writing _cleaned.md")
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()
    brief = apply_cli_overrides(brief, args)

    if args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)
        text = input_path.read_text(encoding="utf-8")
        print(f"📄 Cleaning: {input_path.name} ({len(text)} chars)...")
    else:
        if sys.stdin.isatty():
            print("Paste the text to clean (then Ctrl+Z on Windows / Ctrl+D on Unix to submit):")
        text = sys.stdin.read()
        input_path = None
        print(f"📄 Cleaning stdin input ({len(text)} chars)...")

    if not text.strip():
        print("❌ No text to clean")
        sys.exit(1)

    template = load_prompt_template()
    prompt = template.format(text=text)

    print("✍️  Running voice cleanup (Claude)...")
    result = await polish(prompt)

    if not result["success"] or not result["text"].strip():
        print(f"❌ Cleanup failed: {result.get('error', 'Empty response')}")
        sys.exit(1)

    cleaned = result["text"].strip()

    if input_path:
        if args.inplace:
            output_path = input_path
        else:
            output_path = input_path.parent / f"{input_path.stem}_cleaned{input_path.suffix}"
        output_path.write_text(cleaned, encoding="utf-8")
        print(f"""
✅ Voice cleanup complete via {result['provider']}

Output: {output_path}

--- Preview (first 300 chars) ---
{cleaned[:300]}
""")
    else:
        print(f"\n✅ Voice cleanup complete via {result['provider']}\n")
        print("--- Cleaned Output ---")
        print(cleaned)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    asyncio.run(main())
