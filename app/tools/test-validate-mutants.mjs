#!/usr/bin/env node
/* Scratch cases for the code-widget `mutants` rules (ENGINE-BACKLOG 1263; docs/AUTHORING.md section 9, strand "ai").
   Copies tools/fixtures/mini-app (lib/validate-harness.mjs). A code lesson is placed in algo-think (untagged) and in ai-sample (strand "ai").
     shape (any course): mutants not a list, a mutant not an object, an empty or missing source, a test that is not an integer or is outside 1..tests.length
     [ai-mutants] warning: an ai course's Python code widget with fewer than two mutants; none for two valid mutants or in an untagged course
   Usage: node tools/test-validate-mutants.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import { openHarness } from './lib/validate-harness.mjs';

const h = openHarness({ name: 'mutants' });
const srcFile = h.path('content/courses/algo-think/l1-counting-work.json');
const base = JSON.parse(fs.readFileSync(srcFile, 'utf8'));
const aiFile = h.path('content/courses/ai-sample/l1-step-1.json');
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const M = (n) => ({ source: 'def count_pairs(prices, threshold):\n    return 0\n', test: n });
const run = (mutants, { ai = false } = {}) => {
  h.reset();
  const d = JSON.parse(JSON.stringify(base));
  const w = d.screens[8].widget;
  if (mutants !== undefined) w.mutants = mutants;
  if (ai) { d.course = 'ai-sample'; d.id = 'l1-step-1'; d.skills = ['ai-loss']; fs.writeFileSync(aiFile, JSON.stringify(d, null, 2)); }
  else { fs.writeFileSync(srcFile, JSON.stringify(d, null, 2)); fs.rmSync(aiFile, { force: true }); }
  const r = h.validate(['--no-manifest']);
  return { shape: r.errors.filter((l) => /mutants/.test(l)), warn: r.warnings.filter((l) => /\[ai-mutants\]/.test(l)) };
};

let r = run([M(1), M(2)]);
say(r.shape.length === 0 && r.warn.length === 0, 'two valid mutants in an untagged course: nothing', r.shape.concat(r.warn).join(' | '));
r = run(undefined);
say(r.warn.length === 0, 'no mutants in an untagged course: no warning', r.warn.join(' | '));
r = run('nope');
say(r.shape.some((l) => /mutants is a list/.test(l)), 'mutants that is not a list is an error', r.shape.join(' | '));
r = run(['x']);
say(r.shape.some((l) => /mutants\[0\]/.test(l)), 'a mutant that is not an object is an error', r.shape.join(' | '));
r = run([{ source: '  ', test: 1 }]);
say(r.shape.some((l) => /mutants\[0\]\.source/.test(l)), 'a blank source is an error', r.shape.join(' | '));
r = run([{ test: 1 }]);
say(r.shape.some((l) => /mutants\[0\]\.source/.test(l)), 'a missing source is an error', r.shape.join(' | '));
for (const bad of [0, 99, 1.5, '2', undefined]) {
  r = run([{ source: 'x = 1', test: bad }]);
  say(r.shape.some((l) => /mutants\[0\]\.test/.test(l)), `test ${JSON.stringify(bad)} is an error`, r.shape.join(' | '));
}
r = run(undefined, { ai: true });
say(r.warn.length === 1, 'ai course, no mutants: one [ai-mutants] warning', r.warn.join(' | '));
r = run([M(1)], { ai: true });
say(r.warn.length === 1 && r.shape.length === 0, 'ai course, one mutant: warning', r.warn.join(' | '));
r = run([M(1), M(2)], { ai: true });
say(r.warn.length === 0 && r.shape.length === 0, 'ai course, two mutants: no warning', r.shape.concat(r.warn).join(' | '));
h.close();
console.log(fails ? `${fails} failure(s)` : 'all passed');
process.exit(fails ? 1 : 0);
