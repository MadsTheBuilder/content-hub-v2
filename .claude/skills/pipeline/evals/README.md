---
name: pipeline-evals
description: Manual test harness for validating interactive pipeline skill behavior — blocking gates, routing order, step number consistency
---

# Pipeline Evals

Manual regression-test checklist for the 8-step interactive content pipeline:
`/researcher → /ideation → /hook → /outline → /title → /cascade → /short-form → /voice-cleanup`

Run these after any change to any of the 8 SKILL.md files above.

## Files

- [harness.md](harness.md) — the step-by-step run spec (5 runs, ~15 min total)

## Running the evals

1. Start a fresh Claude Code session in the Content Hub working directory.
2. Read `harness.md` and follow each run in order.
3. Record pass/fail in the result log at the bottom of `harness.md`. Don't commit the filled-in log.
4. Any failed run = do not ship the change. Diagnose, fix, re-run the full harness.

## When to add new runs

Add a run when you find a new failure mode in production (e.g. "Claude suggested /outline before I picked a hook" or "researcher routed directly to /hook"). Each run should test one specific behavior and have a clear pass/fail.
