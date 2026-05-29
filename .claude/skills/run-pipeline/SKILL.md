# /run-pipeline

Fire the full content pipeline autonomously. NIM handles all LLM calls — no Claude tokens consumed during execution.

## Usage

```
/run-pipeline "<topic>" "<url1,url2,...>"
```

Example:
```
/run-pipeline "AI agents for developers" "https://youtube.com/watch?v=abc,https://youtube.com/watch?v=xyz"
```

## What Claude does

1. Parse topic and URLs from the user's command.
2. Run `python skills/pipeline.py "<topic>" "<url1,url2,...>"` **in the background** (use `run_in_background: true`).
3. Tell the user the pipeline has started and where output will appear.
4. **Stop.** Do not monitor, do not read output, do not follow up.

The pipeline runs autonomously. Output appears in the terminal. Vault files are written to `Content-Hub-Vault-V2/` under the topic slug.

## Pipeline steps (all use NIM)

1. Research — NotebookLM + NIM guardrails
2. Hooks — NIM draft
3. Outline — NIM draft
4. Short-form scripts — NIM
5. Distribution cascade — NIM (blog, Twitter, LinkedIn)

## Claude's response after firing

> Pipeline started for **"{topic}"**.
> Watch the terminal for live progress. Output lands in `Content-Hub-Vault-V2/` under `{today}_{slug}/`.
> I'm stepping away — come back when it's done.
