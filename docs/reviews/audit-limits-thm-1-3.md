# Concept audit: limits-thm L1 to L3 (round 1, blind read, 11 Nov 2026)

Scope: lessons l1 to l13, review-1 to review-3, homework-1 to homework-3, problems-1 to problems-3, `fluency-l1-counting-successes.json`, `fluency-l7-bell-curve.json`. Every screen, item, hint, `why`, `byKey`, `explain`, model answer, rubric and code solution was read. Ledger: `docs/reports/audit-limits-thm-1-3-ledger.md` (368 rows: 335 correct, 26 imprecise, 5 misleading, 2 wrong, 0 unverified). Script: `docs/reports/limits-thm-L1-3-concepts.py` (76 checks, 2 left failing on purpose, findings 1 and 2). Sources are named in the ledger header.

Format: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

Totals: 28 findings. `wrong` 2 (both minor). `imprecise` 23 (1 serious, 22 minor). `misleading` 3 (all minor). No graded key, `wrong[]` value, slip line or code solution was found wrong: every one was recomputed.

## Wrong

1. l4-without-replacement.json | `screens[7].explain.text` | wrong | minor | "Each factor is below 0.8, so the binomial overstates a clean result." The first factor of the product on the same line is $\tfrac{16}{20} = 0.8$ exactly. | Arithmetic: the factors are 0.8, 0.789, 0.778, 0.765, 0.75. Script check "l4 s7 CLAIM" fails on purpose. The conclusion (the product is below $0.8^5$) stands. | Replace the last sentence with: "The first factor is 0.8 and each later one is smaller, so the binomial overstates a clean result."

2. l7-bell-curve.json | `screens[3].explain.text` | wrong | minor | "So the desk loses more than £8k on about 2.3% of days, roughly once a month." A month has about 21 trading days; 2.28% of days is one day in 44. | $1/(1 - \Phi(2)) = 43.96$ days, about two months of trading. Script check "l7 s3 CLAIM" fails on purpose. The lesson's own later screen converts correctly (0.55% is "about once in 180 trading days"). | Replace the sentence with: "So the desk loses more than £8k on about 2.3% of days, roughly once every two months of trading."

## Imprecise, serious

3. l12-skill-or-luck.json | `screens[5].prose`, `screens[5].widget.lines[2].text` (also `summary.ideas[2]`, `summary.formula`) | imprecise | serious | The Sharpe ratio is defined as $\mu\sqrt{252}/\sigma$ for "daily returns", with no risk-free rate. This is the first definition of the Sharpe ratio a learner meets in the curriculum; the `markets` course states the excess-return form later. A learner carries "mean return over sd" into an interview. | Sharpe (1966; 1994, "The Sharpe Ratio"): mean return in excess of the risk-free (or benchmark) return, over the sd of that excess. Hull, *Options, Futures and Other Derivatives*, uses the same form. For a self-funded P&L the two agree, which is why the numbers on these screens need no change. | `screens[5].prose`: "Daily returns, measured above the risk-free rate, have mean $\mu$ and sd $\sigma$, independent across 252 trading days a year. We record $T$ years." `screens[5].widget.lines[2].text`: "So the annualised Sharpe ratio, mean excess return over sd, is $SR = \dfrac{252\mu}{\sqrt{252}\,\sigma} = \dfrac{\mu\sqrt{252}}{\sigma}$". No key changes.

## Imprecise, minor: conditions of the limit theorems

4. l11-sums-look-normal.json | `screens[4].explain.text` | imprecise | minor | "The theorem needs independence, identical draws and a finite $\sigma^2$." Independence and identical distribution are sufficient for this form, not necessary. The same lesson's last transfer screen and summary already say that dependence only slows or can block the limit, so the "needs" contradicts them. | Lindeberg-Feller drops identical distribution; martingale and mixing versions relax independence (Durrett 3.4.2, 8.2). The course's own homework-3 `items[9]` proves a law for non-identical bets. | Replace the explanation with: "This form of the theorem assumes independent, identical draws and a finite $\sigma^2$; other forms relax the first two. Divide by $\sigma/\sqrt n$ and the limit is $N(0, 1)$ whatever the starting shape. That is why sums of many small effects look normal."

