// Stage workspace — used by Trends/Research/Ideation/Hooks/Distribution

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

function StageWorkspace({ stageId, onBack, initialState = {} }) {
  const s = STAGES[stageId];
  const [prompt, setPrompt] = useState(initialState.prompt || "");
  const [files, setFiles] = useState(initialState.files || []);
  const [urlDraft, setUrlDraft] = useState("");
  const [urls, setUrls] = useState(initialState.urls || []);
  const [runState, setRunState] = useState(initialState.runState || "idle"); // idle | loading | done
  const [historyOpen, setHistoryOpen] = useState(false);

  // Reset when stage changes
  useEffect(() => {
    setPrompt(initialState.prompt || "");
    setFiles(initialState.files || []);
    setUrls(initialState.urls || []);
    setRunState(initialState.runState || "idle");
    setUrlDraft("");
    setHistoryOpen(false);
    // eslint-disable-next-line
  }, [stageId]);

  const handleRun = () => {
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
          onRun={handleRun} />
        
        <StackedPanel
          front={<OutputZone stage={s} runState={runState} />}
          back={<SourcesPanel stageId={stageId} />} />
        
      </div>

      <HistoryDrawer stage={s} open={historyOpen} onClose={() => setHistoryOpen(false)} />
    </div>);

}

function InputZone({ stage, prompt, setPrompt, files, setFiles, urls, setUrls, urlDraft, setUrlDraft, handleUrlKey, runState, onRun }) {
  const [mode, setMode] = useState("fast");
  const showModeToggle = stage.id === "research";
  const modeMeta = mode === "fast"
    ? "~6s · single-pass synthesis"
    : "~45s · multi-source cross-check, citations";

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
                onClick={() => setMode("fast")}>
                <Icon.Zap size={12} />
                Fast
              </button>
              <button
                type="button"
                className={"mode-toggle-option" + (mode === "deep" ? " is-active" : "")}
                onClick={() => setMode("deep")}>
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

      <button
        className={"run-btn" + (runState === "loading" ? " loading" : runState === "done" ? " done" : "")}
        onClick={onRun}
        disabled={runState === "loading"}>
        
        {runState === "loading" ?
        <>
            <span className="spinner-icon" style={{ display: "grid", placeItems: "center", animation: "spin 0.8s linear infinite" }}>
              <Icon.Loader size={14} />
            </span>
            Running…
          </> :
        runState === "done" ?
        <>
            <Icon.Check size={14} />
            Done — View Results
          </> :

        <>
            <Icon.Play size={13} />
            {stage.runCta}
          </>
        }
      </button>
    </section>);

}

function OutputZone({ stage, runState }) {
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
            Add a prompt, paste a URL or drop context — then hit {stage.runCta}.
          </div>
        </div>
      </section>);

  }
  if (runState === "loading") {
    return (
      <section className="output-zone">
        <div className="output-meta">
          <span>Running {stage.label}… · streaming from Claude Sonnet</span>
        </div>
        <div className="output-body">
          <div className="skeleton skeleton-row long" />
          <div className="skeleton skeleton-row medium" />
          <div className="skeleton skeleton-block" />
          <div className="skeleton skeleton-row long" />
          <div className="skeleton skeleton-row short" />
          <div className="skeleton skeleton-row medium" />
          <div className="skeleton skeleton-block" />
          <div className="skeleton skeleton-row long" />
          <div className="skeleton skeleton-row short" />
        </div>
      </section>);

  }

  const renderer = OUTPUTS[stage.id];
  return (
    <section className="output-zone">
      <div className="output-meta">
        <span>Generated 2 min ago · 1,240 tokens · via Claude Sonnet</span>
        <div className="output-meta-actions">
          <button className="btn-icon" title="Copy"><Icon.Copy size={14} /></button>
          <button className="btn-icon" title="Save to Vault"><Icon.Save size={14} /></button>
          <button className="btn-icon" title="Share"><Icon.Share2 size={14} /></button>
        </div>
      </div>
      <div className="output-body md">
        {renderer ? renderer() : <p>No output renderer yet.</p>}
      </div>
    </section>);

}

