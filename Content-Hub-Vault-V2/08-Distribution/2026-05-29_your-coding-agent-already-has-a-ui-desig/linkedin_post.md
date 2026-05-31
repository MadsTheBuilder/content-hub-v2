# LinkedIn Post

Open Design doesn't add another AI to your stack. It turns the coding agent you're already running into a UI designer.

The architecture is what makes this interesting:

- Scans your PATH at startup and detects whatever CLI you have installed — Claude Code, Cursor, Codex, Devin. No manual config. Presence detection plus a capability negotiation pass.

- Your agent gets a skill file, a design system token set (71 brand-grade options included), and a sandboxed working directory. OD streams the output back to a web UI. The agent loop stays entirely yours.

- Different agents speak different protocols. Claude Code outputs `claude-stream-json`. Devin uses ACP JSON-RPC. Qwen sends plain text. OD normalizes all of it into a live progress feed.

- Skill injection adapts per agent: symlink into `~/.claude/skills/` for Claude Code, `.cursorrules` for Cursor, stdin for Codex. The right strategy fires automatically.

- Outputs are real artifacts — HTML, PDF, PPTX, MP4, sandboxed preview. Not mockups that stop at the screenshot.

Which agent CLI are you running day-to-day, and would you trust it for design work if the scaffolding was already handled?

#OpenSource #DeveloperTools #AITools #DesignSystems #BuildInPublic
