"""Researcher — Content gap discovery via NotebookLM.

Pipeline (one isolated notebook per repo):
  1. Read trend URLs from Content-Hub-Vault-V2/04-Trends/github_trending.md
  2. For each URL: create a notebook, add that repo as the sole source,
     run web research, verify sources via Claude, query for content gaps
  3. Compile all findings into one brief →
     Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche>_brief.md

Usage:
  python -m skills.researcher --list
  python -m skills.researcher --niche "AI agents" --repos owner/repo1 owner/repo2
  python -m skills.researcher --niche "AI agents" --repos owner/repo1 --mode deep
"""

import asyncio
import argparse
import json
import logging
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKLM_SRC = PROJECT_ROOT / "notebooklm-py" / "src"
if str(NOTEBOOKLM_SRC) not in sys.path:
    sys.path.insert(0, str(NOTEBOOKLM_SRC))

import httpx
from notebooklm import ChatGoal, NotebookLMClient
from skills.researcher_crawler import discover_primary_docs
from skills.helpers.nlm_seed import seed_questions_from_nlm
from skills.helpers.open_notebook_seed import seed_questions_from_readme
from skills.open_notebook_client import OpenNotebookClient
from skills.research_plan import QuestionPlan, generate_followups
from skills.brief_loader import load_brief, apply_cli_overrides
from skills.brief_args import add_brief_args
from dataclasses import dataclass

logger = logging.getLogger(__name__)


