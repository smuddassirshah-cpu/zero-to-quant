# Topic exam items and Option B skills for the four syllabus-hole levels

Brief: the main session's task of session AB (rulings 1 and 6 of `docs/briefs/gap-syllabus-holes-course-json.md`). Five commits in the worktree: `df46f5b` (number-sense, topic-0.1), `b7cf653` (quadratics, topic-0.2), `d53ec18` (testing, topic-1.6), `4c374ab` (topic-0.1, fresh numbers for one item), `5506967` (stat-learning, topic-2.1). `manifest.json` is not committed.

## Self-check

| Check | Result |
| --- | --- |
| `node tools/validate.mjs` | 0 errors, 4664 warnings, the same count as before the work; no warning on any new item. The exam warnings that remain are on older items (topic-0.2 `e-formula`, `e-gap-table`; topic-1.6 `s-welch`, `s-overlap-hac`, `s-vol-annual`; topic-2.1 `e-rf-variance`). |
| `node tools/test-exam-minutes.mjs` | All passed (56 exams) |
| `node tools/readiness-sums.mjs` | run with `--write` after topic-0.1 and topic-0.2 (exam minutes moved), and after topic-1.6; OK |
| Number scripts | `docs/reports/exam-0.1-holes-numbers.py` 90 of 90, `exam-0.2-holes-numbers.py` 58 of 58, `exam-1.6-holes-numbers.py` 90 of 90, `exam-2.1-holes-numbers.py` 72 of 72; each exits 0 (scratchpad venv; NumPy 2.5.4, SciPy 1.18.1, scikit-learn 1.6.1 installed into it, as it was empty) |
| Playthrough, exams | `--exam topic-0.1`, `topic-0.2`, `topic-1.6`, `topic-2.1` with `--local-cdn`: all passed, desktop and `--mobile` (29/29, 30/30, 30/30, 30/30). 440 px screenshots of every new item read: no overflow or clipping. |
| Playthrough, re-tagged files | number-sense l17 to l19, review-4, homework-4; quadratics l14 to l17, review-4, homework-4; testing l13 to l18, review-4, homework-4; stat-learning l15 to l18, review-4, homework-4: all passed |
| Voice scan 35 | exams folder 0 and 0; number-sense, quadratics, stat-learning 0 and 0; testing reports 1 sentence over 35 words, in `homework-3.json` item 8 (not touched here) |
| Fresh-check | gate run (`--exam <id>`): 0 hits on all four exams. Triage run (`--min-run 8 --min-share 0`): one hit on a new item, below |

## Skills added (`course.json`, each course now at 6)

| Course | Skill | Lessons re-tagged | Review-4 and homework-4 items re-tagged |
| --- | --- | --- | --- |
| number-sense | `ns-measures` Measures and averages | l17, l18, l19 to `[ns-measures]` | r-l-shape, r-triangle, r-circle-14, r-54, r-freq-mean, r-remove; h-semicircle, h-speed, h-freq, h-leaver, h-long-leaflet |
| quadratics | `quad-rational` Surds, algebraic fractions and polynomials | l14, l15, l17 to `[quad-rational]`; l16 to `[quad-rational, quad-solve]` | r4-surd-sum, r4-conjugate, r4-cancel, r4-add, r4-remainder, r4-factor-cubic; r4-reject with quad-solve; hw4-surd-form, hw4-cubic-root, hw4-two-factors; hw4-fraction-equation and hw4-find-the-errors with quad-solve |
| testing | `ht-theory` Estimation theory; `ht-likelihood` Likelihood-ratio and chi-squared tests | l13 to l16 to `[ht-theory]`; l17 to `[ht-likelihood]`; l18 to `[ht-likelihood, ht-pvalue]` | ht-theory: r-gamma, r-suff-sigma, r-se-hit, r-eff, r-rb-exp, r-param, h-rb-zero, h-mom-negative, h-eff-min, h-two-forms, h-cr-poisson; ht-likelihood: r-lrt-coin, r-np, h-lrt-exp, h-np-normal; with ht-pvalue: r-chi-23, h-gof-code; h-analyst both new skills |
| stat-learning | `sl-flexible` Margins, clusters, networks and splines | l15 `[sl-flexible, sl-classify]`, l16 and l17 `[sl-flexible]`, l18 `[sl-flexible, sl-linear]`; l19 unchanged | r-street-width, r-gamma-tie, h-margin-table, h-rbf-decision with sl-classify; r-kmeans-2d, r-linkage, r-forward, r-params, h-dendro-cuts, h-kmeans, h-net-count, h-derive-linear; r-spline-value, r-additive-blind, h-spline-df, h-additive-cols with sl-linear; h-cluster-story with sl-setup |

