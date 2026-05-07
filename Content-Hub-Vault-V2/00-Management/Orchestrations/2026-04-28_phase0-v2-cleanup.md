---
slug: phase0-v2-cleanup
created: 2026-04-28
status: complete
current_group: null
groups_complete: [1, 2, 3]
specialists_involved: [general-purpose]
---

# Orchestration: Phase 0 — V2 Cleanup & Foundation

## Recon summary

- V2 is not a git repo (no `.git` at root) — `git rm` commands skipped; will `git init` at end
- `Content-Hub-Vault/00-Management-V2/` in V2 contains only `Sessions/session_log_2026_04_28.md`; full structure lives in V1 at `Content Hub/Content-Hub-Vault/00-Management-V2/`
- V1 has 9 files to copy: Memory/context.md, Plans/CLAUDE.md, Plans/Local_First_Skill_Engine_Plan.md, Tasks/Current_Sprint.md, Orchestrations/README.md, Program-Architecture/README.md, Sessions/README.md, Superpowers/README.md, README.md
- `remotion-service/` already gone; all 4 renderer files (renderer_video.py, renderer_slides.py, renderer_talking_head.py, storyboard.py) already deleted — skip those Phase 0 items
- `frontend/` and `supabase/` confirmed present — to be deleted
- `backend/experiments/` has `__init__.py`, `models.py`, `router.py` — archive rather than delete
- `tmp/` confirmed present — archive
- `skills/` already exists at V2 root; only `prompts/` and vault content folders need creating
- Root `CLAUDE.md` is V1-era (references `00-Management/` paths) — needs V2 path updates

## Execution plan

**Tasks:** 6 across 3 groups
**Specialists:** general-purpose agents (Phase 0 is filesystem/config restructuring, not feature development)

### Group 1 — parallel (independent setup)

