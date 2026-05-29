import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { readVaultFile } from './api.js';

// Loads a vault file by path and renders it as markdown.
// Shows loading/error/empty states; never inlines demo markdown.
export default function MarkdownViewer({ path }) {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!path) {
      setContent(null);
      return;
    }
    setLoading(true);
    setError(null);
    setContent(null);
    readVaultFile(path)
      .then((data) => setContent(data.content))
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [path]);
  /* eslint-enable react-hooks/set-state-in-effect */

  if (!path) {
    return (
      <div className="output-empty">
        <div style={{ fontSize: 13, color: "var(--text-muted)" }}>No file selected.</div>
      </div>
    );
  }
  if (loading) {
    return (
      <div className="output-body">
        <div className="skeleton skeleton-row long" />
        <div className="skeleton skeleton-row medium" />
        <div className="skeleton skeleton-block" />
        <div className="skeleton skeleton-row long" />
        <div className="skeleton skeleton-row short" />
      </div>
    );
  }
  if (error) {
    return (
      <div className="output-body">
        <p style={{ color: "var(--text-muted)", fontSize: 13 }}>Could not load file: {error}</p>
      </div>
    );
  }
  if (content === null) return null;

  return (
    <div className="output-body md">
      <ReactMarkdown>{content}</ReactMarkdown>
    </div>
  );
}
