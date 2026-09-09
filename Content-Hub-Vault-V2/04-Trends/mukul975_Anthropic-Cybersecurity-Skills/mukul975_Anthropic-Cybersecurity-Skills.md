# mukul975/Anthropic-Cybersecurity-Skills

> 754 structured cybersecurity skills for AI agents · Mapped to 5 frameworks: MITRE ATT&amp;CK, NIST CSF 2.0, MITRE ATLAS, D3FEND &amp; NIST AI RMF · agentskills.io standard · Works with Claude Code, GitHub Copilot, Codex CLI, Cursor, Gemini CLI &amp; 20+ platforms · 26 security domains · Apache 2.0

**Language:** Python · **Stars:** 12,913 · **Velocity:** 773.9/day · [GitHub](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)

*Captured 2026-06-01*

---

## What problem does it solve?

AI coding agents lack structured, standardized security knowledge — they can write code but don't natively understand attack patterns, defense frameworks, or compliance mappings. Security teams and developers using AI tools have no common skill vocabulary to instruct agents on cybersecurity tasks, leading to inconsistent and unreliable security-aware automation.

## How it works

The repo provides 754 pre-structured cybersecurity skills formatted to the agentskills.io standard, each mapped to one or more of five industry frameworks: MITRE ATT&CK (offense), MITRE ATLAS (AI-specific threats), D3FEND (defense), NIST CSF 2.0, and NIST AI RMF. These skills are Python-based and designed to be loaded directly into AI agent runtimes, giving platforms like Claude Code, Copilot, or Cursor a shared, framework-aligned security capability layer across 26 security domains.

## Best use cases

- A developer building a secure code review pipeline can load relevant ATT&CK-mapped skills into Claude Code so the agent flags vulnerabilities using standardized threat taxonomy
- A security engineer can use NIST CSF 2.0-aligned skills to automate compliance gap analysis across a codebase with any of the 20+ supported AI platforms
- A red team researcher can pull MITRE ATLAS skills to test AI-specific attack surfaces — prompt injection, model evasion — with structured, reusable agent primitives

## Getting started

Clone the repo, browse the 754 skills organized by domain and framework mapping, then import the relevant Python skill files into your AI agent platform using the agentskills.io standard — most major platforms (Claude Code, Cursor, Codex CLI) are already supported out of the box.