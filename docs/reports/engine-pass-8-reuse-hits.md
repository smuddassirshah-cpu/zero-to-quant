# Same-course reuse hits added by engine pass 8 B

Every hit of `node tools/same-course-reuse.mjs --all --no-waivers --exam-errors` over the 149 problem sets, less the hits that the older checker already reported (same set, item, kind and source file), written by `node tools/reuse-hits-report.mjs`. No content was edited and no waiver added.

A block gives the set, the item id and part, the kind, the source (file and unit; an **exam** source also names the exam item), a tag, and every matched pair, the problem's text first and the source's second. Tags: `[exam-reuse]` the source is an item of a topic, stage or mock exam that carries the course's skills; `[slip-line]` the hit rests on an identical short slip line ("You ...", numbers and maths masked) alone. `retold`: sentences or a chain of steps retold; `rate`: a rate in a decimal or fraction against a per cent; a pair printed as `[w, n]` has the weight of the match and its count of informative common words (99: an identical slip line).

## Count

| course | retold | text | exam | slip-line | total |
|---|---|---|---|---|---|
| coint | 3 |  |  | 3 | 3 |
| complex | 14 |  |  | 14 | 14 |
| conditional | 5 |  |  | 5 | 5 |
| counting | 7 |  |  | 7 | 7 |
| elimination | 3 |  |  | 3 | 3 |
| ensembles | 1 |  |  | 1 | 1 |
| equations | 5 |  |  | 5 | 5 |
| estimation | 5 |  | 1 | 5 | 5 |
| exp-log | 3 |  |  | 3 | 3 |
| fin-ml |  | 1 | 1 |  | 1 |
| functions | 12 |  | 2 | 12 | 12 |
| garch | 8 |  |  | 8 | 8 |
| integrals | 4 |  |  | 4 | 4 |
| limits | 7 |  |  | 7 | 7 |
| limits-thm | 6 |  |  | 6 | 6 |
| linear-maps | 2 |  |  | 2 | 2 |
| multivar | 7 |  | 1 | 6 | 7 |
| number-sense | 14 |  |  | 14 | 14 |
| odes | 1 |  |  | 1 | 1 |
| quadratics | 1 |  |  | 1 | 1 |
| random-vars | 6 |  |  | 6 | 6 |
| ratio | 4 |  |  | 4 | 4 |
| regression | 3 | 1 | 1 | 3 | 4 |
| series | 2 |  |  | 2 | 2 |
| stat-learning | 18 |  | 1 | 18 | 18 |
| taylor | 5 |  |  | 5 | 5 |
| testing | 21 |  | 5 | 21 | 21 |
| trig | 9 |  |  | 9 | 9 |
| vector-calc | 4 |  |  | 4 | 4 |
| vectors | 6 |  |  | 6 | 6 |
| **all** | **186** | **2** | **12** | **185** | **188** |

## Hits by course

### coint

- `coint/problems-1.json` p-paper-mill-multiple (items[0], part 1) | retold | `coint/l1-two-walks.json:quiz[0]` | [slip-line]
  - "You multiplied by 0.15 instead of $0.15^2$." <- "You multiplied by $r^2 = 0.25$ instead of $r = 0.5$." [10, 99]
- `coint/problems-1.json` p-paper-mill-multiple (items[0], part 1) | retold | `coint/review-1.json:items[0]` | [slip-line]
  - "You multiplied by 0.15 instead of $0.15^2$." <- "You multiplied by $r^2 = 0.09$ instead of $r = 0.3$." [10, 99]
- `coint/problems-1.json` p-screen-real-share (items[3], part 1) | retold | `coint/l2-not-correlation.json:screens[11]` | [slip-line]
  - "You applied 0.40 to all 1,200 pairs." <- "You applied 5% to all 124,750 pairs." [10, 99]

### complex

- `complex/problems-1.json` p-parallel-branches (items[0], part 1) | retold | `complex/l1-square-root-of-minus-one.json:screens[3]` | [slip-line]
  - "You multiplied real by real and imaginary by imaginary only." <- "You multiplied real by real and imaginary by imaginary only." [10, 99]
- `complex/problems-1.json` p-parallel-branches (items[0], part 3) | retold | `complex/l2-points-in-a-plane.json:screens[1]` | [slip-line]
  - "You added the two parts." <- "You added the two parts." [10, 99]
- `complex/problems-1.json` p-parallel-branches (items[0], part 5) | retold | `complex/problems-2.json:items[0]` | [slip-line]
  - "You took the real part over the imaginary part." <- "You took the real part over the imaginary part." [10, 99]
- `complex/problems-1.json` p-turning-frames (items[1], part 2) | retold | `complex/l2-points-in-a-plane.json:screens[1]` | [slip-line]
  - "You added the two parts." <- "You added the two parts." [10, 99]
- `complex/problems-1.json` p-turning-frames (items[1], part 3) | retold | `complex/problems-2.json:items[0]` | [slip-line]
  - "You took the real part over the imaginary part." <- "You took the real part over the imaginary part." [10, 99]
- `complex/problems-1.json` p-neutral-wire (items[3], part 1) | retold | `complex/l8-exp-and-log.json:screens[2]` | [slip-line]
  - "You swapped cosine and sine." <- "You swapped cosine and sine:" [10, 99]
- `complex/problems-1.json` p-neutral-wire (items[3], part 1) | retold | `complex/review-1.json:items[5]` | [slip-line]
  - "You swapped cosine and sine." <- "You swapped cosine and sine." [10, 99]
- `complex/problems-1.json` p-neutral-wire (items[3], part 4) | retold | `complex/l2-points-in-a-plane.json:screens[1]` | [slip-line]
  - "You added the two parts." <- "You added the two parts." [10, 99]
- `complex/problems-1.json` p-neutral-wire (items[3], part 5) | retold | `complex/problems-2.json:items[0]` | [slip-line]
  - "You took the real part over the imaginary part." <- "You took the real part over the imaginary part." [10, 99]
- `complex/problems-2.json` p-mesh-map (items[0], part 4) | retold | `complex/problems-1.json:items[0]` | [slip-line]
  - "You took the real part over the imaginary part." <- "You took the real part over the imaginary part." [10, 99]
- `complex/problems-2.json` p-plate-heat (items[1], part 5) | retold | `complex/l2-points-in-a-plane.json:quiz[0]` | [slip-line]
  - "You added the sizes of the parts." <- "You added the sizes of the parts." [10, 99]
- `complex/problems-2.json` p-plate-heat (items[1], part 5) | retold | `complex/review-1.json:items[1]` | [slip-line]
  - "You added the sizes of the parts." <- "You added the sizes of the parts." [10, 99]
  - "You added the sizes of the parts. The modulus is $\sqrt{5^2 + 2^2}$." <- "You added the sizes of the parts. The modulus is $\sqrt{(-2)^2 + 2^2}$." [10, 99]
- `complex/problems-2.json` p-log-branches (items[2], part 1) | retold | `complex/l2-points-in-a-plane.json:quiz[0]` | [slip-line]
  - "You added the sizes of the parts." <- "You added the sizes of the parts." [10, 99]
