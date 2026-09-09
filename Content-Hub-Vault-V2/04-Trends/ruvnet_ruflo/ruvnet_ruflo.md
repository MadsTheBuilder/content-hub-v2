# ruvnet/ruflo

> 🌊 The leading agent orchestration platform for Claude. Deploy intelligent multi-agent swarms, coordinate autonomous workflows, and build conversational AI systems. Features enterprise-grade architecture, self-learning swarm intelligence, RAG integration, and native Claude Code / Codex Integration

**Language:** TypeScript · **Stars:** 56,918 · **Velocity:** 767.9/day · [GitHub](https://github.com/ruvnet/ruflo)

*Captured 2026-06-01*

---

## What problem does it solve?

Building multi-agent AI systems requires coordinating multiple LLMs, managing state across autonomous workflows, and handling enterprise-scale reliability — all of which are painful to wire from scratch. Ruflo solves this by providing a production-ready orchestration layer specifically designed for Claude-based agent swarms, so developers don't have to reinvent the coordination infrastructure.

## How it works

Ruflo exposes an orchestration platform built in TypeScript that lets developers define agent roles, spawn swarms of Claude instances, and wire them into conversational or autonomous pipelines. It includes RAG integration for knowledge retrieval, self-learning swarm intelligence for adaptive behavior, and native Claude Code / Codex hooks for code-aware agents.

## Best use cases

- Deploying a customer support swarm where specialized sub-agents handle billing, technical, and escalation tiers autonomously
- Building a research pipeline where agents decompose a question, search knowledge bases in parallel, then synthesize a final answer
- Orchestrating a code review workflow where separate agents audit security, performance, and style — then a coordinator agent merges findings

## Getting started

A developer would clone the repo, install TypeScript dependencies, and define an agent swarm config pointing at their Anthropic API key — the platform handles spawning, routing, and state management from there.