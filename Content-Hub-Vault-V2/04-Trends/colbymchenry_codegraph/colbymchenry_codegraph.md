# colbymchenry/codegraph

> Pre-indexed code knowledge graph for Claude Code, Codex, Gemini, Cursor, OpenCode, AntiGravity, Kiro, and Hermes Agent — fewer tokens, fewer tool calls, 100% local

**Language:** TypeScript · **Stars:** 35,269 · **Velocity:** 2272.7/day · [GitHub](https://github.com/colbymchenry/codegraph)

*Captured 2026-06-01*

---

## What problem does it solve?

AI coding assistants waste tokens and make excessive tool calls by re-reading and re-indexing your codebase on every session, slowing down responses and burning context window. Without a persistent knowledge graph, tools like Claude Code and Cursor have no memory of your repo's structure between sessions, forcing redundant exploration. This creates latency, higher API costs, and shallower code understanding.

## How it works

CodeGraph pre-indexes your entire codebase into a local knowledge graph — capturing symbols, relationships, and file structure — so AI agents can query it directly instead of crawling files at runtime. The graph is stored locally and reused across sessions, meaning agents get instant structural context with far fewer tool calls. It targets multiple AI runtimes (Claude Code, Codex, Gemini, Cursor, OpenCode, and others) through a shared interface.

## Best use cases

- Reducing token usage and API costs when working with large codebases across multiple AI coding sessions
- Giving AI agents accurate cross-file symbol and dependency awareness without live file traversal
- Speeding up onboarding for AI tools on an unfamiliar repo by providing a pre-built structural map

## Getting started

Clone the repo and run the indexer against your codebase to generate the local knowledge graph, then configure your AI tool (Claude Code, Cursor, etc.) to reference the graph output. Check the README for tool-specific integration instructions for your preferred AI runtime.