def claude_cli(prompt: str, timeout: int = 120) -> str:
    """Call `claude -p <prompt>` and return stdout. Raises RuntimeError on failure."""
    cmd = shutil.which("claude")
    if cmd is None:
        raise RuntimeError("claude CLI not found in PATH — ensure Claude Code is installed")
    result = subprocess.run(
        [cmd, "-p", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed (exit {result.returncode}): {result.stderr[:200]}")
    return result.stdout.strip()


def _parse_json_output(text: str) -> dict:
    """Strip markdown fences and parse JSON from Claude CLI output."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        end = len(lines)
        for i in range(1, len(lines)):
            if lines[i].strip() == "```":
                end = i
                break
        text = "\n".join(lines[1:end])
    return json.loads(text)


@dataclass
class RepoContext:
    """Structured context extracted from primary docs."""
    core_use_cases: list[str]
    key_concepts: list[str]
    common_patterns: list[str]
    anti_patterns: list[str]
    audience: str

    def to_markdown(self) -> str:
        """Render RepoContext to a markdown block."""
        return (
            f"## Repo Context\n\n"
            f"**Core Use Cases:**\n"
            + "\n".join(f"- {uc}" for uc in self.core_use_cases) + "\n\n"
            f"**Key Concepts:**\n"
            + "\n".join(f"- {kc}" for kc in self.key_concepts) + "\n\n"
            f"**Common Patterns:**\n"
            + "\n".join(f"- {cp}" for cp in self.common_patterns) + "\n\n"
            f"**Anti-Patterns & Pitfalls:**\n"
            + "\n".join(f"- {ap}" for ap in self.anti_patterns) + "\n\n"
            f"**Intended Audience:**\n{self.audience}\n\n"
        )

TRENDS_FILE = PROJECT_ROOT / "Content-Hub-Vault-V2" / "04-Trends" / "github_trending.md"
RESEARCH_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "10-Research"
OBSERVATION_DIR = PROJECT_ROOT / "Content-Hub-Vault-V2" / "source-verification" / "observation"


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



async def synthesize_brief(
    owner_repo: str,
    repo_context: RepoContext,
    raw_qa: list[dict],
    angle_raw: list[dict] | None = None,
) -> str:
    """Synthesize raw Q&A into a readable 5-section brief via Haiku (or Sonnet if needed).

    Args:
        owner_repo: "owner/repo" for context
        repo_context: Extracted RepoContext
        raw_qa: List of {"heading", "answer"} dicts from research questions
        angle_raw: List of {"heading", "answer"} dicts from angle battery

    Returns:
        String containing the 5-section markdown brief:
        ## What it does
        ## Who it's for
        ## How it works
        ## When to use
        ## Watch out for
    """
    qa_text = "\n\n".join(f"**{qa['heading']}:**\n{qa['answer']}" for qa in raw_qa)
    angle_text = "\n\n".join(f"**{qa['heading']}:**\n{qa['answer']}" for qa in angle_raw)
    context_text = (
        f"Use cases: {', '.join(repo_context.core_use_cases)}\n"
        f"Key concepts: {', '.join(repo_context.key_concepts)}\n"
        f"Patterns: {', '.join(repo_context.common_patterns)}\n"
        f"Pitfalls: {', '.join(repo_context.anti_patterns)}\n"
        f"Audience: {repo_context.audience}"
    )
    prompt = (
        f"You are synthesizing research findings on the GitHub project '{owner_repo}' "
        f"into a readable research brief.\n\n"
        f"**Extracted Repo Context:**\n{context_text}\n\n"
        f"**Research Findings (Q&A):**\n{qa_text}\n\n"
        f"**Content Angle Battery:**\n{angle_text}\n\n"
        f"Create a concise, prose-only brief with exactly 5 sections. "
        f"NO bullet points, NO question headers. Each section 2-4 short paragraphs.\n\n"
        f"## What it does\n[Prose about what this project/tool does]\n\n"
        f"## Who it's for\n[Prose about the intended audience]\n\n"
        f"## How it works\n[Prose about key concepts and how it functions]\n\n"
        f"## When to use\n[Prose about use cases and when to apply it]\n\n"
        f"## Watch out for\n[Prose about pitfalls, limitations, and anti-patterns]\n\n"
        f"Start with '## What it does' and end with '## Watch out for'."
    )
    return claude_cli(prompt, timeout=120)



def list_available_repos() -> list[str]:
    """Print repos from the trending file and return their slugs."""
    if not TRENDS_FILE.exists():
        print(f"Trends file not found: {TRENDS_FILE}")
        return []
    text = TRENDS_FILE.read_text(encoding="utf-8")
    urls = extract_urls(text)
    slugs = [f"{u.split('/')[-2]}/{u.split('/')[-1]}" for u in urls]
    print(f"Available repos in {TRENDS_FILE.name} ({len(slugs)} total):\n")
    for i, slug in enumerate(slugs, 1):
        print(f"  {i:2}. {slug}")
    print(f'\nUse --repos to pick: --repos owner/repo1 owner/repo2')
    return slugs


async def research_one(client: "NotebookLMClient", url: str, mode: str) -> dict:
    """Run a fully isolated research pipeline for a single repo URL.

    Returns a dict with keys: url, notebook_id, finding (str), sources_found (list),
    angle_battery (list[str]), primary_sources_found (int).
    """
    slug = repo_slug(url)
    title = f"Research: {slug} — {date.today().isoformat()}"

    print(f"\n[{slug}] Creating notebook...")
    nb = await client.notebooks.create(title)
    logger.info("[%s] Notebook: %s", slug, nb.id)

    await client.sources.add_url(nb.id, url, wait=True)

    # Guardrail 1 — Primary-source pre-flight: add raw README as a primary source
    owner_repo = "/".join(url.rstrip("/").split("/")[-2:])
    primary_count = 0
    for branch in ("main", "master"):
        readme_url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/README.md"
        try:
            await client.sources.add_url(nb.id, readme_url, wait=False)
            primary_count += 1
            print(f"[{slug}] Added primary source: README ({branch})")
            break
        except Exception:
            continue

    # Discover additional primary docs (docs/, examples/, etc.)
    try:
        doc_candidates = await discover_primary_docs(owner_repo, max_docs=6)
        for doc in doc_candidates:
            try:
                await client.sources.add_url(nb.id, doc.raw_url, wait=False)
                primary_count += 1
                print(f"[{slug}] Added primary source: {doc.path}")
            except Exception as e:
                logger.warning("[%s] Failed to add primary doc %s: %s", slug, doc.path, e)
        if doc_candidates:
            print(f"[{slug}] Discovered {len(doc_candidates)} additional primary docs")
    except Exception as e:
        logger.warning("[%s] Doc crawler failed: %s", slug, e)

    print(f"[{slug}] Sources indexed. Starting web research ({mode} mode)...")

    repo_name = url.rstrip("/").split("/")[-1].replace("-", " ")
    research_query = f"{repo_name} GitHub {owner_repo} software project"
    research = await client.research.start(nb.id, research_query, source="web", mode=mode)
    task_id = research.task_id if research else None

    max_polls = 24 if mode == "deep" else 12
    poll_interval = 15 if mode == "deep" else 10
    sources_found: list = []

    for i in range(max_polls):
        await asyncio.sleep(poll_interval)
        status = await client.research.poll(nb.id)
        state = status.status
        print(f"[{slug}] Research [{i + 1}/{max_polls}]: {state}")
        if state == "completed":
            sources_found = list(status.sources)
            if sources_found and sources_found[0].research_task_id:
                task_id = sources_found[0].research_task_id
            else:
                task_id = status.task_id or task_id
            print(f"[{slug}] Discovered {len(sources_found)} related sources")
            break

    imported_source_ids: list[str] = []
    if mode == "deep" and sources_found and task_id:
        repo_short = url.rstrip("/").split("/")[-1].lower()
        owner_lower = owner_repo.split("/")[0].lower()
        name_tokens = [t for t in re.split(r"[-_]", repo_short) if len(t) > 2]
        def _plausibly_relevant(src) -> bool:
            haystack = f"{src.title} {src.url}".lower()
            return (
                repo_short in haystack
                or owner_lower in haystack
                or sum(1 for t in name_tokens if t in haystack) >= max(1, len(name_tokens) - 1)
            )
        relevant_sources = [s for s in sources_found if _plausibly_relevant(s)]
        dropped_count = len(sources_found) - len(relevant_sources)
        if dropped_count:
            print(f"[{slug}] Pre-filter dropped {dropped_count} off-topic discovered source(s) before import")
        import_count = min(len(relevant_sources), 10)
        if import_count:
            imported = await client.research.import_sources(nb.id, task_id, relevant_sources[:import_count])
            imported_source_ids = [s["id"] for s in imported if s.get("id")]
            print(f"[{slug}] Imported {import_count} sources")
        else:
            print(f"[{slug}] No discovered sources passed relevance pre-filter — skipping import")
    elif sources_found:
        print(f"[{slug}] Fast mode — skipping import of {len(sources_found)} discovered sources")

    # Poll until all sources are ready — max 3 minutes
    for _ in range(18):  # 18 × 10s = 3 min
        current_sources = await client.sources.list(nb.id)
        pending = [s for s in current_sources if not s.is_ready and not s.is_error]
        if not pending:
            break
        print(f"[{slug}] Indexing: {len(pending)} source(s) still processing...")
        await asyncio.sleep(10)

    # Verify discovered sources semantically — keep only those relevant to this repo
    all_sources = await client.sources.list(nb.id)
    imported_id_set = set(imported_source_ids)
    primary_ids = [s.id for s in all_sources if s.id not in imported_id_set]
    discovered_sources = [s for s in all_sources if s.id in imported_id_set]

    verified_source_ids: list[str] = list(primary_ids)
    observation_log: list[str] = ["## Verification Decisions\n\n"]
    if discovered_sources:
        guides: list[dict] = []
        skipped_ids: list[str] = []
        for src in discovered_sources:
            try:
                guide = await client.sources.get_guide(nb.id, src.id)
                summary = guide.summary.strip()
                if not summary:
                    logger.warning("[%s] Source %s has no/empty guide summary — treating as unknown, keeping", slug, src.id)
                guides.append({
                    "id": src.id,
                    "title": src.title or "Untitled",
                    "summary": summary,
                    "keywords": list(guide.keywords)[:5],
                })
            except Exception as e:
                logger.warning("[%s] Failed to fetch guide for source %s: %s — keeping (benefit of the doubt)", slug, src.id, e)
                skipped_ids.append(src.id)

        # Note: skipped_ids are kept by default (couldn't fetch guide, so assume relevant)
        verified_source_ids.extend(skipped_ids)

        if guides:
            try:
                guide_text = "\n\n".join(
                    f"ID: {g['id']}\nTitle: {g['title']}\nSummary: {g['summary']}\nKeywords: {', '.join(str(k) for k in g['keywords'])}"
                    for g in guides
                )
                prompt = (
                    f"We are researching the GitHub project '{owner_repo}' ({url}).\n\n"
                    f"Below are AI-generated summaries of web sources in a research notebook.\n"
                    f"Keep a source if it is about this specific project, the same technology or "
                    f"problem space, or evaluates/contextualizes this repo.\n"
                    f"Drop a source if it is about a different entity that shares part of the name.\n\n"
                    f"CRITICAL: Watch out for wrong-entity matches. Example:\n"
                    f"  - Project: 'mercury-agent' (a multi-agent system)\n"
                    f"  - Wrong match: 'mercury chemistry' (the chemical element) — DROP THIS\n"
                    f"  - Correct match: 'Mercury messenger' (related service) — KEEP IF RELEVANT\n\n"
                    f"{guide_text}\n\n"
                    f"Return ONLY a JSON object (no markdown, no code fences):\n"
                    f'{{"ids": ["source_id_to_keep"], "reasons": {{"dropped_id": "reason for dropping"}}}}\n'
                    f"Include in 'ids' all source IDs to keep. "
                    f"Include in 'reasons' a brief reason for each dropped source."
                )
                raw = claude_cli(prompt, timeout=60)
                result_json = _parse_json_output(raw)
                kept_ids = set(result_json.get("ids", []))
                reasons_dict = result_json.get("reasons", {})
                dropped = [g for g in guides if g["id"] not in kept_ids]
                if dropped:
                    for g in dropped:
                        reason = reasons_dict.get(g["id"], "no reason given")
                        logger.warning("[%s] Verification dropped %s (%s): %s", slug, g["id"], g["title"], reason)
                    drop_titles = ", ".join(g["title"] for g in dropped)
                    print(f"[{slug}] Verification dropped {len(dropped)}: {drop_titles}")
                verified_source_ids.extend(kept_ids)
                print(f"[{slug}] Verified: {len(verified_source_ids)} sources ({len(primary_ids)} primary + {len(kept_ids)} discovered)")
                kept_guides = [g for g in guides if g["id"] in kept_ids]
                observation_log.append(f"### Kept — {len(kept_guides)} discovered source(s)\n")
                for g in kept_guides:
                    observation_log.append(f"- {g['title']}\n")
                observation_log.append(f"\n### Dropped — {len(dropped)}\n")
                for g in dropped:
                    reason = reasons_dict.get(g["id"], "no reason given")
                    observation_log.append(f"- {g['title']} — {reason}\n")
                if skipped_ids:
                    observation_log.append(f"\n### Auto-kept (guide unavailable, benefit of the doubt) — {len(skipped_ids)}\n")
            except Exception as e:
                logger.warning("[%s] Source verification call failed: %s — keeping all %d discovered sources", slug, e, len(guides))
                verified_source_ids.extend(g["id"] for g in guides)

        if len(verified_source_ids) == len(primary_ids) and discovered_sources:
            print(f"[{slug}] Verification: all discovered sources dropped — using primary sources only")

    repo_context = RepoContext([], [], [], [], "")

    # Save observation to vault
    try:
        OBSERVATION_DIR.mkdir(parents=True, exist_ok=True)
        obs_slug = owner_repo.replace("/", "-")
        obs_file = OBSERVATION_DIR / f"{date.today().isoformat()}_{obs_slug}_observation.md"
        obs_content = (
            f"---\ndate: {date.today().isoformat()}\nrepo: {owner_repo}\n---\n\n"
            f"# Source Verification Observation: {owner_repo}\n\n"
            + "".join(observation_log)
            + "\n\n"
            + repo_context.to_markdown()
        )
        obs_file.write_text(obs_content, encoding="utf-8")
        print(f"[{slug}] Observation saved → {obs_file.name}")
    except Exception as e:
        logger.warning("[%s] Failed to save observation: %s", slug, e)

    # Anchor the chat context to this specific repo before asking any questions
    repo_context_md = repo_context.to_markdown()
    await client.chat.configure(
        nb.id,
        goal=ChatGoal.CUSTOM,
        custom_prompt=(
            f"{repo_context_md}\n\n"
            f"You are a technical researcher analysing the GitHub project '{owner_repo}' "
            f"(URL: {url}). Answer every question strictly in the context of this software project. "
            f"If a source appears unrelated (wrong company, person, or topic sharing a similar name), "
            f"ignore it and state that the source was irrelevant."
        ),
    )

    print(f"[{slug}] Seeding questions from NotebookLM...")
    seed_qs = await seed_questions_from_nlm(nb.id)
    plan = QuestionPlan(seed_qs, budget=15)
    print(f"[{slug}] Querying for content gaps ({len(seed_qs)} initial questions, budget 15)...")
    finding_parts: list[str] = []
    raw_qa: list[dict] = []  # For Phase 4 synthesis

    while True:
        item = plan.next_question()
        if item is None:
            break
        heading, question = item
        try:
            result = await client.chat.ask(nb.id, question, source_ids=verified_source_ids)
            answer = result.answer or "[no answer]"
            finding_parts.append(f"### {heading}\n\n{answer}\n")
            raw_qa.append({"heading": heading, "answer": answer})
            plan.record(question)

            # Generate follow-ups
            followups = await generate_followups(heading, question, answer)
            for fh, fq in followups:
                if plan.add_followup(fh, fq):
                    print(f"  Queued follow-up: {fh}")
        except Exception as e:
            logger.warning("[%s] Research question failed for %s: %s", slug, heading, e)
            finding_parts.append(f"### {heading}\n\n[failed: {e}]\n")
            raw_qa.append({"heading": heading, "answer": f"[failed: {e}]"})
            plan.record(question)

    angle_answers: list[str] = []
    angle_raw: list[dict] = []  # Pass empty for Phase 4 synthesis since questions now come from NLM

    # Phase 4 — Synthesize brief
    answered_qa = [qa for qa in raw_qa if not qa["answer"].startswith("[failed:")]
    synthesized_brief = "[Synthesis failed]"
    if not answered_qa:
        logger.warning("[%s] No answered research questions — skipping synthesis", slug)
    else:
        try:
            synthesized_brief = await synthesize_brief(owner_repo, repo_context, raw_qa, angle_raw)
            if len(synthesized_brief) < 200 or "## What it does" not in synthesized_brief:
                logger.warning("[%s] Synthesized brief failed shape check (len=%d) — discarding", slug, len(synthesized_brief))
                synthesized_brief = "[Synthesis failed]"
            else:
                print(f"[{slug}] Brief synthesized")
        except Exception as e:
            logger.warning("[%s] Brief synthesis failed: %s", slug, e)

    # Phase 5 — Generate slides and infographics
    slide_deck_id = None
    infographic_id = None
    slide_deck_path = None
    infographic_path = None
    try:
        print(f"[{slug}] Generating slides and infographics...")
        use_cases_str = ", ".join(repo_context.core_use_cases) if repo_context.core_use_cases else ""
        concepts_str = ", ".join(repo_context.key_concepts) if repo_context.key_concepts else ""
        brief_excerpt = synthesized_brief[:500] if synthesized_brief else (raw_qa[:500] if raw_qa else "")
        artifact_instructions = "\n".join(filter(None, [
            f"Use cases: {use_cases_str}" if use_cases_str else None,
            f"Key concepts: {concepts_str}" if concepts_str else None,
            f"Brief excerpt: {brief_excerpt}" if brief_excerpt else None,
        ])) or None

        # Generate slide deck
        try:
            slides = await client.artifacts.generate_slide_deck(nb.id, instructions=artifact_instructions)
            if slides.task_id:
                print(f"[{slug}] Slide deck submitted (task: {slides.task_id}), waiting for completion...")
                final = await client.artifacts.wait_for_completion(nb.id, slides.task_id, timeout=300)
                if final.is_complete:
                    out_path = str(RESEARCH_DIR / f"{slug}_slides.pdf")
                    await client.artifacts.download_slide_deck(nb.id, out_path, artifact_id=slides.task_id)
                    slide_deck_id = slides.task_id
                    slide_deck_path = out_path
                    print(f"[{slug}] Slide deck downloaded: {out_path}")
                else:
                    logger.warning("[%s] Slide deck generation did not complete: %s", slug, final.error)
            else:
                logger.warning("[%s] Slide deck generation failed: %s", slug, slides.error)
        except Exception as e:
            logger.warning("[%s] Slide deck generation failed: %s", slug, e)

        # Generate infographic
        try:
            infographic = await client.artifacts.generate_infographic(nb.id, instructions=artifact_instructions)
            if infographic.task_id:
                print(f"[{slug}] Infographic submitted (task: {infographic.task_id}), waiting for completion...")
                final = await client.artifacts.wait_for_completion(nb.id, infographic.task_id, timeout=300)
                if final.is_complete:
                    out_path = str(RESEARCH_DIR / f"{slug}_infographic.png")
                    await client.artifacts.download_infographic(nb.id, out_path, artifact_id=infographic.task_id)
                    infographic_id = infographic.task_id
                    infographic_path = out_path
                    print(f"[{slug}] Infographic downloaded: {out_path}")
                else:
                    logger.warning("[%s] Infographic generation did not complete: %s", slug, final.error)
            else:
                logger.warning("[%s] Infographic generation failed: %s", slug, infographic.error)
        except Exception as e:
            logger.warning("[%s] Infographic generation failed: %s", slug, e)

    except Exception as e:
        logger.warning("[%s] Artifact generation failed: %s", slug, e)

    return {
        "url": url,
        "notebook_id": nb.id,
        "finding": "\n".join(finding_parts),
        "sources_found": sources_found,
        "angle_battery": angle_answers,
        "primary_sources_found": primary_count,
        "repo_context": repo_context,
        "verified_sources": [s for s in all_sources if s.id in verified_source_ids],
        "raw_qa": raw_qa,
        "angle_raw": angle_raw,
        "synthesized_brief": synthesized_brief,
        "slide_deck_id": slide_deck_id,
        "slide_deck_path": slide_deck_path,
        "infographic_id": infographic_id,
        "infographic_path": infographic_path,
    }


async def research_one_open_notebook(on_client: OpenNotebookClient, url: str, mode: str) -> dict:
    """Research pipeline for a single repo using open-notebook backend.

    Mirrors research_one() but uses open-notebook's REST API instead of notebooklm-py.
    No web research phase (open-notebook has no equivalent); sources are GitHub primary docs only.
    """
    slug = repo_slug(url)
    title = f"Research: {slug} — {date.today().isoformat()}"
    owner_repo = "/".join(url.rstrip("/").split("/")[-2:])

    print(f"\n[{slug}] Creating notebook (open-notebook)...")
    nb = await on_client.create_notebook(title)
    nb_id = nb.get("id") or nb.get("notebook_id", "")
    logger.info("[%s] Notebook: %s", slug, nb_id)

    # Add repo URL as primary source
    try:
        await on_client.add_source(nb_id, url, wait=True)
    except Exception as e:
        logger.warning("[%s] Failed to add repo URL: %s", slug, e)

    # Add raw README and fetch its text for context extraction
    primary_count = 0
    readme_text = ""
    for branch in ("main", "master"):
        readme_url = f"https://raw.githubusercontent.com/{owner_repo}/{branch}/README.md"
        try:
            async with httpx.AsyncClient(timeout=15) as http:
                resp = await http.get(readme_url)
                if resp.status_code == 200:
                    readme_text = resp.text
            await on_client.add_source(nb_id, readme_url, wait=False)
            primary_count += 1
            print(f"[{slug}] Added primary source: README ({branch})")
            break
        except Exception:
            continue

    # Discover and add additional primary docs (wait=True so sources are indexed before chatting)
    try:
        doc_candidates = await discover_primary_docs(owner_repo, max_docs=6)
        for doc in doc_candidates:
            try:
                await on_client.add_source(nb_id, doc.raw_url, wait=True)
                primary_count += 1
                print(f"[{slug}] Added primary source: {doc.path}")
            except Exception as e:
                logger.warning("[%s] Failed to add primary doc %s: %s", slug, doc.path, e)
        if doc_candidates:
            print(f"[{slug}] Discovered {len(doc_candidates)} additional primary docs")
    except Exception as e:
        logger.warning("[%s] Doc crawler failed: %s", slug, e)

    repo_context = RepoContext([], [], [], [], "")

    # Build notebook context for chat
    context = await on_client.get_notebook_context(nb_id)

    # Create chat session
    try:
        session_id = await on_client.create_chat_session(nb_id)
        print(f"[{slug}] Chat session: {session_id}")
    except Exception as e:
        logger.error("[%s] Failed to create chat session: %s", slug, e)
        session_id = ""

    # Seed questions from README via Gemma
    print(f"[{slug}] Seeding questions via Gemma...")
    seed_qs = await seed_questions_from_readme(readme_text[:4000], owner_repo)
    plan = QuestionPlan(seed_qs, budget=15)
    print(f"[{slug}] Querying ({len(seed_qs)} seed questions, budget 15)...")

    finding_parts: list[str] = []
    raw_qa: list[dict] = []

    while True:
        item = plan.next_question()
        if item is None:
            break
        heading, question = item
        try:
            answer = await on_client.ask(session_id, question, context=context)
            finding_parts.append(f"### {heading}\n\n{answer}\n")
            raw_qa.append({"heading": heading, "answer": answer})
            plan.record(question)

            followups = await generate_followups(heading, question, answer)
            for fh, fq in followups:
                if plan.add_followup(fh, fq):
                    print(f"  Queued follow-up: {fh}")
        except Exception as e:
            logger.warning("[%s] Question failed for %s: %s", slug, heading, e)
            finding_parts.append(f"### {heading}\n\n[failed: {e}]\n")
            raw_qa.append({"heading": heading, "answer": f"[failed: {e}]"})
            plan.record(question)

    synthesized_brief = "[Synthesis failed]"
    try:
        synthesized_brief = await synthesize_brief(owner_repo, repo_context, raw_qa, [])
        print(f"[{slug}] Brief synthesized")
    except Exception as e:
        logger.warning("[%s] Brief synthesis failed: %s", slug, e)

    return {
        "url": url,
        "notebook_id": nb_id,
        "finding": "\n".join(finding_parts),
        "sources_found": [],
        "angle_battery": [],
        "primary_sources_found": primary_count,
        "repo_context": repo_context,
        "verified_sources": [],
        "raw_qa": raw_qa,
        "angle_raw": [],
        "synthesized_brief": synthesized_brief,
        "slide_deck_id": None,
        "slide_deck_path": None,
        "infographic_id": None,
        "infographic_path": None,
    }


async def run(
    niche: str,
    mode: str = "deep",
    repos: list[str] | None = None,
    backend: str = "notebooklm",
) -> Path:
    """Run isolated research per repo. Returns path to the compiled brief."""

    if not repos:
        raise ValueError(
            "No repos specified. Run with --list to see available repos, "
            "then pass them explicitly with --repos owner/repo1 owner/repo2"
        )

    # Accept "owner/repo" or a full URL; research exactly the repos passed in
    # (do not require them to be present in the aggregate trends file).
    def to_url(r: str) -> str:
        r = r.strip().rstrip("/")
        return r if r.startswith("http") else f"https://github.com/{r}"

    urls: list[str] = []
    seen: set[str] = set()
    for r in repos:
        u = to_url(r)
        if u and u not in seen:
            seen.add(u)
            urls.append(u)

    if not urls:
        raise ValueError(f"No valid repo URLs in --repos: {repos}")

    today = date.today().isoformat()

    # Resolve backend
    effective_backend = backend
    if backend == "auto":
        async with OpenNotebookClient() as on_client:
            effective_backend = "open-notebook" if await on_client.health_check() else "notebooklm"
        print(f"[auto] Backend: {effective_backend}")

    print(f"Found {len(urls)} repos. Running isolated research on each ({effective_backend})...\n")

    findings = []
    if effective_backend == "open-notebook":
        async with OpenNotebookClient() as on_client:
            for url in urls:
                try:
                    result = await research_one_open_notebook(on_client, url, mode)
                    findings.append(result)
                except Exception as e:
                    logger.error("Failed for %s: %s", url, e)
                    findings.append({"url": url, "notebook_id": None, "finding": f"ERROR: {e}", "sources_found": []})
    else:
        async with await NotebookLMClient.from_storage(timeout=300) as client:
            for url in urls:
                try:
                    result = await research_one(client, url, mode)
                    findings.append(result)
                except Exception as e:
                    logger.error("Failed for %s: %s", url, e)
                    findings.append({"url": url, "notebook_id": None, "finding": f"ERROR: {e}", "sources_found": []})

    # Compile all findings into one brief
    sections = []
    for f in findings:
        slug = repo_slug(f["url"])
        nb_line = f"notebook_id: {f['notebook_id']}" if f["notebook_id"] else "notebook_id: failed"

        # Use synthesized brief (from Phase 4)
        brief_content = f.get("synthesized_brief", "[Synthesis failed]")

        # Append Sources section
        verified_sources = f.get("verified_sources", [])
        if verified_sources:
            sources_md = "## Sources\n\n"
            for src in verified_sources:
                title = src.title or "Untitled"
                sources_md += f"- **{title}**\n"
            brief_content += f"\n\n{sources_md}"

        # Append Raw findings in details block
        raw_findings = "## Raw Findings\n\n<details><summary>Expand for full Q&A and angle battery</summary>\n\n"
        raw_findings += "### Research Questions\n\n"
        for qa in f.get("raw_qa", []):
            raw_findings += f"**{qa['heading']}**\n\n{qa['answer']}\n\n"
        raw_findings += "### Angle Battery\n\n"
        for qa in f.get("angle_raw", []):
            raw_findings += f"**{qa['heading']}**\n\n{qa['answer']}\n\n"
        raw_findings += "</details>\n"
        brief_content += f"\n\n{raw_findings}"

        artifact_lines = ""
        if f.get("slide_deck_path"):
            artifact_lines += f"slide_deck: {f['slide_deck_path']}  \n"
        if f.get("infographic_path"):
            artifact_lines += f"infographic: {f['infographic_path']}  \n"

        sections.append(
            f"## {slug}\n"
            f"Source: {f['url']}  \n"
            f"{nb_line}  \n"
            f"{artifact_lines}\n"
            f"{brief_content}\n"
        )

    niche_slug = niche.lower().replace(" ", "-")
    if urls:
        repo_names = "_".join(u.rstrip("/").split("/")[-1].lower() for u in urls[:2])
        niche_slug = f"{niche_slug}_{repo_names}"
    notebook_ids = [f["notebook_id"] for f in findings if f["notebook_id"]]
    total_primaries = sum(f.get("primary_sources_found", 0) for f in findings)

    # Collect artifact IDs and local paths
    slide_deck_ids = [f.get("slide_deck_id") for f in findings if f.get("slide_deck_id")]
    infographic_ids = [f.get("infographic_id") for f in findings if f.get("infographic_id")]
    slide_deck_paths = [f.get("slide_deck_path") for f in findings if f.get("slide_deck_path")]
    infographic_paths = [f.get("infographic_path") for f in findings if f.get("infographic_path")]

    artifact_frontmatter = ""
    if slide_deck_ids:
        artifact_frontmatter += f"slide_deck_ids: [{', '.join(slide_deck_ids)}]\n"
    if slide_deck_paths:
        artifact_frontmatter += f"slide_deck_files: [{', '.join(slide_deck_paths)}]\n"
    if infographic_ids:
        artifact_frontmatter += f"infographic_ids: [{', '.join(infographic_ids)}]\n"
    if infographic_paths:
        artifact_frontmatter += f"infographic_files: [{', '.join(infographic_paths)}]\n"

    output = (
        f"---\n"
        f"date: {today}\n"
        f"niche: {niche}\n"
        f"repos_researched: {len(findings)}\n"
        f"primary_sources_found: {total_primaries}\n"
        f"notebook_ids: [{', '.join(notebook_ids)}]\n"
        f"{artifact_frontmatter}"
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
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Content gap research via NotebookLM")
    parser.add_argument("--niche", help='Topic label for the output file, e.g. "AI agents"')
    parser.add_argument("--mode", choices=["fast", "deep"], default="deep")
    parser.add_argument("--repos", nargs="+", metavar="OWNER/REPO",
                        help="Repos to research, e.g. --repos owner/repo1 owner/repo2")
    parser.add_argument("--list", action="store_true", dest="list_repos",
                        help="List available repos from the trending file and exit")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print planned questions without calling NLM/NIM then exit")
    parser.add_argument(
        "--backend",
        choices=["auto", "open-notebook", "notebooklm"],
        default="notebooklm",
        help="Research backend. Default: notebooklm. Use 'open-notebook' when Docker backend is ready.",
    )
    add_brief_args(parser)
    args = parser.parse_args()
    brief = load_brief()
    brief = apply_cli_overrides(brief, args)

    if args.list_repos:
        list_available_repos()
        return

    if args.dry_run:
        if not args.repos:
            print("ERROR: --repos is required for --dry-run.\n")
            list_available_repos()
            return
        if not args.niche:
            parser.error("--niche is required for --dry-run")
        print(f"\n[dry-run] Topic: {args.niche}")
        print(f"[dry-run] Repos: {args.repos}")
        print(f"[dry-run] Backend: {args.backend}")
        print("[dry-run] Would seed questions and run up to 15 chat queries")
        print("[dry-run] (exiting without calling backend)\n")
        return

    if not args.repos:
        print("ERROR: --repos is required. Run with --list to see available repos.\n")
        list_available_repos()
        return

    if not args.niche:
        parser.error("--niche is required when running research")

    output_path = await run(args.niche, mode=args.mode, repos=args.repos, backend=args.backend)

    print("\n" + "=" * 60)
    brief = output_path.read_text(encoding="utf-8")
    print(brief[:2000])
    if len(brief) > 2000:
        print(f"\n...({len(brief) - 2000} more chars — open {output_path})")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    asyncio.run(main())
