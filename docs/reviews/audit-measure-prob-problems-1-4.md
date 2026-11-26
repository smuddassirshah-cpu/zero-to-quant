# Blind concept audit: measure-prob problems-1 to problems-4

Auditor brief `docs/briefs/concept-audit.md` ("Auditor brief (binding)"), common rules of session 13. Content at commit 4489fd2f. Scope: `app/content/courses/measure-prob/problems-1.json` to `problems-4.json` (16 problems, 74 parts), added after the course closed. Stage 3 course, full ledger. Lessons were opened only to confirm that a named idea is taught (Vitali set in l1, null sets and "almost surely" in l3, the moving spike in l7, Pythagoras in l10, predictable in l11 and l12, optional stopping in l13). No content, engine or state file was edited. No browser.

Blind rule kept: the ledger and the three findings below were written before any earlier read was opened.

## Result

- Ledger `docs/reports/audit-measure-prob-problems-1-4-ledger.md`: 512 rows; `correct` 509, `imprecise` 3, `wrong` 0, `misleading` 0, `unverified` 0.
- Findings: 3, all `imprecise`, all `minor`. No graded key, slip value, tolerance or carried value is wrong.
- Every numeric key (55) and every slip value recomputes, exactly where a closed form or an enumeration exists. Every expression key, accepted form and wrong form was evaluated at sample points. Every chained part uses the value the earlier part produced, and where a rounded value is carried (0.00676, 1.12, 1.7523 and 0.9063, $\Phi(0.5) = 0.6915$) the key is the one the carried figure gives and the unrounded figure rounds to the same answer.

## Method

Each part was read as question, key, tolerance, each slip against the mistake its line names, each option and its `why`, the `correct` line, the `generic` hint and the `explain`. The concepts script `docs/reports/measure-prob-problems-concepts.py` loads the four files and holds every key and slip against a value recomputed from the stem (590 checks). It also checks that each slip band is clear of its key band, that the script recomputes every slip the content carries, and that the key and each slip typed at the places asked land in their own bands.

Things watched for, and what was found:

| topic | where | verdict |
|---|---|---|
| sigma-algebras and measurability | p-fat-cantor 4, p-ball-machine 1, 2, 5, p-quote-ladder 4 | Correct. Atoms counted by enumeration; $\sigma(N)$ uncountable is right (one event per subset of the values); the finite-or-cofinite option is correctly refused. Finding 3 is a rider left standing in one `why`. |
| continuity from above | p-fat-cantor 3, p-no-double-four 4 | Correct, and the finite-measure hypothesis is stated both times. |
| union bound and Borel-Cantelli | p-no-double-four 3 to 5, p-boom-bust 4, 5 | Correct. The sets use countable subadditivity only, so no independence condition is needed and none is claimed. Independence is used only for disjoint digit pairs, where it holds. The slip line "only the disjoint pairs give a valid bound" was tested: exact $P(D_{200}) = 0.1599$, above $0.99^{199} = 0.1353$. |
| monotone and dominated convergence, Fatou | p-settlement-fails 1, 2, 5, p-compounding 3, 4, p-random-maturity 2 | Correct with hypotheses: non-negative and rising for MCT, an integrable bound for DCT, Fatou as an inequality only. The `dct` option is false as worded ("needs no further check"). Finding 1 is one word in a `why`. |
| modes of convergence | p-boom-bust 5 | Correct: almost sure convergence is argued for every $\varepsilon$, and $E[M_n^2] = 1.36^n$ rules out mean square. Simulation agrees. |
| conditional expectation, tower, projection | p-nested-forecasts, p-trial-stake 1 | Correct. $E[X \mid \mathcal G]$ is given atom by atom as a random variable; tower and Pythagoras hold exactly in fractions. |
| martingales and optional stopping | p-doob-split, p-two-ups-stop, p-trial-stake | Correct. Every use states a bounded stopping time. $M = S^2 - A$ was checked as a martingale at every node; $E[S_T] = 0$ and $E[S_T^2] = E[T]$ by enumeration of 16 paths. |
| Radon-Nikodym and change of measure | problems-4, all four problems | Correct. Absolute continuity is stated where a weight is formed; the direction of each ratio is right; $E_Q[Z_3] = 1$ and positivity are both asked for equivalence; the share-measure price agrees with direct pricing to $10^{-10}$. Finding 2 is a loose use of "density". |

Monte Carlo and simulation checks (seed 20261126):

