<div align="center">

# Content Hub V2

**A local-first content production engine. Research → script, in 7 slash-commands.**

</div>

<p align="center">
  <img alt="License" src="https://img.shields.io/badge/license-Private-lightgrey">
  <img alt="Stage" src="https://img.shields.io/badge/status-active--development-brightgreen">
  <img alt="Runtime" src="https://img.shields.io/badge/runtime-Claude%20Code-blueviolet">
</p>

## Install

Requires [Claude Code](https://claude.com/claude-code) and Python 3.11+.

```bash
git clone https://github.com/MadsTheBuilder/content-hub-v2.git
cd content-hub-v2
pip install -r requirements.txt
claude
```

Or launch the control room directly:

```bash
bin\run_control_room.bat
```

## What it does

Content Hub V2 turns a trending topic into a finished long-form script — plus every asset needed to distribute it — without ever touching a render pipeline. It's modeled on Chase AI's 10M-views workflow: **9 deliverables per video**, produced by chaining 7 Claude Code skills, each one reading the previous stage's output from a shared Obsidian vault instead of a database.

It stops at the script. No video rendering, no publishing — that part stays a human decision.

## The pipeline

```
/researcher → /ideation → /hook → /outline → /cascade → /short-form → /voice-cleanup
```

| Stage | Command | Produces |
|---|---|---|
| 1. Research | `/researcher` | Dated research brief from GitHub trending repos + NotebookLM deep dives |
| 2. Ideation | `/ideation` | 9 ranked video ideas with gap analysis and audience-desire mapping |
| 3. Hook | `/hook` | 5 Kallaway-trained hook variations for the first 30 seconds |
| 4. Outline | `/outline` | Full Dopamine Ladder script outline |
| 5. Distribution | `/cascade` | Blog post + Twitter/X thread + LinkedIn post |
| 6. Short-form | `/short-form` | 30s / 60s / 90s vertical scripts |
| 7. Voice cleanup | `/voice-cleanup` | Final pass in Madhur's voice |

`/title` (10 title options) and `/yt-pipeline` (single YouTube URL → full teardown) are one-shot helpers that plug into any stage.

## Architecture

Every stage follows the same two-layer skill pattern:

```
.claude/skills/<name>/SKILL.md   ← Claude Code entry point (the /<name> trigger)
skills/<name>.py                 ← Python helper — calls the model(s), writes to the vault
prompts/<name>.md                ← Single source of truth for prompt text
```

Stages don't talk to each other directly. Each one reads its input from the previous stage's folder in `Content-Hub-Vault-V2/` and writes its own output there — the vault is the interface.

**Cost-aware model routing** (`skills/utils/ai.py`, the only place a provider is ever called):

- **Ollama** (local, free) — first-draft outlines, structural work
- **Claude** (paid) — hooks, titles, voice cleanup, final polish
- **Gemini** — kept wired for tools that already use it (research)

## Tune it

Fork it and make it yours:

- Prompt text lives entirely in `prompts/*.md` — edit those before touching any Python.
- Vault structure and management rules are documented in `CLAUDE.md` and `Content-Hub-Vault-V2/00-Management-V2/`.
- Agent/domain ownership (which specialist owns which files) is in `AGENTS.md` — read it before delegating work across the pipeline, the webapp, or the vault.
- A minimal FastAPI + React control-room UI lives in `Design-doc/` if you'd rather drive stages from a browser than the CLI.

## Credits

Pipeline structure and hook methodology adapted from Chase AI's long-form YouTube workflow. Built and run by [Madhur](mailto:befitwithmads@gmail.com) as the active fork of V1 (parked, SaaS-stack version) — see `CLAUDE.md` for the V1→V2 pivot rationale.

## License

Private project — not currently licensed for external use or redistribution.
