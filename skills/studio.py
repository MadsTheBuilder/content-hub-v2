"""Studio artifact generation for NotebookLM.

Entry points:
  - generate_reports() — create explainer + technical reports
  - inject_cascade_and_generate() — add cascade to notebook, generate slides + video
"""

import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from notebooklm import NotebookLMClient, ReportFormat, SlideDeckFormat, SlideDeckLength, VideoFormat, VideoStyle
from skills.helpers.nim_picker import pick_best_report

logger = logging.getLogger(__name__)

VAULT_REPORTS = PROJECT_ROOT / "Content-Hub-Vault-V2" / "11-Reports"
VAULT_SLIDES = PROJECT_ROOT / "Content-Hub-Vault-V2" / "12-Slides"
VAULT_VIDEO = PROJECT_ROOT / "Content-Hub-Vault-V2" / "13-Video"


EXPLAINER_PROMPT = """Write a plain-language explainer for an intelligent but non-technical reader (product manager, founder, marketer who doesn't ship code). Goal: the reader can confidently explain this thing to a colleague in 30 seconds after reading.

Required structure:
1. **What it is** — one paragraph, no jargon. Anchor with a one-line analogy to something the reader already knows.
2. **Why it matters** — concrete real-world impact. Name the problem it removes and what was painful before.
3. **How it works (mental model)** — high-level only. No code, no API names, no version numbers. Use a single sustained metaphor across the section.
4. **Who should care** — 3 specific reader profiles, one paragraph each, naming the problem each profile solves with this.
5. **Tradeoffs and watch-outs** — honest limitations, what it isn't for, where it breaks down.

Style rules: short paragraphs, no bullet-dumps, no marketing-speak ("revolutionize", "unleash", "empower"), no hedging ("might", "could potentially"). Every section opens with a clear topic sentence. Inline cite the sources. Target length: 1200–1800 words."""

TECHNICAL_PROMPT = """Write a deep-dive technical and architecture report for a senior engineer evaluating whether to adopt this in production. Goal: the reader can make a build-vs-buy decision and write an ADR after reading.

Required structure:
1. **Architecture overview** — components, responsibilities, control flow. Use a text-based diagram (ASCII or mermaid-style) showing how requests/data move.
2. **Data flow** — what moves between components, where state lives, sync vs async boundaries, ownership of mutation.
3. **Integration surface** — public APIs, SDK shape, extension points, plugin/middleware model. Include a representative code snippet if sources support one.
4. **Performance and scale** — concurrency model, throughput numbers if cited, known bottlenecks, resource footprint.
5. **Failure modes and resilience** — what happens when a dependency dies, retry/timeout/fallback semantics, idempotency guarantees.
6. **Comparison to alternatives** — side-by-side with named competitors if sources mention them. Be specific about where each one wins.
7. **Production readiness** — observability hooks, security model, auth model, deployment story, operational gotchas.

Style rules: precise, terminology-correct, no hedging, no analogies. Schema fragments and pseudo-code welcome where they clarify. Cite sources inline. Target length: 2000–3000 words."""


async def generate_reports(notebook_id: str, slug: str) -> dict:
    """Generate explainer + technical reports for a notebook.

    1. Calls client.studio.suggest_reports() for NLM suggestions.
    2. Uses NIM to pick best explainer-like + technical-like from suggestions.
    3. If NIM picks None for either slot, falls back to CUSTOM format.
    4. Downloads both reports to 11-Reports/{slug}/*.

    Args:
        notebook_id: The notebook ID.
        slug: Topic slug for output directory (e.g., "ai-agents").

    Returns:
        Dictionary with keys: explainer_path, technical_path, notebook_id, slug.
    """
    out_dir = VAULT_REPORTS / slug
    out_dir.mkdir(parents=True, exist_ok=True)

    async with await NotebookLMClient.from_storage() as client:
        # Get suggested reports from NLM
        suggestions = await client.artifacts.suggest_reports(notebook_id)
        logger.info("NLM suggested %d report formats", len(suggestions))

        # Use NIM to pick best explainer
        explainer_suggestion = None
        technical_suggestion = None

        if suggestions:
            explainer_suggestion = await pick_best_report(suggestions, "explainer")
            technical_suggestion = await pick_best_report(suggestions, "technical")

        # Generate explainer
        if explainer_suggestion:
            logger.info("Using NLM suggestion: %s", explainer_suggestion.title)
            gen = await client.artifacts.generate_report(
                notebook_id,
                report_format=ReportFormat.CUSTOM,
                custom_prompt=explainer_suggestion.prompt,
            )
        else:
            logger.info("No good explainer match found, using fallback prompt")
            gen = await client.artifacts.generate_report(
                notebook_id,
                report_format=ReportFormat.CUSTOM,
                custom_prompt=EXPLAINER_PROMPT,
            )

        if gen.task_id:
            logger.info("Waiting for explainer report generation...")
            final = await client.artifacts.wait_for_completion(notebook_id, gen.task_id, timeout=600)
            if final.is_complete:
                explainer_path = str(out_dir / "explainer_report.md")
                await client.artifacts.download_report(notebook_id, explainer_path, artifact_id=gen.task_id)
                logger.info("Explainer report downloaded: %s", explainer_path)
            else:
                logger.error("Explainer generation failed: %s", final.error)
                explainer_path = None
        else:
            logger.error("Explainer generation submission failed: %s", gen.error)
            explainer_path = None

        # Generate technical
        if technical_suggestion:
            logger.info("Using NLM suggestion: %s", technical_suggestion.title)
            gen = await client.artifacts.generate_report(
                notebook_id,
                report_format=ReportFormat.CUSTOM,
                custom_prompt=technical_suggestion.prompt,
            )
        else:
            logger.info("No good technical match found, using fallback prompt")
            gen = await client.artifacts.generate_report(
                notebook_id,
                report_format=ReportFormat.CUSTOM,
                custom_prompt=TECHNICAL_PROMPT,
            )

        if gen.task_id:
            logger.info("Waiting for technical report generation...")
            final = await client.artifacts.wait_for_completion(notebook_id, gen.task_id, timeout=600)
            if final.is_complete:
                technical_path = str(out_dir / "technical_report.md")
                await client.artifacts.download_report(notebook_id, technical_path, artifact_id=gen.task_id)
                logger.info("Technical report downloaded: %s", technical_path)
            else:
                logger.error("Technical generation failed: %s", final.error)
                technical_path = None
        else:
            logger.error("Technical generation submission failed: %s", gen.error)
            technical_path = None

    return {
        "explainer_path": explainer_path,
        "technical_path": technical_path,
        "notebook_id": notebook_id,
        "slug": slug,
    }


