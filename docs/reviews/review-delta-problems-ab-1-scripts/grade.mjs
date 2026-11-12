#!/usr/bin/env node
/* Delta read of the three problems fix passes (estimation and regression, testing, vectors): what the engine's own graders
   (app/js/engine/grade.js: numGrade for numeric parts, exprGrade with the local Compute Engine for expression parts) do
   with every changed part.
     - the stored answer and each accept[] form grade correct; each wrong[] entry typed at its stored value grades wrong,
       lands on its own id and has a byKey line (FAIL if not). A wrong matrix typed whole is the known engine fault and is
       counted, not failed.
     - TYPED rows [typed, expected, note?]: expected is true (accepted), a wrong id (refused with that line), null (refused
       with the generic line) or "NOPARSE" (the field does not read it). A row with a note is one the reader records in the
       review: when it does not behave as expected it prints as FINDING and does not fail the run.
   node docs/reviews/review-delta-problems-ab-1-scripts/grade.mjs --local-cdn <pkgs> [--show]      (from the repo root) */
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

const ES = 'estimation', RG = 'regression', TS = 'testing', VC = 'vectors';
const UNIT = 'engine, deferred by the fix pass (in the inbox): a unit typed in full after the number stops the field';
const LIT = 'a number in front of a bracket matrix is matched as text against the accept list, not computed: this spelling of a right answer is refused';
const LEN = 'engine (same family as the known list-reading fault): a wrong multiple of a vector is told "That is a single value. The answer has 2 components."';
const SHARED = 'the `decimal` band is wide: this is the decimal of another slip, and the line names a decimal the learner did not type';
// [course, item, part (1-based), rows]
const TYPED = [
  // ---------------- estimation
  [ES, 'p-robot-deliveries', 3, [['0.9', true], ['0.90', true], ['.9', true], ['9/10', true], ['90%', true], ['p=0.9', true], ['0.95', 'middle'], ['0.75', 'unrestricted'], ['1', 'top'], ['1.00', 'top'], ['0.91', null], ['0.85', null]]],
  [ES, 'p-currency-vol', 1, [['0.25', true], ['0.25%', true], ['0.25 %', true], ['.25', true], ['1/4', true], ['0.250', true], ['0.29', 'by-seven'], ['0.286', 'by-seven'], ['0.29%', 'by-seven'], ['1', 'sizes'], ['1%', 'sizes'], ['1.00', 'sizes'],
    ['0.0025', null], ['0.3', null]]],
  [ES, 'p-currency-vol', 2, [['1.09', true], ['1.0874', true], ['1.09%', true], ['1.08', true], ['1.16', 'n-minus-one'], ['1.1625', 'n-minus-one'], ['1.16%', 'n-minus-one'], ['1.12', 'zero-mean'], ['1.1158', 'zero-mean'], ['1.18', 'variance'], ['1.1825', 'variance'],
    ['1.1', null], ['0.0109', null]]],
  [ES, 'p-currency-vol', 3, [['7.84', true], ['7.84%', true], ['7.8414', true], ['7.86', true], ['7.85', true], ['7.83', true], ['56.54', 'times-52'], ['56.55', 'times-52'], ['56.68', 'times-52'], ['56.54%', 'times-52'], ['17.26', 'trading-days'], ['17.30', 'trading-days'],
    ['8.38', 'carried'], ['8.37', 'carried'], ['8.36', 'carried'], ['8.39', 'carried'], ['61.49', 'variance'], ['61.78', 'variance'], ['61.5', 'variance'], ['7.8', null], ['0.0784', null]]],
  [ES, 'p-currency-vol', 4, [['1.96', true], ['1.96%', true], ['1.9603', true], ['1.97', true], ['1.95', true], ['2.77', 'no-two'], ['2.7719', 'no-two'], ['0.77', 'weeks-in-year'], ['0.49', 'no-root'], ['0.49%', 'no-root'], ['2', null], ['0.0196', null], ['1.96 points', true], ['1.96 percentage points', true, UNIT]]],
  [ES, 'p-currency-vol', 5, [['123', true], ['123 weeks', true], ['n=123', true], ['122', 'round-down'], ['246', 'no-two'], ['8', 'unsquared'], ['7.84', 'unsquared'], ['16', 'no-two-unsquared'], ['15.68', 'no-two-unsquared'], ['122.9', null], ['124', null]]],
  [ES, 'p-three-month-fund', 1, [['2.08', true], ['2.08%', true], ['2.0817', true], ['3.61', 'sd'], ['1.70', 'by-n'], ['1.7', 'by-n'], ['4.33', 'no-root'], ['2.1', null], ['0.0208', null]]],
  [ES, 'p-three-month-fund', 3, [['1.70', true], ['1.7', true], ['1.70%', true], ['1.6997', true], ['2.08', 'carried'], ['2.89', 'no-root'], ['2.94', 'one-draw'], ['0.017', null]]],
  [ES, 'p-three-month-fund', 4, [['0.817', true], ['0.816', true], ['0.8165', true], ['.817', true], ['1.224', 'inverted'], ['1.225', 'inverted'], ['1.2247', 'inverted'], ['0.667', 'squared'], ['0.668', 'squared'], ['2/3', 'squared'], ['1', 'same'], ['1.000', 'same'],
    ['0.82', null], ['0.815', null], ['0.818', null], ['81.7%', true]]],
  [ES, 'p-ping-latency', 1, [['310', true], ['310 microseconds', true], ['387.5', 'by-four'], ['388', 'by-four'], ['26', 'range'], ['310.0', true]]],
  [ES, 'p-ping-latency', 4, [['28', true], ['28 pings', true], ['n=28', true], ['28.0', true], ['27.5', null], ['27', 'round-down'], ['22', 'carried'], ['55', 'no-square'], ['5.24', 'unsquared'], ['5.2', 'unsquared'], ['5', 'unsquared'], ['6', 'unsquared'], ['110', null], ['29', null]]],
  [ES, 'p-reference-mass', 1, [['2', true], ['2 mg', true], ['2mg', true], ['2.5', 'by-four'], ['3', 'by-four'], ['8.4', 'sizes'], ['8', 'sizes'], ['-2', null], ['52', null]]],
  [ES, 'p-reference-mass', 5, [['0.51', true], ['0.513', true], ['.51', true], ['0.5130', true], ['0.47', 'carried-90'], ['0.471', 'carried-90'], ['0.53', 'carried-72'], ['0.527', 'carried-72'], ['0.13', 'no-root'], ['0.23', 'sd-not-se'], ['1.95', 'inverted'], ['1.949', 'inverted'],
    ['0.5', null], ['0.52', null], ['3.90', null], ['19', null]]],
  [ES, 'p-tank-sensor', 1, [['51', true], ['51 cm', true], ['51cm', true], ['68', 'by-three'], ['52.5', 'last-two'], ['53', 'last-two'], ['52', null]]],
  [ES, 'p-ticket-bot', 4, [['0.53', true], ['0.5255', true], ['0.526', true], ['27.6', 'no-root'], ['27.62', 'no-root'], ['27.619', 'no-root'], ['1.90', 'inverted'], ['0.019', 'se'], ['0.5', null]]],
  [ES, 'p-routing-test', 3, [['-0.10', true], ['-0.1', true], ['-0.1035', true], ['−0.10', true], ['-0.10 bp', true], ['-0.10bp', true], ['0.10', 'no-sign'], ['0.1', 'no-sign'], ['0.1035', 'no-sign'], ['1.70', 'upper'], ['0.04', 'ninety'], ['-0.47', 'added-se']]],
  // ---------------- regression
  [RG, 'p-stopping-distances', 1, [['1.52', true], ['1.520', true], ['1.52 m per mph', true, UNIT], ['b=1.52', true], ['0.66', 'reverse'], ['0.658', 'reverse'], ['0.6579', 'reverse'], ['0.65', 'other-way'], ['0.648', 'other-way'], ['0.6481', 'other-way'], ['1.9', 'mixed'], ['1.04', 'through-origin'], ['1.5', null]]],
  [RG, 'p-stopping-distances', 2, [['-21.4', true], ['−21.4', true], ['-21.4 m', true], ['-21.40', true], ['a=-21.4', true], ['21.4', 'no-sign'], ['21.4 m', 'no-sign'], ['100.2', 'sign'], ['39.4', 'mean'], ['-2.4', 'carried'], ['-21', null]]],
  [RG, 'p-car-prices', 4, [['7850', true], ['7,850', true], ['£7850', true], ['£7,850', true], ['7850.00', true], ['6600', 'old-slope'], ['£6,600', 'old-slope'], ['2930', 'raw-x'], ['5350', 'wrong-way'], ['7517', 'old-mean'], ['7516.67', 'old-mean'], ['7516', 'old-mean'],
    ['6267', 'both-old', 'the old slope with the old mean, 13,667 - 1,480 x 5: the uncorrected line\'s own price at 9 years, which a learner who misses the word "corrected" gives; no line'], ['-7850', null], ['8200', null]]],
  [RG, 'p-power-price', 4, [['0.04', true], ['0.040', true], ['.04', true], ['1/25', true], ['0.0400', true], ['0.032', 'by-vif'], ['0.0625', 'times'], ['0.063', 'times'], ['0.062', 'times'], ['0.078', 'times-vif'], ['0.0781', 'times-vif'], ['0.044', 'carried'], ['0.0439', 'carried'],
    ['0.05', null], ['0.041', null], ['0.039', null]]],
  [RG, 'p-freight-summary', 1, [['10', true], ['10.00', true], ['F=10', true], ['10.0', true], ['0.25', 'no-df'], ['10.5', 'by-n'], ['10.25', 'n-1'], ['40', null]]],
  [RG, 'p-solar-output', 2, [['-0.5', true], ['-0.50', true], ['-.5', true], ['-1/2', true], ['−0.50', true], ['0.5', 'no-sign'], ['0.50', 'no-sign'], ['1.5', 'simple'], ['3.5', 'sign']]],
  [RG, 'p-raw-intercept', 4, [['205', true], ['205 months', true], ['204', 'round-down'], ['105', 'extra'], ['105 months', 'extra'], ['124', 'raw'], ['143', 'linear'], ['278', 'beta'], ['204.08', null], ['104', null]]],
  [RG, 'p-bond-fund-weeks', 1, [['-0.60', true], ['-0.6', true], ['-0.60%', true], ['−0.60', true], ['-.6', true], ['0.60', 'no-sign'], ['0.6', 'no-sign'], ['0.6%', 'no-sign'], ['-0.65', 'no-intercept'], ['-0.9', 'spread-sign'], ['0.7', 'all-signs'], ['-0.006', null]]],
  [RG, 'p-overlap-signal', 4, [['1.90', true], ['1.9', true], ['1.898', true], ['1.8981', true], ['1.89', true], ['1.57', 'root-h'], ['1.565', 'root-h'], ['1.03', 'no-root'], ['2.36', 'no-two'], ['6.45', 'times'], ['0.63', 'carried'], ['1.84', null], ['3.5', null]]],
  // ---------------- testing
  [TS, 'p-pizza-delivery', 2, [['0.0401', true], ['.0401', true], ['p=0.0401', true], ['0.0801', 'two-sided'], ['0.0802', 'two-sided'], ['0.0803', 'two-sided'], ['0.9599', 'lower-tail'], ['0.08', null], ['0.04', null], ['0.0400', null], ['0.0402', null]]],
  [TS, 'p-blood-screen', 1, [['0.0359', true], ['0.0718', 'two-tail'], ['0.0719', 'two-tail'], ['0.0717', 'two-tail'], ['0.9641', 'lower'], ['0.6554', 'disease-curve'], ['0.036', null]]],
  [TS, 'p-fund-managers', 2, [['0.0035', true], ['0.0069', 'two-sided'], ['0.007', 'two-sided'], ['0.0070', 'two-sided'], ['0.0071', 'two-sided'], ['0.9965', 'lower'], ['0.0036', null], ['0.0034', null], ['0.0068', null]]],
  [TS, 'p-running-shoes', 2, [['3', true], ['3 s', true], ['3s', true], ['3 seconds', true], ['3.0', true], ['2.83', 'divide-by-n'], ['2.828', 'divide-by-n'], ['2.8', null], ['3.05', 'carried'], ['3.046', 'carried'], ['9', 'variance']]],
  [TS, 'p-running-shoes', 3, [['-4', true], ['-4.0', true], ['-4.00', true], ['−4', true], ['t=-4', true], ['-1.33', 'over-sd'], ['-1.333', 'over-sd'], ['-3.77', 'root-eight'], ['-4.24', 'carried'], ['-4.243', 'carried'], ['4', 'sign'], ['-4.01', null], ['-3.99', null]]],
  [TS, 'p-fertiliser-trials', 2, [['0.7274', true], ['0.9878', 'centre-only'], ['0.2726', 'beta'], ['0.05', 'alpha'], ['0.727', null]]],
  [TS, 'p-fertiliser-trials', 4, [['0.9379', true], ['0.9993', 'centre-only'], ['0.7274', 'unchanged'], ['0.0621', 'beta'], ['0.938', null]]],
  [TS, 'p-phone-battery', 1, [['18', true], ['18 h', true], ['18h', true], ['18 hours', true], ['18 hrs', true], ['18 hr', true], ['18.0', true], ['20.57', 'n-minus-one']]],
  [TS, 'p-phone-battery', 2, [['2', true], ['2 h', true], ['2h', true], ['2 hours', true], ['s=2', true], ['1.87', 'divide-by-n'], ['4', 'variance'], ['3.4', 'carried']]],
  [TS, 'p-phone-battery', 5, [['19.34', true], ['19.34 h', true], ['19.34h', true], ['19.34 hours', true], ['19.16', 'normal'], ['19.67', 'two-sided'], ['16.66', 'wrong-side'], ['21.79', 'sd-not-se'], ['19.3', null], ['19.5', null]]],
  [TS, 'p-wine-taster', 2, [['0.0193', true], ['79/4096', true], ['0.01929', true], ['0.019', 'carried'], ['0.0190', 'carried'], ['78/4096', 'carried'], ['0.0161', 'exactly-ten'], ['0.02', null]]],
  [TS, 'p-wine-taster', 4, [['10', true], ['9', 'nine'], ['11', 'eleven'], ['10 right', true]]],
  [TS, 'p-fund-managers', 3, [['5', true], ['3', 'first-fail'], ['2', 'bonferroni'], ['6', 'unadjusted'], ['4', null]]],
  [TS, 'p-gene-screen', 1, [['0.001667', true], ['1/600', true], ['0.0016667', true], ['.001667', true], ['0.1/60', true], ['0.001666', null], ['0.00167', null], ['0.0017', null], ['0.1', 'unadjusted'], ['0.10', 'unadjusted'], ['6', 'times-m'], ['0.000833', 'five-percent']]],
  [TS, 'p-gene-screen', 2, [['1', true], ['1 gene', true], ['8', 'unadjusted'], ['6', 'bh'], ['0', null], ['3', null]]],
  [TS, 'p-gene-screen', 3, [['6', true], ['6 genes', true], ['2', 'first-fail'], ['1', 'bonferroni'], ['8', 'unadjusted'], ['4', 'count-passes'], ['5', null], ['3', null], ['7', null]]],
  [TS, 'p-gene-screen', 4, [['0.096', true], ['.096', true], ['q=0.096', true], ['0.0960', true], ['0.095', null], ['0.0948', null], ['0.576', 'no-divide'], ['0.108', 'rank-five'], ['0.01', 'bar'], ['0.0100', 'bar'], ['0.10', null], ['0.0962', null]]],
  [TS, 'p-checkout-designs', 1, [['0.9', true], ['.9', true], ['0.90', true], ['9/10', true], ['0.9 launches', true], ['0.45', 'one-sided'], ['0.5', 'one-sided'], ['18', 'all-pages'], ['17.1', 'complement'], ['1', null], ['0.6', null]]],
  [TS, 'p-checkout-designs', 2, [['3600', true], ['£3600', true], ['£3,600', true], ['3,600', true], ['3600.00', true], ['£3600.00', true], ['72000', 'all-pages'], ['£72,000', 'all-pages'], ['4000', 'one-launch'], ['3.6', 'thousands'], ['200', null]]],
  [TS, 'p-checkout-designs', 3, [['0.002778', true], ['1/360', true], ['0.0027778', true], ['0.05/18', true], ['0.002777', null], ['0.00278', null], ['0.0028', null], ['0.05', 'unadjusted'], ['0.9', 'times-n'], ['0.002846', 'sidak']]],
  [TS, 'p-checkout-designs', 4, [['0.0488', true], ['0.04884', true], ['.0488', true], ['0.05', 'bound'], ['0.0500', 'bound'], ['0.9512', 'no-complement'], ['0.6028', 'carried'], ['0.049', null], ['0.0489', null]]],
  [TS, 'p-biomarker-field', 1, [['0.002632', true], ['1/380', true], ['0.0026316', true], ['0.002631', null], ['0.0025', 'over-400'], ['0.002500', 'over-400'], ['380', 'times'], ['0.000132', 'five-percent'], ['0.0026', null], ['0.00263', null]]],
  [TS, 'p-biomarker-field', 3, [['15', true], ['15 biomarkers', true], ['18', 'old-bar'], ['20', 'all-real'], ['12', 'next-bar'], ['12.2', 'next-bar'],
    ['17', 'lower-bar'], ['16.8', 'lower-bar']]],
  [TS, 'p-biomarker-field', 4, [['0.0459', true], ['0.04592', true], ['.0459', true], ['0.9541', 'true-share'], ['0.0018', 'over-400'], ['0.0348', 'no-power'], ['0.046', null], ['0.0460', null], ['0.0481', null]]],
  // ---------------- vectors
  [VC, 'p-charging-robot', 1, [['(2,3)', true], ['(2, 3)', true], ['[2,3]', true], ['\\left(2,3\\right)', true], ['(2.0, 3.0)', true], ['(3,2)', 'swapped'], ['(3, 2)', 'swapped'], ['(2,2)', null], ['(11,11)', null]]],
  [VC, 'p-charging-robot', 2, [['42', true], ['42.0', true], ['7', 'unweighted'], ['14', 'only-u'], ['21', 'only-v'], ['36', null]]],
  [VC, 'p-charging-robot', 3, [['58', true], ['58°', true], ['58 degrees', true], ['57.5', true], ['57.53', true], ['58.0', true], ['57', null], ['59', null], ['1.004', 'radians'], ['1.0', 'radians'], ['90', 'no-root'], ['89.6', 'no-root'], ['45', null]]],
  [VC, 'p-charging-robot', 4, [['2.18', true], ['2.17', true], ['2.177', true], ['2.18 m', true], ['2.18m', true], ['2.18 metres', true], ['2.19', true], ['2.2', null], ['2.16', null], ['2.20', null], ['15.56', 'straight'], ['15.55', 'straight'], ['17.73', 'path'], ['17.74', 'path'], ['5.16', 'no-cross'], ['5.17', 'no-cross']]],
  [VC, 'p-active-bets', 2, [['-0.55', true], ['-0.55%', true], ['−0.55', true], ['-0.55 %', true], ['-.55', true], ['-0.0055', 'decimal'], ['−0.0055', 'decimal'], ['0.55', 'flipped'], ['0.55%', 'flipped'], ['0.95', 'fund'], ['1.5', 'benchmark'], ['-0.6', null], ['0.0055', null], ['-0.0095', null, SHARED], ['-0.01', null, SHARED], ['-0.0145', null, SHARED]]],
  [VC, 'p-stress-hedge', 1, [['-2.2', true], ['-2.20', true], ['-2.2%', true], ['-2.20%', true], ['−2.20', true], ['-0.022', 'decimal'], ['-0.02', 'decimal'], ['-3', 'unweighted'], ['-3.00', 'unweighted'], ['-1', 'equal'], ['2.2', null], ['-2', null], ['-0.03', null], ['-0.016', null, SHARED]]],
  [VC, 'p-stress-hedge', 3, [['-1.46', true], ['-1.46%', true], ['−1.46', true], ['-0.0146', 'decimal'], ['-0.8', 'old'], ['-0.80', 'old'], ['-0.14', 'shift-added'], ['-1.5', null], ['1.46', null], ['-0.008', null, SHARED], ['-0.0066', null, SHARED]]],
  [VC, 'p-stress-hedge', 4, [['-0.73', true], ['-0.73%', true], ['−0.73', true], ['-0.0073', 'decimal'], ['-1.5', 'unhedged'], ['-1.50', 'unhedged'], ['-1.46', 'no-half'], ['-0.7', null], ['0.73', null], ['-0.0146', null, SHARED], ['-0.008', null, SHARED]]],
  [VC, 'p-drone-crosswind', 1, [['(0.6,0.8)', true], ['(3/5,4/5)', true], ['\\frac15(3,4)', true], ['\\frac{1}{5}\\left(3,4\\right)', true], ['0.05(12,16)', true], ['0.2(3,4)', true], ['(12/20,16/20)', true], ['(0.60, 0.80)', true],
    ['\\frac{1}{4}(3,4)', null, LEN], ['5(3,4)', null, LEN], ['(3,4)', 'not-unit'], ['(0.8,0.6)', 'swapped'], ['(12,16)', 'whole'], ['(0.6,-0.8)', null]]],
  [VC, 'p-goat-feed', 3, [['[[3,-1],[-2,4]]', true], ['[[3, -1], [-2, 4]]', true], ['10[[0.3,-0.1],[-0.2,0.4]]', true], ['\\frac{1}{0.1}[[0.3,-0.1],[-0.2,0.4]]', true], ['[[3.0,-1.0],[-2.0,4.0]]', true], ['10\\cdot[[0.3,-0.1],[-0.2,0.4]]', true, LIT], ['10\\times[[0.3,-0.1],[-0.2,0.4]]', true, LIT], ['5[[0.3,-0.1],[-0.2,0.4]]', null], ['0.1[[0.3,-0.1],[-0.2,0.4]]', null]]],
  [VC, 'p-engraver-dial', 1, [['[[6+2k,2+k],[5,2]]', true], ['[[2k+6,k+2],[5,2]]', true], ['[[2(k+3),2+k],[5,2]]', true], ['[[2(3+k),2+k],[5,2]]', true],
    ['[[2(k+3),k+2],[5,2]]', true, 'the first entry factorised with the second entry written k + 2: each accept form is matched whole, so this mix of two accepted spellings is refused'],
    ['[[2\\left(k+3\\right),2+k],[5,2]]', true, 'the factorised entry as the maths keyboard types it, with \\left( and \\right)'],
    ['[[2k+6,2+k],[5,2]]', true, 'the first entry as 2k + 6 with the second as 2 + k'], ['[[6+2k,k+2],[5,2]]', true, 'the first entry as 6 + 2k with the second as k + 2']]],
  [VC, 'p-engraver-dial', 3, [['2', true], ['k=2', true], ['-2', 'added'], ['-2.44', 'added'], ['-2.444', 'added'], ['0', null]]],
  [VC, 'p-site-plan', 4, [['126.9', true], ['126.87', true], ['126.9°', true], ['126.9 degrees', true], ['53.1', 'clockwise'], ['53.13', 'clockwise'], ['36.9', 'theta'], ['90', 'plan-angle'], ['127', null], ['-126.9', null]]],
  [VC, 'p-factor-risk', 1, [['(1.105,0.2)', true], ['(1.105, 0.20)', true], ['[1.105,0.2]', true], ['(221/200,1/5)', true], ['\\left(1.105,0.2\\right)', true], ['(1.105, .2)', true], ['(1.1,0.2)', null], ['(1.11,0.2)', null], ['(3.4,0.7)', 'unweighted'], ['(0.2,1.105)', null]]],
  [VC, 'p-factor-risk', 2, [['0.605', true], ['.605', true], ['x=0.605', true], ['121/200', true], ['0.6050', true], ['1.105', 'to-zero'], ['1.605', 'added'], ['-0.3', 'size'], ['0.61', null], ['0.6', null], ['-0.605', null]]],
  [VC, 'p-factor-risk', 3, [['(0.5,0.04875)', true], ['(1/2,39/800)', true], ['(0.50, 0.04875)', true], ['[0.5,0.04875]', true], ['(.5,.04875)', true], ['(0.5,0.049)', null], ['(0.5,0.0488)', null], ['(0.5,0.2)', 'market-only'], ['(0.5,-0.405)', 'size-whole'], ['(1.71,0.35125)', 'added']]],
  [VC, 'p-factor-risk', 4, [['0.00376', true], ['0.003758', true], ['0.0037579', true], ['.00376', true], ['0.0038', null], ['0.004', null], ['0.00361', 'diagonal'], ['0.25238', 'no-f'], ['0.0191', 'unhedged'], ['0.01910', 'unhedged'], ['0.019105', 'unhedged'],
    ['0.376', null], ['0.376%', true, 'the variance typed as a percentage with its sign, 0.376% = 0.00376']]],
  [VC, 'p-factor-risk', 5, [['80.3', true], ['80.3%', true], ['80.3 %', true], ['80.31', true], ['80.33', true], ['80.30', true], ['80', null], ['80.4', null], ['80.2', null], ['0.803', 'decimal'], ['0.8031', 'decimal'], ['0.80', 'decimal'], ['0.8', 'decimal'], ['0.76', null, SHARED], ['0.85', null, SHARED],
    ['19.7', 'ratio'], ['19.69', 'ratio'], ['1.5', 'difference'], ['1.53', 'difference'], ['55.6', 'volatility'], ['55.63', 'volatility']]],
  [VC, 'p-colour-sensor', 1, [['[[1.4,0.4],[0.1,0.6]]', true], ['[[7/5,2/5],[1/10,3/5]]', true], ['[[1.40,0.40],[0.10,0.60]]', true], ['[[1.4, 0.4], [0.1, 0.6]]', true], ['[[14/10,4/10],[1/10,6/10]]', true], ['[[1.4,.4],[.1,.6]]', true]]],
  [VC, 'p-colour-sensor', 2, [['0.8', true], ['.8', true], ['4/5', true], ['0.80', true], ['0.88', 'added'], ['0.84', 'diagonal'], ['0.4', 'leak-only'], ['-0.8', null], ['1.25', null], ['2', null]]],
  [VC, 'p-colour-sensor', 3, [['[[0.75,-0.5],[-0.125,1.75]]', true], ['[[3/4,-1/2],[-1/8,7/4]]', true], ['1.25[[0.6,-0.4],[-0.1,1.4]]', true], ['\\frac{1}{0.8}[[0.6,-0.4],[-0.1,1.4]]', true], ['\\frac{5}{4}[[0.6,-0.4],[-0.1,1.4]]', true, LIT], ['\\frac54[[0.6,-0.4],[-0.1,1.4]]', true, LIT], ['1.25\\cdot[[0.6,-0.4],[-0.1,1.4]]', true, LIT], ['1.25\\times[[0.6,-0.4],[-0.1,1.4]]', true, LIT], ['1.25[[0.60,-0.40],[-0.10,1.40]]', true, LIT],
    ['[[.75,-.5],[-.125,1.75]]', true], ['[[0.75,-0.50],[-0.125,1.75]]', true], ['0.8[[0.6,-0.4],[-0.1,1.4]]', null], ['[[0.75,-0.5],[-0.13,1.75]]', 'length']]],
  [VC, 'p-colour-sensor', 4, [['(120,80)', true], ['(120, 80)', true], ['[120,80]', true], ['\\left(120,80\\right)', true], ['(120.0, 80.0)', true], ['(304,56)', 'forward'], ['(270,55)', 'leak-only'], ['(96,64)', 'no-divide'], ['(80,120)', 'swapped'], ['(100,60)', null], ['(200,60)', null]]],
];

