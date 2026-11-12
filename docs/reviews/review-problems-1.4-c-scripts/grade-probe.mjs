#!/usr/bin/env node
/* Second read, eigen problems-1 to -3: what the engine's own graders do with each typed part.
   Loads app/js/engine/grade.js and the local Compute Engine (as review-problems-1.4-b-scripts/grade-probe.mjs does), then for
     numeric     numGrade, or numSetGrade for the three parts that take a pair of eigenvalues (the calls numeric.js makes):
                 the key grades correct, also with more places, a letter and "=", a true minus sign and its unit;
                 every wrong[] is refused on its own key and has a byKey line
     expression  exprGrade (the call expression.js makes): the key and every accept[] grade correct; every wrong[].tex is refused
                 on its own key and has a line; then other ways to type the same vector (FORMS)
   and the reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line,
   'LEN' = refused with the engine's shape line, 'CNT' = refused with the engine's count line, N = Check stays unavailable (no number
   read). A row with a note is one the reader holds to be a fault (FINDING, not a failure).

   node docs/reviews/review-problems-1.4-c-scripts/grade-probe.mjs --local-cdn <pkgs> [--all]      (from the repo root) */
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
const isSet = (w) => Array.isArray(w.answers) && w.answers.length > 0;
const num = (w, t) => { const r = isSet(w) ? G.numSetGrade(w, t) : G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null), line: r.line }; };
const expr = (w, t) => { try { const r = G.exprGrade(ce, w, t, t); return { ok: !!r.ok, key: r.key || null, line: r.line }; } catch (e) { return { ok: false, key: 'THROW ' + e.message }; } };

