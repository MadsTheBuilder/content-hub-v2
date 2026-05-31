---
title: Self-Improvement Loop — Task Breakdown
type: TaskList
status: Active
created: 2026-05-28
date: 2026-05-28
description: "Execution task list for [[The-Self-Improvement-Loop]]. Breaks the 5 Opportunities into 6 specialist-agent dispatches with dependencies, deliverables, and verification gates."
tags: [autoresearch, prompt-optimization, execution, multi-agent]
---

# Self-Improvement Loop — Execution Tasks

Source plan: [[The-Self-Improvement-Loop]] (2026-05-28).
Session log seed: [[2026-05-28_Self-Improvement-Loop-Plan]].

**User overrides on 2026-05-28:**
- Phase 7 webapp gating skipped — focus shifts to Self-Improvement Loop.
- Build all 5 Opportunities (full scope).
- Agents must ASK when they hit an open question — no silent picks.

**Verification scope (this session):** structural only. Functional verification (scorer trust, loop convergence, prompt-beats-baseline) requires real NLM/NIM pipeline runs — out of scope until first `/prompt-lab` execution.

---

## Plan → 6 Agent Dispatches

| # | Agent | Covers | Net new files | Depends on |
|---|---|---|---|---|
| A1 | Tracking Foundation | Opp 2 + Opp 4 | `pipeline_results.tsv` + log hooks in `skills/pipeline.py` | — |
| A2 | Fixtures Builder | Opp 1 (inputs) | 8 × `prompt-lab/fixtures/<skill>_test_topics.json` | — |
| A3 | Scorers Builder | Opp 1 (scoring) | 8 × `prompt-lab/scorers/<skill>_scorer.py` | A1 (schema) |
| A5 | Brief.md + Integration | Opp 3 | `brief.md` + read-brief hooks in 8 skills | — |
| A4 | Loop Builder | Opp 1 (loop) | `prompt-lab/loop.py` | A1, A2, A3 |
| A6 | /pipeline-loop | Opp 5 | `.claude/skills/pipeline-loop/` + quality gate | A1, A4 |

---

## Dispatch Sequencing

**Phase 1 (parallel)** — A1 + A2 truly independent.
**Phase 2 (parallel, after A1)** — A3 + A5. Both may halt on open questions; user answers batched.
**Phase 3 (sequential)** — A4 after Phases 1+2 complete.
**Phase 4 (sequential)** — A6 last. Plan § 9 explicitly warns Opp 5 is fragile until scorer trust is validated by real runs — building shell now, functional validation deferred.

---

## Agent Briefing Contract (every agent receives these)

1. **State assumptions explicitly.** If uncertain, ask rather than guess.
2. **Present multiple interpretations.** Don't pick silently when ambiguity exists.
3. **Push back when warranted.** If a simpler approach exists, say so.
4. **Stop when confused.** Name what's unclear and ask.
5. **Surgical changes.** Every changed line must trace to the brief. Don't refactor adjacent code. Match existing style. Don't delete pre-existing dead code unless asked.
6. **Goal-driven execution.** State plan as `[step] → verify: [check]` and loop until verified.
7. **Report back** in this format: files created/modified (paths), assumptions made, open questions raised, what was tested, what could not be tested.

---

## Open Questions (per plan § 11)

These BLOCK agents until answered:

1. **Trust LLM-as-judge scoring?** — Blocks A3 (scorers) and A6 (quality gate). If "no," Opps 1 + 5 are dead.
2. **Is `.claude/skills/*/iteration-1/` eval scaffolding active or stale?** — Blocks A3 (reuse vs. fresh start).
3. **`brief.md` vs CLI flags?** — Blocks A5 (file convention vs. argparse).

Per user (2026-05-28): agents must ASK before deciding. Relay to user is **batched** — collect blocking questions across A3 + A5, ask user once.

---

## Verification Gates (main session owns these)

After each phase:
- [ ] **A1**: `pipeline_results.tsv` exists at `Content-Hub-Vault-V2/00-Management-V2/pipeline_results.tsv` with documented schema covering all 8 skills' heterogeneous metrics; `skills/pipeline.py` imports + writes one test row.
- [ ] **A2**: 8 fixtures files at `prompt-lab/fixtures/`; each is valid JSON with the documented shape (`topics: [...]`, `model_settings: {...}`).
- [ ] **A3**: 8 scorer files at `prompt-lab/scorers/`; each exposes `score_<skill>_output(...) -> float`; Python import smoke test passes.
- [ ] **A5**: `brief.md` exists at `Content-Hub-Vault-V2/00-Management-V2/brief.md` (or CLI alternative if user picked flags); 8 skills updated with read-brief hook OR argparse flag; no skill regressions on existing CLI args.
- [ ] **A4**: `prompt-lab/loop.py` exists; smoke-imports; CLI surface documented; structural dry-run (no real model calls) writes ≥ 1 row to TSV.
- [ ] **A6**: `.claude/skills/pipeline-loop/SKILL.md` exists with YAML frontmatter; quality-gate threshold + retry-cap documented; section-9 fragility caveat noted in SKILL.md header.

---

## Out of Scope This Sprint

- Real `/prompt-lab` execution (burns NLM/NIM credits — separate session).
- Scorer rubric tuning (depends on real runs).
- Phase 7 webapp launcher (skipped per user 2026-05-28).

---

**Related:** [[The-Self-Improvement-Loop]] · [[2026-05-28_Self-Improvement-Loop-Plan]] · [[Local_First_Skill_Engine_Plan]] · [[Current_Sprint]]

---

## 🅿 Parked — 2026-05-29

**Status: Parked pending major decisions and real-run data.**

Dry run completed successfully (structural pass). Three gaps remain in `prompt_lab/loop.py` that cannot be resolved without prior decisions:

1. **`_mutate_prompt()` is a stub** — Multiple valid strategies exist (Claude rewrites a section, swap example order, tighten constraints). The right choice depends on what the scorer responds to in real runs. Cannot decide this in the abstract.

2. **`_run_skill_over_fixtures()` is a stub** — Skills are CLI scripts, not importable modules. Two paths forward: (a) subprocess with a `--output-only` flag added to each of 8 skills, or (b) refactor skills to expose a callable `run(topic) -> str` function. Both touch the skill files and need a deliberate decision on architecture before touching 8 files.

3. **`_score_output()` missing 6 scorer imports** — The 6 scorer files exist and are complete but were never wired into the dispatch table. This is the only gap that is purely unfinished work (not a design decision). Straightforward to fix once the above two decisions are made and a real run is scheduled.

**Blocked on:**
- Mutation strategy decision (needs first real scorer output to inform it)
- Skill invocation architecture decision (subprocess vs. importable module)
- A scheduled real `/prompt-lab` run to validate scorer trust before anything else moves

**Resuming:** Pick this up after at least one real pipeline run produces scored output in `pipeline_results.tsv`.
