// Usage (from repo root): node docs/reports/prereq-mapping-scripts/fix-pass.mjs
// Fix pass of docs/reviews/review-prereq-mapping.md. Step 1 edits mapping.txt (the decided changes);
// step 2 drops references implied by another reference of the same level and deletes lists that equal
// the implicit previous-level list; step 3 syncs levels[].requires and lessonRequires in every course.json
// by text edit (no other byte changes). Prints every drop.
import fs from 'fs'; import path from 'path';
import { loadCourses } from './lib.mjs';
const MAP = 'docs/reports/prereq-mapping-scripts/mapping.txt';
const courses = loadCourses();
let lines = fs.readFileSync(MAP, 'utf8').split('\n');
const keyOf = l => l.split(' | ')[0];
const find = k => lines.findIndex(l => !l.startsWith('#') && keyOf(l) === k);
const fmt = refs => refs.map(r => `${r[0]}: ${r[1]}`).join('; ');
const parseRefs = l => l.split(' | ')[1].split('; ').map(s => { const i = s.indexOf(': '); return [s.slice(0, i), s.slice(i + 2)]; });
const set = (k, refs) => { const i = find(k); if (i < 0) throw new Error('no line ' + k); lines[i] = `${k} | ${fmt(refs)}`; };
const del = k => { const i = find(k); if (i < 0) throw new Error('no line ' + k); lines.splice(i, 1); };
const add = (k, ref, why) => { const i = find(k); const r = parseRefs(lines[i]); r.push([ref, why]); set(k, r); };

// ---- step 1: decided changes
set('puzzles L2', [...parseRefs(lines[find('puzzles L2')]), ['limits-thm/L2', 'continuous distributions: l11-largest-of-several uses uniform draws and densities']]); // error 1
del('puzzles L3'); // error 1: only the implicit puzzles/L2 remains
set('coding-int L1', [['graphs-dp/L4', 'ds and graph patterns'], ['algo-think/L3', 'sorting by hand and greedy'], ['contests/L3', 'greedy proofs (l1 cites l10) and bitmasks (l5 uses l11)']]); // error 2
del('coding-int L1 l5-bit-tricks'); // error 2
set('brainteasers L1', [['counting-chance/L2', 'counting in stages']]); // warning 1
set('brainteasers L3', [['brainteasers/L2', 'quick reasoning'], ['mental/L3', 'squaring and known decimals (l8, l10)'], ['series/L2', 'Gauss'], ['exp-log/L3', 'doubling time and natural log'], ['contests/L2', 'modulo (l5) for digits and remainders']]); // warning 1
set('conditional L1', [['counting-chance/L2', 'conditioning shrinks sample spaces and uses counting in stages and the multiplication rule']]); // warning 3
set('random-vars L1', [['counting-chance/L2', 'a random variable labels outcomes of counted experiments']]); // warning 3
set('game-theory L3', [...parseRefs(lines[find('game-theory L3')]), ['counting-chance/L3', 'l12-poker-hands: hand counts']]); // warning 3
set('mental-pressure L4', [...parseRefs(lines[find('mental-pressure L4')]), ['counting-chance/L3', 'l10-birthday: the birthday benchmark']]); // warning 3 and 6 (partly)
set('linear-maps L2', [['linear-maps/L1', 'maps between vector spaces'], ['least-squares/L1', 'four subspaces'], ['eigen/L1', 'l13 changes the basis of a matrix, taught in eigen l3-eigenbasis']]); // warning 4
set('systems L1', [['cpp-pricing/L3', 'timing, memory layout and flags (cpp/L4 is implied by it)']]); // note 1

// ---- step 2: implied references
const key = (c, n) => `${c}/L${n}`;
const explicit = {};
for (const l of lines) { if (l.startsWith('#') || !l.trim()) continue; const [h] = l.split(' | '); const p = h.split(' '); if (p.length === 2) explicit[key(p[0], p[1].slice(1))] = parseRefs(l); }
const deps = k => { const [c, n] = k.split('/L'); return explicit[k] ? explicit[k].map(r => r[0]) : (+n === 1 ? [] : [key(c, +n - 1)]); };
const reach = (k, seen = new Set()) => { for (const d of deps(k)) if (!seen.has(d)) { seen.add(d); reach(d, seen); } return seen; };
const dropped = [];
for (const k of Object.keys(explicit)) {
  const refs = explicit[k];
  const keep = refs.filter(([r]) => !refs.some(([o]) => o !== r && reach(o).has(r)));
  refs.filter(x => !keep.includes(x)).forEach(x => dropped.push(`${k} drops ${x[0]}`));
  const [c, n] = k.split('/L');
  const implicit = +n === 1 ? [] : [key(c, +n - 1)];
  const lk = `${c} L${n}`;
  if (keep.length === implicit.length && keep.every((x, i) => x[0] === implicit[i])) { del(lk); delete explicit[k]; dropped.push(`${k} list deleted (equals the implicit one)`); }
  else if (keep.length !== refs.length) set(lk, keep);
}
console.log(dropped.length + ' lines:\n' + dropped.join('\n'));
fs.writeFileSync(MAP, lines.join('\n'));

// ---- step 3: sync course.json
const final = {}, fl = {};
for (const l of lines) { if (l.startsWith('#') || !l.trim()) continue; const [h] = l.split(' | '); const p = h.split(' '); const refs = parseRefs(l).map(r => r[0]); if (p.length === 2) (final[p[0]] ||= {})[p[1].slice(1)] = refs; else (fl[p[0]] ||= {})[p[2]] = refs; }
const jf = r => '[' + r.map(x => JSON.stringify(x)).join(', ') + ']';
for (const c of Object.keys(courses)) {
  const f = path.join('app/content/courses', c, 'course.json');
  let txt = fs.readFileSync(f, 'utf8'); const j = JSON.parse(txt);
  for (const lv of j.levels) {
    const want = (final[c] || {})[lv.n];
    const hw = `"homework": ${JSON.stringify(lv.homework)}`;
    const re = new RegExp(`(${hw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})(,\\r?\\n\\s*"requires": \\[[^\\]]*\\])?(\\r?\\n)(\\s*)\\}`);
    if (!re.test(txt)) throw new Error(`${c} L${lv.n}: anchor`);
    txt = txt.replace(re, (_, a, old, nl, ind) => want ? `${a},${nl}${ind}  "requires": ${jf(want)}${nl}${ind}}` : `${a}${nl}${ind}}`);
  }
  const lrRe = /\n  "lessonRequires": \{[^}]*\},(?=\n  "levels")/;
  txt = txt.replace(lrRe, '');
  const lw = fl[c];
  if (lw) txt = txt.replace('\n  "levels": [', `\n  "lessonRequires": {\n${Object.entries(lw).map(([id, r]) => `    ${JSON.stringify(id)}: ${jf(r)}`).join(',\n')}\n  },\n  "levels": [`);
  fs.writeFileSync(f, txt);
}
console.log('synced');
