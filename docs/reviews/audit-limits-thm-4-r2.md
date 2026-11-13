# Concept audit, round 2 (blind): limits-thm level 4

- Course `limits-thm` (Stage 1, topic 1.5), level 4. Full ledger depth.
- Files read, every string: `l14-joint-densities.json`, `l15-new-variables.json`, `l16-adding-densities.json`, `l17-smallest-and-largest.json`, `l18-gamma-beta.json`, `l19-generating-functions.json`, `review-4.json`, `homework-4.json`, `problems-4.json`, at commit `f65b7657`.
- Blind rule kept: the round 1 audit, its ledger and scripts, the author reports, the earlier reviews, the audit log and notes, and the course folder's git history were opened only after the commit "WIP: limits-thm L4 r2 ledger and findings".
- Ledger: `docs/reports/audit-limits-thm-4-r2-ledger.md`, 1,585 rows: correct 1,568, wrong 0, imprecise 17, misleading 0, unverified 0. The 17 imprecise rows are the 13 findings below (findings 1 and 9 cover several paths).
- Script: `docs/reports/limits-thm-L4-concepts-r2.py`, 710 checks, exit 0. It recomputes every graded key, every numeric wrong option and slip from the mistake its feedback names, the figures quoted in prose, a Monte Carlo for each empirical or distributional claim, and every code solution and starter against its hidden tests. No check is named FINDING: this round found nothing false as stated.
- Result: 13 findings, all `imprecise`, all `minor`. No `wrong`, no `misleading`, no `serious`.

CB below is Casella and Berger, *Statistical Inference*, 2nd edition.

## Findings

1. `l14-joint-densities.json` | `screens[7].explain.text`, `summary.ideas[2]` (the same claim recurs in `screens[9].explain.text` and in `problems-4.json` `items[0].parts[2].explain.text`) | imprecise | minor | "A joint density can be independent only if its support is a rectangle" is an "only" claim that is false outside the interval case. | Take $X$ uniform on $[0, 1] \cup [2, 3]$ and $Y$ uniform on $[0, 1]$, independent: the support is two rectangles, not one. The exact condition is a product set, an $x$ range times a $y$ range (CB Lemma 4.2.7 and the remark on cross-product supports). The script simulates this pair. Every example in the course has interval ranges, so nothing graded changes. | Say it exactly once, at first use, and the later "rectangle" lines then read as the interval case. `screens[7].explain.text`: "The product of the marginals is $4x(1 - y)$, not the constant 2. Equivalently, $f(y \mid x)$ changes with $x$. Independence needs a density that factors on a support that is an $x$ range times a $y$ range, a rectangle when both are intervals." `summary.ideas[2]`: "$X$ and $Y$ are independent when $f(x, y) = f_X(x)f_Y(y)$ everywhere, which needs a support that is an $x$ range times a $y$ range."

2. `l15-new-variables.json` | `screens[5].explain.text` | imprecise | minor | "The sample mean at 100,000 draws is within a percent of $\tfrac{1}{\text{rate}}$, as the law of large numbers promises." The law of large numbers gives no rate, so it promises nothing at a fixed sample size. | The size of the error comes from the standard error, $\tfrac{1}{\text{rate}\sqrt{100000}}$, which is 0.32% of the mean; "within a percent" is a 3.2 standard error statement (CB Thm 5.5.2 against Thm 5.5.14). Simulation: 99.8% of such means fall within 1%. | "Each draw is one uniform pushed through $F^{-1}$. At 100,000 draws the standard error of the sample mean is about 0.3% of $\tfrac{1}{\text{rate}}$, so the mean lands within a percent of it. Any CDF you can invert gives a sampler this way."

3. `l15-new-variables.json` | `screens[11].explain.text` | imprecise | minor | "Every Monte Carlo engine starts from uniforms because $F^{-1}(U)$ turns them into any distribution with an invertible CDF." The "every ... because" overstates: three screens earlier the lesson itself made normals by Box and Muller, which is not an inverse CDF. | Engines start from uniforms because generators produce them; inversion is one of several maps (CB 5.6.1 and 5.6.2). | "The draw triggers a default when $U < 1 - e^{-0.1} = 0.0952$, so about 9.5 of 100 names default. Monte Carlo engines start from uniforms, and $F^{-1}(U)$ turns them into any distribution whose CDF can be inverted."

