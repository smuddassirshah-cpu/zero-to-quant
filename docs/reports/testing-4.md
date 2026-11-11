# testing level 4: Theory of estimation and tests

Brief: `docs/briefs/gap-testing.md`, section "Level 4". Commits: `testing L4: l13` to `l18`, `review-4`, `homework-4`, the number script and two small fix commits (l16 rounding, voice).

## Files

| File | Screens or items | Quiz | Canvases and widgets of note |
|---|---|---|---|
| `l13-matching-moments.json` | 10 | 4 | plane with a rate slider (hook), Gamma density with two sliders, grouped `bars` sim of $2\bar x$ against $\max x_i$ (seed 13), number-line trap, `order` derive with a distractor, `code` (`mom_gamma`, `mom_uniform`, `mle_uniform`), Beta transfer |
| `l14-what-data-can-forget.json` | 10 | 4 | 10 × 12 `grid` of the 120 orders with a $p$ slider and live ratio caption, factorisation `generalise`, `multi` ladders, uniform likelihood plane, Rao-Blackwell on a binomial, Poisson factorisation `order`, risk-store `multi` transfer |
| `l15-sharpness-of-the-peak.json` | 11 | 4 | two log-likelihoods with a dragged point (hook), tangent for the score, `table` widget of three informations, quadratic approximation, the $\sigma/\sqrt{2n}$ debt from estimation l8 paid, uniform edge case, parameterisation trap, $E[S] = 0$ `order`, `code` (`info_bernoulli`, `observed_info`, `mle_sd`, seed 1 and 3) |
| `l16-best-possible-precision.json` | 10 | 4 | three-estimator histogram (2,000 NumPy samples, seed 2016, static values), live grouped sim with a sample-size control (seed 21), exponential MLE sim (seed 5), trap with the $n + 1$ divisor, two-part Cramér-Rao `order` proof, $t = 2$ transfer |
| `l17-ratio-of-likelihoods.json` | 11 | 4 | stacked `pair` of binomials, log-scale ratio curve with a snapped point, Wilks on a $\chi^2_1$ plane, three-test table, degrees-of-freedom ladder, $\Lambda$ trap, $-2\ln\Lambda = z^2$ `order`, `code` (`lr_binomial`, `size_power`, `lrt_poisson`), two-regime volatility transfer |
| `l18-counts-against-expectations.json` | 11 | 4 | `table` widget for expected counts and contributions over grouped bars, $\chi^2_4$ plane with a cut slider and exact tail $e^{-x/2}(1 + x/2)$, $G$ statistic, 2 × 2 and 3 × 2 tables, Poisson goodness of fit, rescaling trap, expected-count `order`, `code` with SciPy checked against `chi2_contingency`, venue transfer `table` |
| `review-4.json` | 9 items, `pass` 0.8, difficulty 2 to 4 | | every lesson at least once |
| `homework-4.json` | 9 items, difficulty 3 to 5 (three at 5) | | `code` (`gof_poisson`, planted bugs caught), `order` (two forms of $I$), longform `h-analyst` (10-point rubric), performance task `h-cr-poisson` (`derivation`, report `docs/reports/testing-4-perf.md`) |

Skills: `course.json` lists only the four original skills, so per the brief l13 and l14 use `ht-setup`, l15 `ht-setup` and `ht-errors`, l16 `ht-errors`, l17 `ht-setup` and `ht-errors`, l18 `ht-setup` and `ht-pvalue`.

## Self-check (SESSION PROTOCOL 4)

1. Validator, `cd app && node tools/validate.mjs`: 0 errors. Warnings on these files: ladder canvas-kind changes, a few problem screens without a canvas, O2 sentence-length advisories.
2. Voice, `VOICE_BASE=app/content/courses/testing python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences; 1 sentence over 35 words, in `homework-3.json` item 8 (level 3, already there, outside this level's files). 0 in level 4.
3. Numbers, `<venv>/bin/python docs/reports/testing-L4-numbers.py`: exit 0, 468 of 468 checks; 36 `byKey` lines listed "check by hand" were read and are explanatory numbers.
4. Playthrough, `node tools/playthrough.mjs --lesson testing/<id>` (and `--set testing/review-4`, `--set testing/homework-4`) with `--local-cdn <pkgs>`: All passed for all eight files, with and without `--mobile`; the six lessons also pass `--tablet`. Every `code` expected value comes from CPython and was confirmed in Pyodide by the playthrough (the solution passes every hidden test there; the seeded `random.Random` tests, `gammavariate` and `mle_sd`, match to the last digit). Screenshots read: fixed a lost $\ell''$ header, literal `\"` quotes, an answer-revealing pair of lines, an empty pre-run sim, a stray point label and an unscaled y axis.

