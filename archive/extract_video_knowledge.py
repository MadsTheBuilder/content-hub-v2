"""
Extract bug/failure knowledge from a Content Hub demo video via NotebookLM.
Writes everything to tmp/video-notes.md for direct paste into next session.
"""
import asyncio
import os
from datetime import datetime
from notebooklm import NotebookLMClient

DRIVE_URL = "https://drive.google.com/file/d/1grw1vBFm8hcJgNaDIyqV2thOsnJH6WFf/view?usp=drive_link"
DRIVE_FILE_ID = "1grw1vBFm8hcJgNaDIyqV2thOsnJH6WFf"
NOTEBOOK_TITLE = "Content Hub - Bug Triage Video"
OUTPUT_PATH = "tmp/video-notes.md"

# Questions targeted at extracting actionable debugging info
QUESTIONS = [
    ("Overview", "Describe the video chronologically. What application is being demoed, what features are being shown, and in what order? Include any UI screens, buttons clicked, or pages navigated."),
    ("Failures", "List EVERY failure, error, bug, crash, unexpected behavior, broken UI element, or moment where the user shows frustration. For each, describe: (1) what the user was trying to do, (2) what happened instead, (3) any error messages visible, (4) approximate timestamp in the video."),
    ("Verbal_Notes", "Quote or paraphrase everything the user says or narrates verbally. Include any complaints, observations, intended outcomes, or descriptions of how things 'should' work."),
    ("UI_Details", "List every visible UI element relevant to the failures: button names, page URLs, form fields, error toasts, console errors, network errors, anything in DevTools if shown."),
    ("Expected_vs_Actual", "For each broken feature, what is the user clearly expecting to happen vs what actually happens? Be specific."),
    ("Severity_Ranking", "Rank the failures from most severe (blocks core functionality) to least severe (cosmetic). Justify each ranking."),
]


async def main():
    os.makedirs("tmp", exist_ok=True)
    output_lines = []

    def log(line=""):
        print(line)
        output_lines.append(line)

    log(f"# Content Hub — Video Knowledge Extraction")
    log(f"\n*Generated: {datetime.now().isoformat()}*")
    log(f"\n*Source video: {DRIVE_URL}*\n")

    async with await NotebookLMClient.from_storage() as client:

        log("## Setup\n")
        log("Creating notebook...")
        notebook = await client.notebooks.create(NOTEBOOK_TITLE)
        nb_id = notebook.id
        log(f"- Notebook ID: `{nb_id}`")

        log("\nAdding Google Drive video source...")
        source = None
        errors = []
        for attempt_label, attempt in [
            ("add_url with URL", lambda: client.sources.add_url(nb_id, DRIVE_URL, wait=True)),
            ("add_drive with video/mp4", lambda: client.sources.add_drive(nb_id, DRIVE_FILE_ID, title="Demo Video", mime_type="video/mp4", wait=True)),
            ("add_drive default", lambda: client.sources.add_drive(nb_id, DRIVE_FILE_ID, title="Demo Video", wait=True)),
        ]:
            try:
                source = await attempt()
                log(f"- Source added via: **{attempt_label}**")
                log(f"- Title: {source.title}")
                log(f"- Type: {source.source_type}")
                break
            except Exception as e:
                errors.append(f"{attempt_label}: {e}")

        if source is None:
            log("\n## ERROR — Could not add source\n")
            for err in errors:
                log(f"- {err}")
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                f.write("\n".join(output_lines))
            return

        log("\n## Source Guide (AI auto-summary)\n")
        try:
            guide = await client.sources.guide(nb_id, source.id)
            log(f"```\n{guide}\n```")
        except Exception as e:
            log(f"*Guide unavailable: {e}*")

        log("\n## Knowledge Extraction\n")
        for label, question in QUESTIONS:
            log(f"### {label}\n")
            log(f"**Q:** {question}\n")
            try:
                response = await client.chat.ask(nb_id, question)
                text = response.text if hasattr(response, "text") else str(response)
                log(f"**A:**\n\n{text}\n")
            except Exception as e:
                log(f"*Error: {e}*\n")

        log("\n## Notebook Reference\n")
        log(f"- Notebook ID: `{nb_id}`")
        log(f"- View at: https://notebooklm.google.com")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"\n{'='*60}")
    print(f"OUTPUT WRITTEN TO: {os.path.abspath(OUTPUT_PATH)}")
    print(f"{'='*60}")


if __name__ == "__main__":
    asyncio.run(main())
