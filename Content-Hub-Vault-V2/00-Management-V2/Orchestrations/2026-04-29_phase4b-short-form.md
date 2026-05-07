---
slug: phase4b-short-form
created: 2026-04-29
status: complete
current_group: null
groups_complete: []
specialists_involved: [pipeline-agent]
---

# Orchestration: Phase 4b — `/short-form` Skill Build

## Recon summary

- `skills/utils/ai.py` — AI router with `generate()`, `draft()`, `polish()`. Gemini Flash → Ollama → Claude cascade. All new skills use this.
- `Content-Hub-Vault-V2/09-Shorts/` — exists, empty (only .gitkeep). Ready for output.
- `skills/cascade.py` — reference implementation: extract_transcript() via yt_dlp, load_prompts() splits by `## SECTION` headers, `generate()` for each section, writes to vault.
- `prompts/cascade.md` — uses 3 `## SECTION NAME` headers to split prompt templates. Same pattern for short_form.md.
- Naming convention: `YYYY-MM-DD_<slug>/` directories with per-format markdown files inside.
- Existing SKILL.md pattern: `.claude/skills/cascade/SKILL.md` — no frontmatter, plain markdown, ## Trigger + numbered steps.
- Phase 4a orchestration (`2026-04-29_phase4a-cascade.md`) complete — cascade skill confirmed working.
- No file conflicts: all 3 new files (`prompts/short_form.md`, `.claude/skills/short-form/SKILL.md`, `skills/short_form.py`) are independent.

## Execution plan

```
## Execution Plan: Phase 4b — /short-form Skill

**Tasks:** 4 across 3 groups
**Specialists:** pipeline-agent

### Group 1 (parallel)
- [pipeline-agent | EASY] Create prompts/short_form.md
  Files: prompts/short_form.md (create)
  Criteria:
  1. Three sections with exact headers: ## 30 SECOND SCRIPT, ## 60 SECOND SCRIPT, ## 90 SECOND SCRIPT
  2. Each section specifies: role (vertical video scriptwriter), voice guidelines (same banned phrases as cascade.md), word count targets (30s≈75-90w, 60s≈150-180w, 90s≈225-270w)
  3. Each section's output format includes: SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION
  4. Opening hook (3-4 seconds) is the first element — stops the scroll
  5. Placeholders: {title}, {transcript}

- [pipeline-agent | EASY] Create .claude/skills/short-form/SKILL.md
  Files: .claude/skills/short-form/SKILL.md (create)
  Criteria:
  1. Matches cascade/SKILL.md format (no YAML frontmatter, plain markdown)
  2. ## Trigger: /short-form <YouTube URL>
  3. Documents: confirm URL → run python -m skills.short_form <url> → report 3 output files
  4. Output section: 30s_script.md, 60s_script.md, 90s_script.md in Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/
  5. Notes: re-scripted for vertical format (not clipped), review before recording

### Group 2 (depends on Group 1)
- [pipeline-agent | MEDIUM] Create skills/short_form.py
  Files: skills/short_form.py (create)
  Read for context: skills/cascade.py, skills/utils/ai.py, prompts/short_form.md
  Criteria:
  1. CLI: python -m skills.short_form <youtube_url> [--title "..."]
  2. Transcript extraction: reuse extract_transcript() pattern from cascade.py (yt_dlp, VTT parsing, dedup)
  3. Prompt loading: read prompts/short_form.md, split by ## 30 SECOND SCRIPT / ## 60 SECOND SCRIPT / ## 90 SECOND SCRIPT headers
  4. Generation: call generate() 3 times (one per duration) with {title} and {transcript} filled in
  5. Output: Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/ with 30s_script.md, 60s_script.md, 90s_script.md, README.md
  6. README.md: metadata + review checklist per script
  7. File ≤ 180 lines, async main, argparse, Path — match cascade.py style

### Group 3 (depends on Group 2)
- [pipeline-agent | MEDIUM] Smoke test + verification
  Files: Content-Hub-Vault-V2/09-Shorts/ (verify output created)
  Criteria:
  1. python -m skills.short_form --help runs without error
  2. Run against Kallaway top video: https://www.youtube.com/watch?v=h_yQswsXwhY
  3. Three files created: 30s_script.md, 60s_script.md, 90s_script.md
  4. Each file contains SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION sections
  5. Word counts are plausible: 30s < 60s < 90s
  6. No AI-isms in the output (no "Let's dive in", "game-changer", etc.)
  7. README.md created with correct metadata
```

