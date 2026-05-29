"""Per-skill subprocess wrappers + output resolvers.

Each run_* function:
  1. Builds the argv list from request body fields.
  2. Calls launch_job(), which spawns the subprocess and streams stdout/stderr
     into the job's asyncio.Queue.
  3. On exit-0, calls the stage-specific resolver to produce a typed JobResult.
  4. Returns the job_id immediately (non-blocking).

Resolvers parse known stdout markers first; deterministic-slug fallbacks are
used only when parsing fails. No skill files are modified (§3 Surgical Changes).
"""

import asyncio
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Callable

PROJECT_ROOT = Path(__file__).parent.parent.parent
VAULT_ROOT = PROJECT_ROOT / "Content-Hub-Vault-V2"

# jobs module lives in the same directory
sys.path.insert(0, str(Path(__file__).parent))
from jobs import create_job, complete_job, fail_job, JobResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _match(pattern: str, text: str) -> str | None:
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else None


def _bundle_result(output_dir: str) -> JobResult:
    dir_path = Path(output_dir)
    members = sorted([str(p) for p in dir_path.glob("*.md")]) if dir_path.exists() else []
    primary = (
        str(dir_path / "README.md")
        if (dir_path / "README.md").exists()
        else (members[0] if members else output_dir)
    )
    return JobResult(result_type="bundle", primary_path=primary, outputs=members or [output_dir])


# ---------------------------------------------------------------------------
# Stage output resolvers
# ---------------------------------------------------------------------------

def resolve_researcher(stdout: str, niche: str) -> JobResult:
    path = _match(r"Brief written to:\s*(.+\.md)", stdout)
    if not path:
        slug = re.sub(r"[^a-z0-9]+", "-", niche.lower()).strip("-")
        path = str(VAULT_ROOT / "10-Research" / f"{date.today().isoformat()}_{slug}_brief.md")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


def resolve_ideation(stdout: str, topic: str) -> JobResult:
    path = _match(r"Output:\s*(.+\.md)", stdout)
    if not path:
        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40]
        path = str(VAULT_ROOT / "02-Ideas" / f"{date.today().isoformat()}_{slug}.md")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


def resolve_hook(stdout: str, topic: str) -> JobResult:
    path = _match(r"Hooks written to:\s*(.+\.md)", stdout)
    if not path:
        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40]
        path = str(VAULT_ROOT / "05-Hooks" / f"{date.today().isoformat()}_{slug}.md")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


def resolve_outline(stdout: str, topic: str) -> JobResult:
    path = _match(r"Outline written to:\s*(.+\.md)", stdout)
    if not path:
        slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40]
        path = str(VAULT_ROOT / "06-Outlines" / f"{date.today().isoformat()}_{slug}.md")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


def resolve_title(stdout: str, concept: str) -> JobResult:
    # title.py prints just the path as its only stdout line
    lines = [l.strip() for l in stdout.splitlines() if l.strip().endswith(".md")]
    path = lines[-1] if lines else None
    if not path:
        slug = re.sub(r"[^a-z0-9]+", "-", concept.lower()).strip("-")[:50]
        path = str(VAULT_ROOT / "07-Titles" / f"{date.today().isoformat()}_{slug}.md")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


def resolve_cascade(stdout: str, title: str) -> JobResult:
    # "✅ Distribution package written to:\n   <dir>"
    m = re.search(r"Distribution package written to:\s*\n\s*(.+)", stdout)
    output_dir = m.group(1).strip() if m else None
    if not output_dir:
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
        output_dir = str(VAULT_ROOT / "08-Distribution" / f"{date.today().isoformat()}_{slug}")
    return _bundle_result(output_dir)


def resolve_short_form(stdout: str, title: str) -> JobResult:
    # "✅ Short-form package written to:\n   <dir>"
    m = re.search(r"Short-form package written to:\s*\n\s*(.+)", stdout)
    output_dir = m.group(1).strip() if m else None
    if not output_dir:
        slug = re.sub(r"[^\w\s-]", "", title.lower())
        slug = re.sub(r"[\s_-]+", "-", slug).strip("-")[:40]
        output_dir = str(VAULT_ROOT / "09-Shorts" / f"{date.today().isoformat()}_{slug}")
    return _bundle_result(output_dir)


def resolve_voice_cleanup(stdout: str, file_path: str, inplace: bool) -> JobResult:
    if inplace:
        return JobResult(result_type="file", primary_path=file_path, outputs=[file_path])
    path = _match(r"Output:\s*(.+\.md)", stdout)
    if not path:
        p = Path(file_path)
        path = str(p.parent / f"{p.stem}_cleaned{p.suffix}")
    return JobResult(result_type="file", primary_path=path, outputs=[path])


