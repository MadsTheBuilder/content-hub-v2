---
name: pipeline-loop
description: >-
  Extend /run-pipeline with per-stage quality gates. After each pipeline stage (researcher → ideation → hook → outline → title → cascade → short-form → voice-cleanup), stage output is scored. If composite score is below threshold (≥ 7/10), the stage is retried. If still below threshold after max retries, the pipeline aborts that stage and reports failure. Triggered by user typing /pipeline-loop, "autonomous quality-gated pipeline", or "overnight run with retries".
---

# /pipeline-loop

Extend `/run-pipeline` with per-stage quality gates. Run a full content pipeline autonomously, retrying stages that score below threshold until quality target is reached or retry cap is exhausted.

## ⚠️ EXPERIMENTAL — Fragility Caveat

**This is a shell-only skill.** The `/pipeline-loop` command exists and documents future behavior, but **will not execute the autonomous loop until scorer trust is validated by real `/prompt-lab` runs.**

Per plan § 9 — *"Most fragile of the five Opportunities. Quality lift is capped by the scorer — if the LLM-judge gives noisy scores, the quality gate becomes theater."*

**Status:** This skill documents the behavior. It refuses to execute until Opportunity 1 (`/prompt-lab`) completes at least one full optimization run on a single skill, proving the scoring layer is trustworthy enough to drive retry decisions. Before that validation, calling `/pipeline-loop` will inform the user: *"The quality gate mechanism requires `/prompt-lab` to complete a full run first. Run `/prompt-lab --skill hook --iterations 20` and review the `pipeline_results.tsv` to validate scorer trust before enabling `/pipeline-loop`."*

---

## Pipeline Position

`/pipeline-loop` is a **wrapper around** `/run-pipeline`, not a pipeline stage itself. It adds a quality-gate layer on top of the existing pipeline.

**Wraps:** `/run-pipeline` (the full autonomous pipeline: researcher → ideation → hook → outline → title → cascade → short-form → voice-cleanup)

**Adds:** Per-stage score check + automatic retry on low quality

---

## Quality Gate Parameters

These parameters are documented here. Actual implementation is deferred until scorer trust is validated.

### `--threshold` (default `7.0`)

Minimum composite score per stage (out of 10). After each pipeline stage completes:
- Composite score is computed from that stage's skill-specific scorer
- If composite ≥ `--threshold`: stage is **kept**, pipeline continues
- If composite < `--threshold`: stage is **retried** (see `--max-retries`)

**Range:** 0.0–10.0 (float)

**Recommendation:** 7.0 balances quality gate with reasonable success rate. Raising to 8.0+ demands near-perfect output; lowering to 6.0 becomes permissive.

### `--max-retries` (default `3`)

Maximum retry attempts per stage before abort. On each retry:
- The stage is re-run with a **different angle or seed** (exact mutation strategy TBD — see *Deferred Work* below)
- Output is re-scored
- If composite ≥ `--threshold`: stage is kept, loop continues
- If composite still < `--threshold` after `--max-retries` attempts: stage aborts with **FAILED** status, pipeline halts

**Range:** 1–10 (int)

**Note:** Each retry burns wall-clock time and NLM/NIM credits. Default 3 is a reasonable stopping point before manual intervention is warranted.

### `--budget-hours` (default `8.0`)

Wall-clock time cap for the entire pipeline run, including all retries. Once wall-clock time exceeds this limit:
- Current retry is completed
- Pipeline stops, reports final status

**Range:** 1.0–72.0 (float, hours)

**Note:** Inherited from `/prompt-lab` loop.py design. Prevents overnight runs from spilling into daytime.

---

## What it does

