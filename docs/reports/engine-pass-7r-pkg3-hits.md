# Engine pass 7 remainder, package 3: new reuse hits for a human reader

Run: `node tools/same-course-reuse.mjs --all --all-exams --no-waivers --json` on the content of this branch. Every hit is a warning (never an error, never gated). No waiver was added, no content changed.
"Waived now" marks a hit that an existing waiver of `tools/same-course-waivers.json` (keyed by file, item and kind, no source) already clears in the gate run.

Counts by tag: all-exams 65, chain-union 1, question 1, ratio 7; total 74.


## all-exams (65)

| File | Item | Other file | Message | Waived now |
|---|---|---|---|---|
| courses/algebra/problems-1.json | p-probe-stride items[0] part 4 | exams/mock-oa-arith.json:parts[0].items[21] (exam item q55-percent) | the ratio 4.3077 of two stated amounts (13 to 56 here, 65 to 280 there) | no |
| courses/analysis/problems-2.json | p-sum-law-band items[0] part 5 | exams/topic-2.1.json:items[26] (exam item e-kelly-wrong) | the rate 4/311 here and 1.29% there, with 0.04 in both | no |
| courses/arma/problems-3.json | p-smoothed-fund items[0] part 4 | exams/topic-2.1.json:items[28] (exam item e-honest-t) | the rate 10.0% here and 1/10 there, with 0.52 in both | no |
| courses/coint/problems-1.json | p-screen-real-share items[3] part 3 | exams/topic-3.3.json:items[33] (exam item e-late-window) | the rate 19.4% here and 0.1944 there, with 36 in both | no |
| courses/coint/problems-1.json | p-screen-real-share items[3] part 3 | exams/mock-oa-trader.json:parts[1].items[11] (exam item b12-max-of-dice) | the rate 19.4% here and 7/36 there, with 36 in both | no |
| courses/complex/problems-2.json | p-plate-heat items[1] part 5 | courses/complex/review-1.json:items[1] | 1 retold sentence (weight 10.0): "You added the sizes of the parts. The modulus is $\sqrt{5^2 + 2^2}$." against "You added the sizes of the parts. The modulus is $\sqrt{(-2)^2 + 2^2}$." | yes |
| courses/conditional/problems-2.json | p-takeover-rumour items[0] part 3 | exams/topic-0.5.json:items[5] (exam item m-chain) | the ratio 2.5333 of two stated amounts (180 to 456 here, 15 to 38 there) | no |
| courses/conditional/problems-4.json | p-two-strategies items[1] part 2 | courses/conditional/homework-4.json:items[0] | 2 retold sentences (weight 2.5, weight 2.3): "That is the chance B wins." against "That is the chance staying wins." | yes |
| courses/conditional/problems-5.json | p-two-houses items[1] part 2 | courses/conditional/homework-5.json:items[3] | a question that holds a source question whole, with a phrase added or a word changed: "For House S, by how many percentage points does the survivors' 8% overstate the average ov" against "By how many percentage points does the survivors’ average overstate the average of all fun" | no |
| courses/counting/problems-3.json | p-grain-merchant items[2] part 4 | courses/counting/l13-portfolio-vector.json:quiz[2] | 2 retold sentences (weight 6.5, weight 4.0): "Divide the dot product by both magnitudes, then take the inverse cosine." against "Divide the dot product by both magnitudes, then take the inverse cosine." | yes |
| courses/eigen/problems-3.json | p-crab-sizes items[1] part 1 | exams/mock-oa-trader.json:parts[0].items[8] (exam item a09-digit-sum) | the ratio 1.3409 of two stated amounts (88 to 118 here, 44 to 59 there) | no |
| courses/eigen/problems-3.json | p-site-anomalies items[2] part 3 | exams/topic-2.6.json:items[1] (exam item e-pd-at-leverage) | the rate 0.769 here and 76.85\% there, with 1.2 in both | no |
| courses/elimination/problems-1.json | p-florist-prices items[0] part 1 | exams/mock-superday-trader.json:parts[1].items[2] (exam item b3-two-by-two) | the ratio 1.4615 of two stated amounts (13 to 19 here, 26 to 38 there) | no |
| courses/elimination/problems-3.json | p-vinyl-cutter items[0] part 1 | courses/elimination/l9-area-scale.json:quiz[0] | 2 retold sentences (weight 10.0, weight 1.8): "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." against "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$." | yes |
| courses/elimination/problems-3.json | p-vinyl-cutter items[0] part 1 | courses/elimination/review-3.json:items[0] | 2 retold sentences (weight 10.0, weight 1.8): "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." against "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$." | yes |
| courses/fin-ml/problems-3.json | p-power-spread-cap items[3] part 1 | courses/fin-ml/l9-probability-to-position.json:screens[3] | 2 retold sentences (weight 3.5, weight 2.5): "What fraction of capital does Kelly stake at $p = 0.70$?" against "What fraction does Kelly stake?" | yes |
| courses/fin-ml/problems-3.json | p-power-spread-cap items[3] part 1 | courses/fin-ml/review-3.json:items[1] | 2 retold sentences (weight 3.5, weight 2.5): "What fraction of capital does Kelly stake at $p = 0.70$?" against "What fraction does Kelly stake?" | yes |
| courses/functions/problems-1.json | p-sapling-log items[3] part 1 | exams/topic-3.3.json:items[0] (exam item e-mult-58-64) | the ratio 1.1034 of two stated amounts (29 to 32 here, 58 to 64 there) | no |
| courses/garch/problems-2.json | p-two-filters-one-score items[0] part 1 | exams/stage-2.json:parts[1].items[2] (exam item b-ljung-box) | the rate 1.44 % here and 0.0144 there, with 0.08 in both | no |
| courses/garch/problems-3.json | p-bank-index-flat-var items[1] part 1 | exams/topic-2.5.json:items[22] (exam item e-long-only-kkt) | the rate 2.25 % here and 0.0225 there, with 1.25 in both | no |
| courses/garch/problems-3.json | p-bank-index-flat-var items[1] part 1 | exams/stage-2.json:parts[2].items[6] (exam item c-kkt-hand) | the rate 2.25 % here and 0.0225 there, with 1.25 in both | no |
| courses/integrals/problems-2.json | p-area-function items[0] part 3 | courses/integrals/l6-working-backwards.json:quiz[0] | 2 retold sentences (weight 4.3, weight 2.8): "Raise each power by one and divide by the new power:" against "Raise the power by one and divide by the new power." | yes |
| courses/integrals/problems-2.json | p-line-and-parabola items[2] part 2 | courses/integrals/l8-between-curves.json:screens[2] | 4 retold sentences across parts 2, 3 (weight 20.3): "You took parabola minus line. Top minus bottom keeps the area positive." against "You took parabola minus line. Top minus bottom keeps the area positive." | yes |
| courses/least-squares/problems-3.json | p-runner-heart items[0] part 5 | exams/mock-oa-trader.json:parts[0].items[8] (exam item a09-digit-sum) | the ratio 1.475 of two stated amounts (4 to 5.9 here, 40 to 59 there) | no |
| courses/limits-thm/problems-1.json | p-settlement-checks items[3] part 2 | courses/limits-thm/review-1.json:items[7] | 2 retold sentences (weight 2.3, weight 2.3): "That is the binomial variance $50 \times 0.03 \times 0.97$." against "Multiply the binomial variance by $\tfrac{N - n}{N - 1}$." | yes |
| courses/limits-thm/problems-2.json | p-digital-share items[1] part 5 | courses/limits-thm/review-2.json:items[7] | 1 retold sentence (weight 10.0): "You used 1.96, which leaves 2.5% in each tail." against "You used 1.96, which leaves 2.5% in each tail." | yes |
| courses/limits-thm/problems-3.json | p-fund-months items[3] | exams/topic-1.6.json:items[4] (exam item s-sharpe-p) | 3 shared distinctive numbers (0.0359 0.0719 0.9641) | no |
| courses/limits/problems-3.json | p-relative-strength items[0] | exams/topic-1.6.json:items[0] (exam item s-hit-rate-se) | consecutive part keys 0.0004 and 0.02 sit together in "The root of 0.0004 is 0.02, or 2 percentage points." | no |
| courses/limits/problems-5.json | p-camera-pan items[0] part 1 | courses/limits/l19-running-backwards.json:screens[7] | 2 retold sentences (weight 2.8, weight 2.5): "The slope of $\arctan u$ is $\dfrac{1}{1+u^2}$, times the slope of $u = \dfrac{x}{30}$." against "The slope of $\arctan u$ is $\dfrac{1}{1 + u^2}$, times the slope of $u$." | yes |
| courses/markov/problems-3.json | p-maker-edge items[0] part 3 | exams/topic-3.5.json:items[13] (exam item e-crossing-buy) | the ratio 10.05 of two stated amounts (39.8 to 400 here, 10 to 100.5 there) | no |
| courses/markov/problems-5.json | p-signal-trial items[1] part 2 | courses/markov/review-5.json:items[1] | 2 retold sentences (weight 2.5, weight 2.3): "Which base $r$ makes $r^{S_n}$ a martingale?" against "Which base $r$ makes $r^{S_n}$ a martingale?" | yes |
| courses/multivar/problems-4.json | p-corner-sprinkler items[1] part 1 | courses/multivar/problems-5.json:items[1] | 1 retold sentence (weight 10.0): "You wrote $x^2 + y^2$ as $r$. It is $r^2$." against "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." | yes |
| courses/multivar/problems-5.json | p-dome-tent items[1] part 2 | courses/multivar/problems-4.json:items[1] | 1 retold sentence (weight 10.0): "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." against "You wrote $x^2 + y^2$ as $r$. It is $r^2$." | yes |
| courses/multivar/problems-5.json | p-triangle-field items[2] part 2 | courses/limits-thm/l17-smallest-and-largest.json:screens[6] | -x^4 + 3x^3 - 3x^2 + x (the same polynomial in another course) | yes |
| courses/number-sense/problems-3.json | p-comet-probe items[2] part 2 | courses/number-sense/l13-estimate-first.json:quiz[0] | 2 retold sentences (weight 2.8, weight 2.5): "The first significant figure of 8,760 is the 8 thousands." against "The first significant figure is the 5." | yes |
| courses/number-sense/problems-4.json | p-cycle-commute items[2] part 5 | courses/number-sense/l18-circles-and-units.json:screens[5] | 1 retold sentence (weight 10.0): "You multiplied by 3,600 and divided by 1,000." against "You multiplied by 3,600 and divided by 1,000." | yes |
| courses/number-sense/problems-4.json | p-cycle-commute items[2] part 5 | courses/number-sense/review-4.json:items[7] | 1 retold sentence (weight 10.0): "You multiplied by 3,600 and divided by 1,000." against "You multiplied by 3,600 and divided by 1,000." | yes |
| courses/number-sense/problems-4.json | p-cycle-commute items[2] part 2 | exams/topic-2.3.json:items[28] (exam item e-code-net-book) | the number set 24, 26, 27, 31 against 0.04, -0.03, 0.01, 0.02: equal after x -> a x + b | no |
| courses/numerics/problems-4.json | p-grid-node-budget items[2] part 1 | exams/topic-0.5.json:items[5] (exam item m-chain) | the ratio 2.5333 of two stated amounts (30 to 76 here, 15 to 38 there) | no |
| courses/random-vars/problems-1.json | p-tightest-quote items[3] part 4 | exams/topic-2.3.json:items[19] (exam item e-cost-drag) | the rate 0.0101 here and 1.01% there, with 0.6 in both | no |
| courses/random-vars/problems-4.json | p-file-retry items[3] part 4 | exams/mock-oa-trader-3.json:parts[0].items[13] (exam item a14-square-digit-sum) | the ratio 2.3125 of two stated amounts (3.2 to 7.4 here, 16 to 37 there) | no |
| courses/ratio/problems-3.json | p-partners-profit items[0] part 3 | exams/topic-1.6.json:items[6] (exam item s-ci-meaning) | the ratio 4.2105 of two stated amounts (2850 to 12000 here, 95 to 400 there) | no |
| courses/regression/problems-1.json | p-car-prices items[1] part 1 | exams/topic-1.1.json:items[17] (exam item e-assert-catch) | the ratio 1.1688 of two stated amounts (15400 to 18000 here, 77 to 90 there) | no |
| courses/regression/problems-2.json | p-grocer-beta items[3] part 1 | courses/regression/problems-3.json:items[2] | 2 retold sentences (weight 3.5, weight 3.0): "What is the residual standard deviation $s$, in % a month?" against "What is the residual standard deviation $s$, in %?" | yes |
| courses/regression/problems-3.json | p-overlap-signal items[2] part 1 | courses/regression/problems-2.json:items[3] | 2 retold sentences (weight 3.5, weight 3.0): "What is the residual standard deviation $s$, in %?" against "What is the residual standard deviation $s$, in % a month?" | yes |
| courses/series/problems-2.json | p-bouncing-ball items[2] part 1 | exams/topic-2.3.json:items[19] (exam item e-cost-drag) | the rate 0.0101 here and 1.01% there, with 1.8 in both | no |
| courses/stat-learning/problems-1.json | p-loaves-k items[1] part 5 | exams/mock-oa-trader.json:parts[0].items[8] (exam item a09-digit-sum) | the ratio 1.7931 of two stated amounts (5.8 to 10.4 here, 29 to 52 there) | no |
| courses/stat-learning/problems-1.json | p-heat-demand items[3] part 1 | courses/stat-learning/l2-training-error-lies.json:quiz[1] | 2 retold sentences (weight 2.8, weight 2.8): "Degree 2 has the lowest test MSE, 1.80." against "B has the lowest test MSE." | yes |
| courses/stat-learning/problems-3.json | p-sterling-calls items[2] part 3 | courses/stat-learning/problems-4.json:items[0] | 1 retold sentence (weight 10.0): "You compared with a coin's 0.5." against "You compared with a coin's 0.5." | yes |
| courses/stat-learning/problems-4.json | p-spam-filter items[0] part 5 | courses/stat-learning/problems-3.json:items[2] | 1 retold sentence (weight 10.0): "You compared with a coin's 0.5." against "You compared with a coin's 0.5." | yes |
| courses/stat-learning/problems-4.json | p-renewals items[3] part 3 | courses/stat-learning/problems-3.json:items[2] | 1 retold sentence (weight 10.0): "You compared with a coin's 0.5." against "You compared with a coin's 0.5." | yes |
| courses/stat-models/problems-2.json | p-two-looks items[2] part 4 | exams/topic-2.2.json:items[9] (exam item e-breach-days) | the rate 0.0107 here and 1.07% there, with 37 in both | no |
| courses/stat-models/problems-3.json | p-spread-day-tail items[1] part 3 | exams/topic-0.5.json:items[5] (exam item m-chain) | the ratio 1.4074 of two stated amounts (2.003 to 2.819 here, 27 to 38 there) | no |
| courses/taylor/problems-1.json | p-newton-cubic items[1] part 3 | courses/taylor/l8-convexity.json:quiz[3] | 2 retold sentences (weight 4.5, weight 3.8): "A curve that bends up lies above its tangent." against "The curve bends up, so it lies above its tangents." | yes |
| courses/taylor/problems-3.json | p-tail-bound items[2] part 1 | courses/taylor/l7-standard-series.json:screens[9] | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial, factorised or not, with the letter renamed) | yes |
| courses/taylor/problems-3.json | p-tail-bound items[2] part 1 | exams/topic-1.3.json:items[10] (exam item c-e2x-series) | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial in another course) | yes |
| courses/taylor/problems-3.json | p-big-gain items[3] part 2 | courses/taylor/l7-standard-series.json:screens[5] | -0.25x^4 + 0.333333x^3 - 0.5x^2 + x (the same polynomial, factorised or not, with the letter renamed) | yes |
| courses/testing/problems-3.json | p-fund-managers items[1] part 3 | courses/testing/homework-3.json:items[2] | 3 retold sentences (weight 3.8, weight 2.3): "With p = 0.0035, the largest rank under its bar is 5." against "rank 5 is the largest rank under its bar." | yes |
| courses/testing/problems-3.json | p-fund-managers items[1] part 3 | courses/testing/l10-correcting.json:quiz[0] | 2 retold sentences (weight 3.8, weight 1.8): "With p = 0.0035, the largest rank under its bar is 5." against "rank 3 is the largest rank under its bar." | yes |
| courses/trig/problems-2.json | p-two-buoys items[1] | courses/trig/l9-stretching-a-wave.json:screens[4] | consecutive part keys 2.5 and 5.5 sit together in "So $y$ runs from 2.5 to 5.5." | yes |
| courses/validation/problems-2.json | p-gas-demand items[0] part 3 | exams/mock-oa-trader-2.json:parts[0].items[9] (exam item a10-reversed-squares) | the ratio 1.1731 of two stated amounts (5.2 to 6.1 here, 52 to 61 there) | no |
| courses/validation/problems-2.json | p-gas-demand items[0] part 3 | exams/mock-oa-trader-3.json:parts[0].items[9] (exam item a10-digit-sum-five) | the ratio 1.1731 of two stated amounts (5.2 to 6.1 here, 104 to 122 there) | no |
| courses/validation/problems-2.json | p-spread-blocks items[3] part 4 | exams/topic-1.1.json:items[17] (exam item e-assert-catch) | the ratio 1.2987 of two stated amounts (3.85 to 5 here, 77 to 100 there) | no |
| courses/vector-calc/problems-2.json | p-rectangle-edges items[0] part 1 | exams/topic-1.3.json:items[12] (exam item c-slope-graph) | x^3 - 4x (the same polynomial, factorised or not, with the letter renamed) | no |
| courses/vectors/problems-1.json | p-charging-robot items[0] part 3 | courses/vectors/l3-lengths-angles.json:screens[4] | 2 retold sentences (weight 6.3, weight 2.5): "Divide the dot product by the two lengths, then take the inverse cosine." against "Divide the dot product by both lengths, then take the inverse cosine." | yes |