// --- Output renderers per stage -----------------------------
const OUTPUTS = {
  trends: () =>
  <>
      <h1>AI dev-tools — week of May 19</h1>
      <p>
        Three signals broke containment this week. The strongest is a <strong>frustration arc around AI IDEs</strong> —
        Cursor users hitting context limits, Cline picking up the spillover. A second wave is forming around
        <strong> local-first AI dev loops</strong> (RAG, code search, agents that run offline).
      </p>
      <h2>Top signals</h2>
      <ol>
        <li><strong>"Cline vs Cursor"</strong> — 4.2× volume vs last week. Discourse is shifting from features to <em>cost &amp; lock-in</em>.</li>
        <li><strong>Llama 3.3 + 24GB consumer GPUs</strong> — viral threads on r/LocalLLaMA, 7 high-engagement YT shorts in 72h.</li>
        <li><strong>v0 + product-engineer hybrid</strong> — peaking discussion on "is the senior PM dead?"</li>
        <li><strong>Bun 1.2</strong> — Node compatibility milestone is being framed as a Node killer (overblown but trending).</li>
      </ol>
      <h2>Suggested angles</h2>
      <ul>
        <li>"I tried Cline for a week. Here's why I'm switching." — frustration → solution arc</li>
        <li>"You can run Llama on a $400 GPU now. Here's the build." — accessibility + spec porn</li>
        <li>"v0 made my whole team uncomfortable" — controversy + workplace narrative</li>
      </ul>
      <blockquote>
        Heads up: the Bun vs Node angle is saturating fast. If you take it, ship within 4 days.
      </blockquote>
    </>,

  research: () =>
  <>
      <h1>Why AI tutorial videos go viral</h1>
      <p>
        Across <strong>1,240 sample videos</strong> &gt;500k views in the past 90 days, viral AI tutorials share four structural
        traits. None of them are about production quality. All of them are about <em>compression</em>.
      </p>
      <h2>1 · The first 11 seconds make or break</h2>
      <p>
        Top-quartile videos open with a <strong>working demo</strong>, not a face cam. 78% show the finished result running
        before the creator says a word. The hypothesis (and the dropoff data backs it): viewers don't need to be told what
        they're getting — they need to <em>see</em> the payoff is real.
      </p>
      <h2>2 · Tooling specificity outperforms abstract concepts</h2>
      <p>
        Titles naming specific tools (<code>Claude Code</code>, <code>llama.cpp</code>, <code>Cursor</code>) outperform generic
        ones ("AI agent", "LLM workflow") by <strong>3.4×</strong> on impressions-to-CTR.
      </p>
      <h2>3 · The "lazy build" narrative is the dominant template</h2>
      <p>
        61% of viral tutorials lean on some flavor of <em>"I built X in Y minutes / lines / hours"</em>. The constraint is
        load-bearing — it gives the viewer a binary success metric to measure the demo against.
      </p>
      <h2>4 · Mid-roll friction is the new outro</h2>
      <p>
        Channels averaging 80%+ AVD park their CTA at <strong>~55% into the video</strong>, not the end. Watchers who have
        invested half their time are most receptive — and they convert at <strong>2.1×</strong> the rate of end-of-video CTAs.
      </p>
      <hr />
      <h2>Sources</h2>
      <ul>
        <li><a href="#">YouTube Data API — Top AI tutorials, 90d window</a> (n=1,240)</li>
        <li><a href="#">Tubular — Audience retention curves, AI/dev verticals</a></li>
        <li><a href="#">Channel-level interviews</a> — Fireship, Theo, AI Jason, NetworkChuck</li>
        <li>9 more sources in vault</li>
      </ul>
    </>,

  ideation: () =>
  <>
      <h1>12 ideas — Channel: dev-leaning, beginner-friendly</h1>
      <p>Ranked by predicted retention × topic momentum, using your last 6 months of analytics as the baseline.</p>
      <h2>Top 5</h2>
      <ol>
        <li>
          <strong>I built a local RAG in 20 minutes (no API calls, no cloud).</strong>
          <br /><em>Lazy-build template + privacy angle. Predicts ~340k views @ 7.6% CTR.</em>
        </li>
        <li>
          <strong>Cursor lost me. Here's the 4-tool setup I use now.</strong>
          <br /><em>Frustration arc, hot timing. Audience is primed (see Trends report).</em>
        </li>
        <li>
          <strong>The smallest LLM that's actually useful for code.</strong>
          <br /><em>Spec-porn + accessibility. Could pair with a sponsor in the local-AI space.</em>
        </li>
        <li>
          <strong>Why your AI agent is bad (and 3 prompts that fix it).</strong>
          <br /><em>Listicle + how-to. Lower ceiling, more dependable floor.</em>
        </li>
        <li>
          <strong>I gave Claude my entire codebase. Here's what it found.</strong>
          <br /><em>Voyeurism angle. Strong shareability inside dev circles.</em>
        </li>
      </ol>
      <h2>Long tail (6–12)</h2>
      <p>7 more ideas scored ≥6.0 — see expanded list in the vault.</p>
    </>,

  hooks: () =>
  <>
      <h1>5 hooks — "Local RAG in 20 minutes"</h1>
      <p style={{ color: "var(--text-secondary)" }}>Each hook is &lt;9 seconds. Score is predicted 15-second retention vs your channel average.</p>
      <div className="hook-list">
        {[
      { text: "I just built a RAG system that runs on my laptop. No API calls. No subscription. Here's the entire thing in twenty minutes.", score: 9.1, pattern: "demo-first, constraint" },
      { text: "Everyone is paying for AI coding tools. I'm not. And after today, you won't either.", score: 8.7, pattern: "contrarian, audience-flatter" },
      { text: "This is the file every developer should have. It's 47 lines. It replaces $200 of subscriptions.", score: 8.4, pattern: "object-first, numbers" },
      { text: "What you're looking at is running entirely offline. Search. Memory. Reasoning. All of it.", score: 8.0, pattern: "screen-first, list" },
      { text: "I spent six months on this so you don't have to. Here is local RAG in twenty minutes.", score: 7.6, pattern: "sacrifice + payoff" }].
      map((h, i) =>
      <div key={i} className="hook-card" style={{ "--stage-color": "var(--stage-hooks)" }}>
            <div className="hook-num">{i + 1}</div>
            <div className="hook-body">
              <p className="hook-text">"{h.text}"</p>
              <div className="hook-meta">
                <span className="hook-score">▲ {h.score.toFixed(1)} retention</span>
                <span>·</span>
                <span>{h.pattern}</span>
              </div>
            </div>
          </div>
      )}
      </div>
    </>,

  distribution: () =>
  <>
      <h1>Distribution kit — "Local RAG in 20 minutes"</h1>
      <h2>Title candidates</h2>
      <ol>
        <li>I built a RAG that runs on my laptop. In 20 minutes.</li>
        <li>You don't need an API. (Local RAG, 47 lines)</li>
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
      <h2>Chapters · 7 generated</h2>
      <h2>Thumbnail brief</h2>
      <p>
        Left: <strong>laptop with terminal open</strong>, "OFFLINE" label glowing. Right:
        face cam, mild shock expression. Top text: <code>20 MIN. NO API.</code> — punch font, yellow.
      </p>
    </>,

  title: () =>
  <>
      <h1>5 titles — "Local RAG in 20 minutes"</h1>
      <p style={{ color: "var(--text-secondary)" }}>Each ranked against your channel's last-12-months CTR baseline (median 7.8%).</p>
      <ol>
        <li><strong>I built a RAG that runs on my laptop. In 20 minutes.</strong> <em>(predicted CTR 9.4%)</em></li>
        <li><strong>You don't need an API. (Local RAG, 47 lines)</strong> <em>(9.1%)</em></li>
        <li><strong>This RAG runs offline. It cost me $0 to build.</strong> <em>(8.7%)</em></li>
        <li><strong>20 minutes. 47 lines. No API key.</strong> <em>(8.5%)</em></li>
        <li><strong>I gave Claude my entire codebase… locally.</strong> <em>(7.9%)</em></li>
      </ol>
      <h2>Why these work</h2>
      <ul>
        <li>Constraints up front (numbers, scope) outperform abstract titles by <strong>3.4×</strong>.</li>
        <li>"No API" wins the cost-sensitive search traffic.</li>
        <li>First-person framing ("I built…") outperforms second-person on this channel.</li>
      </ul>
      <blockquote>
        Heads up: option 2 reads as clickbait to ~30% of your audience. Use it only if the body delivers in 90 seconds.
      </blockquote>
    </>,

  outline: () =>
  <>
      <h1>Outline — "Local RAG in 20 minutes"</h1>
      <p style={{ color: "var(--text-secondary)" }}>8 sections · target runtime 20:30 · retention shape: demo-first, mid-roll CTA</p>
      <ol>
        <li><strong>The setup (00:00–01:30)</strong> — working demo on screen, narrate the claim.</li>
        <li><strong>Why local matters (01:30–04:12)</strong> — cost + privacy framing in one minute.</li>
        <li><strong>Embedding model: nomic-embed-text (04:12–07:40)</strong> — install + first query, no fluff.</li>
        <li><strong>Vector store: sqlite-vss (07:40–11:05)</strong> — schema + insert path.</li>
        <li><strong>Putting it together (11:05–16:20)</strong> — wiring + retrieval loop. <em>CTA loop here at 11:00.</em></li>
        <li><strong>Live demo on my codebase (16:20–18:45)</strong> — real query, real answer.</li>
        <li><strong>Where it breaks (18:45–20:10)</strong> — honest failure modes. Builds trust.</li>
        <li><strong>Outro + next video tease (20:10–20:30)</strong></li>
      </ol>
      <h2>Retention shape target</h2>
      <p>Demo on screen by 0:02. Pre-pay the hook by 0:30. CTA at the 11-minute mark (≈55% of runtime, matching top-channel pattern).</p>
    </>

};

