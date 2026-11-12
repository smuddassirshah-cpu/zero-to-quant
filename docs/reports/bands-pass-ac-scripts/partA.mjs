// Part A: [percent-form] warnings. For each widget add a wrong[] entry "decimal" (key over 100, or over 10,000 for %^2)
// and its byKey line. Run from app/ after the validator (reads /tmp/v.txt). --apply writes the files.
import fs from 'fs';
import { scan, at, upPath, prop, toJS, appendEdit, applyEdits } from './jsonscan.mjs';
const apply = process.argv.includes('--apply');
const fmt = (x) => { let s = Number(x.toPrecision(10)).toString(); if (/e/.test(s)) s = x.toFixed(12).replace(/0+$/, '').replace(/\.$/, ''); return s; };
const sig2 = (x) => Number(x.toPrecision(2));
const lines = fs.readFileSync('/tmp/v.txt', 'utf8').split('\n').filter(l => l.includes('[percent-form]'));
const byFile = new Map();
for (const l of lines) { const m = l.match(/^warning (\S+)\s+(\S+): \[/); if (!m) continue; (byFile.get(m[1]) ?? byFile.set(m[1], []).get(m[1])).push(m[2]); }
const report = [];
let done = 0;
for (const [f, paths] of byFile) {
  const text = fs.readFileSync(f, 'utf8');
  const root = scan(text);
  const edits = [];
  for (const p of paths) {
    const wn = at(root, p), w = toJS(text, wn);
    const parentPath = upPath(p), par = at(root, parentPath);
    const q = (() => { // the question text of the nearest holder
      let pp = parentPath; for (;;) { const n = pp ? at(root, pp) : root; const qq = prop(n, 'question'); if (qq) return toJS(text, qq); if (!pp) return ''; pp = upPath(pp); }
    })();
    const tag = `${f.replace('content/', '')} ${p}`;
    const sq = /%²|%\^2|%\^\{2\}|%\^\s*2/.test(q);
    const ans = w.answer;
    if (typeof ans !== 'number' || !w.tol || w.tol.abs === undefined) { report.push(`SKIP ${tag}: answer or tol shape`); continue; }
    if (ans === 0) { report.push(`SKIP ${tag}: key is 0, no decimal form to catch`); continue; }
    const dec = ans / (sq ? 1e4 : 100);
    const dp = (() => { const m = /(\d+)\s*(?:decimal places?|places|dp)/i.exec(q); return m ? +m[1] : null; })();
    let tolNew = Math.max(w.tol.abs / (sq ? 1e4 : 100), sig2(Math.abs(dec) * 0.02));
    if (dp !== null) tolNew = Math.max(tolNew, 0.5 * Math.pow(10, -dp));
    tolNew = Number(tolNew.toPrecision(2));
    // overlaps
    const bands = [{ id: 'answer', v: ans, t: w.tol.abs }, ...(w.wrong || []).filter(x => typeof x.value === 'number').map(x => ({ id: x.id, v: x.value, t: x.tol?.abs ?? 0 }))];
    const clash = bands.find(b => Math.abs(b.v - dec) <= b.t + tolNew + 1e-12);
    if (clash) { report.push(`SKIP ${tag}: ${fmt(dec)} (+-${tolNew}) meets ${clash.id}`); continue; }
    const wr = prop(wn, 'wrong');
    const byKey = prop(prop(par, 'feedback'), 'byKey');
    if (!wr || !byKey) { report.push(`SKIP ${tag}: no wrong or byKey node`); continue; }
    let id = 'decimal'; if ((w.wrong || []).some(x => x.id === id)) id = 'as-decimal';
    // template: last wrong entry that has only id, value and tol with an abs
    const cand = [...wr.items].reverse().find(n => { const o = toJS(text, n); const ks = Object.keys(o); return ks.length === 3 && o.id !== undefined && typeof o.value === 'number' && o.tol && o.tol.abs !== undefined && ks.includes('tol'); });
    if (!cand) { report.push(`SKIP ${tag}: no template wrong entry`); continue; }
    let et = text.slice(cand.s, cand.e); const en = scan(et);
    const reps = [
      [prop(en, 'id'), JSON.stringify(id)],
      [prop(en, 'value'), fmt(dec)],
      [prop(prop(en, 'tol'), 'abs'), fmt(tolNew)],
    ].sort((a, b) => b[0].s - a[0].s);
    for (const [n, t] of reps) et = et.slice(0, n.s) + t + et.slice(n.e);
    const A = fmt(ans);
    const msg = sq ? `${fmt(dec)} is the answer with the returns written as decimals. The question asks for %², so multiply by 10,000 and type ${A}.`
      : /percentage points?/i.test(q) ? `${fmt(dec)} is ${A} points written as a decimal. Type the number of percentage points, ${A}.`
      : `${fmt(dec)} is ${A}% written as a decimal. The field asks for the number of per cent, so type ${A} without a % sign.`;
    edits.push(appendEdit(text, wr, et));
    edits.push(appendEdit(text, byKey, `${JSON.stringify(id)}: ${JSON.stringify(msg)}`));
    report.push(`ADD  ${tag}: ${id}=${fmt(dec)} tol ${fmt(tolNew)} (key ${A})`);
    done++;
  }
  if (apply && edits.length) fs.writeFileSync(f, applyEdits(text, edits));
}
console.log(report.join('\n'));
console.log('added', done, 'of', lines.length);
