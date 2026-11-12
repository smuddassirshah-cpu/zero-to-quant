#!/usr/bin/env node
/* Second read, eigen problems-1 to -3: the content fixes the review proposes, tried on in-memory copies with the engine's graders.
   Nothing is written. Rows: [text, expected] with T accepted, F refused on no line, an id = refused on that line.

   node docs/reviews/review-problems-1.4-c-scripts/try-fix.mjs --local-cdn <pkgs>      (from the repo root) */
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
const T = true, F = false;
const widget = (n, item, k) => JSON.parse(JSON.stringify(JSON.parse(fs.readFileSync(`app/content/courses/eigen/problems-${n}.json`, 'utf8')).items.find(i => i.id === item).parts[k - 1].widget));
const grade = (w, t) => { const r = w.kind === 'numeric' ? G.numGrade(w, t) : G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; };
let checks = 0, fails = 0;
const run = (title, w, rows) => {
  for (const [text, want] of rows) {
    const r = grade(w, text); checks++;
    const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
    if (!good) fails++;
    console.log(`${good ? 'ok  ' : 'FAIL'} ${title}: "${text}" ${r.ok ? 'accepted' : 'refused'} (key ${r.key})`);
  }
  for (const x of w.wrong || []) { const r = grade(w, x.tex != null ? x.tex : String(x.value)); checks++; if (r.ok || r.key !== x.id) { fails++; console.log(`FAIL ${title}: wrong ${x.id} no longer on its key (${r.key})`); } }
};

/* finding 1: crabs part 5 asked to 3 places */
let w = widget(3, 'p-crab-sizes', 5);
w.answer = 1.265; w.tol = { abs: 0.0005 };
w.wrong = [{ id: 'variance', value: 0.08, tol: { abs: 0.0005 } }, { id: 'total', value: 1.131, tol: { abs: 0.0005 } }, { id: 'pc2-sd', value: 2.53, tol: { abs: 0.0005 } }];
run('crabs 5, three places', w, [['1.265', T], ['1.2649', T], ['1.26502', T], ['1.26494', T], ['1.26', F], ['1.27', F], ['1.266', F], ['1.264', F], ['0.08', 'variance'], ['1.131', 'total'], ['1.1314', 'total'], ['2.53', 'pc2-sd'], ['2.530', 'pc2-sd'], ['1.13', F]]);

/* finding 3: a number in front of a vector, two parts */
w = widget(3, 'p-branch-sales', 4);
run('sales 4 as it stands', w, [['5(0.8,0.6,0)', 'length']]);
w.accept = [...w.accept, '5(0.8, 0.6, 0)'];
run('sales 4 with the accept form', w, [['5(0.8,0.6,0)', T], ['5\\left(0.8,0.6,0\\right)', T], ['\\sqrt{25}(0.8,0.6,0)', T], ['\\frac{\\sqrt{50}}{\\sqrt{2}}(0.8,0.6,0)', T], ['0.5(8,6,0)', T], ['(4,3,0)', T], ['(0.8,0.6,0)', 'u-only'], ['(40,30,0)', 'carried'], ['5(8,6,0)', 'length'], ['(4,3,2)', F]]);
w = widget(1, 'p-sketch-warp', 5);
run('warp 5 as it stands', w, [['16(3,1)+(2,1)', 'length']]);
w.accept = [...w.accept, '16(3, 1) + (2, 1)', '(48, 16) + (2, 1)'];
run('warp 5 with the accept form', w, [['16(3,1)+(2,1)', T], ['2^4(3,1)+1^4(2,1)', T], ['(48,16)+(2,1)', T], ['(50,17)', T], ['8(3,1)+4(2,1)', 'length'], ['(8,3)', 'one-warp'], ['(32,12)', 'times-four']]);

/* finding 4: three slips given a line */
w = widget(1, 'p-lazy-frog', 4);
w.wrong = [...w.wrong, { id: 'order', tex: '(0.5, 0)' }];
run('frog 4 with `order`', w, [['(0.5,0)', 'order'], ['(1/2, 0)', 'order'], ['(0,0.5)', T], ['(-0.5,0)', 'halved-only'], ['(0,0)', F]]);
w = widget(2, 'p-river-gauges', 4);
w.wrong = [...w.wrong, { id: 'no-divide', value: -1.28, tol: { abs: 0.0005 } }];
run('gauges 4 with `no-divide`', w, [['-1.28', 'no-divide'], ['-1.6', T], ['-1.25', 'no-r'], ['1.28', F]]);
w = widget(3, 'p-site-anomalies', 4);
w.wrong = [...w.wrong, { id: 'variance', value: 0.3, tol: { abs: 0.0005 } }];
run('sites 4 with `variance`', w, [['0.3', 'variance'], ['9', T], ['3', 'unsquared'], ['1.5', F]]);

/* finding 5: gauges part 5 at the reported r = 0.15 */
w = widget(2, 'p-river-gauges', 5);
w.answer = -0.26;
w.wrong = [{ id: 'dropped-sign', value: 0.26, tol: { abs: 0.0005 } }, { id: 'bound', value: 0, tol: { abs: 0 } }, { id: 'no-double', value: 2.15, tol: { abs: 0.0005 } }];
run('gauges 5 at r = 0.15', w, [['-0.26', T], ['−0.26', T], ['-13/50', T], ['0.26', 'dropped-sign'], ['0', 'bound'], ['2.15', 'no-double'], ['-0.16', F], ['-0.3', F]]);

/* finding 6: tank part 5 with weights (0.6, 0.25, 0.15) */
w = widget(2, 'p-tank-thermometers', 5);
w.answer = 1.89;
w.wrong = [{ id: 'no-eigenvalue', value: 1.78, tol: { abs: 0.005 } }, { id: 'd-only', value: 0.22, tol: { abs: 0.005 } }, { id: 'no-cov', value: 1.335, tol: { abs: 0.005 } }];
run('tank 5 with new weights', w, [['1.89', T], ['1.890', T], ['1.8904', T], ['189/100', T], ['1.78', 'no-eigenvalue'], ['1.7783', 'no-eigenvalue'], ['0.22', 'd-only'], ['0.2233', 'd-only'], ['1.34', 'no-cov'], ['1.33', 'no-cov'], ['1.335', 'no-cov'], ['1.76', F], ['1.9', F], ['1.88', F]]);

console.log(`try-fix: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