| claim | check | result |
|---|---|---|
| a uniform pick lands in the fat Cantor set with chance $\tfrac12$, not 0 | 2,000,000 picks against $C_{22}$ | 0.4998 |
| quote ladder: $P(N = 2)$, $P(N \in 3\mathbb{Z})$, $P(X \le 2U)$ | 2,000,000 draws | 0.0962, 0.6409, 0.8328 |
| $P(D_{200})$ from the recursion | 40,000 digit strings | 0.1612 against 0.1599 |
| the law of $N$ is negative binomial; $E[N]$, $E[N^2]$, $E[1.25^N]$ | 2,000,000 draws | 0.4998, 0.8752, 1.1378 |
| $|G_n| \le e^{|R|}$ on every draw; $G_1 < 0$ on 2.3% of draws | 1,000,000 draws, $n = 1, 2, 3, 7, 50$ | holds |
| $E[G_n]$ rises to $e^{1/8}$ | quadrature, $n = 2, 4, 50, 400$ | 1.0625, 1.0945, up to 1.1327 |
| $P(M_n > 0.01$ for some $n \ge 200)$ is under 0.00518; $M_n \to 0$ | 20,000 paths of 600 days | 0.00005; under $10^{-6}$ on over 99.9% of paths |
| $E[M_{10}^2] = 21.65$ with $E[M_{10}] = 1$ | 4,000,000 paths | 21.68, 1.0008 |
| reverse sampler is unbiased, its mean square has no finite limit, its error does not shrink like $1/\sqrt n$ | 4,000,000 draws from $Q$ | mean weight 1.0008; block mean squares 1.60, 2.80, 4.12; $\sqrt n$ times spread 7.14 to 8.34 |
| ten trades: unbiased, relative error 1.12, about 14 plain draws per weighted draw | 4,000,000 draws each | 0.05472, 1.1224, 13.73 |

## Findings

1. `problems-2.json` | `items[3].parts[1].widget.options[2].why` (`p-random-maturity` part 2, option `none`) | `imprecise`, `minor` | "the swap needs one integrable bound on all the quotients at once" states a sufficient condition as a necessary one. | Dominated convergence gives the swap when such a bound exists; the exact condition is uniform integrability (Williams 13.7), and a swap can hold with no single dominating variable. The key and the other options are right. | Replace the `why` with: "Smooth paths are not enough on their own. Dominated convergence asks for one integrable bound on all the quotients at once."

2. `problems-4.json` | `items[0].parts[2].explain.text` (`p-recovery-reweight` part 3) | `imprecise`, `minor` | "Every density has $P$-mean 1" is true of the weight $\tfrac{dQ}{dP}$ only. The stem uses "density" for $2x$ and $4x^3$, and those have $P$-means $\tfrac43$ and $\tfrac85$. | $E_P\big[\tfrac{dQ}{dP}\big] = Q(\Omega) = 1$ (Williams 5.14); $\int_0^1 2x \cdot 2x\,dx = \tfrac43$. The key $\tfrac13$ is right. | Replace the text with: "The weight $Z = \tfrac{dQ}{dP}$ has $P$-mean 1, as $Q$ has total mass 1. So the variance is $E_P[Z^2] - 1$, and $E_P[Z^2] = \int_0^1 8x^5\,dx = \tfrac86$. The variance is $\tfrac43 - 1 = \tfrac13 \approx 0.3333$."

3. `problems-1.json` | `items[0].parts[3].widget.options[1].why` (`p-fat-cantor` part 4, option `noint`) | `imprecise`, `minor` | The option makes two claims: $C$ is null, and every null set of $[0, 1]$ is an event. The `why` refutes the first and leaves the second standing. | With the Borel events the keyed answer uses, the second claim is false: the middle-thirds Cantor set is null with $2^{\mathfrak c}$ subsets, and there are only $\mathfrac c$ Borel sets (Billingsley, section 3). It holds only after completing the measure. The option is wrong under either convention, since $C$ has length $\tfrac12$. | Replace the `why` with: "$C$ holds no interval, yet its length is $\tfrac12$ by part 3, so it is not null. Nor is every null set Borel. The reason lies in how $C$ is built."

## Checked and left alone

