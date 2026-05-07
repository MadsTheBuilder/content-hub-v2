# /ideation

Read vault research notes for a topic and generate 9 ranked video ideas with gap analysis, competitive reasoning, and audience desire mapping. Run this after `/yt-pipeline` has produced a research brief.

## Trigger
User types `/ideation` with a topic.

## Execution Steps

1. Get the topic from the user (inline or ask if not provided): "What topic should I ideate on?"
2. Check that research files exist in `Content-Hub-Vault-V2/10-Research/` — if none, remind the user to run `/yt-pipeline` first.
3. Confirm before running: "Generating ideas for: [topic] using [research file] — confirm?"
4. Wait for user confirmation.
5. Run: `python -m skills.ideation --topic "<topic>"`
6. Report: output file path + preview of the top-ranked idea.

## Output

Writes one file to `Content-Hub-Vault-V2/02-Ideas/YYYY-MM-DD_<slug>.md` containing:
- 9 ranked video ideas
- Each with: angle, gap filled, audience desire, competitive signal, hook direction, format recommendation

## After Completion

Report:
- Path to the ideas file
- The Rank 1 idea title and angle (2-3 lines)
- Remind the user: "Review the list, pick one idea, then run `/hook topic=\"<chosen>\"` to draft the opening."

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
- All 9 ideas are written to the vault. You pick which one to pursue.
- The prompt source of truth is `prompts/ideation.md`.
