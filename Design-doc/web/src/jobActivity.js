// In-session job activity bus. Resets on page reload — no persistence.
const _running = new Set();
const _listeners = new Set();

function _notify() {
  _listeners.forEach((fn) => fn(new Set(_running)));
}

export function announceStart(stageId) {
  _running.add(stageId);
  _notify();
}

export function announceDone(stageId) {
  _running.delete(stageId);
  _notify();
}

export function announceFail(stageId) {
  _running.delete(stageId);
  _notify();
}

export function subscribe(fn) {
  _listeners.add(fn);
  return () => _listeners.delete(fn);
}

export function isRunning(stageId) {
  return _running.has(stageId);
}
