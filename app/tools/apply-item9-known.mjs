#!/usr/bin/env node
// apply-item9-known.mjs: PLAN 2c item 9, the five known precision lines (F08, N05) and the
// lines that repeat them (fix-pass rule: grep the old value). Rows 2, 6, 15, 53, K1 to K3 of
// docs/reviews/review-precision-3.2.md. Idempotent: an old value already replaced is skipped;
// an old value missing and its new value absent is an error.
// Run from anywhere: node app/tools/apply-item9-known.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const C = join(dirname(fileURLToPath(import.meta.url)), '..', 'content', 'courses');
const enc = (s) => JSON.stringify(s).slice(1, -1);
const EDITS = {
  'ito/l1-walk-to-bm.json': [ // K1 (F08 example A)
    ['As $n \\to \\infty$ the walk becomes Brownian motion $W_t$, and by the central limit theorem $W_t \\sim N(0, t)$.',
     'As $n \\to \\infty$ the walk converges in distribution to Brownian motion $W_t$. By the central limit theorem, $W_t \\sim N(0, t)$.'],
    ['W_t = \\lim_{n \\to \\infty} \\frac{S_{\\lfloor nt \\rfloor}}{\\sqrt{n}}, \\qquad W_t \\sim N(0, t)',
     '\\frac{S_{\\lfloor nt \\rfloor}}{\\sqrt{n}} \\to W_t \\text{ in distribution}, \\qquad W_t \\sim N(0, t)'],
    ['Scale by $1/\\sqrt{n}$: $1/n$ flattens the walk, anything bigger blows it up.',
     'Scale by $c/\\sqrt{n}$ and the limit is $cW_t$. A scale that shrinks faster, like $1/n$, flattens the walk; one that shrinks slower blows it up.'],
  ],
  'pdes/l1-equations-in-two-variables.json': [ // row 15 (F08 example B), K3
    ['A coefficient that depends on $S$ does not make an equation nonlinear; only $V$ times $V$ does.',
     'A coefficient that depends on $S$ does not make an equation nonlinear. A product or function of $V$ and its derivatives does, such as $V^2$, $(V_S)^2$ or $\\sin V$.'],
    ['Several terms with $V$ are fine. What breaks linearity is $V$ times $V$, or $V$ inside a function.',
     'Several terms with $V$ are fine. What breaks linearity is a product like $V^2$ or $(V_S)^2$, or $V$ inside a function.'],
    ['You counted the terms that hold $V$. Linearity needs $V$ times $V$ to break, and nothing here does.',
     'You counted the terms that hold $V$. Linearity breaks on a product like $V^2$ or $(V_S)^2$, and nothing here has one.'],
  ],
  'ito/l13-martingale-or-not.json': [ // row 2 (N05)
    ['A smooth $f(t, W_t)$ is a martingale exactly when its drift $f_t + \\tfrac12f_{xx}$ is zero.',
     'A smooth $f(t, W_t)$ with tame $f_x$ is a martingale exactly when its drift $f_t + \\tfrac12f_{xx}$ is zero. Tame means $E\\int_0^t f_x^2\\,ds$ is finite; without it, zero drift is not enough.'],
    ['Zero drift means a martingale. Add $\\mu f_x$ if the process also has drift $\\mu$.',
     'Zero drift means a martingale when $f_x$ is tame, as for every process in this lesson. Add $\\mu f_x$ if the process also has drift $\\mu$.'],
  ],
  'ito/l17-derivation-aloud.json': [ // row 6 (N05), K2
    ['The equation holds for any claim, puts and forwards included. Only the payoff at $T$ differs, and a forward has $V_{SS} = 0$.',
     'The equation holds for any European claim paying $g(S_T)$, puts and forwards included. Only the payoff at $T$ differs; a forward has $V_{SS} = 0$. American and path-dependent claims need more.'],
    ['You brought $\\mu$ back. The hedge cancels it for any claim, puts included.',
     'You brought $\\mu$ back. The hedge cancels it for any European claim, puts included.'],
    ['You changed the equation. It holds for any claim; the put\'s $V_S$ is simply negative.',
     'You changed the equation. It holds for any European claim; the put\'s $V_S$ is simply negative.'],
    ['You restarted. The derivation holds for any claim, so only the payoff at $T$ changes.',
     'You restarted. The derivation holds for any European claim, so only the payoff at $T$ changes.'],
    ['You let $\\mu$ back in. The hedge cancels it for any claim.',
     'You let $\\mu$ back in. The hedge cancels it for any European claim.'],
  ],
  'random-vars/l5-long-run-average.json': [ // row 53 (N05)
    ['Averaging the values without their chances. It agrees with $E[X]$ only when the pmf is symmetric.',
     'Averaging the values without their chances. It can agree with $E[X]$, as for equal chances or a symmetric pmf, but in general it does not.'],
  ],
};

let changed = 0, skipped = 0, bad = 0;
for (const [f, pairs] of Object.entries(EDITS)) {
  const p = join(C, f);
  let t = readFileSync(p, 'utf8');
  for (const [o, n] of pairs) {
    const eo = enc(o), en = enc(n);
    const k = t.split(eo).length - 1;
    if (k === 1) { t = t.replace(eo, en); changed++; }
    else if (k === 0 && t.includes(en)) skipped++;
    else { console.error(`ERROR ${f}: old value found ${k} times: ${o.slice(0, 60)}`); bad++; }
  }
  JSON.parse(t);
  writeFileSync(p, t);
}
console.log(`apply-item9-known: changed ${changed}, already applied ${skipped}, errors ${bad}`);
process.exit(bad ? 1 : 0);
