---
name: short-form
description: Generate 3 vertical video scripts (30s, 60s, 90s) from your research + outline or a YouTube URL — step 6 of 7 in the content pipeline (/cascade → /short-form → /voice-cleanup). Use this skill whenever the user types /short-form, says "write shorts", "generate short-form scripts", "make vertical videos", "create Reels scripts", "create TikTok scripts", "repurpose this for shorts", "make short clips from this", or asks to adapt long-form content into short vertical format. Also trigger automatically after /cascade completes and the user says "what's next?", "continue", "move forward", or "next step" — /short-form is always the step after /cascade.
---

# /short-form

Generate 3 vertical video scripts (30s, 60s, 90s) from research + outline or a YouTube URL. Each script is self-contained — hook, body, CTA — written to the Obsidian vault for review and recording.

**Pipeline position:** Step 6 of 7 → runs after `/cascade`, before `/voice-cleanup`.

## Mode Selection

**Mode A — Research + Outline (default, preferred):**  
Use when the user has come through the pipeline (after `/cascade`) or specifies a topic for which research + outline files exist.

**Mode B — YouTube URL (fallback):**  
Use when no research/outline exists and the user provides a YouTube URL directly.

## Execution

### Mode A — Research + Outline

1. **Locate the files.** If the user named a topic, resolve the paths:
   - Research: `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>/research.md`
   - Outline: `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md`

   If no topic was specified (user just typed `/short-form`), check both directories for the most recent files and confirm: "Found `<slug>` from `<date>` — run short-form on this?"

2. **Run:**
   ```
   python -m skills.short_form --research-file "<research path>" --outline-file "<outline path>" --title "<topic>"
   ```
   If only one file exists (outline but no research, or vice versa), pass whichever is available — the script handles partial inputs.

### Mode B — YouTube URL

1. Run: `python -m skills.short_form <youtube_url>`

## Output

4 files written to `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`:
- `30s_script.md` — ~75–90 words spoken
- `60s_script.md` — ~150–180 words spoken
- `90s_script.md` — ~225–270 words spoken
- `README.md` — metadata + recording checklist

## After Completion

Report:
- Full path to the output directory
- The 4 files created
- Opening line of the 30s script (the hook — paste it verbatim)
- Suggest `/voice-cleanup` as the next step

## Notes

- Input is truncated to 6,000 chars; this is enough for any single outline + research pair.
- Each script is independent — record any subset, skip one entirely, or record all three.
- No auto-recording — review each script before hitting record.
