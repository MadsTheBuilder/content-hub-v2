---
name: researcher
description: >-
  Step 1 of 8 in the content production pipeline (/researcher → /ideation → /hook → /outline →
  /title → /cascade → /short-form → /voice-cleanup). Runs deep content-gap research on GitHub
  trending repos via NotebookLM and outputs a dated research brief to Content-Hub-Vault-V2/10-Research/.
  Use this skill whenever the user types /researcher, says "research a topic", "find content gaps",
  "what should I make a video about", "check trending repos", "run research on [topic]", "I want
  to start a new video", or asks what to research next. Also trigger when the user wants to kick
  off the production pipeline from scratch — /researcher is always the entry point. Always
  suggest /ideation as the next step after the brief is reviewed.
---

# /researcher — Content Gap Research

Step 1 of the production pipeline. Produces a research brief with a recommended video angle per repo, saved to `Content-Hub-Vault-V2/10-Research/`. The brief feeds into `/ideation` to generate ranked video ideas.

## Interaction Flow

1. **Get niche** — inline with `/researcher <niche>` or ask if not provided.
   Example niches: `AI agents`, `local LLMs`, `open-source tools`

2. **List available repos** so the user can pick:
   ```
   python -m skills.researcher --list
   ```
   Show the numbered list to the user.

3. **Ask which repos** to research. Wait for the user to specify.

4. **Confirm before running**:
   > "Running researcher on: [repo1, repo2] — niche: [niche] — confirm?"

5. **Wait for confirmation**, then run:
   ```
   python -m skills.researcher --niche "[niche]" --repos owner/repo1 owner/repo2
   ```
   Add `--mode fast` only if the user explicitly wants a quick sanity check.

6. **Report results**:
   - Full path to the brief file
   - The "Recommended Video Angle" from each repo's section
   - Notebook IDs listed in the frontmatter (for NotebookLM follow-up)

## CLI Reference

| Flag | Required | Description |
|------|----------|-------------|
| `--niche` | Yes | Topic label for the output file, e.g. `"AI agents"` |
| `--repos` | Yes | One or more `owner/repo` slugs (space-separated) |
| `--mode fast\|deep` | No | Default `deep` (~8 min/repo). `fast` for quick checks only |
| `--backend notebooklm\|open-notebook\|auto` | No | Default `notebooklm`. Use `open-notebook` when Docker backend is ready. |
| `--list` | — | List repos from trending file and exit (no research run) |

Never omit `--repos`. Never auto-select repos without the user's explicit choice.

## Output

`Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<niche-slug>_brief.md`

Each repo section contains:
- Repo URL and NotebookLM notebook ID
- Synthesized 5-section brief (What it does / Who it's for / How it works / When to use / Watch out for)
- Recommended Video Angle — the key field for `/hook`
- Raw Q&A (collapsed) for deeper inspection

## Source Quality Guardrails (built into the pipeline)

- Sources are filtered post-research: only GitHub URLs and title/URL matches to the repo are kept
- `chat.configure()` anchors NotebookLM to the specific repo before any questions are asked
- If no relevant sources survive filtering, a WARNING is printed; answers are flagged as unreliable

## Prerequisites

**notebooklm (default):**
- `notebooklm login` must have run (auth at `~/.notebooklm/storage_state.json`)
- `Content-Hub-Vault-V2/04-Trends/github_trending.md` must exist with GitHub repo URLs

**open-notebook (not yet in use — pending full implementation):**
- Docker running + `docker compose up -d` from the open-notebook directory
- API reachable at `http://localhost:5055` (or set `OPEN_NOTEBOOK_BASE_URL`)
- AI provider configured in open-notebook (Claude via `ANTHROPIC_API_KEY`, or Ollama for free local)
- Model override via `OPEN_NOTEBOOK_MODEL` env var (default: `claude-haiku-4-5-20251001`)

## Timing

- **open-notebook**: ~5–6 min per repo (primary docs only, no web research phase)
- **notebooklm deep**: ~8 min per repo (web research + 75s indexing + 15 questions + synthesis)
- **notebooklm fast**: ~3–4 min per repo
- Each repo gets its own isolated notebook — no cross-contamination

## After Completion → Next Step

After reviewing the brief, the next command is:
```
/ideation <niche>
```
Always surface this suggestion when presenting results.
