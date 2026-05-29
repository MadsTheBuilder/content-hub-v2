"""Control Room — Streamlit UI for Content Hub V2 skill engine."""

import queue
import threading
import time
from pathlib import Path

import streamlit as st

from runner import run_in_thread
from vault_index import (
    latest,
    list_hooks,
    list_ideas,
    list_outlines,
    list_research_briefs,
    list_trending_repos,
)

VAULT = Path(__file__).parent.parent / "Content-Hub-Vault-V2"

st.set_page_config(page_title="Content Hub Control Room", layout="wide")
st.title("Content Hub Control Room")

# ── session state ─────────────────────────────────────────────────────────────
if "log_q" not in st.session_state:
    st.session_state.log_q = queue.Queue()
    st.session_state.running = False
    st.session_state.logs = []
    st.session_state.last_artifact = None

# ── sidebar ───────────────────────────────────────────────────────────────────
stage = st.sidebar.radio(
    "Stage",
    [
        "Trending",
        "Research",
        "Ideation",
        "Title",
        "Hook",
        "Outline",
        "Short-form",
        "Cascade",
        "YT Pipeline",
        "— Run Full Pipeline —",
    ],
)


# ── helpers ───────────────────────────────────────────────────────────────────

def _newest_mtime(folder: str, pattern: str = "*.md") -> float:
    p = latest(folder, pattern)
    return p.stat().st_mtime if p else 0.0


def _launch(cmd: list[str], output_folder: str, output_pattern: str = "*.md"):
    st.session_state.running = True
    st.session_state.logs = []
    st.session_state.last_artifact = None
    st.session_state._output_folder = output_folder
    st.session_state._output_pattern = output_pattern
    st.session_state._mtime_before = _newest_mtime(output_folder, output_pattern)
    run_in_thread(cmd, st.session_state.log_q)


def _drain_logs() -> bool:
    """Pull lines from queue into session_state.logs. Returns True when job exits."""
    finished = False
    while not st.session_state.log_q.empty():
        line = st.session_state.log_q.get_nowait()
        if line.startswith("__EXIT__"):
            st.session_state.running = False
            finished = True
        else:
            st.session_state.logs.append(line)
    return finished


def _detect_artifact():
    folder = st.session_state.get("_output_folder")
    pattern = st.session_state.get("_output_pattern", "*.md")
    before = st.session_state.get("_mtime_before", 0.0)
    if not folder:
        return
    p = latest(folder, pattern)
    if p and p.stat().st_mtime > before:
        st.session_state.last_artifact = p


# ── per-stage panes ───────────────────────────────────────────────────────────

if stage == "Trending":
    st.header("Trending Repos")
    st.caption("Fetches GitHub trending for last 7 and 30 days → `04-Trends/`")
    if st.button("Fetch Last 7d & 30d", disabled=st.session_state.running):
        _launch(["python", "scripts/github_trending.py"], "04-Trends")

elif stage == "Research":
    st.header("Research")
    niche = st.text_input("Niche / topic", placeholder='e.g. "AI agents"')
    repos = list_trending_repos()
    selected_repos = st.multiselect("Filter to repos (optional)", repos)
    mode = st.radio("Mode", ["deep", "fast"], horizontal=True)
    if st.button("Run Researcher", disabled=st.session_state.running):
        if not niche.strip():
            st.error("Niche is required.")
        else:
            cmd = ["python", "-m", "skills.researcher", "--niche", niche, "--mode", mode]
            if selected_repos:
                cmd += ["--repos"] + selected_repos
            _launch(cmd, "10-Research")

elif stage == "Ideation":
    st.header("Ideation")
    briefs = list_research_briefs()
    brief = (
        st.selectbox("Research brief", briefs, format_func=lambda p: p.name)
        if briefs
        else None
    )
    if not briefs:
        st.warning("No research briefs found. Run Research first.")
    default_topic = brief.stem.split("_", 2)[-1].replace("_", " ") if brief else ""
    topic = st.text_input("Topic", value=default_topic)
    if st.button("Generate 9 Ideas", disabled=st.session_state.running or not briefs):
        if not topic.strip():
            st.error("Topic is required.")
        else:
            cmd = ["python", "-m", "skills.ideation", "--topic", topic]
            if brief:
                cmd += ["--research-file", str(brief)]
            _launch(cmd, "02-Ideas")

