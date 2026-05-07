---
slug: phase3a-3b-hook-outline-skills
created: 2026-05-06
status: complete
current_group: null
groups_complete: []
specialists_involved: [pipeline-agent]
---

# Orchestration: Phase 3a + 3b — Hook & Outline Skills

## Recon Summary

- `skills/hook_writer.py` exists — contains both HOOK_PROMPT (3 variations, curiosity/story/contrarian) and OUTLINE_PROMPT, but writes to `output/YYYY-MM-DD/script.md` (wrong path). Reads Kallaway from V1 Exoskeleton path.
- No `prompts/hook.md` or `prompts/outline.md` exist — prompts are hardcoded inside hook_writer.py, not extracted.
- No `.claude/skills/hook/SKILL.md` or `.claude/skills/outline/SKILL.md` — neither slash command exists.
- `Content-Hub-Vault-V2/05-Hooks/` and `06-Outlines/` both exist but are empty (.gitkeep only).
- `marketing_brain.md` is at `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` — 5 sections: Hook Formulas (10 Kallaway patterns), Storytelling Frameworks (Dopamine Ladder 6 stages), Content Strategy Rules (algorithm mechanics, virality), Personal Brand Architecture, Pacing/Retention/Titles.
- `skills/utils/ai.py` provides `draft()` (Ollama→Gemini), `polish()` (Claude→Gemini), `generate()` (generic cascade). `skills/utils/vault.py` provides vault readers but for V1 Exoskeleton path — new skills must read marketing_brain.md directly via V2 vault path.
- SKILL.md pattern: H1 command name → description → Trigger → Execution Steps → Output section → After Completion template → Usage Examples → Notes. Mirror cascade/ideation/short-form.

## Execution Plan

**Tasks:** 6 across 3 groups
**Specialists:** pipeline-agent

### Group 1 — Prompt files (parallel)

- [pipeline-agent | MEDIUM] Create `prompts/hook.md`
  Files: CREATE `prompts/hook.md`; READ `marketing_brain.md`, `skills/hook_writer.py`, `prompts/ideation.md`
  Criteria: Embeds all 10 Kallaway hook patterns as selectable options; output format is 5 variations each with Spoken Line + Visual Cue + Text Overlay + Pattern name + 1-line rationale; placeholder variables for {topic}, {platform}, {audience}, {format}; grounded in marketing_brain Hook Formulas and Dopamine Ladder opening stages; banned-phrases section from existing prompt conventions.

- [pipeline-agent | MEDIUM] Create `prompts/outline.md`
  Files: CREATE `prompts/outline.md`; READ `marketing_brain.md`, `skills/hook_writer.py`, `prompts/ideation.md`
  Criteria: Uses the Dopamine Ladder 6 stages as structural backbone of the outline; embeds Pacing/Retention rules (Speed to Value, Head Fakes, 7/10 Floor, Comprehension Pacing); includes [B-ROLL] and [SHOW SCREEN] markers in output format; per-section duration targets; placeholder variables for {topic}, {hook}, {target_length}, {platform}; grounded in marketing_brain Content Strategy Rules and Storytelling Frameworks.

### Group 2 — Python skill files (parallel, depends on Group 1)

- [pipeline-agent | MEDIUM] Create `skills/hook.py`
  Files: CREATE `skills/hook.py`; READ `prompts/hook.md`, `skills/hook_writer.py`, `skills/cascade.py`, `skills/utils/ai.py`
  Criteria: Loads `prompts/hook.md` at runtime; reads `marketing_brain.md` from `Content-Hub-Vault-V2/01-Knowledge/` (not V1 Exoskeleton); uses `draft()` for Ollama first pass, `polish()` for Claude final; writes 5 hook variations to `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md` (slug from topic); CLI: `python -m skills.hook "topic" [--platform youtube] [--audience "..."] [--format medium]`; matches code style and async pattern of hook_writer.py and cascade.py.

- [pipeline-agent | MEDIUM] Create `skills/outline.py`
  Files: CREATE `skills/outline.py`; READ `prompts/outline.md`, `skills/hook_writer.py`, `skills/cascade.py`, `skills/utils/ai.py`
  Criteria: Loads `prompts/outline.md` at runtime; reads marketing_brain.md from V2 vault; accepts --hook-path to load hook file content as context; uses `draft()` then `polish()`; writes structured outline to `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`; CLI: `python -m skills.outline "topic" [--hook-path "path/to/hook.md"] [--length 8]`; matches code patterns.

