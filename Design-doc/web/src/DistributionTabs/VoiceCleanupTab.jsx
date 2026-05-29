import { useState, useEffect } from 'react';
import Icon from '../Icons.jsx';
import VaultPicker from '../VaultPicker.jsx';
import OutputBrowser from '../OutputBrowser.jsx';
import { runStage, ConflictError } from '../api.js';
import { announceStart, announceDone, announceFail } from '../jobActivity.js';
import useJobStream from '../hooks/useJobStream.js';

// Voice-cleanup can pick from any of these output folders
const VOICE_FOLDERS = [
  { label: 'Ideas (02)', value: '02-Ideas' },
  { label: 'Hooks (05)', value: '05-Hooks' },
  { label: 'Outlines (06)', value: '06-Outlines' },
  { label: 'Titles (07)', value: '07-Titles' },
  { label: 'Distribution (08)', value: '08-Distribution' },
  { label: 'Shorts (09)', value: '09-Shorts' },
  { label: 'Research (10)', value: '10-Research' },
];

export default function VoiceCleanupTab() {
  const [sourceFolder, setSourceFolder] = useState('06-Outlines');
  const [filePath, setFilePath] = useState(null);
  const [inplace, setInplace] = useState(false);
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

  const handleFolderChange = (folder) => {
    setSourceFolder(folder);
    setFilePath(null);
  };

  const handleRun = async () => {
    if (!filePath) return;
    setRunState('loading');
    setJobError(null);
    setJobResult(null);
    setConflictNotice(false);
    announceStart('distribution');
    try {
      const { job_id } = await runStage('voice-cleanup', { file_path: filePath, inplace });
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
          <label className="field-label" htmlFor="vc-folder">Source folder</label>
          <select
            id="vc-folder"
            className="vault-picker"
            value={sourceFolder}
            onChange={(e) => handleFolderChange(e.target.value)}
          >
            {VOICE_FOLDERS.map((f) => (
              <option key={f.value} value={f.value}>{f.label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="field-label">File to clean</label>
          <VaultPicker
            folder={sourceFolder}
            value={filePath}
            onChange={setFilePath}
            placeholder="Select file…"
          />
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <input
            id="vc-inplace"
            type="checkbox"
            checked={inplace}
            onChange={(e) => setInplace(e.target.checked)}
          />
          <label htmlFor="vc-inplace" className="field-label" style={{ margin: 0, cursor: 'pointer' }}>
            In-place (overwrite original)
          </label>
        </div>

        {filePath && (
          <div style={{ fontSize: 12, color: 'var(--text-muted)', wordBreak: 'break-all' }}>
            {inplace ? 'Will overwrite:' : 'Will write to:'} <br />
            <span style={{ color: 'var(--text-secondary)' }}>
              {inplace ? filePath : filePath.replace(/\.md$/, '_cleaned.md')}
            </span>
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
          disabled={runState === 'loading' || !filePath}
        >
          {runState === 'loading' ? (
            <><span className="spinner-icon" style={{ display: 'grid', placeItems: 'center', animation: 'spin 0.8s linear infinite' }}><Icon.Loader size={14} /></span>Running…</>
          ) : runState === 'done' ? (
            <><Icon.Check size={14} />Done — View Results</>
          ) : (
            <><Icon.Play size={13} />Run Voice Cleanup</>
          )}
        </button>
      </section>

      <section className="output-zone">
        {runState === 'idle' && !jobResult && (
          <div className="output-empty">
            <div className="output-empty-icon"><Icon.Zap size={26} /></div>
            <div style={{ fontSize: 14, color: 'var(--text-secondary)' }}>Run Voice Cleanup to see results here</div>
          </div>
        )}
        {runState === 'loading' && (
          <>
            <div className="output-meta"><span>Running Voice Cleanup… · streaming</span></div>
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
              <span>Cleaned · {inplace ? 'original overwritten' : '_cleaned sibling'}</span>
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
