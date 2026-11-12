#!/usr/bin/env node
/* Tries the content fixes of review-problems-complex-1-3.md on in-memory copies, with the engine's own graders.
   Nothing is written. node docs/reviews/review-problems-complex-1-3-scripts/try-fix.mjs --local-cdn <pkgs>   (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || null }; };
const expr = (w, t) => { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; };
const sets = Object.fromEntries([1, 2, 3].map(n => [n, JSON.parse(fs.readFileSync(`app/content/courses/complex/problems-${n}.json`, 'utf8'))]));
const W = (n, id, k) => JSON.parse(JSON.stringify(sets[n].items.find(x => x.id === id).parts[k - 1].widget));
let checks = 0, fails = 0;
const want = (w, text, exp, what) => {
  const r = (w.kind === 'numeric' ? num : expr)(w, text); checks++;
  const good = exp === true ? r.ok : (!r.ok && r.key === exp);
  if (!good) fails++;
  console.log(`${good ? 'ok   ' : 'FAIL '} ${what}: "${text}" -> ${r.ok ? 'accepted' : 'refused on ' + r.key} (wanted ${exp === true ? 'accepted' : 'refused on ' + exp})`);
};
const T = true;

{ // finding 3
  const w = W(1, 'p-neutral-wire', 1);
  w.wrong.find(x => x.id === 'swapped').value = -6;
  w.wrong.push({ id: 'real-size', value: 6, tol: { abs: 0 } });
  for (const [t, e] of [['10.392', T], ['-6', 'swapped'], ['6', 'real-size'], ['0.866', 'unscaled'], ['0.439', 'degrees']]) want(w, t, e, 'finding 3 wire 1');
}
{ // finding 5
  for (const [n, id, k, d, key] of [[1, 'p-turning-frames', 3, '30', '\\frac{\\pi}{6}'], [1, 'p-four-lamps', 2, '120', '\\frac{2\\pi}{3}'], [2, 'p-log-branches', 2, '150', '\\frac{5\\pi}{6}']]) {
    const w = W(n, id, k);
    w.wrong.push({ id: 'degrees', tex: d });
    want(w, key, T, `finding 5 ${id} ${k}`); want(w, d, 'degrees', `finding 5 ${id} ${k}`);
    for (const x of w.wrong.slice(0, -1)) want(w, x.tex, x.id, `finding 5 ${id} ${k}`);
  }
}
{ // finding 7
  const w = W(2, 'p-mesh-map', 1);
  w.wrong.push({ id: 'no-cross', tex: '-12.75-12i' });
  for (const [t, e] of [['-12.75+3i', T], ['-12.75-12i', 'no-cross'], ['-3.75-3i', 'square-parts'], ['5.25+3i', 'i-squared']]) want(w, t, e, 'finding 7 mesh 1');
}
{ // finding 11
  const w = W(3, 'p-traffic-island', 5);
  w.tol = { abs: 0.005 }; w.wrong.find(x => x.id === 'sign').tol = { abs: 0.005 };
  for (const [t, e] of [['0.5', T], ['0.50', T], ['1/2', T], ['0.45', null], ['0.55', null], ['1', 'no-two'], ['-0.5', 'sign']]) want(w, t, e, 'finding 11 island 5');
}
{ // finding 12
  const w = W(3, 'p-share-moments', 4);
  const v = w.wrong.find(x => x.id === 'variance'); v.value = 227.47; v.tol = { abs: 0.08 };
  w.wrong.push({ id: 'own-rounding', value: 15.1, tol: { abs: 0.005 } });
  for (const [t, e] of [['15.08', T], ['15.083', T], ['15.081', T], ['15.10', 'own-rounding'], ['15.1', 'own-rounding'], ['227.44', 'variance'], ['227.50', 'variance'], ['227.4', 'variance'], ['67.81', 'not-squared'], ['14.31', 'log-sd'], ['228.11', null]]) want(w, t, e, 'finding 12 share 4');
}
{ // finding 14: the lighthouse renumbered (2.5 km out, opposite the point 0.5 km along)
  const p1 = W(3, 'p-lighthouse-flashes', 1);
  Object.assign(p1, { answer: '0.5+2.5i', accept: ['0.5+2.5i', '\\frac{1}{2}+\\frac{5}{2}i', '2.5i+0.5'], wrong: [{ id: 'lower', tex: '0.5-2.5i' }, { id: 'minus-b', tex: '-0.5+2.5i' }, { id: 'no-four', tex: '1+5i' }] });
  for (const [t, e] of [['0.5+2.5i', T], ['\\frac{1}{2}+\\frac{5}{2}i', T], ['\\frac12+\\frac{5i}{2}', T], ['0.5-2.5i', 'lower'], ['-0.5+2.5i', 'minus-b'], ['1+5i', 'no-four'], ['\\frac{1+5i}{2}', 'form']]) want(p1, t, e, 'finding 14 part 1');
  const p2 = W(3, 'p-lighthouse-flashes', 2);
  Object.assign(p2, { answer: '-\\frac{1}{10}i', accept: ['-\\frac{1}{10}i', '-\\frac{i}{10}', '-0.1i'], wrong: [{ id: 'no-i', tex: '\\frac{1}{10}' }, { id: 'plus', tex: '\\frac{1}{10}i' }, { id: 'q-prime', tex: '\\frac{1}{52}-\\frac{5}{52}i' }] });
  for (const [t, e] of [['-\\frac{1}{10}i', T], ['-\\frac{i}{10}', T], ['-0.1i', T], ['0.1', 'no-i'], ['0.1i', 'plus'], ['\\frac{1}{52}-\\frac{5}{52}i', 'q-prime'], ['\\frac{1}{10i}', 'form']]) want(p2, t, e, 'finding 14 part 2');
  const p3 = W(3, 'p-lighthouse-flashes', 3);
  Object.assign(p3, { answer: 1.592, wrong: [{ id: 'integral', value: 0.628, tol: { abs: 0.001 } }, { id: 'both-poles', value: 0.796, tol: { abs: 0.001 } }, { id: 'no-two', value: 3.183, tol: { abs: 0.001 } }] });
  for (const [t, e] of [['1.592', T], ['1.5915', T], ['0.628', 'integral'], ['0.796', 'both-poles'], ['3.183', 'no-two'], ['1.59', null]]) want(p3, t, e, 'finding 14 part 3');
  const p4 = W(3, 'p-lighthouse-flashes', 4);
  Object.assign(p4, { answer: 0.0821, wrong: [{ id: 'sign', value: 12.1825, tol: { abs: 0.001 } }, { id: 'no-c', value: 0.0516, tol: { abs: 0.0001 } }, { id: 'standard', value: 0.3679, tol: { abs: 0.0001 } }] });
  for (const [t, e] of [['0.0821', T], ['0.08208', T], ['12.1825', 'sign'], ['12.182', 'sign'], ['0.0516', 'no-c'], ['0.3679', 'standard'], ['0.08', null]]) want(p4, t, e, 'finding 14 part 4');
  const p5 = W(3, 'p-lighthouse-flashes', 5);
  Object.assign(p5, { answer: 0.0821, wrong: [{ id: 'no-half', value: 0.0067, tol: { abs: 0.0001 } }, { id: 'one-factor', value: 0.2865, tol: { abs: 0.0001 } }] });
  for (const [t, e] of [['0.0821', T], ['0.0067', 'no-half'], ['0.2865', 'one-factor'], ['0.3', null]]) want(p5, t, e, 'finding 14 part 5');
}
console.log(`try-fix: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