- [general | EASY] **Task A: Copy vault structure**
  Source: `c:\Users\madhu\Claude cowork\Content Hub\Content-Hub-Vault\00-Management-V2\`
  Destination: `c:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault\00-Management-V2\`
  Files: Memory/context.md, Plans/CLAUDE.md, Plans/Local_First_Skill_Engine_Plan.md, Tasks/Current_Sprint.md, Orchestrations/README.md, Program-Architecture/README.md, Sessions/README.md, Superpowers/README.md, README.md
  Criteria: All 9 files exist in V2 vault; existing Sessions/session_log_2026_04_28.md preserved

- [general | EASY] **Task B: Delete SaaS directories**
  Delete: `frontend/`, `supabase/`
  Criteria: Both directories gone from V2 root

- [general | EASY] **Task C: Archive experiments and tmp**
  Create `archive/`, move `backend/experiments/` → `archive/experiments/`, move `tmp/` → `archive/tmp/`
  Criteria: `archive/experiments/` and `archive/tmp/` exist; originals are gone

### Group 2 — parallel (depends on Group 1)

- [general | EASY] **Task D: Create V2 folder structure**
  Create: `prompts/`, `Content-Hub-Vault/01-Knowledge/`, `05-Hooks/`, `06-Outlines/`, `07-Titles/`, `08-Distribution/`, `09-Shorts/`, `10-Research/` (each with `.gitkeep`)
  Criteria: All 8 folders exist with .gitkeep files

- [general | MEDIUM] **Task E: Update root CLAUDE.md**
  Update `CLAUDE.md` at V2 root: change § 6 Session Start Protocol and § 10 Project Knowledge to use `00-Management-V2/` paths; replace graphify step with Local_First_Skill_Engine_Plan step; update § 7 session log path; update header to reflect V2 local-first framing
  Criteria: Root CLAUDE.md references `00-Management-V2/` throughout; no stale V1-only references remain

### Group 3 — sequential (depends on Groups 1+2)

- [general | MEDIUM] **Task F: Finalize — mark complete, log, git init, commit**
  1. Mark all Phase 0 items `[x]` in `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md`; update status line to `✅ Complete`
  2. Write session log to `Content-Hub-Vault/00-Management-V2/Sessions/2026-04-28_Phase0_Cleanup.md`
  3. `git init` at V2 root; create `.gitignore` (exclude `__pycache__`, `.env`, `node_modules`, `*.pyc`, `.pytest_cache`, `archive/`)
  4. `git add .` and `git commit -m "Strip SaaS layers; restructure as local-first skill engine"`
  Criteria: Phase 0 shows ✅ in Current_Sprint.md; session log exists; `git log` shows 1 commit

## Agent prompts

### Task A: Copy vault structure

- description: "vault-copier: copy 00-Management-V2 from V1 to V2"
- model: haiku
- prompt: |
    You are a filesystem agent for the Content Hub project.

    ## Your Task
    Copy the full 00-Management-V2 vault structure from Content Hub V1 into Content Hub V2.

    ## Scope
    Read from: `c:\Users\madhu\Claude cowork\Content Hub\Content-Hub-Vault\00-Management-V2\` (all files)
    Write to: `c:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault\00-Management-V2\`
    Do NOT overwrite: `Sessions/session_log_2026_04_28.md` (already exists in V2, preserve it)

    Files to copy (read source, write to destination with same relative path):
    - Memory/context.md
    - Plans/CLAUDE.md
    - Plans/Local_First_Skill_Engine_Plan.md
    - Tasks/Current_Sprint.md
    - Orchestrations/README.md
    - Program-Architecture/README.md
    - Sessions/README.md
    - Superpowers/README.md
    - README.md

    Use the Read tool on each source file, then Write to the destination path.
    Create parent directories as needed (the Write tool creates them automatically).

    ## Acceptance Criteria
    1. All 9 files exist in V2's `Content-Hub-Vault/00-Management-V2/`
    2. `Sessions/session_log_2026_04_28.md` still exists in V2 (not overwritten)
    3. No files from V1 are modified

    ## When done
    Report DONE with a list of files written.

### Task B: Delete SaaS directories

- description: "saas-stripper: delete frontend and supabase from V2"
- model: haiku
- prompt: |
    You are a filesystem cleanup agent for the Content Hub project.

    ## Your Task
    Delete the SaaS-layer directories from Content Hub V2. V2 is pivoting to a local-first engine with no frontend or Supabase.

    ## Scope
    Working directory: `c:\Users\madhu\Claude cowork\Content Hub V2\`
    Delete: `frontend/` (entire directory tree)
    Delete: `supabase/` (entire directory tree)
    Skip: `remotion-service/` (already gone — confirm, don't error)

    Use Bash with `rm -rf` on Windows paths (use forward slashes or quote paths with spaces).

    ## Acceptance Criteria
    1. `frontend/` does not exist in V2 root
    2. `supabase/` does not exist in V2 root

    ## When done
    Report DONE confirming both directories are gone.

### Task C: Archive experiments and tmp

- description: "archiver: move experiments and tmp to archive/"
- model: haiku
- prompt: |
    You are a filesystem archiver agent for the Content Hub project.

    ## Your Task
    Move `backend/experiments/` and `tmp/` into an `archive/` directory to preserve them without keeping them in the active codebase.

    ## Scope
    Working directory: `c:\Users\madhu\Claude cowork\Content Hub V2\`
    Create: `archive/`
    Move: `backend/experiments/` → `archive/experiments/`
    Move: `tmp/` → `archive/tmp/`

    Use Bash `mkdir -p archive && mv backend/experiments archive/experiments && mv tmp archive/tmp`

    ## Acceptance Criteria
    1. `archive/experiments/` exists with __init__.py, models.py, router.py
    2. `archive/tmp/` exists
    3. `backend/experiments/` does not exist
    4. `tmp/` does not exist at V2 root

    ## When done
    Report DONE confirming moves completed.

### Task D: Create V2 folder structure

- description: "folder-creator: create prompts/ and vault content folders"
- model: haiku
- prompt: |
    You are a project structure agent for the Content Hub V2 project.

    ## Your Task
    Create the new local-first skill engine folder structure. `skills/` already exists — skip it. Create all others with a `.gitkeep` file so git tracks them.

    ## Scope
    Working directory: `c:\Users\madhu\Claude cowork\Content Hub V2\`
    Create these folders (each with a `.gitkeep` file):
    - `prompts/`
    - `Content-Hub-Vault/01-Knowledge/`
    - `Content-Hub-Vault/05-Hooks/`
    - `Content-Hub-Vault/06-Outlines/`
    - `Content-Hub-Vault/07-Titles/`
    - `Content-Hub-Vault/08-Distribution/`
    - `Content-Hub-Vault/09-Shorts/`
    - `Content-Hub-Vault/10-Research/`

    Use Write tool to create `<folder>/.gitkeep` with empty content for each.

    ## Acceptance Criteria
    1. All 8 folders exist
    2. Each has a `.gitkeep` file

    ## When done
    Report DONE with list of folders created.

### Task E: Update root CLAUDE.md

- description: "claude-md-updater: update root CLAUDE.md to V2 framing"
- model: sonnet
- prompt: |
    You are a configuration agent for the Content Hub V2 project.

    ## Your Task
    Update the root `CLAUDE.md` at `c:\Users\madhu\Claude cowork\Content Hub V2\CLAUDE.md` to reflect V2's local-first engine framing. The file currently references V1 paths (`00-Management/`) and SaaS concepts. Update it to V2.

    ## Scope
    Read: `c:\Users\madhu\Claude cowork\Content Hub V2\CLAUDE.md` (current V1-era file)
    Read: `c:\Users\madhu\Claude cowork\Content Hub V2\Content-Hub-Vault\00-Management-V2\Plans\CLAUDE.md` (V2 reference)
    Modify: `c:\Users\madhu\Claude cowork\Content Hub V2\CLAUDE.md`

    ## What to change

    **Header:** Add subtitle "Content Hub V2 — Local-First Skill Engine" under the main title.

    **§ 6 Session Start Protocol** — replace all 6 steps with:
    1. Read `Content-Hub-Vault/00-Management-V2/Memory/context.md` (project context)
    2. Read `Content-Hub-Vault/00-Management-V2/Plans/CLAUDE.md` (V2 rules and stack)
    3. Read `Content-Hub-Vault/00-Management-V2/Plans/Local_First_Skill_Engine_Plan.md` (full build plan)
    4. Read `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md` (what to do next)
    5. Plan before acting — ask 1–3 focused questions if anything is ambiguous, then wait.
    6. Load `.claude/skills/<name>/SKILL.md` only when acting on a matching skill task.

    **§ 7 Vault Knowledge Graph** — change session log path from `Content-Hub-Vault/00-Management/Sessions/` to `Content-Hub-Vault/00-Management-V2/Sessions/`. Change WikiLinks note to say "Update `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md`".

    **§ 9 Orchestration** — change state file path from `Content-Hub-Vault/00-Management/Orchestrations/` to `Content-Hub-Vault/00-Management-V2/Orchestrations/`.

    **§ 10 Project Knowledge** table — replace with:
    | What | Where |
    |------|-------|
    | Stack, architecture, decisions | `Content-Hub-Vault/00-Management-V2/Memory/context.md` |
    | Full build plan | `Content-Hub-Vault/00-Management-V2/Plans/Local_First_Skill_Engine_Plan.md` |
    | Active sprint | `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md` |
    | V2 session history | `Content-Hub-Vault/00-Management-V2/Sessions/` |
    | Agent roles | `AGENTS.md` (project root) |
    | V1 (parked) reference | `Content-Hub-Vault/00-Management/` |

    Keep all behavioral guardrails (§1–§5, §8) unchanged — they are still valid for V2.

    ## Acceptance Criteria
    1. No references to `00-Management/` (without -V2) remain in the session/log/orchestration sections
    2. § 6 Session Start Protocol uses `00-Management-V2/` paths
    3. § 10 table reflects V2 structure
    4. Behavioral guardrails §1–§5 and §8 are unchanged

    ## When done
    Report DONE with a summary of sections changed.

### Task F: Finalize

- description: "finalizer: mark Phase 0 complete, write session log, git init, commit"
- model: sonnet
- prompt: |
    You are the finalizer agent for the Content Hub V2 Phase 0 orchestration.

    ## Your Task
    Complete the Phase 0 orchestration by: marking tasks complete, writing the session log, initializing git, and making the first commit.

    ## Scope
    Working directory: `c:\Users\madhu\Claude cowork\Content Hub V2\`
    Modify: `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md`
    Create: `Content-Hub-Vault/00-Management-V2/Sessions/2026-04-28_Phase0_Cleanup.md`
    Create: `.gitignore`
    Run: `git init`, `git add`, `git commit`

    ## Steps

    ### 1. Mark Phase 0 complete in Current_Sprint.md
    Read the file and update:
    - Change `- **Phase 0 (Cleanup):** 🟡 Not started` to `- **Phase 0 (Cleanup):** ✅ Complete`
    - Mark all Phase 0 checkbox items as `[x]` (the ones that were `[ ]`)
    - Note that remotion-service and 4 renderer files were skipped (already gone)

    ### 2. Write session log
    Create `Content-Hub-Vault/00-Management-V2/Sessions/2026-04-28_Phase0_Cleanup.md` with:
    ```
    ---
    status: Completed
    date: 2026-04-28
    type: session_summary
    ---
    # Session: Phase 0 — V2 Cleanup & Foundation

    Implements: [[Current_Sprint]] Phase 0
    References: [[Local_First_Skill_Engine_Plan]] | [[context]]

    ## What Was Done
    - Copied full [[00-Management-V2]] vault structure from V1 to V2 (Memory, Plans, Tasks, Orchestrations, Program-Architecture, Superpowers)
    - Deleted `frontend/` and `supabase/` (SaaS layers removed)
    - Archived `backend/experiments/` → `archive/experiments/` and `tmp/` → `archive/tmp/`
    - Created V2 content folder structure: `prompts/`, `01-Knowledge/`, `05-Hooks/`, `06-Outlines/`, `07-Titles/`, `08-Distribution/`, `09-Shorts/`, `10-Research/`
    - Updated root [[CLAUDE.md]] to V2 local-first framing (00-Management-V2/ paths)
    - Initialized git repo; made initial commit

    ## Skipped (Already Done)
    - `remotion-service/` — already absent
    - `renderer_video.py`, `renderer_slides.py`, `renderer_talking_head.py`, `storyboard.py` — already deleted

    ## Files Changed
    - `Content-Hub-Vault/00-Management-V2/` — full structure created
    - `CLAUDE.md` — updated to V2 framing
    - `archive/` — created with experiments and tmp

    ## Outstanding
    - Phase 1 (Infrastructure): build `skills/runner.py`
    - Phase 2 (Callaway Masterclass): blocked on user-provided URLs
    ```

    ### 3. Create .gitignore
    Create `.gitignore` with:
    ```
    __pycache__/
    *.pyc
    *.pyo
    .env
    .env.local
    node_modules/
    .pytest_cache/
    .next/
    dist/
    build/
    *.egg-info/
    .DS_Store
    archive/
    ```

    ### 4. Git init and commit
    ```bash
    cd "c:/Users/madhu/Claude cowork/Content Hub V2"
    git init
    git add .
    git commit -m "Strip SaaS layers; restructure as local-first skill engine"
    ```

    ## Acceptance Criteria
    1. Phase 0 status is `✅ Complete` in Current_Sprint.md
    2. All Phase 0 items are `[x]`
    3. Session log exists at `Content-Hub-Vault/00-Management-V2/Sessions/2026-04-28_Phase0_Cleanup.md`
    4. `.gitignore` exists
    5. `git log` shows 1 commit with message "Strip SaaS layers; restructure as local-first skill engine"

    ## When done
    Report DONE with git log output confirming the commit.

## Status log
- 2026-04-28 created, status=awaiting-approval
- 2026-04-28T00:00Z approved (resumed)
- 2026-04-28T00:00Z phase 4 dispatch begin, group 1
- 2026-04-28T00:00Z group 1 complete (vault copy, frontend/supabase delete, archive)
- 2026-04-28T00:00Z group 2 complete (folder creation, CLAUDE.md update)
- 2026-04-28T00:00Z group 3 complete (sprint marked, session log, git init + commit 814161b)
- 2026-04-28T00:00Z phase 6 verified, status=complete