1. User types `/pipeline-loop "<topic>" "<url1,url2,..." [options]`
2. Claude confirms **EXPERIMENTAL** status and warnings before proceeding
3. If scorer trust has not been validated by `/prompt-lab` runs, Claude refuses and directs user to run `/prompt-lab` first
4. (Once scorer validation is complete:) Claude fires `/run-pipeline` and wraps each stage with:
   - **After stage completes:** Run the stage's scorer (e.g., `prompt_lab/scorers/hook_scorer.py` after `/hook` completes)
   - **Score decision:**
     - If composite ≥ `--threshold`: Log "KEPT" to `pipeline_results.tsv`, move to next stage
     - If composite < `--threshold` AND retries remaining: Log "RETRY_NEEDED", re-run stage with different prompt angle, re-score
     - If composite < `--threshold` AND no retries remaining: Log "FAILED", halt pipeline, report which stage failed and why
5. Write one summary row per stage attempt to `pipeline_results.tsv` (append-only)
6. Report final status to user: pass/fail per stage, time elapsed, output vault paths

---

## Execution Steps

### Current State (Shell Mode — Scorer Trust Not Yet Validated)

When user types `/pipeline-loop`:

1. **Confirm EXPERIMENTAL status:** Show user this warning:
   ```
   ⚠️  /pipeline-loop is EXPERIMENTAL and shell-only.
   
   This skill will NOT execute the autonomous loop until scorer trust
   is validated by real /prompt-lab runs. 
   
   To enable: 1) Run `/prompt-lab --skill hook --iterations 20`
              2) Wait for it to complete
              3) Review pipeline_results.tsv for convergence
              4) Return here
   
   Once /prompt-lab validates the scoring layer, /pipeline-loop 
   will become functional and run your content pipeline with 
   quality gates.
   ```

2. **Refuse to proceed** with a clear statement:
   ```
   The quality-gate mechanism depends on scorer trust. 
   /prompt-lab has not yet completed a full validation run. 
   
   Next step: /prompt-lab --skill hook --iterations 20
   Estimated time: ~60 minutes
   ```

3. **Stop.** Do not fire the pipeline.

### Future State (After Scorer Validation)

Once Opportunity 1 (`/prompt-lab`) completes and scorer trust is validated:

1. Parse topic, URLs, and optional flags from the user's message:
   - `--threshold` (default 7.0)
   - `--max-retries` (default 3)
   - `--budget-hours` (default 8.0)

2. Warn user about EXPERIMENTAL status and the retry mechanism:
   ```
   Running /pipeline-loop for topic: "{topic}"
   Quality gate: threshold={threshold}/10, max retries={max_retries}, budget={budget_hours}h
   
   This will run the full pipeline (researcher → voice-cleanup),
   retrying stages that score below {threshold}/10.
   
   Expected time: 30+ minutes depending on retries.
   Output: Content-Hub-Vault-V2/{slug}/ + pipeline_results.tsv
   ```

3. Confirm user accepts EXPERIMENTAL status (simple yes/no gate)

4. Run `python skills/pipeline.py "<topic>" "<urls>" --threshold {threshold} --max-retries {max_retries} --budget-hours {budget_hours}` in background

5. Report to user: "Pipeline started. Monitor terminal for live progress. I'm stepping away — check back when it's done."

6. **Stop.** Do not monitor, do not read output, do not follow up. (Same pattern as `/run-pipeline`.)

---

## Output

### Pipeline Results TSV

One row appended to `Content-Hub-Vault-V2/00-Management-V2/pipeline_results.tsv` per stage attempt.

Columns (same schema as `/prompt-lab` runs, extended):

| Column | Type | Example | Notes |
|--------|------|---------|-------|
| `timestamp` | ISO8601 | `2026-06-01T22:15:03Z` | UTC timezone |
| `skill` | string | `hook` | Pipeline stage name |
| `iteration` | int | `1` | Retry attempt (1 = first run, 2 = first retry, etc.) |
| `composite` | float | `7.20` | Aggregate score out of 10 |
| `metric_*` | float | `scroll_stop=7.2, curiosity=6.5, payoff=8.0` | Skill-specific axes (from scorer output) |
| `kept` | string | `YES`, `NO`, `FAILED` | `YES` = score ≥ threshold, `NO` = score < threshold and retried, `FAILED` = exhausted retries |
| `prompt_sha` | string | `a1b2c3d4e5f6...` | SHA256 of the skill's prompt at runtime |

