/* Engine graders on every part of trig problems 1 to 3, plus the forms a learner would type. Run from repo root:
   node docs/reports/problems-trig-grade.mjs --local-cdn <pkgs>
   Numeric parts: key inside its band, each wrong outside the key and the other wrongs, typed strings right or wrong as
   expected, and each typed slip routed to its own wrong key. Expression parts: answer and accept lines graded correct,
   wrong[].tex graded wrong, typed strings as expected (form checks included). Sets: numSetGrade and exprSetGrade. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const argv = process.argv.slice(2);
const cdn = argv[argv.indexOf('--local-cdn') + 1];
const ceFile = path.join(cdn, 'cortex-js-compute-engine-0.30.2', 'package', 'dist', 'compute-engine.min.umd.js');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
vm.runInContext(fs.readFileSync(ceFile, 'utf8'), g);
const ce = new (g.ComputeEngine.ComputeEngine || g.ComputeEngine)();
g.ZQ = {}; vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;

/* [set, item, part, typed, expected: true (right) | false (wrong) | '<wrong id>' (wrong, routed to that key)] */
const T = [
  [1, 'p-zip-wire', 1, '37', true], [1, 'p-zip-wire', 1, '37.0', true], [1, 'p-zip-wire', 1, '47', 'added'], [1, 'p-zip-wire', 1, '38', 'used-14'], [1, 'p-zip-wire', 1, '37.7', 'used-14'], [1, 'p-zip-wire', 1, '33', 'subtracted'], [1, 'p-zip-wire', 1, '32.88', 'subtracted'],
  [1, 'p-zip-wire', 2, '12/37', true], [1, 'p-zip-wire', 2, '0.324', true], [1, 'p-zip-wire', 2, '0.3243', true], [1, 'p-zip-wire', 2, '0.32', false], [1, 'p-zip-wire', 2, '12/35', 'tan'], [1, 'p-zip-wire', 2, '0.343', 'tan'], [1, 'p-zip-wire', 2, '35/37', 'cos'], [1, 'p-zip-wire', 2, '37/12', 'flipped'],
  [1, 'p-zip-wire', 3, '6.49', true], [1, 'p-zip-wire', 3, '6.48', true], [1, 'p-zip-wire', 3, '6.486', true], [1, 'p-zip-wire', 3, '6.5', false], [1, 'p-zip-wire', 3, '18.92', 'cos'], [1, 'p-zip-wire', 3, '6.86', 'tan'], [1, 'p-zip-wire', 3, '7.51', 'height'],
  [1, 'p-zip-wire', 4, '18.92', true], [1, 'p-zip-wire', 4, '18.918', true], [1, 'p-zip-wire', 4, '18.9', false], [1, 'p-zip-wire', 4, '13.51', 'subtracted'], [1, 'p-zip-wire', 4, '21.03', 'added'],
  [1, 'p-hexagon-tile', 1, '5\\sqrt{3}', true], [1, 'p-hexagon-tile', 1, '5\\sqrt3', true], [1, 'p-hexagon-tile', 1, '\\sqrt{75}', true], [1, 'p-hexagon-tile', 1, 'sqrt(75)', true], [1, 'p-hexagon-tile', 1, '8.66', false], [1, 'p-hexagon-tile', 1, '\\sqrt{125}', false], [1, 'p-hexagon-tile', 1, '5', false],
  [1, 'p-hexagon-tile', 2, '10\\sqrt{3}', true], [1, 'p-hexagon-tile', 2, '\\sqrt{300}', true], [1, 'p-hexagon-tile', 2, '2\\times5\\sqrt{3}', true], [1, 'p-hexagon-tile', 2, '17.32', false], [1, 'p-hexagon-tile', 2, '20', false],
  [1, 'p-hexagon-tile', 3, '400', true], [1, 'p-hexagon-tile', 3, '130', 'root-as-three'], [1, 'p-hexagon-tile', 3, '273.2', 'root-left'], [1, 'p-hexagon-tile', 3, '310', 'cd-unsquared'],
  [1, 'p-hexagon-tile', 4, '30', true], [1, 'p-hexagon-tile', 4, '30°', false /* engine limit: the numeric field does not read a degree sign; see BACKLOG-INBOX */], [1, 'p-hexagon-tile', 4, '60', 'angle-d'], [1, 'p-hexagon-tile', 4, '27', 'tan'], [1, 'p-hexagon-tile', 4, '26.57', 'tan'], [1, 'p-hexagon-tile', 4, '0.5236', 'radians'], [1, 'p-hexagon-tile', 4, '1', 'radians'],
  [1, 'p-lake-markers', 2, '50.27', true], [1, 'p-lake-markers', 2, '50.28', true], [1, 'p-lake-markers', 2, '50.275', true], [1, 'p-lake-markers', 2, '50.3', false], [1, 'p-lake-markers', 2, '2527.56', 'no-root'], [1, 'p-lake-markers', 2, '2527.69', 'no-root'], [1, 'p-lake-markers', 2, '93.39', 'plus'], [1, 'p-lake-markers', 2, '75', 'pythagoras'],
  [1, 'p-lake-markers', 3, '47.2', true], [1, 'p-lake-markers', 3, '47.1', true], [1, 'p-lake-markers', 3, '47.17', true], [1, 'p-lake-markers', 3, '47.3', false], [1, 'p-lake-markers', 3, '77.9', 'wrong-side'], [1, 'p-lake-markers', 3, '0.73', 'ratio'], [1, 'p-lake-markers', 3, '0.7333', 'ratio'], [1, 'p-lake-markers', 3, '0.8', 'radians'], [1, 'p-lake-markers', 3, '0.82', 'radians'],
  [1, 'p-lake-markers', 4, '44.0', true], [1, 'p-lake-markers', 4, '44', true], [1, 'p-lake-markers', 4, '43.99', true], [1, 'p-lake-markers', 4, '44.02', true], [1, 'p-lake-markers', 4, '43.95', true], [1, 'p-lake-markers', 4, '44.1', false], [1, 'p-lake-markers', 4, '40.8', 'cos'], [1, 'p-lake-markers', 4, '33.0', 'used-45'], [1, 'p-lake-markers', 4, '64.8', 'tan'],
  [1, 'p-desk-lamp', 1, '20\\sqrt{3}', true], [1, 'p-desk-lamp', 1, '\\sqrt{1200}', true], [1, 'p-desk-lamp', 1, '40\\times\\frac{\\sqrt{3}}{2}', true], [1, 'p-desk-lamp', 1, '34.64', false], [1, 'p-desk-lamp', 1, '20', false], [1, 'p-desk-lamp', 1, '40\\sqrt{3}', false],
  [1, 'p-desk-lamp', 2, '50', true], [1, 'p-desk-lamp', 2, '70', 'added'], [1, 'p-desk-lamp', 2, '26', 'subtracted'], [1, 'p-desk-lamp', 2, '26.46', 'subtracted'],
  [1, 'p-desk-lamp', 3, '36.9', true], [1, 'p-desk-lamp', 3, '36.87', true], [1, 'p-desk-lamp', 3, '36.8', false], [1, 'p-desk-lamp', 3, '53.1', 'flipped'], [1, 'p-desk-lamp', 3, '48.6', 'sine'], [1, 'p-desk-lamp', 3, '0.64', 'radians'], [1, 'p-desk-lamp', 3, '0.6', 'radians'],
  [1, 'p-desk-lamp', 4, '19.6', true], [1, 'p-desk-lamp', 4, '19.62', true], [1, 'p-desk-lamp', 4, '19.64', true], [1, 'p-desk-lamp', 4, '19.7', false], [1, 'p-desk-lamp', 4, '30.0', 'angle-aob'], [1, 'p-desk-lamp', 4, '43.3', 'sixty'], [1, 'p-desk-lamp', 4, '46.0', 'cos'], [1, 'p-desk-lamp', 4, '49.6', 'added'],
  [1, 'p-desk-lamp', 5, '20\\sqrt{3}-15', true], [1, 'p-desk-lamp', 5, '-15+20\\sqrt{3}', true], [1, 'p-desk-lamp', 5, '5(4\\sqrt{3}-3)', true], [1, 'p-desk-lamp', 5, '19.64', false], [1, 'p-desk-lamp', 5, '20\\sqrt{3}+15', false], [1, 'p-desk-lamp', 5, '5\\sqrt{3}', false],
  [2, 'p-water-wheel', 1, '2.25', true], [2, 'p-water-wheel', 1, '9/4', true], [2, 'p-water-wheel', 1, '2.3', false], [2, 'p-water-wheel', 1, '12.96', 'times'], [2, 'p-water-wheel', 1, '0.444', 'flipped'], [2, 'p-water-wheel', 1, '0.358', 'turns'],
  [2, 'p-water-wheel', 2, '128.9', true], [2, 'p-water-wheel', 2, '128.92', true], [2, 'p-water-wheel', 2, '129', false], [2, 'p-water-wheel', 2, '0.04', 'wrong-way'], [2, 'p-water-wheel', 2, '0.0393', 'wrong-way'], [2, 'p-water-wheel', 2, '405', 'no-pi'],
  [2, 'p-water-wheel', 3, '4.87', true], [2, 'p-water-wheel', 3, '4.867', true], [2, 'p-water-wheel', 3, '4.9', false], [2, 'p-water-wheel', 3, '2.77', 'radian-mode'], [2, 'p-water-wheel', 3, '3.09', 'degree-mode'], [2, 'p-water-wheel', 3, '1.49', 'cos'], [2, 'p-water-wheel', 3, '1.87', 'no-hub'],
  [2, 'p-water-wheel', 4, '51.1', true], [2, 'p-water-wheel', 4, '51.08', true], [2, 'p-water-wheel', 4, '51.2', false], [2, 'p-water-wheel', 4, '231.1', 'cos-mirror'], [2, 'p-water-wheel', 4, '308.9', 'half-turn'], [2, 'p-water-wheel', 4, '38.9', 'minus-90'],
  [2, 'p-water-wheel', 5, '2.14', true], [2, 'p-water-wheel', 5, '2.1398', true], [2, 'p-water-wheel', 5, '2.1', false], [2, 'p-water-wheel', 5, '122.64', 'degrees'], [2, 'p-water-wheel', 5, '21.29', 'divided'], [2, 'p-water-wheel', 5, '3.26', 'between'],
  [2, 'p-two-buoys', 1, '10', true], [2, 'p-two-buoys', 1, '5', 'read-five'], [2, 'p-two-buoys', 1, '0.63', 'b-itself'], [2, 'p-two-buoys', 1, '4', 'times'],
  [2, 'p-two-buoys', 2, '2.5', true], [2, 'p-two-buoys', 2, '5/2', true], [2, 'p-two-buoys', 2, '1.57', 'angle'], [2, 'p-two-buoys', 2, '5', 'half'], [2, 'p-two-buoys', 2, '7.5', 'trough'],
  [2, 'p-two-buoys', 3, '5.5', true], [2, 'p-two-buoys', 3, '-0.5', 'early'], [2, 'p-two-buoys', 3, '3', 'lag'],
  [2, 'p-two-buoys', 4, '1.05', true], [2, 'p-two-buoys', 4, '1.047', true], [2, 'p-two-buoys', 4, '1.04', false], [2, 'p-two-buoys', 4, '1.1', false], [2, 'p-two-buoys', 4, '5.75', 'height'], [2, 'p-two-buoys', 4, '0.75', 'degree-mode'], [2, 'p-two-buoys', 4, '1.6', 'full-swing'],
  [2, 'p-observation-wheel', 1, '25', true], [2, 'p-observation-wheel', 1, '50', 'diameter'], [2, 'p-observation-wheel', 1, '53', 'top'], [2, 'p-observation-wheel', 1, '28', 'hub'],
  [2, 'p-observation-wheel', 2, '\\frac{\\pi}{10}', true], [2, 'p-observation-wheel', 2, '\\frac{2\\pi}{20}', true], [2, 'p-observation-wheel', 2, '\\pi/10', true], [2, 'p-observation-wheel', 2, '0.1\\pi', true], [2, 'p-observation-wheel', 2, '0.3142', false], [2, 'p-observation-wheel', 2, '20', 'period'], [2, 'p-observation-wheel', 2, '\\frac{\\pi}{20}', 'half'], [2, 'p-observation-wheel', 2, '\\frac{10}{\\pi}', 'flipped'],
  [2, 'p-observation-wheel', 3, '5', true], [2, 'p-observation-wheel', 3, '0', 'boarding'], [2, 'p-observation-wheel', 3, '10', 'top'], [2, 'p-observation-wheel', 3, '15', 'falling'],
  [2, 'p-observation-wheel', 4, '48.23', true], [2, 'p-observation-wheel', 4, '48.225', true], [2, 'p-observation-wheel', 4, '48.2', false], [2, 'p-observation-wheel', 4, '28.41', 'degree-mode'], [2, 'p-observation-wheel', 4, '42.69', 'no-shift'],
  [2, 'p-observation-wheel', 5, '12', true], [2, 'p-observation-wheel', 5, '7', 'no-shift'], [2, 'p-observation-wheel', 5, '18', 'half-period'], [2, 'p-observation-wheel', 5, '2', 'mirror-start'],
  [3, 'p-two-angles', 1, '-15/17', true], [3, 'p-two-angles', 1, '-0.8824', true], [3, 'p-two-angles', 1, '-0.882', false], [3, 'p-two-angles', 1, '15/17', 'sign'], [3, 'p-two-angles', 1, '9/17', 'one-minus'], [3, 'p-two-angles', 1, '225/289', 'no-root'],
  [3, 'p-two-angles', 2, '0.28', true], [3, 'p-two-angles', 2, '7/25', true], [3, 'p-two-angles', 2, '-0.28', 'negative'], [3, 'p-two-angles', 2, '0.04', 'one-minus'], [3, 'p-two-angles', 2, '0.0784', 'no-root'],
  [3, 'p-two-angles', 3, '0.2047', true], [3, 'p-two-angles', 3, '87/425', true], [3, 'p-two-angles', 3, '0.205', false], [3, 'p-two-angles', 3, '0.6988', 'sign'], [3, 'p-two-angles', 3, '0.7506', 'sum-of-sines'], [3, 'p-two-angles', 3, '-0.9788', 'cos-formula'],
  [3, 'p-two-angles', 4, '-0.9788', true], [3, 'p-two-angles', 4, '-416/425', true], [3, 'p-two-angles', 4, '-0.979', false], [3, 'p-two-angles', 4, '-0.7153', 'plus'], [3, 'p-two-angles', 4, '0.7153', 'sign'],
  [3, 'p-two-angles', 5, '168.2', true], [3, 'p-two-angles', 5, '168.19', true], [3, 'p-two-angles', 5, '168.3', false], [3, 'p-two-angles', 5, '11.8', 'principal'], [3, 'p-two-angles', 5, '191.8', 'third'], [3, 'p-two-angles', 5, '348.2', 'fourth'],
  [3, 'p-quadratic-in-sine', 1, '2s^2-3s+1=0', true], [3, 'p-quadratic-in-sine', 1, '-2s^2+3s-1=0', true], [3, 'p-quadratic-in-sine', 1, '2s^2+1=3s', true], [3, 'p-quadratic-in-sine', 1, '0=2s^2-3s+1', true],
  [3, 'p-quadratic-in-sine', 1, '2s^2-3s+1', false], [3, 'p-quadratic-in-sine', 1, 's^2-3s+2=0', 'not-distributed'], [3, 'p-quadratic-in-sine', 1, '-s^2+3s-2=0', 'not-distributed'], [3, 'p-quadratic-in-sine', 1, '2s^2+3s-3=0', 'cos-as-sin'], [3, 'p-quadratic-in-sine', 1, '2s^2-3s-5=0', 'moved-3'],
  [3, 'p-quadratic-in-sine', 2, '0.5, 1', true], [3, 'p-quadratic-in-sine', 2, '1, 0.5', true], [3, 'p-quadratic-in-sine', 2, '1/2, 1', true], [3, 'p-quadratic-in-sine', 2, 's = 0.5 or s = 1', true], [3, 'p-quadratic-in-sine', 2, '0.5', 'count'], [3, 'p-quadratic-in-sine', 2, '-0.5, -1', 'signs'], [3, 'p-quadratic-in-sine', 2, '2, 1', 'carried'],
  [3, 'p-quadratic-in-sine', 3, '30, 90, 150', true], [3, 'p-quadratic-in-sine', 3, '150, 30, 90', true], [3, 'p-quadratic-in-sine', 3, '30, 150', 'count'], [3, 'p-quadratic-in-sine', 3, '30, 90, 330', 'cos-rule'], [3, 'p-quadratic-in-sine', 3, '30, 90, 210', 'tan-rule'],
  [3, 'p-quadratic-in-sine', 4, '\\frac{5\\pi}{6}', true], [3, 'p-quadratic-in-sine', 4, '\\frac{5}{6}\\pi', true], [3, 'p-quadratic-in-sine', 4, '5\\pi/6', true], [3, 'p-quadratic-in-sine', 4, '150', 'degrees'], [3, 'p-quadratic-in-sine', 4, '150^\\circ', false],
  [3, 'p-quadratic-in-sine', 4, '\\frac{150\\pi}{180}', false], [3, 'p-quadratic-in-sine', 4, '2.618', false], [3, 'p-quadratic-in-sine', 4, '\\frac{\\pi}{2}', 'middle'], [3, 'p-quadratic-in-sine', 4, '\\frac{5\\pi}{12}', 'half'],
  [3, 'p-daylight-model', 1, '4.4', true], [3, 'p-daylight-model', 1, '8.8', 'range'], [3, 'p-daylight-model', 1, '16.4', 'longest'], [3, 'p-daylight-model', 1, '12', 'midline'],
  [3, 'p-daylight-model', 2, '\\frac{\\pi}{6}', true], [3, 'p-daylight-model', 2, '\\frac{2\\pi}{12}', true], [3, 'p-daylight-model', 2, '0.5236', false], [3, 'p-daylight-model', 2, '12', 'period'], [3, 'p-daylight-model', 2, '\\frac{\\pi}{3}', 'half-cycle'], [3, 'p-daylight-model', 2, '\\frac{6}{\\pi}', 'flipped'],
  [3, 'p-daylight-model', 3, '3', true], [3, 'p-daylight-model', 3, '6', 'peak'], [3, 'p-daylight-model', 3, '9', 'falling'], [3, 'p-daylight-model', 3, '12', 'trough'],
  [3, 'p-daylight-model', 4, '4, 8', true], [3, 'p-daylight-model', 4, 't = 8, t = 4', true], [3, 'p-daylight-model', 4, '4', 'count'], [3, 'p-daylight-model', 4, '1, 5', 'no-shift'], [3, 'p-daylight-model', 4, '2, 10', 'below'],
  [3, 'p-daylight-model', 5, '4', true], [3, 'p-daylight-model', 5, '8', 'outside'], [3, 'p-daylight-model', 5, '5', 'counted'],
  [3, 'p-garden-bed', 1, '30\\sin C', true], [3, 'p-garden-bed', 1, '30\\sin(C)', true], [3, 'p-garden-bed', 1, '30sin(C)', true], [3, 'p-garden-bed', 1, '\\frac{1}{2}\\times5\\times12\\sin C', true], [3, 'p-garden-bed', 1, '60\\sin C', 'no-half'], [3, 'p-garden-bed', 1, '30\\cos C', 'cos'], [3, 'p-garden-bed', 1, '30C', 'angle'], [3, 'p-garden-bed', 1, '30\\sin(C^\\circ)', false],
  [3, 'p-garden-bed', 2, '36.87, 143.13', true], [3, 'p-garden-bed', 2, '143.13, 36.87', true], [3, 'p-garden-bed', 2, '36.87', 'count'], [3, 'p-garden-bed', 2, '36.9, 143.1', false], [3, 'p-garden-bed', 2, '17.46, 162.54', 'no-half'], [3, 'p-garden-bed', 2, '36.87, 323.13', 'cos-rule'],
  [3, 'p-garden-bed', 3, '-0.8', true], [3, 'p-garden-bed', 3, '-4/5', true], [3, 'p-garden-bed', 3, '0.8', 'sign'], [3, 'p-garden-bed', 3, '0.4', 'one-minus'], [3, 'p-garden-bed', 3, '-0.64', 'no-root'],
  [3, 'p-garden-bed', 4, '16.28', true], [3, 'p-garden-bed', 4, '16.279', true], [3, 'p-garden-bed', 4, '16.3', false], [3, 'p-garden-bed', 4, '8.54', 'sign'], [3, 'p-garden-bed', 4, '13', 'pythagoras'], [3, 'p-garden-bed', 4, '265', 'no-root'], [3, 'p-garden-bed', 4, '14.73', 'no-two'],
];

