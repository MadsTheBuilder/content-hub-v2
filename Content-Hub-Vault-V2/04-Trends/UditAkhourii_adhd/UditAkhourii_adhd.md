# UditAkhourii/adhd

> ADHD — a skill for coding agents. Tree-of-thought with pruning, built on the Claude & Codex Agent SDK. Fans out parallel divergent thoughts under different cognitive frames, scores, prunes traps, deepens the survivors. The no-brainer skill for creative and interdisciplinary work.

**Language:** TypeScript · **Stars:** 627 · **Velocity:** 125.4/day · [GitHub](https://github.com/UditAkhourii/adhd)

*Captured 2026-05-31*

---

## What problem does it solve?

AI coding agents often get stuck in linear thinking, failing to explore creative or unconventional solutions to hard problems. When a problem requires cross-domain insight or divergent reasoning, single-path agents miss non-obvious answers and fall into common reasoning traps. ADHD gives agents a structured way to fan out multiple competing thought lines simultaneously and kill dead ends before wasting compute.

## How it works

The skill implements a tree-of-thought algorithm where multiple divergent thoughts are spawned in parallel, each evaluated under a different cognitive frame. A scoring and pruning step eliminates low-value branches, then survivors are deepened — iterating until a confident answer emerges. It is built on the Claude and Codex Agent SDK and ships as a TypeScript skill that can be dropped into compatible coding agents.

## Best use cases

- Solving architecture decisions where multiple valid approaches exist and trade-offs are non-obvious
- Debugging hard-to-reproduce bugs that may have several unrelated root causes
- Generating creative feature ideas or API designs that benefit from interdisciplinary thinking

## Getting started

Since it targets the Claude and Codex Agent SDK, a developer would install the skill package into their TypeScript agent project and invoke it as a skill — likely via a slash command or skill registration — passing the problem statement and letting the tree-of-thought loop run.