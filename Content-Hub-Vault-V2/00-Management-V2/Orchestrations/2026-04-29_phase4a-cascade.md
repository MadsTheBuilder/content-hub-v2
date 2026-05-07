---
slug: phase4a-cascade
created: 2026-04-29
status: complete
current_group: null
groups_complete: []
specialists_involved: [pipeline-agent]
---

# Orchestration: Phase 4a — `/cascade` Skill Build

## Recon summary

- `skills/cascade.py` **already exists** (V1 version) — takes CapCut transcript path, outputs to `output/YYYY-MM-DD/distribution/`. Must be rewritten for V2: YouTube URL input, blog post addition, vault output.
- `Content-Hub-Vault-V2/08-Distribution/` exists, empty (only `.gitkeep`). Ready for output.
- `skills/utils/ai.py` — AI router (Gemini Flash → Ollama → Claude CLI cascade). `generate()`, `draft()`, `polish()` available.
- `skills/utils/vault.py` — `get_niche_context()`, `read_skill()`, `read_vault()` helpers.
- `yt-dlp` v2026.3.17 installed — available for transcript extraction via subprocess.
- `youtube-transcript-api` NOT in requirements — yt-dlp is the transcript tool.
- No `prompts/cascade.md` exists yet.
- No `.claude/skills/cascade/SKILL.md` exists yet.
- SKILL.md pattern: no frontmatter, plain markdown, ## Trigger + numbered steps + ## Notes.
- Existing cascade.py generates Twitter + LinkedIn but NOT blog post. Blog post is new.

## Execution plan

```
## Execution Plan: Phase 4a — /cascade Skill

**Tasks:** 3 across 2 groups
**Specialists:** pipeline-agent

### Group 1 (parallel)
- [pipeline-agent | EASY] Create prompts/cascade.md
  Files: prompts/cascade.md (create)
  Criteria: Voice-tuned prompt covering blog post, Twitter thread, LinkedIn post.
  Clear section markers (## BLOG POST PROMPT, ## TWITTER THREAD PROMPT, ## LINKEDIN PROMPT).
  No AI-isms. Uses {transcript}, {title}, {youtube_url} placeholders.

- [pipeline-agent | EASY] Create .claude/skills/cascade/SKILL.md
  Files: .claude/skills/cascade/SKILL.md (create)
  Criteria: Matches yt-pipeline SKILL.md pattern. Clear invocation: /cascade <YouTube URL>.
  Documents output location (Content-Hub-Vault-V2/08-Distribution/).
  Documents 3 outputs: blog_post.md, twitter_thread.md, linkedin_post.md.

### Group 2 (depends on Group 1)
- [pipeline-agent | MEDIUM] Rewrite skills/cascade.py
  Files: skills/cascade.py (rewrite)
  Read for context: prompts/cascade.md, skills/utils/ai.py, skills/utils/vault.py, skills/yt_pipeline.py
  Criteria:
  1. Accepts YouTube URL as CLI arg (python -m skills.cascade <url> [--title "..."])
  2. Extracts transcript via yt-dlp subprocess (auto-subs, VTT, cleaned to plain text)
  3. Reads prompts/cascade.md and splits by section markers
  4. Generates blog post (~600 words), Twitter thread (7-10 tweets ≤280 chars), LinkedIn (~200 words)
  5. Writes to Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/: blog_post.md, twitter_thread.md, linkedin_post.md, README.md
  6. Prints preview of each output + vault path on completion
```

## Agent prompts

### Task: pipeline-agent: Create prompts/cascade.md