5. l9-averages-settle.json | `summary.formula.note` | imprecise | minor | "Needs independent, identically distributed draws with a finite mean." Sufficient, not necessary: uncorrelated draws with bounded variances also obey the weak law. | Chebyshev proof (Durrett Thm 2.2.3), as homework-3 `items[9]` (c) shows for non-identical bets. | "Holds for independent, identically distributed draws with a finite mean. Weaker conditions also work."

6. l11-sums-look-normal.json | `summary.ideas[0]` | imprecise | minor | "Rescaled sums and averages of independent draws with finite variance approach $N(0, 1)$." Without "identically distributed" (or a Lindeberg condition) this is false: one draw can dominate the sum. | Durrett 3.4.2: the Lindeberg condition is needed for non-identical draws. | "Rescaled sums and averages of independent, identically distributed draws with finite variance approach $N(0, 1)$, whatever one draw looks like."

7. l11-sums-look-normal.json | `screens[2].feedback.correct`, `screens[2].explain.text` | imprecise | minor | "A symmetric start gets to the bell fastest" and "How fast the bell appears depends on how lopsided one draw is." Speed also depends on tail weight. A learner infers that symmetric fat-tailed returns reach the bell quickly. | Berry-Esseen bound uses $E|X|^3$, not skew alone. Script check "MC symmetric t(3)": for a symmetric $t$ with 3 degrees of freedom, $P(|Z| < 0.5)$ at $n = 3$ is 0.48 against the normal 0.38, while the uniform is within 0.01. | `feedback.correct`: "A symmetric, light-tailed start reaches the bell quickly." Third sentence of `explain.text`: "How fast the bell appears depends on how lopsided one draw is and how heavy its tails are."

8. l11-sums-look-normal.json | `screens[8].widget.options[2].why` (also `hints[0]`, `feedback.generic`) | imprecise | minor | "A 20-day return is a sum of 20 daily ones." True for log returns; simple returns compound. The convention is not stated in the lesson. | $\ln(S_{20}/S_0) = \sum \ln(S_i/S_{i-1})$; $1 + R_{20} = \prod (1 + R_i)$. | Add as the last sentence of `screens[8].prose`: "Returns here are log returns, which add across days."

9. l11-sums-look-normal.json | `screens[9].explain.text` | imprecise | minor | "correlated positions would widen the bell." Only positive correlation widens it; negative correlation narrows it. | $\operatorname{Var}(\sum X_i) = \sum \operatorname{Var}(X_i) + \sum_{i \ne j}\operatorname{Cov}(X_i, X_j)$. | Third sentence: "Independence is doing the work: positively correlated positions would widen the bell."

10. homework-3.json | `items[2].explain.text` | imprecise | minor | "the law itself holds with a finite mean alone, by a harder argument." That is Khinchin's law for identically distributed draws; the item's hypotheses say only independent with a common mean and variance. | Durrett Thm 2.2.14 (iid, finite mean). Independent, non-identical draws with finite means alone can fail the law. | Second sentence: "This proof needs a finite variance; for identically distributed draws the law holds with a finite mean alone, by a harder argument."

11. l10-bound-that-holds.json | `screens[9].prose`, `screens[9].explain.text` | imprecise | minor | "Chebyshev on $\bar X_n$, whose variance is $\sigma^2/n$" and "Chebyshev says 4,000 trades always suffice." The variance $\sigma^2/n$ needs independent (or uncorrelated) trades, which this screen does not state; "always" then overclaims. | Row 240 of the ledger: the previous lesson derives $\sigma^2/n$ from independence. | First sentence of `prose`: "A strategy's trades are independent, and the return per trade has sd $\sigma = 2\%$." First sentence of `explain.text`: "Chebyshev says 4,000 independent trades suffice, whatever the shape of one trade."

12. l9-averages-settle.json | `screens[4].feedback.correct` | imprecise | minor | "The law bounds the chance of a miss, for any margin you choose." The law gives a limit, not a bound; the bound is Chebyshev's, taught in the next lesson. | Statement on the same screen: $P(\cdot) \to 0$. | "The law says the chance of a miss tends to 0, for any margin you choose."