Every skill of the brief fitted; none was left out. The old placeholder tags were dropped where they were placeholders and kept where the lesson really uses them (quad-solve on l16, ht-pvalue on l18, sl-classify on l15, sl-linear on l18). Every older skill is still used by an earlier lesson. Each exam's `skills` map gained the new skill(s).

## topic-0.1 (23 to 29 items, 50 to 65 minutes)

Added six items, one per level 4 lesson plus a units item; ramp 6, 15, 5, 3 (21%, 52%, 17%, 10%). Minutes follow the pace sum (45.5 to 60.3 min) with the same tenth of slack as before.

| Item | d | Skill | Lesson | Key | Route 1 | Route 2 |
| --- | --- | --- | --- | --- | --- | --- |
| e-feed-updates | 2 | ns-measures | l18 (units) | 351,000 | $15 \times 3600 \times 6.5$ | count second by second |
| e-prime-table | 3 | ns-powers | l15 | 127 and 149 prime | trial division to the root | sieve of Eratosthenes |
| e-plan-hall | 3 | ns-measures | l17 | 234 m² | $18 \times 13$ | plan area $58.5 \times 2^2$ |
| e-pit-area | 3 | ns-measures | l18 | 199 m² | $\pi(50/2\pi)^2 = 198.94$ | $C^2/4\pi$; also 199 with $\pi = 3.14$ (199.04) and $22/7$ (198.86) |
| e-partner-number | 4 | ns-powers | l16 | 56 | $8 \times 168 \div 24$ | search 1 to 2000 for HCF 8, LCM 168 with 24: only 56 |
| e-five-counts | 5 | ns-measures | l19 | 3 | median, mode, mean, range argument | every sorted 5-tuple of 0 to 40: only (3, 8, 9, 10, 10) |

Wrong values (each the named slip, outside the band, with a line): 5,850 (×60 once), 97.5 (per hour), 324,000 (6 h); 117 (scaled once), 58.5 (plan area), 62 (perimeter); 796 (diameter as radius), 1963 (half the distance round as radius), 7854 (distance round as radius); 1344, 7, 192; 2 (median minus range), 11 (sum of the two smallest), 8 (second count). Primes: 119 = 7 × 17, 133 = 7 × 19, 143 = 11 × 13, 161 = 7 × 23.

## topic-0.2 (27 to 30 items, 65 to 75 minutes)

Added four, replaced one: **`e-one-root`** (d3, quad-solve: one root when $b^2 - 4ac = 0$). It adds least: `e-tangent-line` (d5) asks the same discriminant-zero step inside a harder problem, and quad-solve stays on five other items. Three additions alone could not give four level 4 items under the cap of 30. With `e-tangent-line`, which is l19 material already (a line tangent to a parabola), level 4 now has five items over l14, l16, l17, l18 and l19. Ramp 6, 15, 6, 3.

| Item | d | Skills | Lesson | Key | Route 1 | Route 2 |
| --- | --- | --- | --- | --- | --- | --- |
| e-surd-difference | 2 | quad-rational | l14 | $3\sqrt3$ | largest square factors 25 and 4 | floating point $\sqrt{75} - \sqrt{12}$ |
| e-two-desks | 3 | quad-rational, quad-solve | l16 | 3 hours | $x^2 - x - 6 = 0$ by the formula, reject $-2$ | exact search over tenths in $[-10, 10]$: solutions $-2$ and 3 |
| e-diameter-ends | 3 | quad-graph | l18 | centre (1, 10), radius 10 | midpoint and half of $\sqrt{12^2 + 16^2}$ | both ends on $(x-1)^2 + (y-10)^2 = 100$; (9, 4) on it sees the diameter at a right angle |
| e-cubic-remainder (parts) | 4 | quad-rational | l17 | $k = 3$; $(x-2)(x+2)(x+3)$ | $p(1) = k - 15 = -12$ | synthetic division scanned over integer $k$; expansion of the brackets; integer root search |

