"""Retry the timed-out Q2 from the NotebookLM research session."""
import asyncio, sys, json, os
sys.stdout.reconfigure(encoding='utf-8')
from notebooklm import NotebookLMClient

NB_ID = "fed17d39-899a-4c43-92b8-7ce2741d2d14"

async def main():
    client = await NotebookLMClient.from_storage()
    async with client:
        print("Retrying Q2: Specific Claude Code automations...")
        result = await client.chat.ask(
            NB_ID,
            "List every specific Claude Code skill, automation, and script mentioned in the video. For each one, describe: its name, what it does, what inputs it takes, what it outputs, and which phase of the content pipeline it belongs to. Be exhaustive."
        )
        answer = result.answer if hasattr(result, 'answer') else str(result)
        print(f"\nGot answer ({len(answer)} chars):\n")
        print(answer)
        
        # Append to findings
        findings_path = os.path.join(os.path.dirname(__file__), "notebooklm_findings.md")
        with open(findings_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Replace the error line
        content = content.replace(
            "ERROR: Chat request timed out: ",
            answer
        )
        with open(findings_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\nUpdated findings file with Q2 answer.")

if __name__ == "__main__":
    asyncio.run(main())