- description: "pipeline-agent: Create prompts/cascade.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    Your domain: content generation pipeline. You write Python helpers and prompt files for Claude Code skills.

    ## Your Task

    Create `prompts/cascade.md` at `c:\Users\madhu\Claude cowork\Content Hub V2\prompts\cascade.md`.

    This prompt file drives the `/cascade` skill: given a YouTube video transcript, generate content for 3 platforms (blog post, Twitter thread, LinkedIn post) in the creator's voice.

    ## Scope
    Create: prompts/cascade.md

    ## What to write

    The file must have 3 clearly separated sections with these exact headers:
    - `## BLOG POST PROMPT`
    - `## TWITTER THREAD PROMPT`  
    - `## LINKEDIN PROMPT`

    **Creator voice context** (embed this in all 3 prompts):
    - Niche: AI tools, build-in-public, developer productivity
    - Voice: Direct, practical, no fluff. Short sentences. Active voice.
    - Banned phrases: "Let's dive in", "it's not X it's Y", "game-changer", "revolutionize", "in today's fast-paced world", "leverage", "cutting-edge", "unleash", "seamless", "robust", "paradigm shift"
    - Style: Sounds like a practitioner talking to practitioners — specific, opinionated, useful

    **Blog post section:**
    - Structure: Title → opening hook (2-3 sentences) → 3-4 body sections with ## subheadings → practical takeaway → embedded video CTA
    - Length: 500-700 words
    - SEO: natural keywords, no keyword stuffing
    - Placeholders: {title}, {transcript}, {youtube_url}
    - Format: Ready-to-publish markdown

    **Twitter thread section:**
    - 7-10 tweets
    - Tweet 1: hook — strongest insight, stops scroll, ends with "🧵"
    - Tweets 2-8: one idea per tweet, line breaks between sentences, specific numbers
    - Final tweet: CTA with [VIDEO_LINK] placeholder
    - Rules: ≤280 chars each, no hashtags, max 1 emoji per tweet
    - Placeholders: {title}, {transcript}
    - Format: **Tweet 1:** [content] **Tweet 2:** [content] etc.

    **LinkedIn section:**
    - 150-250 words
    - First 2 lines create curiosity (visible before "see more")
    - 3-5 bullet points with key takeaways
    - Contrarian or unique take
    - Question CTA at end (drives comments)
    - 3-5 hashtags at END only
    - Placeholders: {title}, {transcript}, {youtube_url}
    - Format: Single post, copy-paste ready

    ## Acceptance Criteria
    1. File exists at prompts/cascade.md
    2. Contains exactly 3 sections with the specified ## headers
    3. Each section has placeholders for transcript/title/youtube_url
    4. Voice guidelines are embedded (banned phrases listed)
    5. Format instructions are clear and complete

    ## When done
    Report:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but with doubts (explain)
    - STUCK: Cannot proceed (explain)

    Include a summary of what you wrote.

---

### Task: pipeline-agent: Create .claude/skills/cascade/SKILL.md

