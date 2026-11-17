# Problem sets: measure-prob levels 1 to 3 (brief `docs/briefs/wave-c-author-ag.md`)

Files: `app/content/courses/measure-prob/problems-1.json` to `problems-3.json` (level 4 left to another author). Numbers: `docs/reports/problems-measure-prob-numbers.py` (exit 0, 800 checks, 0 failures after the session AF re-author and fix pass below). Builders kept in the scratch folder `author-measure-prob/` (l1.py, l2.py, l3.py).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-fat-cantor | 4 (3 / 1) | l1, l2, l3 | 4 |
| problems-1 | p-ball-machine | 5 (4 / 1) | l2, l4 | 3 |
| problems-1 | p-quote-ladder (AF) | 5 (4 / 1) | l2, l3, l4 | 4 |
| problems-1 | p-no-double-four (was p-no-double-seven) | 5 (4 / 1) | l1, l2, l3 | 5 |
| problems-2 | p-settlement-fails (AF) | 5 (3 / 2) | l5, l6 | 4 |
| problems-2 | p-compounding | 5 (4 / 1) | l6, l7 | 5 |
| problems-2 | p-boom-bust (AF) | 5 (5 / 0) | l5, l8 (l3 union bound) | 4 |
| problems-2 | p-random-maturity | 4 (3 / 1) | l5, l7 | 4 |
| problems-3 | p-nested-forecasts | 5 (5 / 0) | l9, l10 | 3 |
| problems-3 | p-doob-split | 4 (3 / 1) | l11, l12 | 4 |
| problems-3 | p-two-ups-stop | 5 (5 / 0) | l12, l13 (l11 stopping) | 5 |
| problems-3 | p-trial-stake (AF) | 4 (3 / 1) | l10, l12, l13 | 4 |

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

## Level 4 (brief `docs/briefs/wave-c-author-ag.md`, second author)

File: `app/content/courses/measure-prob/problems-4.json`. Numbers: `docs/reports/problems-measure-prob-4-numbers.py` (exit 0, 267 checks, 0 failures; helpers copied from the level 1 to 3 script, which is not edited). Builder kept in the scratch folder `author-measure-prob/l4.py`. Sets 1 to 3 were read as reuse sources and not edited.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-recovery-reweight | 4 (3 / 1) | l14, l15 | 3 |
| problems-4 | p-share-numeraire | 5 (3 / 2) | l14, l16, l17 | 5 |
| problems-4 | p-ten-trades | 4 (4 / 0) | l15, l16 | 4 |
| problems-4 | p-premium-weight | 5 (4 / 1) | l14, l16, l17 | 4 |

4 problems, 18 parts, typed 14 (one expression, 13 numeric). Skills `mt-change` and `mt-martingale`, from the level's lessons. Choice parts are judgements: which way round importance sampling has infinite variance, what makes $Q^S$ a probability, which line rewrites a price under $Q^S$, which step makes the risk-premium identity hold for every asset. Rule 6: no part prints its own target; each proof idea is tested by a number (a variance, a chance under the new measure, a covariance) or the choice of the valid step. Each later part restates the value it uses.

Chains. Recovery: $\tfrac{dQ}{dP} = 2x^2$, $Q(X > 0.8) = 0.5904$ through the weight, $\mathrm{Var}_P(Z) = \tfrac13$, then the reverse sampler's weight has infinite mean square ($\int_0^1 dx/x$) though $P \ll Q$. Numeraire: $Z_3 = S_3/(48 \times 1.02^3) = 0.8510$ on up, down, down; $E_Q[Z_3] = 1$ by the martingale property; $q^S = qu/1.02 = \tfrac{25}{48}$; price $= 48\,Q^S(S_3 > 50)$; $25.50$, equal to the $Q$ price. Trades: weight $0.625^8 \times 2.5^2 = 0.1455$; $E_Q[Y^2] = 0.00676$; relative error per draw 1.12; one $Q$ draw is worth about 14 plain draws. Premium: $q = \tfrac{16}{35}$; $Z_1 = \tfrac{19}{14}$ after a down; $\mathrm{Cov}_P(Z_1, S_1) = -2.00$; the step $E_P[Z_1X_1] = E_Q[X_1]$; over two steps $-4.14$, not twice $-2.00$.

### Checks (level 4)

| check | result |
|---|---|
| validator | 0 errors; no warning on problems-4 (pass-8 rules, `[key-length]`, `[shown-arithmetic]` and O2 all clear) |
| voice scan 35 (course folder) | 0 and 0 |
| `fresh-check --file` | 0 hits; `--files` on problems-1 to 4 together: 0 |
| numbers script | exit 0, 267 checks |
| `grade-all --file --local-cdn` | 0 failures (18 widgets: expression 1, numeric 13, choice 4) |
| playthrough `--local-cdn` | green (18 parts) |
| playthrough `--mobile` | green; the 440 px shots of every part were read, no layout fault |