Wrong values: $\sqrt{63}$, $7\sqrt3$, $21\sqrt3$; $-2$ (kept root), 0.5 (tops and bottoms added), 6 (desk B); 6, 8 (half gaps), 20 (diameter); 15 ($p(1) = 0$), $-3$ ($p(-1)$), $(x-2)(x+2)(x-3)$ ($p(3) = 30$).

## topic-1.6 (27 to 30 items, 60 to 70 minutes)

Added four, replaced one: **`s-summary-dw`** (d3, rg-diagnostics: tap the Durbin-Watson line). It repeats `s-residual-plots`, which already shows Durbin-Watson $d = 0.34$ and asks what autocorrelated residuals mean; rg-diagnostics stays on `s-residual-plots` and `s-overlap-hac`. Without it three additions could not give four level 4 items. Level 4 items cover all six lessons. Ramp 5, 15, 7, 3 (17%, 50%, 23%, 10%).

| Item | d | Skills | Lessons | Key | Route 1 | Route 2 |
| --- | --- | --- | --- | --- | --- | --- |
| s-uniform-moments | 3 | ht-theory | l13 | 0.60 | $\sqrt{3 \times 0.12}$ | root-finding on SciPy's uniform second moment; simulation; the central-moment route 0.599 lies in the band |
| s-chi-order-mix (parts) | 3 | ht-likelihood, ht-pvalue | l18 | $X^2 = 5.23$ on 2 df; keep the model | $1.96 + 3.27$ | `scipy.stats.chisquare`; p $= e^{-x/2} = 0.073$ against `chi2.sf`; cut-offs 3.841, 5.991, 7.815 from `chi2.ppf` |
| s-pool-rates | 4 | ht-likelihood | l17 | $-2\ln\Lambda = 6.04$ on 1 df | $2[90\ln1.2 + 60\ln0.8]$ | SciPy Poisson log-likelihoods with the shared rate fitted numerically (75); simulated size 0.05 at 3.841 over 200,000 null pairs |
| s-pareto-losses (parts) | 4 | ht-theory | l14, l15, l16 | $\sum\ln x_i$; $\hat\alpha = 2.5$; bound 0.078125 | factorisation; $n/\sum\ln x$; $\alpha^2/n$ with $I = 1/\alpha^2$ | equal $\sum\ln x$ gives an $\alpha$-free likelihood ratio; numeric maximisation; numerical second derivative; simulated variance of the MLE over 20,000 samples |

Wrong values: 0.36, 0.3464, 0.04; 4.93 (divided by O), 392 (no division), 3 df; 3.02 (no factor 2), 6.00 (Pearson), $-6.04$, 2 df; 0.4, 1.5; 0.2795 (sd), 12.8 ($nI$), 0.03125 ($\alpha/n$).

## topic-2.1 (30 items, 90 minutes unchanged)

Replaced five items with one per level 4 lesson; ramp unchanged at 6, 15, 6, 3, and every skill still covered (the number script checks each of the thinned skills keeps at least two items).

| Replaced | d | Why it adds least |
| --- | --- | --- |
| e-leak-rows | 3 | the same "tap what leaks" task as `e-lookahead-lines`; vl-leakage keeps four items, vl-time seven |
| e-oob-overlap | 3 | vl-time is the most covered skill (eight items before); en-bagging keeps `e-importance-claims` and `e-rf-variance` |
| e-odds-update | 3 | sl-classify keeps four items (`e-precision-recall`, `e-kelly-wrong`, `e-code-honest-report`, `e-honest-t`) and gains `e-street-inside` |
| e-ridge-shrink | 3 | sl-regularise keeps four items, including the ridge code item `e-code-ridge-inter` |
| e-walk-first-test | 2 | `TimeSeriesSplit` mechanics; vl-time and vl-cv stay on `e-fit-count`, `e-code-purged-roll`, `e-code-honest-report` and others |

