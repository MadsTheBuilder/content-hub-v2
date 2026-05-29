Andrej Karpathy called Claude Skills the cleanest agent primitive he's seen. Most builders haven't figured out what that actually means yet.

Here's the shift:

- Skills aren't prompts. They're not tools. They're a third thing — capabilities the model *chooses* to load based on a description field. Context stays clean. No framework ceremony.

- The composability is the surprising part. Two skills written by two different people, never tested together, just work. No integration code. That's not true of MCP servers, LangChain agents, or anything else in the stack.

- The model is the runtime. The folder is the program. Once that clicked for me, I rebuilt my entire content pipeline — 4 Python services and ~2,400 lines of orchestration code became 7 skill files and ~600 lines of helper Python. Same output.

- The real win isn't speed. It's that skills are trivially deletable. Every framework I've used punishes deletion. Skills don't. That asymmetry compounds fast.

- Writing a good SKILL.md made me a better thinker. The model reads it like a person. Ambiguous instructions fail visibly. My prose got tighter.

If you've built agent tooling — what's the abstraction you wish you'd found earlier instead of hand-rolling?

#AIAgents #DeveloperTools #BuildInPublic #ClaudeAI #LLMEngineering