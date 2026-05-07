"""Researcher — Content gap discovery via NotebookLM.

Pipeline (one isolated notebook per repo):
  1. Read trend URLs from Content-Hub-Vault-V2/04-Trends/github_trending.md
  2. For each URL: create a notebook, add that repo as the sole source,
     run web research, query for content gaps, collect the finding
  3. Compile all findings into one brief →
     Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche>_brief.md

Usage:
  python -m skills.researcher --niche "AI agents"
  python -m skills.researcher --niche "AI agents" --mode deep
  python -m skills.researcher --niche "AI agents" --max-sources 5
"""

import asyncio
import argparse
import logging
import re
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKLM_SRC = PROJECT_ROOT / "notebooklm-py" / "src"
if str(NOTEBOOKLM_SRC) not in sys.path:
    sys.path.insert(0, str(NOTEBOOKLM_SRC))

from notebooklm import NotebookLMClient

logger = logging.getLogger(__name__)

TRENDS_FILE = PROJECT_ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"
RESEARCH_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "10-Research"
PROMPT_FILE = PROJECT_ROOT / "prompts" / "researcher.md"


def extract_urls(trends_text: str) -> list[str]:
    """Extract GitHub repo URLs from the trending markdown file."""
    raw_urls = re.findall(r'\(https?://[^)]+\)', trends_text)
    seen: set[str] = set()
    result = []
    for raw in raw_urls:
        url = raw[1:-1]
        if url in seen:
            continue
        seen.add(url)
        # Only top-level GitHub repo URLs (github.com/owner/repo — exactly 4 slashes)
        if url.startswith("https://github.com/") and url.count("/") == 4:
            result.append(url)
    return result


def repo_slug(url: str) -> str:
    """github.com/owner/repo → owner-repo"""
    parts = url.rstrip("/").split("/")
    return f"{parts[-2]}-{parts[-1]}"


async def research_one(client: "NotebookLMClient", url: str, prompt_text: str, mode: str) -> dict:
    """Run a fully isolated research pipeline for a single repo URL.

    Returns a dict with keys: url, notebook_id, finding (str), sources_found (list).
    """
    slug = repo_slug(url)
    title = f"Research: {slug} — {date.today().isoformat()}"

    print(f"\n[{slug}] Creating notebook...")
    nb = await client.notebooks.create(title)
    logger.info("[%s] Notebook: %s", slug, nb.id)

    await client.sources.add_url(nb.id, url, wait=True)
    print(f"[{slug}] Source indexed. Starting web research ({mode} mode)...")

    repo_name = url.rstrip("/").split("/")[-1].replace("-", " ")
    research = await client.research.start(nb.id, repo_name, source="web", mode=mode)
    task_id = research.get("task_id") if research else None

    max_polls = 24 if mode == "deep" else 12
    poll_interval = 15 if mode == "deep" else 10
    sources_found: list = []

    for i in range(max_polls):
        await asyncio.sleep(poll_interval)
        status = await client.research.poll(nb.id)
        state = status.get("status", "unknown")
        print(f"[{slug}] Research [{i + 1}/{max_polls}]: {state}")
        if state == "completed":
            sources_found = status.get("sources", [])
            print(f"[{slug}] Discovered {len(sources_found)} related sources")
            break

    if sources_found and task_id:
        import_count = min(len(sources_found), 10)
        await client.research.import_sources(nb.id, task_id, sources_found[:import_count])
        print(f"[{slug}] Imported {import_count} sources")

    await asyncio.sleep(75)

    print(f"[{slug}] Querying for content gaps...")
    result = await client.chat.ask(nb.id, prompt_text)

    return {
        "url": url,
        "notebook_id": nb.id,
        "finding": result.answer,
        "sources_found": sources_found,
    }


