#!/usr/bin/env node
/* Second read, analysis problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (the pattern of review-problems-1.4-c-scripts/grade-probe.mjs), then
     numeric     numGrade (the call numeric.js makes): the key grades correct, also with one more place, a letter and "=", and a
                 true minus sign; every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade (the call expression.js makes): the key and every accept[] grade correct; every wrong[].tex is refused
                 on its own key and has a line
   and the reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line.
   A row with a note is one the reader holds to be a fault (FINDING, not a failure). --all prints every row.

   node docs/reviews/review-problems-analysis-1-3-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
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
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null), line: r.line }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false;
const S7 = 'the sum itself (4/25, printed in the explanation) and S_6 to 2 places are told "That is S_7, one term too far"';
const ECHO = 'the question\'s own unsimplified expression is accepted, so the part can be passed by copying it';
const LOWER = 'the right formula with a lower-case n is refused on the generic line';
/* ROWS[set][item][part] = [[text, expected, note?], ...] */
const ROWS = {
  1: {
    'p-cube-root-twenty': {
      1: [['2.625', T], ['21/8', T], ['2.6250', T], ['2.75', 'right-end'], ['2.5', 'two-steps'], ['2.63', F], ['2.6875', F], ['2.125', F]],
      2: [['-979', T], ['−979', T], ['979', 'sign'], ['-839', 'squares'], ['8749', 'no-twenty'], ['-1.912', F], ['0', F]],
      3: [['2k^3', T], ['k^3\\cdot 2', T], ['2k\\cdot k^2', T], ['\\frac{8k^3}{4}', T], ['2\\times k^3', T], ['8k^3', 'no-divide'], ['4k^3', 'half-only'], ['\\frac{k^3}{2}', 'cube-two'], ['0.5k^3', 'cube-two'], ['2k^2', F], ['\\frac{2k^3}{5}', F], ['2k', F]],
      4: [['16', T], ['16.0', T], ['15', 'round-down'], ['11', 'no-ones'], ['12', F], ['15.45', F], ['17', F]],
    },
    'p-climbing-fractions': {
      1: [['0.5', T], ['1/2', T], ['.5', T], ['0.50', T], ['-4', 'n-zero'], ['5', 'sup'], ['0', F], ['2', F]],
      2: [['9(n+1)^{-1}', T], ['\\frac{18}{2n+2}', T], ['\\frac{1}{n+1}', 'minus-four'], ['-\\frac{9}{n+1}', 'sign'], ['\\frac{-9}{n+1}', 'sign'], ['\\frac{9}{n}', F], ['\\frac{9}{n-1}', F], ['9', F],
        ['5-\\frac{5n-4}{n+1}', F, ECHO], ['\\frac{5(n+1)-(5n-4)}{n+1}', T]],
      3: [['-1+\\frac{9}{\\varepsilon}', T], ['9\\varepsilon^{-1}-1', T], ['\\frac{9}{\\epsilon}-1', T], ['\\frac{9}{\\varepsilon}', 'no-minus-one'], ['9\\varepsilon-1', 'flip'], ['\\frac{\\varepsilon}{9}-1', F], ['\\frac{9}{\\varepsilon}+1', F], ['2249', F]],
      5: [['2250', T], ['2,250', T], ['2249', 'equal'], ['2251', 'no-minus-one'], ['2248', F], ['2250.5', F]],
    },
    'p-diagonal-fraction': {
      1: [['0.55445', T], ['.55445', T], ['0.78558', 'diagonal'], ['0.55555', 'all-five'], ['0.44554', 'swapped'], ['0.5544', F], ['0.55446', F], ['0.55455', F]],
      2: [['100001', T], ['100,001', T], ['100000', 'equal'], ['10001', F], ['100002', F]],
      3: [['55446', T], ['55445', 'floor'], ['55447', 'used-b'], ['55445.55445', F]],
      4: [['0.5544545', T], ['0.5544544', T], ['0.55445446', T], ['55446/100001', T], ['0.55446', 'n-slip'], ['0.554454', F], ['0.55445', F], ['0.5544555', F]],
    },
  },
  2: {
    'p-sum-law-band': {
      1: [['\\frac{7}{n+2.5}', T], ['\\frac{28}{4n+10}', T], ['14(2n+5)^{-1}', T], ['\\frac{16}{2n+5}', 'plus-one'], ['-\\frac{14}{2n+5}', 'sign'], ['\\frac{-14}{2n+5}', 'sign'], ['\\frac{14}{2n-5}', F], ['\\frac{14}{n+5}', F], ['14', F]],
      2: [['138', T], ['137', 'round-down'], ['68', 'full-band'], ['137.5', F], ['139', F], ['280', F]],
      3: [['80', T], ['79', 'equal'], ['40', 'full-band'], ['81', F]],
      4: [['138', T], ['80', 'min'], ['218', 'sum'], ['109', F]],
      5: [['109', T], ['138', 'proof'], ['108', 'round-down'], ['110', F], ['80', F]],
    },
    'p-root-recursion': {
      1: [['6.403', T], ['6.4031', T], ['6.40312', T], ['41', 'no-root'], ['5', 'a2'], ['6.40', F], ['6.4', F], ['6.828', F]],
      3: [['7', T], ['7.0', T], ['-3', 'other-root'], ['49', 'bound-only'], ['3', F], ['21', F]],
      4: [['0.5', T], ['1/2', T], ['.5', T], ['4/8', T], ['4/7', 'no-term'], ['0.571', 'no-term'], ['1/3', 'used-a2'], ['0.333', 'used-a2'], ['0.25', F], ['2', F]],
      5: [['14', T], ['11', 'no-six'], ['13', 'power-n'], ['17', 'slip-4'], ['9', F], ['12', F], ['15', F]],
    },
    'p-two-strands-cauchy': {
      1: [['2', T], ['2.0', T], ['-2', 'neg'], ['0', 'zero'], ['1.25', F]],
      2: [['-2', T], ['−2', T], ['2', 'sign'], ['1', 'first'], ['-1', F], ['0', F]],
      3: [['4', T], ['0', 'zero'], ['2', 'two'], ['3', F], ['-4', F]],
      4: [['6', T], ['5', 'round-down'], ['7', 'index-plus'], ['4', F]],
    },
  },
  3: {
    'p-telescoping-tail': {
      1: [['0.5', T], ['1/2', T], ['.5', T], ['2', 'two'], ['1', 'one'], ['0.25', F]],
      2: [['\\frac{5}{12}-\\frac{2N+5}{2(N+2)(N+3)}', T], ['\\frac12\\left(\\frac56-\\frac{1}{N+2}-\\frac{1}{N+3}\\right)', T], ['\\frac{5}{12}-\\frac{1}{2N+4}-\\frac{1}{2N+6}', T], ['\\frac{N(5N+13)}{12(N+2)(N+3)}', T],
        ['\\frac{5N^2+13N}{12N^2+60N+72}', T], ['\\frac{5}{6}-\\frac{1}{N+2}-\\frac{1}{N+3}', 'no-half'], ['\\frac{5}{12}-\\frac{1}{2(N+3)}', 'one-left'], ['\\frac{1}{4}-\\frac{1}{2(N+3)}', 'one-start'],
        ['\\frac{5}{12}', F], ['\\frac{5}{12}-\\frac{1}{2(N+1)}-\\frac{1}{2(N+3)}', F], ['\\frac{5}{12}-\\frac{1}{2(n+2)}-\\frac{1}{2(n+3)}', T, LOWER]],
      3: [['5/12', T], ['0.4167', T], ['0.41667', T], ['0.4166', T], ['0.8333', 'no-half'], ['5/6', 'no-half'], ['0.25', 'one-start'], ['1/4', 'one-start'], ['0.417', F], ['0.42', F], ['0.5', F]],
      4: [['998', T], ['499', 'one-term'], ['1998', 'no-half'], ['997', 'round-down'], ['999', F], ['1000', F], ['997.5', F]],
    },
    'p-alternating-quarters': {
      1: [['0.25', T], ['1/4', T], ['.25', T], ['4', 'flip'], ['1', 'no-four'], ['0.5', F], ['0', F]],
      3: [['0.0049', T], ['5/1024', T], ['0.00488', T], ['0.0048', T], ['0.0156', 'a4'], ['0.015625', 'a4'], ['0.0015', 'a6'], ['0.0014648', 'a6'], ['0.005', F], ['0.0195', F]],
      4: [['6', T], ['7', 'index'], ['5', 'round-down'], ['4', F]],
      5: [['0.1597', T], ['327/2048', T], ['0.15967', T], ['0.1596', T], ['0.15625', 's4'], ['0.1563', 's4'], ['0.4438', 'sizes'], ['0.1601', 's7'], ['0.16', F, S7], ['4/25', F, S7], ['0.160', F, S7], ['0.1611', F]],
    },
    'p-cube-root-greedy': {
      2: [['0.2063', T], ['0.20630', T], ['1.6934', 'positive'], ['0.2929', 'square-root'], ['0.206', F], ['-0.7937', F], ['0.7937', F], ['0.2', F]],
      3: [['-0.63', T], ['-0.6300', T], ['−0.6300', T], ['-0.62996', T], ['0.63', 'sign'], ['0.6300', 'sign'], ['0.6934', 'positive'], ['-0.6934', 'odd-neg'], ['-0.4237', F], ['-0.7937', F]],
      4: [['0.2697', T], ['0.26970', T], ['-0.9740', 'negative-again'], ['0.1611', 'skipped'], ['0.27', F], ['0.6934', F], ['-0.4237', F]],
      5: [['0.2', T], ['1/5', T], ['0.20', T], ['.2', T], ['0.5718', 'original'], ['0.2697', 'last-total'], ['0.2063', F], ['0', F]],
    },
  },
};

let checks = 0, fails = 0, findings = 0, nNum = 0, nExpr = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/analysis/problems-${n}.json`, 'utf8'));
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
      const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
      say(good, note, `${where}: typed "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}), expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
    }
  });
}
console.log(`grade-probe: ${checks} checks over ${nNum} numeric and ${nExpr} expression parts, ${nRows} reader rows, ${fails} failures, ${findings} findings`);
process.exit(fails ? 1 : 0);
