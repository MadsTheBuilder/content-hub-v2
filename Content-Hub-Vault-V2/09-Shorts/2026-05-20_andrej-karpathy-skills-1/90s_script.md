**SPOKEN SCRIPT:**

The model is the runtime. The folder is the program. Karpathy said this publicly and most builders still haven't processed it.

If you're building agents in 2026 and still writing tool wrappers and orchestration code, you're rebuilding something Anthropic already shipped as a folder convention. A `.claude/skills/` directory and a markdown file. The teams moving fastest didn't get smarter — they switched primitives.

A skill isn't a prompt. It's not a tool either. It's a third thing — a self-contained folder the model chooses to load when the description matches your intent. System prompt stays clean. Context only loads when it's needed. And the part Karpathy actually emphasized: every skill composes with every other skill, zero integration code. Two skills written by different people, never tested together, and they just work. MCP servers can't say that. Agent frameworks can't say that.

Here's the number that made it real for me. My content pipeline was 4 Python services, a Postgres queue, and 2,400 lines of orchestration code. I rebuilt it as 7 skills — researcher, hook, outline, title, cascade, short-form, voice cleanup. Six hundred lines of helper Python. Same output, 75% less code. You type `/researcher`, then `/hook`, and the second skill automatically reads what the first wrote. No handoff logic. The model holds the thread.

This week: find one Python script you run manually. Write a 15-line SKILL.md for it. The `description` field is the only thing that determines when the model loads it. Start there.

---

**TEXT OVERLAYS:**
"Model = runtime. Folder = program."
"2,400 lines → 600 lines"
"75% less code. Same output."
"`description:` is the only field that matters"

**CAPTION:**
Karpathy called Claude Skills the cleanest agent primitive he's seen. Here's what that actually changes about how you build — and the one file you should write this week.