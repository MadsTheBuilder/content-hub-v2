# /title

Take a video concept and generate 10 compelling YouTube titles — 5 Tier-1 safe options and 5 Tier-2 experimental options — with thumbnail text suggestions, informed by top-30 competitor titles in the niche.

## Trigger
User types `/title [concept]` with a video concept description.

## Execution Steps

1. Get video concept from user (inline with command or ask if not provided)
2. Confirm concept before running: "Running title generation on: [concept] — confirm?"
3. Wait for user confirmation.
4. Run: `python -m skills.title "[concept]"` (concept must be quoted to handle spaces)
5. Report results: show the file path created + list the 5 Tier-1 safe titles

## Output

Title creates 1 file in `Content-Hub-Vault-V2/07-Titles/YYYY-MM-DD_<slug>.md`:

- `YYYY-MM-DD_<slug>.md` — Markdown file with 10 titles (5 safe + 5 experimental), thumbnail text suggestions, and metadata

The file is written to the Obsidian vault. No auto-publishing — review titles and choose the best fit for your thumbnail design.

## After Completion

Report:
- Path to the output file in `Content-Hub-Vault-V2/07-Titles/`
- List the 5 Tier-1 safe titles generated

## Usage Examples

- `/title how I built a RAG pipeline that actually works` → generates 10 titles with thumbnail suggestions
- `/title` → asks for concept, then generates titles

## Notes

- Output goes to `Content-Hub-Vault-V2/07-Titles/` — this is the Obsidian vault.
- Titles are informed by competitor analysis (top 30 titles in the niche loaded from `skills/data/competitor_titles.json`).
- Tier-1 titles are safe, algorithm-friendly, broad-appeal options.
- Tier-2 titles are experimental, niche-specific, or high-curiosity-gap options — higher risk, higher reward.
- Review the generated titles and choose based on your content angle and audience.
- Thumbnail text suggestions are tailored to each title for visual consistency.
