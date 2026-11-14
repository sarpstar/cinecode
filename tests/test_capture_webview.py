"""Tests for the WebView renderer (capture_webview.py).

capture.mjs keeps its own suite (test_capture.py), which covers the Chrome/Node
path on machines that have both. These tests cover the port: argument handling
needs no browser, and the render tests run against Minis's built-in WebView when
CINECODE_BROWSER_TESTS=1.

Run:  python3 -m unittest tests.test_capture_webview
      CINECODE_BROWSER_TESTS=1 python3 -m unittest tests.test_capture_webview
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "scripts", "capture_webview.py")
STARTER = os.path.join(ROOT, "starter", "index.html")


def run(args, cwd=ROOT, timeout=300):
    return subprocess.run([sys.executable, SCRIPT, *args], cwd=cwd, capture_output=True, text=True,
                          timeout=timeout)


def frame_names(path):
    """--out names the frame directory itself (make.py globs *.jpg straight out of it)."""
    d = os.path.join(path, "frames") if os.path.isdir(os.path.join(path, "frames")) else path
    return sorted(n for n in os.listdir(d) if n.endswith((".png", ".jpg"))) if os.path.isdir(d) else []


class Arguments(unittest.TestCase):
    """Argument handling: no page is opened, so these always run."""

    def test_help_lists_the_renderer_options(self):
        r = run(["--help"])
        self.assertEqual(r.returncode, 0)
        for flag in ("--url", "--out", "--video", "--audio", "--probe", "--verify", "--text-check", "--frames",
                     "--start", "--end", "--format", "--quality", "--maxrate", "--params", "--status", "--fresh"):
            self.assertIn(flag, r.stdout)

    def test_url_is_required(self):
        self.assertNotEqual(run([]).returncode, 0)

    def test_bad_frame_index_is_rejected_before_the_browser_opens(self):
        for frames in ["abc", "-1", "0,,1", "1.5", ""]:
            with self.subTest(frames=frames):
                r = run(["--url", STARTER, "--out", "frames", "--frames", frames])
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("--frames", r.stderr)

    def test_bad_quality_and_text_check_are_rejected(self):
        for flag, value in [("--quality", "abc"), ("--quality", "2"), ("--quality", "0"),
                            ("--text-check", "x"), ("--text-check", "1.5")]:
            with self.subTest(flag=flag, value=value):
                r = run(["--url", STARTER, flag, value])
                self.assertNotEqual(r.returncode, 0)
                self.assertIn(flag, r.stderr)

    def test_zero_workers_is_rejected(self):
        r = run(["--url", STARTER, "--workers", "0"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--workers", r.stderr)

    def test_reversed_range_is_rejected(self):
        r = run(["--url", STARTER, "--start", "10", "--end", "2"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("--start", r.stderr)

    def test_webp_is_rejected_with_a_reason(self):
        r = run(["--url", STARTER, "--format", "webp"])
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("webp", r.stderr)


@unittest.skipUnless(os.environ.get("CINECODE_BROWSER_TESTS") == "1", "set CINECODE_BROWSER_TESTS=1: these open the WebView")
class Render(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="cinecode-webview-")
        self.addCleanup(shutil.rmtree, self.dir, True)

    def cap(self, extra=(), params="w=320&h=180"):
        return run(["--url", STARTER, "--out", self.dir, "--params", params, *extra])

    def test_probe_names_the_renderer_and_the_frame_count(self):
        r = self.cap(["--probe"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertRegex(r.stdout, r"^renderer: ")
        self.assertRegex(r.stdout, r"page: \d+x\d+, \d+ frames @ [\d.]+ fps")

    def test_one_frame_lands_with_the_right_size(self):
        r = self.cap(["--frames", "0"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("1 rendered, 0 skipped", r.stdout)
        names = frame_names(self.dir)
        self.assertEqual(names, ["000000.png"])
        head = open(os.path.join(self.dir, "000000.png"), "rb").read(33)
        self.assertEqual(head[:8], b"\x89PNG\r\n\x1a\n")
        w = int.from_bytes(head[16:20], "big")
        h = int.from_bytes(head[20:24], "big")
        self.assertEqual((w, h), (320, 180))

    def test_rendered_again_without_fresh_is_skipped(self):
        self.cap(["--frames", "0"])
        self.assertIn("0 rendered, 1 skipped", self.cap(["--frames", "0"]).stdout)

    def test_fresh_redraws(self):
        self.cap(["--frames", "0"])
        self.assertIn("1 rendered, 0 skipped", self.cap(["--frames", "0", "--fresh"]).stdout)

    def test_different_params_render_a_different_frame(self):
        self.cap(["--frames", "0"])
        first = open(os.path.join(self.dir, "000000.png"), "rb").read()
        self.cap(["--frames", "0", "--fresh", "--params", "w=320&h=180&seed=99"])
        second = open(os.path.join(self.dir, "000000.png"), "rb").read()
        self.assertNotEqual(first, second)

    def test_two_frames_differ_from_each_other(self):
        self.cap(["--frames", "0,12"])
        a = open(os.path.join(self.dir, "000000.png"), "rb").read()
        b = open(os.path.join(self.dir, "000012.png"), "rb").read()
        self.assertNotEqual(a, b)

    def test_video_gets_every_frame_even_when_the_list_is_sparse(self):
        # A %06d image sequence would stall at the first gap; the encoder uses a
        # concat list instead, so a preview-sized sample still produces a video.
        r = self.cap(["--frames", "0,6,12,18", "--video", "picture.mp4"], params="w=320&h=180")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.dir, "picture.mp4")))
        out = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                              "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0",
                              os.path.join(self.dir, "picture.mp4")], capture_output=True, text=True)
        self.assertEqual(out.stdout.strip(), "4")

    def test_jpeg_output(self):
        r = self.cap(["--frames", "0", "--format", "jpeg"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(os.path.join(self.dir, "000000.jpg")))

    def test_verify_reports_determinism(self):
        r = self.cap(["--verify"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("deterministic: yes", r.stdout)


@unittest.skipUnless(os.environ.get("CINECODE_BROWSER_TESTS") == "1",
                     "set CINECODE_BROWSER_TESTS=1: these need a film page with a soundtrack")
class Audio(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="cinecode-audio-")
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.page = os.path.join(ROOT, "templates", "quick", "film.html")

    def test_soundtrack_is_written_as_a_wav(self):
        out = os.path.join(self.dir, "film.wav")
        r = run(["--url", self.page, "--audio", out, "--params", "w=320&h=180"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("audio:", r.stdout)
        self.assertGreater(os.path.getsize(out), 8000)


if __name__ == "__main__":
    unittest.main()