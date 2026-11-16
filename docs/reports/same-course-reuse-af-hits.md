# Same-course reuse hits of the extended check (engine pass AF part 1)

Every hit of `node tools/same-course-reuse.mjs --all --no-waivers` over the 128 problem sets, written by `node tools/reuse-hits-report.mjs`. No content was edited and no waiver added.

A line gives the set, the item id and part, the kind, the source (file and unit of the same course) and the two texts, each cut to 160 characters (the first is the problem's, the second the source's). `retold`: a sentence skeleton or a chain of steps retold (feedback, explain and why lines are read too); `rate`: a rate in a decimal or fraction against a per cent with a second number shared. Kinds listed as waived are held by `tools/same-course-waivers.json`.

## Count

| course | retold | rate | function | pair | total |
|---|---|---|---|---|---|
| analysis | 2 |  |  |  | 2 |
| complex | 2 |  |  |  | 2 |
| conditional | 6 |  |  |  | 6 |
| counting | 1 |  |  |  | 1 |
| eigen | 1 |  |  |  | 1 |
| elimination | 1 |  |  |  | 1 |
| ensembles | 7 |  |  |  | 7 |
| equations | 6 |  |  |  | 6 |
| exp-log |  | 3 |  |  | 3 |
| fin-ml | 2 |  |  |  | 2 |
| functions | 1 |  |  |  | 1 |
| integrals | 5 |  |  |  | 5 |
| least-squares | 3 |  |  |  | 3 |
| limits | 1 |  |  |  | 1 |
| limits-thm | 3 |  |  |  | 3 |
| markov | 4 |  |  |  | 4 |
| multivar |  |  | 1 |  | 1 |
| number-sense | 1 |  |  |  | 1 |
| proof | 1 |  |  |  | 1 |
| quadratics | 1 |  |  |  | 1 |
| ratio | 3 | 1 |  |  | 4 |
| regression | 2 |  |  |  | 2 |
| stat-learning | 10 |  |  |  | 10 |
| taylor | 3 |  | 3 |  | 6 |
| testing | 9 |  |  |  | 9 |
| trig | 4 |  |  | 1 | 5 |
| validation | 2 |  |  |  | 2 |
| vector-calc | 3 |  |  |  | 3 |
| vectors | 6 |  |  |  | 6 |
| **all** | **90** | **4** | **4** | **1** | **99** |

Of the 99 hits 5 are of kinds that existed before (held by `tools/same-course-waivers.json`, shown here because waivers are ignored); the other 94 are new (retold 90, rate 4).

## Hits by course

### analysis

- `analysis/problems-1.json` p-diagonal-fraction (items[2], part 1) | retold | `analysis/l5-counting-infinite-sets.json:quiz[3]` | "You copied the diagonal digits $7, 8, 5, 5, 8$." | "You copied the diagonal digits."
- `analysis/problems-4.json` p-bump-series (items[2], part 4) | retold | `analysis/l19-uniform-convergence.json:screens[9]` | "a uniform limit of continuous functions is continuous" | "limits of continuous functions are continuous."

### complex

- `complex/problems-1.json` p-four-lamps (items[2], part 1) | retold | `complex/problems-2.json:items[2]` | "Its reference angle, the acute angle to the real axis, is $\tfrac{\pi}{3}$, so $\operatorname{Arg} c = \pi - \tfrac{\pi}{3} = \tfrac{2\pi}{3}$." | "Its reference angle, the acute angle to the real axis, is $\arctan\tfrac{15}{8} \approx 1.0808$, so $\operatorname{Arg} w = \pi - 1.0808 \approx 2.0608$."
- `complex/problems-2.json` p-mesh-map (items[0], part 3) | retold | `complex/l6-complex-differentiability.json:screens[4]` | "The stretch is the modulus of $f'(z_0)$." | "The stretch is the modulus of $f'(1 + i) = 2 + 2i$."

### conditional

