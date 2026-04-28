"""
Researcher — Daily trend discovery and video idea generation.

What it does:
  1. Scrapes trending AI content from YouTube, TikTok, and optionally other platforms via Apify
  2. Analyzes what's performing well and why
  3. Generates 5 video ideas tailored to YOUR niche (AI tools, build-in-public, use cases)
  4. Saves everything to output/YYYY-MM-DD/ideas.md

Usage:
  python -m skills.researcher
  python -m skills.researcher --platform youtube
  python -m skills.researcher --skip-scrape  # use cached trends, just regenerate ideas
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime, date
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from skills.utils.ai import generate
from skills.utils.vault import get_niche_context, read_skill

logger = logging.getLogger(__name__)

OUTPUT_DIR = PROJECT_ROOT / "output"
TRENDS_FILE = PROJECT_ROOT / "Content-Hub-Vault" / "Exoskeleton" / "trends.md"


# ---------------------------------------------------------------------------
# Trend scraping (reuses Apify client from backend)
# ---------------------------------------------------------------------------

async def scrape_trends(platforms: list[str] | None = None) -> list[dict]:
    """Scrape trending content using the existing Apify client.
    
    Returns a list of normalized, scored posts.
    """
    from backend.research.apify_client import scrape_general_trending
    
    platforms = platforms or ["youtube"]
    all_results = []
    
    for platform in platforms:
        try:
            logger.info("Scraping trending content from %s...", platform)
            results = await scrape_general_trending(platform)
            all_results.extend(results)
            logger.info("Got %d trending posts from %s", len(results), platform)
        except Exception as e:
            logger.warning("Failed to scrape %s: %s", platform, e)
    
    # Sort by organic score
    all_results.sort(key=lambda x: x.get("organic_score", 0), reverse=True)
    return all_results


def save_trends_to_vault(trends: list[dict]) -> Path:
    """Save scraped trends to Content-Hub-Vault/Exoskeleton/trends.md for reference."""
    lines = [
        f"# Trending Content — {date.today().isoformat()}\n",
        f"Scraped at {datetime.now().strftime('%H:%M')}\n",
    ]
    
    for i, t in enumerate(trends[:30], 1):
        platform = t.get("platform", "?").upper()
        title = t.get("title", "No title")[:120]
        views = t.get("view_count", 0)
        score = t.get("organic_score", 0)
        author = t.get("author_username", "unknown")
        url = t.get("post_url", "")
        
        lines.append(f"\n## {i}. [{platform}] {title}")
        lines.append(f"- **Author**: @{author}")
        lines.append(f"- **Views**: {views:,} | **Score**: {score:.0f}")
        if url:
            lines.append(f"- **URL**: {url}")
    
    TRENDS_FILE.write_text("\n".join(lines), encoding="utf-8")
    logger.info("Saved %d trends to %s", len(trends), TRENDS_FILE)
    return TRENDS_FILE


def load_cached_trends() -> str:
    """Load previously scraped trends from Content-Hub-Vault/Exoskeleton/trends.md."""
    if TRENDS_FILE.exists():
        return TRENDS_FILE.read_text(encoding="utf-8")
    return ""


# ---------------------------------------------------------------------------
# Idea generation
# ---------------------------------------------------------------------------

IDEA_PROMPT_TEMPLATE = """\
You are a content strategist for a YouTube creator in the AI tools and build-in-public niche.

## Creator's Niche & Brand
{niche_context}

## Today's Trending Content
{trends}

## Content Strategy Knowledge
{strategy_skill}

## Your Task
Based on the trending content above and the creator's niche, generate **5 video ideas** for today.

