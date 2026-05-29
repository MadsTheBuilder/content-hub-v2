# Session: Researcher Fix — Individual Questions Pattern Verified
*2026-05-08*

Implements: [[Research Guardrails]]
References: [[2026-05-08_Guardrails_Reverification]]
Modifies: [[skills/researcher.py]]

---

## Objective

Verify that replacing the single-blob `prompts/researcher.md` prompt with `_RESEARCH_QUESTIONS` (8 individual focused questions, asked one at a time) resolves all guardrail failures.

## Root Cause (from previous session)

The previous approach passed the entire `prompts/researcher.md` file (~157 lines) as a single `chat.ask` call to NotebookLM. Two problems:

1. `prompts/researcher.md` is a Claude-facing research framework — not a question to send to NotebookLM.
2. The `notebooklm-py` parser returns empty when the response stream is large — `6 lines parsed, empty result` — even when NotebookLM returns a full answer.

The fix: define `_RESEARCH_QUESTIONS` as 8 individual focused questions (same pattern as the already-working `_ANGLE_BATTERY`), loop over them, and ask each one independently.

## Changes Applied to skills/researcher.py

- Removed: `PROMPT_FILE` constant and `prompt_text` read in `run()`
- Added: `_RESEARCH_QUESTIONS` list (8 tuples of heading + question)
- Changed: `research_one` signature from `(client, url, prompt_text, mode)` to `(client, url, mode)`
- Replaced: single `chat.ask(prompt_text)` with loop over `_RESEARCH_QUESTIONS`
- Updated: return dict `"finding"` key now holds `"\n".join(finding_parts)` (assembled sections)

## Score Card

| # | Criterion | Result | Notes |
|---|---|---|---|
| 1 | Primary sources (`primary_sources_found` ≥ 1) | **PASS** | Frontmatter: `primary_sources_found: 1` |
| 2 | No duplicate `##` headings | **PASS** | All headings unique |
| 3 | Follow-up drilling | **PASS** | N/A for researcher skill |
| 4 | Competitive Landscape — present with ≥ 2 alternatives | **PASS** | Full section with Claude Design vs Open CoDesign comparison table |
| 5 | Angle Battery — all 3 sub-answers non-empty | **PASS** | Counterintuitive Claim, Emotional Hook, Non-Technical Summary all populated |

**Final score: 5/5**

## Brief Output

- File: `Content-Hub-Vault-V2/10-Research/2026-05-08_typescript_brief.md`
- Notebook: `84dbcac7-09ba-43f7-b885-54381710070c`
- Repo: `nexu-io/open-design`
- All 8 research question sections populated with substantive answers

## Files Touched

- `skills/researcher.py` (fix applied in previous session, verified this session)
- `Content-Hub-Vault-V2/10-Research/2026-05-08_typescript_brief.md` (output)
- `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-08_Researcher_Fix_Verified.md` (this log)
