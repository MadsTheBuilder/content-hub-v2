"""
Generate benchmark.md (and optionally benchmark.html) from benchmark.json.
Usage:
  python generate_review.py           # writes benchmark.md
  python generate_review.py --html    # writes benchmark.md + benchmark.html
"""
import json, os, sys

BASE = os.path.join(os.path.dirname(__file__), "iteration-2")
bm = json.load(open(os.path.join(BASE, "benchmark.json")))
emit_html = "--html" in sys.argv

meta = bm["metadata"]
rs = bm["run_summary"]
ws = rs["with_skill"]
bl = rs["baseline"]
delta = rs["delta"]
eval_names = {1: "views-count", 2: "posting-time", 3: "approval-workflow"}


def pct(v):
    return f"{v * 100:.1f}%"


def pm(d):
    return f"{pct(d['mean'])} ± {pct(d['stddev'])}"


# ── Markdown ────────────────────────────────────────────────────────────────

lines = [
    f"# Skill Benchmark: {meta['skill_name']}",
    "",
    f"**Executor model**: {meta['executor_model']}  ",
    f"**Analyzer model**: {meta['analyzer_model']}  ",
    f"**Date**: {meta['timestamp']}  ",
    f"**Evals**: {', '.join(str(e) for e in meta['evals_run'])} ({meta['runs_per_configuration']} run each per configuration)",
    "",
    "## Summary",
    "",
    "| Metric | with_skill (Opus) | baseline (Haiku) | Delta |",
    "|--------|-------------------|------------------|-------|",
    f"| Pass Rate | {pm(ws['pass_rate'])} | {pm(bl['pass_rate'])} | {delta['pass_rate']} |",
    f"| Time | {ws['time_seconds']['mean']:.1f}s ± {ws['time_seconds']['stddev']:.1f}s | {bl['time_seconds']['mean']:.1f}s ± {bl['time_seconds']['stddev']:.1f}s | {delta['time_seconds']}s |",
    f"| Tokens | {ws['tokens']['mean']:,.0f} ± {ws['tokens']['stddev']:,.0f} | {bl['tokens']['mean']:,.0f} ± {bl['tokens']['stddev']:,.0f} | {delta['tokens']} |",
    "",
    "## Per-Eval Results",
    "",
]

for run in bm["runs"]:
    ev = eval_names.get(run["eval_id"], str(run["eval_id"]))
    cond = run["configuration"]
    r = run["result"]
    lines.append(f"### Eval {run['eval_id']} ({ev}) — {cond}")
    lines.append(f"Pass rate: **{pct(r['pass_rate'])}** ({r['passed']}/{r['total']}) | "
                 f"Time: {r['time_seconds']:.1f}s | Tokens: {r['tokens']:,}")
    lines.append("")
    lines.append("| # | Assertion | Result |")
    lines.append("|---|-----------|--------|")
    for i, exp in enumerate(run["expectations"], 1):
        status = "✓" if exp["passed"] else "✗"
        evidence = exp["evidence"][:80].replace("|", "\\|") + ("…" if len(exp["evidence"]) > 80 else "")
        lines.append(f"| {i} | {exp['text'][:60]} | {status} {evidence} |")
    lines.append("")

if bm.get("notes"):
    lines += ["## Notes", ""]
    for note in bm["notes"]:
        lines.append(f"- {note}")
    lines.append("")

md_out = os.path.join(BASE, "benchmark.md")
with open(md_out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"Written: {md_out}")


# ── HTML ────────────────────────────────────────────────────────────────────

