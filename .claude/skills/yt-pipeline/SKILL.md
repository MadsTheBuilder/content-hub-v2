# /yt-pipeline

Research a topic by finding relevant YouTube videos, running them through NotebookLM, and writing the extracted analysis to the Obsidian vault.

## Trigger
User types `/yt-pipeline` with a topic name or YouTube URLs.

## Two Modes

### Mode A — Topic Search (user gives a topic)
1. Run: `python skills/yt_pipeline.py search "<topic>"`
2. Show the numbered results to the user (title, channel, views, URL)
3. Ask: "Which of these do you want to include? Give me numbers (e.g. 1,3,5) or paste additional URLs."
4. Wait for the user's selection before proceeding.
5. Proceed to the pipeline step below.

### Mode B — Direct URLs (user provides URLs)
1. Confirm the list of URLs with the user: "Running the pipeline on these N URLs — confirm?"
2. Wait for confirmation.
3. Proceed to the pipeline step below.

## Pipeline Step (runs after URL confirmation)
Run: `python skills/yt_pipeline.py run "<topic>" "<url1>,<url2>,..."`

This will:
- Create a new NotebookLM notebook titled `<topic> — YT Research`
- Add all URLs as sources and wait for processing
- Ask 8 analysis questions from `prompts/yt_pipeline.md`
- Write the full analysis to `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<topic>.md`

## After Completion
Report:
- Path to the output file
- NotebookLM notebook title and ID (for future reference)
- One-line summary of what was extracted

## Usage Examples
- `/yt-pipeline AI agents` → searches YouTube for "AI agents", shows results, user picks, runs pipeline
- `/yt-pipeline https://youtube.com/watch?v=abc https://youtube.com/watch?v=xyz` → direct run after confirmation
- `/yt-pipeline content strategy` → topic search mode

## Notes
- Always create a new notebook per topic — do not reuse existing notebooks.
- The `source wait` step can take 1–3 minutes per video. Show the user that it's processing.
- If NotebookLM returns an error on a source, skip it, note it in the output, and continue with remaining URLs.
- Output goes to `Content-Hub-Vault-V2/10-Research/` — this is the Obsidian vault.
