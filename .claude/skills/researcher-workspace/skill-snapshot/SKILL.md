# /researcher

Run isolated content gap research on selected trending repos. You must pick which repos to research — the skill never auto-selects from the trending file.

## Trigger
User types `/researcher` with a niche.

## Execution Steps

1. Get niche from user (inline with command or ask if not provided). Example: `AI agents`, `local LLMs`, `open-source tools`.
2. List available repos so the user can pick:
   `python -m skills.researcher --list`
3. Show the list to the user. Ask which repos they want to research.
4. Wait for the user to specify repos.
5. Confirm before running: "Running researcher on: [repo1, repo2] — niche: [niche] — confirm?"
6. Wait for confirmation.
7. Run: `python -m skills.researcher --niche "[niche]" --repos owner/repo1 owner/repo2`
   - For faster research: add `--mode fast`
8. Report: output file path + the "Recommended Video Angle" from each repo section in the brief.

## Inputs

- `--niche` — required. The topic label used to name the brief. Quoted string.
- `--repos` — required. One or more `owner/repo` slugs (space-separated). Never run without this.
- `--mode fast|deep` — optional. Default `deep` (~5 min per repo). Use `fast` only for quick sanity checks.
- `--list` — list available repos from the trending file and exit (no research run).

## Output

`Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md` containing one section per repo:
- Repo URL and notebook ID (for manual follow-up in NotebookLM)
- Discovered sources count (after relevance filtering)
- Content gap analysis anchored to the specific repo

## Source Quality Guardrails (built into the pipeline)

- After web research completes, sources are filtered: only GitHub URLs and sources whose title/URL matches the repo name are kept. Off-topic sources are dropped before import.
- Before asking questions, `chat.configure()` is called with a custom prompt that names the specific repo and instructs NotebookLM to ignore unrelated sources.
- If no relevant sources survive filtering, a WARNING is printed and the answers will be flagged as unreliable.

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
- Deep mode: budget ~8 min per repo (web research + 75s indexing wait + 11 questions).
- After reviewing the brief, the next command is `/hook topic="<chosen angle>"`.
