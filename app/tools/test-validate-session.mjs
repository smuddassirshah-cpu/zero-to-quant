#!/usr/bin/env node
/* Scratch cases for lesson `session` and the duration-prose warning (PLAN 2c item 10, ENGINE-BACKLOG 556 to 558). Part 1 tests the matcher
   (tools/duration-prose.mjs) directly; part 2 copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), edits one lesson per case and expects the validator to report it
   (or, for "ok", nothing). Run from anywhere: node app/tools/test-validate-session.mjs. One PASS or FAIL line per case, exit 1 on a failure.
   The repo is never touched. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';
import { durationHits, statedMinutes } from './duration-prose.mjs';

let failed = 0;
const report = (name, ok, note) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${note ? ': ' + note : ''}`); if (!ok) failed++; };

/* Part 1: the matcher */
const mins = (t) => durationHits(t).filter((h) => !h.suppressed).map((h) => h.minutes);
const m = [
  ['60 minutes', 'Two problems in 60 minutes.', [60]], ['an hour', 'You have an hour.', [60]], ['45-minute', 'A 45-minute round.', [45]],
  ['35 min', 'About 35 min in all.', [35]], ['half an hour', 'It takes half an hour.', [30]], ['two hours', 'Set aside two hours.', [120]],
  ['digits hours', 'Allow 1.5 hours.', [90]], ['words-min', 'A forty-five minutes round.', [45]],
  ['rate is data', 'It trades every 5 minutes.', []], ['bars are data', 'Use 5-minute bars for the day.', []], ['offset is data', 'Ten minutes later it fills.', []],
  ['no duration', 'Roll two dice.', []], ['seconds are not read', 'About ninety seconds a question.', []],
];
for (const [n, t, want] of m) report(`matcher: ${n}`, JSON.stringify(mins(t)) === JSON.stringify(want), `got ${JSON.stringify(mins(t))}`);
report('matcher: floor ignores item times', statedMinutes({ screens: [{ prose: 'Two minutes a question, 8 minutes for the set.' }] }) === null);
report('matcher: largest figure wins', statedMinutes({ screens: [{ prose: 'This lesson takes about 35 minutes, three minutes a question.' }] })?.minutes === 35);
report('matcher: only the first two screens', statedMinutes({ screens: [{ prose: 'a' }, { prose: 'b' }, { prose: 'Takes 60 minutes.' }] }) === null);

/* Part 2: the validator on a scratch copy */
const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'session', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = (extra = ['--no-manifest']) => h.validate(extra);