# ---------------------------------------------------------------------------
# Job launcher
# ---------------------------------------------------------------------------

async def launch_job(stage: str, args: list[str], resolver: Callable[[str], JobResult]) -> str:
    job = create_job(stage)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONPATH": str(PROJECT_ROOT)}

    async def _run() -> None:
        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(PROJECT_ROOT),
                env=env,
            )

            stdout_lines: list[str] = []
            stderr_lines: list[str] = []

            async def _drain(stream: asyncio.StreamReader, lines: list[str], is_err: bool) -> None:
                async for raw in stream:
                    text = raw.decode("utf-8", errors="replace").rstrip()
                    lines.append(text)
                    job.stdout_lines.append(text) if not is_err else job.stderr_lines.append(text)
                    job.queue.put_nowait({"type": "stderr" if is_err else "stdout", "line": text})

            await asyncio.gather(
                _drain(proc.stdout, stdout_lines, False),
                _drain(proc.stderr, stderr_lines, True),
            )
            await proc.wait()

            if proc.returncode == 0:
                result = resolver("\n".join(stdout_lines))
                complete_job(job.job_id, result)
            else:
                fail_job(job.job_id, "\n".join(stderr_lines[-30:]))
        except Exception as exc:
            fail_job(job.job_id, str(exc))

    asyncio.create_task(_run())
    return job.job_id


# ---------------------------------------------------------------------------
# Per-skill wrappers
# ---------------------------------------------------------------------------

async def run_researcher(niche: str, repos: list[str], mode: str = "deep") -> str:
    args = [sys.executable, "-m", "skills.researcher", "--niche", niche, "--mode", mode]
    if repos:
        args += ["--repos", *repos]
    return await launch_job("researcher", args, lambda out: resolve_researcher(out, niche))


async def run_ideation(topic: str, research_file: str = "", no_trends: bool = False) -> str:
    args = [sys.executable, "-m", "skills.ideation", "--topic", topic]
    if research_file:
        args += ["--research-file", research_file]
    if no_trends:
        args.append("--no-trends")
    return await launch_job("ideation", args, lambda out: resolve_ideation(out, topic))


async def run_hook(
    topic: str,
    platform: str = "yt-long",
    audience: str = "",
    format_type: str = "medium",
    research_file: str = "",
    no_polish: bool = False,
) -> str:
    args = [sys.executable, "-m", "skills.hook", topic, "--platform", platform, "--format", format_type]
    if audience:
        args += ["--audience", audience]
    if research_file:
        args += ["--research-file", research_file]
    if no_polish:
        args.append("--no-polish")
    return await launch_job("hook", args, lambda out: resolve_hook(out, topic))


async def run_outline(
    topic: str,
    hook_path: str = "",
    length: int = 8,
    platform: str = "yt-long",
    no_polish: bool = False,
) -> str:
    args = [sys.executable, "-m", "skills.outline", topic, "--length", str(length), "--platform", platform]
    if hook_path:
        args += ["--hook-path", hook_path]
    if no_polish:
        args.append("--no-polish")
    return await launch_job("outline", args, lambda out: resolve_outline(out, topic))


async def run_title(concept: str) -> str:
    args = [sys.executable, "-m", "skills.title", concept]
    return await launch_job("title", args, lambda out: resolve_title(out, concept))


async def run_cascade(
    research_file: str = "",
    outline_file: str = "",
    title: str = "",
    youtube_url: str = "",
) -> str:
    args = [sys.executable, "-m", "skills.cascade"]
    if youtube_url:
        args.append(youtube_url)
    if research_file:
        args += ["--research-file", research_file]
    if outline_file:
        args += ["--outline-file", outline_file]
    if title:
        args += ["--title", title]
    label = title or youtube_url or research_file or "cascade"
    return await launch_job("cascade", args, lambda out: resolve_cascade(out, label))


async def run_short_form(
    research_file: str = "",
    outline_file: str = "",
    title: str = "",
    youtube_url: str = "",
) -> str:
    args = [sys.executable, "-m", "skills.short_form"]
    if youtube_url:
        args.append(youtube_url)
    if research_file:
        args += ["--research-file", research_file]
    if outline_file:
        args += ["--outline-file", outline_file]
    if title:
        args += ["--title", title]
    label = title or youtube_url or research_file or "short-form"
    return await launch_job("short_form", args, lambda out: resolve_short_form(out, label))


async def run_voice_cleanup(file_path: str, inplace: bool = False) -> str:
    args = [sys.executable, "-m", "skills.voice_cleanup", file_path]
    if inplace:
        args.append("--inplace")
    return await launch_job(
        "voice_cleanup", args,
        lambda out: resolve_voice_cleanup(out, file_path, inplace),
    )
