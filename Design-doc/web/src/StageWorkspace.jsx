import { useState, useEffect } from 'react';
import Icon from './Icons.jsx';
import { SourcesPanel, StackedPanel } from './SourcesPanel.jsx';
import { runStage, getRecent, ConflictError } from './api.js';
import { announceStart, announceDone, announceFail } from './jobActivity.js';
import useJobStream from './hooks/useJobStream.js';
import VaultPicker from './VaultPicker.jsx';
import OutputBrowser from './OutputBrowser.jsx';
import MarkdownViewer from './MarkdownViewer.jsx';

const STAGES = {
  trends: {
    id: "trends",
    label: "Trends",
    icon: "TrendingUp",
    color: "var(--stage-trends)",
    eyebrow: "Pipeline · 01",
    desc: "Discover what's trending across AI, dev, and creator spaces.",
    tagline: "What's breaking. What's saturating. What's next.",
    promptLabel: "What space should I trend-scan?",
    placeholder: "e.g. AI developer tools, productivity apps, LLMs",
    runCta: "Run Trends"
  },
  research: {
    id: "research",
    label: "Research",
    icon: "FlaskConical",
    color: "var(--stage-research)",
    eyebrow: "Pipeline · 02",
    desc: "Deep-research a topic with sourced findings and angle ideas.",
    tagline: "Twelve sources in. One sharp answer out.",
    promptLabel: "What topic should I deep-research?",
    placeholder: "e.g. Why do AI tutorial videos go viral?",
    runCta: "Run Research"
  },
  ideation: {
    id: "ideation",
    label: "Ideation",
    icon: "Lightbulb",
    color: "var(--stage-ideation)",
    eyebrow: "Pipeline · 03",
    desc: "Generate video ideas scored against your channel signal.",
    tagline: "Twelve ideas. Ranked by signal.",
    promptLabel: "Generate ideas based on:",
    placeholder: "e.g. Use my latest research brief, focus on beginner devs",
    runCta: "Run Ideation"
  },
  hooks: {
    id: "hooks",
    label: "Hooks",
    icon: "Zap",
    color: "var(--stage-hooks)",
    eyebrow: "Pipeline · 04",
    desc: "Generate scroll-stopping hooks tuned to your channel voice.",
    tagline: "Stop the scroll. Hold the watch.",
    promptLabel: "What is the video about?",
    placeholder: "e.g. How to build a local RAG system in 20 minutes",
    runCta: "Run Hooks"
  },
  title: {
    id: "title",
    label: "Title",
    icon: "Type",
    color: "var(--stage-title)",
    eyebrow: "Pipeline · 05",
    desc: "Generate scroll-worthy video titles tuned to your channel's CTR baseline.",
    tagline: "Five titles. One that converts.",
    promptLabel: "What's the video about?",
    placeholder: "e.g. How to build a local RAG system in 20 minutes",
    runCta: "Run Title"
  },
  outline: {
    id: "outline",
    label: "Outline",
    icon: "ListTree",
    color: "var(--stage-outline)",
    eyebrow: "Pipeline · 06",
    desc: "Structure the video. Section labels, timestamps, retention shape.",
    tagline: "A spine you can shoot to.",
    promptLabel: "What's the video about?",
    placeholder: "e.g. Local RAG in 20 min — use my Hook + Title from the vault",
    runCta: "Run Outline"
  },
  distribution: {
    id: "distribution",
    label: "Distribution",
    icon: "Share2",
    color: "var(--stage-distribution)",
    eyebrow: "Pipeline · 07",
    desc: "Turn an outline into titles, thumbnails, descriptions, chapters.",
    tagline: "Outline in. Publish-ready out.",
    promptLabel: "What should I distribute?",
    placeholder: "e.g. Use the outline in my vault for my RAG video",
    runCta: "Run Distribution"
  }
};

const LIVE_STAGES = new Set(["research", "ideation", "hooks"]);
const TRENDS_FILE = "04-Trends/github_trending.md";
const STAGE_FOLDER = { trends: "04-Trends", research: "10-Research", ideation: "02-Ideas", hooks: "05-Hooks" };

