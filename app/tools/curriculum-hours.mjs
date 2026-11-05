#!/usr/bin/env node
// Hours by stage and topic from js/hours.js (the one workload function, PLAN 2c item 11), quoted in docs/curriculum.md.
//   node app/tools/curriculum-hours.mjs            print the table
//   node app/tools/curriculum-hours.mjs --check    exit 1 unless the generated block and every hours figure in the prose of docs/curriculum.md agree
//   node app/tools/curriculum-hours.mjs --write    rewrite the block between <!-- generated:hours --> and <!-- /generated -->
// Hours are topic hours as stored in curriculum.json (a stage is the sum of its topics; a stored stage field is ignored). The quant path
// leaves out the courses tagged strand "pure", at the hours their topic shares to them by lesson weight (so 1.11's vector calculus is its lesson share, not a hand split of 30 h). Topics that store 0 (3.2 and 3.4) are listed with the figure their lesson minutes would give.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadHours } from './hours-source.mjs';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const MD = join(APP, '..', 'docs', 'curriculum.md');
const { H, cur, courses, hours } = loadHours(join(APP, 'content'));

const strandOf = (id) => courses[id]?.strand ?? cur.courses?.[id]?.strand ?? null;
const f = (n) => Number(n).toLocaleString('en-GB');
const rows = cur.stages.map((s) => {
  const h = hours.stageHours(s);
  // the share of the stage's hours that the pure courses carry (H.course: topic hours shared by lesson weight), rounded per stage
  const pure = s.topics.flatMap((t) => t.courses ?? []).filter((id) => strandOf(id) === 'pure').reduce((a, id) => a + H.course(id), 0);
  return { id: s.id, name: s.name, hours: h, quant: Math.round(h - pure), months: hours.months(h) };
});
const total = rows.reduce((a, r) => a + r.hours, 0), quant = rows.reduce((a, r) => a + r.quant, 0);

const block = [
  '| Stage | Hours | Quant path | At 15 h/week |', '| --- | --- | --- | --- |',
  ...rows.map((r) => `| ${r.id}. ${r.name} | ${f(r.hours)} | ${f(r.quant)} | ${r.months} months |`),
  `| All stages | ${f(total)} | ${f(quant)} | ${hours.months(total)} months |`, '',
  `Stage hours are the sum of topic hours; nothing stores them. Quant path leaves out the courses tagged Pure maths, at their lesson share of a topic's hours. Topic hours:`, '',
  '| Topic | Name | Hours | Lessons mapped | Lessons written |', '| --- | --- | --- | --- | --- |',
  ...cur.stages.flatMap((s) => s.topics.map((t) => {
    let mapped = 0, written = 0;
    for (const id of t.courses ?? []) { const c = H.courseCounts(id); mapped += c.mapped; written += c.written; }
    const h = hours.topicHours(t);
    const zero = h === 0 && mapped ? ` (stores 0; its lesson minutes would give about ${f(Math.round(H.topicFromMinutes(t.id)))} h)` : '';
    return `| ${t.id} | ${t.name} | ${f(h)}${zero} | ${mapped} | ${written} |`;
  })),
].join('\n');

if (!process.argv.includes('--check') && !process.argv.includes('--write')) { console.log(block); process.exit(0); }

const text = readFileSync(MD, 'utf8');
const re = /(<!-- generated:hours -->\n)([\s\S]*?)(\n<!-- \/generated -->)/;
const errors = [];
const m = text.match(re);
if (!m) errors.push('docs/curriculum.md has no <!-- generated:hours --> block');
if (process.argv.includes('--write') && m) { writeFileSync(MD, text.replace(re, (_, a, __, c) => a + block + c)); console.log('curriculum.md block rewritten'); process.exit(0); }
if (m && m[2] !== block) errors.push('the generated:hours block is out of date (run with --write)');
// Prose figures that must agree: the opening totals, the map table's Hours and Quant path columns, each stage heading.
const num = (s) => Number(String(s).replace(/,/g, ''));
const expect = (re2, want, what) => { const x = text.match(re2); if (!x) errors.push(`prose: ${what} not found`); else if (num(x[1]) !== want) errors.push(`prose: ${what} says ${x[1]}, source gives ${f(want)}`); };
expect(/The full path is about ([\d,]+) hours/, total, 'opening total');
expect(/Without the pure maths items it is ([\d,]+) hours/, quant, 'opening quant-path total');
expect(/Four stages, ([\d,]+) hours \(/, total, 'map total');
expect(/\(([\d,]+) on the quant path/, quant, 'map quant-path total');
for (const r of rows) {
  const row = text.match(new RegExp(`^\\| ${r.id}\\. [^|]*\\| ([\\d,]+) \\| ([\\d,]+) \\| (\\d+) months \\|`, 'm'));
  if (!row) errors.push(`prose: map row for stage ${r.id} not found`);
  else {
    if (num(row[1]) !== r.hours) errors.push(`prose: stage ${r.id} map hours ${row[1]}, source gives ${f(r.hours)}`);
    if (num(row[2]) !== r.quant) errors.push(`prose: stage ${r.id} quant path ${row[2]}, source gives ${f(r.quant)}`);
    if (num(row[3]) !== r.months) errors.push(`prose: stage ${r.id} months ${row[3]}, source gives ${r.months}`);
  }
  expect(new RegExp(`^## Stage ${r.id}: [^(\\n]*\\(([\\d,]+) hours\\)`, 'm'), r.hours, `stage ${r.id} heading`);
}
if (errors.length) { console.error(errors.join('\n')); console.error(`FAIL: ${errors.length} problem(s)`); process.exit(1); }
console.log(`OK: ${rows.length} stages, ${f(total)} hours (${f(quant)} on the quant path), docs/curriculum.md agrees`);
