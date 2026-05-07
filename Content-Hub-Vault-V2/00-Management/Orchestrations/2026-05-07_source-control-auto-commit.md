---
slug: source-control-auto-commit
created: 2026-05-07
status: complete
current_group: null
groups_complete: [1, 2]
specialists_involved: [git-workflow-agent, test-quality-agent, vault-config-agent, scheduler-orchestration-agent]
---

# Orchestration: Source Control Auto-Commit System

## Recon Summary

- **Current safe hands pattern**: checkpoint.py (pre-work) + undo_changes.py (post-work) provides manual rollback guardrails
- **Daily workflow entry**: daily.py orchestrates 4 async steps (research, ideas, script, cascade); manual trigger only
- **Vault as state**: sync_vault.py captures Python/TS/SQL summaries; outputs to Content-Hub-Vault-V2 with mtime-based deduplication
- **Test infrastructure ready**: pytest + conftest.py with autouse fixtures enforces mock mode (no real API/DB calls)
- **Scheduler infrastructure**: APScheduler imported in backend/main.py but not yet wired; ready for activation
- **Change types**: Vault outputs (04-Trends, 05-Hooks, 06-Outlines, 07-Titles, 08-Distribution), config (.env.example), test logs
- **Database gap**: Supabase schema changes manual (no local migration files); auto-commit scope is **files only**, not data
- **No CI/CD yet**: No GitHub Actions; git has 2 commits, single master branch, no branch protection

## Execution Plan

**Tasks:** 4 across 2 groups  
**Specialists:** git-workflow, test-quality, vault-config, scheduler-orchestration  
**Models:** Haiku (all tasks are EASY — mechanical setup, no complex logic)

### Group 1 (parallel, foundational)

