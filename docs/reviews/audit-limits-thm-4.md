# Concept audit: limits-thm level 4 (blind, round 1)

Auditor: Fable, blind to earlier reads until the ledger and findings were committed (commit "WIP: limits-thm L4 ledger and findings").

Scope: `l14-joint-densities`, `l15-new-variables`, `l16-adding-densities`, `l17-smallest-and-largest`, `l18-gamma-beta`, `l19-generating-functions`, `review-4`, `homework-4`, `problems-4`. No `fluency-*.json` in the course belongs to l14 to l19.

Ledger: `docs/reports/audit-limits-thm-4-ledger.md`, 328 hand-judged rows: 297 correct, 10 wrong, 19 imprecise, 2 misleading, 0 unverified.

Script: `docs/reports/limits-thm-L4-concepts.py`, 563 checks. It recomputes every graded key, every numeric `wrong[]` value and slip (553 checks pass), runs all seven code solutions against their hidden tests, and exits 1 because ten checks named `FINDING 1` to `FINDING 10` fail on purpose. Each of those ten is one of the `wrong` findings below. They pass once the fix text is applied.

No graded key is wrong. No numeric slip value is wrong. All ten `wrong` findings are in explanations or feedback lines. Three would leave a learner with a false rule or a false reading of a statistic.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

### Wrong

1. `l14-joint-densities.json` | `screens[10].explain.text` (and `summary.trap`) | wrong, minor | The explain says the rule "uncorrelated means independent" "fails for $Y = X^2$ and for any other pair that is not jointly normal". That is false as a universal. | Two independent exponentials are not jointly normal, are uncorrelated and are independent. The same screen marks that pair independent. Any two two-valued variables are another case. Script: `l14 s10 counterexample exists`. Basis: Casella and Berger section 4.5. | Explain: "A normal pair with $\rho = 0$ factors into two normal densities. So uncorrelated means independent for jointly normal variables, as the eigen course shows in matrix form. For other pairs it can fail, as $Y = X^2$ shows." Summary trap: "A constant density on a triangle is not independence. Zero covariance does not prove independence either, though it does for jointly normal pairs."

2. `l15-new-variables.json` | `screens[10].explain.text` (and `screens[3].prose`, `summary.ideas[0]`) | wrong, minor | "A non-constant monotone $g$ keeps a density." The screen's own payoff $g(s) = \max(s - 105, 0)$ is non-constant and monotone, and it has an atom of 0.6915. The next sentence contradicts the first. | The change-of-variables formula needs $g$ strictly monotone (Casella and Berger Theorem 2.1.5). Script: `l15 s10 MC atom at 0`. | Explain: "A strictly increasing or strictly decreasing $g$ keeps a density. A $g$ that is constant on an interval collapses that interval's probability onto a single value, here 0.6915 at 0. The payoff has an **atom** at 0 and a density above it." In `screens[3].prose` replace "with $g$ monotone" by "with $g$ strictly increasing or strictly decreasing". In `summary.ideas[0]` replace "For monotone $g$" by "For strictly monotone $g$".

3. `l19-generating-functions.json` | `screens[6].explain.text` | wrong, serious | "The product rule needs independence. For dependent variables $E[e^{tX}e^{tY}]$ does not split." This states independence as necessary. It is only sufficient. A learner leaves with "the MGF of a sum is the product exactly when the variables are independent". | The script builds a dependent pair on $\{1, 2, 3\}^2$ (uniform table plus a perturbation with zero row, column and anti-diagonal sums). Its sum has the convolution distribution, so $M_{X+Y}(t) = M_X(t)M_Y(t)$ for every $t$. Basis: Casella and Berger Theorem 4.2.12 gives one direction only; Stoyanov, *Counterexamples in Probability*, section on sums of dependent variables. The lesson's other statements (`screens[3].prose`, `summary.ideas[1]`, `summary.trap`) give the sufficient direction and are correct. | "$M_{X+Y}(t) = M_X(t)M_Y(t) = 0.25 + 0.5e^t + 0.25e^{2t}$: chances 0.25, 0.5, 0.25 on 0, 1, 2 heads. Independence guarantees the product rule. For dependent variables $E[e^{tX}e^{tY}]$ need not split, so check independence first."

4. `review-4.json` | `items[4].explain.text` (`r-best10`) | wrong, serious | "One in five fund pitches this good is luck." This reads $P(\text{best} \ge 2 \mid \text{no skill}) = 0.2056$ as $P(\text{luck} \mid \text{a pitch this good})$. That is the transposed conditional. | In the item's own model every team is skill-free, so every such pitch is luck. The share of good pitches that are luck in practice depends on how many teams have skill, which the item does not give. Basis: Bayes' rule; the same error as reading a p-value as the chance the null is true. | "$\Phi(2)^{10} = 0.7944$ is the chance that none reaches 2, so the best does with chance 0.2056. One skill-free team in five can show a best $t$ of 2 or more."

5. `l15-new-variables.json` | `screens[3].widget.options[3].why` and `screens[3].feedback.byKey.inv` | wrong, minor | The option is $\tfrac12 e^{-2y}$. The feedback says "You used $\tfrac{dy}{dx}$ upside down." Using $\left|\tfrac{dy}{dx}\right|$ gives $\tfrac12 e^{2y}$, not the option. The feedback names a slip that does not produce the value. | $x = e^{-2y}$, so $\left|\tfrac{dx}{dy}\right| = 2e^{-2y}$ and its reciprocal is $\tfrac12 e^{2y}$. The option divides by the 2 where it should multiply. Script: `FINDING 5`. | `why`: "You divided by the 2 from the exponent where you should multiply. Differentiating $x = e^{-2y}$ gives $\left|\tfrac{dx}{dy}\right| = 2e^{-2y}$." `byKey.inv`: "The 2 from the exponent multiplies: $\left|\tfrac{dx}{dy}\right| = 2e^{-2y}$."

