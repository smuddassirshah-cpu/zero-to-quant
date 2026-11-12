#!/usr/bin/env node
/* Scratch cases for the drill-index rules (ENGINE-BACKLOG 859). Copies tools/fixtures/mini-app to a temp folder (lib/validate-harness.mjs), breaks one thing per case and expects the validator to report it
   (or, for the first case, nothing). Rules: a row of drills/index.json must agree with its drill file on name, course and difficulty; a row naming a drill with
   no file is an error; a non-sample drill file with no row is an error. Nothing under app/content is touched.
   Run from anywhere: node app/tools/test-validate-drill-index.mjs. One PASS or FAIL line per case, exit 1 on a failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { openHarness } from './lib/validate-harness.mjs';

const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const h = openHarness({ name: 'drill-index', fixtures: [] });   // a scratch copy of tools/fixtures/mini-app (see lib/validate-harness.mjs)
const tmp = h.dir;
const copy = h.dir;
const run = () => h.validate();
const dir = path.join(copy, 'content/drills');
const idxFile = path.join(dir, 'index.json');
const original = fs.readFileSync(idxFile, 'utf8');
const base = JSON.parse(original)[0];               // the first row and its file
const baseFile = path.join(dir, base.id + '.json');
const baseOriginal = fs.readFileSync(baseFile, 'utf8');
const editIdx = (fn) => { const j = JSON.parse(original); fn(j); fs.writeFileSync(idxFile, JSON.stringify(j, null, 2)); };
const editDrill = (fn) => { const j = JSON.parse(baseOriginal); fn(j); fs.writeFileSync(baseFile, JSON.stringify(j, null, 2)); };
const cases = [
  ['ok-as-shipped', () => {}, null],
  ['name-differs', () => editIdx(j => { j[0].name += ' x'; }), 'says name'],
  ['course-differs', () => editIdx(j => { j[0].course = 'no-such-course'; }), 'says course'],
  ['difficulty-differs', () => editIdx(j => { j[0].difficulty = base.difficulty === 5 ? 1 : base.difficulty + 1; }), 'says difficulty'],
  ['drill-file-changed', () => editDrill(j => { j.name = 'Another name'; }), 'says name'],
  ['row-without-a-file', () => editIdx(j => { j.push({ id: 'ghost-drill', name: 'Ghost', course: base.course, difficulty: 2 }); }), 'ghost-drill'],
  ['file-without-a-row', () => editIdx(j => { j.shift(); }), 'not listed in drills/index.json'],
  ['sample-file-without-a-row-is-fine', () => { const j = JSON.parse(baseOriginal); j.sample = true; j.id = 'sample-zz'; fs.writeFileSync(path.join(dir, 'sample-zz.json'), JSON.stringify(j, null, 2)); }, null],
];
let pass = 0, fail = 0;
for (const [name, mutate, has] of cases) {
  fs.writeFileSync(idxFile, original); fs.writeFileSync(baseFile, baseOriginal); fs.rmSync(path.join(dir, 'sample-zz.json'), { force: true });
  mutate();
  const r = run();
  const errs = r.out.split('\n').filter(l => /^error/.test(l) && /drills/.test(l));
  let problem = null;
  if (has === null) { if (r.code !== 0 || errs.length) problem = `expected no drill error, got ${errs.length}: ${errs[0] || r.out.slice(-300)}`; }
  else if (!errs.some(l => l.includes(has))) problem = `no drill error contains "${has}" (got ${errs.length}: ${errs[0] || 'none'})`;
  if (problem) { console.log(`FAIL ${name}: ${problem}`); fail++; } else { console.log(`PASS ${name}`); pass++; }
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`test-validate-drill-index: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
