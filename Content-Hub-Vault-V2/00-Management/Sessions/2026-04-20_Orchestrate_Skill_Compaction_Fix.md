---
title: Orchestrate Skill — Compaction Recovery Fix
date: 2026-04-20
tags: [session, orchestrate, skills, fix]
---

# 2026-04-20 — Orchestrate Skill: Compaction Recovery Fix

## What was done

Diagnosed why the `/orchestrate` skill failed mid-run during the 2026-04-17 Phase 4 A/B-testing frontend attempt (Phases 1–3 completed, Phases 4–6 never executed). Root cause was that the workflow never persisted the plan to disk — when context compacted between Phase 3 (approve) and Phase 4 (execute), the plan, the subagent prompts, and the task structure were all lost from chat.

Implemented a minimum-viable recovery fix scoped to the user's preferences (vault-based state file, separate resume skill, Haiku recon, manual eval harness). Did NOT pre-inline AGENTS.md specialist definitions or add between-group checkpoints — both flagged as recommended deferrals in the plan file.

## Changes

### Modified
- [orchestrated-execution.md](../Superpowers/orchestrated-execution.md) — Added top-level "State Persistence (required)" section, added `model="haiku"` to Phase 1 recon dispatch, added "Persist the plan to disk" step at end of Phase 2, added status-update instructions in Phases 3/4/6, updated Common Mistakes Never/Always list.
- [.claude/skills/orchestrate/SKILL.md](../../../.claude/skills/orchestrate/SKILL.md) — Cross-linked to `/resume-orchestration`, noted state file location, marked Haiku model for recon.

### Created
- [Content-Hub-Vault/00-Management/Orchestrations/README.md](../Orchestrations/README.md) — Explainer for the new state-file folder (naming, structure, status lifecycle, cleanup).
- [.claude/skills/resume-orchestration/SKILL.md](../../../.claude/skills/resume-orchestration/SKILL.md) — New skill. Reads the active state file from the Orchestrations folder, confirms with user, resumes at the correct phase based on recorded status.
- [.claude/skills/orchestrate/evals/README.md](../../../.claude/skills/orchestrate/evals/README.md) — Eval harness explainer.
- [.claude/skills/orchestrate/evals/harness.md](../../../.claude/skills/orchestrate/evals/harness.md) — Manual run spec with five runs (happy path, resume-approved, resume-executing, stale filtering, malformed file).
- [.claude/skills/orchestrate/evals/fixtures/01_minimal.md](../../../.claude/skills/orchestrate/evals/fixtures/01_minimal.md) — Synthetic 3-task, 2-group `/ping` endpoint fixture for the harness.

## Root causes addressed

1. **No disk persistence** — fixed. Phase 2 now writes a state file with frontmatter status.
2. **No resume entry point** — fixed. New `/resume-orchestration` skill reads the state file and continues.
3. **Recon inherits Opus** — fixed. Phase 1 dispatch now hard-codes `model="haiku"`.
4. **No test harness** — fixed (manual). Five-run checklist exercises happy path plus four edge cases.

## Deferred (documented for future iteration)

1. **Pre-inline AGENTS.md specialist definitions into saved agent prompts at Phase 2.** Would eliminate the need to load AGENTS.md in advisor context at Phase 4 dispatch — the single largest remaining compaction risk. Called out in the workflow file and in the plan file.
2. **Between-group checkpoint writes.** Would turn resume granularity from group-level to task-level. Trivial cost, but user chose to defer.

Residual failure mode: if context compacts *during* Phase 4 (between groups, or mid-group dispatch on a very large group), we lose the in-flight group on resume. Acceptable for now.

## Verification status

- File-level verification: all new/modified files exist and have valid frontmatter. The `resume-orchestration` skill is now visible in the skills list (confirmed in-session).
- End-to-end harness run: **not yet executed.** The harness requires a fresh session and will exercise the fixture against the updated workflow. Run this before closing out the task tracker.

## Outstanding

- Run the `orchestrate/evals/harness.md` Runs A–E in a fresh session to validate the fix works end-to-end.
- Phase 4 A/B testing frontend work remains stranded — by user choice, not picked up this session. Next time, invoke `/orchestrate` against the frontend tasks and the new persistence layer should prevent a repeat failure.
- Consider enabling the two deferred items (pre-inline AGENTS.md, per-group checkpoints) after one real post-fix `/orchestrate` run surfaces whether residual context pressure actually bites.

## Plan file

[what-happened-this-session-mighty-beaver.md](../../../../.claude/plans/what-happened-this-session-mighty-beaver.md) — full pre-execution plan including context, root causes, scope, deferred items.