- `complex/problems-2.json` p-log-branches (items[2], part 1) | retold | `complex/review-1.json:items[1]` | [slip-line]
  - "You added the sizes of the parts." <- "You added the sizes of the parts." [10, 99]
  - "You added the sizes of the parts. The modulus is $\sqrt{8^2 + 15^2}$." <- "You added the sizes of the parts. The modulus is $\sqrt{(-2)^2 + 2^2}$." [10, 99]

### conditional

- `conditional/problems-2.json` p-downgrade-news (items[1], part 2) | retold | `conditional/l10-odds-form.json:screens[4]` | [slip-line]
  - "You multiplied the probability 0.15 by 3." <- "You multiplied the probability 0.2 by 6." [10, 99]
  - "The ratio multiplies the odds, $\tfrac{3}{17}$." <- "The ratio multiplies the old odds of 1 to 4." [3.5, 3]
- `conditional/problems-2.json` p-downgrade-news (items[1], part 2) | retold | `conditional/l11-updating-twice.json:quiz[0]` | [slip-line]
  - "You multiplied the probability 0.15 by 3." <- "You multiplied the probability 0.2 by 6." [10, 99]
- `conditional/problems-2.json` p-downgrade-news (items[1], part 2) | retold | `conditional/l26-trading-signal.json:screens[3]` | [slip-line]
  - "You multiplied the probability 0.15 by 3." <- "You multiplied the probability 0.55 by 1.5." [10, 99]
- `conditional/problems-2.json` p-downgrade-news (items[1], part 2) | retold | `conditional/review-2.json:items[4]` | [slip-line]
  - "You multiplied the probability 0.15 by 3." <- "You multiplied the probability 0.25 by 4." [10, 99]
  - "The ratio multiplies the odds, $\tfrac{3}{17}$." <- "The ratio multiplies the old odds of 1 to 3." [3.5, 3]
- `conditional/problems-3.json` p-gap-days (items[0], part 1) | retold | `conditional/l1-what-changes.json:screens[8]` | [slip-line]
  - "You divided by the 260 up days." <- "You divided by the 120 up days." [10, 99]

### counting

- `counting/problems-1.json` p-ice-cream-van (items[3], part 1) | retold | `counting/problems-2.json:items[3]` | [slip-line]
  - "You multiplied 14 by 3. Choosing 3 of 14 is $\binom{14}{3}$." <- "You multiplied 11 by 4. Choosing 4 of 11 is $\binom{11}{4}$." [10, 99]
- `counting/problems-2.json` p-leisure-centre (items[1], part 1) | retold | `counting/l7-what-you-do-not-want.json:screens[6]` | [slip-line]
  - "You took the 20 away twice." <- "You took the 9 away twice." [10, 99]
- `counting/problems-2.json` p-quiz-team (items[3], part 1) | retold | `counting/problems-1.json:items[3]` | [slip-line]
  - "You multiplied 11 by 4. Choosing 4 of 11 is $\binom{11}{4}$." <- "You multiplied 14 by 3. Choosing 3 of 14 is $\binom{14}{3}$." [10, 99]
- `counting/problems-3.json` p-orienteering (items[0], part 1) | retold | `counting/l12-proving-with-vectors.json:screens[4]` | [slip-line]
  - "You took start minus end." <- "You took start minus end." [10, 99]
- `counting/problems-3.json` p-orienteering (items[0], part 1) | retold | `counting/l9-arrows.json:screens[6]` | [slip-line]
  - "You took start minus end." <- "You took start minus end." [10, 99]
- `counting/problems-3.json` p-orienteering (items[0], part 1) | retold | `counting/review-3.json:items[0]` | [slip-line]
  - "You took start minus end." <- "You took start minus end:" [10, 99]
- `counting/problems-3.json` p-power-line (items[1], part 3) | retold | `counting/l11-how-long.json:screens[0]` | [slip-line]
  - "You subtracted the components." <- "You subtracted the components." [10, 99]

### elimination

- `elimination/problems-1.json` p-three-lines (items[1], part 1) | retold | `elimination/l3-factorisation.json:screens[4]` | [slip-line]
  - "You put the multipliers above the diagonal." <- "You put the multipliers above the diagonal." [10, 99]
- `elimination/problems-3.json` p-vinyl-cutter (items[0], part 1) | retold | `elimination/l9-area-scale.json:quiz[0]` | [slip-line]
  - "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." <- "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$." [10, 99]
  - "What is the area of the cut logo?" <- "What is the area of the image?" [1.8, 1]
- `elimination/problems-3.json` p-vinyl-cutter (items[0], part 1) | retold | `elimination/review-3.json:items[0]` | [slip-line]
  - "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." <- "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$." [10, 99]
  - "What is the area of the cut logo?" <- "What is the area of the image?" [1.8, 1]

### ensembles

- `ensembles/problems-2.json` p-ipo-forest (items[1], part 1) | retold | `ensembles/l6-random-forest.json:screens[10]` | [slip-line]
  - "You used $\sqrt{10} = 3.16$ before rounding down." <- "You used $\sqrt{30} = 5.48$ before rounding down." [10, 99]
  - "scikit-learn offers 3 features." <- "scikit-learn uses 5 features." [3, 3]

### equations

- `equations/problems-1.json` p-family-tickets (items[0], part 1) | retold | `equations/l4-putting-brackets-back.json:screens[0]` | [slip-line]
  - "You took $a$ away from 5." <- "You took 4 away from 12." [10, 99]
- `equations/problems-1.json` p-number-trick (items[2], part 2) | retold | `equations/l13-changing-the-subject.json:screens[5]` | [slip-line]
  - "You divided only $2n$ by 2." <- "You divided only $C$ by 2." [10, 99]
- `equations/problems-2.json` p-climbing-wall (items[0], part 1) | retold | `equations/l1-letters-for-numbers.json:screens[9]` | [slip-line]
  - "You swapped the two charges." <- "You swapped the two charges." [10, 99]
- `equations/problems-4.json` p-remote-cars (items[2], part 3) | retold | `equations/l15-swapping-in.json:quiz[2]` | [slip-line]
  - "You squared 81. Here $t^2 = 81$, so undo the square instead." <- "You squared 4. Here $x^2 = 4$, so undo the square instead." [10, 99]
- `equations/problems-4.json` p-salt-solutions (items[3], part 2) | retold | `equations/homework-1.json:items[5]` | [slip-line]
  - "You multiplied 50 by 0.25. Divide instead: $50 \div 0.25 = 200$." <- "You multiplied 120 by 0.04. Divide instead: $120 \div 0.04 = 3000$." [10, 99]

### estimation

- `estimation/problems-1.json` p-route-delays (items[1], part 3) | retold | `estimation/homework-1.json:items[4]` | [slip-line]
  - "You added the bias, 1.5, without squaring it." <- "You added the bias, −0.4, without squaring it." [10, 99]