const T = true, F = false, N = 'NOPARSE';
const SCAL = 'the right answer as a vector over a number is refused with the false line "That is a single value"';
const R127 = 'the value the part\'s own feedback line gives (20/15.81 = 1.2650, so 1.27) is refused';
const SHORT = 'the answer one step short has no line and gets the generic line, which names the step the learner took';
const SUM = 'the form of the part\'s own `correct` line, a sum of eigenvector parts, is refused with the false line "That is a single value"';
const FRONT = 'a slip typed with a number in front does not reach its line; it gets the false line "That is a single value"';
const UNIT = 'not read as a number, so Check stays unavailable and nothing says why';
/* ROWS[set][item][part] = [[text, expected, note?], ...] */
const ROWS = {
  1: {
    'p-sketch-warp': {
      1: [['2.0', T], ['\\lambda=2', T], ['4', 'sign'], ['3', F], ['-2', F], ['6', F]],
      2: [['b=-6', T], ['−6', T], ['-6.0', T], ['6', 'dropped-sign'], ['-10', 'wrong-entry'], ['0', 'carried'], ['-12', F], ['2', F]],
      3: [['\\mu=1', T], ['1.0', T], ['5', 'added'], ['3', 'trace-sign'], ['-5', 'det-sign'], ['2', F], ['-1', F]],
      4: [['(2, 1.0)', T], ['\\begin{pmatrix}2\\\\1\\end{pmatrix}', T], ['(4,2)', F], ['(1, 0.5)', F], ['(-2,-1)', F], ['(3,1)', 'other'], ['(-2,1)', 'sign'], ['(1,2)', 'swapped'], ['2', 'LEN']],
      5: [['(50.0, 17)', T], ['(8,3)', 'one-warp'], ['(32,12)', 'times-four'], ['(86,29)', 'carried'], ['16(3,1)+(2,1)', T, SUM], ['(17,50)', F], ['(26,9)', F], ['(48,16)', F], ['(50,17,0)', 'LEN']],
    },
    'p-garden-path': {
      1: [['3, -2', T], ['-2, 3', T], ['3,−2', T], ['3.0, -2.0', T], ['2, -3', 'sign'], ['-3, 2', 'sign'], ['3, 2', 'dropped-sign'], ['1, 0', 'diagonal'], ['0, 1', 'diagonal'], ['3', 'CNT'], ['3, -2, 1', 'CNT'], ['(3, -2)', T], ['3 and -2', T], ['x = 3, x = -2', T], ['λ = 3, λ = -2', T, 'the letter the question uses is not read: ' + UNIT], ['6, -1', F], ['-6, 1', F]],
      2: [['(3, 1.0)', T], ['(6,2)', F], ['(1,1/3)', F], ['(-2,1)', 'other'], ['(-3,1)', 'sign'], ['(1,3)', F], ['3', 'LEN']],
      3: [['(\\frac35,\\frac25)', T], ['(0.60, 0.40)', T], ['(6/10, 4/10)', T], ['(.6,.4)', T], ['(3,2)/5', T, SCAL], ['(2/5,3/5)', 'swapped'], ['(0.4,0.6)', 'swapped'], ['(1,1)', 'not-split'], ['(-3,4)', 'carried'], ['(3,2)', F], ['3/5', 'LEN'], ['(0.6,0.4,0)', 'LEN']],
      4: [['35,839', T], ['35 839', T], ['35839.0', T], ['35019.8', 'sign'], ['35020', 'sign'], ['105469', 'first-entry'], ['11605', 'one-short'], ['24234', 'swapped'], ['35838', F], ['35840', F], ['35429', F], ['59049', F]],
    },
    'p-hill-bikes': {
      1: [['0.30', T], ['3/10', T], ['.3', T], ['p=0.3', T], ['30%', T], ['0.075', 'swapped'], ['0.45', 'total'], ['0.15', F], ['0.6', F], ['0.33', F], ['60', F]],
      2: [['.55', T], ['11/20', T], ['0.550', T], ['1.55', 'trace'], ['0.64', 'det-sign'], ['0.775', 'carried'], ['0.5', F], ['0.6', F], ['-0.55', F], ['0.45', F]],
      3: [['321.0', T], ['321 bikes', T], ['420', 'one-night'], ['181.5', 'no-steady'], ['182', 'no-steady'], ['181', 'no-steady'], ['279', 'river'], ['440.25', 'carried'], ['440', 'carried'], ['320', F], ['322', F], ['200', F], ['121', F]],
      4: [['k=5', T], ['5 nights', T], ['5.0', T], ['4', 'rounded-down'], ['6', 'no-steady'], ['4.33', F], ['3', F]],
    },
    'p-lazy-frog': {
      1: [['(1/4,1/2,1/4)', T], ['(\\frac14,\\frac12,\\frac14)', T], ['(.25,.5,.25)', T], ['(0.25, 0.50, 0.25)', T], ['(2/8,4/8,2/8)', T], ['\\frac14(1,2,1)', T], ['(1,2,1)/4', T, SCAL], ['(1,2,1)', 'unscaled'], ['(1/3,1/3,1/3)', 'uniform'], ['(0.5,0.25,0.25)', F], ['(0.25,0.5)', 'LEN'], ['(0.2,0.6,0.2)', F]],
      2: [['−1', T], ['-1.0', T], ['\\lambda=-1', T], ['1', 'dropped-sign'], ['-2', 'middle-entry'], ['0', F], ['2', F]],
      4: [['(0,1/2)', T], ['(0, .5)', T], ['(0.0, 0.50)', T], ['0, 0.5', T], ['(0.5,0)', F], ['(-1,0)', 'kept-m'], ['(0,1)', 'no-half'], ['(-0.5,0)', 'halved-only'], ['(-1/2, 0)', 'halved-only'], ['(0,0.5,1)', 'LEN'], ['(0,0)', F]],
      5: [['5/16', T], ['.3125', T], ['0.31250', T], ['0.313', F], ['0.31', F], ['31.25%', T], ['0.375', 'half-dropped'], ['3/8', 'half-dropped'], ['0.25', 'steady-only'], ['0', 'not-lazy'], ['0.75', 'carried'], ['0.5', F], ['0.1875', F], ['0.0625', F]],
    },
  },
  2: {
    'p-oval-pond': {
      1: [['b=2', T], ['2.0', T], ['4', 'whole-cross'], ['8', F], ['1', F]],
      2: [['4, 9', T], ['9,4', T], ['9.0, 4.0', T], ['5, 8', 'diagonal'], ['-4, -9', 'sign'], ['4', 'CNT'], ['6, 6', F], ['36, 13', F], ['2, 3', F], ['3, 2', F]],
      3: [['(2,−1)', T], ['(2, -1.0)', T], ['(2,4)', 'big'], ['(2,1)', 'sign'], ['(-2,1)', F], ['(1,-0.5)', F], ['(4,-2)', F], ['(1,2)', F], ['-1', 'LEN']],
      4: [['3 m', T], ['3m', T], ['3.0', T], ['3 metres', T], ['2', 'short'], ['9', 'no-root'], ['6', 'full-axis'], ['1.34', F], ['4', F]],
      5: [['18.85 m²', T], ['18.85 m^2', T, 'the unit typed with ^2: ' + UNIT + ' (raised by the author)'], ['18.850', T], ['18.8496', T], ['18.84', F], ['18.8', F], ['18.9', F], ['19', F], ['113.1', 'no-root'], ['113.10', 'no-root'], ['113.097', 'no-root'], ['75.4', 'full-axes'], ['75.40', 'full-axes'], ['75.398', 'full-axes'], ['28.27', 'one-axis'], ['28.274', 'one-axis'], ['12.57', F], ['6', F], ['37.70', F]],
    },
    'p-river-gauges': {
      1: [['.36', T], ['9/25', T], ['0.360', T], ['1.64', 'plus'], ['0.2', 'no-square'], ['0.6', F], ['-0.36', F], ['0.4', F]],
      2: [['1.28r-0.28-r^2', T], ['-(r^2-1.28r+0.28)', T], ['0.36-0.64+1.28r-r^2', T], ['0.36-0.8(0.8-0.8r)+r(0.64-r)', T], ['-r^2+\\frac{32}{25}r-\\frac{7}{25}', T], ['-r^{2}+1.28r-0.28', T], ['-r^2+1.28\\cdot r-0.28', T], ['-r^2+1.28r-.28', T],
        ['r^2-1.28r+0.28', F], ['-r^2-1.28r-0.28', 'cross-sign'], ['1.28r-0.28', 'no-square'], ['-r^2+1.28r+0.28', F], ['-r^2+0.64r-0.28', F], ['-r^2+1.28r+0.36', F], ['-x^2+1.28x-0.28', F]],
      3: [['r=0.28', T], ['r>0.28', T, 'the form the question invites (above what value): ' + UNIT], ['7/25', T], ['.28', T], ['0.280', T], ['1', 'other-root'], ['-0.28', 'carried'], ['0.3', F], ['-1', F], ['0.72', F], ['0.64', F]],
      4: [['a=-1.6', T], ['−1.6', T], ['-8/5', T], ['-1.60', T], ['1.6', 'dropped-sign'], ['-1.25', 'no-r'], ['-1.28', F, SHORT], ['-2', F], ['-1.5', F]],
      5: [['−0.16', T], ['-.16', T], ['-4/25', T], ['-0.160', T], ['0.16', 'dropped-sign'], ['0', 'bound'], ['2.2', 'no-double'], ['-0.2', F], ['4.56', F], ['-0.56', F], ['0.4', F]],
    },
    'p-tank-thermometers': {
      1: [['5.0', T], ['3', 'diagonal'], ['15', 'all-entries'], ['2', F], ['9', F]],
      2: [['2.0', T], ['4', 'added'], ['-2', 'sign'], ['5', F], ['0', F], ['3', F]],
      3: [['2.0', T], ['4', 'no-second'], ['7', 'no-first'], ['9', F], ['5', F]],
      4: [['5/3', T], ['1.6667', T], ['1.66667', T], ['1.67', F], ['1.666', F], ['1.7', F], ['5', 'no-length'], ['0.556', 'ninth'], ['5/9', 'ninth'], ['0.5556', 'ninth'], ['0.56', F], ['15', F]],
      5: [['1.760', T], ['44/25', T], ['1.7604', T], ['1.8', F], ['1.71', 'no-eigenvalue'], ['1.713', 'no-eigenvalue'], ['0.09', 'd-only'], ['0.093', 'd-only'], ['0.0933', 'd-only'], ['1.14', 'no-cov'], ['0.62', F], ['1.67', F], ['1.77', F], ['1.75', F]],
    },
  },
  3: {
    'p-branch-sales': {
      1: [['21.0', T], ['29', 'diagonal-or-sign'], ['24', 'aat'], ['25', F], ['8', F], ['32', F]],
      2: [['50, 8', T], ['8,50', T], ['50.0, 8.0', T], ['29, 21', 'entries'], ['58, 0', 'carried'], ['0, 58', 'carried'], ['7.07, 2.83', F], ['50', 'CNT'], ['58, 400', F]],
      3: [['(4/5,3/5,0)', T], ['(.8,.6,0)', T], ['(0.80, 0.60, 0.0)', T], ['(\\frac{8}{10},\\frac{6}{10},0)', T], ['\\frac{1}{10}(8,6,0)', T], ['(8,6,0)/10', T, SCAL], ['\\frac{(8,6,0)}{10}', T, SCAL],
        ['(8,6,0)', 'unscaled'], ['(0.16,0.12,0)', 'no-root'], ['(-0.8,-0.6,0)', F], ['(0.8,0.6)', 'LEN'], ['(5.66,4.24,0)', F], ['(1.13,0.85,0)', F], ['(0.6,0.8,0)', F]],
      4: [['(4.0,3.0,0)', T], ['5(0.8,0.6,0)', T, 'the form of the part\'s own `carried` line ("the column is $5\\mathbf{u}_1$") is refused with the false line "That is a single value"'], ['(0.8,0.6,0)', 'u-only'], ['(40,30,0)', 'carried'], ['(4,3,2)', F], ['(4,4)', 'LEN'], ['(5.66,4.24,0)', F], ['(4,3)', 'LEN']],
      5: [['50/58', T], ['25/29', T], ['0.8621', T], ['.862', T], ['86.2%', T], ['0.86', F], ['0.863', F], ['0.714', 'unsquared'], ['0.7143', 'unsquared'], ['0.138', 'error-share'], ['4/29', 'error-share'], ['0.5', 'half'], ['0.9', F], ['50', F]],
    },
    'p-crab-sizes': {
      1: [['90.0', T], ['90 mm²', T], ['72', 'over-n'], ['360', 'no-divide'], ['3090', 'raw'], ['130', F], ['182.5', F], ['2472', F], ['-90', F]],
      2: [['250, 62.5', T], ['62.5,250', T], ['250, 125/2', T], ['250.0, 62.50', T], ['130, 182.5', 'diagonal'], ['200, 50', 'over-n'], ['250', 'CNT'], ['312.5, 15625', F], ['250, 62', F], ['250, 63', F]],
      3: [['(3/5,4/5)', T], ['(.6,.8)', T], ['(0.60, 0.80)', T], ['\\frac15(3,4)', T], ['(3,4)/5', T, SCAL], ['0.2(-3,-4)', 'no-flip', FRONT], ['(0.8,-0.6)', 'first-column'], ['(-0.6,-0.8)', 'no-flip'], ['(0.8,0.6)', F], ['(-0.8,0.6)', F], ['(3,4)', F], ['(0.6,0.8,0)', 'LEN']],
      4: [['20.0', T], ['20 mm', T], ['-20', 'no-flip'], ['88', 'raw'], ['-5', 'pc2'], ['5', F], ['19', F], ['27', F]],
      5: [['1.265', T], ['1.2649', T], ['1.26 sd', T], ['1.26 standard deviations', T, 'a unit of two words: ' + UNIT], ['1.27', T, R127], ['1.3', F], ['1.2', F], ['0.08', 'variance'], ['1.13', 'total'], ['2.53', 'pc2-sd'], ['0.8', F], ['1.41', F]],
    },
    'p-site-anomalies': {
      1: [['39.0', T], ['1170', 'no-divide'], ['37.74', 'over-n'], ['38', 'over-n'], ['37.7', 'over-n'], ['1.8', 'unsquared'], ['2', 'unsquared'], ['54', F], ['30', F], ['39.5', F]],
      2: [['37.5/39', T], ['25/26', T], ['0.9615', T], ['96.2%', T], ['0.96', F], ['0.961', F], ['0.833', 'unsquared'], ['0.769', 'pc1-only'], ['0.032', 'carried'], ['0.992', F], ['0.95', F]],
      3: [['3.0', T], ['3 components', T], ['2', 'two'], ['4', 'all'], ['1', F]],
      4: [['9.0', T], ['3', 'unsquared'], ['45', 'rank-two'], ['1161', 'kept'], ['0.3', F], ['1170', F], ['81', F]],
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
const splitTop = (s) => { const out = []; let d = 0, cur = ''; for (const ch of s) { if (ch === '{' || ch === '(') d++; if (ch === '}' || ch === ')') d--; if (ch === ',' && d === 0) { out.push(cur.trim()); cur = ''; } else cur += ch; } out.push(cur.trim()); return out; };

let checks = 0, fails = 0, findings = 0, forms = 0, nNum = 0, nSet = 0, nExpr = 0, nRows = 0, nMat = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const formTable = {};
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/eigen/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${n} ${it.id} ${k}`;
    const by = (p.feedback && p.feedback.byKey) || {};
    let grade;
    if (w.kind === 'numeric' && isSet(w)) {
      nSet++; grade = (t) => num(w, t);
      const a = w.answers.map(String);
      say(grade(a.join(', ')).ok, null, `${where}: key ${a.join(', ')} grades correct`);
      say(grade([...a].reverse().join(',')).ok, null, `${where}: key in the other order grades correct`);
      for (const x of w.wrong || []) {
        const r = grade(String(x.value));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} lands on its key (got ok=${r.ok} key=${r.key})`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
      }
    } else if (w.kind === 'numeric') {
      nNum++; grade = (t) => num(w, t);
      const a = String(w.answer);
      say(grade(a).ok, null, `${where}: key ${a} grades correct`);
      say(grade(a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
      say(grade('x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
      if (w.answer < 0) say(grade(a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
      if (w.unit) say(grade(a + ' ' + w.unit).ok, null, `${where}: key with its unit ${w.unit} grades correct`);
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
      if (/pmatrix/.test(w.answer)) nMat++;
      else if (/^\(/.test(w.answer)) {
        const v = splitTop(w.answer.replace(/^\(|\)$/g, ''));
        for (const [name, [text, want]] of Object.entries(vecForms(v))) {
          const r = grade(text); checks++;
          formTable[name] = formTable[name] || { want, ok: 0, no: [], keys: new Set() };
          if (r.ok) formTable[name].ok++; else { formTable[name].no.push(`${n}.${it.id.slice(2)}.${k}`); formTable[name].keys.add(String(r.key)); }
          if (r.ok !== want) { forms++; console.log(`FORM    ${where}: ${name} "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key})`); }
        }
      }
    } else return;
    const rows = ((ROWS[n] || {})[it.id] || {})[k] || [];
    if (!rows.length) { fails++; console.log(`FAIL    ${where}: no reader rows`); }
    for (const [text, want, note] of rows) {
      nRows++;
      const r = grade(text);
      const good = want === true ? r.ok : want === false ? (!r.ok && (r.key === null)) : want === 'LEN' ? (!r.ok && r.key === 'length') : want === 'CNT' ? (!r.ok && r.key === 'count') : (!r.ok && r.key === want);
      say(good, note, `${where}: typed "${text}" is ${r.ok ? 'accepted' : 'refused'} (key ${r.key}${r.line ? ', line "' + r.line + '"' : ''}), expected ${want === true ? 'accepted' : want === false ? 'refused on no wrong line' : 'refused on ' + want}`);
    }
  });
}
console.log('\nOther ways to type a vector answer: accepted on how many parts, refused on which, with which keys');
for (const [tag, v] of Object.entries(formTable)) console.log(`  ${tag.padEnd(46)} wanted ${v.want ? 'accepted' : 'refused '}  accepted ${String(v.ok).padStart(2)}  refused ${String(v.no.length).padStart(2)}${v.no.length ? '  keys ' + [...v.keys].join(',') + '  ' + v.no.join(' ') : ''}`);
console.log(`\nmatrix parts (the known engine fault): ${nMat}`);
console.log(`grade-probe: ${checks} checks over ${nNum} numeric, ${nSet} set and ${nExpr} expression parts, ${nRows} reader rows, ${fails} failures, ${findings} findings, ${forms} form results against the reader`);
process.exit(fails ? 1 : 0);
