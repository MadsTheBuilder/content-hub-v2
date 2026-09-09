#!/usr/bin/env python3
"""
github_trending.py — Daily AI repo pulse for Content Hub.

Run manually or via Windows Task Scheduler (see run_github_trending.bat).
Output: Content-Hub-Vault-V2/04-Trends/github_trending.md

Ranking: scrapes github.com/trending for weekly + monthly windows.
Winners = highest stars-this-period (total stars shown as context).
"""

import json
import re
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

# ── paths ─────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"
LOG_DIR = ROOT / "logs"


# ── scraper ───────────────────────────────────────────────────────────────────

def _parse_int(s: str) -> int:
    return int(re.sub(r"[,\s]", "", s))


def scrape_trending(since: str, limit: int = 25) -> list[dict]:
    """
    Scrape github.com/trending and return repos ranked by period stars.
    since = 'weekly' | 'monthly'
    Ranking criteria: stars this period (highest wins). Total stars shown as context.
    """
    url = f"https://github.com/trending?since={since}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read().decode("utf-8")

    days = 7 if since == "weekly" else 30
    repos = []

    for block in re.split(r"<article\b[^>]*>", raw)[1:limit + 1]:
        # Full name from the h2 anchor: href="/owner/repo"
        # href is not the first attribute — data-hydro-click comes first
        m = re.search(r'<h2[^>]*>.*?<a\s[^>]*href="/([^/"]+/[^/"]+)"', block, re.DOTALL)
        if not m:
            continue
        full_name = m.group(1).strip()

        # Description
        desc_m = re.search(r'<p\b[^>]*col-9[^>]*>\s*(.*?)\s*</p>', block, re.DOTALL)
        description = re.sub(r"\s+", " ", desc_m.group(1)).strip() if desc_m else ""

        # Language
        lang_m = re.search(r'itemprop="programmingLanguage"[^>]*>\s*([^<]+)', block)
        language = lang_m.group(1).strip() if lang_m else "—"

        # Total stars (link to /stargazers)
        stars_m = re.search(
            rf'href="/{re.escape(full_name)}/stargazers"[^>]*>.*?</svg>\s*([\d,]+)',
            block, re.DOTALL,
        )
        total_stars = _parse_int(stars_m.group(1)) if stars_m else 0

        # Stars this period: "1,234 stars this week" or "5,678 stars this month"
        period_m = re.search(r"([\d,]+)\s+stars?\s+this\s+(?:week|month)", block, re.IGNORECASE)
        period_stars = _parse_int(period_m.group(1)) if period_m else 0

        repos.append({
            "name": full_name,
            "description": description,
            "language": language,
            "stars": total_stars,
            "period_stars": period_stars,
            "velocity": round(period_stars / days, 1),
            "url": f"https://github.com/{full_name}",
        })

    # Rank by stars this period — highest wins
    repos.sort(key=lambda r: r["period_stars"], reverse=True)
    return repos


# ── Claude pick ───────────────────────────────────────────────────────────────

