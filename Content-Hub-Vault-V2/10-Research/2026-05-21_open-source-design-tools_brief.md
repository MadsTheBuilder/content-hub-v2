---
date: 2026-05-21
niche: open-source design tools
repos_researched: 1
primary_sources_found: 7
notebook_ids: [589cc0b9-e5b4-42cf-b015-6bb514a2614d]
---

# Research Brief — open-source design tools
*2026-05-21 — 1 repos, each in its own notebook*

## nexu-io-open-design
Source: https://github.com/nexu-io/open-design  
notebook_id: 589cc0b9-e5b4-42cf-b015-6bb514a2614d  

[Synthesis failed]

## Sources

- **GitHub - nexu-io/open-design: 🎨 Local-first, open-source alternative to Anthropic's Claude Design. ⚡ 19 Skills · ✨ 71 brand-grade Design Systems 🖼 Generate web · desktop · mobile prototypes · slides · images · videos · HyperFrames 📦 Sandboxed preview · HTML/PDF/PPTX/MP4 export 🤖 Runs on Claude Code / Codex / Cursor / Gemini / OpenCode / Qwen / Copilot / Hermes / Kimi CLI. · GitHub**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/CONTRIBUTING.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/README.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/docs/agent-adapters.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/docs/architecture.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/docs/atoms.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/docs/blog-indexing-automation.md**
- **https://raw.githubusercontent.com/nexu-io/open-design/main/docs/blog-indexing-status.md**


## Raw Findings

<details><summary>Expand for full Q&A and angle battery</summary>

### Research Questions

**How does Open Design use my existing coding agent CLIs?**

### Briefing: Agent-Native Architecture and CLI Integration

Open Design (OD) distinguishes itself by being an "agent-native" platform that does not bundle a proprietary AI agent. Instead, it is designed to delegate the entire design and coding loop to the specialized coding agents already installed on a developer's machine [1-3].

#### 1. The Delegation Philosophy
The core tenet of Open Design’s architecture is that existing coding agents are already highly optimized for filesystem operations and tool use. As stated in the documentation:
> "We delegate the **entire agent loop** — model calls, tool use, context management, permission handling, resume, cancel — to the user's existing code agent CLI. OD's job is to detect it, feed it a skill + prompt + working directory, and stream its output back to the web UI" [3].

This approach avoids reimplementing the complex logic of agentic workflows by leveraging tools like Claude Code, Cursor, and Devin as the underlying "design engine" [2, 4, 5].

#### 2. Detection and Capability Negotiation
Upon startup, the Open Design daemon performs a **PATH scan** and a **config-dir probe** to identify installed CLIs [6-8].
*   **PATH Scan:** The daemon runs `which <binary>` for known executables [8].
*   **Config-dir Probe:** It checks for specific directories (e.g., `~/.claude/` or `~/.codex/`) to catch global npm installs that might be shell-specific [8].

Once detected, the daemon negotiates capabilities with the agent, such as its ability to perform **surgical edits** (modifying specific code regions without a full rewrite), support for **native skill loading**, and its **streaming format** [9, 10].

#### 3. The Adapter Layer
The integration is managed through an adapter layer located in `apps/daemon/src/agents.ts` [11-13]. Each supported agent has a dedicated adapter that handles its specific command-line arguments and output parsing [14, 15].

When a design task is initiated, the daemon:
1.  **Spawns the CLI:** It uses `child_process.spawn` to launch the agent [16, 17].
2.  **Sets the Workspace:** The agent’s current working directory (`cwd`) is set to the specific project folder under `.od/projects/<id>/` [18-20].
3.  **Feeds Context:** The agent is provided with a composed prompt including the active `SKILL.md` (the design task instructions), the chosen `DESIGN.md` (brand tokens), and any relevant project metadata [16, 21].