| Item | d | Skills | Lesson | Key | Route 1 | Route 2 |
| --- | --- | --- | --- | --- | --- | --- |
| e-spline-slope | 2 | sl-flexible, sl-linear | l18 | 2.5 bp a year | $-1 + 2 + 1.5$ | least-squares slope of evaluations past 7 |
| e-street-inside | 3 | sl-flexible, sl-classify | l15 | (0.2, 0.9), (−0.5, 0.5), (−1, −1.4) | decision values 0.5, −0.5, 0.4 in $(-1, 1)$ | signed distance under $1/\lVert w\rVert$ |
| e-kmeans-spreads | 3 | sl-flexible | l16 | 91 | hand Lloyd loop, centres 2 and 11.33, 2.5 and 13, 4 and 14.5 | scikit-learn `KMeans` from the same start; best split of the sorted spreads by brute force |
| e-unit-gradient | 3 | sl-flexible | l17 | $-2.4$ | $(\hat y - y) v x_2$ | central finite difference |
| e-report-which | 3 | sl-setup, sl-tradeoff | l19 | 0.63 | arg max of validation, its test score | sort by validation; distractors 0.67, 0.72, 0.6525 recomputed |

Wrong values: 1.5, 3.5, 4.5; 122.5 (stopped at 2.5 and 13), 21 (unsquared); −0.8 ($x_1$), −0.12 ($\partial L/\partial v$), 2.4 (sign), −4.8 (no ½).

## Freshness

Gate run: 0 hits on all four exams. Triage run: one hit on a new item, `s-pareto-losses` against testing l16 quiz 2, the shared phrase "what is the Cramér-Rao bound for" (share 0.14). Judged a question form, not a copy: a Pareto model, a sample of 80 and $\alpha$ appear nowhere in the course. I also compared the numbers in each new item with every screen and item of its course (scratchpad script). Two real overlaps were fixed: `e-partner-number` first used 36 and LCM 180, the numbers of review-4 `r-lcm-36-60`, now 24, HCF 8, LCM 168. `e-report-which` first used accuracies 0.55 to 0.61, the range of homework-4 `h-pick-learner`, now 0.63 to 0.72 with no value in common. The rest are small integers or axis labels. Settings checked against each course: no feeds, coupons, clips, fences, ponds, desks' trade-count days (number-sense); no share-hook, tilted squares or subscription (quadratics); no exponential gaps, Gamma sizes, weekday counts or venues' fills (testing); no loans, six-share volatilities, rings or impact data (stat-learning).

## Derived figures that moved

- Census: unchanged (exams 49, topic exams 29, items 20 to 30). Topic exam items: 0.1 23 to 29, 0.2 27 to 30, 1.6 27 to 30, 2.1 30.
- Exam minutes: topic-0.1 50 to 65, topic-0.2 65 to 75, topic-1.6 60 to 70, topic-2.1 90.
- `readiness-sums.mjs --write` (from the exam minutes): trader required outside hours 953 to 952, header 1,441 to 1,440; researcher required in the app 324 to 325 and outside 1,329 to 1,328, header 499 to 500 and 2,261 to 2,260; developer required outside 560 to 559, recommended 685 to 684, header 1,245 to 1,243; undecided required and header in the app 154 to 155. Lesson counts do not move.
- Skill counts: the four courses now hold 6 skills each, the validator's maximum.

## Notes for the main session

- `topic-0.2` and `topic-1.6` each needed one replacement to reach four level 4 items within 30; the brief asked for additions only. Both replaced items are named above with the reason.
- No engine limitation met; no `BACKLOG-INBOX.md` bullets.
- `stage-0`, `stage-1` and `stage-2` were not touched (the brief allows one or two items each later).