def claude_picks(weekly: list[dict], monthly: list[dict]) -> tuple[str, str, str, str]:
    """Return (name_weekly, reason_weekly, name_monthly, reason_monthly)."""

    def fmt(repos: list[dict], period: str) -> str:
        return "\n".join(
            f"{i+1}. {r['name']} | {r['stars']:,} total stars | {r['period_stars']:,} stars this {period} | {r['language']}\n"
            f"   {r['description']}\n   {r['url']}"
            for i, r in enumerate(repos)
        )

    prompt = (
        "You are a tech content strategist for an AI-focused YouTube channel.\n\n"
        "Pick ONE repo from each list as the best candidate for a YouTube tutorial or explainer.\n"
        "Criteria: genuine novelty, teaching potential, audience interest, not already overexposed.\n\n"
        f"THIS WEEK — TOP {len(weekly)} (ranked by stars this week):\n{fmt(weekly, 'week')}\n\n"
        f"THIS MONTH — TOP {len(monthly)} (ranked by stars this month):\n{fmt(monthly, 'month')}\n\n"
        "Respond with ONLY valid JSON, no markdown fences:\n"
        '{"pick_weekly": {"name": "owner/repo", "reason": "1-2 sentences"}, '
        '"pick_monthly": {"name": "owner/repo", "reason": "1-2 sentences"}}'
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
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    parsed = json.loads(raw.strip())
    pw = parsed["pick_weekly"]
    pm = parsed["pick_monthly"]
    return pw["name"], pw["reason"], pm["name"], pm["reason"]


# ── Claude deep dive ─────────────────────────────────────────────────────────

def claude_deep_dive(repo: dict) -> dict:
    """Return detailed breakdown for one repo."""
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

def _table(repos: list[dict], period_label: str, highlight: str) -> list[str]:
    rows = [
        f"| Repo | Total Stars | ⚡ Stars this {period_label} | Language | Description |",
        f"|------|------------:|-------------------:|----------|-------------|",
    ]
    for r in repos:
        flag = " 🎯" if r["name"] == highlight else ""
        desc = r["description"][:72] + "…" if len(r["description"]) > 75 else r["description"]
        rows.append(
            f"| [{r['name']}]({r['url']}){flag}"
            f" | {r['stars']:,} | {r['period_stars']:,} | {r['language']} | {desc} |"
        )
    return rows


def render(weekly, monthly, name_w, reason_w, name_m, reason_m) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    url_w = next((r["url"] for r in weekly if r["name"] == name_w), "")
    url_m = next((r["url"] for r in monthly if r["name"] == name_m), "")
    slug_w = name_w.replace("/", "_")
    slug_m = name_m.replace("/", "_")

    lines = [
        f"# GitHub Trending Repos — {today}",
        "",
        "> Auto-generated daily. Ranked by stars this period. 🎯 = Claude's pick for best video topic.",
        "",
        "---",
        "",
        "## This Week — Top 10",
        "",
        *_table(weekly[:10], "week", name_w),
        "",
        "## This Month — Top 10",
        "",
        *_table(monthly[:10], "month", name_m),
        "",
        "---",
        "",
        "## Claude's Daily Picks",
        "",
        f"### Weekly pick → [{name_w}]({url_w})",
        "",
        reason_w,
        "",
        f"→ Deep dive: [[{slug_w}/{slug_w}]]",
        "",
        f"### Monthly pick → [{name_m}]({url_m})",
        "",
        reason_m,
        "",
        f"→ Deep dive: [[{slug_m}/{slug_m}]]",
        "",
        "---",
        f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        " · [GitHub Trending](https://github.com/trending)*",
    ]
    return "\n".join(lines)


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Scraping GitHub Trending (this week)...")
    weekly = scrape_trending("weekly", limit=25)
    print(f"  {len(weekly)} repos | top: {weekly[0]['name']} ({weekly[0]['period_stars']:,} stars this week)" if weekly else "  0 repos")

    print("Scraping GitHub Trending (this month)...")
    monthly = scrape_trending("monthly", limit=25)
    print(f"  {len(monthly)} repos | top: {monthly[0]['name']} ({monthly[0]['period_stars']:,} stars this month)" if monthly else "  0 repos")

    if not weekly or not monthly:
        raise SystemExit("Scraping returned no results — GitHub HTML structure may have changed.")

    print("Asking Claude for picks...")
    name_w, reason_w, name_m, reason_m = claude_picks(weekly[:10], monthly[:10])

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    # Deep dives for all shortlisted repos, deduped
    seen: set[str] = set()
    shortlisted = []
    for r in weekly[:10] + monthly[:10]:
        if r["name"] not in seen:
            seen.add(r["name"])
            shortlisted.append(r)

    print(f"Generating deep dives for {len(shortlisted)} repos...")
    for i, repo in enumerate(shortlisted, 1):
        print(f"  [{i}/{len(shortlisted)}] {repo['name']}")
        dive = claude_deep_dive(repo)
        write_repo_file(repo, dive, OUTPUT.parent)

    OUTPUT.write_text(
        render(weekly, monthly, name_w, reason_w, name_m, reason_m),
        encoding="utf-8",
    )
    print(f"Done. Written to {OUTPUT}")


if __name__ == "__main__":
    main()