## chain-union (1)

| File | Item | Other file | Message | Waived now |
|---|---|---|---|---|
| courses/validation/problems-2.json | p-spread-blocks items[3] part 1 | courses/validation/l5-shuffling-lies.json:screens[1] | 3 parts (1, 2, 3) each follow a step of 2 different sources: l5-shuffling-lies.json:screens[1], l5-shuffling-lies.json:screens[7], homework-2.json:items[2] | no |

## question (1)

| File | Item | Other file | Message | Waived now |
|---|---|---|---|---|
| courses/conditional/problems-5.json | p-two-houses items[1] part 2 | courses/conditional/homework-5.json:items[3] | a question that holds a source question whole, with a phrase added or a word changed: "For House S, by how many percentage points does the survivors' 8% overstate the average ov" against "By how many percentage points does the survivors’ average overstate the average of all fun" | no |

## ratio (7)

| File | Item | Other file | Message | Waived now |
|---|---|---|---|---|
| courses/equations/problems-2.json | p-interest-split items[3] part 3 | courses/equations/l15-swapping-in.json:screens[9] | the ratio 1.5152 of two stated amounts (660 to 1000 here, 8.25 to 12.5 there) | no |
| courses/numerics/problems-1.json | p-float32-overnight items[0] part 3 | courses/numerics/l8-splines.json:screens[5] | the ratio 2.5316 of two stated amounts (3.16 to 8 here, 3.95 to 10 there) | no |
| courses/numerics/problems-4.json | p-pilot-control items[1] part 1 | courses/numerics/l1-floating-point.json:screens[9] | the ratio 25.974 of two stated amounts (77 to 2000 here, 2.31 to 60 there) | no |
| courses/regression/problems-1.json | p-stopping-distances items[3] part 1 | courses/regression/l3-how-much-explained.json:screens[1] | the ratio 1.5652 of two stated amounts (23 to 36 here, 2.3 to 3.6 there) | no |
| courses/stat-learning/problems-1.json | p-heat-demand items[3] part 1 | courses/stat-learning/review-2.json:items[5] | the ratio 1.9355 of two stated amounts (3.1 to 6 here, 31 to 60 there) | no |
| courses/trig/problems-3.json | p-daylight-model items[2] part 1 | courses/trig/homework-3.json:items[6] | the ratio 2.1579 of two stated amounts (7.6 to 16.4 here, 380 to 820 there) | no |
| courses/vectors/problems-1.json | p-charging-robot items[0] part 4 | courses/vectors/l4-portfolio-return.json:quiz[3] | the ratio 1.619 of two stated amounts (42 to 68 here, 2.1 to 3.4 there) | no |
