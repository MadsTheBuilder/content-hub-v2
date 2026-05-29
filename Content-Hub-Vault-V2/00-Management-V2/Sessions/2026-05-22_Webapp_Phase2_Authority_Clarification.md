---
status: Completed
date: "2026-05-22"
type: session_summary
tags: [session, web-app, phase-2, drift, claude, decision]
description: "Clarified the Phase 2 execution drift between Webapp_sprint and Current_Sprint; confirmed the webapp plan is authoritative and documented the impact of using Claude CLI instead of the planned SDK for Brain."
implements: "[[Design_Doc_Web_App_Plan]]"
references:
  - "[[Webapp_sprint]]"
  - "[[Current_Sprint]]"
  - "[[2026-05-22_Webapp_Phase2_Backend]]"
---

# Session: Webapp Phase 2 - Authority Clarification

Implements: [[Design_Doc_Web_App_Plan]]
References: [[Webapp_sprint]], [[Current_Sprint]], [[2026-05-22_Webapp_Phase2_Backend]]

## Context

The user noticed that the most recent Phase 2 backend execution followed [[Current_Sprint]] instead of [[Webapp_sprint]] while implementing [[Design_Doc_Web_App_Plan]].

That created confusion because the webapp documents do not say exactly the same thing for the Brain backend:

- [[Webapp_sprint]] points back to [[Design_Doc_Web_App_Plan]] as the source of truth for phases, contracts, and locked decisions.
- [[Design_Doc_Web_App_Plan]] says `server/brain.py` should use a direct Anthropic SDK call.
- [[Current_Sprint]] records the shipped implementation as "Claude CLI analysis (no separate API key)."

The user asked which instruction is actually correct and whether using Claude CLI breaks anything.

## What Was Reviewed

The clarification pass reviewed four things:

1. [[Webapp_sprint]] header and Phase 2 section.
2. [[Design_Doc_Web_App_Plan]] Brain workspace and Phase 2 backend requirements.
3. [[Current_Sprint]] Active block for the webapp sprint.
4. The shipped `Design-doc/server/brain.py` implementation plus `skills/utils/ai.py`.

## Findings

### 1. Source-of-truth order is clear

For this workstream, the authority order is:

1. [[Design_Doc_Web_App_Plan]]
2. [[Webapp_sprint]]
3. [[Current_Sprint]]

Reason:

- [[Webapp_sprint]] explicitly says the source of truth is [[Design_Doc_Web_App_Plan]] and that phases, contracts, and locked decisions come from that document.
- [[Current_Sprint]] functions as the active status board. It records what happened, but it is not the implementation-spec authority when it diverges from the plan.

### 2. Claude CLI is correct for the 8 pipeline wrappers

There is no conflict for the 8 existing pipeline skills.

Phase 2 in [[Webapp_sprint]] calls for exact CLI passthrough wrappers for:

- `researcher`
- `ideation`
- `hook`
- `outline`
- `title`
- `cascade`
- `short-form`
- `voice-cleanup`

Using CLI for those wrappers is aligned with the approved webapp architecture.

### 3. The drift is only in Brain

The mismatch is limited to `server/brain.py`.

- [[Design_Doc_Web_App_Plan]] says Brain should use a direct Anthropic SDK call because Brain is the one new AI invocation outside the existing 8 pipeline skills.
- The shipped implementation in `Design-doc/server/brain.py` instead calls `generate(..., provider="claude")`.
- That helper routes through the Claude CLI subprocess path in `skills/utils/ai.py`.

So the actual Phase 2 backend did ship a working Brain path, but it shipped a different implementation choice than the approved plan specified.

### 4. Claude CLI does not automatically break local-first behavior

Using Claude CLI for Brain is not inherently broken.

It has real advantages:

- no separate Anthropic API key required
- reuses the same local Claude auth/session already used elsewhere
- keeps the local-first setup simpler for one-machine usage

But it also introduces tradeoffs the plan was likely trying to avoid:

- runtime depends on local CLI install and login state
- harder to run in headless CI or a deployed server environment
- subprocess failures and output parsing become part of the Brain path
- code now drifts from the approved design and from [[Webapp_sprint]]

### 5. "Phase 2 complete" needs one nuance

[[2026-05-22_Webapp_Phase2_Backend]] records Phase 2 as complete and documents the CLI-based Brain implementation.

That is accurate for "what shipped," but not fully accurate for "did implementation exactly match the approved plan."

The better reading is:

- Phase 2 backend is functionally complete.
- Brain has one documented implementation deviation: CLI instead of the planned SDK call.

## Decision Clarified

The right interpretation is:

- Follow [[Design_Doc_Web_App_Plan]] and [[Webapp_sprint]] for implementation authority.
- Read [[Current_Sprint]] as the live status/history board.
- Treat the current Brain implementation as a deviation, not as the new source of truth by itself.

Using Claude CLI for Brain does not break the local app by default, but it does break alignment with the approved plan.

## Recommended Next Step

Pick one of these two paths and reconcile docs/code explicitly:

1. **Bless the CLI path**
   - Keep `Design-doc/server/brain.py` as-is.
   - Update [[Design_Doc_Web_App_Plan]] and [[Webapp_sprint]] so Brain officially uses Claude CLI.
   - Best if the app is intended to stay local-first and operator-run.

2. **Return Brain to the planned SDK path**
   - Patch `Design-doc/server/brain.py` to use Anthropic SDK directly.
   - Keep the plan and sprint docs unchanged except for a small correction note.
   - Best if deployability and plan fidelity matter more than local CLI convenience.

Until that reconciliation happens, the safest status line is:

> Phase 2 backend is complete with one implementation drift: Brain uses Claude CLI instead of the plan's Anthropic SDK call.

## Files Reviewed

- `Content-Hub-Vault-V2/00-Management-V2/Plans/Design_Doc_Web_App_Plan.md`
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/Webapp_sprint.md`
- `Content-Hub-Vault-V2/00-Management-V2/Tasks/Current_Sprint.md`
- `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-22_Webapp_Phase2_Backend.md`
- `Design-doc/server/brain.py`
- `skills/utils/ai.py`

## Outstanding

- Decide whether Brain should stay CLI-based or be brought back to the planned SDK implementation.
- After that decision, reconcile the plan, sprint board, and backend note so they all say the same thing.
