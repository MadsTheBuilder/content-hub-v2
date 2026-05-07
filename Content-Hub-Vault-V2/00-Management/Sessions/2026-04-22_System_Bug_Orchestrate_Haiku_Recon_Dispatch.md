---
date: 2026-04-22
type: system-bug-report
status: closed-not-a-bug
component: Claude Agent SDK — subagent dispatch from within skill-loaded sessions
skill: orchestrate (.claude/skills/orchestrate/SKILL.md)
vault-ref: orchestrated-execution.md Phase 1
---

# System Bug: Haiku Recon Agent Not Dispatched in Orchestrate Skill Phase 1

## Bug ID
`ORCH-001`

## Summary

When the `orchestrate` skill is triggered, Phase 1 requires dispatching a Haiku Explore subagent for codebase recon. The model consistently skips this dispatch and performs inline recon using `Glob`, `Read`, and `Grep` tools instead — across 3 eval runs and 3 fix iterations, with a 0/3 pass rate on this specific behavior.

---

## Bug Behavior (Observed)

**What happens:**

1. The orchestrate skill is triggered (via `/orchestrate` or auto-trigger).
2. The model reads `orchestrated-execution.md`, including Phase 1's `Agent(subagent_type="Explore", model="haiku", ...)` dispatch instruction.
3. **Phase 1 is skipped.** Instead of dispatching the Haiku agent, the model calls `Read`, `Glob`, and `Grep` directly on codebase files.
4. The model proceeds to Phase 2 (planning) using the inline recon data.
5. The model self-reports the violation accurately — it knows it broke the protocol.

**Evidence from run summary (2026-04-22, eval-1):**

> "Did you dispatch Agent(subagent_type="Explore", model="haiku") for Phase 1 recon? **NO**"
>
> "Root cause: Unable to invoke the Agent() function directly within this session context."
>
> "First file read: backend/content/models.py was read BEFORE recon agent dispatch — PROTOCOL VIOLATION."

**Metric:** `Agent tool calls = 0` in all 3 eval runs across iterations 1 and 2.

---

## Fix Attempts Made

### Fix Attempt 1 — Soft framing in skill SKILL.md

**What changed:** Phase 1 in `orchestrated-execution.md` originally said:

> "Dispatch a Haiku recon agent to scan the codebase."

**Result:** 0/3. Model treated it as a recommendation and skipped it without comment.

---

### Fix Attempt 2 — Hard blocking language + protocol violation framing

**What changed:** Phase 1 in `orchestrated-execution.md` was rewritten to:

> "**MANDATORY BLOCKING STEP — You MUST dispatch a Haiku recon agent BEFORE reading any files inline or doing any planning.**"
>
> "**Performing inline recon (Glob, Read, Grep) before dispatching this agent is a protocol violation.**"
>
> Also added the `why` explanation: *"Opus context is expensive and limited. Haiku returns structured file summaries at a fraction of the token cost."*

**Result:** 0/3. Model now reads the instruction, extracts it verbatim, acknowledges it is a protocol violation — but still performs inline recon, citing inability to call `Agent()`.

---

### Fix Attempt 3 — Eval prompt permission note

**What changed:** All 3 eval prompts in `evals.json` were updated to include:

> "Note: You may (and should) dispatch a Haiku Explore agent for Phase 1 recon — this is required by orchestrated-execution.md. Only executor agents that write files are restricted until the user approves the plan."

**Hypothesis:** The model may have been confusing the "no execution before approval" rule with a blanket prohibition on all Agent calls.

**Result:** 0/3. Model explicitly addresses the permission note in its summary, confirms it understands the distinction — but still cites "session context limitations" as the reason it cannot call `Agent()`.

---

## Behavior Change After Fix Attempts

| Iteration | Dispatches Haiku? | Model's own explanation |
|-----------|-------------------|-------------------------|
| Before any fix | No | Instruction ignored silently |
| After Fix 1 (hard language) | No | Instruction read and extracted, violation not self-reported |
| After Fix 2 (protocol violation framing) | No | Violation explicitly self-reported — "unable to invoke Agent() in this session context" |
| After Fix 3 (permission note in prompt) | No | Permission understood, violation still self-reported, same stated inability |

**Pattern:** The failure mode shifted from *ignoring* the instruction to *understanding it but believing `Agent()` is unavailable*. The model does not appear to be suppressed by a permissions layer — it is reasoning its way to a belief that dispatching subagents is not possible in its current context, then self-correcting with inline tools.

---

## Desired Behavior

When the `orchestrate` skill is active and Phase 1 begins, the model should:

1. Call `Agent(subagent_type="Explore", model="haiku", description="Recon for orchestration", prompt="...")` as its **first tool call** — before any `Glob`, `Read`, or `Grep`.
2. Wait for the Haiku agent to return its findings.
3. Use those findings to proceed to Phase 2 (planning).

The `Agent()` tool is available in the environment. The model should be aware it can call it, and should do so when the skill instructs it to.

---

## Hypothesis for Root Cause

The model appears to have a runtime belief that `Agent()` dispatch is unavailable or restricted in the current session context — possibly because:

- The session is itself already a subagent (spawned by a parent), and the model infers a recursion constraint.
- The model is conflating "executor agents are gated on user approval" with "no agent dispatch is allowed at all."
- The `Agent` tool schema is not reliably visible to the model inside skill-loaded sessions, so it falls back to tools it can confirm are present.

---

## Reproduction Steps

1. Open a Claude Code session in the Content Hub working directory (`c:\Users\madhu\Claude cowork\Content Hub`).
2. Type `/orchestrate` followed by any multi-domain task (e.g., "Add a views_count column to content_items, increment on access, show on library page").
3. Observe Phase 1: does the model call `Agent(subagent_type="Explore", model="haiku", ...)`?
4. Check: if the first tool call after reading `orchestrated-execution.md` is `Read`, `Glob`, or `Grep` — the bug is reproduced.

**Pass rate on reproduction:** 3/3 (consistent, not flaky).

---

## Environment

- Platform: Claude Code, VSCode extension, Windows 11
- Model: claude-sonnet-4-6 (orchestrate evals run via skill-creator subagents)
- Skill: `.claude/skills/orchestrate/SKILL.md`
- Skill source of truth: `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md`
- Eval framework: `.claude/skills/orchestrate/evals/evals.json` (3 prompts, assertion 3 = Haiku dispatch check)

---

## Related Session Logs

- [[2026-04-22_Orchestrate_Eval_Test]] — iteration-1 benchmark, initial 0/3 finding
- [[2026-04-22_Orchestrate_Benchmark_Pipeline_Complete]] — iteration-2 benchmark, Fix 2 applied, still 0/3
- This session (2026-04-22) — Fix 3 applied and tested, still 0/3
- [[2026-04-22_ORCH-001_Root_Cause_Analysis]] — root cause identified, resolution applied

---

## Resolution (2026-04-22)

**Status:** `closed-not-a-bug`.

### Actual root cause

The 0/3 result is not a skill defect. It is an **eval-harness architecture constraint**: the skill-creator eval workflow spawns a subagent to run each test case, and spawned subagents in Claude Code do not have the `Agent` tool in their toolset. The model's self-report — *"unable to invoke Agent() in this session context"* — is factually correct.

### Evidence

1. [skill-creator/SKILL.md](file:///c:/Users/madhu/.claude/plugins/marketplaces/claude-plugins-official/plugins/skill-creator/skills/skill-creator/SKILL.md), section "Running and evaluating test cases", Step 1: *"For each test case, spawn two subagents in the same turn — one with the skill, one without."* The with_skill run is always a subagent, never a top-level session.
2. Claude Code's Agent tool schema excludes `Agent` from `Explore` and `Plan` subagent types (*"All tools except Agent, ..."*); nested Agent dispatch is architecturally blocked.
3. The eval transcript at [orchestrate-workspace/iteration-2/eval-1-views-count/with_skill/outputs/transcript_summary.md:20](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/orchestrate-workspace/iteration-2/eval-1-views-count/with_skill/outputs/transcript_summary.md#L20) explicitly says *"in this constrained evaluation environment"* — the subagent correctly identifies its own capability gap.
4. Prompt-layer fixes (soft → MUST → permission note) had no effect because prompt pressure cannot add back a tool that is not in the tool list. They only made the self-report more verbose.

### /model selection is NOT the cause

The `/model` slash command sets the main interactive session's model. It does not alter the toolset of a subagent spawned via Agent(). Opus in the same subagent context would fail to dispatch the same way — possibly less verbosely, but the missing tool is the structural blocker, not the model.

### Action taken

1. [.claude/skills/orchestrate/evals/evals.json](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/.claude/skills/orchestrate/evals/evals.json) — rephrased assertion 3 in all three evals from *"Dispatches or mentions dispatching..."* to *"Mentions dispatching a Haiku recon agent in Phase 1 (actual dispatch not testable in subagent eval harness — see ORCH-001; authoritative test is evals/harness.md Run A step A2)"*. The new wording is satisfiable inside the subagent harness; the previous wording was structurally unsatisfiable.
2. [.claude/skills/orchestrate/SKILL.md](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/.claude/skills/orchestrate/SKILL.md) — appended a "Note on eval-harness behavior (ORCH-001)" section that documents the limitation and pins [evals/harness.md](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/.claude/skills/orchestrate/evals/harness.md) Run A step A2 as the authoritative test for actual Haiku dispatch.
3. [Content-Hub-Vault/00-Management/Sessions/2026-04-22_ORCH-001_Root_Cause_Analysis.md](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/Content-Hub-Vault/00-Management/Sessions/2026-04-22_ORCH-001_Root_Cause_Analysis.md) — session log for this investigation.

### Authoritative test going forward

[.claude/skills/orchestrate/evals/harness.md](file:///c:/Users/madhu/Claude%20cowork/Content%20Hub/.claude/skills/orchestrate/evals/harness.md) Run A step A2 — run manually in a top-level Claude Code session, where `Agent` is available. The JSON evals under skill-creator test *everything else* about the skill; Haiku dispatch specifically must be tested in the top-level harness.