/* Fix pass, problems 0.3 c: the rows of every renumbered or reshaped part (hexagon, lamp 1 3 5, two angles 1 3 4 5, daylight 4 5, garden 1 to 4, and the
   labelled angle of quadratic part 4) are replaced by the rows below; the other rows stand as they were. */
const NEW = [
  [1, 'p-hexagon-tile', 1, '4\\sqrt{3}', true], [1, 'p-hexagon-tile', 1, '4\\sqrt3', true], [1, 'p-hexagon-tile', 1, '\\sqrt{48}', true], [1, 'p-hexagon-tile', 1, 'sqrt(48)', true], [1, 'p-hexagon-tile', 1, '4\\cdot\\sqrt{3}', true],
  [1, 'p-hexagon-tile', 1, '\\sqrt{8^2-4^2}', false], [1, 'p-hexagon-tile', 1, '8\\sin(60^\\circ)', false], [1, 'p-hexagon-tile', 1, '6.93', false], [1, 'p-hexagon-tile', 1, '\\sqrt{80}', 'added'], [1, 'p-hexagon-tile', 1, '8\\sqrt{3}', 'whole-side'], [1, 'p-hexagon-tile', 1, '4\\sqrt{2}', 'half-square'], [1, 'p-hexagon-tile', 1, '4', false],
  [1, 'p-hexagon-tile', 2, '8\\sqrt{3}', true], [1, 'p-hexagon-tile', 2, '\\sqrt{192}', true], [1, 'p-hexagon-tile', 2, '2\\cdot4\\sqrt{3}', false], [1, 'p-hexagon-tile', 2, '13.86', false], [1, 'p-hexagon-tile', 2, '4\\sqrt{3}', 'half'], [1, 'p-hexagon-tile', 2, '8', 'side'], [1, 'p-hexagon-tile', 2, '16', 'long'],
  [1, 'p-hexagon-tile', 3, '256', true], [1, 'p-hexagon-tile', 3, '88', 'root-as-three'], [1, 'p-hexagon-tile', 3, '174.8', 'root-left'], [1, 'p-hexagon-tile', 3, '200', 'cd-unsquared'], [1, 'p-hexagon-tile', 3, '192', false],
  [1, 'p-hexagon-tile', 4, '30', true], [1, 'p-hexagon-tile', 4, '60', 'angle-d'], [1, 'p-hexagon-tile', 4, '27', 'tan'], [1, 'p-hexagon-tile', 4, '26.57', 'tan'], [1, 'p-hexagon-tile', 4, '0.5', 'half'], [1, 'p-hexagon-tile', 4, '0.5236', 'radians'], [1, 'p-hexagon-tile', 4, '0.52', 'radians'], [1, 'p-hexagon-tile', 4, '1', 'radians'], [1, 'p-hexagon-tile', 4, '31', false],
  [1, 'p-desk-lamp', 1, '20\\sqrt{3}', true], [1, 'p-desk-lamp', 1, '\\sqrt{1200}', true], [1, 'p-desk-lamp', 1, '40\\times\\frac{\\sqrt{3}}{2}', false], [1, 'p-desk-lamp', 1, '40\\sin(60^\\circ)', false], [1, 'p-desk-lamp', 1, '34.64', false], [1, 'p-desk-lamp', 1, '20', 'sin-30'], [1, 'p-desk-lamp', 1, '40\\sqrt{3}', 'no-half'],
  [1, 'p-desk-lamp', 3, '36.9', true], [1, 'p-desk-lamp', 3, '36.87', true], [1, 'p-desk-lamp', 3, '36.8', false], [1, 'p-desk-lamp', 3, '53.1', 'flipped'], [1, 'p-desk-lamp', 3, '48.6', 'sine'], [1, 'p-desk-lamp', 3, '0.64', 'radians'], [1, 'p-desk-lamp', 3, '0.644', 'radians'], [1, 'p-desk-lamp', 3, '0.6435', 'radians'],
  [1, 'p-desk-lamp', 3, '0.6', 'ratio-sin'], [1, 'p-desk-lamp', 3, '0.75', 'ratio-tan'], [1, 'p-desk-lamp', 3, '0.65', false], [1, 'p-desk-lamp', 3, '0.5', false],
  [1, 'p-desk-lamp', 5, '20\\sqrt{3}-15', true], [1, 'p-desk-lamp', 5, '-15+20\\sqrt{3}', true], [1, 'p-desk-lamp', 5, '5(4\\sqrt{3}-3)', false], [1, 'p-desk-lamp', 5, '40\\sin(60^\\circ)-30\\sin(30^\\circ)', false], [1, 'p-desk-lamp', 5, '19.64', false], [1, 'p-desk-lamp', 5, '20\\sqrt{3}+15', 'above'], [1, 'p-desk-lamp', 5, '5\\sqrt{3}', 'cos-30'],
  [3, 'p-two-angles', 1, '-45/53', true], [3, 'p-two-angles', 1, '-0.849057', true], [3, 'p-two-angles', 1, '-0.849', true], [3, 'p-two-angles', 1, '-0.85', false], [3, 'p-two-angles', 1, '-0.88', false], [3, 'p-two-angles', 1, '45/53', 'sign'], [3, 'p-two-angles', 1, '0.4717', 'one-minus'], [3, 'p-two-angles', 1, '2025/2809', 'no-root'],
  [3, 'p-two-angles', 3, '0.2694', true], [3, 'p-two-angles', 3, '357/1325', true], [3, 'p-two-angles', 3, '0.269', false], [3, 'p-two-angles', 3, '0.7449', 'sign'], [3, 'p-two-angles', 3, '0.8083', 'sum-of-sines'], [3, 'p-two-angles', 3, '-0.963', 'cos-formula'],
  [3, 'p-two-angles', 4, '-0.9630', true], [3, 'p-two-angles', 4, '-1276/1325', true], [3, 'p-two-angles', 4, '-0.96', false], [3, 'p-two-angles', 4, '-0.6672', 'plus'], [3, 'p-two-angles', 4, '0.6672', 'sign'],
  [3, 'p-two-angles', 5, '164.4', true], [3, 'p-two-angles', 5, '164.37', true], [3, 'p-two-angles', 5, '164.3', false], [3, 'p-two-angles', 5, '15.6', 'principal'], [3, 'p-two-angles', 5, '195.6', 'third'], [3, 'p-two-angles', 5, '344.4', 'fourth'],
  [3, 'p-quadratic-in-sine', 4, 'x=\\frac{5\\pi}{6}', false /* engine limit, inbox: the question now says "with no x = in front" */],
  [3, 'p-daylight-model', 4, '2, 10', true], [3, 'p-daylight-model', 4, 't = 10, t = 2', true], [3, 'p-daylight-model', 4, '2', 'count'], [3, 'p-daylight-model', 4, '7, 11', 'no-shift'], [3, 'p-daylight-model', 4, '4, 8', 'above'],
  [3, 'p-daylight-model', 5, '8', true], [3, 'p-daylight-model', 5, '4', 'outside'], [3, 'p-daylight-model', 5, '9', 'counted'],
  [3, 'p-garden-bed', 1, '65\\sin C', true], [3, 'p-garden-bed', 1, '65\\sin(C)', true], [3, 'p-garden-bed', 1, '65sin(C)', true], [3, 'p-garden-bed', 1, '\\frac{1}{2}\\times10\\times13\\sin C', true], [3, 'p-garden-bed', 1, '130\\sin C', 'no-half'], [3, 'p-garden-bed', 1, '65\\cos C', 'cos'], [3, 'p-garden-bed', 1, '65C', 'angle'],
  [3, 'p-garden-bed', 2, '22.62, 157.38', true], [3, 'p-garden-bed', 2, '157.38, 22.62', true], [3, 'p-garden-bed', 2, '22.62', 'count'], [3, 'p-garden-bed', 2, '22.6, 157.4', false], [3, 'p-garden-bed', 2, '11.09, 168.91', 'no-half'], [3, 'p-garden-bed', 2, '22.62, 337.38', 'cos-rule'],
  [3, 'p-garden-bed', 3, '-12/13', true], [3, 'p-garden-bed', 3, '-0.923', true], [3, 'p-garden-bed', 3, '-0.9231', true], [3, 'p-garden-bed', 3, '-0.92', false], [3, 'p-garden-bed', 3, '12/13', 'sign'], [3, 'p-garden-bed', 3, '8/13', 'one-minus'], [3, 'p-garden-bed', 3, '-0.852', 'no-root'],
  [3, 'p-garden-bed', 4, '22.56', true], [3, 'p-garden-bed', 4, '22.561', true], [3, 'p-garden-bed', 4, '22.6', false], [3, 'p-garden-bed', 4, '5.385', 'sign'], [3, 'p-garden-bed', 4, '16.4', 'pythagoras'], [3, 'p-garden-bed', 4, '509', 'no-root'], [3, 'p-garden-bed', 4, '19.72', 'no-two'],
];
const REPLACED = new Set(NEW.map((r) => r.slice(0, 3).join('|')));
const TT = [...T.filter((r) => !REPLACED.has(r.slice(0, 3).join('|'))), ...NEW];

