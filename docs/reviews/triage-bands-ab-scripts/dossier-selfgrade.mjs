#!/usr/bin/env node
/* Pile 3: the authored answers that do not grade correct themselves.
     node tools/grade-regression.mjs --local-cdn <pkgs> --out gr.json      (run from app/)
     node dossier-selfgrade.mjs <gr.json> --local-cdn <pkgs>
   For each failing "answer" entry this opens the widget and grades, with the real grader, the forms a learner could type instead:
   each accept form, the answer with its label ("x =") dropped, each side of a relation, and for a numeric answer the stored value at
   12 significant figures. Writes out/pile3.json and out/pile3.txt. */
import fs from 'node:fs';
import path from 'node:path';
import { APP, OUT, boot, gradeText, cdnArg, resolve, holder, itemId, qText, short, readJson } from './lib.mjs';

const gr = readJson(process.argv[2]);
const { reg } = boot(cdnArg());
const cache = {};
const load = (f) => (cache[f] ??= readJson(path.join(APP, f)));
const bad = Object.entries(gr).filter(([id, r]) => /answer$/.test(id) && r.ok === false);
const out = [];
for (const [id, r] of bad) {
  const m = /^(\S+) (\S*) answer$/.exec(id);
  const file = m[1], where = m[2].replace(/^\./, '');
  const { node: w, chain } = resolve(load(file), where), h = holder(chain);
  const rec = { file, path: where, id: itemId(chain), kind: w.kind, q: qText(h), answer: w.answer ?? w.answers, text: r.text, key: r.key, form: w.form || '', vars: w.vars || w.variables || '',
    accept: w.accept ?? '', unit: w.unit || '', tol: w.tol, unordered: w.unordered === true, isSet: Array.isArray(w.answers),
    opts: Object.fromEntries(Object.entries(w).filter(([k]) => !['kind', 'answer', 'answers', 'accept', 'wrong', 'label', 'placeholder', 'canvas', 'hint'].includes(k))),
    fbc: short(h.feedback && h.feedback.correct, 200), ex: short(h.explain && h.explain.text, 240) };
  rec.again = await gradeText(reg, w, r.text);   // the same text once more (a flaky grade would differ)
  rec.forms = [];
  const tryForm = async (what, t) => { if (typeof t !== 'string' || !t.trim()) return; const g = await gradeText(reg, w, t); rec.forms.push({ what, text: t, ok: g.ok, key: g.key }); };
  if (w.kind === 'expression') {
    for (const [i, a] of (Array.isArray(w.accept) ? w.accept : []).entries()) await tryForm(`accept[${i}]`, a);
    const t = String(r.text);
    const rel = /^(.*?)(\\leq?|\\geq?|\\neq?|<=|>=|<|>|=)(.*)$/s.exec(t);
    if (rel) { await tryForm('right side', rel[3].trim()); await tryForm('left side', rel[1].trim()); }
    if (Array.isArray(w.answers)) for (const [i, a] of w.answers.entries()) await tryForm(`answers[${i}] alone`, String(a));
  } else {
    if (typeof w.answer === 'number') {
      const k = w.unit === '%' ? 100 : 1;
      await tryForm('15 figures', String(w.answer * k));
      await tryForm('6 figures', String(+(w.answer * k).toPrecision(6)));
      await tryForm('3 figures', String(+(w.answer * k).toPrecision(3)));
    }
  }
  out.push(rec);
}
fs.writeFileSync(path.join(OUT, 'pile3.json'), JSON.stringify(out, null, 1));
const j = (o) => JSON.stringify(o);
fs.writeFileSync(path.join(OUT, 'pile3.txt'), out.map((r, n) => `#${n} ${r.file.replace('content/', '')} ${r.path} id=${r.id} ${r.kind}${r.isSet ? ' set' : ''}\n  Q: ${short(r.q, 260)}\n  text=${j(r.text)} key=${r.key} opts=${short(j(r.opts), 200)}\n  accept=${short(j(r.accept), 260)}\n  forms: ${r.forms.map(f => `${f.what} ${j(short(f.text, 60))}->${f.ok ? 'OK' : 'no' + (f.key ? ':' + f.key : '')}`).join('; ')}\n  fb: ${r.fbc}\n`).join('\n'));
console.log(`pile 3: ${out.length} authored answers do not grade correct themselves`);
const c = {}; out.forEach(r => { const k = r.kind + (r.isSet ? ' set' : '') + ' key=' + r.key; c[k] = (c[k] || 0) + 1; }); console.log(c);
