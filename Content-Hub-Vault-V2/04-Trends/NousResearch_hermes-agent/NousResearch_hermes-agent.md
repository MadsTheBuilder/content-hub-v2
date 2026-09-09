# NousResearch/hermes-agent

> The agent that grows with you

**Language:** Python · **Stars:** 243,586 · **Velocity:** 603.0/day · [GitHub](https://github.com/NousResearch/hermes-agent)

*Captured 2026-09-09*

---

## What problem does it solve?

Developers need conversational agents that can retain context and improve their behavior across sessions instead of resetting to a blank slate every time, and building that persistence layer from scratch is repetitive, error-prone work. hermes-agent packages that adaptive, memory-driven agent loop into a reusable Python framework so teams don't have to reinvent it for every project.

## How it works

It runs an agent loop written in Python that wraps LLM calls with a persistent memory/state layer, letting the agent accumulate context, feedback, and learned behavior over time rather than starting fresh each run. This is exposed as a library/framework other applications can import and extend, with the memory and growth mechanics as the core differentiator over a plain prompt-response wrapper.

## Best use cases

- Long-running personal or team assistants that need to remember user preferences and past interactions across sessions
- Customer support or onboarding bots that improve their responses as they accumulate more conversation history
- Research or coding agents that build up project-specific context over many iterative tasks instead of re-explaining state each time

## Getting started

Clone the NousResearch/hermes-agent repo, install its Python dependencies, and follow the README to configure an LLM backend and initialize the agent's memory store before running your first session.