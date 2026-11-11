# testing level 4 (Theory of estimation and tests): second-reader findings

Scope: `l13-matching-moments`, `l14-what-data-can-forget`, `l15-sharpness-of-the-peak`, `l16-best-possible-precision`, `l17-ratio-of-likelihoods`, `l18-counts-against-expectations`, `review-4`, `homework-4` in `app/content/courses/testing/`. Continuity: prerequisites `testing` L1 and L2, `estimation` L1 to L3, `limits-thm` L4 (and `random-vars` L3 for correlation; L5 is diagnostic only), exam `topic-1.6`.

Method: every screen and item worked from its text before its answer was read. Scripts in `docs/reviews/testing-4-scripts/`:

- `read-numbers.py`: every key, `wrong[]` value and stated number recomputed by a second route (SciPy distributions and tests, SymPy integrals for each information and tail formula, seeded simulation for each sampling claim), plus a probe of each numeric key with the engine's `within` for 2 dp and 3 s.f. roundings and for the values the hints lead to.
- `run-code.py`: each `code` item run in CPython under the engine's comparison rule: author solution, starter, the reader's own independent solution, and 31 plausible wrong solutions.
- `dump.py`: the reader used to print each file.

Format: `N. file | screen or item | tag | what is wrong | fix`. Tags: `wrong` = a wrong number, a false statement or wrong grading; `unclear` = teaching that misleads, states a conditional result without its condition, or uses something not yet taught; `minor` = wording, coverage, freshness.

## Tool results

- Author script `docs/reports/testing-L4-numbers.py`: exit 0, 468 of 468 checks.
- Reader script `read-numbers.py`: 398 of 404 checks pass; exit 1. The six failing checks are findings 1 and 2 (two checks between them), 3, 5, 12 and 13 below and pass once those are fixed.
- `run-code.py`: exit 0. All five code items (l13 s8, l15 s9, l17 s9, l18 s9, `h-gof-code`): author solution passes, starter fails, reader's solution passes, every one of the 31 mutants is caught (divisor $n - 1$, swapped outputs, unsigned or undoubled statistics, one-sided p-value, missing zero guard, degrees of freedom cells $- 1$, Yates applied, merging from one end only, merging on observed counts, no tail cell).
- Validator: 0 errors. Warnings on these files are advisory only (ladder canvas kind, 20-word sentences).
- Voice scan (`voice-scan.py 35`): 0 explanations over three sentences and 0 sentences over 35 words in this level. No exclamation mark, em-dash or en-dash; spelling British; no option named by place.
- Playthrough with `--local-cdn`: all six lessons, `review-4` and `homework-4` pass, with and without `--mobile` (16 runs, so every code item holds in Pyodide). Screenshots at 440 px read for l18 s0 and s10: no layout fault.
- `rubric-passes.mjs` on `h-cr-poisson`: rows 1 to 4 required, row 5 optional, as the report says.

## Statements checked (reader's own source or derivation)

References: DeGroot and Schervish (DS), 4th ed.; Casella and Berger (CB), 2nd ed.

