---
name: orchestrate-evals
description: Manual test harness for validating /orchestrate and /resume-orchestration skill behavior
---

# Orchestrate Evals

A manual regression-test checklist for the `/orchestrate` and `/resume-orchestration` skills. Run these after any change to:

- `.claude/skills/orchestrate/SKILL.md`
- `.claude/skills/resume-orchestration/SKILL.md`
- `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md`
- `Content-Hub-Vault/00-Management/Plans/AGENTS.md` (when specialist definitions change)

## Why manual?

Automating these evals would require a test runner that can spawn an Opus session, dispatch agents, and kill sessions mid-run. That's its own project and would itself need validation. A written checklist an operator can run in ~15 minutes is a better ratio of effort to regression-catch value for a single-user workflow.

## Files

- [harness.md](harness.md) — the step-by-step run spec
- [fixtures/01_minimal.md](fixtures/01_minimal.md) — a synthetic 3-task, 2-group scenario

## Running the evals

1. Start a fresh Claude Code session in the Content Hub working directory.
2. Read `harness.md` and follow each step in order.
3. Record pass/fail in the "Result log" section of `harness.md` for each run. Don't commit the filled-in log — use it as a scratch record during the run.
4. Any failed step = don't ship the change. Diagnose root cause, fix, re-run the full harness.

## When to add new fixtures

Add a fixture when you find a new failure mode in production use (e.g. "recon agent hallucinated a file" or "two tasks in the same group tried to edit the same file"). Each fixture should be small (≤5 tasks) and exercise one specific behavior.

## Cleanup after an eval run

- Delete any state file created under `Content-Hub-Vault/00-Management/Orchestrations/` during the run.
- Revert any files the executor agents modified on the fixture (the fixture spec says which files).
- `git status` should be clean before you start the next harness run.