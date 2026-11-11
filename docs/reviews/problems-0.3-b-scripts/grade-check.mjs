#!/usr/bin/env node
/* Second read, problems 0.3 (b): what the engine's own graders do with each part of exp-log problem sets 1 to 3.
   Harness as problems-0.2-b-scripts/grade-check.mjs (app/js/engine/grade.js and the local Compute Engine). The numeric
   model is the widget's own grade() (app/js/engine/widgets/numeric.js): parseNum, a bare number in a "%" box divided by
   100, within, then matchWrong. The expression model is the widget's equal(): exprEqual or the normExpr text match
   against answer and accept[], then wrong[].tex (no part of these sets sets a form).
   Every answer and accept[] form must grade correct, every wrong[] must grade wrong and land on its own key, and every
   TYPED row must grade as expected. A row with a 6th field is one the reader holds to be a fault: it prints as FINDING.
   --show prints what every typed row did.

   node docs/reviews/problems-0.3-b-scripts/grade-check.mjs --local-cdn <pkgs>      (from the repo root) */
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
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

const Y = 'p-yeast-culture', LP = 'p-laptop-value', RC = 'p-rare-coin', CP = 'p-curve-point';
const FS = 'p-fault-search', FD = 'p-forty-doublings', DR = 'p-drawdown-recovery', AU = 'p-app-users';
const SD = 'p-savings-doubling', WT = 'p-weekly-target', LC = 'p-log-chart-line', MD = 'p-monthly-deposit';
/* [set, item, part, typed, expected ok, (finding note)]; expected "key:<id>" means wrong and landing on that key;
   expected "noparse" means the field does not take the text at all (Check stays disabled) */
