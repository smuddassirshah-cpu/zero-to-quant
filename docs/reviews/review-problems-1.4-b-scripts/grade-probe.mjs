#!/usr/bin/env node
/* Second read, elimination and least-squares problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (as review-problems-1.4-a-scripts/grade-probe.mjs does), then for
     numeric     numGrade: the key grades correct, also with more places, a letter and "=", a true minus sign and its unit;
                 every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade (the call expression.js makes): the key and every accept[] grade correct; every wrong[].tex is refused
                 on its own key and has a line; then other ways to type the same vector (FORMS)
     matrix      the three parts that ask for a matrix typed whole: each wrong matrix retyped as the question asks,
                 `[[a, b, c], ...]`; the known engine fault is counted, not failed
   and the reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line,
   'LEN' = refused with the engine's shape line. A row with a note is one the reader holds to be a fault (FINDING, not a failure).

   node docs/reviews/review-problems-1.4-b-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
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
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false;
const SCAL = 'the right answer as a number times a vector is refused with the false line "That is a single value"';
const NORM = 'the unit vector (the step l4 always takes next) gets the generic line, which tells the learner to do what they did';
const NEG = 'solving 4 + 6 + c = 0 gives -10, which does not reach the `added` line (the stored slip is +10)';
/* ROWS[course][set][item][part] = [[text, expected, note?], ...] */
const ROWS = {
  elimination: {
    1: {
      'p-florist-prices': {
        1: [['(0,4,3,17.0)', T], ['\\left(0,4,3,17\\right)', T], ['0, 4, 3, 17', T], ['(0,4,3,\\frac{34}{2})', T], ['(0, 4, 3)', 'LEN'], ['(0, 2, 1, 7)', F], ['(0, 0, 1, 3)', F], ['(0, 8, 6, 34)', F], ['(-3,1,-3,-\\frac{23}{2})', 'upside-down']],
        2: [['£3', T], ['3.00', T], ['3 pounds', T], ['z=3', T], ['17', 'cost-kept'], ['1', F], ['7', F]],
        3: [['£2', T], ['2.00', T], ['3.5', 'no-subtract'], ['7/2', 'no-subtract'], ['5', 'added'], ['4', F]],
        4: [['1.50', T], ['£1.50', T], ['3/2', T], ['1 1/2', T], ['7', 'coefficients'], ['3', 'no-divide'], ['2', F], ['1.6', F]],
        5: [['£18', T], ['18.00', T], ['40', 'carried'], ['21', 'counts-swapped'], ['18.5', F]],
      },
      'p-three-lines': {
        1: [['[[1,0,0],[3,1,0],[\\frac{1}{2},2,1]]', T], ['[[1, 0, 0], [3, 1, 0], [.5, 2, 1]]', T], ['[[1, 0, 0], [3, 1, 0], [2/4, 2, 1]]', T], ['\\left\\lbrack\\left\\lbrack1,0,0\\right\\rbrack,\\left\\lbrack3,1,0\\right\\rbrack,\\left\\lbrack\\frac12,2,1\\right\\rbrack\\right\\rbrack', T], ['(3, 0.5, 2)', 'LEN']],
        2: [['(12, 5, 2.0)', T], ['c=(12,5,2)', T], ['\\begin{pmatrix}12\\\\5\\\\2\\end{pmatrix}', T], ['(12, 41, 18)', F], ['(12, 5, 8)', F], ['(3,2,1)', F]],
        3: [['(1,2,3)', F], ['(6,2,1)', F], ['(12,5,2)', F]],
        4: [['(1,2,2)', 'extra-only'], ['(13,10,5)', 'added-c'], ['(3,2,1)', F], ['(22,79,43)', F]],
      },
      'p-courier-rounds': {
        1: [['[[0,1,0],[1,0,0],[0,0,1]]', T]],
        2: [['[[1,0,0],[0,1,0],[0,2,1]]', T], ['[[1, 0, 0], [0, 1, 0], [0, 6/3, 1]]', T]],
        3: [['(14,15,39)', F], ['(15,14,39)', F], ['(15, 14, 9)', F]],
        4: [['(3,4,2)', 'reversed'], ['(4,3,2)', F]],
        5: [['30 minutes', T], ['30 min', T], ['30.0', T], ['31', 'reversed'], ['11', F], ['0.5 hours', F]],
      },
      'p-roaster-beans': {
        1: [['(0, -2+k, 3)', T], ['(0,-(2-k),3)', T], ['\\left(0,k-2,3\\right)', T], ['(0, 2-k, 3)', F], ['(0, k-2, 3, 15)', 'LEN'], ['(0, 0, 1)', F], ['(0, 2, 3)', F]],
        2: [['k=2', T], ['2.0', T], ['0', 'k-zero'], ['3', 'triple'], ['4', F], ['-2', F]],
        4: [['£8', T], ['8.00', T], ['15.5', 'no-z'], ['15.50', 'no-z'], ['43', 'cost-kept'], ['16', F], ['5', F]],
        5: [['(6.00, 8.00, 5.00)', T], ['(9/4, 31/2, 5)', 'carried'], ['(12,8,5)', 'no-divide'], ['(5,8,6)', F], ['(6, 8, 15)', F]],
      },
    },
    2: {
      'p-burning-ethanol': {
        1: [['r=3', T], ['4', 'columns'], ['2', F]],
        2: [['3', 'rank'], ['0', 'full'], ['2', F]],
        3: [['(\\frac13,1,\\frac23,1)', T], ['(2/6, 1, 4/6, 1)', T], ['(0.333, 1, 0.667, 1)', F], ['(1/3, 1, 2/3)', 'LEN'], ['(-1/3, -1, -2/3, 1)', F], ['\\frac{1}{3}(1,3,2,3)', T, SCAL], ['(1,3,2,3)/3', T, SCAL]],
        4: [['1,3,2,3', T], ['(2,6,4,6)', 'double'], ['(3,9,6,9)', F], ['(1, 3, -2, -3)', F]],
      },
      'p-tilted-gantry': {
        1: [['k=-4', T], ['−4', T], ['-4.0', T], ['4', 'sign'], ['0', 'zero'], ['2', F], ['-2', F]],
        2: [['(−2, 2)', T], ['-2, 2', T], ['(2,-2)', 'sign'], ['(2, 2)', F], ['(-2, 2, 0)', 'LEN']],
        3: [['c=4', T], ['6', 'half-step'], ['-4', 'sign'], ['2', F]],
        4: [['(2,1,0)', 'no-motor-3'], ['(0,3,1)', 'sign'], ['(2,-2,1)', F], ['(6,-3,2)', F]],
      },
      'p-futures-packages': {
        1: [['3', 'columns'], ['1', F]],
        2: [['(1,-1,1)', 'sign'], ['(1,-1,-1)', F], ['(1, 1, 1)', F]],
        3: [['c=-3', T], ['3', 'sign'], ['1', 'stale-rhs'], ['5', F]],
        4: [['(4, 3, 0.0)', T], ['(4,-3,0)', 'sign'], ['(3,4,1)', F], ['(4,3)', 'LEN']],
        5: [['(6,1,2)', 'sign'], ['(-2,2,2)', 'nullspace-only'], ['(4,3,2)', F], ['(3,4,1)', F]],
      },
      'p-coin-hopper': {
        1: [['3', 'columns'], ['1', 'one']],
        2: [['(-5,8,3)', 'sign'], ['(5/3,-8/3,1)', 'special'], ['(5, 8, 3)', F], ['(-5, 8, -3)', F]],
        3: [['(3,6,1)', 'swapped'], ['(11,-5,4)', F], ['(1,11,-2)', F]],
      },
    },
    3: {
      'p-vinyl-cutter': {
        1: [['50 cm²', T], ['50 cm^2', T], ['50cm2', T], ['50.0', T], ['10', F], ['70', 'plus'], ['60', 'diagonal']],
        2: [['k=6', T], ['-6', 'sign'], ['12', 'factor'], ['2', F]],
        3: [['c=4', T], ['12', 'row'], ['9', F]],
        4: [['(2, -1.0)', T], ['(2,1)', 'sign'], ['(2,-3)', 'perpendicular'], ['(-2,1)', F], ['(1,-1/2)', F], ['(4,-2)', F]],
      },
      'p-deformed-part': {
        1: [['13.0', T], ['11', 'no-sign'], ['12', 'diagonal'], ['-13', F]],
        2: [['13/6', T], ['2.167', T], ['2.1667', T], ['2.166', T], ['2 1/6', T], ['2.17', F], ['2.2', F], ['1.833', 'sign'], ['11/6', 'sign'], ['13', F], ['6/13', F]],
        3: [['195 cm³', T], ['195 cm^3', T], ['195cm3', T], ['165', 'no-sign'], ['180', 'diagonal'], ['28', F]],
        4: [['−26', T], ['26', 'swap-ignored'], ['-13', 'scale-ignored'], ['-52', 'scale-squared'], ['13', F], ['52', F]],
        5: [['5,070', T], ['5 070', T], ['5070 cm³', T], ['-5070', 'signed'], ['2535', 'scale-ignored'], ['390', F]],
      },
      'p-draw-bet': {
        1: [['-1,000', T], ['−1000', T], ['1000', 'plus'], ['0', 'diagonal'], ['-100', F]],
        2: [['0', 'none'], ['3', 'rank'], ['4', F], ['2', F]],
        3: [['(1, −1, 1)', T], ['(-1,1,-1)', 'sign'], ['(1,1,1)', 'no-sale'], ['(10,-10,10)', F], ['(1,1,-1)', F]],
        4: [['3.30', T], ['£3.30', T], ['£3.3', T], ['33/10', T], ['17.3', 'all-plus'], ['-3.3', 'sign'], ['3', F], ['3.29', F], ['3.31', F]],
        5: [['£15', T], ['15.00', T], ['15 pounds', T], ['0.3', 'per-bet'], ['0.30', 'per-bet'], ['-15', 'reversed'], ['150', F], ['165', F]],
      },
    },
  },
  'least-squares': {
    1: {
      'p-hall-drone': {
        1: [['(1, -1, 1.0)', T], ['(1,0,-1)', 'sign'], ['(1,1,1)', 'b-sign'], ['(-1,1,-1)', F], ['(2,-2,2)', F], ['(1,-1,-1)', F]],
        2: [['c=2', T], ['-2', 'sign'], ['10', 'added'], ['-10', 'added', NEG], ['8', F]],
        3: [['(18/6, 2/2)', T], ['(3.0,1.0)', T], ['(18,2)', 'no-divide'], ['(3,3)', 'sign-x2'], ['(1,3)', F]],
        4: [['(7/2,-1/2,1)', T], ['(\\frac72,-\\frac12,1)', T], ['(3.50, -0.50, 1)', T], ['(21/6, -1/2, 3/3)', T], ['(3,1,1)', 'kept-plan'], ['(0.5,-1.5,1)', F], ['\\frac12(7,-1,2)', T, SCAL]],
      },
      'p-station-codes': {
        1: [['1,-1,-1,1', T], ['(1,-1,1,-1)', 'c1-only'], ['(-1,1,1,-1)', 'flipped'], ['(1,1,-1,-1)', F], ['(1,-1,-1)', 'LEN']],
        2: [['x_4=2', T], ['8', 'no-divide'], ['4', 'by-length'], ['-2', F]],
        3: [['(12,4,-4,8)', 'no-divide'], ['(6,2,-2,4)', 'by-length'], ['(3,1,1,2)', 'sign'], ['(2,-1,1,3)', F]],
        4: [['60.0', T], ['36', 'cross-term'], ['15', 'no-four'], ['120', F], ['9', F]],
      },
      'p-crystal-cell': {
        1: [['(2, -2, -1.0)', T], ['(-6,-6,-9)', 'length-not-squared'], ['(10,2,7)', 'added'], ['(4,2,4)', F], ['(-2,2,1)', F], ['(2/3,-2/3,-1/3)', 'normalised', NORM]],
        2: [['9.0', T], ['20.12', 'slanted'], ['20', 'slanted'], ['4.5', 'triangle'], ['3', F], ['18', F], ['27', F]],
        3: [['(-3/5, 0, -24/5)', 'originals'], ['(-15,18,6)', 'unit-skipped'], ['(-1,-2,2)', F], ['(3,0,-3)', F], ['(1/3,2/3,-2/3)', 'normalised', NORM]],
        4: [['27.0', T], ['104.57', 'no-straightening'], ['105', 'no-straightening'], ['81', 'squared'], ['43.54', 'carried'], ['44', 'carried'], ['9', F], ['-27', F]],
      },
      'p-rotor-changes': {
        1: [['(0,-1,0,1)', 'roll-sign'], ['(-1,1,0,1)', 'lift-short'], ['(2,1,0,1)', 'no-minus'], ['(-1,0,1,0)', F], ['(-2,1,1)', 'LEN']],
        2: [['(0,1,-2,1)', 'no-divide'], ['(-3,1,1,1)', 'added'], ['(0,-1,0,1)', 'carried'], ['(1,-1,1,-1)', F], ['(-2,1,0,1)', F], ['(-1/2,1/2,-1/2,1/2)', 'normalised', NORM]],
        3: [['−2', T], ['c=-2', T], ['-8', 'no-divide'], ['-4', 'by-length'], ['2', 'no-sign'], ['-1', F]],
        4: [['(1,2,1,0)', 'row-part'], ['(2,-2,2,-2)', 'e2-only'], ['(13/3,-5/3,-1,-5/3)', 'used-s2'], ['(1,0,-1,0)', F], ['(4,0,2,-2)', F], ['(-3,2,-1,2)', F]],
      },
    },
    2: {
      'p-grey-pixel': {
        1: [['(420,420,420)', 'no-divide'], ['140', 'LEN'], ['(200,140,80)', F]],
        2: [['(-60,0,60)', 'reversed'], ['(-220,-280,-340)', 'carried'], ['(140,140,140)', F], ['(60, 0, 60)', F]],
        3: [['(100,70,40)', 'halved-all'], ['(130,70,10)', 'grey-halved'], ['(30,0,-30)', F], ['(155,140,125)', F]],
        4: [['(170,140,110)', 'projection'], ['(85,70,55)', 'halved-twice-all'], ['(15,0,-15)', F], ['(147.5,140,132.5)', F]],
      },
      'p-power-line': {
        1: [['7/5', T], ['1.40', T], ['1 2/5', T], ['x=1.4', T], ['35', 'no-divide'], ['7', 'by-length'], ['1.5', F], ['5.6', F]],
        2: [['(-18/5,24/5)', T], ['(-3.60, 4.80)', T], ['(5.6,4.2)', 'p-not-e'], ['(7.6,13.2)', 'added'], ['(-26,-12)', 'carried'], ['(3.6,4.8)', 'sign'], ['(3.6,-4.8)', F], ['(-4, 5)', F]],
        3: [['6 km', T], ['6km', T], ['6.0', T], ['6 kilometres', T], ['7', 'along'], ['9.22', 'to-origin'], ['9', 'to-origin'], ['36', 'squared'], ['8.5', F], ['10', F]],
        4: [['0.71', T], ['0.708', T], ['0.7082', T], ['0.71 km', T], ['.71', T], ['0.7', F], ['0.72', F], ['3', 'added'], ['6.708', 'total'], ['6.71', 'total'], ['9', 'squares'], ['6.7', F]],
      },
      'p-solar-drone': {
        1: [['(-2,1,1)', 'sign'], ['(-2,0,1)', 'one-edge'], ['(2,1,-1)', F], ['(2,1,1)', F]],
        2: [['(-24,-12,12)', 'no-divide'], ['(-14/3,7/3,7/3)', 'carried'], ['(4,2,-2)', F], ['(-2,-1,1)', F], ['(2,3,7)', F], ['2(-2,-1,1)', T, SCAL]],
        3: [['(-6,-1,11)', 'added'], ['(22,13,-3)', 'carried'], ['(-4,-2,2)', F], ['(2,3)', 'LEN']],
        4: [['(-2,1)', 'straight-down'], ['(-6,-1)', 'carried'], ['(3,2)', F], ['(16,10)', F], ['(2,3,7)', 'LEN']],
      },
      'p-dye-mix': {
        1: [['49/7', T], ['7.0', T], ['49', 'no-unit'], ['1', 'coefficient'], ['14', F]],
        2: [['(\\frac67,\\frac27,-\\frac37)', T], ['(6,2,-3)', 'not-normalised'], ['(-6,-16,-39)', 'used-a1'], ['(0.857,0.286,-0.429)', F], ['(-6/7,-2/7,3/7)', F], ['(2/7,3/7,6/7)', F],
          ['\\frac17(6,2,-3)', T, SCAL], ['\\frac{1}{7}\\left(6,2,-3\\right)', T, SCAL], ['(6,2,-3)/7', T, SCAL]],
        3: [['(147/7, 49/7)', T], ['(147,196)', 'a-not-q'], ['(21,28)', 'used-a2'], ['(7,21)', F], ['(3,1)', F]],
        4: [['(2, 1.0)', T], ['(3,1)', 'top-down'], ['(3,-2)', 'transposed'], ['(1,2)', F], ['(14, 7)', F]],
        5: [['7.0', T], ['49', 'squared'], ['9.9', 'carried'], ['9.899', 'carried'], ['1.08', 'lengths'], ['1.1', 'lengths'], ['0', F], ['22.14', F]],
      },
    },
    3: {
      'p-runner-heart': {
        1: [['59.0', T], ['7059', 'uncentred'], ['10', 'sxx'], ['11.8', F], ['5.9', F], ['-59', F]],
        2: [['59/10', T], ['5.90', T], ['5 9/10', T], ['11.8', 'over-n'], ['0.1695', 'upside-down'], ['0.17', 'upside-down'], ['6', F], ['59', F]],
        3: [['81.0', T], ['199', 'sign'], ['134.1', 'no-xbar'], ['134', 'no-xbar'], ['140', F], ['80', F]],
        5: [['82.0', T], ['81', 'old'], ['87', 'full-shift'], ['141', 'mean-only'], ['83', F], ['146', F]],
      },
      'p-ramp-ball': {
        1: [['k=-8', T], ['−8', T], ['8', 'sign'], ['0', F]],
        2: [['(1/2,-4/5,3/10)', T], ['(.5,-.8,.3)', T], ['(0.50,-0.80,0.30)', T], ['(49,-78.4,29.4)', 'no-divide'], ['(6,21,46)', 'gave-p'], ['(5,-8,3)', F], ['(-0.5,0.8,-0.3)', F], ['0.1(5,-8,3)', T, SCAL], ['\\frac{1}{10}(5,-8,3)', T, SCAL]],
        3: [['(1.0,5.0)', T], ['(5,1)', 'swapped'], ['(6,21,46)', 'LEN'], ['(0.5,5.1)', F]],
        4: [['126 cm', T], ['126cm', T], ['126.0', T], ['26', 't-not-squared'], ['125', 'no-intercept'], ['30', 'swapped'], ['130', F], ['46', F]],
      },
      'p-gas-hubs': {
        1: [['15.0', T], ['5', 'sum'], ['25', 'sum-squared'], ['10', F], ['-25', F]],
        2: [['(1.0, -2.0)', T], ['[1, -2]', T], ['(-1,-5/3)', 'diagonal'], ['(-2,1)', 'swapped'], ['(1,2)', 'no-sign'], ['(-1, 2)', F]],
        3: [['(1/2,-3/2)', T], ['(.5,-1.5)', T], ['(-1,-4/3)', 'diagonal'], ['(0.5,1.5)', 'no-sign'], ['(-1.5,0.5)', F]],
        4: [['(1/2,-1/2)', T], ['(1.5,-3.5)', 'added'], ['(-0.5,0.5)', 'reversed'], ['(0.5, 0.5)', F]],
        5: [['0.333', T], ['1/3', T], ['0.3333', T], ['.333', T], ['33.3%', T], ['0.33', F], ['0.3', F], ['0.334', F], ['0.667', 'ratio'], ['2/3', 'ratio'], ['0.6', 'added-sse'], ['0.964', 'hub-n'], ['0.9375', F]],
      },
    },
  },
};

