---
name: hook
description: >-
  Step 3 of 8 in the content pipeline (/researcher → /ideation → /hook → /outline → /title →
  /cascade → /short-form → /voice-cleanup). Generate 5 Kallaway-trained YouTube hook variations
  for a video topic — the critical first 30 seconds that stop the scroll and open a curiosity
  loop. Use this skill whenever the user types /hook, asks to "write hooks", "generate hooks",
  "create my opening", "write my intro", "give me hooks for", or mentions wanting
  attention-grabbing YouTube video openings. Trigger automatically when /ideation has just
  completed and the user has picked an idea. After generating 5 hooks, show all 5 Spoken Lines
  and ask the user to pick one before suggesting /outline — hook choice determines the structure
  of the entire video outline.
---

# /hook

Generate 5 Kallaway-trained hook variations for a video topic — the first 30 seconds that stop the scroll and open a curiosity loop. Each variation uses a different Kallaway pattern with a Spoken Line, Visual Cue, Text Overlay, and one-sentence psychological rationale.

## Pipeline Position

**Step 3 of 8:** `/researcher` → `/ideation` → **/hook** → `/outline` → `/title` → `/cascade` → `/short-form` → `/voice-cleanup`

- **Comes after:** `/ideation` — use the idea the user chose as your topic input
- **Comes before:** `/outline` — the user's chosen hook drives the Dopamine Ladder structure

## Execution Steps

1. Get the topic from the user's message. If not provided, check whether `/researcher` was just run and use that topic. If still unclear, ask: "What topic should I write hooks for?"
2. Note optional flags with their defaults: `--platform yt-long`, `--audience "AI builders and content creators"`, `--format medium`. Only ask about these if the user specified them or the topic is ambiguous.
3. Confirm before running: "Writing 5 hooks for: [topic] — [platform] · [format]. Running now."
4. Run:
   ```
   python -m skills.hook "{topic}" --platform {platform} --audience "{audience}" --format {format}
   ```
   Add `--no-polish` if the user asked for a faster or cheaper run.
5. Wait for completion. Report the vault path and preview the ⭐ recommended hook's Spoken Line.

## Output

Writes one file to `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md` containing:
- 5 hook variations, each using a different Kallaway pattern
- Per variation: Spoken Line (3 sec) + Setup (10 sec) + Promise (15 sec) + Visual Cue + Text Overlay + Pattern name + Why (psychological rationale)
- Recommended hook marked with ⭐

## After Completion — BLOCKING GATE

Report the full path to the hooks file, then show all 5 hooks as a numbered list of Spoken Lines:

```
1. "[Spoken Line for hook 1]"
2. "[Spoken Line for hook 2]"
3. "[Spoken Line for hook 3]"
4. "[Spoken Line for hook 4]"
5. "[Spoken Line for hook 5]" ⭐ recommended
```

Then ask — **do not suggest /outline until you have the answer**:

> "Which hook do you prefer? Reply with a number (1–5)."

Once the user replies, confirm:

> "Using hook #N. Next step: `/outline topic=\"{topic}\" --hook-path \"{path}\"` — I'll use hook #N to build the Dopamine Ladder structure."

## Usage Examples

- `/hook "Why your AI content gets zero traction"` — 5 hooks with default settings (yt-long, medium format)
- `/hook "AI agents for non-coders" --platform yt-shorts --format short` — short-form hooks optimised for Shorts
- `/hook "How I built a content engine in one weekend" --no-polish` — fast draft, skips Claude polish
- After `/ideation` → user picks an idea → type `/hook topic="<chosen idea>"` to continue

## Notes

- Trained on the Kallaway framework: all 10 hook patterns from `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` are embedded in `prompts/hook.md` and injected at runtime.
- AI cascade: Ollama/Gemini draft → Claude polish. Use `--no-polish` to skip the polish pass (faster, cheaper — draft quality only).
- Prompt source of truth: `prompts/hook.md`. Edit that file to change hook generation behaviour globally.
- Works standalone or as step 2 after `/researcher` and before `/outline`.
- Output path: `Content-Hub-Vault-V2/05-Hooks/`
