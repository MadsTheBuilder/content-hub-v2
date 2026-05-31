---
date: 2026-05-31
type: session-log
tags: [webapp, pipeline, frontend, full-pipeline]
description: "New Full Pipeline web page running trends→research→ideation→hook→outline→title→cascade→short-form with a human approve/pick gate per stage that auto-runs the next stage; frontend-only, build verified."
---

# Session — Full Pipeline Page (auto-run, human-in-the-loop)

**Implements:** [[Full Pipeline Page]]
**Modifies:** [[App]], [[Sidebar]], [[styles.css]]
**References:** [[useJobStream]], [[StageWorkspace]], [[DistributionWorkspace]], [[api.js]], [[MarkdownViewer]], [[OutputBrowser]], [[VaultPicker]]

## Goal

Add a single new page to the web app (`Design-doc/web`) that runs the **entire content pipeline end-to-end** with a human gate at every stage. The user enters a seed, picks/approves each stage's output, and the **next stage runs automatically** with that selection threaded into its input.

Chain (confirmed scope, hook step included):

```
trends → research → ideation → hook → outline → title → cascade → short-form
```

Two product decisions confirmed with the user:
- **Trends source:** instant vault list (`04-Trends`, subfolders) **+ a Refresh button** for a fresh scan.
- **Scope:** full chain through short-form.

## What changed

- **NEW** `Design-doc/web/src/FullPipelinePage.jsx` — page-level state machine, one `useJobStream`, vertical stepper. Drives all 8 stages through `runStage(stage, body)` and routes each completed job's `primary_path` / bundle into the next stage's input.
- **EDIT** `Design-doc/web/src/App.jsx` — import + `full-pipeline` view render, accent (`#06B6D4`), Tweaks "Jump to screen" option.
- **EDIT** `Design-doc/web/src/Sidebar.jsx` — dedicated `Rocket` nav button (its own divider block, **not** inside the per-stage `PIPELINE` array — it is the whole chain, not one stage).
- **EDIT** `Design-doc/web/src/styles.css` — appended a small stepper block (`.fp-*`) reusing existing design tokens (`--bg-surface`, `--border`, `--r-card`, `--stage-*`). No new token system.

**No backend / skill / prompt changes** — every stage already had an endpoint, body model, and result resolver. Frontend-only (§3 Surgical Changes).

## Gate model — approve vs pick

- **Pick gates** (output is a discrete list → chosen item becomes a *string* downstream): **ideation** (`### Rank N — Title`), **title** (`- **Title**`). Each has a **mandatory manual text-input fallback** when parsing yields < 2 items.
- **Approve gates** (output is a *single* file the next skill consumes whole): **research**, **hook**, **outline**, **cascade** — review in `MarkdownViewer`/`OutputBrowser`, then continue.
- **trends** = pick from vault list (+Refresh); **short-form** = terminal (done).

## Path threading (integration contract)

`trendPath → research` · `briefPath → ideation/hook/cascade/short-form` · `ideaTitle → hook/outline/title` · `hooksPath → outline` · `outlinePath → title/cascade/short-form` · `titleString → cascade/short-form`.

## Failure / conflict handling

- Job `failed` → inline error banner on that stage + working **Retry** (re-issues the same `runStage` call); the rest of the run is preserved.
- `ConflictError` (single-job server guard) on any launch → friendly "another job is already running" message instead of a crash. The sequential chain never self-conflicts.

## Verification

- `npx eslint src/FullPipelinePage.jsx src/App.jsx src/Sidebar.jsx` → 0 errors (2 intentional exhaustive-deps warnings, consistent with codebase norm).
- `npx vite build` → clean, 196 modules. `dist/` is gitignored.

## Open items

- **Live end-to-end run still pending** — needs the backend (`uvicorn` on :8765) + `npm run dev` (:5173) and real skill spend (multi-minute, real API calls). Left for the user to run via `start.ps1` / `npm run dev`. Verify in particular: trends pick → research auto-run, the 9-idea parse, title parse, and both distribution bundles in `OutputBrowser` at the terminal step.

See [[Current_Sprint]].
