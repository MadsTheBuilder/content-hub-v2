---
name: resume-orchestration
description: Resume an in-flight orchestration produced by the /orchestrate skill after context compaction or a killed session. Use this whenever the user types /resume-orchestration or /resume, or says "resume the orchestration", "pick up the orchestration", "continue the last orchestration". Only triggers when an active state file exists in Content-Hub-Vault/00-Management/Orchestrations/. Do NOT use to start a new orchestration — that is /orchestrate.
user-invocable: true
---

# Resume Orchestration

You are resuming an orchestration that was started in a prior session. The original advisor wrote a state file to `Content-Hub-Vault/00-Management/Orchestrations/` before handing off for approval or before context compacted. Your job is to load that file, announce where we left off, confirm with the user, and continue the 6-phase workflow from the correct phase.

## Step 1: Announce

Say this immediately, before reading any file:

> "I'm resuming an orchestration. Let me find the active state file."

## Step 2: Find active state files

List files in `Content-Hub-Vault/00-Management/Orchestrations/` (excluding `README.md`). Read the frontmatter of each. Keep only files whose `status` is in `{awaiting-approval, approved, executing}`.

- **Zero active files**: respond "No active orchestrations found in `Content-Hub-Vault/00-Management/Orchestrations/`. If you want to start a new one, use `/orchestrate`." Stop.
- **One active file**: proceed with that file.
- **Multiple active files**: present the list to the user (slug, created date, status, current_group) and ask which one to resume. Stop until the user answers.

## Step 3: Load the workflow definition

Read `Content-Hub-Vault/00-Management/Superpowers/orchestrated-execution.md` fully. You need the Phase 4, 5, and 6 definitions to continue correctly. If the file is missing, stop and say:

> "I can't find the orchestrated-execution.md vault file. Please confirm the working directory."

## Step 4: Load AGENTS.md

Read `Content-Hub-Vault/00-Management/Plans/AGENTS.md`. You'll splice its specialist definitions into each saved agent prompt's `{SPECIALIST_DEFINITION}` placeholder before dispatching.

## Step 5: Summarise and confirm with user

Read the selected state file in full. Tell the user:

> "Resuming `<slug>`, created `<date>`, status `<status>`.
>  - Groups complete: `<groups_complete>`
>  - Current group: `<current_group>`
>  - Specialists involved: `<specialists_involved>`
>
>  Plan summary:
>  <one-line title for each task in the plan>
>
>  Based on status `<status>`, I'll resume at Phase `<N>`: `<phase name>`.
>  Proceed?"

Wait for user confirmation. Do not dispatch any agents or modify any files until the user confirms.

## Step 6: Resume at the correct phase

Based on the state file's `status` field:

### `status: awaiting-approval`
The original advisor wrote the plan but never got approval. Re-present the **Execution plan** section from the state file to the user exactly as written. Treat this as a fresh Phase 3. On approval, update the state file:
- `status: approved`
- Append to status log: `<ISO timestamp> approved (resumed)`

Then continue to Phase 4.

### `status: approved`
The user already approved the plan. Go directly to Phase 4. Update the state file before dispatching the first group:
- `status: executing`
- `current_group: 1` (or the first group number in the plan)
- Append to status log: `<ISO timestamp> phase 4 dispatch begin (resumed)`

Dispatch Group 1 per the saved Agent prompts (fill in `{SPECIALIST_DEFINITION}` placeholders from AGENTS.md).

### `status: executing`
Phase 4 was already in progress when the session ended. **Do not re-dispatch `current_group`** — its outcome is uncertain and re-running would duplicate file writes. Instead:
1. Ask the user: "Group `<current_group>` was in flight when the session ended. Should I assume it completed and continue from Group `<current_group + 1>`, or rollback and re-run Group `<current_group>`?"
2. **Default** (if the user says "continue"): move `current_group` into `groups_complete`, set `current_group: <current_group + 1>`, append to status log, dispatch the next group.
3. **Rollback** (if the user says "re-run"): the user is responsible for reverting any partial file changes from the stuck group before you dispatch. Once they confirm, re-dispatch the same group.

If `current_group` equals the highest group number in the plan, skip to Phase 6 verification.

## Step 7: Continue Phases 5 and 6 per the workflow file

Handle results (Phase 5) and verify (Phase 6) exactly as `orchestrated-execution.md` specifies. On Phase 6 close-out, set `status: complete` in the state file and append the final status-log line.

## The rule that applies throughout

Do not create, modify, or delete any file (other than the state file itself) until the user has confirmed the resume plan in Step 5. This is the same iron law as `/orchestrate` — resume is no different.

## If the state file is malformed

If the state file is missing required frontmatter fields, has an unknown `status`, or the Agent prompts section is empty, do not guess. Tell the user what's missing and ask whether to abandon the run (set `status: abandoned`) or to manually fix the file before retrying.