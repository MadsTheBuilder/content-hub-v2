# Graph Report - scratch  (2026-04-20)

## Corpus Check
- 91 files · ~78,654 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 158 nodes · 161 edges · 29 communities detected
- Extraction: 88% EXTRACTED · 12% INFERRED · 0% AMBIGUOUS · INFERRED: 20 edges (avg confidence: 0.76)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Code Review & Conduct|Code Review & Conduct]]
- [[_COMMUNITY_Plan & Spec Review|Plan & Spec Review]]
- [[_COMMUNITY_Svelte Todo App|Svelte Todo App]]
- [[_COMMUNITY_Systematic Debugging|Systematic Debugging]]
- [[_COMMUNITY_Codex Compatibility|Codex Compatibility]]
- [[_COMMUNITY_TDD & Testing|TDD & Testing]]
- [[_COMMUNITY_Server Tests|Server Tests]]
- [[_COMMUNITY_Subagent Workflows|Subagent Workflows]]
- [[_COMMUNITY_Scratch Module 8|Scratch Module 8]]
- [[_COMMUNITY_Scratch Module 9|Scratch Module 9]]
- [[_COMMUNITY_Scratch Module 10|Scratch Module 10]]
- [[_COMMUNITY_Scratch Module 11|Scratch Module 11]]
- [[_COMMUNITY_Scratch Module 12|Scratch Module 12]]
- [[_COMMUNITY_Scratch Module 13|Scratch Module 13]]
- [[_COMMUNITY_Scratch Module 14|Scratch Module 14]]
- [[_COMMUNITY_Scratch Module 15|Scratch Module 15]]
- [[_COMMUNITY_Scratch Module 16|Scratch Module 16]]
- [[_COMMUNITY_Scratch Module 17|Scratch Module 17]]
- [[_COMMUNITY_Scratch Module 18|Scratch Module 18]]
- [[_COMMUNITY_Scratch Module 19|Scratch Module 19]]
- [[_COMMUNITY_Scratch Module 20|Scratch Module 20]]
- [[_COMMUNITY_Scratch Module 21|Scratch Module 21]]
- [[_COMMUNITY_Scratch Module 22|Scratch Module 22]]
- [[_COMMUNITY_Scratch Module 23|Scratch Module 23]]
- [[_COMMUNITY_Scratch Module 24|Scratch Module 24]]
- [[_COMMUNITY_Scratch Module 25|Scratch Module 25]]
- [[_COMMUNITY_Scratch Module 26|Scratch Module 26]]
- [[_COMMUNITY_Scratch Module 27|Scratch Module 27]]
- [[_COMMUNITY_Scratch Module 28|Scratch Module 28]]

## God Nodes (most connected - your core abstractions)
1. `Superpowers` - 23 edges
2. `brainstorming skill` - 12 edges
3. `subagent-driven-development skill` - 10 edges
4. `systematic-debugging skill` - 8 edges
5. `Basic Superpowers Workflow` - 8 edges
6. `writing-plans skill` - 7 edges
7. `Test-Driven Development Skill` - 7 edges
8. `Svelte Todo List Implementation Plan` - 6 edges
9. `runTests()` - 5 edges
10. `Brainstorm â†’ Plan â†’ Implement Workflow` - 5 edges

## Surprising Connections (you probably didn't know these)
- `writing-plans skill` --conceptually_related_to--> `Test-Driven Development Skill`  [INFERRED]
  scratch/superpowers/README.md → scratch/superpowers/skills/test-driven-development/SKILL.md
- `executing-plans skill` --implements--> `Brainstorm â†’ Plan â†’ Implement Workflow`  [INFERRED]
  scratch/superpowers/README.md → scratch/superpowers/docs/superpowers/specs/2026-01-22-document-review-system-design.md
- `Action-Oriented Skill Request` --conceptually_related_to--> `subagent-driven-development skill`  [INFERRED]
  scratch/superpowers/tests/explicit-skill-requests/prompts/action-oriented.txt → scratch/superpowers/README.md
- `systematic-debugging skill` --implements--> `Four-Phase Debugging Process`  [INFERRED]
  scratch/superpowers/README.md → scratch/superpowers/skills/systematic-debugging/CREATION-LOG.md
- `Verification Before Completion Skill` --conceptually_related_to--> `systematic-debugging skill`  [INFERRED]
  scratch/superpowers/skills/verification-before-completion/SKILL.md → scratch/superpowers/README.md

