#!/usr/bin/env node
// Test for engine pass 7 remainder, package 3 (reuse checkers): ENGINE-BACKLOG 1062 (a taught formula is no copied setup), 1088 (ratio of two stated amounts), 1106 (chain across sources and model answers),
// 1128 (story in its own nouns), 1153 ("x over n years" givens), and --all-exams (a problem set against every exam, warnings only). Trees are built in the test; the word frequencies are the snapshot tools/retold-model.json.
// Run from app/: node tools/test-fresh-check-pkg3.mjs
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const SC = join(HERE, 'same-course-reuse.mjs'), FC = join(HERE, 'fresh-check.mjs');
let fails = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `  ${String(detail).slice(0, 900)}`}`); if (!ok) fails++; };
const put = (root, rel, o) => { const p = join(root, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, typeof o === 'string' ? o : JSON.stringify(o)); };
const withTree = (files, f) => { const tmp = mkdtempSync(join(tmpdir(), 'zq-pkg3-')); try { for (const [rel, o] of Object.entries(files)) put(tmp, rel, o); return f(tmp); } finally { rmSync(tmp, { recursive: true, force: true }); } };
const sc = (root, extra = ['--all']) => { const r = spawnSync('node', [SC, '--content', root, ...extra], { encoding: 'utf8' }); return { out: r.stdout, err: r.stderr, status: r.status }; };
const scan = (root, extra = ['--all']) => { const r = sc(root, [...extra, '--json']); try { return { hits: JSON.parse(r.out), status: r.status }; } catch { check('the scan prints JSON', false, r.out + r.err); return { hits: [], status: r.status }; } };
const fc = (root, file, extra = []) => { const r = spawnSync('node', [FC, '--content', root, '--file', join(root, file), ...extra], { encoding: 'utf8' }); return { out: r.stdout + r.stderr, status: r.status }; };
const fb = (extra = {}) => ({ correct: 'Yes.', generic: 'Not quite right.', ...extra });
const num = (a, o = {}) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 }, ...o });
const screen = (o) => ({ type: 'ladder', title: 'A screen', widget: num(1), feedback: fb(), ...o });
const part = (question, o = {}) => ({ question, widget: num(1), feedback: fb(), ...o });
const lesson = (id, screens) => ({ id, screens });
const set = (items) => ({ id: 'problems-1', items });
const COURSE = { id: 'c', topic: '9.9', skills: { 'sk-c': 'A skill of c', 'sk-d': 'Another skill of c' }, levels: [] };
const run = (files, extra) => withTree({ 'courses/c/course.json': COURSE, ...files }, (root) => scan(root, extra));
const kinds = (r, id) => r.hits.filter((h) => h.itemId === id).map((h) => h.kind);

// ---- 1062: a formula that a lesson screen teaches is not a copied setup ----
{
  const F = 'p = \\dfrac{1}{1 + e^{-0.35 x}}';
  const taught = lesson('l1', [screen({ prose: 'Squash a score into a probability.', formula: { name: 'Logistic', tex: F } })]);
  const shows = lesson('l2', [screen({ prose: `A first desk turns a score into a chance with $${F}$ in its own way.` })]);
  const prob = set([{ id: 'p-a', prose: `A desk turns a score into a chance with $${F}$ for a wider book.`, widget: num(2), feedback: fb() }]);
  withTree({ 'courses/c/course.json': COURSE, 'courses/c/l2.json': shows, 'courses/c/problems-1.json': prob }, (root) => {
    const r = fc(root, 'courses/c/problems-1.json', ['--no-same-course']);
    check('1062 control: a formula shared with a lesson screen that does not teach it (no formula.tex) is still listed as advisory', /shared formula/.test(r.out), r.out);
  });
  withTree({ 'courses/c/course.json': COURSE, 'courses/c/l1.json': taught, 'courses/c/l2.json': shows, 'courses/c/problems-1.json': prob }, (root) => {
    const r = fc(root, 'courses/c/problems-1.json', ['--no-same-course']);
    check('1062 a formula the course teaches in a screen formula.tex is not listed, though another screen shows it too', !/shared formula/.test(r.out), r.out);
  });
}

// ---- 1088: the ratio of two stated amounts ----
{
  const les = (t) => lesson('l1', [screen({ prose: t, question: 'What is the gain?' })]);
  const prob = (t) => set([{ id: 'p-r', prose: t, widget: num(2), feedback: fb() }]);
  const go = (a, b) => run({ 'courses/c/l1.json': les(a), 'courses/c/problems-1.json': prob(b) });
  const r = go('A dealer buys a coin for 640 and sells it for 1,000.', 'A fund grows from 32,000 to 50,000 over its first year.');
  const h = r.hits.find((x) => x.itemId === 'p-r' && x.kind === 'ratio');
  check('1088 640 to 1,000 and 32,000 to 50,000 share the ratio 1.5625: a ratio warning (never an error, exit 0), tag ratio', !!h && h.level === 'warn' && h.tag === 'ratio' && r.status === 0 && /1\.5625/.test(h.evidence), JSON.stringify(r.hits));
  check('1088 control: a simple ratio (20 to 30 against 40 to 60) is no hit', !kinds(go('A dealer buys a coin for 20 and sells it for 30.', 'A fund grows from 40 to 60 over its first year.'), 'p-r').includes('ratio'));
  check('1088 control: a ratio near 1 (61.9 to 62.4 against 49.5 to 49.9) is no hit', !kinds(go('A stock opens at 61.9 and closes at 62.4.', 'A stock opens at 49.5 and closes at 49.9.'), 'p-r').includes('ratio'));
  check('1088 control: two different ratios are no hit', !kinds(go('A dealer buys a coin for 640 and sells it for 1,000.', 'A fund grows from 32,000 to 51,000 over its first year.'), 'p-r').includes('ratio'));
}

// ---- 1153: "x over n years" of one skill, problem against exam item ----
{
  const exam = (t, skills = ['sk-c']) => ({ id: 'topic-9.9', topic: '9.9', items: [{ id: 'e-sharpe', skills, prose: t, widget: num(1), feedback: fb() }] });
  const prob = (t, skills = ['sk-c']) => set([{ id: 'p-g', skills, prose: t, widget: num(2), feedback: fb() }]);
  const go = (e, p) => run({ 'exams/topic-9.9.json': e, 'courses/c/problems-1.json': p });
  const r = go(exam('A fund has a Sharpe ratio of 0.6 over 9 years of monthly data.'), prob('Fund managers claim a Sharpe ratio of 0.9 over 9 years.'));
  const h = r.hits.find((x) => x.itemId === 'p-g' && x.kind === 'xparam');
  check('1153 "0.6 over 9 years" against "0.9 over 9 years" of one skill: an xparam warning naming the exam item (exit 0)', !!h && h.level === 'warn' && h.tag === 'xparam' && h.exam && h.sourceId === 'e-sharpe' && r.status === 0, JSON.stringify(r.hits));
  check('1153 control: another number of years is no hit', !kinds(go(exam('A fund has a Sharpe ratio of 0.6 over 8 years of monthly data.'), prob('Fund managers claim a Sharpe ratio of 0.9 over 9 years.')), 'p-g').includes('xparam'));
  check('1153 control: a short span (3 years) is no hit', !kinds(go(exam('A fund has a Sharpe ratio of 0.6 over 3 years of monthly data.'), prob('Fund managers claim a Sharpe ratio of 0.9 over 3 years.')), 'p-g').includes('xparam'));
  check('1153 control: items of two skills are no hit', !kinds(go(exam('A fund has a Sharpe ratio of 0.6 over 9 years of monthly data.'), prob('Fund managers claim a Sharpe ratio of 0.9 over 9 years.', ['sk-d'])), 'p-g').includes('xparam'));
}

// ---- 1106: a chain across sources, and the model answer of a longform item ----
{
  const steps = [['What is the standard error of the best rule\'s Sharpe ratio over 3 years?', 'The standard error of a yearly Sharpe ratio is one over the square root of the years. It uses only the years of data.'], ['How many standard errors above zero is the best rule?', 'Divide the Sharpe ratio by its standard error. The best of many tries always looks better than a single try.'], ['What Sharpe ratio would the best of the tries show by luck alone?', 'Searching adds a haircut for the number of tries. The expected maximum of many noise tries sits well above zero.'], ['After the haircut what Sharpe ratio is left?', 'Subtract the haircut from the observed Sharpe ratio. What is left is the edge that survives the search.']];
  const scr = (a) => a.map(([q, e]) => screen({ title: 'Step', prose: 'A researcher keeps the best of 40 rules.', question: q, explain: e }));
  const swapped = [['Over 4 years, how large is the standard error of the best blend\'s Sharpe ratio?', 'With yearly data the standard error of the Sharpe ratio is one over the root of the number of years.'], ['By how many standard errors does the best blend clear zero?', 'Take the Sharpe ratio over its standard error. A best pick among many tries beats one try by chance.'], ['Which Sharpe ratio would the best blend reach by luck alone?', 'A search needs a haircut for its tries. The largest of many noise tries lies far above zero.'], ['What Sharpe ratio is left once the haircut is taken?', 'Take the haircut off the observed Sharpe ratio. The remainder is the edge that survives the search.']];
  const p = set([{ id: 'p-u', prose: 'A desk keeps the best of 60 blends.', parts: swapped.map(([q, e]) => part(q, { explain: { text: e } })) }]);
  const split = run({ 'courses/c/l1.json': lesson('l1', scr(steps.slice(0, 2))), 'courses/c/l2.json': lesson('l2', scr(steps.slice(2))), 'courses/c/problems-1.json': p });
  const h = split.hits.find((x) => x.itemId === 'p-u' && x.kind === 'chain-union');
  check('1106 four parts that follow screens of two lessons (two steps each) fire chain-union, a warning (exit 0 for this kind)', !!h && h.level === 'warn' && h.tag === 'chain-union' && /different sources/.test(h.evidence), JSON.stringify(split.hits));
  const one = run({ 'courses/c/l1.json': lesson('l1', scr(steps)), 'courses/c/problems-1.json': p });
  check('1106 control: all four steps in one lesson are the old chain error, no chain-union', kinds(one, 'p-u').includes('retold') && !kinds(one, 'p-u').includes('chain-union'), JSON.stringify(one.hits));
  const lone = run({ 'courses/c/l1.json': lesson('l1', scr(steps.slice(0, 2))), 'courses/c/problems-1.json': p });
  check('1106 control: only two parts matched is no chain-union', !kinds(lone, 'p-u').includes('chain-union'), JSON.stringify(lone.hits));
  // the model answer of a longform item is read by the sentence test, as a warning tagged model
  const model = 'The test block holds the newest trades. A score on trades the model has seen flatters it. Only the unseen trades tell you how it will do.';
  const same = 'The test block holds the newest orders. A score on orders the model has seen flatters it. Only the unseen orders tell you how it will do.';
  const prob = set([{ id: 'p-m', prose: 'A broker fits a model on 1,200 orders and scores it on 300.', parts: [part('How many orders does the broker score?', { explain: { text: same } })] }]);
  const hw = { id: 'homework-1', items: [{ id: 'h1-long', kind: 'longform', prompt: 'Explain why a score on seen trades flatters a model.', model, rubric: ['a'], feedback: fb() }] };
  const m = run({ 'courses/c/homework-1.json': hw, 'courses/c/problems-1.json': prob });
  const hm = m.hits.find((x) => x.itemId === 'p-m' && x.kind === 'retold');
  check('1106 a problem that retells a homework model answer sentence by sentence gets a retold warning tagged model (exit 0)', !!hm && hm.level === 'warn' && hm.tag === 'model' && m.status === 0, JSON.stringify(m.hits));
  const ex = run({ 'courses/c/l1.json': lesson('l1', [screen({ prose: 'A desk fits a model on 800 trades.', question: 'How many?', explain: model })]), 'courses/c/problems-1.json': prob });
  check('1106 control: the same sentences in a lesson explain stay a retold error', ex.hits.some((x) => x.itemId === 'p-m' && x.kind === 'retold' && x.level === 'error'), JSON.stringify(ex.hits));
}

// ---- 1128: a story told in its own nouns with the same question ----
{
  const les = (t, q) => lesson('l1', [screen({ prose: t, question: q })]);
  const prob = (t, q) => set([{ id: 'p-s', prose: t, question: q, widget: num(2), feedback: fb() }]);
  const Q = 'How many trades does the desk score on average before the model fails?';
  const go = (a, qa, b, qb) => run({ 'courses/c/l1.json': les(a, qa), 'courses/c/problems-1.json': prob(b, qb) });
  const A = 'An economist at a dinner in a drought district reads an editorial on the dilution of a fund.', B = 'At a dinner, an economist from a district in drought reads an editorial about dilution.';
  const r = go(A, Q, B, 'How many orders does the desk score on average before the model fails?');
  const h = r.hits.find((x) => x.itemId === 'p-s' && x.kind === 'story');
  check('1128 six particular words in common and one question skeleton: a story warning (exit 0), tag story', !!h && h.level === 'warn' && h.tag === 'story' && r.status === 0, JSON.stringify(r.hits));
  check('1128 control: the same nouns with another question is no hit', !kinds(go(A, Q, B, 'Why does the editorial blame the dilution so sharply?'), 'p-s').includes('story'));
  check('1128 control: the same question with other nouns is no hit', !kinds(go(A, Q, 'A baker in a harbour town counts loaves for a wedding.', 'How many orders does the desk score on average before the model fails?'), 'p-s').includes('story'));
}

// ---- 1121: a question that holds a source question whole, with a phrase added ----
{
  const les = lesson('l1', [screen({ prose: 'An economist at a dinner in a drought district reads an editorial.', question: 'How many trades does the desk score on average before the model fails?' })]);
  const prob = (q, t = 'At a dinner, an economist from a district in drought reads an editorial.') => set([{ id: 'p-q', prose: t, question: q, widget: num(2), feedback: fb() }]);
  const r = run({ 'courses/c/l1.json': les, 'courses/c/problems-1.json': prob('How many trades does the desk score on average before the model fails, with the same budget?') });
  const h = r.hits.find((x) => x.itemId === 'p-q' && x.kind === 'question');
  check('1121 one phrase added to a source question: a question warning (exit 0), tag question', !!h && h.level === 'warn' && h.tag === 'question' && r.status === 0, JSON.stringify(r.hits));
  check('1121 control: a different question on the same story is no hit', !kinds(run({ 'courses/c/l1.json': les, 'courses/c/problems-1.json': prob('Which of the two ways leaves the bank with the smaller standard error after many runs?') }), 'p-q').includes('question'));
  check('1121 control: the same stock question in another story (no two particular words in common) is no hit', !kinds(run({ 'courses/c/l1.json': les, 'courses/c/problems-1.json': prob('How many trades does the desk score on average before the model fails, with the same budget?', 'A baker in a harbour town counts loaves.') }), 'p-q').includes('question'));
}

// ---- --all-exams: a problem set against every exam and mock, warnings only ----
{
  const mock = { id: 'mock-9', items: [{ id: 'm-top', skills: ['sk-other'], prose: 'A bag holds 1234.5 grams, then 6789.1 grams and 4321.7 grams of salt.', widget: num(1), feedback: fb() }], parts: [{ title: 'Part B', items: [{ id: 'm-nested', skills: ['sk-other'], prose: 'A tank holds 2468.3 litres, then 1357.9 litres and 8642.1 litres.', widget: num(1), feedback: fb() }] }] };
  const prob = set([{ id: 'p-a', prose: 'A sack holds 1234.5 kilos, then 6789.1 kilos and 4321.7 kilos of grain.', widget: num(2), feedback: fb() }, { id: 'p-b', prose: 'A drum holds 2468.3 litres, then 1357.9 litres and 8642.1 litres of oil.', widget: num(2), feedback: fb() }]);
  withTree({ 'courses/c/course.json': COURSE, 'exams/mock-9.json': mock, 'courses/c/problems-1.json': prob }, (root) => {
    const d = scan(root);
    check('--all-exams off: an exam item that carries no skill of the course is not read', !d.hits.length, JSON.stringify(d.hits));
    const a = scan(root, ['--all', '--all-exams']);
    const hs = a.hits.filter((x) => x.allExams);
    check('--all-exams: a top-level exam item and a mock item in parts[].items are read, as warnings tagged all-exams, never failing (exit 0)', hs.some((x) => x.itemId === 'p-a' && x.sourceId === 'm-top') && hs.some((x) => x.itemId === 'p-b' && x.sourceId === 'm-nested') && hs.every((x) => x.level === 'warn' && x.tag === 'all-exams') && a.status === 0, JSON.stringify(a.hits));
    const t = sc(root, ['--all', '--all-exams']);
    check('--all-exams prints a count line that says it is not gated', /--all-exams: 2 warning\(s\).*not gated/.test(t.out), t.out);
    const f = fc(root, 'courses/c/problems-1.json', ['--all-exams']);
    check('fresh-check --file --all-exams passes the flag on (the lines are tagged [all-exams])', /\[all-exams\] warn/.test(f.out), f.out);
  });
}

if (process.argv[1].endsWith('test-fresh-check-pkg3.mjs')) { console.log(fails ? `${fails} FAILED` : 'all passed'); process.exitCode = fails ? 1 : 0; }
