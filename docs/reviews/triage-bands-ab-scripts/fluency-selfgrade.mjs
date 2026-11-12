#!/usr/bin/env node
/* Pile 3, second step. The regression tool grades a fluency family's template text ("{key}"), which is not an answer. This script
   draws each such family as the app does (js/engine/gen.js through tools/fluency-rules.mjs, seeds 1 to N) and grades, with the real
   grader, for every drawn item: the realised answer as typed, every accept form, the answer rounded as the prompt asks, and every
   wrong value (which must not grade correct).
     node fluency-selfgrade.mjs --local-cdn <pkgs> [--seeds 40] [--part k/n]
   Reads out/pile3.json, writes out/pile3-fluency[-k].json: per entry { drawn, failed, selfBad, acceptBad, roundBad, wrongOk, examples }.
   --part k/n takes every n-th entry from k, so a run stays under two minutes. */
import fs from 'node:fs';
import path from 'node:path';
import { APP, OUT, boot, gradeText, cdnArg, readJson, short } from './lib.mjs';
const { gen } = await import(path.join(APP, 'tools/fluency-rules.mjs'));

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const SEEDS = +arg('--seeds', 40), [pk, pn] = arg('--part', '0/1').split('/').map(Number);
const { reg } = boot(cdnArg());
const pile = readJson(path.join(OUT, 'pile3.json'));
const fmt = (n) => String(+(+n).toPrecision(10));
const WORDS = { zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6 };
const asked = (prompt) => {
  const t = String(prompt).replace(/\$[^$]*\$/g, ' ').toLowerCase();
  const m = /\b(zero|one|two|three|four|five|six|\d)\s*(?:decimal places?|d\.?p\.?)/.exec(t);
  if (m) return WORDS[m[1]] ?? +m[1];
  if (/nearest (?:whole number|integer|pound)\b/.test(t)) return 0;
  if (/nearest (?:penny|pence)\b/.test(t)) return 2;
  return null;
};
const res = [];
for (const [n, r] of pile.entries()) {
  if (n % pn !== pk) continue;
  const m = /^families\[(\d+)\]\.widget$/.exec(r.path);
  if (!m || !/fluency-/.test(r.file)) { res.push({ file: r.file, path: r.path, notFamily: true }); continue; }
  const doc = readJson(path.join(APP, r.file)), f = doc.families[+m[1]];
  const out = { file: r.file, path: r.path, family: f.id, kind: r.kind, drawn: 0, failed: 0, selfBad: 0, acceptBad: 0, acceptN: 0, roundBad: 0, roundN: 0, wrongOk: 0, wrongN: 0, examples: [] };
  const bad = gen.checkFamily(f);
  if (bad.length) { out.error = bad.join('; '); res.push(out); continue; }
  const s = gen.sample(f, { seeds: SEEDS, set: doc.id });
  out.failed = s.failed;
  const note = (what, it, text, g) => { if (out.examples.length < 3) out.examples.push({ what, seed: it.seed, prompt: short(it.prompt, 200), typed: text, answer: it.widget.answer ?? it.widget.answers, tol: it.widget.tol, form: it.widget.form, key: g.key }); };
  for (const it of s.items) {
    out.drawn++;
    const w = { ...it.widget, wrong: it.wrong }, pct = w.unit === '%', isSet = Array.isArray(w.answers);
    const typed = w.kind === 'expression' ? (isSet ? w.answers.join(', ') : String(w.answer)) : (isSet ? w.answers.map((a) => fmt(a)).join(', ') : fmt(pct ? w.answer * 100 : w.answer));
    const g = await gradeText(reg, w, typed);
    if (!g.ok) { out.selfBad++; note('self', it, typed, g); }
    if (w.kind === 'expression') for (const a of (Array.isArray(w.accept) ? w.accept : [])) { out.acceptN++; const ga = await gradeText(reg, w, a); if (!ga.ok) { out.acceptBad++; note('accept', it, a, ga); } }
    if (w.kind === 'numeric' && !isSet && typeof w.answer === 'number') {
      const d = asked(it.prompt);
      if (d != null) { const step = Math.pow(10, -d), v = pct ? w.answer * 100 : w.answer, t = fmt(Math.round(v / step) * step); out.roundN++; const gr = await gradeText(reg, w, t); if (!gr.ok) { out.roundBad++; note(`rounded to ${d} dp`, it, t, gr); } }
    }
    for (const x of (it.wrong || [])) {
      const t = x.tex !== undefined ? String(x.tex) : (typeof x.value === 'number' ? fmt(pct ? x.value * 100 : x.value) : String(x.value));
      out.wrongN++; const gw = await gradeText(reg, w, t);
      if (gw.ok) { out.wrongOk++; note(`wrong "${x.id}" graded correct`, it, t, gw); }
    }
  }
  res.push(out);
}
const name = pn > 1 ? `pile3-fluency-${pk}.json` : 'pile3-fluency.json';
fs.writeFileSync(path.join(OUT, name), JSON.stringify(res, null, 1));
const tot = (k) => res.reduce((a, r) => a + (r[k] || 0), 0);
console.log(`${name}: ${res.length} entries, ${tot('drawn')} items drawn; self refused ${tot('selfBad')}, accept refused ${tot('acceptBad')} of ${tot('acceptN')}, rounded refused ${tot('roundBad')} of ${tot('roundN')}, wrong graded correct ${tot('wrongOk')} of ${tot('wrongN')}, draws failed ${tot('failed')}`);
