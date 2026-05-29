import { useState, useEffect, useRef } from 'react';

// Subscribes to a job's SSE stream. Pass jobId=null to stay idle.
// Returns { lines, status, result, error }
//   status: "idle" | "running" | "completed" | "failed"
export default function useJobStream(jobId) {
  const [lines, setLines] = useState([]);
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const esRef = useRef(null);

  /* eslint-disable react-hooks/set-state-in-effect */
  useEffect(() => {
    if (!jobId) return;

    setLines([]);
    setStatus("running");
    setResult(null);
    setError(null);

    const es = new EventSource(`/api/jobs/${jobId}/stream`);
    esRef.current = es;

    es.onmessage = (evt) => {
      let data;
      try { data = JSON.parse(evt.data); } catch { return; }

      const { type, line, result: res, error: err } = data;
      if (type === "stdout" || type === "stderr") {
        setLines((prev) => [...prev, line]);
      } else if (type === "done") {
        setResult(res);
        setStatus("completed");
        es.close();
      } else if (type === "error") {
        setError(err || "Job failed");
        setStatus("failed");
        es.close();
      }
      // ping: intentionally ignored
    };

    es.onerror = () => {
      if (es.readyState === EventSource.CLOSED) return;
      setError("Stream connection lost");
      setStatus("failed");
      es.close();
    };

    return () => {
      es.close();
      esRef.current = null;
    };
  }, [jobId]);
  /* eslint-enable react-hooks/set-state-in-effect */

  return { lines, status, result, error };
}
