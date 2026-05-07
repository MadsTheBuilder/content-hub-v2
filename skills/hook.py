"""Hook Skill — Generate 5 Kallaway-trained hook variations for a video topic."""

import asyncio
import argparse
import logging
import re
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import draft, polish

logger = logging.getLogger(__name__)

VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "05-Hooks"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "hook.md"
MARKETING_BRAIN_PATH = PROJECT_ROOT / "Content-Hub-Vault-V2" / "01-Knowledge" / "marketing_brain.md"


def load_prompt():
    if not PROMPT_PATH.exists():
        logger.error("prompts/hook.md not found at %s", PROMPT_PATH)
        sys.exit(1)
    return PROMPT_PATH.read_text(encoding="utf-8")


def load_marketing_brain():
    if not MARKETING_BRAIN_PATH.exists():
        logger.warning("marketing_brain.md not found — proceeding without supplemental context")
        return ""
    return MARKETING_BRAIN_PATH.read_text(encoding="utf-8")


def make_slug(topic):
    slug = re.sub(r"[^\w\s-]", "", topic.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")
    return "-".join(slug.split("-")[:6])


def build_prompt(template, topic, platform, audience, format_type, marketing_brain):
    filled = template.format(
        topic=topic,
        platform=platform,
        audience=audience,
        format=format_type,
    )
    if marketing_brain:
        filled += f"\n\n---\n\n## SUPPLEMENTAL KALLAWAY CONTEXT\n\n{marketing_brain[:3000]}"
    return filled


async def run(topic, platform, audience, format_type, no_polish):
    template = load_prompt()
    marketing_brain = load_marketing_brain()
    prompt = build_prompt(template, topic, platform, audience, format_type, marketing_brain)

    print("Drafting hooks (Ollama → Gemini)...")
    draft_result = await draft(prompt)
    if not draft_result["success"]:
        logger.error("Draft failed: %s", draft_result.get("error"))
        sys.exit(1)

    hook_text = draft_result["text"]

    if not no_polish:
        print("Polishing with Claude...")
        polish_prompt = (
            prompt
            + f"\n\nDRAFT TO POLISH:\n{hook_text}\n\n"
            "Polish these into 5 tight, Kallaway-caliber hook variations. "
            "Keep the exact same format (Hook N, Spoken Line, Setup, Promise, Visual Cue, Text Overlay, Pattern, Why). "
            "Make every word earn its place. Remove any AI-isms or generic phrasing."
        )
        polish_result = await polish(polish_prompt)
        if polish_result["success"]:
            hook_text = polish_result["text"]
        else:
            logger.warning("Polish failed, using draft: %s", polish_result.get("error"))

    return hook_text


def save_output(topic, platform, audience, format_type, hook_text):
    slug = make_slug(topic)
    today = date.today().isoformat()
    output_path = VAULT_DIR / f"{today}_{slug}.md"
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    content = (
        f"---\n"
        f"topic: {topic}\n"
        f"platform: {platform}\n"
        f"audience: {audience}\n"
        f"format: {format_type}\n"
        f"created: {today}\n"
        f"---\n"
        f"# Hook Variations: {topic}\n\n"
        f"{hook_text}\n"
    )
    output_path.write_text(content, encoding="utf-8")
    logger.info("Hooks written to %s", output_path)
    return output_path


async def main():
    parser = argparse.ArgumentParser(description="Generate 5 Kallaway hook variations for a video topic")
    parser.add_argument("topic", help="Video topic or idea")
    parser.add_argument("--platform", default="yt-long",
                        choices=["yt-long", "yt-shorts", "tiktok", "reels"],
                        help="Target platform (default: yt-long)")
    parser.add_argument("--audience", default="AI builders and content creators",
                        help="Target audience description")
    parser.add_argument("--format", dest="format_type", default="medium",
                        choices=["short", "medium", "long"],
                        help="Video format: short=30-60s, medium=5-8min, long=10-15min (default: medium)")
    parser.add_argument("--no-polish", action="store_true",
                        help="Skip Claude polish pass (faster, cheaper — uses draft only)")
    args = parser.parse_args()

    print(f"Hook writer: \"{args.topic}\" | {args.platform} | {args.format_type}")

    hook_text = await run(args.topic, args.platform, args.audience, args.format_type, args.no_polish)
    output_path = save_output(args.topic, args.platform, args.audience, args.format_type, hook_text)

    print(f"\n{'='*60}")
    print(f"Hooks written to: {output_path}")
    print(f"{'='*60}\n")
    print(hook_text[:800])
    if len(hook_text) > 800:
        print(f"\n... (see full output at {output_path})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