- [git-workflow-agent | EASY] Create Git Workflow Manager module
  Files: Create `backend/git_manager.py`
  Context: Read `checkpoint.py`, `undo_changes.py`, `daily.py`, `.gitignore`
  Criteria:
    1. Module exports `GitManager` class with methods: `stage_files(patterns)`, `commit(message, author)`, `get_status()`, `get_staged_changes()`
    2. Uses `GitPython` library (add to requirements.txt if missing)
    3. Handles commit author as "Claude + {user}" (co-authored)
    4. Validates .gitignore patterns (doesn't stage secrets)
    5. Returns commit hash on success

- [test-quality-agent | EASY] Create Test & Quality Validator module
  Files: Create `backend/quality_check.py`
  Context: Read `backend/tests/conftest.py`, `requirements.txt`, pytest.ini
  Criteria:
    1. Module exports `QualityValidator` class with method: `run_checks()` → dict with `tests_passed`, `test_count`, `lint_errors`, `type_errors`
    2. Runs `pytest backend/tests/ --tb=short` and captures exit code + summary
    3. Integrates basic linting: `ruff check backend/` (add ruff to requirements.txt)
    4. Type checking: `mypy backend/` (add mypy to requirements.txt)
    5. Returns `True` if all pass, `False` if any fail; logs details to stdout
    6. Blocks commit in calling code if checks fail

### Group 2 (parallel, depends on Group 1)

- [vault-config-agent | EASY] Enhance Vault Sync & Config Validator
  Files: Modify `sync_vault.py`, modify `checkpoint.py`
  Context: Read `sync_vault.py`, `checkpoint.py`, `.env.example`, `CLAUDE.md`
  Criteria:
    1. Update `sync_vault.py`: add `track_commit()` method that records commit hash in synced file frontmatter (e.g., `synced_at_commit: <hash>`)
    2. Update `checkpoint.py`: after git commit, call `sync_vault.track_commit(hash)` to mark vault state with commit reference
    3. Validate `.env.example` consistency: check all `backend/config.py` env var references exist in `.env.example` as keys
    4. Add config validation to `QualityValidator` pipeline (test agent calls this)
    5. Return `commit_tracked: bool`, `config_valid: bool`

- [scheduler-orchestration-agent | EASY] Wire APScheduler & Update Daily Workflow
  Files: Modify `backend/main.py`, modify `daily.py`
  Context: Read `backend/main.py`, `daily.py`, `github_trending.py`
  Criteria:
    1. In `backend/main.py`: Activate APScheduler in lifespan context manager (currently imported but unused)
    2. Add scheduled job: "daily-auto-commit" at 6am local time
    3. Job should call new function `auto_commit_daily()` → runs vault sync, quality checks, stages + commits vault changes
    4. Update `daily.py`: after each step (research, ideas, script, cascade), call auto-commit-safe checkpoint (don't commit yet, just mark dirty)
    5. Return list of scheduled jobs and next run times
    6. Ensure `/on-demand` CLI flag in daily.py for manual trigger: `python daily.py --auto-commit` runs full suite

## Agent Prompts

### Task: git-workflow-agent: Create Git Workflow Manager module

- description: "git-workflow-agent: Create Git Workflow Manager module"
- model: haiku
- prompt: |
    You are the Git Workflow Agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new Python module `backend/git_manager.py` that abstracts all git operations needed for the auto-commit system. This module will be the single source of truth for staging, committing, and checking git status.

    ## Scope
    Read for context: checkpoint.py, undo_changes.py, daily.py, .gitignore
    Create: backend/git_manager.py
    Modify: requirements.txt (add GitPython if not present)

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. Module exports `GitManager` class
    2. Methods exist and work:
       - `stage_files(patterns: list[str])` → stages files matching glob patterns, respects .gitignore
       - `commit(message: str, author: str = "Claude")` → commits staged changes, returns commit hash
       - `get_status()` → returns dict with staged/unstaged/untracked file counts
       - `get_staged_changes()` → returns list of staged file paths
    3. Commit author format: "Claude + {user}" or "Claude" (co-authored style)
    4. Uses GitPython library; add to requirements.txt if missing
    5. Handles git errors gracefully (raises ValueError with clear messages)
    6. No hardcoded paths — uses relative paths or config

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of the GitManager API and any decisions you made about error handling or path resolution.

### Task: test-quality-agent: Create Test & Quality Validator module

- description: "test-quality-agent: Create Test & Quality Validator module"
- model: haiku
- prompt: |
    You are the Test & Quality Agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Create a new Python module `backend/quality_check.py` that runs tests, linting, and type checks, then reports results. This module will be called before every auto-commit to ensure code quality gates pass.

    ## Scope
    Read for context: backend/tests/conftest.py, requirements.txt, pytest.ini
    Create: backend/quality_check.py
    Modify: requirements.txt (add ruff and mypy if not present)

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. Module exports `QualityValidator` class with method `run_checks(verbose: bool = False)` → returns dict
    2. `run_checks()` output dict keys: `tests_passed` (bool), `test_count` (int), `test_output` (str), `lint_errors` (int), `type_errors` (int)
    3. Runs `pytest backend/tests/ --tb=short` and captures exit code
    4. Runs `ruff check backend/` and counts errors
    5. Runs `mypy backend/ --ignore-missing-imports` and counts errors
    6. If verbose=True, prints full output to stdout; else logs to file `logs/quality_check.log`
    7. Returns `True` if all checks pass (tests pass AND lint count==0 AND type count==0), `False` otherwise
    8. Add ruff and mypy to requirements.txt

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of the QualityValidator API and which tool failures would block a commit.

### Task: vault-config-agent: Enhance Vault Sync & Config Validator

- description: "vault-config-agent: Enhance Vault Sync & Config Validator"
- model: haiku
- prompt: |
    You are the Vault & Config Agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Enhance sync_vault.py to track which commit each synced file corresponds to, and add config validation to ensure .env.example stays in sync with backend/config.py.

    ## Scope
    Read for context: sync_vault.py, checkpoint.py, .env.example, backend/config.py, CLAUDE.md
    Modify: sync_vault.py, checkpoint.py

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. Add method to sync_vault.py: `track_commit(commit_hash: str)` → updates frontmatter of all recently synced files with `synced_at_commit: {hash}` and `synced_at_time: {timestamp}`
    2. Update checkpoint.py: after git commit, call sync_vault.track_commit(commit_hash) to mark vault files
    3. Add config validation: scan backend/config.py for `os.getenv("KEY")` calls and verify each KEY exists in .env.example as a documented key
    4. Create function `validate_config()` → returns dict with `config_valid: bool`, `missing_keys: list[str]`, `extra_keys: list[str]`
    5. If config validation fails, log warnings but don't block (auto-commit can proceed with warning)

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of the vault tracking feature and config validation rules.

### Task: scheduler-orchestration-agent: Wire APScheduler & Update Daily Workflow

- description: "scheduler-orchestration-agent: Wire APScheduler & Update Daily Workflow"
- model: haiku
- prompt: |
    You are the Scheduler & Orchestration Agent for the Content Hub project.

    {SPECIALIST_DEFINITION}

    ## Your Task
    Activate the APScheduler infrastructure in backend/main.py and update daily.py to integrate with the auto-commit system. Create a daily auto-commit job that runs at 6am and handles vault sync + quality checks + commit.

    ## Scope
    Read for context: backend/main.py, daily.py, github_trending.py, backend/database.py
    Modify: backend/main.py, daily.py

    IMPORTANT: Only touch the files listed above. Other agents are working on other files in parallel. Modifying anything outside your scope WILL cause conflicts.

    ## Acceptance Criteria
    1. In backend/main.py: Activate APScheduler in the lifespan context manager
    2. Add job: "daily-auto-commit" scheduled for 6:00 AM every day
    3. Job function: runs vault sync (sync_vault.py), quality checks (quality_check.py), stages vault changes, commits if all checks pass
    4. Job function returns dict with `job_name`, `next_run_time`, `last_run_time`, `commit_hash` (or None if skipped)
    5. Update daily.py: add `--auto-commit` CLI flag that manually triggers the full auto-commit pipeline
    6. Update daily.py: add `--check-only` flag that runs quality checks but doesn't commit (dry-run)
    7. Ensure scheduler logs all job executions to `logs/scheduler.log`
    8. Return list of all scheduled jobs with next run times

    ## When done
    Report your status:
    - DONE: All criteria met
    - DONE_WITH_CONCERNS: Complete but you have doubts (explain)
    - STUCK: Cannot proceed (explain what blocks you)
    - NEEDS_CONTEXT: Need information not provided (specify what)

    Include a summary of the scheduled jobs, CLI flags added, and next run times.

## Status Log
- 2026-05-07 12:15 created, status=awaiting-approval
- 2026-05-07 12:25 approved by user
- 2026-05-07 12:27 executing, dispatched Group 1 (git-workflow-agent, test-quality-agent)
- 2026-05-07 12:35 Group 1 complete, dispatched Group 2 (vault-config-agent, scheduler-orchestration-agent)
- 2026-05-07 12:45 Group 2 complete, all 4 agents DONE
- 2026-05-07 12:50 verification complete, status=complete
