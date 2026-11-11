/* Delta read, session AA: follow-up to review (d) finding A8.
   The expression grader reads only the real part of a value, so two expressions that are pure imaginary at every sample
   point (a root or a fractional power of something negative for 0.3 < symbol < 3) compare equal whatever their size.
   This scan asks, for every `expression` widget in app/content: does twice the answer grade as equal to the answer?
   A hit is an item where a wrong answer would be marked right.
   Usage (from the repo root): node docs/reviews/delta-session-aa-scripts/expr_scale_scan.mjs <pkgs> */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const cdn = path.resolve(process.argv[2]);
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const C = g.ComputeEngine.ComputeEngine || g.ComputeEngine, ce = new C();
g.ZQ = {};
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const files = [];
const walkDir = (d) => { for (const f of fs.readdirSync(d)) { const p = path.join(d, f); if (fs.statSync(p).isDirectory()) walkDir(p); else if (f.endsWith('.json')) files.push(p); } };
walkDir('app/content');
let n = 0, skipped = 0; const hits = [];
const visit = (o, file, trail) => {
  if (Array.isArray(o)) { o.forEach((v, i) => visit(v, file, trail)); return; }
  if (!o || typeof o !== 'object') return;
  const here = o.id ? trail + '/' + o.id : trail;
  if (o.kind === 'expression' && typeof o.answer === 'string') {
    const a = o.answer;
    if (/[=<>]|\\le|\\ge|\\ne|\\begin|,/.test(a)) skipped++;      // relations, vectors and matrices are another path
    else {
      n++;
      const opts = { functions: o.functions, integers: o.integers };
      let same = false, zero = false;
      try { same = !!G.exprEqual(ce, a, `2\\left(${a}\\right)`, opts); zero = !!G.exprEqual(ce, a, '0', opts); } catch { same = false; }
      if (same && !zero) hits.push(`${file} ${here} | ${a}`);
    }
  }
  for (const k of Object.keys(o)) visit(o[k], file, here);
};
for (const f of files) { let j; try { j = JSON.parse(fs.readFileSync(f, 'utf8')); } catch { continue; } visit(j, f.replace('app/content/', ''), ''); }
console.log(`expression answers tried: ${n} (skipped ${skipped} relations, vectors or lists)`);
console.log(`answers that grade equal to twice themselves: ${hits.length}`);
hits.slice(0, 40).forEach(h => console.log('  ' + h));