#### 4. Communication and Streaming
Open Design supports **16 coding-agent CLIs** and handles various communication protocols to ensure real-time feedback in the web UI [4, 14, 22].
*   **Stdio Transport:** Most agents communicate over standard input/output [5, 23].
*   **Diverse Formats:** The daemon normalizes diverse output formats, including `claude-stream-json` (Claude Code), `acp-json-rpc` (Devin, Hermes, Kimi), `pi-rpc` (Pi), and `plain` text (Qwen, DeepSeek) [14, 16, 17, 24].
*   **Real-time Updates:** This normalization allows the UI to show a "live todo progress" card and stream tool calls as they happen [25, 26].

#### 5. Skill and Context Injection
To teach an agent a specific design skill, OD uses three primary strategies based on the agent's capabilities:
*   **Native Skill Loading:** For agents like Claude Code, OD symlinks the skill into the agent's native skills directory (e.g., `~/.claude/skills/`) [27, 28].
*   **Prompt Injection:** The skill instructions and design system are concatenated directly into the system prompt [27, 29].
*   **File-Placed Workflow:** For agents like Cursor, OD writes a project-level instruction file (e.g., `.cursorrules`) into the working directory [29, 30].

#### 6. Summary of Supported Agents
| Agent | Bin | Core Advantage |
| :--- | :--- | :--- |
| **Claude Code** | `claude` | Reference implementation; supports native skills and surgical edits [28, 31]. |
| **Codex CLI** | `codex` | Sandbox workspace-write support; uses stdin for long prompts [14, 32]. |
| **Devin for Terminal** | `devin` | Uses Agent Client Protocol (ACP) for rich tool-use streaming [33, 34]. |
| **Cursor Agent** | `cursor-agent` | High surgical-edit reliability via `.cursorrules` [30, 31]. |
| **GitHub Copilot CLI** | `copilot` | Uses `copilot-stream-json` and supports non-interactive tool calls via `--allow-all-tools` [14, 35, 36]. |

Through this architecture, Open Design ensures that:
> "The daemon makes the agent feel like it's on your laptop, because it is. The agent gets real Read, Write, Bash, WebFetch — real tools against a real filesystem" [19, 20].

**Follow-up: CLI Spawning and IPC Mechanism**

The Open Design daemon invokes coding-agent CLIs using a **`child_process.spawn`** mechanism that operates primarily over **stdio** (piping `stdin`, `stdout`, and `stderr`) [1-3]. To ensure a stable and isolated execution environment, the daemon spawns each CLI with its **`cwd` (current working directory)** set specifically to the active project's artifact folder located under `.od/projects/<id>/` [4, 5].

### Spawning Mechanism Details
*   **Prompt Delivery:** While some agents are invoked with a `-p <prompt>` argument, the daemon uses a "Windows-friendly" fallback for long prompts that would exceed the 32 KB `CreateProcess` limit [6, 7]. In these cases, it sets `promptViaStdin: true` and writes the composed prompt directly to the child process's **`stdin`** [8, 9].
*   **Non-Interactive Execution:** The daemon runs every CLI **without a TTY/PTY** [10]. It passes flags like `--yolo`, `--permission-mode dangerous`, or `--permission-mode bypass_permissions` to ensure the agents operate in a headless, non-interactive mode that does not hang on approval prompts [10-13].
*   **Process Lifecycle:** For RPC-based agents like Pi, the daemon manages the lifecycle by sending a `prompt` command over JSON-RPC, monitoring for an `agent_end` event, and then closing `stdin` and sending a `SIGTERM` after a grace period [14].

### Output Streaming to the Web UI
The daemon acts as a normalization layer between the various CLI output formats and the web frontend:
*   **Event Parsing:** The daemon uses specialized parsers (e.g., `claude-stream-json`, `acp-json-rpc`, `pi-rpc`, or `plain` stdout chunking) to translate raw CLI output into a standardized set of **`AgentEvent`** objects, such as `text_delta`, `tool_call`, and `thinking` [1, 2, 14, 15].
*   **SSE Normalization:** These events are streamed from the daemon to the Next.js web application via **Server-Sent Events (SSE)** at the `/api/chat` or `/api/proxy/.../stream` endpoints [1, 16, 17]. 
*   **Frontend Consumption:** The SSE stream provides normalized `delta`, `end`, and `error` chunks, allowing the web UI to render live todo progress, tool-call feeds, and streaming text in real-time [2, 18, 19].