## Definitions and theorems, with conditions and evidence (for the concept audit)

Reference: DeGroot and Schervish, *Probability and Statistics*, 4th edition (2012). Section numbers as I recall that edition; a reader with the book should confirm them: 7.6 (properties of MLEs, including the method of moments), 7.7 and 7.8 (sufficient and jointly sufficient statistics, factorisation, minimal sufficiency), 7.9 (improving an estimator: Rao-Blackwell), 8.8 (Fisher information and the information inequality), 9.1 (likelihood ratio tests and the large-sample Theorem 9.1.4), 9.2 (simple hypotheses, Neyman-Pearson), 10.1 to 10.3 (goodness of fit, composite hypotheses, contingency tables).

| Statement as taught | Conditions stated in the lesson | Evidence |
|---|---|---|
| Method of moments: match the first $k$ moments to the sample's | population-style moments (divisor $n$); a higher moment when a lower one does not involve the parameter (Laplace) | DeGroot 7.6; Gamma solution derived in l13's `order`; simulations of Gamma(3, rate 0.5) and Laplace in the script |
| Moments agree with the MLE for exponential, Poisson, normal mean; not for the uniform | named per model | score equations by hand; uniform MSEs $\tfrac{1}{3n}$, $\tfrac{2}{(n + 1)(n + 2)}$ checked by a 400,000-run simulation |
| Sufficiency: distribution of the data given $T$ free of $\theta$ | definition | DeGroot 7.7; 120 orders each $\tfrac{1}{120}$ (l14 explore) |
| Factorisation theorem: $f = g(T, \theta)h(x)$ | $h$ free of $\theta$ | DeGroot 7.7 (Fisher-Neyman); Poisson case checked in SymPy and derived in l14's `order` |
| MLE is a function of a sufficient statistic | when both exist (unique MLE) | DeGroot 7.8 |
| Rao-Blackwell | $\hat\theta$ unbiased with finite variance, $T$ sufficient; variance never larger | DeGroot 7.9; Bernoulli 0.24 to 0.024 and the Poisson $(\tfrac45)^{10}$ simulated |
| $E[S] = 0$; $I = \mathrm{Var}(S) = -E[\ell'']$ | support free of $\theta$, differentiation under the integral | DeGroot 8.8; derived in l15 (`order`) and homework `h-two-forms`; SymPy for every $I$; simulated $\mathrm{Var}(S)$ |
| MLE approximately $N(\theta, \tfrac{1}{nI})$ | independent observations, smooth model with fixed support, true value interior, large $n$ | DeGroot 7.6 / 8.8 (asymptotic normality); $\hat\sigma$ and $\hat\sigma^2$ standard errors simulated (20,000 years of 252 days) |
| Information is per parameterisation | chain rule $I(\sigma^2) = I(\sigma)/(2\sigma)^2$ | SymPy; simulated SE of $\hat\sigma^2$ |
| Uniform breaks regularity; error shrinks like $\tfrac1n$ | support moves with $\theta$ | score $-\tfrac1\theta$ by hand; $\mathrm{Var}(\tfrac{n + 1}{n}\max) = \tfrac{1}{120}$ simulated |
| Cramér-Rao: $\mathrm{Var}(\hat\theta) \ge \tfrac{1}{nI(\theta)}$ | unbiased estimator, $n$ independent observations, regular model, $0 < I < \infty$ | DeGroot 8.8 (information inequality); proof in l16's two `order` screens via $\mathrm{Cov}(\hat\theta, S) = 1$ and $\rho^2 \le 1$ |
| Equality iff $\hat\theta$ linear in $S$; efficient estimators are MLEs | regular model | stated in l16 (derive part 2, quiz); Poisson identity $\bar X = \lambda + \tfrac{\lambda}{n}S$ checked on every simulated sample |
| Median efficiency $\tfrac{2}{\pi}$ | large $n$, normal data | asymptotic variance $\tfrac{\pi\sigma^2}{2n}$ (standard result); simulation at $n = 101$ gave ratio 1.59 |
| Neyman-Pearson lemma | two simple hypotheses; among tests of the same size | DeGroot 9.2 (Neyman and Pearson 1933); sizes and powers exact by `math.comb` and SciPy |
| Wilks: $-2\ln\Lambda \approx \chi^2_r$ | independent observations, regular model, null value interior, large $n$; $r$ = parameters the null removes; not for non-nested models or a null on the boundary (then a 50:50 mix of 0 and $\chi^2_1$) | DeGroot Theorem 9.1.4 (Wilks 1938; boundary mix: Self and Liang 1987); size of the two-regime test simulated at 5% |
| $-2\ln\Lambda = z^2$ for a normal mean, $\sigma$ known | exact | derived in l17's `order` |
| Pearson's $X^2 \approx \chi^2$ | null true, independent (multinomial) counts, expected counts not small (rule of thumb at least 5); degrees of freedom cells $- 1$, minus one per estimated parameter, $(r - 1)(c - 1)$ for independence | DeGroot 10.1 to 10.3 (Pearson 1900; Fisher 1922 on degrees of freedom; the 5 rule is Cochran's); every statistic checked against `scipy.stats.chisquare` / `chi2_contingency` |
| Estimated-parameter rule | exact in the limit when the parameter is fitted to the cell counts; with the raw-data mean it is the usual approximation (Chernoff and Lehmann 1954) | said in l18 screen 6's explanation |
| 2 × 2 $X^2$ equals the two-proportion $z^2$; continuity correction 6.017 | pooled-variance $z$ | SciPy both ways |

