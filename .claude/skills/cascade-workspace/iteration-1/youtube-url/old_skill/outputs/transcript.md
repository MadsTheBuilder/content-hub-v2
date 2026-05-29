# Cascade Skill Execution — YouTube URL Mode

**Date:** 2026-05-15  
**Input:** `cascade this video for me: https://www.youtube.com/watch?v=dQw4w9WgXcQ`  
**Mode Detected:** Mode B (YouTube URL fallback)

---

## Step 1: Mode Detection

Claude detects that the user provided a raw YouTube URL. No research or outline files are referenced or available, so Mode B (YouTube fallback) is triggered.

**Claude's response:**

```
Got it — I'll cascade this YouTube video for you using the transcript.

Detected: YouTube URL
Link: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Step 2: Confirmation Prompt

Claude asks the user to confirm before proceeding with the skill execution.

**Claude's response:**

```
Running cascade on: https://www.youtube.com/watch?v=dQw4w9WgXcQ — confirm?
```

**User confirmation:** Assume `yes` / approved.

---

## Step 3: Execute Cascade Command

Claude would run the cascade script with the YouTube URL.

**Command executed:**

```bash
python -m skills.cascade https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

---

## Step 4: Script Execution (Simulated)

The Python script would:

1. **Fetch YouTube metadata** — Extract video title, duration, channel name.
2. **Download and transcribe** — Fetch the video transcript (or generate one if unavailable).
3. **Generate distribution content:**
   - Extract key themes and talking points from the transcript.
   - Write a blog post (~600 words) with heading, introduction, body sections, and conclusion.
   - Create a 7–10 tweet Twitter/X thread with hooks and call-to-action.
   - Write a LinkedIn post (~200 words) optimized for professional audience.
4. **Write outputs** to `Content-Hub-Vault-V2/08-Distribution/YYYY-MM-DD_<slug>/`:
   - `blog_post.md`
   - `twitter_thread.md`
   - `linkedin_post.md`
   - `README.md` (with metadata and tracking info)

**Simulated output log:**

```
[cascade] Starting YouTube URL mode...
[cascade] Fetching video metadata from: https://www.youtube.com/watch?v=dQw4w9WgXcQ
[cascade] Video title: "Never Gonna Give You Up"
[cascade] Video channel: Rick Astley
[cascade] Duration: 3:32
[cascade] Extracting transcript...
[cascade] Transcript length: 2,847 characters
[cascade] Generating blog post...
[cascade] Generating Twitter thread (8 tweets)...
[cascade] Generating LinkedIn post...
[cascade] Writing files to: Content-Hub-Vault-V2/08-Distribution/2026-05-15_never-gonna-give-you-up/
[cascade] ✓ blog_post.md (612 words)
[cascade] ✓ twitter_thread.md (8 tweets)
[cascade] ✓ linkedin_post.md (198 words)
[cascade] ✓ README.md
[cascade] Complete!
```

---

## Step 5: Completion Report

Claude reports the results to the user in the standard format.

**Claude's response:**

```
Done! Cascade generated distribution content from the YouTube video.

**Output directory:**
Content-Hub-Vault-V2/08-Distribution/2026-05-15_never-gonna-give-you-up/

**Files created:**
1. blog_post.md — Full blog post with introduction, sections, and conclusion
2. twitter_thread.md — 8-tweet thread optimized for X
3. linkedin_post.md — Professional LinkedIn post
4. README.md — Metadata and post tracking

**Twitter hook (first tweet):**
"Just watched this classic music moment and here's why it still hits... 🎵"

**Next steps:**
- Review each file in the vault
- Replace `[VIDEO_LINK]` placeholders with the actual URL
- Customize tone/voice as needed
- Post manually when ready

All files are ready for review in your Obsidian vault.
```

---

## Summary

| Element | Value |
|---------|-------|
| **Mode** | Mode B (YouTube URL fallback) |
| **Input** | https://www.youtube.com/watch?v=dQw4w9WgXcQ |
| **Confirmation** | User approved |
| **Command** | `python -m skills.cascade <url>` |
| **Output Location** | `Content-Hub-Vault-V2/08-Distribution/2026-05-15_never-gonna-give-you-up/` |
| **Files Generated** | blog_post.md, twitter_thread.md, linkedin_post.md, README.md |
| **Status** | Complete ✓ |
