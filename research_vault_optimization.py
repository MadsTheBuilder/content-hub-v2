"""
Vault Optimization Research Pipeline
=====================================
Uses Gemini as NotebookLM (research analyst) + 2nd Brain (strategic advisor)
to research and optimize our Obsidian vault + CLAUDE.md system.

Flow:
  Claude (orchestrator) -> Gemini NotebookLM (extract insights from research)
  Claude (orchestrator) -> Gemini 2nd Brain (apply insights to our specific setup)
  Full communication log output for transparency.
"""

import json
import os
import sys
import time
from datetime import datetime

# Add parent to path so we can use backend config
sys.path.insert(0, os.path.dirname(__file__))
from backend.config import settings

from google import genai
from google.genai import types

client = genai.Client(api_key=settings.google_ai_studio_key)

# ── Research documents (gathered from web) ─────────────────────────────

RESEARCH_DOCS = {
    "anthropic_official": """
# Anthropic Official: Using CLAUDE.md Files
- CLAUDE.md is loaded into context every session — keep it concise (<200 lines)
- Use markdown headers and bullets, organized sections
- Split large files: use @path/to/file imports or .claude/rules/ files
- Content areas: project mapping, dev standards, common commands, tool integration, workflows
- Don't include: API keys, credentials, security details
- Use /init to generate starter CLAUDE.md, refine from there
- Custom slash commands via .claude/commands/ directory
- Every few weeks, ask Claude to review and optimize CLAUDE.md
- Treat as high-level curated guardrails, not comprehensive manual
""",

    "chase_ai_persistent_memory": """
# Chase AI: Claude Code + Obsidian Persistent Memory
- Vault is just a regular directory — no vendor lock-in, all standard markdown
- CLAUDE.md for personal assistant is about how you think and want notes formatted, NOT code conventions
- Folder structure: daily-notes/, research/, projects/, people/, inbox/
- Claude reads CLAUDE.md at session start, scans vault structure
- Symbiotic: Claude supercharges Obsidian (formats notes), Obsidian supercharges Claude (structured context)
- Periodically: "Review all vault notes. Compare against CLAUDE.md. Update conventions."
- CLAUDE.md becomes living document that gets smarter as vault grows
- WARNING: LLM-generated context files decrease agent performance by 0.5-2% while raising costs 20%+ in coding contexts
- Keep CLAUDE.md lean — bloated files consume valuable context tokens
- Works best for personal knowledge management, not pure coding
""",

    "railly_hugo_agentic_second_brain": """
# Railly Hugo: Obsidian as Personal OS for AI Coding Agents
- Three layers: Persistence (Obsidian), Execution (AI agents), Personality (config files)
- PARA + Zettelkasten hybrid: 01_Inbox, 02_Journal, 03_Garden, 04_Projects, 05_Areas, 06_Content, 07_System
- CLAUDE.md establishes identity: name, role, stack preferences, repo map, goals, anti-patterns
- Anti-patterns tracked with (xN) recurrence notation across annual reviews
- Session protocols: /morning (MITs, calendar), /ship (auto-log), /today (review), /pulse (weekly analysis)
- Project-level context files in 07_System/context-files/ loaded via @ syntax
- Memory auto-saves to ~/.claude/projects/memory/ as markdown with frontmatter
- /scaffold skill: zero-to-production app in ~2 minutes
- Skills are universal (cross-project), Commands are project-specific
- Session 100 is dramatically more useful than session 1 due to compounding
- QMD semantic search handles 2,900+ documents with 30ms latency
""",

    "obsidian_mind_template": """
# Obsidian Mind: Full Vault Template for Engineers
- 285-line CLAUDE.md as operating manual
- Folders: work/ (active, archive, incidents, 1-1), org/ (people, teams), perf/ (brag doc, competencies, evidence), brain/ (North Star, Memories, Decisions, Patterns, Gotchas, Skills), reference/, thinking/, templates/, bases/
- Session hooks: SessionStart (inject context), UserPromptSubmit (classify & route), PostToolUse (validate frontmatter), PreCompact (backup transcript), Stop (archive, update indexes)
- Commands: /standup, /dump (freeform capture, auto-routed), /wrap-up, /weekly, /incident-capture, /review-brief, /vault-audit
- YAML frontmatter on all notes: date, status, project, quarter, tags
- Performance graph: competency notes as link targets, work notes link to competencies
- brain/North Star.md read every session for goal grounding
- brain/Gotchas.md, brain/Patterns.md, brain/Key Decisions.md as dedicated files
- QMD skill: semantic search before reading, after creating (auto-linking)
- /vault-upgrade command to migrate existing vaults
""",
}