- `estimation/problems-1.json` p-reference-mass (items[3], part 1) | retold | `estimation/problems-2.json:items[2]` | [slip-line]
  - "You dropped the minus signs." <- "You dropped the minus signs." [10, 99]
- `estimation/problems-2.json` p-currency-vol (items[2], part 1) | retold | `estimation/problems-1.json:items[3]` | [slip-line]
  - "You dropped the minus signs." <- "You dropped the minus signs." [10, 99]
- `estimation/problems-2.json` p-currency-vol (items[2], part 3) | retold | `estimation/l8-volatility-mle.json:quiz[1]` | [slip-line]
  - "You multiplied the sd by 52." <- "You multiplied the sd by 252." [10, 99]
- `estimation/problems-2.json` p-currency-vol (items[2], part 3) | retold | **exam** `exams/topic-1.6.json:items[23]` (s-vol-annual) | [exam-reuse] | [slip-line]
  - "You multiplied the sd by 52." <- "You multiplied the sd by 252." [10, 99]

### exp-log

- `exp-log/problems-1.json` p-yeast-culture (items[0], part 1) | retold | `exp-log/problems-2.json:items[3]` | [slip-line]
  - "You raised $3000 \times 2$ to the power." <- "You raised $2000 \times 1.3$ to the power." [10, 99]
- `exp-log/problems-2.json` p-fault-search (items[0], part 2) | retold | `exp-log/review-2.json:items[1]` | [slip-line]
  - "You multiplied the logs, $5 \times 11$." <- "You multiplied the logs, $2 \times 3$." [10, 99]
- `exp-log/problems-2.json` p-app-users (items[3], part 1) | retold | `exp-log/problems-1.json:items[0]` | [slip-line]
  - "You raised $2000 \times 1.3$ to the power." <- "You raised $3000 \times 2$ to the power." [10, 99]

### fin-ml

- `fin-ml/problems-3.json` p-power-spread-cap (items[3], part 1) | text | **exam** `exams/topic-2.1.json:items[3]` (e-kelly-odds) | [exam-reuse]
  - 10 shared words: "a win pays # per # staked and a loss costs the"

### functions

- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | `functions/homework-2.json:items[1]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | `functions/l6-how-steep.json:screens[2]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
  - "You divided the run by the rise. The gradient is rise over run: $-7.5 \div 3$." <- "You divided the run by the rise. The gradient is rise over run: $3 \div 6$." [10, 99]
- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | `functions/l7-slope-and-start.json:screens[2]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | `functions/l8-line-through-two-points.json:screens[5]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | `functions/review-2.json:items[1]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-candle-burn (items[0], part 1) | retold | **exam** `exams/topic-0.2.json:items[2]` (e-gradient) | [exam-reuse] | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | `functions/homework-2.json:items[1]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | `functions/l6-how-steep.json:screens[2]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
  - "You divided the run by the rise. The gradient is rise over run: $28 \div 7$." <- "You divided the run by the rise. The gradient is rise over run: $3 \div 6$." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | `functions/l7-slope-and-start.json:screens[2]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | `functions/l8-line-through-two-points.json:screens[5]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | `functions/review-2.json:items[1]` | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]
- `functions/problems-2.json` p-path-and-pipe (items[1], part 1) | retold | **exam** `exams/topic-0.2.json:items[2]` (e-gradient) | [exam-reuse] | [slip-line]
  - "You divided the run by the rise." <- "You divided the run by the rise." [10, 99]

### garch

- `garch/problems-2.json` p-two-filters-one-score (items[0], part 1) | retold | `garch/problems-3.json:items[0]` | [slip-line]
  - "You worked in decimals." <- "You worked in decimals." [10, 99]
- `garch/problems-2.json` p-weekly-gas-arch (items[1], part 5) | retold | `garch/review-2.json:items[0]` | [slip-line]
  - "You gave 0.80 to the squared return." <- "You gave 0.94 to the squared return." [10, 99]
- `garch/problems-2.json` p-weekly-gas-arch (items[1], part 5) | retold | `garch/problems-3.json:items[3]` | [slip-line]
  - "You gave it in decimals." <- "You gave it in decimals." [10, 99]
- `garch/problems-2.json` p-silver-moment-fit (items[2], part 4) | retold | `garch/l6-arch.json:screens[2]` | [slip-line]
  - "You used $0.13 \times 4.5$ rather than $0.13 \times 4.5^2$." <- "You used 3 rather than $3^2 = 9$." [10, 99]
- `garch/problems-2.json` p-silver-moment-fit (items[2], part 4) | retold | `garch/review-2.json:items[0]` | [slip-line]
  - "You used $0.13 \times 4.5$ rather than $0.13 \times 4.5^2$." <- "You used 2 rather than $2^2 = 4$." [10, 99]
- `garch/problems-2.json` p-crash-then-quiet (items[3], part 1) | retold | `garch/problems-3.json:items[3]` | [slip-line]
  - "You gave it in decimals." <- "You gave it in decimals." [10, 99]
  - "You gave it in decimals. Everything here is in %, so the variance is 2.9495 %²." <- "You gave it in decimals. Everything here is in %, so the variance is 43.35 %²." [10, 99]
  - "Everything here is in %, so the variance is 2.9495 %²." <- "Everything here is in %, so the variance is 43.35 %²." [2.5, 2]
- `garch/problems-3.json` p-forecasts-to-parameters (items[0], part 2) | retold | `garch/problems-2.json:items[0]` | [slip-line]
  - "You worked in decimals." <- "You worked in decimals." [10, 99]
- `garch/problems-3.json` p-monthly-sleeve (items[3], part 1) | retold | `garch/problems-2.json:items[3]` | [slip-line]
  - "You gave it in decimals." <- "You gave it in decimals." [10, 99]
  - "You gave it in decimals. Everything here is in %, so the variance is 43.35 %²." <- "You gave it in decimals. Everything here is in %, so the variance is 2.9495 %²." [10, 99]
  - "Everything here is in %, so the variance is 43.35 %²." <- "Everything here is in %, so the variance is 2.9495 %²." [2.5, 2]

### integrals

- `integrals/problems-2.json` p-line-and-parabola (items[2], part 2) | retold | `integrals/review-2.json:items[3]` | [slip-line]
  - "You took parabola minus line." <- "You took parabola minus line." [10, 99]
- `integrals/problems-3.json` p-order-size-tail (items[0], part 1) | retold | `integrals/l6-working-backwards.json:quiz[0]` | [slip-line]
  - "You lowered the power." <- "You lowered the power." [10, 99]
- `integrals/problems-3.json` p-time-to-fill (items[1], part 1) | retold | `integrals/l10-undo-product.json:quiz[0]` | [slip-line]
  - "You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$." <- "You took $v = e^{2x}$. Its derivative is $2e^{2x}$, so $v = \tfrac{1}{2}e^{2x}$." [10, 99]
- `integrals/problems-3.json` p-time-to-fill (items[1], part 1) | retold | `integrals/review-3.json:items[1]` | [slip-line]
  - "You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$." <- "You took $v = \cos x$. Its derivative is $-\sin x$, so $v = -\cos x$." [10, 99]

### limits

- `limits/problems-2.json` p-inventory-penalty (items[2], part 1) | retold | `limits/problems-5.json:items[2]` | [slip-line]
  - "You dropped the 0.5 in front of $q^2$." <- "You dropped the 2 in front of $\arctan$." [10, 99]
- `limits/problems-3.json` p-relative-strength (items[0], part 2) | retold | `limits/l9-products-quotients.json:screens[10]` | [slip-line]
  - "You divided $u'$ by $v'$. The derivative of a quotient is not the quotient of the derivatives." <- "You divided $u'$ by $v'$. The derivative of a quotient is not the quotient of the derivatives." [10, 99]
  - "The derivative of a quotient is not the quotient of the derivatives." <- "The derivative of a quotient is not the quotient of the derivatives." [5, 4]
- `limits/problems-3.json` p-research-price (items[1], part 1) | retold | `limits/l11-standard-derivatives.json:screens[9]` | [slip-line]
  - "You left out the inside's derivative, $-1$." <- "You left out the inside's derivative, 5." [10, 99]
- `limits/problems-3.json` p-research-price (items[1], part 2) | retold | `limits/l7-power-rule.json:quiz[3]` | [slip-line]
  - "You multiplied the two derivatives, $1 \times (-60)$." <- "You multiplied the two derivatives, $1 \times \frac{1}{2\sqrt{x}}$." [10, 99]
- `limits/problems-3.json` p-gas-season (items[3], part 1) | retold | `limits/l11-standard-derivatives.json:screens[9]` | [slip-line]
  - "You left out the inside's derivative, $\tfrac{\pi}{6}$." <- "You left out the inside's derivative, 5." [10, 99]
- `limits/problems-3.json` p-gas-season (items[3], part 3) | retold | `limits/l7-power-rule.json:quiz[3]` | [slip-line]
  - "You multiplied the two derivatives, $5 \times (-0.05\pi)$." <- "You multiplied the two derivatives, $1 \times \frac{1}{2\sqrt{x}}$." [10, 99]
- `limits/problems-5.json` p-impact-curve (items[2], part 1) | retold | `limits/problems-2.json:items[2]` | [slip-line]
  - "You dropped the 2 in front of $\arctan$." <- "You dropped the 0.5 in front of $q^2$." [10, 99]

### limits-thm

- `limits-thm/problems-2.json` p-digital-share (items[1], part 4) | retold | `limits-thm/homework-2.json:items[5]` | [slip-line]
  - "You used $0.06 + 0.045$ as the log drift." <- "You used 0.05 as the log drift." [10, 99]
- `limits-thm/problems-2.json` p-digital-share (items[1], part 4) | retold | `limits-thm/l8-lognormal.json:screens[8]` | [slip-line]
  - "You used $0.06 + 0.045$ as the log drift." <- "You used $m = 0.05$ as the log drift." [10, 99]
- `limits-thm/problems-2.json` p-digital-share (items[1], part 4) | retold | `limits-thm/review-2.json:items[8]` | [slip-line]
  - "You used $0.06 + 0.045$ as the log drift." <- "You used $mT = 0.16$ as the log drift." [10, 99]
- `limits-thm/problems-3.json` p-direction-calls (items[1], part 3) | retold | `limits-thm/l12-skill-or-luck.json:screens[7]` | [slip-line]
  - "You added 12 chances of 0.0606." <- "You added 20 chances of 0.0455." [10, 99]
- `limits-thm/problems-3.json` p-rejected-orders (items[2], part 1) | retold | `limits-thm/l10-bound-that-holds.json:screens[3]` | [slip-line]
  - "You divided the threshold by the mean." <- "You divided the threshold by the mean." [10, 99]
- `limits-thm/problems-3.json` p-fund-months (items[3], part 2) | retold | `limits-thm/l12-skill-or-luck.json:screens[2]` | [slip-line]
  - "You divided the standard error by the average." <- "You divided the standard error by the average." [10, 99]

### linear-maps

- `linear-maps/problems-1.json` p-scenario-space (items[2], part 2) | retold | `linear-maps/l1-axioms.json:screens[7]` | [slip-line]
  - "You took the usual zero." <- "You took the usual zero." [10, 99]
- `linear-maps/problems-2.json` p-futures-exposure (items[1], part 2) | retold | `linear-maps/homework-2.json:items[1]` | [slip-line]
  - "You wrote the coordinates as rows." <- "You wrote the coordinates as rows." [10, 99]

### multivar

- `multivar/problems-2.json` p-slopes-around (items[0], part 2) | retold | `multivar/l5-steepest-climb.json:screens[3]` | [slip-line]
  - "You added the components." <- "You added the components." [10, 99]
  - "Using $\nabla f = (12, 9)$, how steep is the steepest climb from P?" <- "How steep is the steepest climb from P?" [3.8, 3]
- `multivar/problems-2.json` p-slopes-around (items[0], part 2) | retold | `multivar/review-2.json:items[0]` | [slip-line]
  - "You added the components." <- "You added the components." [10, 99]
  - "The steepest climb runs along $\nabla f$, with slope $|\nabla f| = \sqrt{144 + 81} = 15$." <- "The steepest climb is along (4, 3) with slope $\sqrt{4^2 + 3^2} = 5$." [4.5, 4]
- `multivar/problems-3.json` p-min-variance-pair (items[2], part 1) | retold | **exam** `exams/topic-1.3.json:items[23]` (c-min-variance) | [exam-reuse]
  - "Asset A has volatility 40% and asset B 25%, with correlation 0.3." <- "Asset 1 has volatility 30% and asset 2 has 15%, with correlation 0.25." [4.8, 4]
  - "You dropped the correlation term $0.06w(1 - w)$." <- "You dropped the covariance term." [1.8, 1]
- `multivar/problems-3.json` p-min-variance-pair (items[2], part 2) | retold | `multivar/l12-min-variance.json:screens[3]` | [slip-line]
  - "You solved $0.1625w - 0.065 = 0$. The derivative of $0.1625w^2$ is $0.325w$." <- "You solved $0.038w_1 = 0.008$. The derivative of $0.038w_1^2$ is $0.076w_1$." [10, 99]
- `multivar/problems-4.json` p-corner-sprinkler (items[1], part 1) | retold | `multivar/problems-5.json:items[1]` | [slip-line]
  - "You wrote $x^2 + y^2$ as $r$. It is $r^2$." <- "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." [10, 99]
- `multivar/problems-4.json` p-drone-landing (items[2], part 2) | retold | `multivar/l13-volume.json:screens[8]` | [slip-line]
  - "You added the two single integrals." <- "You added the two single integrals." [10, 99]
- `multivar/problems-5.json` p-dome-tent (items[1], part 2) | retold | `multivar/problems-4.json:items[1]` | [slip-line]
  - "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." <- "You wrote $x^2 + y^2$ as $r$. It is $r^2$." [10, 99]

### number-sense

- `number-sense/problems-1.json` p-garden-beds (items[0], part 2) | retold | `number-sense/l3-adding-pieces.json:screens[2]` | [slip-line]
  - "You added the tops and the bottoms to get $\tfrac{3}{9}$." <- "You added the tops and the bottoms to get $\tfrac{2}{7}$." [10, 99]
- `number-sense/problems-1.json` p-garden-beds (items[0], part 2) | retold | `number-sense/review-1.json:items[2]` | [slip-line]
  - "You added the tops and the bottoms to get $\tfrac{3}{9}$." <- "You added the tops and the bottoms to get $\tfrac{3}{7}$." [10, 99]
- `number-sense/problems-1.json` p-squash-jugs (items[3], part 1) | retold | `number-sense/homework-1.json:items[1]` | [slip-line]
  - "You added 27 to the top and the bottom." <- "You added 1 to the top and the bottom." [10, 99]
- `number-sense/problems-1.json` p-squash-jugs (items[3], part 1) | retold | `number-sense/l2-same-amount.json:screens[6]` | [slip-line]
  - "You added 27 to the top and the bottom." <- "You added 1 to the top and the bottom." [10, 99]
- `number-sense/problems-1.json` p-squash-jugs (items[3], part 3) | retold | `number-sense/review-1.json:items[3]` | [slip-line]
  - "You added the two fractions." <- "You added the two fractions." [10, 99]
  - "multiply the tops and the bottoms." <- "Multiply the tops and multiply the bottoms." [3, 2]
- `number-sense/problems-1.json` p-squash-jugs (items[3], part 3) | retold | `number-sense/l4-fraction-of-fraction.json:screens[6]` | [slip-line]
  - "You added the two fractions." <- "You added the two fractions." [10, 99]
- `number-sense/problems-3.json` p-cube-tub (items[0], part 1) | retold | `number-sense/l11-undoing-a-square.json:screens[4]` | [slip-line]
  - "You took the square root." <- "You took the square root." [10, 99]
- `number-sense/problems-3.json` p-comet-probe (items[2], part 1) | retold | `number-sense/homework-4.json:items[7]` | [slip-line]
  - "You added the indices." <- "You added the indices." [10, 99]
- `number-sense/problems-3.json` p-comet-probe (items[2], part 1) | retold | `number-sense/l10-repeated-multiplication.json:screens[4]` | [slip-line]
  - "You added the indices." <- "You added the indices." [10, 99]
- `number-sense/problems-3.json` p-comet-probe (items[2], part 1) | retold | `number-sense/l14-very-big-very-small.json:screens[9]` | [slip-line]
  - "You added the indices." <- "You added the indices:" [10, 99]
- `number-sense/problems-3.json` p-comet-probe (items[2], part 1) | retold | `number-sense/review-3.json:items[0]` | [slip-line]
  - "You added the indices." <- "You added the indices." [10, 99]
- `number-sense/problems-4.json` p-hall-tiles (items[0], part 2) | retold | `number-sense/review-4.json:items[1]` | [slip-line]
  - "You multiplied the indices, $3 \times 1 \times 1$." <- "You multiplied the indices, $2 \times 2 \times 1$." [10, 99]
- `number-sense/problems-4.json` p-cycle-commute (items[2], part 5) | retold | `number-sense/l18-circles-and-units.json:screens[5]` | [slip-line]
  - "You multiplied by 3,600 and divided by 1,000." <- "You multiplied by 3,600 and divided by 1,000." [10, 99]
- `number-sense/problems-4.json` p-cycle-commute (items[2], part 5) | retold | `number-sense/review-4.json:items[7]` | [slip-line]
  - "You multiplied by 3,600 and divided by 1,000." <- "You multiplied by 3,600 and divided by 1,000." [10, 99]

### odes

- `odes/problems-3.json` p-liquidity-arbitrage (items[1], part 1) | retold | `odes/l13-linearising.json:screens[0]` | [slip-line]
  - "You swapped the coordinates." <- "You swapped the coordinates." [10, 99]

### quadratics

- `quadratics/problems-1.json` p-cinema-block (items[0], part 1) | retold | `quadratics/l1-two-brackets.json:screens[3]` | [slip-line]
  - "You added 4 and 11 for the corner." <- "You added 6 and 2 for the corner." [10, 99]

### random-vars

- `random-vars/problems-1.json` p-straddle-days (items[2], part 2) | retold | `random-vars/problems-3.json:items[1]` | [slip-line]
  - "You used $c = 0.85$ from part 1's slip." <- "You used $E[AB] = 2.0$ from part 3's slip." [10, 99]
  - "You used $c = 0.85$ from part 1's slip. With $c = 0.15$ the answer is 0.25." <- "You used $E[AB] = 2.0$ from part 3's slip. With $\operatorname{Cov} = 1.68$ the answer is 0.5833." [10, 99]
- `random-vars/problems-2.json` p-reversal-days (items[1], part 1) | retold | `random-vars/l8-indicators.json:quiz[2]` | [slip-line]
  - "You treated up and down as equally likely." <- "You treated up and down as equally likely." [10, 99]
- `random-vars/problems-3.json` p-quote-trades (items[0], part 3) | retold | `random-vars/l10-scaling-and-adding.json:screens[10]` | [slip-line]
  - "You multiplied the sd by 100." <- "You multiplied the sd by 4." [10, 99]
- `random-vars/problems-3.json` p-fund-hedge (items[1], part 4) | retold | `random-vars/problems-1.json:items[2]` | [slip-line]
  - "You used $E[AB] = 2.0$ from part 3's slip." <- "You used $c = 0.85$ from part 1's slip." [10, 99]
  - "You used $E[AB] = 2.0$ from part 3's slip. With $\operatorname{Cov} = 1.68$ the answer is 0.5833." <- "You used $c = 0.85$ from part 1's slip. With $c = 0.15$ the answer is 0.25." [10, 99]
- `random-vars/problems-4.json` p-file-retry (items[3], part 3) | retold | `random-vars/problems-5.json:items[3]` | [slip-line]
  - "You used $m = 2.1$, part 2's slip." <- "You used $\ln 1.05$, part 1's slip." [10, 99]
  - "You used $m = 2.1$, part 2's slip. With $m = 4.2$ the answer is 7.4." <- "You used $\ln 1.05$, part 1's slip. With $E[\ln R] = -0.0527$ the answer is $-0.2108$." [10, 99]
- `random-vars/problems-5.json` p-startup-rounds (items[3], part 2) | retold | `random-vars/problems-4.json:items[3]` | [slip-line]
  - "You used $\ln 1.05$, part 1's slip." <- "You used $m = 2.1$, part 2's slip." [10, 99]
  - "You used $\ln 1.05$, part 1's slip. With $E[\ln R] = -0.0527$ the answer is $-0.2108$." <- "You used $m = 2.1$, part 2's slip. With $m = 4.2$ the answer is 7.4." [10, 99]

### ratio

- `ratio/problems-1.json` p-platform-fee (items[1], part 1) | retold | `ratio/l1-out-of-a-hundred.json:screens[7]` | [slip-line]
  - "You moved the point one place." <- "You moved the point one place." [10, 99]
- `ratio/problems-1.json` p-phone-rise (items[2], part 1) | retold | `ratio/l1-out-of-a-hundred.json:screens[7]` | [slip-line]
  - "You moved the point one place." <- "You moved the point one place." [10, 99]
- `ratio/problems-3.json` p-partners-profit (items[0], part 3) | retold | `ratio/homework-3.json:items[0]` | [slip-line]
  - "You treated £2,850 as one part." <- "You treated £1,260 as one part." [10, 99]
- `ratio/problems-3.json` p-partners-profit (items[0], part 3) | retold | `ratio/l9-sharing.json:screens[5]` | [slip-line]
  - "You treated £2,850 as one part." <- "You treated £18 as one part." [10, 99]

### regression

- `regression/problems-1.json` p-stopping-distances (items[3], part 3) | retold | `regression/problems-3.json:items[3]` | [slip-line]
  - "You left out the intercept $-21.4$." <- "You left out the intercept, 0.05." [10, 99]
  - "A residual is actual minus fitted, $36 - 39.4$, so it is negative." <- "A residual is actual minus fitted." [3.3, 3]
- `regression/problems-2.json` p-sunny-cones (items[0], part 2) | retold | `regression/l5-how-sure.json:screens[4]` | [slip-line]
  - "You divided by 64 itself." <- "You divided by 82.5 itself." [10, 99]
- `regression/problems-2.json` p-grocer-beta (items[3], part 1) | text | **exam** `exams/topic-1.6.json:items[8]` (s-alpha-beta-table) | [exam-reuse]
  - 10 shared words: "s monthly excess returns are regressed on the market s"
- `regression/problems-3.json` p-bond-fund-weeks (items[3], part 1) | retold | `regression/problems-1.json:items[3]` | [slip-line]
  - "You left out the intercept, 0.05." <- "You left out the intercept $-21.4$." [10, 99]

### series

- `series/problems-1.json` p-pendulum-swings (items[1], part 2) | retold | `series/homework-1.json:items[1]` | [slip-line]
  - "You raised $80 \times 0.9$ to the power." <- "You raised $96 \times 0.5$ to the power." [10, 99]
- `series/problems-1.json` p-pendulum-swings (items[1], part 2) | retold | `series/l3-multiplying-each-time.json:screens[7]` | [slip-line]
  - "You raised $80 \times 0.9$ to the power." <- "You raised $5 \times 3$ to the power." [10, 99]

### stat-learning

- `stat-learning/problems-1.json` p-loaves-k (items[1], part 2) | retold | `stat-learning/review-1.json:items[3]` | [slip-line]
  - "You left out the noise." <- "You left out the noise." [10, 99]
- `stat-learning/problems-1.json` p-loaves-k (items[1], part 2) | retold | `stat-learning/homework-1.json:items[3]` | [slip-line]
  - "You divided by 4 for the variance." <- "You divided by 3 for the variance." [10, 99]
  - "You divided by 4 for the variance. Here the variance divides by 5." <- "You divided by 3 for the variance. Here the variance divides by 4." [10, 99]
- `stat-learning/problems-2.json` p-rent-ridge (items[1], part 2) | retold | `stat-learning/l7-shrinking.json:screens[1]` | [slip-line]
  - "You subtracted the penalty." <- "You subtracted the penalty." [10, 99]
  - "You added the penalty on top." <- "You added the penalty on top." [10, 99]
  - "You added the penalty on top. It belongs underneath, beside $\sum x^2$." <- "You added the penalty on top. It belongs underneath, beside $\sum x^2$." [10, 99]
- `stat-learning/problems-2.json` p-built-ridge (items[3], part 4) | retold | `stat-learning/problems-3.json:items[3]` | [slip-line]
  - "You used 0.515, part 3's slip." <- "You used £1,080, part 4's slip." [10, 99]
- `stat-learning/problems-2.json` p-built-ridge (items[3], part 4) | retold | `stat-learning/problems-4.json:items[2]` | [slip-line]
  - "You used 0.515, part 3's slip." <- "You used $\hat y = 9$, part 1's slip." [10, 99]
- `stat-learning/problems-3.json` p-order-fill (items[0], part 3) | retold | `stat-learning/review-3.json:items[1]` | [slip-line]
  - "You multiplied the probability by 0.407." <- "You multiplied the probability by $e^{0.3}$." [10, 99]
  - "The factor applies to the odds, $p/(1 - p)$." <- "The factor applies to the odds." [2.8, 2]
- `stat-learning/problems-3.json` p-order-fill (items[0], part 3) | retold | **exam** `exams/topic-2.1.json:items[20]` (e-odds-update) | [exam-reuse] | [slip-line]
  - "You multiplied the probability by 0.407." <- "You multiplied the probability by $e^{-1.2}$." [10, 99]
- `stat-learning/problems-3.json` p-sterling-calls (items[2], part 3) | retold | `stat-learning/problems-4.json:items[0]` | [slip-line]
  - "You compared with a coin's 0.5." <- "You compared with a coin's 0.5." [10, 99]
- `stat-learning/problems-3.json` p-price-spikes (items[3], part 2) | retold | `stat-learning/homework-3.json:items[5]` | [slip-line]
  - "You put the miss cost on top." <- "You put the miss cost on top." [10, 99]
- `stat-learning/problems-3.json` p-price-spikes (items[3], part 2) | retold | `stat-learning/review-3.json:items[2]` | [slip-line]
  - "You put the miss cost on top." <- "You put the miss cost on top." [10, 99]
  - "You put the miss cost on top. The threshold is the false-alarm cost over the total." <- "You put the miss cost on top. The threshold is the false-alarm cost over the total." [10, 99]
  - "The threshold is the false-alarm cost over the total." <- "The threshold is the false-alarm cost over the total." [4.5, 3]
- `stat-learning/problems-3.json` p-price-spikes (items[3], part 5) | retold | `stat-learning/problems-2.json:items[3]` | [slip-line]
  - "You used £1,080, part 4's slip." <- "You used 0.515, part 3's slip." [10, 99]
- `stat-learning/problems-3.json` p-price-spikes (items[3], part 5) | retold | `stat-learning/problems-4.json:items[2]` | [slip-line]
  - "You used £1,080, part 4's slip." <- "You used $\hat y = 9$, part 1's slip." [10, 99]
- `stat-learning/problems-4.json` p-spam-filter (items[0], part 5) | retold | `stat-learning/problems-3.json:items[2]` | [slip-line]
  - "You compared with a coin's 0.5." <- "You compared with a coin's 0.5." [10, 99]
- `stat-learning/problems-4.json` p-order-sizes (items[1], part 3) | retold | `stat-learning/l16-groups-nobody-labelled.json:screens[2]` | [slip-line]
  - "You added plain distances, $2 + 0 + 2 + 4 + 0 + 4$." <- "You added plain distances, $2 + 0 + 2 + 4 + 2 + 6$." [10, 99]
  - "You added plain distances, $2 + 0 + 2 + 4 + 0 + 4$. Inertia squares them." <- "You added plain distances, $2 + 0 + 2 + 4 + 2 + 6$. Inertia squares them." [10, 99]
- `stat-learning/problems-4.json` p-order-sizes (items[1], part 4) | retold | `stat-learning/l18-bending-the-line.json:screens[1]` | [slip-line]
  - "You left out the hinge." <- "You left out the hinge." [10, 99]
- `stat-learning/problems-4.json` p-one-unit (items[2], part 2) | retold | `stat-learning/problems-2.json:items[3]` | [slip-line]
  - "You used $\hat y = 9$, part 1's slip." <- "You used 0.515, part 3's slip." [10, 99]
- `stat-learning/problems-4.json` p-one-unit (items[2], part 2) | retold | `stat-learning/problems-3.json:items[3]` | [slip-line]
  - "You used $\hat y = 9$, part 1's slip." <- "You used £1,080, part 4's slip." [10, 99]
- `stat-learning/problems-4.json` p-renewals (items[3], part 3) | retold | `stat-learning/problems-3.json:items[2]` | [slip-line]
  - "You compared with a coin's 0.5." <- "You compared with a coin's 0.5." [10, 99]

### taylor

- `taylor/problems-2.json` p-three-halves (items[0], part 4) | retold | `taylor/l6-matching-derivatives.json:quiz[0]` | [slip-line]
  - "You divided by 3. The coefficient divides by $3! = 6$." <- "You divided by $k = 4$. The coefficient divides by $4! = 24$." [10, 99]
- `taylor/problems-2.json` p-square-geometric (items[1], part 2) | retold | `taylor/l6-matching-derivatives.json:quiz[0]` | [slip-line]
  - "You divided by 3. The coefficient divides by $3! = 6$." <- "You divided by $k = 4$. The coefficient divides by $4! = 24$." [10, 99]
- `taylor/problems-2.json` p-log-two (items[3], part 4) | retold | `taylor/l6-matching-derivatives.json:quiz[0]` | [slip-line]
  - "You divided by 3. The coefficient divides by $3! = 6$." <- "You divided by $k = 4$. The coefficient divides by $4! = 24$." [10, 99]
- `taylor/problems-3.json` p-two-months (items[1], part 2) | retold | `taylor/l2-how-wrong.json:screens[7]` | [slip-line]
  - "You divided by $3! = 6$, as for $e^x$." <- "You divided by 64, as for $h^3$." [10, 99]
- `taylor/problems-3.json` p-big-gain (items[3], part 2) | retold | `taylor/l2-how-wrong.json:screens[7]` | [slip-line]
  - "You divided by $k!$, as for $e^x$." <- "You divided by 64, as for $h^3$." [10, 99]

### testing

- `testing/problems-1.json` p-cereal-boxes (items[0], part 2) | retold | `testing/l2-measuring-surprise.json:screens[7]` | [slip-line]
  - "You divided by 36. The standard error divides by $\sqrt{36} = 6$." <- "You divided by $\sigma\sqrt n$. The standard error divides by $\sqrt n$." [10, 99]
- `testing/problems-1.json` p-cereal-boxes (items[0], part 2) | retold | `testing/l4-t-test.json:screens[2]` | [slip-line]
  - "You divided by 36. The standard error divides by $\sqrt{36} = 6$." <- "You divided by $s/n$. The standard error divides by $\sqrt n$." [10, 99]
- `testing/problems-1.json` p-cereal-boxes (items[0], part 4) | retold | `testing/homework-1.json:items[0]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-cereal-boxes (items[0], part 4) | retold | `testing/problems-3.json:items[1]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-cereal-boxes (items[0], part 4) | retold | `testing/review-1.json:items[7]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-cereal-boxes (items[0], part 4) | retold | **exam** `exams/topic-1.6.json:items[4]` (s-sharpe-p) | [exam-reuse] | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-phone-battery (items[1], part 1) | retold | `testing/problems-2.json:items[2]` | [slip-line]
  - "You divided the total, 144, by 7." <- "You divided the total, $-36$, by 8." [10, 99]
  - "You divided by $s$ itself." <- "You divided by $s_d$ itself." [10, 99]
  - "You used $s = 1.871$, from dividing by 8." <- "You used $s_d = 2.828$, from dividing by 9." [10, 99]
  - "You used $s = 1.871$, from dividing by 8. With $s = 2$ the statistic is $-2.121$." <- "You used $s_d = 2.828$, from dividing by 9. With $s_d = 3$ the statistic is $-4$." [10, 99]
  - "Using $\bar x = 18$ and $s = 2$, what is the $t$ statistic for $H_0: \mu = 19.5$?" <- "Using $\bar d = -4$ and $s_d = 3$, what is the paired $t$ statistic?" [2.8, 2]
  - "$-2.121$ is below $-1.895$, the one-sided cut-off of $t_7$" <- "The one-sided 5% cut-off of $t_8$ is 1.860." [2.8, 2]
  - "Using $t = -2.121$ from part 3, which conclusion is right at 5%?" <- "Using $p = 0.0118$ from part 3, which statement is right?" [2, 1]
