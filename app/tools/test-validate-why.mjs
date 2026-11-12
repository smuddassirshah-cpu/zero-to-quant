#!/usr/bin/env node
/* Scratch cases for requires entries and the why rule (ENGINE-BACKLOG 551). Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), edits one cross-course edge of one
   course.json per case and expects the validator to report it (or, for "ok", no error). Run from anywhere: node app/tools/test-validate-why.mjs.
   One PASS or FAIL line per case, exit 1 on a failure. The repo is never touched. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'why', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = (extra) => h.validate(['--no-manifest', ...extra]);

/* the first level of the first course with a cross-course entry in requires; since 2c item 7 every such entry is an object
   with a why, so the copy turns that one entry back into a plain string as the fixture */
let target = null;
for (const id of fs.readdirSync(path.join(copy, 'content', 'courses')).sort()) {
  const f = path.join(copy, 'content', 'courses', id, 'course.json');
  if (!fs.existsSync(f)) continue;
  const j = JSON.parse(fs.readFileSync(f, 'utf8'));
  const refOf = (r) => (typeof r === 'string' ? r : r && r.ref);
  const isX = (r) => typeof refOf(r) === 'string' && refOf(r).split('/')[0] !== id;
  const i = (j.levels || []).findIndex(lv => Array.isArray(lv.requires) && lv.requires.some(isX));
  if (i >= 0) { const k = j.levels[i].requires.findIndex(isX); j.levels[i].requires[k] = refOf(j.levels[i].requires[k]); fs.writeFileSync(f, JSON.stringify(j, null, 2) + '\n'); target = { id, f, i, k }; break; }
}
if (!target) { console.log('FAIL no cross-course requires entry to test'); process.exit(1); }
const orig = fs.readFileSync(target.f, 'utf8');
const edit = (fn) => { const j = JSON.parse(orig); const lv = j.levels[target.i]; fn(lv, lv.requires[target.k]); fs.writeFileSync(target.f, JSON.stringify(j, null, 2) + '\n'); };
const as = (lv, o) => { lv.requires[target.k] = o; };
const count = (out) => { const m = /Requires: (\d+) cross-course edges, (\d+) without why/.exec(out); return m ? [+m[1], +m[2]] : [-1, -1]; };
const base = count(run(['--lax-why']).out);
const WHY = 'Needs the integral rules for the expectation step';
const twenty = Array.from({ length: 20 }, (_, i) => 'word' + i).join(' ');
const cases = [
  ['string-lax', () => {}, ['--lax-why'], (r) => r.code === 0 && count(r.out)[1] === base[1], 'a plain string is a warning with --lax-why'],
  ['string-strict-default', () => {}, [], (r) => r.code === 1 && /error .*has no why/.test(r.out), 'a plain cross-course string is an error by default'],
  ['object-with-why', () => edit((lv, r) => as(lv, { ref: r, why: WHY })), [], (r) => r.code === 0 && count(r.out)[1] === base[1] - 1, 'valid, one fewer edge without why'],
  ['missing-why-lax', () => edit((lv, r) => as(lv, { ref: r })), ['--lax-why'], (r) => r.code === 0 && /warning .*has no why/.test(r.out), 'a warning with --lax-why, exit 0'],
  ['missing-why-strict', () => edit((lv, r) => as(lv, { ref: r })), [], (r) => r.code === 1 && /error .*has no why/.test(r.out), 'an error by default'],
  ['long-why', () => edit((lv, r) => as(lv, { ref: r, why: twenty })), [], (r) => r.code === 1 && /why is 20 words/.test(r.out), 'an error at 20 words'],
  ['em-dash-why', () => edit((lv, r) => as(lv, { ref: r, why: 'Needs integrals — for the step' })), [], (r) => r.code === 1 && /em-dash/.test(r.out), 'an error'],
  ['multi-line-why', () => edit((lv, r) => as(lv, { ref: r, why: 'Needs integrals\nfor the step' })), [], (r) => r.code === 1 && /one line/.test(r.out), 'an error'],
  ['diagnostic-ok', () => edit((lv, r) => as(lv, { ref: r, why: WHY, gate: false })), [], (r) => r.code === 0, 'gate false with a why is valid'],
  ['diagnostic-without-why', () => edit((lv, r) => as(lv, { ref: r, gate: false })), [], (r) => r.code === 1 && /gate: false .* needs a why/.test(r.out), 'an error'],
  ['unknown-key', () => edit((lv, r) => as(lv, { ref: r, why: WHY, note: 'x' })), [], (r) => r.code === 1 && /unknown key note/.test(r.out), 'an error'],
  ['bad-ref-in-object', () => edit((lv) => as(lv, { ref: 'nothing/L1', why: WHY })), [], (r) => r.code === 1 && /unknown course "nothing"/.test(r.out), 'an error'],
];
let pass = 0, fail = 0;
for (const [name, mutate, extra, ok, what] of cases) {
  fs.writeFileSync(target.f, orig);
  mutate();
  const r = run(extra);
  const good = ok(r);
  console.log(`${good ? 'PASS' : 'FAIL'} ${name}  (${what})`);
  if (good) pass++; else { fail++; console.log(r.out.split('\n').filter(l => /^error|Requires:/.test(l)).slice(0, 4).join('\n')); }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`${pass} passed, ${fail} failed; ${base[1]} of ${base[0]} cross-course edges without why in the fixture (1 expected)`);
process.exit(fail ? 1 : 0);
