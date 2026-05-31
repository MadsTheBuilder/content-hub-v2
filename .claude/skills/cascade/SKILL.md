---
name: cascade
description: Generate a full distribution package (blog post, Twitter/X thread, LinkedIn post) from a completed video outline+research or a YouTube URL. Use this skill whenever the user types /cascade, says "generate distribution content", "create social posts from my outline", "write a blog post from my research", "turn this into a Twitter thread and LinkedIn", "cascade this", or asks to repurpose a YouTube video into written content for multiple platforms. Also trigger when the user has just approved an outline and asks "what's next?" — cascade is the natural next step after /outline.
---

# /cascade

Turn approved research + outline (or a YouTube URL) into a ready-to-publish distribution package: a blog post, Instagram carousel, and LinkedIn post — all voice-cleaned before they land in the vault. No raw AI drafts are written to disk.

**Default: use your own research + outline.** This is the mode to use after you've completed `/outline`. The YouTube URL fallback is for one-off cases where you want to repurpose someone else's video.

## How to run it

### After `/outline` (preferred)

The user will typically just type `/cascade` with no extra arguments. Your job is to find the right files.

1. **Find the files.** Look in:
   - Research: `Content-Hub-Vault-V2/10-Research/` — find the most recent folder matching the topic, grab `research.md` inside it (or the dated `_brief.md` file at the root)
   - Outline: `Content-Hub-Vault-V2/06-Outlines/` — find the most recent `.md` file matching the topic
   
   If the topic is ambiguous or multiple files match, list them and ask which one.

2. **Confirm once, then run.**
   Say: "Running cascade on: [topic] — research from [filename], outline from [filename]. Go?"
   
   Wait for a yes. Then run:
   ```
   python -m skills.cascade --research-file "Content-Hub-Vault-V2/10-Research/..." --outline-file "Content-Hub-Vault-V2/06-Outlines/..." --title "<topic>"
   ```

3. **Report.** See "After completion" below.

### YouTube URL fallback

Use this when the user provides a YouTube URL and there's no research/outline for the topic.

1. Confirm: "Running cascade on: [URL]. This will extract the transcript and generate blog + Twitter + LinkedIn. Go?"
2. Wait for yes. Then run: `python -m skills.cascade <url>`
3. Report. See "After completion" below.

## After completion

Report:
- Full path to the output directory (`Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/`)
- The 4 files created: `blog_post.md`, `twitter_thread.md`, `linkedin_post.md`, `README.md`
- One-line preview of the Twitter hook (first tweet, ≤280 chars)
- Reminder: replace `[VIDEO_LINK]` placeholder in `twitter_thread.md` and `linkedin_post.md` before posting

Next step: `/short-form` to generate 3 short-form scripts from the same outline.

## Things to know

- **Built-in voice cleanup**: After generating all three pieces, the script runs each through `prompts/voice_cleanup.md` via Claude before writing to disk. What lands in the vault is already polished. If a cleanup call fails, the raw draft is written with a warning in the terminal.
- **Content cap**: The helper uses up to 6,000 characters of combined research + outline. Long research files will be truncated — that's expected and fine.
- **Title**: The helper auto-extracts the title from the outline's `topic:` frontmatter field. Use `--title` to override if it picks the wrong thing.
- **If it fails**: Check that `ANTHROPIC_API_KEY` is set in `.env` and that the research/outline paths are correct. The script will print which step failed.
- **Prompt source of truth**: `prompts/cascade.md` — edit that file to change tone, structure, or platform-specific rules globally. Voice cleanup rules live in `prompts/voice_cleanup.md`.

## Examples

- `/cascade` (no args, after `/outline` approved) → finds most recent research+outline, runs automatically
- `/cascade "AI agents for non-coders"` → finds matching files for that topic
- `/cascade https://youtube.com/watch?v=abc123` → YouTube fallback mode
