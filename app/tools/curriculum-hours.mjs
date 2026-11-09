#!/usr/bin/env node
// Hours by stage and topic from js/hours.js (the one workload function, PLAN 2c item 11), quoted in docs/curriculum.md.
//   node app/tools/curriculum-hours.mjs            print the table
//   node app/tools/curriculum-hours.mjs --check    exit 1 unless the generated block and every hours figure in the prose of docs/curriculum.md agree
//   node app/tools/curriculum-hours.mjs --write    rewrite the block between <!-- generated:hours --> and <!-- /generated -->
// Every figure is two: hours in the app (lesson, level review and homework, topic exam minutes) and hours of outside study (stored hours less in-app,
// never below 0), in-app first; the stored total is never shown alone (AUTHORING section 14). Months at 15 h a week still come from the stored hours.
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
  // the share of the stage's hours that the pure courses carry (H.courseApp and H.courseOut: topic hours shared by lesson weight), rounded per stage
  const pureIds = s.topics.flatMap((t) => t.courses ?? []).filter((id) => strandOf(id) === 'pure');
  const pureApp = pureIds.reduce((a, id) => a + H.courseApp(id), 0), pureOut = pureIds.reduce((a, id) => a + H.courseOut(id), 0);
  return { id: s.id, name: s.name, hours: h, app: Math.round(H.stageApp(s.id)), out: Math.round(H.stageOut(s.id)),
    qapp: Math.round(H.stageApp(s.id) - pureApp), qout: Math.round(H.stageOut(s.id) - pureOut), months: hours.months(h) };
});
const sum = (k) => rows.reduce((a, r) => a + r[k], 0);
const total = rows.reduce((a, r) => a + r.hours, 0), tApp = sum('app'), tOut = sum('out'), qApp = sum('qapp'), qOut = sum('qout');

const block = [
  '| Stage | In the app | Outside study | Quant path in the app | Quant path outside study | At 15 h/week |', '| --- | --- | --- | --- | --- | --- |',
  ...rows.map((r) => `| ${r.id}. ${r.name} | ${f(r.app)} | ${f(r.out)} | ${f(r.qapp)} | ${f(r.qout)} | ${r.months} months |`),
  `| All stages | ${f(tApp)} | ${f(tOut)} | ${f(qApp)} | ${f(qOut)} | ${hours.months(total)} months |`, '',
  `Stage hours are the sum of topic hours; nothing stores them. In the app counts each lesson's minutes, a level review (20 min) and homework (45 min) unless the file states minutes, and the topic exam's minutes. Outside study is the stored hours less that, never below 0; months use the stored hours. Quant path leaves out the courses tagged Pure maths, at their lesson share of a topic's hours. Topic hours:`, '',
  '| Topic | Name | In the app | Outside study | Lessons mapped | Lessons written |', '| --- | --- | --- | --- | --- | --- |',
  ...cur.stages.flatMap((s) => s.topics.map((t) => {
    let mapped = 0, written = 0;
    for (const id of t.courses ?? []) { const c = H.courseCounts(id); mapped += c.mapped; written += c.written; }
    const h = hours.topicHours(t);
    const zero = h === 0 && mapped ? ` (stores 0; its lesson minutes would give about ${f(Math.round(H.topicFromMinutes(t.id)))} h)` : '';
    return `| ${t.id} | ${t.name} | ${f(Math.round(H.topicApp(t.id)))} | ${f(Math.round(H.topicOut(t.id)))}${zero} | ${mapped} | ${written} |`;
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
expect(/The full path is about ([\d,]+) hours in the app and about [\d,]+ hours of outside study/, tApp, 'opening in-app total');
expect(/The full path is about [\d,]+ hours in the app and about ([\d,]+) hours of outside study/, tOut, 'opening outside total');
expect(/Without the pure maths items it is ([\d,]+) hours in the app and [\d,]+ hours of outside study/, qApp, 'opening quant-path in-app total');
expect(/Without the pure maths items it is [\d,]+ hours in the app and ([\d,]+) hours of outside study/, qOut, 'opening quant-path outside total');
expect(/Four stages, ([\d,]+) hours in the app and [\d,]+ of outside study/, tApp, 'map in-app total');
expect(/Four stages, [\d,]+ hours in the app and ([\d,]+) of outside study/, tOut, 'map outside total');
expect(/\(([\d,]+) and [\d,]+ on the quant path/, qApp, 'map quant-path in-app total');
expect(/\([\d,]+ and ([\d,]+) on the quant path/, qOut, 'map quant-path outside total');
for (const r of rows) {
  const row = text.match(new RegExp(`^\\| ${r.id}\\. [^|]*\\| ([\\d,]+) \\| ([\\d,]+) \\| ([\\d,]+) \\| ([\\d,]+) \\| (\\d+) months \\|`, 'm'));
  if (!row) errors.push(`prose: map row for stage ${r.id} not found`);
  else {
    [['in the app', 'app'], ['outside study', 'out'], ['quant path in the app', 'qapp'], ['quant path outside study', 'qout']].forEach(([what, k], i) => {
      if (num(row[i + 1]) !== r[k]) errors.push(`prose: stage ${r.id} map ${what} ${row[i + 1]}, source gives ${f(r[k])}`);
    });
    if (num(row[5]) !== r.months) errors.push(`prose: stage ${r.id} months ${row[5]}, source gives ${r.months}`);
  }
  expect(new RegExp(`^## Stage ${r.id}: [^(\\n]*\\(about ([\\d,]+) h in the app, about [\\d,]+ h of outside study\\)`, 'm'), r.app, `stage ${r.id} heading in-app`);
  expect(new RegExp(`^## Stage ${r.id}: [^(\\n]*\\(about [\\d,]+ h in the app, about ([\\d,]+) h of outside study\\)`, 'm'), r.out, `stage ${r.id} heading outside`);
}
if (errors.length) { console.error(errors.join('\n')); console.error(`FAIL: ${errors.length} problem(s)`); process.exit(1); }
console.log(`OK: ${rows.length} stages, ${f(tApp)} h in the app and ${f(tOut)} h of outside study (${f(qApp)} and ${f(qOut)} on the quant path), docs/curriculum.md agrees`);