async def run(niche: str, mode: str = "deep", max_sources: int = 8, repos: list[str] | None = None) -> Path:
    """Run isolated research per repo. Returns path to the compiled brief."""

    if not TRENDS_FILE.exists():
        raise FileNotFoundError(f"Trends file not found: {TRENDS_FILE}")

    trends_text = TRENDS_FILE.read_text(encoding="utf-8")
    urls = extract_urls(trends_text)

    if repos:
        # Normalise slugs: accept "owner/repo" or full URL
        def to_slug(r: str) -> str:
            r = r.strip().rstrip("/")
            if r.startswith("https://"):
                parts = r.split("/")
                return f"{parts[-2]}/{parts[-1]}"
            return r

        wanted = {to_slug(r) for r in repos}
        urls = [u for u in urls if f"{u.split('/')[-2]}/{u.split('/')[-1]}" in wanted]
    else:
        urls = urls[:max_sources]

    if not urls:
        raise ValueError(f"No matching GitHub repo URLs found in {TRENDS_FILE}")

    prompt_text = PROMPT_FILE.read_text(encoding="utf-8")
    today = date.today().isoformat()

    print(f"Found {len(urls)} repos. Running isolated research on each...\n")

    findings = []
    async with await NotebookLMClient.from_storage(timeout=300) as client:
        for url in urls:
            try:
                result = await research_one(client, url, prompt_text, mode)
                findings.append(result)
            except Exception as e:
                logger.error("Failed for %s: %s", url, e)
                findings.append({"url": url, "notebook_id": None, "finding": f"ERROR: {e}", "sources_found": []})

    # Compile all findings into one brief
    sections = []
    for f in findings:
        slug = repo_slug(f["url"])
        nb_line = f"notebook_id: {f['notebook_id']}" if f["notebook_id"] else "notebook_id: failed"
        sources = f["sources_found"]
        if sources:
            source_lines = "\n".join(
                f"- [{s.get('title', 'Untitled')}]({s['url']})" if s.get("url")
                else f"- {s.get('title', 'Untitled')}"
                for s in sources
            )
            sources_section = f"### Discovered Sources ({len(sources)})\n{source_lines}\n"
        else:
            sources_section = "### Discovered Sources (0)\n"
        sections.append(
            f"## {slug}\n"
            f"Source: {f['url']}  \n"
            f"{nb_line}  \n\n"
            f"{sources_section}\n"
            f"{f['finding']}\n"
        )

    niche_slug = niche.lower().replace(" ", "-")
    notebook_ids = [f["notebook_id"] for f in findings if f["notebook_id"]]

    output = (
        f"---\n"
        f"date: {today}\n"
        f"niche: {niche}\n"
        f"repos_researched: {len(findings)}\n"
        f"notebook_ids: [{', '.join(notebook_ids)}]\n"
        f"---\n\n"
        f"# Research Brief — {niche}\n"
        f"*{today} — {len(findings)} repos, each in its own notebook*\n\n"
        + "\n---\n\n".join(sections)
    )

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESEARCH_DIR / f"{today}_{niche_slug}_brief.md"
    output_path.write_text(output, encoding="utf-8")

    print(f"\nBrief written to: {output_path}")
    return output_path


async def main() -> None:
    parser = argparse.ArgumentParser(description="Content gap research via NotebookLM")
    parser.add_argument("--niche", required=True, help='Topic to research, e.g. "AI agents"')
    parser.add_argument("--mode", choices=["fast", "deep"], default="deep")
    parser.add_argument("--max-sources", type=int, default=8,
                        help="Max trend URLs to research (default: 8)")
    parser.add_argument("--repos", nargs="+", metavar="OWNER/REPO",
                        help='Filter to specific repos, e.g. --repos HKUDS-AI/polymarket-ai-trading MemPalace/mempalace')
    args = parser.parse_args()

    output_path = await run(args.niche, mode=args.mode, max_sources=args.max_sources, repos=args.repos)

    print("\n" + "=" * 60)
    brief = output_path.read_text(encoding="utf-8")
    print(brief[:2000])
    if len(brief) > 2000:
        print(f"\n...({len(brief) - 2000} more chars — open {output_path})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
