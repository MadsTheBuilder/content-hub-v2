---
name: Orchestrations folder
description: Persisted state files for every /orchestrate and /resume-orchestration run
---

# Orchestrations

This folder holds the **state file** for every orchestration run produced by the `/orchestrate` skill. Each file is the recovery anchor that lets `/resume-orchestration` pick up where a prior session left off when context gets compacted.

## File naming

```
YYYY-MM-DD_<kebab-case-slug>.md
```

Example: `2026-04-20_phase4-ab-testing-frontend.md`

One file per orchestration attempt. Multiple attempts of the same task get distinct files (append `-v2`, `-retry`, etc. to the slug).

## File structure

Every file has YAML frontmatter followed by four markdown sections:

```yaml
---
slug: phase4-ab-testing-frontend
created: 2026-04-20
status: awaiting-approval   # | approved | executing | complete | abandoned
current_group: null
groups_complete: []
specialists_involved: [frontend-agent]
---
```

- **Recon summary** — 3–8 bullets capturing the Phase 1 findings the plan depends on (file paths, existing patterns, gaps).
- **Execution plan** — the full Phase 2 plan as presented to the user: groups, tasks, complexity, files, acceptance criteria.
- **Agent prompts** — one section per task. Contains the exact `Agent(...)` dispatch payload with a `{SPECIALIST_DEFINITION}` placeholder filled in from `AGENTS.md` at Phase 4 dispatch time.
- **Status log** — append-only list of `<timestamp> <event>` lines covering every state transition.

## Status lifecycle

| Status | Meaning | Next action |
|--------|---------|-------------|
| `awaiting-approval` | Plan written to disk, user has not yet approved | User approves → status flips to `approved` |
| `approved` | User accepted the plan, Phase 4 not yet started | Advisor begins Phase 4 dispatch |
| `executing` | Phase 4 is in flight | Advisor continues; status updates each phase transition |
| `complete` | Phase 6 verification passed, orchestration done | Historical record only |
| `abandoned` | Manually set by user to mark a failed/retired run | Ignored by `/resume-orchestration` |

## Resuming

Run `/resume-orchestration`. The skill looks for files with `status` in `{awaiting-approval, approved, executing}` and prompts to resume one.

## Cleanup

Completed files stay as historical record — they document what shipped and how it was decomposed. Set `status: abandoned` on any run that should be skipped by the resume skill. Do not delete state files — the git history is easier to audit with them in place.