6. `l16-adding-densities.json` | `screens[1].prose` | wrong, minor | "Flip $Y$'s density, slide it so it is centred on $t$". The flipped copy $f_Y(t - x)$ covers $[t - 1, t]$. Its centre is $t - \tfrac12$. | The canvas on the same screen draws the copy on `[t - 1, t]`, and the hint says it "covers $[0.5, 1.5]$" at $t = 1.5$. | "Fix $t$ and ask how many ways the two fills can add to $t$. Flip $Y$'s density and slide it so that it covers $[t - 1, t]$. Then measure the overlap with $X$'s density, and slide $t$."

7. `l16-adding-densities.json` | `screens[7].widget.options[0].why` and `screens[7].feedback.byKey.prod` | wrong, minor | "That only counts the case where both fills are at 0.5, and ignores every other way to add to 0.5." Both fills at 0.5 add to 1. That pair is not a way to add to 0.5 at all. | $f_X(0.5)f_Y(0.5)$ is the joint density at the point $(0.5, 0.5)$, which lies on the line $x + y = 1$. The explain on the same screen has it right. | `why`: "You multiplied the heights at one point. That is the joint density of both fills at 0.5, a pair that adds to 1, not 0.5." `byKey.prod`: "You multiplied the heights at one point. The density at 0.5 adds up every split $x$ and $0.5 - x$."

8. `l17-smallest-and-largest.json` | `screens[10].feedback.byKey.cdf` | wrong, minor | "0.25 is $P(\max \le 3)$ ... That includes totals of 1 and 2 as well." The quantity is the larger die, not a total. Two dice cannot total 1. | Slip-names-the-wrong-quantity class. | "0.25 is $P(\max \le 3) = \left(\tfrac12\right)^2$. That includes a maximum of 1 or 2 as well."

9. `problems-4.json` | `items[2].parts[4].explain.text` (`p-dealer-quotes`, part 5) | wrong, serious | "$X_{(3)} > 0.5$ exactly when at most 1 of the 4 quotes is below 0.5." The right event is at most 2 below, which is at least 2 above. The explain then calls $\tfrac{1 + 4}{16}$ the failing share, which contradicts its own first sentence. The answer $\tfrac{11}{16}$ is right only because the threshold is 0.5 and the counts are symmetric. | The third smallest of four exceeds $c$ when fewer than three quotes are at or below $c$. Script: at $c = 0.6$ the simulated chance matches "at most 2 below" and misses "at most 1 below" by more than 0.2. The `feedback.correct` line on the same part states the event correctly. Basis: Casella and Berger section 5.4 (the order statistic CDF as a binomial sum). | "$X_{(3)} > 0.5$ exactly when at least 2 of the 4 quotes are above 0.5. Each is above with chance $\tfrac12$, so it fails with 0 or 1 above, $\tfrac{1 + 4}{16}$ of the time, and $P = \tfrac{11}{16} = 0.6875$. The Beta(3, 2) integral $\int_{0.5}^1 12x^2(1 - x)\,dx$ gives the same."

10. `problems-4.json` | `items[3].parts[0].feedback.byKey.power` (`p-part-errors`, part 1) | wrong, minor | The slip is $(1 - 2s)^{-1/8}$. The feedback says "You multiplied the exponent by $\tfrac12$ again." That gives $-\tfrac14$. | $-\tfrac18 = -\tfrac12 \div 4$: the learner took a fourth root where a fourth power is needed. | "You divided the exponent by 4. Four copies multiply it by 4: $-\tfrac12 \times 4 = -2$."

### Imprecise and misleading

11. `l18-gamma-beta.json` | `screens[5].prose`, `summary.ideas[1]` | imprecise, minor | "$t = \dfrac{Z}{\sqrt{V/n}}$ has the $t$ distribution" with no word that $Z$ and $V$ must be independent. The summary also drops "independent" from the chi-square sum. | Casella and Berger Definition 5.3.4. Script: with $V = Z^2$ the ratio is $\pm 1$. The independence of the sample mean and sample variance is the reason a $t$-ratio is $t$-distributed, and it is a standard interview question. | In `screens[5].prose` replace the second sentence by: "With $V$ chi-square on $n$ degrees of freedom and independent of $Z$, $t = \dfrac{Z}{\sqrt{V/n}}$ has the **$t$ distribution**, with heavier tails than the normal." `summary.ideas[1]`: "A sum of $n$ independent squared standard normals is chi-square (Gamma with $a = \tfrac n2$, $\lambda = \tfrac12$). With $Z$ independent of $V$, $\tfrac{Z}{\sqrt{V/n}}$ has the $t$ distribution, with heavier tails than the normal."

12. `l16-adding-densities.json` | `screens[8].prose`, `screens[10].prose` | imprecise, minor | Both keys need independence that the item does not state: the two strategies in screen 8 (key 0.1587) and the two desks in screen 10 (key 0.1590). Two desks or two strategies at one firm are usually correlated. | Variances add only for uncorrelated variables. The averaging in screen 10 uses $P(L > 2 + a)$ free of $a$. | Screen 8: replace "Two strategies' daily P&L, in £k, are" by "Two independent strategies have daily P&L, in £k, of". Screen 10: replace "Desk B only loses: its loss $L$ has density $e^{-l}$, mean £1k." by "Desk B only loses, independently of desk A. Its loss $L$ has density $e^{-l}$, mean £1k."

