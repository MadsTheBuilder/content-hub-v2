---
date: 2026-05-22
type: session-log
description: "Review of the Design-doc Web App build plan. Captures execution blockers, contract mismatches, and dependency risks before implementation starts."
tags: [session-log, plan-review, web-app, design-doc, codex]
---

# Session Log: Codex Plan reviewer webapp

**Date:** 2026-05-22  
**Session Type:** Plan Review  
**Reader:** Future implementer reviewing the Design-doc web app plan before coding  
**Post-read action:** Correct the plan before implementation starts so the wrapper app is wired to the real skill contracts and runtime

---

## Scope Reviewed

Reviewed the approved build plan for wiring the React prototype in `Design-doc/Content Hub/` into a working local web app with:

- Vite + React frontend
- FastAPI wrapper service
- Subprocess orchestration of the 8 existing pipeline skills
- Vault-backed artifact browsing and rendering

Primary review target:

- `Content-Hub-Vault-V2/00-Management-V2/Plans/Design_Doc_Web_App_Plan.md`

Code reality was checked against the existing skill entrypoints and prototype components before writing findings.

---

## Findings

### 1. High risk: the plan assumes every stage returns a single markdown file

The plan models job completion around one final `vault_path` that the UI can open in a markdown viewer. That is not true for every skill.

- `title`, `ideation`, `hook`, `outline`, and non-inplace `voice_cleanup` produce a single markdown file.
- `cascade` produces a dated output directory containing multiple files.
- `short_form` also produces a dated output directory containing multiple files.

Why this matters:

- The proposed `MarkdownViewer` flow is valid for single-file stages, but not for bundle-producing stages.
- The current plan for `/api/vault/file`, history, and post-run rendering will break for `cascade` and `short_form` unless the backend and UI distinguish between a file result and a bundle result.

Required correction:

- Redefine job results as either `file` or `bundle`.
- Add UI behavior for bundle stages:
  - show the generated directory
  - list bundle members
  - open `README.md` by default if present
  - allow switching among generated files

### 2. High risk: the Outline stage in the plan does not match the real CLI

The plan gives Outline a `research_file` input. The existing `skills.outline` entrypoint does not accept that argument.

Actual Outline contract:

- positional `topic`
- optional `--hook-path`
- optional `--length`
- optional `--platform`
- optional `--no-polish`

Why this matters:

- The wrapper cannot safely send `research_file` to Outline as currently designed.
- The UI field design for that stage is overstated relative to the real implementation.

Required correction:

- Either remove `research_file` from the Outline stage in the plan, or explicitly approve a skill change to support it.
- Keep the plan honest about whether the wrapper is "no skill changes" or not.

### 3. High risk: the proposed server virtualenv is too small to run the real pipeline

The plan proposes a new `Design-doc/server` venv with only a thin set of backend packages. That is enough to start FastAPI, but not enough to run the existing skills reliably.

Reality:

- The skill layer depends on shared project config and utility imports.
- `researcher` depends on NotebookLM-related code and external CLI access.
- `skills.utils.ai` imports the main backend settings and uses multiple provider paths.
- The repo already has a broad dependency set in the root `requirements.txt`.

Why this matters:

- The server may boot successfully and still fail on the first real job with missing Python imports or missing runtime dependencies.
- This is especially likely for `researcher`, but not limited to it.

Required correction:

- Decide up front whether the wrapper server:
  - reuses the repo's main Python environment, or
  - owns a full runtime environment with the same dependency surface required by the skills
- Do not proceed with a minimal isolated venv unless the subprocessed skills are also validated inside it.

### 4. Medium risk: output-path parsing is not standardized across skills

The plan assumes the wrapper can parse one common success string like "Written to: <path>" and use a "newest file after start time" fallback. The real skills do not emit one uniform format.

Observed output patterns differ:

- bare path
- `Output: <path>`
- `Hooks written to: <path>`
- `Outline written to: <path>`
- bundle banners that point to a directory
- overwrite-in-place behavior for `voice_cleanup`

Why this matters:

- A generic parser will be fragile.
- The fallback scan can fail for in-place rewrites because there may be no new file.
- Bundle-producing stages need directory-aware handling rather than file-only parsing.

Required correction:

- Either define a wrapper-specific parser per skill, or standardize machine-readable completion output across the skills if the "no skill changes" rule is relaxed.
- For `voice_cleanup`, return the target path directly from the wrapper based on the submitted file and `inplace` flag rather than relying only on stdout parsing.

### 5. Medium risk: the health badge is underspecified and can report false green

The plan currently centers health around backend availability plus NotebookLM auth presence. That is not enough to tell whether jobs can really run.

Missing runtime checks include:

- `claude` CLI availability for flows that shell out to Claude
- provider configuration required by the shared AI router
- any local provider availability the skills rely on

Why this matters:

- The UI can claim the system is healthy while the first real run still fails immediately.
- Research is especially exposed because it shells out to `claude` directly.

Required correction:

- Make the health endpoint report capability-level readiness, not just process liveness.
- Recommended breakdown:
  - backend reachable
  - vault reachable
  - `claude` CLI found
  - NotebookLM session present
  - primary AI provider configured

### 6. Medium risk: the Brain workspace scope is narrower than the prototype UI

The plan reduces Brain to a simple `{content}` analysis call. The prototype UI still presents:

- pasted text
- URL chips
- file drop affordances

Why this matters:

- If the UI is ported as-is, users will see controls that do not work in v1.
- That creates dead interactions in a surface that looks fully implemented.

Required correction:

- Either cut URL/file controls from the v1 Brain workspace, or specify the backend behavior for them.
- Keep the shipped UI aligned with the real backend contract.

---

## Recommended Plan Changes Before Execution

1. Change the result model from single `vault_path` to typed results: `file` or `bundle`.
2. Rewrite the endpoint and input tables so every stage mirrors the real skill CLI exactly.
3. Resolve the Python runtime strategy before implementation: shared repo environment or fully provisioned wrapper environment.
4. Replace the generic output-path parser assumption with per-skill completion handling.
5. Expand `/api/health` into a capability check, not just a backend ping.
6. Trim or explicitly redefine the Brain workspace controls for v1.

---

## Review Outcome

The plan is directionally sound, but it is not implementation-safe yet. The main issues are not visual or architectural. They are contract mismatches between the proposed wrapper app and the real skill behavior already in the repo.

If execution starts without correcting those mismatches first, the likely failure mode is:

- backend scaffolding appears to work
- simple stages partly work
- bundle stages and runtime-dependent stages fail late
- the UI contract drifts away from the real subprocess contract

This should be treated as a pre-implementation correction pass, not as a ready-to-build plan.

---

## References

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

- Adds this session log only