13. l11-sums-look-normal.json | `screens[8].explain.text` | imprecise | minor | "the approach is slower than the theorem promises." The theorem promises no rate. | The comparison that holds is with independent days. Script check "MC l11 s8": excess kurtosis of 20-day sums is 4.1 with clustering against 0.5 for the same days shuffled. | Second sentence: "Volatility clusters, so the days are not independent, and the approach is slower than for independent days."

## Imprecise, minor: approximations and conventions

14. l13-approximating-binomial.json | `summary.ideas[2]` | imprecise | minor | "When $p$ is near 0 or 1 the bars are lopsided; the Poisson with $\lambda = np$ does better." For $p$ near 1 the Poisson applies to the failure count with $\lambda = n(1 - p)$, as `screens[7].explain` says. And with $np(1-p)$ large the normal is fine whatever $p$. | Law of rare events needs $p \to 0$ with $np$ fixed (Feller VI.5). | "When $p$ is near 0 and $np(1-p)$ is small, the bars are lopsided and the Poisson with $\lambda = np$ does better. For $p$ near 1, count failures instead."

15. l13-approximating-binomial.json | `screens[9].question` | imprecise | minor | "What is the quick normal estimate of the chance of 30 or more defaults?" The key 0.0159 uses the continuity correction, which the question does not ask for. An uncorrected 0.0119 is a valid reading and gets only the generic line. | $1 - \Phi(10/\sqrt{19.6}) = 0.0119$; $1 - \Phi(9.5/\sqrt{19.6}) = 0.0159$. | Question: "What is the normal estimate, with the continuity correction, of the chance of 30 or more defaults? Give 4 decimal places." Optional `wrong` entry `{"id": "nocc", "value": 0.0119, "tol": {"abs": 0.0003}}` with `byKey.nocc`: "That starts at 30, without the correction. Start at 29.5."

16. l6-uniform-exponential.json | `screens[3].prose`, `quiz[1].prose`, `quiz[3].prose` | imprecise | minor | Exponential waits are asserted from "arrive at random, on average $\lambda$ per minute", and `quiz[3]` says "Trades arrive at 2 a minute, so gaps are exponential". An average rate alone does not give exponential gaps; independent arrivals at a steady rate do. The Poisson process is named only on `screens[8]`. | Ross 9.1: exponential gaps characterise the Poisson process. Evenly spaced trades have the same rate and constant gaps. | `screens[3].prose` first sentence: "Trades arrive independently of each other at a steady average rate of $\lambda$ per minute." `quiz[1].prose`: "Large orders reach a dealer independently at a steady rate, 0.25 a day on average." `quiz[3].prose`: "Trades arrive independently at a steady 2 a minute, so gaps are exponential with mean 30 seconds."

17. l6-uniform-exponential.json | `screens[9].explain.text` | imprecise | minor | "The hazard rate is the exponential's $\lambda$: the default chance per year for an issuer still alive." A hazard is a rate, not a yearly probability; the course's own Poisson trap ("a rate is not a chance") teaches the difference. | One-year default chance is $1 - e^{-0.02} = 0.0198$, not 0.02; at $\lambda = 2$ the gap is plain. Hull 24.1. | Second sentence: "The hazard rate is the exponential's $\lambda$: the default rate per year for an issuer still alive, close to a yearly chance when it is small."

18. l7-bell-curve.json | `screens[9].prose`, `screens[9].explain.text` | imprecise | minor | "The 1-day 99% VaR is the return $r$ that the day beats 99% of the time." VaR is quoted as a positive loss, as this course does in the density lesson and in homework-2 and problems-2. Here it is a negative return. | Hull 22.1: VaR is the loss level not exceeded with the stated confidence. | `prose`: "Same share, $R \sim N(0.05, 1.2^2)$ in %. The 1-day 99% VaR is the loss exceeded on only 1% of days. First find the return $r$ with $P(R < r) = 0.01$; the VaR is $-r$. Here $\Phi(-2.326) = 0.01$." First sentence of `explain.text`: "$r = 0.05 - 2.326 \times 1.2 \approx -2.74\%$, so the VaR is quoted as 2.74%." The key is unchanged.

