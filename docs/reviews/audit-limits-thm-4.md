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

PENDING: filled after the WIP commit.

## Inbox

- Validator or number-script rule: where a feedback line says "`V` is `a × b`" (or `a^n`) with literal numbers, recompute the product from the digits shown and warn when it does not round to `V`. Four cases in this level (finding 20). The slip-names-the-wrong-quantity class also appears four more times here (findings 5, 7, 8, 10).
- Validator warning list for universal wording in explanations: "any other", "does not split", "exactly when", "always", "never", "needs independence". Print them for the second reader. Findings 1, 2, 3 and 9 would each have been listed.
