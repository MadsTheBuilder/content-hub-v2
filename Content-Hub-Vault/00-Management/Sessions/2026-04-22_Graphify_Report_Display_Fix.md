---
date: 2026-04-22
type: session-log
status: complete
---

# Graphify Report Display Fix — api() Label Disambiguation

Follows: [[2026-04-22_Graphify_Update_Validation]]

## What Happened

Investigated the open item from the prior session: "Surprising Connections section dominated by `api()` → various tools — worth investigating if `api` should be excluded from god node analysis."

### Trace Results

The `api()` "problem" turned out to be a display artifact, not a graph corruption:

- **57 correctly-namespaced AST nodes** exist: `activecampaign_api`, `dataforseo_api`, `zoominfo_api`, etc. — one per CLI file.
- **Zero cross-tool collisions** — no edges between different tools' `api()` nodes.
- The GRAPH_REPORT `Surprising Connections` section displayed all of them as `api()` because it used the node `label` field, not the node `id`.

The 5 Surprising Connections were real and came from exactly 2 nodes:
- `dataforseo_api` → conceptually_related_to SEO Tools (code → skill doc cross-reference)
- `zoominfo_api` → references ZoomInfo/Contact Search/Company Search/Scoops Lookup (JS CLI → integration .md doc)

### Fix Applied

Patched two files in the graphify package:

**`graphify/analyze.py`** (`_cross_file_surprises` function, line ~228):
- Added `"source_id": src_id` and `"target_id": tgt_id` fields to each candidate dict alongside the existing label-based `"source"` and `"target"` fields.

**`graphify/report.py`** (Surprising Connections render block, line ~90):
- When `source_id != source_label`, renders as `label (id)` instead of just `label`.
- Same for target nodes.

Result: `api() (dataforseo_api)` and `api() (zoominfo_api)` — unambiguous.

### GRAPH_REPORT.md Regenerated

Re-ran report generation using `graphify.report.generate()` directly against the existing `graph.json` and `analysis.json`. No re-extraction needed.

## Files Touched

- `C:/.../graphify/analyze.py` — added `source_id`/`target_id` fields to surprise candidate dicts
- `C:/.../graphify/report.py` — render `label (id)` when they differ
- `graphify-out/GRAPH_REPORT.md` — regenerated with fixed display

## Open Items

- The 40 "X CLI" singleton communities (43–82) remain in the community listing. These are trivially small 2-node clusters `{api(), main()}` per tool. A `--cluster-only` pass with `min_community_size` filter would clean the listing if that feature is added upstream.
- `skill_landing_page_optimization` still has one variant at degree 1 (carried over from prior session).
