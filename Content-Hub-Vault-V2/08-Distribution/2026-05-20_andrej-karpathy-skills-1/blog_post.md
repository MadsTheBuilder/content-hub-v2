---
title: "andrej-karpathy-skills_1"
date: 2026-05-20
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# Andrej Karpathy on Claude Skills: The Agent Primitive Most Builders Are Missing

Karpathy called Claude Skills the cleanest agent primitive he's seen — and most people building agents in 2026 are still doing it the hard way.

## What a Skill Actually Is (Not What You Think)

A skill isn't a prompt. It isn't a tool either. It's a self-contained folder — a `SKILL.md` file plus any helper scripts — that the model *chooses to load* based on description matching. System prompt stays clean. Context only fills when relevant.

The composability is the thing. Every skill works with every other skill — zero integration code. Two skills written by two different people, never tested together, just work. That's not true of MCP servers, custom tools, or agent frameworks.

His comparison was precise: this is the Unix philosophy applied to AI. Small, composable, text-based units the OS routes intelligently. The model is the runtime. The folder is the program.

## The Real Shift

The surface read is convenience — "I don't have to write a tool definition." That's not the point.

The actual shift is that skills are the first abstraction where the model is the interpreter, not your code. Stop thinking like a software engineer for a second.

Side by side: 200 lines of MCP server boilerplate vs. a 15-line `SKILL.md` doing the same job. The `SKILL.md` wins on every axis — and it's easier to delete.

## Before/After: A Real Pipeline

My old content pipeline was 4 Python services, a Postgres queue, and ~2,400 lines of orchestration code. Rebuilt as 7 skills (`/researcher` → `/hook` → `/outline` → `/title` → `/cascade` → `/short-form` → `/voice-cleanup`), it's now a `.claude/skills/` folder plus ~600 lines of helper Python. Same output. **75% less code.** Faster to change.

The composition demo: type `/researcher`, then `/hook`. The second skill automatically reads what the first wrote because they share a vault path. No state machine. No handoff code. The model holds the thread.

You'd assume the win is speed. It isn't. The real win is that skills are *deletable*. Every framework punishes deletion. Skills don't. That asymmetry is what Karpathy was pointing at.

## Three Things You Can Do This Week

1. **Find one workflow you've automated as a Python script.** Convert it to a `SKILL.md` with a clear `description:` field. That field is the only thing the model uses to decide when to load it.
2. **Stop writing tool wrappers.** If your tool is "call X API and format the response," it's a skill, not a tool.
3. **Write skills like documentation, not like code.** The clearer your `SKILL.md` reads to a human, the better the model uses it.

Something I didn't expect: writing skills made me a better writer. The model reads `SKILL.md` like a person would, so ambiguous instructions fail visibly. My prose got tighter. My thinking got tighter. A file format taught me how to communicate more precisely.

## What This Means

If you're building agents and still hand-rolling tool wrappers, you're burning weeks reinventing what's now a folder with a markdown file. The teams shipping fastest switched primitives — not because they're smarter. They stopped treating the model as a function caller and started treating it as the runtime.

I spent six months in 2025 building a custom router, custom memory, and custom tool registry. Karpathy's post made me realize I'd built a worse version of something Anthropic shipped as a folder convention. I deleted ~70% of my own code the next weekend. Start with one skill. The rest follows.

---

Watch the full video for the live pipeline demo and the side-by-side `SKILL.md` vs. LangChain comparison: [VIDEO_LINK]