const T = [
  // ---- expressions: equal forms a learner would type
  [1, Y, 1, '3000\\cdot2^n', true], [1, Y, 1, '2^n\\cdot3000', true], [1, Y, 1, '3000\\times2^{n}', true], [1, Y, 1, '3000\\left(2\\right)^{n}', true],
  [1, Y, 1, '3000(2^n)', true], [1, Y, 1, '1500\\cdot2^{n+1}', true], [1, Y, 1, '6000\\cdot2^{n-1}', true], [1, Y, 1, '3000\\cdot4^{\\frac{n}{2}}', true],
  [1, Y, 1, '\\frac{3000}{2^{-n}}', true], [1, Y, 1, '3\\cdot10^3\\cdot2^n', true], [1, Y, 1, '2^n3000', true],
  [1, Y, 1, 'N=3000\\cdot2^n', true, 'the feedback and part 2 write N = 3000 x 2^n'],
  [1, Y, 1, '3000\\cdot2n', false], [1, Y, 1, '3000n^2', false], [1, Y, 1, '3000^n', false], [1, Y, 1, '2^n', false], [1, Y, 1, '3000\\cdot2^{-n}', false],
  [1, Y, 1, '3000\\cdot2^{n+1}', false], [1, Y, 1, '3000', false], [1, Y, 1, '3000\\cdot2', false], [1, Y, 1, '3000+2^n', 'key:added'], [1, Y, 1, '6000^n', 'key:base-times'],
  [1, Y, 1, '(3000\\cdot2)^n', 'key:base-times'], [1, Y, 1, '6000n', 'key:steady'], [1, Y, 1, '3000\\cdot2\\cdot n', 'key:steady'], [1, Y, 1, '3000+3000n', false],
  [2, AU, 1, '2000\\cdot1.3^n', true], [2, AU, 1, '2000(1+0.3)^n', true], [2, AU, 1, '2000\\cdot\\left(\\frac{13}{10}\\right)^n', true], [2, AU, 1, '1.3^n\\cdot2000', true],
  [2, AU, 1, '2000\\times1.30^{n}', true], [2, AU, 1, '2600\\cdot1.3^{n-1}', true], [2, AU, 1, '2000\\left(1.3\\right)^n', true], [2, AU, 1, '2000\\cdot(1+\\frac{30}{100})^n', true],
  [2, AU, 1, 'U=2000\\cdot1.3^n', true, 'the feedback and part 2 write U = 2000 x 1.3^n'],
  [2, AU, 1, '2000\\cdot1.3n', false], [2, AU, 1, '2000\\cdot30^n', false], [2, AU, 1, '2000\\cdot1.03^n', false], [2, AU, 1, '2000\\cdot0.3^n', 'key:rate-only'],
  [2, AU, 1, '2600^n', 'key:joined'], [2, AU, 1, '(2000\\cdot1.3)^n', 'key:joined'], [2, AU, 1, '2000+600n', 'key:steady'], [2, AU, 1, '2000(1+0.3n)', 'key:steady'],
  [2, AU, 1, '2000e^{0.3n}', false], [2, AU, 1, '1.3^n', false], [2, AU, 1, '2000\\cdot1.3', false],
  [3, SD, 1, '2400e^{0.055t}', true], [3, SD, 1, '2400\\cdot e^{0.055\\cdot t}', true], [3, SD, 1, '2400\\exp(0.055t)', true], [3, SD, 1, '2400e^{\\frac{5.5}{100}t}', true],
  [3, SD, 1, '2400e^{\\frac{11t}{200}}', true], [3, SD, 1, '2400\\left(e^{0.055}\\right)^t', true], [3, SD, 1, '2400e^{t\\cdot0.055}', true], [3, SD, 1, '2400e^{.055t}', true],
  [3, SD, 1, '\\frac{2400}{e^{-0.055t}}', true], [3, SD, 1, 'e^{0.055t}\\cdot2400', true], [3, SD, 1, '2400\\mathrm{e}^{0.055t}', true], [3, SD, 1, '2400\\exponentialE^{0.055t}', true],
  [3, SD, 1, 'A=2400e^{0.055t}', true, 'the feedback and part 2 write A = 2400e^{0.055t}'],
  [3, SD, 1, '2400e^{0.55t}', false], [3, SD, 1, '2400e^{0.055}', false], [3, SD, 1, '2400e^{0.055}t', false], [3, SD, 1, '2400\\cdot1.0565^t', false],
  [3, SD, 1, '2400e^{5.5t}', 'key:percent'], [3, SD, 1, '2400\\cdot1.055^t', 'key:yearly'], [3, SD, 1, '2400(1+0.055)^t', 'key:yearly'], [3, SD, 1, '2400e^{1.055t}', 'key:factor'],
  [3, SD, 1, '2400\\cdot2^{\\frac{t}{12.6}}', false], [3, SD, 1, '2400(1+0.055t)', false], [3, SD, 1, 'e^{0.055t}', false],
  // ---- numbers: the forms the prose and accept lines suggest
  [1, Y, 2, '750', true], [1, Y, 2, '750.0', true], [1, Y, 2, '3000/4', true], [1, Y, 2, 'N=750', 'noparse'], [1, Y, 2, '750 cells', 'noparse'], [1, Y, 2, '-12000', 'key:negative'], [1, Y, 2, '−12,000', 'key:negative'],
  [1, Y, 3, '4243', true], [1, Y, 3, '4,243', true], [1, Y, 3, '4242', true], [1, Y, 3, '4242.64', true], [1, Y, 3, '4242.6', true], [1, Y, 3, '4244', false], [1, Y, 3, '4241', false], [1, Y, 3, '4230', false],
  [1, Y, 3, '4500', 'key:halfway'], [1, Y, 3, '3000', 'key:times-half'], [1, Y, 3, '1500', 'key:halved'], [1, Y, 3, '77', 'key:base-times'],
  [1, Y, 4, '2.5', true], [1, Y, 4, '5/2', true], [1, Y, 4, '2 1/2', true], [1, Y, 4, '2.50', true], [1, Y, 4, 'k=2.5', 'noparse'], [1, Y, 4, '-1.5', 'key:added-powers'], [1, Y, 4, '5.66', 'key:ratio'], [1, Y, 4, '5.7', false],
  [1, LP, 1, '0.75', true], [1, LP, 1, '.75', true], [1, LP, 1, '3/4', true], [1, LP, 1, '75%', true], [1, LP, 1, '75', false], [1, LP, 1, '0.25', 'key:loss'], [1, LP, 1, '25%', 'key:loss'], [1, LP, 1, '-0.25', false],
  [1, LP, 2, '675', true], [1, LP, 2, '£675', true], [1, LP, 2, '675.00', true], [1, LP, 2, '£675.00', true], [1, LP, 2, '600', 'key:steady'], [1, LP, 2, '£900', 'key:one-year'],
  [1, LP, 3, '379.69', true], [1, LP, 3, '£379.69', true], [1, LP, 3, '379.6875', true], [1, LP, 3, '379.68', false], [1, LP, 3, '379.7', false], [1, LP, 3, '380', false], [1, LP, 3, '506.25', 'key:one-year'],
  [1, LP, 4, '68.36', true], [1, LP, 4, '68.36%', true], [1, LP, 4, '68.359', true], [1, LP, 4, '68.4', false], [1, LP, 4, '68', false], [1, LP, 4, '0.6836', 'key:decimal'], [1, LP, 4, '0.68', 'key:decimal'],
  [1, LP, 4, '31.64', 'key:kept'], [1, LP, 4, '100', 'key:added'], [1, LP, 4, '57.81', 'key:one-short'], [1, LP, 4, '820.31', false],
  [1, RC, 1, '1.5625', true], [1, RC, 1, '25/16', true], [1, RC, 1, '1000/640', true], [1, RC, 1, '1.56', false], [1, RC, 1, '1.563', false], [1, RC, 1, '0.64', 'key:inverted'], [1, RC, 1, '156.25%', true],
  [1, RC, 2, '1.25', true], [1, RC, 2, '5/4', true], [1, RC, 2, '1 1/4', true], [1, RC, 2, 'g=1.25', 'noparse'], [1, RC, 2, '1.28', false], [1, RC, 2, '1.281', 'key:halved-rise'], [1, RC, 2, '0.78', false],
  [1, RC, 3, '25', true], [1, RC, 3, '25%', true], [1, RC, 3, '25.0', true], [1, RC, 3, '0.25', 'key:decimal'], [1, RC, 3, '125', 'key:factor'], [1, RC, 3, '28.125', 'key:halved-rise'], [1, RC, 3, '28.13', 'key:halved-rise'], [1, RC, 3, '28', false],
  [1, RC, 4, '1398', true], [1, RC, 4, '£1,398', true], [1, RC, 4, '1,398', true], [1, RC, 4, '1397.54', true], [1, RC, 4, '1397', true], [1, RC, 4, '1397.5', true],
  [1, RC, 4, '1399', false, 'the band 1397.54 ± 1.5 takes £1,399, which no rounding of the answer gives'], [1, RC, 4, '1396', false], [1, RC, 4, '1400', false],
  [1, RC, 4, '1406.25', 'key:halfway'], [1, RC, 4, '1406', 'key:halfway'], [1, RC, 4, '1375', 'key:simple'], [1, RC, 4, '1450', 'key:carried'],
  [1, CP, 1, '4', true], [1, CP, 1, 'a=4', 'noparse'], [1, CP, 1, '8', 'key:square-root'], [1, CP, 1, '21.33', 'key:divided'], [1, CP, 1, '21', 'key:divided'], [1, CP, 1, '-4', false],
  [1, CP, 2, '0.5', true], [1, CP, 2, '1/2', true], [1, CP, 2, '.5', true], [1, CP, 2, '2', 'key:factor'], [1, CP, 2, '1', 'key:one'],
  [1, CP, 3, '5.5', true], [1, CP, 3, '11/2', true], [1, CP, 3, '5 1/2', true], [1, CP, 3, 'x=5.5', 'noparse'], [1, CP, 3, '2.5', 'key:distance-only'], [1, CP, 3, '8', 'key:step-one'],
  [1, CP, 4, '-5.5', true], [1, CP, 4, '−5.5', true], [1, CP, 4, '-11/2', true], [1, CP, 4, '-5 1/2', true], [1, CP, 4, '5.5', 'key:no-flip'], [1, CP, 4, '0.18', 'key:reciprocal'], [1, CP, 4, '0.1818', 'key:reciprocal'],
  [2, FS, 1, '11', true], [2, FS, 1, '11.0', true], [2, FS, 1, '10', 'key:off-by-one'], [2, FS, 1, '1024', 'key:halved'], [2, FS, 1, '1,024', 'key:halved'], [2, FS, 1, '12', false],
  [2, FS, 2, '16', true], [2, FS, 2, '55', 'key:multiplied-logs'], [2, FS, 2, '352', 'key:times-batches'], [2, FS, 2, '43', 'key:added-count'], [2, FS, 2, '15', 'key:carried'], [2, FS, 2, '65536', false], [2, FS, 2, '65,536', false],
  [2, FS, 3, '19', true], [2, FS, 3, '18', 'key:rounded-down'], [2, FS, 3, '18.32', false], [2, FS, 3, '21', 'key:added-five'], [2, FS, 3, '80', 'key:times-five'], [2, FS, 3, '20', false],
  [2, FD, 1, '12.0412', true], [2, FD, 1, '12.04120', true], [2, FD, 1, '12.041', false], [2, FD, 1, '12.04', false], [2, FD, 1, '12', false], [2, FD, 1, '3.2041', 'key:swapped'], [2, FD, 1, '40.30103', 'key:added'],
  [2, FD, 2, '12', true], [2, FD, 2, '13', 'key:rounded-up'], [2, FD, 2, '40', 'key:power'], [2, FD, 2, '3', 'key:carried'], [2, FD, 2, '12.0412', false],
  [2, FD, 3, '1.10', true], [2, FD, 3, '1.1', true], [2, FD, 3, '1.0995', true], [2, FD, 3, '1.09', false], [2, FD, 3, '1.11', false], [2, FD, 3, '1.04', 'key:one-plus'], [2, FD, 3, '0.04', 'key:fraction-part'], [2, FD, 3, '1', false],
  [2, FD, 4, '10', true], [2, FD, 4, '9', 'key:rounded-down'], [2, FD, 4, '9.83', false], [2, FD, 4, '3', 'key:tenfold-steps'], [2, FD, 4, '50', 'key:total'],
  [2, DR, 1, '32000', true], [2, DR, 1, '32,000', true], [2, DR, 1, '£32,000', true], [2, DR, 1, '£32,000.00', true], [2, DR, 1, '30000', 'key:added-falls'], [2, DR, 1, '£40,000', 'key:one-fall'],
  [2, DR, 2, '56.25', true], [2, DR, 2, '56.25%', true], [2, DR, 2, '56.3', false], [2, DR, 2, '56', false], [2, DR, 2, '0.5625', 'key:decimal'], [2, DR, 2, '40', 'key:two-twenties'], [2, DR, 2, '36', 'key:the-loss'],
  [2, DR, 2, '156.25', 'key:factor'], [2, DR, 2, '66.67', 'key:carried'], [2, DR, 2, '66.7', false],
  [2, DR, 3, '5.80', true], [2, DR, 3, '5.8', true], [2, DR, 3, '5.7995', true], [2, DR, 3, '5.7989', true], [2, DR, 3, '5.79', false], [2, DR, 3, '5.81', false], [2, DR, 3, '6', false], [2, DR, 3, 'n=5.80', 'noparse'],
  [2, DR, 3, '2.90', 'key:no-power'], [2, DR, 3, '0.17', 'key:inverted'], [2, DR, 3, '7.03', 'key:simple'], [2, DR, 3, '1.45', 'key:divided-numbers'],
  [2, DR, 4, '6', true], [2, DR, 4, '5', 'key:rounded-down'], [2, DR, 4, '8', 'key:with-falls'], [2, DR, 4, '5.8', false], [2, DR, 4, '6 months', 'noparse'],
  [2, AU, 3, '12.27', true], [2, AU, 3, '12.269', true], [2, AU, 3, '12.26', false], [2, AU, 3, '12.3', false], [2, AU, 3, '12.28', false], [2, AU, 3, '1.38', 'key:joined'], [2, AU, 3, '19.23', 'key:divided'], [2, AU, 3, '-2.67', 'key:rate-only'],
  [2, AU, 4, '13', true], [2, AU, 4, '12', 'key:rounded-down'], [2, AU, 4, '2', 'key:joined'], [2, AU, 4, '12.27', false],
  [3, SD, 2, '12.60', true], [3, SD, 2, '12.6', true], [3, SD, 2, '12.603', true], [3, SD, 2, '12.59', false], [3, SD, 2, '12.61', false], [3, SD, 2, '13', false], [3, SD, 2, '13.09', 'key:rule-72'], [3, SD, 2, '12.95', 'key:yearly'],
  [3, SD, 2, '12.73', false], [3, SD, 2, '12.6 years', 'noparse'],
  [3, SD, 3, '37.80', true], [3, SD, 3, '37.8', true], [3, SD, 3, '37.81', true], [3, SD, 3, '37.79', false], [3, SD, 3, '38', false], [3, SD, 3, '100.8', 'key:eight-times'], [3, SD, 3, '100.82', 'key:eight-times'],
  [3, SD, 3, '50.4', 'key:four'], [3, SD, 3, '25.2', 'key:two'], [3, SD, 3, '25.21', 'key:two'],
  [3, SD, 4, '6788', true], [3, SD, 4, '£6,788', true], [3, SD, 4, '6787', true], [3, SD, 4, '6788.23', true], [3, SD, 4, '6786.73', true], [3, SD, 4, '6786', false], [3, SD, 4, '6789', false],
  [3, SD, 4, '10800', 'key:halfway-pounds'], [3, SD, 4, '7200', 'key:midpoint'], [3, SD, 4, '2606', 'key:years'], [3, SD, 4, '2606.40', 'key:years'],
  [3, WT, 1, '0.043', true], [3, WT, 1, '.043', true], [3, WT, 1, '4.3%', true], [3, WT, 1, '0.04', false], [3, WT, 1, '0.107', 'key:signs'], [3, WT, 1, '0.011', 'key:averaged'], [3, WT, 1, '0.01075', 'key:averaged'],
  [3, WT, 2, '41.76', true], [3, WT, 2, '£41.76', true], [3, WT, 2, '41.7575', true], [3, WT, 2, '41.75', false], [3, WT, 2, '41.72', 'key:one-plus'], [3, WT, 2, '40.04', 'key:added'], [3, WT, 2, '44.52', 'key:carried'],
  [3, WT, 3, '0.0748', true], [3, WT, 3, '0.0747', true], [3, WT, 3, '0.07472', true], [3, WT, 3, '0.075', false], [3, WT, 3, '0.0746', false], [3, WT, 3, '0.0776', 'key:simple'], [3, WT, 3, '0.1178', 'key:from-monday'],
  [3, WT, 3, '-0.0748', 'key:inverted'], [3, WT, 3, '-0.0747', 'key:inverted'], [3, WT, 3, '3.24', 'key:difference'], [3, WT, 3, '7.48%', true],
  [3, WT, 4, '0.0249', true], [3, WT, 4, '0.02493', true], [3, WT, 4, '0.0250', true], [3, WT, 4, '0.025', true], [3, WT, 4, '0.0248', false], [3, WT, 4, '0.0251', false],
  [3, WT, 4, '0.4213', 'key:cube-root'], [3, WT, 4, '0.2244', 'key:times-three'], [3, WT, 4, '0.0259', 'key:carried'],
  [3, WT, 5, '2.52', true], [3, WT, 5, '2.52%', true], [3, WT, 5, '2.521', true], [3, WT, 5, '2.51', false], [3, WT, 5, '2.53', false], [3, WT, 5, '2.5', false], [3, WT, 5, '2.49', 'key:log-as-simple'],
  [3, WT, 5, '2.59', 'key:simple-split'], [3, WT, 5, '0.0252', 'key:decimal'], [3, WT, 5, '102.52', 'key:e-power'],
  [3, WT, 5, '0.0249', 'key:log-as-simple', 'the log return retyped (0.0249) lands on "decimal", whose line says the learner typed 0.0252'],
  [3, LC, 1, '27.47', true], [3, LC, 1, '27.47%', true], [3, LC, 1, '27.465', true], [3, LC, 1, '27.5', false], [3, LC, 1, '27', false], [3, LC, 1, '0.2747', 'key:decimal'], [3, LC, 1, '0.27', 'key:decimal'],
  [3, LC, 1, '100', 'key:simple-total'], [3, LC, 1, '112.5', 'key:ratio-over-years'], [3, LC, 1, '31.61', 'key:yearly-factor'], [3, LC, 1, '11.93', 'key:log10'],
  [3, LC, 2, '2.52', true], [3, LC, 2, '2.523', true], [3, LC, 2, '2.53', false], [3, LC, 2, '2.5', false], [3, LC, 2, '2.62', 'key:rule-72'], [3, LC, 2, '3.64', 'key:inverse'], [3, LC, 2, '4', 'key:tripling'], [3, LC, 2, '0.03', 'key:percent'], [3, LC, 2, '0.025', 'key:percent'],
  [3, LC, 3, '45', true], [3, LC, 3, '£45', true], [3, LC, 3, '45.07', true], [3, LC, 3, '45.16', true], [3, LC, 3, '45.47', true], [3, LC, 3, '46', false], [3, LC, 3, '44', false], [3, LC, 3, '75', 'key:pounds-midpoint'], [3, LC, 3, '30', 'key:whole-doublings'], [3, LC, 3, '60', 'key:rounded-up'],
  [3, LC, 4, '6', true], [3, LC, 4, '6.0', true], [3, LC, 4, '6 cm', 'noparse'], [3, LC, 4, '6cm', 'noparse'], [3, LC, 4, '3', 'key:pounds'], [3, LC, 4, '4', 'key:ratio'],
  [3, MD, 1, '1.0491', true], [3, MD, 1, '1.04907', true], [3, MD, 1, '1.049', false], [3, MD, 1, '1.0490', false], [3, MD, 1, '1.05', false], [3, MD, 1, '1.048', 'key:once'], [3, MD, 1, '1.0480', 'key:once'], [3, MD, 1, '1.0492', 'key:continuous'], [3, MD, 1, '1.7552', 'key:whole-rate'],
  [3, MD, 2, '4.79', true], [3, MD, 2, '4.79%', true], [3, MD, 2, '4.793', true], [3, MD, 2, '4.80', 'key:quoted'], [3, MD, 2, '4.8', 'key:quoted'], [3, MD, 2, '4.91', 'key:factor-rate'], [3, MD, 2, '0.0479', 'key:decimal'], [3, MD, 2, '2.08', 'key:log10'], [3, MD, 2, '4.78', false],
  [3, MD, 3, '0.2395', true], [3, MD, 3, '0.23952', true], [3, MD, 3, '23.95%', true], [3, MD, 3, '0.24', 'key:quoted'], [3, MD, 3, '0.240', 'key:quoted'], [3, MD, 3, '0.239', false], [3, MD, 3, '0.2708', 'key:simple'], [3, MD, 3, '0.2706', 'key:simple'], [3, MD, 3, '0.0479', 'key:one-year'],
  [3, MD, 4, '7624', true], [3, MD, 4, '£7,624', true], [3, MD, 4, '7623.68', true], [3, MD, 4, '7623.84', true], [3, MD, 4, '7623', false], [3, MD, 4, '7625', false], [3, MD, 4, '7437', 'key:one-plus'], [3, MD, 4, '7627', 'key:quoted'], [3, MD, 4, '7440', 'key:simple-interest'],
];