The script computes each key twice: exact sympy integrals or fractions first, then scipy quadrature, enumeration of all 8 three-step paths, 4 two-step paths and 1,024 trade sequences, or a seeded simulation (inverse sampling of $P$, a million tree paths, two million binomial draws). It rebuilds each `wrong` value from its slip, checks every printed working figure (0.7225, 50.938, 0.531232, 0.14552, 0.0029907, 17.29 and the rest), and checks the rounded inputs a part tells the learner to use (0.1455, 0.00676, 1.12) give the same key. The 25 "check by hand" byKey lines were read: each states working numbers that are right. The script caught one false distractor claim early ("$Z_3 \le 1.5$" was false, the top path gives 1.84); it now reads $Z_3 < 2$ and the script checks it.

### Reuse: closest course material per problem (level 4)

Exam scope: of `topic-3.2.json`, e-die-reweight, e-is-weight and e-tree-price carry `mt-change`, and e-ruin-by-martingale and e-adapted-predictable `mt-martingale`; all were read. No stage or mock exam carries an `mt-` skill.

| problem | lesson screen | quiz | review | homework | exam |
|---|---|---|---|---|---|
| p-recovery-reweight | l14 "Two normals" (weight of $N(\theta, 1)$): ours is a polynomial density on $[0, 1]$ and goes on to the weight's variance | l14 q-reverse ($\tfrac{dP}{dQ}$ on uniforms): ours asks the reverse weight's mean square | r-weights ($E_Q[X]$ on three outcomes): no chance or variance asked | h-expect ($Z$ and $E_Q$ on four outcomes): ours is continuous, ends on infinite variance | e-is-weight (one normal weight): ours has no normal |
| p-share-numeraire | l17 "Discounted prices on the tree" (martingale test): ours uses the martingale to build a new measure | l16 q-down (down weight from density): ours turns a weight into a new up chance | r-twostep ($Z_2$ and call by $E_P$): ours changes from $Q$, not from $P$, and prices an asset-or-nothing payoff | h-tree (put via $E_P[Z_2 \cdot]$): no real-world chance here | e-tree-price ($q$ and a call): ours prices under the share measure |
| p-ten-trades | l15 "How many draws for the risk report" (draws from a given error table): ours computes the second moment from the weights and compares two samplers | l15 q-weight (a normal weight): ours weights a sequence of trades | r-n (plain draws for 5%): ours is the ratio of two samplers | h-is (normal tail, three steps): ours is discrete, exact | e-is-weight: one weight only |
| p-premium-weight | l17 "Pricing by the martingale" (put price): ours finds the covariance of the density with the price, the risk premium | l14 q-state ($Z$ after a down): one step of ours, other numbers | r-q ($q$ only): one step of ours | h-long (q, density, price, written): ours never prices; it proves the premium identity by choice and number | e-tree-price: ours has no option |

`fresh-check` reported 0 hits from the first run. Key numbers (0.5904, $2x^2$, $4x^3$, 0.8510, 25/48, 25.50, 0.1455, 0.00676, 16/35, 19/14, 4.14, 40.4, 42.4, 43.35, 7/128) were grepped in the course folder by hand: none occurs. 0.625 occurs as the tree's $q$ in l14 to l17; here it is the ratio $0.5/0.8$, an unrelated setting. 1.06 occurs in l1, problems-2 and review-4 in other roles. The stories (recovery-rate models, a share measure on a three-step tree, ten trades, the premium as a covariance) appear nowhere in the course; "recovery rate" occurs in `exams/topic-1.6.json` (a likelihood fit, another course). Slip lines are written per part; none repeats a course line.

