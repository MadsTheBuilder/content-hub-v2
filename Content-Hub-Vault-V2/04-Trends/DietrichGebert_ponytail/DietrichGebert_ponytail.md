# DietrichGebert/ponytail

> Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote.

**Language:** JavaScript · **Stars:** 132,612 · **Velocity:** 1799.7/day · [GitHub](https://github.com/DietrichGebert/ponytail)

*Captured 2026-09-09*

---

## What problem does it solve?

Developers routinely over-engineer solutions—adding abstractions, config options, and speculative flexibility for requirements that don't exist yet. This bloats codebases, slows reviews, and creates maintenance burden for code nobody needed. Ponytail nudges toward the simplest thing that works instead.

## How it works

It acts as a behavioral layer (system prompt/rules) that an AI coding agent follows: before writing code, it climbs a priority ladder—question if the code needs to exist, check for existing reuse, stdlib, native platform features, and installed dependencies—before allowing new code. It also enforces surgical diffs and flags deliberate simplifications with explicit comments naming their ceiling.

## Best use cases

- Enforcing lean, no-frills output from AI coding assistants on a team to reduce PR bloat
- Auditing existing codebases for unnecessary abstractions, unused config, and over-engineered patterns
- Onboarding AI agents into legacy codebases where reuse of existing helpers/utilities matters more than writing new code

## Getting started

Drop the Ponytail instructions/config into your AI coding agent's system prompt or rules file (e.g., CLAUDE.md or equivalent) and toggle intensity levels (lite/full/ultra) to control how aggressively it pushes back on unnecessary code.