19. l12-skill-or-luck.json | `screens[4].prose` | imprecise | minor | The $t$-ratio is written with $\sigma$ as if known. In practice, and in interview usage, it uses the sample sd. | With the sample sd the ratio is Student $t$ with $n - 1$ degrees of freedom, close to $N(0, 1)$ for the $n$ used here (Slutsky). | Add as the last sentence of `prose`: "In practice $\sigma$ is estimated by the sample sd, which changes little over hundreds of days."

20. homework-3.json | `items[7].prompt` (part 4), `items[7].model` (part 4) | imprecise | minor | $1 - (1 - 0.097)^{10} \approx 0.64$ needs the 10 strategies to be independent. Neither the prompt nor the model says so, though the lesson screen it follows does. Correlated variants give a smaller figure. | Product rule needs independence. | Prompt part 4: "Explain how testing 10 strategies changes your view. Put a number on it, assuming none has skill and the 10 are independent." Model: "The chance the best of 10 independent strategies does is $1 - (1 - 0.097)^{10} \approx 0.64$."

21. l3-rare-events.json | `screens[5].explain.text` | imprecise | minor | "As $n \to \infty$, $2(1 - 2/n) \to 2$. So a Poisson count has mean and variance both equal to $\lambda$." A limit in distribution does not by itself carry the variance, so the "So" is a heuristic. The number is right. | Billingsley Thm 25.12 (needs uniform integrability). Direct proof: $E[X(X-1)] = \lambda^2$, as homework-1 `items[1]` says. | "As $n \to \infty$, $2(1 - 2/n) \to 2$, which points to a variance of $\lambda$; summing the Poisson pmf directly confirms it. So a Poisson count has mean and variance both equal to $\lambda$. Its standard deviation is $\sqrt{\lambda} \approx 1.414$ here."

22. l2-first-success.json | `screens[5].explain.text` | imprecise | minor | "If fills really do get likelier, the minutes are not independent and the geometric model is wrong." A chance that changes from minute to minute breaks the model even when the minutes are independent. | Geometric needs both independence and a constant $p$. | Third sentence: "If fills really do get likelier, the chance is not the same each minute and the geometric model is wrong."

23. l1-counting-successes.json | `quiz[1].explain.text` | imprecise | minor | "So $X$ is often 0 or 10, far more than $\text{Bin}(10, 0.4)$ predicts." Overstated: a shared position raises the chance of counts near the ends; nothing in the item makes exactly 0 or 10 "often". | Under partial dependence the mass spreads towards both ends, not onto them. | Third sentence: "So $X$ lands near 0 or near 10 far more often than $\text{Bin}(10, 0.4)$ predicts."

24. l4-without-replacement.json | `quiz[2].explain.text` | imprecise | minor | "No replacement is needed for the mean." Reads as a condition on the sampling. The point is that replacement makes no difference to the mean. | Linearity, as the sentence before says. | Third sentence: "The mean is the same with or without replacement."

25. l8-lognormal.json | `screens[6].prose` (also option `sure`) | imprecise | minor | "Its expected price in a year is $50e^{0.08} = \text{£}54.16$, so it is expected to rise 8%." The expected simple rise is 8.3%. | $54.16/50 - 1 = e^{0.08} - 1 = 0.0833$. | "…so it is expected to rise about 8%." Option `sure`: "More than 0.6, since it is expected to rise about 8%".

## Misleading, minor

26. l6-uniform-exponential.json | `screens[10].prose`, `screens[10].explain.text`, `summary.ideas[0]` | misleading | minor | "Knowing only the range, the honest choice is the uniform", "Any other shape would claim knowledge we lack" and "It is the density to use when you know only the range" state the principle of indifference as a rule. It is a modelling convention (maximum entropy on an interval), and it depends on the scale chosen: uniform in price is not uniform in log price. | Cover and Thomas ch. 12 (maximum entropy); Bertrand's paradox for the scale dependence. | `prose` second sentence: "Knowing only the range, a common default is the uniform: it favours no price." `explain.text`: "Width $b - a = 8$, so the variance is $\tfrac{64}{12} \approx 5.33$ and the sd is about 2.31 pence. The uniform is the maximum-entropy density on an interval: it adds least beyond the range. It is a modelling default, not a fact about fills, so check it against data when you can." `summary.ideas[0]` last sentence: "It is the usual default when you know only the range."

