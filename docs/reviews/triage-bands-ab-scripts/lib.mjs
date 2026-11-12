/* Shared helpers for the band triage (docs/reviews/triage-bands-ab.md).
   boot() loads the real grader exactly as app/tools/grade-regression.mjs does (grade.js, widgets/expression.js, widgets/numeric.js in a stub DOM,
   the Compute Engine from the local pkgs folder), so every probe here is graded by the app's own code. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

export const HERE = path.dirname(fileURLToPath(import.meta.url));
export const REPO = path.resolve(HERE, '..', '..', '..');
export const APP = path.join(REPO, 'app');
export const OUT = path.join(HERE, 'out');
fs.mkdirSync(OUT, { recursive: true });

const stubEl = () => {
  const el = { value: '', hidden: false, textContent: '', innerHTML: '', readOnly: false, className: '', children: [],
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    addEventListener() {}, removeEventListener() {}, setAttribute() {}, getAttribute() { return null; }, append() {}, prepend() {}, focus() {}, remove() {},
    querySelector() { return stubEl(); }, querySelectorAll() { return []; } };
  return el;
};
export const boot = (cdn) => {
  const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
  if (!fs.existsSync(ceFile)) { console.error('give the pkgs folder (local Compute Engine) as ZQ_LOCAL_CDN or --local-cdn'); process.exit(2); }
  const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; }, createElement: stubEl, head: stubEl() }, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g);
  vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
  const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
  const reg = {};
  g.ZQ = { h: () => stubEl(), esc: (s) => String(s), widgets: { register: (k, f) => { reg[k] = f; }, dataPanel: () => null }, mathify() {} };
  for (const f of ['js/engine/grade.js', 'js/engine/widgets/expression.js', 'js/engine/widgets/numeric.js']) vm.runInContext(fs.readFileSync(path.join(APP, f), 'utf8'), g, { filename: f });
  g.ZQ.grade.maths = () => Promise.resolve({ mathlive: false, ce });
  return { reg, ce, g };
};
export const gradeText = async (reg, spec, text) => {
  const host = stubEl(), ctx = { change() {} };
  try {
    const api = reg[spec.kind](host, spec, ctx);
    api.set(String(text));
    await new Promise((r) => setTimeout(r, 0));
    const r = await api.grade();
    return { ok: !!r.ok, key: r.key || null };
  } catch (e) { return { ok: null, key: 'ERROR ' + String(e.message).slice(0, 60) }; }
};
export const cdnArg = () => { const i = process.argv.indexOf('--local-cdn'); return i >= 0 ? process.argv[i + 1] : process.env.ZQ_LOCAL_CDN; };

/* "quiz[3].widget" or ".problems[0].parts[2].widget" -> the object, and the chain of its ancestors (nearest last) */
export const resolve = (data, p) => {
  const toks = [...String(p).matchAll(/\.?([A-Za-z_][\w-]*)|\[(\d+)\]/g)].map(m => m[1] ?? +m[2]);
  const chain = [data]; let v = data;
  for (const t of toks) { if (v == null) return { node: undefined, chain }; v = v[t]; chain.push(v); }
  return { node: v, chain };
};
/* the item that holds the widget: nearest ancestor with a question, prompt or text of its own */
export const holder = (chain) => {
  for (let i = chain.length - 2; i >= 0; i--) { const a = chain[i]; if (a && typeof a === 'object' && !Array.isArray(a) && (a.question || a.prompt || a.q || a.text || a.stem)) return a; }
  return chain[Math.max(0, chain.length - 2)] || {};
};
export const itemId = (chain) => { for (let i = chain.length - 1; i >= 0; i--) { const a = chain[i]; if (a && typeof a === 'object' && !Array.isArray(a) && typeof a.id === 'string') return a.id; } return ''; };
export const qText = (h) => String(h.question || h.prompt || h.q || h.text || h.stem || '');
export const course = (file) => { const m = /content\/(courses\/[^/]+|exams|[^/]+)/.exec(file); return m ? m[1].replace(/^courses\//, '') : file; };
export const short = (s, n = 160) => { s = String(s ?? '').replace(/\s+/g, ' ').trim(); return s.length > n ? s.slice(0, n - 1) + '~' : s; };
export const num = (x) => String(+(+x).toPrecision(10));
export const halfWidth = (ans, tol) => Math.max(tol && tol.abs != null ? +tol.abs : 0, tol && tol.rel != null ? Math.abs(ans) * +tol.rel : 0);
export const readJson = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));
