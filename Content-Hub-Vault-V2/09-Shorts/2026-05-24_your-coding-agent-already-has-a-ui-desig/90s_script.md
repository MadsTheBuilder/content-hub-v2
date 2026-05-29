---
title: "Your Coding Agent Already Has a UI Designer Built In — You Just Don't Know It"
date: 2026-05-24
youtube_url: "[VIDEO_LINK]"
duration: 90s
---

```
**SPOKEN SCRIPT:**

Claude Code can design your UI. You just haven't pointed it at the right tool yet.

Most developers treat design as a separate phase — Figma, handoff, then code. That gap costs hours. And every AI design tool that's shipped this year bundles its own model, which means you're learning a new agent on top of the one you already have.

Open Design solves this differently. It's a local-first, open-source design platform that ships zero AI of its own. When the daemon starts, it scans your PATH and config directories — looking for ~/.claude/, ~/.codex/, .cursorrules support — and detects whatever coding agent you already have installed. Then it hands that agent the design task. Your tool. Your model. Your context. Open Design just feeds it the skill definition and your brand tokens.

Under the hood: the daemon spawns your CLI, sets the working directory to .od/projects/id/, and injects two files — a SKILL.md describing the design task and a DESIGN.md containing your brand system tokens. For Claude Code specifically, it symlinks the skill directly into ~/.claude/skills/, so Claude treats it as a native command. Live progress streams back to the web UI in real time. The agent thinks it's running on your laptop. Because it is.

Sixteen agents supported right now — Claude Code, Cursor, Codex, Copilot, Devin. GitHub link in bio. Star the repo.

**TEXT OVERLAYS:**
- "Open Design — ships zero AI of its own"
- "Daemon scans PATH → detects your CLI"
- "Injects SKILL.md + DESIGN.md → your agent executes"
- "16 agents supported"

**CAPTION:**
Open Design doesn't bundle its own AI — it uses whichever coding agent you already have installed. The daemon detects it, feeds it the task, and streams output back live.
```