- `p-settlement-fails` part 2, option `fatou`: Fatou with the bound $Ns^{N-1} \le N$ does give the equality, but the option claims Fatou alone turns the limit into an equality, which is false as stated.
- `p-recovery-reweight` part 4, "the error does not shrink like $\tfrac{1}{\sqrt n}$": the weight has tail $P_Q(W > w) = \tfrac{1}{4w^2}$, so the error shrinks like $\sqrt{\log n / n}$. The sentence is right, and the simulation shows the slow growth.
- `p-compounding` part 2, slip `fourth-one` (1.094): a learner who gives the right answer to 3 places meets this line. The part asks for 4 places, so no finding.
- `p-ten-trades` part 2, slip `eight-only` stored as 0.006395 with band $5 \times 10^{-6}$: the value typed at 5 places (0.00639) sits on the band edge and is caught in floating point. Band width is an earlier read's topic (`review-pass9-hits`), not a concept.
- `p-premium-weight` part 4, "any traded price": true for an asset with no payout over the step, which is the only kind in the course.

## Overlap with earlier reads

Earlier reads opened after the ledger was written: `docs/reviews/review-problems-measure-prob-1-3.md`, `review-problems-measure-prob-4.md`, `review-delta-ag-measure-prob.md` (each with its fix pass), the measure-prob lines of `review-delta-ah.md` and `review-pass9-hits.md`, and `docs/reports/problems-measure-prob.md`. `audit-measure-prob-1-3.md` and `audit-measure-prob-4.md` do not cover the problem sets.

Conceptual findings only (reuse, continuity, band and layout findings are left out):

| found by | count | which |
|---|---|---|
| this audit only | 3 | findings 1 to 3 above |
| earlier reads only | 6 | first read 9 (sign of the quotient in p-random-maturity part 2); delta read 5 (almost sure limit from one $\varepsilon$), 6 ($s^{N-1}$ at $N = 0$), 7 (sets "are uncountable"), 9 (option `dct` true as worded); problems-4 read 1 (two-step tree not given). All six were fixed before this audit, and each fix was read here as a ledger row and is correct. |
| both | 0 | |

New `wrong` found by this audit: 0.

## Tool results

| check | result |
|---|---|
| `docs/reports/measure-prob-problems-concepts.py` (venv Python, NumPy and SciPy newer than CI's pins; no figure depends on the version) | 590 checks, 0 failed, exit 0 |
| `node tools/validate.mjs` | 0 errors, 4615 warnings |
| `node tools/run-number-scripts.mjs --only measure-prob` | 8 scripts, 8 passed, 0 new failures |
| `node tools/grade-all.mjs --file` on problems-1 to problems-4 | 19, 19, 18 and 18 widgets, 0 failures each |
| playthrough | not run (auditor rule) |

Inbox: no engine limit was met, so no bullet was added to `docs/BACKLOG-INBOX.md`.

## Fix pass

Opus fixer, from commit 4ee62e13. Only the three `why`/`explain` strings were edited. No key, slip, tolerance or test changed.

1. Fixed (auditor's text). Basis: dominated convergence (Williams 5.9) needs $|f_h| \le Y$ integrable, but that is only sufficient for swapping limit and mean; uniform integrability is the exact condition (Williams 13.7). Own example: $X_n = \tfrac{n}{\log n}$ on $[\tfrac1{n+1}, \tfrac1n)$ is uniformly integrable with $E[X_n] \to 0$, yet $E[\sup_n X_n] = \sum \tfrac{1}{(n+1)\log n} = \infty$, so no single bound dominates. The new `why` names the hypothesis of dominated convergence, which is what the stem asks for.
2. Fixed (auditor's text, joined into three sentences). Basis: $E_P[\tfrac{dQ}{dP}] = Q(\Omega) = 1$, while the stem's densities have $E_P[2X] = \tfrac43$ and $E_P[4X^3] = \tfrac85$ (SymPy). Recomputed twice: $E_P[Z] = \int_0^1 4x^3\,dx = 1$, $E_P[Z^2] = \tfrac43$, variance $\tfrac13$; Monte Carlo with 4,000,000 draws gives mean 0.99996 and variance 0.33332.
3. Fixed differently. The course uses "null set" for a set of chance 0, under which "every null set is an event" is true by definition, so the auditor's "Nor is every null set Borel" would contradict the course's own usage. The new sentence says "Nor does being small make a set an event: a subset of a null set need not be Borel." Basis: the middle-thirds Cantor set is Borel, null and of size $\mathfrak c$, so it has $2^{\mathfrak c}$ subsets, while the Borel sets number only $\mathfrak c$; every such subset is measurable only after completion.

Gates: validator 0 errors; voice scan 35 at 0 and 0 on the three files; `measure-prob-problems-concepts.py` 590 checks, exit 0 (no check encodes the old text, so nothing re-pointed); number scripts 8 of 8 passed; `grade-all.mjs --file` 0 failures on problems-1, 2 and 4; playthrough `--problems` of problems-1, 2 and 4 green desktop and `--mobile`.
