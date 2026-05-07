import asyncio
import json
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from dotenv import load_dotenv
from backend.research.apify_client import scrape_profiles

# Load environment variables
load_dotenv()


async def main():
    """Scrape competitor titles from YouTube channels."""
    all_results = []

    # Scrape first channel
    print("Scraping nateherk...")
    results_1 = await scrape_profiles(
        workflow_id="competitor-research",
        platform="youtube",
        usernames=["nateherk"]
    )
    all_results.extend(results_1)
    print(f"  Got {len(results_1)} results from nateherk")

    # Scrape second channel
    print("Scraping Chase-H-AI...")
    results_2 = await scrape_profiles(
        workflow_id="competitor-research",
        platform="youtube",
        usernames=["Chase-H-AI"]
    )
    all_results.extend(results_2)
    print(f"  Got {len(results_2)} results from Chase-H-AI")

    # Extract and filter entries
    entries = []
    for p in all_results:
        title = p.get("title", "")
        # Filter entries with empty or None title
        if title:
            entries.append({
                "title": title,
                "view_count": p.get("view_count", 0),
                "channel": p.get("author_username", "")
            })

    # Sort by view_count descending
    entries.sort(key=lambda x: x["view_count"], reverse=True)

    # Take top 60
    entries = entries[:60]

    # Create directory
    os.makedirs("skills/data", exist_ok=True)

    # Write to JSON
    with open("skills/data/competitor_titles.json", "w") as f:
        json.dump(entries, f, indent=2)

    print(f"Wrote {len(entries)} entries to skills/data/competitor_titles.json")


if __name__ == "__main__":
    asyncio.run(main())
