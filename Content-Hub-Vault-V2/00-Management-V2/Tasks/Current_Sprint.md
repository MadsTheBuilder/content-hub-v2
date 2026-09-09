---
date: 2026-05-15
updated: 2026-05-22 (session 2)
tags: [sprint, tasks]
description: "Active sprint tasks for Content Hub V2 — tracks completed, in-progress, and next-up work items with links to session logs."
---

# Current Sprint

## In Progress — Full Pipeline Page (2026-05-31)

- [x] **Full pipeline state loss + ideation naming (2026-05-31)** — See [[2026-05-31_Full_Pipeline_State_Loss_Ideation_Name_Fix]]
  - Bug 1 fixed: `App.jsx` switched from conditional render to `display:none` wrapper — component stays mounted across tab switches, all `useState` preserved.
  - Bug 3 fixed: `approveResearch` now sends `research.niche.trim() || seed.trim()` instead of `seed` — ideation gets a real topic even when the top-level seed input was left blank.
  - Bug 2 (research file naming) — **pending user clarification**: current format `2026-05-31_design_brief.md` is `{date}_{niche}_brief.md`; user expects repo name included but exact format TBD.

- [x] **Research config gate + options** — picking a trend now opens a Research config form (instead of auto-running) on `FullPipelinePage.jsx`: niche (editable, prefilled, **required**), `fast/deep` mode toggle, target-length, and a collapsed Advanced section (tone/audience/banned, all optional → `brief.md` defaults when blank). Fixes the empty-niche crash (`--niche is required`) by disabling **Run Research** until a niche is entered. Backend: `ResearcherBody` + `run_researcher` forward `--target-length/--tone/--audience/--banned-phrase`; no `researcher.py` change (flags already exist via [[brief_args]]). Build + lint clean. **Backend restart (`--reload`) needed to load new body fields.** See [[2026-05-31_Research_Options_Config_Gate]].

- [x] **Full Pipeline auto-run page** — new `Design-doc/web/src/FullPipelinePage.jsx` chains all 8 stages (trends → research → ideation → hook → outline → title → cascade → short-form) with a human-in-the-loop gate at each step; selecting a result auto-runs the next stage. Reuses [[useJobStream]], `runStage`/`readVaultFile` (`api.js`), `MarkdownViewer`, `OutputBrowser`, `VaultPicker`. Wired into `App.jsx` (new `full-pipeline` view + accent + Tweaks jump) and `Sidebar.jsx` (Rocket nav button). Build + lint clean (196 modules, 0 errors). **Live end-to-end run still pending** (needs backend + dev server; real skill spend). See [[2026-05-31_Full_Pipeline_Page]].

## Completed — Webapp Sprint (2026-05-22 → 2026-05-29)

