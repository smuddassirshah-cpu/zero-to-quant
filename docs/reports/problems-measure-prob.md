# Problem sets: measure-prob levels 1 to 3 (brief `docs/briefs/wave-c-author-ag.md`)

Files: `app/content/courses/measure-prob/problems-1.json` to `problems-3.json` (level 4 left to another author). Numbers: `docs/reports/problems-measure-prob-numbers.py` (exit 0, 704 checks, 0 failures). Builders kept in the scratch folder `author-measure-prob/` (l1.py, l2.py, l3.py).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-fat-cantor | 4 (3 / 1) | l1, l2, l3 | 4 |
| problems-1 | p-ball-machine | 5 (4 / 1) | l2, l4 | 3 |
| problems-1 | p-reciprocal-grid | 5 (4 / 1) | l3, l4 (l1 null points) | 4 |
| problems-1 | p-no-double-seven | 5 (4 / 1) | l1, l2, l3 | 5 |
| problems-2 | p-billed-hours | 4 (4 / 0) | l5, l6 | 3 |
| problems-2 | p-compounding | 5 (4 / 1) | l6, l7 | 5 |
| problems-2 | p-root-of-uniform | 5 (4 / 1) | l5, l8 | 4 |
| problems-2 | p-random-maturity | 4 (3 / 1) | l5, l7 | 4 |
| problems-3 | p-nested-forecasts | 5 (5 / 0) | l9, l10 | 3 |
| problems-3 | p-doob-split | 4 (3 / 1) | l11, l12 | 4 |
| problems-3 | p-two-ups-stop | 5 (5 / 0) | l12, l13 (l11 stopping) | 5 |
| problems-3 | p-red-card-call | 4 (4 / 0) | l10, l12, l13 | 4 |

12 problems, 55 parts; typed 47 (level 1 15 of 19, level 2 15 of 18, level 3 17 of 18). Choice parts are judgements only: which closure makes $C$ Borel, which variable is measurable, what happens to $F_X$ at 0, which union step, which theorem swaps the limit, which bound dominates, which modes hold, whether $A$ is predictable. Proof steps are tested through a number (a length, a count, a limit) or the choice of the valid step; no part can be passed by working back from a printed target. Each later part restates the value it uses. Every lesson of each level appears; nothing runs past its level (level 3 uses only finite spaces and bounded stopping times).

Chains. L1: stage-3 gap, length of $C_n$, length of $C$ by continuity from above, why $C$ is Borel; atoms and events of $\sigma(X)$, of $\sigma(X, Y)$ (7 atoms, not 8), $F_X(2.5)$ of the pushforward, the 0.75 point, a measurable function; $P(N = 3)$, $P(N \ge n)$, $F_X(0.3)$, the left limit at 0.2, continuity at 0; strings with no 77, the recursion, a disjoint-pair bound, $P(D) = 0$, countable subadditivity. L2: one billed hour, the tail sum by monotone convergence, the half-hour grid, the first grid above 0.99; $E[G_2]$, $E[G_4]$, the dominator's mean, the theorem, the limit $e^{0.125}$; $E[X_4]$ by layer cake, the mean-square distance, Chebyshev's useless bound, the exact chance, the modes; $V(0.05)$, the dominating bound, $-V'(0.05)$, the duration. L3: new events, an atom forecast, the tower, the forecast error, the error the finer information removes; the drift of $S^2$, $A_3$ on a path, predictability, $E[S_3^2]$; $P(T = 3)$, $E[T]$, $E[S_T]$, $E[S_T^2] = E[T]$, the day-4 share; $E[M_1]$, the martingale step, the chance of calling at once and winning, the total chance by optional stopping.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| validator | 0 errors; no pass-8 warning (`[working-band]`, `[rounding-tie]`, `[table-source]`, `[percent-unit]`, `[wide-wrong-tol]`) | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| `fresh-check --file` | 0 hits | 0 hits | 0 hits (also `--files` on all three: 0) |
| numbers script | exit 0 (704 checks for the three sets) | same | same |
| `grade-all --file --local-cdn` | 0 failures (19 widgets) | 0 failures (18) | 0 failures (18) |
| playthrough `--local-cdn` | green (19 parts) | green (18) | green (18) |
| playthrough `--mobile` | green; 440 px shots read, no fault | green | green |

Two advisory O2 lines (sentences of 20 words or more) remain in problems-1 and one in problems-2; none is over 35. The numbers script computes each key twice: exact fractions, sympy and closed forms first; then brute force (bitmask sigma-algebra closure on the 12 balls, all digit strings, all coin paths, all 35 card orders), quadrature (scipy, trapezoid on a normal grid), weighted least squares for the projections, or a seeded simulation. It rebuilds every `wrong` value from its slip, checks the key band takes the rounding asked and the printed figure, keeps every slip outside the key band and clear of the other slips, and runs `numbers_lib.Level.check_wrongs` (the 70 "check by hand" byKey lines state working numbers, each read and correct).

## Reuse: closest course material per problem

Exam scope: `topic-3.2.json` holds the course's skills (e-atoms-three-sets, e-tail-integral, e-die-reweight, e-sigma-families, e-var-of-condexp, e-adapted-predictable, e-ruin-by-martingale, e-is-weight, e-swap-limits, e-tree-price, e-variance-split); all were read. No mock or stage exam carries an `mt-` skill.

