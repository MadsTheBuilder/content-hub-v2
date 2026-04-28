"""
Use NotebookLM to deeply analyze the YouTube video:
"These Claude Code Automations Got Me 10M Views in 1 Month"
"""
import asyncio
import json
import sys
import os

# Fix Windows Unicode output
sys.stdout.reconfigure(encoding='utf-8')

from notebooklm import NotebookLMClient

VIDEO_URL = "https://www.youtube.com/watch?v=7q_rbT1a9dE"
NOTEBOOK_NAME = "Content Engine Deep Dive"

async def main():
    print("=== NotebookLM Research Session ===\n")
    
    try:
        client = await NotebookLMClient.from_storage()
    except Exception as e:
        print(f"ERROR: Could not create client. Did you complete login? Error: {e}")
        return
    
    async with client:
        # Step 1: Create notebook
        print("[1/5] Creating notebook...")
        try:
            nb = await client.notebooks.create(NOTEBOOK_NAME)
            nb_id = nb.id
            print(f"  Created: {nb_id}")
        except Exception as e:
            print(f"  Error creating notebook: {e}")
            # Try listing existing notebooks
            print("  Listing existing notebooks...")
            notebooks = await client.notebooks.list()
            for n in notebooks:
                print(f"    - {n.title} ({n.id})")
            return

        # Step 2: Add YouTube video as source
        print(f"\n[2/5] Adding YouTube source: {VIDEO_URL}")
        try:
            source = await client.sources.add_url(nb_id, VIDEO_URL, wait=True)
            print(f"  Source added successfully!")
        except Exception as e:
            print(f"  Error adding source: {e}")
            print("  Continuing with whatever sources exist...")

        # Step 3: Deep analysis questions
        questions = [
            "Give me a complete, detailed summary of everything discussed in this video. What is the creator's full workflow and content engine? Include every tool, step, and automation mentioned.",
            
            "What specific Claude Code automations does the creator use? List every single automation, script, or workflow mentioned with exact details on what each one does.",
            
            "What is the complete content creation pipeline from idea to published video? Break it down into every stage, tool used at each stage, and how they connect.",
            
            "What metrics and results does the creator report? How many views, subscribers, videos produced, time saved? What was the before vs after comparison?",
            
            "What are the key strategic insights and lessons about using AI agents for content creation at scale? What advice does the creator give? What mistakes to avoid?"
        ]
        
        print(f"\n[3/5] Querying NotebookLM with {len(questions)} deep-dive questions...\n")
        
        results = []
        for i, question in enumerate(questions, 1):
            print(f"  Question {i}/{len(questions)}: {question[:80]}...")
            try:
                result = await client.chat.ask(nb_id, question)
                answer = result.answer if hasattr(result, 'answer') else str(result)
                results.append({"question": question, "answer": answer})
                print(f"  Got answer ({len(answer)} chars)\n")
            except Exception as e:
                results.append({"question": question, "answer": f"ERROR: {e}"})
                print(f"  Error: {e}\n")

        # Step 4: Save results
        output_path = os.path.join(os.path.dirname(__file__), "notebooklm_findings.md")
        print(f"\n[4/5] Saving findings to {output_path}...")
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Content Engine Deep Dive — NotebookLM Analysis\n\n")
            f.write(f"**Source:** [{VIDEO_URL}]({VIDEO_URL})\n")
            f.write(f"**Video:** These Claude Code Automations Got Me 10M Views in 1 Month\n\n")
            f.write("---\n\n")
            
            for i, r in enumerate(results, 1):
                f.write(f"## Q{i}: {r['question']}\n\n")
                f.write(f"{r['answer']}\n\n")
                f.write("---\n\n")
        
        print(f"  Saved!")

        # Step 5: Also save raw JSON
        json_path = os.path.join(os.path.dirname(__file__), "notebooklm_findings.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n[5/5] Done! Notebook ID: {nb_id}")
        print(f"  Markdown: {output_path}")
        print(f"  JSON: {json_path}")

if __name__ == "__main__":
    asyncio.run(main())