const vecForms = (v) => ({
  'round, no space': [`(${v.join(',')})`, true],
  'round, MathLive \\left( \\right)': [`\\left(${v.join(',')}\\right)`, true],
  'square brackets': [`[${v.join(', ')}]`, true],
  'square, MathLive \\lbrack': [`\\left\\lbrack${v.join(',')}\\right\\rbrack`, true],
  'angle brackets': [`\\langle ${v.join(', ')}\\rangle`, true],
  'column pmatrix': [`\\begin{pmatrix}${v.join('\\\\')}\\end{pmatrix}`, true],
  'row pmatrix (a row where a column is meant)': [`\\begin{pmatrix}${v.join('&')}\\end{pmatrix}`, true],
  'no brackets': [v.join(', '), true],
  'semicolons': [`(${v.join('; ')})`, true],
  'entries reversed': [`(${[...v].reverse().join(', ')})`, v.join() === [...v].reverse().join()],
  'one entry short': [v.length > 2 ? `(${v.slice(0, -1).join(', ')})` : `${v[0]}`, false],
});
const rowsOf = (tex) => /\\begin\{pmatrix\}(.*)\\end\{pmatrix\}/.exec(tex)[1].split('\\\\').map(r => r.split('&').map(s => s.trim()));
const asked = (rows) => `[[${rows.map(r => r.join(', ')).join('], [')}]]`;
const splitTop = (s) => { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '{' || ch === '(') d++; if (ch === '}' || ch === ')') d--; if (ch === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += ch; } out.push(cur.trim()); return out; };

