"""
Daily Runner — One-command workflow for your daily video production.

This is your main entry point. Run it every morning.

Usage:
  python daily.py                    # Full workflow: scrape → ideas → pick → script
  python daily.py --step ideas       # Just regenerate ideas (skip scrape)
  python daily.py --step script "My Video Title"   # Jump to scripting
  python daily.py --step cascade transcript.txt    # Post-production distribution
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║           🎬 DAILY CONTENT EXOSKELETON 🎬            ║
║                                                      ║
║   Your AI-powered daily video production system      ║
║   Niche: AI Tools • Build in Public • Tech Reviews   ║
╚══════════════════════════════════════════════════════╝
    """)


async def step_research():
    """Step 1: Scrape trends and generate ideas."""
    from skills.researcher import scrape_trends, save_trends_to_vault, generate_ideas, save_ideas, load_cached_trends
    
    print("\n🔍 STEP 1: Research & Ideation")
    print("─" * 40)
    
    # Scrape
    print("Scraping trending AI content...")
    trends = await scrape_trends(["youtube"])
    
    if trends:
        save_trends_to_vault(trends)
        print(f"✅ Found {len(trends)} trending posts")
    else:
        print("⚠️  Scrape returned empty (using cache if available)")
    
    trends_text = load_cached_trends()
    if not trends_text:
        print("❌ No trends data available. Check your APIFY_API_TOKEN.")
        return
    
    # Generate ideas
    print("\n💡 Generating 5 video ideas...")
    ideas = await generate_ideas(trends_text)
    output = save_ideas(ideas)
    
    print(f"\n📄 Ideas saved to: {output}")
    print(f"\n{ideas}")
    
    print("\n" + "─" * 40)
    print("👉 NEXT: Pick an idea, then run:")
    print('   python daily.py --step script "Your Chosen Video Title"')


async def step_ideas_only():
    """Regenerate ideas from cached trends (no scraping)."""
    from skills.researcher import generate_ideas, save_ideas, load_cached_trends
    
    print("\n💡 STEP 1b: Regenerate Ideas (from cached trends)")
    print("─" * 40)
    
    trends_text = load_cached_trends()
    if not trends_text:
        print("❌ No cached trends. Run the full workflow first: python daily.py")
        return
    
    ideas = await generate_ideas(trends_text)
    output = save_ideas(ideas)
    
    print(f"\n📄 Ideas saved to: {output}")
    print(f"\n{ideas}")


async def step_script(title: str, format_type: str = "medium", do_polish: bool = False):
    """Step 2: Generate hook + outline for a chosen idea."""
    from skills.hook_writer import generate_hook, generate_outline, polish_hook, save_script
    
    print(f"\n🎬 STEP 2: Script Generation")
    print("─" * 40)
    print(f"Title: \"{title}\"")
    print(f"Format: {format_type} | Platform: YouTube")
    
    # Hook
    print("\n🎣 Writing hook variations...")
    hook = await generate_hook(title, format_type, "youtube")
    
    if do_polish:
        print("✨ Polishing hook with Claude...")
        hook = await polish_hook(hook)
    
    # Outline
    print("📋 Writing full outline...")
    outline = await generate_outline(title, hook, format_type, "youtube")
    
    # Save
    output = save_script(title, hook, outline)
    
    print(f"\n📄 Script saved to: {output}")
    print(f"\n🎣 HOOK PREVIEW:\n")
    print(hook[:1200])
    
    print("\n" + "─" * 40)
    print("👉 NEXT: Review the script, film your video, export transcript, then run:")
    print("   python daily.py --step cascade path/to/transcript.txt")


async def step_cascade(transcript_path: str, title: str = ""):
    """Step 3: Generate distribution content from transcript."""
    from skills.cascade import generate_twitter_thread, generate_linkedin_post, save_distribution
    
    print(f"\n📦 STEP 3: Distribution Cascade")
    print("─" * 40)
    
    path = Path(transcript_path)
    if not path.exists():
        print(f"❌ File not found: {path}")
        return
    
    transcript = path.read_text(encoding="utf-8")
    print(f"📄 Loaded transcript: {len(transcript)} characters")
    
    print("\n🐦 Generating Twitter/X thread...")
    twitter = await generate_twitter_thread(transcript)
    
    print("💼 Generating LinkedIn post...")
    linkedin = await generate_linkedin_post(transcript)
    
    output_dir = save_distribution(twitter, linkedin, title)
    
    print(f"\n📦 Distribution content saved to: {output_dir}")
    
    print(f"\n🐦 TWITTER PREVIEW:\n")
    print(twitter[:600])
    
    print(f"\n💼 LINKEDIN PREVIEW:\n")
    print(linkedin[:400])
    
    print("\n" + "─" * 40)
    print("👉 NEXT: Review, replace [VIDEO_LINK], and post!")
    print("✅ Today's content pipeline is COMPLETE.")


async def main():
    parser = argparse.ArgumentParser(
        description="Daily content exoskeleton — your AI video production system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python daily.py                              # Full: scrape + ideas
  python daily.py --step ideas                 # Regen ideas from cache
  python daily.py --step script "Video Title"  # Generate hook + outline
  python daily.py --step script "Title" --polish  # With Claude polish
  python daily.py --step cascade transcript.txt   # Post-production
        """
    )
    parser.add_argument("--step", choices=["research", "ideas", "script", "cascade"],
                        default="research",
                        help="Which step to run (default: research)")
    parser.add_argument("input", nargs="?", default="",
                        help="Title (for script step) or transcript path (for cascade step)")
    parser.add_argument("--format", choices=["short", "medium", "long"], default="medium",
                        help="Video format for script step")
    parser.add_argument("--polish", action="store_true",
                        help="Add Claude polish pass (script step)")
    parser.add_argument("--title", default="",
                        help="Video title (for cascade step)")
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.step == "research":
        await step_research()
    elif args.step == "ideas":
        await step_ideas_only()
    elif args.step == "script":
        if not args.input:
            print("❌ Please provide a video title:")
            print('   python daily.py --step script "Your Video Title Here"')
            return
        await step_script(args.input, args.format, args.polish)
    elif args.step == "cascade":
        if not args.input:
            print("❌ Please provide a transcript file:")
            print("   python daily.py --step cascade path/to/transcript.txt")
            return
        await step_cascade(args.input, args.title)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    asyncio.run(main())
