# Problem sets 2.2, arma levels 1 to 3: second-reader findings

Scope: `app/content/courses/arma/problems-1.json`, `-2`, `-3`: 12 problems, 51 parts (44 numeric, 7 choice), 105 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Reader, Tail, Session AE additions). Pattern: `review-problems-analysis-1-3.md`.

Method. The author's script was run first. Lessons l1 to l12, `review-1` to `-3`, `homework-1` to `-3`, and the time-series items of `exams/topic-2.2.json` (items 0, 3, 5, 6, 8, 11, 14, 15, 16, 22) and `exams/stage-2.json` (part 2, items 0 to 5) were then read in full as learner-facing text, for what each level teaches and for reused stories, numbers, sentences and chains of steps. Every part was solved from its text and again in `docs/reports/problems-arma-numbers-read.py`, which imports nothing from the author's script. Second routes: direct damped sums in place of $1/(1 - \phi^2)$, brute search for every "first" or "largest" whole number, the 2 by 2 Yule-Walker system solved as a matrix, the ARMA forecast and impulse path run as a recursion, statsmodels psi weights and AR(2) autocorrelations, SciPy tails, and seeded simulation (the Dickey-Fuller points at 365 days, the four rates of p-ppp-screen on 360 months, the weekly sampling of p-peg-fridays, the smoothed fund, the inventory fan). Every `wrong` value was rebuilt from its slip and held against the key band and the other slip bands. Each replacement text below was applied to a scratch copy of the content and run through `fresh-check.mjs --file`, `grade-all.mjs --file` and the voice scan; the worktree content was not edited.

Severities: `wrong`, `misleading`, `reuse` (line-level or number-level, with exact replacement), `re-author` (a whole problem walks course or exam items; no replacement text, only what it must not walk), `continuity`, `voice`.

## Tool results

