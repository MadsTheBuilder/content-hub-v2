---
slug: phase3c-title-skill
created: 2026-05-07
status: complete
current_group: null
groups_complete: [1, 2, 3]
specialists_involved: [research-agent, pipeline-agent]
---

# Orchestration: Phase 3c — Title Skill

## Recon Summary

- `backend/research/apify_client.py`: async `scrape_profiles(workflow_id, platform, usernames)` returns list of dicts per video — keys include title, view_count, author_username (up to 30 per call, sorted by organic_score). YouTube actor: `streamers~youtube-scraper`, maxResults=20 per profile, builds start_urls as `https://www.youtube.com/@{username}`.
- `skills/` has 8 existing modules (cascade.py, short_form.py, yt_pipeline.py, researcher.py, ideation.py, hook.py, outline.py, voice_cleanup.py) + `utils/` (ai.py, vault.py). Module invoked as `python -m skills.<name>`.
- `prompts/` has 8 matching .md templates; `skills/utils/ai.py` provides cascade helpers but task requires direct anthropic SDK call.
- `.claude/skills/` has 13 skill directories. SKILL.md format: H1 command, description, Trigger, Execution Steps, Output, After Completion, Usage Examples.
- `skills/data/` does NOT exist — must be created.
- `Content-Hub-Vault-V2/07-Titles/` EXISTS.
- `.env` has both `APIFY_API_TOKEN` and `APIFY_API_KEY` — agent must read apify_client.py to confirm which key name it reads.
- `anthropic==0.39.0` in requirements.txt; importable.

## Execution Plan

**Tasks:** 4 across 3 groups
**Specialists:** research-agent, pipeline-agent

### Group 1 (parallel)

- [research-agent | MEDIUM] Scrape competitor channels → write data file
  Files: CREATE `scripts/scrape_competitor_titles.py`, CREATE `skills/data/competitor_titles.json`
  Criteria: JSON exists, valid array, each entry {title: str, view_count: int, channel: str}, sorted by view_count desc, ≥1 non-empty entry

- [pipeline-agent | EASY] Create title prompt template
  Files: READ `prompts/cascade.md`; CREATE `prompts/title.md`
  Criteria: Has {competitor_titles} and {concept} placeholders; output = 5 Tier-1 (cite pattern) + 5 Tier-2 (A/B risk flag) + thumbnail text per title; tone fits technical AI/dev channel

### Group 2 (depends on Group 1)

- [pipeline-agent | MEDIUM] Create title skill Python module
  Files: READ `skills/cascade.py`, `prompts/title.md`, `skills/data/competitor_titles.json`, `requirements.txt`; CREATE `skills/title.py`
  Criteria: `python -m skills.title "[concept]"` reads JSON top-30, calls Claude (anthropic SDK, claude-haiku-4-5-20251001), writes `Content-Hub-Vault-V2/07-Titles/YYYY-MM-DD_<slug>.md`, prints path

### Group 3 (depends on Group 2)

- [pipeline-agent | EASY] Create title SKILL.md
  Files: READ `.claude/skills/cascade/SKILL.md`; CREATE `.claude/skills/title/SKILL.md`
  Criteria: Triggers on `/title [concept]`, runs `python -m skills.title "[concept]"`, reports vault path; matches existing SKILL.md format

## Agent Prompts

### Task: research-agent: Scrape competitor channels → skills/data/competitor_titles.json

