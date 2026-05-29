import { useState, useEffect } from 'react';
import { getRecent } from '../api.js';
import { subscribe } from '../jobActivity.js';

const CARD_FOLDERS = {
  trends: "04-Trends",
  research: "10-Research",
  ideation: "02-Ideas",
  outline: "06-Outlines",
};

const STATUS_FOLDERS = {
  trends: "04-Trends",
  research: "10-Research",
  ideation: "02-Ideas",
  hooks: "05-Hooks",
  distribution: "06-Outlines",
};

// Returns { recents, runningSet, sidebarStatuses }
// recents: { [cardId]: [{name, path, modified}] }
// runningSet: Set of currently running stageIds (from jobActivity)
// sidebarStatuses: { [stageId]: "running"|"done"|"idle" }
export function usePipelineSnapshot() {
  const [recents, setRecents] = useState({});
  const [hasFiled, setHasFiled] = useState({});
  const [runningSet, setRunningSet] = useState(new Set());

  useEffect(() => {
    let cancelled = false;
    async function load() {
      const entries = await Promise.all(
        Object.entries(CARD_FOLDERS).map(async ([id, folder]) => {
          const items = await getRecent(folder, 3);
          return [id, items];
        })
      );
      if (cancelled) return;
      setRecents(Object.fromEntries(entries));

      const statusEntries = await Promise.all(
        Object.entries(STATUS_FOLDERS).map(async ([id, folder]) => {
          const items = await getRecent(folder, 1);
          return [id, items.length > 0];
        })
      );
      if (cancelled) return;
      setHasFiled(Object.fromEntries(statusEntries));
    }
    load();
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    return subscribe((nextSet) => setRunningSet(nextSet));
  }, []);

  const sidebarStatuses = {};
  for (const stageId of Object.keys(STATUS_FOLDERS)) {
    if (runningSet.has(stageId)) {
      sidebarStatuses[stageId] = "running";
    } else if (hasFiled[stageId]) {
      sidebarStatuses[stageId] = "done";
    } else {
      sidebarStatuses[stageId] = "idle";
    }
  }

  return { recents, runningSet, sidebarStatuses };
}
