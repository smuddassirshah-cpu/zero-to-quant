#!/usr/bin/env node
// Advisory tool (ENGINE-BACKLOG 698): list every rubric tick set that passes a longform self-mark.
// Run from app/:  node tools/rubric-passes.mjs --item content/courses/<course>/homework-<n>.json#<item-id>
//                 node tools/rubric-passes.mjs --course <course> | --all   [--json]
// Pass rule mirrors js/engine/widgets/longform.js: `const PASS = 7` (an absolute points
// threshold, not a share of the total) and every row with `required: true` must be ticked.
// Exit code is always 0.
import fs from 'node:fs';
import path from 'node:path';

export const PASS = 7; // mirrors PASS in app/js/engine/widgets/longform.js

const MAX_ROWS = 20;

export function analyse(rubric) {
  const n = rubric.length;
  if (n > MAX_ROWS) return { error: `rubric has ${n} rows, over the ${MAX_ROWS} limit` };
  const pts = rubric.map((r) => +r.points || 0);
  const req = rubric.map((r) => r.required === true);
  const total = pts.reduce((a, b) => a + b, 0);
  const passes = (mask) => {
    let s = 0;
    for (let i = 0; i < n; i++) {
      if (mask & (1 << i)) s += pts[i];
      else if (req[i]) return false;
    }
    return s >= PASS;
  };
  const passing = [];
  for (let m = 0; m < 1 << n; m++) if (passes(m)) passing.push(m);
  // passing is closed upwards, so a set is minimal when removing any one row fails.
  const minimal = passing.filter((m) => {
    for (let i = 0; i < n; i++) if ((m & (1 << i)) && passes(m & ~(1 << i))) return false;
    return true;
  });
  const rows = rubric.map((r, i) => ({
    row: i + 1, points: pts[i], required: req[i], text: String(r.text || '').slice(0, 60),
    canBeLeftOut: passing.some((m) => !(m & (1 << i))),
  }));
  return {
    total, pass: PASS, passingSets: passing.length, canPass: passing.length > 0, rows,
    minimalSets: minimal.map((m) => rubric.map((_, i) => i + 1).filter((k) => m & (1 << (k - 1)))
    ),
  };
}

const sum = (rows, set) => set.reduce((a, k) => a + rows[k - 1].points, 0);

function render(label, res) {
  const out = [`${label}`];
  if (res.error) return out.concat(`  ${res.error}`).join('\n');
  out.push(`  points total ${res.total}, pass line ${res.pass}, passing tick sets ${res.passingSets}${res.total !== 10 ? ', NOTE: points do not sum to 10' : ''}`);
  for (const r of res.rows) out.push(`  ${r.row}. ${r.points} pt${r.points === 1 ? '' : 's'}${r.required ? ' required' : ''}: ${r.text}`);
  if (!res.canPass) out.push('  No tick set passes.');
  else {
    out.push('  Minimal passing sets:');
    for (const s of res.minimalSets) out.push(`    rows ${s.join(', ')} (${sum(res.rows, s)} points)`);
  }
  out.push('  Can be left out of a pass:');
  for (const r of res.rows) out.push(`    row ${r.row}: ${r.canBeLeftOut ? 'yes' : 'no'}`);
  return out.join('\n');
}

// Homework items come in two shapes: `widget: { kind: 'longform', rubric }` or a flat longform item with `rubric` on the item.
const rubricOf = (it) => (it.widget && Array.isArray(it.widget.rubric) ? it.widget.rubric : Array.isArray(it.rubric) ? it.rubric : null);

function loadItems(file) {
  let j;
  try { j = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { return []; }
  return (j.items || []).map((it) => ({ file, it }));
}

function main() {
  const a = process.argv.slice(2);
  const json = a.includes('--json');
  const val = (f) => { const i = a.indexOf(f); return i >= 0 ? a[i + 1] : null; };
  const root = path.join('content', 'courses');
  const courseFiles = (c) => {
    const d = path.join(root, c);
    if (!fs.existsSync(d)) return [];
    return fs.readdirSync(d).filter((f) => /^(homework|review)-\d+\.json$/.test(f)).sort((x, y) => x.localeCompare(y, 'en', { numeric: true })).map((f) => path.join(d, f));
  };
  let targets = [];
  if (val('--item')) {
    const [file, id] = val('--item').split('#');
    const hit = loadItems(file).find((x) => x.it.id === id);
    if (!hit) console.log(`Item not found: ${val('--item')}`);
    else targets = [hit];
  } else if (val('--course') || a.includes('--all')) {
    const courses = a.includes('--all') ? fs.readdirSync(root).filter((c) => fs.existsSync(path.join(root, c, 'course.json'))).sort() : [val('--course')];
    for (const c of courses) for (const f of courseFiles(c)) for (const x of loadItems(f)) {
      if (x.it.performance && rubricOf(x.it)) targets.push(x);
    }
  } else {
    console.log('Usage: node tools/rubric-passes.mjs --item <file>#<item-id> | --course <course> | --all [--json]');
    return;
  }
  const results = [];
  for (const { file, it } of targets) {
    const rubric = rubricOf(it);
    const res = rubric ? analyse(rubric) : { error: 'item has no rubric' };
    results.push({ item: `${file}#${it.id}`, performance: it.performance || null, ...res });
  }
  if (json) { console.log(JSON.stringify(results, null, 2)); return; }
  for (const r of results) console.log(render(`${r.item}${r.performance ? ` (performance: ${r.performance})` : ''}`, r) + '\n');
  if (results.length > 1 || !results.length) console.log(`${results.length} item(s) analysed.`);
}

if (process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname)) main();
