# 2aronS/Duel-Agents

> CLI, SDK, and IDE plugins for Duel Agents

**Language:** TypeScript · **Stars:** 495 · **Velocity:** 247.5/day · [GitHub](https://github.com/2aronS/Duel-Agents)

*Captured 2026-05-31*

---

## What problem does it solve?

Building and testing multi-agent AI systems is fragmented across tools, making it hard to orchestrate, compare, or pit agents against each other in a structured way. Developers lack a unified interface — CLI, programmatic SDK, and IDE-level tooling — to work with competing or collaborating agent pipelines from a single cohesive surface.

## How it works

Duel Agents provides a TypeScript SDK as the core runtime, a CLI for running and inspecting agent matchups from the terminal, and IDE plugins that bring agent orchestration into the editor. The 'duel' model implies two or more agents can be run in parallel against the same input, with their outputs compared or adjudicated programmatically.

## Best use cases

- Evaluating two LLM prompt strategies head-to-head on the same task to pick the better performer
- Integrating multi-agent workflows directly into a TypeScript/Node.js application via the SDK
- Running agent duels from the terminal in CI pipelines to regression-test AI behavior across model versions

## Getting started

Install the package via npm or your preferred Node.js package manager, then use the CLI to run your first agent duel or import the SDK into a TypeScript project to wire agents programmatically.