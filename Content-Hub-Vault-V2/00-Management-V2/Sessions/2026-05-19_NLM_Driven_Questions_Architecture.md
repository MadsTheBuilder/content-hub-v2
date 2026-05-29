---
date: 2026-05-19
type: session
status: brainstorm-complete — awaiting implementation go-ahead
description: Architecture decision to replace hardcoded question injection with NLM-driven suggested topics in both researcher.py and yt_pipeline.py. Implementation pending user go-ahead.
tags: [architecture, nlm, researcher, yt-pipeline, brainstorm, refactor]
---

# NLM-Driven Questions Architecture — Session Handoff

Implements: [[Local_First_Skill_Engine_Plan]]
References: [[2026-05-08_Researcher_Fix_Verified]] | [[2026-05-08_YT_Pipeline_Friction_Repair]]
Modifies (pending): [[skills/researcher.py]] | [[skills/yt_pipeline.py]]

---

## Why This Session Happened

The NIM test run eval report (`Content-Hub-Vault-V2/NIM test run/EVAL_REPORT.md`) showed 3 failures. The first failure was the researcher again passing all NotebookLM questions as one blob — a regression.

User asked for explanation only (no fix). Then, after watching their own NLM workflow on video, proposed a fundamental architecture change.

---

## Part 1 — The Regression: What Happened and Why

### Root Cause

This was **not a reversion** of the 2026-05-08 fix. It was a **parallel bug** that always existed in `yt_pipeline.py`.

Timeline:
- 2026-05-08: `researcher.py` was fixed — the single `prompts/researcher.md` blob was replaced with `_RESEARCH_QUESTIONS` (8 individual tuples), looped one at a time.
- That fix was **never ported** to `yt_pipeline.py`, which was built separately on a different pattern.
- `yt_pipeline.py` uses `SECTION_PATTERN` + `_load_questions()` to parse `prompts/yt_pipeline.md`. The regex has a DOTALL bug.

### The Bug in `yt_pipeline.py`

```
Line 28: SECTION_PATTERN = re.compile(r"## (Q\d+ — .+)\n(.*?)(?=\n## |\Z)", re.DOTALL)
```

`re.DOTALL` makes `.` match newlines. The `.+` in the heading capture group therefore matches across every heading line in the file, causing all 12 questions to collapse into a single match — one giant blob sent to NotebookLM as a single question.

Fix (if patching in isolation): change `.+` to `[^\n]+`.

**Decision:** Don't patch the regex. Retire the whole `prompts/yt_pipeline.md` + `_load_questions()` mechanism as part of the NLM-driven architecture below.

---

## Part 2 — New Architecture: NLM-Driven Questions

### Core Decision

**Stop injecting hardcoded questions. Let NotebookLM drive its own questions.**

Current approach (broken): Claude generates a fixed list of questions → injects them into NLM → NLM answers them.

New approach: Sources are added to the notebook → NotebookLM's own `get_description()` API returns `suggested_topics` (questions NLM itself thinks are worth asking based on the sources) → those become the seed for the research loop.

### Why This Is Better

- NLM's suggested questions are grounded in the actual sources loaded — they reflect what the notebook *can* answer, not what Claude thinks it should answer.
- Eliminates the entire injection failure surface (regex bugs, prompt file drift, format mismatch).
- Questions are already in NLM's internal format (`.prompt` field) — no translation needed.
- Inline citations in answers (the numbered markers) are **contextual pointers only** — not auto-ingested. They give humans traceability, not Claude follow-up work.

### What Changes and What Stays

**Removed:**
- `skills/yt_pipeline.py`: `PROMPTS_FILE` (line 26), `SECTION_PATTERN` (line 28), `_load_questions()` (lines 103-105)
- `skills/researcher.py`: `_RESEARCH_QUESTIONS` list (lines 121-153), `_ANGLE_BATTERY` list (lines 156-169), the two for-loops that iterate them (lines 492-516)

