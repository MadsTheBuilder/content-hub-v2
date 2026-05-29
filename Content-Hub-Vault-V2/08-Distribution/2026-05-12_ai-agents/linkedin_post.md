# LinkedIn Post

Forget treating LLMs as clever chatbots. See them as unreliable, slow general-purpose computers. This shift is crucial for building production-ready LLM systems.

Here's how to engineer for reliability and efficiency:

*   **Context isn't infinite.** Beyond ~100k tokens, models lose details. Use `jq` to surgically update JSON state files rather than reloading entire documents for every minor change.

*   **CLI tools often beat Model Context Protocol (MCP) servers.** Benchmarks show well-designed CLI tools can be 39% more cost-effective for complex tasks, avoiding MCP's context-bloating JSON-RPC overhead.

*   **Embrace minimalist agent design.** An effective agent needs only `bash`, `read_file`, `write_to_file`, and `edit_file`. Force the agent to maintain `TODO.md` or `PLAN.md` files; plans must be version-controlled, not ephemeral context.

*   **Develop in "YOLO mode" (with monitoring).** In dev environments, constant permission prompts are "security theater." Granting unrestricted (but monitored) filesystem access allows for far more efficient iteration.

What's one counter-intuitive principle you've adopted for building stable LLM agents?

#AIAgents #LLMEngineering #DeveloperProductivity #SoftwareArchitecture #BuildInPublic
