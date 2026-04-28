---
name: orchestrate-harness
description: Step-by-step manual run spec for validating /orchestrate and /resume-orchestration
---

# Orchestrate Skill — Manual Eval Harness

Run every check below in order. Each one has a clear pass/fail. Any failure = do not ship.

## Preconditions

- Working tree is clean (`git status` shows nothing).
- The fixture file `fixtures/01_minimal.md` exists at `.claude/skills/orchestrate/evals/fixtures/01_minimal.md`.
- `Content-Hub-Vault/00-Management/Orchestrations/` contains only `README.md` (no stale state files).

## Run A: Happy path (`/orchestrate` end-to-end)

| # | Step | Pass criteria |
|---|------|---------------|
| A1 | In a fresh session, type `/orchestrate` followed by the fixture task (copy from `fixtures/01_minimal.md` § "User request"). | Skill announces "I'm using orchestrated-execution…" and reads `orchestrated-execution.md`. |
| A2 | Advisor dispatches the Phase 1 recon agent. | Tool call shows `Agent(subagent_type="Explore", model="haiku", …)`. If `model` is missing or `model="opus"`, **FAIL**. |
| A3 | Advisor reads `AGENTS.md` and produces a Phase 2 plan. | Plan has 2 groups and 3 tasks, matches the fixture's expected decomposition. |
| A4 | Advisor writes a state file to `Content-Hub-Vault/00-Management/Orchestrations/`. | A file exists with today's date. Its frontmatter has `status: awaiting-approval`, `current_group: null`, `groups_complete: []`. |
| A5 | Advisor presents the plan and waits for user approval. | No file writes beyond the state file. No executor agents dispatched. |
| A6 | Operator approves: "yes, proceed". | State file frontmatter flips to `status: approved`, then `status: executing` before the first dispatch. Status log has a new `approved` line. |
| A7 | Advisor dispatches Group 1 in parallel (single message, multiple Agent calls). | All Group 1 agents run in parallel. Each dispatches with `model="sonnet"` or `model="haiku"` per the saved prompts. |
| A8 | After Group 1 summaries return, advisor processes results and dispatches Group 2. | No file conflicts. Group 2 agents run. |
| A9 | Phase 6 verification runs. | Advisor reads the files modified, reports what changed, state file flips to `status: complete`. |
| A10 | All files modified match the fixture's "expected writes" list. | No files outside the expected list were touched. |

**If A1–A10 all pass:** Run A succeeded. **Cleanup:** revert the fixture-expected changes and delete the state file, then proceed to Run B.

## Run B: Resume after approval (`/resume-orchestration`)

Simulates the original failure: plan is approved, context is lost, user re-enters.

| # | Step | Pass criteria |
|---|------|---------------|
| B1 | Manually create a state file at `Content-Hub-Vault/00-Management/Orchestrations/2026-04-20_harness-resume.md` by copying the file from Run A (from before Phase 4 dispatched) and setting `status: approved`, `current_group: null`, `groups_complete: []`. | File exists and is well-formed. |
| B2 | In a fresh session, type `/resume-orchestration`. | Skill announces, lists the one active file, asks to confirm resume. |
| B3 | Operator confirms: "yes". | Advisor reads `orchestrated-execution.md` and `AGENTS.md`, then updates state file to `status: executing`, `current_group: 1`. Dispatches Group 1. |
| B4 | Complete to Phase 6 as in Run A. | State file reaches `status: complete`. Files modified match the fixture. |

**If B1–B4 all pass:** Run B succeeded. **Cleanup:** revert fixture changes and delete the state file.

## Run C: Resume mid-execution

Simulates compaction during Phase 4 between groups.

| # | Step | Pass criteria |
|---|------|---------------|
| C1 | Create a state file with `status: executing`, `current_group: 1`, `groups_complete: []`. Set the Agent prompts section to match the fixture. | File exists. |
| C2 | `/resume-orchestration` in a fresh session. Operator confirms resume. | Skill asks: "Group 1 was in flight. Continue from Group 2 or re-run Group 1?" |
| C3 | Operator says "continue". | State file updates: `current_group: 2`, `groups_complete: [1]`. Advisor dispatches Group 2 only. |
| C4 | Phase 6 runs. | State file → `status: complete`. **Only Group 2 agents were dispatched** during this run. |

**Cleanup:** revert fixture changes and delete the state file.

## Run D: Stale-state filtering

| # | Step | Pass criteria |
|---|------|---------------|
| D1 | Create a state file with `status: abandoned` and a second file with `status: complete`. | Both files exist. |
| D2 | `/resume-orchestration` in a fresh session. | Skill reports "No active orchestrations found" and stops. Does not prompt to resume either file. |

**Cleanup:** delete the two test state files.

## Run E: Malformed state file

| # | Step | Pass criteria |
|---|------|---------------|
| E1 | Create a state file missing the `status` field in frontmatter. | File exists. |
| E2 | `/resume-orchestration` in a fresh session. | Skill reports the file is malformed, tells operator what's missing, asks whether to abandon or fix. Does not dispatch any agent. |

**Cleanup:** delete the test file.

## Result log (scratch, do not commit)

```
Run A:  [ ]  Date: ____  Notes:
Run B:  [ ]  Date: ____  Notes:
Run C:  [ ]  Date: ____  Notes:
Run D:  [ ]  Date: ____  Notes:
Run E:  [ ]  Date: ____  Notes:
```

Failures? Diagnose and re-run the whole harness. The skill is not regression-safe until all five runs pass in one sitting.