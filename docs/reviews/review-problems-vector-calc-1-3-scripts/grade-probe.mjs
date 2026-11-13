#!/usr/bin/env node
/* Second read, vector-calc problems-1 to -3: what the engine's own graders do with each typed part.
   Pattern: docs/reviews/review-problems-analysis-1-3-scripts/grade-probe.mjs.
     numeric     numGrade: the key grades correct, also with one more place, after a letter and "=", with a true minus sign;
                 every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade: the key and every accept[] grade correct; every wrong[].tex is refused on its own key
   and the reader's rows (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line,
   '?' = report only (what happens to an exact form in a decimal field).
   A row with a note is one the reader holds to be a fault (FINDING, not a failure). --all prints every row.

   node docs/reviews/review-problems-vector-calc-1-3-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]   (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const ALL = argv.includes('--all');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js'), 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null) }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false, Q = '?';
const FREE = 'P is fixed only up to a function of x: this P also gives the double integral of y, and is refused';
const ECHO = 'the unsimplified form is accepted although the part asks for no brackets';
const ROWS = {
  1: {
    'p-bead-semicircle': {
      1: [['7.071', T], ['7.0711', T], ['7.07', F], ['7.1', F], ['\\sqrt{50}', Q], ['5\\sqrt2', Q]],
      2: [['5(x^2+y^2)', T], ['5y^2+5x^2', T], ['(2x-y)^2+(x+2y)^2', T, ECHO], ['45', F], ['5x^2+5y^2+8xy', F]],
      3: [['252.89', T], ['252.893', T], ['252.9', F], ['253', F], ['36\\sqrt5\\pi', Q], ['113.1', F]],
      4: [['36', T], ['36.0', T], ['-36', F], ['6', F]],
      5: [['0.447', T], ['0.4472', T], ['.447', T], ['0.45', F], ['0.4', F], ['1/\\sqrt5', Q], ['2.236', 'inverse']],
    },
    'p-two-routes-cubic': {
      1: [['3t^5+t^4+3t^3', T], ['t^4+3t^2(t+t^3)', T], ['t^3(3t^2+t+3)', T], ['t^4+3t^3+3t^6', F]],
      2: [['252/5', T], ['50.4', T], ['50.40', T], ['50', F], ['50.5', F], ['62/5', 'no-dot'], ['316/15', 'no-chain']],
      3: [['152/3', T], ['50.667', T], ['50.6667', T], ['50.67', F], ['50.7', F], ['32/3', 'p-only'], ['208.904', 'ds'], ['40', 'q-only'], ['62/3', 'no-four']],
      4: [['-4/15', T], ['-0.2667', T], ['-0.26667', T], ['-0.267', F], ['-0.27', F], ['4/15', 'sign'], ['0.2667', 'sign'], ['1516/15', 'added']],
    },
    'p-cubic-potential': {
      1: [['(16,12)', T], ['(16, 12)', T], ['(12,16)', 'swap'], ['(10,12)', 'y-not-squared'], ['(16,6)', F]],
      2: [['6y', T], ['y\\cdot 6', T], ['12x^2', 'px'], ['6x', 'qy'], ['6', F]],
      3: [['x^4+3xy^2', T], ['x(x^3+3y^2)', T], ['3y^2x+x^4', T], ['x^4+3xy^2+1', F], ['x^4+6xy^2', 'double'], ['x^4+3x^2y', 'wrong-var'], ['x^4+y^2', F]],
      4: [['69', T], ['69.0', T], ['70', 'end-only'], ['123', 'double'], ['-69', F], ['68', F]],
    },
    'p-ellipse-family': {
      1: [['3', T], ['-3', 'sign'], ['2', F], ['0', F]],
      2: [['xy^2+3xy', T], ['xy(y+3)', T], ['3xy+y^2x', T], ['2xy^2+6xy', 'double'], ['xy^2', 'missing'], ['xy^2+3xy+1', F]],
      3: [['20\\sin^2(t)', T], ['20\\sin^2 t', T], ['20\\sin(t)^2', T], ['10-10\\cos(2t)', T], ['(-10\\sin t)(-2\\sin t)', T], ['20-20\\cos^2 t', T], ['-20\\sin^2 t', 'sign'], ['-20\\sin t\\cos t', 'position'], ['20\\sin t', F]],
      4: [['62.83', T], ['62.832', T], ['62.8', F], ['63', F], ['20\\pi', Q], ['-62.83', 'sign'], ['125.66', 'sin-sq'], ['31.42', F]],
      5: [['10\\pi(3-k)', T], ['30\\pi-10k\\pi', T], ['-10\\pi(k-3)', T], ['(3-k)10\\pi', T], ['10\\pi(k-3)', 'sign'], ['20\\pi', 'constant'], ['10(3-k)', F], ['20\\pi(3-k)', F]],
    },
  },
  2: {
    'p-rectangle-edges': {
      1: [['6-2y^2', T], ['2(3-y^2)', T], ['(y^2+2)-(3y^2-4)', T], ['2y^2-6', 'reversed'], ['2xy', 'div'], ['6-2y', F]],
      2: [['16', T], ['16.0', T], ['-16', 'reversed'], ['0', 'axes'], ['18', 'const'], ['16/3', F]],
      3: [['7', T], ['1', 'drop-2x'], ['6', F], ['-7', F]],
      4: [['9', T], ['-9', 'direction'], ['23', 'added'], ['-3', F]],
    },
    'p-cycloid-arch': {
      1: [['(1-\\cos(t))^2', T], ['(1-\\cos t)^2', T], ['1-2\\cos t+\\cos^2 t', T], ['(1-\\cos t)(1-\\cos t)', T], ['-(1-\\cos t)^2', 'sign'], ['(1-\\cos t)(t-\\sin t)', 'no-derivative'], ['1-\\cos t', F], ['1-\\cos^2 t', F]],
      2: [['9.42', T], ['9.425', T], ['9.4', F], ['9', F], ['3\\pi', Q], ['-9.42', 'sign'], ['6.28', 'cos-sq'], ['3.14', 'square']],
      3: [['-\\frac{y^2}{2}', T], ['-\\frac12y^2', T], ['-0.5y^2', T], ['-y^2/2', T], ['\\frac{y^2}{2}', 'sign'], ['-y^2', 'no-half'],
          ['-\\frac{y^2}{2}+x', 'x-term'], ['-\\frac{y^2}{2}+1', 'constant'], ['-\\frac{y^2}{2}-y', F], ['-y', F]],
      4: [['7.85', T], ['7.854', T], ['7.9', F], ['8', F], ['\\frac{5\\pi}{2}', Q], ['15.71', 'no-half'], ['-7.85', 'sign']],
      5: [['5/6', T], ['0.833', T], ['0.8333', T], ['.833', T], ['0.83', F], ['0.8', F], ['1.2', 'inverse'], ['6/5', 'inverse'], ['5/3', 'no-half'], ['1.667', 'no-half']],
    },
    'p-triangle-flux': {
      1: [['4x', T], ['2x+2x', T], ['2y-1', 'curl'], ['2x', 'only-p'], ['4', F]],
      2: [['36', T], ['36.0', T], ['35', F], ['37', F], ['27', 'curl'], ['108', 'rectangle'], ['18', 'only-p']],
      3: [['-18', T], ['−18', T], ['-18.0', T], ['18', 'sign'], ['0', 'tangent'], ['-36', F]],
      4: [['54', T], ['54.0', T], ['53', F], ['18', 'add-edge'], ['36', 'all-out']],
    },
    'p-quadrilateral-plot': {
      1: [['21', T], ['-21', 'swap'], ['29', 'plus'], ['10.5', F]],
      2: [['14', T], ['28', 'no-half'], ['23', 'plus'], ['-14', F], ['12.5', F]],
      3: [['42', T], ['70', 'curl'], ['84', 'no-half'], ['3', F]],
      4: [['70', T], ['42', 'div'], ['-70', 'reversed'], ['-42', 'plus'], ['5', F], ['140', F]],
    },
  },
  3: {
    'p-saddle-roof': {
      1: [['(-y,-x,1)', T], ['(-y, -x, 1)', T], ['(y,x,1)', 'sign'], ['(-x,-y,1)', 'swap'], ['(y,x,-1)', F], ['(-y,-x,0)', F]],
      2: [['\\sqrt{1+x^2+y^2}', T], ['\\sqrt{x^2+y^2+1}', T], ['(1+x^2+y^2)^{1/2}', T], ['1+x^2+y^2', 'no-root'], ['\\sqrt{x^2+y^2}', 'no-one'], ['\\sqrt{1+x^2y^2}', F]],
      3: [['14.66', T], ['14.661', T], ['14.7', F], ['15', F], ['\\frac{14\\pi}{3}', Q], ['15.02', 'no-r'], ['9.42', 'flat']],
      4: [['32.99', T], ['32.987', T], ['33', F], ['33.0', F], ['\\frac{21\\pi}{2}', Q], ['-32.99', 'down'], ['47.12', 'z-only'], ['61.26', 'sign-normal']],
    },
    'p-open-tank': {
      1: [['z+2y+3', T], ['3+2y+z', T], ['2y+z+3', T], ['x+2y+3', 'wrong-var'], ['z+2y', 'drop-const'], ['z+y^2+3', F]],
      2: [['40', T], ['16', 'drop-const'], ['48', 'wrong-var'], ['5', F], ['32', F]],
      3: [['24', T], ['48', 'wrong-area'], ['12', 'no-z'], ['6', F]],
      4: [['16', T], ['64', 'added'], ['-8', 'from-16'], ['-16', F], ['40', F]],
    },
    'p-slanted-ellipse': {
      1: [['(3,-2y,2z)', T], ['(3, -2y, 2z)', T], ['(-3,2y,-2z)', 'reversed'], ['(3,-y,z)', 'half'], ['(3,2y,2z)', F]],
      2: [['(1,0,1)', T], ['(1, 0, 1)', T], ['(-1,0,1)', 'fx'], ['(-1,0,-1)', 'down'], ['(0,1,0)', F]],
      3: [['7-2x', T], ['3+2(2-x)', T], ['-2x+7', T], ['3+2z', 'z-left'], ['1-2x', 'fx'], ['7-2y', F]],
      4: [['87.96', T], ['87.965', T], ['88', F], ['88.0', F], ['28\\pi', Q], ['12.57', 'fx'], ['21.99', 'unit-disc'], ['124.40', 'extra-root']],
      5: [['-4', T], ['−4', T], ['4', 'sign'], ['-3', F], ['0', F]],
    },
    'p-can-curl': {
      1: [['(-3,-y-2z,z-1)', T], ['(-3, -2z-y, z-1)', T], ['(-3,-(y+2z),z-1)', T], ['(3,y+2z,1-z)', 'reversed'], ['(x-3,-y-2z,z-1)', 'qz-slip'], ['(-3,-y-2z,z+1)', F]],
      2: [['0', T], ['0.0', T], ['1', 'qz-slip'], ['-1', F], ['2', F]],
      3: [['-50.27', T], ['−50.27', T], ['-50.265', T], ['-50.3', F], ['-16\\pi', Q], ['50.27', 'sign'], ['-12.57', 'radius']],
      4: [['50.27', T], ['50.265', T], ['50.3', F], ['16\\pi', Q], ['-50.27', 'z0'], ['12.57', 'radius']],
      5: [['-100.53', T], ['−100.53', T], ['-100.531', T], ['-100.5', F], ['-32\\pi', Q], ['0', 'added'], ['100.53', 'sign'], ['-50.27', 'no-base']],
    },
  },
};

let checks = 0, fails = 0, findings = 0, nNum = 0, nExpr = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/vector-calc/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${n} ${it.id} ${k}`;
    const by = (p.feedback && p.feedback.byKey) || {};
    let grade;
    if (w.kind === 'numeric') {
      nNum++; grade = (t) => num(w, t);
      const a = String(w.answer);
      say(grade(a).ok, null, `${where}: key ${a} grades correct`);
      say(grade(a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
      say(grade('x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
      if (w.answer < 0) say(grade(a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    } else if (w.kind === 'expression') {
      nExpr++; grade = (t) => expr(w, t);
      say(grade(w.answer).ok, null, `${where}: key grades correct`);
      for (const a of w.accept || []) say(grade(a).ok, null, `${where}: accept "${a}" grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(x.tex);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    } else return;
    const rows = ((ROWS[n] || {})[it.id] || {})[k] || [];
    if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
    for (const [text, want, note] of rows) {
      nRows++;
      const r = grade(text);
      if (want === Q) { console.log(`NOTE    ${where}: exact form "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key})`); continue; }
      const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
      const flagged = note ? !good || want === true && /accepted although/.test(note) : false;
      if (note && good && /accepted although/.test(note)) { checks++; findings++; console.log(`FINDING ${where}: typed "${text}" is accepted   [${note}]`); continue; }
      say(good, note, `${where}: typed "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}), expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
      void flagged;
    }
  });
}
console.log(`${checks} checks (${nNum} numeric, ${nExpr} expression parts, ${nRows} reader rows), ${fails} failure(s), ${findings} row(s) held to be faults`);
process.exit(fails ? 1 : 0);
