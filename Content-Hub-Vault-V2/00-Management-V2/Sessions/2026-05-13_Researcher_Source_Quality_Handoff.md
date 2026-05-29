---
date: 2026-05-13
type: session-handoff
topic: Researcher skill — source quality architecture
status: in-progress, handed off
files_modified:
  - skills/researcher.py
  - .claude/skills/researcher/SKILL.md
files_to_revert:
  - skills/researcher.py (partial — see "Revert List" below)
---

# Session Handoff — Researcher Source Quality & Pipeline Fixes

This document is a full context handover. The next session should read this before touching any file.

---

## What This Session Was About

We did a full post-mortem on the `2026-05-12_ai-agents_brief.md` smoke test run of the `/researcher` skill. The session covered:
1. Honest productivity audit of the NotebookLM run
2. Three structural problems identified and partially addressed
3. An architectural brainstorm that landed on a better solution not yet implemented

---

## Smoke Test Post-Mortem (What We Found)

The run was `python -m skills.researcher --niche "AI agents"` on 8 repos from `github_trending.md`.

### Raw Scorecard

| # | Repo | Questions Answered | Verdict |
|---|------|--------------------|---------|
| 1 | yaojingang/yao-open-prompts | 11/11 | Poisoned — sources drifted to Shunyu Yao's ReAct papers, not the repo |
| 2 | lightseekorg/tokenspeed | 0/11 | Total failure — import timed out, zero sources |
| 3 | TitanFlow-Systems/best-of-algorithmic-trading | 11/11 | Usable — but unrelated to "AI agents" niche |
| 4 | kyegomez/OpenMythos | 11/11 | Best quality — viral repo, relevant sources, strong answers |
| 5 | Manavarya09/design-extract | ~11/11 | Partial drift — "Unanswered Questions" section answered about circuit extraction |
| 6 | earthtojake/text-to-cad | ~4/11 | Rate-limited mid-run, 7 questions failed |
| 7 | crynta/terax-ai | 0/11 | Complete failure — sources were TetraxAI renewable energy company, HP LoadRunner, Mercury marine |
| 8 | cosmicstack-labs/mercury-agent | 0/11 | Complete failure — sources were mercury chemistry, access control boards, Mercury programming language |

**Adjusted useful output: 2 repos out of 8.**

### Root Causes Identified

**Problem 1: Rate limiting** — NotebookLM's chat API rejected requests after sustained use across repos 6–8. The pipeline has no backoff or retry. *Decision: ignore for now — treat as an infrastructure constraint, not a code problem.*

**Problem 2: Source quality drift** — When a repo name is ambiguous ("mercury", "terax", "yao"), NotebookLM's web search pulls in completely unrelated material. The pipeline has no mechanism to detect or reject bad sources before asking questions. *This is the core problem being solved.*

**Problem 3: Auto-selection of repos** — The `--niche` parameter has zero effect on which repos get researched. It only names the output file. All repos from `github_trending.md` were researched regardless of relevance. The user never chose what to research. *This was fixed in this session — see "Confirmed Changes" below.*

**Structural discovery:** The title file `07-Titles/2026-05-12_ai-agents-building-reliable-systems.md` has no connection to any specific repo's research output. It was generated from a concept string, not from a brief. This is a broken handoff between `/researcher` and `/title` — not addressed in this session, flagged for later.

---

## Three Decisions Made in This Session

### Decision 1: Rate Limiting — Ignore
Not worth solving in the pipeline. NotebookLM rate limits are an external constraint. The fix is operational (space out runs, do fewer repos per session), not architectural.

### Decision 2: Repo Selection — Fixed (confirmed good, keep)
The old behavior: if `--repos` not given, auto-select the top `N` repos from trending. This was silent and wrong.

The new behavior: `--repos` is required. If not given, the pipeline lists available repos and exits. Added `--list` flag so the user can see what's in trending before deciding.

**This change is correct and should stay.**

### Decision 3: Source Quality — Partially Implemented, Partially Wrong
This is the live problem. We went through two proposals before landing on the right architecture.

---

