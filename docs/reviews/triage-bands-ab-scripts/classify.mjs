#!/usr/bin/env node
/* Writes docs/reviews/triage-bands-ab.md from out/pile1.json, out/pile2.json, out/pile3.json and out/pile3-fluency.json.
     node classify.mjs --local-cdn <pkgs> [--commit <sha>] [--counts "149,36,257"]
   A verdict is automatic where the dossier settles it (a probe the real grader took or refused, a printed figure that is one of the
   item's own wrong values) and comes from the hand-read tables below otherwise. Every proposed fix is applied to a copy of the
   widget and graded again here, so the "Fix" column is checked, not asserted. */
import fs from 'node:fs';
import path from 'node:path';
import { APP, OUT, REPO, boot, gradeText, cdnArg, resolve, readJson, num } from './lib.mjs';

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const { reg } = boot(cdnArg());
const have = (f) => fs.existsSync(path.join(OUT, f));
const p1 = have('pile1.json') ? readJson(path.join(OUT, 'pile1.json')) : [];
const p2 = have('pile2.json') ? readJson(path.join(OUT, 'pile2.json')) : [];
const p3 = have('pile3.json') ? readJson(path.join(OUT, 'pile3.json')) : [];
const fl = have('pile3-fluency.json') ? readJson(path.join(OUT, 'pile3-fluency.json')) : [];
const stem = (f) => f.replace(/^content\//, '').replace(/^courses\//, '').replace(/\.json$/, '');
const group = (f) => { const s = f.replace(/^content\//, ''); return s.startsWith('courses/') ? s.split('/')[1] : s.startsWith('exams/') ? 'exams/' + path.basename(s, '.json') : s.startsWith('tools/fixtures') ? 'tools/fixtures (not content)' : s.split('/')[0]; };

/* ---------- classes ---------- */
const CLS = {
  H1: ['harmless', 'half-unit band: the answer rounded as asked is accepted and the item\'s printed working lands on it'],
  H2: ['harmless', 'the explanation prints fewer places than the question asks; the form asked is accepted'],
  H3: ['harmless', 'a small slip value with an absolute band: only that slip, rounded as asked, falls inside'],
  H4: ['harmless', 'a deliberate catch-all band (any huge number, any small positive number)'],
  T1: ['tool limit', 'the printed figure is one of the item\'s own wrong[] values (a slip the text names)'],
  T2: ['tool limit', 'the printed figure is the value before a whole-number round-up or round-down'],
  T3: ['tool limit', 'the printed figure is followed by \\ldots: it is the unrounded working'],
  T4: ['tool limit', 'the last "=" or "\\approx" belongs to another quantity (a step, a check, the exact value beside an estimate)'],
  T5: ['tool limit', 'a "{,}" thousands separator is read as the end of the number'],
  T6: ['tool limit', '"whole number" in the prose describes the thing picked, not the form of the answer'],
  T7: ['tool limit', 'the band counted is the grader\'s float slack (1e-9 absolute, 1e-12 relative), not the authored tol'],
  T8: ['tool limit', 'a fluency family template ("{key}") is graded as if it were the answer'],
  T9: ['tool limit', 'a carried value ("{{carry.name}}") is graded as if it were the answer'],
  F1: ['content fault', 'right answer marked wrong: the item\'s own printed figure is refused'],
  F2: ['content fault', 'right answer marked wrong: a working with rounded figures lands one unit out'],
};

/* ---------- pile 1: hand-read verdicts, keyed "<file stem>:<item id>" ---------- */
const P1 = {
  'number-sense/homework-2:hw-seven-twelfths': ['T3', 'asked for 3 places; 0.583 accepted'],
  'equations/problems-2:p-climbing-wall': ['T3', 'asked for whole pence; 7.28 accepted'],
  'series/l12-small-x:q-three-terms': ['T4', '1.26677 is the exact value set beside the three-term estimate 1.2652'],
  'mental/l7-near-round:q-hedge': ['T4', '6400 is the round number before the 1% is taken off'],
  'plotting/review-2:r7': ['T4', '0.99 is one up-and-down pair; the answer is two pairs'],
  'taylor/l3-newton:q-root-five': ['T4', '2.2361 is the root, the answer is the first Newton step'],
  'taylor/l3-newton:q-cube-nine': ['T4', '2.0801 is the root, the answer is the first Newton step'],
  'micro/l10-inventory:q-skew-ask': ['T4', '796 is the skewed centre; the ask is 3p above it'],
  'micro/review-3:r-skew-bid': ['T4', '1202 is the skewed centre; the bid is 3p below it'],
  'analysis/l12-convergence-tests:q-n-over-2n': ['T4', '1.9883 is the check value S_10'],
  'analysis/review-3:r-integral-mid': ['T4', '1.64493 is pi^2/6, set beside the estimate 1.64497'],
  'micro/l2-walking-the-book:q-sell': ['T5', 'the text prints 49{,}988 (the total), read as 49'],
  'counting-chance/l9-double-counting:q-two-or-five': ['T6', 'no rounding is asked; the answer 0.6 is accepted'],
  'counting-chance/l9-double-counting:q-two-three-five': ['T6', 'no rounding is asked; 0.7333 and 11/15 are accepted'],
  'counting-chance/review-2:r-flush': ['H2', 'a fraction is asked; 33/66640 accepted'],
  'random-vars/homework-2:h-squares-game': ['H2', 'three places asked; 0.167 accepted'],
  'analysis/l4-archimedes:q-third-half': ['H2', 'a fraction is asked; 3/7 accepted'],
  'puzzles/l2-every-coupon:q-suits': ['H2', 'four places asked; 8.3333 accepted'],
  'puzzles/l4-indicator-tricks:q-three-dice': ['H2', 'four places asked; 2.5278 accepted'],
  'puzzles/review-1:r1-months': ['H2', 'four places asked; 37.2385 accepted'],
  'mm-games/l3-how-wide:q-three-nine-twelve': ['H2', 'four places or a fraction asked; 0.4815 and 13/27 accepted'],
  'mm-games/review-1:r-abs-diff': ['H2', 'four places or a fraction asked; 1.9444 and 35/18 accepted'],
  'mm-games/review-1:r-eight-thirteen': ['H2', 'four places or a fraction asked; 0.6759 and 73/108 accepted'],
  'mm-games/homework-1:h-distinct-faces': ['H2', 'four places or a fraction asked; 2.5278 and 91/36 accepted'],
  'mm-games/homework-3:h-mock-fair-1': ['H2', 'four places asked; 21.9608 accepted'],
  'mm-games/l17-options-on-a-game:q-strad8': ['H2', 'four places asked; 2.1111 accepted'],
  'bank/probability-2:duels-weaker-shoots-first': ['H2', 'four places or a fraction asked; 0.5172 and 15/29 accepted'],
  'conditional/review-5:r-low-prior': ['F1', 'no form is asked (placeholder "fraction or decimal"); the explanation gives $\\tfrac{6}{13} \\approx 0.46$', { tol: { abs: 0.005 } }, ['0.46', '6/13', '0.4615', '0.462']],
  'regression/l5-how-sure:q-month-sd': ['F1', 'no form is asked; the feedback gives $6 / 23.66 = 0.25$', { tol: { abs: 0.005 } }, ['0.25', '0.254', '0.2535']],
  'cpp-pricing/l6-binomial-cpp:q-one-step': ['F1', 'asked "in pounds"; the explanation and the accept line both give £11.90', { tol: { abs: 0.005 } }, ['11.90', '11.9', '11.9048']],
  'cpp-pricing/review-2:r-one-step-put': ['F1', 'asked "in pounds"; the whole of feedback.correct is "£3.92."', { tol: { abs: 0.005 } }, ['3.92', '3.9216']],
  'alpha/l7-ranks-and-z:q4': ['F1', 'no form is asked; feedback.correct and explain.text both end "= 2.47"', { tol: { abs: 0.005 } }, ['2.47', '2.475', '2.4749']],
  'exams/stage-3:r-t-bar': ['F2', 'two places asked, no working printed; a standard error kept to three places (3.1/sqrt(360) = 0.163) gives 0.45/0.163 = 2.76', { tol: { abs: 0.01 } }, ['2.76', '2.75']],
  'exams/stage-3:r-best-of-twenty': ['F2', 'two places asked and the answer 0.225156 sits on the rounding edge; tables at z = 2.24 give 1 - 0.9875^20 = 0.2224, so 0.22; the explanation\'s own 1 - 0.775 = 0.225 also rounds either way', { tol: { abs: 0.006 } }, ['0.22', '0.23', '0.225']],
};
/* ---------- pile 2: hand-read verdicts, keyed "<file stem>:<path>" ---------- */
const P2 = {
  'pytest/l4-floats-in-tests:quiz[1].widget.wrong[1]': ['T7', 'authored tol 1e-13 is a tenth of the value 1e-12'],
  'exams/topic-2.5:items[3].widget.wrong[0]': ['T7', 'authored tol is 0.1% of the value 2.2e-16'],
  'stat-learning/l8-setting-to-zero:screens[8].widget.wrong[0]': ['H4', 'catches any huge number as "infinity"; the answer 0.6 and the slips 1.55 and 0.05 are far below 1000'],
  'measure-prob/l1-why-measure:screens[1].widget.wrong[0]': ['H4', 'the answer is 0 exactly; the band catches a small positive number'],
};
const P2_NOTE = {
  'backtest/review-3:items[3].widget.wrong[0]': 'the answer typed as a decimal in the per cent field (0.03024) lands in this band and is told "that is alpha per day"; it is marked wrong either way',
};

/* ---------- fixes, graded again ---------- */
const cache = {};
const widget = (file, where) => resolve((cache[file] ??= readJson(path.join(APP, file))), where).node;
const checkFix = async (file, where, set, accepts) => {
  const w0 = widget(file, where), w = { ...w0, ...set };
  const ok = [], badOk = [];
  for (const t of accepts) { const g = await gradeText(reg, w, t); (g.ok ? ok : badOk).push(t); }
  let wrongKept = true;
  for (const x of (w.wrong || [])) { if (typeof x.value !== 'number') continue; const g = await gradeText(reg, w, num(w.unit === '%' ? x.value * 100 : x.value)); if (g.ok || g.key !== x.id) wrongKept = false; }
  return { ok, badOk, wrongKept, n: (w.wrong || []).length };
};

const rows = [];   // { pile, group, file, path, id, cls, ev, fix }
/* pile 1 */
for (const r of p1) {
  const key = `${stem(r.file)}:${r.id}`;
  let cls, ev, fix = '';
  const man = P1[key];
  const whole = Number.isInteger(r.answer) && r.hw <= 0.5 + 1e-9;
  if (man && (r.cls !== 'half-unit' || man[0][0] === 'F')) {
    cls = man[0]; ev = (r.cls === 'prints' ? `${r.src} prints ${r.probe.typed}, refused; ` : r.cls === 'rounded' ? `the rule rounds ${r.answer} to ${r.probe.typed}; ` : `${r.probe.typed} accepted, ${r.up.typed} and ${r.down.typed} refused; `) + man[1];
    if (man[2]) {
      const c = await checkFix(r.file, r.path, man[2], man[3]);
      if (c.badOk.length || !c.wrongKept) throw new Error(`fix for ${key} fails: refused ${c.badOk.join(', ')} wrongKept ${c.wrongKept}`);
      fix = `\`"tol": ${JSON.stringify(man[2].tol)}\` (was \`${JSON.stringify(r.tol)}\`); with it the grader takes ${c.ok.join(', ')} and ${c.n === 1 ? 'the wrong value keeps its own line' : `the ${c.n} wrong values keep their own lines`}`;
    }
  } else if (r.cls === 'half-unit') { cls = 'H1'; ev = `${r.d} place${r.d === 1 ? '' : 's'} asked; ${r.probe.typed} accepted, ${r.up.typed} and ${r.down.typed} refused`; }
  else if (r.cls === 'prints' && r.probe.key) { cls = 'T1'; ev = `${r.src} prints ${r.probe.typed}, the wrong value "${r.probe.key}"; the answer ${num(r.unit === '%' ? r.answer * 100 : r.answer)} is accepted`; }
  else if (r.cls === 'prints' && whole && !Number.isInteger(r.printed)) { cls = 'T2'; ev = `${r.src} prints ${r.probe.typed}, then rounds to the whole number ${r.answer}, which is accepted`; }
  else if (r.cls === 'prints' && whole) { cls = 'T2'; ev = `${r.src} prints ${r.probe.typed} as the bound; the first whole number past it, ${r.answer}, is accepted`; }
  else throw new Error('pile 1 entry with no verdict: ' + key + ' ' + r.cls);
  if (!r.self.ok) throw new Error('stored answer refused: ' + key);
  rows.push({ pile: 1, group: group(r.file), file: r.file, path: r.path, id: r.id, cls, ev, fix });
}
/* pile 2 */
for (const r of p2) {
  const key = `${stem(r.file)}:${r.path}`;
  const man = P2[key], shadow = r.others.filter(o => o.shadowed);
  if (!r.self.ok || r.ansInWrongBand || shadow.length) throw new Error('pile 2 entry needs a hand verdict: ' + key);
  const cls = man ? man[0] : 'H3';
  const k = r.unit === '%' ? 100 : 1, band = `[${num(r.lo * k)}, ${num(r.hi * k)}]${r.unit === '%' ? ' %' : ''}`;
  let ev = `slip "${r.wid}" ${num(r.wvalue * k)} has band ${band}; the answer ${num(r.answer * k)} grades correct${r.others.length ? ` and the other ${r.others.length === 1 ? 'slip keeps its' : r.others.length + ' slips keep their'} own line${r.others.length === 1 ? '' : 's'}` : ''}${!r.zero.ok && r.zero.key === r.wid ? '; a typed 0 gets this line' : ''}`;
  if (man) ev += '; ' + man[1];
  if (P2_NOTE[key]) ev += '; ' + P2_NOTE[key];
  rows.push({ pile: 2, group: group(r.file), file: r.file, path: r.path, id: r.id, cls, ev, fix: '' });
}
/* pile 3 */
const flBy = Object.fromEntries(fl.map(f => [f.file + ' ' + f.path, f]));
for (const r of p3) {
  const f = flBy[r.file + ' ' + r.path];
  let cls, ev;
  if (/\{\{carry\./.test(JSON.stringify(r.answer))) {
    cls = 'T9';
    const w0 = widget(r.file, r.path), got = [];
    for (const v of ['-2', '0', '3']) { const g = await gradeText(reg, { ...w0, answer: v }, v); const g2 = await gradeText(reg, { ...w0, answer: v }, String(+v + 1)); if (!g.ok || g2.ok) throw new Error('carry check fails'); got.push(v); }
    ev = `the answer is "${r.answer}", filled from an earlier screen; with the carried value set to ${got.join(', ')} the same number grades correct and its neighbour does not`;
  } else if (f && !f.notFamily && !f.error) {
    if (f.selfBad || f.acceptBad || f.roundBad || f.wrongOk || f.failed) throw new Error('fluency family needs a hand verdict: ' + r.file + ' ' + r.path);
    cls = 'T8';
    ev = `template ${JSON.stringify(r.answer)}; ${f.drawn} draws of family "${f.family}": every realised answer grades correct${f.acceptN ? `, as do ${f.acceptN} accept forms` : ''}${f.roundN ? `, and the answer rounded as asked (${f.roundN})` : ''}; none of ${f.wrongN} wrong values grades correct`;
  } else throw new Error('pile 3 entry with no verdict: ' + r.file + ' ' + r.path);
  rows.push({ pile: 3, group: group(r.file), file: r.file, path: r.path, id: f && f.family ? f.family : r.id, cls, ev, fix: '' });
}

/* ---------- the document ---------- */
const V = ['content fault', 'harmless', 'tool limit'];
const count = (pile, v) => rows.filter(r => r.pile === pile && CLS[r.cls][0] === v).length;
const piles = [[1, '`[tight-band]`'], [2, '`[wide-wrong-band]`'], [3, '`grade-regression` self-grade notes']].filter(([n]) => rows.some(r => r.pile === n));
const L = [];
L.push('# Triage: band warnings and self-grade notes (session AB)', '');
L.push(`Scope: every \`[tight-band]\` and \`[wide-wrong-band]\` warning of \`node tools/validate.mjs\` and every authored answer that \`node tools/grade-regression.mjs\` notes as not grading correct itself, at commit \`${arg('--commit', 'unknown')}\`. Counts seen: ${arg('--counts', '').split(',').join(', ')} (tight-band, wide-wrong-band, self-grade notes). The self-grade count has moved from the 198 of session AA; a grader pass is running on another branch, so the count is tied to this commit.`, '');
L.push('Method: `triage-bands-ab-scripts/` opens each item and grades probe answers with the real grader (`js/engine/grade.js` and the numeric and expression widgets, loaded as `grade-regression.mjs` loads them, Compute Engine from the local `pkgs`). Probes: the answer as stored; the answer rounded as asked; one unit either side; the figure the text prints; every other `wrong[]` value; 0. For pile 3 each fluency family is drawn 40 times with `js/engine/gen.js` and the realised answer, accept forms and wrong values are graded. A verdict comes from the probe where it settles the case, and from a hand reading of the item otherwise (tables `P1` and `P2` in `classify.mjs`). Every proposed fix is applied to a copy of the widget and graded again. No content or engine file was edited.', '');
L.push('Verdicts: `content fault` (a right answer in the form asked is marked wrong, or a wrong one right); `harmless` (the rule fires, no sensible answer is misgraded); `tool limit` (the rule or tool misreads the item).', '');
L.push('## Summary', '', `| Pile | Entries | ${V.join(' | ')} |`, '|---|---|---|---|---|');
for (const [n, name] of piles) L.push(`| ${n}. ${name} | ${rows.filter(r => r.pile === n).length} | ${V.map(v => count(n, v)).join(' | ')} |`);
L.push(`| Total | ${rows.length} | ${V.map(v => rows.filter(r => CLS[r.cls][0] === v).length).join(' | ')} |`, '');
L.push('By class:', '', '| Class | Verdict | Pile | Entries | What it is |', '|---|---|---|---|---|');
for (const c of Object.keys(CLS)) { const rs = rows.filter(r => r.cls === c); if (rs.length) L.push(`| ${c} | ${CLS[c][0]} | ${[...new Set(rs.map(r => r.pile))].join(', ')} | ${rs.length} | ${CLS[c][1]} |`); }
L.push('');
const faults = rows.filter(r => CLS[r.cls][0] === 'content fault');
const items = [...new Set(faults.map(r => r.file + ' ' + r.path))];
L.push(`Content faults: ${faults.length} entries on ${items.length} items, all in pile 1 and all "right answer marked wrong". By course or exam: ${Object.entries(faults.reduce((a, r) => { const s = new Set(a[r.group] || []); s.add(r.file + r.path); a[r.group] = s; return a; }, {})).map(([g, s]) => `${g} ${s.size}`).join(', ')}. No wrong answer is marked right anywhere in the three piles.`, '');
L.push('## Content faults, with the fix', '');
for (const k of items) { const r = faults.find(x => x.file + ' ' + x.path === k); L.push(`- \`${stem(r.file)}.json\` \`${r.path}\` (${r.id}): ${r.ev}. Fix: ${r.fix}.`); }
L.push('');
L.push('## Entries', '', 'One line per entry: pile, file, path, item id (or family), verdict and class, evidence. A fix is given only for a content fault.', '');
const groups = [...new Set(rows.map(r => r.group))].sort((a, b) => (a.startsWith('exams') - b.startsWith('exams')) || (a.startsWith('tools') - b.startsWith('tools')) || a.localeCompare(b));
for (const g of groups) {
  const rs = rows.filter(r => r.group === g);
  L.push(`### ${g} (${rs.length})`, '');
  for (const r of rs.sort((a, b) => a.pile - b.pile)) L.push(`- P${r.pile} \`${path.basename(r.file)}\` \`${r.path}\` (${r.id}) | ${CLS[r.cls][0]} ${r.cls} | ${r.ev}${r.fix ? ` | fix: ${r.fix}` : ''}`);
  L.push('');
}
const n = (c) => rows.filter(r => r.cls === c).length;
const tail = path.join(path.dirname(new URL(import.meta.url).pathname), 'rule-changes.md');
if (fs.existsSync(tail)) L.push(fs.readFileSync(tail, 'utf8').replace(/\{n:(\w+)\}/g, (_, c) => String(n(c))).trim(), '');
fs.writeFileSync(path.join(REPO, 'docs/reviews/triage-bands-ab.md'), L.join('\n'));
console.log('| pile | entries | ' + V.join(' | ') + ' |');
for (const [k] of piles) console.log(`| ${k} | ${rows.filter(r => r.pile === k).length} | ${V.map(v => count(k, v)).join(' | ')} |`);
console.log(Object.keys(CLS).map(c => `${c}=${n(c)}`).join(' '));
