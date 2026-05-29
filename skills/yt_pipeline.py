"""
YT Pipeline skill helper.

Modes:
  search  <topic>              Search YouTube, print numbered URL list
  run     <topic> <url,...>    Create NLM notebook, add sources, extract analysis, write vault
"""

import asyncio
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

from skills.helpers.nlm_seed import seed_questions_from_nlm
from skills.research_plan import QuestionPlan, generate_followups
from skills.research_sources import collect_primary_sources

VAULT = Path(__file__).parent.parent / "Content-Hub-Vault-V2" / "10-Research"
_NLM_SRC = str(Path(__file__).parent.parent / "notebooklm-py" / "src")
NLM_CMD = [sys.executable, "-m", "notebooklm"]

_existing_pythonpath = os.environ.get("PYTHONPATH", "")
_pythonpath = f"{_NLM_SRC}{os.pathsep}{_existing_pythonpath}" if _existing_pythonpath else _NLM_SRC
_SUBPROCESS_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONIOENCODING": "utf-8", "PYTHONPATH": _pythonpath}

# Artifacts generated one at a time after Q&A extraction.
# Each entry: (generate subcommand, download subcommand, file extension)
ARTIFACT_QUEUE = [
    ("slide-deck",  "slide-deck",  "pdf"),
    ("infographic", "infographic", "png"),
    ("report",      "report",      "md"),
    ("mind-map",    "mind-map",    "json"),
]


def search(topic: str, also: list[str] | None = None) -> None:
    import yt_dlp

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }
    queries = [f"ytsearch25:{topic}"]
    if also:
        queries.extend(f"ytsearch25:{q}" for q in also)

    seen_ids: set[str] = set()
    all_entries: list[dict] = []
    with yt_dlp.YoutubeDL(opts) as ydl:
        for q in queries:
            info = ydl.extract_info(q, download=False)
            for entry in info.get("entries", []):
                vid_id = entry.get("id", "")
                if vid_id and vid_id not in seen_ids:
                    seen_ids.add(vid_id)
                    all_entries.append(entry)

    results = []
    for i, entry in enumerate(all_entries, 1):
        url = f"https://www.youtube.com/watch?v={entry.get('id', '')}"
        title = entry.get("title", "Unknown")
        channel = entry.get("channel", entry.get("uploader", "Unknown"))
        views = entry.get("view_count")
        views_str = f"{views:,}" if views else "?"
        results.append({"n": i, "title": title, "channel": channel, "views": views_str, "url": url})

    for r in results:
        print(f"{r['n']}. [{r['views']} views] {r['title']}")
        print(f"   Channel: {r['channel']}")
        print(f"   {r['url']}")
        print()


