---
date: 2026-05-14
type: session-log
---

# Graphify Update — 2026-05-14

## What Changed

Full incremental update of the knowledge graph (`/graphify --update`) covering all 1,633 new/changed files accumulated since the last run on 2026-04-29 (which only covered 118 files).

## Result

| Metric | Before (2026-04-29) | After (2026-05-14) |
|---|---|---|
| Nodes | 279 | 13,054 |
| Edges | 0 | 37,982 |
| Communities | — | 802 |

## Pipeline Steps

1. **Incremental detect** — 1,633 changed files: 539 code, 494 docs, 1 paper, 28 images + notebooklm-py
2. **AST extraction** — 11,344 nodes, 47,426 edges from 539 code files
3. **Semantic cache check** — 133 files already cached; 961 files needed fresh extraction
4. **76 parallel subagents** — 37 doc chunks (25 files each) + 39 image chunks (1 image each). All completed.
5. **Merge** — cached (199 nodes, 305 edges) + new (1,775 nodes, 1,689 edges) → 1,657 semantic nodes
6. **Full extract** — AST + semantic = 12,815 nodes, 49,420 edges (pre-dedup)
7. **Graph build + cluster** — 13,054 nodes, 37,982 edges, 802 communities
8. **Outputs** — `graph.json` (21.7 MB), `GRAPH_REPORT.md` (336 KB), `graph.html` (215 KB)

## Files Touched

- `graphify-out/graph.json` — rebuilt (backed up as `.graphify_old.json`)
- `graphify-out/GRAPH_REPORT.md` — rebuilt
- `graphify-out/graph.html` — rebuilt
- `graphify-out/manifest.json` — updated
- `graphify-out/cost.json` — updated

## Open Items

- Community labels are auto-generated (top node by degree per community). Many are function names like "Authtokens", "Fetch()", etc. — the large communities (0–5, each 700–1,600 nodes) have very low cohesion (0.0–0.01), which suggests they're broad catch-all clusters rather than tight semantic groups. This is expected for a large mixed codebase.
- The `total_words` field in GRAPH_REPORT is 0 because we ran `--update` mode which doesn't re-run full detect. Cosmetic only.

## Related

Modifies: [[graphify-out/GRAPH_REPORT.md]], [[graphify-out/graph.json]]
References: [[Current_Sprint]], [[context.md]]