Notes: attribution as for levels 1 to 3 (the session's Opus 5.5 lines). One inbox bullet under `Raised later (problems measure-prob level 4):`. No `course.json` change proposed.
## Session AF: re-author and fix pass (review `docs/reviews/review-problems-measure-prob-1-3.md`)

Re-authored: `p-reciprocal-grid` as `p-quote-ladder`, `p-billed-hours` as `p-settlement-fails`, `p-root-of-uniform` as `p-boom-bust`, and, by the main session's ruling, `p-red-card-call` as `p-trial-stake`. Fixed as written: findings 3, 4 and 7 to 11 (`p-no-double-seven` renamed `p-no-double-four` with the block 44). Now 12 problems, 56 parts, typed 46 (level 1 15 of 19, level 2 15 of 19, level 3 16 of 18). The sets table above holds the new rows; the AG chains and reuse rows of the four replaced problems no longer apply.

Chains. `p-quote-ladder`: $P(N = 2) = 0.096$, the law $0.6 \times 0.4^k$, $P(N \in \{0, 3, 6, \dots\}) = \tfrac{25}{39}$ by countable additivity, the size of $\sigma(N)$, $P(X \le 2U) = \tfrac56$. `p-settlement-fails`: $E[1.25^N] = \tfrac{256}{225}$ through a series, monotone convergence in $s$ for $G'(s) \uparrow E[N]$, $E[N] = 0.5$, $E[N^2] = 0.875$, $E[5^N] = \infty$. `p-boom-bust`: $E[\sqrt{M_n}] = 0.9^{n/2}$, the root bound 1.1455, the exact 0.3125, the union bound 0.00518 after day 200, $E[M_{10}^2] = 21.65$. `p-trial-stake`: $M_1 = 77.5$, $P(T = 2) = 0.45$, both selling rules at $E[M_T] = 54.5$, $\mathrm{Var}(M_T) = 1074.75$.

Closest course material, per new problem (one line on how each differs).

| problem | lesson screen | quiz | review | homework | exam | other set |
|---|---|---|---|---|---|---|
| p-quote-ladder | l2 "Why countable unions" (cofinite family, the even numbers): ours asks the size of $\sigma(N)$ with infinitely many atoms, not whether a family is closed | l2 q-two (8 events from two sets): ours is uncountable | r-counting (counting measure, $A_n \downarrow \varnothing$): ours is a probability on the whole numbers, no limit | h-build-space ($p_k = \tfrac{1}{k(k+1)}$, tails, continuity): the closest; ours has the law $0.6 \times 0.4^k$ from a map of $U$, a union over every third atom and an event mixing $X$ and $U$, no tail or continuity | e-atoms-three-sets (64 events): finite atoms | p-ball-machine parts 1 and 2 count the finite $\sigma(X)$, $\sigma(X, Y)$ |
| p-settlement-fails | l6 "Summing the tail" (an indicator sum by monotone convergence): ours sums $1.25^k\mathbf 1_{\{N = k\}}$ and then uses the theorem in $s$; l5 "Does every random variable have a mean?": part 5 is the same idea (finite everywhere, infinite mean) on $5^N$ | l6 q-sum ($\sum 3^{-k}$): part 1 is one such swap | r-heavy ($1.5^K$ by series): a draft charged $1.5^N$, moved to $1.25^N$ on that grep | h-sp (capped St Petersburg): no cap | e-tail-integral: no tail used | none |
| p-boom-bust | l8 "Mean square implies in probability": part 2 uses its indicator bound with $\sqrt{M}$; l8 "The spike in mean square": part 5 has the same contrast (almost surely yes, mean square no) for a product of daily factors | l8 q-cheb (0.16 from a given 0.04): ours computes the mean and sets the bound beside the exact chance | r-cheb (from $\tfrac1n$): another bound and other numbers; r-mode: no modes are picked | homework-1 h-long (Borel-Cantelli): part 4 is the union bound that drives it, by number | e-swap-limits: no part compares $E[M_n]$ with the mean of the limit | none |
| p-trial-stake | l12 "The forecaster" (quotes at every node of three tosses): part 1 is one quote on an unequal tree; a root part was dropped so the chain does not follow the screen; l13 "Optional stopping, bounded case" (proof): part 3 applies it to two rules | l12 q-doob, l13 q-fixed | r-doob (heads count, coin 0.8), r-stop | homework-3 h-long (bounded optional stopping): used by a choice; h-prove-urn: no urn | e-tree-price, e-ruin-by-martingale: no pricing measure, no exit | p-two-ups-stop part 3 uses the same theorem by number |

Reuse checks. `fresh-check --file` on each set and `--files` on all three: 0 hits. Grepped by hand: each new key (0.096, 25/39, 5/6, 256/225, 0.875, 1.1455, 0.3125, 0.00518, 21.65, 77.5, 54.5, 1074.75) in the course folder (only unrelated chart or table values), the bases $0.4^k$, $1.25^N$, $5^N$, the multipliers 1.6 and 0.4, and the stories (quote ladder, settlement fails, a biotech's staged news) across `app/content`: none in use. `markov/problems-2` holds a takeover deal with a regulator, so the staged story is a biotech, not a deal.

Gates (session AF): validator 0 errors, no pass-8 warning on the sets; voice scan 35, 0 and 0; `fresh-check` 0 hits; author's script 800 checks, 0 failures; reader's script 665 checks, 0 findings; `grade-all --file` 19, 19 and 18 widgets, 0 failures; playthrough `--problems` green for all three sets with and without `--mobile`, 440 px shots read (no fault). Commits: one per set; the number scripts, this report and the review's fix pass land with the problems-3 commit, so the scripts pass from that commit on. Two engine bullets under `Raised later (problems measure-prob re-author AF)`.