async def inject_cascade_and_generate(cascade_dir: str, notebook_id: str, slug: str) -> dict:
    """Add cascade files to notebook and generate slides + video.

    1. Reads blog_post.md, instagram_post.md, linkedin_post.md from cascade_dir.
    2. Adds each as text source to the notebook.
    3. Generates 3 slide decks (one per channel) to 12-Slides/{slug}/*.
    4. Generates 1 video (LinkedIn format) to 13-Video/{slug}/linkedin_video.mp4.

    Args:
        cascade_dir: Path to directory containing blog_post.md, instagram_post.md, linkedin_post.md.
        notebook_id: The notebook ID.
        slug: Topic slug for output directories (e.g., "ai-agents").

    Returns:
        Dictionary with keys: slides (dict of channel->path), video_path, notebook_id, slug.
    """
    cascade_path = Path(cascade_dir)
    if not cascade_path.exists():
        logger.error("Cascade directory not found: %s", cascade_dir)
        return {
            "slides": {},
            "video_path": None,
            "notebook_id": notebook_id,
            "slug": slug,
        }

    async with await NotebookLMClient.from_storage() as client:
        # Add cascade files as sources
        for filename in ["blog_post.md", "instagram_post.md", "linkedin_post.md"]:
            fpath = cascade_path / filename
            if fpath.exists():
                content = fpath.read_text(encoding="utf-8")
                logger.info("Adding %s as source...", filename)
                try:
                    await client.sources.add_text(notebook_id, filename, content)
                except Exception as e:
                    logger.warning("Failed to add %s: %s", filename, e)

        # Generate 3 slide decks
        slides = {}
        for channel in ["blog", "instagram", "linkedin"]:
            logger.info("Generating %s slide deck...", channel)
            gen = await client.artifacts.generate_slide_deck(
                notebook_id,
                slide_format=SlideDeckFormat.DETAILED_DECK,
                slide_length=SlideDeckLength.DEFAULT,
            )

            if gen.task_id:
                logger.info("Waiting for %s slide deck...", channel)
                final = await client.artifacts.wait_for_completion(notebook_id, gen.task_id, timeout=1800)
                if final.is_complete:
                    out_dir = VAULT_SLIDES / slug
                    out_dir.mkdir(parents=True, exist_ok=True)
                    slide_path = str(out_dir / f"{channel}_deck.pdf")
                    await client.artifacts.download_slide_deck(notebook_id, slide_path, artifact_id=gen.task_id)
                    logger.info("Slide deck downloaded: %s", slide_path)
                    slides[channel] = slide_path
                else:
                    logger.error("%s slide deck generation failed: %s", channel, final.error)
            else:
                logger.error("%s slide deck submission failed: %s", channel, gen.error)

        # Generate LinkedIn video only
        logger.info("Generating LinkedIn video...")
        gen = await client.artifacts.generate_video(
            notebook_id,
            video_format=VideoFormat.EXPLAINER,
            video_style=VideoStyle.AUTO_SELECT,
        )

        video_path = None
        if gen.task_id:
            logger.info("Waiting for video generation...")
            try:
                final = await client.artifacts.wait_for_completion(notebook_id, gen.task_id, timeout=3600)
                if final.is_complete:
                    out_dir = VAULT_VIDEO / slug
                    out_dir.mkdir(parents=True, exist_ok=True)
                    video_path = str(out_dir / "linkedin_video.mp4")
                    await client.artifacts.download_video(notebook_id, video_path, artifact_id=gen.task_id)
                    logger.info("Video downloaded: %s", video_path)
                else:
                    logger.error("Video generation failed: %s", final.error)
            except TimeoutError as e:
                logger.error("Video generation timed out: %s", e)
        else:
            logger.error("Video submission failed: %s", gen.error)

    return {
        "slides": slides,
        "video_path": video_path,
        "notebook_id": notebook_id,
        "slug": slug,
    }