## Agent prompts

### Task: pipeline-agent: Create prompts/short_form.md

- description: "pipeline-agent: Create prompts/short_form.md"
- model: sonnet
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    Your domain: content generation pipeline. You write Python helpers and prompt files for Claude Code skills.

    ## Your Task

    Create `prompts/short_form.md` at `c:\Users\madhu\Claude cowork\Content Hub V2\prompts\short_form.md`.

    This file drives the `/short-form` skill: given a YouTube video transcript, generate scripts for 30, 60, and 90 second vertical videos. This is NOT clipping — it's re-scripting the core insight for the vertical format.

    ## Scope
    Read for context: prompts/cascade.md (to match voice guidelines and section format)
    Create: prompts/short_form.md

    ## What to write

    The file must have 3 clearly separated sections with these EXACT headers (the parser splits on them):
    - `## 30 SECOND SCRIPT`
    - `## 60 SECOND SCRIPT`
    - `## 90 SECOND SCRIPT`

    Each section is a complete, standalone system prompt with:

    **Role:** You are a vertical video scriptwriter specialising in AI tools and developer productivity content. You write short-form scripts that re-package a single core insight from a longer video — not a summary, not a clip, but a self-contained piece built for the format.

    **Voice guidelines (embed in every section):**
    - Direct, practical, no fluff. Short sentences. Active voice.
    - Sound like a practitioner talking to practitioners — specific, opinionated, useful.
    - Banned phrases: "Let's dive in", "it's not X it's Y", "game-changer", "revolutionize", "in today's fast-paced world", "leverage", "cutting-edge", "unleash", "seamless", "robust", "paradigm shift", "delve into", "it's worth noting", "as we navigate"
    - No rhetorical questions as hooks. Open with a statement or a contrarian take.
    - The hook is the first 3-4 seconds — it must stop the scroll. State the payoff immediately.

    **Per-section specs:**

    30-second section:
    - Word count: 75-90 words spoken (at natural pace ≈ 150 wpm)
    - Structure: hook (1 sentence, 3-4 seconds) → single core insight (2-3 sentences) → micro-CTA (1 sentence)
    - Focus: pick the ONE most surprising or counterintuitive idea from the transcript

    60-second section:
    - Word count: 150-180 words spoken
    - Structure: hook → problem/tension (2-3 sentences) → insight + proof (3-4 sentences) → CTA
    - Focus: the strongest idea with enough context to make it land

    90-second section:
    - Word count: 225-270 words spoken
    - Structure: hook → problem → insight → supporting detail or example → CTA
    - Focus: a mini-narrative arc — setup, turn, resolution

    **Output format for each script (embed this in all 3 sections):**

    Each generated script must use this format:
    ```
    **SPOKEN SCRIPT:**
    [Word-for-word script, written to be read aloud]

    **TEXT OVERLAYS:**
    [2-4 on-screen text lines that reinforce key points — these appear while speaking]

    **CAPTION:**
    [1-2 sentence post caption for the vertical platform]
    ```

    **Placeholders:** {title} and {transcript} — include both in every section.

    ## Acceptance Criteria
    1. File exists at prompts/short_form.md
    2. Contains exactly 3 sections with the specified ## headers
    3. Each section has {title} and {transcript} placeholders
    4. Voice guidelines and banned phrases are embedded
    5. Output format (SPOKEN SCRIPT / TEXT OVERLAYS / CAPTION) is specified in each section
    6. Word count targets are specified per section

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but with doubts (explain)
    - STUCK: Cannot proceed (explain)

    Include a brief summary of what you wrote.

---

### Task: pipeline-agent: Create .claude/skills/short-form/SKILL.md

