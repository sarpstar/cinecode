// Cue-file clock for music videos (dependency-free: Node 22+ built-ins only, no DOM).
//
// A cue file (audio/cues.json, one per take) says where the song's sections and
// bars fall in film time. The page reads only that file, so a new take means a
// new cue file and the choreography — written as section + beat — never changes.
// See references/music-video.md §5 for the format and the workflow.
//
// Cue file shape (all times in film seconds; film time 0 is a downbeat):
//   {
//     "bpm": 120,                 // required: the tempo the grid is cut to
//     "beatsPerBar": 4,           // optional, default 4 (3 for a 6/8 read as 3, or a waltz)
//     "beat0": 0,                 // optional, default 0: film time of beat 0
//     "pictureLeadMs": 45,        // optional, default 45: the picture leads the beat by this much
//     "lyricLeadMs": 130,         // optional, default 130: on-screen lyric lines appear this early
//     "sections": [               // optional: the song's chapters, in order
//       { "name": "verse", "bar": 8 }, { "name": "chorus", "bar": 24 }
//     ],
//     "bars": [0, 1.9, 3.8],      // optional: measured bar-start times (beat_grid.py --json,
//                                  // or an outside beat analysis); beats inside a bar interpolate
//     "lines": [                  // optional: lyric lines, for on-screen type
//       { "text": "...", "bar": 8, "beat": 0 }
//     ]
//   }
//
// All times this clock returns are PICTURE times: the grid time minus
// pictureLeadMs, because the picture leads the beat (a hit placed exactly on
// the beat reads late). The music itself still plays on the grid.
// Bar and beat numbers are 0-based, matching film.html's bar(n)/beat(n):
// bar(0) is the first bar, beat(0) the first beat.

function fail(msg) { throw new Error('timing: ' + msg); }

function isNum(v) { return typeof v === 'number' && Number.isFinite(v); }

function checkCues(c) {
  if (!c || typeof c !== 'object' || Array.isArray(c)) fail('cue file must be an object');
  if (!isNum(c.bpm) || c.bpm <= 0) fail('bpm must be a number above 0');
  const bpb = c.beatsPerBar === undefined ? 4 : c.beatsPerBar;
  if (!Number.isInteger(bpb) || bpb < 1) fail('beatsPerBar must be a whole number of 1 or more');
  const beat0 = c.beat0 === undefined ? 0 : c.beat0;
  if (!isNum(beat0)) fail('beat0 must be a number');
  for (const k of ['pictureLeadMs', 'lyricLeadMs']) {
    if (c[k] !== undefined && (!isNum(c[k]) || c[k] < 0)) fail(k + ' must be a number of 0 or more');
  }
  const sections = c.sections === undefined ? [] : c.sections;
  if (!Array.isArray(sections)) fail('sections must be a list');
  const names = new Set();
  for (const s of sections) {
    if (!s || typeof s !== 'object' || typeof s.name !== 'string' || !s.name) fail('each section needs a name');
    if (names.has(s.name)) fail('section "' + s.name + '" is listed twice');
    names.add(s.name);
    if (!Number.isInteger(s.bar) || s.bar < 0) fail('section "' + s.name + '" needs a whole bar of 0 or more');
  }
  const bars = c.bars === undefined ? null : c.bars;
  if (bars !== null) {
    if (!Array.isArray(bars) || bars.length === 0 || !bars.every(isNum)) fail('bars must be a non-empty list of times');
    for (let i = 1; i < bars.length; i++) if (!(bars[i] > bars[i - 1])) fail('bars must rise, bar ' + i + ' does not');
  }
  const lines = c.lines === undefined ? [] : c.lines;
  if (!Array.isArray(lines)) fail('lines must be a list');
  for (const l of lines) {
    if (!l || typeof l !== 'object' || typeof l.text !== 'string') fail('each line needs text');
    if (!Number.isInteger(l.bar) || l.bar < 0 || !isNum(l.beat) || l.beat < 0) {
      fail('line "' + l.text.slice(0, 30) + '" needs a whole bar and a beat of 0 or more');
    }
  }
  return { bpm: c.bpm, beatsPerBar: bpb, beat0,
           pictureLeadMs: c.pictureLeadMs === undefined ? 45 : c.pictureLeadMs,
           lyricLeadMs: c.lyricLeadMs === undefined ? 130 : c.lyricLeadMs,
           sections, bars, lines };
}