let checks = 0, fails = 0, findings = 0;
const say = (ok, finding, msg) => { checks++; if (ok) return; if (finding) { findings++; console.log('FINDING ' + msg + '   [' + finding + ']'); } else { fails++; console.log('FAIL    ' + msg); } };

const gradeNumeric = (w, text) => {
  const t = text.trim(), pct = w.unit === '%';
  let v = G.parseNum(t); if (pct && !t.includes('%')) v /= 100;
  if (!Number.isFinite(v)) return { ok: false, key: 'NOPARSE' };
  if (G.within(v, +w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, { abs: 1e-9 }); return { ok: false, key: m ? m.id : null };
};
const gradeExpr = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  if ([w.answer, ...(w.accept || [])].some(eq)) return { ok: true, key: null };
  const x = (w.wrong || []).find(x => x.tex && eq(x.tex));
  return { ok: false, key: x ? x.id : null };
};

let parts = 0;
for (const n of [1, 2, 3]) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/exp-log/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    parts++;
    const w = p.widget, where = `${n} ${it.id} part ${i + 1}`, by = (p.feedback && p.feedback.byKey) || {};
    const typed = T.filter((r) => r[0] === n && r[1] === it.id && r[2] === i + 1);
    if (w.kind === 'choice') { say(w.options.filter(o => o.correct).length === 1 && w.options.every(o => o.correct || o.why), null, `${where}: choice key or why missing`); return; }
    const grade = w.kind === 'numeric' ? (t) => gradeNumeric(w, t) : (t) => gradeExpr(w, t);
    say(typed.length >= 4, null, `${where}: fewer than four typed rows`);
    if (w.kind === 'numeric') {
      const k = w.unit === '%' ? 100 : 1;
      say(grade(String(+(w.answer * k).toPrecision(10))).ok, null, `${where}: the key itself is refused`);
      for (const x of w.wrong || []) {
        const r = grade(String(+(x.value * k).toPrecision(10)));
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.value} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    } else {
      for (const a of [w.answer, ...(w.accept || [])]) say(grade(a).ok, null, `${where}: "${a}" is refused`);
      for (const x of w.wrong || []) {
        const r = grade(x.tex);
        say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${x.tex} grades ${r.ok ? 'correct' : 'to key ' + r.key}`);
        say(!!by[x.id], null, `${where}: wrong "${x.id}" has no byKey line`);
      }
    }
    for (const r of typed) {
      const res = grade(r[3]), want = r[4];
      const good = want === true ? res.ok : want === false ? !res.ok && res.key !== 'NOPARSE' : want === 'noparse' ? res.key === 'NOPARSE' : !res.ok && 'key:' + res.key === want;
      if (SHOW) console.log(`      ${where}: "${r[3]}" -> ${res.ok ? 'correct' : 'wrong'} (key ${res.key})`);
      say(good, r[5], `${where}: typed "${r[3]}" -> ${res.ok ? 'correct' : 'wrong'} (key ${res.key}), expected ${want}`);
    }
  });
}
console.log(`grade-check: ${parts} parts, ${T.length} typed rows, ${checks} checks, ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
