import anthropic
import sys
import json
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def route_task(task_description):
    """Uses Haiku to classify task complexity."""
    prompt = f"Categorize this task as 'EASY' or 'HARD'. Reply with exactly ONE WORD. Task: {task_description}"
    response = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip().upper()

def run_haiku_delegate(instructions):
    """Sub-agent worker function invoked by Sonnet."""
    print(f"      [intern] Haiku is grabbing this sub-task: {instructions[:50]}...")
    resp = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": instructions}]
    )
    return resp.content[0].text

def execute_task_with_advisor(task_description, executor_model, advisor_model):
    """Runs the main tier with the Advisor beta tool."""
    print(f"\n🚀 Router: Dispatching to Executor: {executor_model} | 🧠 Advisor: {advisor_model}")
    
    tools = [
        # 1. The native Advisor Tool
        {"type": "advisor_20260301", "name": "advisor", "model": advisor_model},
        
        # 2. Our Local Sub-executor Tool (The 3rd Tier)
        {
            "name": "delegate_to_haiku",
            "description": "Hand off simple formatting, syntax translation, or repetitive typing tasks to a faster model.",
            "input_schema": {
                "type": "object",
                "properties": {"task_instructions": {"type": "string"}}
            }
        }
    ]
    
    messages = [{"role": "user", "content": f"Execute this MVP task. Consult your advisor for a strategic plan. You may use delegate_to_haiku for scaffolding: {task_description}"}]
    
    # We use a primitive loop here in case Sonnet invokes delegate_to_haiku
    while True:
        response = client.beta.messages.create(
            model=executor_model,
            max_tokens=4096,
            betas=["advisor-tool-2026-03-01"],
            tools=tools,
            messages=messages
        )
        
        # Append the assistant's turn
        messages.append({"role": "assistant", "content": response.content})
        
        tool_executed = False
        for block in response.content:
            if block.type == "text" and block.text.strip() != "":
                print("\n💻 EXECUTOR:\n", block.text)
            elif block.type == "advisor_tool_result":
                print("\n🧠 ADVISOR STRATEGY:\n", block.content.text)
            elif block.type == "tool_use":
                if block.name == "delegate_to_haiku":
                    result_text = run_haiku_delegate(block.input.get("task_instructions"))
                    print(f"      [intern] Haiku completed the sub-task. Sending back to Sonnet.")
                    messages.append({
                        "role": "user",
                        "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result_text}]
                    })
                    tool_executed = True
        
        if not tool_executed:
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/orchestrator.py '<task>'")
        sys.exit(1)
        
    task = sys.argv[1]
    complexity = route_task(task)
    
    if complexity == "EASY":
        execute_task_with_advisor(task, "claude-3-5-haiku-20241022", "claude-3-5-sonnet-20241022")
    else:
        execute_task_with_advisor(task, "claude-3-5-sonnet-20241022", "claude-3-opus-20240229")
