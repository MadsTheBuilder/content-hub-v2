# Eval 1 — No Args (old_skill)

## Prompt
"I want to start making a video but I'm not sure what angle to take yet. Can you kick off researcher for me?"

## Skill Content
The old SKILL.md specifies:
- Researcher is triggered by `/researcher` with a niche
- **Step 1 requires a niche** from the user (inline with the command OR ask if not provided)
- Must get a niche before proceeding (examples: "AI agents", "local LLMs", "open-source tools")
- Cannot auto-select repos — user must pick them after seeing the list
- Execution flow: get niche → list repos → user picks → confirm → run with `--niche` and `--repos` flags
- Output is a dated brief file in `Content-Hub-Vault-V2/10-Research/` with content gap analysis per repo

## Response

I can help you kick off the researcher skill. This skill runs isolated content gap research on GitHub trending repos to help you find a strong video angle.

Before we start, I need one thing from you: **what's your general interest area or niche?**

This could be something like:
- "AI agents"
- "local LLMs"
- "open-source dev tools"
- "database optimization"
- Or any other topic you're curious about

Once you give me a niche, I'll:
1. Show you the list of trending repos that match
2. Ask you to pick which repos you want me to deep-dive on
3. Run the research and generate a brief with content gap analysis + recommended video angles for each repo

What niche should I research?
