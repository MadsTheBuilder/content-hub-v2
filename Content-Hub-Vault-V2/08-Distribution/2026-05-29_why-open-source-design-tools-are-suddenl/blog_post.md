---
title: "Why open-source design tools are suddenly worth watching"
date: 2026-05-29
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# Why Open-Source Design Tools Are Suddenly Worth Watching

Most AI design tools lock you into their model, their interface, their pricing. Open Design doesn't. It runs on whatever coding agent you already have installed.

## What Open Design Actually Is

Open Design (`nexu-io/open-design`) is a local-first, open-source design system that generates web, desktop, and mobile prototypes, plus slides, images, videos, and HyperFrames. It ships with 19 skills and 71 brand-grade design systems out of the box. Exports to HTML, PDF, PPTX, and MP4 — all with a sandboxed preview before anything leaves your machine.

The headline isn't the feature list. It's the architecture underneath it.

## The Agent-Native Approach

Open Design doesn't bundle a proprietary AI model. It delegates the entire design loop — model calls, tool use, context management, permissions — to the coding agent CLI you already have installed.

From the docs:

> "OD's job is to detect it, feed it a skill + prompt + working directory, and stream its output back to the web UI."

That's the whole thing. The daemon does a PATH scan (`which <binary>`) and a config-dir probe (checking for `~/.claude/` or `~/.codex/`) on startup. If you have Claude Code, Codex, Cursor, Copilot, Qwen, or any of the other 16 supported agents installed, Open Design finds it and uses it.

This matters because it avoids the most common failure mode in AI tooling: a layer of indirection that buffers you from the model's actual capabilities. You're not using a wrapper around Claude. You're using Claude, with Open Design acting as the context layer.

## How Skill Injection Works

Once it detects your agent, Open Design negotiates what that agent can do — surgical edits, native skill loading, streaming format — then picks an injection strategy accordingly.

Three paths:

1. **Native skill loading** — For Claude Code, OD symlinks the skill directly into `~/.claude/skills/`. The agent treats it as a first-party skill.
2. **Prompt injection** — The skill instructions and design tokens get concatenated into the system prompt.
3. **File-placed workflow** — For Cursor, OD writes a `.cursorrules` file into the working directory.

The communication layer handles the normalization: `claude-stream-json` for Claude Code, `acp-json-rpc` for Devin and Kimi, `pi-rpc` for Pi, plain text for Qwen and DeepSeek. The UI shows live tool call streaming and a real-time progress card regardless of which agent is running.

The adapter logic lives in `apps/daemon/src/agents.ts`. Straightforward to read if you want to add your own.

## Why This Architecture Will Keep Winning

The standard approach in AI tooling is to build a vertical stack: one model, one interface, one workflow. It ships fast, but it creates lock-in. When the model improves or a better agent comes out, you're stuck until the tool vendor catches up.

Open Design's approach inverts this. The design system and skill layer stay stable. The agent underneath gets swapped or upgraded independently. If Codex gets meaningfully better next month, you switch adapters — the rest of your workflow is untouched.

It also means the tool improves every time your agent does. That's a compounding advantage most proprietary tools can't match.

## What This Means

If you're building with AI coding agents today, Open Design is worth a few hours of your time. Install it, point it at the agent you already use, and see whether the design system layer adds anything to your current workflow.

The project is early. Synthesis from the research pipeline failed on first pass, which usually means the documentation is still catching up with the code. Worth watching the repo closely over the next few months rather than betting a production workflow on it today.

The architecture is right. That's the thing to track.

---

Watch the full video for a walkthrough of the agent adapter layer and a live demo of skill injection across Claude Code and Cursor: [VIDEO_LINK]
