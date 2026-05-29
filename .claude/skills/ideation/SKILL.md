---
name: ideation
description: >-
  Step 2 of 8 in the content production pipeline (/researcher → /ideation → /hook → /outline →
  /title → /cascade → /short-form → /voice-cleanup). Reads vault research briefs and generates
  9 ranked video ideas with gap analysis, competitive reasoning, and audience desire mapping.
  Use this skill whenever the user types /ideation, says "generate ideas", "what video should
  I make", "give me video ideas", or asks what to do after research. Always trigger after
  /researcher completes. After showing the 9 ideas, ask the user to pick one before suggesting
  /hook — this choice determines the entire downstream pipeline.
---

# /ideation

Step 2 of the production pipeline. Reads vault research briefs and generates 9 ranked video ideas, then waits for the user to choose one before handing off to `/hook`.

## Pipeline Position

**Step 2 of 8:** `/researcher` → **/ideation** → `/hook` → `/outline` → `/title` → `/cascade` → `/short-form` → `/voice-cleanup`

- **Comes after:** `/researcher` — uses the research brief for the topic
- **Comes before:** `/hook` — the chosen idea becomes the topic for hook generation

## Execution Steps

1. Get the topic from the user (inline or ask if not provided): "What topic should I ideate on?"
2. Check that research files exist in `Content-Hub-Vault-V2/10-Research/` — if none, remind the user to run `/researcher` first.
3. Confirm before running: "Generating ideas for: [topic] using [research file] — confirm?"
4. Wait for user confirmation.
5. Run: `python -m skills.ideation --topic "<topic>"`
6. Report: output file path + the full numbered list of 9 ideas (title + angle, 1–2 lines each).

## After Completion — BLOCKING GATE

After showing the 9 ideas, **do not suggest /hook yet**. Instead, ask:

> "Which idea do you want to pursue? Reply with a number (1–9)."

Wait for the user's reply. Once they select a number, confirm:

> "Got it — going with idea #N: [title]. Next step: `/hook topic=\"<chosen title>\"` to draft the opening 30 seconds."

Only then suggest the `/hook` command with the exact chosen title as the topic.

## Output

Writes one file to `Content-Hub-Vault-V2/02-Ideas/YYYY-MM-DD_<slug>.md` containing:
- 9 ranked video ideas
- Each with: angle, gap filled, audience desire, competitive signal, hook direction, format recommendation

## Usage Examples

- `/ideation AI agents` → finds latest AI agents research file, generates 9 ideas
- `/ideation topic="machine learning for beginners"` → same with explicit topic
- `/ideation AI agents --research-file Content-Hub-Vault-V2/10-Research/2026-04-30_ai_agents.md` → uses a specific file

## Flags

- `--research-file <path>` — use a specific research file instead of auto-detecting by topic
- `--no-trends` — skip loading GitHub trending context (faster, use if trends file is stale)

## Notes

- Auto-detects the most recent research file whose name matches the topic. Falls back to the most recent file overall.
- Also loads `Content-Hub-Vault-V2/04-Trends/` (most recent file) as trending context — helps ideas stay timely.
- Uses Claude-first routing (`polish()`) — idea quality is premium work.
- All 9 ideas are written to the vault. The user picks which one to pursue — this drives the entire downstream pipeline.
- The prompt source of truth is `prompts/ideation.md`.
