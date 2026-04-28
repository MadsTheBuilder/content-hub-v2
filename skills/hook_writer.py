"""
Hook & Outline Writer — Turns a chosen video idea into a ready-to-film script.

What it does:
  1. Takes a video idea (title + angle) as input
  2. Loads Kallaway masterclass rules + marketing skills + niche context
  3. Generates a complete hook (first 30 seconds) + full outline
  4. Saves to output/YYYY-MM-DD/script.md

Usage:
  python -m skills.hook_writer "I Built an AI Content Engine — Here's What Actually Works"
  python -m skills.hook_writer "title" --format medium --platform youtube
  python -m skills.hook_writer "title" --polish  # adds a Claude polish pass
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

from skills.utils.ai import generate, polish
from skills.utils.vault import get_niche_context, get_kallaway, read_skill

logger = logging.getLogger(__name__)

OUTPUT_DIR = PROJECT_ROOT / "output"


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------

HOOK_PROMPT = """\
You are an expert YouTube scriptwriter specializing in AI/tech content.

## Creator's Brand & Voice
{niche_context}

## Branding & Storytelling Masterclass (Kallaway's Rules)
{kallaway}

## Copywriting Principles
{copywriting}

## Social Content Execution
{social_content}

## The Video Idea
**Title**: {title}
**Format**: {format} ({platform})
**Additional notes**: {notes}

## Your Task: Write the HOOK (first 30 seconds)

Create 3 hook variations for this video. For EACH hook:

