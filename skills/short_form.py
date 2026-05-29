"""Short Form — V2 Vertical Video Scripts from YouTube."""

import asyncio, argparse, logging, sys, re
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import generate
from skills.utils.transcript import extract_transcript
from skills.brief_loader import load_brief, apply_cli_overrides
from skills.brief_args import add_brief_args

logger = logging.getLogger(__name__)
VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "09-Shorts"


def load_prompts() -> tuple[str, str, str]:
    """Load and split prompts/short_form.md into three templates."""
    content = (PROJECT_ROOT / "prompts" / "short_form.md").read_text()
    thirty_start = content.find("## 30 SECOND SCRIPT")
    sixty_start = content.find("## 60 SECOND SCRIPT")
    ninety_start = content.find("## 90 SECOND SCRIPT")
    if thirty_start == -1 or sixty_start == -1 or ninety_start == -1:
        logger.error("Could not find section headers in prompts/short_form.md")
        sys.exit(1)
    thirty = content[thirty_start + len("## 30 SECOND SCRIPT"):sixty_start].strip()
    sixty = content[sixty_start + len("## 60 SECOND SCRIPT"):ninety_start].strip()
    ninety = content[ninety_start + len("## 90 SECOND SCRIPT"):].strip()
    return thirty, sixty, ninety

def make_output_dir(title: str) -> Path:
    """Create output directory with slug-based name."""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
    out = VAULT_DIR / f"{date.today().isoformat()}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    return out

async def main():
    parser = argparse.ArgumentParser(description="Generate short-form vertical video scripts from research+outline or YouTube")
    parser.add_argument("youtube_url", nargs="?", help="YouTube video URL (optional if --research-file provided)")
    parser.add_argument("--title", default="", help="Override content title")
    parser.add_argument("--research-file", help="Path to research markdown file (relative to project root or absolute)")
    parser.add_argument("--outline-file", help="Path to outline markdown file (relative to project root or absolute)")
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()
    brief = apply_cli_overrides(brief, args)

    raw_url = args.youtube_url

    if args.research_file or args.outline_file:
        parts = []
        title = args.title
        if args.research_file:
            rp = Path(args.research_file)
            if not rp.is_absolute():
                rp = PROJECT_ROOT / rp
            parts.append(f"## RESEARCH NOTES\n\n{rp.read_text(encoding='utf-8')}")
        if args.outline_file:
            op = Path(args.outline_file)
            if not op.is_absolute():
                op = PROJECT_ROOT / op
            outline_text = op.read_text(encoding="utf-8")
            parts.append(f"## VIDEO OUTLINE\n\n{outline_text}")
            if not title:
                m = re.search(r"^topic:\s*(.+)$", outline_text, re.MULTILINE)
                if m:
                    title = m.group(1).strip()
        title = title or "Content"
        transcript = "\n\n".join(parts)
        youtube_url = raw_url or "[VIDEO_LINK]"
        print(f"📄 Loaded research+outline ({len(transcript)} chars) for '{title}'")
    elif raw_url:
        print(f"📹 Extracting transcript from {raw_url}...")
        transcript, extracted_title = extract_transcript(raw_url)
        if not transcript:
            print("❌ Failed to extract transcript")
            sys.exit(1)
        title = args.title or extracted_title
        youtube_url = raw_url
        print(f"✅ Extracted {len(transcript)} characters from '{title}'")
    else:
        print("❌ Provide either a YouTube URL or --research-file / --outline-file")
        sys.exit(1)

    thirty_tpl, sixty_tpl, ninety_tpl = load_prompts()
    transcript_trunc = transcript[:6000]
    today = date.today().isoformat()

    print("Generating 30s script...")
    thirty_result = await generate(thirty_tpl.format(title=title, transcript=transcript_trunc))
    print("Generating 60s script...")
    sixty_result = await generate(sixty_tpl.format(title=title, transcript=transcript_trunc))
    print("Generating 90s script...")
    ninety_result = await generate(ninety_tpl.format(title=title, transcript=transcript_trunc))

    thirty_content = thirty_result["text"] if thirty_result["success"] else ""
    sixty_content = sixty_result["text"] if sixty_result["success"] else ""
    ninety_content = ninety_result["text"] if ninety_result["success"] else ""

    if not all([thirty_content, sixty_content, ninety_content]):
        print("❌ One or more generations failed")
        sys.exit(1)

    output_dir = make_output_dir(title)

    (output_dir / "30s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: "{youtube_url}"
duration: 30s
---

{thirty_content}
""", encoding="utf-8")

    (output_dir / "60s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: "{youtube_url}"
duration: 60s
---

{sixty_content}
""", encoding="utf-8")

    (output_dir / "90s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: "{youtube_url}"
duration: 90s
---

{ninety_content}
""", encoding="utf-8")

    (output_dir / "README.md").write_text(f"""# Short Form Scripts — {title}

**Date:** {today}
**Video:** {youtube_url}

## Scripts
- `30s_script.md` — 30-second vertical script
- `60s_script.md` — 60-second vertical script
- `90s_script.md` — 90-second vertical script

## Checklist
- [ ] Review 30s_script.md → record
- [ ] Review 60s_script.md → record
- [ ] Review 90s_script.md → record
""", encoding="utf-8")

    print(f"""✅ Short-form package written to:
   {output_dir}

🎬 30s_script.md
🎬 60s_script.md
🎬 90s_script.md
📋 README.md
""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
