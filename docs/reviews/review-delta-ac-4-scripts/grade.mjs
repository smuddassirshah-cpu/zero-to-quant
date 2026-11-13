#!/usr/bin/env node
/* Delta read AC-4: what the engine's own graders (app/js/engine/grade.js: numGrade and exprGrade with the local
   Compute Engine) do with the parts changed by the four fix passes, typed as a learner types.
     - BASE: for every numeric and expression part of the twelve problem sets, the stored answer and each accept[] form
       grade correct; each wrong[] entry typed at its stored value is refused, lands on its own id and has a byKey line.
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id, 'form', null (generic refusal) or
       "NOPARSE". A row with a note is one the review records: when it misbehaves it prints FINDING and does not fail.
   node docs/reviews/review-delta-ac-4-scripts/grade.mjs --local-cdn <pkgs> [--show]     (from the repo root) */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const SHOW = argv.includes('--show');
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return r.ok ? true : (r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null)); };
const expr = (w, t) => { let r; try { r = G.exprGrade(ce, w, t, t); } catch (e) { return 'THROW ' + e.message; } return r.ok ? true : (r.key || null); };

const P1 = 'courses/proof/problems-1', P2 = 'courses/proof/problems-2', P3 = 'courses/proof/problems-3';
const A1 = 'courses/analysis/problems-1', A2 = 'courses/analysis/problems-2', A3 = 'courses/analysis/problems-3';
const L1 = 'courses/linear-maps/problems-1', L2 = 'courses/linear-maps/problems-2', L3 = 'courses/linear-maps/problems-3';
const C1 = 'courses/complex/problems-1', C2 = 'courses/complex/problems-2', C3 = 'courses/complex/problems-3';
const N17 = 'recorded under Verified: the uncollected sum is accepted, which is right (fix-pass finding 17)';
const NFRAC = 'known engine limit, in the inbox: a right exact p + qi in another shape gets the form line (the questions now warn of the shape)';
const N1509 = 'recorded under Verified: the key band edge';
// [file, item id, part (1-based), rows]
const TYPED = [
  // ---- 1. proof
  [P2, 'p-rule-and-domain', 1, [['0', true], ['-4', 'constant'], ['1', 'unit'], ['4', null]]],
  [P2, 'p-rule-and-domain', 2, [['\\frac{y+4}{c}', true], ['(y+4)/c', true], ['\\frac{4+y}{c}', true], ['\\frac{1}{c}(y+4)', true], ['\\frac{y}{c}+\\frac{4}{c}', true], ['\\frac{y-4}{c}', 'sign'], ['cy-4', 'applied-f'], ['c(y+4)', 'times-c'], ['\\frac{y+4}{-2}', null], ['y+\\frac{4}{c}', null]]],
  [P2, 'p-rule-and-domain', 3, [['3', true], ['7', 'sign'], ['16', 'applied-f'], ['-3', 'dropped-minus'], ['-7', null], ['5', null]]],
  [P2, 'p-rule-and-domain', 4, [['23', true], ['7', 'hits'], ['0', 'onto'], ['20', null], ['22', null], ['8', null]]],
  [P3, 'p-two-odd-squares', 1, [['5jk+j+k', true], ['j+k+5jk', true], ['5kj+k+j', true], ['j(5k+1)+k', true], ['5jk', 'lost-middle'], ['25jk+5j+5k', 'factor-five'], ['5jk+j+k+1', null], ['2jk+j+k', null], ['j^2+j+k^2+k', null]]],
  [P3, 'p-two-odd-squares', 3, [['35', true], ['30', 'lost-middle'], ['176', 'whole-product'], ['42', null], ['34', null]]],
  [P3, 'p-two-odd-squares', 4, [['4', true], ['1', 'if-fails'], ['9', null], ['2', null], ['6', null]]],
  [P3, 'p-step-three-sum', 2, [['145', true], ['37', 'guess-a'], ['28', 'last-term']]],
  [P3, 'p-step-three-sum', 3, [['3k^2+5k+2', true], ['2+5k+3k^2', true], ['5k+3k^2+2', true], ['(k+1)(3k+2)', 'form'], ['k(3k-1)+2(3k+1)', 'form'], ['3k^2-k+6k+2', true, N17], ['3k^2+2k+1', 'no-double'], ['3k^2-k', 'copied'], ['3k+2', 'bracket'], ['3k^2+5k+1', null], ['\\frac{3k^2+5k+2}{2}', null]]],
  [P3, 'p-even-test-contra', 2, [['3k^2', true], ['3k^{2}', true], ['3\\cdot k^2', true], ['k^2\\cdot 3', true], ['9k^2', 'no-third'], ['k^2', 'ninth'], ['3k', null], ['2k^2+6k', null], ['3k^2+2', null]]],
  [P3, 'p-even-test-contra', 4, [['12', true], ['-12', 'sign'], ['36', 'n-squared'], ['38', 'whole'], ['-8', null], ['6', null]]],
  // ---- 2. analysis
  [A1, 'p-cube-root-twenty', 1, [['2.6875', true], ['2.75', 'right-end'], ['2.625', 'one-short'], ['2.5', null], ['2.69', null], ['2.688', null], ['43/16', true]]],
  [A1, 'p-cube-root-twenty', 2, [['-2413', true], ['2413', 'sign'], ['-3271', 'squares'], ['75411', 'no-twenty'], ['-979', null], ['-2,413', true]]],
  [A1, 'p-cube-root-twenty', 4, [['53', true], ['52', 'round-down'], ['51', 'no-plus-one'], ['37', 'no-ones'], ['16', null], ['52.16', null], ['54', null]]],
  [A2, 'p-sum-law-band', 1, [['\\frac{17}{2n+5}', true], ['17/(2n+5)', true], ['\\frac{17}{5+2n}', true], ['\\frac{23}{2n+5}', 'plus-one'], ['-\\frac{17}{2n+5}', 'sign'], ['\\frac{-17}{2n+5}', 'sign'], ['\\frac{14}{2n+5}', null], ['\\frac{17}{2n}', null]]],
  [A2, 'p-sum-law-band', 2, [['423', true], ['422', 'round-down'], ['211', 'full-band'], ['138', null], ['422.5', null], ['424', null]]],
  [A2, 'p-sum-law-band', 3, [['200', true], ['199', 'equal'], ['100', 'full-band'], ['80', null], ['201', null]]],
  [A2, 'p-sum-law-band', 4, [['423', true], ['200', 'min'], ['623', 'sum'], ['138', null]]],
  [A2, 'p-sum-law-band', 5, [['311', true], ['423', 'proof'], ['310', 'round-down'], ['109', null], ['312', null], ['310.48', null]]],
  [A3, 'p-alternating-quarters', 5, [['0.1597', true], ['0.15967', true], ['0.159668', true], ['327/2048', true], ['0.1596', true], ['0.16', 'sum'], ['0.160', 'sum'], ['0.1600', 'sum'], ['4/25', 'sum'], ['0.1601', 's7'], ['0.16010', 's7'], ['0.1600952', 's7'], ['0.1563', 's4'], ['0.4438', 'sizes'], ['0.1598', null], ['0.1599', null], ['0.15', null]]],
  // ---- 3. linear-maps
  [L2, 'p-futures-exposure', 4, [['(3, 4)', true], ['(3,4)', true], ['(1, 1)', 'b-coords'], ['(37, 41)', 'applied-a'], ['(\\frac{17}{3}, \\frac{20}{3})', 'carried-sign'], ['(\\frac{29}{6}, \\frac{35}{6})', 'carried-entrywise'], ['(29/6, 35/6)', 'carried-entrywise'], ['(4, 3)', null]]],
  [L3, 'p-currency-duals', 4, [['(67, 56)', true], ['(67,56)', true], ['(11, 12)', 'standard'], ['(56, 67)', 'swapped'], ['(57, 46)', 'carried-three'], ['(57,46)', 'carried-three'], ['(23, 22)', 'carried'], ['(46, 57)', null]]],
  // ---- 4. complex
  [C1, 'p-parallel-branches', 2, [['4.15+0.95i', true], ['2.75+3.25i', 'wrong-factor']]],
  [C1, 'p-parallel-branches', 4, [['2.819', true], ['2.819 A', true], ['2.819A', true], ['2.819 amps', true], ['51.084', 'times']]],
  [C1, 'p-turning-frames', 1, [['\\frac{3}{2}+\\frac{\\sqrt{3}}{2}i', true], ['1.5+\\frac{\\sqrt{3}}{2}i', true], ['\\frac{3}{2}+\\frac{\\sqrt{3}i}{2}', true, NFRAC], ['\\frac{3+\\sqrt{3}i}{2}', true, NFRAC], ['\\frac{3}{2}+\\frac{1}{2}\\sqrt{3}i', true, NFRAC], ['\\frac{3}{2}+i\\frac{\\sqrt{3}}{2}', true, NFRAC], ['1.5+0.866i', null], ['\\frac{3}{2}-\\frac{\\sqrt{3}}{2}i', 'lower']]],
  [C1, 'p-turning-frames', 3, [['\\frac{\\pi}{6}', true], ['\\pi/6', true], ['30', 'degrees'], ['30^\\circ', 'degrees', 'recorded: the degree sign typed'], ['\\frac{\\pi}{3}', 'inverted'], ['\\frac{5\\pi}{6}', 'carried-minus-b'], ['0.5236', 'form', 'recorded: a decimal where exact is asked']]],
  [C1, 'p-four-lamps', 2, [['\\frac{2\\pi}{3}', true], ['2\\pi/3', true], ['120', 'degrees'], ['-\\frac{\\pi}{3}', 'arctan'], ['\\frac{\\pi}{3}', 'reference'], ['\\frac{5\\pi}{6}', 'swapped']]],
  [C1, 'p-four-lamps', 3, [['\\frac{3\\sqrt{3}}{2}+\\frac{3}{2}i', true], ['\\frac{3\\sqrt{3}}{2}+1.5i', true], ['\\frac{3}{2}\\sqrt{3}+\\frac{3}{2}i', true, NFRAC], ['\\frac{3\\sqrt{3}+3i}{2}', true, NFRAC], ['2.598+1.5i', null]]],
  [C1, 'p-four-lamps', 4, [['\\frac{3}{2}-\\frac{3\\sqrt{3}}{2}i', true], ['1.5-\\frac{3\\sqrt{3}}{2}i', true], ['\\frac{3}{2}-\\frac{3}{2}\\sqrt{3}i', true, NFRAC], ['1.5-1.5\\sqrt{3}i', true, NFRAC], ['\\frac{3-3\\sqrt{3}i}{2}', true, NFRAC], ['-\\frac{3}{2}+\\frac{3\\sqrt{3}}{2}i', 'times-i'], ['\\frac{3\\sqrt{3}}{2}-\\frac{3}{2}i', 'conjugate']]],
  [C1, 'p-four-lamps', 5, [['4.243', true], ['4.243 m', true], ['4.243m', true], ['4.243 metres', true], ['3', 'radius'], ['4.712', 'arc'], ['6', 'opposite']]],
  [C1, 'p-neutral-wire', 1, [['10.392', true], ['10.3923', true], ['-6', 'swapped'], ['6', 'real-size'], ['0.866', 'unscaled'], ['0.439', 'degrees'], ['10.39', null], ['-10.392', null]]],
  [C1, 'p-neutral-wire', 2, [['-\\frac{7}{2}-\\frac{7\\sqrt{3}}{2}i', true], ['-3.5-\\frac{7\\sqrt{3}}{2}i', true], ['-\\frac{7}{2}-\\frac{7}{2}\\sqrt{3}i', true, NFRAC], ['-3.5-3.5\\sqrt{3}i', true, NFRAC], ['-\\frac{7}{2}+\\frac{7\\sqrt{3}}{2}i', 'sin-sign'], ['-\\frac{7\\sqrt{3}}{2}-\\frac{7}{2}i', 'swapped']]],
  [C1, 'p-neutral-wire', 3, [['\\frac{5}{2}+\\frac{5\\sqrt{3}}{2}i', true], ['2.5+\\frac{5\\sqrt{3}}{2}i', true], ['2.5+2.5\\sqrt{3}i', true, NFRAC], ['\\frac{5}{2}+\\frac{5}{2}\\sqrt{3}i', true, NFRAC], ['-\\frac{19}{2}+\\frac{5\\sqrt{3}}{2}i', 'no-first'], ['\\frac{5}{2}+\\frac{19\\sqrt{3}}{2}i', 'carried-sin-sign']]],
  [C1, 'p-neutral-wire', 4, [['5', true], ['5 A', true], ['5A', true], ['5 amps', true], ['25', 'squared']]],
  [C2, 'p-mesh-map', 1, [['-12.75+3i', true], ['3i-12.75', true], ['-3.75-3i', 'square-parts'], ['-12.75-12i', 'no-cross'], ['5.25+3i', 'i-squared'], ['-\\frac{51}{4}+3i', true]]],
  [C2, 'p-log-branches', 1, [['17', true], ['23', 'added'], ['289', 'no-root'], ['8', null], ['7', null]]],
  [C2, 'p-log-branches', 2, [['2.0608', true], ['2.06075', true], ['2.0607', true, 'recorded: one digit down at the band edge'], ['2.061', null], ['2.06', null], ['-1.0808', 'arctan'], ['1.0808', 'reference'], ['2.6516', 'inverted'], ['118.07', 'degrees'], ['118.1', null], ['118.0725', 'degrees'], ['2.6180', null], ['-4.2224', null]]],
  [C2, 'p-log-branches', 3, [['-4.2224', true], ['-4.22243', true], ['4.2224', 'sign'], ['2.0608', 'principal'], ['-2.0608', 'dropped-turn'], ['-4.222', null], ['8.3440', null]]],
  [C2, 'p-log-branches', 4, [['0.0588', true], ['0.05882', true], ['1/17', true], ['0.059', null], ['0.06', null], ['17', 'no-inverse'], ['2.8332', 'log-of-modulus'], ['0.0035', 'squared'], ['0.125', null]]],
  [C2, 'p-log-branches', 5, [['0.1274', true], ['0.12736', true], ['0.1273', true, 'recorded: one digit down at the band edge'], ['0.127', null], ['7.852', 'sign'], ['7.8516', 'sign'], ['68.2', 'carried-branch'], ['68.20', 'carried-branch'], ['68.197', 'carried-branch'], ['1', 'unit'], ['0.0729', null]]],
  [C2, 'p-modulus-plus-z', 1, [['3x^2+y^2+4x', true], ['y^2+4x+3x^2', true], ['x^2-y^2+4x', 'no-mod'], ['2x^2+4x', 'one-copy'], ['3x^2+y^2', 'no-linear'], ['x^2+y^2+x', null], ['3x^2+y^2+4x+i(2xy+4y)', null]]],
  [C2, 'p-modulus-plus-z', 2, [['4x', true], ['6x+4', 'no-v'], ['4x+4', 'short-v'], ['2x', null]]],
  [C2, 'p-modulus-plus-z', 3, [['4y', true], ['0', 'minus'], ['2y', 'no-v'], ['4x', null]]],
  [C2, 'p-modulus-plus-z', 4, [['4-0.01i', true], ['-0.01i+4', true], ['4-\\frac{1}{100}i', true], ['4-\\frac{i}{100}', true], ['4+0.01i', 'sign'], ['4+0.03i', 'mod-as-square'], ['-0.01i', 'no-linear'], ['1-0.01i', null], ['4', null]]],
  [C3, 'p-traffic-island', 5, [['0.5', true], ['0.50', true], ['1/2', true], ['0.5 m^2', true], ['0.5 m²', true], ['0.45', null], ['0.55', null], ['1', 'no-two'], ['-0.5', 'sign']]],
  [C3, 'p-lighthouse-flashes', 1, [['0.5+2.5i', true], ['\\frac{1}{2}+\\frac{5}{2}i', true], ['2.5i+0.5', true], ['\\frac{1+5i}{2}', true, NFRAC], ['0.5-2.5i', 'lower'], ['-0.5+2.5i', 'minus-b'], ['1+5i', 'no-four'], ['1+3i', null]]],
  [C3, 'p-lighthouse-flashes', 2, [['-\\frac{1}{10}i', true], ['-\\frac{i}{10}', true], ['-0.1i', true], ['0-\\frac{1}{10}i', true, NFRAC], ['\\frac{1}{10i}', true, NFRAC], ['\\frac{-i}{10}', true, NFRAC], ['\\frac{1}{10}', 'no-i'], ['\\frac{1}{10}i', 'plus'], ['\\frac{1}{52}-\\frac{5}{52}i', 'q-prime'], ['-\\frac{i}{6}', null]]],
  [C3, 'p-lighthouse-flashes', 3, [['1.592', true], ['1.5915', true], ['5/\\pi', 'NOPARSE', 'recorded: the exact form is not read by a numeric field'], ['1.59', null], ['0.628', 'integral'], ['0.796', 'both-poles'], ['3.183', 'no-two'], ['0.955', null]]],
  [C3, 'p-lighthouse-flashes', 4, [['0.0821', true], ['0.08208', true], ['0.082', true, 'recorded: 3 places at the band edge'], ['0.08', null], ['12.1825', 'sign'], ['12.182', 'sign'], ['0.0516', 'no-c'], ['0.3679', 'standard'], ['0.0498', null]]],
  [C3, 'p-lighthouse-flashes', 5, [['0.0821', true], ['0.0067', 'no-half'], ['0.2865', 'one-factor'], ['0.0498', null]]],
  [C3, 'p-share-moments', 2, [['0.7985', true], ['0.79852', true], ['0.799', null], ['0.9277', 'no-square'], ['0.6376', 'no-half'], ['1.2523', 'sign'], ['66.61', null], ['£0.7985', true, 'recorded: no unit is asked now']]],
  [C3, 'p-share-moments', 4, [['15.08', true], ['£15.08', true], ['15.081', true], ['15.10', 'own-rounding'], ['15.1', 'own-rounding'], ['15.09', true, N1509], ['15.07', true, N1509], ['227.44', 'variance'], ['227.4', 'variance'], ['227.49', 'variance'], ['227.84', null], ['228.11', null], ['67.81', 'not-squared'], ['14.31', 'log-sd']]],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (SHOW) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const docs = {};
const load = (f) => docs[f] || (docs[f] = JSON.parse(fs.readFileSync(`app/content/${f}.json`, 'utf8')));
const describe = (got) => (got === true ? 'accepted' : got === null ? 'refused, generic line' : got === 'NOPARSE' ? 'not read (field will not submit)' : 'refused, line "' + got + '"');

// BASE: every numeric and expression part of the twelve sets
for (const file of [P1, P2, P3, A1, A2, A3, L1, L2, L3, C1, C2, C3]) {
  for (const it of load(file).items) {
    (it.parts || []).forEach((p, i) => {
      const w = p.widget; if (!w || (w.kind !== 'numeric' && w.kind !== 'expression')) return;
      const by = (p.feedback && p.feedback.byKey) || {}, where = `${file.replace('courses/', '')} ${it.id} part ${i + 1}`;
      if (w.kind === 'expression') {
        for (const a of [w.answer, ...(w.accept || [])]) say(expr(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${expr(w, a)})`);
        for (const x of w.wrong || []) { say(expr(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${expr(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
      } else if (!Array.isArray(w.answers)) {
        say(num(w, String(w.answer)) === true, null, `${where}: answer ${w.answer} grades correct (got ${num(w, String(w.answer))})`);
        for (const x of w.wrong || []) { say(num(w, String(x.value)) === x.id, null, `${where}: wrong ${x.id} ${x.value} lands on its id (got ${num(w, String(x.value))})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); }
      }
    });
  }
}
const base = checks;
for (const [file, id, part, rows] of TYPED) {
  const it = load(file).items.find((x) => x.id === id);
  if (!it) throw new Error('no item ' + file + ' ' + id);
  const w = it.parts[part - 1].widget, grade = w.kind === 'expression' ? expr : num;
  const where = `${file.replace('courses/', '')} ${id} part ${part}`;
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    say(got === want, note, `${where}: typed "${typed}" -> ${describe(got)}; expected ${describe(want)}`);
  }
}
// Small item 1: bank/statistics-2 es-intervals-poll-margin, the `decimal` wrong entry 0.04801 with tol 0.05 (finding 5.1)
{
  const NP = 'finding 5.1: the `decimal` band is wider than its value';
  const w0 = JSON.parse(fs.readFileSync('app/content/bank/statistics-2.json', 'utf8')).items.find((x) => x.id === 'es-intervals-poll-margin').widget;
  const where = 'bank/statistics-2 es-intervals-poll-margin';
  // as it stands: [typed, what the learner did, what it should reach]
  for (const [t, want] of [['4.8', true], ['4.80', true], ['4.801', true], ['4.9', 'used-half'], ['2.4', 'no-multiplier'], ['2.45', 'no-multiplier'], ['0.048', 'decimal'], ['0.04801', 'decimal'], ['0.0480', 'decimal']]) say(num(w0, t) === want, null, `${where}: typed "${t}" -> ${describe(num(w0, t))}; expected ${describe(want)}`);
  for (const [t, what] of [['0.049', 'the p = 0.5 margin as a decimal'], ['0.0245', 'one standard error as a decimal'], ['0.024', 'one standard error as a decimal'], ['0.05', 'two worst-case standard errors as a decimal'], ['0', 'nothing'], ['0.01', 'a guess'], ['0.09', 'a guess'], ['0.096', 'twice the margin as a decimal'], ['0.0024', 'p(1 - p) = 0.24 over 100']]) say(num(w0, t) === null, NP, `${where}: typed "${t}" (${what}) -> ${describe(num(w0, t))}; expected ${describe(null)}`);
  // PROPOSED: tol 0.0004 (the key's 0.04 points as a decimal)
  const w = { ...w0, wrong: w0.wrong.map((x) => (x.id === 'decimal' ? { ...x, tol: { abs: 0.0004 } } : x)) };
  for (const [t, want] of [['4.8', true], ['4.801', true], ['4.9', 'used-half'], ['2.4', 'no-multiplier'], ['0.048', 'decimal'], ['0.04801', 'decimal'], ['0.0480', 'decimal'], ['0.0484', 'decimal'], ['0.049', null], ['0.0245', null], ['0.024', null], ['0.05', null], ['0', null], ['0.01', null], ['0.09', null], ['0.096', null], ['0.0024', null]]) say(num(w, t) === want, null, `PROPOSED ${where} decimal tol 0.0004: typed "${t}" -> ${describe(num(w, t))}; expected ${describe(want)}`);
}
console.log(`grade: ${checks} checks (${base} base, ${checks - base} typed), ${fails} failures, ${findings} FINDING rows (recorded in the review)`);
process.exit(fails ? 1 : 0);
