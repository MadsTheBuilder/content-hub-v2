"""GitHub documentation crawler — discover primary docs for a repo.

Exports:
  - DocCandidate: dataclass for discovered doc file
  - discover_primary_docs(owner_repo, token=None) -> list[DocCandidate]
"""

import os
import re
from dataclasses import dataclass
from typing import Optional

import httpx


@dataclass
class DocCandidate:
    """A discovered doc file candidate for inclusion as a primary source."""
    path: str  # e.g. "docs/getting-started.md"
    raw_url: str  # e.g. "https://raw.githubusercontent.com/owner/repo/main/docs/..."
    rank: int  # lower = higher priority


def _gh_headers() -> dict:
    """Build GitHub API headers, with auth if token available."""
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "researcher-crawler/1.0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


async def _get_branch_name(owner_repo: str) -> str:
    """Detect the default branch (main or master) via GitHub API."""
    url = f"https://api.github.com/repos/{owner_repo}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, headers=_gh_headers())
            if resp.status_code == 200:
                data = resp.json()
                return data.get("default_branch", "main")
    except Exception:
        pass
    return "main"  # fallback


async def _list_dir_contents(owner_repo: str, branch: str, path: str) -> list[str]:
    """List filenames in a directory via GitHub Contents API.

    Returns list of filenames (without path prefix) in that dir, or [] if not found.
    """
    url = f"https://api.github.com/repos/{owner_repo}/contents/{path}"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params={"ref": branch}, headers=_gh_headers())
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    # Filter to .md files
                    return [item["name"] for item in data if item["type"] == "file" and item["name"].endswith(".md")]
    except Exception:
        pass
    return []


def _rank_path(path: str) -> int:
    """Assign rank to a doc path (lower = higher priority)."""
    name = path.lower()

    # Tier 0: README at root (not crawled here, added separately)

    # Tier 1: docs/{index, readme, introduction}
    if name in ("docs/index.md", "docs/readme.md", "docs/introduction.md"):
        return 10 + ["docs/index.md", "docs/readme.md", "docs/introduction.md"].index(name)

    # Tier 2: quickstart/getting-started/installation
    if name in ("docs/getting-started.md", "docs/quickstart.md", "docs/installation.md"):
        return 20 + ["docs/getting-started.md", "docs/quickstart.md", "docs/installation.md"].index(name)

    # Tier 2.5: tutorial*.md
    if name.startswith("docs/tutorial") and name.endswith(".md"):
        return 25

    # Tier 3: root architecture/contributing/design
    if name in ("contributing.md", "architecture.md", "design.md"):
        return 30 + ["contributing.md", "architecture.md", "design.md"].index(name)

    # Tier 4: remaining docs/*.md (alphabetical)
    if name.startswith("docs/"):
        return 40 + ord(name[5])  # sort by first char of filename

    # Tier 5: examples/*.md or examples/readme.md
    if name.startswith("examples/"):
        if name == "examples/readme.md":
            return 50
        return 51 + ord(name[9])

    # Fallback (should not reach)
    return 999


async def discover_primary_docs(
    owner_repo: str,
    token: Optional[str] = None,
    max_docs: int = 6
) -> list[DocCandidate]:
    """Discover primary documentation files in a GitHub repo.

    Args:
        owner_repo: "owner/repo" format string
        token: GitHub token (optional; reads GITHUB_TOKEN env var if not provided)
        max_docs: Maximum number of docs to return (default 6)

    Returns:
        list[DocCandidate] sorted by rank (ascending), capped at max_docs
    """
    if token:
        os.environ["GITHUB_TOKEN"] = token

    # Detect default branch
    branch = await _get_branch_name(owner_repo)

    candidates: list[DocCandidate] = []

    # Search directories: docs, documentation, examples
    search_dirs = ["docs", "documentation", "examples"]
    for dir_name in search_dirs:
        files = await _list_dir_contents(owner_repo, branch, dir_name)
        for fname in files:
            path = f"{dir_name}/{fname}"
            raw_url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{path}"
            rank = _rank_path(path)
            candidates.append(DocCandidate(path=path, raw_url=raw_url, rank=rank))

    # Root-level docs (check once)
    root_files = await _list_dir_contents(owner_repo, branch, "")
    for fname in ["CONTRIBUTING.md", "ARCHITECTURE.md", "DESIGN.md"]:
        if fname.lower() in [f.lower() for f in root_files]:
            # Found it; get exact case
            exact_name = next((f for f in root_files if f.lower() == fname.lower()), fname)
            raw_url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/{exact_name}"
            rank = _rank_path(exact_name.lower())
            candidates.append(DocCandidate(path=exact_name, raw_url=raw_url, rank=rank))

    # Sort by rank and cap
    candidates.sort(key=lambda c: c.rank)
    return candidates[:max_docs]
