"""
Distribution Cascade — Post-production content repurposing.

What it does:
  1. Takes your finished video transcript (from CapCut export)
  2. Generates a Twitter/X thread
  3. Generates a LinkedIn post
  4. Saves all distribution content to output/YYYY-MM-DD/distribution/

Usage:
  python -m skills.cascade path/to/transcript.txt
  python -m skills.cascade path/to/transcript.txt --title "My Video Title"
  python -m skills.cascade path/to/transcript.txt --platforms twitter linkedin
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime, date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skills.utils.ai import generate
from skills.utils.vault import get_niche_context, read_skill

logger = logging.getLogger(__name__)

OUTPUT_DIR = PROJECT_ROOT / "output"


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

TWITTER_THREAD_PROMPT = """\
You are a Twitter/X ghostwriter for an AI tools and build-in-public creator.

## Creator's Brand
{niche_context}

## Copywriting Principles
{copywriting}

## The Video Transcript
{transcript}

## Your Task: Write a Twitter/X Thread

Convert this video into a **7-10 tweet thread** that stands on its own (people who haven't seen the video should still get value).

### Thread Structure:
1. **Tweet 1 (Hook)** — The most surprising or valuable insight from the video. Must stop the scroll. End with "🧵👇" or "A thread:" 
2. **Tweets 2-8 (Value)** — Key points, each tweet is one idea. Use:
   - Short sentences and line breaks
   - Specific numbers and examples (from the transcript)
   - No fluff or filler words
3. **Tweet 9-10 (CTA)** — Wrap up + link to the video

### Rules:
- Each tweet MUST be under 280 characters
- Use line breaks between sentences within tweets
- No hashtags (they look desperate on X)
- Use emojis sparingly (max 1 per tweet)
- Sound like a real person, not a corporate account
- Include the video title and a placeholder [VIDEO_LINK] in the last tweet

Format as:
**Tweet 1:**
[content]

**Tweet 2:**
[content]
...
"""

LINKEDIN_PROMPT = """\
You are a LinkedIn content strategist for a tech professional in the AI space.

## Creator's Brand
{niche_context}

## Marketing Psychology
{psychology}

## The Video Transcript
{transcript}

## Your Task: Write a LinkedIn Post

Convert this video into a **single LinkedIn post** optimized for engagement.

### Structure:
1. **Hook line** (first 2 lines visible before "see more") — must create curiosity
2. **Story/Context** — brief personal angle (2-3 sentences)
3. **Key insights** — 3-5 bullet points with the main takeaways
4. **Opinion/Take** — your contrarian or unique perspective
5. **CTA** — ask a question to drive comments (LinkedIn algorithm loves comments)

### Rules:
- Total length: 150-200 words (LinkedIn sweet spot)
- Use line breaks between every 1-2 sentences (readability on mobile)
- Start with a bold statement, NOT "I just published a video..."
- Include 3-5 relevant hashtags at the END (LinkedIn is different from X — hashtags help here)
- Sound professional but human — no corporate buzzword salad
- Include [VIDEO_LINK] placeholder

Format as a single post, ready to copy-paste.
"""


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

async def generate_twitter_thread(transcript: str) -> str:
    """Generate a Twitter/X thread from a video transcript."""
    niche = get_niche_context()
    copywriting = read_skill("copywriting.md")
    
    prompt = TWITTER_THREAD_PROMPT.format(
        niche_context=niche,
        copywriting=copywriting[:2000] if copywriting else "",
        transcript=transcript[:5000],
    )
    
    result = await generate(prompt)
    if result["success"]:
        return result["text"]
    return f"❌ Twitter thread generation failed: {result.get('error')}"


async def generate_linkedin_post(transcript: str) -> str:
    """Generate a LinkedIn post from a video transcript."""
    niche = get_niche_context()
    psychology = read_skill("marketing-psychology.md")
    
    prompt = LINKEDIN_PROMPT.format(
        niche_context=niche,
        psychology=psychology[:2000] if psychology else "",
        transcript=transcript[:5000],
    )
    
    result = await generate(prompt)
    if result["success"]:
        return result["text"]
    return f"❌ LinkedIn post generation failed: {result.get('error')}"


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_distribution(
    twitter_thread: str,
    linkedin_post: str,
    video_title: str = "",
) -> Path:
    """Save all distribution content to output/YYYY-MM-DD/distribution/."""
    today_dir = OUTPUT_DIR / date.today().isoformat() / "distribution"
    today_dir.mkdir(parents=True, exist_ok=True)
    
    # Twitter thread
    twitter_path = today_dir / "twitter_thread.md"
    twitter_path.write_text(
        f"# Twitter Thread — {video_title or date.today().isoformat()}\n\n"
        f"Generated at {datetime.now().strftime('%H:%M')}\n\n---\n\n"
        f"{twitter_thread}\n",
        encoding="utf-8",
    )
    
    # LinkedIn post
    linkedin_path = today_dir / "linkedin_post.md"
    linkedin_path.write_text(
        f"# LinkedIn Post — {video_title or date.today().isoformat()}\n\n"
        f"Generated at {datetime.now().strftime('%H:%M')}\n\n---\n\n"
        f"{linkedin_post}\n",
        encoding="utf-8",
    )
    
    # Summary
    summary_path = today_dir / "README.md"
    summary_path.write_text(
        f"# Distribution Package — {date.today().isoformat()}\n\n"
        f"**Video**: {video_title or '(untitled)'}\n\n"
        f"## Contents\n"
        f"- `twitter_thread.md` — 7-10 tweet thread\n"
        f"- `linkedin_post.md` — LinkedIn post\n\n"
        f"## Checklist\n"
        f"- [ ] Review Twitter thread\n"
        f"- [ ] Post thread on X\n"
        f"- [ ] Review LinkedIn post\n"
        f"- [ ] Post on LinkedIn\n"
        f"- [ ] Replace [VIDEO_LINK] with actual URL\n",
        encoding="utf-8",
    )
    
    logger.info("Distribution content saved to %s", today_dir)
    return today_dir


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def main():
    parser = argparse.ArgumentParser(description="Generate distribution content from a video transcript")
    parser.add_argument("transcript", help="Path to the video transcript file (.txt or .md)")
    parser.add_argument("--title", default="", help="Video title (for headers)")
    parser.add_argument("--platforms", nargs="+", default=["twitter", "linkedin"],
                        help="Platforms to generate for (default: twitter linkedin)")
    args = parser.parse_args()
    
    # Read transcript
    transcript_path = Path(args.transcript)
    if not transcript_path.exists():
        print(f"❌ Transcript file not found: {transcript_path}")
        return
    
    transcript = transcript_path.read_text(encoding="utf-8")
    if not transcript.strip():
        print("❌ Transcript file is empty")
        return
    
    print(f"📄 Loaded transcript: {len(transcript)} characters")
    print(f"🎯 Generating for: {', '.join(args.platforms)}")
    
    twitter_thread = ""
    linkedin_post = ""
    
    if "twitter" in args.platforms:
        print("\n🐦 Generating Twitter/X thread...")
        twitter_thread = await generate_twitter_thread(transcript)
    
    if "linkedin" in args.platforms:
        print("💼 Generating LinkedIn post...")
        linkedin_post = await generate_linkedin_post(transcript)
    
    # Save
    output_dir = save_distribution(twitter_thread, linkedin_post, args.title)
    
    print(f"\n{'='*60}")
    print(f"📦 Distribution content saved to: {output_dir}")
    print(f"{'='*60}")
    
    if twitter_thread:
        print(f"\n🐦 TWITTER THREAD PREVIEW:\n")
        print(twitter_thread[:800])
        if len(twitter_thread) > 800:
            print(f"\n... (see full thread at {output_dir / 'twitter_thread.md'})")
    
    if linkedin_post:
        print(f"\n💼 LINKEDIN POST PREVIEW:\n")
        print(linkedin_post[:600])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
