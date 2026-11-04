# Fix pass: per cent numeric keys

Bug: `numeric.js` divides a typed value by 100 when `unit: "%"` (a typed % sign is read as a per cent too), so the stored key must be the fraction. Keys stored as the per cent figure (15.87) matched only a typed 1587. Fix: `answer`, every `wrong[].value` and every absolute `tol` divided by 100; `accept`, feedback and explanation text untouched (they already show the per cent form).

Hand-typed column: a real input was filled by keystrokes in a mounted widget; T = the number in the accept text, T% = the same with a % sign, x100 = the old wrong way (answer times 100). Every old `wrong` value, typed in per cent, was also checked to return its own key. Playwright script: scratchpad `fix-pct/hand.mjs`.

| File | Widget | Scan | Verdict | Old key | New key | Hand-typed |
|---|---|---|---|---|---|---|
| courses/eigen/l16-correlated-normals.json | `.screens[10].widget` | BUG | fixed | -2.25 | -0.0225 | T -2.25 right, T% right, x100 wrong: pass |
| courses/ensembles/l4-predicting-numbers.json | `.screens[10].widget` | CHECK | fixed | 31.21 | 0.3121 | T 31.21 right, T% right, x100 wrong: pass |
| courses/ensembles/l4-predicting-numbers.json | `.quiz[1].widget` | CHECK | fixed | 21 | 0.21 | T 21 right, T% right, x100 wrong: pass |
| courses/ensembles/review-1.json | `.items[3].widget` | CHECK | fixed | 17 | 0.17 | T 17 right, T% right, x100 wrong: pass |
| courses/ensembles/review-1.json | `.items[6].widget` | CHECK | fixed | 31 | 0.31 | T 31 right, T% right, x100 wrong: pass |
| courses/garch/homework-1.json | `.items[1].widget` | BUG | fixed | 2.77 | 0.0277 | T 2.77 right, T% right, x100 wrong: pass |
| courses/garch/homework-2.json | `.items[0].widget` | BUG | fixed | 19.44 | 0.1944 | T 19.44 right, T% right, x100 wrong: pass |
| courses/garch/homework-2.json | `.items[3].widget` | CHECK | fixed | 28.34 | 0.2834 | T 28.3 right, T% right, x100 wrong: pass |
| courses/garch/l4-realised-vol.json | `.screens[2].widget` | BUG | fixed | 15.11 | 0.1511 | T 15.11 right, T% right, x100 wrong: pass |
| courses/garch/l4-realised-vol.json | `.quiz[0].widget` | BUG | fixed | 14.42 | 0.1442 | T 14.42 right, T% right, x100 wrong: pass |
| courses/garch/l5-recent-days-more.json | `.screens[1].widget` | BUG | fixed | 71.0 | 0.71 | T 71.0 right, T% right, x100 wrong: pass |
| courses/garch/l5-recent-days-more.json | `.screens[10].widget` | CHECK | fixed | 2.2566 | 0.022566 | T 2.26 right, T% right, x100 wrong: pass |
| courses/garch/l5-recent-days-more.json | `.quiz[0].widget` | BUG | fixed | 26.3 | 0.263 | T 26.3 right, T% right, x100 wrong: pass |
| courses/garch/l6-arch.json | `.screens[2].widget` | CHECK | fixed | 2.2361 | 0.022361 | T 2.24 right, T% right, x100 wrong: pass |
| courses/garch/l6-arch.json | `.screens[11].widget` | CHECK | fixed | 5.7966 | 0.057966 | T 5.80 right, T% right, x100 wrong: pass |
| courses/garch/l8-long-run-variance.json | `.screens[2].widget` | BUG | fixed | 15.87 | 0.1587 | T 15.87 right, T% right, x100 wrong: pass |
| courses/garch/l8-long-run-variance.json | `.screens[3].widget` | BUG | fixed | 14.96 | 0.1496 | T 14.96 right, T% right, x100 wrong: pass |
| courses/garch/l8-long-run-variance.json | `.screens[6].widget` | BUG | fixed | 24.69 | 0.2469 | T 24.69 right, T% right, x100 wrong: pass |
| courses/garch/l8-long-run-variance.json | `.quiz[1].widget` | BUG | fixed | 23.81 | 0.2381 | T 23.81 right, T% right, x100 wrong: pass |
| courses/garch/review-1.json | `.items[3].widget` | BUG | fixed | 23.81 | 0.2381 | T 23.81 right, T% right, x100 wrong: pass |
| courses/garch/review-2.json | `.items[1].widget` | CHECK | fixed (tol also widened to 0.00005, the old 0.003 rejected the accepted 1.48) | 1.4832 | 0.014832 | T 1.48 right, T% right, x100 wrong: pass |
| courses/garch/review-2.json | `.items[7].widget` | BUG | fixed | 15.87 | 0.1587 | T 15.87 right, T% right, x100 wrong: pass |
| courses/garch/review-2.json | `.items[9].widget` | BUG | fixed | 22.45 | 0.2245 | T 22.45 right, T% right, x100 wrong: pass |
| courses/measure-prob/l11-filtrations.json | `.screens[8].widget` | CHECK | skipped measure-prob (another agent) | 250 | n/a | n/a |
| courses/measure-prob/l3-measures.json | `.screens[7].widget` | BUG | skipped measure-prob (another agent) | 3 | n/a | n/a |
| courses/measure-prob/l3-measures.json | `.quiz[1].widget` | BUG | skipped measure-prob (another agent) | 2 | n/a | n/a |
| courses/measure-prob/review-1.json | `.items[9].widget` | BUG | skipped measure-prob (another agent) | 4 | n/a | n/a |
| courses/opt-dash/homework-4.json | `.items[5].widget` | BUG | fixed | 18.38 | 0.1838 | T 18.38 right, T% right, x100 wrong: pass |
| courses/options/l3-payoff-minus-premium.json | `.screens[9].widget` | CHECK | correct as is: key 2.3333 is the fraction for the typed 233%, accept text reads "233%" | 2.3333 | 2.3333 | not changed |
| courses/options/review-1.json | `.items[7].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 2.2 | 2.2 | not changed |
| courses/pdes/l7-when-fourier-converges.json | `.screens[1].widget` | BUG | fixed | 8.95 | 0.0895 | T 8.95 right, T% right, x100 wrong: pass |
| courses/py-found/homework-4.json | `.items[3].widget` | BUG | fixed | 18.03 | 0.1803 | T 18.03 right, T% right, x100 wrong: pass |
| courses/py-found/l13-one-at-a-time.json | `.quiz[0].widget` | BUG | fixed | 25 | 0.25 | T 25 right, T% right, x100 wrong: pass |
| courses/py-found/l14-sorting-by-what-matters.json | `.quiz[1].widget` | CHECK | fixed | -2 | -0.02 | T -2 right, T% right, x100 wrong: pass |
| courses/py-found/l15-checking-your-code.json | `.screens[6].widget` | BUG | fixed | 19.05 | 0.1905 | T 19.05 right, T% right, x100 wrong: pass |
| courses/py-found/l15-checking-your-code.json | `.quiz[1].widget` | BUG | fixed | 12.7 | 0.127 | T 12.70 right, T% right, x100 wrong: pass |
| courses/py-found/review-4.json | `.items[2].widget` | BUG | fixed | 15 | 0.15 | T 15 right, T% right, x100 wrong: pass |
| courses/py-found/review-4.json | `.items[4].widget` | BUG | fixed | 22.45 | 0.2245 | T 22.45 right, T% right, x100 wrong: pass |
| courses/py-found/review-4.json | `.items[8].widget` | BUG | fixed | 4.74 | 0.0474 | T 4.74 right, T% right, x100 wrong: pass |
| courses/pytest/homework-3.json | `.items[5].widget` | BUG | fixed | 37.7 | 0.377 | T 37.70 right, T% right, x100 wrong: pass |
| courses/pytest/l10-test-first.json | `.screens[7].widget` | BUG | fixed | 3.125 | 0.03125 | T 3.125 right, T% right, x100 wrong: pass |
| courses/pytest/l10-test-first.json | `.quiz[1].widget` | BUG | fixed | 6.25 | 0.0625 | T 6.25 right, T% right, x100 wrong: pass |
| courses/pytest/l11-testing-drawdown.json | `.screens[0].widget` | BUG | fixed | 25 | 0.25 | T 25 right, T% right, x100 wrong: pass |
| courses/pytest/l11-testing-drawdown.json | `.quiz[0].widget` | BUG | fixed | 40 | 0.4 | T 40 right, T% right, x100 wrong: pass |
| courses/pytest/l12-every-push.json | `.screens[4].widget` | BUG | fixed | 90.48 | 0.9048 | T 90.48 right, T% right, x100 wrong: pass |
| courses/pytest/l12-every-push.json | `.quiz[1].widget` | BUG | fixed | 85 | 0.85 | T 85 right, T% right, x100 wrong: pass |
| courses/pytest/l9-logic-apart.json | `.quiz[1].widget` | BUG | fixed | 2.5 | 0.025 | T 2.5 right, T% right, x100 wrong: pass |
| courses/pytest/review-3.json | `.items[6].widget` | BUG | fixed | 68 | 0.68 | T 68 right, T% right, x100 wrong: pass |
| courses/ratio/homework-2.json | `.items[2].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 1.4 | 1.4 | not changed |
| courses/ratio/l1-out-of-a-hundred.json | `.quiz[3].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 1.2 | 1.2 | not changed |
| courses/ratio/l3-what-percentage.json | `.screens[5].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 1.25 | 1.25 | not changed |
| courses/ratio/l5-rise-or-fall.json | `.screens[5].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 1.5 | 1.5 | not changed |
| courses/ratio/l5-rise-or-fall.json | `.quiz[3].widget` | ok-fraction>1 | correct as is: a genuine percentage over 100%, stored as a fraction | 1.5 | 1.5 | not changed |
| courses/systems/l18-feed-handler.json | `.screens[1].widget` | BUG | fixed (wrong "frac" 0.4 became 0.004, the fraction typed as 0.4) | 40 | 0.4 | T 40 right, T% right, x100 wrong: pass |
| courses/validation/l7-purging.json | `.screens[5].widget` | BUG | fixed | 19.4 | 0.194 | T 19.4 right, T% right, x100 wrong: pass |
| exams/topic-2.2.json | `.items[1].widget` | CHECK | fixed | 1.37 | 0.0137 | T 1.37 right, T% right, x100 wrong: pass |
| exams/topic-2.2.json | `.items[11].widget` | CHECK | fixed | 1.45 | 0.0145 | T 1.45 right, T% right, x100 wrong: pass |

Fixed: 46. CHECK verdicts: every CHECK was a bug except `options/l3-payoff-minus-premium.json` screens[9] (233% stored as 2.3333, correct). The ensembles, garch daily-vol, py-found daily-return and topic-2.2 CHECK lines all asked for a per cent figure with a % unit, so their keys were bugs.

Validator: 0 errors. Playthroughs (`--local-cdn`) green for all 16 changed lessons, 10 changed sets and exam topic-2.2.

## Second batch (keys at or below 1)

Each old value was recomputed first: 10/sqrt(252) = 0.62994, (-1.2+1.5+0.6)/3 = 0.3, 1.10 x 0.90 - 1 = -0.01, half of (ln 1.07 + ln 0.95) = 0.8183, 1% - half of 0.04^2 = 0.92%. The answer, every wrong value and every abs tol were divided by 100; accept and feedback text unchanged. A grep of the old values found no other holder in each file.

| File | Widget | Old answer | New answer | Old wrong values | New wrong values | Typed results |
|---|---|---|---|---|---|---|
| courses/garch/l4-realised-vol.json | `.quiz[1]` | 0.63 | 0.0063 | 0.0397, 0.523 | 0.000397, 0.00523 | 0.63, 0.63%, 0.630 right; 63 wrong; 0.0397 hits 252; 0.523 hits 365 |
| courses/numpy-pandas/l12-split-apply-combine.json | `.screens[1]` | 0.3 | 0.003 | 0.2333, 0.9, -1.2 | 0.002333, 0.009, -0.012 | 0.3, 0.3% right; 30 wrong; each old wrong hits all, sum, first |
| courses/py-found/l16-returns-from-a-file.json | `.quiz[3]` | -1 | -0.01 | 0 | 0 | -1, -1%, unicode minus 1 right; -100 wrong; 0 hits sum |
| courses/random-vars/l19-convex-bets.json | `.screens[11]` | 0.818 | 0.00818 | 1, 0.64, 0.18 | 0.01, 0.0064, 0.0018 | 0.818, 0.818%, 0.82 right; 81.8 wrong; each old wrong hits arith, nohalf, drag |
| courses/random-vars/review-5.json | `.items[5]` | 0.92 | 0.0092 | 1, 0.84, 0.08 | 0.01, 0.0084, 0.0008 | 0.92, 0.92% right; 92 wrong; each old wrong hits arith, nohalf, drag |

Tolerances: abs 0.001 became 1e-05, 0.005 became 5e-05, 0.01 became 0.0001; each still accepts the precision the prompt asks for. Typed checks ran the real `grade.js` with the numeric widget's parse rule (a node harness, not a browser). Validator: 0 errors. Playthroughs with `--local-cdn` green for the four lessons and set random-vars/review-5.