- `conditional/problems-2.json` p-bad-ticks (items[3], part 3) | retold | `conditional/problems-5.json:items[0]` | "After A's flag the starting chance is 0.3265." | "After one flag the chance is 0.3125."
- `conditional/problems-3.json` p-losing-week (items[1], part 3) | retold | `conditional/l16-conditional-independence.json:quiz[2]` | "The squeeze explains the loss." | "the crash explains the loss"
- `conditional/problems-4.json` p-two-strategies (items[1], part 2) | retold | `conditional/homework-4.json:items[0]` | "That is the chance B wins." | "That is the chance staying wins."
- `conditional/problems-4.json` p-dated-coins (items[3], part 1) | retold | `conditional/l19-bertrands-box.json:screens[5]` | "What is the chance the other coin is gold?" | "Now what is the chance the other coin is gold?"
- `conditional/problems-5.json` p-warning-screen (items[0], part 3) | retold | `conditional/problems-2.json:items[3]` | "After one flag the chance is 0.3125." | "After A's flag the starting chance is 0.3265."
- `conditional/problems-5.json` p-doubling-desk (items[3], part 1) | retold | `conditional/review-5.json:items[5]` | "In a round a trader stakes £1, doubles after each loss, and stops at the first win or after five losses in a row." | "You stake £1, double after each loss, and stop at the first win or after three losses in a row."

### counting

- `counting/problems-3.json` p-grain-merchant (items[2], part 4) | retold | `counting/l13-portfolio-vector.json:quiz[2]` | "Divide the dot product by both magnitudes, then take the inverse cosine." | "Divide the dot product by both magnitudes, then take the inverse cosine."

### eigen

- `eigen/problems-3.json` p-branch-sales (items[0], part 1) | retold | `eigen/homework-3.json:items[1]` | "Find the off-diagonal entry of $\mathbf{A}^T\mathbf{A}$." | "The off-diagonal entry is $(2,1,1)\cdot(1,2,-1) = 2 + 2 - 1$."

### elimination

- `elimination/problems-2.json` p-burning-ethanol (items[0], part 3) | retold | `elimination/l6-inputs-to-zero.json:quiz[0]` | "Type the special solution as $(x_1, x_2, x_3, x_4)$." | "What is the special solution?"

### ensembles

- `ensembles/problems-1.json` p-spoof-alerts (items[0], part 1) | retold | `ensembles/l2-good-split.json:screens[0]` | "What is the weighted Gini of the two sides?" | "What is the weighted Gini of the two sides?"
- `ensembles/problems-1.json` p-opening-gaps (items[3], part 2) | retold | `ensembles/l2-good-split.json:screens[11]` | "0.267 is the weighted impurity left after the split." | "0.253 is the weighted impurity left after the split."
- `ensembles/problems-2.json` p-ipo-forest (items[1], part 1) | retold | `ensembles/l6-random-forest.json:screens[5]` | "$\tfrac{1}{10}$ is the chance with one feature on offer." | "$1/8$ is the chance with one feature on offer."
- `ensembles/problems-3.json` p-callable-bonds (items[1], part 1) | retold | `ensembles/homework-3.json:items[4]` | "Boosting works on the log-odds scale." | "Boosting works on the log-odds scale."
- `ensembles/problems-3.json` p-callable-bonds (items[1], part 2) | retold | `ensembles/review-3.json:items[4]` | "0.25 is the bond's current probability, not how far it is from the outcome." | "That is the current probability, not how far it is from the outcome."
- `ensembles/problems-3.json` p-callable-bonds (items[1], part 5) | retold | `ensembles/l9-fixing-mistakes.json:screens[8]` | "Summing on the log-odds scale keeps $p$ between 0 and 1 however many trees follow." | "Summing on the log-odds scale keeps every $p$ between 0 and 1, however many trees we add."
- `ensembles/problems-3.json` p-futures-study (items[2], part 1) | retold | `ensembles/l12-trees-on-returns.json:screens[3]` | "Start from the first test row and step back past the gap of 2." | "Start from the first test row and step back past the gap."

### equations

