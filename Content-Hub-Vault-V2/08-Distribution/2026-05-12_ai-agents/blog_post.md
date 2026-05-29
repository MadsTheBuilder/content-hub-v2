---
title: "AI agents"
date: 2026-05-12
youtube_url: "[VIDEO_LINK]"
tags: [ai-tools, build-in-public]
---

# LLM Systems Engineering: Building Production AI Agents

Building production LLM systems requires a different engineering mindset. Treat the LLM as an unreliable, slow, general-purpose computer. This approach applies traditional software engineering principles to non-deterministic AI systems.

## The LLM as a Shitty General Purpose Computer

Forget the conversational partner. Your LLM is a CPU you can barely trust. This means your prompt is the program. It defines logic, control flow, and "imports" tools as libraries. Inputs are documentation, code context, user input, and tool results. State is complex. Information in the context window is ephemeral. It suffers "context degradation." Store true persistent state to disk. Use LLM-friendly formats like JSON (for `jq` manipulation) or Markdown (for unstructured summaries). Outputs are not just text. They include tool calls that create artifacts, modify files, or trigger system actions.

## Context Engineering: The Core Constraint

Context is the biggest bottleneck in agentic systems. "Context Rot" means the model loses detail as a session grows. Performance impacts typically hit around 100k tokens, regardless of the theoretical window size. Optimize context ruthlessly:

*   **Surgical Updates:** Use tools like `jq` to update specific fields in state files. This avoids re-writing entire documents and saves tokens.
*   **Progressive Disclosure:** Do not load all tool definitions upfront. This "poisons" the context. Instead, provide a README. The agent reads it only when a task requires a specific tool.
*   **Minimalist Prompts:** Shorter prompts perform better. Effective agents often use system prompts under 1,000 tokens. "Spaceship" prompts, 10,000+ tokens long, confuse the model.

## Agentic Architectures: CLI Trumps MCP

Your tool integration protocol impacts performance and cost. Model Context Protocol (MCP) and Command Line Interface (CLI) tools offer different trade-offs:

| Feature      | MCP (Model Context Protocol)                          | CLI / Bash Tools                                     |
| :----------- | :---------------------------------------------------- | :--------------------------------------------------- |
| **State**    | Stateful by default; easier for persistent sessions.  | Generally stateless; requires manual state management. |
| **Efficiency** | Often "thin wrappers" that flood context with JSON-RPC. | Composable via pipes; higher token efficiency.         |
| **Security** | Bypasses some malicious command detection.             | Subject to frequent security checks.                 |
| **Portability** | Requires specific server implementations.             | Highly portable; any tool with a README is a "skill."  |

Benchmarking shows CLI tools are 39% more cost-effective for complex tasks than standard multiplexers like `tmux`. They provide cleaner, filtered output. While MCP servers sometimes bypass security checks in environments like Claude Code, reducing Haiku token usage significantly, they often introduce context bloat. Over-engineered MCP servers, like Playwright, can consume 9% of the context window (13k–18k tokens) before any real work starts.

## Minimalist Agent Design: The "Pi" Philosophy

Build production agents by resisting feature bloat. The "pi" philosophy prioritizes stability and observability:

1.  **The Minimal Toolset:** Four core tools are enough for a coding agent: `bash`, `read_file`, `write_to_file`, and `edit_file` (using linetags/search-replace).
2.  **YOLO Mode:** For development, skip permission prompts. They are security theater. Production efficiency requires giving agents unrestricted (but monitored) filesystem and network access.
3.  **Observability over Sub-agents:** Sub-agents are black boxes. Instead, make the agent spawn processes via Bash or `tmux`. This allows human operators to inspect raw ANSI streams or attach to sessions for co-debugging.
4.  **Externalize Plan/State:** Avoid built-in "Plan Modes." Force the agent to maintain a `TODO.md` or `PLAN.md` file. This ensures the plan persists through context compaction and is version-controlled.

## Key Takeaway

Treating an LLM as a flaky computer changes your approach to building AI agents. Focus on efficient context management, smart tool integration (favoring CLI where possible), and a minimalist design. This leads to more stable, observable, and cost-effective production systems.

Want to see these principles in action? Watch the full video here: [VIDEO_LINK]
