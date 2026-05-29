# Instagram Carousel

**Slide 1:**
Your coding agent is already a UI designer.
Open Design just proves it.

---

**Slide 2:**
Most AI design tools bundle their own agent.
Open Design does the opposite — it detects the CLI already on your machine and hands it the wheel.

Claude Code. Cursor. Codex. Devin. Copilot. 16 supported agents total.

---

**Slide 3:**
On startup, the daemon runs a PATH scan + config-dir probe (`~/.claude/`, `~/.codex/`) to find what you have installed.

Then it negotiates: can this agent do surgical edits? Does it support native skill loading? What streaming format does it speak?

Zero config. It just finds your tools.

---

**Slide 4:**
Skill injection is where it gets precise.

For Claude Code → symlinks the skill into `~/.claude/skills/`
For Cursor → writes `.cursorrules` into the project directory
For everything else → prompt injection

Each agent gets taught the same design task in the way it natively understands.

---

**Slide 5:**
What it actually builds:

71 brand-grade design systems. 19 design skills. Web + desktop + mobile prototypes, slides, images, videos.
Export to HTML, PDF, PPTX, or MP4.

All output runs in a sandboxed preview before it ever touches your filesystem.

---

**Slide 6:**
The architecture quote that says it all:

> "The daemon makes the agent feel like it's on your laptop."

No cloud lock-in. No proprietary model. The agent loop — model calls, tool use, context, permissions — stays entirely with your existing CLI.

---

**Slide 7:**
If you're already running Claude Code or Cursor, you're one install away from a full design engine.

Watch the full video: [VIDEO_LINK]

---

#OpenSource #DeveloperTools #AITools #ClaudeCode #BuildInPublic
