---
date: 2026-05-26
tags: [cleanup, maintenance, dead-weight, verification]
description: "Full dead-weight audit and cleanup of Content Hub V2 project root and vault. ~8 GB freed. All pipeline dependencies verified clean."
---

# 8 GB Shed — Dead Weight Audit & Cleanup

## Summary

Full meticulous audit of the V2 project root and vault. Every directory and file categorised as live pipeline, dead V1 remnant, or orphaned artifact. ~8 GB freed. All pipeline imports verified clean post-cleanup.

---

## What Was Removed

### Phase 1 — Storage Bombs (7.8 GB)

| Item | Size | Reason |
|------|------|--------|
| `.venv-tribe/` | 6,507 MB | TRIBE v2 fMRI project — marked FAILED in [[Current_Sprint]]; Windows hard-killed every run |
| `models/tribev2/best.ckpt` | 676 MB | TRIBE checkpoint file — same dead project |
| `.venv-py314-backup-20260522/` | 638 MB | Python 3.14 backup venv; `.venv` (3.12) is confirmed source of truth |

### Phase 2 — Orphaned Directories (175 MB)

| Item                          | Size   | Reason                                                                                    |
| ----------------------------- | ------ | ----------------------------------------------------------------------------------------- |
| `free-claude-code/`           | 122 MB | Cloned external Claude Code API project — zero connection to pipeline                     |
| `thinking/`                   | 45 MB  | 30 Claude session `.jsonl` debug traces from May 23–24 subagent runs                      |
| `tmp_marketingskills/`        | 2.7 MB | Cloned skills marketplace repo — not part of V2 pipeline                                  |
| `scratch/`                    | 3.3 MB | Old one-off experiment scripts (`notebooklm_research.py`, `notebooklm_retry_q2.py`, etc.) |
| `graphs/`                     | 3 MB   | Old graph output; active graph lives in `graphify-out/`                                   |
| `archive/`                    | 7.9 MB | Pre-NLM code snapshots, old yt_pipeline.md, experiment frames                             |
| `cache/`, `output/`, `tools/` | ~0 MB  | Empty or near-empty artifact dirs                                                         |
| `orchestrate-workspace/`      | 0.6 MB | Root-level duplicate of `.claude/skills/orchestrate-workspace/`                           |

### Phase 3 — Tool Artifacts & Loose Files

**Tool orchestration artifacts (no pipeline connection):**
`.claude-flow/`, `.hive-mind/`, `.swarm/`, `.agents/`, `.agent/`, `.claire/`, `.gsd/`, `.bg-shell/`, `claude-flow.config.json`

**V1 orphaned root scripts:**
`apify_live_test.py`, `checkpoint.py`, `copy_skills.py`, `debug_browser.py`, `push_trends_telegram.py`, `research_vault_optimization.py`, `setup_safe_hands.py`, `smoke_test.py`, `sync_vault.py`, `undo_changes.py`

**Dead test files:**
`test_claude_cli.py`, `test_claude_large_prompt.py`, `test_keys.py`

**V1 architecture diagrams:**
`GENERATION_TREE.excalidraw`, `MARKETING_SKILLS_INTEGRATION.excalidraw`, `TECHNICAL_FLOW.excalidraw`, `TECHNICAL_FLOW_FIXED.excalidraw`, `ux_flow.excalidraw`
 
**Orphaned log + config files:**
`dev_server.log`, `server.log`, `pipeline_eval.log`, `package-lock.json` (root-level), `local_agent_context.md`, `local_system_prompt.txt`

**V1 entry points:**
`run.py` (launched `backend.main:app` — deleted), `daily.py` (V1 "scrape → ideas → pick → script" runner, superseded by `skills/pipeline.py`)

**scripts/ V1 remnants:**
`scripts/twitter_scheduler.py`, `scripts/scrape_competitor_titles.py`

**Orphaned log:**
`logs/quality_check.log` (from deleted `backend/quality_check.py`)

### Phase 4 — V1 SaaS Backend & Vault Content

**Project root:**
`backend/` (0.8 MB) — full V1 FastAPI skeleton: `auth/`, `brand/`, `content/`, `intelligence/`, `research/`, `storage/`, `workflows/`. V2 pipeline imports exclusively from `skills/` — zero overlap.

