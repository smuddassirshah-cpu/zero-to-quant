// Fix-pass read probe: integrals r3 accept lines against the real numGrade / within in app/js/engine/grade.js
import fs from 'node:fs'; import vm from 'node:vm';
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; }, createElement: () => ({}), head: {} }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g); g.ZQ = {};
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const B = 'app/content/courses/integrals/';
const E = Math.E, ln = Math.log;
// exact values recomputed here, independent of the stored answers; [file, item, part, exact, t, example, exact-form texts]
const rows = [
  ['problems-1', 2, 3, 8 / 3 - 8, 0.005, '-5.33', ['-16/3']],
  ['problems-1', 2, 4, -3 - (8 / 3 - 8), 0.005, '2.33', ['7/3']],
  ['problems-2', 0, 3, 8 / 3 - 12 + 16, 0.0005, '6.667', ['20/3']],
  ['problems-2', 1, 3, 2 * ln(4), 0.005, '2.77', []],
  ['problems-2', 2, 1, (1.5 ** 2 / 2 + 4.5 - 2 * 1.5 ** 3 / 3) - (0.5 - 3 + 2 / 3), 0.0005, '5.208', ['125/24']],
  ['problems-2', 2, 2, (-2 / 3 - 0.5 + 3) - (-16 / 3 - 2 + 6), 0.0005, '3.167', ['19/6']],
  ['problems-3', 0, 3, Math.sqrt(99), 0.005, '9.95', []],
  ['problems-3', 2, 1, (1.5 * ln(1.5) - 1.5) - (0.5 * ln(0.5) - 0.5), 0.00005, '-0.0452', []],
  ['problems-3', 2, 2, 0.0267 / 16, 0.00005, '0.0017', []],
  ['problems-3', 3, 1, 4 * (1 - E ** -2), 0.0005, '3.459', []],
  ['problems-3', 3, 2, 1 - E ** -2, 0.0005, '0.865', []],
];
let bad = 0;
const say = (ok, msg) => { if (!ok) bad++; console.log((ok ? 'ok   ' : 'FAIL ') + msg); };
for (const [f, i, p, exact, t, ex, forms] of rows) {
  const spec = JSON.parse(fs.readFileSync(B + f + '.json', 'utf8')).items[i].parts[p].widget;
  const id = `${f} items[${i}].parts[${p}]`;
  say(Math.abs(spec.answer - exact) < 1e-12, `${id} stored answer ${spec.answer} = recomputed ${exact}`);
  say(spec.tol && spec.tol.abs === t && spec.accept.includes(`within ${t.toFixed(String(t).includes('e') ? 5 : String(t).length - 2)} of`), `${id} stated t ${t} = tol.abs ${spec.tol.abs}`);
  say(spec.accept.includes(ex) && G.numGrade(spec, ex).ok, `${id} example ${ex} accepted (off by ${Math.abs(+ex - exact).toExponential(2)})`);
  for (const s of forms) say(G.numGrade(spec, s).ok, `${id} exact form ${s} accepted`);
  // the promise "a decimal within t of exact" against the grader: decimals just inside accepted, just outside refused
  const dp = 9, r = (x) => x.toFixed(dp);
  const inside = [exact + t - 2e-9, exact - t + 2e-9, exact + t * 0.5, exact - t * 0.5, exact];
  const outside = [exact + t + 2e-9, exact - t - 2e-9, exact + 2 * t, exact - 2 * t];
  say(inside.every(x => G.numGrade(spec, r(x)).ok), `${id} decimals inside the band accepted`);
  say(outside.every(x => !G.numGrade(spec, r(x)).ok), `${id} decimals outside the band refused`);
  // random sweep: grader verdict equals |x - exact| <= t for decimals typed to 7 places (away from the 1e-9 edge)
  let mism = 0;
  for (let k = 0; k < 4000; k++) { const x = +(exact + (Math.random() * 6 - 3) * t).toFixed(7); if (Math.abs(Math.abs(x - exact) - t) < 1e-8) continue; if (G.numGrade(spec, x.toFixed(7)).ok !== (Math.abs(x - exact) <= t)) mism++; }
  say(mism === 0, `${id} sweep of 4000 decimals: grader = |x - exact| <= t`);
  // no wrong[] band reaches into the promised band
  say((spec.wrong || []).every(w => Math.abs(+w.value - exact) > t + (w.tol?.abs ?? 0)), `${id} no wrong[] band overlaps`);
}
// the one terminating exact value: decimals exactly on the boundary
const s9 = JSON.parse(fs.readFileSync(B + 'problems-3.json', 'utf8')).items[2].parts[2].widget;
for (const x of ['0.00171875', '0.00161875', '0.0016', '0.0018', '0.00167', '0.001668']) console.log('edge  problems-3 items[2].parts[2]', x, G.numGrade(s9, x).ok);
// l10 quiz[3]
const q = JSON.parse(fs.readFileSync(B + 'l10-undo-product.json', 'utf8')).quiz[3];
const F = (x) => x * ln(x) - x;
say(Math.abs(F(E) - F(1) - 1) < 1e-12, 'l10 quiz[3] integral = 1');
say(Math.abs(E * ln(E) - 1 * ln(1) - E) < 1e-12, 'l10 slip [x ln x]_1^e = e');
say(Math.abs((E * ln(E) - 0) - (E - 1) - 1) < 1e-12, 'l10 e - (e - 1) = 1');
let N = 2e6, sum = 0; for (let k = 0; k < N; k++) sum += ln(1 + (k + 0.5) * (E - 1) / N); sum *= (E - 1) / N;
say(Math.abs(sum - 1) < 1e-9, `l10 midpoint sum of ln x on [1, e] = ${sum.toFixed(10)}`);
for (const x of ['2.7183', '2.718', 'e', '1', '0']) { const r = G.numGrade(q.widget, x); console.log('l10  ', x, JSON.stringify({ ok: r.ok, key: r.key })); }
console.log(bad ? `${bad} FAIL` : 'all ok'); process.exit(bad ? 1 : 0);
