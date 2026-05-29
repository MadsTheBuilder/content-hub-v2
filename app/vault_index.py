"""Vault index helpers — sorted newest-first lists for Control Room dropdowns."""

import re
from pathlib import Path

VAULT = Path(__file__).parent.parent / "Content-Hub-Vault-V2"


def _sorted(paths):
    return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)


def list_research_briefs() -> list[Path]:
    return _sorted((VAULT / "10-Research").glob("*.md"))


def list_ideas() -> list[Path]:
    return _sorted((VAULT / "02-Ideas").glob("*.md"))


def list_hooks() -> list[Path]:
    return _sorted((VAULT / "05-Hooks").glob("*.md"))


def list_outlines() -> list[Path]:
    return _sorted((VAULT / "06-Outlines").glob("*.md"))


def list_trending_repos() -> list[str]:
    f = VAULT / "04-Trends" / "github_trending.md"
    if not f.exists():
        return []
    repos = re.findall(r'https://github\.com/([\w.-]+/[\w.-]+)\)', f.read_text(encoding="utf-8"))
    seen, result = set(), []
    for r in repos:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result


def latest(folder: str, pattern: str = "*.md") -> Path | None:
    candidates = _sorted((VAULT / folder).glob(pattern))
    return candidates[0] if candidates else None