function createClock(cues) {
  const c = checkCues(cues);
  const beatLen = 60 / c.bpm;
  const barLen = beatLen * c.beatsPerBar;
  const lead = c.pictureLeadMs / 1000;
  const sectionByName = new Map(c.sections.map((s) => [s.name, s]));

  // Grid time of a beat, before the picture lead. With a measured bars table
  // the beat sits inside its bar by interpolation; past the table the last
  // measured bar length carries on, so the grid never jumps.
  function gridBeat(n) {
    if (n < 0) fail('beat ' + n + ' is before beat 0');
    if (!c.bars) return c.beat0 + n * beatLen;
    const bar = Math.floor(n / c.beatsPerBar);
    if (bar >= c.bars.length) {
      const lastLen = c.bars.length > 1
        ? c.bars[c.bars.length - 1] - c.bars[c.bars.length - 2] : barLen;
      return c.bars[c.bars.length - 1] + (n - (c.bars.length - 1) * c.beatsPerBar) * (lastLen / c.beatsPerBar);
    }
    const barStart = c.bars[bar];
    const nextStart = bar + 1 < c.bars.length ? c.bars[bar + 1] : barStart + barLen;
    return barStart + ((n - bar * c.beatsPerBar) / c.beatsPerBar) * (nextStart - barStart);
  }

  const clock = {
    bpm: c.bpm,
    beatsPerBar: c.beatsPerBar,
    beat0: c.beat0,
    pictureLeadMs: c.pictureLeadMs,
    lyricLeadMs: c.lyricLeadMs,
    sectionNames() { return c.sections.map((s) => s.name); },
    // Picture time of beat n (n may be fractional: beat 12.5 is halfway through beat 12).
    beat(n) { return gridBeat(n) - lead; },
    // Picture time of bar n (bar 0 is the first bar).
    bar(n) { return gridBeat(n * c.beatsPerBar) - lead; },
    // Picture time the named section starts.
    section(name) {
      const s = sectionByName.get(name);
      if (!s) fail('no section named "' + name + '"');
      return gridBeat(s.bar * c.beatsPerBar) - lead;
    },
    // Picture time of a beat inside a section: at('chorus', 2) is two beats
    // into the chorus. The beat may be fractional.
    at(section, beat) {
      if (!isNum(beat) || beat < 0) fail('beat must be a number of 0 or more');
      const s = sectionByName.get(section);
      if (!s) fail('no section named "' + section + '"');
      return gridBeat(s.bar * c.beatsPerBar + beat) - lead;
    },
    // Name of the section holding film time t, or null before the first section.
    sectionAt(t) {
      if (!isNum(t)) fail('time must be a number');
      let found = null, foundStart = -Infinity;
      for (const s of c.sections) {
        const start = gridBeat(s.bar * c.beatsPerBar) - lead;
        if (start <= t + 1e-9 && start >= foundStart) { found = s.name; foundStart = start; }
      }
      return found;
    },
    // Time a lyric line appears on screen: its bar/beat on the grid, minus
    // the lyric lead (lines appear just before the first word). A line may
    // also be given as { time } in film seconds.
    lineTime(line) {
      if (!line || typeof line !== 'object') fail('line must be an object');
      if (isNum(line.time)) return line.time - c.lyricLeadMs / 1000;
      if (!Number.isInteger(line.bar) || line.bar < 0 || !isNum(line.beat) || line.beat < 0) {
        fail('line needs a whole bar and a beat of 0 or more, or a time');
      }
      return gridBeat(line.bar * c.beatsPerBar + line.beat) - c.lyricLeadMs / 1000;
    },
  };
  return clock;
}

if (typeof module !== 'undefined' && module.exports) module.exports = { createClock };
