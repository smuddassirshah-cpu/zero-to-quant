# Concept audit: estimation, levels 1 to 3 (round 1)

Blind audit at commit 43e99544. Scope: `app/content/courses/estimation/`, lessons l1 to l12, review-1 to 3, homework-1 to 3, problems-1 to 3, fluency-l9 and fluency-l10. Stage 1, so the full ledger.

- Ledger: `docs/reports/audit-estimation-1-3-ledger.md`, 3,056 rows: correct 3,026, imprecise 21, misleading 6, wrong 3, unverified 0.
- Concepts script: `docs/reports/estimation-L1-3-concepts.py` (venv Python 3.13, NumPy and SciPy newer than the CI pins; no figure depends on the version). It exits 1: two checks fail, and both are findings (1 and 2). Every other check passes.
- Findings: 16. Wrong 2 (serious 1, minor 1). Imprecise 11 (serious 3, minor 8). Misleading 3 (minor 3). Serious 4, minor 12.

Sources: Casella and Berger, *Statistical Inference*, 2nd ed. (CB); Wasserman, *All of Statistics* (W); Hull, *Options, Futures and Other Derivatives*; Efron and Tibshirani, *An Introduction to the Bootstrap*.

## What was checked and held

The watch list, with the result of each check (all in the concepts script unless a source is named).

- Unbiased against consistent. The course never uses "consistent" loosely. l3 separates "unbiased" from "right in any one sample"; l9 quiz 4 has $s$ settle near $\sigma$ without calling it unbiased. Held.
- $n - 1$ against $n$, and which is the MLE. $E[\tfrac1n SS] = 0.8\sigma^2$ at $n = 5$ (MC 0.7991, SE 0.0009). The numeric maximiser of the normal log-likelihood divides by $n$ (CB Example 7.2.11). $E[s] = 0.94\sigma$ at $n = 5$ (MC 0.9394). Held.
- MSE = variance + bias². MSE of $SS/c$ at $n = 5$: 0.499, 0.360, 0.333 for $c = 4, 5, 6$ (MC), and $c = n + 1$ is the minimiser for every $n$ from 2 to 60 (CB Example 7.3.4). The claim is always tied to "normal samples". Held.
- Standard error against standard deviation. Held in every item; every slip value recomputed.
- MLE properties. The course states none of the asymptotic properties, so no regularity condition is missing. Boundary maxima, restricted ranges and the $n = 1$ blow-up are all treated. Held.
- Method of moments is not taught at these levels.
- Confidence interval reading. Every key has the interval random and $\mu$ fixed; every "95% chance that $\mu$..." option is keyed wrong and sent to the Bayesian reading. The wrong option "95% of future means land in this interval" is false by a wide margin: 83.5% (MC). Held.
- $t$ against $z$. Coverage 0.918 for $\pm 1.96\,s/\sqrt{10}$ and 0.950 for 2.262 with normal data (MC 1e6). Two gaps: findings 4 and 5.
- CLT intervals stated as approximate. Mostly "about" and "close to normal". Three places say more than is true: findings 6, 7 and 8.
- Bootstrap. Seeded runs reproduce ($-0.29$ to 0.555; the table of four runs; the Sharpe interval). Single-day resampling under lag-1 correlation 0.6 gives sd 0.155 against a true 0.317, and 10-day blocks 0.246 (MC). 35 distinct resamples of 4; 63% contain the maximum. Held, apart from finding 1.
- Bayes. Beta quantiles and a simulated posterior agree with every stated figure. One overstatement: finding 2.