## What Needs to Be Reverted (The Wrong Path)

During this session, a keyword-based source filter was added to `skills/researcher.py`. **This needs to be removed.** It was the first attempt at fixing source quality and we explicitly agreed it was the wrong approach.

### Functions to remove entirely:

```python
def _repo_keywords(url: str) -> set[str]:
    ...

def _is_relevant_source(source: dict, keywords: set[str]) -> bool:
    ...
```

### Block to remove from `research_one()`:

```python
if sources_found and task_id:
    keywords = _repo_keywords(url)
    relevant = [s for s in sources_found if _is_relevant_source(s, keywords)]
    dropped = len(sources_found) - len(relevant)
    if dropped:
        print(f"[{slug}] Filtered out {dropped} off-topic sources (kept {len(relevant)})")
    import_count = min(len(relevant), 10)
    if import_count:
        await client.research.import_sources(nb.id, task_id, relevant[:import_count])
        print(f"[{slug}] Imported {import_count} sources")
    else:
        print(f"[{slug}] WARNING: no relevant sources survived filtering — answers may be unreliable")
```

Replace this entire block with the original simple import (the one that was there before this session):

```python
if sources_found and task_id:
    import_count = min(len(sources_found), 10)
    await client.research.import_sources(nb.id, task_id, sources_found[:import_count])
    print(f"[{slug}] Imported {import_count} sources")
```

### Why the keyword filter is wrong:

