"""Ideation — V2 Ranked Video Idea Generator from vault research notes."""

import asyncio, argparse, logging, sys, re
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import polish
from skills.brief_loader import load_brief, apply_cli_overrides
from skills.brief_args import add_brief_args

logger = logging.getLogger(__name__)

RESEARCH_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "10-Research"
TRENDS_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "04-Trends"
VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "02-Ideas"
PROMPT_FILE = PROJECT_ROOT / "prompts" / "ideation.md"


def find_research_file(topic: str) -> Path | None:
    """Find the most recent research file matching the topic. Falls back to most recent overall."""
    if not RESEARCH_DIR.exists():
        return None

    candidates = sorted(
        [f for f in RESEARCH_DIR.glob("**/*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )

    if not candidates:
        return None

    # Try topic match first (case-insensitive substring)
    slug = topic.lower().replace(" ", "_")
    for f in candidates:
        if slug in f.stem.lower() or topic.lower() in f.stem.lower().replace("_", " "):
            return f

    # Fallback: most recent file
    return candidates[0]


def load_trends() -> str:
    """Load today's or most recent trending note from the vault."""
    if not TRENDS_DIR.exists():
        return ""
    md_files = sorted(
        [f for f in TRENDS_DIR.glob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not md_files:
        return ""
    content = md_files[0].read_text(encoding="utf-8", errors="ignore")
    # Truncate to keep token usage manageable
    return content[:3000]


def make_output_path(topic: str) -> Path:
    slug = re.sub(r"[^\w\s-]", "", topic.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
    VAULT_DIR.mkdir(parents=True, exist_ok=True)
    return VAULT_DIR / f"{date.today().isoformat()}_{slug}.md"


async def main():
    parser = argparse.ArgumentParser(description="Generate ranked video ideas from vault research notes")
    parser.add_argument("--topic", required=True, help="Topic / niche to ideate on (e.g. 'AI agents')")
    parser.add_argument("--research-file", default="", help="Path to a specific research .md file (optional)")
    parser.add_argument("--no-trends", action="store_true", help="Skip loading trending context")
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()
    brief = apply_cli_overrides(brief, args)

    # Load research notes
    if args.research_file:
        research_path = Path(args.research_file)
        if not research_path.exists():
            print(f"❌ Research file not found: {args.research_file}")
            sys.exit(1)
    else:
        research_path = find_research_file(args.topic)
        if not research_path:
            print(f"❌ No research files found in {RESEARCH_DIR}")
            print("   Run /yt-pipeline first to generate research notes.")
            sys.exit(1)

    print(f"📚 Research file: {research_path.name}")
    research_notes = research_path.read_text(encoding="utf-8", errors="ignore")

    # Warn if research was run without primary sources
    psc_match = re.search(r'^primary_sources_found:\s*(\d+)', research_notes, re.MULTILINE)
    if psc_match and int(psc_match.group(1)) == 0:
        print("[warn] Research file has 0 primary sources — findings rest on secondary commentary only")

    # Truncate to avoid token overflow; research files can be long
    research_notes = research_notes[:6000]

    # Load trends (optional)
    trends_context = ""
    if not args.no_trends:
        trends_context = load_trends()
        if trends_context:
            print(f"📈 Loaded trending context ({len(trends_context)} chars)")
        else:
            print("📈 No trending context found (continuing without it)")

    # Build prompt
    template = PROMPT_FILE.read_text(encoding="utf-8")
    prompt = template.format(
        topic=args.topic,
        research_notes=research_notes,
        trends_context=trends_context or "(none provided)",
    )

    print(f"💡 Generating 9 ranked ideas for: {args.topic}")
    result = await polish(prompt)

    if not result["success"] or not result["text"].strip():
        print(f"❌ Generation failed: {result.get('error', 'Empty response')}")
        sys.exit(1)

    ideas_text = result["text"].strip()

    output_path = make_output_path(args.topic)
    today = date.today().isoformat()

    output_path.write_text(
        f"---\n"
        f"topic: {args.topic}\n"
        f"date: {today}\n"
        f"research_source: {research_path.name}\n"
        f"provider: {result['provider']}\n"
        f"---\n\n"
        f"# Video Ideas — {args.topic}\n\n"
        f"{ideas_text}\n",
        encoding="utf-8",
    )

    # Print preview: first idea only
    first_idea_end = ideas_text.find("\n---\n\n### Rank 2")
    preview = ideas_text[:first_idea_end].strip() if first_idea_end != -1 else ideas_text[:600]

    print(f"""
✅ 9 ranked ideas written via {result['provider']}

Output: {output_path}

--- Top Idea Preview ---
{preview}
""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    asyncio.run(main())
