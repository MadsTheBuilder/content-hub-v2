---
title: "Why open-source design tools are suddenly worth watching"
date: 2026-05-29
youtube_url: "[VIDEO_LINK]"
duration: 90s
---

```
**SPOKEN SCRIPT:**

Your coding agent is already a design tool. You just don't know it yet.

Most design tools have the same problem. They're isolated. They live in a browser tab, they bundle their own AI, and when you need actual code, you copy-paste and pray. The gap between design and development is a workflow tax on every project.

Open Design fixes this differently. It has no bundled AI. None. Instead, it scans your machine for whatever coding agent CLIs you already have installed — Claude Code, Cursor, Codex, Copilot — and delegates the entire design loop to them. The docs say it plainly: "We delegate the entire agent loop — model calls, tool use, context management — to the user's existing code agent CLI."

Here's what that looks like in practice. You start Open Design. Its daemon runs a PATH scan, finds Claude Code on your machine, negotiates capabilities — can it do surgical edits, does it support native skill loading — then spawns it with a design-specific SKILL.md and a DESIGN.md containing your brand tokens. The agent produces real HTML prototypes directly. No export step. No translation layer.

It supports 16 CLI agents right now. Each gets normalized output parsing — so whether you're running Claude Code, Devin, or Qwen, the web UI shows live progress identically.

Open source. GitHub: nexu-io/open-design. If you're already on Claude Code or Cursor, you're one install away from prototypes that live inside your actual codebase.

---

**TEXT OVERLAYS:**
- "No bundled AI. Your agent does the work."
- "PATH scan → detect → delegate"
- "16 CLI agents supported"
- "nexu-io/open-design"

---

**CAPTION:**
Open Design has no AI of its own — it detects Claude Code, Cursor, or Codex on your machine and uses that as the design engine. Your coding agent was already capable. It just needed the right prompt.
```