### Group 3 — SKILL.md entry points (parallel, depends on Group 2)

- [pipeline-agent | EASY] Create `.claude/skills/hook/SKILL.md`
  Files: CREATE `.claude/skills/hook/SKILL.md`; READ `.claude/skills/ideation/SKILL.md`, `.claude/skills/cascade/SKILL.md`, `skills/hook.py`
  Criteria: Follows exact SKILL.md format (Trigger, Execution Steps, Output, After Completion, Usage Examples, Notes); describes `/hook topic="..." [platform] [audience] [format]` invocation; output path is `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md`; instructs Claude to run `python -m skills.hook` with correct args.

- [pipeline-agent | EASY] Create `.claude/skills/outline/SKILL.md`
  Files: CREATE `.claude/skills/outline/SKILL.md`; READ `.claude/skills/ideation/SKILL.md`, `.claude/skills/short-form/SKILL.md`, `skills/outline.py`
  Criteria: Same format; describes `/outline topic="..." [--hook-path] [--length]`; output path is `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`; notes that hook-path is optional but recommended for best results.

## Agent Prompts

### Task 1.1: pipeline-agent: Create prompts/hook.md

- description: "pipeline-agent: Create prompts/hook.md"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `prompts/hook.md` — the single source-of-truth prompt file for the `/hook` skill.

    This file will be loaded at runtime by `skills/hook.py` and injected into the LLM call. It must be high-quality, grounded entirely in the Kallaway marketing framework documented in `marketing_brain.md`, not generic YouTube advice.

    ## Scope
    Read for context:
    - `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` — the Kallaway framework (the brain behind all hooks)
    - `skills/hook_writer.py` — existing HOOK_PROMPT embedded at lines ~39–78 (starting point, but expand and improve it)
    - `prompts/ideation.md` — format reference for how prompt files are structured in this project
    - `prompts/cascade.md` — additional format reference

    Create:
    - `prompts/hook.md`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## What the prompt must contain

    1. **Role / context block** — who the LLM is, what this is for (first 30 seconds of a YouTube video).

    2. **Kallaway Hook Formulas** — Embed ALL 10 hook patterns from marketing_brain.md (6-Power-Word Stack, Contrast-Driven Curiosity, Speed to Value, You/Your Pivot, Stated Contrast, Implied Contrast, Visual Stun Gun, Anticipation/Edging, Pain Point Agitation, Shock Value). For each pattern include: name, structure, brief example, when to use. These are the actual frameworks to draw from.

    3. **Dopamine Ladder — Opening Stages** — From marketing_brain.md Storytelling Frameworks, include the first 2 stages (Stimulation, Captivation) as the psychological target the hook must achieve.

    4. **Speed to Value rule** — from marketing_brain.md Pacing/Retention section.

    5. **Banned openers** — "Hey guys", "In this video", "Today we're going to", "Welcome back", "Let's dive in" — start with the payload.

    6. **Input variables** (runtime placeholders):
       - `{topic}` — the video topic
       - `{platform}` — yt-long | yt-shorts | tiktok | reels
       - `{audience}` — who they are
       - `{format}` — short (30–60s) | medium (5–8 min) | long (10–15 min)

    7. **Output format** — exactly 5 hook variations (the sprint requires 5, not 3). For EACH:
       ```
       ### Hook N — [Pattern Name]
       **Spoken Line** (first 3 seconds):
       > ...

       **Visual Cue** (what's on screen):
       > ...

       **Text Overlay:**
       > ...

       **Kallaway Pattern:** [name]
       **Why:** [1 sentence psychological rationale]
       ```
       Mark the recommended hook with ⭐.

    ## Quality bar
    - Every hook pattern should feel like it came from studying Kallaway's actual videos, not from a generic content template.
    - The output format section must be unambiguous — no interpretation required.
    - Length: 80–140 lines is right. Not shorter (too thin), not longer (bloat).
    - Match the style of `prompts/ideation.md` — declarative, numbered, no filler sentences.

    ## Acceptance Criteria
    1. File exists at `prompts/hook.md`
    2. All 10 Kallaway hook patterns from marketing_brain.md are present in the prompt
    3. Dopamine Ladder opening stages (Stimulation, Captivation) are referenced
    4. Output format clearly specifies 5 variations, each with Spoken Line + Visual Cue + Text Overlay + Pattern + Why
    5. Runtime placeholders {topic}, {platform}, {audience}, {format} are present
    6. Banned openers list is included
    7. Style matches other prompts/ files in this project

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of what you created.

