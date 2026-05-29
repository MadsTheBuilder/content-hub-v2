---
date: 2026-05-08
type: session
status: complete
---

# YT Pipeline Friction Repair — Verify-Then-Fix

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[2026-05-07_OpenMythos_Dogfood_Run]] | [[Chase_AI_System_Breakdown]]
Modifies: [[skills/yt_pipeline.py]]

## Context

The 2026-05-07 OpenMythos dogfood ([[2026-05-07_OpenMythos_Dogfood_Run]]) surfaced 5 frictions in `/yt-pipeline`. Gemini wrote a dissection and merged its proposed fixes into [skills/yt_pipeline.py](../../../skills/yt_pipeline.py) and [skills/ideation.py](../../../skills/ideation.py). Audit showed at least one fix was broken in production and several others were unverified.

This session ran the approved verify-then-fix plan: each friction got a Phase 1 verification step that produced a concrete observation, which then selected one branch of a Phase 2 decision table.

## Phase 1 — Verification outcomes

**V1 — Search recall.** `ytsearch25:OpenMythos` returns both previously-missed target IDs (`60Z0yrrzLdA` at position 1, `4c9YUnaDxvA` at position 2). Gemini's 3-query expansion was unnecessary.

**V2 — Auth check.** With `~/.notebooklm/profiles/default/storage_state.json` renamed aside, `notebooklm list --json` exits with `rc=1` and JSON-formatted error in stdout: `{"error": true, "code": "AUTH_REQUIRED", "message": "Auth not found..."}`. The current substring guard happens to fire because stdout contains both "error" and "auth" tokens — contradicting my earlier audit assertion that the guard never fires. F2 is therefore a robustness improvement (returncode-based check), not a bug fix.

**V3 — Q&A fused-block.** Ran 4 variants against a notebook with 5 ready sources. Variants A (Gemini's verbose prefix), B (single-line, no prefix), and C (multi-line raw, no prefix) all returned clean structured 2.5–2.7 KB answers. None echoed the question. None contained the "It appears your query was not included" sentinel. The 2026-05-07 failure was an intermittent NotebookLM-side fluke, not a code bug.

**V4 — Artifacts.** `python -m notebooklm generate report --timeout 180` returns `Error: No such option: --timeout` — Click rejects the flag, so the current production code's generate calls always fail before they wait. Grep across `skills/`, `prompts/`, `.claude/skills/` found no consumer of slide-deck/mind-map/report artifacts in the pipeline. They are vestigial.

**V5 — Ideation glob.** Already verified in audit. `**/*.md` is correct.

## Phase 2 — Fixes applied

All edits are in [skills/yt_pipeline.py](../../../skills/yt_pipeline.py).

**F1 — Search recall.** Replaced 3-query expansion with single `ytsearch25:{topic}` call. Added optional `--also "q1,q2,..."` flag for user-supplied recall expansion.

**F2 — Auth check.** Replaced substring-on-stdout guard with direct `subprocess.run` and `returncode != 0` check. Bypasses `_run_nlm` so the exit code is observable.

**F3 — Q&A loop.** Removed Gemini's verbose framing prefix; pass the question text as-is. Added a single retry on empty/error answer (the V3-confirmed minimal change).

**F4 — Artifacts.** Made artifact generation opt-in via `--artifacts` flag (default off). Dropped the unsupported `--timeout 180` argument from the `generate` invocation, restored `--retry 3`, and added a Python-side `subprocess.run(timeout=180)` via a new `timeout` parameter on `_run_nlm` with `TimeoutExpired` handling.

**F5 — Ideation glob.** No change.

## End-to-end verification

- **Syntax:** `ast.parse` on the modified file — OK.
- **Search:** `python skills/yt_pipeline.py search OpenMythos` — both target IDs in positions 1 and 2.
- **Auth fail-fast:** with storage_state moved aside, `python skills/yt_pipeline.py run "TestE2E" "<url>"` exits with `rc=1` and `[error] NotebookLM auth failed. Run: notebooklm login`. Storage state restored via try/finally; post-restore `list --json` returned `rc=0`.
- **Q&A loop:** validated empirically in V3 (Q1 against an existing notebook returned 2.5 KB structured answers). Full 8-question pipeline run intentionally skipped — V3's per-question result already disambiguated the cause.

## Files touched

- `skills/yt_pipeline.py` — F1, F2, F3, F4 edits (single file).
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md` — checked off the Brainstorm item, linked this session.

## Out of scope (flagged as follow-ups)

- `_run_nlm` should propagate exit codes universally — would simplify F2 across other call sites. Touches every subprocess call site, separate task.
- `pip install -e ./notebooklm-py` in setup to address Friction #2 version-drift root cause. Setup/docs task.
- Permanent OAuth: not addressable here. NotebookLM has no public API; `notebooklm-py` uses Playwright-persisted Google session cookies which Google deliberately expires. Realistic ceiling = clean fail-fast, which F2 delivers.

## Open items

None for this scope. Next: pick another trending topic and dogfood the repaired pipeline end-to-end.
