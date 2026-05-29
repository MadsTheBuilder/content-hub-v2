---
title: "Your Coding Agent Already Has a UI Designer Built In — You Just Don't Know It"
date: 2026-05-21
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# Your Coding Agent Already Has a UI Designer Built In — You Just Don't Know It

Most developers think UI design requires a separate tool, a separate workflow, and frankly, a separate person. Open Design disagrees — and its architecture makes a compelling argument.

## What Open Design Actually Is

Open Design is a local-first, open-source project that turns your existing coding agent CLI into a full design engine. No proprietary AI. No new subscription. It works with Claude Code, Codex, Cursor, Copilot, Qwen, Devin, and 10 more CLIs you probably already have installed.

The output side is broad: web, desktop, and mobile prototypes, slides, images, videos, and something called HyperFrames. Export targets include HTML, PDF, PPTX, and MP4. It ships with 19 design skills and 71 brand-grade design systems out of the box.

But the interesting part isn't the feature list — it's *how* it works.

## The Delegation Model

Open Design doesn't bundle its own AI agent. Instead, on startup, its daemon scans your PATH and probes config directories (`~/.claude/`, `~/.codex/`, etc.) to detect what you already have installed. Then it negotiates capabilities: can this agent do surgical edits? Does it support native skill loading? What streaming format does it output?

Once it knows, it delegates *everything* — model calls, tool use, context management, permission handling — to your existing CLI. The daemon's job is to detect the agent, feed it a skill prompt and a working directory, and stream the output back to a web UI.

From the architecture docs:

> "We delegate the entire agent loop... to the user's existing code agent CLI. OD's job is to detect it, feed it a skill + prompt + working directory, and stream its output back to the web UI."

This is a genuinely different philosophy from most AI design tools, which want to own the model layer. Open Design treats your CLI as the engine and positions itself as the orchestration and UI layer on top.

## How It Injects Design Context

Teaching an agent to design requires more than a prompt. Open Design uses three strategies depending on what the agent supports:

- **Native skill loading**: For Claude Code, it symlinks the design skill directly into `~/.claude/skills/`, so the agent treats it as a first-class skill.
- **Prompt injection**: Skill instructions and design system tokens get concatenated into the system prompt.
- **File-placed workflow**: For Cursor, it writes `.cursorrules` into the project directory.

The adapter layer (in `apps/daemon/src/agents.ts`) handles the per-agent differences. Each supported CLI gets a dedicated adapter that knows its command-line arguments and output format. Claude Code outputs `claude-stream-json`. Devin uses `acp-json-rpc`. Qwen and DeepSeek output plain text. The daemon normalizes all of it so the UI sees a consistent stream.

## The Design System Layer

The 71 bundled design systems are more than templates — they're structured `DESIGN.md` files containing brand tokens (colors, typography, spacing) that get injected alongside the skill prompt. Every generated prototype is grounded in a specific design system, which keeps output consistent across a project.

This is what separates it from just asking Claude to "make a UI." The agent isn't making aesthetic decisions from scratch — it's executing against a defined token set.

## What This Means for Your Workflow

If you already use Claude Code or Cursor, Open Design is additive with no new model costs. You're already paying for (or using) the agent — this just gives it design skills and a structured output layer.

The practical implication: prototyping a new feature no longer requires context-switching to Figma or a separate design session. You describe what you want, pick a design system, and let your existing CLI generate a sandboxed HTML preview.

It's still early — the synthesis from the research notes hit limits, and some parts of the architecture are more documented than battle-tested. But the core idea is sound: coding agents are already capable of producing structured UI output. Open Design is a harness that makes that repeatable.

Watch the full video for a live walkthrough: [VIDEO_LINK]
