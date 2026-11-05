#!/usr/bin/env node
// apply-item9-rulings.mjs: PLAN 2c item 9, user rulings on docs/reviews/review-precision-3.2.md
// (rows 4, 14, 19, 21, 22, 32, 34, 36, 43, 44, 47, 56, 58, 69, 70, 71, 72, K4, Draft notes).
// Exact old to new pairs on the file text (JSON-escaped). Idempotent: an old value already replaced
// is skipped; an old value found other than once, or missing with its new value absent, is an error.
// Run from anywhere: node app/tools/apply-item9-rulings.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const C = join(dirname(fileURLToPath(import.meta.url)), '..', 'content', 'courses');
const enc = (s) => JSON.stringify(s).slice(1, -1);
const EDITS = {
  'ito/l15-moments-quickly.json': [ // row 4
    ['The mean is 0. It applies to $dW$ integrals only.',
     'The mean is 0 for a $dW$ integral whose $E\\int f^2\\,dt$ is finite. It does not hold for $dt$ integrals.'],
  ],
  'measure-prob/l17-risk-neutral-rigorous.json': [ // row 14 and draft note
    ['A finite tree has no arbitrage exactly when one exists. It is complete exactly when it is unique.',
     'A finite tree has no arbitrage exactly when one exists. With no arbitrage, it is complete exactly when the measure is unique.'],
    ['Existence gives no arbitrage; uniqueness gives completeness.',
     'Existence gives no arbitrage; with no arbitrage, uniqueness gives completeness.'],
  ],
  'pdes/l8-heat-on-a-rod.json': [ // row 19 and draft note
    ['One term is accurate only once the other terms $e^{-k^2t}$ have died. At $t = 0$ the series overshoots by Gibbs\'s 8.95% of the jump.',
     'One term is accurate once the other terms $e^{-k^2t}$ have died. At $t = 0$ a partial sum overshoots by Gibbs\'s 8.95% of the jump.'],
    ['The overshoot is $8.95\\% \\times 200 = 17.9$, so the peak is 117.9.',
     'The overshoot of a partial sum is $8.95\\% \\times 200 = 17.9$, so its peak is 117.9.'],
  ],
  'markov/l2-transition-matrix.json': [ // row 21, K4 and draft notes
    ['Squaring the entries keeps only the path that stays put. Multiply the matrices',
     'Squaring an entry is not a two-step chance: off the diagonal it matches no path. Multiply the matrices'],
    ['You squared the one-step entry 0.1. That is the path Sunny, Rain, Rain only; the chain may pass through Sunny or Cloudy.',
     'You squared the one-step entry 0.1, which is no path. Sunny, Rain, Rain has chance $0.1 \\times 0.3 = 0.03$; add the paths through Sunny and Cloudy.'],
    ['You squared the entry, which keeps only the path that stays Sunny. Squared rows',
     'You squared the entry, which matches only the path that stays Sunny. Squared rows'],
    ['Squaring an entry keeps one path, the one that stays put. The matrix product',
     'Squaring an entry matches one path on the diagonal, the one that stays put, and none off it. The matrix product'],
    ['That keeps only the paths that never change state, as the squared sheet did.',
     'On the diagonal that matches only the paths that never change state; off it, no path at all.'],
  ],
  'markov/l3-never-leave.json': [ // row 22
    ['a recurrent one is always revisited ($f_i = 1$)',
     'a recurrent one is revisited with probability 1 ($f_i = 1$)'],
  ],
  'markov/l13-balanced-flows.json': [ // row 32 and draft note
    ['Birth-death chains are always reversible.',
     'Birth-death chains on a finite set of states are always reversible.'],
    ['Every such chain is reversible, with',
     'Every such chain on a finite set of states is reversible, with'],
  ],
  'markov/l15-sampling-by-chain.json': [ // row 34
    ['A Metropolis chain proposes a neighbour and accepts with chance',
     'A Metropolis chain proposes a neighbour up or down with equal chance. It accepts with chance'],
  ],
  'markov/l17-fair-bets.json': [ // row 36
    ['A forecast of revealed information is always fair, and a price is fair under the chance that balances its moves.',
     'A forecast of revealed information is fair when the quantity has a finite mean. A price is fair under the chance that balances its moves.'],
  ],
  'limits-thm/l9-averages-settle.json': [ // rows 43, 44
    ['The average of many independent draws settles near the mean $\\mu$: a miss of any size becomes rare.',
     'Take independent draws with one distribution and a finite mean $\\mu$. Their average settles near $\\mu$: a miss of any size becomes rare.'],
    ['and a draw with no finite mean never settles.',
     'and a heavy-tailed draw such as the Cauchy, with no finite mean, does not settle.'],
  ],
  'limits-thm/l19-generating-functions.json': [ // row 47
    ['$M_{X+Y}$ is a product, and only for independent variables.',
     '$M_{X+Y}$ is a product when $X$ and $Y$ are independent.'],
  ],
  'random-vars/l7-linearity.json': [ // rows 56, 58
    ['$E[X^2] \\ne E[X]^2$, and $E[XY] = E[X]E[Y]$ only for independent variables.',
     '$E[X^2] \\ne E[X]^2$ unless $X$ is constant. $E[XY] = E[X]E[Y]$ when $X$ and $Y$ are independent.'],
    ['For any $X$ and $Y$, dependent or not.',
     'For any $X$ and $Y$ with finite means, dependent or not.'],
  ],
  'research-int/l5-matrices-on-the-spot.json': [ // rows 69, 70 and draft notes
    ['A rank-one matrix $uv^\\top$ has one non-zero eigenvalue, $v \\cdot u$; the all-ones matrix has $n$.',
     'A rank-one matrix $uv^\\top$ has eigenvalue $v \\cdot u$ and otherwise only 0; the all-ones matrix has $n$.'],
    ['The all-ones matrix has eigenvalues $n$ and 0, never 1.',
     'For $n \\ge 2$ the all-ones matrix has eigenvalues $n$ and 0, never 1.'],
    ['Rank 1 leaves one non-zero eigenvalue.',
     'Rank 1 leaves at most one non-zero eigenvalue.'],
    ['With rank 1, only one of them is non-zero.',
     'With rank 1, at most one of them is non-zero.'],
    ['The trace then hands the last one over: $v \\cdot u$.',
     'The trace then hands the last one over: $v \\cdot u$, which is 0 if $v$ is perpendicular to $u$.'],
  ],
  'research-int/l6-bias-variance-aloud.json': [ // row 71 and draft notes
    ['The lowest training error is not the best model: training error always falls with flexibility.',
     'The lowest training error is not the best model. For nested least-squares fits, training error never rises as flexibility grows.'],
    ['Training error is the first number; it always falls with degree.',
     'Training error is the first number; it never rises with degree.'],
    ['Training error always falls as the model bends more, so it cannot pick the model.',
     'Training error never rises as the model bends more, so it cannot pick the model.'],
    ['Training error always falls with flexibility. It cannot find the turning point.',
     'Training error never rises as flexibility grows. It cannot find the turning point.'],
  ],
  'research-int/l7-ridge-against-lasso.json': [ // row 72
    ['Ridge divides each coefficient by $1 + \\lambda$ and never reaches zero.',
     'With uncorrelated, standardised columns, ridge divides each coefficient by $1 + \\lambda$ and never reaches zero.'],
  ],
};

let changed = 0, skipped = 0, bad = 0;
for (const [f, pairs] of Object.entries(EDITS)) {
  const p = join(C, f);
  let t = readFileSync(p, 'utf8');
  for (const [o, n] of pairs) {
    const eo = enc(o), en = enc(n);
    const k = t.split(eo).length - 1;
    if (k === 1) { t = t.replace(eo, () => en); changed++; }
    else if (k === 0 && t.includes(en)) skipped++;
    else { console.error(`ERROR ${f}: old value found ${k} times: ${o.slice(0, 60)}`); bad++; }
  }
  JSON.parse(t);
  writeFileSync(p, t);
}
console.log(`changed ${changed}, skipped ${skipped}, errors ${bad}`);
process.exit(bad ? 1 : 0);
