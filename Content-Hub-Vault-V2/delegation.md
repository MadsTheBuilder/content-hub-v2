---
name: delegation
description: Trigger for orchestrated multi-agent execution — use when task spans multiple domains or user invokes /orchestrate or /delegate
---

# Delegation

## When to Use

- User starts a prompt with `/delegate` or `/orchestrate`
- Task spans 2+ specialist domains from AGENTS.md (e.g., DB + backend + frontend)
- Task touches 10+ files across different subsystems

## When NOT to Use

- Single-domain task — just do it directly or dispatch one agent
- Simple bug fix, rename, or config change — no orchestration needed
- Exploratory debugging — use `systematic-debugging` instead

## How to Execute

Read and follow `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md`.

That skill covers the full workflow: recon, planning, approval, parallel agent dispatch, stuck-agent handling, and verification.

## Key Rules

1. **One specialist per task.** No task should span multiple agent domains.
2. **No file overlap.** Two parallel agents must never touch the same file.
3. **Approval before execution.** Always show the decomposition plan and wait for user confirmation.
4. **Advisor pattern.** You (Opus) are the advisor. Subagents (Sonnet/Haiku) are the executors. Guide them when stuck.