- `equations/problems-3.json` p-bakery-stock (items[0], part 2) | retold | `equations/l11-one-twist.json:quiz[3]` | "$-18h \ge -180$, and dividing by $-18$ reverses the sign:" | "Dividing by $-3$ reverses the sign:"
- `equations/problems-3.json` p-bakery-stock (items[0], part 2) | retold | `equations/l12-trapped.json:screens[8]` | "$-18h \ge -180$, and dividing by $-18$ reverses the sign:" | "Dividing by $-450$ reverses the sign:"
- `equations/problems-3.json` p-bakery-stock (items[0], part 2) | retold | `equations/review-3.json:items[1]` | "$-18h \ge -180$, and dividing by $-18$ reverses the sign:" | "$8 \div -2 = -4$, and dividing by $-2$ reverses the sign."
- `equations/problems-3.json` p-van-value (items[2], part 3) | retold | `equations/l11-one-twist.json:quiz[3]` | "$-2400t > -18000$, and dividing by $-2400$ reverses the sign:" | "Dividing by $-3$ reverses the sign:"
- `equations/problems-3.json` p-van-value (items[2], part 3) | retold | `equations/l12-trapped.json:screens[8]` | "$-2400t > -18000$, and dividing by $-2400$ reverses the sign:" | "Dividing by $-450$ reverses the sign:"
- `equations/problems-3.json` p-van-value (items[2], part 3) | retold | `equations/review-3.json:items[1]` | "$-2400t > -18000$, and dividing by $-2400$ reverses the sign:" | "$8 \div -2 = -4$, and dividing by $-2$ reverses the sign."

### exp-log

- `exp-log/problems-1.json` p-laptop-value (items[1], part 2) | rate | `exp-log/problems-2.json:items[2]` | "$1200 \times 0.75^2 = 1200 \times 0.5625 = 675$, so £675." | "$\tfrac{50{,}000}{32{,}000} = 1.5625$, a gain of 56.25%." (the rate 0.5625 here and 56.25% there, with 1.25 in both)
- `exp-log/problems-1.json` p-rare-coin (items[2], part 1) | rate | `exp-log/problems-2.json:items[2]` | "0.5625 is the rise as a part of £640." | "$\tfrac{50{,}000}{32{,}000} = 1.5625$, a gain of 56.25%." (the rate 0.5625 here and 56.25% there, with 1.5625 in both)
- `exp-log/problems-2.json` p-drawdown-recovery (items[2], part 2) | rate | `exp-log/problems-1.json:items[2]` | "$\tfrac{50{,}000}{32{,}000} = 1.5625$, a gain of 56.25%." | "0.5625 is the rise as a part of £640." (the rate 56.25% here and 0.5625 there, with 1.5625 in both)

### fin-ml

- `fin-ml/problems-3.json` p-power-spread-cap (items[3], part 1) | retold | `fin-ml/l9-probability-to-position.json:screens[3]` | "What fraction of capital does Kelly stake at $p = 0.70$?" | "What fraction does Kelly stake?"
- `fin-ml/problems-3.json` p-power-spread-cap (items[3], part 1) | retold | `fin-ml/review-3.json:items[1]` | "What fraction of capital does Kelly stake at $p = 0.70$?" | "What fraction does Kelly stake?"

### functions

- `functions/problems-4.json` p-photo-mount (items[0], part 1) | retold | `functions/l16-machine-after-machine.json:screens[2]` | "In $m(e(12))$ the inner machine $e$ acts first." | "In $f(g(4))$ the inner machine, $g$, acts first."

### integrals

- `integrals/problems-1.json` p-subscriptions (items[1], part 4) | retold | `integrals/homework-1.json:items[4]` | "Reversing the limits flips the sign:" | "Reversing the limits flips the sign:"
- `integrals/problems-1.json` p-subscriptions (items[1], part 4) | retold | `integrals/l3-signed-area.json:quiz[1]` | "Reversing the limits flips the sign:" | "Reversing the limits flips the sign."
- `integrals/problems-1.json` p-subscriptions (items[1], part 4) | retold | `integrals/l7-evaluating.json:screens[5]` | "Swapping the limits flips the sign." | "Swapping the limits flips the sign:"
- `integrals/problems-2.json` p-area-function (items[0], part 3) | retold | `integrals/l6-working-backwards.json:quiz[0]` | "Raise each power by one and divide by the new power:" | "Raise the power by one and divide by the new power."
- `integrals/problems-2.json` p-line-and-parabola (items[2], part 2) | retold | `integrals/l8-between-curves.json:screens[4]` | "Integrate top minus bottom between the two crossings." | "Integrate top minus bottom, $8 - 2x^2$, between the crossings."

