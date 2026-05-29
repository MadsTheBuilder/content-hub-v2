# Session: Research Guardrails Orchestration Design
**Date:** 2026-05-08
**Status:** Architecture complete — execution not yet started

---

## What This Session Was About

Designed a multi-agent execution plan to implement the 9/10 research guardrails from the OpenMythos audit into the Content Hub pipeline. No code was written — this session was entirely architecture and decision-making.

Implements: [[Local First Skill Engine Plan]]
Modifies: [[yt_pipeline skill]], [[researcher skill]], [[ideation skill]]

---

## Conversation Flow

### 1. The Plan
User opened `C:\Users\madhu\.claude\plans\here-s-the-full-audit-parsed-goblet.md` — a pre-written plan scoring the current research pipeline at 4.5/10 and prescribing 5 guardrails to reach 9/10.

**The 5 guardrails:**
1. **Primary-source pre-flight** — harvest arxiv/github/docs from seed material before chat starts
2. **Question-budget tracker with dedup** — `QuestionPlan` class prevents duplicate turns
3. **Adaptive follow-up drilling** — Gemini 2.5 Flash extracts 0–2 drill questions per answer
4. **Competitive landscape question** — always asked, forces "how does this compare" framing
5. **Content-angle battery** — 3 fixed questions at end: counterintuitive claim, emotional hook, non-technical summary

**8 files to touch:**
| File | Action |
|---|---|
| `skills/research_sources.py` | NEW — `collect_primary_sources()` |
| `skills/research_plan.py` | NEW — `QuestionPlan` class |
| `prompts/research_followups.md` | NEW — drill-down rules |
| `prompts/researcher.md` | MODIFY — add Lens 7.5 + Angle Battery |
| `prompts/yt_pipeline.md` | MODIFY — add Q8 Competitive Landscape, Q10–Q12 Angle Battery |
| `skills/yt_pipeline.py` | MODIFY — wire pre-flight + QuestionPlan |
| `skills/researcher.py` | MODIFY — wire pre-flight + QuestionPlan |
| `skills/ideation.py` | MODIFY — update expected sections, warn if 0 primary sources |

---

### 2. Agent Environment Design

User requested spawning multiple subagents with their own memory, running in parallel, divided by dependency group.

**Decision: 5 agents in 3 phases, dependency-grouped as teams.**

```
Phase 1 (parallel):
  Agent A — Foundation: research_sources.py + research_plan.py
  Agent B — Prompts:    research_followups.md + researcher.md + yt_pipeline.md

Phase 2 (parallel, blocked on Phase 1):
  Agent C — YT Pipeline: skills/yt_pipeline.py
  Agent D — Researcher:  skills/researcher.py

Phase 3 (blocked on Phase 2):
  Agent E — Downstream:  skills/ideation.py + end-to-end verification

Dependency map:
Agent A ─┐
         ├──► Agent C ─┐
Agent B ─┘             ├──► Agent E
         ├──► Agent D ─┘
```

**Why these teams:** Agents C and D both import from Agent A's new modules. Agent E reads the section schema that C and D produce. Agent B is pure text — no blockers, fully parallel.

---

### 3. Execution Model Decision

**Problem raised:** Running agents inside the orchestrator session bloats its context window → hallucination risk.

**Decision: Pure filesystem handoff.**
- Agents read inputs from disk directly
- Agents write outputs to disk
- Orchestrator (Claude) never reads agent-produced code between phases
- Phase 2 agent prompts are pre-written and self-contained — no relay needed

**What the orchestrator DOES between phases:**
```powershell
Test-Path ".agents/phase1_agent_a.done" -and Test-Path ".agents/phase1_agent_b.done"
# Returns True/False only — zero content enters context
```

---

### 4. Phase Verification Without Context Bloat

**Problem raised:** How do we know a phase completed without reading agent output?

**Decision: Sentinel files in `.agents/` directory.**
- Each agent writes `.agents/<phase>_<agent>.done` as its final act
- Orchestrator checks file existence only — never reads content
- Boolean result → launch next phase or wait

```
.agents/
  phase1_agent_a.done
  phase1_agent_b.done
  phase2_agent_c.done
  phase2_agent_d.done
  phase3_agent_e.done
```

Note: `.agents/` already existed as an untracked directory in the repo.

---

### 5. Resumability Design

**Problem raised:** Usage may run out mid-run — needs to be resumable without losing progress.

**Decision: `orchestration_state.json` + sentinel files = source of truth.**

State file written: `.agents/orchestration_state.json`
- Tracks all 5 agents, their status, sentinel path, and files owned
- On resume: check which `.done` files exist → skip those agents → launch remainder

Resume instructions written: `.agents/resume.md`

**Resume trigger (new session):**
> "Resume the research guardrails orchestration. Check `.agents/orchestration_state.json` and `.agents/*.done` sentinel files to see what completed. Skip finished agents. Launch only the remaining incomplete agents."

**Resume verification command:**
```powershell
Get-ChildItem .agents\*.done | Select-Object Name
```

---

## Artifacts Created This Session

| Artifact | Path | Purpose |
|---|---|---|
| Orchestration state file | `.agents/orchestration_state.json` | Resume source of truth |
| Resume instructions | `.agents/resume.md` | What to say in a new session |
| Memory entry | `memory/project_research_guardrails_orchestration.md` | Persists across sessions |
| Session log | This file | Vault knowledge graph node |

---

## What Was NOT Done

- No code written
- No agents launched
- No files in `skills/` or `prompts/` modified

---

## What's Next

Launch Phase 1: Agent A (Foundation) + Agent B (Prompts) in parallel.
User trigger: "go"

References: [[Local First Skill Engine Plan]], [[YT Pipeline Skill]], [[Researcher Skill]]
