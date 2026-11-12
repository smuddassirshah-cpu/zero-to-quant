# Claim ledger: delta audit batch 2, 12 Nov 2026

Audit file: `docs/reviews/audit-delta-2026-11-12-2.md`. Script: `docs/reports/delta-2026-11-12-2-concepts.py` (rows marked S are also checked there). Engine facts used as basis: `app/js/engine/grade.js` `within` (band is the value plus or minus `abs`, plus 1e-9), `numGrade` (key first, then `wrong[]` in order), `parseNum` (a typed `%` divides by 100; with `unit: "%"` a bare number is divided by 100).

105 rows: 100 correct, 5 imprecise, 0 wrong, 0 misleading, 0 unverified.

| # | course | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|---|
| 1 | puzzles | homework-4.json | items[6].widget.wrong[2] | Slip `sign` is 0.2713, the key with its sign dropped | correct | S. $512(19/37)^9 - 1 = 0.27130$. |
| 2 | puzzles | homework-4.json | items[6].feedback.byKey.sign | $1 - 512q^9$ is below zero because the £511 loss outweighs the £1 gain; a positive value books a loss as a gain | correct | Derivation: $(1 - q^9) \times 1 - 511q^9 = 1 - 512q^9 = -0.2713$. The loss term is $511 \times 0.002483 = 1.269$ against a win term of 0.9975. |
| 3 | puzzles | homework-4.json | items[6].widget | 0.2713 is no valid reading; bands of key, `fair`, `ten`, `sign` are disjoint | correct | S. The prompt asks for expected gain, so the sign is fixed. Values −0.2713, 0, −0.3056, 0.2713 at ±0.0005. |
| 4 | game-theory | l9-winners-curse.json | screens[5].widget.wrong[2] | Slip `sign` is 7.2 | correct | S. $0.6 \times 12 = 7.2$. |
| 5 | game-theory | l9-winners-curse.json | screens[5].feedback.byKey.sign | Accepted with chance 0.6, then loses £12m, so $0.6 \times (-12)$ is negative | correct | Prose of the screen; $1.6 \times 30 - 60 = -12$. Standard acquire-a-company working (Bazerman and Samuelson 1983). |
| 6 | game-theory | l9-winners-curse.json | screens[5].widget | 7.2 is no valid reading; bands disjoint | correct | S. "Expected profit" fixes the sign. Values −7.2, −12, 20, 7.2 at ±0.01. |
| 7 | game-theory | review-2.json | items[7].widget.wrong[2] | Slip `sign` is 4 | correct | S. $0.4 \times (40 - 30) = 4$. |
| 8 | game-theory | review-2.json | items[7].feedback.byKey.sign | You pay £40m for a firm worth £30m to you, so $0.4 \times (30 - 40)$ is negative | correct | Accepted firms have $V$ uniform on 0 to 40, mean 20, worth $1.5 \times 20 = 30$. "Worth £30m" is the conditional average, as the neighbouring `naive` line and the explain say. |
| 9 | game-theory | review-2.json | items[7].widget | 4 is no valid reading; bands disjoint | correct | S. Values −4, −10, 35, 4 at ±0.01. |
| 10 | coding-int | l7-parsing-with-a-stack.json | screens[4].widget.wrong[2] | Slip `sign` is 3 | correct | S. $-7/2 = -3.5$, truncated to −3; without the sign, 3. |
| 11 | coding-int | l7-parsing-with-a-stack.json | screens[4].feedback.byKey.sign | Truncating towards zero turns −3.5 into −3; a positive 3 drops the minus sign | correct | C++ `/` on `int` and Python `int(-7/2)` both give −3 (C++17 [expr.mul] para 4). |
| 12 | coding-int | l7-parsing-with-a-stack.json | screens[4].widget | 3 is no valid reading; values −3, −4, −3.5, 3 are distinct at tolerance 0 | correct | S. No division convention gives a positive quotient for $-7/2$. |
| 13 | coding-int | l7-parsing-with-a-stack.json | quiz[1].widget.wrong[1] | Slip `sign` is 2 | correct | S. $-8/3$ truncates to −2. |
| 14 | coding-int | l7-parsing-with-a-stack.json | quiz[1].feedback.byKey.sign | $-8/3$ is −2.67 and truncates to −2 | correct | $-8/3 = -2.667$, shown to 2 places as the item's `accept` and `correct` lines do. |
| 15 | coding-int | l7-parsing-with-a-stack.json | quiz[1].widget | 2 is no valid reading; values −2, −3, 2 distinct | correct | S. |
| 16 | coding-int | l8-simulating-the-rules.json | screens[9].widget.wrong[3] | Slip `sign` is 1 | correct | S. $13 - 12 = 1$. |
| 17 | coding-int | l8-simulating-the-rules.json | screens[9].feedback.byKey.sign | Day 3 gains 12, day 6 loses 13, total $12 - 13$ | correct | S. Cells: $252 - 240 = 12$, $236 - 249 = -13$; $25{,}200 \ge 105 \times 240$ and $23{,}600 \le 97 \times 249 = 24{,}153$. |
| 18 | coding-int | l8-simulating-the-rules.json | screens[9].widget | 1 is no valid reading; values −1, 3, −2, 12, 1 distinct | correct | S. "Total profit" fixes the sign. |
| 19 | coding-int | review-2.json | items[5].widget.wrong[1] | Slip `sign` is 2 | correct | S. $-9/4 = -2.25$, truncated to −2. |
| 20 | coding-int | review-2.json | items[5].feedback.byKey.sign | $-9/4$ is −2.25 and truncates to −2 | correct | Arithmetic; as row 11. |
| 21 | coding-int | review-2.json | items[5].widget | 2 is no valid reading; values −2, −3, 2 distinct | correct | S. |
| 22 | measure-prob | l15-likelihood-ratios.json | screens[5].widget.wrong[2] | Slip `decimal` is 0.021 ± 0.001 | correct | S. $6.73 \times 10^{-7} / 3.185 \times 10^{-5} = 0.02113$, inside the band. |
| 23 | measure-prob | l15-likelihood-ratios.json | screens[5].feedback.byKey.decimal | 0.021 is 2.1% as a decimal; the field wants the number of per cent, typed without a % sign | correct | The question asks for a percentage and the label is "%". The engine reads a typed "2.1%" as 0.021 on this widget (no `unit`), so the last clause is true and needed. Inbox bullet raised. |
| 24 | measure-prob | l15-likelihood-ratios.json | screens[5].widget | Bands disjoint: 2.1 ± 0.1, 47.3 ± 0.5, 212.4 ± 3, 0.021 ± 0.001 | correct | S. No other slip's decimal form (0.473, 2.124) falls in the new band. |
| 25 | measure-prob | homework-3.json | items (h-prove-urn).rubric[3] | $P(D_{n+1} = 1) = E[M_n] = \tfrac12$ by the tower property | correct | $E[D_{n+1}] = E[E[D_{n+1} \mid \mathcal{F}_n]] = E[M_n] = M_0$ (Williams, *Probability with Martingales*, 9.7 and 10.3). |
| 26 | measure-prob | homework-3.json | items (h-prove-urn).rubric[3] | The symmetry of the two colours is also a valid reason | correct | The urn starts with one ball of each colour and the rule treats colours alike, so swapping colours preserves the law: $P(\text{red}) = P(\text{blue}) = \tfrac12$. |
| 27 | mm-games | l11-hedging.json | screens[3].widget.wrong[2] | Slip `decimal` is 0.012 ± 0.00024 | correct | S. $2 \times \sqrt{1 - 0.64} = 1.2$, over 100. |
| 28 | mm-games | l11-hedging.json | screens[3].feedback.byKey.decimal | 0.012 is 1.2% as a decimal; type 1.2 without a % sign | correct | The question says "in per cent". A typed "1.2%" parses to 0.012 here. |
| 29 | mm-games | l11-hedging.json | screens[3].widget | Bands disjoint: 1.2, 0.72, 0.4 at ±0.001, 0.012 ± 0.00024 | correct | S. Decimal forms of the other slips (0.0072, 0.004) lie outside. |
| 30 | mm-games | l11-hedging.json | quiz[1].widget.wrong[2] | Slip `decimal` is 0.04 ± 0.0008 | correct | S. $5 \times 0.8 = 4$, over 100. |
| 31 | mm-games | l11-hedging.json | quiz[1].feedback.byKey.decimal | 0.04 is 4% as a decimal; type 4 | correct | As row 28. |
| 32 | mm-games | l11-hedging.json | quiz[1].widget | Bands disjoint: 4, 3.2, 2 at ±0.001, 0.04 ± 0.0008 | correct | S. Decimal forms 0.032 and 0.02 lie outside. |
| 33 | mm-games | l17-options-on-a-game.json | screens[4].widget.wrong[2] | Slip `sign2` is 0.3 | correct | S. $3 - 2.70 = 0.30$. |
| 34 | mm-games | l17-options-on-a-game.json | screens[4].feedback.byKey.sign2 | Short 1 and the straddle pays 3, so the P&L is $2.70 - 3$ | correct | Straddle payoff $|4 + 6 - 7| = 3$; a short position owes it. |
| 35 | mm-games | l17-options-on-a-game.json | screens[4].widget | 0.3 is no valid reading; bands disjoint | correct | S. "P&L" fixes the sign. Values −0.3, 1.7, 5.7, 0.3 at ±0.001. |
| 36 | mm-games | review-3.json | items[5].widget.wrong[2] | Slip `decimal` is 0.0087 | correct | S. $2 \times \sqrt{0.19} = 0.8718$, over 100 is 0.008718. |
| 37 | mm-games | review-3.json | items[5].feedback.byKey.decimal | 0.0087 is 0.87% as a decimal; type 0.87 | correct | As row 28. |
| 38 | mm-games | review-3.json | items[5].widget.wrong[2].tol | The band ±0.005 marks only the decimal form of the key | imprecise | S, FINDING 1. The band is 0.0037 to 0.0137. It takes 0.0038 (the `var` slip typed as "0.38%") and 0.01 ("1%"), and tells both they wrote 0.87%. |
| 39 | recruiting | l9-sitting-an-assessment.json | screens[3].widget.wrong[3] | Slip `sign` is 0.5 | correct | S. $\tfrac34 - \tfrac14 = 0.5$. |
| 40 | recruiting | l9-sitting-an-assessment.json | screens[3].feedback.byKey.sign | Right a quarter of the time, wrong three quarters, so $\tfrac14 - \tfrac34$ is below zero | correct | $E = \tfrac14(+1) + \tfrac34(-1) = -\tfrac12$. |
| 41 | recruiting | l9-sitting-an-assessment.json | screens[3].widget | 0.5 is no valid reading; bands disjoint | correct | S. "Worth on average, in marks" fixes the sign. Values −0.5, 0.25, 0, −0.75, 0.5 at ±0.01. |
| 42 | conditional | l25-survivorship.json | screens[9].widget.wrong[3] | Slip `sign2` is 0.0025 (0.25% on a `%` widget) | correct | S. $(45 - 40)/20 = 0.25$; the engine divides a bare 0.25 by 100. |
| 43 | conditional | l25-survivorship.json | screens[9].feedback.byKey.sign2 | $(40 - 45)/20 = -5/20$; the abandoned lost 45 in total against 40 gained | correct | $5 \times 8 = 40$, $15 \times 3 = 45$ percentage points. |
| 44 | conditional | l25-survivorship.json | screens[9].widget | 0.25% is no valid reading; bands disjoint | correct | S. Values −0.0025, 0.08, 0.025, 0.0425, 0.0025 at ±0.00005. |
| 45 | conditional | problems-5.json | items[3].parts[2].widget.wrong[3] | Slip `sign` is 22.55 | correct | S. $20 \times (31/32)^{20} / (1 - (31/32)^{20}) = 22.549$. |
| 46 | conditional | problems-5.json | items[3].parts[2].feedback.byKey.sign | Survivors made £20 and the total average is £0, so quitters lost money | correct | Law of total expectation: $0 = 0.5299 \times 20 + 0.4701 \times E[\text{profit} \mid \text{quit}]$. |
| 47 | conditional | problems-5.json | items[3].parts[2].widget.wrong[3].tol | The band ±0.005 catches the sign-dropped answer | imprecise | S, FINDING 2. The prompt says to use 0.5299, which gives 22.54. The key takes −22.54 (±0.01), but the slip band 22.545 to 22.555 misses +22.54. |
| 48 | conditional | review-5.json | items[5].widget.wrong[3] | Slip `sign` is 0.331 | correct | S. $7 \times 0.166375 - 0.833625 = 0.331$. |
| 49 | conditional | review-5.json | items[5].feedback.byKey.sign | $0.833625 - 7 \times 0.166375$ is below zero | correct | $0.55^3 = 0.166375$; $1.164625 > 0.833625$. |
| 50 | conditional | review-5.json | items[5].widget | 0.331 is no valid reading; bands disjoint | correct | S. Values −0.331, 1, 0, 0.833625, 0.331 at ±0.001. |
| 51 | conditional | review-5.json | items (r-low-prior).widget.tol | The key 0.4615 is now taken within ±0.005; no slip falls inside | correct | S. $6/13 = 0.46154$. Slips 0.6 and 0.8571 are far outside 0.4565 to 0.4665. |
| 52 | conditional | review-5.json | items (r-low-prior).widget.accept | "or $0.4615 \pm 0.0005$" | imprecise | S, FINDING 3. The widget now takes ±0.005, so the line a learner reads after grading understates what was accepted. |
| 53 | odes | fluency-l2-separable.json | families[0].widget.answer | $v' = kv$, $v(0) = y_0$ has solution $y_0e^{kt}$ | correct | S (sympy, every draw). Boyce and DiPrima, *Elementary Differential Equations*, 2.2. |
| 54 | odes | fluency-l2-separable.json | families[0].wrong[0] | `constant-added` is $e^{kt} + (y_0 - 1)$: the constant added after exponentiating and fitted to the start | correct | S. It meets $v(0) = y_0$ and fails the equation. $e^{kt + C} = e^Ce^{kt}$. |
| 55 | odes | fluency-l2-separable.json | families[0].wrong[1] | `start-not-used` $e^{kt}$ solves the equation but has $v(0) = 1$ | correct | S. $y_0 \ge 2$, so it never equals the key. |
| 56 | odes | fluency-l2-separable.json | families[0].solution | $\ln|v| = kt + C$, $v = Ae^{kt}$, $A = y_0$ | correct | $A = \pm e^C$; the lost solution $v = 0$ is not needed since $y_0 > 0$. |
| 57 | odes | fluency-l2-separable.json | families[1].widget.answer | $y' = (bt + a)y$ has solution $y_0e^{(b/2)t^2 + at}$ | correct | S. $b$ is even, so the exponent has whole coefficients. |
| 58 | odes | fluency-l2-separable.json | families[1].wrong[0] | `rate-kept-constant` is $y_0e^{at}$, the rate held at its value at $t = 0$ | correct | S. The rate at 0 is $a$. |
| 59 | odes | fluency-l2-separable.json | families[1].wrong[1] | `not-halved` is $y_0e^{bt^2 + at}$; $\int bt\,dt = (b/2)t^2$ | correct | S. |
| 60 | odes | fluency-l2-separable.json | families[1].solution | $\ln|y| = (b/2)t^2 + at + C$, $A = y_0$ | correct | S. |
| 61 | odes | fluency-l2-separable.json | families[2].widget.answer | $y' = ky^2$, $y(0) = y_0$ has solution $y_0/(1 - ky_0t)$ | correct | S. Boyce and DiPrima 2.2 and 2.4 (example of finite-time blow-up). |
| 62 | odes | fluency-l2-separable.json | families[2] | Domain of validity | correct | The solution holds on the interval round 0 where $1 - ky_0t \ne 0$. The item makes no claim for all $t$, and the form typed is the same either way. |
| 63 | odes | fluency-l2-separable.json | families[2].wrong[0] | `solved-linear` is $y_0e^{kt}$, which solves $y' = ky$ | correct | S. |
| 64 | odes | fluency-l2-separable.json | families[2].wrong[1] | `sign-lost` is $y_0/(1 + ky_0t)$, from $+1/y = kt + C$ | correct | S. $C = 1/y_0$ gives $y = 1/(kt + 1/y_0)$. |
| 65 | odes | fluency-l2-separable.json | families[2].solution | $-1/y = kt + C$, $C = -1/y_0$, $1/y = 1/y_0 - kt$ | correct | S, including negative $y_0$. |
| 66 | odes | fluency-l2-separable.json | families[3].widget.answer | Value today is $pe^{-rT}$, to the penny, tolerance 0.0051 | correct | S. Hull, *Options, Futures and Other Derivatives*, 4.2 (continuous compounding). |
| 67 | odes | fluency-l2-separable.json | families[3].prompt | $D' = -rD$, $D(0) = 1$ defines the discount factor; $r$ per year with $T$ in years | correct | $D(T) = e^{-rT}$. The unit of $r$ is implied by "in $n$ years". |
| 68 | odes | fluency-l2-separable.json | families[3].wrong[0] | `simple-discount` is $p(1 - rT)$; "took off $r$% of £$p$ for each year" | correct | S. Its band never meets the key's: the gap is at least $100(e^{-0.02} - 0.98) = 0.0199$. |
| 69 | odes | fluency-l2-separable.json | families[3].wrong[1] | `yearly-discount` is $p/1.0r^{n}$, offered when more than 0.01 from the key | correct | S. Withheld for $p = 100$, $r = 1$, $n = 2$ (gap 0.0097). |
| 70 | odes | fluency-l2-separable.json | families[3].solution | $D(T) = e^{-rT}$, $rT = x$, value $pe^{-x}$ | correct | S. |
| 71 | odes | fluency-l2-separable.json | families[3].widget.placeholder | "For example 81.87" is only an example | imprecise | S, FINDING 5. 81.87 is the key when $p = 100$ and $rT = 0.2$: draws (100, 2, 10), (100, 4, 5), (100, 5, 4), 3 of 729. |
| 72 | odes | fluency-l3-integrating-factor.json | families[0].widget.answer | $\mu = e^{\int p\,dt}$ for $y' + p(t)y = q(t)$ | correct | S: $\mu(y' + py) = (\mu y)'$ for every draw. Boyce and DiPrima 2.1. |
| 73 | odes | fluency-l3-integrating-factor.json | families[0] | "The" factor takes the constant of integration as zero | correct | Standard convention (Boyce and DiPrima 2.1); any constant multiple also works but is never the natural answer. |
| 74 | odes | fluency-l3-integrating-factor.json | families[0].wrong[0] | `e-to-the-p` is $e^{p}$ | correct | S. Never equals the key in the eleven power pairs. |
| 75 | odes | fluency-l3-integrating-factor.json | families[0].wrong[1] | `sign-flipped` is $e^{-\int p\,dt}$; the factor is $e^{+\int p\,dt}$ for $y' + py$ | correct | S. For a minus in the prompt, $p$ is negative and the key's exponent is negative. |
| 76 | odes | fluency-l3-integrating-factor.json | families[0].solution | $p(t)$ and $\int p\,dt$ as stated | correct | S. The pairs make $m/(n+1)$ whole. |
| 77 | odes | fluency-l3-integrating-factor.json | families[1].widget.answer | $v' = av - as$, $v(0) = y_0$ has solution $(y_0 - s)e^{at} + s$ | correct | S. |
| 78 | odes | fluency-l3-integrating-factor.json | families[1].wrong[0] | `steady-sign` is $(y_0 + s)e^{at} - s$, the steady level taken as $+q/a = -s$ | correct | S. $av + q = 0$ gives $v = -q/a = s$. |
| 79 | odes | fluency-l3-integrating-factor.json | families[1].wrong[1] | `inflow-dropped` is $y_0e^{at}$, which solves $v' = av$; withheld at $y_0 = 0$ | correct | S. |
| 80 | odes | fluency-l3-integrating-factor.json | families[1].solution | The gap $v - v^*$ moves as $e^{at}$ and starts at $y_0 - s$ | correct | $(v - s)' = a(v - s)$. |
| 81 | odes | fluency-l3-integrating-factor.json | families[1].prompt | The answer is a function of $t$ | imprecise | S, FINDING 4. The prompt writes $v'$ and $v(0)$ and never names $t$; $e^{ax}$ is marked wrong. |
| 82 | odes | fluency-l3-integrating-factor.json | families[2].widget.answer | $B' = \rho B + d$, $B(0) = 0$ gives $B(n) = (d/\rho)(e^{\rho n} - 1)$ | correct | S (sympy `dsolve`, every draw). |
| 83 | odes | fluency-l3-integrating-factor.json | families[2].wrong[0] | `deposits-only` is $dn$ | correct | S. |
| 84 | odes | fluency-l3-integrating-factor.json | families[2].wrong[1] | `minus-one-dropped` is $(d/\rho)e^{\rho n}$; the $-1$ comes from $B(0) = 0$ | correct | S. |
| 85 | odes | fluency-l3-integrating-factor.json | families[2].solution | The factor is $e^{-\rho t}$ | correct | $B' - \rho B = d$, so $p = -\rho$. |
| 86 | odes | fluency-l3-integrating-factor.json | families[2].widget.placeholder | 15569.31 is no draw's key | correct | S, all 819 draws. |
| 87 | odes | fluency-l7-characteristic-equation.json | families[0].widget.answers | The roots of $r^2 + br + c = 0$ are $r_1$ and $r_2$ | correct | S. Boyce and DiPrima 3.1. |
| 88 | odes | fluency-l7-characteristic-equation.json | families[0].wrong[0] | `signs-flipped` solves $r^2 - br + c = 0$ | correct | S. `where` keeps $r_1 + r_2 \ne 0$, so the set differs from the key. |
| 89 | odes | fluency-l7-characteristic-equation.json | families[0].wrong[1] | `not-halved` is $2r_1, 2r_2$, the formula without the division by $2a = 2$ | correct | S: $-b \pm \sqrt{b^2 - 4c}$. |
| 90 | odes | fluency-l7-characteristic-equation.json | families[0].solution | Trying $e^{rt}$ gives the characteristic equation; it factorises as stated | correct | S. |
| 91 | odes | fluency-l7-characteristic-equation.json | families[1].widget.answer | The root with positive imaginary part is $\alpha + \beta i$ | correct | S. Boyce and DiPrima 3.3. |
| 92 | odes | fluency-l7-characteristic-equation.json | families[1].wrong[0] | `other-root` is the conjugate | correct | S. |
| 93 | odes | fluency-l7-characteristic-equation.json | families[1].wrong[1] | `minus-b-dropped` is $-\alpha + \beta i$; the real part is $-b/2 = \alpha$ | correct | S. |
| 94 | odes | fluency-l7-characteristic-equation.json | families[1].wrong[2] | `not-halved` is $\alpha + 2\beta i$, the root of the discriminant not halved | correct | S. $\sqrt{-4\beta^2} = 2\beta i$. |
| 95 | odes | fluency-l7-characteristic-equation.json | families[1].solution | Discriminant $-4\beta^2$, $r = (2\alpha \pm 2\beta i)/2$ | correct | S. |
| 96 | odes | fluency-l7-characteristic-equation.json | families[2].widget.answer | $y = c_1e^{r_1t} + c_2e^{r_2t}$ fitted to $y(0)$ and $y'(0)$ | correct | S (sympy `dsolve` with both starting values, every draw). Unique since $r_1 \ne r_2$. |
| 97 | odes | fluency-l7-characteristic-equation.json | families[2].wrong[0] | `constants-swapped`, offered when $c_1 \ne c_2$ | correct | S. Meets $y(0)$, fails $y'(0)$. |
| 98 | odes | fluency-l7-characteristic-equation.json | families[2].wrong[1] | `one-constant` is $y_0e^{r_1t}$, offered when $y_0 \ne 0$ | correct | S. Never the key, since $c_2 \ne 0$. |
| 99 | odes | fluency-l7-characteristic-equation.json | families[2].solution | $c_1 + c_2 = y_0$ and $r_1c_1 + r_2c_2 = y'(0)$ | correct | S. |
| 100 | odes | fluency-l7-characteristic-equation.json | families[2].prompt | The answer is a function of $t$ | imprecise | S, FINDING 4. As row 81. |
| 101 | odes | fluency-l7-characteristic-equation.json | families[3].widget.answer | A repeated root $r$ gives $y = (c_1 + c_2t)e^{rt}$, here $(kt + y_0)e^{rt}$ | correct | S (sympy `dsolve`). Boyce and DiPrima 3.4. |
| 102 | odes | fluency-l7-characteristic-equation.json | families[3].wrong[0] | `rc1-forgotten` sets $c_2 = y'(0)$; in fact $y'(0) = rc_1 + c_2$ | correct | S. $c_2 = y'(0) - ry_0 = k$. |
| 103 | odes | fluency-l7-characteristic-equation.json | families[3].wrong[1] | `t-term-dropped` is $y_0e^{rt}$; a repeated root needs $te^{rt}$ too | correct | S. $k \ne 0$, so it never equals the key. |
| 104 | odes | fluency-l7-characteristic-equation.json | families[3].solution | $(r - r_0)^2 = 0$, $c_1 = y_0$, $c_2 = k$ | correct | S. |
| 105 | odes | fluency-l7-characteristic-equation.json | families[3].prompt | The answer is a function of $t$ | imprecise | S, FINDING 4. As row 81. |