1. **Opening line** (spoken in first 3 seconds — must stop the scroll)
2. **Setup** (next 10 seconds — establish the problem or curiosity gap)
3. **Promise** (next 15 seconds — what they'll learn/see if they keep watching)
4. **Visual cue** — what should be on screen during the hook

### Rules:
- The hook must work WITHOUT context — someone scrolling must stop
- Use patterns from the Kallaway masterclass if available
- No "Hey guys" or "In this video" — start with the payload
- Each hook should use a different psychological pattern:
  - Hook 1: Curiosity gap / surprising statement
  - Hook 2: Personal story / "I did X and here's what happened"
  - Hook 3: Contrarian take / "Everyone says X but actually Y"

Mark your recommended hook with ⭐.
"""

OUTLINE_PROMPT = """\
You are an expert YouTube scriptwriter. You've already written the hook (below).
Now create the FULL OUTLINE for the rest of the video.

## Creator's Brand
{niche_context}

## Content Strategy Knowledge
{strategy}

## The Hook (already written)
{hook}

## Video Details
**Title**: {title}
**Format**: {format} ({platform})
**Target length**: {length}

## Your Task: Full Video Outline

Create a detailed outline with:

### Structure
For each section provide:
- **Section name** and **target duration** (e.g., "Problem Setup — 1:30")
- **Talking points** — bullet points of what to say (NOT a word-for-word script — this is for a talking head, keep it natural)
- **Visual notes** — what should be on screen (screen share, B-roll, text overlay)
- **Transition** — how to bridge to the next section

### Required Sections
1. **Hook** (already written — include it)
2. **Context/Problem** — why this matters to the viewer
3. **Main Content** — the meat (tutorial, demo, analysis, story)
4. **Personal Take** — your opinion as a builder who uses these tools
5. **CTA** — what to do next (subscribe, try the tool, comment)

### Rules
- Keep it conversational — this is a talking head video, not a TED talk
- Include [SHOW SCREEN] markers where you should share your screen
- Include [B-ROLL] markers for visual variety
- Total sections should fit the target length
- End strong — the last 10 seconds should give them a reason to watch the next video
"""


# ---------------------------------------------------------------------------
# Generation pipeline
# ---------------------------------------------------------------------------

async def generate_hook(
    title: str,
    format_type: str = "medium",
    platform: str = "youtube",
    notes: str = "",
) -> str:
    """Generate 3 hook variations for a video idea."""
    niche = get_niche_context()
    kallaway = get_kallaway()
    copywriting = read_skill("copywriting.md")
    social_content = read_skill("social-content.md")
    
    # Trim large skills to save tokens
    if len(copywriting) > 3000:
        copywriting = copywriting[:3000] + "\n...(truncated)"
    if len(social_content) > 3000:
        social_content = social_content[:3000] + "\n...(truncated)"
    
    prompt = HOOK_PROMPT.format(
        niche_context=niche,
        kallaway=kallaway[:4000] if kallaway else "(Not yet filled — see vault/kallaway_masterclass.md)",
        copywriting=copywriting,
        social_content=social_content,
        title=title,
        format=format_type,
        platform=platform,
        notes=notes or "None",
    )
    
    result = await generate(prompt)
    if result["success"]:
        return result["text"]
    return f"❌ Hook generation failed: {result.get('error')}"


async def generate_outline(
    title: str,
    hook_text: str,
    format_type: str = "medium",
    platform: str = "youtube",
) -> str:
    """Generate a full video outline based on the hook."""
    niche = get_niche_context()
    strategy = read_skill("content-strategy.md")
    
    length_map = {
        "short": "30-60 seconds",
        "medium": "5-8 minutes",
        "long": "10-15 minutes",
    }
    
    prompt = OUTLINE_PROMPT.format(
        niche_context=niche,
        strategy=strategy[:3000] if strategy else "",
        hook=hook_text,
        title=title,
        format=format_type,
        platform=platform,
        length=length_map.get(format_type, "5-8 minutes"),
    )
    
    result = await generate(prompt)
    if result["success"]:
        return result["text"]
    return f"❌ Outline generation failed: {result.get('error')}"


async def polish_hook(hook_text: str) -> str:
    """Polish hook using Claude for elite copywriting quality."""
    prompt = (
        "You are an elite YouTube copywriter. Polish this hook to be more compelling, "
        "more specific, and more scroll-stopping. Keep the same structure and length, "
        "but make every word count harder. Remove any AI-isms or generic phrasing.\n\n"
        f"HOOK TO POLISH:\n{hook_text}\n\n"
        "Return ONLY the polished hook in the same format. No commentary."
    )
    result = await polish(prompt)
    if result["success"]:
        return result["text"]
    return hook_text  # Return original if polish fails


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_script(title: str, hook: str, outline: str, provider: str = "") -> Path:
    """Save the full script to output/YYYY-MM-DD/script.md."""
    today_dir = OUTPUT_DIR / date.today().isoformat()
    today_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = today_dir / "script.md"
    content = (
        f"# Script: {title}\n\n"
        f"Generated at {datetime.now().strftime('%H:%M')} on {date.today().isoformat()}\n\n"
        f"---\n\n"
        f"## 🎣 HOOK OPTIONS\n\n{hook}\n\n"
        f"---\n\n"
        f"## 📋 FULL OUTLINE\n\n{outline}\n\n"
        f"---\n\n"
        f"## 📝 FILMING NOTES\n\n"
        f"- [ ] Pick your hook (mark with ⭐ above)\n"
        f"- [ ] Review outline sections for accuracy\n"
        f"- [ ] Prep any screen shares / demos mentioned\n"
        f"- [ ] Film it!\n"
    )
    
    output_path.write_text(content, encoding="utf-8")
    logger.info("Script saved to %s", output_path)
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def main():
    parser = argparse.ArgumentParser(description="Generate hook + outline for a video idea")
    parser.add_argument("title", help="The video title/idea to script")
    parser.add_argument("--format", choices=["short", "medium", "long"], default="medium",
                        help="Video format (default: medium = 5-8 min)")
    parser.add_argument("--platform", default="youtube", help="Target platform (default: youtube)")
    parser.add_argument("--notes", default="", help="Extra notes to guide the script")
    parser.add_argument("--polish", action="store_true", help="Add a Claude polish pass on the hook")
    args = parser.parse_args()
    
    print(f"🎬 Generating script for: \"{args.title}\"")
    print(f"   Format: {args.format} | Platform: {args.platform}")
    
    # Step 1: Generate hook
    print("\n🎣 Writing hook variations...")
    hook = await generate_hook(args.title, args.format, args.platform, args.notes)
    
    # Step 1.5: Optional polish
    if args.polish:
        print("✨ Polishing hook with Claude...")
        hook = await polish_hook(hook)
    
    # Step 2: Generate outline
    print("📋 Writing full outline...")
    outline = await generate_outline(args.title, hook, args.format, args.platform)
    
    # Step 3: Save
    output_path = save_script(args.title, hook, outline)
    
    print(f"\n{'='*60}")
    print(f"📄 Script saved to: {output_path}")
    print(f"{'='*60}")
    
    # Print the hook (outline is long, just point to file)
    print(f"\n🎣 HOOK PREVIEW:\n")
    print(hook[:1500])
    if len(hook) > 1500:
        print(f"\n... (see full script at {output_path})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
