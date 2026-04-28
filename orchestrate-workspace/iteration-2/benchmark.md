# Skill Benchmark: orchestrate

**Executor model**: opus  
**Analyzer model**: sonnet  
**Date**: 2026-04-22T12:19:47Z  
**Evals**: 1, 2, 3 (1 run each per configuration)

## Summary

| Metric | with_skill (Opus) | baseline (Haiku) | Delta |
|--------|-------------------|------------------|-------|
| Pass Rate | 87.5% ± 0.0% | 25.0% ± 0.0% | +0.62 |
| Time | 143.6s ± 14.2s | 118.8s ± 15.1s | +24.7s |
| Tokens | 59,784 ± 7,656 | 53,077 ± 3,689 | +6707 |

## Per-Eval Results

### Eval 1 (views-count) — with_skill
Pass rate: **87.5%** (7/8) | Time: 127.9s | Tokens: 52,864

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✓ SKILL.md Step 1 instructs the announcement; the agent stated 'I'm using orchestr… |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✓ Transcript confirms: 'Read orchestrated-execution vault file (Content-Hub-Vault/… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent to sc | ✗ Transcript explicitly documents the violation: 'Performed inline recon (using Gl… |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✓ Transcript confirms: 'Wrote state file to: Content-Hub-Vault/00-Management/Orche… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✓ Plan shows 'Group 1 (Parallel)' and 'Group 2 (Depends on Group 1)' â€” exact ski… |
| 6 | Identifies db-agent and frontend-agent as specialists involv | ✓ Plan identifies db-agent (Group 1), pipeline-agent (Group 2), and frontend-agent… |
| 7 | Requests user approval before proceeding to execution | ✓ Transcript ends with 'Awaiting Approval' section; state file status=awaiting-app… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Agent completed Phase 1 (4 glob searches, 9 file reads), Phase 2 (plan decomposi… |

### Eval 1 (views-count) — baseline
Pass rate: **25.0%** (2/8) | Time: 112.9s | Tokens: 48,854

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✗ Baseline followed CLAUDE.md session start protocol (context.md, AGENTS.md, GRAPH… |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✗ Transcript lists 12 files read; orchestrated-execution.md is not among them. Ses… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent to sc | ✗ Did inline codebase reads directly (7 files in investigation table). No mention … |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✗ Write operations: only plan.md and transcript_summary.md in the workspace. No st… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✗ Plan uses 'Phase 1 (DB)', 'Phase 2 (Backend)', 'Phase 3 (Frontend)' sections â€”… |
| 6 | Identifies db-agent and frontend-agent as specialists involv | ✓ Transcript mentions 'db-agent', 'pipeline-agent', 'frontend-agent' under 'Coordi… |
| 7 | Requests user approval before proceeding to execution | ✗ Session ends with 'Plan Quality: Ready for execution' and 'Next Steps (if user a… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Agent read 12 files, composed a comprehensive plan across 3 layers, documented 5… |

### Eval 2 (posting-time) — with_skill
Pass rate: **87.5%** (7/8) | Time: 155.6s | Tokens: 58,479

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✓ Transcript confirms: 'Announced orchestration immediately per SKILL.md Â§ Step 1… |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✓ Transcript confirms: 'Read orchestrated-execution.md source-of-truth vault file'… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent in Ph | ✗ Transcript says: 'Attempted to dispatch Haiku recon agent per protocol, but Agen… |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✓ State file written to 'Content-Hub-Vault/00-Management/Orchestrations/2026-04-22… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✓ Plan shows: 'Group 1: Database Schema (Parallel)', 'Group 2: Backend Models (Par… |
| 6 | Identifies at least 3 different specialist agents | ✓ Plan involves db-agent, brand-agent, intelligence-agent, frontend-agent â€” 4 di… |
| 7 | Requests user approval before proceeding to execution | ✓ State file status set to 'awaiting-approval'; transcript ends with 'Awaiting Use… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Summary table shows 7 tasks across 4 groups, 5 codebase areas scanned, state fil… |

### Eval 2 (posting-time) — baseline
Pass rate: **25.0%** (2/8) | Time: 107.6s | Tokens: 55,676

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✗ No announcement of orchestrated-execution. Baseline proceeded directly with rese… |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✗ Baseline was instructed not to read skill files. Read context.md, Plans/CLAUDE.m… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent in Ph | ✗ No mention of recon agent dispatch. Baseline performed inline codebase reads (br… |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✗ No state file written. Only outputs were plan.md and transcript_summary.md in th… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✗ Plan used Phase 1/2/3 implementation sequence sections, not the 'Group N (parall… |
| 6 | Identifies at least 3 different specialist agents | ✓ Baseline read AGENTS.md as part of session start and named db-agent, brand-agent… |
| 7 | Requests user approval before proceeding to execution | ✗ Plan described implementation phases ready for execution. No explicit approval g… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Agent scanned 5 codebase areas, read multiple files, produced a 887-line plan ac… |

### Eval 3 (approval-workflow) — with_skill
Pass rate: **87.5%** (7/8) | Time: 147.2s | Tokens: 68,008

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✓ Transcript compliance notes confirm: 'âœ“ Announced orchestrated-execution usage… |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✓ Compliance notes confirm: 'âœ“ Read orchestrated-execution.md vault file complet… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent to sc | ✗ Transcript shows Phase 1 Recon performed via inline file reads (6 files listed: … |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✓ State file written to 'Content-Hub-Vault/00-Management/Orchestrations/2026-04-22… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✓ Transcript decomposition shows: 'Group 1 (Parallel): Database Migration', 'Group… |
| 6 | Identifies db-agent, pipeline-agent, and frontend-agent as s | ✓ Phase 2 plan assigns: db-agent to Group 1, pipeline-agent to Group 2, frontend-a… |
| 7 | Requests user approval before proceeding to execution | ✓ Transcript: 'User Action Required: Approve plan before proceeding to Phase 4 (Ex… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Summary Statistics: 8 files touched during planning, 3 execution groups, 3 tasks… |

### Eval 3 (approval-workflow) — baseline
Pass rate: **25.0%** (2/8) | Time: 136.0s | Tokens: 54,700

| # | Assertion | Result |
|---|-----------|--------|
| 1 | Announces using orchestrated-execution before doing any othe | ✗ Transcript explicitly states: 'This investigation was completed WITHOUT reading … |
| 2 | Reads Content-Hub-Vault/00-Management/Superpowers/orchestrat | ✗ Explicitly did not read orchestrated-execution.md. Read context.md, CLAUDE.md, G… |
| 3 | Dispatches or mentions dispatching a Haiku recon agent to sc | ✗ Performed inline reads of 6 files (migrations, router, models, types, api.ts, pa… |
| 4 | Writes a state file to Content-Hub-Vault/00-Management/Orche | ✗ No state file written. Outputs are plan.md and transcript_summary.md in eval wor… |
| 5 | Plan output uses labeled group notation such as 'Group N (pa | ✗ Plan uses numbered implementation phases (1-4: DB â†’ Backend â†’ Types â†’ UI) … |
| 6 | Identifies db-agent, pipeline-agent, and frontend-agent as s | ✓ Read AGENTS.md in session start (CLAUDE.md Â§ 6) and identified 'db-agent, pipel… |
| 7 | Requests user approval before proceeding to execution | ✗ Transcript ends at 'Stopping Point: produce a plan'. No explicit approval reques… |
| 8 | Self-reported total_steps or step count in any metrics or su | ✓ Agent read 10 files (4 context + 6 codebase), identified 6 files for changes, do… |

## Notes

- Iteration 2: 8 assertions per eval (up from 7). New assertions: group notation, step-count > 3.
- Assertion 3 (Haiku recon dispatch): 0/3 with_skill passes — eval prompt interference suspected.
- Fix: eval prompt should explicitly allow recon agent dispatch to remove ambiguity.