- `testing/problems-1.json` p-phone-battery (items[1], part 5) | retold | `testing/review-1.json:items[8]` | [slip-line]
  - "You used 2.365, the two-sided cut-off." <- "You used 1.96, the two-sided cut-off." [10, 99]
- `testing/problems-1.json` p-phone-battery (items[1], part 5) | retold | **exam** `exams/topic-1.6.json:items[28]` (s-trades-needed) | [exam-reuse] | [slip-line]
  - "You used 2.365, the two-sided cut-off." <- "You used 1.96, the two-sided cut-off." [10, 99]
- `testing/problems-1.json` p-pizza-delivery (items[3], part 2) | retold | `testing/homework-1.json:items[0]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-pizza-delivery (items[3], part 2) | retold | `testing/problems-3.json:items[1]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
  - "The upper tail beyond 1.75 holds $1 - 0.9599 = 0.0401$." <- "The upper tail beyond 2.7 holds 0.0035." [3.5, 3]
- `testing/problems-1.json` p-pizza-delivery (items[3], part 2) | retold | `testing/review-1.json:items[7]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-1.json` p-pizza-delivery (items[3], part 2) | retold | **exam** `exams/topic-1.6.json:items[4]` (s-sharpe-p) | [exam-reuse] | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-2.json` p-running-shoes (items[2], part 1) | retold | `testing/problems-1.json:items[1]` | [slip-line]
  - "You divided the total, $-36$, by 8." <- "You divided the total, 144, by 7." [10, 99]
  - "You divided by $s_d$ itself." <- "You divided by $s$ itself." [10, 99]
  - "You used $s_d = 2.828$, from dividing by 9." <- "You used $s = 1.871$, from dividing by 8." [10, 99]
  - "You used $s_d = 2.828$, from dividing by 9. With $s_d = 3$ the statistic is $-4$." <- "You used $s = 1.871$, from dividing by 8. With $s = 2$ the statistic is $-2.121$." [10, 99]
  - "Using $\bar d = -4$ and $s_d = 3$, what is the paired $t$ statistic?" <- "Using $\bar x = 18$ and $s = 2$, what is the $t$ statistic for $H_0: \mu = 19.5$?" [2.8, 2]
  - "The one-sided 5% cut-off of $t_8$ is 1.860." <- "$-2.121$ is below $-1.895$, the one-sided cut-off of $t_7$" [2.8, 2]
  - "The mean of 9 differences has standard error $\tfrac{3}{\sqrt 9} = 1$." <- "The mean of $n$ boxes has standard error $\tfrac{\sigma}{\sqrt n}$." [2, 1]
- `testing/problems-3.json` p-fund-managers (items[1], part 2) | retold | `testing/problems-1.json:items[3]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
  - "The upper tail beyond 2.7 holds 0.0035." <- "The upper tail beyond 1.75 holds $1 - 0.9599 = 0.0401$." [3.5, 3]
