# Concept audit, round 2: estimation levels 1 to 3 (`estimation-1-3-r2`)

Blind read at commit `0116a24e` (after the round 1 fix pass). Stage 1, full ledger.
Files read: `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l9-how-precise`, `fluency-l10-catching-the-truth`.
Sources: Casella and Berger, *Statistical Inference* (ch. 5, 7, 9); Wasserman, *All of Statistics* (ch. 6, 8, 9, 11); Efron and Tibshirani, *An Introduction to the Bootstrap* (ch. 6, 7, 8, 13).

- Ledger: `docs/reports/audit-estimation-1-3-r2-ledger.md`, 3,875 rows: correct 3,859, wrong 0, imprecise 13, misleading 3, unverified 0.
- Concepts script: `docs/reports/estimation-L1-3-concepts-r2.py`, 128 checks, exit 0 (venv Python 3.13, NumPy and SciPy newer than CI's pins; no figure depends on the version).
- Findings: 10. wrong 0, imprecise 8 (all minor), misleading 2 (1 serious, 1 minor).

## What was checked

Every graded key, slip value and wrong option was recomputed; the ledger gives the basis per screen. Watch-list results:

| Topic | Result |
|---|---|
| Bias, MSE | MSE = variance + bias² everywhere; divisor $n + 1$ stated for normal samples only (l4 s5, quiz; homework 1). Monte Carlo: MSE 0.498, 0.359, 0.333 for $c = 4, 5, 6$ at $n = 5$. One misleading reason in homework 1 (finding 1). |
| $n - 1$ against $n$ | Consistent: $s^2$ unbiased, $s$ biased low ($E[s] = 0.940\sigma$ at $n = 5$, exact and simulated), MLE divides by $n$, known mean divides by $n$ (problems 1). One loose sentence (finding 4). |
| SE formulas and their distribution | $\sigma/\sqrt n$ with independence stated; $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$ carries "for normal returns" in l8 s9, l9 s7, l9 summary, l10 s10, review 3, problems 2. Simulated ratio to the formula: normal 0.97, 1.00, 1.00 at $n = 5, 20, 250$; $t_5$ data 1.22, 1.50, 1.80. The condition is missing in the l8 summary and l8 s10 (finding 3). |
| $t$ against $z$ | l10 s5 states that 1.96 assumes $\sigma$ known and gives $t_9$: 0.918 and 2.262 (simulated coverage 0.918 and 0.950). Fluency uses $n \ge 64$, where the $t$ multiplier is within 3.5% of $z$. |
| Interval interpretation | Repeated-sampling reading throughout; probability statements about the parameter are marked as needing a prior (l10 s6, l12 s8, problems 3, homework 3). |
| MLE regularity | Boundary and restricted-range maxima handled (l6 s4, s5, review 2, homework 2); $n = 1$ unbounded likelihood (l8 s5); non-regular uniform maximum treated exactly (homework 3). One over-general sentence (finding 6). |
| Fluency families | All five swept over every combination (140, 108, 98, 3,363, 147): keys right, slips distinct, answers rounded to 3 places inside the tolerance. |

### Bootstrap tests: share of correct programs that fail

Three correct codings per widget, different RNG calls, run under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs`, each test's seed replaced by 400 fresh seeds (120 for the Sharpe test). The sweep script is in the session scratchpad (`est13-r2/sweep.mjs`) and is not committed; its CPython twin is in the concepts script.

| Widget and test | `random.choices` | `random.choice` loop | NumPy (seeded) | Law-based sweep |
|---|---|---|---|---|
| l11 s4, width (B 500) | 0 of 400 | 0 of 400 | 0 of 400 | |
| l11 s4, ends within 0.05 of −0.30, 0.55 (B 4,000) | 0 of 400 | 0 of 400 | 0 of 400 | 0 of 40,000 |
| l11 s4, same seed twice | 0 of 50 | 0 of 50 | 0 of 50 | |
| l11 s4, `[0, 0, 0, 0, 10]` gives exactly 0 and 6 | 0 of 400 | 0 of 400 | 0 of 400 | |
| l11 s4, eight values within 0.06 of −0.39, 0.92 (B 3,000) | 1 of 400 | 0 of 400 | 0 of 400 | 10 of 40,000 in the script; 14 of 40,000 by direct index draws (0.03%) |
| homework 3, maximum | 0 of 400 | 0 of 400 | 0 of 400 | |
| homework 3, median within 0.1 of −0.25, 0.80 (B 2,000) | 0 of 400 | 0 of 400 | 0 of 400 | |
| homework 3, Sharpe within 0.25 of −0.98, 3.00 (B 2,000) | 0 of 120 | 0 of 120 | 0 of 120 | 0 of 3,000 |
| homework 3, order (B 40), width (B 500) | 0 of 800 | 0 of 800 | 0 of 800 | |

Totals under Pyodide: lesson 11, 1 failure in 4,950 correct runs (0.02%); homework 3, 0 in 5,160. The same sweeps in CPython (400 seeds, three pure-Python codings) gave 2 failures in 4,800 lesson 11 runs, both on the eight-value test, and 0 in 3,780 homework 3 runs. The eight-value test is the only one with a measurable rate: its long-run ends are −0.3875 and 0.9125 against centres −0.39 and 0.92, and the upper end has sd 0.017, so a correct program fails about 3 times in 10,000. That is well under 1%. The homework 3 test 4 change from round 1 (B = 2,000, tolerance 0.25) holds: simulated ends average −0.977 and 2.995 with sd 0.060, so the band is 4 sd wide each side.

Wrong programs against the hidden tests (Pyodide): sampling without replacement, a shuffle, one draw repeated, $n - 1$ or $B$ draws, the unsorted list, a normal or reflected interval, a 90% or 50% cut, and an ignored seed all fail. A 94% cut (3% from each end) passes homework 3: it sits inside the tolerances any seed-robust test needs, so it is not raised as a finding.

One correct coding does fail lesson 11: `np.random.choice(data, size=n)` in the starter's slot. `random.seed(seed)` does not seed NumPy, so test 5 (same seed twice) fails every time. See finding 8.

### Code feedback lines (`feedback.byKey.test-N`)

| Widget | Line | Natural codings submitted (Pyodide) | Verdict |
|---|---|---|---|
| l3 s10 | test-1 | starter, manual divide by $n$, `ddof=0`: return 1.633, as the line says. `np.var(ddof=1)` returns 4.0; `ddof=2` returns 2.83 | imprecise (finding 9) |
| l7 s6 | test-3 | four mutants (log of the product, `math.pow`, a loop, `np.log`) all fail test 3 first | correct |
| homework 1 `expected_vn` | test-1 | divide by $n - 1$, no count, deviations from the population mean, no division: all fail test 1 first; the line describes its test | correct |
| homework 2 `log_lik` | test-9 | three product mutants fail test 9 first; a sum of log densities passes | correct |
| homework 3 bump | test-1 | normal approximations, first or last delay, one-sided, swapped ends, power 1: fail test 1 first | correct |
| homework 3 bump | test-2, test-5, test-8 | each line describes its test truthfully; `delays[1]` and an $n \ge 2$ guard fail test 2 first | correct |
| homework 3 bump | test-6 | count for share, list length, fresh generator per trial, misses counted, percentage, NumPy generator, drawing only the maximum: fail test 6 first | correct |

No line is timing-dependent: the slowest correct case took 1.7 s against a limit of 5 s (35 s with NumPy).

## Findings

1. `homework-1.json` | `items[9].model` (part 5) and `items[9].rubric[6].text` | misleading, serious | The model answer's last reason to keep $c = n - 1$ reads "The MSE gain at $n = 20$ is small, and it relies on normality, which fat-tailed returns break." The rubric credits "reliance on normality" as a sound reason. A learner takes away that biased divisors stop helping when tails are fat. The opposite holds: the gain grows. | With excess kurtosis $\kappa$, $\operatorname{Var}(S^2) = \sigma^4\left(\tfrac{2}{n-1} + \tfrac{\kappa}{n}\right)$, so $\mathrm{MSE}(c)/\sigma^4 = \left[2k + \kappa k^2/n + (k - c)^2\right]/c^2$ with $k = n - 1$, smallest at $c = n + 1 + \kappa(n-1)/n$. Monte Carlo, $n = 20$, $t_8$ draws ($\kappa = 1.5$): MSE 0.180, 0.165, 0.157 for $c = 19, 20, 21$, a gain of 13% against 10% for normal draws (script "HW1 MC (n = 20)"). Only the exact optimum $n + 1$ needs normality (Casella and Berger, Example 7.3.4). | Model, part 5, replace the last sentence with: "The MSE gain at $n = 20$ is small, about 10%. The exact answer $n + 1$ holds for normal data only; fat tails push the best divisor higher still, so they are no reason to go back to $n - 1$." Rubric item 7: "Gives a sound reason to keep $c = n - 1$: pooling or averaging many estimates, or auditability and comparison with other desks."

2. `l2-estimates-vary.json` | `screens[4].widget.accept`, `screens[4].explain.text` | imprecise, minor | The slider runs to $n = 100$ on the 100-day population, and the key says 100 days give a standard error of 0.10%. Lesson 1 screen 5 said that averaging all 100 days is a census with no sampling error. Both are right, under different draws, and the screen does not say so. | $\sigma/\sqrt n$ needs independent draws: with replacement, as screen 1 says once, or from a population far larger than the sample. For $n$ distinct days out of $N$ the variance is $\tfrac{\sigma^2}{n}\tfrac{N - n}{N - 1}$, which is 0 at $n = N$ (Cochran, *Sampling Techniques*, section 2.5). | Replace `screens[4].explain.text` with: "Halving the standard error needs $\sqrt n$ doubled, so four times the data: the square-root law. The formula assumes independent draws, with replacement or from a long history. Drawing 100 different days from these 100 would be lesson 1's census, with no error at all."

3. `l8-volatility-mle.json` | `summary.ideas[2]`, `screens[10].explain.text`, `screens[10].hints[2].text` | imprecise, minor | The summary states "the SE of $\hat\sigma$ is about $\sigma/\sqrt{2n}$" with no distribution, and screen 10 applies it to a stock's realised volatility. Screen 9 and lesson 9 carry "for normal returns"; the summary is what a learner rereads. | For normal data $(n - 1)S^2/\sigma^2$ is chi-squared (Casella and Berger, Theorem 5.3.1), which gives the formula. In general $\operatorname{Var}(S^2) = \sigma^4(2/(n-1) + \kappa/n)$. Monte Carlo: $t_5$ returns give 1.50 and 1.80 times the formula at $n = 20$ and 250 (script "L9 MC: fat tails"). | `summary.ideas[2]`: "Annualise by scaling the variance by 252 and the sd by $\sqrt{252}$; for normal returns the SE of $\hat\sigma$ is about $\sigma/\sqrt{2n}$, and fat tails make it larger." `screens[10].explain.text`, second sentence: "With 20 days the SE of $\hat\sigma$ is about 0.16% a day, or 2.5% a year, if returns are normal, and more if their tails are fat." `screens[10].hints[2].text`: "The two MLE versions both give about 16%. With $n = 20$ and normal returns the SE is about $1.0/\sqrt{40} = 0.16\%$ a day."

4. `l9-how-precise.json` | `screens[5].explain.text` | imprecise, minor | "That is the same $s/\sqrt n$ rule, with $s^2 = \hat p(1 - \hat p)$." In this course $s^2$ divides by $n - 1$, and for 0 or 1 data that gives $\tfrac{n}{n-1}\hat p(1 - \hat p)$. | Direct: $\sum (x_i - \bar x)^2 = n\hat p(1 - \hat p)$ for $x_i \in \{0, 1\}$, so $\hat p(1 - \hat p)$ is the divide-by-$n$ variance. Lessons 3 and 8 make this distinction the point. | Last sentence: "That is the same $\sigma/\sqrt n$ rule: one day's 0 or 1 has variance $p(1 - p)$, estimated by $\hat p(1 - \hat p)$."

5. `l9-how-precise.json` | `summary.ideas[0]`, `screens[2].prose` | imprecise, minor | "The standard error is the spread of an estimate's sampling distribution: how far it typically lands from the truth." The spread is about the estimator's own mean. It measures distance from the truth only when the estimator is unbiased; lesson 4 taught that the two differ. | $\mathrm{MSE} = \operatorname{Var} + \mathrm{bias}^2$ (Casella and Berger, section 7.3.1). Analyst B's halved mean in lesson 4 has standard error 0.1 and a root mean squared distance from the truth of 0.14. | `summary.ideas[0]`: "The standard error is the spread of an estimate's sampling distribution. For an unbiased estimate it says how far the estimate typically lands from the truth." `screens[2].prose`, second sentence: "It says how far an unbiased estimate, such as a mean, typically lands from the truth."

6. `l6-maximising.json` | `screens[4].explain.text` | imprecise, minor | "A boundary maximum has no flat tangent, so always check the ends." As a general statement it is false: $1 - p^2$ on $[0, 1]$ has its maximum at $p = 0$ with a flat tangent. | Derivation: a boundary maximum needs only $L' \le 0$ at a left end; equality is allowed. | "A boundary maximum need not have a flat tangent, so always check the ends."

7. `homework-2.json` | `items[3].explain.text` | imprecise, minor | "Maximising a log score is maximum likelihood, which is why it rewards honest forecasts." The second half does not follow from the first. The hindsight-best constant being the observed share says nothing about what a forecaster should state beforehand. | The log score is strictly proper: $p\ln q + (1 - p)\ln(1 - q)$ is largest at $q = p$ (Good 1952; Gneiting and Raftery 2007, JASA, section 4). That is the reason it rewards honesty. | Replace the last sentence with: "The log score rewards honest forecasts: its expected value, $p\ln q + (1 - p)\ln(1 - q)$, is highest when the stated chance $q$ equals the true chance $p$."

8. `l11-bootstrap.json` | `screens[4].widget.how`, `screens[4].feedback` | misleading, minor | The note says "Another correct way of drawing gives slightly different numbers and still passes. NumPy is available". A learner who writes `resample = np.random.choice(data, size=n)` draws correctly, yet fails test 5 every time, because `random.seed(seed)` does not seed NumPy. The only feedback is the generic line, which blames the draw: "Check that each resample has `n` draws and that a day can come up more than once." | Pyodide run: that coding returns `test-5` with rows `....x..`; with `np.random.seed(seed)` added it passes all seven tests on 400 seeds. | Add `feedback.byKey.test-5`: "Test 5 runs the same seed twice and expects the same interval. Draw with the `random` module, which `random.seed(seed)` controls. NumPy keeps its own generator, so `np.random.choice` ignores that seed." In `widget.how`, replace the last sentence with: "NumPy is available but loads slowly, and `random.seed` does not seed it; pure Python is enough here."

9. `l3-right-target.json` | `screens[10].feedback.byKey.test-1` | imprecise, minor | "For `[2, 4, 6]` you returned the divide-by-$n$ sd, 1.633." The line fires on every test-1 failure. A learner who copies `np.var(..., ddof=1)` from the screen's own prose returns 4.0 and is told they returned 1.633. | Pyodide runs: starter, manual divide by $n$ and `ddof=0` return 1.633; `np.var(returns, ddof=1)` returns 4.0 and fails test 1 first. | "For `[2, 4, 6]` the sample sd is 2.0. The starter's `np.std` gives the divide-by-$n$ sd, 1.633, and `np.var` gives a variance, 4.0. Use `np.std` with `ddof=1`."

10. `review-1.json` | `items[2].widget.wrong[3]` (`decimal`) | imprecise, minor | The slip value 0.00066667 has tolerance 0.005, so entries from −0.0043 to 0.0057, such as 0 or 0.005, get "0.00066667 is the answer with the returns written as decimals". Those entries are not that slip. | The other decimal slips in the course use tight bands (l3 quiz: 0.0004 ± 0.000008). | Set `"tol": {"abs": 0.00002}` on that slip.

## Notes that are not findings

- `l11` screen 3 keeps ranks 26 to 975 of 1,000; Efron and Tibshirani (section 13.3) keep ranks 25 to 975. The page states its rule ("25 values from each end") and the code uses the same one, so the key is right under the stated convention.
- `l12` reads $\mathrm{Beta}(a, b)$ as $a$ imagined heads and $b$ imagined tails, the convention under which the posterior mean is the pooled share. It is stated on first use and kept throughout.
- `l2` screen 1 and screen 8 quote the page's own seeded run (0.095, 0.312, 96.2%). Replayed with the engine's generator (mulberry32, seed 1610): 0.0953, 0.3124, 0.962.
- `homework-3` item 8: the max-based interval for a uniform has coverage exactly the level at every $n$ (simulated 0.500, 0.800, 0.950, 0.901, 0.990 at $n = 1, 2, 5, 20, 50$).

## Overlap with earlier reads

Filled in after the ledger and the ten findings above were written. Earlier reads opened then: `docs/reviews/audit-estimation-1-3.md` (round 1, its sixteen findings, overlap section and fix pass), and, by search for the ten topics, `review-1.6.md`, `review-problems-1.6-a.md`, `review-problems-1.6-b.md`, `review-holes-1.6-2.1.md`, `review-exam-second-item-1.6-1.11.md`, the `review-delta-*` and `review-pass*` files, and the author reports `docs/reports/estimation-2-perf.md`, `estimation-3-perf.md`, `fluency-estimation.md` and `problems-estimation.md`. Counting follows round 1: only findings about a claim, a key, a slip's meaning or a line of reasoning.

| | count |
|---|---|
| conceptual findings by this audit only | 9 (findings 1, 2 and 4 to 10) |
| conceptual findings by the earlier reads only | 22 (round 1 audit 15, earlier reviews 7; all fixed before this round) |
| conceptual findings by both | 1 (finding 3) |

New `wrong` findings that no earlier read found: 0.

- Finding 3 is the defect of round 1's finding 3, $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$ without its normal condition. Round 1 fixed it in l9, l10, review 3 and problems 2. Its fix pass left l8, judging that the summary "already sits under 'For normal returns'". That phrase opens the first summary bullet; the rule is in the third, and screen 10 applies it with no condition. Counted as both.
- Every sentence the round 1 fix pass wrote was read here as a ledger row, blind to its origin. All are marked correct. The round 1 keys and tests that changed hold: homework 3 test 4 at B = 2,000 (sweep above), fluency l10 from $n = 64$ ($t$ multiplier within 3.5% of $z$ on all 147 combinations), l10 screen 5 with "if daily returns are normal" (simulated cover 0.918 and 0.950).
- Round 1's finding 1 was about the homework 3 widget and a tolerance centred on one seed. Finding 8 here is the lesson 11 widget and a different cause: a generator the seed does not reach.
- What a single read missed: finding 1 needed the moments of $S^2$ beyond the normal case; finding 8 needed a correct program that does not use `random`; finding 9 needed a second natural wrong coding on a one-line widget.

## Inbox

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (audit estimation):".

## Runs

- `cd app && node tools/validate.mjs`: 0 errors, 4,617 warnings.
- `node tools/run-number-scripts.mjs --only estimation`: 4 of 436 scripts, 4 passed.
- `node tools/grade-all.mjs --file <each of the 23 files> --local-cdn <pkgs>`: 0 failures in every file; with `--code` on the seven files that hold Python widgets: 8 widgets run, 0 failures (solutions pass, starters fail, mutants fail at their named tests).
- `python docs/reports/estimation-L1-3-concepts-r2.py`: 128 checks, 0 failed, exit 0.
- No playthrough, as the common rules say.

## Fix pass

Opus fixer, from commit `7e16a33b`. Each basis below is the fixer's own derivation or run; simulations are in the session scratchpad (`fix-est13r2/f1.py`) and seven new checks ("fix r2") at the end of `docs/reports/estimation-L1-3-concepts-r2.py`.

1. Fixed differently. Basis: for iid data with finite variance $E[SS] = (n - 1)\sigma^2$ needs no other assumption, and $\operatorname{Var}(SS) = \sigma^4(2k + \kappa k^2/n)$ with $k = n - 1$ gives an MSE-best divisor $n + 1 + \kappa(n - 1)/n$ (grid minimum agrees to 2e-4). Own Monte Carlo, $n = 20$, 400,000 samples: $E[s^2]/\sigma^2$ = 1.000 (normal), 0.999 ($t_8$), 1.000 (uniform); gain of $c = 21$ over 19 is 9.6% normal, 12.9% $t_8$, 15.5% $t_5$, and −1.9% uniform (light tails put the optimum at 19.86). Part 5 now says $n - 1$ is unbiased for any distribution with a finite variance, that $n + 1$ is exact only for normal data, and that fat tails push the best divisor higher, not back to $n - 1$; kept to three sentences as the prompt asks. Rubric item 7 credits pooling, auditability or distribution-free unbiasedness and says fat tails are not a reason.
2. Fixed (shortened wording). Basis: without replacement $\operatorname{Var}(\bar X) = \tfrac{\sigma^2}{n}\tfrac{N - n}{N - 1}$, 0 at $n = N$; the trial screen draws with replacement. l2 s4 explain gains "It assumes independent draws, here with replacement; 100 different days out of these 100 would be the census of lesson 1, with no error at all." and keeps its other two sentences.
3. Fixed. Basis: delta method, $\operatorname{Var}(\hat\sigma) \approx \operatorname{Var}(S^2)/(4\sigma^2) = \sigma^2(2 + \kappa)/(4n)$, so $\sigma/\sqrt{2n}$ is the $\kappa = 0$ case and grows with $\kappa > 0$; $1.0/\sqrt{40} = 0.158$, times $\sqrt{252}$ is 2.51. l8 summary idea 3, s10 explain and s10 step hint now carry "normal returns", the first two with "fat tails make it larger".
4. Fixed. Basis: for $x_i \in \{0, 1\}$, $\sum (x_i - \bar x)^2 = n\hat p(1 - \hat p)$, so $\hat p(1 - \hat p)$ is the divide-by-$n$ variance and $s^2 = \tfrac{n}{n - 1}\hat p(1 - \hat p)$ (NumPy check on 90 ones and 60 zeros). l9 s5 explain: "the same $\sigma/\sqrt n$ rule: one day's 0 or 1 has variance $p(1 - p)$, estimated by $\hat p(1 - \hat p)$."
5. Fixed. Basis: MSE = Var + bias²; the SE measures distance from the estimator's own mean, which is the truth only when unbiased. l9 summary idea 1 and s2 prose reworded as the audit proposes.
6. Fixed. Basis: $1 - p^2$ on $[0, 1]$ peaks at $p = 0$ with $L'(0) = 0$; a left-end maximum needs only $L' \le 0$. "need not have a flat tangent".
7. Fixed. Basis: $\tfrac{d}{dq}[p\ln q + (1 - p)\ln(1 - q)] = p/q - (1 - p)/(1 - q)$, zero only at $q = p$, and the function is concave: strictly proper (grid check at $p$ = 0.3, 0.7, 0.8). Last sentence of homework 2 item 4 explain now states that reason.
8. Fixed. Basis: own reading of the widget; `random.seed` seeds only the `random` module's generator. Added `feedback.byKey.test-5` (same seed twice must match, so draw from the generator `random.seed(seed)` sets; NumPy keeps its own) and "and `random.seed` does not seed it" in `widget.how`; "Another correct way of drawing" now reads "with `random`". Three mutants added, each first failing test 5 under Pyodide: `np.random.choice(data, size=n)`, `[data[np.random.randint(n)] ...]`, and `random.Random().choices(data, k=n)` (a clock-seeded generator per resample).
9. Fixed differently. Basis: `[2, 4, 6]` has SS 8: sd 2.0, divide-by-$n$ sd 1.633, `np.var` 2.667 by default and 4.0 with `ddof=1`. The audit's line would tell a learner who used `np.var(returns)` that they got 4.0, so the line names both: "For `[2, 4, 6]` the sample sd is 2.0. Dividing by $n$ gives 1.633, and `np.var` gives a variance (2.667, or 4.0 with `ddof=1`), not an sd. Use `np.std` with `ddof=1`." Four mutants added, each first failing test 1: divide by $n$ by hand, `np.var(ddof=1)`, `np.var()`, `np.std(ddof=0)`.
10. Fixed differently. Basis: 0.01, 0.03, 0.05, 0.07 give SS 0.002, so 0.002/3 = 0.00066667. Tolerance set to 0.00004, not 0.00002, so the one-figure rounding 0.0007 still gets the decimal message; 0, 0.005 and the key 6.6667 fall outside.

No graded key, existing hidden test or solution changed. One slip tolerance changed (review 1 `decimal`). No hidden test added.

Runs at the fix commit: validator 0 errors; `voice-scan.py 35` on the nine edited files: 0 over three sentences, 0 over 35 words; `estimation-L1-3-concepts-r2.py` 135 checks, 0 failed, and `estimation-L1-3-concepts.py` all passed; `run-number-scripts.mjs --only estimation` 4 of 4 passed; `grade-all.mjs --file` 0 failures on all nine files, with `--code` on l3 and l11 (mutants checked; a negative control with a wrong test number was caught); playthrough of the six lessons and three sets, desktop and `--mobile`: 18 runs, all passed.