27. l9-averages-settle.json | `screens[1].explain.text` | misleading | minor | "Rare big wins make a payoff lopsided, and lopsided averages need more draws." The slow settling comes from the size of the sd against the mean, not from skew. A symmetric bet of plus or minus £3 settles as slowly. | $\operatorname{Var}(\bar X_n) = \sigma^2/n$, the result this lesson derives; here $\sigma = \sqrt{100 \times 0.1 - 1} = 3$ against a mean of 1. | Third sentence: "One card has sd £3 against a mean of £1, and noisier draws need more of them."

28. l12-skill-or-luck.json | `screens[8].canvas.params.xLabel` | misleading | minor | The axis "Plausible true Sharpe ratio" sits under a normal curve centred on the estimate. That reads as a probability distribution for the true value, the swap `screens[4]` calls the prosecutor's fallacy. | The curve is the sampling spread of the estimate; a statement about the true value needs a prior. | xLabel: "Estimated Sharpe ratio, plus or minus two standard errors".

## Checked and clean

Points pressed for this course, with the outcome.

- Law of large numbers. The statement (`l9` `screens[4]`) has iid and a finite mean; the derivation uses "need not add" for dependent draws; St Petersburg and Cauchy are right (data and Monte Carlo). Only the "needs" note (finding 5) and one feedback line (12) slip.
- Central limit theorem. The statement is Lindeberg-Lévy. The trap that a large sample of single draws is not normal is right. Sums of normals are exactly normal. Exact bars for exponential and uniform averages were recomputed from the gamma and Irwin-Hall CDFs. The exact gamma tail 0.0844 is right.
- Markov and Chebyshev. Hypotheses ($X \ge 0$; finite mean and variance) are stated where used; the sharpness example is right; one-sided events are placed inside two-sided ones each time.
- Continuity correction. Every corrected key and every "wrong side" slip was recomputed; every quoted exact value (0.0553, 0.1308, 0.162, 0.0284, 0.0207, 0.0796, 0.0978, 0.5704, 0.0190, 0.0626, 0.0605) matches.
- Poisson limit. The derivation is the standard one with $k$ fixed; rate against probability is handled well; "when the approximation is good" is taught through $np(1-p)$ with the rule of thumb labelled as one each time.
- Lognormal. Median $e^{\mu}$, mean $e^{\mu + \sigma^2/2}$, drag, and $P(S_T > K)$ are right throughout; the mode is not taught and nothing false is said about it.
- Memorylessness. Geometric and exponential proofs are right; the without-replacement and triangle counter-examples are right.
- One- and two-sided figures. 1.645, 1.96, 2.326, 0.0228 against 0.0455 are used on the correct side everywhere, including `problems-3`.
- Finite-sample statements. The long exact claim in homework-3 `items[9]` (0.0528 at 131, first at most 0.05 at 136, stays below) was verified by exact summation to $n = 419$.
- Code. `binom_pmf`, `hyper_pmf`, `phi`, `exact_tail`, `normal_tail` teach the taught method and their test values were recomputed.
- Ledger notes that are not findings: trading days are 250 on two screens and 252 elsewhere, each stated where used; `l11` `quiz[2]` (0.121) has no continuity correction because the correction is taught two lessons later (exact 0.1152).

## Overlap with the earlier reviews

Read after the blind pass was committed (commit "WIP: concept audit limits-thm L1 to L3 round 1"): `docs/reviews/review-1.5.md` (limits-thm section and its fix pass), `docs/reviews/review-problems-1.5-c.md` (sets 1 to 3), `docs/reviews/review-perf-retrofit-9.md` (the three derivation items). Their fix passes were applied before this audit, so the text audited here is the corrected text. Only conceptual findings are counted (meaning, hypothesis, convention, reasoning, or a slip value that does not match its stated slip); notation, sentence counts, tolerances, rubric marking and re-teaching notes are not.

| | count | findings |
|---|---|---|
| Audit only | 28 | all 28 above |
| Both | 0 | none |
| Review only | 11 | all fixed before this read, so none could be found here (listed below) |

