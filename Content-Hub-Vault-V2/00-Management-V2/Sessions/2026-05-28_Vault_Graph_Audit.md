---
date: 2026-05-28
tags: [session, audit, cleanup, storage]
description: "Space audit of project root — identified bloat, clarified intent, deferred decisions on 3 items."
---

# Session: Project Space Audit

## What Happened

Ran a full size analysis of `Content Hub V2` project root. Surfaced all items over ~1 MB and categorised each as intentional, undecided, or removable.

## Findings

| Path | Size | Decision |
|------|------|----------|
| `.venv/` | 719 MB | Keep — runtime dependency |
| [[Content-Hub-Vault-V2]] | 109 MB | Keep |
| `Design-doc/web/` (node_modules) | 82 MB | **Keep** — intentional landing page for the system |
| [[graphify-out]] intermediates (`.graphify_*.json`, `cache/`) | ~60 MB | **Keep** — planned use for evals + self-evolving layer |
| `graph.json` | 20.7 MB | Keep — primary graph output (stale, rebuild pending) |
| `notebooklm-py/tests/` (VCR cassettes) | 35 MB | **Candidate for removal** — these are the library developer's HTTP recordings, NOT user's runs; user's own interaction recording would need to be built separately |
| `notebooklm-py/.git/` | 26.7 MB | **Keep** — git history lets Claude read library evolution to understand capabilities/constraints |
| `Content-Hub-Vault-V2/10-Research/` PDFs + PNGs | ~55 MB | **Undecided** — slides.pdf (22 MB), slides_ruflo_focused.pdf (15 MB), ~10 PNG exports |
| `thinking/` (session JSONLs) | 7.7 MB | **Undecided** — auto-captured conversation transcripts, grows each session |

## Key Clarifications

- **`Design-doc/web/`**: Not V1 SaaS bloat as initially assessed — it IS the landing page being built for this system. See [[Webapp_sprint]].
- **graphify intermediates**: Kept intentionally for future eval pipeline and self-evolution layer. Modifies: [[graphify-out/GRAPH_REPORT.md]].
- **notebooklm-py VCR cassettes**: User's idea to use NotebookLM interaction recordings for pattern analysis and improvement is sound — but these specific files are the wrong recordings (library developer's test fixtures, not user's production runs). User's own recording infrastructure would need to be purpose-built.
- **notebooklm-py `.git`**: Retained as a knowledge source — Claude can read commit history to understand library design decisions and constraints. References: [[notebooklm-py]].

## Open Items

- [ ] Decide on `notebooklm-py/tests/` removal (35 MB) — only worth keeping if planning to patch the library itself
- [ ] Decide on `Content-Hub-Vault-V2/10-Research/` PDFs/PNGs (~55 MB)
- [ ] Decide on `thinking/` session JSONL retention policy

## Files Touched

None — audit only, no changes made.
