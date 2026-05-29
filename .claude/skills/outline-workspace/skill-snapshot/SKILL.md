# /outline

Generate a full Dopamine Ladder video outline for a topic. Maps the entire video across 6 psychological stages — Stimulation → Captivation → Anticipation → Validation → Affection → Revelation — with per-section duration targets, talking points, visual markers ([B-ROLL], [SHOW SCREEN], [TEXT OVERLAY]), and head fakes. Works standalone or after `/hook`.

## Trigger
User types `/outline` with a topic.

## Execution Steps

1. Get the topic from the user's message. If not provided, ask: "What topic should I outline?"
2. Check if the user has a hook file from a prior `/hook` run. If yes, note the path for `--hook-path`. If no hook file exists, continue — the hook is optional but produces a tighter outline when provided.
3. Confirm target length (default 8 min) and platform (default yt-long).
4. Run:
   ```
   python -m skills.outline "{topic}" [--hook-path "{path/to/hook.md}"] --length {n} --platform {platform}
   ```
   Add `--no-polish` if the user wants a faster or cheaper draft.
5. Wait for completion. Report the vault path and preview the Stage 2 (Captivation) section.

## Output

Writes one file to `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md` containing:
- 6 sections mapped to Dopamine Ladder stages with target durations
- Per section: Dopamine Goal + Talking Points + Visual Notes + Head Fake (where applicable) + Transition
- CTA section (0:30–0:45) with specific next-video hook

## After Completion

Report:
- Full path to the outline file
- Total estimated runtime (sum of all section durations)
- Next step prompt: "Review the outline for accuracy. Prep any screen shares or demos listed. Then film — the outline is your shooting script."

## Usage Examples

- `/outline "Why your AI content gets zero traction"` — standalone 8-min outline, no hook file
- `/outline "AI agents for non-coders" --hook-path "Content-Hub-Vault-V2/05-Hooks/2026-05-06_ai-agents-for-non-coders.md" --length 10` — builds on a prior /hook run, targets 10 min

## Notes

- The Dopamine Ladder is the structural backbone: every section is explicitly labeled by stage and psychological purpose.
- Works best after `/hook` — the hook content injects into the outline prompt so sections build on it coherently. Without a hook, the outline is still valid but more generic.
- AI cascade: Ollama/Gemini draft → Claude polish. Polish pass checks that all 6 stages are present, visual markers appear in every section, and head fakes appear at least twice.
- Use `--no-polish` to skip Claude and get a faster structural skeleton (Ollama/Gemini only).
- Prompt source of truth: `prompts/outline.md`. Edit that file to change outline generation behaviour globally.
- Output path: `Content-Hub-Vault-V2/06-Outlines/`