| check | result |
|---|---|
| author's script | `problems-arma-numbers.py` 577 of 577, exit 0 |
| reader's script | `problems-arma-numbers-read.py` 592 checks, exit 0, 11 FINDING lines (findings 1, 2, 7, 10, 11, 13, 14, 16) |
| validator | 0 errors, 4571 warnings, none on the three files; `manifest.json` restored |
| `grade-all.mjs --file`, three sets | 0 failures (18, 16, 17 widgets) |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file`, three sets | 0 hits; 4, 5 and 8 advisories, read |
| scratch copy with every replacement below | `fresh-check` 0 hits (4, 6, 7 advisories, none new on a changed line); `grade-all` 0 failures; voice 0 and 0 |
| browser | not run (reader rule) |

Result. All 44 typed keys and 7 choice keys agree with mine, as do all 105 `wrong` values and every number printed in prose, feedback and `explain`. No learner is told a false result. The four simulated rates of p-ppp-screen hold (5.2%, 20.0%, 46.2%, 88.8% on 30,000 paths against the stated 5, 20, 45, 89). Two faults are in p-airport-anomaly (data that cannot come from one sample; a band that refuses the value its own feedback leads to). The rest is reuse. The checker's 0 hits hide three problems that walk course or exam items part by part, two number sets taken from `exams/stage-2.json`, which the author did not read, and a group of feedback lines retold from lessons, reviews and homework.

## Verdict per problem (closest lesson, review, homework and exam items)

| problem | closest items | verdict |
|---|---|---|
| p-airport-anomaly | l3 screens[1] ($t = \hat\gamma/\text{se}$); homework-1 items[2] ($t$, 1% point, implied $\hat\phi$); review-1 items[4] (AR(1) variance); stage-2 parts[1].items[1] (AR(1) long-run sd); topic-2.2 items[5] (variance 7.84, chance likeness to 7.86) | clean chain: sums to slope, test, variance, tail is in no item. One slip line retold (finding 3). |
| p-ppp-screen | l3 screens[3], [7], [8]; review-1 items[6] ("power bought with false alarms"); l4 screens[9], [11]; topic-2.2 items[0] | clean chain (rates turned into shares of rejections). Part 5 lines retold (finding 4). |
| p-gdp-trend | l4 screens[4]; review-1 items[5]; homework-1 items[1], [4]; topic-2.2 items[11] | clean. One slip line retold (finding 5). |
| p-gold-drift | l1 screens[1], [3]; review-1 items[0]; l4 quiz[0]; no exam item | clean. `explain` of part 1 retold (finding 6). |
| p-etf-flows | l5 screens[2]; review-2 items[2] ($Q(2)$ against 5.99); l8 screens[2] and l9 screens[8] ($\hat\rho_2$ against $\hat\rho_1^2$); stage-2 parts[1].items[4] ($\hat\rho_1 = 0.45$, $0.2025$) and items[2] | reuse: number pair of the exam item, and one recipe line (finding 7). |
| p-vol-index-order | l8 screens[3], [4], [7], [8], quiz[3]; review-2 items[0], [1], [7]; homework-2 items[0], [7]; l6 screens[1], [6]; topic-2.2 items[3], [14] | **re-author** (finding 8). |
| p-peg-fridays | l7 screens[9], [11]; homework-2 items[5]; stage-2 parts[1].items[1]; topic-2.2 items[5] ($\sigma = 2$, $\sigma^2 = 4$, one shared number) | clean: weekly sampling is in no item. Two slip lines retold (finding 9), one restatement missing (finding 10). |
| p-freight-ar2 | stage-2 parts[1].items[2] and items[4]; l6 screens[3], [11]; l8 screens[2]; homework-2 items[3] | **re-author** (finding 11). |
| p-smoothed-fund | l9 screens[2], [9], [10]; homework-3 items[3]; l11 screens[7]; l9 quiz[3]; stage-2 parts[1].items[5] | clean: unequal weights, the conditional width and the 12-month sum are new. One `explain` retold (finding 12). |
| p-inflation-arma | l11 screens[2], [7]; review-3 items[5]; homework-3 items[8]; stage-2 parts[1].items[5] (MA coefficient 0.35) | reuse: the exam item's coefficient on the same two steps (finding 13). |
| p-inventory-half-life | l7 screens[11] ($\hat\phi = 0.915$); l12 screens[0], [2], [3], quiz[2]; l11 screens[11]; review-3 items[4] to [6]; homework-3 items[7]; topic-2.2 items[15] | **re-author** (finding 14). |
| p-dual-listing | homework-3 items[2] (BIC gap); topic-2.2 items[14]; l10 screens[1], [2], quiz[2]; homework-3 items[8]; p-peg-fridays ($0.88^5$) | reuse: part 1 lines, l10 screens[2] lines, and a number set shared across sets (findings 15, 16). The path from 1.13 and its half-life are new. |

## A. `problems-1`

1. `misleading` | `arma/problems-1.json` | `p-airport-anomaly` | `items[0].prose`, `parts[0]` to `parts[2]` | the sums cannot come from the sample that parts 4 and 5 describe.
   $S_{xx} = 1{,}250$ over 364 pairs is a sample variance of 3.43 °C². Part 4 gives the same series a variance of 7.86 °C², from $s^2 = 3.2$ and $\hat\phi = 0.77$. A variance of 3.43 beside a shock variance of 3.2 would mean $\phi$ near 0.26. A learner who checks $S_{xx}/364$ against part 4 finds a factor of 2.3.
   Fix: $S_{xx} = 2{,}880$, $S_{xy} = -662.4$ ($2{,}880/364 = 7.91$; $\hat\gamma$ still $-0.23$; $s^2/S_{xx} = \tfrac{1}{900}$, se $\tfrac{1}{30}$, $t = -6.90$, which also matches $\hat\gamma\sqrt{n}/\sqrt{1 - \hat\phi^2} = -6.88$). None of 2,880, 662.4, $-6.90$, $-207$, $-9.2286$ is in the course.
   - `prose`: "... The regressor's sum of squares is $S_{xx} = 2{,}880$, its cross products with $\Delta x_t$ sum to $S_{xy} = -662.4$, and the residual variance is $s^2 = 3.2$."
   - `parts[0]`: key and both `wrong` values unchanged ($-0.23$; flip $2{,}880/-662.4 = -4.3478$; sign 0.23). `feedback.correct`: "Correct. $\hat\gamma = -662.4/2{,}880 = -0.23$, so $\hat\phi = 1 + \hat\gamma = 0.77$." `explain.text`: "With $x_{t-1}$ as the regressor, the slope is $S_{xy}/S_{xx} = -662.4/2{,}880 = -0.23$. Since $\gamma = \phi - 1$, the anomaly keeps $\hat\phi = 0.77$ of yesterday's value."
   - `parts[1]`: `answer` $-6.9$ (tol 0.006). `wrong`: `no-sqrt` $-207.0$ (tol 0.05), `s-not-s2` $-9.2286$ (tol 0.01), `sign` 6.9 (tol 0.006). `feedback.correct`: "Correct. The standard error is $\sqrt{3.2/2{,}880} = \tfrac{1}{30}$, so $t = -0.23 \times 30 = -6.90$." `byKey.no-sqrt`: "You divided by $s^2/S_{xx} = \tfrac{1}{900}$ itself. The standard error is its square root, $\tfrac{1}{30}$." `explain.text`: "The standard error of the slope is $\sqrt{3.2/2{,}880} = \tfrac{1}{30} = 0.0333$. Dividing, $t = -0.23 \times 30 = -6.90$. Part 3 decides which critical value this has to beat." (`byKey.s-not-s2` and `byKey.sign` stand.)
   - `parts[2]`: replace $-4.55$ by $-6.90$ in all six places (question, three option texts, the `too-far` `why`, `explain.text`). The verdict is unchanged: $-6.90$ is below $-3.45$.

2. `misleading` | `arma/problems-1.json` | `p-airport-anomaly` | `items[0].parts[4].widget.tol`, `wrong[0].tol`, `feedback.correct`, `explain.text` | a band refuses the answer its own feedback leads to.
   The feedback prints "$5/2.804 = 1.78$ sds, and $P(Z > 1.78) = 0.037$". But $P(Z > 1.78) = 0.0375$, which a learner with a table rounds to 0.038. The key band is $0.03726 \pm 0.0006$, so 0.038 is refused with the generic line. The `shock-sd` slip, 0.00259, typed to 3 places as asked is 0.003, outside its own band of ±0.0003, so it never reaches its line.
   Fix: key `tol.abs` 0.0008 (takes 0.037 and 0.038; `no-square` at 0.09 stays far off). `wrong` `shock-sd` `tol.abs` 0.0005. `feedback.correct`: "Correct. 5 °C is $5/2.804 = 1.783$ sds, and $P(Z > 1.783) = 0.037$." `explain.text`: "At an sd of 2.80 °C, 5 °C is 1.783 sds above the mean. The normal tail beyond is 0.037, about 14 days a year. With the shock's sd alone the desk would expect about one."

3. `reuse` | `arma/problems-1.json` | `p-airport-anomaly` | `items[0].parts[3].feedback.byKey.no-square`.
   Set: "You divided by $1 - \phi = 0.23$. The variance formula needs $1 - \phi^2$." stage-2 parts[1].items[1]: "You divided by $1 - \phi$. The variance divides by $1 - \phi^2$, then take the root." (also review-1 items[4] and l2 quiz[1]: "You used $1 - \phi$ instead of $1 - \phi^2$.")
   Fix: "That is $3.2/0.23$. The denominator is $1 - 0.77^2 = 0.4071$, not $1 - 0.77$."

4. `reuse` | `arma/problems-1.json` | `p-ppp-screen` | `items[1].parts[4].widget.options[0].text`, `options[1].why`.
   Set, `over`: "It over-differences them: the level they return to, which the desk wanted to trade, is thrown away"; `no-harm` `why`: "The result is stationary, but the level the series returns to is lost. A reversion trade bets on that level." l4 screens[9] option: "Differencing a stationary series adds a negative lag-1 correlation and throws away its level". l4 screens[11]: "Differencing the spread throws away the very distance from the mean you want to trade", "Its distance from the mean is what a pairs trade bets on."
   Fix, `over`: "It removes what the screen was for: a series of changes no longer shows how far a rate sits from its long-run value". Fix, `no-harm` `why`: "Stationary, yes, but the changes say nothing about the gap to the long-run value. That gap was the reason for the screen."

5. `reuse` | `arma/problems-1.json` | `p-gdp-trend` | `items[2].parts[0].feedback.byKey.same`.
   Set: "You assumed differencing keeps the noise's sd. Growth holds two noise terms, so its variance doubles." l4 screens[4] option `why`: "Here each change holds two shocks, $\varepsilon_t - \varepsilon_{t-1}$, not one."
   Fix: "You kept 3.5%. A quarter's growth is the slope plus $u_t - u_{t-1}$, and the variances of $u_t$ and $u_{t-1}$ add."

6. `reuse` | `arma/problems-1.json` | `p-gold-drift` | `items[3].parts[0].explain.text`.
   Set: "Adding $\ln p_t - \ln p_{t-1}$ over every day cancels all the middle closes and leaves $\ln(1{,}820/1{,}450) = 0.2273$. 501 closes give 500 returns, so the mean is ..." review-1 items[0]: "The middle price cancels: log returns telescope." l1 summary: "$n$ prices give $n - 1$ returns, and the returns add up to $\ln(p_n/p_0)$."
   Fix: "The 500 daily log returns sum to $\ln 1{,}820 - \ln 1{,}450 = 0.2273$, whatever the closes in between. Divide by 500 returns, not 501 closes, to get 4.55 bp."

## B. `problems-2`

7. `reuse` | `arma/problems-2.json` | `p-etf-flows` | `items[0]`, the number set, and `parts[1].feedback.generic`.
   stage-2 parts[1].items[4]: "sample autocorrelations $\hat\rho_1 = 0.45$ and $\hat\rho_2 = 0.05$", with "$0.05 - 0.2025$" and "$-0.1525/0.7975$" in its lines. The problem has $\hat\rho_1 = 0.45$, holds $0.45^2 = 0.2025$ against $\hat\rho_2$, and uses $1 - 0.2025 = 0.7975$ in part 4. The recipe line of part 2, "Weight $0.45^2$ by $1/199$ and $0.24^2$ by $1/198$, add, then scale by $200 \times 202$", retells review-2 items[2] "Divide each square by $n - k$, add, and multiply by $n(n + 2) = 2600$" and stage-2 parts[1].items[2] "Square each autocorrelation, divide by $n - k$, add, then multiply by $n(n + 2)$".
   Fix: cross products 79,200, so $\hat\rho_1 = 0.44$ (0.44 occurs in the course only as the 20-day band of l5 quiz[0]; 0.1936, 51.06, 725.76 and 26.94 do not occur).
   - `prose`: "$\sum (x_t - \bar x)(x_{t-1} - \bar x) = 79{,}200$".
   - `parts[0]`: `answer` 0.44; `flip` 2.2727. `correct`: "Correct. $79{,}200/180{,}000 = 0.44$." `byKey.flip`: "That is 180,000/79,200, upside down. An autocorrelation is at most 1, so the cross products sit in the numerator." `explain`: "... $79{,}200/180{,}000 = 0.44$. A week of strong inflows tends to follow another."
   - `parts[1]`: question "Using $\hat\rho_1 = 0.44$ and $\hat\rho_2 = 0.24$, ...". `answer` 51.0564; `box-pierce` 50.24; `no-n-k` 10148.48. `correct`: "Correct. $200 \times 202 \times (0.1936/199 + 0.0576/198) = 51.06$, far above 5.99, the 5% point of $\chi^2_2$." `generic`: "Not quite. $Q(2)$ has one term for each lag, $\hat\rho_k^2/(200 - k)$, and $200 \times 202$ multiplies their total." `explain`: "The squares are 0.1936 and 0.0576, divided by 199 and 198 and scaled by $200 \times 202 = 40{,}400$. $Q = 51.06$ rejects white noise with room to spare. The flows have memory worth modelling."
   - `parts[2]`: question "An AR(1) with $\phi = 0.44$, from part 1, ...". `answer` 0.1936; `double` 0.88; `sample` 0.24. `correct`: "Correct. $\rho_2 = \phi^2 = 0.44^2 = 0.1936$, close to the sample's 0.24." `byKey.double`: "You doubled $\phi$. Two lags apart the AR(1) multiplies by $\phi$ twice: $0.44^2$." `explain`: "An AR(1) multiplies by $\phi$ for each week of separation, so two weeks apart it gives $0.44^2 = 0.1936$. The sample's 0.24 is 0.05 away, small next to the band of ±0.139 for 200 weeks."
   - `parts[3]`: question "Fit the AR(1) with $\phi = 0.44$. ...". `answer` 26.9399; `no-square` 22.4499; `series-sd` 30; `variance` 725.76. `correct`: "Correct. $\sigma^2 = 900 \times (1 - 0.1936) = 725.76$, so $\sigma = 26.94$ £m." `byKey.no-square`: "That is $\sqrt{900 \times 0.56}$. The factor is $1 - 0.44^2 = 0.8064$, not $1 - 0.44$." `explain`: "From $\gamma_0 = \sigma^2/(1 - \phi^2)$, $\sigma^2 = 900 \times 0.8064 = 725.76$ and $\sigma = 26.94$ £m. Knowing last week's flow cuts the sd of the uncertainty from 30 to 26.94, about 10%."

8. `re-author` | `arma/problems-2.json` | `p-vol-index-order` | `items[1]`, whole item.
   Each part is a course or exam item in other numbers, and the chain is the story of l8 screens[7].
   - Part 1 is review-2 items[0]. Set: "That is one sd, $1/\sqrt{680}$. The band is 1.96 sds." and "You divided by 680. The band shrinks like $1/\sqrt n$." Review: "You gave one sd, $1/\sqrt{250}$. The band is 1.96 sds." and "You divided by 250. The band shrinks like $1/\sqrt n$."
   - Part 2 is review-2 items[1] and l8 screens[4]. Set: lag 6 at $-0.092$, option "AR(6): the last bar outside the band is at lag 6", "barely clears the band after three empty lags. That is how a stray bar looks." Review: option "An AR(6), since lag 6 is outside the band", "Lag 6 at 0.092 is a stray bar", "A real lag-6 effect would not leave lags 2 to 5 empty." The same lag, the same size, the same distractor. topic-2.2 items[3] has two real bars and one stray ("One chance exit in twenty bars is expected").
   - Part 3 is homework-2 items[0] and l6 screens[1] with "exactly one" for "at least one"; its `none` and `no-count` lines are the homework's `none` and `one`.
   - Part 4 is homework-3 items[2] (BIC gap from two log-likelihoods) and l8 quiz[3]. Set: "BIC charges $\ln 680 = 6.52$ a parameter, not 2." Quiz: "BIC charges $\ln 500 \approx 6.2$ per parameter against AIC's 2". The prose sentence "Here $k$ counts the constant, the AR terms and $\sigma^2$" is topic-2.2 items[14] "Here $k$ counts the constant, the ARMA coefficients and $\sigma^2$". The close, "The PACF proposes 2 and leaves lag 6 to the criteria", is l8 screens[8] "the PACF proposes and AIC, BIC and the residuals decide".
   - Part 4 does not use part 3's value, so the chain also breaks there.
   Must not walk: l8 screens[3], [4], [7], [8], quiz[3]; review-2 items[0], [1], [7]; homework-2 items[0], [7]; l6 screens[1], [6]; homework-3 items[2]; topic-2.2 items[3], [14]. The new problem still has to draw on l6 or l8 with one other lesson of the level.

9. `reuse` | `arma/problems-2.json` | `p-peg-fridays` | `items[2].parts[0].feedback.byKey.no-square`, `parts[1].feedback.byKey.linear`.
   `no-square`, set: "You divided by $1 - \phi = 0.12$. The variance needs $1 - \phi^2$." stage-2 parts[1].items[1]: "You divided by $1 - \phi$. The variance divides by $1 - \phi^2$". Fix: "That is $4/0.12$. The denominator is $1 - 0.88^2 = 0.2256$, not $1 - 0.88$."
   `linear`, set: "You took 0.12 off five times. The memory shrinks by a factor of 0.88 each day." l7 screens[11]: "You took off a fixed amount each day. The gap shrinks by a factor, so use $\hat\phi^5$." Fix: "That is $1 - 5 \times 0.12$. Each day multiplies what remains by 0.88, so five days give $0.88^5$."

10. `continuity` | `arma/problems-2.json` | `p-peg-fridays` | `items[2].parts[2].question`.
   "... with $\phi_w = 0.5277$ from part 2 and the variance from part 1." The variance is named, not restated; a slip in part 1 sinks part 3.
   Fix: "The weekly series is itself an AR(1) with $\phi_w = 0.5277$ from part 2 and the variance 17.73 bp² from part 1. What is the variance of its weekly shock, in bp²? Give a decimal to 2 places." ($17.73 \times (1 - 0.5277^2) = 12.79$, inside the band.)

11. `re-author` | `arma/problems-2.json` | `p-freight-ar2` | `items[3]`, whole item.
   The problem walks two neighbouring items of `exams/stage-2.json` in order.
   - Parts 1 and 2 are stage-2 parts[1].items[2]: "An AR(1) fit on 250 days leaves residual autocorrelations ... What is the Ljung-Box statistic", then the verdict by "three lags less one fitted coefficient". Here an AR(1) on 400 days leaves five residual autocorrelations, the same statistic is asked, and the verdict turns on five lags less one fitted coefficient. Set: "That is Box and Pierce's $n\sum\hat\rho_k^2$. Ljung-Box weights each term by $(n + 2)/(n - k)$." Exam: "You used $n\sum\hat\rho_k^2$, the Box-Pierce form. Ljung-Box weights each lag by $(n + 2)/(n - k)$." (p-etf-flows part 2 carries the same line; reword it there too if finding 7 is applied without it: "That is $200 \times (0.1936 + 0.0576)$, with no $1/(n - k)$ weights and $n$ in place of $n + 2$.") l6 screens[3] is the same five-lag count against 11.07.
   - Parts 3 and 4 are stage-2 parts[1].items[4]. Exam: "An AR(2) fitted by Yule-Walker solves $\rho_1 = \phi_1 + \phi_2\rho_1$ and $\rho_2 = \phi_1\rho_1 + \phi_2$. What is $\hat\phi_2$, which is also the lag-2 partial autocorrelation?", slips "You gave $\hat\rho_2$" and "You stopped at $\rho_2 - \rho_1^2$. Divide by $1 - \rho_1^2$.", then "$\hat\phi_1 \approx 0.5361$". Set: "Its coefficients solve $\rho_1 = b_1 + b_2\rho_1$ and $\rho_2 = b_1\rho_1 + b_2$ ... what is $b_2$, the PACF at lag 2?", slips "That is $\hat\rho_2$ itself" and "You stopped at $\rho_2 - \rho_1^2$. Divide by $1 - \rho_1^2 = 0.8236$.", then $b_1$.
   Must not walk: stage-2 parts[1].items[2], [4]; l6 screens[3], [11]; review-2 items[2]; l8 screens[2]; homework-2 items[3]. With finding 8 the set loses its two l8 problems, so one of the two new problems has to carry l8, and no second hand-computed $Q$ is needed beside p-etf-flows part 2.

## C. `problems-3`

12. `reuse` | `arma/problems-3.json` | `p-smoothed-fund` | `items[0].parts[1].explain.text`.
   Set: "... so the covariance is $0.24\sigma^2$. Over $0.52\sigma^2$ that is 0.4615. Months two apart have disjoint windows, so the ACF stops after lag 1: an MA(1)." homework-3 items[3]: "Windows two days apart share 3 of their 5 days, so the covariance is $3\sigma^2$ over a variance of $5\sigma^2$ ... The ACF cuts off after lag 4: an MA(4)". l9 screens[9]: "Two days apart there is no shared shock, so the ACF is exactly 0 from lag 2".
   Fix: "Each reported return holds $r_{t-1}$ once, with weight 0.4 in one month and 0.6 in the month before. So the covariance is $0.4 \times 0.6\,\sigma^2 = 0.24\sigma^2$, and $0.24/0.52 = 0.4615$. Reported returns two months apart hold no true month in common, so their autocorrelation is 0."

13. `reuse` | `arma/problems-3.json` | `p-inflation-arma` | `items[1]`, the coefficient $\theta$ and parts 2 to 4.
   stage-2 parts[1].items[5]: "$r_t = 0.0008 + \varepsilon_t + 0.35\varepsilon_{t-1}$", part 1 "the mean plus 0.35 times today's shock", part 2 "Today's shock does not reach two days ahead." The problem's MA coefficient is $-0.35$, part 2 adds $0.35 \times 0.12$ of today's shock, and part 3 drops it ("This month's shock enters next month only, then it is gone"). The AR part and part 4 are the problem's own.
   Fix: $\theta = -0.20$ (0.472, 0.222, 0.4320 and 0.1820 do not occur in the course or the two exams; $\theta = -0.30$ was tried and gives 0.46 and 0.21, the pair of l9 screens[8]).
   - `prose`: "$\theta = -0.20$".
   - `parts[1]`: `answer` 0.472; `no-ma` 0.496; `theta-sign` 0.52. `correct`: "Correct. $0.25 + 0.82 \times 0.30 - 0.20 \times 0.12 = 0.25 + 0.246 - 0.024 = 0.472$." `byKey.no-ma`: "You left out the MA term, $\theta\hat\varepsilon_n = -0.024$." `byKey.theta-sign`: "You added $0.20 \times 0.12$. With $\theta = -0.20$ the MA term is negative." `explain`: "The AR part shrinks today's gap of 0.30 to 0.246. The MA part adds $\theta\hat\varepsilon_n = -0.024$, taking back some of this month's surprise. The forecast is 0.472."
   - `parts[2]`: question "Using the forecast 0.472 from part 2, what is the forecast two months ahead? Give a decimal to 4 places." `answer` 0.43204; `ma-again` 0.40804; `from-xn` 0.45172. `correct`: "Correct. $0.25 + 0.82 \times (0.472 - 0.25) = 0.25 + 0.1820 = 0.4320$." `byKey.from-xn`: "... so start from 0.472." `explain`: "... Only the AR part acts: the gap 0.222 shrinks to 0.1820, giving 0.4320. Every later month repeats that step."
   - `parts[3]`: question "... That distance is 0.222 one month ahead. ..." Key 9, `no-ma` 10, `off-by-one` 8, all unchanged. `correct`: "Correct. The gap is $0.222 \times 0.82^{h-1}$: 0.0553 at $h = 8$ and 0.0454 at $h = 9$." `generic`: "Not quite. Solve $0.222 \times 0.82^{h-1} < 0.05$ for $h$." `byKey.no-ma`: "... The MA term already cut the first step to 0.222." `byKey.off-by-one`: "At $h = 8$ the gap is $0.222 \times 0.82^7 = 0.0553$, just above 0.05." `explain`: "Solve $0.222 \times 0.82^{h-1} < 0.05$: $h - 1 > \ln 0.225/\ln 0.82 = 7.51$, so $h = 9$ months. An AR(1) from today's gap of 0.30 would say 10, because it ignores the MA term's pull."

14. `re-author` | `arma/problems-3.json` | `p-inventory-half-life` | `items[2]`, whole item.
   - $\phi = 0.915$ is the fitted $\hat\phi$ of l7 screens[11] ("`ARIMA` gives ... $\hat\phi = 0.915$. Today the spread is £2.00 above its mean. What is the expected gap above the mean in 5 days?", $2 \times 0.915^5$). Part 2 is that screen with 30 for 2 and 15 for 5.
   - Part 1 is l12 screens[2]. Set: "You took 8.5% of the first position off each minute. The decay is geometric: 8.5% of what is left." Lesson: "You took 20% of the starting gap off each day. The decay is geometric: 20% of what is left." The `approx` line is l12 screens[3] and screens[5] `approx`.
   - Part 3 is l11 screens[11], with its three slips in the same roles. Lesson: "You used the random walk's $\sigma\sqrt{h}$. The spread reverts, so old shocks fade.", "That is one day ahead.", "That is the limit as $h \to \infty$ ... so the half-width is a little smaller", and "half-width 11.70, close to the limit of 12.16". Set: "That is a random walk's $1.96\sigma\sqrt{15}$ ... an early shock has decayed", "That is the one-minute half-width.", "That is the limit far ahead. At 15 minutes a little of the sum is still missing.", and "The half-width is 11.25, close to the long-run ±11.66". topic-2.2 items[15] has the same pair of slips ("You used the one-day half-width", "You scaled by $\sqrt{3}$, as a random walk would").
   - Part 4 is l12 quiz[2] (days to a fraction, counted in half-lives) and l7 screens[0]. Its question says "Using the half-life from part 1" with no value (a continuity fault on its own).
   - The `one-step` slip of part 3, $1.96 \times 2.4 = 4.704$, is the key of p-smoothed-fund part 3 in the same set ($1.96 \times 0.6 \times 4\%$).
   Must not walk: l7 screens[0], [11]; l12 screens[0], [2], [3], [4], quiz[2]; l11 screens[5], [11]; review-3 items[4], [5], [6]; homework-3 items[7]; topic-2.2 items[15], [16]. No $\phi = 0.915$, and no unknown part with sd 2.4. The new problem still has to draw on l12 and one other lesson.

15. `reuse` | `arma/problems-3.json` | `p-dual-listing` | `items[3].parts[0].feedback.generic`, `byKey.aic`, `explain.text`.
   The part is homework-3 items[2] in other numbers, lines included. Homework: "Compute $k\ln n - 2\ell$ for both, with $k = 4$ and $k = 6$.", "That is the AIC gap, in favour of ARMA(2, 2). BIC charges $\ln 1000 = 6.91$ per parameter.", "Two parameters cost 13.82 on BIC and buy 12." Set: "Work out $k\ln n - 2\ell$ for both, with $k = 3$ and $k = 4$.", "That is the AIC gap, $21.0 - 2$. On BIC the extra parameter costs $\ln 750 = 6.62$.", "The MA term costs $\ln 750 = 6.62$ on BIC and buys 21.0 points of $-2\ell$."
   Fix, `generic`: "Not quite. The models differ by one parameter and by 21.0 points of $-2\ell$. Weigh $\ln 750$ for the parameter against the 21.0." Fix, `byKey.aic`: "That is $21.0 - 2$: you took 2 for the MA term, as AIC does. BIC takes $\ln 750 = 6.62$." Fix, `explain.text`: "The two values of $-2\ell$ are 2920.4 and 2899.4, a gap of 21.0 in the ARMA(1, 1)'s favour. Its fourth parameter adds $\ln 750 = 6.62$ to its BIC. So its BIC is 14.38 lower, and the MA term earns its place."

16. `reuse` | `arma/problems-3.json` | `p-dual-listing` | `items[3].parts[2]` (numbers and question), `parts[3].explain.text`, `parts[4].widget.options[1].why`.
   Numbers: $\phi = 0.88$, five steps and $0.88^5 = 0.5277$ are the setting and key of p-peg-fridays part 2 in `problems-2`; here 0.527732 is the `ar` slip of part 3 and its `explain` prints "$0.88^5 = 0.5277$". Lines: "From tomorrow on the MA part is spent, so each day keeps 0.88 of the day before" is l10 screens[2] "After lag 1 the shock term is spent, so each lag is a fixed multiple of the one before". "The decay runs at the AR rate, but from 1.13 instead of 1" and "Where the decay starts depends on $\theta$ too" are l10 screens[2] "The MA term only changes where the decay starts: $\rho_1 = 0.819$ instead of 0.7".
   Fix: ask part 3 at 7 days (6 days would put $0.88^5$ in the key's working).
   - `parts[2].question`: "After day 1 only the AR term acts on the effect, so each day keeps 0.88 of the day before. Using 1.13 from part 2, what is the effect after 7 days, in bp? Give a decimal to 4 places." `answer` 0.524777; `ar` 0.408676; `off-by-one` 0.461803 (tolerances unchanged). `correct`: "Correct. $1.13 \times 0.88^6 = 1.13 \times 0.4644 = 0.5248$ bp." `generic`: "Not quite. Day 1 carries 1.13; days 2 to 7 each multiply by 0.88." `byKey.ar`: "That is $0.88^7$, the AR(1) path. The MA term lifts day 1 to 1.13." `byKey.off-by-one`: "You applied 0.88 seven times after day 1. Day 1 already holds 1.13, so six more steps reach day 7." `explain`: "Day 1 carries 1.13 and days 2 to 7 multiply by 0.88, six steps in all: $1.13 \times 0.88^6 = 0.5248$ bp. An AR(1) with the same $\phi$ would leave $0.88^7 = 0.4087$."
   - `parts[3].explain.text`: "$0.88^{h-1} = 0.5/1.13 = 0.4425$, so $h - 1 = 6.38$ and $h = 7.38$ days. That is the AR(1)'s 5.42 days, one day for the MA step, and 0.96 days to work off the extra 0.13." ($\ln 1.13/\ln(1/0.88) = 0.96$.)
   - `parts[4]` `phi-only` `why`: "$\phi$ fixes how much each day keeps. The time to reach half the shock also depends on day 1's effect, which $\theta$ raises to 1.13."
   The effect after 7 days, 0.5248, is still above one half, which agrees with part 4's 7.38 days.

## Notes, not findings

- p-ppp-screen states 45% for walks under the normal point, the rate l3 screens[3] teaches for 250 days (45.25%). On 360 months my simulation gives 46.2%. The prose says the rates come from a seeded simulation, and 45% is inside a seed's range; the fresh-check advisory on 1.645 and 45 is a taught constant.
- p-freight-ar2 shares a freight index with `regression/problems-2` `p-freight-summary` (another course, another task); p-airport-anomaly shares "temperature anomaly" with `least-squares/problems-3` (a regressor there). Neither is in the arma course or its exams.
- Coverage holds today (each lesson in at least one problem, each problem on two lessons). After the three re-authors, l8 and l12 need care: l8 is drawn on only by the two level-2 problems marked re-author, and l12 by p-dual-listing and the level-3 one.
- Voice: nothing to report.

## Engine

1. The `retold` kind missed two-sentence slip lines that differ only in one number: "You divided by 680. The band shrinks like $1/\sqrt n$." against review-2 items[0], and "The decay is geometric: 8.5% of what is left." against l12 screens[2].
2. Same-course reuse does not read the exams of the course's topic. Three findings here (7, 11, 13) are pairings with `exams/stage-2.json` part 2, and two more lines pair with `exams/topic-2.2.json`.
3. A single fitted parameter shared with the same task ($\hat\phi = 0.915$, start times $\phi^h$) and a power shared between two sets of one course ($0.88^5 = 0.5277$ in `problems-2` and `problems-3`) raise nothing: the first is one number, and the second sits in a `wrong` value and an `explain`.

Inbox bullets: `docs/BACKLOG-INBOX.md`, `Raised later (review problems arma):`.
