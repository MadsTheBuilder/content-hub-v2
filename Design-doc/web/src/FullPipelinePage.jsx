import { useState, useEffect } from 'react';
import useJobStream from './hooks/useJobStream.js';
import { runStage, readVaultFile, ConflictError, getJobStatus } from './api.js';
import { announceStart, announceDone, announceFail } from './jobActivity.js';
import MarkdownViewer from './MarkdownViewer.jsx';
import OutputBrowser from './OutputBrowser.jsx';
import VaultPicker from './VaultPicker.jsx';
import Icon from './Icons.jsx';

const STORAGE_KEY = "fp_pipeline_v1";
const JOB_KEY = STORAGE_KEY + "_job";
function readSaved() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "null") || {}; }
  catch { return {}; }
}

// Ordered chain. `key` is the runStage() endpoint key (see api.js STAGE_ENDPOINTS).
const STEPS = [
  { id: "trends",    key: "trends",     label: "Trends",     color: "var(--stage-trends)",       gate: "pick" },
  { id: "research",  key: "research",   label: "Research",   color: "var(--stage-research)",     gate: "approve" },
  { id: "ideation",  key: "ideation",   label: "Ideation",   color: "var(--stage-ideation)",     gate: "pick" },
  { id: "hook",      key: "hooks",      label: "Hook",       color: "var(--stage-hooks)",        gate: "approve" },
  { id: "outline",   key: "outline",    label: "Outline",    color: "var(--stage-distribution)", gate: "approve" },
  { id: "title",     key: "title",      label: "Title",      color: "var(--stage-distribution)", gate: "pick" },
  { id: "cascade",   key: "cascade",    label: "Cascade",    color: "var(--stage-distribution)", gate: "approve" },
  { id: "shortform", key: "short-form", label: "Short-form", color: "var(--stage-distribution)", gate: "terminal" },
];

const idx = (id) => STEPS.findIndex((s) => s.id === id);

// Whether the active step already has the output/gate it needs to render its
// selection UI. Trends is always ready (its gate is the vault picker itself).
function gateReady(stepId, picks, results) {
  switch (stepId) {
    case "trends": return true;
    case "research": return true; // config form is the gate; ApproveGate shows once a brief exists
    case "ideation": return !!results.ideaSrc;
    case "hook": return !!picks.hooksPath;
    case "outline": return !!picks.outlinePath;
    case "title": return !!results.titleSrc;
    case "cascade": return !!results.cascade;
    default: return false;
  }
}

