// Part D: narrow the overlapping wrong[] bands of six widgets (the four duplicate entries were edited by hand). Run from app/.
import fs from 'fs';
import { scan, at, prop, toJS, applyEdits } from './jsonscan.mjs';
const plan = [
  ['content/courses/markov/l20-when-stopping-fails.json', 'screens[5].widget', { win: 0.0004, most: 0.0005 }],
  ['content/courses/multivar/l4-chain-two-inputs.json', 'screens[8].widget', { rates: 0.1 }],
  ['content/courses/numerics/l12-stiff-equations.json', 'screens[0].widget', { exact: 0.00002 }],
  ['content/courses/stat-learning/review-2.json', 'items[0].widget', { pos: 0.0003, flip: 0.00015 }],
  ['content/courses/taylor/l2-how-wrong.json', 'screens[10].widget', { zero: 0.1 }],
  ['content/courses/trees/l13-rules-of-thumb.json', 'screens[7].widget', { rule: 0.01, atm: 0.015 }],
];
for (const [f, p, tols] of plan) {
  const text = fs.readFileSync(f, 'utf8'), root = scan(text), wn = at(root, p);
  const edits = [];
  for (const en of prop(wn, 'wrong').items) {
    const id = prop(en, 'id').v;
    if (!(id in tols)) continue;
    const t = prop(prop(en, 'tol'), 'abs');
    console.log(`${f} ${p} ${id}: tol.abs ${t.v} -> ${tols[id]}`);
    edits.push({ pos: t.s, del: t.e - t.s, text: String(tols[id]) });
  }
  if (process.argv.includes('--apply')) fs.writeFileSync(f, applyEdits(text, edits));
}