**Stays untouched:**
- `QuestionPlan` class in `skills/research_plan.py` — budget, dedup, adaptive follow-ups machinery all stay. Only the **seed** changes from `_load_questions()` to `get_description().suggested_topics`.
- `generate_followups()` in `skills/research_plan.py` — stays as-is.
- All artifact generation, vault write, frontmatter structure.

### Stopping Condition (Pending)

User will provide research methodology articles. From those, Claude will build a completeness checklist that determines when the NLM question loop is "done enough." This checklist replaces the hard `budget=12` cap as the primary stopping signal. Budget stays as a safety ceiling.

**Status: User has not yet provided the articles. Implementation blocked on this.**

---

## Part 3 — Structure Injection Decision

**Where brand/format instructions go: NotebookLM Studio, not Claude post-processing.**

When generating Studio artifacts (reports, slide decks), inject structure/brand instructions directly into NLM's Studio generation prompt. Examples:
- Reports: "small, concise, bullet points"
- Slide decks: "modern, techy presentation style"

This is separate from the question loop. The question loop is for research extraction. Studio generation is a distinct step after research is complete.

**Status: Spec not yet defined. Follow-up task after NLM-driven questions is implemented.**

---

## Part 4 — Implementation Plan (Ready to Execute, Not Yet Started)

### `researcher.py` changes

Remove `_RESEARCH_QUESTIONS` and `_ANGLE_BATTERY` constants. Replace the two for-loops in `research_one()` (lines ~492-516) with:

```python
desc = await client.notebooks.get_description(nb.id)
for topic in desc.suggested_topics:
    heading = topic.question
    prompt = topic.prompt or topic.question
    result = await client.chat.ask(nb.id, prompt, source_ids=verified_source_ids)
    answer = result.answer or "[no answer]"
    finding_parts.append(f"### {heading}\n\n{answer}\n")
    raw_qa.append({"heading": heading, "answer": answer})
```

Pass `angle_raw=[]` to `synthesize_brief()`.

### `yt_pipeline.py` changes

Remove `PROMPTS_FILE` (line 26), `SECTION_PATTERN` (line 28), `_load_questions()` (lines 103-105).

Add async helper:
```python
async def _get_nlm_suggested_questions(notebook_id: str) -> list[tuple[str, str]]:
    async with await NotebookLMClient.from_storage(timeout=60) as client:
        desc = await client.notebooks.get_description(notebook_id)
        return [(t.question, t.prompt or t.question) for t in desc.suggested_topics]
```

Change line 210 from:
```python
plan = QuestionPlan(_load_questions(), budget=12)
```
to:
```python
plan = QuestionPlan(asyncio.run(_get_nlm_suggested_questions(notebook_id)), budget=12)
```

### API details confirmed

- `notebooklm-py/src/notebooklm/_notebooks.py` — `get_description()` at lines 158-212, calls `RPCMethod.SUMMARIZE`, returns `NotebookDescription`
- `notebooklm-py/src/notebooklm/types.py` — `SuggestedTopic(question: str, prompt: str)`, `NotebookDescription(summary: str, suggested_topics: list[SuggestedTopic])`
- `researcher.py` uses the Python client directly (async). `yt_pipeline.py` uses CLI subprocess — adding a one-off async helper for the seed call bridges both patterns cleanly.

---

## Part 5 — Open Items from EVAL_REPORT.md (Unresolved)

Three bugs documented, none fixed this session:

1. **SECTION_PATTERN regression** — will be eliminated by the NLM-driven architecture refactor above, not patched in isolation.
2. **NIM silent failures with blank error logs** — separate task, not addressed.
3. **Hook step not receiving `--research-file`** — separate task, not addressed.

---

## Blockers Before Implementation Can Start

1. **Research methodology articles** — user will provide; needed to build completeness checklist.
2. **User explicit go-ahead** — brainstorming phase explicitly declared not complete; no edits until user confirms.

---

## Files Touched This Session

- `Content-Hub-Vault-V2/00-Management-V2/Sessions/2026-05-19_NLM_Driven_Questions_Architecture.md` — this log

No code was changed. All edits are pending.
