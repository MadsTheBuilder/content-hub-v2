"""
Aggregate iteration-2 run-1 grading files into benchmark.json.
Usage: python aggregate_benchmark.py
"""
import json, os, statistics
from datetime import datetime, timezone

BASE = os.path.join(os.path.dirname(__file__), "iteration-2")
EVALS = [
    ("eval-1-views-count", 1),
    ("eval-2-posting-time", 2),
    ("eval-3-approval-workflow", 3),
]
CONDITIONS = ["with_skill", "baseline"]

runs = []
by_condition = {c: {"pass_rates": [], "times": [], "tokens": []} for c in CONDITIONS}

for eval_dir, eval_id in EVALS:
    for cond in CONDITIONS:
        run1 = os.path.join(BASE, eval_dir, cond, "run-1")
        g = json.load(open(os.path.join(run1, "grading.json")))
        t = json.load(open(os.path.join(run1, "timing.json")))

        pr = g["summary"]["pass_rate"]
        secs = t["total_duration_seconds"]
        tokens = t["total_tokens"]

        by_condition[cond]["pass_rates"].append(pr)
        by_condition[cond]["times"].append(secs)
        by_condition[cond]["tokens"].append(tokens)

        runs.append({
            "eval_id": eval_id,
            "configuration": cond,
            "run_number": 1,
            "result": {
                "pass_rate": pr,
                "passed": g["summary"]["passed"],
                "failed": g["summary"]["failed"],
                "total": g["summary"]["total"],
                "time_seconds": secs,
                "tokens": tokens,
            },
            "expectations": g["expectations"],
            "notes": [],
        })


def stats(vals):
    mean = round(statistics.mean(vals), 4)
    stddev = round(statistics.stdev(vals), 4) if len(vals) > 1 else 0.0
    return {"mean": mean, "stddev": stddev, "min": min(vals), "max": max(vals)}


ws = by_condition["with_skill"]
bl = by_condition["baseline"]
delta_pr = round(statistics.mean(ws["pass_rates"]) - statistics.mean(bl["pass_rates"]), 4)
delta_time = round(statistics.mean(ws["times"]) - statistics.mean(bl["times"]), 1)
delta_tokens = round(statistics.mean(ws["tokens"]) - statistics.mean(bl["tokens"]))

benchmark = {
    "metadata": {
        "skill_name": "orchestrate",
        "skill_path": ".claude/skills/orchestrate/SKILL.md",
        "executor_model": "opus",
        "analyzer_model": "sonnet",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "evals_run": [e[1] for e in EVALS],
        "runs_per_configuration": 1,
    },
    "runs": runs,
    "run_summary": {
        "with_skill": {
            "pass_rate": stats(ws["pass_rates"]),
            "time_seconds": stats(ws["times"]),
            "tokens": stats(ws["tokens"]),
        },
        "baseline": {
            "pass_rate": stats(bl["pass_rates"]),
            "time_seconds": stats(bl["times"]),
            "tokens": stats(bl["tokens"]),
        },
        "delta": {
            "pass_rate": f"+{delta_pr:.2f}" if delta_pr >= 0 else f"{delta_pr:.2f}",
            "time_seconds": f"+{delta_time:.1f}" if delta_time >= 0 else f"{delta_time:.1f}",
            "tokens": f"+{delta_tokens}" if delta_tokens >= 0 else str(delta_tokens),
        },
    },
    "notes": [
        "Iteration 2: 8 assertions per eval (up from 7). New assertions: group notation, step-count > 3.",
        "Assertion 3 (Haiku recon dispatch): 0/3 with_skill passes — eval prompt interference suspected.",
        "Fix: eval prompt should explicitly allow recon agent dispatch to remove ambiguity.",
    ],
}

out = os.path.join(BASE, "benchmark.json")
with open(out, "w") as f:
    json.dump(benchmark, f, indent=2)
print(f"Written: {out}")
print(f"with_skill mean pass_rate: {statistics.mean(ws['pass_rates']):.3f}")
print(f"baseline mean pass_rate:   {statistics.mean(bl['pass_rates']):.3f}")
print(f"delta: {delta_pr:+.3f}")
