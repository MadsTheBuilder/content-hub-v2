# Eval Run: youtube-url-fallback / with_skill

## Skill Read

**SKILL.md Summary:**
- Name: `short-form`
- Position: Step 6 of 7 in content pipeline (after `/cascade`, before `/voice-cleanup`)
- Two modes of operation:
  - **Mode A:** Research + Outline (default) — loads from vault, runs with `--research-file` and `--outline-file` flags
  - **Mode B:** YouTube URL (fallback) — runs when no research/outline exists, takes a URL as positional argument
- Output: 4 files written to `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`
  - `30s_script.md` (75–90 words)
  - `60s_script.md` (150–180 words)
  - `90s_script.md` (225–270 words)
  - `README.md` (metadata + checklist)

**Applicable Mode:** Mode B (YouTube URL fallback, no research/outline provided)

---

## Steps Taken

### Step 1: Read SKILL.md
- Confirmed Mode B applies (user has URL, no research/outline)
- Confirmed command format: `python -m skills.short_form <youtube_url>`

### Step 2: Locate Python Module
- Found module at `./skills/short_form.py`
- Verified module is importable: `import skills.short_form` ✓

### Step 3: Inspect Module
- Read `short_form.py` to understand error handling
- Flow: CLI args → extract_transcript() → generate 3 scripts → write vault

---

## Command Run

```bash
cd "C:\Users\madhu\Claude cowork\Content Hub V2" && python -m skills.short_form https://www.youtube.com/watch?v=RpEblXjLxB0
```

---

## Result

**Exit Code:** 1 (failure)

**Output:**
```
ERROR: [youtube] RpEblXjLxB0: Video unavailable
ERROR: yt_dlp failed: ERROR: [youtube] RpEblXjLxB0: Video unavailable
📹 Extracting transcript from https://www.youtube.com/watch?v=RpEblXjLxB0...
❌ Failed to extract transcript
```

**Analysis:**
1. `yt_dlp` library attempted to fetch the video via YouTube API/downloader
2. YouTube returned "Video unavailable" — this could mean:
   - Video is geoblocked
   - Video is private/deleted
   - Video requires authentication
   - URL is invalid
   - Rate-limiting or API key issue
3. `extract_transcript()` in `skills/utils/transcript.py` caught the yt_dlp error and returned empty transcript
4. `short_form.py` line 78 detected empty transcript and exited with status 1

**Script behavior (confirmed in code):**
- Line 74–79: If Mode B (YouTube URL provided) and transcript extraction fails, prints "❌ Failed to extract transcript" and exits
- The skill correctly implemented error handling — it doesn't generate scripts with no input

---

## Tool Calls Summary

| Tool | Calls |
|------|-------|
| Read | 2 |
| Bash | 2 |
| Glob | 1 (timed out) |
| Write | 1 |
| **Total** | **6** |

---

## Errors Encountered

1. **Video Unavailable Error** — yt_dlp could not access the video
   - Root cause: YouTube API returned 403 or video doesn't exist
   - Impact: Transcript extraction failed → skill exited cleanly at expected error point
   - No fix possible without a valid video URL

---

## Final Response to User

**Status:** FAILED (as expected — video is unavailable)

**What happened:**
- ✅ Skill loaded correctly (Mode B identified)
- ✅ Python module verified and ran
- ✅ Error handling worked as designed
- ❌ Video extraction failed: YouTube reported "Video unavailable"

**Reason for failure:**
The YouTube video at `https://www.youtube.com/watch?v=RpEblXjLxB0` is not accessible. This could be due to:
- Video deleted or made private
- Geoblocking or regional restriction
- YouTube API rate limit or authentication issue
- Invalid video ID

**Output generated:** None (transcript extraction is a prerequisite; without it, script generation cannot proceed)

**Next steps to test Mode B successfully:**
1. Provide a valid, publicly accessible YouTube URL
2. Re-run: `python -m skills.short_form <valid_url>`
3. Skill will extract transcript → generate 3 scripts → save to vault

**Expected output on success:**
- 4 files in `Content-Hub-Vault-V2/09-Shorts/YYYY-MM-DD_<slug>/`
- Console print: "✅ Short-form package written to: [path]"
