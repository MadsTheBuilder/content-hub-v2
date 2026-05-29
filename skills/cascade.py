"""Cascade — V2 Multi-Platform Content Generation from YouTube."""

import asyncio, argparse, logging, sys, re
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import generate
from skills.utils.transcript import extract_transcript
from skills.brief_loader import load_brief
from skills.brief_args import add_brief_args

logger = logging.getLogger(__name__)
VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "08-Distribution"


def load_prompts() -> tuple[str, str, str]:
    """Load and split prompts/cascade.md into three templates."""
    content = (PROJECT_ROOT / "prompts" / "cascade.md").read_text()
    blog_start = content.find("## BLOG POST PROMPT")
    instagram_start = content.find("## INSTAGRAM PROMPT")
    linkedin_start = content.find("## LINKEDIN PROMPT")
    if blog_start == -1 or instagram_start == -1 or linkedin_start == -1:
        logger.error("Could not find section headers in prompts/cascade.md")
        sys.exit(1)
    blog = content[blog_start + len("## BLOG POST PROMPT"):instagram_start].strip()
    instagram = content[instagram_start + len("## INSTAGRAM PROMPT"):linkedin_start].strip()
    linkedin = content[linkedin_start + len("## LINKEDIN PROMPT"):].strip()
    return blog, instagram, linkedin


def make_output_dir(title: str) -> Path:
    """Create output directory with slug-based name."""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
    out = VAULT_DIR / f"{date.today().isoformat()}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    return out


async def main():
    parser = argparse.ArgumentParser(description="Generate distribution content from research+outline or YouTube")
    parser.add_argument("youtube_url", nargs="?", help="YouTube video URL (optional if --research-file provided)")
    parser.add_argument("--title", default="", help="Override content title")
    parser.add_argument("--research-file", help="Path to research markdown file (relative to project root or absolute)")
    parser.add_argument("--outline-file", help="Path to outline markdown file (relative to project root or absolute)")
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()

    raw_url = args.youtube_url  # None when omitted — used for routing only

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

    blog_tpl, instagram_tpl, linkedin_tpl = load_prompts()
    transcript_trunc = transcript[:6000]
    today = date.today().isoformat()

    print("\n" + "=" * 60)
    blog_result = await generate(blog_tpl.format(title=title, transcript=transcript_trunc, youtube_url=youtube_url))
    print("Generating Instagram carousel...")
    instagram_result = await generate(instagram_tpl.format(title=title, transcript=transcript_trunc, youtube_url=youtube_url))
    print("Generating LinkedIn post...")
    linkedin_result = await generate(linkedin_tpl.format(title=title, transcript=transcript_trunc, youtube_url=youtube_url))
    print("=" * 60)

    blog_content = blog_result["text"] if blog_result["success"] else ""
    instagram_content = instagram_result["text"] if instagram_result["success"] else ""
    linkedin_content = linkedin_result["text"] if linkedin_result["success"] else ""

    if not all([blog_content, instagram_content, linkedin_content]):
        print("❌ One or more generations failed")
        sys.exit(1)

    output_dir = make_output_dir(title)

    (output_dir / "blog_post.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: "{youtube_url}"
tags: [ai-tools, build-in-public]
---

{blog_content}
""", encoding="utf-8")

    (output_dir / "instagram_post.md").write_text(f"# Instagram Carousel\n\n{instagram_content}\n", encoding="utf-8")
    (output_dir / "linkedin_post.md").write_text(f"# LinkedIn Post\n\n{linkedin_content}\n", encoding="utf-8")
    (output_dir / "README.md").write_text(f"""# Distribution — {title}

**Date:** {today}
**Video:** {youtube_url}

## Files
- `blog_post.md` — ready to publish
- `instagram_post.md` — carousel slides (5-7 slides)
- `linkedin_post.md` — single post

## Checklist
- [ ] Review blog_post.md → publish
- [ ] Review instagram_post.md → replace [VIDEO_LINK] → post as carousel
- [ ] Review linkedin_post.md → replace [VIDEO_LINK] → post
""", encoding="utf-8")

    instagram_hook = instagram_content[:280]
    print(f"""
✅ Distribution package written to:
   {output_dir}

📝 blog_post.md
📸 instagram_post.md
💼 linkedin_post.md
📋 README.md

Preview — Instagram hook:
{instagram_hook}
""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())