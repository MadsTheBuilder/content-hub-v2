# Content Hub V2 — Button Wrapper (`control_room.py`)

Tags: [[Control Room]], [[Streamlit]], [[Wrapper]], [[Pipeline]]
Status: Ready for build — hand to Ruflo agent swarm
Date: 2026-05-11

## Context

The V2 skill engine is feature-complete and dogfooded. Every stage (trending → research → ideation → hook → outline → short_form / cascade / title) is invokable via `python -m skills.<name>` and lands artifacts in a predictable vault folder. The friction left is **typing**: remembering CLI flags, paths to the latest brief, which folder a hook lives in, etc.

This plan introduces a **Streamlit dashboard** (`control_room.py`) that exposes each skill as a button, auto-populates inputs from the most recent vault artifacts via dropdowns, and shows a Dev Logs panel for live stdout when desired. No skill code changes — the wrapper is a thin orchestration layer that shells out to the existing modules.

## Architecture

```
┌──────────────────────────────────────────────┐
│  Streamlit UI (control_room.py)              │
│  ─ sidebar: stage selector                   │
│  ─ main:    inputs (dropdowns) + Run button  │
│  ─ footer:  Dev Logs expander (live stdout)  │
└──────────────┬───────────────────────────────┘
               │ calls
               ▼
┌──────────────────────────────────────────────┐
│  runner.py   (thin subprocess executor)      │
│  ─ run_skill(cmd, log_queue) → exit_code     │
│  ─ streams stdout line-by-line into queue    │
│  ─ background thread; UI polls queue         │
└──────────────┬───────────────────────────────┘
               │ subprocess.Popen
               ▼
┌──────────────────────────────────────────────┐
│  Existing skills (unchanged)                 │
│  python -m skills.researcher ...             │
│  python -m skills.ideation ...               │
│  python github_trending.py ...               │
└──────────────────────────────────────────────┘
               │ writes
               ▼
        Content-Hub-Vault-V2/
        02-Ideas, 04-Trends, 05-Hooks, 06-Outlines,
        07-Titles, 08-Distribution, 09-Shorts, 10-Research
```

**Why Streamlit + subprocess (not import skills directly):**
- Skills are CLI-shaped (argparse). Importing would couple us to their internals and break on changes.
- Subprocess gives us free stdout streaming for Dev Logs.
- Skills already write to the vault on disk; UI just reads files back.

## File layout (new files only)

```
Content Hub V2/
├── control_room.py          ← Streamlit app (single page)
├── runner.py                ← subprocess + log queue helper
├── vault_index.py           ← list/sort/glob vault folders for dropdowns
└── run_control_room.bat     ← one-click launcher (streamlit run ...)
```

No edits to `skills/`, `prompts/`, `daily.py`, or the vault. Existing FastAPI backend stays untouched.

## Stage definitions

Each stage = one tab/page in the sidebar. Inputs are vault dropdowns sorted newest-first.

| # | Stage | Button | Inputs (dropdowns / fields) | Command spawned | Output folder |
|---|---|---|---|---|---|
| 1 | **Trending Repos** | Fetch Last 7d & 30d | (none) | `python github_trending.py` | `04-Trends/` |
| 2 | **Research** | Run Researcher | niche (text, default last topic); repos (multi-select from `04-Trends/github_trending.md`); mode (deep/fast) | `python -m skills.researcher --niche "<x>" --mode <m> --repos <r>` | `10-Research/*_brief.md` |
| 3 | **Ideation** | Generate 9 Ideas | research file (dropdown of `10-Research/*.md`); topic (auto-filled from filename) | `python -m skills.ideation --topic "<x>" --research-file "<path>"` | `02-Ideas/` |
| 4 | **Title** | Draft Titles | concept (text, prefilled from selected idea); idea file (dropdown of `02-Ideas/`) | `python -m skills.title "<concept>"` | `07-Titles/` |
| 5 | **Hook** | Generate Hooks | topic (text); platform (yt-long/shorts/tiktok/reels); audience (text); format (short/medium/long) | `python -m skills.hook "<topic>" --platform <p> --audience "<a>" --format <f>` | `05-Hooks/` |
| 6 | **Outline** | Build Outline | topic (text); hook file (dropdown of `05-Hooks/`); length (slider 5–15); platform | `python -m skills.outline "<topic>" --hook-path "<path>" --length <n> --platform <p>` | `06-Outlines/` |
| 7 | **Short-form** | Generate Shorts | research file + outline file (dropdowns) OR YouTube URL | `python -m skills.short_form --research-file "<r>" --outline-file "<o>" --title "<t>"` | `09-Shorts/` |
| 8 | **Cascade** | Distribution Pack | YouTube URL OR research+outline pair (dropdowns) | `python -m skills.cascade ...` | `08-Distribution/` |
| 9 | **YT Pipeline** | Research from URLs | topic (text); YouTube URLs (text, comma-separated); artifacts (toggle) | `python -m skills.yt_pipeline run "<topic>" "<urls>" [--artifacts]` | `10-Research/<slug>/` |