# ── Our current system (for 2nd brain analysis) ───────────────────────

OUR_CURRENT_SYSTEM = """
# Our Current Obsidian + Claude Code Setup

## Projects
1. **Content Hub** — AI content generation engine (FastAPI + Next.js + Supabase + Gemini)
   - ~95% complete, has RAG system, trending content scraping, video generation
2. **Brokerage Agent** — Dubai real estate AI platform (MVP Phase 3: Market Intelligence)
   - DLD transactions, rental yields, off-plan analysis, ROI calculations

## Parent CLAUDE.md (51 lines)
- Session start protocol (read context.md, detect project, read Decisions.md)
- Projects list, vault location, vault structure tree
- Hooks documentation, session logging rules

## Content Hub CLAUDE.md (107 lines — TOO LONG)
- Session protocol, stack info, current state, architecture decisions
- ALSO has: file structure tree (35 lines), design system colors, Supabase details, dev commands
- Much of this is static data that rarely changes

## Vault Structure (_vault/)
```
00-Meta/        Claude-Instructions.md, Home.md
01-Projects/    Content-Hub/ and Brokerage-Agent/ (Overview, Decisions, Tasks each)
02-Research/    Ideas and reference links
03-Daily/       Daily notes (YYYY-MM-DD.md)
04-Claude-Memory/  context.md (persistent user context), session-log.md
scripts/        load-vault.js (SessionStart hook)
```

## Hooks
- SessionStart: load-vault.js injects context.md, BOTH project Decisions.md, Claude-Instructions.md, last 30 lines of session-log
- Stop: reminds to log session + run /evolve-claude-md

## What Works
- Auto-injection of vault context at session start
- Single source of truth for tasks (vault Tasks.md)
- Numbered folder prefixes
- Proactive session logging rule
- Preference discovery rule

## Known Gaps
1. Content Hub CLAUDE.md is bloated (107 lines of mostly static data)
2. No "Active Context" section (current focus, open questions, blockers)
3. load-vault.js loads BOTH projects' context every time (wasteful)
4. Session log format doesn't capture learnings, gotchas, open questions
5. No frontmatter on vault files (no Dataview queries)
6. No dedicated Gotchas/Lessons file per project
7. No slash commands for session management (/standup, /wrap-up)
8. No anti-pattern tracking or goal grounding (North Star)
"""

# ── Communication log ──────────────────────────────────────────────────

communication_log = []

