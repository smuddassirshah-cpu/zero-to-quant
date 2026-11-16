#!/usr/bin/env node
// Test for the retold-screen and rate-form kinds of tools/same-course-reuse.mjs and tools/retold-reuse.mjs (engine pass AF part 1, ENGINE-BACKLOG 1075, 1076, 1078, 1080).
// True positives: the pre-fix text of the reuse findings of docs/reviews/review-problems-ensembles-1-3, -fin-ml-1-3, -validation-1-3, review-delta-ae-2, -ae-3 and -ae-4, rebuilt from git
// (tools/fixtures/retold-af/sets: each problem set as it stood when the reader read it; tools/fixtures/retold-af/src: the lessons, reviews and homework it was held against, canvases and code left out,
// see fixtures/retold-af/README.md). Each set is scanned in a temporary course next to its sources. Negatives: stock lines, the level's standard task in new numbers, the four fin-ml likenesses
// the readers ruled clean, rates with no shared second number or in one form only.
// The word frequencies and stock sentences are the snapshot tools/retold-model.json (learned over the whole content: `node tools/same-course-reuse.mjs --learn`), so the test does not move with the content.
// Run from app/: node tools/test-fresh-check-retold-af.mjs   (about thirty seconds)
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, readdirSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = dirname(fileURLToPath(import.meta.url));
const SC = join(HERE, 'same-course-reuse.mjs'), FC = join(HERE, 'fresh-check.mjs');
const FIX = join(HERE, 'fixtures', 'retold-af');
let fails = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : `  ${String(detail).slice(0, 700)}`}`); if (!ok) fails++; };
const put = (root, rel, o) => { const p = join(root, rel); mkdirSync(dirname(p), { recursive: true }); writeFileSync(p, JSON.stringify(o)); };
const scan = (root, extra = ['--all'], noWaivers = true) => { const r = spawnSync('node', [SC, '--content', root, ...extra, '--json', ...(noWaivers ? ['--no-waivers'] : [])], { encoding: 'utf8' }); try { return { hits: JSON.parse(r.stdout), status: r.status }; } catch { check('the scan prints JSON', false, r.stdout + r.stderr); return { hits: [], status: r.status }; } };
const withTree = (files, f) => { const tmp = mkdtempSync(join(tmpdir(), 'zq-af-')); try { for (const [rel, o] of Object.entries(files)) put(tmp, rel, o); return f(tmp); } finally { rmSync(tmp, { recursive: true, force: true }); } };

// ---- the review findings: a set as the reader saw it, next to its sources ----
const cache = new Map();
const setHits = (name) => {
  if (cache.has(name)) return cache.get(name);
  const set = JSON.parse(readFileSync(join(FIX, 'sets', `${name}.json`), 'utf8')), { course, as, ...doc } = set;
  const files = { [`courses/${course}/${as}.json`]: doc };
  for (const f of readdirSync(join(FIX, 'src', course))) files[`courses/${course}/${f}`] = JSON.parse(readFileSync(join(FIX, 'src', course, f), 'utf8'));
  const r = withTree(files, (root) => scan(root));
  r.hits = r.hits.filter((h) => h.file === `courses/${course}/${as}.json`);
  cache.set(name, r);
  return r;
};
const fires = (name, id, kind, src) => setHits(name).hits.some((h) => h.itemId === id && h.kind === kind && (!src || src.test(h.source)));
const show = (name, id) => JSON.stringify(setHits(name).hits.filter((h) => !id || h.itemId === id).map((h) => `${h.itemId} ${h.kind} ${h.source} ${h.evidence}`));

// kind (a): feedback, explain and why are read; kind (b): a retold sentence skeleton
check('1 ensembles review finding 3: the feedback lines of p-bond-downgrades repeat homework-2 item 1 ("We need every tree to have drawn it")', fires('ensembles-p2-first', 'p-bond-downgrades', 'retold', /ensembles\/homework-2/), show('ensembles-p2-first'));
check('2 validation review finding 5: p-arrears-grid retells the l4 model card (the options and their why lines)', fires('validation-p1-first', 'p-arrears-grid', 'retold', /validation\/l4-nested/), show('validation-p1-first'));
check('3 validation review finding 8: p-forward-label asks l7\'s two purging questions in l7\'s words', fires('validation-p2-first', 'p-forward-label', 'retold', /validation\/l7-purging/), show('validation-p2-first'));
check('4 validation review finding 8 (part 3): the same problem against homework-2 "Take a block in the middle"', fires('validation-p2-first', 'p-forward-label', 'retold', /validation\/homework-2/), show('validation-p2-first'));
check('5 validation review finding 14: p-closed-funds repeats l11\'s generic line word for word', fires('validation-p3-first', 'p-closed-funds', 'retold', /validation\/l11-dead-companies/), show('validation-p3-first'));
check('6 validation review finding 13: p-fund-flows keeps l10\'s slip lines', fires('validation-p3-first', 'p-fund-flows', 'retold', /validation\/l10-scaling/), show('validation-p3-first'));
check('7 delta AE-2 finding 3: p-power-spread-cap walks l9 screens 3 and 4 with other numbers (the retold task and its lines)', fires('finml-p3-ae2', 'p-power-spread-cap', 'retold', /fin-ml\/(l9-probability|review-3)/), show('finml-p3-ae2'));
check('8 delta AE-4 finding 1: p-futures-study part 1 is l12 screen 3 sentence for sentence (460 and gap=2 for 730 and gap=1)', fires('ensembles-p3-ae4', 'p-futures-study', 'retold', /ensembles\/l12-trees-on-returns/), show('ensembles-p3-ae4'));
check('9 delta AE-2: the same finding stood in the state the AE-2 reader read', fires('ensembles-p3-ae2', 'p-futures-study', 'retold', /ensembles\/l12-trees-on-returns/), show('ensembles-p3-ae2'));
// kind (c): rate form
check('10 fin-ml review finding 1: base rate 5/12 = 0.4167 with threshold 0.6 against review-1 "50/120 = 41.7%" and "threshold 0.6"', fires('finml-p1-first', 'p-copper-breakout', 'rate', /fin-ml\/review-1/), show('finml-p1-first'));
check('every new hit is an error (exit code 1) and the scan of a set with one exits non-zero', setHits('finml-p1-first').hits.filter((h) => ['retold', 'rate'].includes(h.kind)).every((h) => h.level === 'error') && setHits('finml-p1-first').status === 1);

// ---- negatives: what the readers ruled clean, stock lines, the standard task ----
const quiet = (name, ids, why) => { const h = setHits(name).hits.filter((x) => ids.includes(x.itemId) && ['retold', 'rate'].includes(x.kind)); check(`no hit: ${why}`, h.length === 0, show(name)); };
quiet('finml-p3-first', ['p-five-day-sizing', 'p-trial-log-dsr', 'p-bond-sign-model', 'p-index-fund-day', 'p-q3-earnings-join'], 'the four fin-ml likenesses the reader ruled clean (the level\'s standard task with its own numbers: frame of homework-3 item 3, the log device of review-3 item 7, average uniqueness 0.1, h = 4)');
quiet('finml-p1-first', ['p-silver-windows', 'p-index-fund-day', 'p-bond-sign-model'], 'the other problems of fin-ml problems-1 (their sentences meet no source in more than one stock line)');
quiet('validation-p3-ae4', ['p-fund-encoding'], 'p-fund-encoding of validation problems-3');
quiet('ensembles-p2-ae4', ['p-bond-downgrades'], 'p-bond-downgrades after the AE-2 fix pass re-wrote its feedback lines');

// ---- synthetic cases ----
const fb = (extra = {}) => ({ correct: 'Yes.', generic: 'Not quite right.', ...extra });
const num = (a, o = {}) => ({ kind: 'numeric', answer: a, tol: { abs: 0.001 }, ...o });
const screen = (o) => ({ type: 'ladder', title: 'A screen', widget: num(1), feedback: fb(), ...o });
const part = (question, o = {}) => ({ question, widget: num(1), feedback: fb(), ...o });
const set = (items) => ({ id: 'problems-1', items });
const run = (files) => withTree(files, (root) => scan(root));
const kindsOf = (r, id) => r.hits.filter((h) => h.itemId === id).map((h) => h.kind);

{
  // retold: a lesson's explanation and slip lines told again with other nouns and numbers
  const lesson = { id: 'l1', screens: [screen({ prose: 'A desk fits a model on 800 trades and scores it on 200.', question: 'How many trades does the desk score?', explain: 'The test block holds the newest trades. A score on trades the model has seen flatters it. Only the unseen trades tell you how it will do.', feedback: fb({ byKey: { seen: 'That score is on trades the model has already seen. It flatters the model, so use the unseen ones.', total: 'You counted every trade. Only the newest block is scored, and the model never saw it.' } }) })] };
  const same = 'The test block holds the newest orders. A score on orders the model has seen flatters it. Only the unseen orders tell you how it will do.';
  const p = (lines, explain = same) => set([{ id: 'p-retold', prose: 'A broker fits a model on 1,200 orders and scores it on 300.', parts: [part('How many orders does the broker score?', { feedback: fb({ byKey: lines }), explain: { text: explain } })] }]);
  let r = run({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': p({ seen: 'That score is on orders the model has already seen. It flatters the model, so use the unseen ones.', total: 'You counted every order. Only the newest block is scored, and the model never saw it.' }) });
  check('11 retold: the explanation and the two slip lines of a lesson with trades turned into orders fire', kindsOf(r, 'p-retold').includes('retold') && r.status === 1, JSON.stringify(r.hits));
  r = run({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': p({ seen: 'You scored on the training orders. They are the ones the model fitted, so the score is too kind.', total: 'You divided by all 1,500 orders. The score uses only the 300 held back.' }, '300 orders were held back. Fitting used the other 1,200, and the score counts only the held-back ones.') });
  check('12 the same setting with the explanation re-worded and its own slip lines is silent', !kindsOf(r, 'p-retold').length, JSON.stringify(r.hits));
}
{
  // chain: four steps of a lesson in order, with other nouns and numbers
  const steps = [['What is the standard error of the best rule\'s Sharpe ratio over 3 years?', 'The standard error of a yearly Sharpe ratio is one over the square root of the years. It uses only the years of data.'], ['How many standard errors above zero is the best rule?', 'Divide the Sharpe ratio by its standard error. The best of many tries always looks better than a single try.'], ['What Sharpe ratio would the best of the tries show by luck alone?', 'Searching adds a haircut for the number of tries. The expected maximum of many noise tries sits well above zero.'], ['After the haircut what Sharpe ratio is left?', 'Subtract the haircut from the observed Sharpe ratio. What is left is the edge that survives the search.']];
  const lesson = { id: 'l1', screens: steps.map(([q, e]) => screen({ title: 'Step', prose: 'A researcher keeps the best of 40 rules.', question: q, explain: e })) };
  const swapped = [['Over 4 years, how large is the standard error of the best blend\'s Sharpe ratio?', 'With yearly data the standard error of the Sharpe ratio is one over the root of the number of years.'], ['By how many standard errors does the best blend clear zero?', 'Take the Sharpe ratio over its standard error. A best pick among many tries beats one try by chance.'], ['Which Sharpe ratio would the best blend reach by luck alone?', 'A search needs a haircut for its tries. The largest of many noise tries lies far above zero.'], ['What Sharpe ratio is left once the haircut is taken?', 'Take the haircut off the observed Sharpe ratio. The remainder is the edge that survives the search.']];
  const r = run({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': set([{ id: 'p-chain', prose: 'A desk keeps the best of 60 blends.', parts: swapped.map(([q, e]) => part(q, { explain: { text: e } })) }]) });
  check('13 chain: four parts that follow a lesson\'s four screens step for step in other words, nouns and numbers fire', r.hits.some((h) => h.itemId === 'p-chain' && h.kind === 'retold' && /^chain of [34] steps/.test(h.evidence)), JSON.stringify(r.hits));
  const other = [['How many days of data does the rule need before its Sharpe ratio can be trusted?', 'A rule needs about four years of daily data before one standard error falls under a quarter.'], ['What does a second rule with the same signal add to the portfolio?', 'Two rules on the same signal add nothing. Their returns move together, so the book is no safer.'], ['What turnover does the rule cost the desk each month?', 'Costs scale with turnover. A rule that trades every day pays the spread many times over.'], ['What capital should the desk give the rule?', 'Capital follows the edge after costs. A small edge deserves a small stake.']];
  const r2 = run({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': set([{ id: 'p-other', prose: 'A desk runs a daily rule on one signal.', parts: other.map(([q, e]) => part(q, { explain: { text: e } })) }]) });
  check('14 four parts on the same topic with other steps are silent', !kindsOf(r2, 'p-other').length, JSON.stringify(r2.hits));
}
{
  // (c) a per cent meets a fraction in the key-pair comparison
  const r = run({ 'courses/c/l1.json': { id: 'l1', screens: [screen({ prose: 'Of the claims, 41.7% were paid late and the rest, 58.3%, on time.', question: 'What share was paid on time?', widget: num(0.583) })] },
    'courses/c/problems-1.json': set([{ id: 'p-pct', prose: 'A set of claims.', parts: [part('Late share?', { widget: num(0.417) }), part('On-time share?', { widget: num(0.583) })] }]) });
  check('15 per cents are read as fractions: part keys 0.417 and 0.583 meet "41.7% ... 58.3%" in one sentence (pair)', kindsOf(r, 'p-pct').includes('pair'), JSON.stringify(r.hits));
}
{
  // rate form, and what it must not fire on
  const lesson = (text) => ({ id: 'l1', screens: [screen({ prose: text, question: 'Value?', explain: 'It is the stated share.' })] });
  const prob = (text) => set([{ id: 'p-rate', prose: text, parts: [part('Value?')] }]);
  const go = (a, b) => run({ 'courses/c/l1.json': lesson(a), 'courses/c/problems-1.json': prob(b) });
  let r = go('Out of 120 calls, 50 paid, a base rate of 41.7%. The threshold is 0.6 and the model takes 40 calls.', 'Of 12 calls, 5 paid, so the base rate is 5/12 = 0.4167. The threshold is 0.6.');
  check('16 rate: 41.7% against 5/12 = 0.4167 with 0.6 in both fires', kindsOf(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The base rate is 41.7% on 120 calls.', 'The base rate is 0.4167 on 12 calls with threshold 0.6.');
  check('17 no hit: the same rate in two forms with no second number in common', !kindsOf(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The base rate is 41.7% and the threshold 0.6.', 'The base rate is 45.2% and the threshold 0.6.');
  check('18 no hit: a shared threshold with different rates', !kindsOf(r, 'p-rate').length, JSON.stringify(r.hits));
  r = go('The base rate is 0.4167 and the threshold 0.6.', 'The base rate is 5/12 = 0.4167 and the threshold 0.6 again.');
  check('19 no hit: the rate in one form only (decimal and fraction), left to the number and pair kinds', !kindsOf(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The share is 20% and the cut-off 0.6.', 'The share is 0.2 and the cut-off 0.6.');
  check('20 no hit: a stock rate (20%, one significant figure)', !kindsOf(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
  r = go('The base rate is 94.1% with threshold 0.6.', 'The base rate is 0.9381 with threshold 0.6.');
  check('21 no hit: a per cent and a decimal that differ beyond their rounding (94.1% against 0.9381)', !kindsOf(r, 'p-rate').includes('rate'), JSON.stringify(r.hits));
}
{
  // stock lines and the standard task
  const lesson = { id: 'l1', screens: [screen({ prose: 'A sample of 36 tins has mean 410 g and sd 12 g.', question: 'What is the standard error of the mean? Give 2 decimal places.', feedback: fb({ generic: 'Not quite right. Give 2 decimal places.' }), explain: 'The standard error is the standard deviation divided by the square root of n.' })] };
  const prob = set([{ id: 'p-std', prose: 'A sample of 49 bags has mean 880 g and sd 14 g.', parts: [part('What is the standard error of the mean? Give 2 decimal places.', { feedback: fb({ generic: 'Not quite right. Give 2 decimal places.' }), explain: { text: 'The standard error is the standard deviation divided by the square root of n.' } })] }]);
  const r = run({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': prob });
  check('22 no hit: stock feedback and the standard task with new numbers and nouns, one shared definition sentence', !kindsOf(r, 'p-std').length, JSON.stringify(r.hits));
  const r2 = run({ 'courses/a/l1.json': lesson, 'courses/b/problems-1.json': prob });
  check('23 no hit: the same text in another course (the kinds are same-course)', !r2.hits.some((h) => h.itemId === 'p-std'), JSON.stringify(r2.hits));
}

// ---- errors, waivers and the author-facing command ----
{
  const lesson = { id: 'l1', screens: [screen({ prose: 'Out of 120 calls, 50 paid, a base rate of 41.7%. The threshold is 0.6.', question: 'Value?' })] };
  const prob = (extra = {}) => set([{ id: 'p-rate', prose: 'Of 12 calls, 5 paid, so the base rate is 5/12 = 0.4167. The threshold is 0.6.', parts: [part('Value?')], ...extra }]);
  withTree({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': prob({ reuseWaiver: 'stands: ruled by the main session' }) }, (root) => {
    const a = scan(root, ['--all'], false);
    check('24 "reuseWaiver" on the item waives a rate hit (exit 0)', a.hits.some((h) => h.kind === 'rate' && h.waived) && a.status === 0, JSON.stringify(a));
  });
  withTree({ 'courses/c/l1.json': lesson, 'courses/c/problems-1.json': prob() }, (root) => {
    const r = spawnSync('node', [FC, '--content', root, '--file', join(root, 'courses', 'c', 'problems-1.json')], { encoding: 'utf8' });
    check('25 fresh-check.mjs --file prints the rate hit as an error and exits 1', r.status === 1 && /\[same-course-reuse\] error .*p-rate.*rate .*0\.6/.test(r.stdout), r.stdout + r.stderr);
    const r2 = spawnSync('node', [SC, '--content', root, '--all', '--no-retold'], { encoding: 'utf8' });
    check('26 --no-retold drops both new kinds', !/ (?:retold|rate) {2}<-/.test(r2.stdout), r2.stdout);
  });
}
console.log(fails ? `${fails} check(s) failed` : 'all checks passed');
process.exit(fails ? 1 : 0);