Sidebar also has a **"Pipeline" mega-button** that runs Trending → Research → Ideation back-to-back (uses the freshest artifact from the prior stage as input for the next).

## Job execution model

- **Default**: press button → spinner blocks the page → on completion, success banner + link to the new artifact.
- **Dev Logs expander** (top-right, sticky): when opened, shows live stdout streaming via a `queue.Queue` filled by a background thread reading `subprocess.Popen.stdout`. Streamlit polls the queue with `st.empty().code(...)` on a 0.5s rerun loop.
- Single-job at a time (skills aren't safe to parallelise — they share Claude API quota and NotebookLM session). A second click is disabled while a job is running.
- Job state held in `st.session_state` (running flag, log buffer, last-artifact path).

## Vault index helper (`vault_index.py`)

One function each, returning lists sorted newest-first by mtime:

```python
def list_research_briefs() -> list[Path]    # 10-Research/*.md
def list_ideas() -> list[Path]              # 02-Ideas/*.md
def list_hooks() -> list[Path]              # 05-Hooks/*.md
def list_outlines() -> list[Path]           # 06-Outlines/*.md
def list_trending_repos() -> list[str]      # parse 04-Trends/github_trending.md table → owner/repo
def latest(folder: str, pattern: str = "*.md") -> Path | None
```

## Runner skeleton (`runner.py`)

```python
import subprocess, threading, queue
from pathlib import Path

REPO = Path(r"c:\Users\madhu\Claude cowork\Content Hub V2")

def run_skill(cmd: list[str], log_q: queue.Queue) -> int:
    proc = subprocess.Popen(
        cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1,
    )
    for line in proc.stdout:
        log_q.put(line.rstrip())
    proc.wait()
    log_q.put(f"__EXIT__ {proc.returncode}")
    return proc.returncode

def run_in_thread(cmd, log_q):
    t = threading.Thread(target=run_skill, args=(cmd, log_q), daemon=True)
    t.start()
    return t
```

## Streamlit skeleton (`control_room.py`)

```python
import streamlit as st, queue
from runner import run_in_thread
from vault_index import list_research_briefs, list_hooks, ...

st.set_page_config(page_title="Content Hub Control Room", layout="wide")
st.title("Content Hub Control Room")

if "log_q" not in st.session_state:
    st.session_state.log_q = queue.Queue()
    st.session_state.running = False
    st.session_state.logs = []

stage = st.sidebar.radio("Stage", [
    "Trending", "Research", "Ideation", "Title",
    "Hook", "Outline", "Short-form", "Cascade", "YT Pipeline",
    "— Run Full Pipeline —",
])

# --- per-stage pane (example: Ideation) ---
if stage == "Ideation":
    brief = st.selectbox("Research brief", list_research_briefs(),
                         format_func=lambda p: p.name)
    topic = st.text_input("Topic", value=brief.stem.split("_", 2)[-1])
    if st.button("Generate 9 Ideas", disabled=st.session_state.running):
        st.session_state.running = True
        st.session_state.logs = []
        run_in_thread(
            ["python", "-m", "skills.ideation",
             "--topic", topic, "--research-file", str(brief)],
            st.session_state.log_q,
        )

# --- Dev Logs (sticky expander) ---
with st.expander("Dev Logs ▸", expanded=False):
    drain = st.session_state.log_q
    while not drain.empty():
        line = drain.get_nowait()
        if line.startswith("__EXIT__"):
            st.session_state.running = False
        else:
            st.session_state.logs.append(line)
    st.code("\n".join(st.session_state.logs[-200:]) or "(no output yet)")

if st.session_state.running:
    st.spinner("Running…")
    st.rerun()
```

## Critical files (read-only references for the build agent)

- `skills/researcher.py`, `skills/ideation.py`, `skills/hook.py`, `skills/outline.py`, `skills/short_form.py`, `skills/cascade.py`, `skills/title.py`, `skills/yt_pipeline.py` — argparse signatures
- `github_trending.py` — entry for stage 1
- `daily.py` — reference for chain order in the "Run Full Pipeline" mega-button
- `Content-Hub-Vault-V2/04-Trends/github_trending.md` — parsed for repo dropdown in Research stage

## Verification

1. `pip install streamlit` into the active venv.
2. `streamlit run control_room.py` → opens browser at `http://localhost:8501`.
3. Smoke test each stage in order: press Trending → wait → press Research → press Ideation → … → Cascade.
4. Open Dev Logs while a long stage (Research, YT Pipeline) is running and confirm stdout streams live.
5. Confirm new artifacts land in correct vault folders and dropdowns refresh on next interaction.
6. Kill streamlit mid-run and reopen — confirm running flag resets cleanly.

## Out of scope

- Authentication / multi-user
- Persistent job history beyond session_state
- Editing artifacts in-browser (Obsidian handles that)
- Touching the FastAPI backend
- Parallel job execution