**Follow-up: Capability Negotiation Protocol**

The OD daemon determines agent capabilities through a combination of **hardcoded adapter definitions**, **CLI probing commands**, and **protocol handshakes**, primarily documented in **`docs/agent-adapters.md`** [1-3].

The mechanism for identifying capabilities like surgical edits, native skill loading, and streaming formats involves the following layers:

### 1. Hardcoded Adapter Definitions
For most standard coding-agent CLIs, capabilities are not "negotiated" in real-time but are **pre-defined** within the adapter's code in `apps/daemon/src/agents.ts` [1, 3, 4].
*   **Capability Interface:** Every adapter implements an `AgentCapabilities` interface that explicitly declares boolean flags such as `surgicalEdit`, `nativeSkillLoading`, and `streaming` [5, 6].
*   **Static Mapping:** The daemon includes an "Adapter catalog" that maps specific CLIs (like `claude-code` or `devin`) to their known functional P0/P1/P2 priorities and native features [7, 8].

### 2. Detection and Probing
The daemon uses several signals to confirm which agent is active and what it can do:
*   **PATH Scan and Config-Dir Probes:** On startup, the daemon runs a `detect()` function for all adapters in parallel, performing a `which <binary>` scan and checking for specific configuration directories (e.g., `~/.claude/` or `~/.codex/`) [7, 9].
*   **Version Checks:** For some agents, like Codex, the daemon checks the **version string** to determine its strategy for skill loading, as native support varies by version [10].
*   **Model Probing:** To populate the model picker, the daemon probes the CLI using commands like `<bin> --list-models` or `<bin> models` [1, 11, 12].

### 3. Protocol Handshakes (ACP/RPC)
For agents that follow more formal communication standards, the negotiation is more dynamic:
*   **Agent Client Protocol (ACP):** Agents like Devin, Hermes, and Kimi use a JSON-RPC handshake over stdio. The daemon uses a shared `acp-json-rpc` transport to negotiate the process lifecycle and message flow [13, 14].
*   **Pi-RPC:** The Pi agent uses a specific `pi-rpc` stdio JSON-RPC protocol where the daemon sends a `prompt` command and receives typed events [15].

### 4. Strategy Adaptation
Once detection is complete, the daemon adapts its workflow based on the identified capabilities:
*   **Skill Injection:** If `nativeSkillLoading` is true (as in Claude Code), the daemon symlinks skills into the agent's native directory. Otherwise, it falls back to **prompt injection**, where skill instructions are concatenated into the system prompt [16, 17].
*   **Windows-Friendly Spawning:** The daemon checks if the environment is Windows and if the agent supports stdin. If an agent (like Gemini) would blow the Windows command-line limit (~32 KB), the daemon negotiates this by feeding the prompt over stdin instead of as a positional argument [18-20].

**Follow-up: Frontend SSE Consumption (cut-off section)**

The Next.js client consumes the SSE stream through a dedicated transport layer located in `apps/web/src/providers/`, which handles normalized chunks from the daemon's `/api/chat` endpoint [1, 2]. 

### **Frontend Consumption Mechanism**
Because the daemon’s chat and proxy endpoints use **`POST`** requests to transmit the `text/event-stream` (to accommodate large prompt payloads), the client does not use the native `EventSource` API, which is limited to `GET` [3, 4]. Instead, the frontend utilizes a **fetch-based reader** within its transport layer to consume normalized `delta`, `end`, and `error` SSE chunks [3, 5].

These events are routed through an in-memory **session bus** [5, 6]. This bus acts as the central coordinator, broadcasting the raw stream events to various React state modules for real-time rendering [5, 7].

### **Application to React State**
The normalized `AgentEvent` objects are applied to the React state as follows:

