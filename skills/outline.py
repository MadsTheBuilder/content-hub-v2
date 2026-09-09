"""Outline Skill — Generate a Dopamine Ladder video outline for a topic."""

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
from skills.brief_loader import load_brief, apply_cli_overrides
from skills.brief_args import add_brief_args

logger = logging.getLogger(__name__)

VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "06-Outlines"
PROMPT_PATH = PROJECT_ROOT / "prompts" / "outline.md"
MARKETING_BRAIN_PATH = PROJECT_ROOT / "Content-Hub-Vault-V2" / "01-Knowledge" / "marketing_brain.md"


def load_prompt():
    if not PROMPT_PATH.exists():
        logger.error("prompts/outline.md not found at %s", PROMPT_PATH)
        sys.exit(1)
    return PROMPT_PATH.read_text(encoding="utf-8")


def load_marketing_brain():
    if not MARKETING_BRAIN_PATH.exists():
        logger.warning("marketing_brain.md not found — proceeding without supplemental context")
        return ""
    return MARKETING_BRAIN_PATH.read_text(encoding="utf-8")


def load_hook(hook_path):
    if not hook_path:
        return "(no hook provided — generate the outline structure without a specific hook)"
    p = Path(hook_path)
    if not p.exists():
        logger.warning("Hook file not found at %s — continuing without it", hook_path)
        return "(hook file not found — generate the outline structure without a specific hook)"
    return p.read_text(encoding="utf-8")


def make_slug(topic):
    slug = re.sub(r"[^\w\s-]", "", topic.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")
    return "-".join(slug.split("-")[:6])


def build_prompt(template, topic, hook, target_length, platform, marketing_brain):
    filled = template.format(
        topic=topic,
        hook=hook,
        target_length=target_length,
        platform=platform,
    )
    if marketing_brain:
        filled += f"\n\n---\n\n## KALLAWAY CONTEXT\n\n{marketing_brain[:3000]}"
    return filled


async def run(topic, hook, target_length, platform, no_polish):
    template = load_prompt()
    marketing_brain = load_marketing_brain()
    prompt = build_prompt(template, topic, hook, target_length, platform, marketing_brain)

    print("Drafting outline (NIM → Gemini)...")
    draft_result = await draft(prompt)
    if not draft_result["success"]:
        logger.error("Draft failed: %s", draft_result.get("error"))
        sys.exit(1)

    outline_text = draft_result["text"]

    if not no_polish:
        print("Polishing with NIM → Gemini → Ollama → Claude cascade...")
        polish_prompt = (
            prompt
            + f"\n\nDRAFT OUTLINE:\n{outline_text}\n\n"
            "Polish this outline: sharpen every talking point to be specific and non-generic, "
            "verify all 6 Dopamine Ladder stages are present and explicitly named, "
            "ensure [B-ROLL], [SHOW SCREEN], or [TEXT OVERLAY] markers appear in every section, "
            "and confirm Head Fakes appear at least twice. "
            "Keep the exact same format."
        )
        polish_result = await polish(polish_prompt)
        if polish_result["success"]:
            outline_text = polish_result["text"]
        else:
            logger.warning("Polish failed, using draft: %s", polish_result.get("error"))

    return outline_text


def save_output(topic, platform, target_length, hook_path, outline_text):
    slug = make_slug(topic)
    today = date.today().isoformat()
    output_path = VAULT_DIR / f"{today}_{slug}.md"
    VAULT_DIR.mkdir(parents=True, exist_ok=True)

    content = (
        f"---\n"
        f"topic: {topic}\n"
        f"platform: {platform}\n"
        f"target_length: {target_length}m\n"
        f"hook_source: {hook_path or 'none'}\n"
        f"created: {today}\n"
        f"---\n"
        f"# Outline: {topic}\n\n"
        f"{outline_text}\n"
    )
    output_path.write_text(content, encoding="utf-8")
    logger.info("Outline written to %s", output_path)
    return output_path


async def main():
    parser = argparse.ArgumentParser(description="Generate a Dopamine Ladder video outline")
    parser.add_argument("topic", help="Video topic or idea")
    parser.add_argument("--hook-path", default=None,
                        help="Path to a hook .md file from a /hook run (optional but recommended)")
    parser.add_argument("--hook-text", default="",
                        help="Selected hook spoken line text — overrides hook-path when provided")
    parser.add_argument("--length", type=int, default=8,
                        help="Target video length in minutes (default: 8)")
    parser.add_argument("--platform", default="yt-long",
                        choices=["yt-long", "yt-shorts"],
                        help="Target platform (default: yt-long)")
    parser.add_argument("--no-polish", action="store_true",
                        help="Skip Claude polish pass (faster, cheaper — uses draft only)")
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()
    brief = apply_cli_overrides(brief, args)
    if brief.get("target_length_minutes"):
        args.length = brief["target_length_minutes"]

    print(f"Outline writer: \"{args.topic}\" | {args.platform} | {args.length} min")

    hook = args.hook_text if args.hook_text else load_hook(args.hook_path)
    outline_text = await run(args.topic, hook, args.length, args.platform, args.no_polish)
    output_path = save_output(args.topic, args.platform, args.length, args.hook_path, outline_text)

    print(f"\n{'='*60}")
    print(f"Outline written to: {output_path}")
    print(f"{'='*60}\n")
    print(outline_text[:800])
    if len(outline_text) > 800:
        print(f"\n... (see full output at {output_path})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
