// SourcesPanel — the "behind page" with vault files, folders, and sources used.
// All wired stages load real vault data via api.js.

import { useState, useEffect } from 'react';
import MarkdownViewer from './MarkdownViewer.jsx';
import { getRecent } from './api.js';

// ---------------------------------------------------------------------------
// Wired stage folder mapping
// ---------------------------------------------------------------------------

const LIVE_FOLDERS = {
  trends: "04-Trends",
  research: "10-Research",
  ideation: "02-Ideas",
  hooks: "05-Hooks",
  outline: "06-Outlines",
  title: "07-Titles",
  cascade: "08-Distribution",
  "short-form": "09-Shorts",
  "voice-cleanup": "09-Shorts",
};

// ---------------------------------------------------------------------------
// Shared UI primitives
// ---------------------------------------------------------------------------

function TreeRow({ row, onClick }) {
  const folderIcon =
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6Z" />
    </svg>;

  const fileIcon =
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
      <path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>;

  const clickable = row.type === "file";
  return (
    <div
      className={"tree-row " + (row.type === "folder" ? "is-folder " : "") + (row.current ? "is-current " : "") + (clickable ? "is-clickable" : "")}
      onClick={clickable ? onClick : undefined}
      role={clickable ? "button" : undefined}
      tabIndex={clickable ? 0 : undefined}>
      {row.depth ? <span className="tree-indent" /> : null}
      <span className="tree-icon">{row.type === "folder" ? folderIcon : fileIcon}</span>
      <span className="tree-name">{row.name}</span>
      {row.type === "folder" && <span className="tree-meta">{row.count} items</span>}
      {row.type === "file" && <span className="tree-meta">{row.meta}</span>}
    </div>
  );
}

const backArrow =
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15 18 9 12 15 6" />
  </svg>;

// ---------------------------------------------------------------------------
// Live file viewer (wired stages — uses MarkdownViewer)
// ---------------------------------------------------------------------------

function LiveFileViewer({ item, onBack, totalCount }) {
  return (
    <div className="sources-panel">
      {totalCount !== undefined && <VaultBookmark count={totalCount} />}
      <div className="viewer-toolbar">
        <button className="viewer-back" onClick={onBack}>
          {backArrow}
          Files
        </button>
        <div className="viewer-path">
          <span className="viewer-path-name">{item.name}</span>
        </div>
        <span className="viewer-meta-pill">vault file</span>
      </div>
      <MarkdownViewer path={item.path} />
    </div>
  );
}

// ---------------------------------------------------------------------------
// Live sources panel (wired stages)
// ---------------------------------------------------------------------------

function LiveSourcesPanel({ folder }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    setLoading(true);
    setSelected(null);
    getRecent(folder)
      .then(setItems)
      .finally(() => setLoading(false));
  }, [folder]);
  /* eslint-enable react-hooks/set-state-in-effect */

  if (selected) {
    return (
      <LiveFileViewer
        item={selected}
        onBack={() => setSelected(null)}
        totalCount={items.length}
      />
    );
  }

  return (
    <div className="sources-panel">
      <VaultBookmark count={items.length} />
      <div className="sources-meta">
        <div className="sources-meta-left">
          <span className="sources-meta-eyebrow">Vault</span>
          <span>~/{folder}/</span>
        </div>
        <span>local-first · synced</span>
      </div>
      <div className="sources-body">
        <div className="sources-section">
          <h3 className="sources-section-title">
            Files &amp; folders
            <span className="sources-section-count">{items.length} files</span>
          </h3>
          {loading ? (
            <div style={{ padding: "12px 0", color: "var(--text-muted)", fontSize: 13 }}>Loading…</div>
          ) : items.length === 0 ? (
            <div style={{ padding: "12px 0", color: "var(--text-muted)", fontSize: 13 }}>
              No files yet in {folder}
            </div>
          ) : (
            <div className="tree">
              {items.map((item) => (
                <TreeRow
                  key={item.path}
                  row={{ type: "file", name: item.name, meta: item.modified?.slice(0, 10) || "", depth: 1 }}
                  onClick={() => setSelected(item)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// SourcesPanel — public component
// ---------------------------------------------------------------------------

function SourcesPanel({ stageId }) {
  const folder = LIVE_FOLDERS[stageId];
  if (folder) {
    return <LiveSourcesPanel folder={folder} />;
  }
  return (
    <div className="sources-panel" style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: 40 }}>
      <div style={{ fontSize: 13, color: "var(--text-muted)" }}>No live source panel for this workspace.</div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// StackedPanel — two faces, swap on click of the back card
// ---------------------------------------------------------------------------

function StackedPanel({ front, back }) {
  const [frontIsActive, setFrontIsActive] = useState(true);
  const swap = () => setFrontIsActive((v) => !v);

  return (
    <div className="stacked-panel">
      <div
        className={"stacked-face " + (frontIsActive ? "is-front" : "is-back")}
        onClick={frontIsActive ? undefined : swap}>
        {front}
      </div>
      <div
        className={"stacked-face " + (!frontIsActive ? "is-front" : "is-back")}
        onClick={!frontIsActive ? undefined : swap}>
        {back}
      </div>
    </div>
  );
}

// VaultBookmark — always-visible vertical tab on the right edge of the SourcesPanel
function VaultBookmark({ count }) {
  return (
    <div className="vault-bookmark" aria-hidden="true">
      <div className="vault-bookmark-icon">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
          <path d="M2 6a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6Z" />
        </svg>
      </div>
      <div className="vault-bookmark-text">Vault · Sources</div>
      <div className="vault-bookmark-count">{count}</div>
    </div>
  );
}

export { SourcesPanel, StackedPanel };
export default SourcesPanel;
