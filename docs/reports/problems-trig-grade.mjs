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
];

let checks = 0, fails = 0;
const say = (ok, msg) => { checks++; if (!ok) { fails++; console.log('FAIL ' + msg); } };
const exprOk = (w, L) => {
  const fo = { functions: w.functions || [], integers: w.integers || [] };
  const eq = (t) => { try { return !!G.exprEqual(ce, L, t, fo); } catch { return false; } };
  return [w.answer, ...(w.accept || [])].some(eq) && (!w.form || G.exprFormOk(ce, w.form, L, fo.functions));
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
    const typed = T.filter((r) => r[0] === n && r[1] === it.id && r[2] === i + 1);
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
  for (const r of T.filter((x) => x[0] === n)) say(set.items.some((it) => it.id === r[1] && it.parts[r[2] - 1]), `typed row for missing part ${r[1]} p${r[2]}`);
}
console.log(`grade: ${checks} checks, ${fails} failures`);
process.exit(fails ? 1 : 0);
