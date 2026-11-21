"""Regression checks for project safety, local references, narration and metadata."""
import contextlib
import io
import json
import os
import tempfile

os.environ["CINECODE_VIEWER_WAIT"] = "0"   # a final never waits for a viewer in tests
os.environ["CINECODE_NO_OPEN"] = "1"   # boards and drafts never pop up during tests
os.environ["CINECODE_SHOWN"] = os.path.join(tempfile.gettempdir(), "cinecode-test-shown.json")
os.environ["CINECODE_SHOWN_MUSIC"] = os.path.join(tempfile.gettempdir(), "cinecode-test-music.json")
os.environ["CINECODE_SHOWN_SOUNDS"] = os.path.join(tempfile.gettempdir(), "cinecode-test-sounds.json")
os.environ["CINECODE_SOUNDS_CACHE"] = os.path.join(tempfile.gettempdir(), "cinecode-test-sound-cache")
os.environ["CINECODE_SAMPLES_CACHE"] = os.path.join(tempfile.gettempdir(), "cinecode-test-samples")
from pathlib import Path
import shutil
import subprocess
import sys
import unittest
import urllib.parse
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import asset_search
import captions
import keys
import tts


class Tools(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cinecode-tools-")
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "needs ffmpeg")
    def test_a_wildcard_reaches_python_as_it_is_and_still_finds_the_pictures(self):
        refs = self.path / "refs"
        refs.mkdir()
        subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=c=orange:s=64x36", "-frames:v", "1",
                        str(refs / "a.png")], check=True)
        (refs / "notes.txt").write_text("why these pictures", encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "direction.py"), "measure", "refs/*.*", "--out", "m"],
                           cwd=self.path, capture_output=True, text=True)       # as PowerShell hands it over: unexpanded
        self.assertEqual(r.returncode, 0, r.stderr[-400:])
        self.assertIn("passed over: " + os.path.join("refs", "notes.txt"), r.stdout)
        self.assertIn("1 stills", r.stdout)
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "direction.py"), "measure", "nowhere/*.png", "--out", "m"],
                           cwd=self.path, capture_output=True, text=True)
        self.assertIn("nothing matches nowhere/*.png", r.stderr)

    def test_turkish_case_matching(self):
        self.assertEqual(captions.stem("IŞIK"), captions.stem("ışık"))
        self.assertEqual(captions.stem("İZMİR"), captions.stem("izmir"))

    def test_key_file_comments_are_not_keys(self):
        p = self.path / "keys.env"
        p.write_text('EMPTY= # comment\nTOKEN=synthetic # note\nQUOTED="synthetic"\n', encoding="utf-8")
        self.assertEqual(keys.read_env(str(p)), {"EMPTY": "", "TOKEN": "synthetic", "QUOTED": "synthetic"})

    def test_local_thumbnail_is_read_without_download(self):
        p = self.path / "own.png"
        p.write_bytes(b"local image fixture")
        with patch.object(asset_search, "get") as download, patch.object(asset_search.subprocess, "run"), contextlib.redirect_stdout(io.StringIO()):
            sheet = asset_search.contact_sheet([{"n": 1, "thumb": str(p)}], str(self.path / "board"))
        download.assert_not_called()
        self.assertIsNotNone(sheet)
        self.assertEqual((self.path / "board/thumbs/01.img").read_bytes(), p.read_bytes())

    def test_failed_thumbnail_download_keeps_previous_bytes(self):
        p = self.path / "board/thumbs/01.img"
        p.parent.mkdir(parents=True)
        p.write_bytes(b"previous image")
        with patch.object(asset_search, "get", side_effect=RuntimeError("synthetic HTTP failure")), contextlib.redirect_stdout(io.StringIO()):
            result = asset_search.contact_sheet([{"n": 1, "thumb": "https://example.invalid/changed.png"}], str(self.path / "board"))
        self.assertIsNone(result)
        self.assertEqual(p.read_bytes(), b"previous image")

    def test_wikimedia_license_version(self):
        data = {"query": {"pages": {"1": {"index": 1, "pageid": 1, "title": "File:Test", "imageinfo": [{
            "descriptionurl": "https://example.invalid/item", "url": "https://example.invalid/full.jpg",
            "thumburl": "https://example.invalid/thumb.jpg", "extmetadata": {
                "LicenseShortName": {"value": "CC BY 2.0"}, "Artist": {"value": "Test author"}}}]}}}}
        with patch.object(asset_search, "get", return_value=data):
            record = asset_search.src_wikimedia("test", 1, "image")[0]
        self.assertEqual(record["licence_url"], "https://creativecommons.org/licenses/by/2.0/")

    def test_music_searches_audio_and_the_archive_keeps_only_open_licences(self):
        seen = []
        def fake(url, as_json=True):
            seen.append(url)
            if "advancedsearch" in url:
                return {"response": {"docs": [
                    {"identifier": "ok-by", "title": "Taksim", "creator": "A", "licenseurl": "https://creativecommons.org/licenses/by/4.0/"},
                    {"identifier": "nc", "title": "No", "creator": "B", "licenseurl": "http://creativecommons.org/licenses/by-nc/3.0/"},
                    {"identifier": "nd", "title": "No", "creator": "C", "licenseurl": "https://creativecommons.org/licenses/by-nd/4.0/"},
                    {"identifier": "ok-pd", "title": "78 rpm", "creator": ["D"], "licenseurl": "http://creativecommons.org/publicdomain/mark/1.0/"}]}}
            if "/metadata/" in url:
                return {"files": [{"name": "track one.mp3", "format": "VBR MP3"}]}
            return {"query": {"pages": {}}}
        with patch.object(asset_search, "get", side_effect=fake):
            got = asset_search.src_archive("taksim", 3, "music")
            asset_search.src_wikimedia("oud", 2, "music")
        self.assertEqual([(r["id"], r["licence"]) for r in got], [("ok-by", "cc-by"), ("ok-pd", "pd")])
        self.assertEqual(got[0]["file"], "https://archive.org/download/ok-by/track%20one.mp3")
        query = next(urllib.parse.unquote_plus(u) for u in seen if "advancedsearch" in u)
        self.assertIn("collection:(jamendo-albums OR netlabels)", query, "music comes from released tracks, not radio shows")
        self.assertIn(r"licenseurl:(*\/licenses\/by\/* OR *publicdomain*)", query, "only usable licences are asked for")
        self.assertIn("filetype%3Aaudio", seen[-1])
        self.assertEqual(asset_search.src_archive("x", 3, "image"), [])

    def test_a_search_asks_its_sources_side_by_side_and_rests_one_that_did_not_answer(self):
        import time, types
        calls = []
        def slow(q, n, kind):
            calls.append("slow")
            time.sleep(0.6)
            raise TimeoutError("over its time")
        def fast(q, n, kind):
            calls.append("fast")
            time.sleep(0.6)
            return [asset_search.rec("fast", 1, "Track", "A", "cc-by", "https://p", "https://f.mp3", None, "music")]
        a = types.SimpleNamespace(q="epic", n=3, type="music", sources=None, licence=None, out=str(self.path / "m"),
                                  max_wait=None, patient=False, purpose="cinematic")
        with patch.dict(asset_search.SOURCES, {"fast": fast, "slow": slow}), \
                patch.dict(asset_search.DEFAULT, {"music": "fast,slow"}), \
                patch.object(asset_search, "CACHE", str(self.path / "cache")), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            started = time.time()
            asset_search.search(a)
            first = time.time() - started
            asset_search.search(a)
            asset_search.search(types.SimpleNamespace(**dict(vars(a), sources="fast,slow")))
        self.assertLess(first, 1.1, "two 0.6 s sources asked side by side take about 0.6 s, not 1.2 s")
        self.assertEqual(calls.count("slow"), 2, "a source that did not answer sits out the next default search, "
                                                 "and is asked again when named with --sources")
        self.assertIn("asked again from", out.getvalue())
        self.assertEqual(json.loads((self.path / "m" / "results.json").read_text())["results"][0]["title"], "Track")
        self.assertIn("openverse", asset_search.DEFAULT["music"])
        waits = []
        def thumb(url, as_json=True):
            waits.append(asset_search.wait_cap())
            raise TimeoutError("over its time")
        pic = lambda q, n, kind: [asset_search.rec("fast", 2, "Pier", "B", "cc0", "https://p", "https://f.jpg",
                                                   "https://t.jpg", "image")]
        with patch.dict(asset_search.SOURCES, {"pic": pic}), patch.object(asset_search, "get", side_effect=thumb), \
                patch.object(asset_search, "CACHE", str(self.path / "cache")), contextlib.redirect_stdout(io.StringIO()):
            asset_search.search(types.SimpleNamespace(**dict(vars(a), type="image", sources="pic", out=str(self.path / "i"))))
        self.assertEqual(waits, [20], "a stalled thumbnail gets one short try, not the long default with a retry")

    def test_pixabay_brings_real_stock_video_and_photos_with_their_licence(self):
        store = self.path / "keys.env"
        store.write_text("PIXABAY_API_KEY=synthetic\n", encoding="utf-8")
        seen = []
        def fake(url, as_json=True):
            seen.append(url)
            if "/api/videos/" in url:
                clip = lambda i, w: {"url": f"https://cdn.example/{i}-{w}.mp4", "width": w, "thumbnail": f"https://cdn.example/{i}-{w}.jpg"}
                return {"hits": [
                    {"id": 1, "pageURL": "https://pixabay.com/videos/id-1/", "tags": "city, traffic, night", "user": "Ann",
                     "duration": 12, "videos": {"large": clip(1, 3840), "medium": clip(1, 1920), "tiny": clip(1, 640)}},
                    {"id": 2, "pageURL": "u", "tags": "city, traffic, ai generated", "user": "B", "videos": {"medium": clip(2, 1280)}},
                    {"id": 3, "pageURL": "u", "tags": "forest, birds", "user": "C", "videos": {"medium": clip(3, 1280)}},
                    {"id": 4, "pageURL": "u", "tags": "city, traffic, cartoon", "user": "D", "videos": {"medium": clip(4, 1280)}}]}
            return {"hits": [{"id": 9, "pageURL": "https://pixabay.com/photos/id-9/", "tags": "courthouse, columns", "user": "E",
                              "largeImageURL": "https://cdn.example/9-large.jpg", "webformatURL": "https://cdn.example/9-web.jpg"}]}
        env = {k: v for k, v in os.environ.items() if k != "PIXABAY_API_KEY"}
        with patch.dict(os.environ, dict(env, CINECODE_KEYS=str(store)), clear=True), \
                patch.object(asset_search, "get", side_effect=fake):
            videos = asset_search.src_pixabay("city traffic night", 5, "video")
            photos = asset_search.src_pixabay("courthouse", 5, "image")
        self.assertEqual([r["id"] for r in videos], ["1"], "off-subject, AI-generated and cartoon hits are left out")
        self.assertEqual((videos[0]["file"], videos[0]["thumb"], videos[0]["type"], videos[0]["duration"], videos[0]["licence"]),
                         ("https://cdn.example/1-1920.mp4", "https://cdn.example/1-640.jpg", "video", 12, "pixabay"))
        self.assertIn("video_type=film", seen[0])
        self.assertIn("safesearch=true", seen[0])
        self.assertIn("image_type=photo", seen[1])
        self.assertEqual(photos[0]["file"], "https://cdn.example/9-large.jpg")
        self.assertIn("on Pixabay (Pixabay Content License)", photos[0]["attribution"])
        with patch.dict(os.environ, dict(env, CINECODE_KEYS=str(self.path / "none.env")), clear=True), \
                patch.object(asset_search, "get", side_effect=fake):
            with self.assertRaisesRegex(RuntimeError, "keys.py open PIXABAY_API_KEY"):
                asset_search.src_pixabay("city", 3, "video")
        self.assertEqual(asset_search.src_pixabay("rain", 3, "sound"), [])
        self.assertIn("pixabay", asset_search.DEFAULT["video"])
        self.assertIn("PIXABAY_API_KEY", keys.KNOWN)

    def test_museum_sources_give_film_sized_open_files(self):
        en, pdm = "http://vocab.getty.edu/aat/300388277", "https://creativecommons.org/publicdomain/mark/1.0/"
        def obj(number, licence):
            return {"identified_by": [{"type": "Identifier", "content": number},
                                      {"type": "Name", "content": "Gezicht op een haven", "language": [{"id": "nl"}]},
                                      {"type": "Name", "content": "View of a Harbour", "language": [{"id": en}]}],
                    "produced_by": {"referred_to_by": [{"content": "Josua de Grave", "language": [{"id": en}]}]},
                    "subject_of": [{"digitally_carried_by": [{"access_point": [{"id": "https://iiif.micr.io/abc/full/max/0/default.jpg"}],
                                                              "referred_to_by": [{"content": licence}]}]}]}
        def fake(url, as_json=True):
            if "artic.edu" in url:
                return {"config": {"iiif_url": "https://www.artic.edu/iiif/2"}, "data": [
                    {"id": 1, "title": "Harbour", "artist_display": "A\nB", "image_id": "i1", "is_public_domain": True,
                     "thumbnail": {"width": 4200, "height": 2100}},
                    {"id": 2, "title": "Small", "artist_display": "C", "image_id": "i2", "is_public_domain": True,
                     "thumbnail": {"width": 1200, "height": 900}},
                    {"id": 3, "title": "Unknown size", "artist_display": "D", "image_id": "i3", "is_public_domain": True}]}
            if "clevelandart" in url:
                return {"data": [
                    {"id": 7, "title": "Harbour", "share_license_status": "CC0", "url": "https://clevelandart.org/art/7",
                     "creators": [{"description": "Fitz Henry Lane"}],
                     "images": {"web": {"url": "https://cdn/7_web.jpg"}, "print": {"url": "https://cdn/7_print.jpg"}}},
                    {"id": 8, "title": "Copyrighted", "share_license_status": "Copyrighted",
                     "images": {"web": {"url": "https://cdn/8_web.jpg"}}}]}
            if "search/collection" in url:
                return {"orderedItems": [{"id": "https://evil.example/1"}, {"id": "https://id.rijksmuseum.nl/1"},
                                         {"id": "https://id.rijksmuseum.nl/2"}]}
            if url == "https://id.rijksmuseum.nl/1":
                return obj("SK-A-1", pdm)
            if url == "https://id.rijksmuseum.nl/2":
                return obj("SK-A-2", "In copyright")
            raise AssertionError(f"unexpected request {url}")
        with patch.object(asset_search, "get", side_effect=fake):
            aic = asset_search.src_aic("harbour", 5, "image")
            cle = asset_search.src_cleveland("harbour", 5, "image")
            rijks = asset_search.src_rijks("harbour", 5, "image")
        self.assertEqual([r["file"].split("/full/")[1] for r in aic],
                         ["3000,/0/default.jpg", "1200,/0/default.jpg", "843,/0/default.jpg"],
                         "AIC files come at the original's size up to 3000 px, never upscaled")
        self.assertEqual([(r["id"], r["file"], r["licence"]) for r in cle], [("7", "https://cdn/7_print.jpg", "cc0")])
        self.assertEqual(len(rijks), 1, "a copyrighted object and an id off the museum's host are passed over")
        self.assertEqual((rijks[0]["id"], rijks[0]["title"], rijks[0]["creator"], rijks[0]["licence"]),
                         ("SK-A-1", "View of a Harbour", "Josua de Grave", "pd"))
        self.assertEqual(rijks[0]["file"], "https://iiif.micr.io/abc/full/!3400,3400/0/default.jpg")
        self.assertEqual(rijks[0]["page"], "https://www.rijksmuseum.nl/en/collection/SK-A-1")
        self.assertIn("cleveland", asset_search.DEFAULT["image"])
        self.assertEqual(asset_search.SOURCE_NAME["rijks"], "Rijksmuseum")

    def test_wikimedia_and_the_archive_search_films_too(self):
        seen = []
        def fake(url, as_json=True):
            seen.append(url)
            if "advancedsearch" in url:
                return {"response": {"docs": [
                    {"identifier": "city-1950", "title": "A City", "creator": "X", "licenseurl": "http://creativecommons.org/publicdomain/mark/1.0/"},
                    {"identifier": "nc-film", "title": "No", "creator": "Y", "licenseurl": "https://creativecommons.org/licenses/by-nc/4.0/"}]}}
            if "/metadata/" in url:
                return {"files": [{"name": "a city.ogv", "format": "Ogg Video"}, {"name": "a city.mp4", "format": "h.264"}]}
            return {"query": {"pages": {}}}
        with patch.object(asset_search, "get", side_effect=fake):
            films = asset_search.src_archive("city street", 3, "video")
            asset_search.src_wikimedia("ocean waves", 2, "video")
        self.assertIn("mediatype%3A%28movies%29", seen[0])
        self.assertEqual([(r["id"], r["licence"], r["type"]) for r in films], [("city-1950", "pd", "video")])
        self.assertEqual(films[0]["file"], "https://archive.org/download/city-1950/a%20city.mp4")
        self.assertEqual(films[0]["thumb"], "https://archive.org/services/img/city-1950")
        self.assertIn("filetype%3Avideo", seen[-1])

    def test_a_fetched_stock_clip_is_logged_and_credited(self):
        import argparse
        import make
        results = self.path / "results.json"
        results.write_text(json.dumps({"results": [{"n": 1, "source": "pixabay", "id": "1", "title": "city, traffic, night",
            "creator": "Ann", "licence": "pixabay", "page": "https://pixabay.com/videos/id-1/",
            "file": "https://cdn.example/1-1920.mp4", "thumb": None, "type": "video",
            "licence_url": asset_search.LIC_URL["pixabay"],
            "attribution": '"city, traffic, night" by Ann on Pixabay (Pixabay Content License)'}]}), encoding="utf-8")
        class Reply(io.BytesIO):
            def __enter__(self): return self
            def __exit__(self, *a): return False
        args = argparse.Namespace(results=str(results), pick="1", dest=str(self.path / "assets" / "video"),
                                  licenses=str(self.path / "LICENSES.csv"), variant=None, preview=None)
        with patch.object(asset_search.urllib.request, "urlopen", return_value=Reply(b"clip")), \
                contextlib.redirect_stdout(io.StringIO()):
            asset_search.fetch(args)
        row = (self.path / "LICENSES.csv").read_text(encoding="utf-8")
        self.assertIn("pixabay,https://pixabay.com/service/license-summary/", row)
        self.assertEqual(len(list((self.path / "assets" / "video").glob("pixabay-1-*.mp4"))), 1)
        with patch.object(make, "PROJECT", self.path):
            make.credits_file("Film", "")
        self.assertIn('"city, traffic, night" by Ann on Pixabay (Pixabay Content License)',
                      (self.path / "Film-credits.txt").read_text(encoding="utf-8"))

    def test_stills_names_a_missing_page_and_the_film_option(self):
        import argparse
        import make
        a = argparse.Namespace(film="film.html", size=None, at=None, workers="2")
        out = io.StringIO()
        with patch.object(make, "PROJECT", self.path), patch.object(make, "LOGS", self.path / "logs"), \
                contextlib.redirect_stdout(out), self.assertRaises(SystemExit) as stop:
            make.stills(a)
        self.assertEqual(stop.exception.code, 2)
        self.assertIn("FAILED: no film.html", out.getvalue())
        self.assertIn("--film PATH", out.getvalue())

    def test_check_accepts_the_film_option(self):
        out = subprocess.run([sys.executable, str(ROOT / "scripts/make.py"), "check", "--help"],
                             capture_output=True, text=True, timeout=30)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("--film", out.stdout)

    def test_a_short_wait_skips_a_stalled_source_cleanly(self):
        import socket, urllib.error
        asset_search.MAX_WAIT[0] = 0.5
        try:
            with patch("urllib.request.urlopen", side_effect=urllib.error.URLError(socket.timeout("timed out"))), \
                    patch.object(asset_search, "CACHE", str(self.path / "cache")):
                with self.assertRaises(TimeoutError):           # a stall now surfaces as TimeoutError so the source funcs keep the hits already collected
                    asset_search.get("https://api.openverse.org/v1/audio/?q=x")
        finally:
            asset_search.MAX_WAIT[0] = None

    def test_tts_failure_preserves_previous_take_and_success_replaces_it(self):
        p = self.path / "VO1.wav"
        p.write_bytes(b"previous take")
        def fail(data, target):
            Path(target).write_bytes(b"partial output")
            raise RuntimeError("synthetic decoder failure")
        def succeed(data, target):
            Path(target).write_bytes(b"complete new take")
            return 1.0
        argv = ["tts.py", "--engine", "elevenlabs", "--voice", "test", "--text", "test", "--out", str(self.path)]
        with patch.object(sys, "argv", argv), patch.object(tts.keys, "get", return_value="synthetic-not-a-key"), patch.object(tts, "post", return_value=(b"test", "audio/test")), contextlib.redirect_stdout(io.StringIO()):
            with patch.object(tts, "to_wav", side_effect=fail):
                with self.assertRaises(SystemExit):
                    tts.main()
            self.assertEqual(p.read_bytes(), b"previous take")
            self.assertFalse((self.path / ".VO1.new.wav").exists())
            with patch.object(tts, "to_wav", side_effect=succeed):
                tts.main()
        self.assertEqual(p.read_bytes(), b"complete new take")

    def test_text_outside_shot_is_rejected(self):
        data = json.loads((ROOT / "templates/shots.example.json").read_text(encoding="utf-8"))
        data["shots"][0]["text_on_screen"] = [{"text": "Never visible", "t": [100, 104]}]
        p = self.path / "shots.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        result = subprocess.run([sys.executable, str(ROOT / "scripts/validate_shots.py"), str(p)], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside", result.stdout)

    @unittest.skipUnless(shutil.which("git"), "Git is required")
    def test_snapshot_removes_unicode_media_and_preserves_text(self):
        subprocess.run(["git", "init", "-q"], cwd=self.path, check=True)
        for name in ["photo.png", "ışık.png", "notlar.md"]:
            (self.path / name).write_bytes(b"fixture")
        subprocess.run(["git", "add", "."], cwd=self.path, check=True)
        cmd = [sys.executable, str(ROOT / "scripts/snapshot.py"), "test"]
        r = subprocess.run(cmd, cwd=self.path, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        result = subprocess.run(["git", "ls-files", "-z"], cwd=self.path, capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, "notlar.md\0")
        result = subprocess.run(cmd, cwd=self.path, capture_output=True, text=True, check=True)
        self.assertIn("nothing changed", result.stdout)

    @unittest.skipUnless(shutil.which("git"), "Git is required")
    def test_snapshot_skips_parent_repository(self):
        subprocess.run(["git", "init", "-q"], cwd=self.path, check=True)
        (self.path / "unrelated.txt").write_text("fixture", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.path, check=True)
        index = self.path / ".git/index"
        before = index.read_bytes()
        child = self.path / "film"
        child.mkdir()
        result = subprocess.run([sys.executable, str(ROOT / "scripts/snapshot.py"), "test"], cwd=child, capture_output=True, text=True, check=True)
        self.assertIn("skipped", result.stdout)
        self.assertEqual(index.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