/* a lesson whose opening prose states no duration, first screen not a title-less oddity */
const root = path.join(copy, 'content', 'courses');
const ignore = JSON.parse(fs.readFileSync(path.join(APP, 'tools', 'duration-prose-ignore.json'), 'utf8'));
let target = null;
outer: for (const cid of fs.readdirSync(root).sort()) {
  const cj = path.join(root, cid, 'course.json');
  if (!fs.existsSync(cj)) continue;
  for (const f of fs.readdirSync(path.join(root, cid)).filter((x) => /^l\d+.*\.json$/.test(x)).sort()) {
    const file = path.join(root, cid, f), L = JSON.parse(fs.readFileSync(file, 'utf8'));
    if (!Array.isArray(L.screens) || !L.screens.length || typeof L.screens[0].prose !== 'string') continue;
    if (statedMinutes(L) || ignore[`${cid}/${f.replace(/\.json$/, '')}`]) continue;
    if (/duration-prose/.test(run().out.split('\n').filter((l) => l.includes(`${cid}/${f}`)).join('\n'))) continue;
    target = { file, key: `${cid}/${f.replace(/\.json$/, '')}`, orig: fs.readFileSync(file, 'utf8') }; break outer;
  }
}
if (!target) { report('setup', false, 'no lesson to edit'); process.exit(1); }
const edit = (fn) => { const L = JSON.parse(target.orig); fn(L); fs.writeFileSync(target.file, JSON.stringify(L, null, 1) + '\n'); };
const mine = (r) => r.out.split('\n').filter((l) => l.includes(path.basename(target.file)));
const errs = (r) => mine(r).filter((l) => /error/.test(l)).join('\n');
const dur = (r) => mine(r).filter((l) => /duration-prose/.test(l)).join('\n');
const baseMinutes = JSON.parse(target.orig).minutes;
const say = (t) => (L) => { L.screens[0].prose = `${t} ${L.screens[0].prose}`; };
const cases = [
  ['as-shipped', () => {}, [], (r) => r.code === 0 && !errs(r) && !dur(r), 'no error, no duration warning'],
  ['workshop-60-ok', () => edit((L) => { L.session = 'workshop'; L.minutes = 60; }), [], (r) => r.code === 0 && !errs(r), 'workshop at 60 minutes'],
  ['project-120-ok', () => edit((L) => { L.session = 'project'; L.minutes = 120; }), [], (r) => r.code === 0 && !errs(r), 'project at 120 minutes'],
  ['short-explicit-ok', () => edit((L) => { L.session = 'short'; }), [], (r) => r.code === 0 && !errs(r), 'session short is the default spelled out'],
  ['bad-session', () => edit((L) => { L.session = 'seminar'; }), [], (r) => r.code === 1 && /session is one of short, workshop, project/.test(errs(r)), 'an error'],
  ['short-30-fails', () => edit((L) => { L.minutes = 30; }), [], (r) => r.code === 1 && /minutes is 5 to 20 for a short lesson/.test(errs(r)), 'an error that names the fix'],
  ['workshop-10-fails', () => edit((L) => { L.session = 'workshop'; L.minutes = 10; }), [], (r) => r.code === 1 && /minutes is 20 to 90 for a workshop/.test(errs(r)), 'an error'],
  ['workshop-120-fails', () => edit((L) => { L.session = 'workshop'; L.minutes = 120; }), [], (r) => r.code === 1 && /20 to 90 for a workshop/.test(errs(r)), 'an error'],
  ['project-30-fails', () => edit((L) => { L.session = 'project'; L.minutes = 30; }), [], (r) => r.code === 1 && /60 to 240 for a project/.test(errs(r)), 'an error'],
  ['prose-45-warns', () => edit(say('This lesson takes about 45 minutes.')), [], (r) => r.code === 0 && /duration-prose.*45 min.*minutes is/.test(dur(r)), 'a warning, exit 0'],
  ['prose-45-agrees', () => edit((L) => { say('This lesson takes about 45 minutes.')(L); L.session = 'workshop'; L.minutes = 45; }), [], (r) => r.code === 0 && !dur(r), 'no warning once minutes is 45'],
  ['prose-within-5-quiet', () => edit((L) => { say('This lesson takes about 20 minutes.')(L); L.minutes = 15; }), [], (r) => r.code === 0 && !dur(r), 'a gap of 5 is not reported'],
  ['prose-hour-warns', () => edit(say('You have an hour for this.')), [], (r) => r.code === 0 && /duration-prose.*60 min/.test(dur(r)), 'an hour reads as 60'],
  ['prose-rate-quiet', () => edit(say('The desk trades every 25 minutes.')), [], (r) => r.code === 0 && !dur(r), 'a rate is not a lesson length'],
  ['prose-third-screen-quiet', () => edit((L) => { L.screens[2].prose = `Takes 60 minutes. ${L.screens[2].prose || ''}`; }), [], (r) => r.code === 0 && !dur(r), 'only the first two screens count'],
  ['manifest-sessions', () => edit((L) => { L.session = 'workshop'; L.minutes = 60; }), ['--force-manifest'], (r) => {
    const mf = JSON.parse(fs.readFileSync(path.join(copy, 'content', 'manifest.json'), 'utf8'));
    return r.code === 0 && mf.sessions && mf.sessions[target.key] && mf.sessions[target.key].session === 'workshop' && mf.sessions[target.key].minutes === 60;
  }, 'manifest.sessions lists the workshop with its minutes'],
];
for (const [name, setup, extra, check, note] of cases) {
  fs.writeFileSync(target.file, target.orig);
  setup();
  const r = run(extra[0] === '--force-manifest' ? [] : ['--no-manifest', ...extra]);
  let ok = false; try { ok = check(r); } catch (e) { ok = false; }
  report(name, ok, note);
  if (!ok) console.log(mine(r).join('\n') || r.out.split('\n').slice(-6).join('\n'));
}
fs.writeFileSync(target.file, target.orig);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`${failed ? 'FAIL' : 'OK'}: ${failed} failure(s); base minutes ${baseMinutes} on ${target.key}`);
process.exit(failed ? 1 : 0);