// Out-of-scope stages keep fake renderers until their pipeline is wired
const OUTPUTS = {
  distribution: () =>
  <>
      <h1>Distribution kit &#8212; &#8220;Local RAG in 20 minutes&#8221;</h1>
      <h2>Title candidates</h2>
      <ol>
        <li>I built a RAG that runs on my laptop. In 20 minutes.</li>
        <li>You don&#8217;t need an API. (Local RAG, 47 lines)</li>
        <li>This RAG runs offline. It cost me $0 to build.</li>
      </ol>
      <h2>Description</h2>
      <pre><code>{`Local RAG in 20 minutes — no API calls, no cloud, no subscription.

00:00 — The setup
01:30 — Why local matters (cost + privacy)
04:12 — Embedding model: nomic-embed-text
07:40 — Vector store: sqlite-vss
11:05 — Putting it together
16:20 — Live demo on my codebase
18:45 — Where it breaks

Code: github.com/yourname/local-rag-demo
Tools: Ollama, sqlite-vss, nomic-embed-text`}</code></pre>
      <h2>Chapters &#183; 7 generated</h2>
      <h2>Thumbnail brief</h2>
      <p>
        Left: <strong>laptop with terminal open</strong>, &#8220;OFFLINE&#8221; label glowing. Right:
        face cam, mild shock expression. Top text: <code>20 MIN. NO API.</code> &#8212; punch font, yellow.
      </p>
    </>,

  title: () =>
  <>
      <h1>5 titles &#8212; &#8220;Local RAG in 20 minutes&#8221;</h1>
      <p style={{ color: "var(--text-secondary)" }}>Each ranked against your channel&#8217;s last-12-months CTR baseline (median 7.8%).</p>
      <ol>
        <li><strong>I built a RAG that runs on my laptop. In 20 minutes.</strong> <em>(predicted CTR 9.4%)</em></li>
        <li><strong>You don&#8217;t need an API. (Local RAG, 47 lines)</strong> <em>(9.1%)</em></li>
        <li><strong>This RAG runs offline. It cost me $0 to build.</strong> <em>(8.7%)</em></li>
        <li><strong>20 minutes. 47 lines. No API key.</strong> <em>(8.5%)</em></li>
        <li><strong>I gave Claude my entire codebase&#8230; locally.</strong> <em>(7.9%)</em></li>
      </ol>
      <h2>Why these work</h2>
      <ul>
        <li>Constraints up front (numbers, scope) outperform abstract titles by <strong>3.4&#215;</strong>.</li>
        <li>&#8220;No API&#8221; wins the cost-sensitive search traffic.</li>
        <li>First-person framing (&#8220;I built&#8230;&#8221;) outperforms second-person on this channel.</li>
      </ul>
      <blockquote>
        Heads up: option 2 reads as clickbait to ~30% of your audience. Use it only if the body delivers in 90 seconds.
      </blockquote>
    </>,

  outline: () =>
  <>
      <h1>Outline &#8212; &#8220;Local RAG in 20 minutes&#8221;</h1>
      <p style={{ color: "var(--text-secondary)" }}>8 sections &#183; target runtime 20:30 &#183; retention shape: demo-first, mid-roll CTA</p>
      <ol>
        <li><strong>The setup (00:00&#8211;01:30)</strong> &#8212; working demo on screen, narrate the claim.</li>
        <li><strong>Why local matters (01:30&#8211;04:12)</strong> &#8212; cost + privacy framing in one minute.</li>
        <li><strong>Embedding model: nomic-embed-text (04:12&#8211;07:40)</strong> &#8212; install + first query, no fluff.</li>
        <li><strong>Vector store: sqlite-vss (07:40&#8211;11:05)</strong> &#8212; schema + insert path.</li>
        <li><strong>Putting it together (11:05&#8211;16:20)</strong> &#8212; wiring + retrieval loop. <em>CTA loop here at 11:00.</em></li>
        <li><strong>Live demo on my codebase (16:20&#8211;18:45)</strong> &#8212; real query, real answer.</li>
        <li><strong>Where it breaks (18:45&#8211;20:10)</strong> &#8212; honest failure modes. Builds trust.</li>
        <li><strong>Outro + next video tease (20:10&#8211;20:30)</strong></li>
      </ol>
      <h2>Retention shape target</h2>
      <p>Demo on screen by 0:02. Pre-pay the hook by 0:30. CTA at the 11-minute mark (&#8776;55% of runtime, matching top-channel pattern).</p>
    </>
};

function StageWorkspace({ stageId, onBack, initialState = {} }) {
  const s = STAGES[stageId];
  const [prompt, setPrompt] = useState(initialState.prompt || "");
  const [files, setFiles] = useState(initialState.files || []);
  const [urlDraft, setUrlDraft] = useState("");
  const [urls, setUrls] = useState(initialState.urls || []);
  const [runState, setRunState] = useState(initialState.runState || "idle");
  const [historyOpen, setHistoryOpen] = useState(false);
  const [mode, setMode] = useState("fast");
  const [jobId, setJobId] = useState(null);
  const [researchFile, setResearchFile] = useState(null);
  const [jobResult, setJobResult] = useState(null);
  const [jobError, setJobError] = useState(null);
  const [conflictNotice, setConflictNotice] = useState(false);

  const jobStream = useJobStream(jobId);

  /* eslint-disable react-hooks/set-state-in-effect, react-hooks/exhaustive-deps */
  useEffect(() => {
    setPrompt(initialState.prompt || "");
    setFiles(initialState.files || []);
    setUrls(initialState.urls || []);
    setRunState(initialState.runState || "idle");
    setUrlDraft("");
    setHistoryOpen(false);
    setMode("fast");
    setJobId(null);
    setResearchFile(null);
    setJobResult(null);
    setJobError(null);
    setConflictNotice(false);
  }, [stageId]);
  /* eslint-enable react-hooks/set-state-in-effect, react-hooks/exhaustive-deps */

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (jobStream.status === "running") setRunState("loading");
    else if (jobStream.status === "completed") {
      setRunState("done");
      setJobResult(jobStream.result);
      announceDone(stageId);
    } else if (jobStream.status === "failed") {
      setRunState("idle");
      setJobError(jobStream.error);
      announceFail(stageId);
    }
  }, [jobStream.status, jobStream.result, jobStream.error, stageId]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const handleRun = async () => {
    if (stageId === "trends") return;

    if (LIVE_STAGES.has(stageId)) {
      setRunState("loading");
      setJobError(null);
      setConflictNotice(false);
      announceStart(stageId);
      try {
        const body = stageId === "research"
          ? { niche: prompt, repos: urls, mode }
          : { topic: prompt, research_file: researchFile || "" };
        const { job_id } = await runStage(stageId, body);
        setJobId(job_id);
      } catch (e) {
        if (e instanceof ConflictError) {
          setConflictNotice(true);
          announceFail(stageId);
        } else {
          setJobError(e.message);
          announceFail(stageId);
        }
        setRunState("idle");
      }
      return;
    }

    setRunState("loading");
    setTimeout(() => setRunState("done"), 1400);
  };

  const handleUrlKey = (e) => {
    if (e.key === "Enter" && urlDraft.trim()) {
      e.preventDefault();
      setUrls([...urls, urlDraft.trim()]);
      setUrlDraft("");
    }
  };

  const IconCmp = Icon[s.icon];

  return (
    <div data-screen-label={s.label} style={{ "--stage-color": s.color }}>
      <div className="stage-banner">
        <div style={{ display: "flex", alignItems: "center", gap: 14, position: "relative", zIndex: 1 }}>
          <button className="back-btn" onClick={onBack} title="Back to Dashboard">
            <Icon.ArrowLeft size={16} />
          </button>
          <div className="stage-banner-icon"><IconCmp size={28} /></div>
        </div>
        <div className="stage-banner-text">
          <div className="stage-banner-eyebrow">{s.eyebrow}</div>
          <h1 className="stage-banner-title">{s.label}</h1>
          <p className="stage-banner-tagline">{s.tagline}</p>
        </div>
        <div className="stage-banner-actions">
          <button className="btn btn-ghost" onClick={() => setHistoryOpen(true)}>
            <Icon.History size={14} />
            History
          </button>
        </div>
        <div className="stage-banner-orb stage-banner-orb-1" aria-hidden="true" />
        <div className="stage-banner-orb stage-banner-orb-2" aria-hidden="true" />
      </div>

      <div className="stage-split">
        <InputZone
          stage={s}
          prompt={prompt} setPrompt={setPrompt}
          files={files} setFiles={setFiles}
          urls={urls} setUrls={setUrls}
          urlDraft={urlDraft} setUrlDraft={setUrlDraft}
          handleUrlKey={handleUrlKey}
          runState={runState}
          onRun={handleRun}
          mode={mode} onModeChange={setMode}
          researchFile={researchFile} onResearchFileChange={setResearchFile}
          conflictNotice={conflictNotice}
        />

        <StackedPanel
          front={
            <OutputZone
              stage={s}
              runState={runState}
              jobResult={jobResult}
              jobError={jobError}
              liveLines={jobStream.lines}
            />
          }
          back={<SourcesPanel stageId={stageId} />}
        />
      </div>

      <HistoryDrawer
        stage={s}
        open={historyOpen}
        onClose={() => setHistoryOpen(false)}
        folder={STAGE_FOLDER[stageId]}
      />
    </div>
  );
}

function InputZone({ stage, prompt, setPrompt, files, setFiles, urls, setUrls, urlDraft, setUrlDraft, handleUrlKey, runState, onRun, mode, onModeChange, researchFile, onResearchFileChange, conflictNotice }) {
  const isTrends = stage.id === "trends";
  const showModeToggle = stage.id === "research";
  const showVaultPicker = stage.id === "ideation" || stage.id === "hooks";
  const showUrlInput = stage.id === "research";
  const modeMeta = mode === "fast"
    ? "~6s · single-pass synthesis"
    : "~45s · multi-source cross-check, citations";

  if (isTrends) {
    return (
      <section className="input-zone">
        <div style={{ color: "var(--text-muted)", fontSize: 13 }}>
          Read-only &#183; auto-updated from vault.
        </div>
      </section>
    );
  }

  return (
    <section className="input-zone">
      {showModeToggle && (
        <>
          <div className="mode-toggle-row">
            <span className="mode-toggle-row-label">Mode</span>
            <div className="mode-toggle" data-mode={mode}>
              <span className="mode-toggle-slider" />
              <button
                type="button"
                className={"mode-toggle-option" + (mode === "fast" ? " is-active" : "")}
                onClick={() => onModeChange("fast")}>
                <Icon.Zap size={12} />
                Fast
              </button>
              <button
                type="button"
                className={"mode-toggle-option" + (mode === "deep" ? " is-active" : "")}
                onClick={() => onModeChange("deep")}>
                <Icon.FlaskConical size={12} />
                Deep Research
              </button>
            </div>
          </div>
          <div className="mode-toggle-meta">
            <span className="mode-toggle-meta-dot" />
            {modeMeta}
          </div>
        </>
      )}

      <div>
        <label className="field-label" htmlFor="prompt">{stage.promptLabel}</label>
        <div className="prompt-area">
          <textarea
            id="prompt"
            className="prompt-textarea"
            placeholder={stage.placeholder}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4} />
          <span className="char-count">{prompt.length}</span>
        </div>
      </div>

      {showVaultPicker ? (
        <div>
          <label className="field-label">Research file</label>
          <VaultPicker
            folder="10-Research"
            value={researchFile}
            onChange={onResearchFileChange}
            placeholder="Select research file…"
          />
        </div>
      ) : (
        <div>
          <label className="field-label">Add context</label>
          <div className="drop-zone">
            <Icon.Upload size={20} color="var(--text-muted)" />
            <div className="drop-zone-text">Drop files here</div>
            <div className="drop-zone-sub">or click to browse</div>
            <div className="format-pills">
              <span className="format-pill">.md</span>
              <span className="format-pill">.txt</span>
              <span className="format-pill">.pdf</span>
              <span className="format-pill">.docx</span>
            </div>
          </div>
          {files.length > 0 &&
          <div style={{ marginTop: 4 }}>
              {files.map((f, i) =>
            <span key={i} className="file-chip">
                  <span className="file-chip-icon"><Icon.FileText size={12} /></span>
                  {f}
                  <button className="chip-close" onClick={() => setFiles(files.filter((_, j) => j !== i))}>
                    <Icon.X size={12} />
                  </button>
                </span>
            )}
            </div>
          }
        </div>
      )}

      {showUrlInput && (
        <div>
          <label className="field-label">Or paste a URL</label>
          <div className="url-input-row">
            <Icon.Link size={14} color="var(--text-muted)" />
            <input
              type="text"
              className="url-input"
              placeholder="https://…"
              value={urlDraft}
              onChange={(e) => setUrlDraft(e.target.value)}
              onKeyDown={handleUrlKey} />
          </div>
          {urls.length > 0 &&
          <div style={{ marginTop: 4 }}>
              {urls.map((u, i) =>
            <span key={i} className="url-chip">
                  <span className="file-chip-icon"><Icon.Link size={12} /></span>
                  <span style={{ maxWidth: 220, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{u}</span>
                  <button className="chip-close" onClick={() => setUrls(urls.filter((_, j) => j !== i))}>
                    <Icon.X size={12} />
                  </button>
                </span>
            )}
            </div>
          }
        </div>
      )}

      {conflictNotice && (
        <p style={{ fontSize: 12, color: "var(--text-muted)", margin: "0 0 8px" }}>
          A job is already running — wait for it to finish.
        </p>
      )}
      <button
        className={"run-btn" + (runState === "loading" ? " loading" : runState === "done" ? " done" : "")}
        onClick={onRun}
        disabled={runState === "loading"}>

        {runState === "loading" ?
        <>
            <span className="spinner-icon" style={{ display: "grid", placeItems: "center", animation: "spin 0.8s linear infinite" }}>
              <Icon.Loader size={14} />
            </span>
            Running&#8230;
          </> :
        runState === "done" ?
        <>
            <Icon.Check size={14} />
            Done &#8212; View Results
          </> :

        <>
            <Icon.Play size={13} />
            {stage.runCta}
          </>
        }
      </button>
    </section>
  );
}

function OutputZone({ stage, runState, jobResult, jobError, liveLines }) {
  if (stage.id === "trends") {
    return (
      <section className="output-zone">
        <div className="output-meta">
          <span>Live from vault &#183; auto-updated</span>
        </div>
        <MarkdownViewer path={TRENDS_FILE} />
      </section>
    );
  }

  if (jobError) {
    return (
      <section className="output-zone">
        <div className="output-body">
          <p style={{ color: "var(--text-muted)", fontSize: 13 }}>Error: {jobError}</p>
        </div>
      </section>
    );
  }

  if (runState === "idle") {
    const EmptyIcon = Icon[stage.icon];
    return (
      <section className="output-zone">
        <div className="output-empty">
          <div className="output-empty-icon">
            <EmptyIcon size={26} />
          </div>
          <div style={{ fontSize: 14, color: "var(--text-secondary)" }}>
            Run {stage.label} to see results here
          </div>
          <div style={{ fontSize: 12, color: "var(--text-muted)", maxWidth: 320 }}>
            {stage.id === "ideation" || stage.id === "hooks"
              ? <>Add a prompt, select a research file &#8212; then hit {stage.runCta}.</>
              : <>Add a prompt, paste a URL or drop context &#8212; then hit {stage.runCta}.</>
            }
          </div>
        </div>
      </section>
    );
  }

  if (runState === "loading") {
    return (
      <section className="output-zone">
        <div className="output-meta">
          <span>Running {stage.label}&#8230; &#183; streaming from Claude Sonnet</span>
        </div>
        <div className="output-body">
          {LIVE_STAGES.has(stage.id) && liveLines.length > 0 ? (
            <div style={{ fontFamily: "monospace", fontSize: 12, lineHeight: 1.6 }}>
              {liveLines.map((line, i) => <div key={i}>{line}</div>)}
            </div>
          ) : (
            <>
              <div className="skeleton skeleton-row long" />
              <div className="skeleton skeleton-row medium" />
              <div className="skeleton skeleton-block" />
              <div className="skeleton skeleton-row long" />
              <div className="skeleton skeleton-row short" />
              <div className="skeleton skeleton-row medium" />
              <div className="skeleton skeleton-block" />
              <div className="skeleton skeleton-row long" />
              <div className="skeleton skeleton-row short" />
            </>
          )}
        </div>
      </section>
    );
  }

  // done
  if (LIVE_STAGES.has(stage.id)) {
    return (
      <section className="output-zone">
        <div className="output-meta">
          <span>Saved to vault</span>
          <div className="output-meta-actions">
            <button
              className="btn-icon"
              title="Copy path"
              onClick={() => navigator.clipboard.writeText(jobResult?.primary_path || "")}>
              <Icon.Copy size={14} />
            </button>
          </div>
        </div>
        <OutputBrowser result={jobResult} />
      </section>
    );
  }

  const renderer = OUTPUTS[stage.id];
  return (
    <section className="output-zone">
      <div className="output-meta">
        <span>Generated 2 min ago &#183; 1,240 tokens &#183; via Claude Sonnet</span>
        <div className="output-meta-actions">
          <button className="btn-icon" title="Copy"><Icon.Copy size={14} /></button>
          <button className="btn-icon" title="Save to Vault"><Icon.Save size={14} /></button>
          <button className="btn-icon" title="Share"><Icon.Share2 size={14} /></button>
        </div>
      </div>
      <div className="output-body md">
        {renderer ? renderer() : <p>No output renderer yet.</p>}
      </div>
    </section>
  );
}

function HistoryDrawer({ stage, open, onClose, folder }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selected, setSelected] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!open || !folder) return;
    setLoading(true);
    setSelected(null);
    getRecent(folder, 20)
      .then(setItems)
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [open, folder]);
  /* eslint-enable react-hooks/set-state-in-effect */

  return (
    <>
      <div className={"drawer-backdrop" + (open ? " open" : "")} onClick={onClose} />
      <aside className={"drawer" + (open ? " open" : "")} style={{ "--stage-color": stage.color }}>
        <div className="drawer-handle" aria-hidden="true">
          <Icon.History size={16} />
          <span className="drawer-handle-text">History</span>
          {items.length > 0 && <span className="drawer-handle-count">{items.length}</span>}
        </div>
        <div className="drawer-content">
          <header className="drawer-header">
            <div>
              <div className="drawer-eyebrow">{stage.label}</div>
              <h2 className="drawer-title">Run history</h2>
            </div>
            <button className="btn-icon" onClick={onClose} title="Close"><Icon.X size={14} /></button>
          </header>
          <div className="drawer-body">
            {selected ? (
              <>
                <button className="btn btn-ghost" onClick={() => setSelected(null)} style={{ marginBottom: 12 }}>
                  <Icon.ArrowLeft size={12} />
                  Back
                </button>
                <MarkdownViewer path={selected} />
              </>
            ) : loading ? (
              <>
                <div className="skeleton skeleton-row long" />
                <div className="skeleton skeleton-row medium" />
              </>
            ) : items.length === 0 ? (
              <p style={{ color: "var(--text-muted)", fontSize: 13 }}>No history yet.</p>
            ) : (
              items.map((it) => (
                <div key={it.path} className="history-item" style={{ cursor: "pointer" }} onClick={() => setSelected(it.path)}>
                  <div className="history-time">{it.modified || ""}</div>
                  <div className="history-prompt">{it.name}</div>
                </div>
              ))
            )}
          </div>
        </div>
      </aside>
    </>
  );
}

export default StageWorkspace;
