"""Short Form — V2 Vertical Video Scripts from YouTube."""

import asyncio, argparse, logging, sys, re, tempfile
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from skills.utils.ai import generate

logger = logging.getLogger(__name__)
VAULT_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "09-Shorts"


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
    """Load and split prompts/short_form.md into three templates."""
    content = (PROJECT_ROOT / "prompts" / "short_form.md").read_text()
    thirty_start = content.find("## 30 SECOND SCRIPT")
    sixty_start = content.find("## 60 SECOND SCRIPT")
    ninety_start = content.find("## 90 SECOND SCRIPT")
    if thirty_start == -1 or sixty_start == -1 or ninety_start == -1:
        logger.error("Could not find section headers in prompts/short_form.md")
        sys.exit(1)
    thirty = content[thirty_start + len("## 30 SECOND SCRIPT"):sixty_start].strip()
    sixty = content[sixty_start + len("## 60 SECOND SCRIPT"):ninety_start].strip()
    ninety = content[ninety_start + len("## 90 SECOND SCRIPT"):].strip()
    return thirty, sixty, ninety

def make_output_dir(title: str) -> Path:
    """Create output directory with slug-based name."""
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
    out = VAULT_DIR / f"{date.today().isoformat()}_{slug}"
    out.mkdir(parents=True, exist_ok=True)
    return out

async def main():
    parser = argparse.ArgumentParser(description="Generate short-form vertical video scripts from YouTube")
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

    thirty_tpl, sixty_tpl, ninety_tpl = load_prompts()
    transcript_trunc = transcript[:4000]
    today = date.today().isoformat()

    print("Generating 30s script...")
    thirty_result = await generate(thirty_tpl.format(title=title, transcript=transcript_trunc))
    print("Generating 60s script...")
    sixty_result = await generate(sixty_tpl.format(title=title, transcript=transcript_trunc))
    print("Generating 90s script...")
    ninety_result = await generate(ninety_tpl.format(title=title, transcript=transcript_trunc))

    thirty_content = thirty_result["text"] if thirty_result["success"] else ""
    sixty_content = sixty_result["text"] if sixty_result["success"] else ""
    ninety_content = ninety_result["text"] if ninety_result["success"] else ""

    if not all([thirty_content, sixty_content, ninety_content]):
        print("❌ One or more generations failed")
        sys.exit(1)

    output_dir = make_output_dir(title)

    (output_dir / "30s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: {args.youtube_url}
duration: 30s
---

{thirty_content}
""", encoding="utf-8")

    (output_dir / "60s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: {args.youtube_url}
duration: 60s
---

{sixty_content}
""", encoding="utf-8")

    (output_dir / "90s_script.md").write_text(f"""---
title: "{title}"
date: {today}
youtube_url: {args.youtube_url}
duration: 90s
---

{ninety_content}
""", encoding="utf-8")

    (output_dir / "README.md").write_text(f"""# Short Form Scripts — {title}

**Date:** {today}
**Video:** {args.youtube_url}

## Scripts
- `30s_script.md` — 30-second vertical script
- `60s_script.md` — 60-second vertical script
- `90s_script.md` — 90-second vertical script

## Checklist
- [ ] Review 30s_script.md → record
- [ ] Review 60s_script.md → record
- [ ] Review 90s_script.md → record
""", encoding="utf-8")

    print(f"""✅ Short-form package written to:
   {output_dir}

🎬 30s_script.md
🎬 60s_script.md
🎬 90s_script.md
📋 README.md
""")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
