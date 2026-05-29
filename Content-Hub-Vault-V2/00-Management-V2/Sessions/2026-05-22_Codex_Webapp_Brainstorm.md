---
date: 2026-05-22
type: session-log
description: "Brainstorm follow-up to the Design-doc web app plan review. Captures the implementation direction chosen for findings 1-4 and the preferred low-friction architecture."
tags: [session-log, brainstorm, web-app, design-doc, codex]
---

# Session Log: codex_webapp_brainstorm

**Date:** 2026-05-22  
**Session Type:** Architecture Brainstorm / Review Follow-up  
**Reader:** Future implementer refining the web app plan before coding  
**Post-read action:** Update the plan so the wrapper app reflects the actual skill system and the clarified v1 constraints

---

## Scope

This session did not replace the earlier plan review. It refined the remediation direction for findings 1-4 from [[2026-05-22_Codex_Plan_Reviewer_Webapp]].

The discussion centered on:

- whether multi-file outputs still break the current plan if they are not bundle directories
- whether the Outline finding meant research was being modeled incorrectly in the pipeline
- what runtime strategy is safest for v1 and easiest to operate for a demo
- whether issue 4 can be solved by forcing one file format
- whether the web app should remove the vault from its UI surface and use Supabase instead

---

## Clarified Direction by Finding

### 1. Result handling is a cardinality problem, not only a bundle problem

The user asked whether the system still breaks if a stage returns multiple files but no bundle directory. The answer is yes if the result contract is still one `vault_path` string.

Clarified direction:

- The real issue is output cardinality.
- A single-file-only result model is too narrow for:
  - one primary file plus related sidecar files
  - multiple first-class files
  - directory-style bundle outputs
- Adding a UI area that can display outputs is useful, but it only fixes the presentation layer.
- The actual contract fix is a structured result model such as:
  - `result_type`
  - `primary_path`
  - `outputs[]`

Recommended taxonomy for v1:

- `file`
- `file_set`
- `bundle`

### 2. The Outline issue is about contract shape, not pipeline intent

The user clarified that research is meant to feed Ideation, and from there hooks, outlines, and titles are created. That is compatible with the intended workflow.

Clarified direction:

- The finding should not imply that research must never influence Outline.
- The finding should say the current plan incorrectly models Outline as directly accepting `research_file`.
- Under the current CLI, Outline is better described as deriving from topic/hook context downstream of Ideation rather than consuming raw research directly.
- If direct research ingestion for Outline is desired, that is a separate skill change and should be stated as such.

Suggested revised wording for the finding:

> The plan incorrectly models Outline as directly consuming `research_file`; in the current pipeline, research feeds Ideation, and Outline is derived downstream from topic/hook context rather than raw research input.

### 3. Lowest-friction runtime: reuse the repo's existing Python environment

The user asked for the safest and most stable option that is easy to fix and manage if something breaks.

Preferred direction:

- Do not create a separate `Design-doc/server/.venv` for v1.
- Run the web backend in the same Python environment the existing repo already uses.
- Treat the new backend as a thin wrapper/orchestrator around the current skills and shared modules.
- Install and operate from the real repo dependency surface, not a reduced environment that only boots FastAPI.

Why this direction won:

- lowest migration risk
- less config drift
- faster recovery when a skill breaks
- no second runtime to debug

Demo-user implication:

- This setup is acceptable for a controlled demo user.
- It is not a proper multi-user system yet.
- If demo access is exposed externally, add at least:
  - a simple access gate
  - a dedicated demo workspace or output namespace
  - clear understanding that the runtime is still shared

### 4. Output discovery should be normalized at the API boundary, not by rewriting the vault

The user asked whether forcing one file format would solve the issue. The answer was no unless the entire output contract also became uniform.

Clarified direction:

- File format uniformity helps only slightly.
- The deeper issue is inconsistent result reporting and mixed output shapes across skills.
- Forcing the vault itself into a new standardized shape is risky because it can break the current local system.
- The v1-safe approach is to leave vault artifacts alone and adapt them in the web backend.

Preferred v1 fix:

- build per-stage adapters or a `stage_runner` layer
- resolve outputs according to each skill's actual behavior
- return normalized result metadata to the UI

Future optional improvement:

- add machine-readable completion output such as `--json`
- do this without changing the underlying vault artifact layout

---

## Supabase Direction

The user asked whether using Supabase and removing the vault from the web app stage would solve the issue.

Answer reached in the session:

- Good version:
  - keep the vault as the execution-layer artifact system for v1
  - use Supabase for web app state, jobs, outputs metadata, and later optional storage links
  - remove direct vault browsing from the UI surface if desired
- Risky version:
  - replace the vault itself as the execution-layer source of truth in v1

Recommended direction:

- keep the vault in the pipeline
- remove it only from the web-facing UX layer
- let the backend or Supabase expose structured outputs to the frontend

This preserves compatibility with the current local-first skill engine while still allowing the web app to behave like a modern app.

---

## Resulting Architecture Preference for V1

The discussion converged on this low-friction architecture:

1. FastAPI backend runs inside the repo's existing Python environment.
2. Existing skills remain the execution layer and continue writing to the vault as they do now.
3. The web backend normalizes per-stage outputs into a typed result contract.
4. The frontend renders those normalized outputs rather than assuming one markdown file.
5. Supabase, if used, sits above the vault as the app-state registry rather than replacing the vault immediately.

---

## Open Decisions Still Pending

This session did not settle findings 5 and 6 from the earlier review.

Still open:

- what `/api/health` should verify beyond liveness
- whether Brain v1 should keep or remove URL/file-drop affordances
- whether the normalized result metadata should live only in backend job state or also in Supabase tables from day one

---

## Recommended Plan Edits

Before implementation starts, update `Design_Doc_Web_App_Plan` to reflect the following:

1. Replace single `vault_path` assumptions with typed outputs for `file`, `file_set`, and `bundle`.
2. Rewrite the Outline section so research influences it indirectly through Ideation/Hooks unless the skill is explicitly changed.
3. Replace the dedicated minimal server venv recommendation with shared-runtime guidance for v1.
4. Replace generic stdout/newest-file discovery with per-stage output resolution.
5. If Supabase is introduced, describe it as app-state/output metadata infrastructure rather than an immediate vault replacement.

---

## Review Outcome

The earlier findings still stand, but this session narrowed the practical fix path:

- keep the current vault-based system intact
- adapt at the web/API boundary
- minimize new runtime surfaces
- defer larger storage/runtime migrations until after the wrapper app is proven

This is the least-friction path that still leaves room for later hardening.

---

## References

- Prior review session: `2026-05-22_Codex_Plan_Reviewer_Webapp`
- Reviewed plan: `Design_Doc_Web_App_Plan`
- Related implementation surface:
  - `skills.researcher`
  - `skills.ideation`
  - `skills.hook`
  - `skills.outline`
  - `skills.title`
  - `skills.cascade`
  - `skills.short_form`
  - `skills.voice_cleanup`
  - `skills.utils.ai`
  - Brain and stage prototype components in `Design-doc/Content Hub/`

## Modifies

- Adds this session log
- Adds `Memory/Codex_Webapp_Brainstorm_Handoff.md`
