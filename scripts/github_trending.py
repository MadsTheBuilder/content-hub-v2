#!/usr/bin/env python3
"""
github_trending.py — Daily AI repo pulse for Content Hub.

Run manually or via Windows Task Scheduler (see run_github_trending.bat).
Output: Content-Hub-Vault-V2/04-Trends/github_trending.md
"""

import json
import os
import subprocess
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
OUTPUT = ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"
LOG_DIR = ROOT / "logs"

# ── config ────────────────────────────────────────────────────────────────────
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
# 3 searches (one per topic) against the 30-day window covers both windows.
# GitHub Search API doesn't support OR across topic qualifiers with date filters.
# Unauthenticated limit: 10 req/min. 3 calls is safe; add GITHUB_TOKEN for 5000/hr.
AI_TOPICS = ["llm", "ai", "machine-learning"]


# ── GitHub API ────────────────────────────────────────────────────────────────

def _gh_headers() -> dict:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "content-hub-trending/1.0",
    }
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def _search_one_topic(topic: str, since_date: str, per_page: int = 10) -> list[dict]:
    q = f"topic:{topic} created:>{since_date}"
    url = (
        "https://api.github.com/search/repositories?"
        + urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": per_page})
    )
    req = urllib.request.Request(url, headers=_gh_headers())
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read()).get("items", [])


def search_repos(since_date: str, fetch: int = 30) -> list[dict]:
    """Return raw GitHub repo items created after since_date, merged across AI topics, sorted by stars."""
    seen: set[int] = set()
    merged: list[dict] = []
    for topic in AI_TOPICS:
        for item in _search_one_topic(topic, since_date, per_page=15):
            if item["id"] not in seen:
                seen.add(item["id"])
                merged.append(item)
    merged.sort(key=lambda r: r["stargazers_count"], reverse=True)
    return merged[:fetch]


def enrich(raw: dict, now: datetime) -> dict:
    created = datetime.fromisoformat(raw["created_at"].replace("Z", "+00:00"))
    age = max(1, (now - created).days)
    return {
        "name": raw["full_name"],
        "description": (raw.get("description") or "").strip(),
        "language": raw.get("language") or "—",
        "stars": raw["stargazers_count"],
        "velocity": round(raw["stargazers_count"] / age, 1),
        "url": raw["html_url"],
    }


# ── Claude pick ───────────────────────────────────────────────────────────────

