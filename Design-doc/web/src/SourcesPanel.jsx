// SourcesPanel — the "behind page" with vault files, folders, and sources used.
// Wired stages (trends/research/ideation/hooks) load real vault data via api.js.
// Unwired stages fall back to static demo data.

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
};

// ---------------------------------------------------------------------------
// Static VAULT_DATA — unwired stages only
// ---------------------------------------------------------------------------

const VAULT_DATA = {
  distribution: {
    accent: "var(--stage-distribution)",
    folder: "distribution/",
    tree: [
      { type: "folder", name: "distribution/", count: 14 },
      { type: "file", name: "local-rag-20min.kit.md", meta: "today", current: true, depth: 1, kind: "dist-output" },
      { type: "folder", name: "outlines/", count: 12 },
      { type: "file", name: "local-rag-20min.outline.md", meta: "8 sections", depth: 1, kind: "dist-outline-rag" },
      { type: "file", name: "cursor-vs-cline.outline.md", meta: "in progress", depth: 1, kind: "outline-cursor" },
      { type: "folder", name: "thumbnails/", count: 36 },
      { type: "file", name: "brief-template.md", meta: "channel style", depth: 1, kind: "thumb-brief" }],
    sources: [
      { host: "📄", title: "Outline · local-rag-20min.outline.md", url: "vault://outlines/local-rag…", meta: "primary" },
      { host: "📄", title: "Hooks · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
      { host: "🎬", title: "Thumbnail brief template", url: "vault://thumbnails/brief.md", meta: "channel" }]
  },
  brain: {
    accent: "var(--brain)",
    folder: "brain/",
    tree: [
      { type: "folder", name: "brain/", count: 142 },
      { type: "file", name: "vision-pro-teardown.md", meta: "today", current: true, depth: 1, kind: "brain-current" },
      { type: "file", name: "fireship-svelte-rant.md", meta: "yesterday", depth: 1, kind: "brain-prev1" },
      { type: "file", name: "marques-segment-cuts.md", meta: "2d", depth: 1, kind: "brain-prev2" },
      { type: "folder", name: "techniques/", count: 37 },
      { type: "file", name: "authority-claim.md", meta: "8 examples", depth: 1, kind: "tech-authority" },
      { type: "file", name: "timestamp-promise.md", meta: "12 examples", depth: 1, kind: "tech-timestamp" },
      { type: "folder", name: "raw-imports/", count: 88 }],
    sources: [
      { host: "YT", title: "Vision Pro teardown — original video", url: "youtube.com/watch?v=demo-tear-down", meta: "input" },
      { host: "📝", title: "Pasted transcript (3,420 words)", url: "session://pasted-1", meta: "input" },
      { host: "📚", title: "Technique library cross-references", url: "vault://brain/techniques/", meta: "linked" }]
  },
  title: {
    accent: "var(--stage-title)",
    folder: "titles/",
    tree: [
      { type: "folder", name: "titles/", count: 22 },
      { type: "file", name: "local-rag-20min.titles.md", meta: "today", current: true, depth: 1, kind: "title-output" },
      { type: "file", name: "cursor-vs-cline.titles.md", meta: "3d", depth: 1, kind: "title-cursor" },
      { type: "folder", name: "patterns/", count: 8 },
      { type: "file", name: "i-built-X-in-Y.md", meta: "highest CTR", depth: 1, kind: "title-pattern-built" },
      { type: "file", name: "contrarian-claim.md", meta: "high variance", depth: 1, kind: "title-pattern-contra" },
      { type: "file", name: "number-prefix.md", meta: "safe floor", depth: 1, kind: "title-pattern-num" },
      { type: "folder", name: "ab-history/", count: 96 }],
    sources: [
      { host: "📄", title: "Hook · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
      { host: "📄", title: "Ideation · may-batch-12.md", url: "vault://ideation/may-batch-12.md", meta: "linked" },
      { host: "📊", title: "Channel · title CTR history (12mo)", url: "vault://analytics/titles-12mo.csv", meta: "primary" }]
  },
  outline: {
    accent: "var(--stage-outline)",
    folder: "outlines/",
    tree: [
      { type: "folder", name: "outlines/", count: 17 },
      { type: "file", name: "local-rag-20min.outline.md", meta: "8 sections", current: true, depth: 1, kind: "outline-rag" },
      { type: "file", name: "cursor-vs-cline.outline.md", meta: "in progress", depth: 1, kind: "outline-cursor" },
      { type: "folder", name: "templates/", count: 6 },
      { type: "file", name: "how-to-tutorial.md", meta: "default", depth: 1, kind: "outline-tpl-howto" },
      { type: "file", name: "opinion-essay.md", meta: "channel style", depth: 1, kind: "outline-tpl-opinion" },
      { type: "folder", name: "retention-shapes/", count: 4 }],
    sources: [
      { host: "📄", title: "Hook · local-rag-20min.md", url: "vault://hooks/local-rag…", meta: "linked" },
      { host: "📄", title: "Title · local-rag-20min.titles.md", url: "vault://titles/local-rag…", meta: "linked" },
      { host: "📊", title: "Channel · retention shapes (top 20)", url: "vault://analytics/retention-top20.csv", meta: "reference" }]
  }
};

// ---------------------------------------------------------------------------
// Static FILE_CONTENT — unwired stages only
// ---------------------------------------------------------------------------

const FILE_CONTENT = {
  // Distribution
  "dist-output":
    <>
      <h1>Distribution kit — Local RAG in 20 min</h1>
      <h2>Titles</h2>
      <ol>
        <li>I built a RAG that runs on my laptop. In 20 minutes.</li>
        <li>You don&apos;t need an API. (Local RAG, 47 lines)</li>
        <li>This RAG runs offline. It cost me $0 to build.</li>
      </ol>
      <h2>Chapters · 7</h2>
      <h2>Thumbnail brief</h2>
      <p>Laptop with terminal open, &quot;OFFLINE&quot; label glowing. Face cam mild shock. Top text: <code>20 MIN. NO API.</code></p>
    </>,

  "dist-outline-rag":
    <>
      <h1>Outline — Local RAG in 20 min</h1>
      <ol>
        <li>The setup (00:00)</li>
        <li>Why local matters (01:30)</li>
        <li>Embedding model: nomic-embed-text (04:12)</li>
        <li>Vector store: sqlite-vss (07:40)</li>
        <li>Putting it together (11:05)</li>
        <li>Live demo on my codebase (16:20)</li>
        <li>Where it breaks (18:45)</li>
        <li>Outro + next video tease (20:10)</li>
      </ol>
    </>,

  "outline-cursor":
    <>
      <h1>Outline — Cursor vs Cline</h1>
      <p style={{ color: "var(--warning)" }}>⚠ In progress — 4 of 8 sections drafted.</p>
    </>,

  "thumb-brief":
    <>
      <h1>Thumbnail brief template</h1>
      <p>Channel style guide: high-contrast object/face split, max 4 words of text, yellow accent on the number.</p>
    </>,

  // Brain
  "brain-current":
    <>
      <h1>Vision Pro teardown — analysis</h1>
      <p><strong>Hook Quality:</strong> 8.4/10 · <strong>Structure:</strong> 7.9/10 · <strong>Triggers:</strong> 5</p>
      <p>The opening does three jobs in eleven seconds. Authority claim, payoff promise, antagonist frame. Active watching pattern.</p>
    </>,

  "brain-prev1":
    <>
      <h1>Fireship — Svelte rant</h1>
      <p><strong>Hook Quality:</strong> 9.1/10. Heavy reliance on the contrarian-claim pattern. Audience pre-flattered as &quot;smart enough to disagree&quot;.</p>
    </>,

  "brain-prev2":
    <>
      <h1>Marques — segment cuts breakdown</h1>
      <p><strong>Structure:</strong> 9.4/10. Cuts at exact retention dips. CTA lives at the 47% mark.</p>
    </>,

  "tech-authority":
    <>
      <h1>Technique — Authority Claim</h1>
      <p>Place an unjustified expertise assertion in the first 3 seconds. Don&apos;t introduce yourself; assume it.</p>
      <h2>8 examples</h2>
      <ul>
        <li>&quot;The first second I saw this, I knew…&quot;</li>
        <li>&quot;I&apos;ve been building this for 12 years…&quot;</li>
        <li>&quot;Most people will get this wrong…&quot;</li>
      </ul>
    </>,

  "tech-timestamp":
    <>
      <h1>Technique — Timestamp Promise</h1>
      <p>Reference a specific later moment in the video. &quot;Watch what happens at 0:23.&quot; Locks in a forward-looking attention contract.</p>
    </>,

  // Title
  "title-output":
    <>
      <h1>Title candidates — Local RAG in 20 min</h1>
      <ol>
        <li><strong>I built a RAG that runs on my laptop. In 20 minutes.</strong> <em>(predicted CTR 9.4%)</em></li>
        <li><strong>You don&apos;t need an API. (Local RAG, 47 lines)</strong> <em>(9.1%)</em></li>
        <li><strong>This RAG runs offline. It cost me $0 to build.</strong> <em>(8.7%)</em></li>
        <li><strong>20 minutes. 47 lines. No API key.</strong> <em>(8.5%)</em></li>
        <li><strong>I gave Claude my entire codebase… locally.</strong> <em>(7.9%)</em></li>
      </ol>
    </>,

  "title-cursor":
    <>
      <h1>Title candidates — Cursor vs Cline</h1>
      <ol>
        <li>Cursor lost me. Here&apos;s the 4-tool setup I use now. <em>(9.0%)</em></li>
        <li>I switched from Cursor to Cline. No regrets. <em>(8.6%)</em></li>
        <li>The Cursor pricing change pushed me out. <em>(8.2%)</em></li>
      </ol>
    </>,

  "title-pattern-built":
    <>
      <h1>Pattern — I built X in Y</h1>
      <p>Highest-CTR title template on this channel. Pairs a verb with a constraint (time, lines, dollars).</p>
      <ul>
        <li>I built a RAG in 20 minutes.</li>
        <li>I shipped a CLI in 47 lines.</li>
        <li>I deployed an AI agent for $0.</li>
      </ul>
    </>,

  "title-pattern-contra":
    <>
      <h1>Pattern — Contrarian claim</h1>
      <p>Higher variance. When it lands it dominates; when it misses it underperforms baseline by ~30%.</p>
    </>,

  "title-pattern-num":
    <>
      <h1>Pattern — Number-prefix</h1>
      <p>&quot;3 prompts that fix…&quot;, &quot;5 hooks that…&quot;. Safe floor, low ceiling.</p>
    </>,

  // Outline
  "outline-rag":
    <>
      <h1>Outline — Local RAG in 20 min</h1>
      <ol>
        <li><strong>The setup (00:00–01:30)</strong> — demo on screen, narrate the claim.</li>
        <li><strong>Why local matters (01:30–04:12)</strong> — cost + privacy framing.</li>
        <li><strong>Embedding model: nomic-embed-text (04:12–07:40)</strong> — install + first query.</li>
        <li><strong>Vector store: sqlite-vss (07:40–11:05)</strong> — schema + insert path.</li>
        <li><strong>Putting it together (11:05–16:20)</strong> — wiring + retrieval loop.</li>
        <li><strong>Live demo on my codebase (16:20–18:45)</strong> — real query, real answer.</li>
        <li><strong>Where it breaks (18:45–20:10)</strong> — honest failure modes.</li>
        <li><strong>Outro + next video tease (20:10–end)</strong></li>
      </ol>
    </>,

  "outline-tpl-howto":
    <>
      <h1>Template — How-to tutorial</h1>
      <ol>
        <li>Working demo on screen</li>
        <li>Why it matters (cost / risk / time)</li>
        <li>The 3–4 building blocks, one at a time</li>
        <li>Wiring them together</li>
        <li>Live demo</li>
        <li>Failure modes</li>
        <li>CTA loop + next video</li>
      </ol>
    </>,

  "outline-tpl-opinion":
    <>
      <h1>Template — Opinion essay</h1>
      <ol>
        <li>Claim, no setup</li>
        <li>Single piece of evidence</li>
        <li>Counter-objection acknowledged + refuted</li>
        <li>Stakes / who this changes things for</li>
        <li>Concrete next action</li>
      </ol>
    </>
};

// ---------------------------------------------------------------------------
// Shared UI primitives
// ---------------------------------------------------------------------------

function generateSourcePreview(s) {
  return (
    <>
      <div className="viewer-empty-meta">
        <div><span className="viewer-empty-meta-key">URL · </span><span className="viewer-empty-meta-val">{s.url}</span></div>
        <div><span className="viewer-empty-meta-key">Type · </span><span className="viewer-empty-meta-val">{s.host === "YT" ? "Video source" : s.host === "RD" ? "Forum thread" : s.host === "HN" ? "Forum thread" : s.host === "X" ? "Microblog" : "Document"}</span></div>
        <div><span className="viewer-empty-meta-key">Scope · </span><span className="viewer-empty-meta-val">{s.meta}</span></div>
      </div>
      <h1>{s.title}</h1>
      <p style={{ color: "var(--text-secondary)" }}>
        Source preview cached locally. Click &quot;Open externally&quot; to load the live page in your browser.
      </p>
    </>
  );
}

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
// Static file viewer (unwired stages)
// ---------------------------------------------------------------------------

function FileViewer({ item, onBack, folder, totalCount }) {
  const isSource = item._kind === "source";
  const content = isSource
    ? generateSourcePreview(item)
    : FILE_CONTENT[item.kind] || <p style={{ color: "var(--text-muted)" }}>Preview not yet generated for this file.</p>;

  return (
    <div className="sources-panel">
      {totalCount !== undefined && <VaultBookmark count={totalCount} />}
      <div className="viewer-toolbar">
        <button className="viewer-back" onClick={onBack}>
          {backArrow}
          Files
        </button>
        <div className="viewer-path">
          {isSource
            ? <>session://sources/<span className="viewer-path-name">{item.url}</span></>
            : <>~/content-hub/{folder}<span className="viewer-path-name">{item.name}</span></>
          }
        </div>
        {isSource
          ? <button className="viewer-external">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                <polyline points="15 3 21 3 21 9" />
                <line x1="10" y1="14" x2="21" y2="3" />
              </svg>
              Open externally
            </button>
          : <span className="viewer-meta-pill">{item.current ? "current run" : "vault file"}</span>
        }
      </div>
      <div className="viewer-body md">
        {content}
      </div>
    </div>
  );
}

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
// Static sources panel (unwired stages)
// ---------------------------------------------------------------------------

function StaticSourcesPanel({ data }) {
  const [selected, setSelected] = useState(null);
  const filesCount = data.tree.filter((r) => r.type === "file").length;
  const totalCount = filesCount + data.sources.length;

  if (selected) {
    return <FileViewer item={selected} onBack={() => setSelected(null)} folder={data.folder} totalCount={totalCount} />;
  }

  return (
    <div className="sources-panel">
      <VaultBookmark count={totalCount} />
      <div className="sources-meta">
        <div className="sources-meta-left">
          <span className="sources-meta-eyebrow">Vault</span>
          <span>~/content-hub/{data.folder}</span>
        </div>
        <span>local-first · synced</span>
      </div>
      <div className="sources-body">
        <div className="sources-section">
          <h3 className="sources-section-title">
            Files &amp; folders
            <span className="sources-section-count">{data.tree.filter((r) => r.type === "file").length} files</span>
          </h3>
          <div className="tree">
            {data.tree.map((row, i) =>
              <TreeRow key={i} row={row} onClick={() => setSelected({ ...row, _kind: "file" })} />
            )}
          </div>
        </div>
        <div className="sources-section">
          <h3 className="sources-section-title">
            Sources cited by this run
            <span className="sources-section-count">{data.sources.length}</span>
          </h3>
          <div>
            {data.sources.map((s, i) =>
              <button key={i} className="source-link" onClick={() => setSelected({ ...s, _kind: "source" })}>
                <div className="source-link-favicon">{s.host}</div>
                <div className="source-link-body">
                  <div className="source-link-title">{s.title}</div>
                  <div className="source-link-url">{s.url}</div>
                </div>
                <div className="source-link-meta">{s.meta}</div>
              </button>
            )}
          </div>
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
  const data = VAULT_DATA[stageId] || VAULT_DATA.brain;
  return <StaticSourcesPanel data={data} />;
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