def _run_nlm(args: list[str], timeout: float | None = None) -> str:
    try:
        result = subprocess.run(
            NLM_CMD + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=_SUBPROCESS_ENV,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        print(f"[nlm timeout] {' '.join(args[:2])} exceeded {timeout}s", file=sys.stderr)
        return ""
    if result.returncode != 0:
        print(f"[nlm error] {result.stderr.strip()}", file=sys.stderr)
    return (result.stdout or "").strip()


def _parse_notebook_id(output: str) -> str | None:
    match = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", output)
    return match.group(0) if match else None


def _generate_artifact(gen_cmd: str, dl_cmd: str, ext: str, notebook_id: str, out_dir: Path) -> bool:
    """Generate one artifact type and download it. Returns True on success."""
    print(f"Generating {gen_cmd}...")
    raw = _run_nlm([
        "generate", gen_cmd,
        "--notebook", notebook_id,
        "--wait",
        "--retry", "3",
        "--json",
    ], timeout=360)

    try:
        data = json.loads(raw)
        if data.get("error"):
            print(f"[warn] {gen_cmd} failed: {data.get('message', 'unknown')}", file=sys.stderr)
            return False
    except (json.JSONDecodeError, AttributeError):
        if not raw or "error" in raw.lower() or "failed" in raw.lower():
            print(f"[warn] {gen_cmd} generation may have failed — skipping download", file=sys.stderr)
            return False

    filename = gen_cmd.replace("-", "_") + "." + ext
    out_path = out_dir / filename
    print(f"  Downloading {gen_cmd} -> {out_path.name}")
    _run_nlm([
        "download", dl_cmd,
        "--notebook", notebook_id,
        "--latest",
        "--force",
        "--json",
        str(out_path),
    ])
    if out_path.exists():
        print(f"  Saved: {out_path}")
        return True
    print(f"[warn] {gen_cmd} download produced no file at {out_path}", file=sys.stderr)
    return False


def run(topic: str, urls: list[str], generate_artifacts: bool = False) -> None:
    ping = subprocess.run(
        NLM_CMD + ["list", "--json"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=_SUBPROCESS_ENV,
    )
    if ping.returncode != 0:
        print("[error] NotebookLM auth failed. Run: notebooklm login", file=sys.stderr)
        sys.exit(1)

    notebook_title = f"{topic} — YT Research"
    print(f"Creating notebook: {notebook_title}")

    create_out = _run_nlm(["create", "--json", notebook_title])
    try:
        data = json.loads(create_out)
        nb = data.get("notebook") or {}
        notebook_id = data.get("id") or data.get("notebook_id") or nb.get("id")
    except (json.JSONDecodeError, AttributeError):
        notebook_id = _parse_notebook_id(create_out)

    if not notebook_id:
        print(f"[error] Could not parse notebook ID from: {create_out}", file=sys.stderr)
        sys.exit(1)

    print(f"Notebook ID: {notebook_id}")
    _run_nlm(["use", notebook_id])

    for url in urls:
        print(f"Adding source: {url}")
        _run_nlm(["source", "add", "--notebook", notebook_id, url])

    # Guardrail 1 — Primary-source pre-flight
    print("Running primary-source pre-flight...")
    primary_urls, src_meta = asyncio.run(collect_primary_sources(topic, urls))
    for purl in primary_urls:
        print(f"  Adding primary source: {purl}")
        _run_nlm(["source", "add", "--notebook", notebook_id, purl])
    if primary_urls:
        print(f"  {len(primary_urls)} primary source(s) added via {src_meta['strategy']}")
    else:
        print("  [warn] No primary sources found — research rests on secondary sources only",
              file=sys.stderr)

    print("Waiting for all sources to process...")
    sources_out = _run_nlm(["source", "list", "--notebook", notebook_id, "--json"])
    try:
        data = json.loads(sources_out)
        sources_list = data.get("sources", []) if isinstance(data, dict) else data
        for src in sources_list:
            src_id = src.get("id") or src.get("source_id", "")
            if src_id:
                _run_nlm(["source", "wait", "--notebook", notebook_id, "--timeout", "300", src_id])
    except (json.JSONDecodeError, TypeError):
        pass

    # Guardrails 2 & 3 — QuestionPlan with dedup and adaptive follow-ups
    print("Seeding questions from NotebookLM...")
    seed_qs = asyncio.run(seed_questions_from_nlm(notebook_id))
    plan = QuestionPlan(seed_qs, budget=15)
    print(f"Extracting analysis from NotebookLM ({len(seed_qs)} questions, budget 15)...")
    sections: list[str] = []

    while True:
        item = plan.next_question()
        if item is None:
            break
        heading, question = item
        print(f"  Asking: {heading}")
        answer = ""
        for attempt in (1, 2):
            raw = _run_nlm(["ask", "--notebook", notebook_id, "--json", question])
            try:
                answer = (json.loads(raw).get("answer") or "").strip()
            except (json.JSONDecodeError, AttributeError):
                answer = raw.strip()
            if answer:
                break
            print(f"  [retry {attempt}] empty answer for {heading}", file=sys.stderr)
        plan.record(question)
        sections.append(f"## {heading}\n\n{answer}\n")

        if answer:
            followups = asyncio.run(generate_followups(heading, question, answer))
            for fh, fq in followups:
                if plan.add_followup(fh, fq):
                    print(f"  Queued follow-up: {fh}")

    plan_stats = plan.stats()

    _slug_clean = __import__("re").sub(r"[^\w\s-]", "", topic.lower())
    slug = __import__("re").sub(r"[\s_-]+", "-", _slug_clean).strip("-")[:40]
    out_dir = VAULT / f"{date.today().isoformat()}_{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    research_path = out_dir / "research.md"
    frontmatter = (
        f"---\n"
        f"topic: {topic}\n"
        f"date: {date.today().isoformat()}\n"
        f"notebook_id: {notebook_id}\n"
        f"primary_sources_found: {src_meta['primary_sources_found']}\n"
        f"secondary_sources_added: {len(urls)}\n"
        f"questions_asked: {plan_stats['questions_asked']}\n"
        f"questions_deduped: {plan_stats['questions_deduped']}\n"
        f"followups_generated: {plan_stats['followups_generated']}\n"
        f"budget_remaining: {plan_stats['budget_remaining']}\n"
        f"sources:\n"
        + "".join(f"  - {u}\n" for u in urls)
        + "---\n\n"
    )
    content = frontmatter + f"# {topic} — YT Research\n\n" + "\n".join(sections)
    research_path.write_text(content, encoding="utf-8")
    print(f"\nResearch written: {research_path}")

    generated: list[str] = []
    if generate_artifacts:
        print("\nGenerating artifacts (one at a time)...")
        for gen_cmd, dl_cmd, ext in ARTIFACT_QUEUE:
            ok = _generate_artifact(gen_cmd, dl_cmd, ext, notebook_id, out_dir)
            if ok:
                generated.append(gen_cmd)

    print(f"\nDone.")
    print(f"Output directory: {out_dir}")
    print(f"Notebook: {notebook_title} ({notebook_id})")
    if generate_artifacts:
        print(f"Artifacts: {', '.join(generated) if generated else 'none'}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: yt_pipeline.py search <topic> [--also \"q1,q2,...\"]")
        print("       yt_pipeline.py run <topic> <url1,url2,...> [--artifacts]")
        sys.exit(1)

    mode = sys.argv[1]
    rest = list(sys.argv[2:])

    if mode == "search":
        also: list[str] = []
        if "--also" in rest:
            i = rest.index("--also")
            if i + 1 < len(rest):
                also = [s.strip() for s in rest[i + 1].split(",") if s.strip()]
            del rest[i:i + 2]
        if not rest:
            print("[error] No topic provided for search mode", file=sys.stderr)
            sys.exit(1)
        search(" ".join(rest), also)
    elif mode == "run":
        artifacts_flag = False
        if "--artifacts" in rest:
            rest.remove("--artifacts")
            artifacts_flag = True
        if len(rest) < 2:
            print("[error] Usage: run <topic> <url1,url2,...> [--artifacts]", file=sys.stderr)
            sys.exit(1)
        topic_arg = rest[0]
        urls_arg = [u for u in rest[1].split(",") if u.strip()]
        if not urls_arg:
            print("[error] No URLs provided for run mode", file=sys.stderr)
            sys.exit(1)
        run(topic_arg, urls_arg, artifacts_flag)
    else:
        print(f"[error] Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
