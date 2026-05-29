---
date: 2026-05-10
type: session-log
task: Full audit of local-first skill engine
skills_audited: 9 core + 5 unclear
---

# Skill Engine Audit — 2026-05-10

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[Current_Sprint]]

## What was done

Full three-layer audit of all skills in the system. Inspected `skills/*.py`, `prompts/*.md`, `.claude/skills/*/SKILL.md`, and shared utilities (`skills/utils/ai.py`, `skills/utils/vault.py`).

## Files inspected

- `skills/` — 15 .py files
- `prompts/` — 10 .md files
- `.claude/skills/` — 15 SKILL.md files
- `skills/utils/ai.py`, `skills/utils/vault.py`

## Key findings

### Core 9 skills — all 3 layers present

All 9 (researcher, cascade, short_form, yt_pipeline, ideation, voice_cleanup, hook, outline, title) have complete 3-layer stacks. Quality issues flagged below.

### Quality issues in core skills

1. **cascade.py + short_form.py**: `extract_transcript()` is copy-pasted (42 lines identical). Should live in `skills/utils/transcript.py`.
2. **yt_pipeline.py**: Uses subprocess CLI for NotebookLM while `researcher.py` uses the Python async API — two integration patterns for the same service.
3. **title.py**: Calls `subprocess.run("claude -p -", shell=True)` instead of `skills.utils.ai`. Has its own `find_project_root()` function instead of the standard `Path(__file__).parent.parent` pattern.

### Unclear skills verdict

| File | Verdict |
|------|---------|
| `twitter_scout.py` | Real skill — no AI generation, so no prompt layer needed. SKILL.md is good. |
| `twitter_scorer.py` | Utility module, not a skill — pure math functions used by twitter_scout. Correct. |
| `hook_writer.py` | **Dead weight** — superseded by separate hook.py + outline.py. Hardcodes prompts inline, writes to `output/` (not vault), uses vault.py which points to V1 paths. |
| `research_sources.py` | Internal module — used by yt_pipeline. Not a standalone skill. Correct. |
| `research_plan.py` | Internal module — used by yt_pipeline. Not a standalone skill. Correct. |

### Orphaned utility

`skills/utils/vault.py` — points to V1 vault path (`Content-Hub-Vault/Exoskeleton`). Only used by `hook_writer.py`. Both are dead weight in V2.

## Open items

- [ ] Extract `extract_transcript()` to shared util (cascade + short_form)
- [ ] Migrate title.py to use `skills.utils.ai` instead of shell subprocess
- [ ] Delete `hook_writer.py` and `skills/utils/vault.py` (V1 artifacts)
