#!/usr/bin/env node
// Test for engine pass 8 part B (same-course reuse): exam items as sources, the retold false-positive classes and the identical slip line, --pairs, waivers with a source, rate exemptions,
// standard quantiles as stock constants, fresh-check --files. Fixtures: tools/fixtures/pass8/content (a small course "arma" with a lesson, an exam item carrying its skill and an exam item of another course)
// plus trees built in the test. The word frequencies are the snapshot tools/retold-model.json, so the test does not move with the content.
// Run from app/: node tools/test-fresh-check-pass8.mjs   (about forty seconds)
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, statSync, rmSync, copyFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const SC = join(HERE, 'same-course-reuse.mjs'), FC = join(HERE, 'fresh-check.mjs');
const FIX = join(HERE, 'fixtures', 'pass8', 'content');
let fails = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `  ${String(detail).slice(0, 800)}`}`); if (!ok) fails++; };
const put = (root, rel, o) => { const p = join(root, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, typeof o === 'string' ? o : JSON.stringify(o)); };
const copyDir = (from, to) => { mkdirSync(to, { recursive: true }); for (const f of readdirSync(from)) { const a = join(from, f), b = join(to, f); if (statSync(a).isDirectory()) copyDir(a, b); else copyFileSync(a, b); } };
const withTree = (files, f, fix = false) => { const tmp = mkdtempSync(join(tmpdir(), 'zq-p8-')); try { if (fix) copyDir(FIX, tmp); for (const [rel, o] of Object.entries(files)) put(tmp, rel, o); return f(tmp); } finally { rmSync(tmp, { recursive: true, force: true }); } };
const sc = (root, extra = ['--all'], env = {}) => { const r = spawnSync('node', [SC, '--content', root, ...extra], { encoding: 'utf8', env: { ...process.env, ...env } }); return { out: r.stdout, err: r.stderr, status: r.status }; };
const scan = (root, extra = ['--all'], env = {}) => { const r = sc(root, [...extra, '--json'], env); try { return { hits: JSON.parse(r.out), status: r.status }; } catch { check('the scan prints JSON', false, r.out + r.err); return { hits: [], status: r.status }; } };
const fb = (extra = {}) => ({ correct: 'Yes.', generic: 'Not quite right.', ...extra });
const num = (a, o = {}) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 }, ...o });
const screen = (o) => ({ type: 'ladder', title: 'A screen', widget: num(1), feedback: fb(), ...o });
const part = (question, o = {}) => ({ question, widget: num(1), feedback: fb(), ...o });
const lesson = (id, screens) => ({ id, screens });
const set = (items) => ({ id: 'problems-1', items });
const kinds = (r, id) => r.hits.filter((h) => h.itemId === id).map((h) => h.kind);
const COURSE = { id: 'c', topic: '9.9', skills: { 'sk-c': 'A skill of c' }, levels: [] };
const run = (files, extra, env) => withTree({ 'courses/c/course.json': COURSE, ...files }, (root) => scan(root, extra, env));

// ---- 1. the exams that hold the course's items ----
withTree({}, (root) => {
  const r = scan(root, ['--all', '--exam-errors']);
  const h = r.hits.filter((x) => x.file === 'courses/arma/problems-9.json');
  check('1 an exam item carrying the course\'s skill is a source: numbers (three shared figures) and matrix hits name the exam file and the item', h.some((x) => x.kind === 'matrix' && x.exam && x.source.startsWith('exams/topic-2.2.json') && x.sourceId === 'e-grid-matrix') && h.some((x) => x.kind === 'numbers' && x.exam && x.sourceId === 'e-three-numbers'), JSON.stringify(h.map((x) => [x.kind, x.source, x.sourceId])));
  check('2 an exam item of another course (its skill is not the course\'s) is not read', !r.hits.some((x) => x.sourceId === 'e-other-course'), JSON.stringify(r.hits.map((x) => x.sourceId)));
  const t = sc(root, ['--all', '--exam-errors']);
  check('3 the error line names the exam file and the exam item id; a set outside the baseline fails (exit 1)', /error {2}courses\/arma\/problems-9\.json .*matrix {2}<- {2}exams\/topic-2\.2\.json:items\[\d+\] \(exam item e-grid-matrix\)/.test(t.out) && t.status === 1, t.out);
  const b = sc(root, ['--all']);   // arma/problems-1 is in tools/reuse-baseline.json: the same hit is a warning there
  check('4 a set listed in tools/reuse-baseline.json gets its exam hits as warnings tagged [exam-reuse]', /\[exam-reuse\] warn {2}courses\/arma\/problems-1\.json/.test(b.out) && !/ error {2}courses\/arma\/problems-1\.json.*<-  exams\//.test(b.out), b.out);
  const o = scan(root, ['--all', '--no-exams']);
  check('5 --no-exams leaves the exams out', !o.hits.some((x) => x.exam), JSON.stringify(o.hits.map((x) => x.source)));
}, true);

// ---- 2. retold: the three false-positive classes ----
const SRC = 'A desk fits a model on 800 trades and scores it on 200. The test block holds the newest trades.';
const rule = 'The score on trades the model has seen flatters it, so only unseen trades tell the truth.';
const prob = (explain, extra = {}, fbx = {}) => set([{ id: 'p-x', prose: 'A broker fits a model on 1,200 orders and scores it on 300.', parts: [part('How many orders does the broker score?', { explain: { text: explain }, feedback: fb(fbx), ...extra })] }]);
{
  // 1: one sentence said three times (correct, generic, explain) against one source sentence
  const src = lesson('l1', [screen({ prose: SRC, question: 'How many trades?', explain: rule })]);
  const said = 'The score on orders the model has seen flatters it, so only unseen orders tell the truth.';
  const r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': prob(said, {}, { correct: said, generic: said }) });
  check('6 retold class 1: one sentence in correct, generic and explain, matched to one source sentence, counts once (no hit)', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  const r2 = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': prob(said, {}, { generic: 'Only the unseen block is scored, and the model never fitted it. The test block holds the newest orders.' }) });
  check('7 control: two different sentences retold from two different source sentences still fire', kinds(r2, 'p-x').includes('retold'), JSON.stringify(r2.hits));
}
{
  // 2: a rule held by three other files of the course in its only words is course stock
  const stock = 'Dividing by a negative number reverses the sign of the inequality.';
  const mk = (n, extra = '') => lesson(`l${n}`, [screen({ prose: 'A tank holds 40 litres and loses 3 a day.', question: 'When is it empty?', explain: `${stock} ${extra}`.trim() })]);
  const p = set([{ id: 'p-x', prose: 'A van loses 2,400 pounds a year.', parts: [part('When is it worth nothing?', { explain: { text: `${stock} The score on orders the model has seen flatters it, so only unseen orders tell the truth.` } })] }]);
  const three = run({ 'courses/c/l1.json': mk(1, rule), 'courses/c/l2.json': mk(2), 'courses/c/l3.json': mk(3), 'courses/c/l4.json': mk(4), 'courses/c/problems-1.json': p });
  const one = run({ 'courses/c/l1.json': mk(1, rule), 'courses/c/problems-1.json': p });
  check('8 retold class 2: a rule said in the same words by three other files of the course is stock (no hit)', !kinds(three, 'p-x').includes('retold'), JSON.stringify(three.hits));
  check('9 control: the same rule said by one other file, with a second retold sentence, is read and fires', kinds(one, 'p-x').includes('retold'), JSON.stringify(one.hits));
}
{
  // 3: a match made by the masking alone
  const src = lesson('l1', [screen({ prose: 'A walk of 12 steps.', question: 'Which walk?', explain: 'That is $h_1$, the chance of ending at 3. That is $h_2$, the chance of ending at 5. That is $h_3$, the chance of ending at 7.' })]);
  const p = set([{ id: 'p-x', prose: 'A path of 9 steps.', parts: [part('Which path?', { explain: { text: 'That is $\\binom{12}{5}$, the paths ending at $-2$. That is $\\binom{9}{4}$, the paths ending at $-1$. That is $\\binom{8}{3}$, the paths ending at $-4$.' } })] }]);
  const r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': p });
  check('10 retold class 3: "That is ..., the ... ending at ..." matched on the skeleton alone (no informative word in common) is no hit', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
}
{
  // the true cases that must not get weaker: identical short slip lines, one number different
  const src = lesson('l1', [screen({ prose: 'A series of 300 closes.', question: 'What is the ratio?', feedback: fb({ byKey: { flip: 'You divided the other way round.', kept: 'You kept $B$ of the gap, not $1 - B$.', band: 'You divided by 680. The band shrinks like $1/\\sqrt n$.', run: 'You added plain distances, $2 + 0 + 2 + 4$.', tops: 'You divided $u\'$ by $v\'$. The derivative of a quotient is not the quotient of the derivatives.' } }) })]);
  const slip = (lines) => set([{ id: 'p-x', prose: 'A different desk with 41 books.', parts: [part('What is the ratio of the books?', { feedback: fb({ byKey: lines }) })] }]);
  let r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ flip: 'You divided the other way round.' }) });
  check('11 an identical slip line with no number ("You divided the other way round.") is stock: no hit (engine pass 8 C)', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ band: 'You divided by 680. The band shrinks like $1/\\sqrt n$.' }) });
  check('11b an identical numbered slip line (the whole feedback is equal) is a hit', kinds(r, 'p-x').includes('retold') && r.status === 1, JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ tops: 'You divided $u\'$ by $v\'$. The derivative of a quotient is not the quotient of the derivatives.' }) });
  check('11c a whole feedback of two sentences with no number, equal word for word, is a hit', kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ kept: 'You kept $A$ of the gap, not $1 - A$.' }) });
  check('12 a slip line that differs in its maths only ("You kept $B$ of the gap, not $1 - B$.", one shared figure) is no hit', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ run: 'You added plain distances, $2 + 0 + 2 + 4 + 0 + 4$.' }) });
  check('12b a numbered slip line that shares a run of two numbers with its source (2 + 0 + 2 + 4) is a hit', kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ run: 'You added plain distances, $3 + 1 + 5 + 7$.' }) });
  check('12c the same line in other numbers is no hit', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ band: 'You divided by 910. The band shrinks like $1/\\sqrt n$.' }) });
  check('13 a slip line that differs in one number ("You divided by 910." against 680) is no hit', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ flip: 'You flipped it.' }) });
  check('14 a slip line of fewer than four words is not read whole (no hit)', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  const files = { 'courses/c/problems-1.json': slip({ band: 'You divided by 680. The band shrinks like $1/\\sqrt n$.' }) };
  for (let i = 1; i <= 8; i++) files[`courses/c/l${i}.json`] = src;
  r = run(files);
  check('15 a slip line held by eight or more files of the content is stock (no hit)', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits.map((h) => h.source)));
  const rulep = set([{ id: 'p-x', prose: 'A tank.', parts: [part('Which theorem?', { explain: { text: 'Use the divergence theorem.' } })] }]);
  r = run({ 'courses/c/l1.json': lesson('l1', [screen({ prose: 'A flux.', question: 'Which theorem?', explain: 'Use the divergence theorem.' })]), 'courses/c/problems-1.json': rulep });
  check('16 a short rule line ("Use the divergence theorem.") is not a slip line and is stock by length (no hit)', !kinds(r, 'p-x').includes('retold'), JSON.stringify(r.hits));
  // a hit that rests on a slip line alone carries the tag, and a set of the baseline gets a warning
  const t = run({ 'courses/c/l1.json': src, 'courses/c/problems-1.json': slip({ band: 'You divided by 680. The band shrinks like $1/\\sqrt n$.' }) });
  check('17 a hit that stands on an identical slip line alone is tagged "slip-line"', t.hits.some((h) => h.itemId === 'p-x' && h.tag === 'slip-line'), JSON.stringify(t.hits));
}

// ---- 3. --pairs ----
{
  const src = lesson('l1', [screen({ prose: 'A series.', question: 'What is the ratio?', feedback: fb({ byKey: { flip: 'You divided by 680. The band shrinks like $1/\\sqrt n$.', kept: 'You kept 15 of the 40 points, not 25.' } }) })]);
  const p = set([{ id: 'p-x', prose: 'Books.', parts: [part('What is the ratio?', { feedback: fb({ byKey: { flip: 'You divided by 680. The band shrinks like $1/\\sqrt n$.', kept: 'You kept 15 of the 40 points, not 25.' } }) })] }]);
  withTree({ 'courses/c/course.json': COURSE, 'courses/c/l1.json': src, 'courses/c/problems-1.json': p }, (root) => {
    const a = sc(root, ['--all']), b = sc(root, ['--all', '--pairs']);
    check('18 --pairs prints every matched pair of a hit (two lines, both texts); without it none', (b.out.match(/ {6}pair: /g) ?? []).length >= 2 && /pair: "You divided by 680\. The band shrinks like \$1\/\\sqrt n\$\."  <-  "You divided by 680/.test(b.out) && /pair: "You kept 15 of the 40 points/.test(b.out) && !/pair: /.test(a.out), b.out);
    const f = spawnSync('node', [FC, '--content', root, '--file', join(root, 'courses/c/problems-1.json'), '--pairs'], { encoding: 'utf8' });
    check('19 fresh-check.mjs --file --pairs prints the pairs too', /pair: "You kept 15 of the 40 points/.test(f.stdout), f.stdout + f.stderr);
    const j = scan(root);
    check('20 --json carries the pairs', j.hits.some((h) => (h.pairs ?? []).length >= 2), JSON.stringify(j.hits));
    const f2 = spawnSync('node', [FC, '--content', root, '--files', `${join(root, 'courses/c/problems-1.json')},${join(root, 'courses/c/l1.json')}`], { encoding: 'utf8' });
    check('21 fresh-check.mjs --files a,b checks both files in one run (the target count says 2)', /in 2 target file\(s\)/.test(f2.stdout), f2.stdout + f2.stderr);
  });
}

// ---- 4. waivers with a source ----
{
  const LN = 'You divided by 680. The band shrinks like $1/\\sqrt n$.';
  const mk = (id, line) => lesson(id, [screen({ prose: 'A series.', question: 'What is the ratio?', feedback: fb({ byKey: { flip: line } }) })]);
  const p = set([{ id: 'p-x', prose: 'Books.', parts: [part('What is the ratio?', { feedback: fb({ byKey: { flip: LN } }) })] }]);
  const files = { 'courses/c/course.json': COURSE, 'courses/c/l1.json': mk('l1', LN), 'courses/c/l2.json': mk('l2', LN), 'courses/c/problems-1.json': p };
  withTree(files, (root) => {
    const w = (extra) => { const f = join(root, 'w.json'); writeFileSync(f, JSON.stringify([{ file: 'courses/c/problems-1.json', item: 'p-x', kind: 'retold', reason: 'stands: test', ...extra }])); return { ZQ_WAIVERS: f }; };
    const waivedSources = (env) => scan(root, ['--all'], env).hits.filter((h) => h.waived).map((h) => h.source.split(':')[0]).sort();
    check('22 a waiver with no source clears every retold hit of its item (as today)', waivedSources(w({})).length === 2, JSON.stringify(waivedSources(w({}))));
    check('23 a waiver with a source (file) clears only the hit from that source', JSON.stringify(waivedSources(w({ source: 'courses/c/l1.json' }))) === '["courses/c/l1.json"]', JSON.stringify(waivedSources(w({ source: 'courses/c/l1.json' }))));
    check('24 a source list clears the hits of each file named', waivedSources(w({ source: ['courses/c/l1.json', 'courses/c/l2.json'] })).length === 2);
    check('25 a source with a text clears only a hit whose pair holds the text', waivedSources(w({ source: { file: 'courses/c/l1.json', text: 'band shrinks' } })).length === 1 && waivedSources(w({ source: { file: 'courses/c/l1.json', text: 'not in any pair' } })).length === 0);
    check('25b a top-level text (no source) clears only hits whose pair holds that phrase, against any source', waivedSources(w({ text: 'band shrinks' })).length === 2 && waivedSources(w({ text: 'not in any pair' })).length === 0 && waivedSources(w({ text: 'BAND SHRINKS', source: 'courses/c/l2.json' })).length === 1);
    check('26 the unwaived hit still fails the run (exit 1)', scan(root, ['--all'], w({ source: 'courses/c/l1.json' })).status === 1);
  });
  const real = JSON.parse(readFileSync(join(HERE, 'same-course-waivers.json'), 'utf8'));
  check('27 tools/same-course-waivers.json: the 41 waivers all stand and 40 name a source', real.length === 41 && real.filter((x) => x.source).length === 40 && real.every((x) => /^stands/.test(x.reason)), `${real.length} ${real.filter((x) => x.source).length}`);
}

// ---- 5. rate exemptions ----
{
  const les = (t) => lesson('l1', [screen({ prose: t, question: 'Value?', explain: 'It is the stated share.' })]);
  const go = (a, b) => run({ 'courses/c/l1.json': les(a), 'courses/c/problems-1.json': set([{ id: 'p-rate', prose: b, parts: [part('Value?')] }]) });
  let r = go('Out of 120 calls, 50 paid, a base rate of 41.7%. The threshold is 0.6.', 'Of 12 calls, 5 paid, so the base rate is 5/12 = 0.4167. The threshold is 0.6.');
  check('28 control: 5/12 = 0.4167 against 41.7% with 0.6 in both fires', kinds(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('Three eighths of the claims, 37.5%, were paid late. The threshold is 0.6.', 'Of the orders 3/8 = 0.375 are late. The threshold is 0.6.');
  check('29 the eighths (3/8, 0.375, 37.5%) are exempt from rate', !kinds(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The cost is 0.0625w and the base rate 6.25%. The threshold is 0.6.', 'The slope is $-0.01 + 0.0625w$ and the threshold is 0.6.');
  check('30 a decimal that multiplies a variable (0.0625w) is not a rate', !kinds(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The base rate is 6.25% and the threshold 0.6.', 'The share is 0.0625 and the threshold is 0.6.');
  check('31 control: 0.0625 against 6.25% with 0.6 in both fires', kinds(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
}

// ---- 6. standard quantiles are stock in the shared-parameter advisory of fresh-check ----
{
  const les = (t) => lesson('l1', [screen({ prose: t, question: 'Value?', explain: 'A stated value.' })]);
  const tree = (a, b) => ({ 'courses/c/course.json': COURSE, 'courses/c/l1.json': les(a), 'courses/c/problems-1.json': set([{ id: 'p-q', prose: b, parts: [part('Value?')] }]) });
  const adv = (a, b) => withTree(tree(a, b), (root) => spawnSync('node', [FC, '--content', root, '--file', join(root, 'courses/c/problems-1.json'), '--no-same-course'], { encoding: 'utf8' }).stdout);
  const o1 = adv('The 99% value uses 2.3263 and the 95% value 1.6449.', 'At 99% take 2.3263; at 90% take 1.6449 and at 99.5% take 2.5758.');
  check('32 standard quantiles with their levels (2.3263 with 99, 1.6449 with 90) are not shared parameters', !/shared parameters/.test(o1), o1);
  const o2 = adv('The fitted slope is 0.314 and the intercept 0.271.', 'A line has slope 0.314 and intercept 0.271.');
  check('33 control: two shared fitted values (0.314, 0.271) are still listed', /shared parameters/.test(o2), o2);
}
console.log(fails ? `${fails} check(s) failed` : 'all checks passed');
process.exit(fails ? 1 : 0);
