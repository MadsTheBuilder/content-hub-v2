# /short-form

Generate 3 vertical video scripts (30, 60, and 90 seconds) from our own research+outline or a YouTube video transcript — written to the Obsidian vault ready for review and recording.

**Default mode: research + outline.** Use this after `/outline` has been approved. Only fall back to a raw YouTube URL when no research/outline exists for the topic.

## Trigger

User types `/short-form` with optional flags.

## Execution Steps

### Mode A — Research + Outline (preferred, default after /outline)
1. Confirm the topic and locate the files:
   - Research: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>/research.md`
   - Outline: `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`
2. Confirm before running: "Running short-form on research+outline for: [topic] — confirm?"
3. Wait for user confirmation.
4. Run:
   ```
   python -m skills.short_form --research-file "Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>/research.md" --outline-file "Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md" --title "<topic>"
   ```
5. Report results.

### Mode B — YouTube URL (fallback)
1. Get YouTube URL from user.
2. Confirm URL before running: "Running short-form on: [URL] — confirm?"
3. Wait for user confirmation.
4. Run: `python -m skills.short_form <url>`
5. Report results.

## Output

Short-form creates 4 files in `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`:

- `30s_script.md` — 30-second vertical video script (~75–90 words)
- `60s_script.md` — 60-second vertical video script (~150–180 words)
- `90s_script.md` — 90-second vertical video script (~225–270 words)
- `README.md` — Metadata and recording checklist

All files are written to the Obsidian vault. No auto-recording — review each script and record manually.

## After Completion

Report:
- Path to the output directory
- The 4 markdown files created
- One-line preview of the 30-second script hook (opening line)

## Usage Examples

- `/short-form` after `/outline` approved → runs on research+outline automatically
- `/short-form https://youtube.com/watch?v=abc123` → fallback, extracts transcript from YouTube

## Notes

- Research+outline mode uses up to 6,000 chars of combined content.
- Scripts are re-written for vertical format — each stands alone with its own hook, body, and CTA.
- Output goes to `Content-Hub-Vault-V2/09-Shorts/` — this is the Obsidian vault.
- Each script is independent — record any subset or skip one entirely.
- Review for tone, pacing, and vertical storytelling before recording.
