---
status: Completed
date: 2026-05-28
type: session_summary
tags: [command-center, visualization, pipeline-loop, dashboard, html]
description: "Built an HTML command center to visualize self-improvement loop iterations — KPIs, run list, per-run iteration chart, per-skill leaderboard, prompt SHA timeline. Live local server reads pipeline_results.tsv."
---

# Session: Self-Improvement Command Center — HTML Dashboard

## What Was Done

Built a live HTML dashboard to visualize the data produced by the autoresearch loop from [[2026-05-28_Self-Improvement-Loop-Execution]]. Reads `pipeline_results.tsv` and renders four views (per user spec): KPI row, run list, per-run iteration chart, per-skill leaderboard, and prompt SHA timeline.

## Architecture

Two-file delivery — no build step, no npm:

- [app/command_center.html](app/command_center.html) — single-page dashboard, vanilla JS + Chart.js (CDN). Parses TSV client-side, groups rows by `(run_id, timestamp[:second])` into iterations, averages `metric_value` across same-iteration rows to derive composite.
- [app/serve_command_center.py](app/serve_command_center.py) — tiny `http.server` launcher on `localhost:8765`. Serves the HTML at `/` and `pipeline_results.tsv` at `/pipeline_results.tsv` with `Cache-Control: no-store` so Refresh always reads the latest TSV.

## Views

1. **KPI row** — total runs, total iterations, kept rate (real runs only), skills covered.
2. **Run list** — most recent first; columns: run_id, skill, iter count, baseline / final / best composite, delta, kept/reverted counts, last-seen UTC. Click a row to load it into the iteration chart.
3. **Iteration trajectory** — line chart of composite per iteration for a selected run. Points are color-coded: green=kept, red=reverted, amber=dry-run. Tooltip shows full metrics dict + prompt_sha.
4. **Per-skill leaderboard** — horizontal bar chart of best composite per skill across all iterations logged.
5. **Prompt SHA history** — per-skill scrollable timeline of every iteration with the prompt_sha (truncated to 12 chars), a `▶` marker when SHA changed vs prior row, kept/reverted/dry pill, and composite score.

## Design Decisions

- **Live server over static generator**: chosen by user — avoids regenerating the HTML after every loop iteration.
- **Group by `(run_id, ts_to_second)`**: handles both real runs (multiple metric rows per iteration sharing a timestamp) and autoresearch dry-runs (one `metric_value` row per iteration). No schema change needed.
- **Composite = average of `metric_value` across grouped rows**: mirrors `prompt_lab/loop.py::_compute_composite` exactly, so chart values match keep/revert decisions.
- **Dark theme, no framework**: zero install footprint; Chart.js loads from `cdn.jsdelivr.net`.

## How to Run

```
python app/serve_command_center.py
```

Opens browser at `http://localhost:8765/`. After running `/pipeline-loop` (or `python -m prompt_lab.loop --skill hook --dry-run`), hit Refresh to reload the latest TSV.

CLI flags: `--port 9000` to change port, `--no-open` to skip the auto-browser-open.

## Files Changed

### Net new
- [app/command_center.html](app/command_center.html) — dashboard SPA
- [app/serve_command_center.py](app/serve_command_center.py) — launcher (syntax-checked via `py_compile`)

### Modified
- None — surgical, additive.

## Outstanding

1. **Real-run validation** — dashboard is functional against the 28 existing dry-run rows; not yet validated against post-`/prompt-lab` real-run TSV growth (gated by [[The-Self-Improvement-Loop]] §9 scorer trust).
2. **Live auto-refresh** — currently manual Refresh button; could add `setInterval` polling once real runs start producing data continuously.
3. **Filter controls** — no skill/date filters yet; deferred until run count grows.

## Semantic Edges

- **Implements:** Visualization layer for [[The-Self-Improvement-Loop]]
- **References:** [[2026-05-28_Self-Improvement-Loop-Execution]] (data source — TSV schema + loop semantics)
- **Reads:** `Content-Hub-Vault-V2/00-Management-V2/pipeline_results.tsv` (A1 schema)
- **Reads:** [prompt_lab/loop.py](prompt_lab/loop.py) (`_compute_composite` mirrored client-side)
- **Modifies:** [[Current_Sprint]] (Command Center deliverable → ✓)

## Related

[[Local_First_Skill_Engine_Plan]] · [[Refined_Pipeline]]