## Numbers

Every stated number is in `docs/reports/testing-L4-numbers.py`, computed by a closed form and an independent route and found at its path. The planner's list all reproduce: $\hat\lambda = 2$; 0.5 and 3; $\tfrac{1}{30}$, $\tfrac{1}{66}$ (simulation 0.0333, 0.0152); 8 against 9; 155, 80.6, 74.4; 120; 0.24, 0.024; 4.7619, 476.19, 0.0458; 0.0445, 4.45%; 200; 0.6366, 1.5708; 2.2222, 0.5, 0.4; $\tfrac29$, $\tfrac{2}{10}$; $\tfrac{1}{120}$; 2,500 days, 9.9 years; 0.665, 5.049; 0.0207, 0.0577; 0.1256, 0.0016, 0.0467, 0.0156; 3.757, 3.841, 0.0526, 2.0, 0.0455, 1.826, 0.0679; 1.345, 6.806, 0.0091; 2.88, 0.50, 0.08, 1.62, 0.32, 5.4, 9.488, 0.2487, 1.897, 5.311, 0.2568; 6.667, 0.0098, 2.582, 66.67, 6.017; 3.75, 0.1534, 5.991; Rao-Blackwell 0.1074 against 0.1353.

Computed and reported here: score at 0.6 is 4.1667; falls 0.216 and 2.160; SE of $\hat\sigma^2$ 0.0891; median needs 158.7 observations; MSE of the $n + 1$ divisor $\tfrac{2}{11} = 0.1818$; Poisson goodness of fit (200 minutes, mean 1.8): expected 33.06, 59.51, 53.56, 32.13, 21.74, $X^2 = 0.639$ on $5 - 1 - 1 = 3$, p = 0.887; venues 9.38 (p = 0.052) and 9.87 (p = 0.043) on 4; review 2 × 3 table 19.857 on 2; homework LRT of two exponential rates 3.817 (p = 0.0507), binomial $\hat p = -0.25$, efficiency of $n\min$ 0.05, Neyman-Pearson power 0.6387.

Seeds: lesson sims 13 (l13), 21 and 5 (l16); l16 hook values from `numpy.random.default_rng(2016)`; code tests `random.Random(7)`, `(1)`, `(3)`; homework code lists from `random.Random(4)` and `(9)` (written literally into the tests); the number script uses `default_rng(20261111)`.

## Exam support and later work

Supports `s-gap-mle`, `s-power`, `s-beta-posterior`, and makes the planned items answerable: a two-parameter moment estimate (Gamma), the information and its standard error, a likelihood-ratio statistic against a $\chi^2$ cut-off, a 2 × 3 independence test with its degrees of freedom (review `r-chi-23`, l18 quiz).

Fluency candidates: moment estimates for the exponential and Gamma; Fisher-information standard errors (Bernoulli, Poisson, exponential, $\sigma$); $X^2$ from a small table; degrees of freedom. Problem-set candidates: moments then likelihood for the uniform; information, standard error, then a Wald or likelihood-ratio test on the same data.

## course.json

No change needed for this pass. When the topic exam is extended, the brief's skills `ht-theory` (l13 to l16) and `ht-likelihood` (l17, l18) can replace the fallback mapping above.

## Backlog

3 bullets in `docs/BACKLOG-INBOX.md` under "Raised later (testing L4):".