function HistoryDrawer({ stage, open, onClose }) {
  const items = [
  { time: "Today, 10:42", prompt: "AI developer tools, productivity apps, LLMs", words: 1240 },
  { time: "Yesterday, 18:11", prompt: "Local-first AI for indie devs", words: 980 },
  { time: "May 18, 14:07", prompt: "Why dev YouTube is shifting to short-form", words: 1820 },
  { time: "May 16, 09:55", prompt: "Cursor vs Cline weekly scan", words: 740 },
  { time: "May 14, 22:18", prompt: "What's hot in agentic frameworks", words: 1450 }];

  return (
    <>
      <div className={"drawer-backdrop" + (open ? " open" : "")} onClick={onClose} />
      <aside className={"drawer" + (open ? " open" : "")} style={{ "--stage-color": stage.color }}>
        <div className="drawer-handle" aria-hidden="true">
          <Icon.History size={16} />
          <span className="drawer-handle-text">History</span>
          <span className="drawer-handle-count">{items.length}</span>
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
            {items.map((it, i) =>
            <div key={i} className="history-item">
                <div className="history-time">{it.time}</div>
                <div className="history-prompt">{it.prompt}</div>
                <div className="history-stat">{it.words.toLocaleString()} words generated</div>
              </div>
            )}
          </div>
        </div>
      </aside>
    </>);

}

window.StageWorkspace = StageWorkspace;