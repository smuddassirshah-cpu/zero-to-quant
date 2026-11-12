#!/usr/bin/env node
/* Keys, bands and slip routing of all content, in node, with no browser and no baseline file (ENGINE-BACKLOG, engine pass AC part 3).
   Runs every authored answer, `accept` form and `wrong[]` value through the real widget code (js/engine/grade.js and the widget files, loaded in a
   small fake DOM) and asserts, per widget:
     key-refused        the authored `answer` does not grade correct (a band that refuses its own key, a form the key does not meet)
     accept-refused     an `accept` form does not grade correct (expression, and text cells of a table)
     wrong-grades-right a `wrong[]` value grades correct (a band that takes a slip; the slip would be marked right)
     wrong-misrouted    a `wrong[]` value is wrong but its key is another line's id (another wrong[] entry's band or form takes it first)
     wrong-unrouted     a `wrong[]` value is wrong but its key is not its own id (the generic miss: its own line never shows)
     choice-key         a choice has not exactly one correct option, or an option does not grade as its own id; multi: the correct set is refused
                        or a single extra wrong pick is accepted
     error              the widget threw
   Covered kinds: expression and numeric (single and set answers), choice, multi, table (answers, text accept forms, cell wrong[]). Fluency sets
   (families with `vars`) are drawn the way tools/fluency-sample.mjs does (--fluency-seeds, default 2 seeds of the set's own n items) and their
   items checked the same way; a wrong draw that coincides with another family wrong id is a note, not a failure (as in tools/test-fluency.mjs).
   NOT covered (the grade needs a real DOM or a canvas, so the browser playthrough is the check): order, tap-regions, place, drag-point, sketch,
   manipulate, balance, slider, sliders, trade (DOM or canvas), code (Pyodide or C++), longform (self-graded rubric). tools/fixtures is skipped.
     node tools/grade-all.mjs [--local-cdn <pkgs>] [--file <json path>]... [--jobs 4] [--shard i/n] [--fluency-seeds 2] [--root <app dir>] [--quiet]
   The Compute Engine comes from --local-cdn (or ZQ_LOCAL_CDN) if given, else from ZQ_CE_URL or the CDN the app itself uses (cached in the temp
   folder), so CI needs no local copy. Output: one line per failure "file#path: kind: detail", then a count per kind. Exit 0 none, 1 failures, 2 setup. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { fork } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const arg = (k, d = null) => { const i = argv.indexOf(k); return i >= 0 && argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[i + 1] : d; };
const args = (k) => argv.flatMap((a, i) => (a === k && argv[i + 1] && !argv[i + 1].startsWith('--') ? [argv[i + 1]] : []));
const ROOT = path.resolve(arg('--root', path.resolve(HERE, '..')));
const CONTENT = path.join(ROOT, 'content');
const die = (m) => { console.error('grade-all: ' + m); process.exit(2); };
const CE_VER = '0.30.2', CE_URL = process.env.ZQ_CE_URL || `https://cdn.jsdelivr.net/npm/@cortex-js/compute-engine@${CE_VER}/dist/compute-engine.min.umd.js`;
const cdnDir = arg('--local-cdn') ? path.resolve(arg('--local-cdn')) : process.env.ZQ_LOCAL_CDN ? path.resolve(process.env.ZQ_LOCAL_CDN) : null;

/* ---------- the Compute Engine source: a local copy, else the network (cached) ---------- */
const ceSource = async () => {
  if (cdnDir) {
    const f = path.join(cdnDir, `cortex-js-compute-engine-${CE_VER}`, 'package', 'dist', 'compute-engine.min.umd.js');
    if (!fs.existsSync(f)) die(`${f} does not exist (give --local-cdn <pkgs> with the local Compute Engine, or leave it out to load from the network)`);
    return f;
  }
  const cache = path.join(os.tmpdir(), `zq-compute-engine-${CE_VER}.umd.js`);
  if (fs.existsSync(cache) && fs.statSync(cache).size > 100000) return cache;
  let text;
  try {
    if (CE_URL.startsWith('file:')) text = fs.readFileSync(new URL(CE_URL), 'utf8');
    else { const r = await fetch(CE_URL); if (!r.ok) throw new Error(`HTTP ${r.status}`); text = await r.text(); }
  } catch (e) { die(`cannot load the Compute Engine from ${CE_URL} (${e.message}); give --local-cdn <pkgs> or set ZQ_CE_URL`); }
  if (text.length < 100000) die(`the Compute Engine from ${CE_URL} is too short to be the library`);
  fs.writeFileSync(cache, text);
  return cache;
};