- [x] **Design-doc web app wiring** — See [[Webapp_sprint]]
  - Mini-phase breakdown of [[Design_Doc_Web_App_Plan]] across 7 phases (Scaffold → Backend → Frontend port → Wire 5 stages → Distribution multi-tab → Dashboard/Brain/polish → Launch + E2E).
  - 14–19h total estimate; supersedes [[Content_Hub_Web_Design_Spec]] and [[Wrapper_Plan]] (Streamlit).
  - **Plan reconciled with prototype updates (2026-05-22)** — see [[Design_Doc_Web_App_Plan]] § Runtime note + § Prototype updates. Changes: SourcesPanel added to component list + Frontend Port + Phase 1 copy list; canvas instruction corrected (particles.js creates its own canvas dynamically — no `<canvas>` in `web/index.html`); React 19.2.6 (Vite) documented as the resolved version vs prototype's CDN React 18.
  - **Phase 1 (Scaffold) — done, pending browser verify**: `Design-doc/web/` (Vite + React 19.2.6 + `react-markdown` + `clsx`) and `Design-doc/server/` (FastAPI shell + `/api/health` + CORS) both boot; assets (`styles.css`, `particles.js`, `Icons.jsx`, `SourcesPanel.jsx`) ported to `web/src/`; runtime documented in [[runtime|Design-doc/server/runtime.md]]; Vite proxy `/api → :8765` wired. Shared runtime follow-up completed: repo `.venv` is the source of truth (Python 3.12.10), missing wrapper deps were installed, and the FastAPI/Streamlit compatibility gap was closed by reconciling the shared pins. See [[2026-05-22_Webapp_Phase1_Scaffold]] + [[2026-05-22_Webapp_Phase1_Resync]] + [[2026-05-22_Webapp_Phase1_Runtime_Fix]] (re-sync after prototype updates: `styles.css` 2096→2644, `Icons.jsx` +3 icons, new `SourcesPanel.jsx` 794 lines with `useState` import + named/default exports).
  - **Phase 2 (Backend) — complete**: All endpoints shipped and smoke-tested. See [[2026-05-22_Webapp_Phase2_Backend]].
    - `server/jobs.py` — job registry + asyncio.Queue SSE bus + single-job constraint
    - `server/pipeline.py` — 8 subprocess wrappers + stage output resolvers
    - `server/vault.py` — recent/read_file/outputs with path-traversal guard
    - `server/brain.py` — Claude CLI analysis (no separate API key)
    - `server/main.py` — full router: health + vault + jobs/stream + 8 pipeline + brain endpoints
    - All smoke tests passed: health ✅, title job end-to-end ✅, SSE streaming ✅, 409 conflict ✅, vault/recent ✅, vault/file ✅
  - **Phase 3 (Frontend port) — complete**: All 7 verification blockers fixed and confirmed. See [[2026-05-23_Webapp_Phase3_Frontend_Port]] (original session) + [[2026-05-23_Webapp_Phase3_Lint_Fix]] (verification fixes).
    - `Brain.jsx` — removed bogus `./StackedPanel` import; both `StackedPanel` + `SourcesPanel` now imported from `./SourcesPanel.jsx`
    - `TweaksPanel.jsx` — `TweakSection` prop renamed `label` → `title` (matches App.jsx call sites); removed unused `handleOpen`; `react-refresh/only-export-components` suppressed on `useTweaks` export; `react-hooks/refs` suppressed narrowly on `offsetRef` render-read and `valueRef` render-write (both are intentional drag-perf patterns)
    - `SourcesPanel.jsx` — duplicate `"outline-rag"` key resolved; distribution tree entry renamed to `"dist-outline-rag"`
    - `StageWorkspace.jsx` — `react-hooks/set-state-in-effect` + `exhaustive-deps` suppressed on the stage-reset effect (intentionally keyed on `stageId` only)
    - `particles.js` — removed unused `t` accumulator; `catch (e)` → `catch {}` (optional binding)
    - Build: ✅ clean (`vite build`) · Lint: ✅ clean (`eslint .`)
  - **Phase 4 (Wire 5 stages) — complete**: `api.js`, `useJobStream.js`, `VaultPicker.jsx`, `MarkdownViewer.jsx`, `OutputBrowser.jsx` created; `StageWorkspace.jsx` + `SourcesPanel.jsx` rewritten; `App.jsx` cleaned. Build + lint clean (187 modules). Live verification run 2026-05-24: ideation + hooks produce real vault files; SSE streams correctly; history drawer returns real artifacts. Research SSE works but researcher skill requires non-empty `--repos` — with the playbook payload (`repos: []`) no file is written (skill CLI gap, not frontend defect). Agent memory notes 01–08 absent (execution-record gap). See [[2026-05-24_phase4-wire-stages]].
  - **Phase 5 (Distribution multi-tab) — complete + verified (2026-05-29)**: `DistributionWorkspace.jsx` + 5 tab files (`OutlineTab`, `TitleTab`, `CascadeTab`, `ShortFormTab`, `VoiceCleanupTab`) created; `Sidebar.jsx` consolidated (title/outline removed); `App.jsx` routes to `DistributionWorkspace`; `Dashboard.jsx` Outline card links to `#distribution/outline`. Hash routing without router library. Build + lint clean (193 modules). Step 5.8 full-chain verification passed 2026-05-29: all 5 Distribution endpoints confirmed, all vault artifacts dated today, 409 constraint confirmed. See [[2026-05-24_Webapp_Phase5_Distribution]] + [[2026-05-29_Phase5_FullChain_Verification]].
  - **Phase 6 (Dashboard + Brain + polish) — complete**: `usePipelineSnapshot` hook + `jobActivity.js` created; Dashboard live recents; Sidebar dynamic status dots + health badge; Brain real analysis via `runBrainAnalysis` + `useJobStream`; `ConflictError` + 409 inline notices wired in StageWorkspace + Brain + all 5 Distribution tabs; TweaksPanel already localStorage-clean. Build + lint clean (195 modules, 0 problems). See [[2026-05-24_phase6-dashboard-brain-polish]].
  - **Phase 7 (Launch + E2E) — complete (2026-05-29)**: `start.ps1` created. 9/9 stages produced real vault output in browser-facing acceptance run. 3 pipeline bugs fixed (hook.py argparse, StageWorkspace.jsx URL flush, vault.py subdirectory listing). Brain: all 5 fields confirmed. 409: human-readable notice confirmed. 14 post-sprint polish items deferred. See [[2026-05-29_Design_Doc_Web_App_Wired]].
  - **Phase 5/6 repair pass — complete (2026-05-29)**: 4 runtime bugs fixed per [[2026-05-29_Phase5_Phase6_Bug_Fix_Plan]]. Brain reads `result.data` correctly; snapshot refreshes on focus + job settle; Distribution status rolls up across all 4 output folders; hardcoded Dashboard stats removed; static SourcesPanel demo data (~270 lines) deleted. Build + lint clean. Browser-facing acceptance (Phase 7 re-run) still needed. See [[2026-05-29_Phase5_Phase6_Bug_Fixes_Applied]].

