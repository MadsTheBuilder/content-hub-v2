---
name: title
description: Generate 10 YouTube title options (5 safe + 5 experimental) for a video concept, with thumbnail text suggestions and competitor-pattern analysis. Use this skill whenever the user types /title, says "do the titles", "write titles for my video", "generate titles", "title ideas", "name my video", or wants to choose a YouTube title. Also trigger automatically after /outline or /cascade — title generation is the natural next step after a video is structured. If the user has just approved an outline and says "what's next?" or "continue the pipeline", trigger /title immediately. Trigger also when the user says "redo the titles", "regenerate titles", or "give me different title options with [style constraint]". Don't wait for a full outline — trigger on any video concept or topic, even rough ones.
---

# /title

**Step 5 of 8** in the content pipeline:
`researcher → ideation → hook → outline → **title** → cascade → short-form → voice-cleanup`

Generate 10 YouTube title options — 5 Tier-1 safe bets and 5 Tier-2 experimental options — with thumbnail text suggestions, benchmarked against the top-30 competitor titles in the niche.

## How to Get the Concept

Work through these in order until you have a concept:

1. **Inline arg**: User typed `/title [concept]` — use that string directly.
2. **Message context**: No inline arg but the user mentioned their video topic in this message (e.g., "just approved the LangGraph outline, do titles") — extract the concept.
3. **Recent outline**: No concept in the message — check `Content-Hub-Vault-V2/06-Outlines/` for the most recent `.md` file, read its frontmatter `concept:` field or first heading, and use that.
4. **Ask once**: None of the above — ask "What's the video topic?" and wait.

## Handle Style Constraints

If the user specified a style override (e.g., "all question-format", "use 'I tested X' structure", "more curiosity-gap, no numbered lists"), append it to the concept string before running:
`"[concept] — Style: [constraint]"`

The prompt model honors this inline.

## Run

```
python -m skills.title "[concept string]"
```

Double-quote the concept (spaces). Run from the project root (`C:\Users\madhu\Claude cowork\Content Hub V2`).

The script writes to `Content-Hub-Vault-V2/07-Titles/YYYY-MM-DD_<slug>.md` and prints the path to stdout.

Do not ask for confirmation before running — the user typed /title, they want titles.

## Report Results

Show:
1. The vault file path
2. All 5 Tier-1 (safe) titles, numbered
3. Suggested next: "Run `/cascade` for the full distribution package, or `/short-form` for a Shorts script."

## Notes

- Competitor analysis auto-loaded from `skills/data/competitor_titles.json` (top-30 by view count, AI/dev niche).
- Tier-1 = safe, algorithm-friendly, broad appeal. Tier-2 = experimental, higher curiosity gap, higher variance.
- Thumbnail text (2–4 bold words, phone-size readable) generated for all 10 titles.
- Output lives in `07-Titles/` in the Obsidian vault. No auto-publishing — review and choose.