def claude_picks(repos_7d: list[dict], repos_30d: list[dict]) -> tuple[str, str, str, str]:
    """Return (name_7d, reason_7d, name_30d, reason_30d). Uses claude CLI (Pro plan auth)."""

    def fmt(repos: list[dict]) -> str:
        return "\n".join(
            f"{i+1}. {r['name']} | {r['stars']:,} stars | {r['velocity']}/day | {r['language']}\n"
            f"   {r['description']}\n   {r['url']}"
            for i, r in enumerate(repos)
        )

    prompt = (
        "You are a tech content strategist for an AI-focused YouTube channel.\n\n"
        "Pick ONE repo from each list as the best candidate for a YouTube tutorial or explainer.\n"
        "Criteria: genuine novelty, teaching potential, audience interest, not already overexposed.\n\n"
        f"LAST 7 DAYS — TOP {len(repos_7d)}:\n{fmt(repos_7d)}\n\n"
        f"LAST 30 DAYS — TOP {len(repos_30d)}:\n{fmt(repos_30d)}\n\n"
        "Respond with ONLY valid JSON, no markdown fences:\n"
        '{"pick_7d": {"name": "owner/repo", "reason": "1-2 sentences"}, '
        '"pick_30d": {"name": "owner/repo", "reason": "1-2 sentences"}}'
    )

    result = subprocess.run(
        "claude",
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        shell=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed: {result.stderr.strip()}")

    raw = result.stdout.strip()
    # Strip markdown fences if claude wraps the JSON anyway
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    parsed = json.loads(raw.strip())
    p7 = parsed["pick_7d"]
    p30 = parsed["pick_30d"]
    return p7["name"], p7["reason"], p30["name"], p30["reason"]


# ── Claude deep dive ─────────────────────────────────────────────────────────

def claude_deep_dive(repo: dict) -> dict:
    """Return detailed breakdown for one repo: problem, how_it_works, use_cases, getting_started."""
    prompt = (
        f"Repo: {repo['name']}\n"
        f"Description: {repo['description']}\n"
        f"Language: {repo['language']}\n"
        f"Stars: {repo['stars']:,}\n"
        f"URL: {repo['url']}\n\n"
        "Using ONLY the information above (do not fetch URLs or external data), write a breakdown "
        "for a tech content creator. Respond with ONLY valid JSON, no markdown fences:\n"
        '{"problem": "What real problem does this solve? (2-3 sentences)", '
        '"how_it_works": "How does it work technically? (2-3 sentences)", '
        '"use_cases": ["use case 1", "use case 2", "use case 3"], '
        '"getting_started": "How would a developer get started with this? (1-2 sentences)"}'
    )
    result = subprocess.run(
        "claude",
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=60,
        shell=True,
    )
    if result.returncode != 0:
        return {}
    raw = result.stdout.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        return {}


def write_repo_file(repo: dict, dive: dict, trends_dir: Path) -> None:
    if not dive:
        return
    slug = repo["name"].replace("/", "_")
    folder = trends_dir / slug
    folder.mkdir(parents=True, exist_ok=True)
    use_cases = "\n".join(f"- {uc}" for uc in dive.get("use_cases", []))
    today = datetime.now().strftime("%Y-%m-%d")
    content = "\n".join([
        f"# {repo['name']}",
        "",
        f"> {repo['description']}",
        "",
        f"**Language:** {repo['language']} · **Stars:** {repo['stars']:,} · **Velocity:** {repo['velocity']}/day · [GitHub]({repo['url']})",
        "",
        f"*Captured {today}*",
        "",
        "---",
        "",
        "## What problem does it solve?",
        "",
        dive.get("problem", ""),
        "",
        "## How it works",
        "",
        dive.get("how_it_works", ""),
        "",
        "## Best use cases",
        "",
        use_cases,
        "",
        "## Getting started",
        "",
        dive.get("getting_started", ""),
    ])
    (folder / f"{slug}.md").write_text(content, encoding="utf-8")


# ── render ────────────────────────────────────────────────────────────────────

def _table(repos: list[dict], highlight: str) -> list[str]:
    rows = [
        "| Repo | Stars | ⚡ Stars/day | Language | Description |",
        "|------|------:|------------:|----------|-------------|",
    ]
    for r in repos:
        flag = " 🎯" if r["name"] == highlight else ""
        desc = r["description"]
        if len(desc) > 75:
            desc = desc[:72] + "…"
        rows.append(
            f"| [{r['name']}]({r['url']}){flag}"
            f" | {r['stars']:,} | {r['velocity']} | {r['language']} | {desc} |"
        )
    return rows


def render(repos_7d, repos_30d, name_7d, reason_7d, name_30d, reason_30d) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    url_7d = next((r["url"] for r in repos_7d if r["name"] == name_7d), "")
    url_30d = next((r["url"] for r in repos_30d if r["name"] == name_30d), "")
    slug_7d = name_7d.replace("/", "_")
    slug_30d = name_30d.replace("/", "_")

    lines = [
        f"# GitHub Trending AI Repos — {today}",
        "",
        "> Auto-generated daily. 🎯 = Claude's pick for best video topic.",
        "",
        "---",
        "",
        "## Last 7 Days — Top 10",
        "",
        *_table(repos_7d, name_7d),
        "",
        "## Last 30 Days — Top 5",
        "",
        *_table(repos_30d, name_30d),
        "",
        "---",
        "",
        "## Claude's Daily Picks",
        "",
        f"### 7-day pick → [{name_7d}]({url_7d})",
        "",
        reason_7d,
        "",
        f"→ Deep dive: [[{slug_7d}/{slug_7d}]]",
        "",
        f"### 30-day pick → [{name_30d}]({url_30d})",
        "",
        reason_30d,
        "",
        f"→ Deep dive: [[{slug_30d}/{slug_30d}]]",
        "",
        "---",
        f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        " · [GitHub Trending](https://github.com/trending)*",
    ]
    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    now = datetime.now(timezone.utc)
    cutoff_7d = now - timedelta(days=7)
    date_30d = (now - timedelta(days=30)).strftime("%Y-%m-%d")

    # One search against 30-day window; split client-side into both windows.
    print("Fetching trending repos (30-day window)...")
    raw = search_repos(date_30d, fetch=40)
    all_repos = [enrich(r, now) for r in raw]

    created_map = {r["full_name"]: r["created_at"] for r in raw}
    repos_7d = [
        r for r in all_repos
        if datetime.fromisoformat(created_map[r["name"]].replace("Z", "+00:00")) >= cutoff_7d
    ][:10]

    seen_7d = {r["name"] for r in repos_7d}
    repos_30d = [r for r in all_repos if r["name"] not in seen_7d][:5]

    print(f"  7-day: {len(repos_7d)} repos | 30-day extra: {len(repos_30d)} repos")
    print("Asking Claude for picks...")
    name_7d, reason_7d, name_30d, reason_30d = claude_picks(repos_7d, repos_30d)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)
    OUTPUT.write_text(
        render(repos_7d, repos_30d, name_7d, reason_7d, name_30d, reason_30d),
        encoding="utf-8",
    )

    # Every shortlisted repo gets its own subfolder — not just the picks.
    all_shortlisted = repos_7d + repos_30d
    print(f"Generating deep dives for all {len(all_shortlisted)} shortlisted repos...")
    for i, repo in enumerate(all_shortlisted, 1):
        print(f"  [{i}/{len(all_shortlisted)}] {repo['name']}")
        dive = claude_deep_dive(repo)
        write_repo_file(repo, dive, OUTPUT.parent)
    print(f"Done. Written to {OUTPUT.parent}")


if __name__ == "__main__":
    main()