Earlier conceptual findings this audit did not raise, because the text was already fixed: `review-1.5.md`: l1 "skill-free week" for a 55% strategy; l8 `screens[8]` slip `simple` value against its `why`; l9 `screens[5]` proof assumes a finite variance; l12 `screens[3]` "skill shows once" at an expected $t$ of 2; l12 SE of the Sharpe ratio without "for small Sharpe ratios"; homework-2 `items[6]` wrong reason for the normal VaR gap; homework-3 `items[7]` part 5 "any of these". `review-problems-1.5-c.md`: problems-2 `p-default-drag` slip value against its stated slip; problems-1 `p-block-calls` part 2 hand of four against "stops at the first taker". `review-perf-retrofit-9.md`: homework-3 `items[9]` exact claim unsupported; homework-2 `items[8]` sign of $D$.

Each of those fixes was re-read as a ledger row and holds (rows 19, 207, 240, 294, 300, 223, 341, 360, 349, 346, 228). No finding here is in text written by a fix pass.

The two families share ground without sharing a sentence: the earlier read added "assume a finite variance" and "for small Sharpe ratios", and this audit finds the neighbouring gaps (iid stated as needed, the Sharpe ratio without the risk-free rate, $\sigma$ as known). A single read missed all 28; all but one are minor.

## Checks

