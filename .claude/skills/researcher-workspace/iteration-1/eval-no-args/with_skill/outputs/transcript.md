# Eval 1 — No Args (with_skill)

## Prompt
"I want to start making a video but I'm not sure what angle to take yet. Can you kick off researcher for me?"

## Skill Content
The /researcher SKILL.md describes Step 1 of the 7-step content production pipeline. It:
- Takes a niche (topic label) and list of repos as inputs
- Uses NotebookLM to research GitHub repos and find content gaps
- Outputs a dated research brief with recommended video angles
- Requires user input: niche first, then explicit repo selection
- Key constraint: "Never auto-select repos without the user's explicit choice"
- Next step recommendation: /hook with the chosen angle

## Response

Got it — let's kick off the researcher pipeline. This will help you find a strong video angle by researching GitHub trending repos in your niche.

First, **what niche or topic area interests you?** Some examples:
- AI agents
- Local LLMs
- Open-source tools
- Web development
- DevOps / infrastructure
- Data engineering
- Python frameworks
- Or something else?

Once you tell me the niche, I'll show you the list of trending repos we have in that space, and you can pick which ones to research.

