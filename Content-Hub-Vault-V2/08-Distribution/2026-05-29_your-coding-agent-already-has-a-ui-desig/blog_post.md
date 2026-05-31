---
title: "Your Coding Agent Already Has a UI Designer Built In — You Just Don't Know It"
date: 2026-05-29
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# Your Coding Agent Already Has a UI Designer Built In — You Just Don't Know It

You've been running Claude Code or Cursor for months and never generated a production UI prototype with it. Not because you can't — because you didn't know Open Design existed.

## The Tool You Probably Missed

[Open Design](https://github.com/nexu-io/open-design) is a local-first, open-source design layer that sits on top of whatever coding agent CLI you already have installed. It doesn't replace your agent — it feeds work to it.

It ships with 19 design skills and 71 brand-grade design systems. From one prompt it can output HTML pages, desktop apps, mobile prototypes, slides, images, videos, and something it calls HyperFrames. Everything exports to HTML, PDF, PPTX, or MP4 out of a sandboxed preview environment.

That's a lot of surface area from a single `npm install`.

## How It Actually Works

Open Design runs a local daemon. When it starts, it does a PATH scan and a config-dir probe — looking for binaries like `claude`, `codex`, `cursor-agent` and directories like `~/.claude/` or `~/.codex/`. It finds what you already have, and then it uses it.

That's the key design decision here. Open Design has no bundled AI engine. The docs put it plainly:

> "We delegate the entire agent loop — model calls, tool use, context management, permission handling, resume, cancel — to the user's existing code agent CLI."

So the daemon spawns your agent as a child process, sets the working directory to `.od/projects/<id>/`, and passes it a composed prompt: the design task instructions (`SKILL.md`), the brand tokens (`DESIGN.md`), and project metadata. Your agent does the actual work. Open Design just streams the output back to its web UI.

## 16 Agents, One Integration Pattern

The adapter layer in `apps/daemon/src/agents.ts` handles 16 CLIs, all with different communication formats:

- Claude Code uses `claude-stream-json`
- Devin and Hermes use `acp-json-rpc`
- Qwen and DeepSeek use plain text

The daemon normalizes all of these into a single stream so the UI can show live tool call progress regardless of which agent is running.

Skill injection also varies by what the agent supports. For Claude Code, Open Design symlinks the design skill directly into `~/.claude/skills/` — native skill loading. For Cursor, it writes a `.cursorrules` file into the project directory. For agents without either, it concatenates the skill instructions into the system prompt. The agent gets the context it needs, and the delivery mechanism adapts to what that agent actually supports.

Claude Code is the reference implementation — it's the only agent that gets both native skill loading and surgical edit support out of the box.

## What This Means

If you run Claude Code, Codex, or Cursor, you can point Open Design at an existing project and start generating UI artifacts today. No new AI subscription. No tool switching.

The reason this matters: UI prototyping no longer needs a separate Figma handoff step. Your agent generates the prototype directly into the codebase, in the same working directory, using the same brand tokens you configure once. That's it.

Check your PATH. You probably already have what you need.

---

Watch the full video for a walkthrough of the setup and a live prototype generation from scratch: [VIDEO_LINK]
