"""Cascade — V2 Multi-Platform Content Generation from YouTube."""

import asyncio, argparse, logging, sys, re, tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import generate

logger = logging.getLogger(__name__)
VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "08-Distribution"


def extract_transcript(youtube_url: str) -> tuple[str, str]:
    """Extract transcript and title from YouTube via yt_dlp Python API."""
    import yt_dlp

    with tempfile.TemporaryDirectory() as tmpdir:
        tmppath = Path(tmpdir)
        opts = {
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "vtt",
            "skip_download": True,
            "outtmpl": str(tmppath / "%(title)s"),
            "quiet": True,
            "no_warnings": True,
        }
        title = "Untitled"
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(youtube_url, download=True)
                title = info.get("title", "Untitled") if info else "Untitled"
        except Exception as e:
            logger.error("yt_dlp failed: %s", e)
            return "", title

        vtt_files = list(tmppath.glob("*.vtt"))
        if not vtt_files:
            return "", title

        raw = vtt_files[0].read_text(encoding="utf-8", errors="ignore")
        lines = []
        for line in raw.split("\n"):
            line = line.strip()
            if line and not line.startswith("WEBVTT") and "-->" not in line and not re.match(r"^\d+$", line):
                line = re.sub(r"<[^>]+>", "", line).strip()
                if line:
                    lines.append(line)

        deduped = []
        prev = ""
        for line in lines:
            if line != prev:
                deduped.append(line)
                prev = line
        return " ".join(deduped), title


def load_prompts() -> tuple[str, str, str]:
    """Load and split prompts/cascade.md into three templates."""
    content = (PROJECT_ROOT / "prompts" / "cascade.md").read_text()
    blog_start = content.find("## BLOG POST PROMPT")
    twitter_start = content.find("## TWITTER THREAD PROMPT")
    linkedin_start = content.find("## LINKEDIN PROMPT")
    if blog_start == -1 or twitter_start == -1 or linkedin_start == -1:
        logger.error("Could not find section headers in prompts/cascade.md")
        sys.exit(1)
    blog = content[blog_start + len("## BLOG POST PROMPT"):twitter_start].strip()
    twitter = content[twitter_start + len("## TWITTER THREAD PROMPT"):linkedin_start].strip()
    linkedin = content[linkedin_start + len("## LINKEDIN PROMPT"):].strip()
    return blog, twitter, linkedin


def make_output_dir(title: str) -> Path:
    """Create output directory with slug-based name."""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
    out = VAULT_DIR / f"{date.today().isoformat()}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    return out


async def main():
    parser = argparse.ArgumentParser(description="Generate distribution content from YouTube")
    parser.add_argument("youtube_url", help="YouTube video URL")
    parser.add_argument("--title", default="", help="Override video title")
    args = parser.parse_args()

    print(f"📹 Extracting transcript from {args.youtube_url}...")
    transcript, extracted_title = extract_transcript(args.youtube_url)
    if not transcript:
        print("❌ Failed to extract transcript")
        sys.exit(1)

    title = args.title or extracted_title
    print(f"✅ Extracted {len(transcript)} characters from '{title}'")

    blog_tpl, twitter_tpl, linkedin_tpl = load_prompts()
    transcript_trunc = transcript[:4000]
    today = date.today().isoformat()

    print("\n" + "=" * 60)
    blog_result = await generate(blog_tpl.format(title=title, transcript=transcript_trunc, youtube_url=args.youtube_url))
    print("Generating Twitter thread...")
    twitter_result = await generate(twitter_tpl.format(title=title, transcript=transcript_trunc))
    print("Generating LinkedIn post...")
    linkedin_result = await generate(linkedin_tpl.format(title=title, transcript=transcript_trunc, youtube_url=args.youtube_url))
    print("=" * 60)

    blog_content = blog_result["text"] if blog_result["success"] else ""
    twitter_content = twitter_result["text"] if twitter_result["success"] else ""
    linkedin_content = linkedin_result["text"] if linkedin_result["success"] else ""

    if not all([blog_content, twitter_content, linkedin_content]):
        print("❌ One or more generations failed")
        sys.exit(1)

    output_dir = make_output_dir(title)

    (output_dir / "blog_post.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: {args.youtube_url}
tags: [ai-tools, build-in-public]
---

{blog_content}
""", encoding="utf-8")

    (output_dir / "twitter_thread.md").write_text(f"# Twitter Thread\n\n{twitter_content}\n", encoding="utf-8")
    (output_dir / "linkedin_post.md").write_text(f"# LinkedIn Post\n\n{linkedin_content}\n", encoding="utf-8")
    (output_dir / "README.md").write_text(f"""# Distribution — {title}

**Date:** {today}
**Video:** {args.youtube_url}

## Files
- `blog_post.md` — ready to publish
- `twitter_thread.md` — 7-10 tweet thread
- `linkedin_post.md` — single post

## Checklist
- [ ] Review blog_post.md → publish
- [ ] Review twitter_thread.md → replace [VIDEO_LINK] → post
- [ ] Review linkedin_post.md → replace [VIDEO_LINK] → post
""", encoding="utf-8")

    twitter_hook = twitter_content[:280]
    print(f"""
✅ Distribution package written to:
   {output_dir}

📝 blog_post.md
🐦 twitter_thread.md
💼 linkedin_post.md
📋 README.md

Preview — Twitter hook:
{twitter_hook}
""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())