### Vault Outputs

Same as `/run-pipeline`:
- Research brief → `Content-Hub-Vault-V2/10-Research/YYYY-MM-DD_<slug>.md`
- 9 ideas → `Content-Hub-Vault-V2/09-Ideation/YYYY-MM-DD_<slug>.md`
- 5 hooks → `Content-Hub-Vault-V2/05-Hooks/YYYY-MM-DD_<slug>.md`
- … (all 8 stages)

Plus: Append to `pipeline_results.tsv` with per-stage quality metrics.

---

## Open Questions / Deferred Work

1. **Retry mechanism design** — Currently undefined: what does "retry with different angle" mean?
   - Option A: Re-call the skill with the same prompt but different random seed
   - Option B: Ask Claude to mutate the prompt (like `/prompt-lab` does) then re-run
   - Option C: Swap the LLM model (e.g., Sonnet → Haiku) for a different perspective
   - **Decision deferred:** Requires either user direction or validation from first `/prompt-lab` runs.

2. **Final integration LLM-judge** — Plan § 8 table (line 372) mentions "final integration LLM-judge 0-10" as a last-stage gate. Not yet designed.
   - Should it rescore the entire 8-stage output holistically?
   - Should it pass/fail the whole pipeline or just warn?
   - **Decision deferred:** Depends on whether per-stage gates are sufficient (first runs will tell).

3. **Scorer trust validation** — This skill's readiness depends on:
   - First `/prompt-lab` run completes without errors
   - `pipeline_results.tsv` shows convergence (composite score improves over iterations)
   - User reviews the TSV and confirms the scores feel reasonable
   - **Blocker:** This skill will refuse to fire until above is done.

4. **Prompt mutation in retries** — If retry strategy is "mutate and re-run," who mutates?
   - Claude agent on-the-fly? (Fast but may not be good mutations)
   - Pre-defined mutation rules? (Slower to design, more predictable)
   - **Decision deferred:** See Deferred Work #1 above.

---

## Usage Examples

```
/pipeline-loop "AI agents for developers" "https://youtube.com/watch?v=abc,https://youtube.com/watch?v=xyz"
```

Expected response (current shell state):
```
⚠️  /pipeline-loop is EXPERIMENTAL and shell-only.

The quality-gate mechanism depends on scorer trust. /prompt-lab has not yet completed a full validation run.

Next step: /prompt-lab --skill hook --iterations 20
Estimated time: ~60 minutes
```

Once scorer trust is validated:

```
/pipeline-loop "AI agents for developers" "https://youtube.com/watch?v=abc" --threshold 7.5 --max-retries 5
```

Expected response:
```
Running /pipeline-loop for topic: "AI agents for developers"
Quality gate: threshold=7.5/10, max retries=5, budget=8h

Pipeline started. Monitor terminal for live progress. I'm stepping away — check back when it's done.
```

---

## Notes

- This skill is a **documentation-driven shell.** It captures Opportunity 5 from the plan before the underlying infrastructure (scorer validation) is in place.
- The slash command `/pipeline-loop` will exist and can be invoked, but it will refuse to execute the loop until `/prompt-lab` validates the scoring layer.
- Once scorer trust is validated, the skill's behavior will be fully functional. Until then, it serves as a clear specification of what *will* happen.
- Related skills: `/run-pipeline` (base pipeline), `/prompt-lab` (score validator), `/cascade` (one stage in the chain).
- Prompt source of truth: individual stage prompts in `prompts/` directory.

---

**References:** [[The-Self-Improvement-Loop]] · [[Self-Improvement-Loop-Tasks]] · [[Local_First_Skill_Engine_Plan]] · [[reference-autoresearch]]
