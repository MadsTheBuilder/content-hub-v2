---
name: orchestrate
description: Multi-agent orchestration for complex tasks that span multiple domains,
  files, or specialists. Use this skill whenever the user types /orchestrate or
  /delegate, or says "orchestrate this", "dispatch agents", "delegate this",
  "use multi-agent", or "use the orchestrator". Also trigger automatically when
  the task spans 3+ subtasks, touches 2+ specialist domains (e.g. schema + backend
  + frontend, or any combination of roles from AGENTS.md), or involves 10+ files
  across subsystems. If a task touches the database AND the API AND the UI in a
  single request — this skill should fire. Do NOT trigger for single-domain work,
  one-file bug fixes, simple config changes, or exploratory investigation where the
  problem isn't yet defined.
user-invocable: true
---

# Orchestrate

You're about to orchestrate a complex task using the multi-agent workflow defined
in this project's vault. The reason this workflow exists is that large cross-domain
tasks go wrong when a single agent tries to do everything sequentially without a
plan — specialist agents with focused scopes, dispatched in the right order, produce
far better results than one agent context-switching across a dozen files.

## Step 1: Announce

Say this immediately, before reading any file or doing any other work:

> "I'm using orchestrated-execution to decompose and dispatch this task."

## Step 2: Load the full workflow

Read `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md`
from the project working directory. That file is the authoritative definition of
the 6-phase process. Read it completely before proceeding to Phase 1.

## The 6 phases (names only — detail is in the vault file)

1. **Recon** — Explore agent (Haiku) scans relevant codebase areas
2. **Plan** — Decompose into specialist tasks, group for parallelism, write state file to `Content-Hub-Vault/00-Management/Orchestrations/`, present plan to user
3. **Approve** — User reads and approves the plan explicitly; state file flips to `status: approved`
4. **Execute** — Dispatch specialist agents (from AGENTS.md) in parallel groups
5. **Handle results** — Process DONE / STUCK / NEEDS_CONTEXT agent responses
6. **Verify** — Review summaries, check scope, run tests, report to user; state file flips to `status: complete`

## Resuming after context compaction

If the session is interrupted between phases, the state file in `Content-Hub-Vault/00-Management/Orchestrations/` holds everything needed to continue. In a new session, the user invokes `/resume-orchestration` (a separate skill) which reads the state file and picks up at the recorded phase. This is why the state file MUST be written at Phase 2 — without it, the orchestration cannot be recovered.

## The rule that defines the whole point of this skill

Do not create, modify, or delete any file until the user has explicitly approved
the plan produced in Phase 2. Skipping to execution is exactly the failure mode
this skill was created to prevent. If the plan phase is skipped, the orchestration
has failed before it started.

## If the vault file is missing

If `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md` does
not exist at the project root, stop and say:

> "I can't find the orchestrated-execution.md vault file. Please confirm the
> working directory or provide the correct path."

Do not reconstruct the workflow from memory — the vault file is the source of
truth.

## Note on eval-harness behavior (ORCH-001)

When this skill runs inside a skill-creator eval (or any context where the
current session is itself a spawned subagent), the `Agent` tool is not
available in the subagent's toolset. Phase 1's Haiku recon dispatch is
structurally impossible in that context — the model will correctly report
the missing tool and fall back to inline recon.

This is a property of Claude Code's subagent architecture, not a skill
defect. The authoritative test for Phase 1 dispatch behavior is the manual
harness at `evals/harness.md` Run A step A2, which runs in a top-level
session where `Agent` is available.