13. `l17-smallest-and-largest.json` | `screens[10].prose`, `summary.formula.note`, `summary.ideas[0]` | imprecise, minor | "For continuous variables a tie has probability 0" needs independent draws. $X$ and $Y = X$ are both continuous and always tie. The summary states $F(t)^n$ and $(1 - F(t))^n$ with no mention of independent draws. | The lesson body states independence each time; only these three lines drop it. | `screens[10].prose`: "For independent continuous draws a tie has probability 0, so one draw alone is the largest. For whole-number variables a tie is possible. The grid shows the larger of two dice." `summary.formula.note`: "For independent continuous draws ties have chance 0. For discrete ones subtract two CDF values." `summary.ideas[0]`: "An event about the minimum or maximum is an event about every draw. For $n$ independent draws with CDF $F$: $P(\max \le t) = F(t)^n$ and $P(\min > t) = (1 - F(t))^n$."

14. `l19-generating-functions.json` | `summary.ideas[2]`, `summary.formula.tex` | imprecise, minor | "$\min_t e^{-ta}M(t)^n$" with no restriction to $t > 0$. Over all real $t$ it is not a bound. | Markov's step needs $t > 0$. Script: for 100 fair $\pm 1$ trades and $a = -30$ the unrestricted minimum is 0.0104 while $P(S \ge -30) = 0.998$. Screen 9 states "for every $t > 0$" correctly. | In both places write `\min_{t > 0}` for `\min_t`.

15. `l18-gamma-beta.json` | `screens[8].explain.text` | imprecise, minor | "This **arcsine** law describes ... the share of time a fair random walk spends positive." It is the limit law for a long walk. | Feller, *An Introduction to Probability Theory*, volume 1, chapter III section 4. | "A third of the probability lies in the first quarter of the interval, and a third in the last quarter. This **arcsine** law describes, for example, the share of time a long fair random walk spends positive."

16. `l18-gamma-beta.json` | `screens[0].prose` | imprecise, minor | "Trades arrive at 2 a minute, so each gap is exponential". A rate alone does not give exponential gaps. Poisson arrivals do. | The lesson's own quiz item states "as a Poisson process". | First sentence: "Trades arrive as a Poisson process at 2 a minute, so each gap is exponential with mean half a minute."

17. `l18-gamma-beta.json` | `screens[4].question` | imprecise, minor | "Six independent standardised returns are squared and added." The key 12 needs each to be standard normal. A standardised return with fat tails has $\mathrm{Var}(Z^2)$ above 2. | $\mathrm{Var}(Z^2) = E[Z^4] - 1$, which is 2 only when the kurtosis is 3. | "Six independent standard normal returns are squared and added. What is $\mathrm{Var}(V)$?"

18. `l19-generating-functions.json` | `screens[8].prose` | imprecise, minor | "Let $X_i$ be independent with mean $\mu$ and sd $\sigma$". The first proof line uses identical distribution as well. | Casella and Berger Theorem 5.5.14 is stated for iid variables. | Replace "be independent with" by "be independent and identically distributed with".

19. `homework-4.json` | `items[6].explain.text` (`h-order-code`) | imprecise, minor | "within about 0.001 of $\tfrac{k}{n+1}$, since the sd of the mean is $\tfrac{0.18}{\sqrt{20000}}$". The 0.18 is the sd for $n = 5$, $k = 2$ only. The other tested cases have sds from 0.08 to 0.29. | $\mathrm{sd} = \sqrt{k(n - k + 1)/((n + 1)^2(n + 2))}$; script. | "Sorting puts the $k$th smallest at index $k - 1$. For $n = 5$, $k = 2$ the mean of 20,000 trials is within about 0.001 of $\tfrac13$, since the sd of the mean is $\tfrac{0.18}{\sqrt{20000}}$."

20. Rounded products that do not reproduce (four lines) | imprecise, minor | A learner who multiplies the digits shown gets a different last digit. | (a) `l15-new-variables.json` `screens[11].feedback.correct`: $100 \times 0.0952 = 9.52$, not 9.516. (b) `l17-smallest-and-largest.json` `screens[8].feedback.byKey.five`: $5 \times 0.1813 = 0.9065$, not 0.9063. (c) same file `screens[11].feedback.byKey.times`: $20 \times 0.0179 = 0.358$, not 0.3573. (d) same file `screens[11].widget.accept`, `hints[2].text`, `feedback.correct`: $1 - 0.9821^{20} = 0.3032$, not 0.3027. All keys and slip values are right. | (a) "$100 \times 0.09516 = 9.516$ defaults on average." (b) "0.9063 is $5 \times 0.18127$. Adding overcounts the cases where several issuers default." (c) "0.3573 is $20 \times 0.01786$. It overcounts the cases where two or more strategies clear 2.1." (d) write $0.98214^{20}$ for $0.9821^{20}$ in all three lines, and $\Phi(2.1) = 0.98214$ in `hints[1].text`.

21. `l15-new-variables.json` | `screens[1].question` | misleading, minor | "The bars centre near 0.5." For this skewed shape 0.5 is the mean. The median is 0.35, shown on the previous screen, and the mode is 0. | Exponential with rate 2. | "The bars average about 0.5. Which rate $\lambda$ makes an exponential have mean 0.5?"

22. `l14-joint-densities.json` | `screens[1].explain.text` | misleading, minor | "It agrees with the rule $\tfrac{1}{1+2}$ for the faster clock to lose." In a race to default, "lose" can be read as "default first", which for the faster clock B has chance $\tfrac23$. | $P(A \text{ first}) = \lambda_A/(\lambda_A + \lambda_B)$. | Last sentence: "It agrees with the rule $\tfrac{\lambda_A}{\lambda_A + \lambda_B} = \tfrac{1}{1+2}$ for the chance that A is first."

### Counts

| severity | serious | minor | total |
|---|---|---|---|
| wrong | 3 (findings 3, 4, 9) | 7 (1, 2, 5, 6, 7, 8, 10) | 10 |
| imprecise | 0 | 10 (11 to 20) | 10 |
| misleading | 0 | 2 (21, 22) | 2 |
| total | 3 | 19 | 22 |

The ledger has 19 imprecise rows because findings 2, 11, 13 and 20 each cover several rows.

### Checked and found sound (the watch list)

