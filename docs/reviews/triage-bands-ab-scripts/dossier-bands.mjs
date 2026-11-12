#!/usr/bin/env node
/* Piles 1 and 2: reads the validator output (node tools/validate.mjs > validate.txt, run from app/), opens every item with a
   [tight-band] or [wide-wrong-band] warning and grades probe answers with the real grader.
     node dossier-bands.mjs <validate.txt> --local-cdn <pkgs>
   Writes out/pile1.json and out/pile2.json (one record per warning) and out/pile1.txt, out/pile2.txt (the same, for reading). */
import fs from 'node:fs';
import path from 'node:path';
import { APP, OUT, boot, gradeText, cdnArg, resolve, holder, itemId, qText, short, num, halfWidth, readJson } from './lib.mjs';

const lines = fs.readFileSync(process.argv[2], 'utf8').split('\n');
const { reg } = boot(cdnArg());
const cache = {};
const load = (f) => (cache[f] ??= readJson(path.join(APP, f)));
const tail = (s, n = 170) => { s = String(s ?? '').replace(/\s+/g, ' ').trim(); return s.length > n ? '~' + s.slice(-n) : s; };
const typed = (w, v) => num(w.unit === '%' ? v * 100 : v);   // what the learner types for the stored value v
const g = async (w, v) => { const t = typed(w, v), r = await gradeText(reg, w, t); return { typed: t, ok: r.ok, key: r.key }; };

const p1 = [], p2 = [];
for (const ln of lines) {
  const m = /^warning (\S+)\s+(\S+): \[(tight-band|wide-wrong-band)\] (.*)$/.exec(ln);
  if (!m) continue;
  const [, file, where, rule, msg] = m;
  const data = load(file);
  if (rule === 'tight-band') {
    const { node: w, chain } = resolve(data, where), h = holder(chain);
    const rec = { file, path: where, id: itemId(chain), msg, q: qText(h), answer: w.answer, tol: w.tol, unit: w.unit || '', accept: w.accept || '',
      fbc: tail(h.feedback && h.feedback.correct), ex: tail(h.explain && h.explain.text), hw: halfWidth(w.answer, w.tol) };
    rec.self = await g(w, w.answer);
    let mm;
    if ((mm = /rounded as the question asks \((\d) decimal places?\) is (-?[\d.e-]+)/.exec(msg))) {
      rec.cls = 'rounded'; rec.d = +mm[1];
      const step = Math.pow(10, -rec.d) / (w.unit === '%' ? 100 : 1), r = Math.round(w.answer / step) * step;
      rec.probe = await g(w, r);
    } else if ((mm = /more decimals than the (\d) asked/.exec(msg))) {
      rec.cls = 'half-unit'; rec.d = +mm[1];
      const step = Math.pow(10, -rec.d) / (w.unit === '%' ? 100 : 1), r = Math.round(w.answer / step) * step;
      rec.probe = await g(w, r); rec.up = await g(w, r + step); rec.down = await g(w, r - step);
    } else if ((mm = /(feedback\.correct|explain\.text) prints (-?[\d.e-]+)/.exec(msg))) {
      rec.cls = 'prints'; rec.src = mm[1];
      const v = +mm[2]; rec.printed = v;
      rec.probe = await gradeText(reg, w, num(v)).then(r => ({ typed: num(v), ok: r.ok, key: r.key }));
      if (w.unit === '%') rec.probe = await g(w, v);   // the rule has already divided a printed percent by 100
    } else rec.cls = 'other';
    p1.push(rec);
  } else {
    const mw = /^(.*)\.wrong\[(\d+)\]$/.exec(where);
    const { node: w, chain } = resolve(data, mw[1]), h = holder(chain), i = +mw[2], x = w.wrong[i];
    const wh = halfWidth(x.value, x.tol ?? { abs: 1e-9 });
    const rec = { file, path: where, id: itemId(chain), msg, q: qText(h), answer: w.answer, tol: w.tol, unit: w.unit || '', wid: x.id, wvalue: x.value, wtol: x.tol, wh,
      lo: x.value - wh, hi: x.value + wh, line: short((h.feedback && h.feedback.byKey && h.feedback.byKey[x.id]) || x.why || x.line || '', 200) };
    rec.self = await g(w, w.answer);
    /* every other authored slip: does it still get its own line, or this one? */
    rec.others = [];
    for (let j = 0; j < w.wrong.length; j++) {
      if (j === i || typeof w.wrong[j].value !== 'number') continue;
      const r = await g(w, w.wrong[j].value);
      rec.others.push({ id: w.wrong[j].id, value: w.wrong[j].value, key: r.key, shadowed: r.key === x.id });
    }
    /* the band's two ends and the nearby plain values a learner could type that are no part of this slip */
    rec.ends = [await g(w, rec.lo + wh * 1e-6), await g(w, rec.hi - wh * 1e-6)];
    rec.zero = await g(w, 0);
    rec.neg = await g(w, -w.answer);
    rec.ansInWrongBand = Math.abs(w.answer - x.value) <= wh;
    if (w.unit === '%') { const r = await gradeText(reg, w, num(w.answer)); rec.asDecimal = { typed: num(w.answer), ok: r.ok, key: r.key }; }   // the answer typed as a decimal in a per cent field
    p2.push(rec);
  }
}
const j = (o) => JSON.stringify(o);
fs.writeFileSync(path.join(OUT, 'pile1.json'), JSON.stringify(p1, null, 1));
fs.writeFileSync(path.join(OUT, 'pile2.json'), JSON.stringify(p2, null, 1));
fs.writeFileSync(path.join(OUT, 'pile1.txt'), p1.map((r, n) => `#${n} ${r.file.replace('content/', '')} ${r.path} id=${r.id} [${r.cls}${r.src ? ' ' + r.src : ''}]\n  Q: ${tail(r.q, 330)}\n  ans=${r.answer} tol=${j(r.tol)} unit=${r.unit} self=${r.self.ok} probe=${j(r.probe)}${r.up ? ' up=' + r.up.typed + ':' + r.up.ok + ' down=' + r.down.typed + ':' + r.down.ok : ''}\n  fb: ${r.fbc}\n  ex: ${r.ex}\n`).join('\n'));
fs.writeFileSync(path.join(OUT, 'pile2.txt'), p2.map((r, n) => `#${n} ${r.file.replace('content/', '')} ${r.path} id=${r.id}\n  Q: ${tail(r.q, 330)}\n  ans=${r.answer} tol=${j(r.tol)} unit=${r.unit} self=${r.self.ok} wrong ${r.wid}=${r.wvalue} tol=${j(r.wtol)} band [${num(r.lo)}, ${num(r.hi)}] ansInBand=${r.ansInWrongBand}\n  others: ${r.others.map(o => `${o.id}=${o.value}->${o.key}`).join('; ')}\n  zero->${r.zero.ok ? 'OK' : r.zero.key} neg->${r.neg.ok ? 'OK' : r.neg.key}\n  line: ${r.line}\n`).join('\n'));
console.log(`pile 1: ${p1.length} tight-band warnings; pile 2: ${p2.length} wide-wrong-band warnings`);
const c = {}; p1.forEach(r => { const k = r.cls + (r.probe ? (r.probe.ok ? ' probe accepted' : ' probe refused') : ''); c[k] = (c[k] || 0) + 1; }); console.log(c);
