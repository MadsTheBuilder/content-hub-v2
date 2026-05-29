"""Subprocess executor with live stdout streaming via queue.Queue."""

import queue
import subprocess
import threading
from pathlib import Path

REPO = Path(__file__).parent.parent


def run_skill(cmd: list[str], log_q: queue.Queue) -> int:
    proc = subprocess.Popen(
        cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, bufsize=1, encoding="utf-8", errors="replace",
    )
    for line in proc.stdout:
        log_q.put(line.rstrip())
    proc.wait()
    log_q.put(f"__EXIT__ {proc.returncode}")
    return proc.returncode


def run_in_thread(cmd: list[str], log_q: queue.Queue) -> threading.Thread:
    t = threading.Thread(target=run_skill, args=(cmd, log_q), daemon=True)
    t.start()
    return t
