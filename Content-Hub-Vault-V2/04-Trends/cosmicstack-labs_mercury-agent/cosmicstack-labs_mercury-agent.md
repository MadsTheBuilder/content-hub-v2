# cosmicstack-labs/mercury-agent

> Soul-driven AI agent with permission-hardened tools, token budgets, and multi-channel access. Runs 24/7 from CLI or Telegram.

**Language:** TypeScript · **Stars:** 2,130 · **Velocity:** 101.4/day · [GitHub](https://github.com/cosmicstack-labs/mercury-agent)

*Captured 2026-05-12*

---

## What problem does it solve?

Building AI agents that run continuously and securely is hard — most frameworks lack fine-grained permission controls, leaving tools exposed to misuse or runaway token costs. Mercury Agent solves this by combining permission-hardened tool access with token budgets, so the agent can run autonomously without burning through API credits or executing unsafe actions.

## How it works

Mercury Agent is a TypeScript-based AI agent that wraps its tools with permission layers, enforcing what actions can run and capping token usage per session or task. It exposes a multi-channel interface so the same agent logic can be triggered from a CLI or a Telegram bot, running persistently as a 24/7 process rather than a one-shot script.

## Best use cases

- A developer runs a personal AI assistant via Telegram that can execute tasks on their behalf with guardrails preventing accidental destructive actions
- A small team deploys a CLI-accessible agent with token budgets to automate research or triage tasks without surprise API bill spikes
- A solo founder builds a 'soul-driven' always-on agent with customizable permission profiles — allowing safe tools freely while requiring confirmation for sensitive ones

## Getting started

Clone the repo, configure your API keys and permission profiles in the TypeScript config, then run the agent from the CLI or connect it to a Telegram bot token for 24/7 access.