---
date: 2026-06-01
tags: [session, researcher, open-notebook]
description: "Research run on Imbad0202/academic-research-skills (25K stars, 685/day) via open-notebook backend. Brief written. Two known RC failures (context timeout, seed JSON)."
---

# Session Log — Academic Research Skills Research Run

## What Happened

Ran `/researcher` on `Imbad0202/academic-research-skills` via the open-notebook backend.

- **Niche**: research
- **Repo**: https://github.com/Imbad0202/academic-research-skills
- **Stars**: 25,061 | **Velocity**: 685.8/day
- **Notebook**: `notebook:87i0xqztmfpgrpmujj0e`
- **Brief**: [[10-Research/2026-06-01_research_academic-research-skills_brief]]

## Sources Indexed

7 primary docs: README, CONTRIBUTING.md, docs/ARCHITECTURE.md, docs/PERFORMANCE.md, docs/PERFORMANCE.zh-TW.md, docs/SETUP.md, docs/SETUP.zh-TW.md

## Known Issues (same as [[2026-06-01_CloakBrowser-Research-Notebook-Audit]])

- `extract_repo_context` timed out (Claude CLI 60s limit) — returned empty `RepoContext`
- `seed_questions_from_context` failed (empty JSON parse) — fell back to default questions
- All 6 chat questions answered successfully despite fallbacks

## Suggested Video Angle

*"How to Turn Claude Code Into a Research Machine (Real Repo, 25K Stars)"*

Architecture pattern mirrors [[Content Hub V2]] exactly — strong content fit.

## Next Step

Run `/ideation research` to generate ranked video ideas from this brief.
