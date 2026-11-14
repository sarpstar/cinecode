#!/usr/bin/env python3
"""Minis WebView frame server for cinecode (the Chromium-free capture route).

Serves the film page AND receives rendered frames on the SAME origin, so nothing
crosses an origin boundary and no CORS is involved.

Endpoints
  GET  /                      -> health text
  GET  /__listing             -> JSON array of files written into --out
  GET  /<path>                -> static file from --root
  POST /__frame?name=X        -> body is the whole frame; written into --out
  POST /__chunk?name=X&off=N  -> body appended at byte offset N (audio WAVs)
  GET  /__close?name=X        -> finalize the .part file written by /__chunk
"""
import argparse
import http.server
import json
import os
import socketserver
import urllib.parse

ROOT = "."
OUT = "."
QUIET = True


def _safe(name):
    name = urllib.parse.unquote(str(name or "frame.bin"))
    name = os.path.normpath(name).lstrip("/").replace("..", "_")
    return name or "frame.bin"


class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        if not QUIET:
            super().log_message(fmt, *args)

    # ------------------------------------------------------------------ utils
    def _send(self, code, body=b"", ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if n <= 0:
            return b""
        try:
            return self.rfile.read(n)
        except (BrokenPipeError, ConnectionResetError):
            return b""

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode(), "application/json")

    # ------------------------------------------------------------------ verbs
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        name = _safe((qs.get("name") or ["frame.bin"])[0])
        body = self._body()
        dest = os.path.join(OUT, name)
        os.makedirs(os.path.dirname(dest) or ".", exist_ok=True)

        if parsed.path == "/__chunk":
            off = int((qs.get("off") or ["0"])[0])
            with open(dest + ".part", "r+b" if os.path.exists(dest + ".part") else "wb") as f:
                f.seek(off)
                f.write(body)
            return self._json({"ok": True, "bytes": len(body), "off": off})

        with open(dest, "wb") as f:
            f.write(body)
        self._json({"ok": True, "path": name, "bytes": len(body)})

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        path = parsed.path

        if path in ("/", "/__health"):
            return self._send(200, b"CINECODE-WEBVIEW-OK")

        if path == "/__listing":
            files = []
            for dirpath, _dirs, names in os.walk(OUT):
                for n in names:
                    if not n.startswith("."):
                        files.append(os.path.relpath(os.path.join(dirpath, n), OUT))
            return self._json(sorted(files))

        if path == "/__close":
            name = _safe((qs.get("name") or [""])[0])
            part, dest = os.path.join(OUT, name + ".part"), os.path.join(OUT, name)
            if os.path.exists(part):
                os.replace(part, dest)
                return self._json({"ok": True, "closed": name,
                                   "bytes": os.path.getsize(dest)})
            return self._json({"ok": False, "closed": None, "bytes": 0})

        rel = urllib.parse.unquote(path).lstrip("/")
        full = os.path.normpath(os.path.join(ROOT, rel))
        if not os.path.abspath(full).startswith(os.path.abspath(ROOT) + os.sep) and full != os.path.abspath(ROOT):
            return self._send(403, b"forbidden")
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        if not os.path.exists(full):
            return self._send(404, b"not found: " + rel.encode())
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
            ".mjs": "text/javascript; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".webp": "image/webp", ".svg": "image/svg+xml",
            ".wav": "audio/wav", ".mp3": "audio/mpeg", ".ogg": "audio/ogg",
            ".woff2": "font/woff2", ".woff": "font/woff",
        }.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
        with open(full, "rb") as f:
            self._send(200, f.read(), ctype)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    global ROOT, OUT, QUIET
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--port", type=int, default=8790)
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    ROOT = os.path.abspath(a.root)
    OUT = os.path.abspath(a.out)
    QUIET = not a.verbose
    os.makedirs(OUT, exist_ok=True)
    print("serving %s on 127.0.0.1:%d -> frames in %s" % (ROOT, a.port, OUT), flush=True)
    with Server(("127.0.0.1", a.port), Handler) as s:
        s.serve_forever()


if __name__ == "__main__":
    main()