4. `l16-adding-densities.json` | `summary.trap` | imprecise | minor | "Variances of normals add, not standard deviations" drops independence at the one line a learner rereads. | $\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y) + 2\,\mathrm{Cov}(X, Y)$ (CB Thm 4.5.6). The lesson's screens and the quiz say "independent"; the trap line does not. | "The density of a sum is not the product $f_X(t)f_Y(t)$ and not the sum of densities. Variances of independent normals add, not standard deviations."

5. `l17-smallest-and-largest.json` | `screens[2].feedback.byKey.five` | imprecise | minor | "That double counts the years in which two issuers might default" names no event. The question is about one year. | $5 \times 0.0198$ adds the five single chances, so an outcome with two defaults is counted twice (inclusion and exclusion). The slip value 0.0990 is right. | "0.0990 is five times one issuer's chance. That counts a year with two defaults twice."

6. `l17-smallest-and-largest.json` | `screens[4].explain.text` | imprecise | minor | "Five draws almost always put one of them near the top." | $P(\max > 0.9) = 1 - 0.9^5 = 0.41$ and $P(\max > 0.8) = 1 - 0.8^5 = 0.67$. Neither is "almost always". Simulated in the script. | "The slope of $t^5$ at 0.9 is $5 \times 0.9^4 = 3.2805$. The density is highest near 1: the largest of five draws exceeds 0.8 two times in three."

7. `l18-gamma-beta.json` | `quiz[2].widget.options[0].why` | imprecise | minor | "At 5 the $t$ tails are over twice as heavy" is true beyond $\pm 2$ only. | The ratio of two-tail chances is 2.24 beyond 2 and 1.14 beyond 1 (scipy, in the script). | "They agree only when the degrees of freedom are large. At 5 the $t$ puts over twice as much probability beyond $\pm 2$."

8. `l19-generating-functions.json` | `screens[8].widget.lines[4].text` | imprecise | minor | "so $Z_n \to N(0, 1)$, if the MGF exists near 0 and MGF convergence implies convergence of distributions" writes a theorem as if it were an assumption that might fail. | Convergence of MGFs on a neighbourhood of 0 to an MGF does give convergence in distribution (CB Thm 2.3.12). The only real hypothesis is that the MGF exists near 0. | "$e^{t^2/2}$ is the MGF of $N(0, 1)$, so $Z_n \to N(0, 1)$ in distribution, given an MGF that exists near 0: MGFs that converge near 0 force the distributions to converge"

9. `l19-generating-functions.json` | `screens[9].prose`, `summary.ideas[2]` | imprecise | minor | The Chernoff bound $P(S \ge a) \le e^{-ta}M(t)^n$ is stated with $M$ and $n$ undefined. Read as the MGF of $S$, which is how the lesson has used $M$ so far, $M(t)^n$ is false. | Markov on $e^{tS}$ gives $e^{-ta}M_S(t)$, and $M_S = M^n$ only for $n$ independent copies with MGF $M$ (CB Thm 4.2.12; Mitzenmacher and Upfal 4.2). Only the starter's comment says "each trade has MGF cosh(t)". | `screens[9].prose`: "A year has $n = 100$ independent trades, each a £1 gain or loss with equal chance. Their total is $S$, and one trade has MGF $M(t)$. Markov's inequality applied to $e^{tS}$ gives the **Chernoff bound** $P(S \ge a) \le e^{-ta}M(t)^n$ for every $t > 0$. Take the best $t$." `summary.ideas[2]`: "For a sum of $n$ independent copies, each with MGF $M$, Chernoff bounds a tail by $\min_{t > 0} e^{-ta}M(t)^n$. The CLT follows when the standardised sum's MGF tends to $e^{t^2/2}$."

10. `l19-generating-functions.json` | `screens[4].feedback.byKey.add` | imprecise | minor | "Exactly 3 in total can also come as 1 and 2, or 0 and 3" implies the two added chances are themselves ways to total 3. They are not: $P(A = 3)$ ignores B. | The four ways are (3, 0), (2, 1), (1, 2), (0, 3), and their chances sum to 0.2158 (script). The slip value $0.1804 + 0.1255 = 0.3059$ is right. | "You added the two single chances, 0.1804 and 0.1255. A total of 3 needs both counts at once: 3 and 0, 2 and 1, 1 and 2, or 0 and 3."

