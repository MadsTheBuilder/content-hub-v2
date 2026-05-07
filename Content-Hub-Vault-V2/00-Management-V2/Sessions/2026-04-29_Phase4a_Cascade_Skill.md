---
status: Completed
date: 2026-04-29
type: session_summary
---

# Session: Phase 4a — `/cascade` Skill Build

Implements: [[Chase_AI_System_Breakdown]] Phase 4a
References: [[Current_Sprint]] | [[Local_First_Skill_Engine_Plan]] | [[marketing_brain]]
Modifies: `skills/cascade.py` | `prompts/cascade.md` | `.claude/skills/cascade/SKILL.md`

## What Was Done

Built the `/cascade` slash command end-to-end using orchestrated-execution (Sonnet agents).

The skill takes a YouTube URL, extracts the transcript via the `yt_dlp` Python API, generates a blog post + Twitter thread + LinkedIn post using voice-tuned prompts, and writes all 4 files to `Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/`.

**Orchestration:** 2 groups, 3 tasks, all pipeline-agent (Sonnet).

**Smoke test:** Ran on `https://www.youtube.com/watch?v=h_yQswsXwhY` (Kallaway's top video, 921K views). Extracted 24,331 characters. Generated all 3 platform posts. Wrote to vault at `08-Distribution/2026-04-29_social-media-isnt-hard-its-misunderstood/`. Blog post reads clean — practitioner voice, no AI-isms.

## Files Changed

- `skills/cascade.py` — full rewrite from V1 (CapCut transcript + `output/` dir) to V2 (YouTube URL + `yt_dlp` Python API + vault output). 168 lines.
- `prompts/cascade.md` — new file. 3 sections: `## BLOG POST PROMPT`, `## TWITTER THREAD PROMPT`, `## LINKEDIN PROMPT`. Voice guidelines + banned phrases embedded. Placeholders: `{title}`, `{transcript}`, `{youtube_url}`.
- `.claude/skills/cascade/SKILL.md` — new slash command entry. Matches yt-pipeline pattern.
- `Content-Hub-Vault-V2/08-Distribution/2026-04-29_social-media-isnt-hard-its-misunderstood/` — smoke test output (4 files).

## Bugs Fixed During Verification

1. **Windows cp1252 encoding** — emoji in print statements crashed on Windows terminal. Fixed with `sys.stdout.reconfigure(encoding="utf-8")`.
2. **yt-dlp CLI not on PATH** — subprocess calls failed. Switched to `yt_dlp.YoutubeDL` Python API (same pattern as `yt_pipeline.py`).
3. **Double frontmatter** — blog prompt told LLM to output YAML frontmatter, but `cascade.py` also prepends frontmatter in code. Fixed by removing frontmatter instructions from the prompt; code handles it reliably.

## Outstanding

- Phase 4b (`/short-form`) is next in the sprint.
- Phase 4c (`/voice-cleanup`) after that.
- Blog tags are hardcoded as `[ai-tools, build-in-public]` — could be dynamic in the future but not needed now.
