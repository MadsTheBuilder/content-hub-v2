import { useState, useEffect } from 'react';
import { getRecent } from './api.js';

// Dropdown backed by getRecent(folder). Emits the selected vault path upward.
// value: currently selected path (string | null)
// onChange(path | null): called when selection changes
// subfoldersOnly: when true, only shows files from subdirectories (for trend repo pickers)
export default function VaultPicker({ folder, value, onChange, placeholder = "Select a file…", subfoldersOnly = false }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!folder) return;
    setLoading(true);
    setError(null);
    getRecent(folder, 50, subfoldersOnly)
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [folder, subfoldersOnly]);
  /* eslint-enable react-hooks/set-state-in-effect */

  if (loading) {
    return (
      <select className="vault-picker" disabled>
        <option>Loading…</option>
      </select>
    );
  }
  if (error) {
    return (
      <select className="vault-picker" disabled>
        <option>Error: {error}</option>
      </select>
    );
  }

  return (
    <select
      className="vault-picker"
      value={value || ""}
      onChange={(e) => onChange(e.target.value || null)}
    >
      <option value="">{placeholder}</option>
      {items.map((item) => {
        // For subfolder-only pickers (trend repos), format "owner_repo/..." → "owner/repo"
        const displayName = subfoldersOnly
          ? item.name.split('/')[0].replace('_', '/')
          : item.name;
        return (
          <option key={item.path} value={item.path}>
            {displayName}
          </option>
        );
      })}
    </select>
  );
}
