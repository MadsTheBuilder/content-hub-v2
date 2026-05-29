---
title: "AI agents"
date: 2026-05-12
youtube_url: "[VIDEO_LINK]"
duration: 30s
---

**SPOKEN SCRIPT:**
LLMs are shitty, unreliable general-purpose computers. Not your conversational partner. Your prompt *is* the program. Context is just ephemeral RAM – it degrades fast around 100k tokens. Never store persistent state there. Serialize everything to disk using JSON with `jq`, or Markdown files. Ditch complex sub-agents and bloated prompts. Stick to four core tools: `bash`, `read`, `write`, `edit`. This gives you true observability, cleaner context, and cheaper operations. Build robust agents, not black boxes.

**TEXT OVERLAYS:**
LLM = Shitty Computer
Context is Ephemeral RAM
Serialize State: JSON/Markdown
Minimal Tools, Not Sub-Agents

**CAPTION:**
Stop building LLM agents like chatbots. Treat them as unreliable computers where your prompt is the program. Manage state like a pro. #LLMEngineering #AIAgents #DeveloperProductivity