- description: "research-agent: scrape competitor channels → skills/data/competitor_titles.json"
- model: sonnet
- prompt: |
    You are the research-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Scrape two competitor YouTube channels using the existing apify_client and write a JSON data file at `skills/data/competitor_titles.json`.

    Channels:
    - username: nateherk   (https://www.youtube.com/@nateherk)
    - username: Chase-H-AI (https://www.youtube.com/@Chase-H-AI)

    ## Scope
    Read for context: `backend/research/apify_client.py`, `requirements.txt`
    Create: `scripts/scrape_competitor_titles.py`, `skills/data/competitor_titles.json`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## Steps
    1. Read `backend/research/apify_client.py` in full — note the exact import path, whether scrape_profiles is a module-level function or class method, and which env var it uses for the Apify key (APIFY_API_TOKEN or APIFY_API_KEY).
    2. Read `requirements.txt` — confirm the dotenv package name (python-dotenv → `from dotenv import load_dotenv`).
    3. Write `scripts/scrape_competitor_titles.py`:
       ```python
       import asyncio, json, os, sys
       sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
       from dotenv import load_dotenv
       load_dotenv()
       # Import scrape_profiles — match whatever you found in step 1
       from backend.research.apify_client import scrape_profiles  # adjust if class method

       async def main():
           r1 = await scrape_profiles("competitor-research", "youtube", ["nateherk"])
           r2 = await scrape_profiles("competitor-research", "youtube", ["Chase-H-AI"])
           merged = r1 + r2
           titles = [
               {"title": p["title"], "view_count": p.get("view_count", 0), "channel": p.get("author_username", "")}
               for p in merged if p.get("title")
           ]
           titles.sort(key=lambda x: x["view_count"], reverse=True)
           titles = titles[:60]
           os.makedirs("skills/data", exist_ok=True)
           with open("skills/data/competitor_titles.json", "w") as f:
               json.dump(titles, f, indent=2)
           print(f"Written {len(titles)} titles to skills/data/competitor_titles.json")

       if __name__ == "__main__":
           asyncio.run(main())
       ```
       Adjust the import if scrape_profiles is a class method (instantiate with API key, then call).
    4. Run from project root: `python scripts/scrape_competitor_titles.py`
    5. Verify the file exists: print first 3 entries.

    ## Acceptance Criteria
    1. `skills/data/competitor_titles.json` exists
    2. Valid JSON array
    3. Each entry: {title: str, view_count: int or float, channel: str}
    4. At least 1 entry with non-empty title

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but issues found (explain)
    - STUCK: Cannot proceed (explain)
    - NEEDS_CONTEXT: Need information (specify)

    Include a summary of what you changed and why.

### Task: pipeline-agent: Create prompts/title.md

- description: "pipeline-agent: create prompts/title.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `prompts/title.md` — the prompt template for the title skill.

    ## Scope
    Read for context: `prompts/cascade.md`
    Create: `prompts/title.md`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## What to write
    A prompt template for generating YouTube titles for a technical AI/dev channel.
    Must include:
    - Role framing: expert YouTube title strategist, technical AI/dev channel audience
    - Competitor analysis instruction: "Below are the top-performing titles from competitor channels. Identify patterns: structure (How I / The X that / Why / number lists), length, power words, specificity vs curiosity gaps."
    - `{competitor_titles}` placeholder — will be substituted at runtime with a numbered list
    - `{concept}` placeholder — the video concept
    - Output format (exact headers):

    ### Tier-1 Titles (Safe, High-Confidence)
    5 titles optimised for reliability. Each:
    - **Title text**
    - Pattern match: [competitor pattern echoed]

    ### Tier-2 Titles (A/B Risk — Experimental)
    5 higher-risk, higher-reward titles. Each:
    - **Title text**
    - Risk: [what makes this an A/B bet]

    ### Thumbnail Text
    For each of the 10 titles, 2–4 words for the thumbnail overlay (bold, readable at small size).

    ## Acceptance Criteria
    1. `prompts/title.md` exists
    2. Contains `{competitor_titles}` placeholder
    3. Contains `{concept}` placeholder
    4. Output format has Tier-1 (5 titles + pattern), Tier-2 (5 titles + risk), Thumbnail Text sections

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but issues (explain)
    - STUCK: Cannot proceed (explain)

    Include a summary of what you wrote.

### Task: pipeline-agent: Create skills/title.py

- description: "pipeline-agent: create skills/title.py"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `skills/title.py` — the runtime title generation module.

    ## Scope
    Read for context: `skills/cascade.py`, `prompts/title.md`, `skills/data/competitor_titles.json`, `requirements.txt`
    Create: `skills/title.py`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## CLI interface
    `python -m skills.title "video concept string"`

    ## Implementation
    1. Read `skills/cascade.py` for structure patterns (imports, vault path building, CLI args).
    2. Read `skills/data/competitor_titles.json` at runtime — load full list, slice top 30.
    3. Format top-30 as numbered list for the prompt:
       `1. "Title here" — 1,234,567 views (@channel)`
    4. Load `prompts/title.md` (relative to project root).
    5. Substitute `{competitor_titles}` and `{concept}` in the prompt text.
    6. Call Claude via the Claude Code CLI (no API key — uses Pro plan CLI auth):
       ```python
       import subprocess
       result = subprocess.run(
           ["claude", "-p", prompt_text],
           capture_output=True, text=True
       )
       if result.returncode != 0:
           raise RuntimeError(f"claude CLI failed: {result.stderr}")
       output = result.stdout.strip()
       ```
    7. Build slug: lowercase concept, replace non-alphanumeric with hyphens, collapse consecutive hyphens, strip ends, max 50 chars.
    8. Output path: `Content-Hub-Vault-V2/07-Titles/{date}_{slug}.md`
    9. Write with YAML frontmatter:
       ```
       ---
       concept: {concept}
       date: {date}
       ---

       {claude output}
       ```
    10. Create directory if needed (os.makedirs exist_ok=True).
    11. Print the output path to stdout.
    12. `if __name__ == "__main__":` guard with sys.argv[1] as concept.

    Load `.env` at the top of the module (dotenv), so ANTHROPIC_API_KEY and other env vars are available.

    ## Acceptance Criteria
    1. `skills/title.py` exists
    2. `python -m skills.title "concept"` runs without import errors
    3. Reads skills/data/competitor_titles.json (top 30)
    4. Calls anthropic SDK
    5. Writes Content-Hub-Vault-V2/07-Titles/YYYY-MM-DD_<slug>.md
    6. Prints vault path

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but issues (explain)
    - STUCK: Cannot proceed (explain)
    - NEEDS_CONTEXT: Need information (specify)

    Include a summary of what you wrote.

### Task: pipeline-agent: Create .claude/skills/title/SKILL.md

- description: "pipeline-agent: create .claude/skills/title/SKILL.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `.claude/skills/title/SKILL.md` — the Claude Code skill definition for /title.

    ## Scope
    Read for context: `.claude/skills/cascade/SKILL.md`
    Create: `.claude/skills/title/SKILL.md`

    IMPORTANT: Only touch the files listed above.

    ## What it should define
    - Trigger: user types `/title [concept]`
    - Execution: `python -m skills.title "[concept]"` — quote the concept to handle spaces
    - Reports the vault output path after execution
    - Mentions the output directory: `Content-Hub-Vault-V2/07-Titles/`

    ## Acceptance Criteria
    1. `.claude/skills/title/SKILL.md` exists
    2. Defines /title trigger
    3. Execution step runs `python -m skills.title "[concept]"` (quoted)
    4. Reports vault path
    5. Format matches existing SKILL.md convention

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but issues (explain)
    - STUCK: Cannot proceed (explain)

    Include a summary of what you wrote.

## Status log
- 2026-05-07 created, status=awaiting-approval
- 2026-05-07 approved (correction: claude CLI via subprocess, not anthropic SDK), status=approved
- 2026-05-07 all 3 groups complete; /title verified end-to-end; shell=True + encoding=utf-8 patch applied; status=complete
