// Knowledge Brain workspace

function BrainWorkspace() {
  const [prompt, setPrompt] = useState(
    "The first second I saw the Vision Pro demo, I knew Apple was trying to do something most companies wouldn't even attempt. Watch what happens at 0:23…"
  );
  const [urls, setUrls] = useState(["https://youtube.com/watch?v=demo-tear-down"]);
  const [urlDraft, setUrlDraft] = useState("");
  const [runState, setRunState] = useState("done"); // start in "done" for spec screen #4
  const [openSections, setOpenSections] = useState({ 2: true }); // Structure Map open by default

  const toggle = (i) => setOpenSections((s) => ({ ...s, [i]: !s[i] }));
  const handleAnalyze = () => {
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

  return (
    <div data-screen-label="Knowledge Brain" style={{ "--stage-color": "var(--brain)" }}>
      <div className="stage-banner">
        <div style={{ display: "flex", alignItems: "center", gap: 14, position: "relative", zIndex: 1 }}>
          <div className="stage-banner-icon"><Icon.Brain size={28} /></div>
        </div>
        <div className="stage-banner-text">
          <div className="stage-banner-eyebrow">Knowledge Brain</div>
          <h1 className="stage-banner-title">The Brain</h1>
          <p className="stage-banner-tagline">Feed me — and I'll spit analysis.</p>
        </div>
        <div className="stage-banner-actions">
          <button className="btn btn-ghost">
            <Icon.History size={14} />
            History
          </button>
        </div>
        <div className="stage-banner-orb stage-banner-orb-1" aria-hidden="true" />
        <div className="stage-banner-orb stage-banner-orb-2" aria-hidden="true" />
      </div>

      <div className="brain-input-card">
        <label className="field-label">Paste content, drop a file, or enter a URL</label>
        <div className="prompt-area">
          <textarea
            className="prompt-textarea"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Paste the content you want to analyze…"
            rows={4}
          />
          <span className="char-count">{prompt.length}</span>
        </div>
        {urls.length > 0 && (
          <div style={{ marginTop: 6 }}>
            {urls.map((u, i) => (
              <span key={i} className="url-chip">
                <span className="file-chip-icon"><Icon.Link size={12} /></span>
                <span style={{ maxWidth: 280, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{u}</span>
                <button className="chip-close" onClick={() => setUrls(urls.filter((_, j) => j !== i))}>
                  <Icon.X size={12} />
                </button>
              </span>
            ))}
          </div>
        )}
        <div className="brain-toolbar">
          <button className="btn btn-ghost"><Icon.Upload size={14} /> Drop a file</button>
          <div className="url-input-row" style={{ flex: 1, maxWidth: 360 }}>
            <Icon.Link size={14} color="var(--text-muted)" />
            <input
              type="text"
              className="url-input"
              placeholder="Enter a URL…"
              value={urlDraft}
              onChange={(e) => setUrlDraft(e.target.value)}
              onKeyDown={handleUrlKey}
            />
          </div>
          <button className="run-btn" style={{ background: "var(--brain)", color: "var(--bg-base)" }} onClick={handleAnalyze} disabled={runState === "loading"}>
            {runState === "loading" ? (
              <>
                <span style={{ display: "grid", placeItems: "center", animation: "spin 0.8s linear infinite" }}>
                  <Icon.Loader size={14} />
                </span>
                Analyzing…
              </>
            ) : (
              <>
                <Icon.Play size={13} />
                Analyze
              </>
            )}
          </button>
        </div>
      </div>

      {runState === "idle" && (
        <div className="output-empty" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)", borderRadius: "var(--r-card)", padding: 60 }}>
          <div className="output-empty-icon" style={{ color: "var(--brain)" }}>
            <Icon.Brain size={28} />
          </div>
          <div style={{ fontSize: 14, color: "var(--text-secondary)" }}>Drop anything here to decode it</div>
          <div style={{ fontSize: 12, color: "var(--text-muted)", maxWidth: 320 }}>
            Transcripts, articles, threads, hooks. Paste it and we'll show you the machinery.
          </div>
        </div>
      )}

      {runState === "loading" && <BrainSkeleton />}

      {runState === "done" && (
        <div className="brain-stack">
          <StackedPanel
            front={<div className="brain-stack-face"><BrainResults openSections={openSections} toggle={toggle} /></div>}
            back={<SourcesPanel stageId="brain" />}
          />
        </div>
      )}
    </div>
  );
}

function BrainSkeleton() {
  return (
    <>
      <div className="score-grid">
        {[0,1,2].map(i => (
          <div key={i} className="score-card">
            <div className="skeleton" style={{ width: 72, height: 72, borderRadius: "50%" }} />
            <div style={{ flex: 1 }}>
              <div className="skeleton skeleton-row short" />
              <div className="skeleton skeleton-row medium" />
            </div>
          </div>
        ))}
      </div>
      <div className="skeleton skeleton-block" />
      <div className="skeleton skeleton-block" />
    </>
  );
}

function BrainResults({ openSections, toggle }) {
  return (
    <>
      {/* Score cards */}
      <div className="score-grid">
        <ScoreCard label="Hook Quality" value="8.4" sub="/ 10" arc={84} />
        <ScoreCard label="Structure" value="7.9" sub="/ 10" arc={79} />
        <ScoreCard label="Emotional Triggers" value="5" sub="identified" arc={null} />
      </div>

      <AnalysisSection
        num="01"
        title="Why It Works"
        open={openSections[0]}
        onToggle={() => toggle(0)}
      >
        <p>
          The opening is doing three jobs in eleven seconds. First, it asserts authority — "the first second I saw the demo, I knew" — collapsing the speaker's expertise into a snap judgment the viewer can borrow. Second, it makes a <strong>concrete promise</strong> ("watch what happens at 0:23") which is a payoff timer the brain can't easily abandon. Third, it positions Apple as the protagonist of a story about <em>doing the hard thing</em>, which invites the viewer to evaluate the rest of the video as a verdict, not a description.
        </p>
        <p>
          This format works because it converts a passive watch ("a video about the Vision Pro") into an active one ("can the speaker prove it?"). Active watching is the single biggest lever on 30-second retention.
        </p>
      </AnalysisSection>

      <AnalysisSection
        num="02"
        title="Hook Breakdown"
        open={openSections[1]}
        onToggle={() => toggle(1)}
      >
        <p>The first 30 seconds run a tight 4-beat structure:</p>
        <ul>
          <li><strong>Beat 1 (0:00–0:03):</strong> Authority claim, no setup.</li>
          <li><strong>Beat 2 (0:03–0:08):</strong> Specificity hook — a precise timestamp ("0:23") creates a forward-looking promise.</li>
          <li><strong>Beat 3 (0:08–0:18):</strong> A single contrast statement framing Apple as the only company that would try this.</li>
          <li><strong>Beat 4 (0:18–0:30):</strong> Visual cut to the referenced moment — payoff is delivered <em>before</em> the body of the video, banking trust.</li>
        </ul>
      </AnalysisSection>

      <AnalysisSection
        num="03"
        title="Structure Map"
        open={openSections[2]}
        onToggle={() => toggle(2)}
      >
        {[
          { t: "00:00", label: "Pattern interrupt", desc: "Authority claim + precise timestamp promise" },
          { t: "00:30", label: "Stakes frame", desc: "Why this product matters / who else couldn't do it" },
          { t: "02:15", label: "Demonstration", desc: "First evidence reel — visual proof of the claim" },
          { t: "05:40", label: "Counter-objection", desc: "Acknowledges skepticism, then refutes it with specifics" },
          { t: "08:50", label: "Social proof", desc: "Cuts to a known second voice agreeing — borrowed credibility" },
          { t: "11:30", label: "CTA loop", desc: "Subscribes the viewer back into the channel's recurring frame" },
        ].map((s, i) => (
          <div key={i} className="structure-step">
            <div className="structure-step-num">{String(i + 1).padStart(2, "0")}</div>
            <div style={{ flex: 1 }}>
              <p className="structure-step-label">{s.label}</p>
              <p className="structure-step-desc">{s.desc}</p>
            </div>
            <div className="structure-step-timer">{s.t}</div>
          </div>
        ))}
      </AnalysisSection>

      <AnalysisSection
        num="04"
        title="Emotional Triggers"
        open={openSections[3]}
        onToggle={() => toggle(3)}
      >
        <p>Five triggers identified, ordered by load-bearing:</p>
        <div className="trigger-chips">
          <span className="trigger-chip">Curiosity Gap</span>
          <span className="trigger-chip">Aspiration</span>
          <span className="trigger-chip">Fear of Missing Out</span>
          <span className="trigger-chip">Authority Borrowing</span>
          <span className="trigger-chip">Tribal Identity</span>
        </div>
      </AnalysisSection>

      <AnalysisSection
        num="05"
        title="Techniques to Steal"
        open={openSections[4]}
        onToggle={() => toggle(4)}
      >
        <ul>
          <li><strong>Lead with a timestamp promise.</strong> Replace "in this video I'll show you" with "watch what happens at 0:23".</li>
          <li><strong>Burn your authority claim in the first 3 seconds.</strong> Don't introduce yourself — assume it.</li>
          <li><strong>Pre-pay the hook.</strong> Show the referenced moment <em>before</em> the body, not after.</li>
          <li><strong>Use a single, identifiable antagonist.</strong> Here it's "every other company". Make it concrete.</li>
          <li><strong>Park your CTA at ~55% retention</strong>, not the outro. Match the audience peak.</li>
        </ul>
      </AnalysisSection>

      <AnalysisSection
        num="06"
        title="Replication Template"
        open={openSections[5]}
        onToggle={() => toggle(5)}
      >
        <pre><code>{`HOOK (0–11s)
  authority_claim: "[The first time I saw X, I knew…]"
  payoff_promise: "[Watch what happens at MM:SS]"
  antagonist: "[a company / category most wouldn't try]"

STAKES (11–30s)
  why_this_matters: "[1 sentence]"
  who_else_failed: "[name them]"

DEMO (30s–3m)
  visual_proof_first
  narrate_after

CTA_LOOP at ~55% AVD
  "[Subscribe-back hook]"

OUTRO (~last 30s)
  next_video_promise`}</code></pre>
        <p style={{ marginTop: 12 }}>
          <a href="#">→ Send this template to /hooks</a>
        </p>
      </AnalysisSection>
    </>
  );
}

function ScoreCard({ label, value, sub, arc }) {
  const r = 32;
  const c = 2 * Math.PI * r;
  const offset = arc !== null ? c - (arc / 100) * c : c;
  return (
    <div className="score-card">
      <div className="score-arc">
        <svg viewBox="0 0 72 72">
          <circle cx="36" cy="36" r={r} className="score-arc-track" />
          {arc !== null && (
            <circle
              cx="36" cy="36" r={r}
              className="score-arc-fill"
              strokeDasharray={c}
              strokeDashoffset={offset}
            />
          )}
        </svg>
        <div className="score-arc-value">{arc !== null ? value : "5"}</div>
      </div>
      <div className="score-meta">
        <div className="score-label">{label}</div>
        <div className="score-value">{value}<span style={{ color: "var(--text-muted)", fontSize: 13, marginLeft: 4 }}>{sub}</span></div>
      </div>
    </div>
  );
}

function AnalysisSection({ num, title, open, onToggle, children }) {
  return (
    <div className={"analysis-section" + (open ? " open" : "")}>
      <button className="analysis-section-header" onClick={onToggle}>
        <span style={{ display: "flex", alignItems: "center" }}>
          <span className="analysis-section-num">{num}</span>
          {title}
        </span>
        <span className="analysis-section-chevron"><Icon.ChevronDown size={16} /></span>
      </button>
      {open && <div className="analysis-section-body md">{children}</div>}
    </div>
  );
}

window.BrainWorkspace = BrainWorkspace;
