# Eval 3 — Full Invocation (with_skill)

## Prompt
> "research the microsoft/autogen repo, niche is AI agents"

---

## Skill Content

**SKILL.md Summary:**
The `/researcher` skill is Step 1 of a 7-step content production pipeline. It runs deep content-gap research on GitHub repos via NotebookLM and outputs a dated research brief. Key behaviors:

1. **Niche input**: Inline with the command or asked separately
2. **Repo confirmation**: Before running, show the user which repos will be researched and ask for confirmation
3. **CLI command**: `python -m skills.researcher --niche "[niche]" --repos owner/repo1 owner/repo2`
4. **Output format**: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md`
5. **Output structure**: Each repo section includes synthesized brief (5 sections) + "Recommended Video Angle" + raw Q&A
6. **Timing**: Deep mode (default) ~8 min/repo; Fast mode ~3–4 min/repo
7. **Next step**: Always suggest `/hook` after the brief is reviewed

---

## Response

Got it — **researching microsoft/autogen for the AI agents niche**.

Here's what I'll run:

```powershell
python -m skills.researcher --niche "AI agents" --repos microsoft/autogen
```

**Confirm?** This will:
- Index the microsoft/autogen repository in NotebookLM
- Run 11 deep-research questions to extract content gaps
- Synthesize findings into a 5-section brief + recommended video angle
- Save the output to `Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.md`
- Deep mode takes ~8 minutes

---

### [Simulated Execution — After Confirmation]

**Research complete.** Here's what was generated:

**Output file:**
```
Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.md
```

**Brief contents** (from the output):

**microsoft/autogen section:**
- **What it does**: Multi-agent orchestration framework for building collaborative AI systems where agents can communicate, delegate, and solve complex tasks
- **Who it's for**: Developers building enterprise AI workflows, research teams exploring agentic patterns, companies scaling from single-agent to multi-agent architectures
- **How it works**: Conversation-driven agent loops with pluggable LLMs, user proxies, and built-in execution environments
- **When to use**: When you need agents to collaborate on shared goals, handle code execution safely, or maintain conversation state across multiple turns
- **Watch out for**: Token costs scale with multi-turn conversations; setup complexity for custom agent configurations
- **Recommended Video Angle**: *"From Single Agent to Multi-Agent: How AutoGen Solves Real Collaboration Problems"* — Focus on the orchestration gap in existing frameworks, show a working multi-agent workflow, and compare to single-agent alternatives
- **Notebook ID**: `jzp-abc123` (for follow-up queries)

---

### Next Step

Once you've reviewed the brief, kick off the hook generation:

```
/hook topic="From Single Agent to Multi-Agent: How AutoGen Solves Real Collaboration Problems"
```

This takes your video angle and generates a compelling hook + outline structure.
