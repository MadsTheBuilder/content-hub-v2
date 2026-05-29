# Manavarya09/design-extract

> Extract any website's complete design system with one command. DTCG tokens, semantic+primitive+composite, MCP server for Claude Code/Cursor/Windsurf, multi-platform emitters (iOS SwiftUI, Android Compose, Flutter, WordPress), Tailwind v4, Figma variables, shadcn/ui, CSS health audit, WCAG remediation, Chrome extension. MIT, Playwright, Node 20+.

**Language:** JavaScript · **Stars:** 2,488 · **Velocity:** 92.1/day · [GitHub](https://github.com/Manavarya09/design-extract)

*Captured 2026-05-12*

---

## What problem does it solve?

Manually extracting and replicating a website's design system is tedious and error-prone, requiring developers to inspect colors, typography, spacing, and components one by one. This tool automates the entire extraction process, giving developers a complete, standards-compliant design system from any website in a single command.

## How it works

It uses Playwright to crawl a target website and extract design tokens (colors, typography, spacing, etc.) in the DTCG (Design Token Community Group) format, organized into primitive, semantic, and composite layers. The extracted tokens are then emitted to multiple platform formats including iOS SwiftUI, Android Compose, Flutter, Tailwind v4, Figma variables, and shadcn/ui, and also exposed via an MCP server for direct use inside AI-powered editors like Claude Code, Cursor, and Windsurf.

## Best use cases

- Reverse-engineer a competitor's or client's design system to bootstrap a matching UI
- Audit an existing site's CSS for health issues and WCAG accessibility violations, then get automated remediation suggestions
- Generate platform-specific token files (Swift, Kotlin, Dart) from a web design system to keep mobile and web in sync

## Getting started

Install via npm with Node 20+ and run the CLI against any URL to get a full DTCG token export. To use inside Claude Code or Cursor, configure the bundled MCP server so the AI assistant can query design tokens directly during development.