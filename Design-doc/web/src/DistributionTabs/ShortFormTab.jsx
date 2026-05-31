import { useState, useEffect } from 'react';
import Icon from '../Icons.jsx';
import VaultPicker from '../VaultPicker.jsx';
import OutputBrowser from '../OutputBrowser.jsx';
import { SourcesPanel, StackedPanel } from '../SourcesPanel.jsx';
import { runStage, ConflictError } from '../api.js';
import { announceStart, announceDone, announceFail } from '../jobActivity.js';
import useJobStream from '../hooks/useJobStream.js';

export default function ShortFormTab() {
  const [mode, setMode] = useState('vault'); // 'vault' | 'url'
  const [researchFile, setResearchFile] = useState(null);
  const [outlineFile, setOutlineFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [jobId, setJobId] = useState(null);
  const [runState, setRunState] = useState('idle');
  const [jobResult, setJobResult] = useState(null);
  const [jobError, setJobError] = useState(null);
  const [conflictNotice, setConflictNotice] = useState(false);

  const jobStream = useJobStream(jobId);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (jobStream.status === 'completed') {
      setRunState('done');
      setJobResult(jobStream.result);
      announceDone('distribution');
    } else if (jobStream.status === 'failed') {
      setRunState('idle');
      setJobError(jobStream.error);
      announceFail('distribution');
    }
  }, [jobStream.status, jobStream.result, jobStream.error]);
  /* eslint-enable react-hooks/set-state-in-effect */

  const canRun = mode === 'vault'
    ? (researchFile && outlineFile)
    : youtubeUrl.trim().length > 0;

  const handleRun = async () => {
    if (!canRun) return;
    setRunState('loading');
    setJobError(null);
    setJobResult(null);
    setConflictNotice(false);
    announceStart('distribution');
    try {
      const body = mode === 'vault'
        ? { research_file: researchFile, outline_file: outlineFile }
        : { youtube_url: youtubeUrl.trim() };
      const { job_id } = await runStage('short-form', body);
      setJobId(job_id);
    } catch (e) {
      if (e instanceof ConflictError) {
        setConflictNotice(true);
        announceFail('distribution');
      } else {
        setJobError(e.message);
        announceFail('distribution');
      }
      setRunState('idle');
    }
  };

  return (
    <div className="stage-split">
      <section className="input-zone">
        <div className="mode-toggle-row">
          <span className="mode-toggle-row-label">Input mode</span>
          <div className="mode-toggle" data-mode={mode}>
            <span className="mode-toggle-slider" />
            <button
              type="button"
              className={'mode-toggle-option' + (mode === 'vault' ? ' is-active' : '')}
              onClick={() => setMode('vault')}
            >
              <Icon.FileText size={12} />
              Vault files
            </button>
            <button
              type="button"
              className={'mode-toggle-option' + (mode === 'url' ? ' is-active' : '')}
              onClick={() => setMode('url')}
            >
              <Icon.Link size={12} />
              YouTube URL
            </button>
          </div>
        </div>

        {mode === 'vault' ? (
          <>
            <div>
              <label className="field-label">Research file</label>
              <VaultPicker folder="10-Research" value={researchFile} onChange={setResearchFile} placeholder="Select research file…" />
            </div>
            <div>
              <label className="field-label">Outline file</label>
              <VaultPicker folder="06-Outlines" value={outlineFile} onChange={setOutlineFile} placeholder="Select outline file…" />
            </div>
          </>
        ) : (
          <div>
            <label className="field-label" htmlFor="shortform-url">YouTube URL</label>
            <div className="url-input-row">
              <Icon.Link size={14} color="var(--text-muted)" />
              <input
                id="shortform-url"
                type="text"
                className="url-input"
                placeholder="https://youtube.com/watch?v=…"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
              />
            </div>
          </div>
        )}

        {conflictNotice && (
          <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>A job is already running — wait for it to finish.</p>
        )}
        {jobError && (
          <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Error: {jobError}</p>
        )}

        <button
          className={'run-btn' + (runState === 'loading' ? ' loading' : runState === 'done' ? ' done' : '')}
          onClick={handleRun}
          disabled={runState === 'loading' || !canRun}
        >
          {runState === 'loading' ? (
            <><span className="spinner-icon" style={{ display: 'grid', placeItems: 'center', animation: 'spin 0.8s linear infinite' }}><Icon.Loader size={14} /></span>Running…</>
          ) : runState === 'done' ? (
            <><Icon.Check size={14} />Done — View Results</>
          ) : (
            <><Icon.Play size={13} />Run Short-form</>
          )}
        </button>
      </section>

      <StackedPanel
        back={<SourcesPanel stageId="short-form" />}
        front={<section className="output-zone">
        {runState === 'idle' && !jobResult && (
          <div className="output-empty">
            <div className="output-empty-icon"><Icon.Rocket size={26} /></div>
            <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>Run Short-form to see results here</div>
          </div>
        )}
        {runState === 'loading' && (
          <>
            <div className="output-meta"><span>Running Short-form… · streaming</span></div>
            <div className="output-body">
              {jobStream.lines.length > 0 ? (
                <div style={{ fontFamily: 'monospace', fontSize: 12, lineHeight: 1.6 }}>
                  {jobStream.lines.map((line, i) => <div key={i}>{line}</div>)}
                </div>
              ) : (
                <>
                  <div className="skeleton skeleton-row long" />
                  <div className="skeleton skeleton-row medium" />
                  <div className="skeleton skeleton-block" />
                </>
              )}
            </div>
          </>
        )}
        {runState === 'done' && jobResult && (
          <>
            <div className="output-meta">
              <span>Saved to vault · 09-Shorts</span>
              <div className="output-meta-actions">
                <button className="btn-icon" title="Copy path" onClick={() => navigator.clipboard.writeText(jobResult.primary_path || '')}>
                  <Icon.Copy size={14} />
                </button>
              </div>
            </div>
            <OutputBrowser result={jobResult} />
          </>
        )}
      </section>}
      />
    </div>
  );
}