11. `l19-generating-functions.json` | `quiz[2].explain.text` | imprecise | minor | "Its tails decay like $\tfrac{1}{x^2}$, far slower than $e^{-tx}$ can offset" is garbled: nothing is offset by $e^{-tx}$. | $E[e^{tX}]$ diverges because the factor $e^{tx}$ grows faster than the density $\tfrac{1}{\pi x^2}$ decays, for every $t \ne 0$. | "A Cauchy has no mean either. Its tails decay like $\tfrac{1}{x^2}$, far too slowly to offset the growth of $e^{tx}$."

12. `homework-4.json` | `items[10].model` | imprecise | minor | The model answer uses one-sided tails throughout and never says so, while `l18` `screens[6]` taught the same judgement two-sided. | $P(t_{29} \ge 2.6) = 0.0073$ one-sided; two-sided it is 0.0146, which is already above 1% for a single signal. The conclusion is the same under both; the numbers are not. | In part 1 of the model, replace the second sentence with: "One skill-free $t$-ratio is about $N(0, 1)$ and clears 2.6 with chance $1 - \Phi(2.6) = 0.0047$, a one-sided tail, as throughout."

13. `problems-4.json` | `items[0].parts[0].feedback.byKey.constant` | imprecise | minor | The feedback for the slip "1" does not name the mistake, and speaks of the slice's "length", which is infinite. | The slip is $\int_0^\infty e^{-y}\,dy = 1$: the slice taken from $y = 0$ (sympy, in the script). | "That is $\int_0^\infty e^{-y}\,dy$, the slice taken from $y = 0$. The density is 0 below $y = x$, so start there: $\int_x^\infty e^{-y}\,dy = e^{-x}$."

### Checked with care and found sound

- Hypotheses. Independence is stated where the convolution, the product of MGFs, $F^n$ and $(1 - F)^n$, the race of exponentials and the chi-square sum are introduced. The $t$ definition has $Z$ independent of $V$. The change-of-variable rule has "strictly monotone, differentiable inverse" and the absolute value. Convolution limits are taken from the supports on every screen that integrates.
- Order statistics. $n\binom{n-1}{k-1}x^{k-1}(1 - x)^{n-k}$ integrates to 1 with mean $\tfrac{k}{n+1}$ (sympy, four cases); Beta($k$, $n - k + 1$) agrees; the discrete maximum uses a CDF difference.
- Gamma and Beta. The Gamma is written with a rate $\lambda$ on every screen and the scale $\tfrac1\lambda$ is said once, in `l18` `screens[3]`, with the library warning. Chi-square as Gamma($\tfrac n2$, rate $\tfrac12$) holds for $n = 1$ to 10.
- Generating functions. Uniqueness is always tied to "finite near 0"; the Cauchy and lognormal exceptions are right; the CLT sketch states its MGF hypothesis and names the finite-variance theorem.
- `l15` `screens[4]`: the quoted $\varphi(0.6931) = 0.3138$ is right for the rounded argument (0.313758). $\varphi(\ln 2)$ itself is 0.313748. The key 0.1569 and both slips are inside tolerance. No finding.
- Code. Each of the six solutions passes its hidden tests and each starter fails. A maximum in place of a minimum, Box and Muller without the factor 2, and a sampler that multiplies by the rate are all rejected.

## Gates

- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 4,537 warnings. `app/content/manifest.json` unchanged.
- `node tools/run-number-scripts.mjs --python <venv python> --only limits-thm`: 5 of 367 scripts, 5 passed, 0 new failures, exit 0.
- `node tools/grade-all.mjs --file <path> --local-cdn <pkgs>` on each of the nine files: 116 widgets checked in all (14, 12, 13, 14, 14, 12, 9, 8, 20), 0 failures in every file.
- `docs/reports/limits-thm-L4-concepts-r2.py`: 710 checks, 0 failed, exit 0.
- No content was changed, so no playthrough was run.

## Overlap with earlier reads

Pending: filled after the WIP commit, when the round 1 audit and the earlier reviews are opened.

## Inbox

Pending.