- [x] **Design-doc theme rewrite + system graph (2026-05-27)** — See [[2026-05-27_Design_Doc_Theme_And_Graph]]
  - `Design-doc/systems-deck.html` fully reskinned to V2 design system (Inter + JetBrains Mono, `#0D0F12` palette, per-slide `--page-accent` ambient gradients via `data-accent` + JS)
  - `Design-doc/graph.html` created — interactive D3.js v7 force-directed graph, 29 nodes × 6 types, 40 directed edges × 6 link types; click-to-focus, legend toggle, zoom/pan

- [x] **Self-Improvement Loop — structural build (2026-05-28)** — See [[2026-05-28_Self-Improvement-Loop-Execution]] (Implements: [[The-Self-Improvement-Loop]] + [[Self-Improvement-Loop-Tasks]])
  - Six-agent dispatch executed: A1 (tracking foundation) → A2 (8 fixtures, Maximum Realism) → A3 (8 LLM-judge scorers + `_judge.py`) → A5 (`brief.md` + `brief_loader` + 8 skills wired) → A4 (`prompt_lab/loop.py` — dry-run verified, 3 rows written to TSV) → A6 (`.claude/skills/pipeline-loop/SKILL.md` shell with §9 fragility caveat).
  - User overrides applied: Phase 7 webapp skipped; build all 5 Opportunities full scope; LLM-judge YES; brief HYBRID (file + CLI overrides); fixtures MAXIMUM REALISM; agents ASK on ambiguity.
  - A5 hit session limit at 5/8 skills wired — orchestrator closed gap on `researcher.py`, `short_form.py`, `voice_cleanup.py` (4-line surgical wiring each).
  - **Status:** structural only. Functional validation (scorer trust, loop convergence, prompt-beats-baseline) requires first real `/prompt-lab` run — out of scope this sprint, burns NLM/NIM credits.
  - **Next:** run `/prompt-lab --skill hook --iterations 20` against real model + review `pipeline_results.tsv` for convergence before `/pipeline-loop` is permitted to fire.

- [ ] **Vault graph audit — 3 open decisions (2026-05-28)** — See [[2026-05-28_Vault_Graph_Audit]]
  - `notebooklm-py/tests/` (35 MB VCR cassettes) — remove unless patching the library
  - `10-Research/` PDFs/PNGs (~55 MB) — user deciding
  - `thinking/` session JSONLs (7.7 MB, grows) — user deciding retention policy

- [x] **Graph embedded in systems deck as slide 11 (2026-05-28)** — See [[2026-05-28_Graph_Embedded_In_Deck]]
  - Diagnosed graph sizing bug: `clientWidth = 0` at parse time because SVG was inside a hidden `position:absolute` slide
  - Embedded graph as slide 11 in `systems-deck.html` with lazy D3 init (`setTimeout(initGraph, 80)` triggered from `go()` on first visit); SVG reads real dimensions after slide is visible

