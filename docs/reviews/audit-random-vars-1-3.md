# Concept audit, round 1: random-vars levels 1 to 3

Auditor: blind Fable reader, round 1. Scope: `app/content/courses/random-vars/` files `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `h-build-pmf`), `problems-1` to `problems-3` and `fluency-l9-measuring-spread`. Levels 4 and 5 are out of scope. Topic 1.5 is Stage 1, so the ledger has full depth.

Blind rule: the ledger, the findings below and the concepts script were written and committed before any earlier review, audit, ledger, concepts script, author report, git history or diff of the course folder was opened. The overlap table, the gate results and the inbox note were added afterwards.

Ledger: `docs/reports/audit-random-vars-1-3-ledger.md` (334 rows: correct 322, wrong 2, imprecise 10, misleading 0, unverified 0).

Script: `docs/reports/random-vars-L1-3-concepts.py`, run from the repo root. 158 checks, 13 failed, exit 1. The 13 failing checks are the findings below (findings 2, 3 and 4 have two checks each) and stay failing until the content is fixed. The other 145 recompute the graded keys and stated results by exact enumeration, closed form or seeded Monte Carlo, and run the three Python widgets against their hidden tests in CPython 3.13 (solutions pass, starters fail, stated test counts match, the two seeded console values 3.50167 and 2.9207 reproduce).

Findings: 10. wrong 2 (both serious); imprecise 8 (1 serious, 7 minor); misleading 0.

## What was checked and found sound

- A random variable is taught as a rule from outcomes to numbers, events {X = x} as sets, and the pmf as the chance of each value (l1, l2).
- The CDF is F(x) = P(X ≤ x) with the closed dot on the upper step in every staircase, flat between values, and the strict and weak cases are kept apart in every key (l3, review-1, homework-1, problems-1).
- A function that is not one-to-one merges values and their chances add; a one-to-one function only relabels (l4).
- Expectation is a probability-weighted average. Every variable in scope takes finitely many values, so it always exists; the unbounded St Petersburg sum is shown in homework-2.
- "Fair price" is defined as the expected payoff, the price with zero average profit. The lesson says a fair bet is "fair, not good: it has no edge, only risk" and names risk-neutral probabilities, so no claim is made about what anyone would pay (l6).
- Linearity is derived from the joint table without independence (l7 `screens[8]`), and the indicator method is used on dependent events throughout (l8).
- Variance is always that of a distribution, so no item needs an n or n − 1 choice. Var(aX + b) = a²Var(X), with the sd scaling by |a| (l10).
- Zero covariance without independence is taught with Y = X², correlation is unitless and in [−1, 1], and it is distinguished from a slope (l11).
- The portfolio formula carries the weights and the correlation; the equal-weight limit is ρσ², not zero, and only idiosyncratic risk is said to diversify away (l12).
- Annualising uses 252 trading days and is said to assume independent days (l10; see finding 8 for what is left unsaid).

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `l7-linearity.json` | `screens[2].explain.text` (last sentence) | wrong | serious | "Nothing in the argument used the dice being independent." The argument on this screen did use it. | The screen argues that row k averages k + 3.5 and then averages the six rows. Row k averages k + 3.5 only because the second die is uniform within every row, that is E[Y given X = k] = 3.5 for every k, which holds because the dice are independent. For Y = X, row k holds the single possible cell 2k, so the row averages are not k + 3.5 (script: "l7 row k averages..."). Linearity itself needs no independence, and `screens[8]` proves that properly from the joint table. A learner who trusts the sentence takes away that a row average is always k + E[Y], which is false and is exactly what conditional expectation later corrects. Basis: derivation; Blitzstein and Hwang 4.2 and 9.1. | `explain.text`: "The row averages are $X + 3.5$ for each value of $X$, so their average is $E[X] + 3.5 = 7$. This is **linearity of expectation**: $E[X + Y] = E[X] + E[Y]$. Here each row averaged $k + 3.5$ because the dice are independent; the next screens show the rule holds without that."

2. `l7-linearity.json`, `homework-2.json` | l7 `quiz[2].explain.text` (last sentence); homework-2 `items[6].feedback.byKey.product` | wrong | serious | "The product rule fails for dependent variables." As a general statement this is false: dependent variables can satisfy E[XY] = E[X]E[Y]. The homework line makes the same inference ("X and Y are dependent, so the product rule fails"). | X uniform on −1, 0, 1 and Y = X² are dependent, and E[XY] = 0 = E[X]E[Y] (script). The course's own l11 `screens[7]` uses this pair to show zero covariance without independence, so the two lessons contradict each other. The rule can fail under dependence; it fails exactly when the covariance is not zero. In the homework item it fails because Cov(X, 7 − X) = −35/12. Basis: Blitzstein and Hwang 7.3, example 7.3.3. | l7 `quiz[2].explain.text`: "$X \cdot X$ is 1 for heads and 0 for tails, so $E[X \cdot X] = 0.5$. That is not $E[X]^2 = 0.25$. The product rule can fail for dependent variables, and here it does." homework-2 `items[6].feedback.byKey.product`: "You used $E[X]E[Y]$. That rule is safe only for independent variables, and here a high $X$ always comes with a low $Y$."

3. `l7-linearity.json`, `l10-scaling-and-adding.json` | l7 `screens[6].explain.text`, l7 `screens[7].widget.options[3].why`, l7 `quiz[2].feedback.byKey.product`, l10 `screens[6].explain.text`, l10 `summary.formula.note` | imprecise | minor | The product rule and the adding of variances are each said to "need" independence. Independence is sufficient, not necessary: both hold exactly when the covariance is zero. | Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y) (homework-3 `items[2]` proves it) and Cov(X, Y) = E[XY] − E[X]E[Y] (l11 `screens[8]`). The Y = X² pair is dependent and satisfies both rules (script). "Needs" teaches the converse, which l11 and review-3 `items[5]` then deny. The sufficient direction is stated correctly in l7 `summary.ideas[2]`, review-2 `items[6]` and l10 `screens[8]`. | l7 `screens[6].explain.text`: "$E[X^2] = \tfrac{91}{6} \approx 15.17$, more than $3.5^2 = 12.25$. So $E[XY] = E[X]E[Y]$ can fail without independence, and $E[g(X)] \ne g(E[X])$ in general. For a curve that bends upwards, like squaring, the average of the squares beats the square of the average." l7 `screens[7].widget.options[3].why`: "This is safe only for independent variables. With $Y = X$ for a die it gives $3.5^2$, not $\tfrac{91}{6}$." l7 `quiz[2].feedback.byKey.product`: "You multiplied $E[X]$ by itself. That is safe for independent variables, and $X$ is not independent of itself." l10 `screens[6].explain.text`: "$X + X = 2X$ has variance $4 \times 35/12 = 35/3$. Independent dice partly cancel, so $X + Y$ has only $35/6$. Variances add for independent variables; sds add only when the two move in lockstep." l10 `summary.formula.note`: "The second holds when $X$ and $Y$ are independent."

4. `l11-moving-together.json` | `summary.trap` (last sentence), `quiz[2].feedback.correct` | imprecise | serious | "Scaling either variable leaves $\rho$ unchanged." That holds only for a positive scale. A negative scale flips the sign of ρ. | ρ(X, aY + b) = sign(a) ρ(X, Y), since Cov picks up a and the sd picks up |a|. On the l11 `screens[9]` table, ρ(X, −Y) = −0.52 (script). Negative scales are central to this course: l4 shorts 250 shares, l10 `screens[3]` scales by −3 and its summary says the sd scales by |a|, and l12 shorts X. A learner who carries the rule as stated gives a short position the wrong sign of correlation. Every graded item in l11 uses a positive scale, so no key is affected. Basis: derivation; Blitzstein and Hwang 7.3. | `summary.trap`: "Correlation is not a slope, and covariances in different units cannot be compared. Scaling either variable by a positive number leaves $\rho$ unchanged; a negative scale flips its sign." `quiz[2].feedback.correct`: "A positive scale and a shift of $Y$ leave $\rho$ alone."

5. `l10-scaling-and-adding.json` | `summary.ideas[2]` (last clause) | imprecise | minor | "the sd of $n$ copies grows like $\sqrt{n}$." In this lesson "a copy" is the same variable counted again (`screens[6]`: "A copy never cancels", "A copy always agrees"), and for n such copies the sd grows like n. | sd(X + X) = 2σ, the lesson's own trap. √n is for n independent variables, as `screens[8]` states. The clause follows "For independent variables", so the intent is clear, but the word contradicts the trap screen. | `summary.ideas[2]`: "For independent variables, variances add, even for a difference; the sd of a total over $n$ independent days grows like $\sqrt{n}$."

6. `l3-up-to-a-point.json` | `screens[10].prose` (second sentence) | imprecise | minor | "On 95% of days the loss is at most this." With the definition just given, the smallest x with F(x) ≥ 0.95, the loss is at most the VaR on at least 95% of days. Here it is 96%. | F(5) = 0.96 (script). The explanation on the same screen says F "jumps straight past 0.95", and homework-1 `items[5]` tests the "at least" reading, so one word aligns the prose with both. Basis: McNeil, Frey and Embrechts, definition 2.10. | `screens[10].prose`: "The desk's 95% value at risk (VaR) is the smallest loss level $x$ with $F(x) \ge 0.95$. On at least 95% of days the loss is at most this."

7. `l6-fair-price.json` | `quiz[3].widget.options[0].text` (the key) | imprecise | minor | "It is fair: over many bets you expect to roughly break even." The average profit per bet settles at zero, but the total does not stay near zero: its typical size grows like √n. | After 10,000 fair £1 coin bets the mean absolute total is about £80 (script, 300 runs). The item's own explanation says it correctly: "only the long-run average is zero". The key as worded supports the belief that a fair game returns you to level. Basis: Feller vol. 1, III.4 (fluctuations of a fair coin game). | `quiz[3].widget.options[0].text`: "It is fair: over many bets your average profit per bet settles near £0"

8. `l10-scaling-and-adding.json` | `screens[9].explain.text` (last sentence) | imprecise | minor | "The $\sqrt{252}$ rule assumes independent days." It also treats the yearly return as the sum of the 252 daily returns. That is exact for log returns and only approximate for simple returns, and the item never says which it means. | A convention should be said once where it first matters, and this is the course's first annualising. Summed returns give 1.2% × √252 = 19.05% (script, Monte Carlo); compounded simple returns give a slightly different sd. Basis: Hull ch. 15 (volatility from log returns); Tsay 1.1. | `screens[9].explain.text`: "The yearly variance is $252 \times 0.012^2 = 0.0363$, so the sd is $0.012\sqrt{252} \approx 0.1905$. Desks quote this as 19% annual volatility. The $\sqrt{252}$ rule assumes independent days whose returns add, which is exact for log returns."

9. `l4-transforming.json` | `screens[7].explain.text` (last sentence) | imprecise | minor | "So the call pays something on only 39% of paths." Three of the nine paths pay, which is 33% of paths. Their total chance is 0.39. | The paths are not equally likely: up-up 0.09, up-flat 0.15, flat-up 0.15 (script). The lesson's own point, from l1 on, is that outcomes are weighed by chance and not counted. | `screens[7].explain.text`: "The payoffs are 0, 0, 0, 2 and 4. The three prices that pay nothing merge: $P(C = 0) = 0.61$. So the call pays something with chance only 0.39."

10. `l5-long-run-average.json` | `screens[9].explain.text` (second sentence) | imprecise | minor | "Over 250 trading days that is about £50." The expected total is exactly £50. The actual total is not "about" £50: for independent days its sd is about £22. | Var of one day is 1.96, so the sd over 250 days is 1.4 × √250 ≈ 22.1 (script). The sentence invites reading an expected value as a forecast, which l9 later warns against. | `screens[9].explain.text`: "$E[\text{P\&L}] = 0.6 + 0 - 0.4 = 0.2$, so £0.20 a day. Over 250 trading days the expected total is £50. No single day makes £0.20, just as no die shows 3.5."

## Notes that are not findings

- l12 `summary.trap` and `screens[5].explain` ("at $\rho = 1$ mixing gives no benefit", "below 1, the mix is always safer than the average") are read for weights between 0 and 1, which is the case on those screens. With a short position and unequal sds, ρ = 1 allows a riskless mix; the lesson does not claim otherwise.
- homework-3 `items[6]` part (d) asks what the sd "would be if ρ were 1". With these two-point marginals (0.6 and 0.7) ρ = 1 cannot be reached, but the part is a formula exercise on the two sds and is sound as one.
- l9 `screens[3].explain`: "a roll typically lands about 1.7 from 3.5" reads the sd as a typical distance. The mean absolute distance is 1.5; the loose reading is standard and is not graded.
- l12 `screens[7].prose` cites the Lagrange derivation in the multivariable course; `app/content/courses/multivar/l12-min-variance.json` exists and contains it.

## Overlap with the earlier reads

Read after the blind commit `946c5eda`: `docs/reviews/review-1.5.md` (random-vars section and its fix pass) and `docs/reviews/review-problems-1.5-a.md` to `-d.md` (the parts on random-vars `problems-1` to `problems-3`). Only conceptual findings on levels 1 to 3 are counted: meaning, graded keys and slip values. Voice, sentence counts, rounding instructions, restated values and difficulty labels are left out.

| Finding | This audit | Earlier read |
|---|---|---|
| l7 `screens[2]`: "nothing in the argument used independence" (wrong) | 1 | not found |
| l7 `quiz[2]`, homework-2 `items[6]`: the product rule "fails for dependent variables" (wrong) | 2 | not found |
| l7, l10: product rule and adding variances "need" independence | 3 | not found |
| l11 `summary.trap`, `quiz[2]`: scaling leaves ρ unchanged, no "positive" | 4 | not found |
| l10 `summary.ideas[2]`: "n copies" for independent variables | 5 | not found |
| l3 `screens[10]`: "on 95% of days" | 6 | not found |
| l6 `quiz[3]` key: "roughly break even" | 7 | not found |
| l10 `screens[9]`: √252 rule, returns that add | 8 | not found |
| l4 `screens[7]`: "39% of paths" | 9 | not found |
| l5 `screens[9]`: "about £50" | 10 | not found |
| l6 `screens[9]` slip `one-up`: value £40 did not match its described slip | not found (fixed before this read; the value is now £64 and checks) | review-1.5 |
| l11 `screens[2]` slip `count`: value 2 did not match its described slip | not found (fixed; now 0) | review-1.5 |
| homework-2 `items[7]`: overround called the bookmaker's edge | not found (fixed; the explain now separates 5.56% from 1/19) | review-1.5 |
| problems-3 `p-fund-hedge` part 1: key rejected "0.8%" | not found (fixed; the widget now has the % unit) | review-problems-1.5-b, 2 |
| problems-2 `p-token-draw` part 5: `carried` slip value mixed two methods | not found (fixed; 44.48 and 43.72 both check) | review-problems-1.5-c B1, -d B1 |

Counts: found by this audit only 10; by the earlier reads only 5; by both 0. Both of this audit's `wrong` findings are new: no earlier read found them. The five earlier-only findings had been fixed before this read, so a blind reader of the current files could not meet them; each fixed value was recomputed here and is correct in the ledger.

## Gates

- Validator (`node app/tools/validate.mjs`): 0 errors, 4666 warnings. `content/manifest.json` unchanged.
- `docs/reports/random-vars-L1-3-concepts.py`: 158 checks, 13 failed, exit 1 (the 13 are the findings).
- `docs/reports/fluency-random-vars-numbers.py`: 1767 checks, 0 failures, exit 0.
- `docs/reports/problems-random-vars-numbers.py`: 1333 checks over sets 1 to 5, 0 failures, exit 0.
- `docs/reports/random-vars-1-perf-numbers.py`: 109 checks, 0 failures, exit 0.
- No other number script for these levels exists in `docs/reports/`.
- Playthrough with `--local-cdn`, the 12 lessons (`--lesson`), 6 review and homework sets (`--set`), 3 problem sets (`--problems`) and the fluency set (`--fluency`): desktop 22 ok, "All passed", exit 0; `--mobile` 22 ok, "All passed", exit 0.

## Inbox

Two bullets under "Raised later (audit random-vars 1-3):" in `docs/BACKLOG-INBOX.md`: a content lint for independence stated as a necessary condition (findings 2 and 3, seven strings), and one for "scaling leaves ρ unchanged" without "positive" (finding 4).

## Fix pass

Fixer: Opus, 11 Nov 2026. Each finding was checked against the current files before it was applied. No graded key, option set, tolerance, canvas value, hidden test or code changed; one key option's text changed (finding 7) and no number changed.

| # | Status | Fixer's basis |
|---|---|---|
| 1 | fixed | Row k averages k + 3.5 only if E[Y given X = k] = 3.5 for every k; with Y = X row k is the single cell 2k with average 2k. That needs independence (mean independence) of the second die. Linearity itself is proved without it in `screens[8]` from the joint table. |
| 2 | fixed differently | l7 `quiz[2].explain`: "Independence is enough for the product rule; without it the rule can fail, as it does here." homework-2 `items[6]` `product`: "You used $E[X]E[Y]$. Independence would make that safe, but here a high $X$ always comes with a low $Y$, so the rule fails." The auditor's "safe only for independent variables" was not used: "only" restates necessity. Basis: X uniform on −1, 0, 1, Y = X², dependent, E[XY] = E[X³] = 0 = E[X]E[Y]; for the homework, Cov(X, 7 − X) = −Var(X) = −35/12 ≠ 0, so 7(3.5) − 91/6 = 28/3 ≠ 12.25. |
| 3 | fixed differently | Applied the auditor's text for l7 `screens[6]`, l10 `screens[6]` and l10 `summary.formula.note`. For l7 `screens[7]` option `product` the why reads "This holds for independent variables but can fail otherwise", and l7 `quiz[2]` `product` reads "That is safe for independent variables, and $X$ is not independent of itself" (no "only"). Basis: Var(X + Y) = Var X + Var Y + 2Cov and E[XY] − E[X]E[Y] = Cov, so both rules hold exactly when Cov = 0; independence gives Cov = 0 but not conversely. |
| 4 | fixed | Cov(X, aY + b) = a Cov(X, Y) and sd(aY + b) = |a| sd(Y), so ρ(X, aY + b) = sign(a) ρ(X, Y). The l11 item uses a = 2 > 0, so its key 0.3 stands. |
| 5 | fixed | sd(X + X) = 2σ, so n copies of one variable give nσ; √n σ is for n independent variables with sd σ (Var adds to nσ²). |
| 6 | fixed | Table: F(2) = 0.90, F(5) = 0.96, so VaR = 5 and P(L ≤ 5) = 0.96 ≥ 0.95: "at least" is exact, "95%" is not. |
| 7 | fixed | For a fair ±£1 coin game the total after n bets has sd √n (so about £100 at n = 10,000, mean absolute value √(2n/π) ≈ £80), while the average per bet has sd 1/√n → 0. Option text only; it stays the key. |
| 8 | fixed | The √252 rule takes Var(sum of 252 daily returns) = 252σ² for independent days; the yearly return is the sum of daily returns exactly for log returns, since log(1 + R_year) = Σ log(1 + r_t), and only approximately for simple returns. |
| 9 | fixed | Two-day paths with up 0.3, flat 0.5 (from the 0.09 and 0.15 path chances): 3 of 9 paths pay (up-up, up-flat, flat-up), total chance 0.09 + 0.15 + 0.15 = 0.39. "39% of paths" counts paths as equally likely. |
| 10 | fixed | E per day = 2(0.3) − 2(0.2) = 0.2, so 250 days give E = £50 exactly; Var per day = 4(0.5) − 0.04 = 1.96, sd over 250 independent days 1.4√250 ≈ £22.1, so "about £50" reads as a forecast. |

Extra search for the same class (independence stated as necessary): the level 1 to 3 files were grepped for "needs independence", "requires independence", "only for independent", "fails for dependent", "need ... independent" and every sentence containing "independen" or "dependent" was read. Every necessity phrasing found was already one of the listed strings (l7 lines on `screens[6]`, `screens[7]`, `quiz[2]`; l10 `screens[6]`, `summary.formula.note`; homework-2 `items[6]`). The remaining sentences state independence as sufficient ("for independent variables ... add", "because the dice are independent") or state that linearity needs none, which is correct. No extra fixes.

Gates after the fix pass:
- Validator: 0 errors; `content/manifest.json` unchanged.
- `docs/reports/random-vars-L1-3-concepts.py`: 158 checks, 0 failed, exit 0 (no check changed).
- `fluency-random-vars-numbers.py`, `problems-random-vars-numbers.py`, `random-vars-1-perf-numbers.py`: exit 0.
- Voice scan at 35 over the course folder: 0 explanations over three sentences, 0 sentences over 35 words.
- Playthrough with `--local-cdn` of the eight changed files (l3, l4, l5, l6, l7, l10, l11 with `--lesson`, homework-2 with `--set`): desktop all passed; `--mobile` all passed.

## Fix-pass read

Round 1, 11 Nov 2026. Fresh reader, blind to the findings above until the rows below were written. Diff read: `git diff d67c2d45~1 d67c2d45 -- app/content/courses/random-vars/` (eight files, 16 changed strings). Check script: `docs/reports/random-vars-L1-3-fixread.py` (exact fractions, 37 checks, exit 0).

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l3-up-to-a-point | `screens[10].prose` | "On at least 95% of days the loss is at most this." | correct | VaR is the smallest $x$ with $F(x) \ge 0.95$, so $P(L \le \text{VaR}) \ge 0.95$ by definition (McNeil, Frey and Embrechts, *Quantitative Risk Management*, section 2.3.2). Here $F(5) = 0.96$, so "at least" is needed and the old plain "95%" was false for this table. Key 5 unchanged: $F(2) = 0.90$, $F(5) = 0.96$. |
| 2 | l4-transforming | `screens[7].explain.text` | "the call pays something with chance only 0.39" | correct | Prices 96, 98, 100, 102, 104 with chances 0.04, 0.20, 0.37, 0.30, 0.09 (sum 1). $P(C = 0) = 0.61$, so $P(C > 0) = 0.30 + 0.09 = 0.39$. The screen is a one-step pmf, so "chance" fits where "paths" did not. |
| 3 | l5-long-run-average | `screens[9].explain.text` | "Over 250 trading days the expected total is £50." | correct | $E = 2(0.3) + 0(0.5) - 2(0.2) = 0.2$. Linearity gives $250 \times 0.2 = 50$ exactly, with no assumption on how days depend. "Expected total" is exact; the old "about £50" described the realised total, whose sd is about £22. |
| 4 | l6-fair-price | `quiz[3].widget.options[0].text` (graded key) | "It is fair: over many bets your average profit per bet settles near £0" | correct | Law of large numbers for repeated independent bets (Ross, *A First Course in Probability*, section 8.2). The average has sd $\sigma/\sqrt{n}$; the total has sd $\sigma\sqrt{n}$, so the old "roughly break even" was false of the total. Still the only correct option: "good bet" is false (no edge) and "break even on every bet" is false. Feedback and explain agree with it. |
| 5 | l7-linearity | `screens[2].explain.text` | "Here each row averaged $k + 3.5$ because the dice are independent; the next screens show the rule holds without that." | correct | The shown argument takes row $k$ as $k + Y$ over six equally likely $Y$: that is $k + E[Y \mid X = k]$, and it equals $k + 3.5$ because $Y$ is independent of $X$. So the argument did use independence. With $Y = X$ the rows are $2k$, yet the mean is still 7; the next screen but one works that case and the derivation screen proves it for any joint table. |
| 6 | l7-linearity | `screens[6].explain.text` | "So $E[XY] = E[X]E[Y]$ can fail without independence" | correct | $Y = X$ for a die: $E[X \cdot X] = 91/6 \ne 49/4$. "Can fail" is the right strength: $X \in \{-1, 0, 1\}$, $Y = X^2$ is dependent with $E[XY] = E[X]E[Y] = 0$. |
| 7 | l7-linearity | `screens[7].widget.options[3].why` | "This holds for independent variables but can fail otherwise. With $Y = X$ for a die it gives $3.5^2$, not $91/6$." | correct | Independence gives $E[XY] = E[X]E[Y]$ (Ross, section 7.2); two independent dice give $12.25$ on both sides. Counterexample numbers recomputed. Option stays unkeyed, rightly, since the question says "any random variables". |
| 8 | l7-linearity | `quiz[2].feedback.byKey.product` | "That is safe for independent variables, and $X$ is not independent of itself." | correct | Sufficiency only is claimed. A non-constant $X$ is not independent of itself: $P(X = 1, X = 1) = 0.5 \ne 0.25$. Slip value 0.25 is $E[X]^2$. |
| 9 | l7-linearity | `quiz[2].explain.text` | "Independence is enough for the product rule; without it the rule can fail, as it does here." | correct | Coin: $E[X \cdot X] = 0.5$, $E[X]E[X] = 0.25$, covariance $0.25 \ne 0$. "As it does here" is true of this item. |
| 10 | homework-2 | `items[6].feedback.byKey.product` | "Independence would make that safe, but here a high $X$ always comes with a low $Y$, so the rule fails." | correct | $Y = 7 - X$: $E[XY] = 24.5 - 91/6 = 28/3$, $E[X]E[Y] = 12.25$, covariance $-35/12$. The "so" is sound: $Y$ is a strictly decreasing function of a non-constant $X$, which forces a negative covariance. |
| 11 | l10-scaling-and-adding | `screens[6].explain.text` | "Variances add for independent variables; sds add only when the two move in lockstep." | correct | $\sigma_{X+Y}^2 = \sigma_X^2 + \sigma_Y^2 + 2\rho\sigma_X\sigma_Y$ equals $(\sigma_X + \sigma_Y)^2$ exactly when $\rho = 1$. First clause is sufficiency only. $\operatorname{Var}(2X) = 35/3$, $\operatorname{Var}(X + Y) = 35/6$. |
| 12 | l10-scaling-and-adding | `screens[9].explain.text` | "The $\sqrt{252}$ rule assumes independent days whose returns add, which is exact for log returns." | imprecise | Log returns add exactly and simple returns compound (Tsay, *Analysis of Financial Time Series*, section 1.1): true. But the rule also needs every day to have the same variance, and it needs only uncorrelated days, not independent ones. The script builds dependent, uncorrelated days whose 3-day variance is exactly 3 times one day's. See finding 1. Numbers: $252 \times 0.012^2 = 0.0363$, $0.012\sqrt{252} = 0.1905$. |
| 13 | l10-scaling-and-adding | `summary.ideas[2]` | "the sd of a total over $n$ independent days grows like $\sqrt{n}$" | correct | Independent days of one variance $\sigma^2$: $\operatorname{Var} = n\sigma^2$, sd $\sigma\sqrt{n}$. The old "$n$ copies" was false: $n$ copies are $nX$ with sd $n\sigma$ (script: three copies $9\operatorname{Var}(X)$, three independent dice $3\operatorname{Var}(X)$). Equal daily variance is implied by "grows like" and by the lesson's screens. |
| 14 | l10-scaling-and-adding | `summary.formula.note` | "The second holds when $X$ and $Y$ are independent." | correct | Sufficient condition, stated as such. The exact condition is zero covariance; the note no longer denies that. |
| 15 | l11-moving-together | `summary.trap` | "Scaling either variable by a positive number leaves $\rho$ unchanged; a negative scale flips its sign." | correct | $\rho(aX + b, Y) = \operatorname{sign}(a)\,\rho(X, Y)$ for $a \ne 0$: covariance scales by $a$, sd by $|a|$. Script: $\rho$ equal under $2Y + 0.01$ and $3Y$, negated under $-2Y + 5$. |
| 16 | l11-moving-together | `quiz[2].feedback.correct` | "A positive scale and a shift of $Y$ leave $\rho$ alone." | correct | Item is $2Y + 0.01$ with $\rho = 0.3$: $\operatorname{Cov}$ doubles, $\sigma$ doubles, shift drops out, so 0.3. Key "same" unchanged and matches. |

Rows: 16. Verdicts: 15 correct, 0 wrong, 1 imprecise, 0 misleading, 0 unverified.

### Findings

1. `l10-scaling-and-adding.json` | `screens[9].explain.text` | imprecise, minor | The last sentence reads as the full list of what the $\sqrt{252}$ rule assumes. It leaves out equal daily variance, and "assumes independent" overstates the need: uncorrelated days are enough. Real daily returns are close to uncorrelated but not independent, so the stricter wording would make a learner think the rule fails more often than it does. The same file now says "holds when" in its summary, so this line is the odd one out. | $\operatorname{Var}(\sum r_t) = \sum \operatorname{Var}(r_t) + 2\sum_{s<t}\operatorname{Cov}(r_s, r_t)$, which is $n\sigma^2$ when the covariances are zero and the variances equal. Script check "dependent but uncorrelated days". Covariance is not yet taught at this point, so the fix keeps to "independent" as a sufficient condition. | Replace the last sentence with: `The $\sqrt{252}$ rule holds for independent days of equal variance whose returns add; adding is exact for log returns.`

### Leftover in a changed file (not a changed string)

- `l3-up-to-a-point.json` | `screens[10].feedback.byKey.worst`: "VaR at 95% ignores the worst 5% of days." With the prose now saying "at least 95%", the days beyond £5k are 4% here, not 5%. Loose rather than false. Optional fix: `That is the worst loss in the model. VaR at 95% says nothing about the worst days beyond it, here 4% of days.`
