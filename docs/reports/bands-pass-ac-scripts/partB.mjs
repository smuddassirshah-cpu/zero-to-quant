// Part B: widen half-unit bands to one unit where the stored answer has more places than asked and no wrong[] band meets the wider band.
// node partB.mjs [--apply] (run from app/). Targets are the tight-band "stored answer ... use a band of 1 unit" warnings except exams/stage-3 r-t-bar and r-best-of-twenty (part C).
import fs from 'fs';
import { scan, at, prop, toJS, applyEdits } from './jsonscan.mjs';
const apply = process.argv.includes('--apply');
const skipC = ['parts[2].items[7].parts[0].widget', 'parts[2].items[11].widget'];
const lines = fs.readFileSync('/tmp/v2.txt', 'utf8').split('\n').filter(l => l.includes('[tight-band]') && /use a band of 1 unit \(([\d.]+)\)/.test(l));
const out = [];
const edits = new Map();
for (const l of lines) {
  const m = l.match(/^warning (\S+)\s+(\S+): \[.*use a band of 1 unit \(([\d.]+)\)/);
  const [, f, p, unitS] = m;
  if (f.endsWith('stage-3.json') && skipC.includes(p)) { out.push(`PART-C ${f} ${p}`); continue; }
  const text = fs.readFileSync(f, 'utf8'), root = scan(text);
  const wn = at(root, p), w = toJS(text, wn);
  // one unit of the last place asked; for unit "%" the warning states it in the fraction already when it says so, so scale by the widget unit
  let unit = +unitS;
  if (w.unit === '%') unit = unit / 100;   // asked "in % to 2 decimal places": one unit is 0.01 per cent = 0.0001 as a fraction
  const nb = unit, bad = (w.wrong || []).find(x => typeof x.value === 'number' && Math.abs(x.value - w.answer) <= nb + (x.tol?.abs ?? 0) + 1e-12);
  if (bad) { out.push(`LEAVE ${f} ${p}: wrong "${bad.id}" (${bad.value} +-${bad.tol?.abs}) meets the band ${w.answer} +-${nb}`); continue; }
  if (w.tol.abs >= nb) { out.push(`LEAVE ${f} ${p}: band already ${w.tol.abs}`); continue; }
  const tn = prop(prop(wn, 'tol'), 'abs');
  (edits.get(f) ?? edits.set(f, []).get(f)).push({ pos: tn.s, del: tn.e - tn.s, text: String(nb) });
  out.push(`WIDEN ${f} ${p}: tol.abs ${w.tol.abs} -> ${nb} (key ${w.answer} unchanged)`);
}
if (apply) for (const [f, es] of edits) fs.writeFileSync(f, applyEdits(fs.readFileSync(f, 'utf8'), es));
console.log(out.join('\n'));