- `node tools/validate.mjs`: 0 errors.
- Course number scripts: `fluency-limits-thm-numbers.py`, `limits-thm-1-perf-numbers.py`, `limits-thm-2-perf-numbers.py`, `limits-thm-3-perf-numbers.py`, `problems-limits-thm-numbers.py` all exit 0. The last three need `scipy`, which was missing from the sandbox and was installed with pip for this run.
- `docs/reports/limits-thm-L1-3-concepts.py`: 76 checks, 74 pass, exit 1. The two failing checks are findings 1 and 2 and pass once those sentences are fixed (the checks encode the content's claim; the fixer should replace them with the corrected figures).
- Playthrough: not run; no grading defect is suspected.

## Fix pass

Fixer: Opus, 11 Nov 2026. Each basis is the fixer's own. All edits are text-only except finding 15, which adds one slip (`wrong` id `nocc`, value 0.0119, tol 0.0003, with its `byKey` line) to `l13` `screens[9]`; no key, option id, test or code changed. The `l7` `screens[9]` widget label was reworded with finding 18.

1. fixed. $16/20 = 0.8$ exactly; $15/19 = 0.789 < 0.8$ and each factor $(16-i)/(20-i)$ falls with $i$. Concepts check rewritten to assert the corrected sentence.
2. fixed. $1/(1 - \Phi(2)) = 1/0.02275 = 43.96$ days; at about 21 trading days a month that is 2.1 months. Concepts check now asserts about 42 days.
3. fixed differently. The Sharpe ratio is the mean excess return over its sd (Sharpe 1994, J. Portfolio Management 21(1), section 1). Every l12 number takes raw daily means, so the definition screen now says once that the lesson takes the risk-free rate as 0, and the formula line and `summary.ideas[2]` say "mean excess return over sd". No numbers change.
4. fixed. Lindeberg-Feller drops identical distribution (Billingsley, Probability and Measure, Thm 27.2), so iid is the assumption of this form, not a requirement; the finite variance stays.
5. fixed differently. Khinchin's weak law needs iid with $E|X| < \infty$ (Durrett 4th ed. Thm 2.2.14); the shown line $\operatorname{Var}(\bar X_n) = \sigma^2/n$ also needs a finite $\sigma^2$, so the note now says both and that weaker conditions also give the law.
6. fixed. Without identical distribution or Lindeberg's condition one draw can dominate (e.g. $X_k$ with sd $2^k$), so "identically distributed" is restored.
7. fixed. Berry-Esseen: $\sup|F_n - \Phi| \le C\,E|X - \mu|^3/(\sigma^3\sqrt n)$, a third absolute moment, so tail weight matters as well as skew.
8. fixed. $\ln(S_{20}/S_0) = \sum_{i} \ln(S_i/S_{i-1})$ while simple returns compound; one sentence states the log-return convention.
9. fixed. $\operatorname{Var}(\sum X_i) = \sum \operatorname{Var} X_i + \sum_{i \ne j} \operatorname{Cov}(X_i, X_j)$: only positive covariance widens it.
10. fixed. The item assumes independence with a common mean and variance, not identical laws; the finite-mean-only law is Khinchin's, for iid draws.
11. fixed. $\operatorname{Var}(\bar X_n) = \sigma^2/n$ requires uncorrelated trades; independence now stated, and the bound holds for any shape with that variance, so "always" became "whatever the shape of one trade".
12. fixed. The weak law states a limit, $P(|\bar X_n - \mu| > \epsilon) \to 0$; a bound for finite $n$ is Chebyshev's.
13. fixed. Lindeberg-Lévy gives no rate; the valid comparison is with independent days.
14. fixed. Poisson limit needs $p \to 0$ with $np$ fixed (Feller I, VI.5); for $p$ near 1 the failures $n - X \sim \text{Bin}(n, 1 - p)$ take that role; with $np(1-p)$ large the normal is fine.
15. fixed. $1 - \Phi(10/\sqrt{19.6}) = 1 - \Phi(2.259) = 0.0119$; $1 - \Phi(9.5/\sqrt{19.6}) = 1 - \Phi(2.146) = 0.0159$. Question now asks for the corrected estimate; new slip `nocc` 0.0119 (band 0.0116 to 0.0122, clear of the key band 0.0156 to 0.0162). Concepts check added.
16. fixed. Exponential gaps characterise the Poisson process, which needs independent increments at a constant rate (Ross, Introduction to Probability Models, 5.3); a rate alone allows evenly spaced trades.
17. fixed. With hazard 0.02 the one-year default chance is $1 - e^{-0.02} = 0.0198$, so the hazard is a rate, near the yearly chance only when small.
18. fixed. VaR is the loss level not exceeded with the stated confidence, quoted as a positive loss (Jorion, Value at Risk, 3rd ed., ch. 5), as `l5` already defines it in £m. The `l7` screen keeps its key $r = -2.74\%$ and now says the VaR is $-r$, a 2.74% loss; label reworded to "Cut-off return r in percent".
19. fixed differently. With the sample sd, $t$ is Student $t_{n-1}$, within about 0.01 of $N(0, 1)$ at its 2.5% point for $n$ in the hundreds ($t_{250,0.975} = 1.970$ against 1.960). Wording shortened.
20. fixed. $P(\max \ge c) = 1 - (1 - q)^{10}$ is the product rule, which needs independence; positively correlated variants give less.
21. fixed. Convergence in distribution does not carry moments without uniform integrability; $E[X(X-1)] = \lambda^2$ from the pmf gives $\operatorname{Var} X = \lambda$ directly.
22. fixed. The geometric needs a constant $p$ as well as independence; a rising chance breaks the model even with independent minutes.
23. fixed. A common factor moves mass towards both ends, not onto 0 and 10 exactly.
24. fixed. $E[X] = \sum E[I_k]$ by linearity regardless of dependence, so replacement makes no difference to the mean.
25. fixed differently. $e^{0.08} - 1 = 0.0833$; text and option `sure` say "about 8.3%" (option id and its `why` unchanged).
26. fixed. On a bounded interval the uniform maximises entropy (Cover and Thomas 2nd ed., 12.1); it is a modelling choice and scale-dependent (uniform in price is not uniform in log price).
27. fixed. Card payout sd $= \sqrt{100 \times 0.1 - 1^2} = 3$ against mean 1; $\operatorname{Var}(\bar X_n) = \sigma^2/n$ depends on the sd, not skew; a symmetric $1 \pm 3$ bet has the same sd.
28. fixed differently. The curve is the sampling spread of the estimate, not a distribution for the true value; the axis is now plain "Sharpe ratio" (the prose already names the band as estimate plus or minus two standard errors), which avoids the auditor's long label.

Gates: validator 0 errors; concepts script 77 checks, exit 0; `fluency-limits-thm-numbers.py`, `limits-thm-1-perf-numbers.py`, `limits-thm-2-perf-numbers.py`, `limits-thm-3-perf-numbers.py`, `problems-limits-thm-numbers.py` exit 0; voice scan 35 on the course: 0 over 35 words, 0 explanations over three sentences; playthrough of the 12 changed lessons and homework-3, desktop and `--mobile`: all 26 runs "All passed" (one batch was re-run after an external `pkill` of playthrough processes).