- Method of moments (DS 7.6, CB 7.2.1): stated correctly, with the higher-moment case (Laplace) and three failures shown (disagrees with the MLE for the uniform and the Gamma, can contradict the data, can leave the range). Uniform MSEs $\tfrac{\theta^2}{3n}$ and $\tfrac{2\theta^2}{(n + 1)(n + 2)}$ rederived from the Beta$(n, 1)$ law of the maximum and by simulation.
- Sufficiency and factorisation (DS 7.7, CB 6.2.1 to 6.2.6): definition by the conditional law, theorem with $h$ free of $\theta$, "the whole sample is always sufficient", minimality named, and sufficiency tied to the model (uniform trap, drifting $p$, the $t$ model in the transfer). All correct. Rao-Blackwell (CB 7.3.17) stated with unbiasedness and finite variance; $E[X_1 \mid K] = \tfrac{K}{n}$ and $P(X_1 = 0 \mid T) = (\tfrac{n - 1}{n})^T$ confirmed by simulation.
- Fisher information (DS 8.8, CB 7.3.2): defined as $\mathrm{Var}(S)$, with "in a regular model it also equals $-E[\ell'']$"; additivity is tied to independence (quiz `q-overlap`); every information ($\tfrac{1}{p(1 - p)}$, $\tfrac{1}{\sigma^2}$, $\tfrac{1}{\lambda^2}$, $\tfrac{1}{\lambda}$, $\tfrac{2}{\sigma^2}$, $\tfrac{1}{2\sigma^4}$, $\tfrac{1}{\theta^2}$) recomputed in SymPy by the form the screen does not use. The reparametrisation rule $I(\sigma^2) = I(\sigma)/(d\sigma^2/d\sigma)^2$ is right and both standard errors agree with simulation. Asymptotic normality of the MLE carries its conditions (independent, smooth, fixed support, interior truth) and says "approximately".
- Cramér-Rao (DS 8.8, CB 7.3.9 to 7.3.15): regularity and "unbiased" are in the statement; the proof screens are the standard covariance argument; attainment exactly when $\hat\theta$ is linear in the score (CB 7.3.15); exponential example ($E[1/\bar X] = \tfrac{n\lambda}{n - 1}$, variance $\tfrac{\lambda^2}{n - 2}$ from the inverse Gamma); the $n + 1$ divisor beats the bound in MSE because it is biased; uniform$(0, \theta)$ escapes because the support moves ($\tfrac{\theta^2}{n(n + 2)}$ checked). "An unbiased estimator that attains the bound is the MLE" is true (the score is then $(\hat\theta - \theta)\,nI(\theta)$). One sentence overstates (finding 9).
- Likelihood-ratio tests (DS 9.1 to 9.2, CB 8.2.1, 8.3.12, 10.3.1): Neyman-Pearson for simple against simple, confirmed by brute force over the 21 counts; Wilks stated as approximate, large $n$, regular, null inside the range, degrees of freedom the parameters the null fixes; $-2\ln\Lambda = z^2$ exact for the normal mean; boundary failure with the 50:50 mixture (Chernoff 1954; simulated in the script, the $\chi^2_1$ cut has size 0.025 there, so "too strict" is right). Direction and nesting are under-explained (findings 7, 8, 10).
- Chi-squared tests (DS 10.1 to 10.3): Pearson's statistic as approximate with expected counts not small; cells $- 1$, one fewer per estimated parameter, with the Chernoff-Lehmann caveat stated correctly in l18 s6; $(r - 1)(c - 1)$ derived by counting margins; 2 × 2 equals the two-proportion $z^2$; $G$ against $X^2$; raw counts; independence of observations. A simulation of the fitted-Poisson case gives a mean of 3 for $X^2$, not 4. The upper-tail-only region is never said (finding 11).

## Findings

1. `l17-ratio-of-likelihoods.json` | screens[10] widget | wrong | Wrong grading. Key 6.806 with `tol` 0.003 rejects 6.81, the answer to 2 places, and the widget's own `accept` line prints `$29.64 - 22.83$`, which is 6.81. | Set `"tol": {"abs": 0.006}` (both `wrong[]` values, 29.64 and $-6.806$, stay outside). Change `accept` to `"6.806: $29.639 - 22.833$"`.

2. `l15-sharpness-of-the-peak.json` screens[1]; `l16-best-possible-precision.json` screens[4]; `l17-ratio-of-likelihoods.json` screens[4] | widget `tol` | wrong | Wrong grading, same class as 1: the key rounded to 2 places is marked "Not quite". 4.17 for 4.1667 (`tol` 0.001), 2.22 for $\tfrac{20}{9}$ (`tol` 0.002), 3.76 for 3.757 (`tol` 0.002). | Set `"tol": {"abs": 0.005}` on all three. Every `wrong[]` value stays outside ($\pm 4.1667$ and 19.1667; 2 and 1.8182; 1.879 and 43.757).

3. `homework-4.json` | items[7] `h-analyst` prompt claim 3 and model | wrong | Wrong number. With 40 equal-width cells on $(-6\%, 6\%)$, $n = 250$ and the fitted normal (0.05%, 1.2%), 20 cells expect under 1 (26 expect under 5), not 31. | Prompt: `20 cells had expected counts below 1.` Model: `With 20 cells expecting under 1, a single stray return adds a large term.`