## Communities

### Community 0 - "Code Review & Conduct"
Cohesion: 0.11
Nodes (19): code-reviewer agent, Contributor Code of Conduct, DRY (Don't Repeat Yourself), YAGNI (You Aren't Gonna Need It), Brainstorm Server (zero-dependency), Inline Self-Review Feature, Superpowers for Codex Guide, Superpowers for OpenCode Guide (+11 more)

### Community 1 - "Plan & Spec Review"
Cohesion: 0.12
Nodes (18): Plan Review Loop (Chunk-by-Chunk), Spec Review Loop, Brainstorming Skill Request, Visual Brainstorming Companion Feature, Document Review System Plan, Visual Brainstorming Implementation Plan, Hard Gate: Design Before Implementation, One Question at a Time Principle (+10 more)

### Community 2 - "Svelte Todo App"
Cohesion: 0.12
Nodes (17): FilterBar Component, TodoInput Component, TodoItem Component, Action-Oriented Skill Request, Subagent-Driven Development Knowledge, Subagent-Driven Development Request, Task Dispatch Pattern, Go Fractals CLI Design (+9 more)

### Community 3 - "Systematic Debugging"
Cohesion: 0.18
Nodes (11): Root Cause Tracing, Systematic Debugging Request, Root Cause Mandate, Four-Phase Debugging Process, Codex Tool Mapping Reference, Copilot CLI Tool Mapping Reference, Using Git Worktrees Skill, systematic-debugging skill (+3 more)

### Community 4 - "Codex Compatibility"
Cohesion: 0.22
Nodes (10): Codex App Compatibility Design, Environment Detection (Git Worktree vs Sandbox), Codex App Compatibility Plan, Finishing Development Branch Process, requesting-code-review skill, executing-plans skill, Finishing a Development Branch Skill, finishing-a-development-branch skill (+2 more)

### Community 5 - "TDD & Testing"
Cohesion: 0.24
Nodes (10): RED-GREEN-REFACTOR Cycle, Testing Anti-Patterns, CLAUDE.md Testing Example, Anthropic Skill Authoring Best Practices, Persuasion Principles for Skill Design, Testing Skills With Subagents, Test-Driven Development Skill, test-driven-development skill (+2 more)

### Community 6 - "Server Tests"
Cohesion: 0.48
Nodes (5): cleanup(), runTests(), sleep(), startServer(), waitForServer()

### Community 7 - "Subagent Workflows"
Cohesion: 0.29
Nodes (7): Model Routing by Task Complexity, Two-Stage Review (Spec + Quality), Subagent-Driven Development Workflow, Code Quality Reviewer Subagent Role, Implementer Subagent Role, Spec Compliance Reviewer Subagent Role, Subagent-Driven Development Skill

### Community 8 - "Scratch Module 8"
Cohesion: 0.29
Nodes (7): After-Planning Flow Pattern, Claude Suggested It Request, Mid-Conversation Plan Execution, Skip Formalities Directive, Plan Execution Pattern, Executing Plans, Writing Plans Trigger

### Community 9 - "Scratch Module 9"
Cohesion: 0.53
Nodes (4): combineGraphs(), extractDotBlocks(), main(), renderToSvg()

### Community 10 - "Scratch Module 10"
Cohesion: 0.4
Nodes (5): Problem 1: Verification Gap, Problem 2: Background Process Accumulation, Problem 3: Context Bloat in Subagent Prompts, Problem 4: No Self-Reflection Before Handoff, Skills Improvements from User Feedback

### Community 11 - "Scratch Module 11"
Cohesion: 0.4
Nodes (5): Browser-Terminal Split Model, Events File (.events), Non-Blocking Brainstorming Model, Visual Brainstorming Refactor Design, Visual Companion Guide

### Community 12 - "Scratch Module 12"
Cohesion: 0.5
Nodes (0): 

### Community 13 - "Scratch Module 13"
Cohesion: 0.67
Nodes (0): 

### Community 14 - "Scratch Module 14"
Cohesion: 0.67
Nodes (3): Focused Agent Prompts, Parallel Agent Dispatch Process, Dispatching Parallel Agents Skill

### Community 15 - "Scratch Module 15"
Cohesion: 0.67
Nodes (3): Technical Evaluation (vs Emotional Performance), Code Review Reception Process, Receiving Code Review Skill

