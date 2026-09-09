# multica-ai/andrej-karpathy-skills

> A single CLAUDE.md file to improve Claude Code behavior, derived from Andrej Karpathy's observations on LLM coding pitfalls.

**Language:** — · **Stars:** 163,335 · **Velocity:** 2169.2/day · [GitHub](https://github.com/multica-ai/andrej-karpathy-skills)

*Captured 2026-06-01*

---

## What problem does it solve?

Claude Code and similar AI coding assistants often fall into well-documented failure modes: adding unrequested features, over-engineering simple solutions, making sweeping refactors when a surgical fix was asked for, and silently picking one interpretation of an ambiguous request. These pitfalls were observed and catalogued by Andrej Karpathy, whose credibility in the ML community makes the list authoritative. Developers lose trust in AI pair-programmers when the assistant does more than asked — this repo addresses that directly.

## How it works

A CLAUDE.md file placed in a project root is read by Claude Code at every session start, acting as persistent behavioral instructions that override defaults. This single file encodes Karpathy's anti-patterns as explicit guardrails — rules like 'don't add features beyond what was asked', 'surface ambiguity before acting', and 'touch only what you must'. Because it's just a Markdown file checked into the repo, the behavioral rules travel with the codebase and apply to every collaborator using Claude Code.

## Best use cases

- Drop it into any existing project to immediately constrain Claude Code to surgical, minimal diffs instead of sweeping rewrites
- Use it as a template or starting point for writing your own team-specific CLAUDE.md behavioral contract
- Study it as a concise, practitioner-validated list of LLM coding failure modes to inform prompt design in your own AI tooling

## Getting started

Copy the CLAUDE.md file into the root of your project repository — Claude Code will automatically read it at session start and apply the behavioral rules to every subsequent request in that project.