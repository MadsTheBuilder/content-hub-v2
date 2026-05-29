"""
Standalone pipeline runner — orchestrates the 9-step content production workflow.

New order (v2.1):
1. Research (yt_pipeline.py) → 10-Research/{slug}/
2. Studio reports → 11-Reports/{slug}/ (+ voice-cleanup)
3. Ideation → 02-Ideas/{slug}/ (+ voice-cleanup)
4. Hook → 05-Hooks/{slug}/ (+ voice-cleanup)
5. Outline → 06-Outlines/{slug}/ (+ voice-cleanup)
6. Title → 07-Titles/{slug}/ (+ voice-cleanup)
7. Short-form → 09-Shorts/{slug}/ (+ voice-cleanup per script)
8. Cascade → 08-Distribution/{slug}/ (+ voice-cleanup per channel)
9. Studio slides + video (from cascade) → 12-Slides/{slug}/ + 13-Video/{slug}/

Usage:
    python skills/pipeline.py "<topic>" "<url1,url2,...>"
"""

import asyncio
import os
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
VAULT = PROJECT_ROOT / "Content-Hub-Vault-V2"
SKILLS = PROJECT_ROOT / "skills"
PIPELINE_RESULTS_TSV = VAULT / "00-Management-V2" / "pipeline_results.tsv"

from skills import studio

# Ensure all subprocess skill scripts can import from project root
_existing = os.environ.get("PYTHONPATH", "")
_SUBPROCESS_ENV = {
    **os.environ,
    "PYTHONPATH": f"{PROJECT_ROOT}{os.pathsep}{_existing}" if _existing else str(PROJECT_ROOT),
    "PYTHONIOENCODING": "utf-8",
}


def log_result(
    run_id: str,
    skill: str,
    metric_name: str,
    metric_value,
    model: str = "claude-sonnet-4-6",
    kept: str = "YES",
    prompt_sha: str = "none",
    brief_sha: str = "none",
) -> None:
    """
    Log a single metric result to pipeline_results.tsv.

    Appends one row in tidy-data format (long-skinny):
    run_id | timestamp_iso | skill | metric_name | metric_value | model | kept | prompt_sha | brief_sha

    Args:
        run_id: Unique identifier for this pipeline run (e.g., "run-2026-05-28-001")
        skill: Skill name (researcher, ideation, hook, outline, title, cascade, short_form, voice_cleanup)
        metric_name: Name of the metric (e.g., "scroll_stop_score", "composite_judge_score", "banned_phrase_count")
        metric_value: The numeric value (float or int)
        model: LLM used (default: claude-sonnet-4-6)
        kept: "YES" if this variant was kept, "NO" if reverted (default: YES)
        prompt_sha: SHA256 of prompts/<skill>.md at time of run (default: "none")
        brief_sha: SHA256 of brief.md at time of run (default: "none")
    """
    # Ensure the TSV file exists with a header
    if not PIPELINE_RESULTS_TSV.exists():
        PIPELINE_RESULTS_TSV.parent.mkdir(parents=True, exist_ok=True)
        header = "run_id\ttimestamp_iso\tskill\tmetric_name\tmetric_value\tmodel\tkept\tprompt_sha\tbrief_sha\n"
        PIPELINE_RESULTS_TSV.write_text(header, encoding="utf-8")

    # Get current ISO timestamp
    timestamp_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Construct the row
    row = f"{run_id}\t{timestamp_iso}\t{skill}\t{metric_name}\t{metric_value}\t{model}\t{kept}\t{prompt_sha}\t{brief_sha}\n"

    # Append to TSV
    with open(PIPELINE_RESULTS_TSV, "a", encoding="utf-8") as f:
        f.write(row)


def _slug(topic: str) -> str:
    import re
    slug = re.sub(r"[^\w\s-]", "", topic.lower())
    return re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]


