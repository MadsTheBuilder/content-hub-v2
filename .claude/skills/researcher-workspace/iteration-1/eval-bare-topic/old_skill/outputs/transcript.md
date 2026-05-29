# Eval 2 — Bare Topic (old_skill)

## Prompt
```
/researcher AI agents
```

## Skill Content
The old SKILL.md specifies that:
1. User provides a niche (inline or via prompt) ✓ User provided: "AI agents"
2. List available repos via `python -m skills.researcher --list`
3. Show the list to the user and ask which repos they want to research
4. Wait for user to specify repos
5. Confirm the selection before running
6. Run the researcher with `--niche` and `--repos` flags
7. Report the output file path and "Recommended Video Angle" from each repo

The skill emphasizes that **the skill never auto-selects** — the user must explicitly pick which repos to research.

## Command Attempted
```
python -m skills.researcher --list
```

**Result:** Command succeeded. Available repos (9 total):
1. yaojingang/yao-open-prompts
2. lightseekorg/tokenspeed
3. TitanFlow-Systems/best-of-algorithmic-trading
4. kyegomez/OpenMythos
5. Manavarya09/design-extract
6. earthtojake/text-to-cad
7. crynta/terax-ai
8. cosmicstack-labs/mercury-agent
9. nexu-io/open-design

## Response

Got it — I'll run isolated content gap research on **AI agents**.

Here are the 9 available repos from the trending list:

```
1. yaojingang/yao-open-prompts
2. lightseekorg/tokenspeed
3. TitanFlow-Systems/best-of-algorithmic-trading
4. kyegomez/OpenMythos
5. Manavarya09/design-extract
6. earthtojake/text-to-cad
7. crynta/terax-ai
8. cosmicstack-labs/mercury-agent
9. nexu-io/open-design
```

**Which repos would you like me to research for the "AI agents" niche?**

I recommend picking 2–3 that feel most relevant to agents specifically. For example, if you want frameworks, `kyegomez/OpenMythos` or `cosmicstack-labs/mercury-agent` might be a good fit. If you want multi-agent systems, `crynta/terax-ai` could work.

Just tell me the repo numbers or names, and I'll confirm before running the research (~5–8 minutes depending on mode).