The filter kept sources only if their URL or title contained tokens from the repo slug. For `kyegomez/OpenMythos`, the keywords are `{"kyegomez", "openmythos"}`. This means:
- A YouTube video titled "How to Build AI Agent Worlds" → DROPPED (doesn't contain the repo name)
- An Anthropic article about the Mythos model → DROPPED (URL is anthropic.com, title doesn't contain "openmythos")
- A blog post explicitly reviewing OpenMythos → KEPT

The filter removes legitimately relevant sources that don't happen to name the repo explicitly. It solves the "mercury chemistry" problem but creates a new problem: stripping out good contextual research material.

---

## What Stays (Confirmed Good Changes)

### 1. `chat.configure()` with custom_prompt — KEEP

This was added in `research_one()` just before the question loop:

```python
await client.chat.configure(
    nb.id,
    goal=ChatGoal.CUSTOM,
    custom_prompt=(
        f"You are a technical researcher analysing the GitHub project '{owner_repo}' "
        f"(URL: {url}). Answer every question strictly in the context of this software project. "
        f"If a source appears unrelated (wrong company, person, or topic sharing a similar name), "
        f"ignore it and state that the source was irrelevant."
    ),
)
```

This is a semantic anchor. Even if bad sources slip in, the LLM is instructed to flag and ignore them rather than answer from them. This is a valid guard and should stay.

Also requires adding `ChatGoal` to the import: `from notebooklm import ChatGoal, NotebookLMClient` — this is already done and should stay.

### 2. Explicit repo selection — KEEP

- `--repos` required to run research
- `--max-sources` removed (was meaningless once auto-selection was gone)
- `--list` flag added to show available repos
- `run()` signature simplified: `max_sources` param removed
- `SKILL.md` updated to describe the new two-step workflow: list → pick → run

---

## The Right Architecture (Not Yet Built)

This is what the next session needs to implement.

### The Problem Being Solved

NotebookLM web research returns sources based on the repo name string alone. When that name is ambiguous or shared with other entities, the returned sources are completely wrong. We cannot trust the source list to be on-topic.

### The Approach: Source Verification Agent

After sources are imported and indexed, a verification step reads the actual content of each source and decides if it is relevant to the research topic. This is semantic judgment on content, not keyword matching on URLs.

**Key API hooks available (confirmed from notebooklm-py):**

1. `sources.list(notebook_id)` — returns all imported sources with their IDs and metadata
2. `sources.get_guide(notebook_id, source_id)` — returns `{"summary": str, "keywords": list[str]}` for each source. This is an AI-generated summary of the source's actual content.
3. `chat.ask(notebook_id, question, source_ids=list[str])` — the `source_ids` parameter means we can direct questions to ONLY the verified sources, without deleting anything from the notebook.

### Pipeline with Verification (Target State)

```
Create notebook
→ Add repo URL + README as primary sources
→ Run web research (deep mode)
→ Poll until complete
→ Import ALL discovered sources (no filter)
→ Wait 75s for indexing
→ VERIFICATION STEP:
    For each source:
        call sources.get_guide() → get summary + keywords
        pass to verification agent with repo context (name, README summary)
        agent decides: RELEVANT or DROP
    collect verified_source_ids
→ chat.configure() with custom_prompt (keep this, it's additive)
→ For ALL chat.ask() calls: pass source_ids=verified_source_ids
```

The key insight: we don't need to delete sources. We just pass `source_ids` to every `chat.ask()` call so the LLM only reads from verified sources. Non-destructive, clean.

### What the Verification Agent Judges

Relevant if:
- Source is directly about this repo/project
- Source is about the same technology, problem space, or closely related tool (e.g., for OpenMythos: AI world-building, multi-agent simulation, the Anthropic Mythos model)
- Source evaluates, benchmarks, or contextualizes the repo

Drop if:
- Source is demonstrably about a different entity that shares the repo name (different company, chemical compound, marine equipment, etc.)
- Source content has no plausible connection to the repo's purpose

**The Anthropic/Mythos example:** An Anthropic article about the Mythos model would be dropped by keyword filtering. The verification agent reads its guide summary — "Anthropic's Mythos model for AI storytelling and world-building" — knows we're researching `kyegomez/OpenMythos` which is an AI world-building agent, and marks it RELEVANT. This is the exact behavior we want.

### Open Design Decision: Who Makes the Relevance Call?

This was left undecided at end of session. Two options:

**Option A — Claude API call**
Pass the repo README summary + each source's guide summary to Claude. Ask it to judge relevance. Cleanest semantic judgment, handles edge cases well. Adds ~10 API calls per repo (one per source). Requires `anthropic` package + API key — likely already available in this project.

**Option B — NotebookLM's own chat**
Ask the notebook itself: "Based on the README already in this notebook, which of these sources are relevant to researching [repo_name]? List which to keep and which to drop." Self-contained, no extra dependency, uses the same session. Slightly circular but the README is already a grounded primary source so the judgment is informed.

The next session should pick one and implement. Option A is preferred if the project already has the `anthropic` package available. Check `requirements.txt` or `pyproject.toml` first.

---

## Current State of `skills/researcher.py` (What's In It Right Now)

The file has all the confirmed changes PLUS the to-be-reverted filter. Before building the verification agent:

1. Remove `_repo_keywords()` function
2. Remove `_is_relevant_source()` function
3. Replace the filtering import block with the original simple import block (see above)
4. Then add the verification step

`chat.configure()` and `ChatGoal` import stay. Explicit `--repos` requirement stays.

---

## Summary of End Goal

| Behavior | Old | Target |
|----------|-----|--------|
| Repo selection | Auto-picks top N from trending | User explicitly picks repos before run |
| Source import | Import top 10 results, no filter | Import all, then verify content |
| Source verification | None | Agent reads `get_guide()` per source, judges relevance semantically |
| Question context | All sources in notebook | Only verified sources via `source_ids=` |
| Chat anchoring | None | `chat.configure()` custom_prompt names the repo |
| `--niche` effect | Only names output file | Still only names output file (this is fine) |

The researcher drives NotebookLM. Not the other way around.

---

## Related Files

- `skills/researcher.py` — main implementation, partially modified
- `.claude/skills/researcher/SKILL.md` — updated, accurate as of this session
- `Content-Hub-Vault-V2/10-Research/2026-05-12_ai-agents_brief.md` — the smoke test output
- `Content-Hub-Vault-V2/10-Research/2026-05-12_ai_agents/research.md` — separate YT pipeline output, not this skill
- `notebooklm-py/src/notebooklm/` — the client library; key files: `_chat.py`, `_sources.py`, `_research.py`
- `notebooklm-py/docs/python-api.md` — full API reference