let checks = 0, fails = 0, findings = 0, known = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (SHOW) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
const docs = {};
const find = (course, id) => {
  for (const f of fs.readdirSync('app/content/courses/' + course).filter(x => /^problems-\d+\.json$/.test(x))) {
    const d = docs[course + f] || (docs[course + f] = JSON.parse(fs.readFileSync(`app/content/courses/${course}/${f}`, 'utf8')));
    const it = d.items.find(i => i.id === id);
    if (it) return it;
  }
  throw new Error('no item ' + id);
};
for (const [course, id, part, rows] of TYPED) {
  const p = find(course, id).parts[part - 1], w = p.widget;
  const isExpr = w.kind === 'expression';
  const grade = isExpr ? expr : num;
  const by = (p.feedback && p.feedback.byKey) || {};
  const where = `${course} ${id} ${part}`;
  if (isExpr) {
    for (const a of [w.answer, ...(w.accept || [])]) say(grade(w, a) === true, null, `${where}: answer or accept "${a}" grades correct (got ${grade(w, a)})`);
    for (const x of w.wrong || []) {
      if (/pmatrix/.test(x.tex)) { known++; say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`); continue; }
      say(grade(w, x.tex) === x.id, null, `${where}: wrong ${x.id} "${x.tex}" lands on its id (got ${grade(w, x.tex)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
    }
  } else {
    const shown = w.unit === '%' ? String(+(w.answer * 100).toFixed(6)) : String(w.answer);
    say(grade(w, shown) === true, null, `${where}: answer ${shown} grades correct (got ${grade(w, shown)})`);
    if (w.unit === '%') say(grade(w, shown + '%') === true, null, `${where}: answer ${shown}% grades correct (got ${grade(w, shown + '%')})`);
    for (const x of w.wrong || []) {
      const t = w.unit === '%' ? String(+(x.value * 100).toFixed(6)) : String(x.value);
      say(grade(w, t) === x.id, null, `${where}: wrong ${x.id} ${t} lands on its id (got ${grade(w, t)})`); say(!!by[x.id], null, `${where}: wrong ${x.id} has a byKey line`);
      if (w.unit === '%') say(grade(w, t + '%') === x.id, null, `${where}: wrong ${x.id} ${t}% lands on its id (got ${grade(w, t + '%')})`);
    }
  }
  for (const [typed, want, note] of rows) {
    const got = grade(w, typed);
    const okRow = got === want || (note && typeof want === 'string' && false);
    say(okRow, note, `${where}: typed "${typed}" -> ${got === true ? 'accepted' : got === null ? 'refused, generic line' : got === 'NOPARSE' ? 'not read (field will not submit)' : 'refused, line "' + got + '"'}; expected ${want === true ? 'accepted' : want === null ? 'generic refusal' : want}`);
  }
}
console.log(`grade: ${checks} checks, ${fails} failures, ${findings} FINDING rows (recorded in the review); ${known} wrong matrices not typed (known engine fault)`);
process.exit(fails ? 1 : 0);
