# /hook

Generate 5 Kallaway-trained hook variations for a video topic — the first 30 seconds that stop the scroll and open a curiosity loop. Each variation uses a different Kallaway hook pattern with a Spoken Line, Visual Cue, Text Overlay, and one-sentence psychological rationale.

## Trigger
User types `/hook` with a topic.

## Execution Steps

1. Get the topic from the user's message. If not provided, ask: "What topic should I write hooks for?"
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

## After Completion

Report:
- Full path to the hooks file
- The ⭐ recommended hook's Spoken Line (one line)
- Next step prompt: "Review all 5 variations and pick one. Then run `/outline topic=\"{topic}\" --hook-path \"{path}\"` to build the full Dopamine Ladder structure."

## Usage Examples

- `/hook "Why your AI content gets zero traction"` — 5 hooks with default settings (yt-long, medium format)
- `/hook "AI agents for non-coders" --platform yt-shorts --format short` — short-form hooks optimised for Shorts
- `/hook "How I built a content engine in one weekend" --no-polish` — fast draft, skips Claude polish

## Notes

- Trained on the Kallaway framework: all 10 hook patterns from `Content-Hub-Vault-V2/01-Knowledge/marketing_brain.md` are embedded in `prompts/hook.md` and injected at runtime.
- AI cascade: Ollama/Gemini draft → Claude polish. Use `--no-polish` to skip the polish pass (faster, cheaper — draft quality only).
- Prompt source of truth: `prompts/hook.md`. Edit that file to change hook generation behaviour globally.
- Works standalone or as the first step before `/outline`.
- Output path: `Content-Hub-Vault-V2/05-Hooks/`
