# /cascade

Take a YouTube video, extract its transcript, and generate a blog post, Twitter/X thread, and LinkedIn post — all written to the Obsidian vault ready for review and manual posting.

## Trigger
User types `/cascade` with a YouTube URL.

## Execution Steps

1. Get YouTube URL from user (inline with command or ask if not provided)
2. Confirm URL before running: "Running cascade on: [URL] — confirm?"
3. Wait for user confirmation.
4. Run: `python -m skills.cascade <url>`
5. Report results: show the 3 file paths created + one-line preview of the Twitter hook tweet

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

- `/cascade https://youtube.com/watch?v=abc123` → extracts transcript, generates all 3 posts
- `/cascade` → asks for YouTube URL, then runs the cascade

## Notes

- Output goes to `Content-Hub-Vault-V2/08-Distribution/` — this is the Obsidian vault.
- Transcript extraction can take 30–60 seconds depending on video length.
- Replace `[VIDEO_LINK]` placeholder in `twitter_thread.md` and `linkedin_post.md` before posting.
- Each post is independent — you can publish them on different dates or skip one entirely.
- Review the generated content for accuracy and tone before posting to any platform.
