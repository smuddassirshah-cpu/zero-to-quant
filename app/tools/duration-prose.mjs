// One matcher for a duration stated in a lesson's opening prose (PLAN 2c item 10, F07; ENGINE-BACKLOG 557).
// Used by tools/validate.mjs (warning `duration-prose`) and tools/apply-item10-content.mjs. Pattern and known false positives:
// docs/AUTHORING.md section 1 ("Duration in the opening prose").
//   import { durationHits, openingText, statedMinutes } from './duration-prose.mjs';
//   node app/tools/duration-prose.mjs [--scope 1|2] [--all]   hit counts by variant over content/courses (read-only)
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const NUM_WORDS = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10, fifteen: 15, twenty: 20, thirty: 30, forty: 40, 'forty-five': 45, fifty: 50, sixty: 60, ninety: 90 };
const WORD = Object.keys(NUM_WORDS).sort((a, b) => b.length - a.length).join('|');
// Variants, in the order they are tried. Each has a regex whose group 1 is the quantity.
//   digits-min    "60 minutes", "35 min", "45-minute"        digits then minute(s), min(s), with a space or hyphen
//   words-min     "forty-five minutes", "ninety-minute"      a number word then minute(s)
//   digits-hour   "2 hours", "1.5 hours", "3-hour"           digits then hour(s)
//   words-hour    "two hours", "an hour", "one hour", "a full hour"
//   half-hour     "half an hour", "half-hour"
export const VARIANTS = [
  { name: 'digits-min', re: /\b(\d+(?:\.\d+)?)[ -]?(?:minutes?|mins?)\b/gi, mins: (m) => Number(m[1]) },
  { name: 'words-min', re: new RegExp(`\\b(${WORD})[ -]minutes?\\b`, 'gi'), mins: (m) => NUM_WORDS[m[1].toLowerCase()] },
  { name: 'digits-hour', re: /\b(\d+(?:\.\d+)?)[ -]?(?:hours?|hrs?)\b/gi, mins: (m) => Number(m[1]) * 60 },
  { name: 'half-hour', re: /\bhalf[ -](?:an[ -])?hour\b/gi, mins: () => 30 },
  { name: 'words-hour', re: new RegExp(`\\b(?:(${WORD})|an?|one|a full)[ -]hours?\\b`, 'gi'), mins: (m) => (m[1] ? NUM_WORDS[m[1].toLowerCase()] * 60 : 60) },
];
// Context that makes a duration the data of a problem, not the length of the lesson (known false positives, kept narrow):
//   a rate or interval ("every 5 minutes", "per minute", "5-minute bars"), an offset ("10 minutes later"), a deadline inside a task.
const AFTER = /^[ -]?(?:later|earlier|ago|apart|before|after|bars?|candles?|windows?|intervals?|buckets?|samples?|moving|average|lookback|delay|cooldown|timeout|mark(?:s|outs?)?|horizon|ticks?|snapshots?|batch(?:es)?)\b/i;
const BEFORE = /(?:every|each|per)\s+$/i;
// Below this many minutes a duration is an item time ("two minutes a question"), not the length of a lesson: a short lesson holds it.
export const FLOOR = 20;

/* The opening prose: the `prose` of the first `scope` screens (default 2). A title screen's prose counts. */
export function openingText(lesson, scope = 2) {
  return (lesson.screens || []).slice(0, scope).map((s) => String(s.prose ?? '')).join('\n');
}

/* Every duration in `text`: { variant, text, minutes, index, suppressed }. `suppressed` names the false-positive rule that applied (a
   rate, interval or offset), or '' for a hit that states a length. Overlapping matches keep the first variant. */
export function durationHits(text) {
  const hits = [], taken = [];
  for (const v of VARIANTS) {
    v.re.lastIndex = 0;
    let m;
    while ((m = v.re.exec(text))) {
      const a = m.index, b = a + m[0].length;
      if (taken.some(([x, y]) => a < y && b > x)) continue;
      taken.push([a, b]);
      const minutes = v.mins(m);
      if (!Number.isFinite(minutes) || minutes <= 0) continue;
      const before = text.slice(Math.max(0, a - 24), a), after = text.slice(b, b + 24);
      let suppressed = '';
      if (AFTER.test(after)) suppressed = 'interval or offset after';
      else if (BEFORE.test(before)) suppressed = 'rate or offset before';
      hits.push({ variant: v.name, text: m[0], minutes, index: a, suppressed });
    }
  }
  return hits.sort((p, q) => p.index - q.index);
}

/* The one figure a lesson states: the largest unsuppressed duration of FLOOR minutes or more in its opening prose, or null */
export function statedMinutes(lesson, scope = 2) {
  const hs = durationHits(openingText(lesson, scope)).filter((h) => !h.suppressed && h.minutes >= FLOOR);
  return hs.length ? hs.reduce((a, h) => (h.minutes > a.minutes ? h : a)) : null;
}

/* Known false positives: { "<course>/<lesson id>": "why this duration is a problem's data" }, read from tools/duration-prose-ignore.json.
   The validator skips them; apply-item10-content.mjs names the same lessons. Add a lesson here only after reading its opening prose. */
export function ignoreList() {
  const f = join(dirname(fileURLToPath(import.meta.url)), 'duration-prose-ignore.json');
  try { return JSON.parse(readFileSync(f, 'utf8')); } catch { return {}; }
}

// Report: node app/tools/duration-prose.mjs [--scope 1|2] [--all]
if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const args = process.argv.slice(2);
  const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
  const root = join(APP, 'content', 'courses');
  const ign = ignoreList();
  const lessons = [];
  for (const cid of readdirSync(root).sort()) {
    const dir = join(root, cid);
    if (!existsSync(join(dir, 'course.json'))) continue;
    for (const f of readdirSync(dir).filter((x) => /^l\d+.*\.json$/.test(x)).sort()) {
      const L = JSON.parse(readFileSync(join(dir, f), 'utf8'));
      if (Array.isArray(L.screens)) lessons.push({ key: `${cid}/${f.replace(/\.json$/, '')}`, L });
    }
  }
  for (const scope of [1, 2]) {
    const count = (pred) => { const o = {}; let n = 0; const ls = new Set();
      for (const { key, L } of lessons) for (const h of durationHits(openingText(L, scope))) if (pred(h, L, key)) { o[h.variant] = (o[h.variant] ?? 0) + 1; n++; ls.add(key); }
      return `${n} hits in ${ls.size} lessons ${JSON.stringify(o)}`; };
    console.log(`scope first ${scope} screen(s):`);
    console.log(`  every match:                      ${count(() => true)}`);
    console.log(`  minus rates and offsets:          ${count((h) => !h.suppressed)}`);
    console.log(`  and ${FLOOR} minutes or more:          ${count((h) => !h.suppressed && h.minutes >= FLOOR)}`);
    console.log(`  and differing from minutes by >5: ${count((h, L) => !h.suppressed && h.minutes >= FLOOR && Math.abs(h.minutes - L.minutes) > 5)}`);
    console.log(`  and not on the ignore list:       ${count((h, L, k) => !h.suppressed && h.minutes >= FLOOR && Math.abs(h.minutes - L.minutes) > 5 && !ign[k])}`);
  }
  if (args.includes('--all')) for (const { key, L } of lessons) {
    const h = statedMinutes(L);
    if (h) console.log(`${key}: "${h.text}" (${h.variant}, ${h.minutes}) vs minutes ${L.minutes}${Math.abs(h.minutes - L.minutes) > 5 ? '  DISAGREES' : ''}${ign[key] ? '  ignored: ' + ign[key] : ''}`);
  }
}