4. `l14-what-data-can-forget.json` | screens[1] option `rises` | wrong | False statement. The option and its `why` say the order's chance "does rise" with $p$. On the slider it rises only to $p = 0.7$ and then falls (0.00222 at 0.7, 0.00048 at 0.9), as the caption shows. | Text: `It moves as $p$ moves, like the order's chance`. Why: `You read the chance of the order itself, which does move. Divide by the chance of 7 wins, which moves in step.`

5. `l15-sharpness-of-the-peak.json` | quiz[1] `q-overlap` prose | wrong | Wrong count. 254 daily prices give 253 daily returns and 249 overlapping 5-day returns, not 250. The explanation's "254 days of news" needs 254 daily returns. | Prose: `An analyst estimates a mean from 250 overlapping 5-day returns built from 254 daily returns, and adds their information as if they were 250 independent observations.`

6. `l13-matching-moments.json` | screens[3] explain | unclear | "the score equation is the moment equation" uses "score" two lessons before l15 s1 defines it; `estimation` never uses the word in this sense. | `For the exponential, Poisson and normal mean, setting the slope of the log-likelihood to 0 gives the moment equation, so the two methods agree.`

7. `l17-ratio-of-likelihoods.json` | screens[4] prose | unclear | Screens 0 to 3 put the alternative on top and reject when the ratio is large. Screen 4 defines $\Lambda$ with the null on top and never says that the direction has flipped, that $\Lambda \le 1$, or that small $\Lambda$ (large $-2\ln\Lambda$) rejects. The trap on screen 7 then uses $\tfrac{L(0.5)}{L(0.6)}$ without comment. | Insert after the definition: `The null is now on top, so $\Lambda \le 1$, and a small $\Lambda$ (a large $-2\ln\Lambda$) counts against it.`

8. `l17-ratio-of-likelihoods.json` | quiz[1] `q-nonnested`, quiz[2] `q-edge`, quiz[3] | unclear | (a) "Nested" is the key of quiz[1] and sits in quiz[3]'s prose, but no screen defines it. (b) Quiz[1]'s key says the normal and the $t$ "are not nested", while its own explanation and the `df` distractor say the normal is the $t$ at the edge of the range: a boundary failure, the same one as quiz[2], not non-nesting. (c) "Random effect" and "information criterion" are taught nowhere upstream. | (a) Add to screens[6] prose: `Two models are **nested** when the null model is the full model with some parameters fixed or tied.` (b) Quiz[1] correct option: `The normal is not the $t$ with a parameter fixed inside its range, so Wilks' limit does not apply`; `fine` why: `You applied Wilks without its hypotheses. The null must fix parameters of the larger model at values inside the range.`; `small` why: `Sample size is not the issue. The null must sit inside the larger model's range.`; feedback.correct: `Right: Wilks needs the null to fix parameters at values inside the range.`; explain: `The normal is the limit of the $t$ as its degrees of freedom go to infinity, the edge of the range, so Wilks' theorem does not apply. Compare such models by other means, such as a simulation of the statistic.` (c) Quiz[2] prose: `An analyst tests whether a variance parameter is 0, using $-2\ln\Lambda$ against the $\chi^2_1$ cut-off 3.841.`

