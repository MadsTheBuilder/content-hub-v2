---
title: ORCH-001 Root Cause Analysis
date: 2026-04-22
type: session-log
tags: [orchestrate, bug, eval-harness, subagent-architecture]
---

# Session: ORCH-001 Root Cause Analysis

Investigates: [[2026-04-22_System_Bug_Orchestrate_Haiku_Recon_Dispatch]]
References: [[orchestrate skill]], [[orchestrated-execution]]
Modifies: [[orchestrate skill]]

## Summary

Closed ORCH-001 as `not-a-bug`. The persistent 0/3 eval failure on Haiku recon dispatch is an eval-harness architecture constraint, not a skill defect.

## Root Cause

The skill-creator eval workflow spawns a subagent per test case (see skill-creator/SKILL.md Step 1: *"For each test case, spawn two subagents in the same turn — one with the skill, one without."*). Spawned subagents in Claude Code do not have the `Agent` tool in their toolset — the Explore/Plan subagent schemas explicitly exclude it (*"All tools except Agent, ExitPlanMode, Edit, Write, NotebookEdit"*). Nested Agent dispatch is architecturally blocked.

The model's self-report — *"unable to invoke Agent() in this session context"* — is factually correct. Prompt-level fixes (soft → MUST → permission note) could not add a tool back that is not in the tool list; they only made the self-report more verbose.

## Key Evidence

1. skill-creator/SKILL.md Step 1 — eval runs via subagents, not top-level sessions.
2. Claude Code Agent tool schema — Explore/Plan subagent types exclude `Agent`.
3. [iteration-2 eval-1 transcript_summary.md:20](../../../orchestrate-workspace/iteration-2/eval-1-views-count/with_skill/outputs/transcript_summary.md) — subagent self-identifies *"in this constrained evaluation environment"*.
4. Fix-iteration pattern: 0/3 across soft/hard/permission framings. Invariant under prompt pressure because the gap is structural.

## On /model sonnet

The user's `/model sonnet` selection is not the cause. `/model` sets the main interactive session's model. Subagent toolsets are determined by agent-type definitions, not by the parent session's model. Opus in the same subagent context would fail to dispatch identically (possibly with a less verbose self-report).

## Edits Applied

1. [.claude/skills/orchestrate/evals/evals.json](../../../.claude/skills/orchestrate/evals/evals.json) — rephrased assertion 3 across all 3 evals from *"Dispatches or mentions dispatching..."* to *"Mentions dispatching a Haiku recon agent in Phase 1 (actual dispatch not testable in subagent eval harness — see ORCH-001; authoritative test is evals/harness.md Run A step A2)"*. Previous wording was structurally unsatisfiable in the subagent harness.
2. [.claude/skills/orchestrate/SKILL.md](../../../.claude/skills/orchestrate/SKILL.md) — appended *"Note on eval-harness behavior (ORCH-001)"* section documenting the subagent-toolset limitation and pointing to `evals/harness.md` Run A step A2 as the authoritative dispatch test.
3. [2026-04-22_System_Bug_Orchestrate_Haiku_Recon_Dispatch.md](2026-04-22_System_Bug_Orchestrate_Haiku_Recon_Dispatch.md) — frontmatter flipped `status: open` → `status: closed-not-a-bug`; appended Resolution section.

## Open Items

- [ ] Optional: run `/orchestrate` in a fresh top-level session to confirm Phase 1 dispatch works in real use (expected yes, not yet empirically verified in this investigation).
- [ ] Optional: re-run iteration-3 eval benchmark to confirm assertion 3 now passes (transcripts already *mention* dispatch; only the actual call was absent).

## Authoritative Test Going Forward

[.claude/skills/orchestrate/evals/harness.md](../../../.claude/skills/orchestrate/evals/harness.md) Run A step A2 — executed manually in a top-level Claude Code session where `Agent` is available. JSON evals cover everything else about the skill; the Haiku dispatch specifically must be tested in the top-level harness.