- `testing/problems-3.json` p-fund-managers (items[1], part 2) | retold | **exam** `exams/topic-1.6.json:items[4]` (s-sharpe-p) | [exam-reuse] | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
  - "Take the upper tail beyond $t = 2.7$." <- "Then take the upper tail beyond $t$." [3.5, 3]
- `testing/problems-3.json` p-fund-managers (items[1], part 2) | retold | `testing/homework-1.json:items[0]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-3.json` p-fund-managers (items[1], part 2) | retold | `testing/review-1.json:items[7]` | [slip-line]
  - "You doubled the tail." <- "You doubled the tail." [10, 99]
- `testing/problems-4.json` p-website-signups (items[1], part 4) | retold | `testing/homework-4.json:items[2]` | [slip-line]
  - "You divided the variance by the bound." <- "You divided the variance by the bound." [10, 99]
- `testing/problems-4.json` p-website-signups (items[1], part 4) | retold | `testing/l16-best-possible-precision.json:screens[5]` | [slip-line]
  - "You divided the variance by the bound." <- "You divided the variance by the bound." [10, 99]
- `testing/problems-4.json` p-bakery-loaves (items[2], part 2) | retold | **exam** `exams/topic-1.6.json:items[20]` (s-chi-order-mix) | [exam-reuse] | [slip-line]
  - "You added the squared gaps, $4 \times 64$, without dividing each by its expected count." <- "You added the squared gaps, $196 + 196$, without dividing each by its expected count." [10, 99]
  - "You divided by the observed counts." <- "You divided by the observed counts." [10, 99]
  - "Pearson's statistic divides by the expected counts." <- "Pearson's statistic divides by the expected counts, 100 and 60." [3, 2]
  - "The p-value is the upper tail." <- "The p-value is the tail beyond:" [1.8, 1]

