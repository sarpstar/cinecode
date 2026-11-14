#!/usr/bin/env python3
"""Chromium-free frame capture for cinecode, driven by the Minis in-app WebView.

Drop-in replacement for capture.mjs on devices where headless Chrome cannot run
(iOS/iSH). It keeps the same command line and the same page contract:

  window.READY             Promise<{frames, fps, width, height, renderer, ...}>
  window.captureFrame(i)   render frame i, return a PNG/JPEG data URL
  window.renderAudio()     Promise<AudioBuffer>, the whole soundtrack
  window.textCheck(i)      optional, Quick-mode pages loaded with ?textcheck=1

Frames never cross the JS bridge: the page renders each one to a blob and POSTs
it to the same-origin server (webview_server.py), which writes it to disk. Only
short status JSON comes back, so a 1080p frame costs no context.

Usage (same flags as capture.mjs):
  python3 capture_webview.py --url film.html --probe [--params "w=1920&h=1080"]
  python3 capture_webview.py --url film.html --out frames/S01 [--frames 0,48,96]
  python3 capture_webview.py --url film.html --video renders/picture-v1.mp4 [--crf 17]
  python3 capture_webview.py --url film.html --audio audio/film.wav
  python3 capture_webview.py --url film.html --verify
  python3 capture_webview.py --url film.html --text-check 0.5
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
SERVER = os.path.join(HERE, "webview_server.py")
BROWSER = "minis-browser-use"
CHUNK_FRAMES = int(os.environ.get("CINECODE_WV_CHUNK") or 4)
FRAME_TIMEOUT = float(os.environ.get("CINECODE_FRAME_TIMEOUT") or 180)
POLL_S = 1.0


# --------------------------------------------------------------------- helpers
def log(msg):
    print(msg, flush=True)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def wait_port(port, timeout=20):
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection(("127.0.0.1", port), 0.5):
                return True
        except OSError:
            time.sleep(0.2)
    return False


def start_server(root, out, port):
    os.makedirs(out, exist_ok=True)
    # The log lives beside the output directory, not inside it: the frame dir is
    # browsed by the WebView as a document root, and an index.html-like stray file
    # there would shadow the film page.
    logf = open(os.path.join(root, ".webview-server.log"), "ab")
    proc = subprocess.Popen([sys.executable, SERVER, "--root", root, "--out", out,
                             "--port", str(port)], stdout=logf, stderr=logf)
    if not wait_port(port):
        raise SystemExit("FAILED: the frame server did not start")
    return proc


def http_get(url, timeout=15):
    import urllib.request
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def browser(args, timeout=600):
    """Run one minis-browser-use action and return its parsed JSON."""
    cmd = [BROWSER] + args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError:
        raise SystemExit("FAILED: %s not found (this route needs the Minis app)" % BROWSER)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "timeout"}
    return parse_browser(r.stdout, r.returncode)


def parse_browser(stdout, rc=0):
    txt = (stdout or "").strip()
    if not txt:
        return {"ok": rc == 0, "raw": ""}
    # the tool may print a note line before the JSON object
    start = txt.find("{")
    if start < 0:
        return {"ok": rc == 0, "raw": txt}
    obj = None
    for end in range(len(txt), start, -1):
        try:
            obj = json.loads(txt[start:end])
            break
        except json.JSONDecodeError:
            continue
    if obj is None:
        return {"ok": rc == 0, "raw": txt}
    if isinstance(obj, dict):
        obj.setdefault("ok", rc == 0)
    return obj


def js(script, timeout=600):
    """Evaluate JS in the page and return the value the script returned.

    minis-browser-use wraps the result: {"ok":true,"data":{"text":"<json or 'null'>",
    "page_url":...}}. The actual value is JSON-encoded inside data.text, so it is
    decoded here; a plain sentence (or the trailing tab_id note) is returned as-is.
    """
    res = browser(["execute_js", "--script", script, "--compact"], timeout=timeout)
    if not res.get("ok", True):
        err = res.get("error") or res.get("raw") or str(res)[:300]
        if isinstance(err, dict):
            err = err.get("message") or json.dumps(err)
        raise RuntimeError("page error: %s" % err)
    data = res.get("data", res)
    if isinstance(data, str):
        return _decode(data)
    if isinstance(data, dict):
        if "text" in data:
            return _decode(data["text"])
        return {k: v for k, v in data.items() if k not in ("success", "page_url")}
    return data


def _decode(txt):
    """Turn the tool's `text` field into a Python value."""
    if not isinstance(txt, str):
        return txt
    lines = [l for l in txt.splitlines() if l.strip()]
    if not lines:
        return None
    # the last line may be the tool's own "  tab_id: 1" note
    body = "\n".join(l for l in lines if not re.fullmatch(r"\s*tab_id:\s*\d+\s*", l))
    body = body.strip()
    if body in ("", "null", "undefined"):
        return None
    if body == "true":
        return True
    if body == "false":
        return False
    try:
        return json.loads(body)
    except (json.JSONDecodeError, ValueError):
        return body


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


