---
date: 2026-05-22
type: handoff
description: "Current-state handoff for the Design-doc web app brainstorm. Captures the agreed direction for findings 1-4 before the plan is rewritten."
tags: [handoff, web-app, brainstorm, codex, design-doc]
---

# Handoff: codex_webapp_brainstorm

**Status:** Brainstorm complete; plan corrections not yet applied  
**Next reader:** Agent or operator updating the plan/spec before implementation  
**Primary references:** [[2026-05-22_Codex_Webapp_Brainstorm]], [[2026-05-22_Codex_Plan_Reviewer_Webapp]], [[Design_Doc_Web_App_Plan]]

## Last action

Reviewed findings 1-4 with the user and narrowed each one into a lower-friction implementation direction that preserves the current vault-based skill system.

## Next action

Update `Design_Doc_Web_App_Plan` so findings 1-4 reflect the agreed direction:

- typed result model for single-file, multi-file, and bundle outputs
- research feeding Outline indirectly through Ideation/Hooks, not `research_file -> Outline`
- shared repo Python runtime for v1
- API-boundary normalization instead of changing vault output conventions

## Why

The original plan is still directionally useful, but its current contracts are too optimistic. If implementation starts before the plan is corrected, the wrapper app will drift from the real skills and create avoidable late failures.

## Agreed Direction

### Finding 1: output cardinality

- The problem is not only bundle directories. It is any stage that returns more than one meaningful artifact.
- A dedicated UI area for outputs helps, but does not fix the issue alone.
- Required shape: structured result metadata such as `result_type`, `primary_path`, and `outputs[]`.
- Safe result taxonomy for the web layer: `file`, `file_set`, `bundle`.
- If Supabase is added, the UI should read outputs from Supabase metadata rather than browsing the vault directly.

### Finding 2: Outline contract

- The intended pipeline is `research -> ideation -> hooks / outline / titles`.
- The issue is not that research should never influence Outline.
- The issue is that the current plan incorrectly models a direct `research_file` input into the current Outline CLI.
- The finding should be rewritten to say Outline derives downstream from topic/hook context unless the skill itself is changed.

### Finding 3: runtime and deployment

- Lowest-friction v1: run the new web backend in the same Python environment the existing repo already uses.
- Treat the FastAPI layer as a thin orchestrator around existing skills.
- Avoid a separate `Design-doc/server/.venv` for v1.
- For a demo user, this shared runtime is acceptable if access is controlled.
- It is not a true multi-user architecture yet; add at least a simple gate and a dedicated demo workspace/output namespace if exposing it externally.

### Finding 4: output discovery

- Standardizing file format alone is not enough.
- Do not change existing vault output conventions just to make the web app easier; that risks breaking the current local system.
- Normalize at the API boundary instead.
- v1 fix: per-stage adapters or a stage runner that resolves outputs based on each skill's real behavior.
- Future optional fix: add a `--json` or equivalent machine-readable mode to skills without changing their vault artifact layout.

### Supabase direction

- Good version: use Supabase for web app state, jobs, output metadata, and possibly storage links.
- Risky version: replacing the vault as the execution-layer source of truth for v1.
- Recommended v1 stance: keep the vault for pipeline execution; remove the vault from the UI surface by exposing jobs/outputs through the backend or Supabase metadata.

## Open Threads

- Findings 5 and 6 still need explicit product decisions:
  - what `/api/health` should verify beyond basic liveness
  - whether Brain v1 keeps or cuts URL/file-drop controls
- No plan edits were made yet.
- No code changes were made yet.

## Do Not

- Do not split Python environments for v1 unless you are willing to provision the full skill dependency surface.
- Do not rewrite vault storage conventions to force uniform outputs.
- Do not model Outline as direct `research_file` intake unless `skills/outline.py` is changed.
- Do not remove the vault from the pipeline execution path in v1; only remove it from the UI surface if desired.
