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
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run_auto_commit() -> dict:
    """
    Execute the auto-commit pipeline: vault sync + quality checks + commit.

    Stages changes in Content-Hub-Vault-V2, runs quality checks, and commits
    if all checks pass.

    Returns:
        Dictionary with keys:
            - success (bool): True if commit was successful
            - files_staged (int): Number of files staged
            - commit_hash (str or None): Commit SHA if successful, None otherwise
    """
    from backend.git_manager import GitManager
    from backend.quality_check import QualityValidator

    result = {
        "success": False,
        "files_staged": 0,
        "commit_hash": None,
    }

    try:
        # Initialize git manager
        git_manager = GitManager(str(PROJECT_ROOT))

        # Stage vault changes
        patterns = ["Content-Hub-Vault-V2/**/*"]
        staged_files = git_manager.stage_files(patterns)
        result["files_staged"] = len(staged_files)

        if not staged_files:
            logging.info("No files to stage in Content-Hub-Vault-V2")
            result["success"] = True
            return result

        # Run quality checks
        quality_validator = QualityValidator(str(PROJECT_ROOT))
        check_results = quality_validator.run_checks(verbose=False)

        if not check_results["all_passed"]:
            logging.error(
                f"Quality checks failed: "
                f"tests_passed={check_results['tests_passed']}, "
                f"lint_errors={check_results['lint_errors']}, "
                f"type_errors={check_results['type_errors']}"
            )
            result["success"] = False
            return result

        # All checks passed, commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Daily auto-commit: vault + quality [{timestamp}]"

        try:
            commit_hash = git_manager.commit(message, author="Scheduler")
            result["success"] = True
            result["commit_hash"] = commit_hash
            logging.info(f"Auto-commit successful: {commit_hash}")
        except ValueError as e:
            # No staged changes (shouldn't happen, but handle gracefully)
            if "No staged changes" in str(e):
                result["success"] = True
                result["commit_hash"] = None
            else:
                logging.error(f"Commit failed: {str(e)}")
                result["success"] = False

    except Exception as e:
        logging.error(f"Auto-commit pipeline failed: {str(e)}")
        result["success"] = False

    return result


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
  python daily.py --auto-commit                # Trigger auto-commit pipeline
  python daily.py --check-only                 # Run quality checks (dry-run)
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
    parser.add_argument("--auto-commit", action="store_true",
                        help="Manually trigger full auto-commit pipeline (vault sync + quality checks + commit)")
    parser.add_argument("--check-only", action="store_true",
                        help="Run quality checks without committing (dry-run mode)")

    args = parser.parse_args()

    print_banner()

    # Handle auto-commit flags first
    if args.auto_commit:
        print("\n🔄 MANUAL AUTO-COMMIT TRIGGER")
        print("─" * 40)
        result = run_auto_commit()
        if result["success"]:
            print(f"✅ Auto-commit successful")
            if result["commit_hash"]:
                print(f"   Commit: {result['commit_hash']}")
                print(f"   Files staged: {result['files_staged']}")
            else:
                print(f"   (No changes to commit)")
        else:
            print(f"❌ Auto-commit failed")
            print(f"   Files staged: {result['files_staged']}")
        return

    if args.check_only:
        print("\n🔍 QUALITY CHECK (DRY-RUN)")
        print("─" * 40)
        from backend.quality_check import QualityValidator
        quality_validator = QualityValidator(str(PROJECT_ROOT))
        check_results = quality_validator.run_checks(verbose=True)

        print(f"\n📊 Quality Check Results:")
        print(f"   Tests passed: {check_results['tests_passed']}")
        print(f"   Test count: {check_results['test_count']}")
        print(f"   Lint errors: {check_results['lint_errors']}")
        print(f"   Type errors: {check_results['type_errors']}")
        print(f"   All passed: {check_results['all_passed']}")
        return

    # Normal workflow steps
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
