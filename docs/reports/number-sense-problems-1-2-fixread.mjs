// Fix-pass read probe: the 18 decimal-low / decimal-high slips of number-sense problems-1, on the real numeric grader (js/engine/grade.js numGrade).
import fs from 'fs'; import vm from 'vm'; import path from 'path';
const APP = path.resolve(process.argv[2] || 'app');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; }, createElement: () => ({}), head: {} }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { esc: (s) => String(s) };
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
const d = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/number-sense/problems-1.json'), 'utf8'));
// exact keys, derived here from the questions, not read from the file
const EX = { '1.0': [25, 6], '1.2': [1, 30], '2.0': [17, 24], '2.1': [7, 24], '2.2': [7, 9], '2.3': [320, 3], '3.2': [1, 3], '3.3': [31, 48], '3.4': [31, 72] };
let bad = 0, rows = 0, holes = 0; const fail = (m) => { bad++; console.log('FAIL', m); };
const gr = (spec, t) => { const r = G.numGrade(spec, String(t)); return r.ok ? 'OK' : (r.key ?? 'generic'); };
for (const [k, [n, q]] of Object.entries(EX)) {
  const [i, j] = k.split('.').map(Number), part = d.items[i].parts[j], spec = part.widget, x = n / q;
  const lo = spec.wrong.find(w => w.id === 'decimal-low'), hi = spec.wrong.find(w => w.id === 'decimal-high');
  if (!lo || !hi) { fail(k + ' no slips'); continue; }
  rows += 2;
  // integer arithmetic for 2 d.p. cut and round-up
  const cut2 = Math.floor(n * 100 / q) / 100, up2 = cut2 + 0.01, rnd2 = Math.round(n * 100 / q) / 100;
  const cut3 = Math.floor(n * 1000 / q) / 1000, rnd3 = Math.round(n * 1000 / q) / 1000, up3 = cut3 + 0.001;
  const cut1 = Math.floor(n * 10 / q) / 10, rnd1 = Math.round(n * 10 / q) / 10;
  if (Math.abs(spec.answer - x) > 5e-7) fail(k + ' answer not the 6 d.p. key');
  const kL = spec.answer - spec.tol.abs, kH = spec.answer + spec.tol.abs;
  const lL = lo.value - lo.tol.abs, lH = lo.value + lo.tol.abs, hL = hi.value - hi.tol.abs, hH = hi.value + hi.tol.abs;
  // band geometry: low = [cut2, key low), high = (key high, up2]
  if (Math.abs(lL - cut2) > 1e-9) fail(k + ' low band does not start at cut2 ' + lL + ' ' + cut2);
  if (Math.abs(hH - up2) > 1e-9) fail(k + ' high band does not end at up2');
  if (!(lH < kL - 2e-9)) fail(k + ' low band overlaps key');
  if (!(hL > kH + 2e-9)) fail(k + ' high band overlaps key');
  if (kL - lH > 3e-6 || hL - kH > 3e-6) fail(k + ' gap between band and key wider than 3e-6: ' + (kL - lH) + ' ' + (hL - kH));
  // no other slip inside either band (with its own tolerance)
  for (const w of spec.wrong) if (!/^decimal-/.test(w.id)) {
    const a = w.value - (w.tol?.abs ?? 0), b = w.value + (w.tol?.abs ?? 0);
    if (!(b < lL - 1e-9 || a > hH + 1e-9)) fail(k + ' slip ' + w.id + ' touches the bands');
  }
  // real grader
  const f = (v, dp) => v.toFixed(dp);
  const exp = (t, want) => { const got = gr(spec, t); if (got !== want) fail(`${k} typed ${t}: ${got}, expected ${want}`); return `${t}->${got}`; };
  const out = [];
  out.push(exp(`${n}/${q}`, 'OK'));
  if (n > q) out.push(exp(`${Math.floor(n / q)} ${n % q}/${q}`, 'OK'));
  out.push(exp(`${2 * n}/${2 * q}`, 'OK'));
  out.push(exp(f(rnd3, 3), 'OK'));                       // 3-place rounded is inside the 0.0005 window by construction
  const c3 = gr(spec, f(cut3, 3)); out.push(`${f(cut3, 3)}->${c3}`);
  if (Math.abs(cut3 - rnd3) > 1e-9 && c3 !== 'decimal-low') fail(k + ' 3-place cut not decimal-low: ' + c3);
  const u3 = gr(spec, f(up3, 3)); out.push(`${f(up3, 3)}->${u3}`);
  if (Math.abs(up3 - rnd3) > 1e-9 && u3 !== 'decimal-high') fail(k + ' 3-place up not decimal-high: ' + u3);
  out.push(exp(f(cut2, 2), 'decimal-low'));
  out.push(exp(f(up2, 2), 'decimal-high'));
  out.push(exp(f(rnd2, 2), rnd2 === cut2 ? 'decimal-low' : 'decimal-high'));
  out.push(exp(f(cut2, 2) + '5', gr(spec, f(cut2, 2) + '5')));   // informational
  for (const v of [cut1, rnd1]) out.push(`${f(v, 1)}->${gr(spec, f(v, 1))}`);
  // just outside the bands: generic or another slip, never decimal-*
  for (const v of [cut2 - 0.001, up2 + 0.001, cut2 - 0.01, up2 + 0.01]) { const r = gr(spec, v.toFixed(3)); if (/^decimal-|OK/.test(r)) fail(k + ' outside value ' + v.toFixed(3) + ' gives ' + r); }
  // band edges on the grader
  for (const [v, want] of [[lH, 'decimal-low'], [hL, 'decimal-high'], [kL, 'OK'], [kH, 'OK']]) { const r = gr(spec, v.toFixed(6)); if (r !== want) fail(`${k} edge ${v.toFixed(6)}: ${r}, expected ${want}`); }
  // a fine sweep cut2-0.005 .. up2+0.005 in 1e-6 steps: each value has exactly the class the geometry says, no value matches two entries
  for (let s = Math.round((cut2 - 0.005) * 1e6); s <= Math.round((up2 + 0.005) * 1e6); s++) {
    const v = s / 1e6, hits = spec.wrong.filter(w => G.within(v, +w.value, w.tol)).map(w => w.id), ok = G.within(v, +spec.answer, spec.tol);
    if (hits.length > 1 || (ok && hits.length)) fail(`${k} ${v} matches ${ok ? 'key and ' : ''}${hits}`);
    const inR = v >= cut2 - 1e-9 && v <= up2 + 1e-9;
    if (inR && !ok && !hits.length) { holes++; if (Math.min(Math.abs(v - kL), Math.abs(v - kH)) > 2.5e-6) fail(k + ' ' + v + ' inside [cut2, up2] falls to generic'); else console.log('   note: ' + k + ' typed ' + v + ' sits in a 1e-6 seam between band and key and gets the generic line'); }
    if (!inR && (ok || hits.some(h => /^decimal-/.test(h)))) fail(`${k} ${v} outside [cut2, up2] is caught`);
  }
  // the lines: say the decimal is not exact and name the exact key
  const fb = part.feedback.byKey;
  for (const id of ['decimal-low', 'decimal-high']) { if (!fb[id] || !fb[id].startsWith('Your method is right')) fail(k + ' no line for ' + id); }
  // "not exact": q has a prime factor other than 2 and 5, so n/q has no terminating decimal
  let r = q; for (const p of [2, 5]) while (r % p === 0) r /= p;
  const gcd = (a, b) => (b ? gcd(b, a % b) : a);
  if (gcd(n, q) !== 1 || r === 1) fail(k + ' key terminates, the line would be false');
  console.log(`${k} ${n}/${q}=${x.toFixed(7)} key[${kL.toFixed(6)},${kH.toFixed(6)}] low[${lL.toFixed(6)},${lH.toFixed(6)}] high[${hL.toFixed(6)},${hH.toFixed(6)}] cut2 ${f(cut2, 2)} up2 ${f(up2, 2)} rnd2 ${f(rnd2, 2)}\n   ${out.join(' ')}`);
}
console.log(`${rows} slips checked, ${holes} one-in-a-million seam values, ${bad} failures`);
process.exit(bad ? 1 : 0);