/* the widget's own "simplified" check on a constant (expression.js), loaded as the second reader's probe.mjs did */
g.ZQ.widgets = { register() {}, dataPanel() { return null; } }; g.ZQ.h = () => ({}); g.ZQ.esc = (x) => x;
vm.runInContext(fs.readFileSync('app/js/engine/widgets/expression.js', 'utf8'), g);
const size = (j) => (Array.isArray(j) ? 1 + j.slice(1).reduce((a, x) => a + size(x), 0) : 1);
const simplifiedOk = (L) => G.withParsed(ce, L, [], (e) => { const j = e.json; const constant = !(e.unknowns || []).filter((v) => v !== 'iota').length; if (constant && g.ZQ.widgets.exprForms.reducible(j)) return false; try { return size(j) <= size(e.simplify().json); } catch { return true; } });

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } };
const exprOk = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo) || (!!G.normExpr(L) && G.normExpr(L) === G.normExpr(t)); } catch { return false; } };
  const shape = () => { if (!w.form) return true; if (w.form === 'simplified') { try { return !!simplifiedOk(L); } catch { return true; } } if (w.form === 'exact-angle') return !!G.shapeExactAngle(L); return G.exprFormOk(ce, w.form, L, fo.functions); };
  return [w.answer, ...(w.accept || [])].some(eq) && shape();
};
/* numeric single: { ok, key } */
const numGrade = (w, text) => {
  const v = G.parseNum(text);
  if (!Number.isFinite(v)) return { ok: false, key: null };
  if (G.within(v, w.answer, w.tol)) return { ok: true, key: null };
  const m = G.matchWrong(v, w.wrong, w.tol);
  return { ok: false, key: m ? m.id : null };
};
const grade = (w, text) => {
  if (w.kind === 'numeric') return Array.isArray(w.answers) ? G.numSetGrade(w, text) : numGrade(w, text);
  if (Array.isArray(w.answers)) return G.exprSetGrade(ce, w, text);
  if (exprOk(w, text)) return { ok: true, key: null };
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const hit = (w.wrong || []).find((x) => { try { return !!G.exprEqual(ce, text, x.tex, fo); } catch { return false; } });
  return { ok: false, key: hit ? hit.id : null };
};
const sets = argv.includes('--set') ? [Number(argv[argv.indexOf('--set') + 1])] : [1, 2, 3].filter((n) => fs.existsSync(`app/content/courses/trig/problems-${n}.json`));
for (const n of sets) {
  const set = JSON.parse(fs.readFileSync(`app/content/courses/trig/problems-${n}.json`, 'utf8'));
  for (const it of set.items) it.parts.forEach((p, i) => {
    const w = p.widget, where = `${n} ${it.id} p${i + 1}`;
    const typed = TT.filter((r) => r[0] === n && r[1] === it.id && r[2] === i + 1);
    if (w.kind === 'numeric' && !Array.isArray(w.answers)) {
      say(G.within(w.answer, w.answer, w.tol), `${where}: answer outside band`);
      for (const x of w.wrong || []) say(!G.within(x.value, w.answer, w.tol), `${where}: wrong ${x.id} inside answer band`);
      for (const x of w.wrong || []) say(numGrade(w, String(x.value)).key === x.id, `${where}: wrong ${x.id} value does not route to its own key`);
    } else if (w.kind === 'numeric') {
      say(grade(w, w.answers.join(', ')).ok, `${where}: answers do not grade right`);
      say(grade(w, [...w.answers].reverse().join(', ')).ok, `${where}: answers reversed do not grade right`);
      for (const x of w.wrong || []) { const r = grade(w, String(x.value)); say(!r.ok && r.key === x.id, `${where}: wrong set ${x.id} gives ${JSON.stringify(r)}`); }
    } else if (w.kind === 'expression' && !Array.isArray(w.answers)) {
      say(exprOk(w, w.answer), `${where}: answer not correct`);
      for (const a of w.accept || []) say(exprOk(w, a), `${where}: accept ${a} not correct`);
      for (const x of w.wrong || []) { const r = grade(w, x.tex); say(!r.ok && r.key === x.id, `${where}: wrong ${x.id} ${x.tex} gives ${JSON.stringify(r)}`); }
    } else if (w.kind === 'expression') {
      say(grade(w, w.answers.join(', ')).ok, `${where}: answers do not grade right`);
      for (const x of w.wrong || []) { const r = grade(w, x.tex); say(!r.ok && r.key === x.id, `${where}: wrong set ${x.id} gives ${JSON.stringify(r)}`); }
    }
    if (w.kind === 'choice') say(w.options.filter((o) => o.correct).length === 1, `${where}: not one keyed option`);
    for (const r of typed) {
      const got = grade(w, r[3]);
      if (r[4] === true) say(got.ok, `${where}: typed "${r[3]}" refused (${JSON.stringify(got)})`);
      else if (r[4] === false) say(!got.ok, `${where}: typed "${r[3]}" accepted`);
      else say(!got.ok && got.key === r[4], `${where}: typed "${r[3]}" gives ${JSON.stringify(got)}, wanted key ${r[4]}`);
    }
  });
  for (const r of TT.filter((x) => x[0] === n)) say(set.items.some((it) => it.id === r[1] && it.parts[r[2] - 1]), `typed row for missing part ${r[1]} p${r[2]}`);
}
console.log(`grade: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
