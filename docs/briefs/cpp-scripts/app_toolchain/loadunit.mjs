import fs from 'fs';
import vm from 'vm';
const src = fs.readFileSync(new URL('../../../../app/js/engine/widgets/cpp-grade.js', import.meta.url), 'utf8')
  .replace('/* ---------- Reading results ---------- */', 'window.__unit = unit; window.__lit = lit;\n/* ---------- Reading results ---------- */');
const window = { ZQ: new Proxy({}, { get: (t, k) => t[k] ?? (() => {}), set: (t, k, v) => { t[k] = v; return true; } }) };
const ctx = { window, document: new Proxy({}, { get: () => () => ({}) }), console, setTimeout, clearTimeout, navigator: {}, location: {}, localStorage: {}, performance: { now: () => 0 }, Worker: class {}, URL, Blob: class {}, fetch: () => {}, ResizeObserver: class {}, requestAnimationFrame: () => {} };
vm.createContext(ctx);
try { vm.runInContext(src, ctx); } catch (e) { console.error('load error', e.message); }
export const unit = window.__unit;