- [x] **Auto-compaction settings** — See [[2026-05-22_Settings_AutoCompact]]
  - Added `autoCompactEnabled: true` + `autoCompactWindow: 100000` to `.claude/settings.json`
  - Fires at 100k tokens (schema minimum; ~50% of a 200k window); applies to all sessions in this project

- [x] **Phase 4 execution playbook** - See [[2026-05-23_phase4-wire-5-stages]]
  - Subagent-per-task runbook for [[Webapp_sprint]] Phase 4
  - Each worker writes its own memory note under `Design-doc/web/src/.agent-context/phase4/`
  - Final verification agent acts as the eval gate before sprint docs can be marked complete

- [x] **Root file organisation (2026-05-26)** — See [[2026-05-26_Root_File_Organisation]]
  - Eight stranded root files moved into purposeful folders: Streamlit trio → `app/`, daily script → `scripts/`, `.bat` launchers → `bin/`, stale one-offs → `archive/`.
  - Path constants in moved files updated (`.parent` → `.parent.parent`) and subprocess calls in [[control_room.py]] re-pathed for `github_trending.py`.
  - Verified: `py_compile` clean, runtime import smoke test resolves VAULT/REPO/ROOT to correct project paths.

- [x] **V1 strip execution (2026-05-26)** — See [[2026-05-26_Cleanup_Execution]] (Implements: [[2026-05-26_Cleanup_Verification]])
  - Stripped V1 keys/packages from [[.env]], [[.env.example]], [[requirements.txt]]; trimmed stale paths from [[.claude/settings.json]] + [[.gitignore]]; deleted [[.claude/worktrees/]] (~395 MB).
  - [[graphify-out/GRAPH_REPORT.md]] replaced with stale-marker; `/graphify --update` deferred to interactive run.
  - Verified: `import skills.pipeline`, `from skills.utils import ai`, and full `scripts/github_trending.py` run all clean.

## Completed — Pipeline Bug Fix + Claude-First Cascade (2026-05-19)

- [x] **Pipeline hardening** — See [[2026-05-19_Pipeline_Bug_Fix_Claude_First]]
  - Fixed 6 bugs from [[2026-05-19_Refined_Pipeline_E2E_Test]]: ideation `--topic`, slug alignment (hyphens everywhere), NIM timeout 15s, Claude CLI stderr logging, `_ollama_available()` skip check, Claude-first cascade
  - 6 files changed: `skills/utils/ai.py`, `skills/pipeline.py`, `skills/yt_pipeline.py`, `skills/title.py`, `skills/research_plan.py`, `skills/research_sources.py`
  - All 5 verification criteria passed loop 1
  - **Post-session fix**: B_NEW — `--outline-path` renamed to `--outline-file` in `pipeline.py:162,175` (steps 7 & 8 would have crashed with argparse rc=2)
  - **Next**: Re-run full E2E (`python -m skills.pipeline "topic" "url"`) to confirm clean 9/9 pass

## Completed — NIM Eval Run (2026-05-15)

- [x] **NIM full-pipeline eval** — See [[2026-05-15_NIM_Eval_Pipeline_Run]]
  - Ran pipeline against *Claude Code Has Evolved* (`https://www.youtube.com/watch?v=d86VCtQ_dN8`)
  - Fixed `skills/pipeline.py` — added `_SUBPROCESS_ENV` with `PYTHONPATH` so subprocess skills can import from project root
  - All outputs archived to `Content-Hub-Vault-V2/NIM test run/`; eval report at [[NIM test run/EVAL_REPORT.md]]
  - **3 bugs confirmed — pending fixes:**
    1. `skills/yt_pipeline.py:28` — `SECTION_PATTERN` uses `.+` with `re.DOTALL`; must be `[^\n]+` — root cause of empty research file
    2. `skills/utils/ai.py:88` — NIM errors log blank string; HTTP status + body not captured before exception handler
    3. `skills/pipeline.py:64` + `skills/hook.py` — hook step not passed `--research-file`; hooks generated blind from topic title only

