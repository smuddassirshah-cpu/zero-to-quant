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

## Level 4 (second author, `problems-4.json`)

Numbers: `level4()` in `docs/reports/problems-stat-models-numbers.py` (359 checks; the whole script 962 of 962, exit 0). Method 1 is exact fractions and the conjugate formulas. Method 2: a grid posterior built from 36 planted daily figures, a log posterior summed over 8 planted weekly counts, scipy's distributions, Nelder-Mead on the marginal likelihood, a hand Metropolis step, quadrature over the shrinkage posterior, the finite-n AR(1) variance of a chain mean and a simulation of 400 runs of four chains. Every `wrong` value is rebuilt from its slip; every printed number has a `shown` check.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-etf-tracking | 4 (4 / 0) | l14, l15 | 4 |
| problems-4 | p-circuit-breaker | 4 (4 / 0) | l14, l16 | 3 |
| problems-4 | p-quality-six-markets | 5 (5 / 0) | l18, l14 | 5 |
| problems-4 | p-dealer-enquiries | 5 (4 / 1) | l18, l14, l17 | 4 |

Every lesson of level 4 appears; each problem draws on two or more. Skills `sm-bayes`, `sm-mcmc`, `sm-hier`. Typed parts 17 of 18; the choice part is the judgement on a sampler that misses the closed form by 3.21 Monte Carlo errors.

Gates: validator 0 errors, 4571 warnings (the baseline; none on this file). Voice scan 35: 0 and 0. `fresh-check --file`: 0 hits. `grade-all --file`: 18 widgets, 0 failures. Playthrough `--problems stat-models/problems-4 --local-cdn`: green desktop and `--mobile`; part shots at 440 px read, no overflow.

Hand reuse check. Grepped the course folder for every key and printed number (0.1562, $-0.5029$, 0.3700, 0.0896, 5.1765, $-0.7859$, 0.4557, 0.46, 0.21, 0.5435, 0.3978, 0.3378, 0.8805, 0.0627, 0.00140, 3.21, Gamma(44, rate 8.5), Beta(7, 13), Beta(24, 36), 17 of 40): no hit beyond digits inside longer numbers. Beta(7, 13) was chosen over Beta(6, 14), which is twice review-4's Beta(3, 7). Stories grepped across `app/content/`: ETF tracking difference, circuit breaker, quality signal in six markets, bond dealer's price enquiries: no other file. Lines rewritten while drafting because they echoed taught lines: "Precisions add: ..." (l14 S6), "sits between the prior mean and the MLE" (l14 S0), and "That is $n(1 - \phi)$. Divide by $1 + \phi$ as well." (l17 S4 byKey).

| problem | closest lesson screen | closest review | closest homework | closest exam item (topic-2.6) | why not a walk-through |
|---|---|---|---|---|---|
| p-etf-tracking | l14 S6 (alpha, normal prior, posterior mean); l15 S1 (predictive variance adds the doubt) | r-4 item 6 (shrunk alpha) | hw-4 item 6 (posterior sd by precisions) | e-alpha-prior (one normal update) | Course items update a single estimate; here the error comes from 36 days, and the posterior feeds a normal predictive for a 20-day average and its tail, which no item does (the course's predictives are beta-binomial and negative binomial). |
| p-circuit-breaker | l14 S3 (Gamma update); l16 S1 (hand steps on Beta(15, 35)) | r-4 item 3 (one step on a standard normal) | none close | e-default-rate (Gamma mean); e-metropolis-log (log posteriors given, one step) | The log ratio is built from the learner's own Gamma posterior kernel, $43\ln\lambda - 8.5\lambda$, then turned into the accepting threshold for $u$. One step only, not the lesson's table of four. |
| p-quality-six-markets | l18 S4 (ten alphas, $\hat\mu$, $\hat\tau$ given by an optimiser); l14 S4 (precisions) | r-4 item 6 | hw-4 item 6 | e-alpha-prior | The learner fits $\hat\tau^2$ in closed form from equal errors (MLE of the total variance less the noise), which no item does, then carries $B$ into a shrunk mean and a posterior chance that a loss-making backtest has a positive true mean. |
| p-dealer-enquiries | l18 S1 and S2 (weight, shrunk rate); l17 S4 (ESS from $\phi$); l14 Q1 (Beta sd) | r-4 item 8 (shrunk rates) | hw-4 item 4 (record length) | e-hit-rate-shrink (weight then shrunk rate); e-ess-sticky (ESS) | The chain checks MCMC code against the closed form: posterior sd, Monte Carlo error of pooled AR(1) chains, the gap in error units and the verdict. No item puts a Monte Carlo error against an exact posterior mean. |

Problems of sets 1 to 3 that are being re-authored (p-venue-markouts, p-rerun-the-test, p-ten-trading-days, p-block-markout-tail, p-auction-tails) share no story or number with this set.

Waived or open: nothing. No engine limit met; no backlog bullet.