def step(label: str, cmd: list[str]) -> int:
    print(f"\n{'='*60}", flush=True)
    print(f"[pipeline] {label}", flush=True)
    print(f"{'='*60}", flush=True)
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, env=_SUBPROCESS_ENV)
    if result.returncode != 0:
        print(f"[pipeline] FAILED: {label} (exit {result.returncode})", file=sys.stderr, flush=True)
    return result.returncode


def run_voice_cleanup(md_file_path: str) -> int:
    """Run voice-cleanup --inplace on a markdown file. Returns 0 on success."""
    cmd = [sys.executable, str(SKILLS / "voice_cleanup.py"), md_file_path, "--inplace"]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, env=_SUBPROCESS_ENV, capture_output=True)
    if result.returncode != 0:
        print(f"[pipeline] WARNING: voice-cleanup failed for {md_file_path}", file=sys.stderr, flush=True)
    return result.returncode


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("topic")
    parser.add_argument("urls")
    parser.add_argument("--start-step", type=int, default=1, metavar="N", help="Resume from step N (1-9)")
    parser.add_argument("--date", default=None, help="Override run date (YYYY-MM-DD); defaults to today")
    parser.add_argument("--research-file", default=None, help="Explicit path to research.md (overrides date-based lookup)")
    args = parser.parse_args()

    topic = args.topic
    urls = ",".join(u.strip() for u in args.urls.split(",") if u.strip())
    today = args.date or date.today().isoformat()
    start_step = args.start_step
    slug = _slug(topic)

    print(f"\n[pipeline] Topic: {topic}", flush=True)
    print(f"[pipeline] URLs:  {urls}", flush=True)
    print(f"[pipeline] Slug:  {today}_{slug}", flush=True)

    # Step 1 — Research (yt_pipeline.py)
    if start_step <= 1:
        rc = step("1/9 — Research", [sys.executable, str(SKILLS / "yt_pipeline.py"), "run", topic, urls])
        if rc != 0:
            print("[pipeline] Aborting — research step failed.", file=sys.stderr)
            sys.exit(rc)
    else:
        print(f"\n[pipeline] Skipping step 1 (--start-step {start_step})")

    research_dir = VAULT / "10-Research" / f"{today}_{slug}"
    research_file = Path(args.research_file) if args.research_file else research_dir / "research.md"

    if not research_file.exists():
        print(f"[pipeline] Warning: expected research file not found at {research_file}", file=sys.stderr)
    else:
        print(f"[pipeline] Research file: {research_file}")

    # Always extract notebook_id (needed for step 9 regardless of start_step)
    notebook_id = None
    if research_file.exists():
        content = research_file.read_text(encoding="utf-8")
        fm_end = content.find("---", 3)
        if fm_end > 3:
            for line in content[3:fm_end].split("\n"):
                if line.startswith("notebook_id:"):
                    notebook_id = line.split(":", 1)[1].strip()
                    break

    # Step 2 — Studio reports (generate_reports)
    if start_step <= 2:
        print("\n[pipeline] Step 2/9 — Studio reports")
        if notebook_id:
            print(f"[pipeline] Found notebook_id: {notebook_id}")
            try:
                asyncio.run(studio.generate_reports(notebook_id, slug))
                reports_dir = VAULT / "11-Reports" / slug
                if reports_dir.exists():
                    for md_file in reports_dir.glob("*.md"):
                        run_voice_cleanup(str(md_file))
            except Exception as e:
                print(f"[pipeline] WARNING: studio.generate_reports() failed: {e}", file=sys.stderr)
        else:
            print("[pipeline] WARNING: notebook_id not found in research.md — skipping studio reports")
    else:
        print(f"\n[pipeline] Skipping step 2 (--start-step {start_step})")
        if notebook_id:
            print(f"[pipeline] Found notebook_id: {notebook_id}")

    ideation_file = VAULT / "02-Ideas" / f"{today}_{slug}.md"
    hook_file = VAULT / "05-Hooks" / f"{today}_{slug}.md"
    outline_file = VAULT / "06-Outlines" / f"{today}_{slug}.md"
    title_file = VAULT / "07-Titles" / f"{today}_{slug}.md"

    # Step 3 — Ideation
    if start_step <= 3:
        ideation_cmd = [sys.executable, str(SKILLS / "ideation.py"), "--topic", topic]
        if research_file.exists():
            ideation_cmd += ["--research-file", str(research_file)]
        rc = step("3/9 — Ideation", ideation_cmd)
        if rc == 0 and ideation_file.exists():
            run_voice_cleanup(str(ideation_file))

    # Step 4 — Hook
    if start_step <= 4:
        hook_cmd = [sys.executable, str(SKILLS / "hook.py"), topic]
        if research_file.exists():
            hook_cmd += ["--research-file", str(research_file)]
        rc = step("4/9 — Hook", hook_cmd)
        if rc == 0 and hook_file.exists():
            run_voice_cleanup(str(hook_file))

    # Step 5 — Outline
    if start_step <= 5:
        outline_cmd = [sys.executable, str(SKILLS / "outline.py"), topic]
        if hook_file.exists():
            outline_cmd += ["--hook-path", str(hook_file)]
        rc = step("5/9 — Outline", outline_cmd)
        if rc == 0 and outline_file.exists():
            run_voice_cleanup(str(outline_file))

    # Step 6 — Title
    if start_step <= 6:
        title_cmd = [sys.executable, str(SKILLS / "title.py"), topic]
        if outline_file.exists():
            title_cmd += ["--outline-path", str(outline_file)]
        rc = step("6/9 — Title", title_cmd)
        if rc == 0 and title_file.exists():
            run_voice_cleanup(str(title_file))

    # Step 7 — Short-form
    if start_step <= 7:
        short_cmd = [sys.executable, str(SKILLS / "short_form.py"), "--title", topic]
        if research_file.exists():
            short_cmd += ["--research-file", str(research_file)]
        if outline_file.exists():
            short_cmd += ["--outline-file", str(outline_file)]
        rc = step("7/9 — Short-form", short_cmd)
        if rc == 0:
            shorts_dir = VAULT / "09-Shorts" / f"{today}_{slug}"
            if shorts_dir.exists():
                for md_file in shorts_dir.glob("*.md"):
                    run_voice_cleanup(str(md_file))

    # Step 8 — Cascade
    if start_step <= 8:
        cascade_cmd = [sys.executable, str(SKILLS / "cascade.py"), "--title", topic]
        if research_file.exists():
            cascade_cmd += ["--research-file", str(research_file)]
        if outline_file.exists():
            cascade_cmd += ["--outline-file", str(outline_file)]
        rc = step("8/9 — Cascade", cascade_cmd)
        if rc == 0:
            cascade_dir = VAULT / "08-Distribution" / f"{today}_{slug}"
            if cascade_dir.exists():
                for md_file in cascade_dir.glob("*.md"):
                    run_voice_cleanup(str(md_file))

    # Step 9 — Studio slides + video (from cascade sources)
    print("\n[pipeline] Step 9/9 — Studio slides + video")
    if notebook_id:
        cascade_dir = VAULT / "08-Distribution" / f"{today}_{slug}"
        if cascade_dir.exists():
            print(f"[pipeline] Found cascade_dir: {cascade_dir}")
            try:
                asyncio.run(studio.inject_cascade_and_generate(str(cascade_dir), notebook_id, slug))
            except Exception as e:
                print(f"[pipeline] WARNING: studio.inject_cascade_and_generate() failed: {e}", file=sys.stderr)
        else:
            print(f"[pipeline] WARNING: cascade directory not found at {cascade_dir}", file=sys.stderr)
    else:
        print("[pipeline] WARNING: notebook_id not available — skipping studio slides/video")

    print(f"\n{'='*60}", flush=True)
    print(f"[pipeline] Pipeline complete — {today}_{slug}", flush=True)
    print(f"[pipeline] Vault: {VAULT}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()
