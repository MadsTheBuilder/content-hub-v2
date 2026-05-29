# /cascade

Generate a blog post, Twitter/X thread, and LinkedIn post from either our own research+outline or a YouTube video transcript — all written to the Obsidian vault ready for review and manual posting.

**Default mode: research + outline.** Use this after `/outline` has been approved. Only fall back to a raw YouTube URL when no research/outline exists for the topic.

## Trigger
User types `/cascade` with optional URL or flags.

## Execution Steps

### Mode A — Research + Outline (preferred, default after /outline)
1. Confirm the topic and locate the files:
   - Research: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>/research.md`
   - Outline: `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`
2. Confirm before running: "Running cascade on research+outline for: [topic] — confirm?"
3. Wait for user confirmation.
4. Run:
   ```
   python -m skills.cascade --research-file "Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>/research.md" --outline-file "Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md" --title "<topic>"
   ```
5. Report results.

### Mode B — YouTube URL (fallback)
1. Get YouTube URL from user.
2. Confirm URL before running: "Running cascade on: [URL] — confirm?"
3. Wait for user confirmation.
4. Run: `python -m skills.cascade <url>`
5. Report results.

## Output

Cascade creates 4 files in `Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/`:

- `blog_post.md` — Blog post (~600 words, vault markdown with frontmatter)
- `twitter_thread.md` — Twitter/X thread (7–10 tweets, ≤280 chars each)
- `linkedin_post.md` — LinkedIn post (~200 words)
- `README.md` — Metadata and post tracking

All files are written to the Obsidian vault. No auto-publishing — review each file and post manually.

## After Completion

Report:
- Path to the output directory
- The 3 markdown files created
- One-line preview of the Twitter hook (first tweet)

## Usage Examples

- `/cascade` after `/outline` approved → runs on research+outline automatically
- `/cascade https://youtube.com/watch?v=abc123` → fallback, extracts transcript from YouTube

## Notes

- Research+outline mode uses up to 6,000 chars of combined content — covers most research files + outlines in full.
- Output goes to `Content-Hub-Vault-V2/08-Distribution/` — this is the Obsidian vault.
- Replace `[VIDEO_LINK]` placeholder in `twitter_thread.md` and `linkedin_post.md` before posting.
- Each post is independent — you can publish them on different dates or skip one entirely.
- Review the generated content for accuracy and tone before posting to any platform.
