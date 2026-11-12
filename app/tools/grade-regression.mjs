#!/usr/bin/env node
/* Grader regression tool (ENGINE-BACKLOG 898, 902, 904, 905 to 908: a grader change must not change the grade of any authored answer).
   Runs every authored `answer`, every `accept` form and every `wrong[]` value of every `expression` and `numeric` widget in
   app/content through the real widget code (js/engine/grade.js, widgets/expression.js, widgets/numeric.js, loaded in a stub
   DOM, the Compute Engine from --local-cdn) and records { ok, key } for each. Two runs are compared.
     node tools/grade-regression.mjs --local-cdn <pkgs> --out before.json [--root <app dir>] [--jobs 4]
     node tools/grade-regression.mjs --local-cdn <pkgs> --diff before.json [--root <app dir>] [--jobs 4]
   --root names the app folder whose js/engine and content are read (default: this one), so the "before" run can be taken
   from an export of an earlier commit (git archive <commit> app | tar -x -C <dir>) and the content kept the same.
   --content <dir> reads content from another app folder than --root (default: --root).
   A Fluency family (an object with `vars`), a `{{carry...}}` answer and anything under tools/fixtures are not graded (templates and fixtures, not authored
   texts); a --diff against an output file written before this change reports them as GONE.
   --diff prints every outcome that differs (file, path, text, before, after) and exits 1 if any does. Documented in
   docs/AUTHORING.md (section 3, "Grader regression"). Exit 0 same, 1 changed, 2 setup problem. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const arg = (k, d = null) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d; };
const ROOT = path.resolve(arg('--root', path.resolve(HERE, '..')));
const CONTENT = path.resolve(arg('--content', ROOT));
const cdn = arg('--local-cdn') ? path.resolve(arg('--local-cdn')) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;
const die = (m) => { console.error('grade-regression: ' + m); process.exit(2); };
const ceFile = cdn && path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
if (!ceFile || !fs.existsSync(ceFile)) die('give --local-cdn <pkgs> (or ZQ_LOCAL_CDN) with the local Compute Engine');

const walk = (d, out = []) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p, out); else if (e.name.endsWith('.json') && e.name !== 'manifest.json') out.push(p); } return out; };

/* ---------- the stub DOM and the real widget files ---------- */
const stubEl = () => {
  const el = { value: '', hidden: false, textContent: '', innerHTML: '', readOnly: false, className: '', children: [],
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, removeEventListener() {}, setAttribute() {}, getAttribute() { return null; }, append() {}, prepend() {}, focus() {}, remove() {},
    querySelector() { return stubEl(); }, querySelectorAll() { return []; } };
  return el;
};
const boot = () => {
  const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; }, createElement: stubEl, head: stubEl() }, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g);
  vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
  const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
  const reg = {};
  g.ZQ = { h: () => stubEl(), esc: (s) => String(s), widgets: { register: (k, f) => { reg[k] = f; }, dataPanel: () => null }, mathify() {} };
  for (const f of ['js/engine/grade.js', 'js/engine/widgets/expression.js', 'js/engine/widgets/numeric.js']) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), g, { filename: f });
  g.ZQ.grade.maths = () => Promise.resolve({ mathlive: false, ce });
  return { reg, ce };
};
const gradeText = async (reg, spec, text) => {
  const host = stubEl(), ctx = { change() {} };
  const api = reg[spec.kind](host, spec, ctx);
  api.set(text);
  await new Promise((r) => setTimeout(r, 0));
  const r = await api.grade();
  return { ok: !!r.ok, key: r.key || null };
};

