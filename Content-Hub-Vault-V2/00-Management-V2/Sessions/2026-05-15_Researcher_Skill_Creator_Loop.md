---
date: 2026-05-15
type: session-log
tags: [skill-creator, researcher, eval, benchmark]
description: "Full skill-creator improvement loop on /researcher — rewrote SKILL.md with YAML frontmatter, pipeline position, and output structure; ran 6-agent eval; benchmark shows +0.08 pass rate delta over snapshot."
---

# 2026-05-15 — /researcher Skill-Creator Improvement Loop

## What Happened

Ran the full [[skill-creator]] improvement loop on the [[researcher]] skill. This is the first time the skill-creator eval framework has been applied to any skill in this project.

## Files Touched

- `.claude/skills/researcher/SKILL.md` — **rewritten** with YAML frontmatter, pipeline position, defined output structure, and explicit /hook handoff instruction
- `.claude/skills/researcher-workspace/skill-snapshot/SKILL.md` — snapshot of old skill before rewrite
- `.claude/skills/researcher-workspace/evals/evals.json` — 3 eval prompts (no-args, bare topic, full invocation)
- `.claude/skills/researcher-workspace/iteration-1/` — full eval run output (6 subagents × 3 evals)
- `.claude/skills/researcher-workspace/iteration-1/benchmark.json` — aggregated pass rates, timing, tokens
- `.claude/skills/researcher-workspace/iteration-1/eval_review.html` — static viewer (served at localhost:8765)

## Key Changes to SKILL.md

### 1. YAML frontmatter added (was missing entirely)
The old skill had no `name:` or `description:` block. This meant Claude only activated /researcher when the user typed `/researcher` literally. The new frontmatter lists trigger phrases:
- "research a topic", "find content gaps", "what should I make a video about", "check trending repos", "I want to start a new video", "run research on [topic]"

Also positions it explicitly as **Step 1 of 7** in the chain: `/researcher → /hook → /outline → /title → /cascade → /short-form → /voice-cleanup`

### 2. Pipeline position stated in body
First line now reads: "Step 1 of the production pipeline. Produces a research brief... The brief feeds into `/hook`."

### 3. Brief output structure defined
Old skill: "content gap analysis anchored to the specific repo" (vague)
New skill: explicitly names the 5-section structure (What it does / Who it's for / How it works / When to use / Watch out for) + Recommended Video Angle + Raw Q&A. Matches what `skills/researcher.py` actually writes.

### 4. /hook handoff made mandatory
Old: `/hook` mentioned only in a footnote.
New: dedicated "After Completion → Next Step" section with `Always surface this suggestion when presenting results.`

### 5. Confirmation step — unchanged
The prompt `"Running researcher on: [repo1, repo2] — niche: [niche] — confirm?"` is word-for-word identical in both versions.

## Eval Results

| Config | Pass Rate | Time (s) | Tokens |
|---|---|---|---|
| with_skill (new) | 0.85 ± 0.11 | 25.7s | 37,378 |
| old_skill (snapshot) | 0.77 ± 0.23 | 24.4s | 37,106 |
| **Delta** | **+0.08** | +1.3s | +272 |

**Per-eval:**

| Eval | with_skill | old_skill |
|---|---|---|
| 1 — no-args | 0.75 | 0.50 |
| 2 — bare topic | 0.80 | 0.80 |
| 3 — full invocation | 1.00 | 1.00 |

Key insight: the gain is entirely in Eval 1 (no-args entry). The new frontmatter's pipeline framing shapes how Claude introduces the skill when there's no context. Old skill variance (0.23 stddev) vs new skill (0.11 stddev) — the new skill degrades more gracefully on weak inputs.

## Open Items

- [ ] Iteration 2 pending user feedback from HTML viewer (localhost:8765)
- [ ] Two assertions noted as misplaced: assertion 4 on eval-1 (/hook fires too early), assertion 4 on eval-2 (command syntax shown at wrong stage) — tighten in evals.json before next iteration
- [ ] Description optimization (`run_loop.py`) not yet run — deferred until user confirms skill shape is final

## Implements / Modifies

Modifies: [[researcher]]
References: [[skill-creator]]
References: [[2026-05-13_Researcher_Optimisation_Complete]]
