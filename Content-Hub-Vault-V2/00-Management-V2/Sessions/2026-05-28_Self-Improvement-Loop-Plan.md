---
title: Session — Self-Improvement Loop Plan
type: Session
date: 2026-05-28
description: "Session log: drafted and saved [[The-Self-Improvement-Loop]] — survey mapping Karpathy's autoresearch pattern onto Content Hub V2 prompts, scorers, and pipeline."
tags: [autoresearch, planning, prompt-optimization]
---

# 2026-05-28 — Self-Improvement Loop Plan

## Summary

Drafted and saved [[The-Self-Improvement-Loop]] — an opportunity survey mapping Karpathy's `autoresearch` framework (modify→score→keep-or-revert loop) onto Content Hub V2. No code changes. Documentation only.

## What Changed

- **Created:** `Content-Hub-Vault-V2/00-Management-V2/Plans/The-Self-Improvement-Loop.md`
  - 11 sections + file mapping table
  - 5 Opportunities ranked by ROI
  - Locked per-prompt sequential architecture (vs. end-to-end)
  - 9-night schedule covering all 8 production prompts + 1 integration pass
  - Honest fact-vs-assumption split per opportunity

## Edges

- **Implements:** [[reference-autoresearch]] (the integration patterns from the memory reference)
- **References:** [[Local_First_Skill_Engine_Plan]] · [[Refined_Pipeline]] · [[Researcher_Optimisation]]
- **Targets for optimization:** [[researcher]] · [[ideation]] · [[hook]] · [[outline]] · [[title]] · [[cascade]] · [[short-form]] · [[voice-cleanup]]
- **New files proposed (do not exist yet):**
  - `Content-Hub-Vault-V2/00-Management-V2/brief.md` (Opp 3 — per-run rulebook)
  - `Content-Hub-Vault-V2/00-Management-V2/pipeline_results.tsv` (Opp 2 — iteration log)
  - `prompt-lab/fixtures/<skill>_test_topics.json` × 8
  - `prompt-lab/scorers/<skill>_scorer.py` × 8
  - `prompt-lab/loop.py` (Opp 1 — the autoresearch loop)

## Files Touched

- Created: `Content-Hub-Vault-V2/00-Management-V2/Plans/The-Self-Improvement-Loop.md`
- Created: `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-28_Self-Improvement-Loop-Plan.md` (this file)

## Key Decisions Locked

1. **Per-prompt optimization wins over end-to-end.** Matches Karpathy's own approach (he optimizes `train.py` with `prepare.py` frozen).
2. **Build order:** Opp 2 (tracking) → Opp 1 (`/prompt-lab`) → Opp 3 (`brief.md`) → Opp 4 (logged budgets) → Opp 5 (`/pipeline-loop`).
3. **Scorer trustworthiness is the make-or-break.** Voice cleanup's banned-phrase count is the most trustworthy metric (programmatic integer); LLM-judge scoring is the risk surface.
4. **No implementation this session.** Documentation only — `/prompt-lab` build is a separate future session, gated on Phase 7 webapp completion.

## Open Items

1. Does the user trust LLM-as-judge scoring for hook/script quality? (Blocks Opps 1 and 5.)
2. Is the existing per-skill eval scaffolding (`.claude/skills/*/iteration-1/`) active or stale?
3. Would the user actually write a `brief.md` each night, or prefer CLI flags?

## Next Action

Wait for user direction. The plan recommends starting with **Opportunity 2** (`pipeline_results.tsv`) since it's low-effort and unlocks everything else — but that's a separate session post Phase 7.
