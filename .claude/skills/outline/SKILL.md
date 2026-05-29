---
name: outline
description: >-
  Step 4 of 8 in the content production pipeline (/researcher → /ideation → /hook → /outline →
  /title → /cascade → /short-form → /voice-cleanup). Generates the Dopamine Ladder video script
  outline from an approved hook + research brief, then writes it to Content-Hub-Vault-V2/06-Outlines/.
  Use this skill whenever the user types /outline, says "write the outline", "build the outline",
  "structure the video", "create the video structure", "outline this video", "now outline it", or
  asks what to do after hook selection. Also trigger when the user has just picked a hook from
  /hook and says "what's next?", "continue the pipeline", "move forward", or "let's go" — /outline
  is always the next step after hook selection. Always suggest /cascade as the next step after the
  outline is reviewed.
---

# /outline

Generate the full Dopamine Ladder video outline — the complete structural shooting script for a YouTube video. This is Step 4 in the pipeline: after research (/researcher), ideation (/ideation), and hook selection (/hook), the outline maps everything into 6 psychological stages with durations, visual cues, and talking points ready to film from.

## What it reads

- **Approved hook** (from /hook): `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md` — the outline builds on the chosen hook so the full video is coherent from the first second.
- **Research brief** (from /researcher): `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>.md` — grounds Stage 4 (Validation) talking points in actual content gaps and data, not generic advice.

## Execution Steps

1. **Get topic**: Read from the user's message. If not provided, ask: "What topic is this outline for?"

2. **Locate the hook file**:
   - If the user gave a path or pasted hook content, use it directly.
   - Otherwise, scan `Content-Hub-Vault-V2/05-Hooks/` for the most recent file matching the topic slug.
   - If found, confirm: "Using the ⭐ recommended hook from [filename]. Say the hook number if you want a different one." If the user mentioned a specific hook number (e.g., "hook 2"), use that hook's section from the file.
   - If no hook file exists, proceed — the outline is still valid, just more generic.

3. **Locate the research brief**:
   - Scan `Content-Hub-Vault-V2/10-Research/` for a matching file. Pass it to the outline command so the draft pulls from real research rather than defaults.
   - If not found, proceed without it.

4. **Confirm parameters**: Target length (default 8 min) and platform (default yt-long). Only ask if the user hasn't already specified them.

5. **Run**:
   ```
   python -m skills.outline "{topic}" [--hook-path "{path}"] --length {n} --platform {platform}
   ```
   Add `--no-polish` if the user wants a faster or cheaper draft.

6. **Report**: Share the full vault path, preview the Stage 2 (Captivation) section, and suggest the next pipeline step.

## Output

Writes one file to `Content-Hub-Vault-V2/06-Outlines/YYYY-MM-DD_<slug>.md` with:
- 6 sections mapped to Dopamine Ladder stages with target durations
- Per section: Dopamine Goal + Talking Points + Visual Notes + Head Fake (where applicable) + Transition
- CTA section (0:30–0:45) with specific next-video hook

## After Completion

Report:
- Full path to the outline file
- Total estimated runtime (sum of all section durations)
- Next step: "Review the outline for accuracy. Prep any screen shares or demos listed. Then run **/cascade** to generate your blog post, LinkedIn post, and Twitter thread from this outline."

## Usage Examples

- After `/hook` approval: "Hook 2 looks great, let's outline it" — auto-locates the hook file, confirms hook choice, checks for research brief, defaults to 8 min yt-long.
- `/outline "Why your AI content gets zero traction"` — standalone, no hook file, 8 min default.
- `/outline "AI agents for non-coders" --hook-path "Content-Hub-Vault-V2/05-Hooks/2026-05-06_ai-agents-for-non-coders.md" --length 10` — explicit hook + 10 min target.

## Notes

- **Dopamine Ladder** is the structural backbone: Stimulation → Captivation → Anticipation → Validation → Affection → Revelation. Every section is labeled by stage and psychological purpose — don't skip or reorder stages.
- Research brief injection: if found, the brief's key findings are passed as context so Stage 4 (Validation) talks points reference real data and examples, not placeholders.
- AI cascade: Ollama/Gemini draft → Claude polish. Polish verifies all 6 stages are present, visual markers (`[B-ROLL]`, `[SHOW SCREEN]`, `[TEXT OVERLAY]`) appear in every section, and head fakes appear at least twice.
- `--no-polish` skips the Claude pass — faster and cheaper, but less verified structure.
- Prompt source of truth: `prompts/outline.md`. Edit that file to change outline generation globally.
- Output path: `Content-Hub-Vault-V2/06-Outlines/`