if emit_html:
    def h(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def badge(passed, total):
        rate = passed / total if total else 0
        color = "#2da44e" if rate >= 0.8 else "#d29922" if rate >= 0.5 else "#cf222e"
        return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:12px;font-size:.85em">{passed}/{total} ({rate*100:.0f}%)</span>'

    rows_html = []
    for run in bm["runs"]:
        ev = eval_names.get(run["eval_id"], str(run["eval_id"]))
        cond = run["configuration"]
        r = run["result"]
        exp_rows = "".join(
            f'<tr style="background:{"#f0fff4" if e["passed"] else "#fff0f0"}">'
            f'<td style="padding:4px 8px;color:{"#2da44e" if e["passed"] else "#cf222e"};font-weight:bold">{"✓" if e["passed"] else "✗"}</td>'
            f'<td style="padding:4px 8px">{h(e["text"])}</td>'
            f'<td style="padding:4px 8px;font-size:.85em;color:#555">{h(e["evidence"][:120])}{"…" if len(e["evidence"]) > 120 else ""}</td>'
            f'</tr>'
            for e in run["expectations"]
        )
        rows_html.append(f"""
        <details style="margin:12px 0;border:1px solid #d0d7de;border-radius:6px">
          <summary style="padding:10px 14px;cursor:pointer;background:#f6f8fa;font-weight:600">
            Eval {run['eval_id']} ({h(ev)}) — {h(cond)} &nbsp; {badge(r['passed'], r['total'])}
            &nbsp; <span style="font-weight:normal;font-size:.9em">{r['time_seconds']:.1f}s | {r['tokens']:,} tokens</span>
          </summary>
          <table style="width:100%;border-collapse:collapse;font-size:.9em">
            <thead><tr style="background:#f6f8fa">
              <th style="padding:6px 8px;text-align:left">Pass</th>
              <th style="padding:6px 8px;text-align:left">Assertion</th>
              <th style="padding:6px 8px;text-align:left">Evidence</th>
            </tr></thead>
            <tbody>{exp_rows}</tbody>
          </table>
        </details>""")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Benchmark: {h(meta['skill_name'])}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:960px;margin:32px auto;padding:0 16px;color:#24292f}}</style>
</head>
<body>
<h1>Skill Benchmark: {h(meta['skill_name'])}</h1>
<p><b>Executor:</b> {h(meta['executor_model'])} &nbsp;|&nbsp; <b>Analyzer:</b> {h(meta['analyzer_model'])} &nbsp;|&nbsp; <b>Date:</b> {h(meta['timestamp'])}</p>
<h2>Summary</h2>
<table style="border-collapse:collapse;width:100%">
  <thead><tr style="background:#f6f8fa"><th style="padding:8px 12px;border:1px solid #d0d7de">Metric</th><th style="padding:8px 12px;border:1px solid #d0d7de">with_skill (Opus)</th><th style="padding:8px 12px;border:1px solid #d0d7de">baseline (Haiku)</th><th style="padding:8px 12px;border:1px solid #d0d7de">Delta</th></tr></thead>
  <tbody>
    <tr><td style="padding:8px 12px;border:1px solid #d0d7de">Pass Rate</td><td style="padding:8px 12px;border:1px solid #d0d7de">{pm(ws['pass_rate'])}</td><td style="padding:8px 12px;border:1px solid #d0d7de">{pm(bl['pass_rate'])}</td><td style="padding:8px 12px;border:1px solid #d0d7de;font-weight:bold;color:#2da44e">{h(delta['pass_rate'])}</td></tr>
    <tr><td style="padding:8px 12px;border:1px solid #d0d7de">Time</td><td style="padding:8px 12px;border:1px solid #d0d7de">{ws['time_seconds']['mean']:.1f}s ± {ws['time_seconds']['stddev']:.1f}s</td><td style="padding:8px 12px;border:1px solid #d0d7de">{bl['time_seconds']['mean']:.1f}s ± {bl['time_seconds']['stddev']:.1f}s</td><td style="padding:8px 12px;border:1px solid #d0d7de">{h(delta['time_seconds'])}s</td></tr>
    <tr><td style="padding:8px 12px;border:1px solid #d0d7de">Tokens</td><td style="padding:8px 12px;border:1px solid #d0d7de">{ws['tokens']['mean']:,.0f} ± {ws['tokens']['stddev']:,.0f}</td><td style="padding:8px 12px;border:1px solid #d0d7de">{bl['tokens']['mean']:,.0f} ± {bl['tokens']['stddev']:,.0f}</td><td style="padding:8px 12px;border:1px solid #d0d7de">{h(delta['tokens'])}</td></tr>
  </tbody>
</table>
<h2>Per-Eval Results</h2>
{''.join(rows_html)}
{('<h2>Notes</h2><ul>' + ''.join(f'<li>{h(n)}</li>' for n in bm['notes']) + '</ul>') if bm.get('notes') else ''}
</body></html>"""

    html_out = os.path.join(BASE, "benchmark.html")
    with open(html_out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Written: {html_out}")