- Supports and limits: every marginal and convolution integrates over the right slice (triangle, wedge, overlap of supports). All recomputed exactly.
- Marginal against conditional: kept apart in l14, homework and problems.
- Independence as factorisation on a product support: taught correctly, with the triangle and the wedge as counterexamples.
- Jacobian: absolute value is used throughout, two branches for $Z^2$, an atom for the call payoff.
- Order statistics: formulas are right and the lesson body states independent draws with a common CDF.
- Gamma: shape and rate throughout, scale named once as the library convention. No drift.
- Different-rate exponentials: `problems-4` gets $e^{-t/2} - e^{-t}$ and offers the equal-rate Gamma as a slip.
- Gamma function at non-integers, Beta and order statistics, Beta and the Gamma ratio (homework Jacobian item): right.
- MGF existence: Cauchy, lognormal for $t > 0$, uniqueness "when finite near 0": right. The CLT sketch names its own gaps.
- No "memoryless" claim appears in scope.
- Code: all seven solutions pass their hidden tests, and each teaches the stated method.
- Real-world facts: none needed an `unverified` verdict.

## Gates

| gate | result |
|---|---|
| `node tools/validate.mjs` | 0 errors, 5022 warnings (manifest restored afterwards) |
| `docs/reports/problems-limits-thm-numbers.py` | exit 0, 1539 checks, 0 failures |
| `docs/reports/fluency-limits-thm-numbers.py` | exit 0, 3537 checks, 0 failures |
| `docs/reports/limits-thm-L4-concepts.py` | exit 1, 563 checks, 10 failed, all ten are the `FINDING` checks above |
| playthrough, desktop, `--local-cdn` | l14 to l19, `review-4`, `homework-4`, `problems-4`: all passed |
| playthrough, `--mobile`, `--local-cdn` | the same nine files: all passed |

## Overlap with earlier reads

Read after the WIP commit `2cc7bcce`.

**Is a second read of level 4's lessons, review and homework on record? No.** `docs/reviews/review-1.5.md` is the second read of topic 1.5 and its scope line names `limits-thm`, but it is dated 21 October and the level was first committed on 27 October (`39d6582d`). Its limits-thm findings stop at l12 and `homework-3`. `docs/reports/stage-status-2026-11-03.md` lists the level as "Finalised" on the strength of that review. No `answers-*.md`, `recheck-*.md` or `review-perf-retrofit-*.md` file covers l14 to l19, `review-4` or `homework-4`.

Earlier reads that touch the level in part:

| earlier read | what it covered | conceptual findings in scope |
|---|---|---|
| `docs/reviews/review-problems-1.5-d.md` (section A) | full second read of `problems-4` | finding 5 (`p-part-errors` part 3: "An MGF pins down its distribution" lacked "finite near 0"), finding 7 (`p-ticket-stages` part 3: `rates` feedback did not name the slip). Findings 6 (coverage of l15) and 8 (grader sampling range) are not conceptual. It lists `p-dealer-quotes` as clean. |
| `docs/reviews/review-precision-3.2.md` rows 46 and 47 | summary fields only (`summary.ideas`, `summary.trap`, `summary.formula.note`) with an "only / never / any" word | row 47: l19 `summary.trap` said "$M_{X+Y}$ is a product, and only for independent variables", marked False and fixed. Row 46 (l14 formula note) holds. |
| `docs/reviews/triage-bands-ab.md` line 263 | tolerance band of l17 `screens[8]` slip `maxcdf` | none (harmless band note) |
| `docs/reviews/review-delta-session-aa.md` item 11 | formatting of `problems-4` after its fix pass | none |
| `docs/reports/limits-thm-4.md` (author report) | every stated number by two routes | none; it is a number check and agrees with my script on every figure |

All three earlier conceptual findings were fixed before this audit, and I judged the fixed lines correct.

| conceptual findings | count |
|---|---|
| found by this audit only | 22 |
| found by earlier reads only | 3 (all fixed before this audit: `review-problems-1.5-d` 5 and 7, `review-precision-3.2` row 47) |
| found by both | 0 |

One pair is the same class at different paths: my finding 3 (l19 `screens[6].explain`, independence stated as necessary) and precision row 47 (l19 `summary.trap`). The precision scan read summary fields only, so the explanation on the trap screen kept the error after the summary was fixed.

Each `wrong` finding against the earlier reads:

| finding | found by an earlier read? |
|---|---|
| 1 (l14 `screens[10]` "any other pair") | no; file never second-read |
| 2 (l15 `screens[10]` "non-constant monotone") | no; file never second-read |
| 3 (l19 `screens[6]` product rule "needs independence") | no at this path; the same class was found and fixed in `summary.trap` by `review-precision-3.2` row 47 |
| 4 (`review-4` `r-best10` transposed conditional) | no; file never second-read |
| 5 (l15 `screens[3]` `inv` feedback) | no |
| 6 (l16 `screens[1]` "centred on $t$") | no |
| 7 (l16 `screens[7]` `prod` feedback) | no |
| 8 (l17 `screens[10]` "totals") | no |
| 9 (`problems-4` `p-dealer-quotes` part 5 explain) | no; `review-problems-1.5-d` read this part and listed the problem as clean |
| 10 (`problems-4` `p-part-errors` part 1 `power` feedback) | no; `review-problems-1.5-d` finding 8 looked at slips `one` and `added` of the same part, not `power` |

So 10 of 10 `wrong` findings, including all 3 serious ones, were found by no earlier read. Two of them (9 and 10) sit in the one file that did have a full second read.

## Inbox

- Validator or number-script rule: where a feedback line says "`V` is `a × b`" (or `a^n`) with literal numbers, recompute the product from the digits shown and warn when it does not round to `V`. Four cases in this level (finding 20). The slip-names-the-wrong-quantity class also appears four more times here (findings 5, 7, 8, 10).
- Validator warning list for universal wording in explanations: "any other", "does not split", "exactly when", "always", "never", "needs independence". Print them for the second reader. Findings 1, 2, 3 and 9 would each have been listed.

