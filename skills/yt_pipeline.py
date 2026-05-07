"""
YT Pipeline skill helper.

Modes:
  search  <topic>              Search YouTube, print numbered URL list
  run     <topic> <url,...>    Create NLM notebook, add sources, extract analysis, write vault
"""

import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

VAULT = Path(__file__).parent.parent / "Content-Hub-Vault-V2" / "10-Research"
NLM_CMD = [sys.executable, "-m", "notebooklm"]

_SUBPROCESS_ENV = {**os.environ, "NO_COLOR": "1", "PYTHONIOENCODING": "utf-8"}

PROMPTS_FILE = Path(__file__).parent.parent / "prompts" / "yt_pipeline.md"

SECTION_PATTERN = re.compile(r"## (Q\d+ — .+)\n(.*?)(?=\n## |\Z)", re.DOTALL)

# Artifacts generated one at a time after Q&A extraction.
# Each entry: (generate subcommand, download subcommand, file extension)
ARTIFACT_QUEUE = [
    ("slide-deck", "slide-deck", "pdf"),
    ("report",     "report",     "md"),
    ("mind-map",   "mind-map",   "json"),
]


def search(topic: str) -> None:
    import yt_dlp

    opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
        "skip_download": True,
    }
    query = f"ytsearch10:{topic}"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)

    results = []
    for i, entry in enumerate(info.get("entries", []), 1):
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


def _run_nlm(args: list[str]) -> str:
    result = subprocess.run(
        NLM_CMD + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=_SUBPROCESS_ENV,
    )
    if result.returncode != 0:
        print(f"[nlm error] {result.stderr.strip()}", file=sys.stderr)
    return (result.stdout or "").strip()


def _parse_notebook_id(output: str) -> str | None:
    match = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", output)
    return match.group(0) if match else None


def _load_questions() -> list[tuple[str, str]]:
    text = PROMPTS_FILE.read_text(encoding="utf-8")
    return [(heading.strip(), question.strip()) for heading, question in SECTION_PATTERN.findall(text)]


def _generate_artifact(gen_cmd: str, dl_cmd: str, ext: str, notebook_id: str, out_dir: Path) -> bool:
    """Generate one artifact type and download it. Returns True on success."""
    print(f"Generating {gen_cmd}...")
    raw = _run_nlm([
        "generate", gen_cmd,
        "--notebook", notebook_id,
        "--wait",
        "--retry", "3",
        "--json",
    ])

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
    print(f"  Downloading {gen_cmd} → {out_path.name}")
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


def run(topic: str, urls: list[str]) -> None:
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

    print("Extracting analysis from NotebookLM...")
    questions = _load_questions()
    sections: list[str] = []
    for heading, question in questions:
        print(f"  Asking: {heading}")
        raw = _run_nlm(["ask", "--notebook", notebook_id, "--json", question])
        try:
            answer = json.loads(raw).get("answer", raw)
        except (json.JSONDecodeError, AttributeError):
            answer = raw
        sections.append(f"## {heading}\n\n{answer}\n")

    slug = topic.lower().replace(" ", "_")
    out_dir = VAULT / f"{date.today().isoformat()}_{slug}"
    out_dir.mkdir(parents=True, exist_ok=True)

    research_path = out_dir / "research.md"
    frontmatter = (
        f"---\n"
        f"topic: {topic}\n"
        f"date: {date.today().isoformat()}\n"
        f"notebook_id: {notebook_id}\n"
        f"sources:\n"
        + "".join(f"  - {u}\n" for u in urls)
        + "---\n\n"
    )
    content = frontmatter + f"# {topic} — YT Research\n\n" + "\n".join(sections)
    research_path.write_text(content, encoding="utf-8")
    print(f"\nResearch written: {research_path}")

    print("\nGenerating artifacts (one at a time)...")
    generated = []
    for gen_cmd, dl_cmd, ext in ARTIFACT_QUEUE:
        ok = _generate_artifact(gen_cmd, dl_cmd, ext, notebook_id, out_dir)
        if ok:
            generated.append(gen_cmd)

    print(f"\nDone.")
    print(f"Output directory: {out_dir}")
    print(f"Notebook: {notebook_title} ({notebook_id})")
    print(f"Artifacts: {', '.join(generated) if generated else 'none'}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: yt_pipeline.py search <topic>")
        print("       yt_pipeline.py run <topic> <url1,url2,...>")
        sys.exit(1)

    mode = sys.argv[1]
    if mode == "search":
        search(" ".join(sys.argv[2:]))
    elif mode == "run":
        topic_arg = sys.argv[2]
        urls_arg = sys.argv[3].split(",") if len(sys.argv) > 3 else []
        if not urls_arg:
            print("[error] No URLs provided for run mode", file=sys.stderr)
            sys.exit(1)
        run(topic_arg, urls_arg)
    else:
        print(f"[error] Unknown mode: {mode}", file=sys.stderr)
        sys.exit(1)