### Community 16 - "Scratch Module 16"
Cohesion: 0.67
Nodes (3): HTTP Server Implementation, WebSocket Protocol Implementation, Zero-Dependency Brainstorm Server Design

### Community 17 - "Scratch Module 17"
Cohesion: 0.67
Nodes (3): Code Review Request Process, Code Reviewer Subagent, Requesting Code Review Skill

### Community 18 - "Scratch Module 18"
Cohesion: 0.67
Nodes (3): Feature Implementation, Code Review Request, Test-Driven Development Trigger

### Community 19 - "Scratch Module 19"
Cohesion: 1.0
Nodes (1): Day 4 - Task 4A: APScheduler verification script. Run from the project root: pyt

### Community 20 - "Scratch Module 20"
Cohesion: 1.0
Nodes (0): 

### Community 21 - "Scratch Module 21"
Cohesion: 1.0
Nodes (2): 94% PR Rejection Rate Fact, Rationale: Strict PR Requirements

### Community 22 - "Scratch Module 22"
Cohesion: 1.0
Nodes (2): OpenCode Support Implementation Plan, OpenCode Support Design Plan

### Community 23 - "Scratch Module 23"
Cohesion: 1.0
Nodes (1): Release Notes v5.x

### Community 24 - "Scratch Module 24"
Cohesion: 1.0
Nodes (1): Superpowers Changelog

### Community 25 - "Scratch Module 25"
Cohesion: 1.0
Nodes (1): Visual Brainstorming Refactor Plan

### Community 26 - "Scratch Module 26"
Cohesion: 1.0
Nodes (1): Design for Isolation and Clarity Principle

### Community 27 - "Scratch Module 27"
Cohesion: 1.0
Nodes (1): Gemini CLI Tool Mapping Reference

### Community 28 - "Scratch Module 28"
Cohesion: 1.0
Nodes (1): Authentication System Plan Pattern

## Knowledge Gaps
- **86 isolated node(s):** `Day 4 - Task 4A: APScheduler verification script. Run from the project root: pyt`, `Test-Driven Development Philosophy`, `Systematic over ad-hoc Philosophy`, `Claude Code platform`, `Cursor platform` (+81 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Scratch Module 19`** (2 nodes): `test_scheduler.py`, `Day 4 - Task 4A: APScheduler verification script. Run from the project root: pyt`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 20`** (2 nodes): `ws-protocol.test.js`, `runTests()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 21`** (2 nodes): `94% PR Rejection Rate Fact`, `Rationale: Strict PR Requirements`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 22`** (2 nodes): `OpenCode Support Implementation Plan`, `OpenCode Support Design Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 23`** (1 nodes): `Release Notes v5.x`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 24`** (1 nodes): `Superpowers Changelog`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 25`** (1 nodes): `Visual Brainstorming Refactor Plan`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 26`** (1 nodes): `Design for Isolation and Clarity Principle`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 27`** (1 nodes): `Gemini CLI Tool Mapping Reference`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Scratch Module 28`** (1 nodes): `Authentication System Plan Pattern`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Superpowers` connect `Code Review & Conduct` to `Plan & Spec Review`, `Svelte Todo App`, `Systematic Debugging`, `Codex Compatibility`, `TDD & Testing`?**
  _High betweenness centrality (0.244) - this node is a cross-community bridge._
- **Why does `subagent-driven-development skill` connect `Svelte Todo App` to `Code Review & Conduct`, `Scratch Module 8`, `Codex Compatibility`?**
  _High betweenness centrality (0.155) - this node is a cross-community bridge._
- **Why does `brainstorming skill` connect `Plan & Spec Review` to `Code Review & Conduct`, `Scratch Module 11`, `Codex Compatibility`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `brainstorming skill` (e.g. with `Visual Brainstorming Companion Feature` and `Brainstorm â†’ Plan â†’ Implement Workflow`) actually correct?**
  _`brainstorming skill` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `subagent-driven-development skill` (e.g. with `Action-Oriented Skill Request` and `Task Dispatch Pattern`) actually correct?**
  _`subagent-driven-development skill` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `systematic-debugging skill` (e.g. with `Four-Phase Debugging Process` and `Verification Before Completion Skill`) actually correct?**
  _`systematic-debugging skill` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Day 4 - Task 4A: APScheduler verification script. Run from the project root: pyt`, `Test-Driven Development Philosophy`, `Systematic over ad-hoc Philosophy` to the rest of the system?**
  _86 weakly-connected nodes found - possible documentation gaps or missing edges._