### least-squares

- `least-squares/problems-2.json` p-dye-mix (items[3], part 3) | retold | `least-squares/homework-1.json:items[5]` | "Each entry is a column of $\mathbf{Q}$ dotted with $\mathbf{b}$." | "Each $x_i$ is column $i$ of $\mathbf{Q}$ dotted with $(0, 3, 3)$."
- `least-squares/problems-2.json` p-dye-mix (items[3], part 3) | retold | `least-squares/l10-normal-equations.json:screens[0]` | "Each entry is a column of $\mathbf{Q}$ dotted with $\mathbf{b}$." | "Each entry is a column of $\mathbf{A}$ dotted with $\mathbf{e}$."
- `least-squares/problems-2.json` p-dye-mix (items[3], part 3) | retold | `least-squares/review-1.json:items[2]` | "Each entry is a column of $\mathbf{Q}$ dotted with $\mathbf{b}$." | "Each $c_i$ is a column of $\mathbf{Q}$ dotted with $(5, 0)$."

### limits

- `limits/problems-5.json` p-camera-pan (items[0], part 1) | retold | `limits/l19-running-backwards.json:screens[7]` | "The slope of $\arctan u$ is $\dfrac{1}{1+u^2}$, times the slope of $u = \dfrac{x}{30}$." | "The slope of $\arctan u$ is $\dfrac{1}{1 + u^2}$, times the slope of $u$."

### limits-thm

- `limits-thm/problems-1.json` p-dropped-ticks (items[0], part 5) | retold | `limits-thm/l2-first-success.json:screens[7]` | "At $k = 5$ the mean wait is about 42 minutes." | "At $p = 0.2$ the mean wait is 5 minutes."
- `limits-thm/problems-1.json` p-settlement-checks (items[3], part 2) | retold | `limits-thm/review-1.json:items[7]` | "That is the binomial variance $50 \times 0.03 \times 0.97$." | "Multiply the binomial variance by $\tfrac{N - n}{N - 1}$."
- `limits-thm/problems-2.json` p-digital-share (items[1], part 1) | retold | `limits-thm/l8-lognormal.json:screens[2]` | "The median passes straight through the exponential:" | "The median passes straight through the exponential."

### markov

- `markov/problems-1.json` p-carry-pause (items[3], part 1) | retold | `markov/problems-2.json:items[3]` | "You divided by the chance of staying, 0.7." | "You divided 0.25 by 0.6, the chance of staying."
- `markov/problems-3.json` p-barrier-note (items[1], part 1) | retold | `markov/l8-which-end.json:screens[7]` | "That is $\binom{12}{5}$, the paths ending at $-2$." | "That is $h_1$, the chance of ending at 3."
- `markov/problems-5.json` p-signal-trial (items[1], part 2) | retold | `markov/review-5.json:items[1]` | "Which base $r$ makes $r^{S_n}$ a martingale?" | "Which base $r$ makes $r^{S_n}$ a martingale?"
- `markov/problems-5.json` p-capped-close (items[3], part 2) | retold | `markov/l20-when-stopping-fails.json:quiz[0]` | "A bounded stopping time keeps a fair game fair, so $0.625 \times £1{,}000 + 0.375\,m = 0$." | "A bounded stopping time keeps a fair game fair."

### multivar

- `multivar/problems-5.json` p-triangle-field (items[2], part 2) | function | `limits-thm/l17-smallest-and-largest.json:screens[6]` | -x^4 + 3x^3 - 3x^2 + x (the same polynomial in another course)

### number-sense

- `number-sense/problems-3.json` p-comet-probe (items[2], part 2) | retold | `number-sense/l13-estimate-first.json:quiz[0]` | "The first significant figure of 8,760 is the 8 thousands." | "The first significant figure is the 5."