**Vault V1 content (confirmed V1, user decision):**
- `Content-Hub-Vault-V2/Code-Brain/` — 347-file V1 Obsidian knowledge graph of SaaS architecture
- `Content-Hub-Vault-V2/backend/` — Obsidian `.md` mirrors of V1 Python files
- `Content-Hub-Vault-V2/frontend/` — V1 SaaS frontend notes
- `Content-Hub-Vault-V2/supabase/` — V1 DB config notes
- `Content-Hub-Vault-V2/00-Management/` — V1 management folder (parked since 2026-04-28 pivot)

### Twitter Ecosystem — Partial Removal

`skills/twitter_scout.py` and `skills/twitter_scorer.py` hard-imported `backend.database.get_supabase` and `backend.research.apify_client.scrape_twitter` — both V1 SaaS services, now deleted. Skill was non-functional.

Decision: **remove scout + scorer, keep Telegram credentials** (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` in `.env`). Twitter skill can be rebuilt as a V2-native tool when needed.

Removed: `skills/twitter_scout.py`, `skills/twitter_scorer.py`, `.claude/skills/twitter-scout/`

---

## Dead Import Fix — `skills/utils/ai.py`

`ai.py` imported `from backend.config import settings` for two env var reads. Fixed by replacing with direct `os.getenv()` calls:

```python
# Before
from backend.config import settings
settings.google_ai_studio_key   →   os.getenv("GOOGLE_AI_STUDIO_KEY", "")
settings.nvidia_nim_api_key     →   os.getenv("NVIDIA_NIM_API_KEY", "")
```

Added `import os` + `from dotenv import load_dotenv` + `load_dotenv(PROJECT_ROOT / ".env")`. All other pipeline skills were clean.

---

## Verification Results

| Check | Status |
|-------|--------|
| `skills/*.py` — all 15 pipeline files present | ✅ |
| `prompts/*.md` — all 10 prompt files present | ✅ |
| `.claude/skills/*/SKILL.md` — 16/16 present (pipeline dir has none by design) | ✅ |
| Dead imports in `skills/` | ✅ CLEAN |
| Dead imports in `Design-doc/server/` | ✅ CLEAN |
| `.venv` key packages: anthropic 0.39, fastapi 0.136, httpx 0.27, playwright 1.48, streamlit 1.57, uvicorn 0.30 | ✅ |
| `Design-doc/` webapp: 13 JSX + 5 server Python files intact | ✅ |
| `notebooklm-py/` intact | ✅ |
| `vault/00-Management-V2/` structure intact | ✅ |
| `.claude/settings.json` valid JSON | ✅ |
| Vault output folders have content (05–12) | ✅ |

---

## Final Project Root State

```
Content Hub V2/
├── .claude/          ← skills, settings, hooks
├── .github/
├── .venv/            ← Python 3.12.10 (source of truth)
├── .vscode/
├── Content-Hub-Vault-V2/
├── Design-doc/       ← active webapp sprint (Phase 7 pending)
├── docs/
├── graphify-out/     ← knowledge graph
├── logs/             ← empty, ready for pipeline logs
├── notebooklm-py/    ← research integration
├── prompts/          ← 10 pipeline prompt files
├── scripts/          ← empty (V1 scripts removed)
├── skills/           ← 15 pipeline Python files
├── tests/
├── AGENTS.md, CLAUDE.md, .env, requirements.txt, pytest.ini
└── control_room.py, run_skill.py, vault_index.py, runner.py, run_control_room.bat, extract_video_knowledge.py
```

---

## Total Freed

| Category | Approx. Size |
|----------|-------------|
| `.venv-tribe` + `models/` + backup venv | ~7,820 MB |
| `free-claude-code` + `thinking` + other dirs | ~175 MB |
| Loose files, V1 backend, vault V1 content | ~5 MB |
| **Total** | **~8,000 MB (~8 GB)** |

---

Modifies: [[skills/utils/ai.py]]
Implements: Phase 0 Cleanup (long-deferred from [[Local_First_Skill_Engine_Plan]])
References: [[Current_Sprint]], [[2026-04-28_V2_Pivot_Local_First_Engine]]
