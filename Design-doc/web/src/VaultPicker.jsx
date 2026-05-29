import { useState, useEffect } from 'react';
import { getRecent } from './api.js';

// Dropdown backed by getRecent(folder). Emits the selected vault path upward.
// value: currently selected path (string | null)
// onChange(path | null): called when selection changes
export default function VaultPicker({ folder, value, onChange, placeholder = "Select a file…" }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!folder) return;
    setLoading(true);
    setError(null);
    getRecent(folder)
      .then(setItems)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [folder]);
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
      {items.map((item) => (
        <option key={item.path} value={item.path}>
          {item.name}
        </option>
      ))}
    </select>
  );
}
