---
date: 2026-04-22
type: session-log
---

# Orchestrate Skill Eval Test — 2026-04-22

Implements: [[orchestrate skill]]
References: [[orchestrated-execution]]
Modifies: [[orchestrate-workspace]]

## What Happened

Ran a full skill-creator eval loop on the [[orchestrate skill]] (`.claude/skills/orchestrate/SKILL.md`). 3 eval prompts, each with a with_skill (Opus advisor) and without_skill (Haiku baseline) run.

## Benchmark Results

| Config | Pass Rate | Time | Tokens |
|--------|-----------|------|--------|
| with_skill (Opus) | **85.7%** | 170s | ~17,940 |
| without_skill (Haiku) | **14.3%** | 148s | ~11,667 |
| Delta | **+71pp** | +22s | +6,274 |

## What Went Well

- **Announcement** (3/3): All Opus with_skill agents announced using orchestrated-execution as first action.
- **Vault file read** (3/3): All agents read `orchestrated-execution.md` with explicit learning extraction.
- **State file** (3/3): All agents wrote to `Content-Hub-Vault/00-Management/Orchestrations/` as required.
- **Specialist naming** (3/3): All agents correctly identified db-agent, pipeline-agent, frontend-agent by AGENTS.md names.
- **Dependency ordering** (3/3): All agents correctly sequenced db migration before backend before frontend.
- **User approval gate** (3/3): All agents paused at Phase 3 and quoted the approval rule verbatim.
- **Baseline contrast**: Haiku baseline (1/7) confirms the skill is doing real work — not just natural behavior.

## What Went Wrong

### Critical: Haiku Recon Agent Never Dispatched (0/3)

All 3 Opus with_skill agents skipped Phase 1's prescribed `Agent(subagent_type="Explore", model="haiku", ...)` dispatch. Instead they did recon inline with Glob/Read/Grep tools. Evidence: `metrics.json Agent: 0` in all 3 runs.

The agents read and extracted the Haiku dispatch instruction from the vault file, but did not act on it. Root cause: the instruction is framed as contextual guidance, not a hard constraint.

### Minor: Eval 2 metrics self-report bug

`total_steps: 1` in eval-2 with_skill `metrics.json` despite many more steps taken. Self-reporting accuracy is unreliable.

### Non-discriminating assertion (eval feedback)

Assertion 5 (db-first ordering) passes for without_skill too because db-first is natural common sense. Should be replaced with "Plan uses labeled parallel group notation with explicit dependency declarations."

## Fix Suggestions

### Fix 1 — Force Haiku recon dispatch (high priority)

In `orchestrated-execution.md` Phase 1, change the framing from "you should dispatch" to a hard blocking requirement:

```
BEFORE doing any inline file reads, you MUST dispatch a Haiku recon agent:
Agent(subagent_type="Explore", model="haiku", prompt="...", run_in_background=False)
Proceeding with inline recon instead of dispatching is a protocol violation.
```

Add a callout block explaining WHY: inline recon consumes Opus context with raw file content; the Haiku agent returns structured summaries that are cheaper and faster. This is a resource optimization, not bureaucracy.

### Fix 2 — Replace non-discriminating assertion

Swap eval assertion 5 from "db ordered before frontend" to "plan uses labeled parallel group notation with explicit dependency markers (Group 1, Group 2, depends_on)."

### Fix 3 — Add metrics accuracy assertion

Add an assertion checking that `metrics.json total_steps` is plausible (> 3) to catch the self-reporting hallucination seen in eval-2.

## Files Touched

- `orchestrate-workspace/iteration-1/` — all eval outputs, grading.json files, benchmark.json, benchmark.md, eval-review.html
- `.claude/skills/orchestrate/evals/evals.json` — created with 3 prompts and 7 assertions each

## Open Items

- [ ] Apply Fix 1 to `orchestrated-execution.md` and re-run iteration-2
- [ ] Replace assertion 5 in `evals/evals.json`
- [ ] Add metrics accuracy assertion
