---
date: 2026-05-13
type: session-log
topic: Researcher skill — source verification agent implementation
status: complete
files_modified:
  - skills/researcher.py
---

# Session Log — Researcher Source Verification Agent

Implements: [[2026-05-13_Researcher_Source_Quality_Handoff]]
Modifies: [[researcher.py]]

---

## What Changed

Completed the revert + rebuild described in the handoff document.

### Reverted (wrong approach)

Removed `_repo_keywords()` and `_is_relevant_source()` — the keyword-based source filter that dropped legitimately relevant sources not naming the repo explicitly (e.g., an Anthropic article about the Mythos model would have been dropped for `kyegomez/OpenMythos`).

Replaced the filtering import block with simple import that captures `imported_source_ids` from `research.import_sources()` return value.

### Built (verification agent)

After the 75s indexing wait, `research_one()` now runs a verification pass:

1. `sources.list(nb.id)` — fetch all sources in the notebook
2. Partition into `primary_ids` (repo URL + README, always kept) vs `discovered_sources` (web research results, must be verified)
3. `sources.get_guide(nb.id, src.id)` per discovered source — get AI-generated summary + keywords
4. One `AsyncAnthropic().messages.create()` call to `claude-haiku-4-5-20251001` with all guide summaries batched, using `keep_sources` tool-use for deterministic ID extraction
5. `verified_source_ids` = primary_ids + kept discovered IDs

All `chat.ask()` calls (8 research questions + 3 angle battery) now pass `source_ids=verified_source_ids`.

### Also added

`import anthropic` at the top of the file.

---

## Design Decisions

- **Option A (Claude API)** chosen for verification — `anthropic==0.39.0` confirmed in `requirements.txt`
- **`AsyncAnthropic()`** not `Anthropic()` — avoids blocking the event loop inside the async pipeline
- **Tool-use** (`keep_sources`) — deterministic ID extraction, no regex fragility
- **Batch call** — one Claude call with all sources, not one call per source
- **Non-destructive** — sources are never deleted; `source_ids=` limits LLM scope without removing anything
- **Graceful degradation**: `get_guide()` failures → source kept (skipped_ids); Claude call failure → all discovered kept; no tool result → all discovered kept
- **Empty-result log** — prints message when all discovered sources are dropped, so it's visible in output

---

## Files Touched

- `skills/researcher.py` — all changes in this file; `research_one()` function, module imports

---

## Verified State

File reviewed in full at completion. Pipeline flow:
```
create notebook
→ add repo URL + README (primary sources)
→ web research → poll → import all (no filter)
→ sleep 75s
→ sources.list() → partition primary / discovered
→ get_guide() per discovered source
→ Claude Haiku: keep_sources tool call (batch)
→ verified_source_ids = primary + kept
→ chat.configure() custom_prompt
→ 8 research questions (source_ids=verified)
→ 3 angle battery questions (source_ids=verified)
→ compile brief
```

---

## Related

- Handoff: [[2026-05-13_Researcher_Source_Quality_Handoff]]
- Sprint: [[Current_Sprint]]
- Smoke test that motivated this: `Content-Hub-Vault-V2/10-Research/2026-05-12_ai-agents_brief.md`