*   **`text_delta`**: These chunks are appended to the active conversation's message state, causing the assistant's response to stream incrementally into the chat pane [8, 9].
*   **`tool_call` and `tool_result`**: These events drive the **live agent panel**. As the agent calls tools like `Read`, `Write`, or `Edit`, the UI renders a streaming "todo" card showing the progress of each task [10, 11]. Completed tool calls update the project's "artifact tree" and "file workspace" state in real-time [11].
*   **`thinking`**: For models that support reasoning (such as Pi or DeepSeek-v4), these deltas are rendered as a "thinking" indicator or a separate expandable text block in the chat interface [12-14].
*   **`file_write`**: This event specifically signals that a file has been materialized or updated on the filesystem [8, 15]. The frontend updates the local file list and, when the agent signals it is "done," triggers a debounced reload of the **sandboxed preview iframe** to show the new artifact [11, 16, 17].
*   **`error`**: If the stream emits an error (e.g., "daemon not reachable" or "prompt too large"), the client updates the session state to display a "fix-it" toast or an inline error card to the user [18, 19].

The final state of the conversation, including all messages and tool calls, is persisted from the React state back to the daemon's local **SQLite database** to ensure the workspace remains consistent upon reload [15, 20, 21].

**Follow-up: acp-json-rpc parser identity**

In the Open Design project, **ACP** stands for the **Agent Client Protocol** [1-3]. 

It is a standardized **JSON-RPC** message flow over stdio used by the daemon to communicate with several sophisticated coding agents [4, 5].

### Agents Using ACP
The following CLI agents are detected and driven via the `acp-json-rpc` transport [1, 2, 6]:
*   **Devin** (Devin for Terminal) [1, 5]
*   **Hermes** [1, 2]
*   **Kimi** (Kimi CLI) [1, 2]
*   **Kiro** (Kiro CLI) [1, 2]
*   **Kilo** [1, 2]
*   **Mistral Vibe** (Mistral Vibe CLI) [1, 2]

