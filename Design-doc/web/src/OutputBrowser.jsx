import { useState, useEffect } from 'react';
import MarkdownViewer from './MarkdownViewer.jsx';
import { listOutputs } from './api.js';

// Renders the result of a completed job.
// For "file": opens primary_path directly.
// For "bundle" / "file_set": shows a selectable member list; primary_path selected by default.
export default function OutputBrowser({ result }) {
  const [members, setMembers] = useState(null);
  const [selected, setSelected] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!result) {
      setMembers(null);
      setSelected(null);
      return;
    }

    const { result_type, primary_path, outputs } = result;

    if (result_type === "file") {
      const name = primary_path.split(/[\\/]/).pop();
      setMembers([{ name, path: primary_path }]);
      setSelected(primary_path);
      return;
    }

    // bundle or file_set
    if (outputs?.length) {
      const list = outputs.map((p) => ({ name: p.split(/[\\/]/).pop(), path: p }));
      setMembers(list);
      setSelected(primary_path || list[0]?.path);
    } else {
      listOutputs(primary_path).then((items) => {
        setMembers(items);
        setSelected(primary_path || items[0]?.path);
      });
    }
  }, [result]);
  /* eslint-enable react-hooks/set-state-in-effect */

  if (!result || !members) return null;

  return (
    <div className="output-browser">
      {members.length > 1 && (
        <div className="output-browser-tabs">
          {members.map((m) => (
            <button
              key={m.path}
              className={"output-browser-tab" + (selected === m.path ? " is-active" : "")}
              onClick={() => setSelected(m.path)}
            >
              {m.name}
            </button>
          ))}
        </div>
      )}
      <MarkdownViewer path={selected} />
    </div>
  );
}