### trig

- `trig/problems-1.json` p-zip-wire (items[0], part 1) | retold | `trig/homework-1.json:items[0]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-1.json` p-zip-wire (items[0], part 1) | retold | `trig/l1-squares-on-sides.json:screens[5]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-1.json` p-zip-wire (items[0], part 1) | retold | `trig/review-1.json:items[0]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-1.json` p-desk-lamp (items[3], part 2) | retold | `trig/homework-1.json:items[0]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-1.json` p-desk-lamp (items[3], part 2) | retold | `trig/l1-squares-on-sides.json:screens[5]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-1.json` p-desk-lamp (items[3], part 2) | retold | `trig/review-1.json:items[0]` | [slip-line]
  - "You subtracted the squares." <- "You subtracted the squares." [10, 99]
- `trig/problems-2.json` p-water-wheel (items[0], part 5) | retold | `trig/review-2.json:items[5]` | [slip-line]
  - "You used $s = r\theta$ with $\theta$ in degrees." <- "You used $s = r\theta$ with $\theta$ in degrees." [10, 99]
- `trig/problems-2.json` p-observation-wheel (items[2], part 2) | retold | `trig/problems-3.json:items[2]` | [slip-line]
  - "You turned the fraction upside down." <- "You turned the fraction upside down." [10, 99]
  - "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 20$, $b = \tfrac{2\pi}{20}$." <- "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 12$, $b = \tfrac{2\pi}{12}$." [10, 99]
