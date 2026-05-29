"""Primary-source pre-flight for the research pipeline.

Harvests primary sources (arxiv papers, GitHub repos, official docs, PDFs)
from YT video descriptions via yt-dlp, then falls back to a Gemini prompt
backstop if fewer than 5 credible hits are found from scraping.
"""

import json
import re
import subprocess
import sys

# Trusted primary source patterns
_ARXIV = re.compile(r'https?://arxiv\.org/(?:abs|pdf)/[\w./-]+')
_GITHUB = re.compile(r'https?://github\.com/([^/\s#?\'"]+/[^/\s#?\'"]+)')
_PDF = re.compile(r'https?://\S+\.pdf(?:\?\S*)?')
_OFFICIAL = re.compile(
    r'https?://(?:docs\.[^\s]+|[^\s]+\.readthedocs\.io[^\s]*'
    r'|huggingface\.co/[^\s]+|pytorch\.org[^\s]*|tensorflow\.org[^\s]*'
    r'|openai\.com/research[^\s]*)'
)

# Low-trust domains to reject
_REJECT = re.compile(
    r'(?:reddit\.com|twitter\.com|x\.com|youtube\.com|youtu\.be'
    r'|medium\.com|substack\.com|tiktok\.com|instagram\.com)',
    re.I,
)


def _extract_from_text(text: str) -> list[str]:
    found: list[str] = []
    for m in _ARXIV.finditer(text):
        found.append(m.group(0))
    for m in _GITHUB.finditer(text):
        found.append(f"https://github.com/{m.group(1)}")
    for m in _PDF.finditer(text):
        found.append(m.group(0))
    for m in _OFFICIAL.finditer(text):
        found.append(m.group(0))
    return [u for u in found if not _REJECT.search(u)]


def _scrape_yt_descriptions(seed_urls: list[str]) -> list[str]:
    """Run yt-dlp --get-description on each URL, regex-extract primary links."""
    collected: list[str] = []
    for url in seed_urls:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "yt_dlp",
                 "--get-description", "--no-playlist", "--quiet", url],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=30,
            )
            if result.stdout:
                collected.extend(_extract_from_text(result.stdout))
        except (subprocess.TimeoutExpired, Exception):
            continue
    return collected


async def _gemini_backstop(topic: str) -> list[str]:
    """Ask Gemini to suggest primary source URLs from its training data."""
    try:
        from skills.utils.ai import generate
    except ImportError:
        return []

    prompt = (
        f"List the most relevant primary sources for: {topic}\n\n"
        "Return ONLY a JSON array of real, existing URLs from trusted sources:\n"
        "- arxiv.org papers (e.g. https://arxiv.org/abs/XXXX.XXXXX)\n"
        "- github.com repositories (e.g. https://github.com/owner/repo)\n"
        "- official project documentation\n"
        "- peer-reviewed venues\n\n"
        'Format: ["https://...", ...]\n'
        "Return 5-8 URLs. Return [] if you cannot identify credible primaries."
    )

    result = await generate(prompt, cascade=["claude", "nim"])
    if not result["success"] or not result["text"]:
        return []

    text = result["text"].strip()
    match = re.search(r'\[.*?\]', text, re.DOTALL)
    if not match:
        return []
    try:
        urls = json.loads(match.group(0))
        return [u for u in urls if isinstance(u, str) and u.startswith("http")]
    except (json.JSONDecodeError, TypeError):
        return []


def _dedupe_cap(urls: list[str], cap: int = 8) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for u in urls:
        u = u.rstrip(".,;)")
        if u not in seen:
            seen.add(u)
            result.append(u)
        if len(result) >= cap:
            break
    return result


async def collect_primary_sources(
    topic: str, seed_urls: list[str]
) -> tuple[list[str], dict]:
    """Return (primary_urls, metadata).

    Step 1 — scrape: yt-dlp description regex-extract for each seed URL.
    Step 2 — backstop: if scrape found < 5, ask Gemini for likely primaries.
    """
    raw = _scrape_yt_descriptions(seed_urls)
    strategy = "scrape"

    if len(raw) < 5:
        backstop = await _gemini_backstop(topic)
        if backstop:
            raw = raw + backstop
            strategy = "scrape+search-backstop"

    urls = _dedupe_cap(raw)
    return urls, {"primary_sources_found": len(urls), "strategy": strategy}