## Completed — Outline Skill-Creator Loop (2026-05-15)

- [x] **Outline SKILL.md improvement** — See [[2026-05-15_Outline-Skill-Creator-Improvement-Loop]]
  - Added YAML frontmatter with pipeline position (Step 3 of 7) and explicit /cascade routing to `.claude/skills/outline/SKILL.md`
  - Added Step 3 (10-Research/ scan) and improved hook-number handling; snapshot at `.claude/skills/outline-workspace/skill-snapshot/SKILL.md`
  - 6-agent eval run (3 evals × with_skill + without_skill); net: 0.87 vs 0.88 — tie/marginal loss due to eval 2 regression
  - **Win — Eval 1**: 6/6 vs 5/6 — /cascade routing is the differentiator
  - **Regression — Eval 2**: 3/5 vs 4/5 — new skill drops --hook-path when file missing (wrong) and asks platform confirmation for default (unnecessary)
  - Static HTML viewer at `.claude/skills/outline-workspace/iteration-1/eval_review.html`
  - **Next**: patch eval 2 regression (add explicit --hook-path passthrough guard + no-defaults-confirmation note), re-run eval 2 only

## Completed — Hook Skill-Creator Loop (2026-05-15)

- [x] **Hook SKILL.md improvement** — See [[2026-05-15_Hook-Skill-Creator-Improvement-Loop]]
  - Added YAML frontmatter with pushy description to `.claude/skills/hook/SKILL.md`; added Pipeline Position section (Step 2 of 7: researcher → **/hook** → outline)
  - 6-agent eval run (3 evals × with_skill + old_skill); benchmark: +0.103 pass rate delta (100% vs 89.7%)
  - 2 failing assertions for old_skill: no pipeline reference (eval-1), no --no-polish acknowledgment in confirmation (eval-3)
  - Static HTML viewer at `.claude/skills/hook-workspace/iteration-1/eval_review.html`
  - Eval 2 (topic-with-flags) non-discriminating — both skills pass 7/7; replace with bare /hook test in iteration 2

## Completed — Voice-Cleanup Skill-Creator Loop (2026-05-15)

- [x] **Voice-Cleanup SKILL.md improvement** — See [[2026-05-15_Voice_Cleanup_Skill_Improvement]]
  - Rewrote `.claude/skills/voice-cleanup/SKILL.md` with YAML frontmatter, pipeline position (Step 7 of 7), smart no-args path inference, and explicit batch folder mode
  - 6-agent eval run (3 evals × with_skill + old_skill); benchmark: +0.58 pass rate delta (100% vs 43%)
  - Eval 3 (batch folder) was 5/5 vs 0/5 — batch mode was completely missing from old skill
  - Static HTML viewer at `.claude/skills/voice-cleanup-workspace/iteration-1/eval_review.html`
  - Eval 2 (specific file) non-discriminating — both skills pass 5/5; replace in iteration 2

## Completed — Researcher Skill-Creator Loop (2026-05-15)

- [x] **Researcher SKILL.md improvement** — See [[2026-05-15_Researcher_Skill_Creator_Loop]]
  - Rewrote `.claude/skills/researcher/SKILL.md` with YAML frontmatter, pipeline position (Step 1 of 7), defined brief output structure, mandatory /hook handoff
  - 6-agent eval run (3 evals × with_skill + old_skill); benchmark: +0.08 pass rate delta, stddev halved
  - Static HTML viewer at `.claude/skills/researcher-workspace/iteration-1/eval_review.html`
  - Iteration 2 pending user feedback from viewer

## Completed — Researcher Optimisation (2026-05-13)