For EACH idea, provide:
1. **Title** — A compelling YouTube title (use proven patterns: numbers, curiosity gaps, "I tried X so you don't have to")
2. **Hook** — The first 2 sentences that grab attention (under 15 seconds spoken)
3. **Angle** — What makes THIS take unique vs what already exists
4. **Format** — Estimated length (short: 30-60s, medium: 5-8min, long: 10-15min) and style (tutorial, review, commentary, vlog)
5. **Why Now** — Why this topic is timely based on the trending data
6. **Difficulty** — Easy (talking head + screen share), Medium (needs demos), Hard (needs multiple tools/setups)

## Rules
- At least 2 ideas should be "Easy" difficulty (filmable today with minimal prep)
- At least 1 idea should be a "build in public" angle about the creator's own projects
- Ideas should NOT be generic "Top 10 AI Tools" — they need a specific angle or opinion
- Prioritize ideas where the creator's builder experience gives them credibility
- Each title should work as a YouTube thumbnail concept too

Return the 5 ideas in clean markdown format.
"""


async def generate_ideas(trends_text: str) -> str:
    """Generate 5 video ideas from trending data + niche context."""
    niche = get_niche_context()
    strategy = read_skill("content-strategy.md")
    
    # Trim strategy to key sections to save tokens
    if len(strategy) > 3000:
        strategy = strategy[:3000] + "\n...(truncated)"
    
    prompt = IDEA_PROMPT_TEMPLATE.format(
        niche_context=niche,
        trends=trends_text[:4000],  # Cap to avoid token explosion
        strategy_skill=strategy[:2000],
    )
    
    result = await generate(prompt)
    
    if result["success"]:
        return result["text"]
    else:
        logger.error("Idea generation failed: %s", result.get("error"))
        return "❌ Idea generation failed. Check your API keys and try again."


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def save_ideas(ideas_text: str, provider: str = "") -> Path:
    """Save generated ideas to output/YYYY-MM-DD/ideas.md."""
    today_dir = OUTPUT_DIR / date.today().isoformat()
    today_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = today_dir / "ideas.md"
    header = (
        f"# Video Ideas — {date.today().isoformat()}\n\n"
        f"Generated at {datetime.now().strftime('%H:%M')} "
        f"{'via ' + provider if provider else ''}\n\n"
        f"---\n\n"
    )
    output_path.write_text(header + ideas_text, encoding="utf-8")
    logger.info("Ideas saved to %s", output_path)
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

async def main():
    parser = argparse.ArgumentParser(description="Daily trend research + idea generation")
    parser.add_argument("--platform", nargs="+", default=["youtube"],
                        help="Platforms to scrape (default: youtube tiktok)")
    parser.add_argument("--skip-scrape", action="store_true",
                        help="Skip scraping, use cached trends from Content-Hub-Vault/Exoskeleton/trends.md")
    parser.add_argument("--ideas-only", action="store_true",
                        help="Alias for --skip-scrape")
    args = parser.parse_args()
    
    # Step 1: Get trends
    if args.skip_scrape or args.ideas_only:
        print("📋 Loading cached trends from Content-Hub-Vault/Exoskeleton/trends.md...")
        trends_text = load_cached_trends()
        if not trends_text:
            print("❌ No cached trends found. Run without --skip-scrape first.")
            return
    else:
        print(f"🔍 Scraping trending content from: {', '.join(args.platform)}...")
        trends = await scrape_trends(args.platform)
        if trends:
            save_trends_to_vault(trends)
            trends_text = load_cached_trends()
            print(f"✅ Found {len(trends)} trending posts")
        else:
            print("⚠️  No trends scraped (check Apify key). Using cached if available...")
            trends_text = load_cached_trends()
            if not trends_text:
                print("❌ No trends available at all. Check your APIFY_API_TOKEN in .env")
                return
    
    # Step 2: Generate ideas
    print("\n💡 Generating 5 video ideas from trends + your niche...")
    ideas = await generate_ideas(trends_text)
    
    # Step 3: Save
    output_path = save_ideas(ideas)
    
    print(f"\n{'='*60}")
    print(f"📄 Ideas saved to: {output_path}")
    print(f"{'='*60}")
    print(f"\n{ideas}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