# ---------------------------------------------------------------------- server
class Server:
    def __init__(self, page_path, out_dir):
        self.page = os.path.abspath(page_path)
        self.root = os.path.dirname(self.page)
        self.base = os.path.basename(self.page)
        # The page is always served over HTTP (never file://), so its relative
        # imports and fonts resolve; frames land in out_dir when there is one.
        self.out = os.path.abspath(out_dir or os.path.join(
            os.path.dirname(self.page), ".webview-frames"))
        self.port = free_port()
        self.proc = None

    def __enter__(self):
        self.proc = start_server(self.root, self.out, self.port)
        return self

    def __exit__(self, *a):
        if self.proc:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def url(self, params=None):
        u = "http://127.0.0.1:%d/%s" % (self.port, self.base)
        if params:
            u += "?" + params
        return u

    def listing(self):
        try:
            return json.loads(http_get("http://127.0.0.1:%d/__listing" % self.port))
        except Exception:
            return []


# ---------------------------------------------------------------- capture core
# Everything inside this string runs in the page. It returns only small JSON.
READY_JS = """
return await (async () => {
  const info = await window.READY;
  return info;
})();
"""

RENDER_JS = """
return await (async () => {
  const frames = %s;
  const mime = %s, quality = %s;
  const out = [];
  for (const i of frames) {
    const url = window.captureFrame(i, mime, quality);
    if (typeof url !== 'string' || !url.startsWith('data:')) {
      return {error: 'captureFrame(' + i + ') did not return a data URL'};
    }
    const ext = url.slice(5, url.indexOf(';'));
    const blob = await (await fetch(url)).blob();
    const name = String(i).padStart(6, '0') + '.' + (ext === 'image/jpeg' ? 'jpg' : ext.split('/')[1] || 'png');
    const r = await fetch('/__frame?name=' + encodeURIComponent(name), {method: 'POST', body: blob});
    if (!r.ok) return {error: 'upload failed for ' + name + ' (' + r.status + ')'};
    out.push(name);
  }
  return {done: out.length, names: out.slice(0, 3)};
})();
"""

VERIFY_JS = """
return await (async () => {
  const k = %d;
  const a = window.captureFrame(k, 'image/png');
  window.captureFrame(0, 'image/png');
  const b = window.captureFrame(k, 'image/png');
  const h = (s) => { let x = 0; for (let i = 0; i < s.length; i += 97) x = (x * 31 + s.charCodeAt(i)) | 0; return s.length + ':' + (x >>> 0); };
  return {a: h(a), b: h(b), same: a === b};
})();
"""

