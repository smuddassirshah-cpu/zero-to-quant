#!/usr/bin/env node
/* Scratch cases for the trainer widget rules (ENGINE-BACKLOG 1237; docs/AUTHORING.md section 3 "trainer").
   Copies tools/fixtures/mini-app (lib/validate-harness.mjs), swaps screen 0 of one lesson for an explore screen with a trainer widget on a series canvas.
     a well formed trainer (default and extra series, a supplied loop, data) validates with no trainer error
     a missing starter, bad steps, maxSeconds, editable, series, a non-series canvas, a missing params.y or params.length, an undeclared series id
     and a trainer on a problem screen are refused (it is never graded)
   Usage: node tools/test-validate-trainer.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import { openHarness } from './lib/validate-harness.mjs';

const h = openHarness({ name: 'trainer' });
const file = h.path('content/courses/algo-think/l1-counting-work.json');
const base = JSON.parse(fs.readFileSync(file, 'utf8'));
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const CANVAS = { kind: 'series', params: { series: [{ id: 'loss', label: 'Loss', values: [] }, { id: 'val', label: 'Held out', values: [] }], y: [0, 3], length: 200, xLabel: 'Step', yLabel: 'Loss' } };
const WIDGET = { kind: 'trainer', starter: 'for step in range(200):\n    report(step, 1 / (step + 1))\n', steps: 200, maxSeconds: 60 };
const run = (widget, canvas = CANVAS, type = 'explore') => {
  const d = JSON.parse(JSON.stringify(base));
  const s = d.screens[0];
  s.type = type; s.canvas = canvas; s.widget = widget;
  if (type === 'explore') { delete s.question; delete s.feedback; delete s.hints; delete s.explain; }
  fs.writeFileSync(file, JSON.stringify(d, null, 2));
  return h.validate(['--no-manifest']);
};
const bad = (r) => r.errors.filter((l) => /screens\[0\]/.test(l));

let r = run(WIDGET);
say(bad(r).length === 0, 'a well formed trainer has no error on its screen', bad(r).join(' | '));
r = run({ ...WIDGET, series: ['loss', 'val'], editable: false, starter: 'report(0, 1.0, val=2.0)\n' });
say(bad(r).length === 0, 'extra series and a supplied (read only) loop: no error', bad(r).join(' | '));
r = run({ kind: 'trainer', starter: 'x = 1\n' }, { ...CANVAS, params: { ...CANVAS.params, length: 500 } });
say(bad(r).length === 0, 'the defaults (500 steps, 120 s) with params.length 500: no error', bad(r).join(' | '));

const BAD = [
  ['starter-missing', { starter: undefined }, 'starter'], ['starter-number', { starter: 3 }, 'starter'],
  ['steps-zero', { steps: 0 }, 'steps'], ['steps-fraction', { steps: 2.5 }, 'steps'], ['steps-huge', { steps: 50000 }, 'steps'],
  ['seconds-zero', { maxSeconds: 0 }, 'maxSeconds'], ['seconds-huge', { maxSeconds: 900 }, 'maxSeconds'],
  ['editable-text', { editable: 'no' }, 'editable'], ['series-empty', { series: [] }, 'series'], ['series-number', { series: [1] }, 'series'],
  ['series-undeclared', { series: ['loss', 'acc'] }, 'series'], ['prelude-number', { prelude: 4 }, 'prelude'],
  ['data-bad-path', { data: { 'a.txt': 'content/data/nope-not-here.txt' } }, 'data'],
];
for (const [name, patch, sub] of BAD) {
  const w = { ...WIDGET, ...patch }; for (const k of Object.keys(w)) if (w[k] === undefined) delete w[k];
  r = run(w);
  say(bad(r).some((l) => l.includes(sub)), `${name}: an error names ${sub}`, r.errors.slice(0, 3).join(' | '));
}
r = run(WIDGET, { kind: 'plane', params: {} });
say(bad(r).some((l) => /series canvas/.test(l)), 'a trainer on a plane canvas is refused', bad(r).join(' | '));
r = run(WIDGET, { ...CANVAS, params: { ...CANVAS.params, y: undefined } });
say(bad(r).some((l) => /params\.y/.test(l)), 'a series canvas without params.y is refused', bad(r).join(' | '));
r = run(WIDGET, { ...CANVAS, params: { ...CANVAS.params, length: 100 } });
say(bad(r).some((l) => /params\.length/.test(l)), 'params.length below the step cap is refused', bad(r).join(' | '));
r = run(WIDGET, CANVAS, 'problem');
say(r.errors.some((l) => /never graded/.test(l)), 'a trainer on a problem screen is refused (never graded)', r.errors.slice(0, 3).join(' | '));
h.close();
if (fails) { console.error(`test-validate-trainer: ${fails} failed`); process.exit(1); }
console.log('test-validate-trainer: all passed');
