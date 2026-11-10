#!/usr/bin/env node
/* Draws items from a generated fluency set (ENGINE-BACKLOG 814; author side docs/AUTHORING.md section 16).
   Authors feed the --json output to their Python recompute script, which must derive each answer independently from the variable
   values (never from the printed answer), and use it to read the prompts as a learner would.

   node tools/fluency-sample.mjs --set <course>/<set id> [--family <id>] [--seed <s>] [--n <k>] [--json] [--stats]
   node tools/fluency-sample.mjs --set fixture/<id>        a fixture under tools/fixtures/fluency
   node tools/fluency-sample.mjs --file <path>             any set file

   Without --family: one attempt as a learner would meet it (--n items, default the set's n, families round robin by weight,
   no repeated prompt) from seed --seed (default 1). With --family: --n draws of that family (default 20) on seeds s, s+1, ...
   --json prints { set, seed, items: [{ family, seed, vars, lets, prompt, answer (or answers and unordered, for a set), kind, accept, form, upToConstant, tol, unit,
   wrong: [{ id, tex | value, line }], solution }] } (vars are numbers where they are whole or terminating decimals, else
   "n/d" text or the text itself). --stats adds, per family, what the validator samples at 200 seeds: distinct prompts and
   rejected draws. Exit 0, or 1 with the reason when the set or a family cannot be drawn. */
import path from 'node:path';
import { gen, loadSet, SEEDS } from './fluency-rules.mjs';

const argv = process.argv.slice(2);
const val = (k) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : null; };
const has = (k) => argv.includes(k);
const die = (m) => { console.error('fluency-sample: ' + m); process.exit(1); };
if (has('--help') || has('-h') || argv.length === 0) { console.log('usage: node tools/fluency-sample.mjs --set <course>/<set id> [--family id] [--seed s] [--n k] [--json] [--stats]\n       (see the comment at the top of this file)'); process.exit(argv.length ? 0 : 1); }

let loaded;
try { loaded = loadSet(val('--file') ? path.resolve(val('--file')) : val('--set') || ''); } catch (e) { die(e.message); }
const doc = loaded.doc, seed = val('--seed') != null ? val('--seed') : '1', fam = val('--family');
const k = val('--n') != null ? Math.max(1, parseInt(val('--n'), 10) || 0) : null;
const num = (x) => (typeof x === 'string' && /^-?\d+(\.\d+)?$/.test(x) ? Number(x) : x);
const map = (o) => Object.fromEntries(Object.entries(o || {}).map(([a, b]) => [a, num(b)]));
const row = (it, s) => ({
  family: it.family, ...(s !== undefined ? { seed: s } : {}), vars: map(it.vars), lets: map(it.lets), prompt: it.prompt,
  answer: it.widget.answer, ...(it.widget.answers !== undefined ? { answers: it.widget.answers, unordered: it.widget.unordered } : {}), kind: it.widget.kind,
  ...(it.widget.accept !== undefined ? { accept: it.widget.accept } : {}), ...(it.widget.form ? { form: it.widget.form } : {}),
  ...(it.widget.upToConstant ? { upToConstant: true } : {}), ...(it.widget.tol ? { tol: it.widget.tol } : {}), ...(it.widget.unit ? { unit: it.widget.unit } : {}),
  wrong: it.wrong.map((w) => ({ id: w.id, ...(w.tex !== undefined ? { tex: w.tex } : { value: w.value }), line: w.line })), solution: it.solution,
});

let items = [];
if (fam) {
  const f = (doc.families || []).find((x) => x.id === fam);
  if (!f) die(`no family "${fam}" in ${doc.id} (the families are ${(doc.families || []).map((x) => x.id).join(', ')})`);
  const bad = gen.checkFamily(f);
  if (bad.length) die(`family ${fam}: ${bad.join('; ')}`);
  const start = /^\d+$/.test(seed) ? Number(seed) : 1;
  const r = gen.sample(f, { seeds: k || 20, set: doc.id, from: start });
  if (r.failed) die(`family ${fam}: ${r.failed} draws could not be completed (${r.errors.length ? r.errors[0][0] : 'where rejects every draw'})`);
  items = r.items.map((it) => row(it, it.seed));
} else {
  const n = k || doc.n || 20;
  const got = gen.generate(doc, seed, { n });
  if (got.length < n) die(`only ${got.length} of ${n} items could be drawn: a family cannot fill its turns (run the validator)`);
  items = got.map((it) => row(it));
}

const stats = has('--stats') ? (doc.families || []).filter((f) => !gen.checkFamily(f).length).map((f) => { const r = gen.sample(f, { seeds: SEEDS, set: doc.id }); return { family: f.id, drawn: SEEDS, distinctPrompts: r.distinct, attempts: r.attempts, rejected: r.rejected, failed: r.failed }; }) : null;

if (has('--json')) {
  console.log(JSON.stringify({ set: doc.id, lesson: doc.lesson, seed: /^\d+$/.test(seed) ? Number(seed) : seed, items, ...(stats ? { stats } : {}) }, null, 2));
} else {
  items.forEach((it, i) => {
    console.log(`${i + 1}. [${it.family}] ${it.prompt}`);
    console.log(`     vars ${JSON.stringify(it.vars)}${Object.keys(it.lets).length ? ` lets ${JSON.stringify(it.lets)}` : ''}`);
    console.log(`     answer ${JSON.stringify(it.answers !== undefined ? it.answers : it.answer)}${it.answers !== undefined ? ' (a set, in any order)' : ''}${it.form ? ` (form ${it.form})` : ''}${it.upToConstant ? ' (up to a constant)' : ''}`);
    it.wrong.forEach((w) => console.log(`     wrong ${w.id}: ${JSON.stringify(w.tex !== undefined ? w.tex : w.value)}${w.line ? `  "${w.line}"` : ''}`));
    it.solution.forEach((s) => console.log(`     solution: ${s}`));
  });
  if (stats) stats.forEach((s) => console.log(`family ${s.family}: ${s.distinctPrompts} distinct prompts in ${s.drawn} draws, ${s.rejected} of ${s.attempts} draws rejected${s.failed ? `, ${s.failed} could not be completed` : ''}`));
}
