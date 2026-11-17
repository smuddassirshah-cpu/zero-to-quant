# Problem sets: stat-models levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/stat-models/problems-1.json` to `problems-3.json`. Level 4 has its own author. Numbers: `docs/reports/problems-stat-models-numbers.py` (676 of 676 checks, exit 0). Second read: `docs/reviews/review-problems-stat-models-1-3.md`; its fix pass (session AF) re-authored five problems and applied the line fixes. The reader's script `problems-stat-models-numbers-read.py` exits 0 with 0 FINDING lines.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-ipo-underwriter | 4 (4 / 0) | l2, l5 | 4 |
| problems-1 | p-settlement-fails | 4 (4 / 0) | l3, l4, l5 | 5 |
| problems-1 | p-recon-breaks | 4 (4 / 0) | l3, l4, l5 | 4 |
| problems-1 | p-rfq-busy-minutes (new) | 5 (4 / 1) | l1, l5 | 4 |
| problems-2 | p-signal-variants (new) | 5 (5 / 0) | l6, l7 | 4 |
| problems-2 | p-twin-books | 4 (4 / 0) | l8, l9 | 5 |
| problems-2 | p-two-looks (new) | 4 (4 / 0) | l7, l9 | 4 |
| problems-3 | p-hedge-ranks (new) | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-spread-day-tail (new) | 4 (4 / 0) | l12, l13 | 5 |
| problems-3 | p-five-weeks-flip | 4 (3 / 1) | l11, l13 | 3 |

Every lesson of each level appears; every problem draws on two or more. Skills: `sm-glm`, `sm-anova`, `sm-nonpar`. Typed parts 16/17, 13/13, 11/12. The two choice parts are judgements (which variance function; why the median's $p$ exceeds the mean's). Every $F$ or $t$ tail a part needs is now given in it (the $t_{119}$ tail in p-twin-books, the $t_{48}$ critical value in p-signal-variants); the $\chi^2_1$ tail of p-ipo-underwriter keeps the course's precedent (r5-lr, l5 Q1 ask such tails with no tool).

## Checks

