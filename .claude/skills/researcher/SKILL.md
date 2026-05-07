# /researcher

Run isolated content gap research on each trending repo. Reads trend URLs from the vault, creates one NotebookLM notebook per repo (no overlap), runs web research per notebook, queries for content gaps, then compiles all findings into one brief.

## Trigger
User types `/researcher` with a niche.

## Execution Steps

1. Get niche from user (inline with command or ask if not provided). Example: `AI agents`, `local LLMs`, `open-source tools`.
2. Confirm before running: "Running researcher on niche: [niche] — confirm?"
3. Wait for confirmation.
4. Run: `python -m skills.researcher --niche "[niche]"`
   - For deeper research: `python -m skills.researcher --niche "[niche]" --mode deep`
5. Report: output file path + the "Recommended Video Angle" from each repo section in the brief.

## Inputs

- `niche` — required. The topic label used to name the brief. Quoted string.
- `--mode fast|deep` — optional. Default `deep` (~5 min per repo, broader web crawl). Use `fast` only for quick sanity checks.
- `--max-sources N` — optional. How many trend repo URLs to research. Default 8.

## Output

`Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md` containing one section per repo:
- Repo URL and notebook ID (for manual follow-up in NotebookLM)
- Discovered sources count
- Content gap analysis from `prompts/researcher.md`

## After Completion

Report:
- Full path to the brief file
- The "Recommended Video Angle" from each repo's section
- Notebook IDs listed in the frontmatter (for opening individual notebooks in NotebookLM)

## Prerequisites

- `notebooklm login` must have been run (auth stored at `~/.notebooklm/storage_state.json`)
- `Content-Hub-Vault-V2/04-Trends/github_trending.md` must exist and contain GitHub repo URLs

## Notes

- Each repo gets its own isolated NotebookLM notebook — no cross-contamination between repos.
- Notebooks are kept after the run. Find them at notebooklm.google.com via the notebook_ids in the brief frontmatter.
- Deep mode runs per-repo. With post-import indexing wait (75s) and a 5-min generation window, budget ~8 min per repo. Use `--max-sources 3` for a focused run (~24 min).
- After reviewing the brief, the next command is `/hook topic="<chosen angle>"`.
