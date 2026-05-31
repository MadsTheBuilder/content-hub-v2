# LinkedIn Post

Open Design doesn't ship its own AI. It uses whichever coding agent you already have installed.

That's a design decision worth understanding.

- It scans your PATH on startup and detects Claude Code, Codex, Cursor, Copilot, Devin — 16 agents total. Whichever is present becomes the design engine.

- The agent gets a composed prompt: a `SKILL.md` with task instructions + a `DESIGN.md` with brand tokens. For Claude Code, it symlinks the skill directly into `~/.claude/skills/`. For Cursor, it writes `.cursorrules` into the working directory.

- Output formats vary wildly across agents (`claude-stream-json`, `acp-json-rpc`, plain text). Open Design normalizes all of them so the UI shows a live progress card regardless of which agent is running underneath.

- The stated reason: existing coding agents are already optimized for filesystem ops and tool use. Rebuilding that from scratch would just produce a worse version.

This "bring your own agent" pattern is showing up in more tools. It sidesteps the model-lock problem entirely and lets teams standardize on whatever CLI already fits their workflow.

Curious whether this is actually practical in team settings — do you want every developer running a different agent underneath the same design tool, or does that fragmentation create its own problems?

#DeveloperTools #AI #OpenSource #AgentNative #BuildInPublic