/* ---------- the fake DOM and the real widget files ---------- */
const stubEl = (html = '') => {
  const memo = new Map();
  const el = {
    _html: html, value: '', hidden: false, textContent: '', innerHTML: '', readOnly: false, className: '', children: [], dataset: {},
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, removeEventListener() {}, setAttribute() {}, getAttribute() { return null; }, append() {}, prepend() {}, focus() {}, remove() {}, insertAdjacentHTML() {},
    querySelector(sel) { if (!memo.has(sel)) memo.set(sel, stubEl()); return memo.get(sel); },   // one element per selector: an input keeps what is typed into it
    querySelectorAll(sel) { return sel === '.opt' ? Array.from({ length: (html.match(/class="opt /g) || []).length }, () => stubEl()) : []; },
  };
  el.parentElement = html ? null : { classList: el.classList };
  return el;
};
const WIDGET_FILES = ['js/engine/grade.js', 'js/engine/widgets/_base.js', 'js/engine/widgets/expression.js', 'js/engine/widgets/numeric.js', 'js/engine/widgets/choice.js', 'js/engine/widgets/multi.js', 'js/engine/widgets/table.js'];
const boot = (ceFile) => {
  const g = { console, setTimeout, clearTimeout, requestAnimationFrame: (f) => f(), document: { addEventListener() {}, querySelector() { return null; }, createElement: () => stubEl(), head: stubEl() }, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g);
  vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
  const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
  g.ZQ = { h: (html) => stubEl(String(html)), esc: (s) => String(s), sound() {}, icon: () => '', mathify() {} };
  for (const f of WIDGET_FILES) vm.runInContext(fs.readFileSync(path.join(ROOT, f), 'utf8'), g, { filename: f });
  g.ZQ.grade.inline = (s) => String(s);
  g.ZQ.grade.maths = () => Promise.resolve({ mathlive: false, ce });
  return g.ZQ.widgets.kinds;
};
const tick = () => new Promise((r) => setTimeout(r, 0));

/* ---------- one widget ---------- */
const fmt = (spec, n) => (spec.unit === '%' ? String(+(+n * 100).toPrecision(15)) : String(+n));   // a percentage is typed as 25 for 0.25; any other value as written
const isSet = (spec) => Array.isArray(spec.answers) && spec.unordered === true;

/* grade one typed value on a fresh widget: { ok, key } */
const typed = async (kinds, spec, text) => {
  const w = kinds[spec.kind](stubEl(), spec, { change() {} });
  w.set(text);
  await tick();
  const r = await w.grade();
  return { ok: !!r.ok, key: r.key == null ? null : r.key };
};
const routeCheck = (fails, what, w, r, ids, coincide) => {
  const id = w.id;
  if (r.ok) fails.push(['wrong-grades-right', `${what} ${JSON.stringify(w.shown)} grades correct`]);
  else if (r.key === id) return;
  else if (r.key != null && ids.includes(r.key)) { if (coincide) coincide.n++; else fails.push(['wrong-misrouted', `${what} ${JSON.stringify(w.shown)} (wrong "${id}") routes to wrong "${r.key}"`]); }
  else fails.push(['wrong-unrouted', `${what} ${JSON.stringify(w.shown)} (wrong "${id}") gives key ${r.key === null ? 'null (the generic miss)' : JSON.stringify(r.key)}`]);
};

const checkTyped = async (kinds, spec, coincide) => {
  const fails = [], set = isSet(spec), ids = (spec.wrong || []).filter((x) => x && x.id != null).map((x) => String(x.id));
  const answerText = spec.kind === 'expression' ? (set ? spec.answers.join(', ') : spec.answer) : (set ? spec.answers.map((a) => fmt(spec, a)).join(', ') : fmt(spec, spec.answer));
  const a = await typed(kinds, spec, answerText);
  if (!a.ok) fails.push(['key-refused', `answer ${JSON.stringify(answerText)} grades wrong (key ${JSON.stringify(a.key)})`]);
  if (spec.kind === 'expression') {
    for (const [i, t] of (spec.accept || []).entries()) {
      if (typeof t !== 'string') continue;
      const r = await typed(kinds, spec, t);
      if (!r.ok) fails.push(['accept-refused', `accept[${i}] ${JSON.stringify(t)} grades wrong (key ${JSON.stringify(r.key)})`]);
    }
  }
  for (const [i, wr] of (spec.wrong || []).entries()) {
    if (!wr) continue;
    const text = spec.kind === 'expression' ? wr.tex : wr.value == null ? null : typeof wr.value === 'string' ? wr.value : fmt(spec, wr.value);
    if (typeof text !== 'string' || /\{\{carry/.test(text)) continue;
    const r = await typed(kinds, spec, text);
    routeCheck(fails, `wrong[${i}]`, { id: wr.id == null ? `#${i}` : String(wr.id), shown: text }, r, ids, coincide);
  }
  return fails;
};

const checkChoice = async (kinds, spec) => {
  const fails = [], opts = spec.options || [], right = opts.filter((o) => o.correct);
  const s = { ...spec, shuffle: false };
  if (spec.kind === 'choice') {
    if (right.length !== 1) fails.push(['choice-key', `${right.length} correct options (a choice needs exactly one)`]);
    for (const o of opts) {
      const w = kinds.choice(stubEl(), s, { change() {} });
      w.set(o.id);
      const r = w.grade();
      if (!!r.ok !== !!o.correct || r.key !== o.id) fails.push(['choice-key', `option "${o.id}" grades ${JSON.stringify({ ok: r.ok, key: r.key })}`]);
      else if (!o.correct && o.why != null && r.line !== o.why) fails.push(['wrong-unrouted', `option "${o.id}" shows another line than its why`]);
    }
    return fails;
  }
  const w = kinds.multi(stubEl(), s, { change() {} });
  w.set(right.map((o) => o.id));
  if (!w.grade().ok) fails.push(['choice-key', `the correct set ${JSON.stringify(right.map((o) => o.id))} is refused`]);
  for (const o of opts.filter((x) => !x.correct)) {
    w.set([...right.map((x) => x.id), o.id]);
    const r = w.grade();
    if (r.ok || r.key !== o.id) fails.push(['wrong-unrouted', `the correct set plus "${o.id}" grades ${JSON.stringify({ ok: r.ok, key: r.key })}`]);
  }
  for (const o of right) {
    w.set(right.filter((x) => x !== o).map((x) => x.id));
    const r = w.grade();
    if (r.ok) fails.push(['wrong-grades-right', `the correct set without "${o.id}" grades correct`]);
  }
  return fails;
};

const checkTable = async (kinds, spec) => {
  const fails = [], cells = [];
  (spec.rows || []).forEach((row, i) => row.forEach((c, j) => { if (c && typeof c === 'object' && c.edit) cells.push({ id: `r${i}c${j}`, c }); }));
  const shown = (c) => (typeof c.answer === 'string' ? c.answer : fmt(c, c.answer));
  const base = Object.fromEntries(cells.map(({ id, c }) => [id, shown(c)]));
  const grade = async (vals) => { const w = kinds.table(stubEl(), spec, { change() {} }); w.set(vals); await tick(); return w.grade(); };
  if (!cells.length) return fails;
  const a = await grade(base);
  if (!a.ok) fails.push(['key-refused', `the answers grade wrong (cells ${JSON.stringify(a.detail.wrong)})`]);
  for (const { id, c } of cells) {
    for (const [i, t] of (Array.isArray(c.accept) ? c.accept : []).entries()) {
      if (typeof t !== 'string' || typeof c.answer !== 'string') continue;
      const r = await grade({ ...base, [id]: t });
      if (!r.ok) fails.push(['accept-refused', `${id} accept[${i}] ${JSON.stringify(t)} grades wrong`]);
    }
    const wrongs = Array.isArray(c.wrong) ? c.wrong : [];
    const ids = wrongs.filter((x) => x && x.id != null).map((x) => String(x.id));
    for (const [i, wr] of wrongs.entries()) {
      if (!wr) continue;
      const text = wr.text != null ? String(wr.text) : wr.value != null ? (c.unit === '%' ? String(+(+wr.value * 100).toPrecision(15)) : String(wr.value)) : null;
      if (text == null) continue;
      const r = await grade({ ...base, [id]: text });
      routeCheck(fails, `${id} wrong[${i}]`, { id: String(wr.id), shown: text }, { ok: !!r.ok, key: r.key }, ids);
    }
  }
  return fails;
};

const checkWidget = async (kinds, job) => {
  const { spec } = job;
  try {
    if (spec.kind === 'expression' || spec.kind === 'numeric') return await checkTyped(kinds, spec, job.coincide);
    if (spec.kind === 'choice' || spec.kind === 'multi') return await checkChoice(kinds, spec);
    if (spec.kind === 'table') return await checkTable(kinds, spec);
  } catch (e) { return [['error', String(e && e.message || e).split('\n')[0].slice(0, 120)]]; }
  return [];
};

/* ---------- collecting the widgets ---------- */
const walk = (d, out = []) => { for (const e of fs.readdirSync(d, { withFileTypes: true })) { const p = path.join(d, e.name); if (e.isDirectory()) walk(p, out); else if (e.name.endsWith('.json') && e.name !== 'manifest.json') out.push(p); } return out; };
const COVERED = new Set(['expression', 'numeric', 'choice', 'multi', 'table']);
const gradeable = (v) => {
  if (v.kind === 'expression') return typeof v.answer === 'string' || Array.isArray(v.answers);
  if (v.kind === 'numeric') return v.answer != null || Array.isArray(v.answers);
  if (v.kind === 'choice' || v.kind === 'multi') return Array.isArray(v.options);
  if (v.kind === 'table') return Array.isArray(v.rows);
  return false;
};
const collect = (only, seeds) => {
  const jobs = [], skipped = { carry: 0, template: 0 };
  let files = only.length ? only.map((f) => path.resolve(f)) : walk(CONTENT).sort();
  const sh = /^(\d+)\/(\d+)$/.exec(arg('--shard', ''));
  if (arg('--shard') && (!sh || +sh[1] < 1 || +sh[1] > +sh[2])) die('--shard needs i/n with 1 <= i <= n');
  if (sh) files = files.filter((_, i) => i % +sh[2] === +sh[1] - 1);   // every n-th file, so shards 1/n to n/n cover each file once
  const gen = seeds > 0 ? createRequire(import.meta.url)(path.join(ROOT, 'js/engine/gen.js')) : null;
  for (const file of files) {
    let data; try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch (e) { if (only.length) die(`${file}: ${e.message}`); continue; }
    const rel0 = path.relative(CONTENT, file), rel = rel0.startsWith('..') ? path.relative(process.cwd(), file) : rel0;   // a file outside content (a fixture) is named from the working folder
    if (/(^|[\\/])tools[\\/]fixtures[\\/]/.test(path.relative(ROOT, file)) && !only.length) continue;   // test fixtures are not content
    const add = (v, p, host, label) => jobs.push({ file: label, path: p, spec: v, host });
    const go = (v, p, host) => {
      if (Array.isArray(v)) return v.forEach((x, i) => go(x, `${p}[${i}]`, host));
      if (!v || typeof v !== 'object') return;
      if (v.vars && typeof v.vars === 'object' && !Array.isArray(v.vars)) { skipped.template++; return; }   // a Fluency family is a template, drawn below
      const h = v.feedback && typeof v.feedback === 'object' ? v : host;
      if (COVERED.has(v.kind) && gradeable(v)) {
        if (typeof v.answer === 'string' && /\{\{carry/.test(v.answer)) skipped.carry++;   // a carried value, known only when the learner reaches it
        else add(v, p, h, rel);
      }
      Object.entries(v).forEach(([k, x]) => go(x, p ? `${p}.${k}` : k, h));
    };
    go(data, '', null);
    if (gen && data && Array.isArray(data.families) && data.id) {   // a generated Fluency set: items drawn as a learner meets them
      for (let s = 1; s <= seeds; s++) {
        let items;
        try { items = gen.generate(data, s, { n: data.n }); } catch (e) { jobs.push({ file: rel, path: `fluency seed ${s}`, spec: null, error: String(e.message).slice(0, 100) }); continue; }
        items.forEach((it, k) => { const pi = gen.playerItem(it, data, k); if (COVERED.has(pi.widget.kind) && gradeable(pi.widget)) jobs.push({ file: rel, path: `fluency seed ${s} item ${k + 1} (${it.family})`, spec: pi.widget, host: pi, generated: true }); });
      }
    }
  }
  return { jobs, skipped };
};

/* ---------- worker and master ---------- */
const tail = (s) => (s.length > 160 ? s.slice(0, 157) + '...' : s);
if (process.env.ZQ_GA_WORKER) {
  const kinds = boot(process.env.ZQ_GA_CE);
  process.on('message', async (m) => {
    const out = [], notes = { coincide: 0 };
    for (const j of m.jobs) {
      if (!j.spec) { out.push({ file: j.file, path: j.path, kind: 'error', detail: j.error }); continue; }
      const co = { n: 0 };
      const fails = await checkWidget(kinds, { spec: j.spec, coincide: j.generated ? co : null });
      notes.coincide += co.n;
      for (const [kind, detail] of fails) {
        out.push({ file: j.file, path: j.path, kind, detail: tail(detail) });
      }
    }
    process.send({ out, notes, n: m.jobs.length }, () => process.exit(0));
  });
} else {
  const only = args('--file'), nJobs = Math.max(1, +arg('--jobs', 4)), seeds = Math.max(0, +arg('--fluency-seeds', 2));
  const quiet = argv.includes('--quiet');
  const t0 = Date.now();
  const ce = await ceSource();
  const { jobs, skipped } = collect(only, seeds);
  if (only.length && !jobs.length) console.log('grade-all: note: no covered widget in the named files');
  const slices = Array.from({ length: Math.min(nJobs, Math.max(1, jobs.length)) }, () => []);
  jobs.forEach((j, i) => slices[i % slices.length].push(j));
  const fails = []; let widgets = 0, coincide = 0, left = slices.length;
  const byKind = {};
  jobs.forEach((j) => { if (j.spec) byKind[j.spec.kind] = (byKind[j.spec.kind] || 0) + 1; });
  const finish = () => {
    fails.sort((a, b) => (a.file + a.path).localeCompare(b.file + b.path));
    fails.forEach((f) => console.log(`${f.file}#${f.path}: ${f.kind}: ${f.detail}`));
    const counts = {}; fails.forEach((f) => { counts[f.kind] = (counts[f.kind] || 0) + 1; });
    if (!quiet || fails.length) console.log(`grade-all: ${widgets} widgets checked (${Object.entries(byKind).map(([k, n]) => `${k} ${n}`).join(', ')}), ${skipped.carry} carried answers and ${skipped.template} Fluency family templates (drawn at ${seeds} seeds instead)${coincide ? `, ${coincide} coinciding Fluency draws noted` : ''}, ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    console.log(fails.length ? `grade-all: ${fails.length} failure${fails.length === 1 ? '' : 's'}: ${Object.entries(counts).map(([k, n]) => `${k} ${n}`).join(', ')}` : 'grade-all: 0 failures');
    process.exit(fails.length ? 1 : 0);
  };
  if (!jobs.length) finish();
  slices.forEach((s) => {
    const c = fork(fileURLToPath(import.meta.url), argv, { env: { ...process.env, ZQ_GA_WORKER: '1', ZQ_GA_CE: ce } });
    c.on('message', (m) => { fails.push(...m.out); widgets += m.n; coincide += m.notes.coincide; });
    c.on('exit', () => { if (--left === 0) finish(); });
    c.send({ jobs: s });
  });
}