- description: "pipeline-agent: Create .claude/skills/cascade/SKILL.md"
- model: haiku
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    ## Your Task

    Create `.claude/skills/cascade/SKILL.md` at `c:\Users\madhu\Claude cowork\Content Hub V2\.claude\skills\cascade\SKILL.md`.

    First, read the existing SKILL.md at `.claude/skills/yt-pipeline/SKILL.md` to understand the exact format and pattern used.

    This SKILL.md defines the `/cascade` slash command: given a YouTube URL, it generates a blog post + Twitter thread + LinkedIn post and writes them to the Obsidian vault.

    ## Scope
    Read for context: .claude/skills/yt-pipeline/SKILL.md
    Create: .claude/skills/cascade/SKILL.md

    ## What to write

    Match the yt-pipeline SKILL.md format exactly (no frontmatter, plain markdown, ## Trigger + numbered steps).

    The slash command flow:
    1. User invokes: `/cascade <YouTube URL>` or `/cascade` then pastes URL
    2. Confirm the URL with user before running
    3. Run: `python -m skills.cascade <url>`
    4. Report: 3 output file paths in Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/

    Include:
    - ## Trigger section
    - Step-by-step numbered flow
    - Output section: what 3 files are created (blog_post.md, twitter_thread.md, linkedin_post.md)
    - ## Notes: vault path, manual posting required (no auto-publish), replace [VIDEO_LINK] in outputs
    - Usage examples section

    ## Acceptance Criteria
    1. File exists at .claude/skills/cascade/SKILL.md
    2. Matches yt-pipeline format (no YAML frontmatter, plain markdown)
    3. Documents the exact CLI command to run
    4. Documents the 3 output files and vault path
    5. Includes at least 2 usage examples

    ## When done
    Report DONE / DONE_WITH_CONCERNS / STUCK with summary.

---

### Task: pipeline-agent: Rewrite skills/cascade.py

- description: "pipeline-agent: Rewrite skills/cascade.py"
- model: sonnet
- prompt: |
    You are the pipeline-agent for Content Hub V2 — a local-first content production skill engine.

    Your domain: content generation pipeline. Python helpers that drive Claude Code skills.

    ## Your Task

    Rewrite `skills/cascade.py` to implement the V2 `/cascade` skill.

    The V1 file exists and takes a CapCut transcript path. The V2 version must:
    - Accept a YouTube URL as input
    - Extract the transcript via yt-dlp
    - Generate blog post + Twitter thread + LinkedIn post using prompts/cascade.md
    - Write all 3 outputs to the Obsidian vault at Content-Hub-Vault-V2/08-Distribution/

    ## Scope
    Read for context: prompts/cascade.md, skills/utils/ai.py, skills/utils/vault.py, skills/yt_pipeline.py
    Modify: skills/cascade.py (full rewrite)

    **Project root:** `c:\Users\madhu\Claude cowork\Content Hub V2\`

    ## Implementation requirements

    ### CLI interface
    ```
    python -m skills.cascade <youtube_url> [--title "Optional override title"]
    ```

    ### Transcript extraction
    Use yt-dlp via subprocess to extract auto-generated subtitles:
    1. Run `yt-dlp --get-title <url>` to get video title
    2. Run `yt-dlp --write-auto-subs --sub-lang en --sub-format vtt --skip-download --output <tmpdir>/%(title)s <url>`
    3. Find the .vtt file in tmpdir
    4. Parse VTT: strip WEBVTT header, timestamps (lines with "-->"), numeric cue IDs, HTML tags (<c>, <00:00:01.000>, etc.)
    5. Deduplicate consecutive identical lines (VTT repeats segments)
    6. Join to clean plain text transcript

    Use tempfile.TemporaryDirectory() for isolation.

    ### Prompt loading
    Read `prompts/cascade.md` and split by section headers:
    - `## BLOG POST PROMPT` → blog_prompt template
    - `## TWITTER THREAD PROMPT` → twitter_prompt template
    - `## LINKEDIN PROMPT` → linkedin_prompt template

    Fill placeholders: {title}, {transcript} (truncated to 4000 chars), {youtube_url}

    ### Generation
    Use `skills/utils/ai.py` `generate()` function (already does Gemini→Ollama→Claude cascade).
    Run all 3 generations sequentially (not parallel — keeps code simple).

    ### Output
    Create directory: `Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/`
    Where slug = title lowercased, spaces→hyphens, non-alphanumeric stripped, max 40 chars.

    Write 4 files:
    1. `blog_post.md` — blog content with front-matter: title, date, youtube_url, tags
    2. `twitter_thread.md` — thread with header
    3. `linkedin_post.md` — post with header
    4. `README.md` — checklist: review each, replace [VIDEO_LINK], post manually

    Print progress to stdout at each step. Print vault path at end.

    ### Key constraints
    - Use only stdlib + packages already in requirements.txt (yt-dlp, anthropic SDK available but use utils/ai.py)
    - Handle missing transcript gracefully: print error + exit 1
    - Keep it under 200 lines — no over-engineering
    - Match existing code style in cascade.py (asyncio main, argparse, Path)

    ## Acceptance Criteria
    1. `python -m skills.cascade --help` runs without error
    2. Transcript extraction function exists and parses VTT correctly
    3. Prompt loading reads prompts/cascade.md and fills all 3 sections
    4. Output goes to Content-Hub-Vault-V2/08-Distribution/ (not output/ dir)
    5. All 4 files written (blog_post.md, twitter_thread.md, linkedin_post.md, README.md)
    6. File is ≤200 lines

    ## When done
    Report DONE / DONE_WITH_CONCERNS / STUCK with summary of what changed.

## Status log
- 2026-04-29 Recon complete, plan written, status=awaiting-approval
- 2026-04-29 User approved, status=executing, current_group=1
- 2026-04-29 Group 1 complete (prompts/cascade.md ✅, .claude/skills/cascade/SKILL.md ✅), current_group=2
- 2026-04-29 Group 2 complete (skills/cascade.py ✅), smoke test passed, status=complete
