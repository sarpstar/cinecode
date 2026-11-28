"""Calm pacing profile (cinecode #19): Tempo: calm for very young children, sleep and ambient films.

One continuous shot per verse, soft dissolves instead of cuts, shots of 7 s or more, one main action at
a time, no flashing, no fast zooms or whip pans, no unscripted silence. The checks are qc.py calm,
scene_check.py action|sound --calm and validate_shots.py --calm (or "tempo": "calm" in shots.json).
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import make
import moves

FFMPEG = shutil.which("ffmpeg") and shutil.which("ffprobe")
CALM_SHOTS = {"title": "Calm sing-along", "fps": 24, "width": 1920, "height": 1080, "shots": [
    {"id": f"s{i + 1}", "start": i * 360, "end": (i + 1) * 360, "description": f"verse {i + 1}",
     "reads": [{"read": "the bear sings", "t": [0, 14]}], "action": "the bear sings the verse",
     "location": "meadow", "camera": {"size": "wide", "lens_mm": 35,
     "move": {"line": "dolly in, 15 s, slow ease-in-out, toward the bear", "type": "move",
              "moving_at_start": False}}}
    for i in range(4)]}


def run(*argv, cwd=None):
    return subprocess.run([sys.executable, *argv], cwd=cwd, capture_output=True, text=True, timeout=120)


class CalmDeck(unittest.TestCase):
    def test_calm_deck_is_slow_dissolves_and_no_big_move(self):
        decks = [moves.deal(6, "calm", f"toddler sing-along {s}", set()) for s in range(5)]
        for deck in decks:
            for d in deck:
                self.assertIn(d["speed"], ("slow", "very slow"))
                self.assertNotIn(d["move"], ("FPV fly-through", "zoom in", "handheld drift"))
                self.assertNotIn(d.get("cut"), ("whip pan", "smash cut", "hard cut"))
                self.assertNotIn("big", d)
        self.assertTrue(any(d.get("cut") == "cross dissolve" for deck in decks for d in deck),
                        "a calm deck should deal dissolves")

    def test_standard_deck_still_gets_its_big_move(self):
        decks = [moves.deal(6, "standard", f"standard {s}", set()) for s in range(5)]
        self.assertTrue(any("big" in d for deck in decks for d in deck))


class CalmTempo(unittest.TestCase):
    def test_make_tempo_calm_is_eight_seconds(self):
        self.assertEqual(make.TEMPO["calm"], 8)

    def test_even_rhythm_is_the_look_for_calm_not_a_fault(self):
        bounds = [0, 8, 16, 24, 32, 40, 48]
        self.assertNotIn("EVEN RHYTHM", make.rhythm_line(bounds, "**Tempo:** calm, about 8 s a shot"))
        self.assertIn("EVEN RHYTHM", make.rhythm_line(bounds, "**Tempo:** standard, about 6 s a shot"))

    def test_calm_still_flags_scenes_far_over_its_tempo(self):
        self.assertIn("TEMPO:", make.rhythm_line([0, 16, 32, 48, 64, 80, 96], "**Tempo:** calm"))


class CalmShots(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cinecode-calm-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)
        (self.path / "shots.json").write_text(json.dumps(CALM_SHOTS), encoding="utf-8")

    def test_same_shots_fail_default_and_pass_calm(self):
        script = str(ROOT / "scripts" / "validate_shots.py")
        default = run(script, str(self.path / "shots.json"))
        self.assertEqual(default.returncode, 1, default.stdout)
        self.assertIn("HOOK RULE", default.stdout)
        self.assertIn("repeats the framing", default.stdout)
        calm = run(script, str(self.path / "shots.json"), "--calm")
        self.assertEqual(calm.returncode, 0, calm.stdout)
        self.assertIn("0 error(s)", calm.stdout)

    def test_tempo_in_the_file_is_enough(self):
        film = dict(CALM_SHOTS, tempo="calm")
        (self.path / "shots.json").write_text(json.dumps(film), encoding="utf-8")
        r = run(str(ROOT / "scripts" / "validate_shots.py"), str(self.path / "shots.json"))
        self.assertEqual(r.returncode, 0, r.stdout)


@unittest.skipUnless(FFMPEG, "needs ffmpeg")
class CalmVideo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="cinecode-calm-video-")
        cls.dir = Path(cls.temp.name)
        ff = ["ffmpeg", "-v", "error", "-y"]
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=duration=16:size=64x36:rate=24",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dir / "pass.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=duration=3:size=64x36:rate=24",
                             "-f", "lavfi", "-i", "testsrc2=duration=13:size=64x36:rate=24",
                             "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dir / "short.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=duration=16:size=64x36:rate=24",
                             "-vf", "drawbox=x=0:y=0:w=iw:h=ih:color=white:t=fill:enable='eq(n,192)'",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dir / "flash.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "color=c=red:duration=8:size=64x36:rate=24",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dir / "still.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc=duration=1:size=256x36:rate=24",
                             "-frames:v", "1", str(cls.dir / "still.png")], check=True)
        subprocess.run(ff + ["-loop", "1", "-i", str(cls.dir / "still.png"),
                             "-vf", "crop=64:36:'(256-64)*t/16':0", "-t", "16",
                             "-c:v", "libx264", "-pix_fmt", "yuv420p", str(cls.dir / "pan.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "sine=frequency=440:duration=2",
                             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono:duration=2",
                             "-f", "lavfi", "-i", "sine=frequency=440:duration=4",
                             "-filter_complex", "[0:a][1:a][2:a]concat=n=3:v=0:a=1",
                             "-c:a", "aac", str(cls.dir / "gap.m4a")], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_qc_calm_passes_a_long_moving_shot(self):
        r = run(str(ROOT / "scripts" / "qc.py"), "calm", str(self.dir / "pass.mp4"))
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("calm: PASS", r.stdout)

    def test_qc_calm_flags_a_shot_under_seven_seconds(self):
        r = run(str(ROOT / "scripts" / "qc.py"), "calm", str(self.dir / "short.mp4"))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("under 7 s", r.stdout)

    def test_qc_calm_flags_a_one_frame_flash(self):
        r = run(str(ROOT / "scripts" / "qc.py"), "calm", str(self.dir / "flash.mp4"), "0")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("one-frame pops", r.stdout)
        self.assertIn(": 1", r.stdout)

    def test_qc_calm_fails_a_still_open(self):
        r = run(str(ROOT / "scripts" / "qc.py"), "calm", str(self.dir / "still.mp4"))
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL", r.stdout)

    def test_action_calm_lets_a_slow_camera_move_carry_the_scene(self):
        script = str(ROOT / "scripts" / "scene_check.py")
        default = run(script, "action", str(self.dir / "pan.mp4"))
        self.assertEqual(default.returncode, 1, default.stdout)
        self.assertIn("camera-led", default.stdout)
        calm = run(script, "action", str(self.dir / "pan.mp4"), "--calm")
        self.assertEqual(calm.returncode, 0, calm.stdout)

    def test_sound_calm_flags_a_silent_scene(self):
        script = str(ROOT / "scripts" / "scene_check.py")
        default = run(script, "sound", str(self.dir / "gap.m4a"))
        self.assertEqual(default.returncode, 0, default.stdout)
        self.assertIn("silent: scripted?", default.stdout)
        calm = run(script, "sound", str(self.dir / "gap.m4a"), "--calm")
        self.assertEqual(calm.returncode, 1, calm.stdout)
        self.assertIn("1 scene(s) flagged", calm.stdout)


if __name__ == "__main__":
    unittest.main()
