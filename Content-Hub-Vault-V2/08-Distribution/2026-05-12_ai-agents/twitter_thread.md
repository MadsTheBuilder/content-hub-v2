# Twitter Thread

**Tweet 1:** Forget the "conversational partner." Treat your LLM as a shitty, unreliable general-purpose computer. It fundamentally changes how you engineer production agent systems. ðŸ§µ

**Tweet 2:** Context is the ultimate constraint. Models start losing focus and detail around 100k tokens, regardless of max window size. This "context degradation" cripples agent performance.

**Tweet 3:** Combat context rot with surgical updates. Use `jq` to modify specific fields in JSON state files. Don't re-write entire documents; it wastes tokens and reduces errors.

**Tweet 4:** Minimalist prompts win. "Spaceship" prompts over 10,000 tokens often confuse the model. Effective agents thrive on system prompts under 1,000 tokens. Focus clarity over verbosity.

**Tweet 5:** For tool integration, CLI/Bash tools are often superior to MCP. They offer higher token efficiency, composability via pipes, and are 39% more cost-effective for complex tasks.

**Tweet 6:** Resist feature bloat. A production-ready coding agent only needs four core tools: `bash`, `read_file`, `write_to_file`, and `edit_file` (with linetags/search-replace).

**Tweet 7:** In development environments, skip permission prompts. "YOLO mode" â€” give your agent monitored, unrestricted filesystem and network access. Production efficiency demands it.

**Tweet 8:** Externalize agent plans. Avoid built-in "Plan Modes." Force the agent to maintain a `TODO.md` or `PLAN.md`. This ensures persistence, transparency, and version control.

**Tweet 9:** Building robust LLM agents means applying traditional engineering rigor to non-deterministic systems. Focus on efficiency, explicit state, and minimal reliable tools. [VIDEO_LINK]