// --- parsing: only the field the next stage consumes (advisor: minimal surface) ---
function parseIdeas(md) {
  const out = [];
  const re = /^#{2,3}\s+Rank\s+\d+\s*[—–-]\s*(.+?)\s*$/gm;
  let m;
  while ((m = re.exec(md))) out.push(m[1].trim());
  return out;
}
function parseTitles(md) {
  const body = md.split(/^###\s+Thumbnail/m)[0];
  const out = [];
  const re = /^[-*]\s*\*\*(.+?)\*\*/gm;
  let m;
  while ((m = re.exec(body))) {
    const t = m[1].trim();
    if (!/^Tier-\d/i.test(t) && !t.endsWith(":")) out.push(t);
  }
  return [...new Set(out)];
}

export default function FullPipelinePage({ onBack }) {
  const [seed, setSeed] = useState(() => readSaved().seed ?? "");
  const [activeId, setActiveId] = useState(() => readSaved().activeId ?? "trends");
  const [phase, setPhase] = useState(() => readSaved().phase ?? "idle");
  const [runningStage, setRunningStage] = useState(null); // step id of in-flight job
  const [stageError, setStageError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [picks, setPicks] = useState(() => readSaved().picks ?? {
    trendPath: null, briefPath: null, ideaTitle: null,
    hooksPath: null, outlinePath: null, titleString: null,
  });
  const [results, setResults] = useState(() => readSaved().results ?? { ideaSrc: null, titleSrc: null, cascade: null, short: null });
  const [research, setResearch] = useState(() => readSaved().research ?? {
    niche: "", mode: "deep", targetLength: "", tone: "", audience: "", banned: "",
  });

  const [jobId, setJobId] = useState(null);
  const jobStream = useJobStream(jobId);

  // --- persist recoverable state to localStorage ---
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ seed, activeId, phase, picks, results, research }));
    } catch {} // eslint-disable-line no-empty
  }, [seed, activeId, phase, picks, results, research]);

  const resetPipeline = () => {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(JOB_KEY);
    setSeed("");
    setActiveId("trends");
    setPhase("idle");
    setRunningStage(null);
    setStageError(null);
    setRefreshKey(0);
    setPicks({ trendPath: null, briefPath: null, ideaTitle: null, hooksPath: null, outlinePath: null, titleString: null });
    setResults({ ideaSrc: null, titleSrc: null, cascade: null, short: null });
    setResearch({ niche: "", mode: "deep", targetLength: "", tone: "", audience: "", banned: "" });
  };

  function handleCompletion(stageId, res, path) {
    announceDone(STEPS[idx(stageId)].key);
    try { localStorage.removeItem(JOB_KEY); } catch {} // eslint-disable-line no-empty
    if (stageId === "trends") { setRefreshKey((k) => k + 1); setPhase("idle"); }
    else if (stageId === "research") { setPicks((p) => ({ ...p, briefPath: path })); setPhase("review"); }
    else if (stageId === "ideation") { setResults((r) => ({ ...r, ideaSrc: path })); setPhase("review"); }
    else if (stageId === "hook") { setPicks((p) => ({ ...p, hooksPath: path })); setPhase("review"); }
    else if (stageId === "outline") { setPicks((p) => ({ ...p, outlinePath: path })); setPhase("review"); }
    else if (stageId === "title") { setResults((r) => ({ ...r, titleSrc: path })); setPhase("review"); }
    else if (stageId === "cascade") { setResults((r) => ({ ...r, cascade: res })); setPhase("review"); }
    else if (stageId === "shortform") { setResults((r) => ({ ...r, short: res })); setPhase("done"); }
    setRunningStage(null);
  }

  // --- recover in-flight job after page refresh (polls GET /api/jobs/{id} instead of
  //     reconnecting SSE — avoids zombie generator stealing the done event from the queue) ---
  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    const savedPhase = readSaved().phase;
    if (savedPhase !== "running") return;
    const savedJobId = (() => { try { return localStorage.getItem(JOB_KEY); } catch { return null; } })();
    if (!savedJobId) { setPhase("review"); return; }
    const savedActiveId = readSaved().activeId || "trends";
    const intervalRef = { current: null };
    const checkJob = () => {
      getJobStatus(savedJobId)
        .then((job) => {
          if (job.status === "completed") {
            clearInterval(intervalRef.current);
            handleCompletion(savedActiveId, job.result || {}, (job.result || {}).primary_path || "");
          } else if (job.status !== "running") {
            clearInterval(intervalRef.current);
            try { localStorage.removeItem(JOB_KEY); } catch {} // eslint-disable-line no-empty
            setStageError(job.error || "Stage failed during previous session");
            setPhase("review");
          }
          // "running" → keep polling
        })
        .catch(() => {
          clearInterval(intervalRef.current);
          try { localStorage.removeItem(JOB_KEY); } catch {} // eslint-disable-line no-empty
          setStageError("Server was restarted — previous run was lost. Retry to run again.");
          setPhase("review");
        });
    };
    checkJob();
    intervalRef.current = setInterval(checkJob, 3000);
    return () => clearInterval(intervalRef.current);
  }, []);
  /* eslint-enable react-hooks/set-state-in-effect */

  // --- launch a stage; selecting IS the trigger for the next stage ---
  async function launch(step, body) {
    setStageError(null);
    try {
      announceStart(step.key);
      const { job_id } = await runStage(step.key, body);
      setRunningStage(step.id);
      setActiveId(step.id);
      setPhase("running");
      setJobId(job_id);
      try { localStorage.setItem(JOB_KEY, job_id); } catch {} // eslint-disable-line no-empty
    } catch (e) {
      announceFail(step.key);
      setStageError(
        e instanceof ConflictError
          ? "Another job is already running — wait for it to finish, then retry."
          : e.message
      );
      setPhase(step.id === "trends" ? "idle" : "review");
    }
  }

  // --- driver: react to the in-flight job finishing ---
  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!runningStage) return;
    if (jobStream.status === "completed") {
      const res = jobStream.result || {};
      handleCompletion(runningStage, res, res.primary_path || "");
    } else if (jobStream.status === "failed") {
      announceFail(STEPS[idx(runningStage)].key);
      try { localStorage.removeItem(JOB_KEY); } catch {} // eslint-disable-line no-empty
      setStageError(jobStream.error || "Stage failed");
      setRunningStage(null);
      setPhase("review");
    }
  }, [jobStream.status]);
  /* eslint-enable react-hooks/set-state-in-effect */

  // --- gate actions (each advances + auto-runs the next stage) ---
  // Picking a trend no longer auto-runs research — it opens the Research config gate.
  const pickTrend = (path) => {
    setPicks((p) => ({ ...p, trendPath: path }));
    setResearch((r) => ({ ...r, niche: r.niche || seed }));
    setStageError(null);
    setActiveId("research");
    setPhase("review");
  };
  const runResearch = () =>
    launch(STEPS[idx("research")], {
      niche: research.niche.trim(),
      repos: [],
      mode: research.mode,
      trend_repo: picks.trendPath,
      target_length: research.targetLength ? Number(research.targetLength) : null,
      tone: research.tone.trim(),
      audience: research.audience.trim(),
      banned_phrases: research.banned.split(",").map((s) => s.trim()).filter(Boolean),
    });
  const refreshTrends = () => launch(STEPS[idx("trends")], { space: seed });
  const approveResearch = () =>
    launch(STEPS[idx("ideation")], { topic: research.niche.trim() || seed.trim(), research_file: picks.briefPath, no_trends: false });
  const pickIdea = (title) => {
    setPicks((p) => ({ ...p, ideaTitle: title }));
    launch(STEPS[idx("hook")], {
      topic: title, platform: "yt-long", audience: "", format: "medium",
      research_file: picks.briefPath, no_polish: false,
    });
  };
  const approveHooks = () =>
    launch(STEPS[idx("outline")], {
      topic: picks.ideaTitle, hook_path: picks.hooksPath,
      length: 8, platform: "yt-long", no_polish: false,
    });
  const approveOutline = () =>
    launch(STEPS[idx("title")], { concept: picks.ideaTitle, outline_file: picks.outlinePath });
  const pickTitle = (str) => {
    setPicks((p) => ({ ...p, titleString: str }));
    launch(STEPS[idx("cascade")], {
      research_file: picks.briefPath, outline_file: picks.outlinePath, title: str, youtube_url: "",
    });
  };
  const approveCascade = () =>
    launch(STEPS[idx("shortform")], {
      research_file: picks.briefPath, outline_file: picks.outlinePath,
      title: picks.titleString, youtube_url: "",
    });

  // retry the stage that just failed (re-issue with the same threaded inputs)
  const retry = () => {
    const map = {
      research: runResearch,
      ideation: approveResearch,
      hook: () => pickIdea(picks.ideaTitle),
      outline: approveHooks,
      title: approveOutline,
      cascade: () => pickTitle(picks.titleString),
      shortform: approveCascade,
      trends: refreshTrends,
    };
    (map[activeId] || (() => {}))();
  };

  const activeIndex = idx(activeId);
  const seedReady = seed.trim().length > 0;

  return (
    <div data-screen-label="Full Pipeline">
      <header className="page-header">
        <div>
          <h1 className="page-title">Full Pipeline</h1>
          <p className="page-subtitle">
            Run the whole chain end-to-end — trends → research → ideation → hook → outline → title → cascade → short-form.
            Review each step, select, and the next one runs automatically.
          </p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          {(activeIndex > 0 || phase !== "idle") && (
            <button className="btn btn-ghost" onClick={resetPipeline}>Start Over</button>
          )}
          {onBack && <button className="btn btn-ghost" onClick={onBack}>← Dashboard</button>}
        </div>
      </header>

      <div className="fp-seed">
        <label className="fp-seed-label">Niche / space</label>
        <input
          className="fp-seed-input"
          placeholder="e.g. local-first AI tooling for indie devs"
          value={seed}
          onChange={(e) => setSeed(e.target.value)}
          disabled={activeIndex > 0 || phase === "running"}
        />
      </div>

      <div className="fp-stepper">
        {STEPS.map((step, i) => {
          const state =
            i < activeIndex ? "done" :
            i === activeIndex ? (phase === "done" ? "done" : "active") :
            "locked";
          const isRunning = runningStage === step.id || (i === activeIndex && phase === "running");
          return (
            <div
              key={step.id}
              className={`fp-step is-${state}` + (isRunning ? " is-running" : "")}
              style={{ "--stage-color": step.color }}
            >
              <div className="fp-step-head">
                <span className="fp-step-dot">{i + 1}</span>
                <span className="fp-step-label">{step.label}</span>
                <span className="fp-step-status">
                  {isRunning ? "Running…" : state === "done" ? "✓ done" : state === "locked" ? "" : "Ready"}
                </span>
              </div>

              {state === "active" && (
                <div className="fp-step-body">
                  {isRunning ? (
                    <pre className="fp-log">
                      {runningStage === null
                        ? "Reconnecting to server job…"
                        : jobStream.lines.length ? jobStream.lines.join("\n") : "Starting…"
                      }
                    </pre>
                  ) : (
                    <>
                      {stageError && <div className="fp-error-msg">{stageError}</div>}
                      {gateReady(step.id, picks, results) ? (
                        <StepGate
                          step={step}
                          seedReady={seedReady}
                          refreshKey={refreshKey}
                          picks={picks}
                          results={results}
                          research={research}
                          setResearch={setResearch}
                          onPickTrend={pickTrend}
                          onRefresh={refreshTrends}
                          onRunResearch={runResearch}
                          onApproveResearch={approveResearch}
                          onPickIdea={pickIdea}
                          onApproveHooks={approveHooks}
                          onApproveOutline={approveOutline}
                          onPickTitle={pickTitle}
                          onApproveCascade={approveCascade}
                        />
                      ) : (
                        <button className="btn btn-stage" style={{ "--stage-color": step.color }} onClick={retry}>
                          Retry {step.label}
                        </button>
                      )}
                    </>
                  )}
                </div>
              )}

              {state === "done" && step.id !== "shortform" && (
                <div className="fp-step-summary">{summaryFor(step.id, picks)}</div>
              )}
              {state === "done" && step.id === "shortform" && (
                <div className="fp-step-body">
                  <div className="fp-done-banner">🎉 Pipeline complete. Both distribution bundles are below.</div>
                  <OutputBrowser result={results.short} />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function summaryFor(id, picks) {
  switch (id) {
    case "trends": return `Trend: ${shortPath(picks.trendPath)}`;
    case "research": return `Brief: ${shortPath(picks.briefPath)}`;
    case "ideation": return `Idea: ${picks.ideaTitle || "—"}`;
    case "hook": return `Hooks: ${shortPath(picks.hooksPath)}`;
    case "outline": return `Outline: ${shortPath(picks.outlinePath)}`;
    case "title": return `Title: ${picks.titleString || "—"}`;
    case "cascade": return "Distribution bundle generated";
    default: return "";
  }
}
const shortPath = (p) => (p ? p.split(/[\\/]/).pop() : "—");

// --- per-stage gate UI ---
function StepGate(props) {
  const {
    step, seedReady, refreshKey, picks, results, research, setResearch,
    onPickTrend, onRefresh, onRunResearch, onApproveResearch, onPickIdea,
    onApproveHooks, onApproveOutline, onPickTitle, onApproveCascade,
  } = props;

  if (step.id === "trends") {
    return (
      <div className="fp-gate">
        {!seedReady && <div className="fp-hint">Enter a niche above to begin.</div>}
        <div className="fp-trend-row">
          <VaultPicker
            key={refreshKey}
            folder="04-Trends"
            subfoldersOnly
            value={picks.trendPath}
            onChange={(p) => p && onPickTrend(p)}
            placeholder="Pick a trending repo…"
          />
          <button className="btn btn-ghost" onClick={onRefresh} disabled={!seedReady} title="Run a fresh GitHub trend scan (slow)">
            <Icon.TrendingUp size={15} /> Refresh
          </button>
        </div>
        <div className="fp-hint">Selecting a trend opens Research options.</div>
      </div>
    );
  }

  if (step.id === "research") {
    if (picks.briefPath) {
      return (
        <ApproveGate path={picks.briefPath} label="Use this research → run Ideation" color={step.color} onApprove={onApproveResearch} />
      );
    }
    return <ResearchConfig research={research} setResearch={setResearch} color={step.color} onRun={onRunResearch} />;
  }
  if (step.id === "ideation") {
    return <ListPicker path={results.ideaSrc} parse={parseIdeas} onPick={onPickIdea} kind="idea" color={step.color} />;
  }
  if (step.id === "hook") {
    return <ApproveGate path={picks.hooksPath} label="Use these hooks → run Outline" color={step.color} onApprove={onApproveHooks} />;
  }
  if (step.id === "outline") {
    return <ApproveGate path={picks.outlinePath} label="Use this outline → run Title" color={step.color} onApprove={onApproveOutline} />;
  }
  if (step.id === "title") {
    return <ListPicker path={results.titleSrc} parse={parseTitles} onPick={onPickTitle} kind="title" color={step.color} />;
  }
  if (step.id === "cascade") {
    return (
      <div className="fp-gate">
        <OutputBrowser result={results.cascade} />
        <button className="btn btn-stage btn-stage-filled" style={{ "--stage-color": step.color }} onClick={onApproveCascade}>
          Use this bundle → run Short-form
        </button>
      </div>
    );
  }
  return null;
}

function ResearchConfig({ research, setResearch, color, onRun }) {
  const set = (k) => (e) => setResearch((r) => ({ ...r, [k]: e.target.value }));
  const nicheReady = research.niche.trim().length > 0;
  return (
    <div className="fp-gate">
      <div className="fp-opt-grid">
        <label className="fp-opt">
          <span className="fp-opt-label">Niche / topic *</span>
          <input className="fp-seed-input" value={research.niche} onChange={set("niche")} placeholder="e.g. local-first AI tooling" />
        </label>
        <div className="fp-opt">
          <span className="fp-opt-label">Mode</span>
          <div className="fp-seg" style={{ "--stage-color": color }}>
            {["fast", "deep"].map((m) => (
              <button key={m} type="button" className={research.mode === m ? "is-on" : ""} onClick={() => setResearch((r) => ({ ...r, mode: m }))}>
                {m}
              </button>
            ))}
          </div>
        </div>
        <label className="fp-opt">
          <span className="fp-opt-label">Target length (min)</span>
          <input className="fp-seed-input" type="number" min="1" value={research.targetLength} onChange={set("targetLength")} placeholder="brief default" />
        </label>
      </div>

      <details className="fp-adv">
        <summary>Advanced (optional)</summary>
        <div className="fp-opt-grid">
          <label className="fp-opt">
            <span className="fp-opt-label">Tone</span>
            <input className="fp-seed-input" value={research.tone} onChange={set("tone")} placeholder="brief default" />
          </label>
          <label className="fp-opt">
            <span className="fp-opt-label">Audience</span>
            <input className="fp-seed-input" value={research.audience} onChange={set("audience")} placeholder="brief default" />
          </label>
        </div>
        <label className="fp-opt">
          <span className="fp-opt-label">Banned phrases (comma-separated)</span>
          <input className="fp-seed-input" value={research.banned} onChange={set("banned")} placeholder="extends brief.md list" />
        </label>
      </details>

      <button className="btn btn-stage btn-stage-filled" style={{ "--stage-color": color }} disabled={!nicheReady} onClick={onRun}>
        Run Research →
      </button>
      {!nicheReady && <div className="fp-hint">Enter a niche to run research.</div>}
    </div>
  );
}

function ApproveGate({ path, label, color, onApprove }) {
  return (
    <div className="fp-gate">
      <MarkdownViewer path={path} />
      <button className="btn btn-stage btn-stage-filled" style={{ "--stage-color": color }} onClick={onApprove}>
        {label}
      </button>
    </div>
  );
}

function ListPicker({ path, parse, onPick, kind, color }) {
  const [items, setItems] = useState(null);
  const [manual, setManual] = useState("");

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!path) return;
    setItems(null);
    readVaultFile(path)
      .then((d) => setItems(parse(d.content)))
      .catch(() => setItems([]));
  }, [path]);
  /* eslint-enable react-hooks/set-state-in-effect */

  if (items === null) return <div className="fp-hint">Loading options…</div>;

  // Mandatory manual fallback when parsing can't find a clean list.
  if (items.length < 2) {
    return (
      <div className="fp-gate">
        <MarkdownViewer path={path} />
        <div className="fp-hint">Couldn't auto-detect the {kind} list — paste the {kind} you want to continue with:</div>
        <div className="fp-trend-row">
          <input className="fp-seed-input" value={manual} onChange={(e) => setManual(e.target.value)} placeholder={`Type the ${kind}…`} />
          <button className="btn btn-stage btn-stage-filled" style={{ "--stage-color": color }} disabled={!manual.trim()} onClick={() => onPick(manual.trim())}>
            Continue
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="fp-gate">
      <div className="fp-pick-list">
        {items.map((t, i) => (
          <button key={i} className="fp-pick-card" style={{ "--stage-color": color }} onClick={() => onPick(t)}>
            <span className="fp-pick-num">{i + 1}</span>
            <span className="fp-pick-text">{t}</span>
          </button>
        ))}
      </div>
      <div className="fp-hint">Selecting a {kind} immediately runs the next stage.</div>
    </div>
  );
}