1. Number script: 676 of 676, exit 0. New routes: statsmodels variance functions and simulated negative binomial minutes; an OLS on rows built to hold the six variant means and SSW, its dummy-coefficient standard error, root finding for the Bonferroni $t$; all 1,024 win patterns and a simulation of the two-look plan; all 4,096 sign patterns of the ranks, a Walsh-average count for $W^+$ and scipy's `wilcoxon`; `quad` of the kernel estimate. Each `wrong` value is rebuilt from its slip; each printed number has a `shown` check.
2. Validator: 0 errors; one warning on these files, a long sentence in the reader's replacement explain of p-five-weeks-flip part 4 (kept exactly, under the 35-word gate).
3. Playthrough `--problems stat-models/problems-<n> --local-cdn <pkgs>`: green for all three, desktop and `--mobile`. Part shots at 440 px read: no overflow.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file`: 17, 13 and 12 widgets, 0 failures.
6. `fresh-check --file`: 0 hits on each set. Advisories: the logit (l2 S3), 95 and 1.96 (l2 S7), $\mu + \alpha\mu^2$ (l5 S6, the taught NB2 variance), $z_{0.975}$, $z_{0.8}$ and 80% (l8 S2), $1.06\,s\,n^{-1/5}$ (l12 S5). Taught formulas and constants, used with each problem's own numbers.

## Closest material to the new problems

| problem | closest lesson screen | closest review, homework, exam | why not a walk-through |
|---|---|---|---|
| p-rfq-busy-minutes | l1 S5 (variance over mean of fills); l5 S6 (NB2 variance at one mean) | r6-overdisp, l5 Q2 (is Poisson reasonable); r9-quasi | Both variance functions are matched to one regime by moments, then carried to a second mean, where they part; the course never fits two variance functions to the same counts or predicts with them. Own setting (RFQs per minute), own numbers. |
| p-signal-variants | l6 S4 (mean squares); l7 S7 (pairs by Bonferroni from a $p$ table) | r2-bonf (per-test threshold); e-algo-f | No item turns MSW into the standard error of a pairwise gap or a least significant gap; no SSB, no $F$ from sums, no coefficients to means. Six groups of 9, a carry signal's variants, not brokers, algorithms or venues. |
| p-two-looks | l9 S5 (sign test, binomial $p$); l9 S7 (peeking, simulated); l7 S6 (chance one of three tests rejects) | r2-peek, l9 Q1, e-sign-test-ties | Counts the false-alarm rate of a two-look sign test exactly over 1,024 patterns and against Bonferroni's bound; the course only simulates peeking and reasons about it. Own setting (curve models). |
| p-hedge-ranks | l10 S5 ($W^-$ of three losing days); l10 S7, Q0 (ties) | h-mw-z, h-u-moments (normal approximation of $U$) | Signed-rank with a tie, its null SD from the sign-flip view, $z$ and a one-sided $p$; the course approximates $U$, not $W$, and never derives a rank statistic's SD from the flips. No $U$, no splits, no doubling, no plus-one. |
| p-spread-day-tail | l13 S3 (scaled MAD); l12 S5 (rules from $s$); l12 S7 (mass below 0) | e-takeover-week, r3-silver, e-silverman-250 | Kept chain of the old problem (robust spread into the rule, kernel share below a cut, ratio to a robust normal fit) on new data: eight values, an even-count median, two unusual days on both sides, a cut at $-4$ for changes that may be negative. |

Each new problem's key numbers were grepped in `app/content/courses/stat-models/` and each story in `app/content/`: no other hit beyond `markov/problems-2` p-rfq-rounds (RFQ rounds in a Markov chain, another course and task).

## Waived or open

Nothing waived: fresh-check reports 0 hits.

Nothing waived: fresh-check reports 0 hits. No engine limit met; no backlog bullet.

## Level 4 (second author, `problems-4.json`; re-author and fix pass after `review-problems-stat-models-4.md`)

Numbers: `level4()` in `docs/reports/problems-stat-models-numbers.py` (471 checks; the whole script 1074 of 1074, exit 0). Method 1 is exact fractions and the conjugate formulas. Method 2: a grid posterior built from 36 planted daily figures and from 36 planted refill gaps, scipy's log densities, Nelder-Mead on the marginal likelihood, two million simulated first steps of the iceberg sampler, a run of the four-books Gibbs sampler (lag-1 autocorrelation and sd of $\mu$), the joint precision matrix of $(\theta_1, \dots, \theta_4, \mu)$, the exact finite-$n$ AR(1) variance of a chain mean and a brute search for the run length. Every `wrong` value is rebuilt from its slip; every printed number has a `shown` check, the six normal-table values of finding 10 included. The reader's `problems-stat-models-4-numbers-read.py` exits 0 (153 checks): its blocks for the two re-authored problems and their replacement-text checks are removed, and two checks now confirm the old ids and the claim of finding 9 are gone.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-etf-tracking | 4 (4 / 0) | l14, l15 | 4 |
| problems-4 | p-iceberg-refills (new) | 4 (4 / 0) | l14, l16 | 4 |
| problems-4 | p-quality-six-markets | 5 (5 / 0) | l18, l14 | 5 |
| problems-4 | p-four-books (new) | 5 (5 / 0) | l18, l17, l14 | 5 |

Every lesson of level 4 appears; each problem draws on two or more. Skills `sm-bayes`, `sm-mcmc`, `sm-hier`. Typed parts 18 of 18.

Gates after the fix pass: validator 0 errors, no warning on this file. Voice scan 35: 0 and 0. `fresh-check --file`: 0 hits. `grade-all --file`: 18 widgets, 0 failures. Playthrough `--problems stat-models/problems-4 --local-cdn`: green desktop and `--mobile`; part shots at 440 px read, no overflow.

Hand reuse check of the new problems. Grepped the course folder for every key and printed number (2.5, 2.5625, 2.5714, $-0.4632$, $-0.5741$, 0.6293, 0.5632, 0.5962, 1.1925, 0.0132, 0.8, 0.72, 0.5538, 1627.9, 407.0, 2195.1, 0.8964, 0.0222, 12,300, Gamma(5, rate 2), Gamma(41, rate 16)): no hit beyond canvas coordinates (0.72 in l17 and l18 plots) and "rate 16" in l14 S5's swapped Gamma(7, rate 16). Inside the set, p-four-books shares only the scale 1.5 with p-etf-tracking (a prior sd there, a daily sd here). Stories grepped across `app/content/`: an iceberg order's refill gaps and four market-making books: no other file. Lines reworded while drafting because they came near a course line: "neighbouring draws repeat each other" (`e-ess-sticky`), "one over each variance" (l14 S4), "The prior has precision ... and the estimate ..." (`e-alpha-prior`).

| problem | closest lesson screens | closest review, homework | closest exam item (topic-2.6) | why not a walk-through |
|---|---|---|---|---|
| p-etf-tracking | l14 S4, S6 (precisions, posterior mean); l15 S1, S3, S4 (plug-in against predictive) | r4-shrink; h-post-sd | e-alpha-prior | Unchanged task; eight slip lines rewritten (findings 1 to 3) and two tails given (finding 10). |
| p-iceberg-refills | l14 S5 (kernel times kernel); l14 S3, Q2 (Gamma update); l16 S0 (height ratio); l16 S1, Q0 (steps by hand) | r4-gamma, r4-step | e-default-rate, e-metropolis-log | The posterior comes from exponential gaps, not counts, and the learner finds its peak, which no item asks. The log ratio from the learner's own kernel is the step the reader kept. No draw $u$ is given: the parts find the chance of leaving the peak over a two-point proposal and the expected drift, so the sampler is seen to explore the skewed posterior rather than sit at its top. Prior shape 5; the last part is a new result. |
| p-quality-six-markets | l18 S4, S7 (shrunk alpha); l18 Q0 ($B$) | r4-shrink, h-post-sd | e-alpha-prior | Unchanged task; four slip lines rewritten (finding 5) and the tail values given (finding 10). |
| p-four-books | l17 S3 (Gibbs chain is AR(1) with $\phi = \rho^2$); l17 S4, Q2 (ESS); l18 S7, Q0 (shrinkage weight); l14 S6 (normal update) | r4-ess, h-post-sd | e-ess-sticky, e-hit-rate-shrink | The Gibbs sampler of a hierarchical normal model: its two conditional slopes are lesson 18's $B$ and a lesson 14 precision weight, and their product is the AR(1) $\phi$ of the $\mu$ chain, which no item builds. The ESS is the one standard step, on $\phi = 0.72$ and four chains of 2,500; it feeds a Monte Carlo error and then the run length for a target error, which no item asks. No Beta update, no Beta sd, no closed form held against a chain mean, and no verdict on a sampler. |

Problems of sets 1 to 3 as they stood at the reset (`p-venue-markouts`, `p-rerun-the-test`, `p-ten-trading-days`, `p-block-markout-tail`, `p-auction-tails` were being re-authored by another agent) share no story or number with this set.

Waived or open: nothing. No engine limit met; no backlog bullet.

## Session AG: `p-hedge-ranks` re-authored on new data (KNOWN_ISSUES "session AF close", first bullet)

Delta review AF finding 5 left part 1 with twelve values and a rank sum of 8.5 beside l10 screen 5's twelve days and $W^- = 8$. The problem now has 14 months: $-2.3$, $-0.6$, 1.1, $-3.6$, $-1.4$, $-0.3$, $-2.8$, 1.9, $-1.1$, $-4.4$, $-0.8$, $-2.5$, $-1.7$, $-3.2$. Id, skill `sm-nonpar`, story and chain kept; the tie moves to ranks 4 and 5 (l10 quiz `q-ties` has 3 and 4).

| part | old key | new key | new `wrong` values |
|---|---|---|---|
| 1 $W^+$ | 8.5 | 12.5 | tie-low 12, tie-high 13, w-minus 92.5 |
| 2 SD | 12.7475 | 15.9295 ($\sqrt{253.75}$) | variance 253.75, six-divisor 31.8591 ($\sqrt{1015}$) |
| 3 $z$ | $-2.393$ | $-2.511$ | w-minus 2.511, variance $-0.158$, no-centre 0.785 |
| 4 $p$ | 0.0084 | 0.0060 (told $\Phi(2.511) = 0.99398$) | two-sided 0.0120, upper 0.9940 |

Checks. Each band takes the part's printed working ($(12.5 - 52.5)/15.9295$; $1 - 0.99398 = 0.00602$, doubled 0.01204) and refuses every `wrong` value; no key or slip is within 0.01 of a rounding tie at its places; the tail is told in part 4. Exact one-sided $p$ with the tied ranks is 73 of 16,384 (0.0045), so "at the 1% level" holds. Reuse: 12.5, 92.5, 52.5, 253.75, 15.9295, 31.8591, 1015, 2.511 and 0.99398 appear nowhere else in the course or `exams/topic-2.6.json`; 105 (the rank total, printed in part 3's explain) is also l10's rank sum for B and a topic exam SSW, the arithmetic of 14 and no shared set. `fresh-check --file` 0 hits (one advisory, the bandwidth rule, as before).

Scripts: `problems-stat-models-numbers.py` hedge block rewritten for $n = 14$ (Walsh count, all 16,384 sign patterns, told-tail bands, rounding-tie checks), 1182 checks, exit 0. `delta-review-delta-af-stat-models-numbers.py` retargeted from the 12-month data to the 14 months (counts, printed values, listing of 16,384 patterns; its reuse check now also stays quiet on $n \ne 12$), 558 checks, 0 FINDING lines, exit 0. `problems-stat-models-numbers-read.py` (339) and `problems-stat-models-4-numbers-read.py` (153) need no change, exit 0; `stat-models-L1` to `L4-numbers.py` exit 0.

Gates: validator 0 errors (one known warning, `p-five-weeks-flip` part 4); voice 35 0 and 0; `grade-all --file` 12 widgets, 0 failures; playthrough `--problems stat-models/problems-3` green with and without `--mobile`.