elif stage == "Title":
    st.header("Title")
    ideas = list_ideas()
    idea = (
        st.selectbox("Idea file", ideas, format_func=lambda p: p.name)
        if ideas
        else None
    )
    if not ideas:
        st.warning("No idea files found. Run Ideation first.")
    default_concept = idea.stem.replace("_", " ") if idea else ""
    concept = st.text_input("Concept (edit or override)", value=default_concept)
    if st.button("Draft Titles", disabled=st.session_state.running or not ideas):
        if not concept.strip():
            st.error("Concept is required.")
        else:
            _launch(["python", "-m", "skills.title", concept], "07-Titles")

elif stage == "Hook":
    st.header("Hook")
    topic = st.text_input("Topic")
    platform = st.selectbox("Platform", ["yt-long", "yt-shorts", "tiktok", "reels"])
    audience = st.text_input("Audience", value="AI builders and content creators")
    fmt = st.radio("Format", ["short", "medium", "long"], index=1, horizontal=True)
    if st.button("Generate Hooks", disabled=st.session_state.running):
        if not topic.strip():
            st.error("Topic is required.")
        else:
            _launch(
                ["python", "-m", "skills.hook", topic,
                 "--platform", platform, "--audience", audience, "--format", fmt],
                "05-Hooks",
            )

elif stage == "Outline":
    st.header("Outline")
    topic = st.text_input("Topic")
    hooks = list_hooks()
    hook_options = [None] + hooks
    hook = st.selectbox(
        "Hook file (optional)",
        hook_options,
        format_func=lambda p: p.name if p else "(none)",
    )
    length = st.slider("Length (minutes)", 5, 15, 8)
    platform = st.radio("Platform", ["yt-long", "yt-shorts"], horizontal=True)
    if st.button("Build Outline", disabled=st.session_state.running):
        if not topic.strip():
            st.error("Topic is required.")
        else:
            cmd = ["python", "-m", "skills.outline", topic,
                   "--length", str(length), "--platform", platform]
            if hook:
                cmd += ["--hook-path", str(hook)]
            _launch(cmd, "06-Outlines")

elif stage == "Short-form":
    st.header("Short-form")
    input_mode = st.radio("Input mode", ["Vault files", "YouTube URL"], horizontal=True)
    if input_mode == "Vault files":
        briefs = list_research_briefs()
        outlines = list_outlines()
        brief = (
            st.selectbox("Research file", briefs, format_func=lambda p: p.name)
            if briefs else None
        )
        outline = (
            st.selectbox("Outline file", outlines, format_func=lambda p: p.name)
            if outlines else None
        )
        if not briefs:
            st.warning("No research briefs found. Run Research first.")
        if not outlines:
            st.warning("No outlines found. Run Outline first.")
        title_override = st.text_input("Title override (optional)")
        ready = bool(briefs and outlines)
        if st.button("Generate Shorts", disabled=st.session_state.running or not ready):
            cmd = ["python", "-m", "skills.short_form",
                   "--research-file", str(brief), "--outline-file", str(outline)]
            if title_override.strip():
                cmd += ["--title", title_override]
            _launch(cmd, "09-Shorts")
    else:
        url = st.text_input("YouTube URL")
        title_override = st.text_input("Title override (optional)")
        if st.button("Generate Shorts", disabled=st.session_state.running):
            if not url.strip():
                st.error("URL is required.")
            else:
                cmd = ["python", "-m", "skills.short_form", url]
                if title_override.strip():
                    cmd += ["--title", title_override]
                _launch(cmd, "09-Shorts")

elif stage == "Cascade":
    st.header("Cascade (Distribution Pack)")
    input_mode = st.radio("Input mode", ["Vault files", "YouTube URL"], horizontal=True)
    if input_mode == "Vault files":
        briefs = list_research_briefs()
        outlines = list_outlines()
        brief = (
            st.selectbox("Research file", briefs, format_func=lambda p: p.name)
            if briefs else None
        )
        outline = (
            st.selectbox("Outline file", outlines, format_func=lambda p: p.name)
            if outlines else None
        )
        if not briefs:
            st.warning("No research briefs found. Run Research first.")
        if not outlines:
            st.warning("No outlines found. Run Outline first.")
        title_override = st.text_input("Title override (optional)")
        ready = bool(briefs and outlines)
        if st.button("Distribution Pack", disabled=st.session_state.running or not ready):
            cmd = ["python", "-m", "skills.cascade",
                   "--research-file", str(brief), "--outline-file", str(outline)]
            if title_override.strip():
                cmd += ["--title", title_override]
            _launch(cmd, "08-Distribution")
    else:
        url = st.text_input("YouTube URL")
        title_override = st.text_input("Title override (optional)")
        if st.button("Distribution Pack", disabled=st.session_state.running):
            if not url.strip():
                st.error("URL is required.")
            else:
                cmd = ["python", "-m", "skills.cascade", url]
                if title_override.strip():
                    cmd += ["--title", title_override]
                _launch(cmd, "08-Distribution")

