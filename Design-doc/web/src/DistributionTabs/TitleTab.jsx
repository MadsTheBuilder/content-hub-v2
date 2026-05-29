import { useState, useEffect } from 'react';
import Icon from '../Icons.jsx';
import OutputBrowser from '../OutputBrowser.jsx';
import { runStage, ConflictError } from '../api.js';
import { announceStart, announceDone, announceFail } from '../jobActivity.js';
import useJobStream from '../hooks/useJobStream.js';

export default function TitleTab() {
  const [concept, setConcept] = useState('');
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
    if (!concept.trim()) return;
    setRunState('loading');
    setJobError(null);
    setJobResult(null);
    setConflictNotice(false);
    announceStart('distribution');
    try {
      const { job_id } = await runStage('title', { concept: concept.trim() });
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
          <label className="field-label" htmlFor="title-concept">Video concept</label>
          <div className="prompt-area">
            <textarea
              id="title-concept"
              className="prompt-textarea"
              placeholder="e.g. Why open-source design tools are suddenly worth watching"
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              rows={4}
            />
            <span className="char-count">{concept.length}</span>
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
          disabled={runState === 'loading' || !concept.trim()}
        >
          {runState === 'loading' ? (
            <><span className="spinner-icon" style={{ display: 'grid', placeItems: 'center', animation: 'spin 0.8s linear infinite' }}><Icon.Loader size={14} /></span>Running…</>
          ) : runState === 'done' ? (
            <><Icon.Check size={14} />Done — View Results</>
          ) : (
            <><Icon.Play size={13} />Run Title</>
          )}
        </button>
      </section>

      <section className="output-zone">
        {runState === 'idle' && !jobResult && (
          <div className="output-empty">
            <div className="output-empty-icon"><Icon.Type size={26} /></div>
            <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>Run Title to see results here</div>
          </div>
        )}
        {runState === 'loading' && (
          <>
            <div className="output-meta"><span>Running Title… · streaming</span></div>
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
              <span>Saved to vault · 07-Titles</span>
              <div className="output-meta-actions">
                <button className="btn-icon" title="Copy path" onClick={() => navigator.clipboard.writeText(jobResult.primary_path || '')}>
                  <Icon.Copy size={14} />
                </button>
              </div>
            </div>
            <OutputBrowser result={jobResult} />
          </>
        )}
      </section>
    </div>
  );
}
