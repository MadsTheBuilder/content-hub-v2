import { useState, useEffect } from 'react';
import Icon from './Icons';
import { runBrainAnalysis, ConflictError } from './api.js';
import { announceStart, announceDone, announceFail } from './jobActivity.js';
import useJobStream from './hooks/useJobStream.js';

function Brain() {
  const [prompt, setPrompt] = useState("");
  const [jobId, setJobId] = useState(null);
  const [conflictNotice, setConflictNotice] = useState(false);
  const { lines, status, result, error } = useJobStream(jobId);

  const running = status === "running";

  const handleAnalyze = async () => {
    if (!prompt.trim()) return;
    setConflictNotice(false);
    try {
      announceStart("brain");
      const { job_id } = await runBrainAnalysis(prompt);
      setJobId(job_id);
    } catch (e) {
      if (e instanceof ConflictError) {
        setConflictNotice(true);
        announceFail("brain");
      } else {
        announceFail("brain");
        throw e;
      }
    }
  };

  useEffect(() => {
    if (!jobId) return;
    if (status === "completed") announceDone("brain");
    if (status === "failed") announceFail("brain");
  }, [status, jobId]);

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
        <label className="field-label">Paste content to analyze</label>
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
        {conflictNotice && (
          <p style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 8 }}>
            A job is already running — wait for it to finish.
          </p>
        )}
        <div className="brain-toolbar">
          <button
            className="run-btn"
            style={{ background: "var(--brain)", color: "var(--bg-base)" }}
            onClick={handleAnalyze}
            disabled={running || !prompt.trim()}
          >
            {running ? (
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

      {!jobId && (
        <div className="output-empty" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)", borderRadius: "var(--r-card)", padding: 60 }}>
          <div className="output-empty-icon" style={{ color: "var(--brain)" }}>
            <Icon.Brain size={28} />
          </div>
          <div style={{ fontSize: 14, color: "var(--text-secondary)" }}>Paste content here to decode it</div>
          <div style={{ fontSize: 12, color: "var(--text-muted)", maxWidth: 320 }}>
            Transcripts, articles, threads, hooks. Paste it and we'll show you the machinery.
          </div>
        </div>
      )}

      {running && (
        <div className="output-stream">
          {lines.map((l, i) => <div key={i} className="stream-line">{l}</div>)}
        </div>
      )}

      {status === "failed" && error && (
        <div className="job-error" style={{ marginTop: 16, padding: 16, background: "var(--bg-surface)", border: "1px solid var(--border)", borderRadius: "var(--r-card)", color: "var(--text-muted)", fontSize: 13 }}>
          Analysis failed: {error}
        </div>
      )}

      {status === "completed" && result && <BrainResults result={result} />}
    </div>
  );
}

function BrainResults({ result }) {
  const { hook_quality, structure_score, emotional_triggers, techniques_to_steal, replication_template } = result;
  return (
    <div className="brain-stack" style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 12 }}>
      <ResultSection title="Hook Quality">
        <p>{hook_quality}</p>
      </ResultSection>

      <ResultSection title="Structure Score">
        <p>{structure_score}</p>
      </ResultSection>

      {emotional_triggers?.length > 0 && (
        <ResultSection title="Emotional Triggers">
          <div className="trigger-chips">
            {emotional_triggers.map((t, i) => (
              <span key={i} className="trigger-chip">{t}</span>
            ))}
          </div>
        </ResultSection>
      )}

      {techniques_to_steal?.length > 0 && (
        <ResultSection title="Techniques to Steal">
          <ul>
            {techniques_to_steal.map((t, i) => <li key={i}>{t}</li>)}
          </ul>
        </ResultSection>
      )}

      {replication_template && (
        <ResultSection title="Replication Template">
          <pre style={{ whiteSpace: "pre-wrap", fontSize: 12, color: "var(--text-secondary)" }}>
            <code>{replication_template}</code>
          </pre>
        </ResultSection>
      )}
    </div>
  );
}

function ResultSection({ title, children }) {
  return (
    <div className="analysis-section open">
      <div className="analysis-section-header" style={{ cursor: "default" }}>
        <span>{title}</span>
      </div>
      <div className="analysis-section-body md">{children}</div>
    </div>
  );
}

export default Brain;
