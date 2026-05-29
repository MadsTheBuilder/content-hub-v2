---
name: title
description: Generate 10 YouTube title options (5 safe + 5 experimental) for a video concept, with thumbnail text suggestions and competitor-pattern analysis. Use this skill whenever the user types /title, says "do the titles", "write titles for my video", "generate titles", "title ideas", or wants to choose a YouTube title. Also trigger automatically after /outline approval — title generation is the natural next step, even if the user doesn't explicitly type /title. If the user has just approved an outline and says "what's next?" or "continue", suggest /title immediately alongside /cascade. Trigger also when the user says "redo the titles", "regenerate titles", or "give me different title options with [style constraint]".
---

# /title

Generate 10 YouTube title options for a video concept — 5 Tier-1 safe bets and 5 Tier-2 experimental options — with thumbnail text, informed by top-30 competitor titles in the niche.

## How to Get the Concept

1. **Inline arg**: User typed `/title [concept]` — use that string directly.
2. **Recent context**: No inline arg, but the user referenced their video topic in the same message (e.g., "just approved the outline for my LangGraph video, do titles") — extract the topic from their message.
3. **Style constraint or regenerate**: User asked to redo titles with different style (e.g., "more curiosity-gap, no numbered lists") — append the constraint to the concept string before passing to the script, like `"RAG pipeline with LangChain and pgvector — style: curiosity-gap, no numbered lists"`.
4. **No concept anywhere**: Ask once — "What's the video topic?" — then proceed when they answer.

Do not ask for confirmation before running. The user typed /title; they want titles.

## Run

```
python -m skills.title "[concept string]"
```

The concept must be double-quoted so spaces are handled correctly. Run from the project root (`C:\Users\madhu\Claude cowork\Content Hub V2`).

The script writes a `.md` file to `Content-Hub-Vault-V2/07-Titles/YYYY-MM-DD_<slug>.md` and prints the file path to stdout.

## Report Results

After the script runs, show:
1. The vault file path
2. All 5 Tier-1 (safe) titles, numbered
3. A one-line note on what to do next: "Review these and pick your favourite — or `/cascade` to generate the full distribution package."

## Notes

- Competitor title analysis is loaded automatically from `skills/data/competitor_titles.json` (top-30 by view count in the niche).
- Tier-1 = safe, algorithm-friendly, broad appeal. Tier-2 = experimental, higher curiosity gap, higher variance.
- Thumbnail text suggestions (2–4 words, readable at phone size) are generated for all 10 titles.
- Output lives in the Obsidian vault (`07-Titles/`). No auto-publishing.
