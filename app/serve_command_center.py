"""Serve the Self-Improvement Command Center on http://localhost:8787.

Serves `app/command_center.html` and the live `pipeline_results.tsv` so the
dashboard can fetch the latest TSV on every refresh.

Usage:
    python app/serve_command_center.py
    python app/serve_command_center.py --port 9000 --no-open
"""

import argparse
import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
HTML_FILE = PROJECT_ROOT / "app" / "command_center.html"
TSV_FILE = PROJECT_ROOT / "Content-Hub-Vault-V2" / "00-Management-V2" / "pipeline_results.tsv"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            self._serve_file(HTML_FILE, "text/html; charset=utf-8")
        elif self.path.startswith("/pipeline_results.tsv"):
            self._serve_file(TSV_FILE, "text/tab-separated-values; charset=utf-8")
        else:
            self.send_error(404, f"Not found: {self.path}")

    def _serve_file(self, path: Path, content_type: str):
        if not path.exists():
            self.send_error(404, f"Missing: {path.name}")
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"  {self.address_string()} {fmt % args}")


def _bind(port: int, auto_bump: bool) -> socketserver.TCPServer:
    """Try to bind on port. If taken and auto_bump, try +1..+9. Else raise."""
    socketserver.TCPServer.allow_reuse_address = False
    last_err = None
    candidates = [port] if not auto_bump else [port + i for i in range(10)]
    for p in candidates:
        try:
            return socketserver.TCPServer(("127.0.0.1", p), Handler)
        except OSError as e:
            last_err = e
            print(f"  Port {p} unavailable ({e.errno}).")
    raise SystemExit(f"Could not bind any port in {candidates}: {last_err}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--no-open", action="store_true", help="Skip opening browser")
    ap.add_argument("--no-bump", action="store_true",
                    help="Fail instead of trying the next port if the chosen one is taken")
    args = ap.parse_args()

    if not HTML_FILE.exists():
        raise SystemExit(f"Missing: {HTML_FILE}")
    if not TSV_FILE.exists():
        print(f"Warning: TSV not found yet at {TSV_FILE}")

    httpd = _bind(args.port, auto_bump=not args.no_bump)
    actual_port = httpd.server_address[1]
    url = f"http://localhost:{actual_port}/"
    print(f"Command Center → {url}")
    print(f"Serving HTML  : {HTML_FILE}")
    print(f"Serving TSV   : {TSV_FILE}")
    print("Ctrl+C to stop.\n")

    if not args.no_open:
        webbrowser.open(url)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
