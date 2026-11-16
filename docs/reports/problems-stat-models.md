# Problem sets: stat-models levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/stat-models/problems-1.json` to `problems-3.json`. Level 4 has no set yet (another author). Numbers: `docs/reports/problems-stat-models-numbers.py` (603 of 603 checks, exit 0). The sets were drafted by a first agent stopped by a restart; this pass judged each draft, rewrote the lines below, and ran every gate afresh.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-ipo-underwriter | 4 (4 / 0) | l2, l5 | 4 |
| problems-1 | p-settlement-fails | 4 (4 / 0) | l3, l4, l5 | 5 |
| problems-1 | p-recon-breaks | 4 (4 / 0) | l3, l4, l5 | 4 |
| problems-1 | p-auction-tails | 4 (4 / 0) | l1, l2 | 3 |
| problems-2 | p-venue-markouts | 4 (4 / 0) | l6, l7 | 4 |
| problems-2 | p-twin-books | 4 (4 / 0) | l8, l9 | 5 |
| problems-2 | p-rerun-the-test | 4 (4 / 0) | l7, l8 | 4 |
| problems-3 | p-ten-trading-days | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-block-markout-tail | 4 (4 / 0) | l12, l13 | 5 |
| problems-3 | p-five-weeks-flip | 4 (3 / 1) | l11, l13 | 3 |

Every lesson of each level appears; every problem draws on two or more. Skills: `sm-glm`, `sm-anova`, `sm-nonpar`, from the level's lessons. Typed parts 16/16, 12/12, 11/12. The one choice part is a judgement (why the median's p exceeds the mean's).

## Checks

