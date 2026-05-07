---
title: Orchestrate Benchmark Pipeline — Iteration 2 Complete
date: 2026-04-22
tags: [orchestrate, evals, benchmark, skill-creator]
---

# Session: Orchestrate Benchmark Pipeline Complete

Implements: [[orchestrate skill]]
References: [[2026-04-22_Orchestrate_Eval_Test]]
Modifies: [[orchestrate-workspace/iteration-2]]

## What Changed

Completed the iteration-2 benchmarking pipeline that was half-finished at session end.

### Files Written

| File | Purpose |
|------|---------|
| `orchestrate-workspace/aggregate_benchmark.py` | Reads all run-1/grading.json + timing.json, computes stats, writes benchmark.json |
| `orchestrate-workspace/generate_review.py` | Reads benchmark.json, writes benchmark.md with per-assertion table |
| `iteration-2/eval-*/with_skill/run-1/grading.json` (×3) | Parent grading.json + `summary` key wrapper |
| `iteration-2/eval-*/baseline/run-1/grading.json` (×3) | Parent grading.json + `summary` key wrapper |
| `iteration-2/eval-*/*/run-1/timing.json` (×6) | Copied from parent |
| `iteration-2/benchmark.json` | Populated from aggregate script |
| `iteration-2/benchmark.md` | Human-readable review table |

### Iteration 2 Results (Final)

| Config | Pass Rate | Time | Tokens |
|--------|-----------|------|--------|
| with_skill (Opus) | **87.5%** ± 0% | 143.6s | 59,784 |
| baseline (Haiku) | **25.0%** ± 0% | 118.8s | 53,077 |
| **Delta** | **+62.5pp** | +24.7s | +6,707 |

vs Iteration 1: with_skill was 85.7%, baseline 14.3%, delta +71pp. Delta dropped slightly because new assertions 5 and 8 are non-discriminating (both configs pass them).

### Still-Failing Assertion

Assertion 3 (Haiku recon dispatch) scored 0/3 for with_skill across all 3 evals. Root cause: eval prompt says "don't dispatch executor agents" — this suppresses the recon Haiku Explore dispatch too, even though they're different agent types.

**Fix for next iteration**: Add to eval prompt: *"You MAY dispatch a Haiku Explore agent for Phase 1 recon; the restriction only applies to executor agents."*

## Open Items

- [x] Fix assertion-3 eval prompt ambiguity — added explicit recon-agent permission note to all 3 eval prompts in `evals.json`
- [x] Add `--html` flag to `generate_review.py` — now generates collapsible `benchmark.html` with per-assertion evidence rows; run with `python generate_review.py --html`
- [ ] Add 2 more runs per configuration for meaningful stddev (currently n=1; stdev=0 in all metrics)
