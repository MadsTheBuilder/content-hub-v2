import { useState, useEffect } from 'react';
import Icon from '../Icons.jsx';
import VaultPicker from '../VaultPicker.jsx';
import OutputBrowser from '../OutputBrowser.jsx';
import { SourcesPanel, StackedPanel } from '../SourcesPanel.jsx';
import { runStage, ConflictError } from '../api.js';
import { announceStart, announceDone, announceFail } from '../jobActivity.js';
import useJobStream from '../hooks/useJobStream.js';

const PLATFORMS = ['yt-long', 'yt-short', 'podcast'];

export default function OutlineTab() {
  const [topic, setTopic] = useState('');
  const [hookPath, setHookPath] = useState(null);
  const [length, setLength] = useState(8);
  const [platform, setPlatform] = useState('yt-long');
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

  const handleRun = async () => {
    if (!topic.trim()) return;
    setRunState('loading');
    setJobError(null);
    setJobResult(null);
    setConflictNotice(false);
    announceStart('distribution');
    try {
      const body = { topic: topic.trim(), hook_path: hookPath || '', length, platform };
      const { job_id } = await runStage('outline', body);
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
        <div>
          <label className="field-label" htmlFor="outline-topic">Video topic</label>
          <div className="prompt-area">
            <textarea
              id="outline-topic"
              className="prompt-textarea"
              placeholder="e.g. Why open-source design tools are suddenly worth watching"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              rows={3}
            />
            <span className="char-count">{topic.length}</span>
          </div>
        </div>

        <div>
          <label className="field-label">Hook file (optional)</label>
          <VaultPicker
            folder="05-Hooks"
            value={hookPath}
            onChange={setHookPath}
            placeholder="Select hook file…"
          />
        </div>

        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ flex: 1 }}>
            <label className="field-label" htmlFor="outline-length">Sections</label>
            <input
              id="outline-length"
              type="number"
              className="url-input"
              min={4}
              max={16}
              value={length}
              onChange={(e) => setLength(Number(e.target.value))}
              style={{ width: '100%' }}
            />
          </div>
          <div style={{ flex: 2 }}>
            <label className="field-label" htmlFor="outline-platform">Platform</label>
            <select
              id="outline-platform"
              className="vault-picker"
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
            >
              {PLATFORMS.map((p) => <option key={p} value={p}>{p}</option>)}
            </select>
          </div>
        </div>

        {conflictNotice && (
          <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>A job is already running — wait for it to finish.</p>
        )}
        {jobError && (
          <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>Error: {jobError}</p>
        )}

        <button
          className={'run-btn' + (runState === 'loading' ? ' loading' : runState === 'done' ? ' done' : '')}
          onClick={handleRun}
          disabled={runState === 'loading' || !topic.trim()}
        >
          {runState === 'loading' ? (
            <><span className="spinner-icon" style={{ display: 'grid', placeItems: 'center', animation: 'spin 0.8s linear infinite' }}><Icon.Loader size={14} /></span>Running…</>
          ) : runState === 'done' ? (
            <><Icon.Check size={14} />Done — View Results</>
          ) : (
            <><Icon.Play size={13} />Run Outline</>
          )}
        </button>
      </section>

      <StackedPanel
        back={<SourcesPanel stageId="outline" />}
        front={<section className="output-zone">
        {runState === 'idle' && !jobResult && (
          <div className="output-empty">
            <div className="output-empty-icon"><Icon.ListTree size={26} /></div>
            <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>Run Outline to see results here</div>
          </div>
        )}
        {runState === 'loading' && (
          <>
            <div className="output-meta"><span>Running Outline… · streaming</span></div>
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
              <span>Saved to vault · 06-Outlines</span>
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