def log_exchange(system: str, role: str, content: str, tokens: int = 0):
    """Log a communication exchange."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "system": system,
        "role": role,
        "content": content[:3000],  # truncate for display
        "tokens_approx": tokens,
    }
    communication_log.append(entry)
    label = f"[{system}] {role}"
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")
    # Print first 500 chars as preview
    preview = content[:500] + ("..." if len(content) > 500 else "")
    print(preview)


def call_gemini(system_prompt: str, user_prompt: str, system_name: str) -> str:
    """Call Gemini and log the exchange."""
    log_exchange(system_name, "PROMPT (system)", system_prompt)
    log_exchange(system_name, "PROMPT (user)", user_prompt)

    start = time.time()
    for model in ("gemini-2.5-flash",):
        try:
            response = client.models.generate_content(
                model=model,
                contents=[
                    {"role": "user", "parts": [{"text": system_prompt + "\n\n" + user_prompt}]},
                ],
            )
            elapsed = time.time() - start
            result = response.text
            log_exchange(system_name, "RESPONSE", result, tokens=len(result.split()))
            print(f"\n  [Latency: {elapsed:.1f}s | ~{len(result.split())} words]")
            return result
        except Exception as e:
            print(f"  [ERROR with {model}: {e}]")
    return "(Gemini call failed)"


# ══════════════════════════════════════════════════════════════════════
# PHASE 1: NotebookLM — Extract & Synthesize Research
# ══════════════════════════════════════════════════════════════════════

print("\n" + "#"*70)
print("#  PHASE 1: NOTEBOOKLM — Research Analysis")
print("#  Feeding 4 research documents to Gemini for synthesis")
print("#"*70)

all_research = "\n\n---\n\n".join(
    f"## SOURCE: {name}\n{content}" for name, content in RESEARCH_DOCS.items()
)

notebooklm_system = """You are acting as NotebookLM — a research analysis engine.
You have been given 4 research documents about using Obsidian as a "second brain"
for AI coding assistants (specifically Claude Code).

Your job:
1. Cross-reference all 4 sources and find CONSENSUS patterns (things 3+ sources agree on)
2. Find UNIQUE innovations (ideas only 1-2 sources mention but are valuable)
3. Find CONTRADICTIONS between sources
4. Rank the top 15 actionable practices by impact

Output as structured markdown with clear sections. Be specific — cite which source
each finding comes from. Focus on PRACTICAL, IMPLEMENTABLE patterns."""

notebooklm_result = call_gemini(
    notebooklm_system,
    f"Analyze these 4 research documents:\n\n{all_research}",
    "NotebookLM"
)

# ══════════════════════════════════════════════════════════════════════
# PHASE 2: Gemini 2nd Brain — Apply to Our Specific Setup
# ══════════════════════════════════════════════════════════════════════

print("\n" + "#"*70)
print("#  PHASE 2: GEMINI 2nd BRAIN — Strategic Application")
print("#  Applying NotebookLM findings to our specific two-project setup")
print("#"*70)

brain_system = """You are a strategic AI architecture advisor — a "second brain" that
takes research findings and applies them to a SPECIFIC project setup.

You will receive:
1. NotebookLM's synthesized research findings (from Phase 1)
2. The current system architecture we're optimizing

Your job:
1. Map each high-impact finding to a SPECIFIC change in our system
2. For each change, provide: what file to modify, what to add/remove, and WHY
3. Prioritize changes by: effort (low/med/high) vs impact (low/med/high)
4. Flag any research findings that DON'T apply to our two-project setup and explain why
5. Identify our BIGGEST gap compared to best practices
6. Propose a concrete "Active Context" section template for our parent CLAUDE.md
7. Propose the exact load-vault.js changes for smart project detection
8. Design the session log format upgrade

Be extremely specific. Use real file paths from our system. Show exact code/content."""

brain_result = call_gemini(
    brain_system,
    f"## NotebookLM Research Findings\n{notebooklm_result}\n\n## Our Current System\n{OUR_CURRENT_SYSTEM}",
    "Gemini 2nd Brain"
)

# ══════════════════════════════════════════════════════════════════════
# PHASE 3: Gemini Critic — Challenge & Validate
# ══════════════════════════════════════════════════════════════════════

print("\n" + "#"*70)
print("#  PHASE 3: GEMINI CRITIC — Validation Pass")
print("#  Challenge the 2nd Brain's recommendations")
print("#"*70)

critic_system = """You are a skeptical code reviewer and systems architect.
You will receive a set of proposed changes to an Obsidian + Claude Code system.

Your job is to be the DEVIL'S ADVOCATE:
1. Which recommendations are over-engineered for a 2-project solo developer setup?
2. Which changes might HURT context efficiency (add tokens without proportional value)?
3. What's MISSING that none of the sources mentioned but is critical?
4. Are there simpler alternatives to any proposed changes?
5. What order should these changes be implemented in for maximum learning?

