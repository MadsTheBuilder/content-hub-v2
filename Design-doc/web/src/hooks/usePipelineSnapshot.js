import { useState, useEffect, useRef } from 'react';
import { getRecent } from '../api.js';
import { subscribe } from '../jobActivity.js';

const CARD_FOLDERS = {
  trends: "04-Trends",
  research: "10-Research",
  ideation: "02-Ideas",
  outline: "06-Outlines",
};

const STATUS_FOLDERS = {
  trends: ["04-Trends"],
  research: ["10-Research"],
  ideation: ["02-Ideas"],
  hooks: ["05-Hooks"],
  distribution: ["06-Outlines", "07-Titles", "08-Distribution", "09-Shorts"],
};

// Returns { recents, runningSet, sidebarStatuses }
// recents: { [cardId]: [{name, path, modified}] }
// runningSet: Set of currently running stageIds (from jobActivity)
// sidebarStatuses: { [stageId]: "running"|"done"|"idle" }
export function usePipelineSnapshot() {
  const [recents, setRecents] = useState({});
  const [hasFiled, setHasFiled] = useState({});
  const [runningSet, setRunningSet] = useState(new Set());
  const [refreshTick, setRefreshTick] = useState(0);
  const prevSizeRef = useRef(0);

  useEffect(() => {
    let cancelled = false;
    async function loadSnapshot() {
      const entries = await Promise.all(
        Object.entries(CARD_FOLDERS).map(async ([id, folder]) => {
          const items = await getRecent(folder, 3);
          return [id, items];
        })
      );
      if (cancelled) return;
      setRecents(Object.fromEntries(entries));

      const statusEntries = await Promise.all(
        Object.entries(STATUS_FOLDERS).map(async ([id, folders]) => {
          const results = await Promise.all(folders.map(f => getRecent(f, 1)));
          return [id, results.some(items => items.length > 0)];
        })
      );
      if (cancelled) return;
      setHasFiled(Object.fromEntries(statusEntries));
    }
    loadSnapshot();
    return () => { cancelled = true; };
  }, [refreshTick]);

  useEffect(() => {
    const onFocus = () => setRefreshTick(t => t + 1);
    window.addEventListener('focus', onFocus);
    return () => window.removeEventListener('focus', onFocus);
  }, []);

  useEffect(() => {
    return subscribe((nextSet) => {
      setRunningSet(nextSet);
      if (nextSet.size < prevSizeRef.current) {
        setRefreshTick(t => t + 1);
      }
      prevSizeRef.current = nextSet.size;
    });
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