### proof

- `proof/problems-3.json` p-even-test-contra (items[3], part 1) | retold | `proof/problems-2.json:items[0]` | "If $n$ is not a multiple of 3, then $n^2 + 2$ is a multiple of 3." | "Not every multiple of 6 is a multiple of 4:"

### quadratics

- `quadratics/problems-3.json` p-bike-hire (items[1], part 4) | retold | `quadratics/review-3.json:items[9]` | "The cost raised the best price by £4, half of £8." | "The cost raised the best price by £1.00, half of £2.00."

### ratio

- `ratio/problems-1.json` p-pension-split (items[0], part 1) | rate | `ratio/l1-out-of-a-hundred.json:screens[9]` | "$\tfrac{3}{8} = 3 \div 8 = 0.375$, which is 37.5%." | "Put the lines in order to turn $\tfrac{3}{8}$ into a percentage." (the rate 37.5% here and 3/8 there, with 37.5 in both)
- `ratio/problems-3.json` p-print-run (items[1], part 1) | retold | `ratio/l11-direct-or-inverse.json:quiz[1]` | "You scaled the time up with the presses." | "You scaled the time up with the servers."
- `ratio/problems-3.json` p-coffee-suppliers (items[2], part 3) | retold | `ratio/l13-currencies.json:screens[0]` | "Each pound buys €1.20, so divide:" | "Each pound buys €1.16, so multiply."
- `ratio/problems-3.json` p-coffee-suppliers (items[2], part 3) | retold | `ratio/review-3.json:items[1]` | "Each pound buys €1.20, so divide:" | "Each pound buys €1.15, so multiply."

### regression

- `regression/problems-2.json` p-grocer-beta (items[3], part 1) | retold | `regression/problems-3.json:items[2]` | "What is the residual standard deviation $s$, in % a month?" | "What is the residual standard deviation $s$, in %?"
- `regression/problems-3.json` p-overlap-signal (items[2], part 1) | retold | `regression/problems-2.json:items[3]` | "What is the residual standard deviation $s$, in %?" | "What is the residual standard deviation $s$, in % a month?"

### stat-learning

- `stat-learning/problems-1.json` p-ferry-passengers (items[0], part 5) | retold | `stat-learning/l2-training-error-lies.json:screens[7]` | "You chose by training error." | "You chose by training error."
- `stat-learning/problems-1.json` p-ferry-passengers (items[0], part 5) | retold | `stat-learning/review-4.json:items[5]` | "You chose by training error." | "You chose by training fit."
- `stat-learning/problems-1.json` p-loaves-k (items[1], part 3) | retold | `stat-learning/l3-bias-variance.json:quiz[1]` | "That is bias squared plus variance alone." | "That is bias² plus variance alone:"
- `stat-learning/problems-1.json` p-broker-clients (items[2], part 4) | retold | `stat-learning/problems-2.json:items[0]` | "Forecast 5.5 for each held-out client, square the misses, then average." | "Forecast 40 for each held-out day, square the misses, then average."
- `stat-learning/problems-1.json` p-heat-demand (items[3], part 1) | retold | `stat-learning/l2-training-error-lies.json:quiz[1]` | "Degree 2 has the lowest test MSE, 1.80." | "B has the lowest test MSE."
- `stat-learning/problems-2.json` p-futures-lasso (items[2], part 1) | retold | `stat-learning/review-2.json:items[3]` | "A coefficient survives when its size is above $\alpha = 0.15$." | "A coefficient survives when its size is above $\alpha = 0.15$."
- `stat-learning/problems-2.json` p-futures-lasso (items[2], part 2) | retold | `stat-learning/l8-setting-to-zero.json:screens[1]` | "The model is empty once $\alpha$ reaches the largest one." | "The model is empty once $\alpha$ passes the largest one."
- `stat-learning/problems-2.json` p-futures-lasso (items[2], part 4) | retold | `stat-learning/l9-scale-first.json:screens[2]` | "Subtract the training mean, then divide by the training standard deviation." | "Subtract the training mean, then divide by the training standard deviation."
- `stat-learning/problems-2.json` p-built-ridge (items[3], part 1) | retold | `stat-learning/homework-2.json:items[4]` | "We built a market with three uncorrelated z-scored features, true coefficients 0.5, 0.2 and 0, and noise variance 2.0." | "two uncorrelated z-scored features, true coefficients 0.4 and 0, noise variance 4."
- `stat-learning/problems-4.json` p-renewals (items[3], part 2) | retold | `stat-learning/l19-which-learner.json:quiz[1]` | "A tie goes to the simpler, more explainable model." | "A tie goes to the simpler model."

