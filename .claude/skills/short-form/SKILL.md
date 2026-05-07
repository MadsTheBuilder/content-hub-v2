# /short-form

Take a YouTube video, extract its core insight, and generate 3 vertical video scripts (30, 60, and 90 seconds) written to the Obsidian vault ready for review and recording.

## Trigger

User types `/short-form` with a YouTube URL.

## Execution Steps

1. Get YouTube URL from user (inline with command or ask if not provided)
2. Confirm URL before running: "Running short-form on: [URL] — confirm?"
3. Wait for user confirmation.
4. Run: `python -m skills.short_form <url>`
5. Report results: show the output directory path + one-line preview of the 30-second script hook

## Output

Short-form creates 4 files in `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`:

- `30s_script.md` — 30-second vertical video script (~50–75 words, tight hook + payoff)
- `60s_script.md` — 60-second vertical video script (~110–150 words, expanded narrative)
- `90s_script.md` — 90-second vertical video script (~170–220 words, full story with context)
- `README.md` — Metadata, source video link, and recording checklist

All files are written to the Obsidian vault. No auto-recording — review each script and record manually.

## After Completion

Report:
- Path to the output directory
- The 4 markdown files created
- One-line preview of the 30-second script hook (opening line)

## Usage Examples

- `/short-form https://youtube.com/watch?v=abc123` → extracts core insight, generates all 3 scripts
- `/short-form` → asks for YouTube URL, then runs the short-form pipeline

## Notes

- Output goes to `Content-Hub-Vault-V2/09-Shorts/` — this is the Obsidian vault.
- Transcript extraction can take 30–60 seconds depending on video length.
- Scripts are **re-written for vertical format** (optimized for mobile, no clipping). Each script stands alone and contains its own complete hook, body, and call-to-action — not truncated versions of each other.
- Each script is independent — you can record any subset or skip one entirely.
- Review the generated scripts for tone, pacing, and vertical storytelling before recording to any platform.
- Consider adding B-roll notes, visual cues, or on-screen text suggestions in the README before recording.