- `trig/problems-3.json` p-daylight-model (items[2], part 2) | retold | `trig/problems-2.json:items[2]` | [slip-line]
  - "You turned the fraction upside down." <- "You turned the fraction upside down." [10, 99]
  - "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 12$, $b = \tfrac{2\pi}{12}$." <- "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 20$, $b = \tfrac{2\pi}{20}$." [10, 99]

### vector-calc

- `vector-calc/problems-1.json` p-bead-semicircle (items[0], part 3) | retold | `vector-calc/homework-1.json:items[6]` | [slip-line]
  - "You left out the speed $|\mathbf r'(t)| = 6$." <- "You left out the speed $\sqrt2$:" [10, 99]
- `vector-calc/problems-1.json` p-bead-semicircle (items[0], part 3) | retold | `vector-calc/l2-line-integrals.json:screens[3]` | [slip-line]
  - "You left out the speed $|\mathbf r'(t)| = 6$." <- "You left out the speed $\sqrt 2$:" [10, 99]
- `vector-calc/problems-1.json` p-bead-semicircle (items[0], part 3) | retold | `vector-calc/review-1.json:items[2]` | [slip-line]
  - "You left out the speed $|\mathbf r'(t)| = 6$." <- "You left out the speed $|(6, 8)| = 10$." [10, 99]
- `vector-calc/problems-1.json` p-bead-semicircle (items[0], part 3) | retold | `vector-calc/l12-stokes.json:screens[6]` | [slip-line]
  - "You integrated $|\mathbf F|^2 = 180$ instead of $|\mathbf F| = 6\sqrt5$." <- "You integrated 1 instead of $1 - t$." [10, 99]

### vectors

- `vectors/problems-2.json` p-site-plan (items[1], part 2) | retold | `vectors/l7-one-after-another.json:quiz[0]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]
- `vectors/problems-2.json` p-site-plan (items[1], part 2) | retold | `vectors/problems-3.json:items[2]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]
- `vectors/problems-3.json` p-colour-sensor (items[2], part 1) | retold | `vectors/l7-one-after-another.json:quiz[0]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]
- `vectors/problems-3.json` p-colour-sensor (items[2], part 1) | retold | `vectors/problems-2.json:items[1]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]
- `vectors/problems-3.json` p-engraver-dial (items[3], part 1) | retold | `vectors/l7-one-after-another.json:quiz[0]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]
- `vectors/problems-3.json` p-engraver-dial (items[3], part 1) | retold | `vectors/problems-2.json:items[1]` | [slip-line]
  - "You multiplied matching entries." <- "You multiplied matching entries." [10, 99]