9. `l16-best-possible-precision.json` | screens[9] explain, second sentence | unclear | "both are the best any estimator can do" states the bound without its conditions. It covers unbiased estimators only (the lesson's own trap), and for volatility $\tfrac{1}{\sqrt{2n}}$ is the large-sample figure. | `Volatility was known to 5% after 200 days, and no unbiased estimator improves much on either figure.`

10. `l17-ratio-of-likelihoods.json` | screens[2] prose, summary idea 1 | unclear | The lemma is stated for tests "of the same size", then screen 3 uses it against a test of size 0.0156, smaller than 0.0207. The lemma covers that case, but the statement as taught does not. | Prose: `among all tests of the same size or smaller the likelihood-ratio test has the greatest power`. Summary: `has the greatest power among tests of its size or smaller.`

11. `l18-counts-against-expectations.json` | screens[2] prose | unclear | The lesson never says that the rejection region is the upper tail only, although the $z$ and $t$ tests upstream are two-sided. | Add to the prose after the approximation sentence: `Only large values count against the null, so the rejection region is the upper tail alone.`

12. `l18-counts-against-expectations.json` | screens[3] hint 2, widget | minor | The hint sums the printed column to 2.657 (true for the rounded entries); the feedback says 2.6556 and the explanation 2.656. A learner who doubles the hint's sum types 5.314, accepted only by the engine's $10^{-9}$ slack on `tol` 0.003. | `"tol": {"abs": 0.005}` (the `half` value 2.656 stays outside). Hint: `The column adds to about 2.656, then double.`

13. `homework-4.json` | items[6] `h-np-normal` widget | minor | `tol` 0.001 rejects a two-place normal table: $\Phi(0.35) = 0.6368$ and $\Phi(0.36) = 0.6406$ both fail against 0.6387. | `"tol": {"abs": 0.003}` (0.05, 0.3613 and 0.4113 stay outside).

14. `l15-sharpness-of-the-peak.json` | screens[10] explain | minor | "The same 200 days pin down the mean return far worse" is true only relative to the mean's size; in absolute terms the mean's standard error is $\sqrt 2$ times the volatility's. | `Relative to its size, the mean return is pinned down far worse by the same 200 days.`

15. `l16-best-possible-precision.json` | screens[4] feedback `unbiased` | minor | "$\tfrac{1}{\bar X}$ is a convex function of $\bar X$, so it overshoots" leans on Jensen's inequality, taught only in `random-vars` L5, which this level does not gate. | `You assumed the MLE is unbiased. Small values of $\bar X$ send $\tfrac{1}{\bar X}$ up by more than large values bring it down, so it overshoots.`

16. `l17-ratio-of-likelihoods.json` | summary idea 3 | minor | "score tests" is named once, here, and never introduced; screen 5 calls the two $z$ tests by their variances. | `in other models the likelihood-ratio test and the two $z$ tests agree only in large samples.`

17. `l16-best-possible-precision.json` | summary idea 2 | minor | "the median reaches $\tfrac{2}{\pi}$ of it" states a large-sample efficiency as exact and reads as if the variance were below the bound. | `the median's efficiency is about $\tfrac{2}{\pi}$ in large samples, and that of $\tfrac{n - 1}{\sum x_i}$ is $\tfrac{n - 2}{n}$.`

18. `l14-what-data-can-forget.json` | screens[3] explain; screens[8] explain | minor | "as an MLE is whenever a sufficient statistic exists" is loose (the whole sample is always sufficient; the claim needs a unique MLE). "Its MLE" in screen 8 has no referent. | Screen 3: `The MLE, $\tfrac{n}{\sum x_i}$, is a function of it, as a unique MLE is of any sufficient statistic.` Screen 8: `The MLE of $\lambda$, $\bar x = \tfrac{1}{n}\sum x_i$, is a function of it.`

19. `l18-counts-against-expectations.json` | screens[10] explain | minor | "fill type does depend on venue" reads p = 0.043 as a fact, one line after p = 0.052 "survives, narrowly". | `Independence: $X^2 = 9.87$ on 4, p = 0.043, so the data reject independence at 5%, mostly because venue C partially fills 32% of orders against 20% overall.`

20. `l18-counts-against-expectations.json` | screens[7] option `percent` | minor | The question is "What happens to $X^2$?"; this option is an instruction, not an outcome, so it is ruled out by form. | Text: `It is unchanged once the table is entered as percentages, which is the right way`. Keep its `why`.

21. `l15-sharpness-of-the-peak.json` | screens[9] prose and explain | minor | "Observed information" appears in the explanation and the function name without a definition. | Add to the prose: `Minus the second derivative of the log-likelihood at the estimate is called the observed information.`

22. `review-4.json` items[3] `r-eff`; `homework-4.json` items[4] `h-gof-code` | freshness | minor | `r-eff` is l16 s5 with the decimal point moved (0.04 over 0.05 against 0.4 over 0.5, both 0.8). The first test and example of `h-gof-code` is the l18 s6 sample (30, 62, 56, 32 and 20 split as 12, 6, 2). | `r-eff`: bound 0.03, variance 0.05, answer 0.6, `accept` `0.6: $\tfrac{0.03}{0.05}$`, `wrong` 1.6667 and 0.02, explain `Efficiency is $\tfrac{0.03}{0.05} = 0.6$: the estimator needs $\tfrac{1}{0.6} = 1.67$ times the data of an efficient one for the same precision.` `h-gof-code`: leave the test (a fixer must not re-key a code test by hand); note it in the report.

## Counts

22 findings: 5 `wrong`, 6 `unclear`, 11 `minor`.

By file: l13 one (6); l14 two (4, 18); l15 four (2 in part, 5, 14, 21); l16 four (2 in part, 9, 15, 17); l17 six (1, 2 in part, 7, 8, 10, 16); l18 four (11, 12, 19, 20); review-4 one (22); homework-4 three (3, 13, 22).

## Verdict by file

- `l13`: sound. One term used early (6).
- `l14`: sound; the definition, the theorem and the model-dependence of sufficiency are all right. One false distractor explanation (4).
- `l15`: sound mathematics throughout, including both forms, their condition and the reparametrisation. Two grading or count slips (2, 5).
- `l16`: the bound, its conditions, the proof and the counterexamples are right. One overstated closing sentence (9), one tolerance (2).
- `l17`: the theorems are stated with their conditions, but the lesson needs its direction and nesting sentences (7, 8, 10) and two tolerances (1, 2) before it goes on.
- `l18`: correct, with the Chernoff-Lehmann caveat a welcome detail. Add the upper-tail sentence (11).
- `review-4`: covers all six lessons; every key right.
- `homework-4`: covers all six lessons; the performance task `h-cr-poisson`, its model and rubric are correct and complete (SymPy and simulation agree with every line). One wrong number in the analyst note (3).

No finding touches a theorem's truth: the five `wrong` items are three grading or tolerance faults, one count and one distractor explanation. After a fix pass on 1 to 11 the level can ship.

## Continuity

- Prerequisites hold: likelihood, MLE, bias, MSE and the Beta prior (`estimation` l4 to l8, l12); size, power and p-values (`testing` L1, L2, with Bayes in odds form in l7); chi-square, Gamma, $t$ and joint densities (`limits-thm` l14 to l18); $|\rho| \le 1$ (`random-vars` l11). The quoted debt in l15 s5 matches `estimation/l8` word for word. The only reliance on the non-gated `random-vars` L5 is finding 15.
- Exam `topic-1.6` has no item on any level 4 lesson. The brief defers the exam extension with the new skills; nothing to fix here.
- `fresh-check` on `review-4` and `homework-4`: 0 hits, one advisory (shared 0.5, 0.6, 0.4 between `r-lrt-coin` and l17 s0, a different question). Finding 22 is what it missed.

## Engine

- A validator advisory for numeric keys whose own rounding is rejected: when `answer` has more decimal places than `tol` admits (the key rounded to 2 places, or to one place fewer than written, falls outside `tol`), warn. Findings 1, 2 and 12 are this class; the number-sense L4 review found the same class with π.
- `fresh-check` does not read the literals inside a code item's `tests[].call` or `examples[].call`, so a homework code test that reuses a lesson's dataset (finding 22) is not reported.

## Fix pass

Basis sources: DeGroot and Schervish (DS) 4th ed.; Casella and Berger (CB) 2nd ed. All numbers recomputed twice (closed form and SciPy, quadrature or enumeration) in `docs/reports/testing-L4-numbers.py`.

1. l17 s10: fixed. Tolerance 0.006 (6.81 accepted, 29.64 and -6.806 outside); accept line `29.639 - 22.833`. Check: 100 ln 1.345 = 29.639, 100 ln(1.345/1.69) = -22.833, total 6.806.
2. l15 s1, l16 s4, l17 s4: fixed. Tolerance 0.005 each (4.17, 2.22, 3.76 accepted; every wrong value outside). Also widened for the same fault where the 2-place key is a natural answer: l17 s2 (0.1256, tol 0.005), l18 s1 (0.2487, tol 0.0015), l15 s7 (0.0891, tol 0.001), review-4 r-param (0.2828, tol 0.003), homework h-rb-zero (0.1074, tol 0.003); all `wrong[]` stay outside. Keys with tiny magnitude (0.0458, 0.0445, 0.024, 0.0099, 0.0249, 0.0025) left, since 2 places would erase them.
3. homework h-analyst: fixed, 20 cells (not 31). Enumerated by normal cdf, by quadrature and by standardised cdf: 20 of 40 cells expect under 1, 26 under 5. Prompt and model both say 20; no other line of the item gives a count.
4. l14 s1 `rises`: fixed. Order chance p^7 (1-p)^3 is 0.00222 at 0.7 and 0.00048 at 0.9, so it moves but does not rise throughout; option and `why` now say "moves".
5. l15 q-overlap: fixed. 254 prices give 253 returns and 249 windows; 254 daily returns give 254 - 5 + 1 = 250 windows. Prose now says 254 daily returns.
6. l13 s3: fixed (slope of the log-likelihood set to 0, no "score").
7. l17 s4: fixed. Basis CB 8.2.1: lambda = sup over the null / sup over all, so 0 <= Lambda <= 1 and small values reject. Sentence inserted.
8. l17: fixed. (a) "nested" defined in s6. (b) quiz[1] re-worded: normal is the t only as nu goes to infinity, the edge of the range (CB 10.3.1 needs the null to fix parameters inside the range). (c) "random effect" replaced by "a variance parameter".
9. l16 s9: fixed. Basis CB 7.3.9: the bound holds for unbiased estimators; for sigma the 1/sqrt(2n) figure is asymptotic (CB 10.1.12). Sentence now "no unbiased estimator improves much on either figure".
10. l17 s2 and summary: fixed. Basis DS 9.2 (Neyman-Pearson) and CB 8.3.12: the LRT maximises power among all tests with size at most alpha, so a smaller-size test (0.0156) is covered. Wording now "same size or smaller".
11. l18 s2: fixed (upper-tail sentence). Basis DS 10.1: X^2 is a sum of squares, departures from the null only inflate it.
12. l18 s3: fixed. Tolerance 0.005; the 2.656 `wrong` stays outside; hint now "about 2.656".
13. homework h-np-normal: fixed. Tolerance 0.003; 0.6368 and 0.6406 accepted, 0.05, 0.3613 and 0.4113 outside.
14. l15 s10: fixed (relative to its size). Mean SE sqrt(sigma^2/n) vs volatility sigma/sqrt(2n): ratio sqrt 2 in absolute terms, so the claim is relative.
15. l16 s4 feedback `unbiased`: fixed (no Jensen).
16. l17 summary 3: fixed (no "score tests").
17. l16 summary 2: fixed. Basis CB 10.1.12: median efficiency is 2/pi only asymptotically (normal); (n-2)/n for (n-1)/sum x: variance lambda^2/(n-2) against bound lambda^2/n.
18. l14 s3 and s8: fixed (unique MLE; "The MLE of lambda").
19. l18 s10: fixed (p = 0.043 worded as rejection at 5%).
20. l18 s7 `percent`: fixed (now an outcome).
21. l15 s9: fixed (observed information defined).
22. review-4 r-eff: fixed (0.03 over 0.05 = 0.6; wrong 1.6667 and 0.02). homework h-gof-code: left as the reader advised; its first test and example reuse the l18 s6 sample (30, 62, 56, 32, 20 split 12, 6, 2), not re-keyed by hand. Deferred.

Changed graded values (old -> new, working):
- review-4 r-eff answer 0.8 -> 0.6 (0.03/0.05); wrong inv 1.25 -> 1.6667 (0.05/0.03), wrong gap 0.01 -> 0.02 (0.05 - 0.03); accept line updated.
- Tolerances: l17 s10 0.003 -> 0.006; l15 s1 0.001 -> 0.005; l16 s4 0.002 -> 0.005; l17 s4 0.002 -> 0.005; l17 s2 0.0005 -> 0.005; l18 s3 0.003 -> 0.005; l18 s1 0.001 -> 0.0015; l15 s7 0.0003 -> 0.001; homework h-np-normal 0.001 -> 0.003; homework h-rb-zero 0.0005 -> 0.003; review-4 r-param 0.0005 -> 0.003. `r-eff` wrong 1 tolerance 0.001 -> 0.005. No other answer or `wrong` value changed. h-analyst's 31 -> 20 is prose in an ungraded longform item.

Gates: number script exit 0 (523 of 523). `read-numbers.py`: 402 of 404; the two failures are its hard-coded old values (r-eff 0.04/0.05 = 0.8, and "below1 == 31"), which now disagree with the corrected content on purpose. `run-code.py`: exit 0, all code items pass. Validator 0 errors. Voice scan: 0 explanations over three sentences; 1 sentence over 35 words, in homework-3 (level 3, not touched). Playthrough with `--local-cdn`, with and without `--mobile`: l13 to l18, review-4, homework-4 all pass (16 runs). `h-cr-poisson` and its rubric unchanged, so `testing-4-perf.md` is unchanged.