### taylor

- `taylor/problems-1.json` p-newton-cubic (items[1], part 3) | retold | `taylor/l8-convexity.json:quiz[3]` | "A curve that bends up lies above its tangent." | "The curve bends up, so it lies above its tangents."
- `taylor/problems-1.json` p-loss-limit (items[2], part 1) | retold | `taylor/problems-2.json:items[2]` | "A bond is at par only when its coupon rate equals its yield." | "A bond is at par only when its coupon rate equals its yield."
- `taylor/problems-3.json` p-doubling-coefficients (items[0], part 2) | retold | `taylor/homework-3.json:items[7]` | "The ratio itself tends to 2." | "The ratio tends to $\tfrac{|x + 2|}{3}$, so $R = 3$ about $x = -2$."
- `taylor/problems-3.json` p-tail-bound (items[2], part 1) | function | `taylor/l7-standard-series.json:screens[9]` | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial, factorised or not, with the letter renamed)
- `taylor/problems-3.json` p-tail-bound (items[2], part 1) | function | `exams/topic-1.3.json:items[10]` | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial in another course)
- `taylor/problems-3.json` p-big-gain (items[3], part 2) | function | `taylor/l7-standard-series.json:screens[5]` | -0.25x^4 + 0.333333x^3 - 0.5x^2 + x (the same polynomial, factorised or not, with the letter renamed)

### testing

- `testing/problems-1.json` p-cereal-boxes (items[0], part 1) | retold | `testing/l1-could-be-luck.json:screens[6]` | "A null must fix one value of $\mu$, so that surprise can be measured." | "$H_0$ must fix $p$ at one value so that surprise can be measured."
- `testing/problems-1.json` p-cereal-boxes (items[0], part 5) | retold | `testing/l3-p-value.json:screens[4]` | "Failing to reject is not proof." | "Failing to reject is not accepting."
- `testing/problems-1.json` p-phone-battery (items[1], part 2) | retold | `testing/problems-2.json:items[2]` | "The curve has 7 degrees of freedom, but the standard error uses $\sqrt n = \sqrt 8$." | "The curve has 8 degrees of freedom, but the standard error uses $\sqrt 9$."
- `testing/problems-1.json` p-pizza-delivery (items[3], part 3) | retold | `testing/l15-sharpness-of-the-peak.json:quiz[0]` | "The standard error is $\tfrac{9.6}{\sqrt{16}} = 2.4$ minutes." | "$nI(\hat\lambda) = \tfrac{25}{4} = 6.25$, so the standard error is $\tfrac{1}{\sqrt{6.25}} = 0.4$ trades a minute."
- `testing/problems-1.json` p-pizza-delivery (items[3], part 4) | retold | `testing/l3-p-value.json:screens[4]` | "Failing to reject is not proof." | "Failing to reject is not accepting."
- `testing/problems-3.json` p-fund-managers (items[1], part 2) | retold | `testing/l3-p-value.json:screens[8]` | "Take the upper tail beyond $t = 2.7$." | "Double the upper tail beyond $|z|$."
- `testing/problems-3.json` p-fund-managers (items[1], part 3) | retold | `testing/homework-3.json:items[2]` | "With p = 0.0035, the largest rank under its bar is 5." | "rank 5 is the largest rank under its bar."
- `testing/problems-3.json` p-fund-managers (items[1], part 3) | retold | `testing/l10-correcting.json:quiz[0]` | "With p = 0.0035, the largest rank under its bar is 5." | "rank 3 is the largest rank under its bar."
- `testing/problems-4.json` p-bakery-loaves (items[2], part 5) | retold | `testing/l17-ratio-of-likelihoods.json:quiz[0]` | "Wilks counts the parameters the null removes:" | "Count the parameters the null removes."