1. Number script: 603 of 603, exit 0. Method 1 is closed form (fractions, the taught formula); method 2 fits statsmodels GLMs and OLS on data built to hold each stated table, runs a hand IRLS loop, enumerates all labellings and sign patterns, integrates the kernel estimate, and simulates. Every `wrong` value is recomputed from its slip and shown outside the key band and apart from the others; each printed number in feedback and explain has a `shown` check.
2. Validator: 0 errors, 4571 warnings before and after, none on these files.
3. Playthrough `--problems stat-models/problems-<n> --local-cdn <pkgs>`: green for all three, desktop and `--mobile`. Part shots at 440 px read: no overflow; the long GLM prose and the four-option choice wrap cleanly.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file` each set: 0 failures (40 widgets).
6. `fresh-check --file` each set: 0 hits. Advisories only: the logit $\ln\frac{\mu}{1-\mu}$ (l2 S3), $z_{0.975} = 1.95996$, $z_{0.8} = 0.84162$ and 80% power (l8 S2), and the rule $1.06\,s\,n^{-1/5}$ (l12 S5). All are standard constants or the taught rule, used with the problem's own numbers.

## Hand reuse check (this pass)

Lines rewritten because they paraphrased a taught line: p-ipo-underwriter p2 explain (l5 S8, saturated 0/1 model) and p4 explain (l5 S3, "drop roughly $\chi^2_1$: one coefficient added"); p-settlement-fails p3 explain (l5 S4, "keeps the coefficients"); p-recon-breaks p1 explain (l4 S7 formula line); p-auction-tails p3 feedback and explain (l1 S4, "ties its variance to its mean"); p-venue-markouts p1 byKey and explain (l7 S4, "intercept is the base mean; each coefficient is a difference"), p2 explain (l6 S1, "gives every order its broker's mean"), p4 explain (l7 S2 and l6 S7); p-twin-books p1 and p2 explain (now numbers, not the rule restated); p-rerun-the-test p4 explain (l8 S2 formula); p-five-weeks-flip prose and p3 explain (l11 S8, "symmetric about 0 under no edge"), p3 plus-one line (it repeated p-ten-trading-days). Story: "a custodian logs failed settlements" became "an operations team", as `limits-thm/problems-1` opens with a custodian's settlement fails. Grepped the course folder for every key number and letter, and `app/content/` for each story (IPO, gilt auction tails, bid-to-cover, settlement fails, reconciliation breaks, venue markouts, EUR/GBP twin books, block-trade markouts, weekly P&L): no other hit in the course.

Closest material per problem, and why it is not a walk through it:

| problem | closest lesson screen | closest review | closest homework | why not a walk-through |
|---|---|---|---|---|
| p-ipo-underwriter | l5 S8 (0/1 deviance from $\hat\ell$); l5 S3 (drop to $p$) | r2-odds (0/1 flag to odds ratio) | h-nb-lr (LR $p$ from two log-likelihoods) | Course items start from a fitted model; this one builds $\hat\beta_1$ from a 2 by 2 table, gets $\hat\ell$ cell by cell and the null deviance itself. No item chains coefficient, deviance, null deviance and test. |
| p-settlement-fails | l3 S1 (offset, rate ratio); l4 S3 (SE from $\mathbf{X}^T\mathbf{W}\mathbf{X}$) | r9-quasi (SE times $\sqrt\phi$) | h-quasi (scaled deviance $F$) | l4 S3 hands over the matrix for a logistic fit; here the learner builds it from Poisson weights equal to the group totals, then carries it through quasi-Poisson to a rate-ratio interval, which no item does. |
| p-recon-breaks | l4 S0 to S2 (logistic IRLS from zero); l4 S7 (one Poisson $z$) | r4-z (one logistic $z$) | h-irls (IRLS code) | Intercept-only Poisson IRLS, where each update reduces to $\beta + (\bar y - e^\beta)/e^\beta$, iterated to $\ln\bar y$, then a Pearson dispersion; the lesson iterates a two-coefficient logistic fit. |
| p-auction-tails | l2 Q0 (PD of one half); l2 S4 (PD at a point); l1 Q2 (Bernoulli variance) | r7-me (marginal effect) | h-fill-tick (fall in PD over a tick) | Each step is a standard task, but no item runs even-odds point, a point measured from it, its variance and the SD of a count over 12 auctions. Own model, negative slope. |
| p-venue-markouts | l7 S4 (ANOVA as regression); l6 S1 (SSB) | r2-table (F from SSB and SSW) | h-anova-summary (F from means and pooled SD, equal groups) | Starts from regression coefficients with unequal groups, so the grand mean must be weighted, and the residual standard error stands in for MSW; ends in an $F(2, 21)$ tail. The homework has equal groups, given means, no regression and no $p$. |
| p-twin-books | l8 S4 then S5 (SD of $D$, pairs needed); l9 S2 (paired $t$) | r2-sd (SD of a within-day difference) | h-var-diff (derive Var$(D)$ and pairs) | The lesson solves for the pairs given the gain; this one fixes 120 days and solves for the detectable gain, then tests real data with an observed SD that differs from the plan. Own P&L setting. |
| p-rerun-the-test | l7 S5 ($F = t^2$); l8 S2 (pairs per arm) | r2-t2 ($F$ from $t$); r2-n (orders per arm) | h-power500 (power at fixed $n$) | Computes $t$ from summaries first, reads $F(1, 78)$ for its tail, then sizes a rerun at 90% power, a quantile the course never uses. |
| p-ten-trading-days | l10 S2 (rank sum to $U$); l10 S7 (3 against 3, 20 splits); l11 S1 (count relabellings) | r3-u ($U$ from ranks) | h-u-moments (null mean and variance of $U$) | The learner counts the extreme labellings by hand ({7,8,9,10} and {6,8,9,10}) and doubles by symmetry; l10 S7 only asks for the floor of the $p$. |
| p-block-markout-tail | l13 S3 (scaled MAD); l12 S5 (normal-reference rule); l12 S7 (KDE mass below a point) | r3-silver (Silverman's $h$) | h-beta-var (robust beta and KDE tail, written) | Puts the robust spread into the bandwidth rule, which no item does, and compares the KDE tail with a robust normal fit as a ratio; l12 compares quantiles with a classic normal fit. |
| p-five-weeks-flip | l11 S8 (sign-flip, all 1,024 patterns); l13 S0 (one month moves the mean) | r3-flip (what flipping assumes) | h-boot-copy (resamples with the big month) | Uses the median as the flip statistic and counts its patterns by reasoning, then asks why it differs from the mean's; the course only flips with the mean. |

## Waived or open

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