Code widgets. Every Python widget ran under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs` (node, local CDN). 60 submissions (the list is in `scratchpad/est13/sweep.mjs`; the routing results for `h-bump-interval` are repeated in the concepts script): each solution, and two to five natural codings of every mistake a feedback line names. `pytest` is not used in this course. No C++. No line depends on timing. Hidden tests reject every obvious wrong program tried (divide by $n$ or $n - 1$ the wrong way, variance for sd, log of a product, log base 10, sampling without replacement, 5% cut from each end, minimum and maximum, last or first delay, a count for a share). Results are in findings 1, 12 and 13.

## Findings

1. `homework-3.json` | `items[h-bootstrap-code].widget.tests[3]` and `.widget.how` | wrong · serious | The Sharpe test rejects correct programs, and the text calls its targets "long-run ends" when they are one seed's values. | The test asks for ends within 0.15 of $-1.10$ and 2.90 at $B = 1000$. Those are the seed-1 values of `random.choices`. The long-run ends of this bootstrap are $-0.98$ and 3.00 (1e6 resamples). One run of $B = 1000$ has end sd 0.08 and 0.09, so a correct program with its own draws passes with chance 0.46 (600 runs). Under the page Pyodide, `np.random.seed(seed)` with `np.random.choice` gives $-0.904$ to 2.936 and fails test 4; so does `random.Random(seed + 1000).choices`. The widget says NumPy is available. | Replace the test call with `(lambda ci: abs(ci[0] + 0.98) < 0.25 and abs(ci[1] - 3.00) < 0.25)(bootstrap_ci(daily, sharpe, 1000, 1))`. Fresh correct runs then pass 99.2% of the time; the solution ($-1.10$, 2.896), `default_rng`, `np.random.seed` and `random.Random` codings all pass; the 5% cut ($-0.76$, 2.69) and min/max still fail. In `how`, replace the fourth sentence with: "A median must land within 0.1 of its long-run ends, and a Sharpe ratio within 0.25 of $-0.98$ and 3.00." Basis: simulation in the concepts script; W §8.3.

2. `l12-updating-a-belief.json` | `summary.trap` | wrong · minor | "A dogmatic prior such as Beta(100, 100) ignores the data" is false as stated. | The lesson's own screen has the posterior mean move from 0.5 to $160/300 = 0.533$, and its feedback says "The data do move the analyst, a little". No proper beta prior ignores data (CB Example 7.2.14: the weight on the MLE is $n/(a + b + n) > 0$). | "A dogmatic prior such as $\mathrm{Beta}(100, 100)$ barely moves on 100 flips; and the MLE is not the posterior."

3. `l9-how-precise.json` | `screens[7].prose`, `summary.formula.note`, `quiz[1].explain`; `l10-catching-the-truth.json` | `screens[10].prose`, `screens[10].explain`; `review-3.json` | `items[r-vol-se].explain` | imprecise · serious | $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$ is given as a general rule and used to put a 95% interval on a fund's volatility. It holds for normal returns only. | By the delta method $\operatorname{Var}(\hat\sigma) \approx (\kappa - 1)\sigma^2/(4n)$, with $\kappa$ the kurtosis; $\kappa = 3$ gives $\sigma^2/(2n)$. With Student-$t$ returns on 5 degrees of freedom and $n = 504$ the sd of $\hat\sigma$ is 0.0590 against the rule's 0.0315, a factor 1.87 (MC 2e5). Daily equity returns are fat-tailed, so a learner carries away intervals about half their true width. l8 screen 9 does say "For normal returns"; the later screens drop it. | l9 `screens[7].prose`, last sentence: "For normal returns, a volatility estimate has $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$; we state that one without proof. Fat tails make it larger." l9 `summary.formula.note`: "For normal returns, $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$; fat tails make it larger. One observation gives no estimate." l9 `quiz[1].explain`, second sentence: "If returns are normal, the volatility is pinned to within a few per cent of itself, far better than a mean." l10 `screens[10].prose`, second sentence: "For normal returns, the standard error of a volatility estimate is about $\hat\sigma/\sqrt{2n}$." l10 `screens[10].explain`, last sentence: "Two years pin a volatility down far better than a mean, though fat-tailed returns widen this interval." review-3 `r-vol-se.explain`, second sentence: "If returns are normal, a 95% interval is about 24% to 26%: five years pin volatility down well."

4. `fluency-l10-catching-the-truth.json` | `families[half-width-from-s].vars.nr.pick` | imprecise · serious | The drill keys $z \times s/\sqrt n$ for a "95% interval" at $n = 16$ and $n = 25$, against the lesson's own rule. | l10 screen 5 teaches that with $s$ and a small sample the multiplier is the $t$ one, and that the two agree "from about 30 observations". At $n = 16$ the keyed interval covers 0.931 for "95%" and 0.979 for "99%" with normal data; the $t$ multipliers are 2.131 and 2.947 (MC 6e5 and `scipy.stats.t`). The key is right only under a convention the item does not state and the lesson warns against (CB §5.3.2). | Set `nr.pick` to `[[36, 6], [64, 8], [100, 10], [144, 12], [256, 16], [400, 20], [625, 25]]`. Every root stays whole, so prompts, slips and solutions are unchanged.

5. `l10-catching-the-truth.json` | `screens[5].prose`; `homework-3.json` | `items[h-small-t].explain` | imprecise · serious | "$(\bar X - \mu)/(s/\sqrt{10})$ follows a $t$ distribution with 9 degrees of freedom" is stated with no condition. It needs normal data. | CB Theorem 5.3.1 and Definition 5.3.4: the result is for a sample from a normal population. With 2.262 at $n = 10$ the cover is 0.950 for normal days, 0.901 for exponential days and 0.839 for lognormal days (MC 1e6 each). A learner carries away that $t$ repairs any small sample. | l10 `screens[5].prose`: "The 1.96 assumes we know $\sigma$. With 10 days we estimate it by $s$. If daily returns are normal, $(\bar X - \mu)/(s/\sqrt{10})$ follows a $t$ distribution with 9 degrees of freedom. The band is $\pm 1.96$ on that $t$; the dashed curve is the normal." homework-3 `h-small-t.explain`: "For normal returns, $(\bar X - \mu)/(s/\sqrt{10})$ has a $t$ distribution with 9 degrees of freedom, whose 97.5% point is 2.262. The interval is 15% wider than the normal one."

6. `l10-catching-the-truth.json` | `screens[2].explain`, `screens[2].widget.accept`, `screens[3].explain`, `screens[3].widget.accept` | imprecise · minor | "The share that miss converges to exactly 5%" (and "exactly 10%"). Exact only when the 100-day mean is exactly normal. | Screen 0 says $\bar X$ is "close to normal". With skewed days (exponential, sd 1), $n = 100$ and $\sigma$ known, the miss share is 0.0493, split 0.019 below and 0.030 above (MC 4e5). CB §5.5.3: the CLT is a limit. | `screens[2].explain`, second sentence: "Over more and more backtests, the share that miss settles at 5%: exactly so for normal returns, and very nearly so otherwise." `screens[2].widget.accept`: "5 of these 100. The long-run share is 5%." `screens[3].explain`, first sentence: "At $z = 1.645$, 10 of the 100 miss, and the long-run share is 10%." `screens[3].widget.accept`: "10 of these 100. The long-run share is 10%."

7. `homework-3.json` | `items[h-long-trader].model`, part (b) | imprecise · minor | "In repeated samples of 50 trades, 95% of intervals built this way contain the true $p$." The interval $\hat p \pm 1.96\,\mathrm{SE}$ is a normal approximation. | Exact cover at $n = 50$: 0.941 at $p = 0.6$, 0.934 at 0.55, 0.935 at 0.5 and 0.7 (binomial sum). Brown, Cai and DasGupta (2001), *Interval estimation for a binomial proportion*. | Replace the sentence with: "The 95% describes the method: in repeated samples of 50 trades, about 95% of intervals built this way contain the true $p$ (nearer 94% at this $n$, as the normal curve is an approximation)."

8. `l9-how-precise.json` | `screens[10].explain` | imprecise · minor | "A coin-flipper beats 55% about 16% of the time." | Exact binomial, 100 trades at $p = 0.5$: more than 55 wins 0.136; 55 or more 0.184. The 16% is the normal tail beyond one SE (0.157) with no continuity correction. Both readings of "beats" miss 16%. | Second sentence: "By the normal curve a coin-flipper reaches 55% about 16% of the time, the shaded tail; the exact chance of 55 or more wins is 18%."

9. `l4-bias-against-variance.json` | `screens[1].hints[1]` | misleading · minor | "The lowest point of the solid curve is where the two dashed curves cross." True on this chart only because $\mu^2 = \sigma^2/n$. | The MSE $w^2 v + (1 - w)^2 \mu^2$ is lowest at $w = \mu^2/(\mu^2 + v)$; the curves cross at $w = \mu/(\mu + \sqrt v)$. With $v = 0.04$ and $\mu^2 = 0.01$ these are 0.200 and 0.333. homework-1 `h-best-weight` teaches the right rule, so the hint contradicts it in general. | "Here the two dashed curves are mirror images, so the solid curve is lowest halfway along."

10. `l3-right-target.json` | `screens[9].feedback.correct`, `screens[9].explain` | imprecise · minor | "The $n$ version is 2.6% too low" and "dividing by $n$ understates the volatility by 2.6%" treat $s$ as the truth. | The same lesson shows $E[s] < \sigma$. At $n = 20$ with normal data the $n$ version averages $0.962\sigma$ and $s$ averages $0.987\sigma$ (MC 4e5). 2.6% is the gap between the two estimates. | `feedback.correct`: "$\sqrt{20/19} \approx 1.026$: the $n - 1$ volatility is 2.6% higher." `explain`, second sentence: "With 20 days, the $n - 1$ volatility is 2.6% above the $n$ one."

11. `l8-volatility-mle.json` | `screens[8].prose` | imprecise · minor | "Independent daily returns add, so their variances add." Log returns add; simple returns compound. | Hull §15.4 defines $u_i = \ln(S_i/S_{i-1})$ before scaling by $\sqrt{252}$. The course never says which return it uses; this is where the convention first matters. | Second sentence: "Over 252 trading days, daily log returns add, and if they are independent their variances add: annual variance is $252\hat\sigma^2$."

12. `homework-3.json` | `items[h-bump-interval].feedback.byKey.test-2`, `.test-5`, `.test-8` | misleading · minor | Three lines name a mistake whose natural codings fail an earlier test, so the learner who makes it never sees the line. | The page shows the line of the first failing test. Under the page Pyodide: a normal approximation (three codings) fails test 1; using the last or the first delay fails test 1; cutting the whole $1 - \text{level}$ from each end fails test 1; returning a count fails test 6. Only the test-6 line is reached by its own mistakes (a fresh generator per trial, counting misses). The test-1 line does not mention any of them. | `test-1`: "Test 1 expects about 30.25 to 102.60 from delays up to 30. Build both ends from the largest delay, and cut `(1 - level) / 2` from each end of $M/\theta$; a normal approximation cannot give ends this lopsided." `test-2`: "Test 2 has one delay of 4.0 and expects 4.10 to 160. The law of $M$ needs no spread, so one delay is enough." `test-5`: "Test 5 lists the same delays as test 1 in another order and expects the same interval." `test-6`: add at the end "Return a share, not a count." `test-8`: "Test 8 uses one delay per trial at level 0.5 and expects a share near 0.5."

13. `l7-taking-logs.json` | `screens[6].feedback.byKey.error`; `homework-2.json` | `items[hw2-code].feedback.byKey.error` | misleading · minor | The `error` line explains a domain error, but that error cannot arrive under the `error` key. | The page gives key `error` only when the code fails to load. `math.log(p ** heads * (1 - p) ** tails)` loads, then raises inside test 3, and the key is `test-3`, which has no line (run under the page Pyodide). In homework-2 a product of 5,000 densities overflows to `inf`, whose log is `inf`: test 9 fails with no error at all, and an unfilled `...` fails test 1. | l7: add `"test-3": "Test 3 has 2,000 flips. A domain error there means you took the log of a product that underflowed to 0. Add the logs instead."` and set `error` to "Your code stopped with an error before any test ran. Check the line you added." homework-2: add `"test-9": "Test 9 has 5,000 returns. A product of 5,000 densities overflows, so sum the terms of the closed form instead."` and set `error` to "Your code stopped with an error before any test ran. Check that both `...` are replaced."

14. `l7-taking-logs.json` | `screens[2].feedback.byKey.sign` | imprecise · minor | "L = 4/27 is below 1, so every log in the sum is negative." The conclusion does not follow from the premise. | A product below 1 can have a factor above 1 (densities often do). The logs are negative because each factor is below 1. | "Each factor, 2/3, 2/3 and 1/3, is below 1, so every log in the sum is negative: −0.4055 − 0.4055 − 1.0986. A positive 1.910 drops the minus signs."

15. `l6-maximising.json` | `quiz[2].explain` | imprecise · minor | "The value of $\sigma$ scales $L$ but does not move its peak." | $L(\mu) = C(\sigma)\,e^{-S(\mu)/(2\sigma^2)}$: $\sigma$ changes the height and the width, which is not a scaling. | Second sentence: "The value of $\sigma$ changes the height and width of $L$ but does not move its peak."

16. `l2-estimates-vary.json` | `screens[2].prose` | imprecise · minor | "The histogram you built is the sampling distribution of $\bar X$." A histogram of 1,000 trials estimates it. | The exact law is the dashed line on the same chart (found here by convolution: 95.6% within $0.10 \pm 0.63$, against the simulation's 96.2%). CB §5.2. | First sentence: "The histogram you built approximates the **sampling distribution** of $\bar X$: every value the average could take, with its chance."

## Notes that are not findings

- l8 screen 6 and quiz 4 say fixing $\mu = 0$ "avoids a noisy mean". Checked because the variance version of the claim can go either way: at $n = 20$, $\mu = 0.04$, $\sigma = 1$ the zero-mean sd estimate has RMSE 0.1578 against 0.1617 for the MLE with the mean estimated (MC 4e5). The claim holds.
- The percentile bootstrap interval for a mean at $n = 20$ covers 0.926, not 0.95 (MC 4,000 samples). The lesson makes no coverage claim, and its summary says the bootstrap fails for tiny samples. A sentence saying the percentile interval runs a little narrow at $n = 20$ would be a good addition, not a correction.
- l4 screen 8: that the Blume-adjusted beta "forecasts next period's beta better" is Blume's (1975) empirical result, not something a simulation here can settle. Cited, not recomputed.
- Seeded page simulations (l2 screens 1, 2 and 8; l11 screen 1) were replayed in node with `app/js/engine/sim.js`: mean 0.0953, sd 0.312, 96.2% and 66% all reproduce.

## Tool runs

- `node tools/validate.mjs`: 0 errors, 4,616 warnings (repository-wide; none new).
- `node tools/run-number-scripts.mjs --only estimation`: 4 scripts, 4 passed, 0 new failures.
- `node tools/grade-all.mjs --file <file> --local-cdn <pkgs>` on all 23 files: 0 failures each.
- `docs/reports/estimation-L1-3-concepts.py`: exit 1: 88 checks pass, 2 fail (findings 1 and 2), 15 notes carry the evidence for the other findings.
- No playthrough, as instructed.

## Overlap with the earlier reads

Filled after the blind pass was committed (33d81d17). Earlier reads opened then: `docs/reviews/review-1.6.md` (estimation section and its fix pass), `review-problems-1.6-a.md` (section A), `review-holes-1.6-2.1.md`, `review-exam-second-item-1.6-1.11.md`, `review-delta-problems-ab-1.md`, `review-pass8-hits.md`, and the author reports `docs/reports/estimation-2-perf.md`, `estimation-3-perf.md`, `fluency-estimation.md` and `problems-estimation.md`. Only findings about a claim, a key, a slip's meaning or a line of reasoning are counted; tolerance bands, units, voice and reuse are not.

| | count |
|---|---|
| conceptual findings by this audit only | 16 (findings 1 to 16) |
| conceptual findings by the earlier reads only | 7 (all fixed before this audit) |
| conceptual findings by both | 0 |

New `wrong` findings that no earlier read found: 2 (findings 1 and 2).

The earlier reads' conceptual findings, each seen fixed at this commit and marked correct in the ledger:

- review-1.6, l1 `screens[1]` slip `dropped-minus` held 0.0082; now 0.0106 (the ten sizes add to 10.6; concepts script).
- review-1.6, homework-2 `hw2-code` explain said "about 40 each"; now "about 24 each" (density 24.2; concepts script).
- review-1.6, l4 `screens[1].explain` compared variance with bias, not bias²; now "the squared bias starts flat". Finding 9 here is on the hint of the same screen, a different sentence and a different defect.
- review-1.6, l12 `screens[3]` slip `noprior` named no action; now "You added the prior's 2 heads but not its 2 tails".
- review-problems-1.6-a, `p-robot-deliveries` part 3 accepted 0.85 to 0.95 for an estimate that sits at the edge; now tight, with a `middle` slip.
- review-problems-1.6-a, `p-three-month-fund` part 4 feedback and explain disagreed in the third place; now both give 0.816 from the unrounded values.
- review-problems-1.6-a, `p-tank-sensor` part 1 slip said "middle two" for the last two readings; now `last-two`.

What the earlier reads could not have caught by their method: findings 3 to 8 need a simulation or an exact sum against the claim; findings 1, 12 and 13 need mistake codings submitted to the page's grader, which reads a line against the test that fires it. The level 3 performance report lists thirteen planted slips that fail, which is true; it does not check which line each one lands on.

## Inbox

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (audit estimation):".
