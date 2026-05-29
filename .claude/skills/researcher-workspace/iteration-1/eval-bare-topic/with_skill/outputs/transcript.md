# Eval 2 — Bare Topic (with_skill)

## Prompt
```
/researcher AI agents
```

## Skill Content

The `/researcher` skill is Step 1 of the content production pipeline. It:
- Takes a niche/topic from the user (inline or via prompt)
- Lists available GitHub trending repos via `python -m skills.researcher --list`
- Asks the user to select which repos to research
- Confirms the selection before running deep research
- Executes: `python -m skills.researcher --niche "[niche]" --repos owner/repo1 owner/repo2`
- Outputs a timestamped research brief to `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md`
- Each repo gets its own NotebookLM notebook for isolation and source quality
- Always suggests `/hook` as the next step after the brief is reviewed

The skill requires:
- NotebookLM auth at `~/.notebooklm/storage_state.json`
- `Content-Hub-Vault-V2/04-Trends/github_trending.md` to exist with repos
- User explicit repo selection (no auto-selection)

## Command Attempted
```
python -m skills.researcher --list
```

Result: Successfully listed 9 available repos.

## Response

Got it — researching **AI agents**. Let me show you the available repos and you pick which ones to dig into.

Available trending repos:

1. yaojingang/yao-open-prompts
2. lightseekorg/tokenspeed
3. TitanFlow-Systems/best-of-algorithmic-trading
4. kyegomez/OpenMythos
5. Manavarya09/design-extract
6. earthtojake/text-to-cad
7. crynta/terax-ai
8. cosmicstack-labs/mercury-agent
9. nexu-io/open-design

**Which repos would you like me to research?** Pick by number or repo slug — for example, `8 2 4` or `cosmicstack-labs/mercury-agent kyegomez/OpenMythos`.

A few relevant to AI agents I'd flag:
- **#8 (cosmicstack-labs/mercury-agent)** — likely direct fit
- **#4 (kyegomez/OpenMythos)** — might be agent-related
- **#1 (yao-open-prompts)** — could frame agent prompt engineering angles

Pick as few or as many as you want — deep research takes ~8 min per repo, so 2–3 is a good starting point.