- description: "pipeline-agent: Create .claude/skills/short-form/SKILL.md"
- model: sonnet
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    ## Your Task

    Create `.claude/skills/short-form/SKILL.md` at `c:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\short-form\SKILL.md`.

    First, read `.claude/skills/cascade/SKILL.md` to understand the exact format and pattern used.

    This SKILL.md defines the `/short-form` slash command: given a YouTube URL, re-script the core insight into 30, 60, and 90 second vertical video scripts written to the Obsidian vault.

    ## Scope
    Read for context: .claude/skills/cascade/SKILL.md
    Create: .claude/skills/short-form/SKILL.md (create directory if needed)

    ## What to write

    Match the cascade SKILL.md format exactly (no frontmatter, plain markdown, ## sections).

    Key details:
    - Trigger: `/short-form <YouTube URL>` or `/short-form` then ask for URL
    - Before running: confirm the URL with the user
    - Command: `python -m skills.short_form <url>`
    - Output: 3 script files in `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`
      - `30s_script.md` — 30-second vertical script
      - `60s_script.md` — 60-second vertical script
      - `90s_script.md` — 90-second vertical script
      - `README.md` — metadata and review checklist

    Include:
    - ## Trigger section
    - Step-by-step numbered execution flow
    - ## Output section documenting the 4 files and their vault path
    - ## After Completion section: report path + one-line preview of the 30s hook
    - ## Usage Examples (at least 2)
    - ## Notes: scripts are re-written for vertical format (NOT clipped), review before recording

    ## Acceptance Criteria
    1. File exists at .claude/skills/short-form/SKILL.md
    2. Matches cascade SKILL.md format (no YAML frontmatter, plain markdown)
    3. Documents exact CLI command to run
    4. Documents all 4 output files and vault path (09-Shorts)
    5. Notes section explains re-scripting vs clipping distinction
    6. At least 2 usage examples

    ## When done
    Report DONE / DONE_WITH_CONCERNS / STUCK with summary.

---

### Task: pipeline-agent: Create skills/short_form.py

- description: "pipeline-agent: Create skills/short_form.py"
- model: sonnet
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    Your domain: content generation pipeline. Python helpers that drive Claude Code skills.

    ## Your Task

    Create `skills/short_form.py` to implement the V2 `/short-form` skill.

    This skill takes a YouTube URL, extracts the transcript, and generates word-for-word scripts for 30, 60, and 90 second vertical videos. It is NOT a clipping tool — it re-scripts the core insight for each format.

    ## Scope
    Read for context: skills/cascade.py, skills/utils/ai.py, prompts/short_form.md
    Create: skills/short_form.py

    **Project root:** `c:\Users\madhu\Claude cowork\Content Hub V2\`

    ## Implementation requirements

    ### CLI interface
    ```
    python -m skills.short_form <youtube_url> [--title "Optional override title"]
    ```

    ### Transcript extraction
    Reuse the exact same extract_transcript() pattern from cascade.py:
    - Uses yt_dlp Python API (not subprocess)
    - writeautomaticsub, subtitleslangs=["en"], subtitlesformat="vtt", skip_download=True
    - Parse VTT: strip WEBVTT header, timestamps (-->), numeric cue IDs, HTML tags
    - Deduplicate consecutive identical lines
    - Return (transcript_text, video_title)

    You may copy this function verbatim from cascade.py — it's the established pattern.

    ### Prompt loading
    Read `prompts/short_form.md` and split by section headers:
    - `## 30 SECOND SCRIPT` → script_30_prompt template
    - `## 60 SECOND SCRIPT` → script_60_prompt template
    - `## 90 SECOND SCRIPT` → script_90_prompt template

    Fill placeholders: {title} and {transcript} (truncate transcript to 4000 chars).

    ### Generation
    Use `from skills.utils.ai import generate`.
    Generate all 3 scripts sequentially (simple, avoids race conditions).
    Print progress between each generation.

    ### Output directory
    `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`
    Where slug = title lowercased, spaces→hyphens, non-alphanumeric stripped, max 40 chars.
    (Same slugify logic as cascade.py)

    ### Output files
    - `30s_script.md` — frontmatter: title, date, youtube_url, duration=30s + script content
    - `60s_script.md` — same frontmatter + script content
    - `90s_script.md` — same frontmatter + script content
    - `README.md` — metadata + per-script review checklist

    README.md format:
    ```
    # Short Form Scripts — {title}

    **Date:** {today}
    **Video:** {youtube_url}

    ## Scripts
    - `30s_script.md` — 30-second vertical script
    - `60s_script.md` — 60-second vertical script
    - `90s_script.md` — 90-second vertical script

    ## Checklist
    - [ ] Review 30s_script.md → record
    - [ ] Review 60s_script.md → record
    - [ ] Review 90s_script.md → record
    ```

    ### Style constraints
    - Match cascade.py style: asyncio main, argparse, Path, logging
    - Keep under 180 lines — no over-engineering
    - Handle missing transcript: print error + sys.exit(1)
    - Print progress at each step (extracting, generating 30s/60s/90s, done)
    - Reconfigure stdout encoding at top (same as cascade.py)

    ## Acceptance Criteria
    1. `python -m skills.short_form --help` runs without error
    2. extract_transcript() function exists and parses VTT correctly
    3. load_prompts() reads prompts/short_form.md and returns 3 templates
    4. Output goes to Content-Hub-Vault-V2/09-Shorts/ (not output/ dir)
    5. All 4 files written with correct names
    6. File is ≤ 180 lines
    7. Matches cascade.py code style

    ## When done
    Report DONE / DONE_WITH_CONCERNS / STUCK with summary of what you created.

---

### Task: pipeline-agent: Smoke test + verify /short-form

- description: "pipeline-agent: Smoke test /short-form"
- model: sonnet
- prompt: |
    You are the pipeline-agent for Content Hub V2. Your task is to smoke test the newly created `/short-form` skill.

    **Project root:** `c:\Users\madhu\Claude cowork\Content Hub V2\`

    ## Your Task

    Run the smoke test for `skills/short_form.py` and verify all acceptance criteria pass.

    ## Scope
    Read for context: skills/short_form.py, prompts/short_form.md, .claude/skills/short-form/SKILL.md
    Run: python -m skills.short_form (from project root)
    Verify: Content-Hub-Vault-V2/09-Shorts/ output

    ## Smoke test steps

    1. First run --help to verify CLI is correctly wired:
       ```
       cd "c:\Users\madhu\Claude cowork\Content Hub V2" && python -m skills.short_form --help
       ```

    2. Run against the Kallaway top video (same URL used for cascade smoke test):
       ```
       python -m skills.short_form https://www.youtube.com/watch?v=h_yQswsXwhY
       ```

    3. After completion, verify:
       - A new directory exists in Content-Hub-Vault-V2/09-Shorts/ named YYYY-MM-DD_<slug>/
       - 30s_script.md exists and contains SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION sections
       - 60s_script.md exists and contains SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION sections
       - 90s_script.md exists and contains SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION sections
       - README.md exists with metadata and checklist
       - Word count of 30s script < 60s script < 90s script (approximate check — read files)
       - No obvious AI-isms ("Let's dive in", "game-changer", "revolutionize") in any script

    4. Read all 3 script files and include the opening line of each in your report.

    ## If you hit errors

    - Import errors: check that skills/short_form.py is in the right location and the module path is correct
    - yt-dlp failures: check if yt-dlp is installed (`python -c "import yt_dlp"`)
    - Prompt parsing failures: check section headers in prompts/short_form.md match what short_form.py expects
    - API errors from generate(): check .env for API keys

    ## Acceptance Criteria
    1. `--help` runs without error
    2. Script runs to completion without crashing
    3. All 4 output files exist in 09-Shorts/
    4. Each script file contains SPOKEN SCRIPT, TEXT OVERLAYS, CAPTION sections
    5. Word counts are plausible (30s shortest, 90s longest)
    6. No obvious AI-isms in the output

    ## When done
    Report DONE / DONE_WITH_CONCERNS / STUCK with:
    - Which criteria passed/failed
    - Opening line of 30s, 60s, and 90s scripts (to verify quality)
    - Path to the output directory

## Status log
- 2026-04-29 Recon complete, plan written, status=awaiting-approval
- 2026-04-29 User approved, status=approved, current_group=1
- 2026-04-29 Group 1 complete (prompts/short_form.md ✅, .claude/skills/short-form/SKILL.md ✅), current_group=2
- 2026-04-29 Group 2 complete (skills/short_form.py ✅, 180 lines, matches cascade.py style), current_group=3
- 2026-04-29 Group 3 complete — smoke test passed: --help ✅, all 4 files written ✅, word counts 78/138/263 ✅, no AI-isms ✅, status=complete
