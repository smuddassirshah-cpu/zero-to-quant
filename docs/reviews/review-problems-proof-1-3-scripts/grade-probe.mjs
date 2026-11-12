#!/usr/bin/env node
/* Second read, proof problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (as review-problems-1.4-c-scripts/grade-probe.mjs does), then for
     numeric     numGrade (the call numeric.js makes): the key grades correct, also with one more place, after a letter and "=",
                 and with a true minus sign; every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade (the call expression.js makes): the key and every accept[] grade correct; every wrong[].tex is refused
                 on its own key and has a line
   and the reader's own strings (ROWS): T accepted, F refused on no wrong line, an id = refused on that line,
   N = no number read (Check stays unavailable: a sum, a power or a word typed for a count; engine behaviour, the same in every set). A row with a note is one the reader holds to be a fault (FINDING, not a failure).

   node docs/reviews/review-problems-proof-1-3-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
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

const T = true, F = false, N = 'NOPARSE';
const PCT = 'the threshold typed with the % sign the claim itself carries';
/* ROWS[set][item][part] = [[text, expected, note?], ...] */
const ROWS = {
  1: {
    'p-leverage-calls': {
      1: [['3 accounts', T], ['3.0', T], ['6', 'swapped'], ['9', 'both'], ['12', F], ['28', F]],
      2: [['37 accounts', T], ['9', 'true-true'], ['3', 'breakers'], ['28', F], ['31', F], ['34', F]],
      3: [['6 accounts', T], ['3', 'rule'], ['34', 'true-count'], ['15', F], ['9', F]],
    },
    'p-spread-signal': {
      1: [['2 statements', T], ['3', 'all'], ['1', 'one'], ['0', F]],
      3: [['3 rows', T], ['6', 'or-only'], ['4', 'not-r-only'], ['1', 'and'], ['5', F], ['2', F]],
      4: [['5 rows', T], ['3', 'as-and'], ['2', 'only-false-if'], ['6', F], ['7', F]],
    },
    'p-fund-thresholds': {
      2: [['0 years', T], ['none', N], ['4', 'some-fund'], ['1', F], ['2', F]],
      3: [['t=2', T], ['t = 2', T], ['2%', T, PCT], ['3', 'at-least'], ['6', 'swapped'], ['1', F], ['5', F]],
      4: [['t=6', T], ['6%', T, PCT], ['7', 'at-least'], ['2', 'kept-b'], ['8', 'best-fund'], ['9', F], ['5', F]],
    },
  },
  2: {
    'p-multiples-forty': {
      1: [['10.0', T], ['|A|=10', N], ['9', 'no-forty'], ['4', F], ['11', F]],
      2: [['3', T], ['1', 'product'], ['6', 'all-b'], ['2', F], ['13', F]],
      3: [['2^3', N], ['8 subsets', T], ['6', 'times-two'], ['7', 'no-empty'], ['9', F], ['3', F]],
      4: [['13', T], ['16', 'no-overlap'], ['19', 'added'], ['12', F]],
      5: [['27', T], ['24', 'carry-16'], ['37', 'wrong-law'], ['21', F], ['13', F]],
    },
    'p-jobs-servers': {
      1: [['24 pairs', T], ['10', 'added'], ['1296', 'functions'], ['4096', F]],
      2: [['1,296', T], ['1 296', T], ['6^4', N], ['4096', 'flipped'], ['24', 'pairs'], ['360', 'one-to-one']],
      3: [['360', T], ['6*5*4*3', N], ['1296', 'repeat'], ['15', 'unordered'], ['24', 'jobs-only'], ['120', F]],
      5: [['936', T], ['1296-360', N], ['1656', 'added'], ['3736', 'carry-4096'], ['360', F]],
    },
    'p-rule-and-domain': {
      2: [['3-\\frac{y}{3}', T], ['-\\frac{y-9}{3}', T], ['\\frac{9}{3}-\\frac{y}{3}', T], ['3-\\frac13y', T], ['\\frac13(9-y)', T], ['x=\\frac{9-y}{3}', T], ['(9-y)\\div3', T],
        ['\\frac{y}{3}-3', 'sign'], ['9-3y', 'applied-f'], ['3+\\frac{y}{3}', 'sign-y'], ['\\frac{9-x}{3}', F], ['9-\\frac{y}{3}', F], ['\\frac{y}{3}', F]],
      3: [['5.0', T], ['x=5', T], ['-5', 'sign'], ['−5', 'sign'], ['27', 'applied-f'], ['1', 'dropped-minus'], ['-9', F]],
      4: [['20', T], ['10', 'hits'], ['0', 'onto'], ['30', F], ['21', F]],
    },
    'p-shift-images': {
      1: [['3 desks', T], ['4', 'traders'], ['2', F]],
      2: [['3', T], ['1', 'image-of-meet'], ['4', 'union'], ['7', F]],
      3: [['1', T], ['3', 'same'], ['0', 'empty'], ['2', F]],
    },
  },
  3: {
    'p-two-odd-squares': {
      1: [['k^2+k+j^2+j', T], ['(j^2+j)+(k^2+k)', T], ['j(j+1)+k(k+1)', T], ['j^{2}+j+k^{2}+k', T], ['j\\cdot j+j+k\\cdot k+k', T],
        ['j^2+k^2', 'lost-middle'], ['2j^2+2j+2k^2+2k', 'factor-two'], ['2(j^2+j+k^2+k)', 'factor-two'], ['4j^2+4j+4k^2+4k', F], ['j^2+j+k^2+k+2', F], ['j^2+2j+k^2+2k', F], ['m^2+n^2', F]],
      3: [['42', T], ['34', 'squares-only'], ['170', 'whole-sum'], ['43', F], ['168', F], ['84', F]],
      4: [['n=2', T], ['2', T], ['1', 'odd-n'], ['4', F], ['3', F]],
    },
    'p-step-three-sum': {
      1: [['n=3', T], ['2', 'checked'], ['1', F], ['4', F]],
      2: [['145', T], ['37', 'guess-a'], ['28', 'last-term'], ['144', F], ['290', F]],
      3: [['2+3k', T], ['3(k+1)-1', T], ['3k+3-1', T], ['3k-1', 'copied'], ['3k+1', 'term'], ['3k^2+5k+2', 'numerator'], ['(k+1)(3k+2)', 'numerator'], ['3k+4', F], ['k+2', F], ['3n+2', F]],
      4: [['2,380', T], ['2380.0', T], ['2262', 'off-by-one'], ['157', 'guess-a'], ['20827', 'term-as-n'], ['2379', F], ['4760', F]],
    },
    'p-six-nine-lots': {
      2: [['3y+2x', T], ['2x+3y', T], ['2\\cdot x+3\\cdot y', T], ['2x+9y', 'half-factored'], ['18x+27y', 'multiplied'], ['6x+9y', F], ['2x+3', F], ['x+y', F]],
      3: [['1', T], ['33', 'quotient'], ['0', 'zero'], ['2', F], ['33.33', F]],
      4: [['x=14', T], ['14 lots', T], ['17', 'no-y'], ['20', 'added'], ['84', F], ['13', F]],
    },
    'p-even-test-contra': {
      2: [['6k+2k^2', T], ['2k(k+3)', T], ['2(k^2+3k)', T], ['2k^{2}+6k', T], ['4k^2+12k', 'no-half'], ['k^2+3k', 'halved-twice'], ['2k^2+6k+1', F], ['2k^2+12k', F], ['2n^2+6n', F]],
      4: [['−8', T], ['-8.0', T], ['8', 'sign'], ['28', 'sign-6n'], ['-26', 'minus-square'], ['-10', F], ['10', F]],
    },
  },
};