### Schema and Implementation Location
The definition and schema for the protocol are found in the following locations within the codebase and documentation:
*   **Documentation:** The full contract, including the expected stdio transport, JSON-RPC message flow, and process lifecycle, is defined in **`docs/new-agent-runtime-acp.md`** [4, 7].
*   **Codebase Implementation:** 
    *   The shared transport logic is implemented in the daemon as **`acp-json-rpc`** [5].
    *   The streaming events from these agents are mapped onto UI-compatible events by a parser, typically referenced as **`acp.js`** (or a similar naming convention like `acp.ts` in the daemon's source) [8].
    *   General agent definitions and their transport assignments (including `acp-json-rpc`) are located in **`apps/daemon/src/agents.ts`** [1, 2, 9].

**Follow-up: ACP/JSON-RPC Handshake — What Gets Exchanged?**

The document that defines the ACP (Agent Client Protocol) exchange format for agents like Devin, Hermes, and Kimi is **`docs/new-agent-runtime-acp.md`** [1, 2]. This spec document details the expected stdio transport, JSON-RPC message flow, and the process lifecycle contract [2].

While the full message-level handshake protocol is contained in that specific document (which is listed in the repository structure but not fully excerpted here), the **`AgentCapabilities`** surfaced through the adapter layer include the following specific fields:

*   **`surgicalEdit`**: A boolean indicating if the agent can edit a targeted region without rewriting the entire file [3].
*   **`nativeSkillLoading`**: A boolean indicating if the agent automatically picks up skills from its own native skills directory (e.g., `~/.claude/skills/`) [3, 4].
*   **`streaming`**: A boolean indicating if the agent emits tool calls and text deltas in real time [3].
*   **`resume`**: A boolean indicating if the agent can continue an interrupted run [3].
*   **`permissionMode`**: Specifies the security posture, categorized as `"strict"`, `"permissive"`, or `"none"` [3].
*   **`contextWindowHint`**: An optional numeric field providing the agent's context window size in tokens [3].

In addition to these capabilities, the ACP handshake is used dynamically at runtime to populate the available **models** for the agent when the CLI does not expose them via standard help or list commands [5]. The implementation of this transport and the internal parsing of these surfaced capabilities resides in **`apps/daemon/src/agents.ts`** [6].

**Follow-up: Are AgentCapabilities Flags Truly Static?**

In the **nexu-io/open-design** project, `AgentCapabilities` are not strictly compile-time constants; while many are inherent to an adapter's design, others are determined dynamically during the **`detect()`** phase [1, 2].

The documentation in **`docs/agent-adapters.md`** settles this by revealing a stateful relationship between detection and capabilities:

*   **Interface Definition:** The `AgentAdapter` interface defines `capabilities()` as a **method** (`capabilities(): AgentCapabilities`) rather than a static property [2]. This design allows the adapter to return values derived from internal state captured during the probe [2].
*   **Runtime Probing Logic:** The **`detect()`** function body is responsible for capturing environmental data, such as the agent's **`version`** string [2, 3].
*   **The Codex Precedent:** The most definitive evidence is found in the notes for the **Codex** adapter, which explicitly states that its skill-loading capability is version-dependent: "Detect by version string; fall back to prompt injection" [4]. This confirms that the results of the version probe directly update how the adapter reports its `nativeSkillLoading` capability [4].
*   **Capability-Driven UI:** The system is designed to "degrade and document" based on these results; the web UI reads the current adapter's capabilities at runtime to enable or disable features like **Surgical edit** or **Streaming tool-call feeds** [5, 6].

While the "hardcoded" aspect refers to the base capabilities defined for each CLI (as seen in the **Adapter catalog** table), the **`detect()`** function body provides the logic that updates these flags, and the **interface definition** settles the mechanism that makes this runtime flexibility possible [2, 7-10].

**Follow-up: Error Event Handling**

When the Open Design client receives an `error` event via the Server-Sent Events (SSE) stream, it handles the failure by surfacing actionable information to the user and offering manual recovery paths rather than performing silent retries or a total state reset.

### Error Surfacing and Stream Handling
*   **Inline Surfacing:** The client surfaces errors as "actionable" messages. For example, if a prompt exceeds limits, the daemon emits an `AGENT_PROMPT_TOO_LARGE` SSE error that explicitly instructs the user to reduce context (e.g., by shortening the conversation or reducing skills/design-system data) [1]. 
*   **Stream Termination:** Within the agent adapter interface, an `error` event is one of the typed events delivered during a run [2]. Once an error occurs, it is typically followed by a `done` event with a `reason` of `"error"`, which signals the transport layer to stop the stream [2].
*   **Daemon Monitoring:** For specific adapters like Pi, error events (such as `extension_error`) are routed through a `sendAgentEvent` helper. This sets an `agentStreamError` flag and engages an "empty-output guard" to ensure the failure is recognized by the daemon and passed to the web UI [3].

### Retry and Fallback Mechanisms
*   **Manual Fallback (One-Click):** The system does not automatically retry the same agent or silently switch providers if a crash or timeout occurs [4, 5]. Instead, the web UI offers a "one-click fallback" UI that allows the user to explicitly opt-in to a different engine in a specific order:
    1.  The user's preferred agent [5].
    2.  Any other detected agent (e.g., falling back to Claude Code if the primary failed) [5].
    3.  The API fallback path (direct Anthropic Messages API, requiring a BYOK key) [5].
*   **Automated Retry Exceptions:** There is at least one case of automated retry: the desktop runtime will "retry once" if it receives a `503 DESKTOP_AUTH_PENDING` error during a folder import, attempting to re-handshake with the daemon before surfacing a failure toast to the user [6, 7].

### Timeouts and Session State
*   **Timeout Handling:** The agent adapter interface includes a `timeoutMs` parameter in the `AgentRunParams` [8]. If an agent hangs, the daemon can send a `SIGTERM` to the CLI process to flush and exit [9].
*   **Persistence:** Receiving an error does not reset the session state. Because project data, conversations, and open tabs are persisted in a local SQLite database (`.od/app.sqlite`), the workspace remains exactly where the user left it, allowing them to fix the prompt and try again [10-13].

**Follow-up: Session Bus Implementation**

The provided sources identify the **in-memory session bus** as a logical component within the Web App architecture that coordinates activity between the chat pane, artifact tree, preview iframe, and overlay controls [1, 2]. However, the sources **do not specify its concrete implementation** (e.g., whether it uses a custom `EventEmitter`, Zustand, React Context, or a third-party library) [3, 4].

Regarding the coordination and ordering of events, the following details are available:

*   **Sequential Delivery via SSE:** The primary mechanism for delivering events from the backend (daemon) to the frontend is **Server-Sent Events (SSE)** [5-7]. SSE is a unidirectional protocol that naturally preserves the sequence of events emitted by the daemon [7, 8].
*   **Daemon Normalization:** The daemon's transport layer normalizes diverse agent outputs (from CLIs like Claude Code or Codex) into a standardized set of `AgentEvent` objects [9, 10]. These events, which include `tool_call`, `text_delta`, and `thinking`, are streamed back to the web UI as they arrive [11].
*   **Session Management:** The daemon maintains a session for each web tab, tracking the active agent, skill, artifact, and in-flight tool calls [12]. This state is used to hydrate the React/browser state in the Web App [4].
*   **State Hydration:** In the Web App, project and conversation files are hydrated from the daemon APIs, and the "session bus" acts as the interface between these updates and the UI components [2, 4].
*   **Concurrency Handling:** While the sources mention support for multi-screen prototypes and various concurrent UI updates (like the live todo progress stream), they do not detail a specific locking or ordering logic beyond the sequential nature of the normalized SSE stream [13-15].

For more specific implementation details beyond these architectural descriptions, you may need to consult the source code in `apps/web/src/state/` directly, as the documentation focuses on high-level data flow rather than internal class structures [16].

**Follow-up: Exact parser file path for ACP transport**

The actual file path in the daemon's source tree that implements the ACP event-to-UI mapping is **`apps/daemon/src/acp.ts`** [1, 2].

While some documentation refers to the file using a `.js` extension (typically when discussing the compiled runtime or as a naming convention), the project's source tree is written in **TypeScript**, placing the implementation at the `.ts` path [1, 2].

This file is located in the **`apps/daemon/src/`** directory, directly alongside other core parser and transport files, including:
*   **`claude-stream.ts`** (referenced as `claude-stream.js`), which parses Claude Code events [1, 3].
*   **`pi-rpc.ts`**, which handles Pi's JSON-RPC mapping [1].
*   **`copilot-stream.ts`** (referenced as `copilot-stream.js`), which handles Copilot events [1].
*   **`qoder-stream.ts`**, which handles Qoder CLI events [4].
*   **`agents.ts`**, which manages the overall agent detection and dispatching [3, 5].

**Follow-up: ACP JSON-RPC message schema content**

The Agent Client Protocol (ACP) in Open Design is a **JSON-RPC 2.0** implementation designed to facilitate communication between the local daemon and external coding-agent CLIs over **stdio transport** [1-3]. While the full contract is specified in `docs/new-agent-runtime-acp.md`, the provided documentation outlines the following operational details:

### JSON-RPC Methods and Events
The ACP adapter (found in `apps/daemon/src/agents.ts`) handles a variety of structured messages and events that define the interaction between the daemon and the agent [4, 5]. Key message types include:
*   **Discovery and Handshake:** The protocol uses an **ACP handshake** during the daemon's startup phase to populate available models from the agent CLI [6].
*   **Execution (Request):** The daemon sends a `run` command containing `AgentRunParams`, which include the `systemPrompt` (skill and design system context), `userPrompt`, and the artifact directory (`cwd`) [5, 7].
*   **Streaming Events:** The agent emits real-time events that the daemon maps to the UI, including:
    *   `thinking`: Provides the agent's reasoning process [5].
    *   `text_delta`: Streams incremental text output (the "stream_chunk" equivalent) [5].
    *   `tool_call` and `tool_result`: Manages the execution of tools like `Read`, `Write`, and `Edit` [5, 8, 9].
    *   `file_write`: Synthesized by the adapter to track file changes [8].
    *   `done`: Signals completion with a reason (e.g., `completed`, `cancelled`, or `error`) [8].

### Process Lifecycle
The lifecycle of an ACP-backed runtime follows a structured sequence managed by the daemon:
1.  **Detection:** The daemon scans the system `PATH` and config directories for supported binaries (e.g., `devin`, `hermes`, `vibe-acp`) [8, 10, 11].
2.  **Handshake:** Upon selection, the daemon initiates a handshake to verify capabilities such as **streaming**, **surgical edit** support, and **native skill loading** [7, 12, 13].
3.  **Spawning:** The daemon spawns the CLI process with specific flags. For example, Devin is spawned with `devin --permission-mode dangerous --respect-workspace-trust false acp` [3].
4.  **Session Management:** The daemon drives the agent over its stdio, feeding it prompts and capturing JSON-RPC events [3, 14].
5.  **Termination:** To terminate a session, the daemon typically closes the process's `stdin`. If the process remains alive after an `agent_end` event, the daemon issues a **SIGTERM** after a designated grace period to ensure a clean exit [9, 15].

**Follow-up: Session State After Stream Termination**

Open Design **preserves the partial conversation history** and session state when an error occurs, rather than tearing it down [1, 2]. The system is built on a "Filesystem-grade workspace" where the local daemon persists projects, conversations, messages, and tabs into a local **SQLite database** located at `.od/app.sqlite` [2-5].

The specific behavior of the state and history following an error includes:

*   **Durable Message Persistence:** Because every message and conversation is stored in SQLite, the partial history of the turn remains intact even if the stream stops due to an error event [1, 5, 6].
*   **Context Continuity:** The project is designed so that even if the application is closed and reopened, the "todo card and open files are exactly where you left them," allowing the user to resume or retry from the existing context [1, 2, 5].
*   **Adapter-Level Resumption:** While the conversation history is kept, the ability to "resume" an interrupted run directly (as opposed to starting a fresh turn with the existing context) depends on the specific agent adapter's capabilities [7, 8]. If an adapter does not support native resumption, the UI typically offers a "Cancel + restart" option, though this still draws from the persisted conversation context [9].
*   **Error Routing:** For specific adapters like Pi, error events (e.g., `extension_error`) are routed through the daemon to ensure they are handled without crashing the session, maintaining the stability of the underlying SQLite-backed workspace [10].

In summary, the state is not torn down; the user can continue editing or retrying where the agent left off because the "prompt stack is the product" and every layer—including the history—is persisted locally [2, 6, 11].

**Follow-up: 503 DESKTOP_AUTH_PENDING Retry Outcome**

After the desktop runtime re-invokes its registration callback to re-handshake with the new daemon and mints a fresh token, it **retries the import once** [1]. If the retry is successful, the process completes without requiring a desktop restart [2].

However, if the failure is persistent—such as when the daemon is truly down or the IPC socket is missing—the error **surfaces to the user as a "renderer toast"** rather than being silently dropped [2]. This ensures that while the system attempts to transparently recover from a daemon restart, any actual inability to complete the import is explicitly communicated to the user [2].

**Follow-up: Boundary between acp.ts and agents.ts**

In the **Open Design** architecture, the responsibility split between `agents.ts` and `acp.ts` is clearly defined by the distinction between **environment orchestration** and **protocol normalization**.

### Precise Responsibility Split

*   **`agents.ts` (Detection & Dispatching):**
    *   **Orchestration:** This file is the primary registry for supported coding agents [1, 2]. It is responsible for scanning the user's `PATH` to detect available binaries (e.g., `claude`, `devin`, `cursor-agent`) and caching those results [3, 4].
    *   **Execution:** It handles the "dispatch routing" by defining the specific `argv` shapes and command-line arguments needed to spawn each agent process [1, 5]. It manages process-level concerns, such as routing composed prompts via `stdin` on Windows to avoid command-line length limits [6, 7].
    *   **Capability Negotiation:** It defines what each agent can do (e.g., surgical edits, native skill loading) and which streaming format the agent uses [8-10].

*   **`acp.ts` (Protocol-Level Parsing):**
    *   **Event Normalization:** This file (referenced as `acp.js` or the `acp-json-rpc` transport) is responsible for the **protocol-level parsing** of the Agent Client Protocol [11, 12]. 
    *   **Mapping:** It consumes the raw JSON-RPC messages emitted by an agent over `stdio` and maps them into a standardized set of `AgentEvent` objects (such as `text_delta`, `tool_call`, or `thinking`) that the Open Design web UI understands [12, 13]. 
    *   **Scope:** It specifically handles agents that speak the Agent Client Protocol, such as **Devin**, **Hermes**, **Kimi**, and **Mistral Vibe** [11, 14].

### Do they overlap?
There is **minimal overlap**; their relationship is one of delegation rather than duplication [15]. `agents.ts` acts as the router that identifies an agent is using the `acp-json-rpc` stream format and then delegates the actual data-parsing work to the `acp.ts` logic [8, 12]. 

While `agents.ts` knows *that* an agent uses a specific protocol, `acp.ts` is the only one that knows *how* to translate that protocol's specific JSON-RPC lifecycle—such as `agent_start`, `message_update`, and `turn_end`—into the common UI events used across the entire platform [12].

**Follow-up: Termination Signal and Post-Spawn Lifecycle**

In the **nexu-io/open-design** project, the lifecycle of an agent process following its initial spawning involves specific initialization handshakes and termination protocols that vary depending on the adapter type.

### Initialization and Handshake
For agents utilizing the **Agent Client Protocol (ACP)**—such as Devin, Hermes, Kimi, Kiro, Kilo, and Mistral Vibe—initialization follows a standardized JSON-RPC message flow over stdio once the `acp` subcommand is invoked [1-3]. 

Other agents use specific command-based initialization:
*   **Pi Agent:** After spawning the process with `pi --mode rpc`, the daemon initiates the design turn by sending a `prompt` command (and optional `images` for multimodal input) via JSON-RPC over `stdin` [4, 5].
*   **Gemini and Qoder CLI:** To bypass the Windows `CreateProcess` 32 KB argument limit, these adapters are spawned with a flag (like `promptViaStdin: true`), and the entire composed prompt is delivered via a `child.stdin` pipe after the process has successfully started [6-8].
*   **Sidecar IPC:** For desktop and automation processes, a **trust handshake** occurs where a 32-byte secret is generated and registered with the daemon via `REGISTER_DESKTOP_AUTH` before any privileged operations, such as folder imports, are allowed [9, 10].

### Graceful Shutdown and Termination
Graceful termination of an agent run is triggered through several mechanisms:

*   **SIGTERM Signal:** This is the primary method for stopping long-running or interactive agents. For **Claude Code**, the daemon sends a `SIGTERM` to allow the CLI to flush and exit cleanly [11]. For the **Pi agent**, the daemon closes `stdin` and issues a `SIGTERM` after a grace period once the agent has signaled the end of its turn [4].
*   **JSON-RPC SHUTDOWN Notification:** The sidecar protocol, which governs the coordination between the daemon, web, and desktop processes, includes a dedicated `SHUTDOWN` command in its JSON-RPC IPC channel specifically for graceful closure [12-14].
*   **Lifecycle Event Signals:** The `AgentAdapter` interface monitors the process for a `done` event. This event can carry a `reason` of `cancelled`, distinguishing it from a standard `completed` or `error` state [15, 16]. 
*   **Process Exit:** Some agents, like **Qoder CLI**, operate in a "one-request" lifecycle where they emit a final summary and exit automatically after the design turn is finished [8, 17].

### Angle Battery

</details>