/* ---------- collecting the authored texts ---------- */
const collect = () => {
  const jobs = [];
  for (const file of walk(CONTENT)) {
    let data; try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { continue; }
    const rel = path.relative(CONTENT, file);
    if (/(^|[\\/])tools[\\/]fixtures[\\/]/.test(rel)) continue;   // triage-bands-ab 9: test fixtures are not content
    const go = (v, p) => {
      if (Array.isArray(v)) v.forEach((x, i) => go(x, `${p}[${i}]`));
      else if (v && typeof v === 'object') {
        if (v.vars && typeof v.vars === 'object' && !Array.isArray(v.vars)) return;   // triage-bands-ab 8: a Fluency family is a template ({x} slots), drawn at run time, not an authored text
        if (typeof v.answer === 'string' && /\{\{carry/.test(v.answer)) return;   // a carried value, known only when the learner reaches it
        if ((v.kind === 'expression' && (typeof v.answer === 'string' || Array.isArray(v.answers))) || (v.kind === 'numeric' && (v.answer != null || Array.isArray(v.answers)))) {
          const set = Array.isArray(v.answers) && v.unordered === true;
          const texts = [];
          const fmt = (n) => { const a = +n * (v.unit === '%' ? 100 : 1); return String(+a.toPrecision(10)); };
          if (v.kind === 'expression') {
            texts.push(['answer', set ? v.answers.join(', ') : v.answer]);
            (v.accept || []).forEach((a, i) => { if (typeof a === 'string') texts.push([`accept[${i}]`, a]); });
            (v.wrong || []).forEach((w, i) => { if (w && typeof w.tex === 'string') texts.push([`wrong[${i}]`, w.tex]); });
          } else {
            texts.push(['answer', set ? v.answers.map(fmt).join(', ') : fmt(v.answer)]);
            (v.wrong || []).forEach((w, i) => { if (w && w.value != null) texts.push([`wrong[${i}]`, typeof w.value === 'string' ? w.value : fmt(w.value)]); });
          }
          texts.filter(([, text]) => !/\{\{carry/.test(String(text))).forEach(([what, text]) => jobs.push({ id: `${rel} ${p} ${what}`, spec: v, text }));
        }
        Object.entries(v).forEach(([k, x]) => go(x, `${p}.${k}`));
      }
    };
    go(data, '');
  }
  return jobs;
};

/* ---------- worker: grade a slice and send the outcomes back ---------- */
if (process.env.ZQ_GR_WORKER) {
  const { reg } = boot();
  process.on('message', async (m) => {
    const out = {};
    for (const j of m.jobs) {
      try { const r = await gradeText(reg, j.spec, j.text); out[j.id] = { ...r, text: j.text }; } catch (e) { out[j.id] = { ok: null, key: 'ERROR ' + String(e.message).slice(0, 60), text: j.text }; }
    }
    process.send({ out }, () => process.exit(0));
  });
} else {
  const jobs = collect();
  const nJobs = Math.max(1, +arg('--jobs', 4));
  const slices = Array.from({ length: nJobs }, () => []);
  jobs.forEach((j, i) => slices[i % nJobs].push(j));
  const results = {};
  let left = nJobs;
  const finish = () => {
    const outFile = arg('--out'), diffFile = arg('--diff');
    console.log(`grade-regression: ${Object.keys(results).length} authored texts graded (root ${ROOT})`);
    if (outFile) { fs.writeFileSync(outFile, JSON.stringify(results)); console.log('written ' + outFile); }
    if (diffFile) {
      const before = JSON.parse(fs.readFileSync(diffFile, 'utf8'));
      let changed = 0;
      for (const id of Object.keys(results)) {
        const a = before[id], b = results[id];
        if (!a) { console.log(`NEW      ${id}`); changed++; continue; }
        if (a.ok !== b.ok || a.key !== b.key) { changed++; console.log(`CHANGED  ${id}\n         text ${JSON.stringify(b.text)}\n         before ${JSON.stringify({ ok: a.ok, key: a.key })}  after ${JSON.stringify({ ok: b.ok, key: b.key })}`); }
      }
      for (const id of Object.keys(before)) if (!results[id]) { console.log(`GONE     ${id}`); changed++; }
      console.log(`grade-regression: ${changed} outcome${changed === 1 ? '' : 's'} changed`);
      process.exit(changed ? 1 : 0);
    }
    const bad = Object.entries(results).filter(([id, r]) => /answer$/.test(id) && r.ok === false);
    console.log(`${bad.length} authored answers do not grade correct themselves (note, not a failure)`);
  };
  slices.forEach((s) => {
    const c = fork(fileURLToPath(import.meta.url), argv, { env: { ...process.env, ZQ_GR_WORKER: '1' } });
    c.on('message', (m) => { Object.assign(results, m.out); });
    c.on('exit', () => { if (--left === 0) finish(); });
    c.send({ jobs: s });
  });
}