| problem | lesson screen | quiz | review | homework | exam |
|---|---|---|---|---|---|
| p-fat-cantor | l1 "The Cantor set" (length left after 10 stages): ours removes $4^{-n}$ gaps and keeps length $\tfrac12$ | l1 q-cantor (countable?): ours asks why $C$ is Borel | r-cantor (fill stage 6): no stage table here | h-cantor (first stage below 0.001, count intervals): no threshold or count asked | e-sigma-families: finite families, not a limit set |
| p-ball-machine | l2 "The sigma-algebra generated by two events" (die, 16 events): ours has unequal chances, a variable and an empty intersection | l2 q-two (8 events): a single count only | r-events (256 from three sets): ours finds 7 atoms, then a law | h-code (atoms in code): no code, adds the pushforward | e-atoms-three-sets (64): ours goes on to $F_X$ and a quantile |
| p-reciprocal-grid | l4 "A loss with an atom" ($F_L$ at a point): ours has infinitely many atoms crowding at 0 | l4 q-left (left limit as $P(X < x)$): ours computes one | r-var (VaR by inverse): no inverse sampling here | h-var (F at a point, two VaRs): ours is preimages of $\lfloor 1/U \rfloor$ | none close |
| p-no-double-seven | l1 "Covering the rationals": ours bounds an uncountable null set by disjoint blocks | l1 q-irrational: chance 1 of a different event | r-union (union bound total): ours unions null events | h-long (Borel-Cantelli): ours is a direct countable union, no lemma | none close |
| p-billed-hours | l6 "Summing the tail" (fill attempts, $E[N] = 5$): ours floors a continuous time and refines the grid | l6 q-tail ($E[N] = 2$): ours sums $e^{-k}$ | r-tail ($E[N] = 4$): one step only of ours | h-build-integral (simple functions from below): ours uses floors of an exponential with $h/(e^h - 1)$ | e-tail-integral (Pareto tail): different law, no grid |
| p-compounding | l7 "A dominated sequence" ($U^n$ by 1): ours needs a random dominator $e^{\lvert R \rvert}$ | l7 q-hyp (which condition): ours computes the dominator's mean | r-dom ($E[Y] = 3$): ours ties the bound to normal moments | h-nu ($nU^n$, why DCT fails): ours is a case where it holds | e-swap-limits (select sequences): ours computes the limit |
| p-root-of-uniform | l8 "The typewriter in mean square": ours has a.s. convergence with an exact mean-square formula | l8 q-cheb (bound 0.16): ours shows a bound above 1 against the exact chance | r-cheb (0.25): same contrast | h-modes (chart of three sequences): one sequence, computed | none close |
| p-random-maturity | l7 "The pathwise delta of a call": ours differentiates in a rate, with a constant bound 4 | l7 q-digital (where pathwise fails): ours is a smooth case | r-delta (biased digital estimate): not a Monte Carlo item | h-tranche (layer cake for a tranche): ours is an integral in $T$, then a duration | none close |
| p-nested-forecasts | l10 "Splitting the variance" (fill two pieces): ours compares two nested forecasts | l10 q-tower (choice): ours computes the tower | r-die (MSE 2.6667): ours adds the gap between forecasts | h-proj (forecast and MSE): ours adds $\mathcal H \subset \mathcal G$ and the reduction | e-var-of-condexp, e-variance-split: one sigma-algebra only |
| p-doob-split | l12 "A martingale built from squares" ($S^2 - n$, fair): ours has a path-dependent predictable part | l12 q-drift ($S - cn$): ours is the square with drift | r-cube (which is a martingale): ours builds the compensator | h-mart (select martingales): ours computes $A_3$ and $E[S_3^2]$ | e-adapted-predictable (table): ours is one process, numeric |
| p-two-ups-stop | l13 "Stopping at the top" (not a stopping time): ours is a bounded stopping time | l13 q-time ($E[T] = 32$ exit): ours enumerates a capped rule | r-ruin (fill two values): no exit from an interval | h-wald (proof order): ours uses $S^2 - n$ at $T$ by number | e-ruin-by-martingale: no exponential martingale, no interval |
| p-red-card-call | l12 "The forecaster" (Doob quotes): ours is the remaining-share martingale of a deck | l12 q-doob (2): different process | r-doob (2.6): different process | h-prove-urn (Polya urn proof): ours draws without replacement and uses optional stopping for a calling rule | none close |

`fresh-check` reported 0 errors on each set; problems-2 first raised two warnings (part 5's option text shared "almost surely in probability in mean square and in distribution" with l8 and review-2), and the options were reworded; it now reports nothing. The key numbers (78, 128, 57/78, 981, 9720, 0.366, 0.5820, 0.7707, 1.0945, 1.567, 1.5152, 0.3487, 0.9063, 1.7523, 3.5, 2.2, 3.1, 8.5, 5.4, 3.96, 3.375, 0.625, 4/7, 2/7) were also grepped in the course folder by hand: only 0.9063 occurs, as a chart value in `l3-measures.json` (the hitting walk), an unrelated setting. Slip lines are written per part; none repeats a course line.

## Notes

- Attribution: the brief names "Claude Fable 5.2"; the session's system attribution (Opus 5.5) was used, as the harness instructs.
- After `git checkout app/content/manifest.json` the playthrough of a set opens "in state empty" until the validator is run again (the manifest lists the sets). Recorded as an inbox bullet.
- No `course.json` change proposed.