TEXTCHECK_JS = """
return (() => {
  const every = %d;
  const total = %d;
  const spans = [], open = new Map();
  for (let f = 0; f < total; f += every) {
    for (const r of window.textCheck(f)) {
      const key = r.kind === 'overlap' ? 'overlap\\u0000' + [r.a, r.b].sort().join('\\u0000') : 'contrast\\u0000' + r.s;
      const t = f / (window.__fps || 30), sp = open.get(key);
      if (sp && t - sp.to <= (every / (window.__fps || 30)) * 1.5) { sp.to = t; sp.worst = Math.max(sp.worst, r.px ?? r.share); }
      else { const n = Object.assign({}, r, {from: t, to: t, worst: r.px ?? r.share}); spans.push(n); open.set(key, n); }
    }
  }
  return spans;
})();
"""

AUDIO_JS = """
return await (async () => {
  const b = await window.renderAudio();
  const ch = b.numberOfChannels, n = b.length, sr = b.sampleRate;
  const data = Array.from({length: ch}, (_, c) => b.getChannelData(c));
  const head = 58, bytes = new ArrayBuffer(head + n * ch * 4), v = new DataView(bytes);
  const str = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
  str(0, 'RIFF'); v.setUint32(4, bytes.byteLength - 8, true); str(8, 'WAVE');
  str(12, 'fmt '); v.setUint32(16, 18, true); v.setUint16(20, 3, true); v.setUint16(22, ch, true);
  v.setUint32(24, sr, true); v.setUint32(28, sr * ch * 4, true); v.setUint16(32, ch * 4, true);
  v.setUint16(34, 32, true); v.setUint16(36, 0, true);
  str(38, 'fact'); v.setUint32(42, 4, true); v.setUint32(46, n, true);
  str(50, 'data'); v.setUint32(54, n * ch * 4, true);
  const f = new Float32Array(n * ch);
  let peak = 0;
  for (let i = 0; i < n; i++) for (let c = 0; c < ch; c++) {
    const s = data[c][i]; f[i * ch + c] = s; const a = Math.abs(s); if (a > peak) peak = a;
  }
  new Uint8Array(bytes, head).set(new Uint8Array(f.buffer));
  window.__cinecodeWav = new Uint8Array(bytes);
  return {ch, n, sr, size: bytes.byteLength, peak};
})();
"""

AUDIO_CHUNK_JS = """
return await (async () => {
  const off = %d, end = Math.min(off + %d, window.__cinecodeWav.length);
  const part = window.__cinecodeWav.subarray(off, end);
  const r = await fetch('/__chunk?name=%s&off=' + off, {method: 'POST', body: part});
  if (!r.ok) return {error: 'chunk upload failed at ' + off};
  return {off, bytes: part.length, done: end >= window.__cinecodeWav.length};
})();
"""


def open_page(srv, params):
    """Open the film page and return the READY metadata of *this* document.

    Navigating reuses the same tab, and the old document's `window.READY` is still
    readable for a moment after `navigate` returns, so a plain read can hand back
    the previous page's numbers. Comparing `performance.timeOrigin` (which is new
    for every document) makes sure the metadata belongs to the page we just opened.
    """
    try:
        before = float(js("return performance.timeOrigin;", timeout=60) or 0)
    except Exception:
        before = 0.0
    # A tab whose page is still running heavy JS (a previous render loop) can make
    # a same-tab navigate hang; open a fresh tab instead and close it afterwards.
    tab = None
    res = None
    for attempt in range(3):
        try:
            if tab is None:
                tab = browser(["new_tab", "--url", srv.url(params), "--compact"], timeout=120)
            else:
                tab = browser(["navigate", "--url", srv.url(params), "--compact"], timeout=120)
        except Exception as e:
            tab = {"ok": False, "error": str(e)}
        if isinstance(tab, dict) and tab.get("ok"):
            res = tab
            break
        time.sleep(1.0)
    if res is None:
        raise SystemExit("FAILED: the WebView did not open the page: %r" % (tab,))

    deadline = time.time() + 45
    while time.time() < deadline:
        try:
            origin = float(js("return performance.timeOrigin;", timeout=60) or 0)
            if origin > before:
                break
        except Exception:
            pass
        time.sleep(0.5)

    deadline = time.time() + 60
    info = None
    while time.time() < deadline:
        info = get_info(params)
        if isinstance(info, dict) and info.get("frames"):
            return info
        time.sleep(0.5)
    return info