### Task 1.2: pipeline-agent: Create prompts/outline.md

- description: "pipeline-agent: Create prompts/outline.md"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `prompts/outline.md` — the single source-of-truth prompt file for the `/outline` skill.

    This file will be loaded at runtime by `skills/outline.py`. It must be grounded in the Kallaway framework from `marketing_brain.md`, specifically using the Dopamine Ladder as the structural backbone of every video outline.

    ## Scope
    Read for context:
    - `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` — focus on: Storytelling Frameworks (Dopamine Ladder 6 stages), Pacing/Retention/Titles, Content Strategy Rules
    - `skills/hook_writer.py` — existing OUTLINE_PROMPT at lines ~80–122 (starting point, expand significantly)
    - `prompts/ideation.md` — format reference
    - `prompts/short_form.md` — additional format reference

    Create:
    - `prompts/outline.md`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## What the prompt must contain

    1. **Role block** — structural planner for YouTube videos, building on the hook (already written).

    2. **Dopamine Ladder as structural backbone** — From marketing_brain.md, embed all 6 stages:
       - Stage 1: Stimulation (Hook — already written, include it)
       - Stage 2: Captivation (Context / why this matters)
       - Stage 3: Anticipation (Promise / what's coming)
       - Stage 4: Validation (Proof / demonstration / case study)
       - Stage 5: Affection (Personal connection / creator's take)
       - Stage 6: Revelation (Payoff / insight / transformation)
       Each stage maps to an outline section. The LLM should know which stage it's building.

    3. **Pacing/Retention rules** (from marketing_brain.md):
       - Speed to Value
       - Head Fakes (plant a fake expectation, then subvert it for engagement)
       - 7/10 Quality Floor (every section must be at least 7/10 interesting)
       - Comprehension Pacing (don't assume knowledge, don't over-explain)

    4. **B-roll and screen markers** — instruct use of [B-ROLL: description], [SHOW SCREEN: what], [TEXT OVERLAY: text] markers throughout.

    5. **Input variables**:
       - `{topic}`
       - `{hook}` — the hook text from /hook output
       - `{target_length}` — in minutes (e.g., 8)
       - `{platform}` — yt-long | yt-shorts

    6. **Output format** — one section per Dopamine Ladder stage:
       ```
       ## [Stage N: Stage Name] — [target duration, e.g., 1:30]

       **Dopamine goal:** [Stimulation | Captivation | Anticipation | Validation | Affection | Revelation]

       **Talking points:**
       - ...
       - ...

       **Visual notes:**
       [B-ROLL: ...] or [SHOW SCREEN: ...]

       **Transition to next section:**
       ...
       ```

    7. **CTA section** — always last, 30–45 seconds, must give viewer a reason to watch the next video.

    ## Quality bar
    - The Dopamine Ladder is the main framework here — it should be explicitly named and used, not hidden.
    - Output format must make it clear which Dopamine stage each section serves.
    - Length: 90–150 lines.
    - Match style of other prompts/ files.

    ## Acceptance Criteria
    1. File exists at `prompts/outline.md`
    2. All 6 Dopamine Ladder stages from marketing_brain.md are present and mapped to outline sections
    3. Pacing rules (Speed to Value, Head Fakes, 7/10 Floor, Comprehension Pacing) are embedded
    4. [B-ROLL], [SHOW SCREEN], [TEXT OVERLAY] marker conventions are defined
    5. Runtime placeholders {topic}, {hook}, {target_length}, {platform} are present
    6. CTA section is defined
    7. Style matches other prompts/ files

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT
    Include a summary of what you created.

### Task 2.1: pipeline-agent: Create skills/hook.py

- description: "pipeline-agent: Create skills/hook.py"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `skills/hook.py` — the standalone Python skill backing the `/hook` slash command.

    This is the execution layer: it loads the prompt from `prompts/hook.md`, injects runtime inputs, calls the AI cascade, and writes the output to the vault.

    ## Scope
    Read for context:
    - `prompts/hook.md` — the prompt file this skill loads (already created by another agent)
    - `skills/hook_writer.py` — existing combined hook+outline file; pattern reference for imports, async structure, argparse, AI calls
    - `skills/cascade.py` — best pattern reference for how production skills are structured
    - `skills/utils/ai.py` — to understand draft() and polish() signatures

    Create:
    - `skills/hook.py`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## What skills/hook.py must do

    1. **Load prompt** — read `prompts/hook.md` from the project root at startup. Inject runtime variables into the template ({topic}, {platform}, {audience}, {format}) using str.format() or similar.

    2. **Read marketing_brain for context** — load `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` as supplemental context injected into the prompt (the full Kallaway brain). Path relative to PROJECT_ROOT (defined as `Path(__file__).parent.parent`).

    3. **AI cascade**:
       - `draft()` — Ollama → Gemini first pass (cheap)
       - `polish()` — Claude → Gemini final pass (premium quality)
       - If --no-polish flag: skip polish, return draft only

    4. **Output** — write to `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md` where slug is a kebab-case version of the topic (max 6 words). File format:
       ```markdown
       ---
       topic: {topic}
       platform: {platform}
       audience: {audience}
       format: {format}
       created: YYYY-MM-DD
       ---
       # Hook Variations: {topic}

       [5 hook variations from AI output]
       ```

    5. **CLI** (argparse):
       - `title` — positional, the video topic/idea
       - `--platform` — default "yt-long" (choices: yt-long, yt-shorts, tiktok, reels)
       - `--audience` — default "AI builders and content creators"
       - `--format` — default "medium" (choices: short, medium, long)
       - `--no-polish` — flag, skip Claude polish pass

    6. **Print to console** — show the hook preview (first 800 chars) and the vault path.

    ## Key constraints
    - Do NOT write to `output/` directory — output goes to `Content-Hub-Vault-V2/05-Hooks/` only
    - Read marketing_brain.md from `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md`, NOT from V1 Exoskeleton path
    - Match the async main() pattern from hook_writer.py and cascade.py
    - No inline prompts — all prompt text lives in prompts/hook.md

    ## Acceptance Criteria
    1. File exists at `skills/hook.py`
    2. Loads `prompts/hook.md` from disk (not hardcoded prompt)
    3. Reads `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` as context
    4. Calls draft() then polish() (or draft only if --no-polish)
    5. Writes output to `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md`
    6. Has correct argparse CLI (topic, --platform, --audience, --format, --no-polish)
    7. Code style matches hook_writer.py / cascade.py patterns

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT
    Include a summary of what you created.

### Task 2.2: pipeline-agent: Create skills/outline.py

- description: "pipeline-agent: Create skills/outline.py"
- model: sonnet
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `skills/outline.py` — the standalone Python skill backing the `/outline` slash command.

    ## Scope
    Read for context:
    - `prompts/outline.md` — the prompt file this skill loads (already created by another agent)
    - `skills/hook_writer.py` — generate_outline() pattern reference
    - `skills/cascade.py` — production skill pattern reference
    - `skills/utils/ai.py` — draft() and polish() signatures

    Create:
    - `skills/outline.py`

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## What skills/outline.py must do

    1. **Load prompt** — read `prompts/outline.md` from project root. Inject: {topic}, {hook}, {target_length}, {platform}.

    2. **Load hook context** — if --hook-path provided, read that file's content and inject as {hook}. If not provided, {hook} = "(no hook provided — generate outline without it)".

    3. **Read marketing_brain** — load `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` for context (inject into prompt or use as system context). Same V2 path as hook.py.

    4. **AI cascade**:
       - `draft()` first — structural skeleton (Ollama, cheap)
       - `polish()` second — sharpen talking points, check pacing markers
       - `--no-polish` flag to skip

    5. **Output** — write to `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`. Format:
       ```markdown
       ---
       topic: {topic}
       platform: {platform}
       target_length: {target_length}m
       hook_source: {hook_path or "none"}
       created: YYYY-MM-DD
       ---
       # Outline: {topic}

       [full Dopamine Ladder outline from AI]
       ```

    6. **CLI** (argparse):
       - `topic` — positional
       - `--hook-path` — path to hook .md file (optional)
       - `--length` — target length in minutes, default 8
       - `--platform` — default "yt-long"
       - `--no-polish` — skip polish pass

    ## Key constraints
    - Output to `Content-Hub-Vault-V2/06-Outlines/` only
    - Read marketing_brain from V2 vault path
    - No inline prompts — all prompt text in prompts/outline.md
    - Match async patterns from hook_writer.py

    ## Acceptance Criteria
    1. File exists at `skills/outline.py`
    2. Loads `prompts/outline.md` from disk
    3. Reads marketing_brain.md from V2 vault path
    4. Accepts --hook-path and injects hook content into prompt
    5. Calls draft() then polish()
    6. Writes to `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md` with frontmatter
    7. CLI has: topic, --hook-path, --length, --platform, --no-polish

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT
    Include a summary of what you created.

### Task 3.1: pipeline-agent: Create .claude/skills/hook/SKILL.md

- description: "pipeline-agent: Create .claude/skills/hook/SKILL.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `.claude/skills/hook/SKILL.md` — the Claude Code entry point for the `/hook` slash command.

    ## Scope
    Read for context:
    - `.claude/skills/ideation/SKILL.md` — format reference (closest match in complexity)
    - `.claude/skills/cascade/SKILL.md` — additional format reference
    - `skills/hook.py` — the Python file this SKILL.md invokes; read it to get exact CLI args and output path

    Create:
    - `.claude/skills/hook/SKILL.md` (create the directory if it doesn't exist)

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel.

    ## Required structure (match exactly):
    - H1: `/hook`
    - Brief description (1–2 sentences)
    - **Trigger** — when the user types `/hook`
    - **Execution Steps** — numbered, sequential:
      1. Parse topic + optional flags from user's message
      2. Confirm inputs with user (topic, platform, audience, format)
      3. Run: `python -m skills.hook "{topic}" --platform {platform} --audience "{audience}" --format {format}`
      4. Wait for completion, report vault path + hook preview
    - **Output** — `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md` with 5 variations
    - **After Completion** — template to show user (vault path, preview of recommended hook)
    - **Usage Examples** — 2 examples: bare invocation and full with flags
    - **Notes** — mention: Kallaway-trained, draft (Ollama) + polish (Claude), use --no-polish for faster/cheaper run

    ## Acceptance Criteria
    1. File exists at `.claude/skills/hook/SKILL.md`
    2. Trigger, Execution Steps, Output, After Completion, Usage Examples, Notes sections all present
    3. Python command in Execution Steps matches the actual CLI of skills/hook.py
    4. Output vault path is correct (`Content-Hub-Vault-V2/05-Hooks/`)
    5. Format mirrors ideation/SKILL.md style

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT

### Task 3.2: pipeline-agent: Create .claude/skills/outline/SKILL.md

- description: "pipeline-agent: Create .claude/skills/outline/SKILL.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for the Content Hub V2 project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create `.claude/skills/outline/SKILL.md` — the Claude Code entry point for the `/outline` slash command.

    ## Scope
    Read for context:
    - `.claude/skills/ideation/SKILL.md` — format reference
    - `.claude/skills/short-form/SKILL.md` — additional reference (short-form takes a file path input, similar to outline's --hook-path)
    - `skills/outline.py` — read it to get exact CLI args and output path

    Create:
    - `.claude/skills/outline/SKILL.md`

    ## Required structure (match format exactly):
    - H1: `/outline`
    - Brief description
    - **Trigger**
    - **Execution Steps**:
      1. Parse topic + optional flags
      2. If user has a hook file from a previous `/hook` run, resolve its path; if not, note it's optional
      3. Run: `python -m skills.outline "{topic}" [--hook-path "{path}"] [--length {n}] --platform {platform}`
      4. Report vault path + outline preview
    - **Output** — `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`
    - **After Completion**
    - **Usage Examples** — 2 examples: bare (no hook path) and full (with hook path from /hook run)
    - **Notes** — mention: Dopamine Ladder structure, works best after /hook, --no-polish flag available

    ## Acceptance Criteria
    1. File exists at `.claude/skills/outline/SKILL.md`
    2. All required sections present
    3. Python command matches actual CLI of skills/outline.py
    4. Output path correct (`Content-Hub-Vault-V2/06-Outlines/`)
    5. Example showing --hook-path from a prior /hook run
    6. Format mirrors ideation/SKILL.md

    ## When done
    Report: DONE / DONE_WITH_CONCERNS / STUCK / NEEDS_CONTEXT

## Status Log
- 2026-05-06 — created, status=awaiting-approval