- [x] **Researcher Optimisation** — See [[Researcher_Optimisation]], [[2026-05-13_Researcher_Optimisation_Complete]]
  - Goal: deep doc crawler + readable 5-section brief, on top of the existing semantic verification baseline ([[2026-05-13_Researcher_Source_Verification_Agent]])
  - Modifies: [[skills/researcher.py]], [[prompts/researcher.md]], new `skills/researcher_crawler.py`

  ### Phase 1 — Deep documentation crawler ✓
  - [x] 1.1 Create `skills/researcher_crawler.py` with `discover_primary_docs()`
  - [x] 1.2 GitHub Contents API probe (reuse `_gh_headers()` pattern)
  - [x] 1.3 Priority ranker: README → docs/index → quickstart → CONTRIBUTING/ARCHITECTURE → docs/*.md → examples
  - [x] 1.4 Raw fetch via `raw.githubusercontent.com`
  - [x] 1.5 Cap at 6 primary docs (`--max-primary-docs`, default 6)
  - [x] 1.6 Wire into `researcher.py` between README step and web research
  - [x] 1.7 Smoke-test on doc-rich + doc-sparse repos

  ### Phase 2 — Audit + improve Haiku verification ✓
  - [x] 2.1 Read current verify code end-to-end
  - [x] 2.2 Add "wrong entity" failure-mode example to prompt
  - [x] 2.3 Treat short/empty `get_guide()` summaries as "keep, with warning"
  - [x] 2.4 Log warning on Haiku-call failure (currently silent)
  - [x] 2.5 Extend tool schema to return `reasons: dict[source_id, str]`
  - [x] 2.6 Verify on `mercury-agent` + `terax-ai` cases

  ### Phase 3 — Context extraction & injection ✓
  - [x] 3.1 Add `extract_repo_context()` helper
  - [x] 3.2 Haiku tool-use returns `core_use_cases / key_concepts / common_patterns / anti_patterns / audience`
  - [x] 3.3 Render to markdown block
  - [x] 3.4 Prepend to `chat.configure(custom_prompt=...)`
  - [x] 3.5 Add `{repo_context}` placeholder in `prompts/researcher.md`
  - [x] 3.6 Spot-check that answers reference context concepts

  ### Phase 4 — Brief reformatter ✓
  - [x] 4.1 Collect 11 answers + context + sources into structured payload
  - [x] 4.2 Synthesis call (Haiku first, upgrade to Sonnet if flat)
  - [x] 4.3 Output 5 sections: What it does / Who it's for / How it works / When to use / Watch out for
  - [x] 4.4 Append `## Sources` with one-line summaries
  - [x] 4.5 Append `## Raw findings` in collapsed `<details>` block
  - [x] 4.6 Keep existing frontmatter
  - [x] 4.7 Output path unchanged
  - [x] 4.8 User reads cold + confirms

  ### Phase 5 — Slides + infographics ✓
  - [x] 5.1 Build artifact instruction string from context + brief
  - [x] 5.2 `generate_slide_deck(instructions=...)`
  - [x] 5.3 `generate_infographic(instructions=...)`
  - [x] 5.4 Poll via existing `wait_for_completion()`
  - [x] 5.5 Log artifact URLs/IDs into brief frontmatter
  - [x] 5.6 Confirm artifacts reflect actual research

## Completed This Session

- [x] **Research Guardrails (all 5)** — See [[2026-05-08_Research_Guardrails_Implementation]]
  - `skills/research_sources.py` (new) — primary-source pre-flight
  - `skills/research_plan.py` (new) — QuestionPlan dedup + follow-up generator
  - `prompts/research_followups.md` (new) — drill-down prompt
  - `prompts/yt_pipeline.md` — Q8 competitive + Q10-12 angle battery (12 total)
  - `prompts/researcher.md` — Lens 7.5 competitive + Angle Battery output section
  - `skills/yt_pipeline.py` — pre-flight + QuestionPlan loop + frontmatter tracking
  - `skills/researcher.py` — pre-flight + Angle Battery per repo
  - `skills/ideation.py` — `primary_sources_found: 0` warning

## Failed / Parked

- [x] ~~**TRIBE v2 fMRI Content Scoring**~~ — **FAILED (2026-05-11)** — See [[2026-05-11_TRIBE_v2_LLaMA_CPU_Fix]]
  - LLaMA 3.2-3B text pipeline takes ~32 min for a full document; Windows hard-kills the process at ~10 min every run (6 attempts)
  - exca's per-process caching means zero progress accumulates across kills
  - **Parked as future production item**: re-evaluate when scoring real video content (audio/video path suits TRIBE better than raw text; T4/A100 cloud GPU would remove the kill issue entirely)
  - See [[2026-05-11_TRIBE_v2_Analysis_VRAM_Debug]] for all patches applied

## Completed — Researcher Source Quality

- [x] **Researcher source verification agent** — See [[2026-05-13_Researcher_Source_Verification_Agent]]
  - Reverted `_repo_keywords()`, `_is_relevant_source()`, and keyword filtering block
  - Built semantic verification: `sources.get_guide()` per discovered source → Claude Haiku `keep_sources` tool call (batched) → `source_ids=verified_source_ids` on all `chat.ask()` calls
  - Option A (Claude API, `AsyncAnthropic()`) — `anthropic==0.39.0` confirmed present
  - Primary sources (repo URL + README) always kept; only web-research-discovered sources go through verification

## In Progress — Other

- [ ] **Control Room Wrapper — Smoke Test** — All 4 files built. See [[2026-05-12_Control_Room_Build]]
  - `vault_index.py` ✓, `runner.py` ✓, `control_room.py` ✓, `run_control_room.bat` ✓
  - Streamlit 1.57.0 installed. `.vscode/settings.json` created to fix venv auto-activation.
  - **Blocked on:** opening a new VS Code terminal and running `python -m streamlit run control_room.py`
  - Resume: see [[2026-05-12_Control_Room_Build]] § Exact Resumption Steps

## Completed — Refined Pipeline Implementation (2026-05-19)

- [x] **Refined Pipeline — NLM-Driven Content Engine v1** — See [[2026-05-19_Refined_Pipeline_Implementation]]
  - Full implementation of [[Refined_Pipeline]] approved 2026-05-19
  - Removed hardcoded `_RESEARCH_QUESTIONS` + `_ANGLE_BATTERY` from `researcher.py`; replaced with NLM-driven loop via `seed_questions_from_nlm` + `QuestionPlan(budget=15)` + `generate_followups()`
  - Removed `PROMPTS_FILE`, `SECTION_PATTERN`, `_load_questions()` from `yt_pipeline.py`; same NLM-driven loop
  - Rewrote `pipeline.py` from 5-step to 9-step orchestrator with per-step voice-cleanup hooks
  - Studio steps wired: step 2 calls `studio.generate_reports()`, step 9 calls `studio.inject_cascade_and_generate()` — both read `notebook_id` from `research.md` frontmatter
  - Twitter → Instagram rename throughout `cascade.py` + `prompts/cascade.md`
  - New modules: `skills/helpers/nlm_seed.py`, `skills/helpers/nim_picker.py`, `skills/studio.py`
  - NIM error logging fixed in `skills/utils/ai.py` (HTTP status + 500-char body preview)
  - Verified by 4-agent parallel loop (Validator + Smoke Tester + Verifier), 2 iterations, ALL CLEAR
  - **Next: E2E pipeline run in next session** (burns NLM/NIM credits — user's instruction)

## Completed — Trends UI Fix + 404 (2026-05-31)

- [x] **Trends stage UI redesign + 404 resolved** — See [[2026-05-31_Trends_UI_Fix_404_Resolved]]
  - Removed `isTrends` hardcoded markdown-viewer branch from `InputZone`; Trends now uses the standard form (textarea, file drop, URL field, Run button) matching the approved design.
  - Added URL input support for Trends stage; updated `handleRun` body builder to send `{ space: prompt }`.
  - Backend: added `TrendsBody` model to `main.py`; `pipeline.py` `run_trends` now accepts and forwards `--space` arg.
  - 404 root cause: server running old `main.py` without `--reload`. Fix: restart with `.venv/Scripts/python.exe -m uvicorn main:app --app-dir Design-doc/server --port 8765 --reload` (forward slashes for Git Bash).
  - **Open**: `scripts/github_trending.py` ignores `--space` for now — future work to add argparse and niche filtering.

## Completed — Trends Job Fix (2026-05-31)

- [x] **Trends "Job failed" root cause fixed** — See [[2026-05-31_Trends_Job_Fixed_Subprocess]]
  - Root cause: `asyncio.create_subprocess_exec` raises `NotImplementedError` on Windows with uvicorn's `SelectorEventLoop`.
  - Fix: replaced with `loop.run_in_executor(None, lambda: subprocess.run(...))` in [[pipeline.py]]. Tradeoff: SSE output arrives batch-at-end instead of line-by-line.
  - Also wired `--space` argparse in [[github_trending.py]] (was forwarded by pipeline but silently ignored).
  - Verified: job ran 3m 13s, status `completed`, vault file written.
  - **Open**: Phase 7 E2E acceptance re-run (all 9 stages).

## Completed — Pipeline Post-Mortems (2026-06-01)

- [x] **Obsidian WikiLinks plan verification** — See [[2026-06-01_Obsidian-Wiki-Plan-Verification]]
  - Verified the YouTube transcript via `yt-dlp` captions and checked the live open-notebook OpenAPI schema.
  - Confirmed the plan's core idea is sound: master wiki index -> topic index -> relevant markdown articles is exactly the pattern described in the video.
  - Correction: open-notebook can accept raw text sources through `/api/sources/json` (`type: text`, `content`, `title`); the local `open_notebook_client.py` simply has not wrapped that API yet.
  - Recommended next slice: build `/wiki-gen`, generate `01-Knowledge/wiki/`, add index-based retrieval, then inject selected wiki article text into [[researcher.py]].

- [x] **CloakBrowser research run deep audit** — See [[2026-06-01_CloakBrowser-Research-Notebook-Audit]]
  - Full execution trace: notebook `6828efa7-f920-4ae3-ac4d-d85d5e770779` | 2 sources (GitHub page + raw README)
  - **RC-1**: QUERY_URL quota (`GenerateFreeFormStreamed`) pre-exhausted by ARIS run — first `chat.ask` immediately returned `UserDisplayableError` (HTTP 200, error in body, not HTTP 429); traced to `_chat.py:591–613`
  - **RC-2**: `extract_repo_context` subprocess failed silently (`researcher.py:209` exception handler); empty `RepoContext` fed into chat config + synthesis prompt
  - **RC-3**: `synthesize_brief` data-contract breakage — `claude -p` spawns a full agent that writes `research.md` to disk and returns a status message, not brief text; meta file body is always the confirmation string, not the brief
  - **RC-4**: Deep research returned 0 web sources (brand-new viral repo, no indexed content); empty observation file is correct behavior, not a failure
  - 5 structural problems logged: silent exception swallowing in context extraction, `synthesize_brief` agent vs synthesis contract, no retry on QUERY_URL rate limit, `nlm_seed.py` redundant client, stale `_DEFAULT_BL` (March 1, 2026)
  - **Actions needed**: add retry/backoff on `ChatError` in Q&A loop; restructure `synthesize_brief` to return text or make two-file pattern explicit; fix `nlm_seed.py` to use existing client; update `_DEFAULT_BL` from live session capture

- [x] **ARIS research run audit** — See [[2026-06-01_ARIS-Research-Notebook-Audit]]
  - Same QUERY_URL rate-limit pattern; Claude subprocess recovered via pre-captured trend card in [[04-Trends/wanshuiyin_ARIS-in-AI-Offer]]
  - Established that QUERY_URL and batchexecute are separate quota surfaces

## Completed — Research Runs (2026-06-01)

- [x] **academic-research-skills research run** — See [[2026-06-01_Academic-Research-Skills-Research-Run]]
  - Repo: `Imbad0202/academic-research-skills` | 25K stars, 685/day velocity
  - Brief: [[10-Research/2026-06-01_research_academic-research-skills_brief]]
  - Known issues: `extract_repo_context` timeout + `seed_questions_from_context` JSON parse failure (same RCs as [[2026-06-01_CloakBrowser-Research-Notebook-Audit]])
  - **Next**: `/ideation research`

## Next Up

- [x] **End-to-end verification** — TypeScript/nexu-io run scored 5/5 guardrails post-fix. See [[2026-05-08_Researcher_Fix_Verified]]. OpenMythos dogfood run was the trigger; verification confirmed on a clean topic.

- [x] **researcher.py fix verified** — See [[2026-05-08_Researcher_Fix_Verified]] — 5/5 guardrails pass. Root cause was passing `prompts/researcher.md` blob to NotebookLM; fixed with `_RESEARCH_QUESTIONS` individual questions pattern.