let checks = 0, fails = 0, findings = 0, nTyped = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/proof/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${n} ${it.id} ${k}`;
    if (w.kind !== 'numeric' && w.kind !== 'expression') return;
    nTyped++;
    const by = (p.feedback && p.feedback.byKey) || {};
    const gr = w.kind === 'numeric' ? num : expr;
    if (w.kind === 'numeric') {
      const a = String(w.answer);
      say(num(w, a).ok, null, `${where}: key ${a} grades correct`);
      say(num(w, a + '.0').ok, null, `${where}: key with one more place grades correct`);
      say(num(w, 'x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
      if (w.answer < 0) say(num(w, a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
      for (const x of w.wrong || []) {
        const r = num(w, String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    } else {
      say(expr(w, w.answer).ok, null, `${where}: key ${w.answer} grades correct`);
      for (const a of w.accept || []) say(expr(w, a).ok, null, `${where}: accept "${a}" grades correct`);
      for (const x of w.wrong || []) {
        const r = expr(w, x.tex);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    }
    const rows = ((ROWS[n] || {})[it.id] || {})[k];
    say(!!rows, null, `${where}: reader rows exist`);
    for (const [text, want, note] of rows || []) {
      nRows++;
      const r = gr(w, text);
      const good = want === true ? r.ok : want === N ? (!r.ok && r.key === N) : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
      say(good, note, `${where}: "${text}" expected ${want === true ? 'accepted' : want === false ? 'refused, generic' : want}, got ${r.ok ? 'accepted' : r.key || 'refused, generic'}`);
    }
  });
}
console.log(`${nTyped} typed parts, ${checks} checks (${nRows} reader rows), ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