## Fix pass

Fixer: Opus. Each fix rests on the basis given here, checked separately from the auditor's. Every proposed sentence was read as a claim before use. No graded key, `wrong[]` value, slip value or hidden test changed. No script assertion changed: the ten `FINDING` checks test for the old wording only, and they pass on the new text.

| # | status | final text where it differs from the audit | basis |
|---|---|---|---|
| 1 | fixed with different text | Explain as proposed. Trap: "Zero covariance does not prove independence either, though for jointly normal pairs it does." (word order only) | Casella and Berger 4.5: zero covariance is necessary for independence, and sufficient only under joint normality (bivariate normal density factors at $\rho = 0$). |
| 2 | fixed with different text | Explain: "A strictly increasing or strictly decreasing $g$ with $g' \ne 0$ keeps a density." `screens[3].prose`: "with $g$ strictly increasing or strictly decreasing and $x = g^{-1}(y)$ differentiable". `summary.ideas[0]`: "For strictly monotone $g$ with a differentiable inverse it gives". | The audit's "strictly monotone keeps a density" is itself false: take $g = F^{-1}$ for a strictly increasing singular CDF $F$ and $X$ uniform; then $g(X)$ has CDF $F$ and no density. Also a $C^1$ strictly increasing $g$ with $g' = 0$ on a fat Cantor set $Z$ maps $Z$ to a null set holding $P(X \in Z) > 0$. Casella and Berger Thm 2.1.5 assumes a differentiable inverse, so the condition is added. |
| 3 | fixed with different text | "Independence is enough for the product rule. Without it $E[e^{tX}e^{tY}]$ can fail to split, so check independence first." | Derivation: adding to the uniform $3 \times 3$ table a perturbation with zero row, column and anti-diagonal sums keeps both marginals and the law of $X + Y$, so the product holds for a dependent pair. Independence is sufficient (C and B Thm 4.2.12), not necessary. |
| 4 | fixed with different text | "So a search over ten skill-free strategies turns up a best of 2 or more about one time in five. That is not the chance that a reported best of 2 is luck, which also depends on how common skill is." | Bayes: $P(\text{luck} \mid \text{best} \ge 2)$ needs a prior share of skilled strategies; 0.2056 is $P(\text{best} \ge 2 \mid \text{no skill})$. The audit's "one skill-free team in five" introduced teams the item does not mention. |
| 5 | fixed | | $x = e^{-2y}$: $\lvert dx/dy\rvert = 2e^{-2y}$, $\lvert dy/dx\rvert = \tfrac12 e^{2y}$; the option $\tfrac12 e^{-2y}$ is $e^{-2y} \div 2$. |
| 6 | fixed | | $f_Y(t - x) > 0$ iff $x \in [t - 1, t]$ for $Y \sim U(0, 1)$. |
| 7 | fixed, plus sibling | Sibling `screens[7].feedback.generic`: "Not quite right. Count every split of 0.5 into $x$ and $0.5 - x$." (old "not just $x = 0.5$" also misnamed the product as a split) | $f_X(0.5)f_Y(0.5)$ is the joint density at $(0.5, 0.5)$, on $x + y = 1$; the split $x = 0.5$ is $(0.5, 0)$. |
| 8 | fixed | | $P(\max \le 3) = (3/6)^2 = 9/36$, the cells with maximum 1, 2 or 3. |
| 9 | fixed | | $X_{(3)} > c$ iff at most 2 of 4 are $\le c$ iff at least 2 are $> c$. Enumeration of the 16 above/below patterns at $c = 0.6$ gives 0.5248, equal to the Beta(3, 2) tail; a simulation of 400,000 sorted quadruples gives 0.5246. |
| 10 | fixed with different text | "You divided the exponent by 4. Multiplying four copies multiplies the exponent by 4: $-\tfrac12 \times 4 = -2$." | $-\tfrac12 \div 4 = -\tfrac18$; $\left((1 - 2s)^{-1/2}\right)^4 = (1 - 2s)^{-2}$. |
| 11 | fixed | | Casella and Berger Def 5.3.4 (Student's $t$ needs $Z$ and $V$ independent). |
| 12 | fixed | | Convolution and "variances add" both use independence (or zero correlation for the variance). |
| 13 | fixed with different text | `screens[10].prose`: "For independent continuous draws a tie has probability 0, so the maximum comes from one draw alone." Formula note and `ideas[0]` as proposed. | $P(X = Y) = \int P(Y = x)\,dF_X(x) = 0$ for independent atomless draws; $F(t)^n$ is the product rule for independent draws. |
| 14 | fixed | | Markov's step $P(S \ge a) \le e^{-ta}E[e^{tS}]$ holds only for $t > 0$. |
| 15 | fixed | | Feller vol. 1, III.4: the arcsine law is the limit as the walk's length grows. |
| 16 | fixed | | Exponential gaps characterise a Poisson process; a rate alone does not fix the gap law. |
| 17 | fixed | | $\mathrm{Var}(Z^2) = E[Z^4] - 1 = 2$ needs kurtosis 3. |
| 18 | fixed | | The sketch uses $M_{Z_n}(t) = M_Y(t/\sqrt n)^n$, which needs identical distributions. |
| 19 | fixed with different text | "The mean of 20,000 trials has sd $\tfrac{\sigma}{\sqrt{20000}}$, with $\sigma$ the sd of one $k$th smallest. For $n = 5$, $k = 2$ that is $\tfrac{0.18}{\sqrt{20000}} \approx 0.0013$, so the mean usually lands within 0.003 of $\tfrac13$." | Beta(2, 4) variance $8/252$, sd 0.178; $0.178/141.4 = 0.00126$. "Within about 0.001" was under one sd; 0.003 is 2.4 sd. |
| 20 | fixed with different text, plus siblings | (a) as proposed. (b) "0.9063 is $5 \times 0.181269$." (c) "0.3573 is $20 \times 0.017864$." (d) $0.982136^{20}$ in `accept`, `hints[1]` ($\Phi(2.1) = 0.982136$), `hints[2]` and `feedback.correct`. | The audit's digits fail its own rule: $20 \times 0.01786 = 0.3572$ and $1 - 0.98214^{20} = 0.3026$; $5 \times 0.18127 = 0.90635$ sits on a rounding tie. Now $5 \times 0.181269 = 0.906345$, $20 \times 0.017864 = 0.35728$, $1 - 0.982136^{20} = 0.30268$. |
| 21 | fixed | | Exp(rate 2): mean 0.5, median $\ln 2 / 2 = 0.347$, mode 0. |
| 22 | fixed with different text | "It agrees with the rule $\tfrac{\lambda_A}{\lambda_A + \lambda_B} = \tfrac{1}{1+2}$ for the chance that A, the clock with rate 1, is first." | $f = e^{-x}\cdot 2e^{-2y}$, so A has rate 1; $\int_0^\infty e^{-x}e^{-2x}dx = \tfrac13$. |

Sibling fixes (same class, not named in the audit):
- `review-4` `r-best10`: `accept` and `feedback.correct` showed $1 - 0.9772^{10} = 0.2056$, but $1 - 0.9772^{10} = 0.2060$; now $0.97725^{10}$ ($1 - 0.97725^{10} = 0.20557$). `byKey.times` showed $10 \times 0.0228$ for 0.2275; now $10 \times 0.02275$.
- `l17` `screens[8]`: `accept` showed $1 - (1 - 0.1813)^5 = 0.6321$, but the shown digits give 0.6322; `accept` and `hints[1]` now use $(e^{-0.2})^5 = e^{-1}$.
- `l16` `screens[7].feedback.generic` (finding 7 row).

Gates: concepts script exit 0 (563 checks, 0 failed); `problems-limits-thm-numbers.py`, `fluency-limits-thm-numbers.py`, `limits-thm-L1-3-concepts-r2.py` exit 0; validator 0 errors (manifest unchanged); voice scan 35: 0 and 0; playthrough desktop and `--mobile` with `--local-cdn` of l14 to l19, `review-4`, `homework-4`, `problems-4`: all passed.

## Fix-pass read

Commit read: `309e891c` (limits-thm L4 audit round 1: fix pass), course folder only, 44 changed strings in nine files. Read blind: the audit, its ledger, the concepts script and the earlier reviews were not opened. Each string was read in its screen or item as it now stands (prompt, key, `accept`, tolerances, slips, canvas data, neighbouring sentences, summary). Checks: `docs/reports/limits-thm-L4-fixread.py` (659 checks; sympy, enumeration and Monte Carlo; exit 1 because of finding 1, exit 0 once it is fixed).

No change touched a graded number: every edit inside an `accept`, hint or feedback field changed displayed digits or words only. Keys 0.6321, 0.3027, 0.2056, 0.6875 and 1/3 were recomputed and sit inside their tolerances; no slip overlaps a key.

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | homework-4 | items[6].explain.text | Mean of 20,000 trials has sd σ/√20000; for n=5, k=2 that is 0.18/√20000 ≈ 0.0013, so the mean usually lands within 0.003 of 1/3 | correct | X(2) of 5 is Beta(2,4), sd 0.1782; 0.18/141.42 = 0.00127; 0.003 is 2.4 sd, 400 simulated means: over 95% inside; hidden tol 0.01 is above 4 sd for all four tests. Casella and Berger 5.4 |
| 2 | l14 | screens[1].explain.text | Rule λ_A/(λ_A+λ_B) = 1/(1+2) is the chance that A, the rate-1 clock, is first | correct | sympy double integral of 2e^{-x-2y} over y > x is 1/3; general rate integral gives λ_A/(λ_A+λ_B); marginal of x is e^{-x}; polygon is y ≥ x. Ross, Introduction to Probability Models 5.2.3 |
| 3 | l14 | screens[10].explain.text | Uncorrelated means independent for jointly normal pairs; for other pairs it can fail, as Y = X² shows | correct | Cov(X, X²) = 0 for X uniform on [-1, 1]; "can fail" is right since the exponential pair of the same item is non-normal, uncorrelated and independent. Blitzstein and Hwang 7.3, 7.5 |
| 4 | l14 | summary.trap | Zero covariance does not prove independence, though for jointly normal pairs it does | correct | As row 3; Casella and Berger 4.5 |
| 5 | l15 | screens[1].question | The bars average about 0.5 | correct | Y = −½ ln U is Exp(2), mean 0.5; simulated mean 0.500 |
| 6 | l15 | screens[3].prose | For g strictly increasing or strictly decreasing with differentiable inverse, the chain rule on F_Y(y) = F_X(x) gives f_Y = f_X·\|dx/dy\| | imprecise | Formula and hypotheses are right (Casella and Berger Thm 2.1.5). The identity F_Y(y) = F_X(x) holds only for increasing g; for decreasing g it is 1 − F_X(x). The screen's own map is decreasing: F_Y(0.3) = 0.4512, F_U(e^{-0.6}) = 0.5488. Finding 1 |
| 7 | l15 | screens[3].widget.options[3].why | ½e^{-2y}: divided by the 2 where it should multiply; \|dx/dy\| = 2e^{-2y} | correct | d/dy e^{-2y} = −2e^{-2y}; the option is the key with 2 replaced by ½ |
| 8 | l15 | screens[3].feedback.byKey.inv | The 2 from the exponent multiplies | correct | As row 7; agrees with the hint and the key |
| 9 | l15 | screens[10].explain.text | A strictly increasing or decreasing g with g′ ≠ 0 keeps a density; a flat stretch leaves an atom, 0.6915 at 0 | correct | Inverse function theorem gives a differentiable inverse; Φ(0.5) = 0.6915. Casella and Berger 2.1 |
| 10 | l15 | screens[11].feedback.correct | 100 × 0.09516 = 9.516 | correct | 1 − e^{-0.1} = 0.095163; product 9.516 exactly as shown; key unchanged |
| 11 | l15 | summary.ideas[0] | For strictly monotone g with a differentiable inverse the CDF method gives f_X(x)\|dx/dy\| | correct | Casella and Berger Thm 2.1.5; agrees with row 9 |
| 12 | l16 | screens[1].prose | Flip Y's density and slide it to cover [t − 1, t] | correct | f_Y(t − x) with Y uniform on [0, 1] is non-zero for t − 1 ≤ x ≤ t; canvas domain is ["t - 1", "t"] |
| 13 | l16 | screens[7].widget.options[0].why | f_X(0.5)f_Y(0.5) is the joint density of both fills at 0.5, a pair that adds to 1 | correct | Independent fills: joint density is the product; 0.5 + 0.5 = 1 |
| 14 | l16 | screens[7].feedback.generic | Count every split of 0.5 into x and 0.5 − x | correct | Convolution integral over 0 ≤ x ≤ 0.5 gives 0.5; simulated density 0.50. Blitzstein and Hwang 8.2 |
| 15 | l16 | screens[7].feedback.byKey.prod | The density at 0.5 adds up every split | correct | As row 14 |
| 16 | l16 | screens[8].prose | Two independent strategies, X ~ N(2, 3²), Y ~ N(1, 4²) | correct | Independence now stated where the key N(3, 5²) needs it; 9 + 16 = 25 |
| 17 | l16 | screens[10].prose | Desk B loses independently of desk A | correct | The convolution of A and −L needs independence; now stated |
| 18 | l17 | screens[8].widget.accept | 1 − (e^{-0.2})^5 = 1 − e^{-1} = 0.6321 | correct | Display only; key still 0.6321; (e^{-0.2})^5 = e^{-1}, 1 − 0.36788 = 0.63212 |
| 19 | l17 | screens[8].hints[1].text | None default with chance (e^{-0.2})^5 = e^{-1} | correct | As row 18 |
| 20 | l17 | screens[8].feedback.byKey.five | 0.9063 is 5 × 0.181269 | correct | 1 − e^{-0.2} = 0.181269; product 0.906345; slip value 0.9063 unchanged |
| 21 | l17 | screens[10].prose | For independent continuous draws a tie has probability 0, so the maximum comes from one draw alone | correct | P(X = Y) = 0 for independent continuous X, Y; without independence (X = Y) it fails, so the added word is needed. No ties in 200,000 simulated rows |
| 22 | l17 | screens[10].feedback.byKey.cdf | 0.25 is P(max ≤ 3) = (½)², which includes a maximum of 1 or 2 | correct | Enumeration of 36 cells: 9 with max ≤ 3, maxima 1, 2, 3 |
| 23 | l17 | screens[11].widget.accept | 1 − Φ(2.1)^20 = 1 − 0.982136^20 ≈ 0.3027 | correct | Display only; key still 0.3027; Φ(2.1) = 0.9821356; 0.982136^20 = 0.69733; simulation 0.303 |
| 24 | l17 | screens[11].hints[1].text | Φ(2.1) = 0.982136 | correct | scipy norm.cdf |
| 25 | l17 | screens[11].hints[2].text | 1 − 0.982136^20 | correct | As row 23 |
| 26 | l17 | screens[11].feedback.correct | 1 − 0.982136^20 = 0.3027 | correct | As row 23 |
| 27 | l17 | screens[11].feedback.byKey.times | 0.3573 is 20 × 0.017864 | correct | 1 − 0.982136 = 0.017864; product 0.35728; slip value unchanged |
| 28 | l17 | summary.ideas[0] | For n independent draws with CDF F: P(max ≤ t) = F(t)^n, P(min > t) = (1 − F(t))^n | correct | Casella and Berger 5.4; fails for dependent draws, so the hypothesis is needed |
| 29 | l17 | summary.formula.note | For independent continuous draws ties have chance 0 | correct | As row 21 |
| 30 | l18 | screens[0].prose | Trades arrive as a Poisson process at 2 a minute, so each gap is exponential with mean half a minute | correct | Ross 5.3.3; a rate alone would not fix the gap law; third arrival Gamma(3, rate 2) by KS test |
| 31 | l18 | screens[4].question | Six independent standard normal returns squared and added; Var(V) | correct | Chi-square(6), variance 12; simulated 12.0; key unchanged |
| 32 | l18 | screens[5].prose | With V chi-square on n df and independent of Z, Z/√(V/n) has the t distribution | correct | Casella and Berger Def 5.3.4; simulation: dependent Z and V give a different tail beyond ±2 |
| 33 | l18 | screens[8].explain.text | The arcsine law describes the share of time a long fair random walk spends positive | correct | Feller vol. 1, III.4 (limit law); walk of 1,000 steps: share below 0.25 about 1/3; a four-step walk is not close |
| 34 | l18 | summary.ideas[1] | Sum of n independent squared standard normals is chi-square, Gamma(a = n/2, λ = ½); with Z independent of V the ratio is t | correct | Rate convention kept (λ = ½ is a rate, matching the formula box); Casella and Berger 5.3 |
| 35 | l19 | screens[6].explain.text | Independence is enough for the product rule; without it E[e^{tX}e^{tY}] can fail to split | correct | Sufficient, not necessary: script builds a dependent pair whose sum has the product MGF; Y = X gives M(2t) ≠ M(t)². Blitzstein and Hwang 6.4 |
| 36 | l19 | screens[8].prose | X_i independent and identically distributed with mean μ, sd σ | correct | The first line of the derivation uses a common M_Y, so iid is needed; agrees with line `mgf` |
| 37 | l19 | summary.ideas[2] | Chernoff bounds a tail by min over t > 0 of e^{-ta}M(t)^n | correct | Markov on e^{tS} needs t > 0 for an upper tail; agrees with the Chernoff screen; script shows the unrestricted minimum is not a bound. Mitzenmacher and Upfal 4.2 |
| 38 | l19 | summary.formula.tex | P(S ≥ a) ≤ min_{t>0} e^{-ta}M(t)^n | correct | As row 37 |
| 39 | problems-4 | items[2].parts[4].explain.text | X(3) > 0.5 exactly when at least 2 of 4 quotes are above 0.5; fails with 0 or 1 above, (1+4)/16; P = 11/16; Beta(3, 2) integral agrees | correct | Enumeration of 16 patterns at thresholds 0.3, 0.5, 0.8 matches the Beta(3, 2) tail; sympy integral 11/16; prose states uniform and independent |
| 40 | problems-4 | items[3].parts[0].feedback.byKey.power | (1−2s)^{-1/8}: divided the exponent by 4; four copies multiply it by 4: −½ × 4 = −2 | correct | −½ ÷ 4 = −1/8 is the option; −½ × 4 = −2 is the key |
| 41 | review-4 | items[4].widget.accept | 1 − Φ(2)^10 = 1 − 0.97725^10 ≈ 0.2056 | correct | Display only; key still 0.2056; Φ(2) = 0.977250; 0.97725^10 = 0.79443 |
| 42 | review-4 | items[4].feedback.correct | 1 − 0.97725^10 = 0.2056 | correct | As row 41 |
| 43 | review-4 | items[4].feedback.byKey.times | 0.2275 is 10 × 0.02275 | correct | Product exact; slip value unchanged |
| 44 | review-4 | items[4].explain.text | Φ(2)^10 = 0.7944; a search over ten skill-free strategies turns up a best of 2 or more about one time in five; that is not the chance a reported best of 2 is luck, which depends on how common skill is | correct | 0.2056 is P(best ≥ 2 given no skill). By Bayes' rule P(no skill given best ≥ 2) moves from 0.69 to 0.03 as the share of skilled searches goes from 0.1 to 0.9 (script example, skill worth one sd). Neither the inverse reading nor a new error; three sentences |

Counts: 44 rows; 43 correct, 0 wrong, 1 imprecise, 0 misleading, 0 unverified.

Voice on the 44 strings: no exclamation marks, no em-dashes, no US spellings, no lesson numbers, no sentence over 35 words, no explanation over three sentences.

Findings

1. l15-new-variables.json | screens[3].prose | imprecise | minor | The fix added "or strictly decreasing" but kept "the chain rule on $F_Y(y) = F_X(x)$". That identity holds only for increasing $g$. For decreasing $g$, $F_Y(y) = 1 - F_X(x)$. The screen's own map $Y = -\tfrac12\ln U$ is decreasing, so a learner who checks the stated step finds it false there. The final formula and its hypotheses are right. | $F_Y(0.3) = 1 - e^{-0.6} = 0.4512$ against $F_U(e^{-0.6}) = 0.5488$ (script check "l15 prose"). Casella and Berger, Theorems 2.1.3 and 2.1.5: $F_Y(y) = F_X(g^{-1}(y))$ for increasing $g$ and $1 - F_X(g^{-1}(y))$ for decreasing $g$. | Replace the prose with: `You went from $U$ to $Y$ through the CDF. Let $Y = g(X)$ with $x = g^{-1}(y)$ differentiable. For strictly increasing $g$, $F_Y(y) = F_X(x)$. For strictly decreasing $g$, $F_Y(y) = 1 - F_X(x)$. Either way the chain rule gives $$f_Y(y) = f_X(x)\left|\frac{dx}{dy}\right|.$$` (in JSON, each backslash doubled).

## Follow-up (fix-pass read)

Finding 1, `l15-new-variables.json` `screens[3].prose`.

Old: `You went from $U$ to $Y$ through the CDF. For $Y = g(X)$ with $g$ strictly increasing or strictly decreasing and $x = g^{-1}(y)$ differentiable, the chain rule on $F_Y(y) = F_X(x)$ gives $$f_Y(y) = f_X(x)\left|\frac{dx}{dy}\right|.$$`

New: `You went from $U$ to $Y$ through the CDF. Let $Y = g(X)$ with $x = g^{-1}(y)$ differentiable. For strictly increasing $g$, $F_Y(y) = F_X(x)$. For strictly decreasing $g$, like $-\tfrac12\ln U$, $F_Y(y) = 1 - F_X(x)$. Either way the chain rule gives $$f_Y(y) = f_X(x)\left|\frac{dx}{dy}\right|,$$ since $\tfrac{dx}{dy} < 0$ exactly when $g$ decreases.`

Basis: increasing $g$ gives $f_Y = f_X\,dx/dy$ with $dx/dy > 0$; decreasing $g$ gives $P(X \ge x) = 1 - F_X(x)$, so $f_Y = -f_X\,dx/dy$ with $dx/dy < 0$ (Casella and Berger, Theorems 2.1.3 and 2.1.5). For $Y = -\tfrac12\ln U$: $F_Y(y) = P(U \ge e^{-2y}) = 1 - e^{-2y}$, density $2e^{-2y}$, rate 2; simulated mean 0.500, $F_Y(0.3) = 0.4506$ against 0.4512. Sibling statements (`summary.ideas[0]`, `screens[10].explain.text`, hints) state only the final rule and its hypotheses, so they stand. Script: `limits-thm-L4-fixread.py` line 131 tested the old wording; it now anchors on the new decreasing-case sentence, and the identity check finds `1 - F_X` (662 checks, 0 failed).
