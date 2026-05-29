"""Shared YouTube transcript extraction via yt_dlp."""

import re
import tempfile
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_transcript(youtube_url: str) -> tuple[str, str]:
    """Extract transcript and title from a YouTube video via yt_dlp.

    Returns (transcript_text, title). Both are empty strings on failure.
    """
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
