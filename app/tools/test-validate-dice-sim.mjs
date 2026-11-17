#!/usr/bin/env node
/* Scratch cases for the dice-sim canvas rules (ENGINE-BACKLOG 1217; docs/AUTHORING.md section 4).
   Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), swaps the canvas of one lesson screen for a dice-sim, and reads the report.
     a well formed dice-sim (the fixture's params, with and without controlsAfter) validates with no error
     dice, sides, keep (missing, unknown name, does not compile), trials, seed, exact, max, labels and exactLabel are refused when malformed
   Usage: node tools/test-validate-dice-sim.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import { openHarness } from './lib/validate-harness.mjs';

const h = openHarness({ name: 'dice' });
const file = h.path('content/courses/algo-think/l1-counting-work.json');
const base = JSON.parse(fs.readFileSync(file, 'utf8'));
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const GOOD = { dice: 2, keep: 'd1 == 5 || d2 == 5', trials: [10, 100, 1000], seed: 4226, exact: '11/36', max: 0.5, labels: { kept: 'Kept' } };
const run = (canvasExtra, params) => {
  const d = JSON.parse(JSON.stringify(base));
  d.screens[0].canvas = { kind: 'dice-sim', params, state: { caption: 'x' }, ...canvasExtra };
  fs.writeFileSync(file, JSON.stringify(d, null, 2));
  return h.validate(['--no-manifest']);
};

let r = run({}, GOOD);
say(!r.errors.some((l) => /params\.(dice|sides|keep|trials|seed|exact|max|labels)/.test(l)), 'a well formed dice-sim has no dice-sim error', r.errors.slice(0, 3).join(' | '));
r = run({ controlsAfter: 'check' }, { ...GOOD, dice: 3, keep: 'total >= 14', sides: 6, exact: 0.162 });
say(!r.errors.some((l) => /params\./.test(l)), 'three dice, a total rule, a numeric exact: no error', r.errors.slice(0, 3).join(' | '));

const BAD = [
  ['dice-zero', { dice: 0 }, 'params.dice'], ['dice-seven', { dice: 7 }, 'params.dice'], ['dice-fraction', { dice: 2.5 }, 'params.dice'], ['sides-one', { sides: 1 }, 'params.sides'],
  ['keep-missing', { keep: undefined }, 'params.keep'], ['keep-unknown-name', { keep: 'd3 == 5' }, 'params.keep'], ['keep-assignment', { keep: 'd1 = 5' }, 'params.keep'],
  ['trials-empty', { trials: [] }, 'params.trials'], ['trials-zero', { trials: [0, 10] }, 'params.trials'], ['trials-text', { trials: ['ten'] }, 'params.trials'],
  ['seed-object', { seed: {} }, 'params.seed'], ['exact-above-one', { exact: 1.5 }, 'params.exact'], ['exact-bad-fraction', { exact: 'a/b' }, 'params.exact'],
  ['max-zero', { max: 0 }, 'params.max'], ['labels-unknown-key', { labels: { won: 'Won' } }, 'params.labels'], ['labels-number', { labels: { kept: 3 } }, 'params.labels'],
  ['exactLabel-number', { exactLabel: 3 }, 'params.exactLabel'],
];
for (const [name, patch, sub] of BAD) {
  const p = { ...GOOD, ...patch }; for (const k of Object.keys(p)) if (p[k] === undefined) delete p[k];
  r = run({}, p);
  say(r.errors.some((l) => l.includes(sub)), `${name}: an error names ${sub}`, r.errors.slice(0, 3).join(' | '));
}
r = run({ controlsAfter: 'soon' }, GOOD);
say(r.errors.some((l) => l.includes('controlsAfter')), 'controlsAfter still checked on a dice-sim', r.errors.slice(0, 3).join(' | '));
h.close();
if (fails) { console.error(`test-validate-dice-sim: ${fails} failed`); process.exit(1); }
console.log('test-validate-dice-sim: all passed');