Be brutally honest. The goal is a lean, effective system — not a showcase of every
possible feature. A solo developer with 2 projects doesn't need the same setup as
an engineering manager with 20+ repos."""

critic_result = call_gemini(
    critic_system,
    f"## Proposed Changes (from 2nd Brain)\n{brain_result}\n\n## Current System\n{OUR_CURRENT_SYSTEM}",
    "Gemini Critic"
)

# ══════════════════════════════════════════════════════════════════════
# PHASE 4: Final Synthesis
# ══════════════════════════════════════════════════════════════════════

print("\n" + "#"*70)
print("#  PHASE 4: FINAL SYNTHESIS")
print("#  Combining all perspectives into actionable plan")
print("#"*70)

synthesis_system = """You are a technical project manager synthesizing three perspectives:
1. NotebookLM's research findings
2. 2nd Brain's strategic recommendations
3. Critic's challenges and concerns

Create the FINAL optimized plan. For each recommendation:
- State the change clearly (1-2 sentences)
- Show the EXACT content to write (markdown, code, or config)
- Note which perspective(s) supported it
- Mark priority: P0 (do now), P1 (do this week), P2 (nice to have)

The system has TWO projects:
- Content Hub (AI content engine, 95% done)
- Brokerage Agent (Dubai real estate AI, 80% done)

Output the final plan as a structured document with sections:
1. Parent CLAUDE.md changes
2. Content Hub CLAUDE.md changes
3. Vault file changes (new files, modifications)
4. load-vault.js changes
5. Session management upgrades
6. What NOT to do (over-engineering warnings)"""

final_result = call_gemini(
    synthesis_system,
    f"## NotebookLM Research\n{notebooklm_result[:2000]}\n\n## 2nd Brain Recommendations\n{brain_result[:2000]}\n\n## Critic Feedback\n{critic_result[:2000]}\n\n## Current System\n{OUR_CURRENT_SYSTEM}",
    "Final Synthesis"
)

# ══════════════════════════════════════════════════════════════════════
# OUTPUT: Full Communication Report
# ══════════════════════════════════════════════════════════════════════

print("\n" + "="*70)
print("  PIPELINE COMPLETE")
print(f"  Total exchanges: {len(communication_log)}")
print(f"  Total approx words processed: {sum(e['tokens_approx'] for e in communication_log)}")
print("="*70)

# Save full results to file
report = {
    "timestamp": datetime.now().isoformat(),
    "phases": {
        "notebooklm_research": notebooklm_result,
        "second_brain_application": brain_result,
        "critic_validation": critic_result,
        "final_synthesis": final_result,
    },
    "communication_log_summary": [
        {"system": e["system"], "role": e["role"], "words": e["tokens_approx"]}
        for e in communication_log
    ]
}

# Save as markdown for easy reading
report_path = os.path.join(os.path.dirname(__file__), "..", "_vault", "02-Research", "vault-optimization-research.md")
os.makedirs(os.path.dirname(report_path), exist_ok=True)

with open(report_path, "w", encoding="utf-8") as f:
    f.write("---\n")
    f.write(f"date: {datetime.now().strftime('%Y-%m-%d')}\n")
    f.write("type: research\n")
    f.write("topic: vault-optimization\n")
    f.write("sources: anthropic-official, chase-ai, railly-hugo, obsidian-mind\n")
    f.write("---\n\n")
    f.write("# Vault Optimization Research Report\n\n")
    f.write(f"*Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} via Gemini research pipeline*\n\n")
    f.write("---\n\n")
    f.write("## Phase 1: NotebookLM — Research Synthesis\n\n")
    f.write(notebooklm_result + "\n\n")
    f.write("---\n\n")
    f.write("## Phase 2: Gemini 2nd Brain — Strategic Application\n\n")
    f.write(brain_result + "\n\n")
    f.write("---\n\n")
    f.write("## Phase 3: Gemini Critic — Validation\n\n")
    f.write(critic_result + "\n\n")
    f.write("---\n\n")
    f.write("## Phase 4: Final Synthesis\n\n")
    f.write(final_result + "\n\n")

print(f"\nFull report saved to: {report_path}")
