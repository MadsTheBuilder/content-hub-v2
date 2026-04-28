# Content Hub — Claude Code Context
## V2 — Local-First Skill Engine

Behavioral guardrails + project protocol for Content Hub development. The guardrails bias toward caution over speed. For trivial one-liner tasks, use judgment.

---

## § 1. Think Before Acting

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.
- This applies at **every stage** — not just session start. Mid-task ambiguity gets the same treatment.

## § 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## § 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: **Every changed line should trace directly to the user's request.**

## § 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Wire the endpoint" → "Call it from the frontend, verify the response shape matches types.ts"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification — surface that upfront.

## § 5. Communication Discipline

**Match length to complexity. No filler. Results only.**

- No filler phrases or summaries. Match response length to complexity. Read files before editing.

---

## § 6. Session Start Protocol

1. Read `Content-Hub-Vault/00-Management-V2/Memory/context.md` (project context).
2. Read `Content-Hub-Vault/00-Management-V2/Plans/CLAUDE.md` (V2 rules and stack).
3. Read `Content-Hub-Vault/00-Management-V2/Plans/Local_First_Skill_Engine_Plan.md` (full build plan).
4. Read `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md` (what to do next).
5. **Plan before acting**: Ask 1–3 focused questions to surface ambiguities, then wait for answers before touching any file or tool.
6. Load `.claude/skills/<name>/SKILL.md` only when acting on a matching skill task — never on session load.

## § 7. Vault Knowledge Graph — Memory System

The vault is Claude's persistent graph brain. Every log must form an explicit, queryable node. After every significant task:

1. Write a session log → `Content-Hub-Vault/00-Management-V2/Sessions/YYYY-MM-DD_Short_Description.md`.
   - **MANDATORY**: You must use explicit `[[WikiLinks]]` when referencing components, past sessions, or architectural features. 
   - **Edges**: Use semantic patterns to establish edges (e.g., `Implements: [[Feature Name]]`, `References: [[Issue Node]]`, `Modifies: [[Component Name]]`).
   - Include: what changed, files touched, open items.
2. Update `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md` using `[[WikiLinks]]` to connect tasks back to your session log.
3. Write the log **before** giving the final response to the user.

## § 8. Model Routing

- **Sonnet** (default): All task execution — code, edits, migrations, debugging, file writes.
- **Opus**: High-level reasoning only — architecture decisions, complex trade-offs, plan design. Use sparingly; never for routine tasks.

## § 9. Orchestration

- **Manual**: `/orchestrate` or `/delegate` → invoke `.claude/skills/orchestrate/SKILL.md`.
- **Resume**: `/resume-orchestration` or `/resume` → invoke `.claude/skills/resume-orchestration/SKILL.md`.
- **Auto-trigger** (no slash command needed):
  - 3+ subtasks in a single request
  - 2+ specialist domains from AGENTS.md
  - 10+ files across subsystems
- **Do NOT orchestrate**: Single-domain tasks, single-file fixes, exploratory/investigative work — act directly.
- **Source of truth**: `Content-Hub-Vault/00-Management-V2/Superpowers/orchestrated-execution.md` overrides all skill files if they conflict.
- **State files**: Active orchestration plans live in `Content-Hub-Vault/00-Management-V2/Orchestrations/`.

## § 10. Project Knowledge

| What | Where |
|------|-------|
| Stack, architecture, decisions | `Content-Hub-Vault/00-Management-V2/Memory/context.md` |
| Full build plan | `Content-Hub-Vault/00-Management-V2/Plans/Local_First_Skill_Engine_Plan.md` |
| Active sprint | `Content-Hub-Vault/00-Management-V2/Tasks/Current_Sprint.md` |
| V2 session history | `Content-Hub-Vault/00-Management-V2/Sessions/` |
| Agent roles and domains | `AGENTS.md` (project root) |
| V1 (parked) reference | `Content-Hub-Vault/00-Management/` |

---

**These guidelines are working if:** diffs contain only lines that trace to the user's request, clarifying questions come before implementation rather than after mistakes, code output is lean with no speculative abstractions, and session logs are written before the final response.