def get_info(params):
    return js(READY_JS, timeout=FRAME_TIMEOUT * 2)


def render_range(url, frames, mime, quality, out_dir, status_path, total):
    done = 0
    t0 = time.time()
    for i in range(0, len(frames), CHUNK_FRAMES):
        batch = frames[i:i + CHUNK_FRAMES]
        res = js(RENDER_JS % (json.dumps(batch), json.dumps(mime), json.dumps(quality)),
                 timeout=FRAME_TIMEOUT * max(2, len(batch)))
        if not isinstance(res, dict) or "error" in (res or {}):
            raise SystemExit("FAILED: %s" % ((res or {}).get("error") if isinstance(res, dict) else res))
        done += len(batch)
        if status_path:
            secs = time.time() - t0
            rate = done / max(secs, 0.001)
            write_status(status_path, {"state": "running", "done": done, "total": total,
                                       "fps": round(rate, 2),
                                       "eta_s": int((total - done) / rate) if rate > 0 else None})
    return done


def write_status(path, obj):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".part"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(obj, f)
        os.replace(tmp, path)
    except OSError:
        pass


# ----------------------------------------------------------------------- modes
def do_probe(page, params):
    info = get_info(params)
    if not isinstance(info, dict):
        raise SystemExit("FAILED: the page did not report READY: %r" % (info,))
    for k in ("frames", "width", "height"):
        if not isinstance(info.get(k), int) or info[k] <= 0:
            raise SystemExit("FAILED: READY must provide positive integer frames/width/height")
    if not (isinstance(info.get("fps"), (int, float)) and info["fps"] > 0):
        raise SystemExit("FAILED: READY must provide a positive fps")
    log("renderer: %s" % info.get("renderer", "minis-webview"))
    for line in _as_list(info.get("qc")):
        log("qc: %s" % line)
    log("page: %dx%d, %d frames @ %s fps" % (info["width"], info["height"],
                                             info["frames"], info["fps"]))
    keys = ("title", "bounds", "vo", "palette", "lookPalette", "families", "sfx")
    meta = {k: info[k] for k in keys if k in info}
    if meta:
        log("meta: %s" % json.dumps(meta, ensure_ascii=False))
    return info


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def do_verify(page, params):
    info = get_info(params)
    k = min(info["frames"] - 1, info["frames"] // 2)
    res = js(VERIFY_JS % k, timeout=FRAME_TIMEOUT * 3)
    same = bool(res.get("same"))
    log("frame %d rendered twice (with frame 0 in between): %s" % (k, "IDENTICAL" if same else "DIFFERENT"))
    log("deterministic: %s" % ("yes" if same else
                               "NO - find state carried between frames, Date/performance.now, Math.random"))
    return 0 if same else 1


def do_text_check(page, params, every_s):
    # The page only installs window.textCheck when it is loaded with textcheck=1
    # (the instrumentation must wrap fillText before any frame is drawn), so the
    # page is re-opened here with that flag added to the query string.
    extra = "textcheck=1" if "textcheck=" not in (params or "") else None
    merged = (params + "&" + extra) if (params and extra) else (extra or params)
    if extra:
        browser(["navigate", "--url", page.url(merged), "--compact"], timeout=120)
    info = get_info(merged)
    fps = float(info["fps"])
    every = max(1, int(round(fps * (every_s if every_s > 0 else 0.5))))
    js("window.__fps = %s; 1" % fps, timeout=60)
    spans = js(TEXTCHECK_JS % (every, int(info["frames"])), timeout=FRAME_TIMEOUT * 4)
    if not isinstance(spans, list):
        log("text check: the page has no textCheck (load it with textcheck=1 in --params)")
        return 0

    def at(sp):
        return ("%.1f-%.1f s" % (sp["from"], sp["to"])) if sp["to"] > sp["from"] else ("%.1f s" % sp["from"])

    def clip(s):
        s = str(s)
        return json.dumps(s if len(s) <= 28 else s[:27] + "\u2026", ensure_ascii=False)

    for sp in sorted(spans, key=lambda x: x["from"]):
        if sp.get("kind") == "overlap":
            log("TEXT OVERLAP %s: %s and %s share %s px of ink" %
                (at(sp), clip(sp.get("a")), clip(sp.get("b")), sp.get("worst")))
        else:
            log("LOW CONTRAST %s: %s: %s %% of its letters' edges are within 2:1 of their surround" %
                (at(sp), clip(sp.get("s")), sp.get("worst")))
    if not spans:
        log("text check: no overlapping lines, no line lost in its ground")
    return 1 if spans else 0


def do_audio(page, out_wav, info):
    kind = js("return typeof window.renderAudio;", timeout=60)
    if kind != "function":
        raise SystemExit("FAILED: --audio: the page has no window.renderAudio()")
    t0 = time.time()
    meta = js(AUDIO_JS, timeout=FRAME_TIMEOUT * 10)
    if not isinstance(meta, dict) or "size" not in meta:
        raise SystemExit("FAILED: renderAudio did not return audio metadata: %r" % (meta,))
    os.makedirs(os.path.dirname(os.path.abspath(out_wav)) or ".", exist_ok=True)
    name = os.path.basename(out_wav)
    step = 4 * 1024 * 1024
    off = 0
    while off < meta["size"]:
        res = js(AUDIO_CHUNK_JS % (off, step, name), timeout=FRAME_TIMEOUT * 4)
        if not isinstance(res, dict) or res.get("error"):
            raise SystemExit("FAILED: %s" % ((res or {}).get("error") if isinstance(res, dict) else res))
        off = res["off"] + res["bytes"]
        if res.get("done"):
            break
    js("delete window.__cinecodeWav; 1", timeout=60)
    http_get("http://127.0.0.1:%d/__close?name=%s" % (page.port, name))
    part = os.path.join(page.out, name)
    if not os.path.exists(part):
        raise SystemExit("FAILED: the audio did not arrive")
    shutil.move(part, out_wav)
    secs = meta["n"] / meta["sr"]
    peak_db = (20 * (meta["peak"] ** 0.1 if False else 1)) if False else (
        20 * __import__("math").log10(meta["peak"]) if meta["peak"] > 0 else float("-inf"))
    log("audio: %s (%.3f s, %d Hz, %d ch, 32-bit float, peak %.1f dBFS, %.1f s)" %
        (out_wav, secs, meta["sr"], meta["ch"], peak_db, time.time() - t0))
    film = info["frames"] / float(info["fps"])
    if abs(secs - film) > 1.0 / float(info["fps"]):
        log("WARNING: audio is %.3f s but the picture is %.3f s" % (secs, film))
    if meta["peak"] == 0:
        log("WARNING: the audio is silent")
    return out_wav


# ---------------------------------------------------------------------- encode
def encode(frames_dir, video, fps, crf, maxrate, ext="png", wanted=None):
    """Encode the rendered frames to H.264.

    The frames are named by frame index and may be a sparse subset (previews,
    --frames lists), so they are laid out as a concat list rather than a %06d
    sequence, which would stall at the first gap. `wanted` keeps the requested
    order when the caller asked for a specific frame list.
    """
    have = sorted((f for f in os.listdir(frames_dir) if re.fullmatch(r"\d{6}\.(png|jpe?g)", f)),
                  key=lambda f: int(f.split(".")[0]))
    if wanted:
        order = ["%06d.%s" % (f, ext) for f in wanted]
        have = [n for n in order if n in set(have)]
    if not have:
        raise SystemExit("FAILED: no frames to encode in %s" % frames_dir)
    lst = os.path.join(tempfile.mkdtemp(prefix="cinecode-enc-"), "concat.txt")
    step = 1.0 / float(fps)
    with open(lst, "w", encoding="utf-8") as f:
        for name in have:
            f.write("file '%s'\n" % os.path.join(frames_dir, name))
            f.write("duration %.9f\n" % step)

    vf = "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
    # No trailing frame is repeated and no -r is forced: the concat demuxer's
    # per-file `duration` already spaces the frames exactly one step apart, and a
    # forced output rate would duplicate one to fill the final partial slot.
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", lst,
           "-vf", vf, "-fps_mode", "passthrough", "-c:v", "libx264", "-preset", "slow",
           "-crf", str(crf), "-g", str(int(fps * 2)),
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
    if maxrate and str(maxrate) != "0":
        cmd += ["-maxrate", str(maxrate), "-bufsize", str(maxrate)]
    cmd.append(video)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("FAILED: ffmpeg: %s" % (r.stderr or "")[:400])
    return video


# ------------------------------------------------------------------------ main
def pos_int(text, flag):
    """A non-negative integer, or a clear argument error (never a silent clamp)."""
    try:
        v = int(text, 10)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("%s must be a non-negative integer, got %r" % (flag, text))
    if v < 0:
        raise argparse.ArgumentTypeError("%s must be a non-negative integer, got %r" % (flag, text))
    return v


def pos_float(text, flag):
    try:
        v = float(text)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("%s must be a number, got %r" % (flag, text))
    if v <= 0 or v > 1:
        raise argparse.ArgumentTypeError("%s must be greater than 0 and at most 1, got %r" % (flag, text))
    return v


def frame_list(text):
    return [pos_int(p.strip(), "--frames") for p in (text or "").split(",")]


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--out")
    ap.add_argument("--video")
    ap.add_argument("--audio")
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--text-check", nargs="?", const="0.5")
    ap.add_argument("--frames", type=frame_list)
    ap.add_argument("--start", type=lambda t: pos_int(t, "--start"))
    ap.add_argument("--end", type=lambda t: pos_int(t, "--end"))
    ap.add_argument("--format", default="png", choices=("png", "jpg", "jpeg", "webp"))
    ap.add_argument("--quality", default="0.95")
    ap.add_argument("--params")
    ap.add_argument("--crf", default="17")
    ap.add_argument("--maxrate", default=None)
    ap.add_argument("--workers", type=lambda t: pos_int(t, "--workers"),
                    default=1)   # accepted for CLI compatibility; one page renders at a time
    ap.add_argument("--status")
    ap.add_argument("--fresh", action="store_true")
    a = ap.parse_args()

    # Validate before anything is opened: a bad value must not clear a frame folder
    # that an earlier job filled.
    if a.text_check is not None:
        a.text_check = pos_float(a.text_check, "--text-check")
    if a.quality is not None:
        a.quality = pos_float(a.quality, "--quality")
    if a.format == "webp":
        raise SystemExit("FAILED: --format webp: the WebView cannot export webp; use png or jpeg")
    if a.start is not None and a.end is not None and a.end < a.start:
        raise SystemExit("FAILED: --end is before --start")
    if a.workers is not None and a.workers < 1:
        raise SystemExit("FAILED: --workers must be a positive integer, got %r" % a.workers)

    page_path = a.url
    if page_path.startswith("file://"):
        page_path = page_path[7:]
    if not os.path.exists(page_path):
        raise SystemExit("FAILED: no such page: %s" % page_path)
    page_path = os.path.abspath(page_path)

    out_dir = a.out or (os.path.join(os.path.dirname(page_path), "frames") if a.video else None)
    # A relative --video / --audio resolves against --out when there is one (the
    # same directory the frames go to), else against the current directory.
    def resolve(p):
        if os.path.isabs(p):
            return p
        return os.path.join(out_dir or os.getcwd(), p)
    mime = "image/jpeg" if a.format in ("jpg", "jpeg") else "image/png"
    ext = "jpg" if mime == "image/jpeg" else "png"
    quality = str(a.quality)

    with Server(page_path, out_dir) as srv:
        try:
            info = open_page(srv, a.params)
            if not isinstance(info, dict):
                raise SystemExit("FAILED: the page did not report READY: %r" % (info,))
            info["_fps"] = float(info["fps"])

            if a.probe:
                keys = ("title", "bounds", "vo", "palette", "lookPalette", "families", "sfx")
                meta = {k: info[k] for k in keys if k in info}
                log("renderer: %s" % info.get("renderer", "minis-webview"))
                for line in _as_list(info.get("qc")):
                    log("qc: %s" % line)
                log("page: %dx%d, %d frames @ %s fps" %
                    (info["width"], info["height"], info["frames"], info["fps"]))
                if meta:
                    log("meta: %s" % json.dumps(meta, ensure_ascii=False))
                return 0

            if a.verify:
                return do_verify(srv, a.params)

            if a.text_check is not None:
                return do_text_check(srv, a.params, a.text_check)

            if a.audio:
                do_audio(srv, resolve(a.audio), info)
                if not a.out and not a.video:
                    return 0

            if not a.out and not a.video:
                raise SystemExit("FAILED: missing --out (or --video / --audio)")

            frames = list(range(int(a.start or 0), int(info["frames"]) - 1 + 1))
            if a.end is not None:
                frames = [f for f in frames if f <= int(a.end)]
            if a.frames:
                frames = a.frames
            bad = [f for f in frames if f >= int(info["frames"])]
            if bad:
                raise SystemExit("FAILED: --frames must be below %d" % info["frames"])
            if not frames:
                raise SystemExit("FAILED: empty frame range")

            requested = list(frames)
            skipped = 0
            if out_dir and not a.fresh:
                existing = set(srv.listing())
                keep = [f for f in frames if "%06d.%s" % (f, ext) not in existing]
                skipped = len(frames) - len(keep)
                frames = keep
                if skipped:
                    log("%d skipped (already on disk)" % skipped)

            if a.video:
                # A %06d image sequence stalls at the first gap, so a sparse frame
                # list is encoded from a concat list instead — the video then holds
                # exactly the frames asked for, none interpolated.
                all_on_disk = all("%06d.%s" % (f, ext) in set(srv.listing()) for f in requested)
                if not all_on_disk:
                    if not frames:
                        raise SystemExit("FAILED: every frame in the list is already on disk "
                                         "but the video is missing; re-run with --fresh")
                    render_range(srv.url(), frames, mime, quality, out_dir, a.status, len(frames))
                else:
                    frames = []
                    skipped = len(requested)

            total = len(requested)
            status = {"state": "running", "total": total, "done": total - len(frames),
                      "start": requested[0], "end": requested[-1], "format": ext}
            if a.status:
                write_status(a.status, status)

            t0 = time.time()
            done = len(frames)
            if frames:
                done = render_range(srv.url(), frames, mime, quality, out_dir, a.status,
                                    len(frames))
            secs = time.time() - t0

            if a.video:
                video = resolve(a.video)
                encode(out_dir, video, float(info["fps"]),
                       a.crf, a.maxrate, ext, requested)
                log("video: %s (%d frames @ %s fps, no audio yet)" %
                    (video, total, info["fps"]))

            if a.status:
                write_status(a.status, {"state": "done", "eta_s": 0, "done": done, "total": total,
                                        "seconds": round(secs, 1),
                                        "finished_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                        "video": os.path.abspath(a.video) if a.video else None})
            log("done: %d rendered, %d skipped, %.1f s total, %.2f fps, 1 worker(s)" %
                (done, skipped, secs, done / max(secs, 0.001)))
            if out_dir:
                log("frames: %s/%%06d.%s" % (out_dir, ext))
            return 0
        finally:
            pass


if __name__ == "__main__":
    sys.exit(main() or 0)