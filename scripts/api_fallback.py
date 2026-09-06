#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from services.api.fallback import dispatch  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def _respond(self, status, body):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json; charset=utf-8")
        self.send_header("content-length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        status, body = dispatch("GET", self.path.split("?", 1)[0], None)
        self._respond(status, body)

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            payload = json.loads(raw.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("payload must be an object")
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            self._respond(400, {"error": "invalid json body"})
            return
        status, body = dispatch("POST", self.path.split("?", 1)[0], payload)
        self._respond(status, body)

    def log_message(self, fmt, *args):
        print("api:", fmt % args)


def main():
    port = int(os.environ.get("NEXTLAW_API_PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print("NextLaw607 fallback API: http://127.0.0.1:%d" % port)
    server.serve_forever()


if __name__ == "__main__":
    main()
