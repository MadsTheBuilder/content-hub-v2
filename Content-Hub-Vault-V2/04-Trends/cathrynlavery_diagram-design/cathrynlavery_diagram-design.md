# cathrynlavery/diagram-design

> 38 editorial diagram types for Claude Code, Codex, and Pi. Self-contained HTML + SVG. No shadows. No Mermaid slop.

**Language:** HTML · **Stars:** 35,602 · **Velocity:** 1026.6/day · [GitHub](https://github.com/cathrynlavery/diagram-design)

*Captured 2026-09-09*

---

## What problem does it solve?

Developers using AI coding assistants (Claude Code, Codex, Pi) often need to visually explain architecture, flows, or systems to teammates or stakeholders, but default diagram tools produce generic, cluttered visuals (Mermaid-style boxes, drop shadows, cookie-cutter styling) that look unpolished and don't fit editorial or documentation contexts.

## How it works

It's a library of 38 diagram types built as self-contained HTML files with embedded SVG, meaning each diagram is a standalone, portable artifact with no external dependencies or rendering services required. AI coding agents can generate or fill in these templates directly as part of their output, producing clean, editorial-style visuals instead of relying on Mermaid or similar auto-layout diagramming syntax.

## Best use cases

- Generating architecture and system-design diagrams directly from AI coding assistant sessions for documentation
- Producing polished, presentation-ready visuals for technical blog posts or READMEs without a separate design tool
- Embedding lightweight, dependency-free diagrams into internal docs or wikis where Mermaid's default styling feels too generic

## Getting started

Clone the repo and reference the relevant self-contained HTML/SVG diagram template directly in a prompt to Claude Code, Codex, or Pi, letting the agent populate it with project-specific content.