elif stage == "YT Pipeline":
    st.header("YT Pipeline")
    yt_mode = st.radio("Mode", ["run", "search"], horizontal=True)
    topic = st.text_input("Topic")
    if yt_mode == "run":
        urls_raw = st.text_area("YouTube URLs (comma-separated)")
        artifacts = st.checkbox("Generate artifacts")
        if st.button("Research from URLs", disabled=st.session_state.running):
            if not topic.strip() or not urls_raw.strip():
                st.error("Topic and URLs are required.")
            else:
                cmd = ["python", "-m", "skills.yt_pipeline", "run",
                       topic, urls_raw.strip()]
                if artifacts:
                    cmd.append("--artifacts")
                _launch(cmd, "10-Research")
    else:
        also = st.text_input("Also search (comma-separated queries, optional)")
        if st.button("Search Topics", disabled=st.session_state.running):
            if not topic.strip():
                st.error("Topic is required.")
            else:
                cmd = ["python", "-m", "skills.yt_pipeline", "search", topic]
                if also.strip():
                    cmd += ["--also", also.strip()]
                _launch(cmd, "10-Research")

elif stage == "— Run Full Pipeline —":
    st.header("Full Pipeline")
    st.caption("Trending → Research → Ideation — sequential, feeds freshest artifact at each step.")
    niche = st.text_input("Niche / topic")
    research_mode = st.radio("Research mode", ["deep", "fast"], horizontal=True)

    def _pipeline(niche: str, mode: str, log_q: queue.Queue):
        import subprocess
        repo = Path(__file__).parent.parent

        def _run(cmd):
            proc = subprocess.Popen(
                cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, bufsize=1, encoding="utf-8", errors="replace",
            )
            for line in proc.stdout:
                log_q.put(line.rstrip())
            proc.wait()
            return proc.returncode

        log_q.put("=== STEP 1: Trending ===")
        _run(["python", "scripts/github_trending.py"])

        log_q.put("=== STEP 2: Research ===")
        _run(["python", "-m", "skills.researcher", "--niche", niche, "--mode", mode])

        log_q.put("=== STEP 3: Ideation ===")
        brief = latest("10-Research")
        cmd = ["python", "-m", "skills.ideation", "--topic", niche]
        if brief:
            cmd += ["--research-file", str(brief)]
        rc = _run(cmd)

        log_q.put(f"__EXIT__ {rc}")

    if st.button("Run Full Pipeline", disabled=st.session_state.running):
        if not niche.strip():
            st.error("Niche is required.")
        else:
            st.session_state.running = True
            st.session_state.logs = []
            st.session_state.last_artifact = None
            st.session_state._output_folder = "02-Ideas"
            st.session_state._output_pattern = "*.md"
            st.session_state._mtime_before = _newest_mtime("02-Ideas")
            threading.Thread(
                target=_pipeline,
                args=(niche, research_mode, st.session_state.log_q),
                daemon=True,
            ).start()


# ── drain + artifact detection ────────────────────────────────────────────────
finished = _drain_logs()
if finished:
    _detect_artifact()

if st.session_state.last_artifact:
    st.success(f"Done! → `{st.session_state.last_artifact.name}`")
    st.code(str(st.session_state.last_artifact))

# ── dev logs ──────────────────────────────────────────────────────────────────
with st.expander("Dev Logs ▸", expanded=st.session_state.running):
    st.code("\n".join(st.session_state.logs[-200:]) or "(no output yet)")

# ── polling loop while running ────────────────────────────────────────────────
if st.session_state.running:
    with st.spinner("Running…"):
        time.sleep(0.5)
    st.rerun()