let checks = 0, fails = 0, findings = 0, forms = 0, nNum = 0, nExpr = 0, nRows = 0;
let matParts = 0, matWrong = 0, matOnKey = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const formTable = {};
for (const course of ['elimination', 'least-squares']) for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/${course}/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${course} ${n} ${it.id} ${k}`;
    const by = (p.feedback && p.feedback.byKey) || {};
    let grade;
    if (w.kind === 'numeric') {
      nNum++; grade = (t) => num(w, t);
      const a = String(w.answer);
      say(grade(a).ok, null, `${where}: key ${a} grades correct`);
      say(grade(a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
      say(grade('x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
      if (w.answer < 0) say(grade(a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
      if (w.unit) say(grade(w.unit === '£' ? '£' + a : a + ' ' + w.unit).ok, null, `${where}: key with its unit ${w.unit} grades correct`);
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
      if (/pmatrix/.test(w.answer)) {
        matParts++;
        say(grade(asked(rowsOf(w.answer))).ok, null, `${where}: the right matrix in the asked form grades correct`);
        for (const x of w.wrong || []) { matWrong++; const r = grade(asked(rowsOf(x.tex))); if (!r.ok && r.key === x.id) matOnKey++; else if (ALL) console.log(`KNOWN   ${where}: wrong "${x.id}" in the asked form gets key ${r.key}${r.line ? ', line "' + r.line + '"' : ''}`); checks++; }
      } else {
        const v = splitTop(w.answer.replace(/^\(|\)$/g, ''));
        for (const [name, [text, want]] of Object.entries(vecForms(v))) {
          const r = grade(text); checks++;
          formTable[name] = formTable[name] || { want, ok: 0, no: [], keys: new Set() };
          if (r.ok) formTable[name].ok++; else { formTable[name].no.push(`${course.slice(0, 2)}${n}.${it.id.slice(2)}.${k}`); formTable[name].keys.add(String(r.key)); }
          if (r.ok !== want) { forms++; if (ALL) console.log(`FORM    ${where}: ${name} "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key})`); }
        }
      }
    } else return;
    const rows = (((ROWS[course] || {})[n] || {})[it.id] || {})[k] || [];
    if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
    for (const [text, want, note] of rows) {
      nRows++;
      const r = grade(text);
      const good = want === true ? r.ok : want === false ? (!r.ok && (r.key === null)) : want === 'LEN' ? (!r.ok && r.key === 'length') : (!r.ok && r.key === want);
      say(good, note, `${where}: typed "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}${r.line ? ', line "' + r.line + '"' : ''}), expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
    }
  });
}
console.log('\nOther ways to type a vector answer: accepted on how many parts, refused on which, with which keys');
for (const [tag, v] of Object.entries(formTable)) console.log(`  ${tag.padEnd(46)} wanted ${v.want ? 'accepted' : 'refused '}  accepted ${String(v.ok).padStart(2)}  refused ${String(v.no.length).padStart(2)}${v.no.length ? '  keys ' + [...v.keys].join(',') : ''}${ALL && v.no.length ? '  ' + v.no.join(' ') : ''}`);
console.log(`\nmatrix parts: ${matParts}; wrong matrices retyped as the question asks: ${matWrong}; on their own key: ${matOnKey} (known engine fault)`);
console.log(`grade-probe: ${checks} checks over ${nNum} numeric and ${nExpr} expression parts, ${nRows} reader rows, ${fails} failures, ${findings} findings, ${forms} form results against the reader`);
process.exit(fails ? 1 : 0);
