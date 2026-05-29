---
date: 2026-05-15
type: session-log
tags: [skill-creator, outline, eval, benchmark]
description: Full skill-creator improvement loop on /outline — drafted improved SKILL.md, ran 3 evals (6 subagents), graded all runs, wrote benchmark.json, generated HTML viewer.
---

# 2026-05-15 — Outline Skill: Full Skill-Creator Improvement Loop

## What Changed

Ran the complete skill-creator improvement loop on the `/outline` skill:
- Drafted improved [[Outline Skill]] with YAML frontmatter, pipeline context, and explicit /cascade routing
- Snapshotted original skill to `.claude/skills/outline-workspace/skill-snapshot/SKILL.md`
- Wrote 3 eval test cases and spawned 6 parallel subagents (3 evals × with_skill + old_skill)
- Graded all 6 runs, wrote `benchmark.json`, generated static HTML viewer at `.claude/skills/outline-workspace/iteration-1/eval_review.html`

## Benchmark Results

| Eval | with_skill | without_skill (snapshot) | Δ |
|------|-----------|--------------------------|---|
| 1: Hook approval, no args | 6/6 (1.00) | 5/6 (0.83) | **+1 win** |
| 2: Topic + hook path explicit | 3/5 (0.60) | 4/5 (0.80) | **−1 regression** |
| 3: Regenerate with feedback | 5/5 (1.00) | 5/5 (1.00) | tie |
| **Overall mean** | **0.87** | **0.88** | −0.01 |

## Key Findings

**Win — Eval 1**: New skill routes to /cascade after outline review. Old skill ends with "Then film — the outline is your shooting script." This is the most important pipeline-continuity fix.

**Regression — Eval 2**: New skill over-applies CLAUDE.md §1 when hook file is missing:
1. Asks for platform confirmation even though yt-long is the default (unnecessary)
2. Drops `--hook-path` from the Python command when file doesn't exist (wrong — `skills/outline.py`'s `load_hook()` has its own missing-file fallback; the path should always be passed through)

**Tie — Eval 3**: Both skills handle regeneration with structural feedback equally well.

## Root Cause of Eval 2 Regression

New SKILL.md is missing two explicit guard rails:
- "Always pass --hook-path to the Python command unchanged, even if the file doesn't exist locally — Python handles the fallback via `load_hook()`"
- "Defaults (length, platform) never require confirmation, even during a clarification moment"

## Files Touched

- `.claude/skills/outline/SKILL.md` — improved (adds YAML frontmatter, pipeline position, research scan, /cascade routing)
- `.claude/skills/outline-workspace/skill-snapshot/SKILL.md` — old skill baseline
- `.claude/skills/outline-workspace/evals/evals.json` — 3 eval test cases
- `.claude/skills/outline-workspace/iteration-1/` — 6 run dirs with grading.json, timing.json, outputs/
- `.claude/skills/outline-workspace/iteration-1/benchmark.json` — full benchmark result
- `.claude/skills/outline-workspace/iteration-1/eval_review.html` — static HTML viewer
- `generate_review.py` (plugin) — patched all `read_text()` calls to use UTF-8 (Windows encoding fix)

## Open Items

- [ ] Patch eval 2 regression in `.claude/skills/outline/SKILL.md`: add explicit note about passing `--hook-path` unchanged and not confirming defaults
- [ ] Re-run eval 2 only after the patch to verify the regression is fixed
- [ ] Consider running `/outline` end-to-end to verify live behavior

## References

Implements: [[Local First Skill Engine Plan]]
Modifies: [[Outline Skill]]
References: [[Skill Creator Plugin]]
