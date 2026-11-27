"""Cue-file clock regressions (starter/timing.js). Standard library only.

The assertions live in JavaScript and run under Node, because the clock is
plain JS with no DOM; this file only drives it and checks it exits cleanly.
"""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
NODE = os.environ.get("CINECODE_NODE") or shutil.which("node")
TIMING = ROOT / "starter" / "timing.js"

CASES = r"""
const assert = require('node:assert/strict');
const { createClock } = require(process.env.CINECODE_TIMING);

const cues = { bpm: 120, sections: [
  { name: 'intro', bar: 0 }, { name: 'verse', bar: 8 }, { name: 'chorus', bar: 24 },
], lines: [{ text: 'first line', bar: 8, beat: 0 }] };
const clock = createClock(cues);
// 120 BPM, 4 beats a bar: a beat is 0.5 s, a bar 2 s; picture leads by 45 ms.
assert.equal(clock.beat(0), -0.045);
assert.equal(clock.beat(1), 0.455);
assert.equal(clock.bar(0), -0.045);
assert.equal(clock.bar(1), 1.955);
assert.equal(clock.bar(8), 15.955);
assert.equal(clock.section('verse'), 15.955);
assert.equal(clock.section('chorus'), 47.955);
assert.equal(clock.at('verse', 2), 16.955);
assert.equal(clock.at('chorus', 0.5), 48.205);
assert.equal(clock.sectionAt(-1), null);
assert.equal(clock.sectionAt(0), 'intro');
assert.equal(clock.sectionAt(16), 'verse');
assert.equal(clock.sectionAt(100), 'chorus');
assert.deepEqual(clock.sectionNames(), ['intro', 'verse', 'chorus']);
// Lyric lines appear 130 ms before the first word.
assert.equal(clock.lineTime({ bar: 8, beat: 0 }), 15.87);
assert.equal(clock.lineTime({ time: 10 }), 9.87);

// 6/8 read as three beats a bar: a bar is 1.5 s at 120 BPM.
const sixEight = createClock({ bpm: 120, beatsPerBar: 3 });
assert.equal(sixEight.bar(1), 1.455);
assert.equal(sixEight.beat(3), 1.455);

// Leads are off when the take says so.
const noLead = createClock({ bpm: 120, pictureLeadMs: 0, lyricLeadMs: 0 });
assert.equal(noLead.beat(0), 0);
assert.equal(noLead.lineTime({ bar: 0, beat: 0 }), 0);

// A measured bars table rules inside its range; past it the last bar
// length carries on, so the grid never jumps.
const tabled = createClock({ bpm: 120, bars: [0, 2, 4] });
assert.equal(tabled.bar(0), -0.045);
assert.equal(tabled.bar(1), 1.955);
assert.equal(tabled.bar(2), 3.955);
assert.equal(tabled.beat(5), 2.455);
assert.equal(tabled.bar(3), 5.955);

// Bad cue files fail plainly instead of mis-timing a render.
for (const bad of [
  {}, { bpm: 0 }, { bpm: -120 }, { bpm: '120' },
  { bpm: 120, beatsPerBar: 0 }, { bpm: 120, beatsPerBar: 2.5 },
  { bpm: 120, sections: [{ name: 'a', bar: 0 }, { name: 'a', bar: 4 }] },
  { bpm: 120, sections: [{ name: 'a', bar: -1 }] },
  { bpm: 120, bars: [0, 2, 2] }, { bpm: 120, bars: [] },
  { bpm: 120, lines: [{ text: 'x', bar: 0 }] },
]) {
  assert.throws(() => createClock(bad), /timing:/, JSON.stringify(bad));
}
const named = createClock({ bpm: 120, sections: [{ name: 'a', bar: 0 }] });
assert.throws(() => named.section('b'), /no section named "b"/);
assert.throws(() => named.at('b', 0), /no section named "b"/);
assert.throws(() => named.beat(-1), /before beat 0/);
assert.throws(() => named.lineTime({ bar: 0, beat: -1 }), /line needs/);

console.log('timing cases OK');
"""


@unittest.skipUnless(NODE, "Node.js is required")
class TimingClock(unittest.TestCase):
    def test_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            case = Path(tmp) / "timing_cases.cjs"
            case.write_text(CASES, encoding="utf-8")
            env = dict(os.environ, CINECODE_TIMING=str(TIMING))
            result = subprocess.run([NODE, str(case)], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("timing cases OK", result.stdout)
