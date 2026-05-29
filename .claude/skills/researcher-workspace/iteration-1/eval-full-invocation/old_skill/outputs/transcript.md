# Eval 3 — Full Invocation (old_skill)

## Prompt
```
research the microsoft/autogen repo, niche is AI agents
```

## Skill Content Summary

The old `/researcher` skill:
- **Trigger**: `/researcher` with a niche
- **Workflow**: 
  1. Get niche (provided: "AI agents") ✓
  2. List available repos (`--list` flag)
  3. Ask user to pick repos
  4. **BUT** — user provided specific repo inline: `microsoft/autogen`
  5. Confirm before running
  6. Execute: `python -m skills.researcher --niche "[niche]" --repos owner/repo`
  7. Report output file path + "Recommended Video Angle" for each repo
- **Output**: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md`
- **Quality**: Source filtering for GitHub URLs + relevance matching to repo name
- **Next Step**: `/hook topic="<chosen angle>"`

## Response

Got it. You've specified the repo and niche directly, so I'll skip the listing step and move to confirmation.

---

### Repo Confirmation

**Repository**: microsoft/autogen  
**Niche**: AI agents  
**Mode**: deep (default, ~8 min)

I'm about to run:
```powershell
python -m skills.researcher --niche "AI agents" --repos microsoft/autogen
```

This will:
1. Research the microsoft/autogen repo through NotebookLM
2. Generate a content gap analysis anchored to AutoGen and AI agents
3. Identify 2–3 video angles from the repo's strategic position
4. Save the brief to `Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.md`

**Confirm? (yes/no)**

---

## Simulated Execution (Post-Confirmation)

Assuming user confirms with "yes":

```
Running researcher on: [microsoft/autogen] — niche: AI agents — confirm? yes

[Researcher running...]
✓ Web research complete (32 sources found)
✓ Filtering for relevance to microsoft/autogen...
✓ 18 sources retained after filtering
✓ NotebookLM notebook created: notebook_abc12345xyz
✓ Indexing (75s timeout)...
✓ Analysis complete (11 questions answered)
✓ Brief written
```

---

## Report Output

**Brief file**: `Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.md`

**Notebook ID** (for manual follow-up): `notebook_abc12345xyz`  
Open at: https://notebooklm.google.com

**Content Gaps Identified** (from simulated brief):

1. **microsoft/autogen** — "Building Production Agent Orchestration Systems"
   - Gap: While AutoGen is well-documented, there's sparse content on productionizing multi-agent workflows at scale
   - **Recommended Video Angle**: "How to Ship Agent Orchestration: AutoGen Patterns in Production"
   - Source diversity: Mostly official docs (7) + conference talks (4) + GitHub discussions (5)

---

## Next Step

Once you've reviewed the brief, run:
```
/hook topic="How to Ship Agent Orchestration: AutoGen Patterns in Production"
```

This kicks off the hook research phase (deep-dive into the specific video angle).

---

## Files Written

- `Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.md` ← Main output
- `Content-Hub-Vault-V2/10-Research/2026-05-15_ai-agents_brief.frontmatter` ← Notebook IDs (internal)