### trig

- `trig/problems-2.json` p-water-wheel (items[0], part 4) | retold | `trig/l11-every-angle.json:screens[10]` | "$180^\circ - 128.9^\circ = 51.1^\circ$, the mirror image in the vertical axis." | "$\sin(180^\circ - x) = \sin x$, the mirror in the vertical axis, so $150^\circ$ is another"
- `trig/problems-2.json` p-two-buoys (items[1]) | pair | `trig/l9-stretching-a-wave.json:screens[4]` | consecutive part keys 2.5 and 5.5 sit together in "So $y$ runs from 2.5 to 5.5."
- `trig/problems-2.json` p-two-buoys (items[1], part 1) | retold | `trig/l9-stretching-a-wave.json:screens[8]` | "One wave is drawn while the angle runs from 0 to $2\pi$." | "One wave of $\sin(bx)$ is drawn while the angle $bx$ runs from 0 to $2\pi$."
- `trig/problems-2.json` p-observation-wheel (items[2], part 1) | retold | `trig/problems-3.json:items[2]` | "The amplitude is the swing either side of the hub:" | "The amplitude is the swing either side of the midline:"
- `trig/problems-3.json` p-daylight-model (items[2], part 1) | retold | `trig/problems-2.json:items[2]` | "The amplitude is the swing either side of the midline:" | "The amplitude is the swing either side of the hub:"

### validation

- `validation/problems-1.json` p-arrears-grid (items[2], part 2) | retold | `validation/l4-nested.json:screens[11]` | "By what share of the nested score does the best flatter the model?" | "By what percentage of the nested score does the grid’s best number flatter the model?"
- `validation/problems-2.json` p-forward-label (items[1], part 3) | retold | `validation/homework-2.json:items[2]` | "How many rows train the model for that middle block?" | "How many rows train the model for that block?"

### vector-calc

- `vector-calc/problems-3.json` p-open-tank (items[1], part 2) | retold | `vector-calc/l11-divergence-theorem.json:screens[1]` | "Use the divergence theorem:" | "This is the **divergence theorem**."
- `vector-calc/problems-3.json` p-open-tank (items[1], part 2) | retold | `vector-calc/l12-stokes.json:screens[10]` | "Use the divergence theorem:" | "The divergence theorem agrees:"
- `vector-calc/problems-3.json` p-open-tank (items[1], part 2) | retold | `vector-calc/review-3.json:items[3]` | "Use the divergence theorem:" | "Use the divergence theorem."

### vectors

- `vectors/problems-1.json` p-charging-robot (items[0], part 3) | retold | `vectors/l3-lengths-angles.json:screens[4]` | "Divide the dot product by the two lengths, then take the inverse cosine." | "Divide the dot product by both lengths, then take the inverse cosine."
- `vectors/problems-2.json` p-italic-letters (items[0], part 3) | retold | `vectors/problems-3.json:items[2]` | "Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{S}$." | "Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{M}$."
- `vectors/problems-2.json` p-italic-letters (items[0], part 3) | retold | `vectors/l8-identity-transpose.json:screens[4]` | "Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{S}$." | "Each entry is a row of $\mathbf{B}^T$ dotted with a column of $\mathbf{A}^T$."
- `vectors/problems-3.json` p-goat-feed (items[0], part 3) | retold | `vectors/l10-undoing.json:screens[6]` | "You swapped and negated but did not divide by $\det\mathbf{A} = 0.1$." | "You swapped and negated correctly but did not divide by $ad - bc$."
- `vectors/problems-3.json` p-colour-sensor (items[2], part 1) | retold | `vectors/problems-2.json:items[0]` | "Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{M}$." | "Each entry of a product is a row of $\mathbf{D}$ dotted with a column of $\mathbf{S}$."
- `vectors/problems-3.json` p-engraver-dial (items[3], part 1) | retold | `vectors/problems-2.json:items[0]` | "You multiplied matching entries." | "You multiplied matching entries."

