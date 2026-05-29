---
date: 2026-05-22
type: review-packet
description: "Packet for Claude/Opus to review the corrected Design-doc web app plan before finalization."
tags: [review-packet, claude, opus, web-app, design-doc, plan]
---

# Claude Review Packet: Design-doc Web App Plan

## Files to Review

- Corrected plan: `C:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault-V2\00-Management-V2\Plans\Design_Doc_Web_App_Plan.md`
- Brainstorm handoff: `C:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault-V2\00-Management-V2\Memory\Codex_Webapp_Brainstorm_Handoff.md`
- Brainstorm session log: `C:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault-V2\00-Management-V2\Sessions\2026-05-22_Codex_Webapp_Brainstorm.md`
- Prior plan review: `C:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault-V2\00-Management-V2\Sessions\2026-05-22_Codex_Plan_Reviewer_Webapp.md`

## Git State Note

`Design_Doc_Web_App_Plan.md` is currently untracked in git, so a normal `git diff` does not show the internal edits. Review the file contents directly and use the line references below as the change map.

Current relevant status:

```text
?? Content-Hub-Vault-V2/00-Management-V2/Memory/Codex_Webapp_Brainstorm_Handoff.md
?? Content-Hub-Vault-V2/00-Management-V2/Plans/Design_Doc_Web_App_Plan.md
?? Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-22_Codex_Webapp_Brainstorm.md
```

## What Changed in the Plan

The plan was corrected before finalization to address findings 1-4 from the prior review and brainstorm.

### Finding 1: Output Cardinality

Relevant plan lines:

- Line 52: Locked result contract now uses `{result_type, primary_path, outputs[]}` with `file`, `file_set`, and `bundle`.
- Line 93: Adds `OutputBrowser.jsx` for file, file_set, and bundle display.
- Lines 135-138: Job result model defines typed result metadata.
- Lines 160-173: Adds stage output resolver table.
- Lines 223, 231, 233: Frontend now renders typed results through `OutputBrowser`, not a single markdown path.
- Lines 332-334: Verification now checks typed result and bundle rendering.

### Finding 2: Outline Contract

Relevant plan lines:

- Line 53: Locked decision says research feeds Ideation and Hooks, while Outline derives downstream from topic/hook context.
- Line 122: `/api/pipeline/outline` body no longer accepts `research_file`.
- Line 167: Outline resolver says inputs are topic/hook context, not raw `research_file`.
- Line 263: Pipeline-to-UI mapping says Outline has no direct `research_file`.
- Line 274: Explicitly states research still shapes Outline indirectly through Ideation and Hook generation.

### Finding 3: Runtime and Deployment

Relevant plan lines:

- Line 54: Locked decision says the FastAPI wrapper uses the repo's existing Python environment for v1.
- Line 109: Backend section says subprocessed skills inherit the same dependency surface as the working local pipeline.
- Line 139: Subprocess launch uses `sys.executable`.
- Lines 282-283: Phase 1 removes the separate `server/.venv` step and adds `server/runtime.md`.

### Finding 4: Output Discovery / Vault Normalization

Relevant plan lines:

- Line 55: Vault remains execution-layer source of truth; Supabase, if added, sits above it as app state/output metadata.
- Line 118: Adds `/api/vault/outputs?path=...`.
- Lines 140-142: No generic `"Written to: <path>"` or newest-file fallback as the primary contract; use per-stage resolvers.
- Lines 160-173: Normalizes outputs at the API boundary instead of changing vault conventions.
- Lines 356-357: Supabase is non-mandatory for v1 and must not replace the vault execution layer.

## Known Open Threads

These are intentionally not fully resolved yet:

- Finding 5: `/api/health` capability checks. See line 115 and line 319. The plan currently says not to overstate readiness beyond backend reachability until the product decision is made.
- Finding 6: Brain URL/file-drop controls. See line 240 and line 268. The plan says not to ship visible controls that do not work.

## Review Prompt for Claude/Opus

Please review `Design_Doc_Web_App_Plan.md` before finalization.

Focus on whether the corrected plan now addresses findings 1-4 without introducing new implementation risks:

1. Output cardinality and typed results.
2. Outline contract and indirect research flow.
3. Shared repo Python runtime for v1.
4. API-boundary output normalization instead of changing vault conventions.

Also flag any remaining high/medium-risk blockers, especially around findings 5-6 if they would prevent implementation from starting.

Return:

- Findings first, severity ordered, with exact plan section/line references where possible.
- Then open questions.
- Then a short verdict: finalizable as-is, finalizable after small edits, or not finalizable.

Do not edit files during this review.
