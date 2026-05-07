 GitHub Trending AI Repos — 2026-04-29

> Auto-generated daily. 🎯 = Claude's pick for best video topic.

---

## Last 7 Days — Top 10

| Repo | Stars | ⚡ Stars/day | Language | Description |
|------|------:|------------:|----------|-------------|
| [nexu-io/open-design](https://github.com/nexu-io/open-design) 🎯 | 2,657 | 2657.0 | TypeScript | 🎨 Local-first, open-source alternative to Anthropic's Claude Design. ⚡ 1… |
| [HKUDS-AI/polymarket-ai-trading](https://github.com/HKUDS-AI/polymarket-ai-trading) | 147 | 147.0 | HTML | AI-assisted paper trading for Polymarket: OpenAI market insight, vector … |

## Last 30 Days — Top 5

| Repo | Stars | ⚡ Stars/day | Language | Description |
|------|------:|------------:|----------|-------------|
| [MemPalace/mempalace](https://github.com/MemPalace/mempalace) | 50,278 | 2094.9 | Python | The best-benchmarked open-source AI memory system. And it's free. |
| [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | 49,713 | 2071.4 | Python | 🪨 why use many token when few token do trick — Claude Code skill that cu… |
| [kyegomez/OpenMythos](https://github.com/kyegomez/OpenMythos) | 11,100 | 1110.0 | Python | A theoretical reconstruction of the Claude Mythos architecture, built fr… |
| [JackChen-me/open-multi-agent](https://github.com/JackChen-me/open-multi-agent) 🎯 | 5,966 | 213.1 | TypeScript | From a goal to a task DAG, automatically. TypeScript-native multi-agent … |
| [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | 3,657 | 166.2 | Python | Claude + Obsidian knowledge companion. Persistent, compounding wiki vaul… |

---

## Claude's Daily Picks

### 7-day pick → [nexu-io/open-design](https://github.com/nexu-io/open-design)

Local-first design tooling that runs inside AI coding environments is a genuinely new category, and the multi-agent compatibility angle (Claude Code, Cursor, Gemini CLI) gives you a concrete demo hook that differentiates it from 'just another Figma clone' explainer.

### 30-day pick → [JackChen-me/open-multi-agent](https://github.com/JackChen-me/open-multi-agent)

Goal-to-DAG orchestration with live tracing is a teachable, visual concept that demystifies multi-agent systems without requiring a PhD — the three-dependency constraint makes it approachable enough to build on-screen in a single video.

---

## Deep Dive: 7-Day Pick — [nexu-io/open-design](https://github.com/nexu-io/open-design)

**Language:** TypeScript · **Stars:** 2,657 · **Velocity:** 2657.0/day

### What problem does it solve?

Design tools like Figma and cloud-based AI design assistants lock you into subscriptions, send your work to remote servers, and offer little control over design system consistency. Developers and content creators who want AI-generated UI components, presentations, or brand assets have no fully offline, open-source option that respects data privacy and integrates with their existing coding workflow.

### How it works

open-design runs as a local skill layer on top of AI coding agents (Claude Code, Codex, Cursor, Gemini CLI, etc.), giving each agent access to 19 design skills and 71 pre-built brand-grade design systems. It renders output in a sandboxed preview environment and exports finished assets as HTML, PDF, or PPTX — all processed locally with no cloud dependency.

### Best use cases

- A developer uses it inside Cursor to scaffold a polished landing page with a consistent design system, then exports it as an HTML file — without leaving their editor or touching Figma.
- A content creator runs it via Claude Code to generate on-brand pitch deck slides as PPTX, iterating with natural language prompts while keeping all assets local.
- An indie hacker integrates it into their Codex workflow to rapidly prototype and preview multiple UI variants across different brand design systems before committing to one.

### Getting started

Clone the repo from GitHub, install dependencies with npm/bun, then drop the skill files into your AI agent's skills directory (e.g., .claude/skills/ for Claude Code) and invoke a design skill via your agent's slash command or prompt interface.

---

## Deep Dive: 30-Day Pick — [JackChen-me/open-multi-agent](https://github.com/JackChen-me/open-multi-agent)

**Language:** TypeScript · **Stars:** 5,966 · **Velocity:** 213.1/day

### What problem does it solve?

Building multi-agent AI systems requires manually wiring task dependencies, managing execution order, and coordinating tool calls across agents — a brittle, hard-to-maintain process. open-multi-agent removes that orchestration burden by automatically decomposing a plain-language goal into a dependency graph (DAG) and executing it without manual wiring. This unlocks complex, multi-step AI workflows that would otherwise require significant infrastructure code.

### How it works

Given a goal string, the system uses an LLM to produce a Directed Acyclic Graph of subtasks, where each node is an agent with defined inputs, outputs, and MCP tool access. A scheduler resolves dependencies in topological order, running independent tasks in parallel and feeding outputs downstream, while a live tracer streams execution state in real time. The entire runtime sits on just three dependencies, keeping the footprint minimal and the internals transparent.

### Best use cases

- Automated research pipelines — input a topic and let agents fan out to search, summarize, and synthesize findings in parallel before a final agent writes the report
- Codebase analysis workflows — decompose 'audit this repo for security issues' into agents that read files, cross-reference dependencies, and aggregate findings with no manual task ordering
- Data enrichment pipelines — take a list of companies and orchestrate concurrent agents to scrape, classify, and score each one, with a reducer agent joining results at the end

### Getting started

Install the package, define your MCP tool server connections in a config object, then call the orchestrator with a plain-language goal string — the DAG is inferred and executed automatically with trace output to stdout. The TypeScript-native design means full type safety from goal definition through agent outputs with no additional build tooling required.

---

*Generated 2026-04-29 13:33 · [GitHub Trending](https://github.com/trending)*