# Problem sets 1.6 (a): second-reader findings

Scope: `app/content/courses/estimation/problems-1.json` to `problems-3.json` and `app/content/courses/regression/problems-1.json` to `problems-3.json` at commit 05c94b1: 24 problems, 106 parts (99 typed, 7 choice). Rules: `docs/briefs/chained.md`. Patterns: `review-problems-1.5-a.md`, `review-holes-1.6-2.1.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness, coverage.

Method. Lessons l1 to l12 of both courses were read first (every screen and quiz question), then each course's reviews, homework and `exams/topic-1.6.json`, for what is taught and what is reused. The two authors' scripts were run. Every part was then solved from its text before its key was read, and again in `review-problems-1.6-a-scripts/mine.py`, with no import from the authors' scripts and by another route where one exists: numerical maximisation for each MLE (the restricted and the censored one too), a root-finder for each cut-off, all 27 bootstrap resamples, simulation for the two MSE problems, statsmodels fits of data built to each problem's stated sums (the freight summary, the raw and excess regressions, the gas and carbon fit with its VIF, the solar moment matrix), SciPy quantiles and statsmodels' Durbin-Watson. Every `wrong` value was re-derived from the slip its line names. Every typed part then went through the engine's own graders in node (`grade-probe.mjs`: `numGrade` and `exprGrade` of `app/js/engine/grade.js`, with the local Compute Engine): the key, each `accept` form, each `wrong` entry on its own key, and 841 strings of my own. Those are the right answer in other forms (fraction, more or fewer places, a % sign, a unit, a letter and `=`, a true minus sign, a pound sign), the value the part's working gives after its stated rounding, and the answer one step short or from the commonest slip.

Tool results.

| check | result |
|---|---|
| authors' scripts (scratchpad venv) | `problems-estimation-numbers.py` 884 checks, 0 failures; `problems-regression-numbers.py` 1,109 checks, 0 failures; both exit 0 |
| `mine.py` (reader's keys, slips and claims) | 1,659 checks, 0 failures; 6 CLAIM lines (findings 3, 4, 12, 13, 14, 17) |
| `mine.py --sim` (overlap, 4,000 runs a case) | signal built from the past 5 days: sd of the naive $t$ 1.82, HAC with 4, 8 and 20 lags 1.19, 1.15, 1.16; independent daily signal: 1.00 (findings 14, 15) |
| `grade-probe.mjs` (engine graders) | 1,971 checks over 99 typed parts, 0 failures; 41 rows held to be faults (findings 1, 2, 5, 6, 8, 12, 18 and Engine) |
| `proposed.py` (numbers of the fixes below) | 80 checks, 0 failures |
| validator | 0 errors; on these six files only four `O2-long-sentence` advisories (estimation, all under 35 words); `manifest.json` unchanged |
| playthrough `--problems`, all six sets, `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, both course folders | 0 and 0 each; no exclamation mark, no em-dash, £ throughout |
| `fresh-check.mjs --file`, all six | 0 hits; 19 advisories read (findings 9 and 20 list what it missed) |

Result. Every key agrees with mine: all 106 parts. Every `wrong` value is the slip its line describes, lands on its own key and has a line; no two bands overlap. No explanation states a wrong value of the quantity asked. The four `wrong` findings are one band that marks a wrong answer right (1) and three false sentences, all in regression (12, 13, 14).

## A. Estimation

1. `wrong` | `estimation/problems-2.json` | `p-robot-deliveries` | `items[0].parts[2].widget` (`tol`).
   The key is 0.9, an end of the range "between 0.9 and 1", with `tol` 0.05. The grader accepts everything from 0.85 to 0.95: `0.95`, the middle of the allowed range, and `0.85`, which is outside it, are both marked right (`grade-probe.mjs`). The part's point is that the estimate sits exactly at the edge.
   Fix: question ends "Give your answer to 2 decimal places."; `tol` `{ "abs": 0.005 }` on the key and on `unrestricted` (0.75) and `top` (1). Add `{ "id": "middle", "value": 0.95, "tol": { "abs": 0.005 } }`: "You took the middle of the allowed range. $L$ falls all the way from 0.9 to 1, so the best value is the left end."

2. `unclear` | `estimation/problems-2.json` `p-currency-vol` parts 1 to 4, `estimation/problems-3.json` `p-three-month-fund` parts 1 and 3 | `widget` (no `unit`).
   Each question asks for a value "in %" (part 4 of the first "in percentage points"), and the field has no `unit`. The grader reads a typed % as a hundredth, so `0.25%`, `1.09%`, `7.84%`, `1.96%`, `2.08%` and `1.70%` are marked wrong with the generic line. The regression sets carry `unit: "%"` on the same kind of part and accept both forms. This is the class of `review-holes-1.6-2.1.md` findings 11, 18 and 19.
   Fix: add `"unit": "%"` and divide the key, its `tol`, and each `wrong` value and `tol` by 100, as `regression/problems-2.json` `p-grocer-beta` part 1 does. Keys: 0.0025, 0.010874, 0.078414, 0.0196, 0.020817, 0.016997 (currency part 1 in full: `tol` 0.00005, `by-seven` 0.002857, `sizes` 0.01).

3. `minor` | `estimation/problems-3.json` | `p-three-month-fund` | `items[1].parts[3].feedback.correct`.
   "$1.70 / 2.08 \approx 0.817$, which is $\sqrt{2 / 3}$." The explanation gives $\sqrt{2/3} \approx 0.816$ (it is 0.8165). Both are accepted, but the two lines disagree in the third place.
   Fix: "$1.70 / 2.08 \approx 0.817$. From the unrounded values it is $\sqrt{2 / 3} \approx 0.816$."

4. `minor` | `estimation/problems-2.json` | `p-tank-sensor` | `items[1].parts[0]` `wrong` `middle-two`.
   The id says middle two; the line says "That averages 50 and 55". The middle two readings are 50 and 52, whose mean is the key, 51. The value 52.5 is the mean of the last two readings.
   Fix: id `last-two`, line "That averages the last two readings, 55 and 50. Use all four."

5. `minor` | slip bands too tight for the rounded value the question itself hands over (three parts, seven entries).
   - `estimation/problems-2.json` `p-currency-vol` part 3. Part 2 asks for 2 places, so the learner holds 1.09. $1.09 \times 52 = 56.68$ and $1.09 \times \sqrt{252} = 17.30$ miss `times-52` (56.545 ± 0.005) and `trading-days` (17.262 ± 0.005) and get the generic line. The key's own band was widened to 0.02 for this reason; the slips were not.
     Fix: `times-52` 56.61 ± 0.08, `trading-days` 17.28 ± 0.03, `carried` 8.38 ± 0.02, `variance` 61.6 ± 0.2 (each takes the value from 1.0874 and from 1.09, and is clear of the key).
   - `estimation/problems-3.json` `p-three-month-fund` part 4. The question gives 1.70 and 2.08. $2.08 / 1.70 = 1.224$ misses `inverted` (1.2247 ± 0.0005) and $(1.70 / 2.08)^2 = 0.668$ misses `squared` (0.6667 ± 0.0005).
     Fix: `tol` `{ "abs": 0.0015 }` on both.
   - `estimation/problems-3.json` `p-ticket-bot` part 4. `no-root` is 27.62 ± 0.005, so 27.6 misses it.
     Fix: `tol` `{ "abs": 0.05 }`.

6. `minor` | real slips that get only the generic line.
   - `estimation/problems-2.json` `p-currency-vol` part 5: 122, from rounding 122.9 down. The regression sets name this slip (`round-down`). Add `{ "id": "round-down", "value": 122, "tol": { "abs": 0 } }`: "122 weeks leave the error just above 0.5. Round 122.9 up to 123."
   - `estimation/problems-3.json` `p-routing-test` part 3: 0.10, the lower end with its minus sign dropped. Add `{ "id": "no-sign", "value": 0.1035, "tol": { "abs": 0.01 } }`: "$1.96 \times 0.461 = 0.904$ is more than 0.8, so the lower end is below 0: $-0.10$."

7. `minor` | form sentence and placeholders.
   `chained.md` asks every numeric part to state its form. Three do not: `problems-1` `p-ping-latency` part 1, `p-reference-mass` part 1, `problems-2` `p-tank-sensor` part 1 (whole-number keys, `tol` 0). Three parts that say "Give a whole number." show the placeholder "decimal": `problems-1` `p-reference-mass` parts 2 and 3, `problems-3` `p-ticket-bot` part 3.
   Fix: end the three questions with "Give a whole number."; set the three placeholders to "whole number".

8. `minor` | `estimation/problems-1.json` | last parts of `p-ping-latency` and `p-reference-mass`.
   Both problems close on the same task, the sample size for a target standard error. It is also l2 screens 5 and 11 and `homework-1` `h-days-needed`. In `p-ping-latency` part 4 the answer, 110, is the $s^2 = 110$ printed in the question, so retyping it passes.
   Fix, numbers in `proposed.py`:
   - `p-ping-latency` part 4: "... to bring the standard error down to at most 2 microseconds? Give a whole number." Key 28. `carried` 22, `no-square` 55 ("You divided 110 by 2, not by $2^2 = 4$."), `unsquared` 5.5 ± 0.5, `round-down` 27. `feedback.correct`: "$\sqrt{110 / n} \le 2$ gives $n \ge 27.5$, so 28 pings."
   - `p-reference-mass` part 5: "Part 1's mean was 2 mg, though the true mean is 0. Using $\hat\sigma^2 = 76$ for $\sigma^2$, how many standard errors of a five-reading mean is 2 mg? Give your answer to 2 decimal places." Key 0.513 ± 0.005. `carried-90` 0.471, `carried-72` 0.527, `no-root` 0.132, `sd-not-se` 0.229, `inverted` 1.949, each ± 0.005. Explain: "The standard error of the mean of 5 readings is $\sqrt{76 / 5} \approx 3.90$ mg. So 2 mg is about 0.51 standard errors from 0, well within the noise of an unbiased scale." If part 5 is kept as it is, widen `unsquared` to 4.5 ± 0.5: today 5, which is $\sqrt{76}/2 = 4.36$ rounded up, misses it.

9. `minor` | freshness by reading: task or story reused with new numbers (`fresh-check` reports 0 hits).
   - `problems-1` `p-route-delays` parts 1 to 3: the halved estimator $\tfrac12\bar X$, its bias, variance and MSE, is l4 screens 1 to 3 ("Analyst B always reports half of it") and `review-1` `r-half-shrink`. Part 4, the cut-off, is new.
   - `problems-3` `p-ticket-bot` prose and part 1: l12 screen 11 (a desk's average as a beta prior for a new trader) with bots for traders. `exams/topic-1.6.json` `s-beta-posterior` uses $\mathrm{Beta}(12, 8)$, "worth 20 trades"; this item uses $\mathrm{Beta}(8, 12)$.
   - `problems-2` `p-currency-vol` part 4: the standard error of an annualised volatility by $\hat\sigma/\sqrt{2n}$ is l10 screen 11 and `review-3` `r-vol-se`. Part 5 is new.
   - `problems-2` `p-ride-waits` parts 1 and 2: the exponential rate by maximum likelihood is `exams/topic-1.6.json` `s-gap-mle`. Parts 3 and 4, the censored rider, are new.
   Fix: none needed where the last part is new. If one is changed, change the prior of `p-ticket-bot` so it does not mirror the exam's.

10. `minor` | coverage | `estimation/problems-1.json` | l1.
    Every other lesson of the three levels is tested by a graded part. l1 (parameter against statistic, estimator against estimate, sampling error) appears only as remarks in two explanations.
    Fix: `p-reference-mass` part 1 can carry it at no cost: "What is the sampling error $\bar x - \mu$ of the five readings' mean, in mg? Give a whole number." The key stays 2, since the true mean is 0 in these units.

11. `minor` | chain | `estimation/problems-2.json` | `p-tank-sensor` part 4.
    Part 3's result, 3.08, is used nowhere. Part 4 restates $\hat\mu$ and the sum of squares only.
    Fix: open part 4 with "Part 3 found the readings 3.08 times as likely at 51 as at 48."

## B. Regression

12. `wrong` | `regression/problems-1.json` | `p-stopping-distances` | `items[3].parts[0].feedback.byKey.reverse`.
    "That is $S_{xx}/S_{xy}$, the slope of speed on distance." It is not. The least squares slope of speed on distance is $S_{xy}/S_{yy} = 1{,}520 / 2{,}345.2 = 0.648$ (statsmodels fit in `mine.py`), as l2 screen 8 and quiz item `q-reverse` teach. $S_{xx}/S_{xy} = 0.658$ is the slope turned upside down. A learner who really regresses speed on distance types 0.65 and gets the generic line.
    Fix: `reverse` line "That is $S_{xx}/S_{xy}$, the slope turned upside down. The slope of distance on speed is $S_{xy}/S_{xx}$."; its `tol` 0.004. Add `{ "id": "other-way", "value": 0.6481, "tol": { "abs": 0.004 } }`: "That is $S_{xy}/S_{yy}$, the slope of speed on distance. For distance on speed divide by $S_{xx} = 1{,}000$."

13. `wrong` | `regression/problems-1.json` | `p-stopping-distances` | `items[3].parts[4].widget.options` `outlier` `why`.
    "It is no larger than the misses at the ends." The residual at 40 mph is $-3.4$ m; the end misses are $+3.0$ and $+3.2$ m, both listed in the question. It is the largest of the five.
    Fix: "It is about the size of the misses at the ends, 3.0 and 3.2 m. All five residuals follow one smooth arch."

14. `wrong` | `regression/problems-3.json` | `p-overlap-signal` | `items[2].parts[3].explain`.
    "HAC errors with at least 4 lags would give much the same." They would not. In 4,000 simulated fits of a next-5-day return on a signal built from the past 5 days, with no true effect, the naive $t$ has sd 1.82, as the factor $\sqrt{3.4} = 1.84$ says. With HAC errors the sd is still 1.19, 1.15 and 1.16 at 4, 8 and 20 lags, and a true zero is rejected about 10% of the time (`mine.py --sim`). So HAC turns a naive 3.5 into about 2.3, above 1.96, not 1.90. With the part's own autocorrelations, Bartlett weights at 4 lags give a factor of 1.61, not 1.84. The course's own l11 screen 10 says HAC under-corrects ("cut that to 12%, still above 5%").
    Fix: "Overlap makes neighbouring residuals share news, so the naive error is too small by a factor of about 1.844. Dividing gives an honest $t$ of about 1.90. HAC errors go only part of the way: in simulation they still reject a true zero about one time in ten."

15. `unclear` | `regression/problems-3.json` | `p-overlap-signal` prose and part 4; `p-bond-fund-weeks` part 5 `cautious` `why`.
    The factor $\sqrt{1 + 2\sum (1 - j/h)^2}$ holds when the predictor overlaps as the returns do. `homework-3` `h-overlap10` says so ("overlapping $h$-day returns on overlapping $h$-day returns") and l11 screen 10 uses a past-20-day return. The problem says only "two signals". For a signal that is fresh each day the naive $t$ is honest: its sd is 1.00 in the same simulation. Part 4's "so the naive $t$ is too big by a factor of about" is then a general statement without its hypothesis. The same holds for "Positive autocorrelation makes the usual errors too small" in `p-bond-fund-weeks`; l11's summary says "usually".
    Fix: prose, after the first sentence: "Each signal is a 5-day rolling average, so it shares 4 days with its neighbour." Part 4 opens "The returns and the signals both overlap by 4 days in 5, so the naive $t$ is too big by a factor of about ...". `cautious` line: "With residuals and predictors that both echo, the usual errors are too small: 8 echoing weeks hold less news than 8 independent ones."

16. `unclear` | `regression/problems-2.json` | `p-freight-summary` | `items[1].parts[0].question`.
    "With one predictor, $F = \mathrm{ESS}/s^2$" does not say what ESS is. l3, l12, `review-1` and `problems-1` call the explained sum SSR; only one derivation screen of l7 uses ESS. The part cannot be started without the definition. `problems-3` `p-solar-output` spells it out in its question and then prints "ESS" in feedback.
    Fix: "With one predictor, $F = \mathrm{ESS}/s^2$. ESS is the explained sum of squares, lesson 3's SSR, and $s^2 = \mathrm{SSE}/(n - 2)$. What is $F$? Give your answer to 2 decimal places."

17. `minor` | `regression/problems-3.json` | `p-bond-fund-weeks` | `items[3].parts[3].explain`.
    $1 - d/2$ gives 0.89, but the lag-1 autocorrelation of the eight residuals, worked directly, is 0.73. The two end terms, $(e_1^2 + e_8^2)/\sum e_t^2 = 0.32$, are what $d \approx 2(1 - \hat\rho)$ drops, and at $n = 8$ they are large. The verdict stands either way.
    Fix: "Halve $d$ and take it from 1, which gives $\hat\rho \approx 0.89$. With only 8 weeks the rule is rough: the lag-1 correlation worked directly is 0.73. Either way, each week's miss carries most of the week before's."

18. `minor` | real slips that get only the generic line (seven parts).
    Five are a negative key typed without its sign; `p-gas-demand` part 1, `p-car-prices` part 2 and `p-grocer-beta` part 3 name that slip, these do not. Entries to add, each clear of the key and of the bands already there (`proposed.py`):
    - `problems-1` `p-car-prices` part 4: `no-sign` 1230, `tol` 0: "The slope is still negative: older cars sell for less. $-1{,}480 + 250 = -1{,}230$." (Moot if finding 19 is applied.)
    - `problems-1` `p-stopping-distances` part 2: `no-sign` 21.4 ± 0.05: "The intercept is negative: $39.4 - 60.8 = -21.4$."
    - `problems-3` `p-solar-output` part 2: `no-sign` 0.5 ± 0.005: "$45 - 60 = -15$, so $b_2$ is negative: $-0.5$."
    - `problems-3` `p-bond-fund-weeks` part 1: `no-sign` 0.006 ± 0.00005: "The yield rise costs more than the spreads give back, so the prediction is negative: $-0.60\%$."
    - `problems-2` `p-raw-intercept` part 4: `extra` 105, `tol` 0: "That is the months still to add. The question asks for the whole record: 205."
    - `problems-3` `p-power-price` part 4: `extra` 113, `tol` 0: "That is the extra days. The fit needs 313 in all."
    - `problems-3` `p-overlap-signal` part 4: `root-h` 1.5652 ± 0.005: "You divided by $\sqrt 5$. The factor is $\sqrt{1 + 2 \times 1.2} = \sqrt{3.4}$." (l11 names this slip, `sqrt20`.)

19. `minor` | `regression/problems-1.json` | `p-car-prices` | `items[1].parts[3]`.
    "Part 2 gave a slope of $-£1{,}480$ a year, and part 3 a rise of £250. What is the corrected slope?" The last part of a difficulty 4 is one addition of two numbers printed in the question.
    Fix: "Part 2 gave $-£1{,}480$ a year and part 3 a rise of £250, so the corrected slope is $-£1{,}230$ a year. The corrected prices average £14,000. What price does the corrected line give a 9-year-old car? Give a whole number of pounds." Key 7850. `old-slope` 6600, `raw-x` 2930, `wrong-way` 5350, `old-mean` 7517 ± 1 ("You used the old mean price, £13,667. The correction lifts the mean to £14,000."). Explain: "The line passes through the mean point, $(4, 14{,}000)$, and 9 is 5 years on: $14{,}000 - 6{,}150 = £7{,}850$. The car sold for £8,200, only £350 above its own line. A far point pulls the line towards itself."

20. `minor` | freshness by reading: task reused with new numbers (`fresh-check` reports 0 hits; two of these it lists as advisories).
    - `problems-3` `p-power-price` part 4: `homework-3` `h-vif-n`, the same question ("shrinks variances in proportion to $1/n$", the sample that matches uncorrelated predictors), with months for days.
    - `problems-3` `p-overlap-signal` parts 2 to 4: `review-3` `r-t` ($s^2$, a diagonal entry, a coefficient, then $t$), `homework-3` `h-overlap10` (the same factor at $h = 10$) and the story of l11 screen 10. The author's report judges this "only the taught tool is shared".
    - `problems-3` `p-bond-fund-weeks` parts 3 and 4: l11 screen 4, which also has eight residuals, four positive then four negative, $d$ and then $\hat\rho \approx 1 - d/2$.
    - `problems-2` `p-sunny-cones` part 4: l5 screen 6 ("each $x$ ... is observed four times", $s$ kept).
    - `problems-2` `p-raw-intercept` part 4: `exams/topic-1.6.json` `s-alpha-years` (how long until an alpha's $t$ reaches 2, with $\mathrm{SE} \approx s/\sqrt n$).
    Fix: accept the last three, where the chain before them is new. For `p-power-price` part 4: "The two-predictor fit reports a standard error of 0.05 for the gas slope. Using $\mathrm{VIF} = 1.5625$, what would it be with uncorrelated predictors, the same spreads and the same noise? Give your answer to 3 decimal places." Key 0.04; `by-vif` 0.032, `times` 0.0625, `times-vif` 0.0781, each ± 0.0005. For `p-overlap-signal`, finding 15's new prose already separates it from the homework item.

## Per set

- Coverage: every lesson of each level is drawn on by a graded part, apart from estimation l1 (finding 10). Every problem draws on at least two lessons; the reports' tables agree with my reading. Each set has a 5.
- Chains: all 24 are real chains and each later part restates what it needs. Results not used later: finding 11. Last parts that are weak: findings 8 and 19.
- Typed parts: 17 of 18, 17 of 17, 14 of 16 (estimation); 18 of 19, 16 of 17, 17 of 19 (regression). Each choice part is a judgement. No option is given away by length or refers to another by place.
- Only ideas taught: the censored likelihood (`p-ride-waits` part 3) and the interval for a difference of two means (`p-routing-test`) are new to their levels, and each question hands over the one fact it needs. $\mathrm{SE}(\hat\sigma) \approx \hat\sigma/\sqrt{2n}$ is taken as given in l8, as here; over 200,000 normal samples of 8 the sd of $\hat\sigma$ is $0.245\sigma$ against the rule's $0.25\sigma$.
- Theory checked and found sound: the blend's cross term vanishes because one lab is unbiased and the labs are independent; the known-mean variance divides by $n$; the restricted MLE sits at the edge; the bootstrap standard error of a mean is $\sqrt{(n-1)/n}$ of $s/\sqrt n$; the posterior mean's weights; $s_y\sqrt{1 - r^2}$ is the residual sd with the divisor of $s_y$; $F = t^2$ and $F = \tfrac{R^2}{1 - R^2}(n - 2)$ with a constant and one predictor; the raw intercept is $\alpha + (1 - \beta)r_f$ with the same slope; the short regression's slope is $b_1 + b_2\delta$; with two predictors $R_j^2 = r^2$; statsmodels' `scale` is $\mathrm{SSE}/(n - k - 1)$; the eight bond-fund residuals add to 0.

## Engine

- A unit typed in full after the number still stops the field (eleven probe rows): `-12 GWh per °C`, `-12 GWh/°C`, `1.52 m per mph`, `1.5 cones per hour`, `2.5 MWh per hour`, `-£1,480 a year`, `-1480 pounds a year`, `0.35% a month`, `0.25 per minute`, `1.96 percentage points`, `6.8 h`. Already raised twice (inbox, "review holes 1.6 and 2.1" and "problems regression").
- A plus sign before a positive number is not read: `+42`, `+250`, `+2` stop the field. Residuals and changes are where a learner types one.
- `\ell(\lambda) =` or `\ell =` before an expression answer is not dropped as a label, though `L(p) =` and `l(\lambda) =` are (`p-ride-waits` part 1 asks for "the log-likelihood $\ell(\lambda)$").

## Counts

| tag | estimation | regression |
|---|---|---|
| wrong | 1 | 3 |
| unclear | 1 | 2 |
| minor | 9 | 4 |

Finding classes seen three times or more: a % sign refused where the question asks "in %" and the part has no `unit` (6 parts; with `review-holes-1.6-2.1.md` a fourth sighting); a negative key with no line for the dropped sign (5 parts); a slip band narrower than the gap between the exact value and the rounded value the question hands over (7 entries); a task reused with new numbers that `fresh-check` passes (9 items); a false sentence in a feedback, `why` or explanation, with every key right (3, all regression).

Clean problems (no finding at all): estimation `p-sulphur-labs`, `p-email-clicks`; regression `p-gas-demand`, `p-smudged-shift`, `p-grocer-beta`.

## Fix pass

Scope: `app/content/courses/estimation/problems-1.json` to `-3` and `regression/problems-1.json` to `-3` only, by targeted edits (a scripted load, edit and dump that round-trips each file byte for byte before the change). I recomputed every changed number twice before writing it, and every one of them, with the numbers in feedback and `wrong` strings, is now a check in `docs/reports/problems-estimation-numbers.py` (1,080 checks) and `docs/reports/problems-regression-numbers.py` (1,202 checks): method 1 exact (fractions, closed forms), method 2 by another route (a root search, a loop over n, the raw readings, statsmodels fits, a seeded simulation). Each re-authored part also has a stale-value check (the old key, the old slips and the old wording must be gone). Both scripts exit 0 with the scratchpad venv. I disputed nothing: every reader key and slip value agreed with my own recomputation.

Status: fixed 20, disputed 0, deferred 0 (three engine items, already in the inbox, listed last).

### A. Estimation

1. Fixed. `p-robot-deliveries` part 3 now asks for 2 decimal places, with `tol` 0.005 on the key, `unrestricted` (0.75) and `top` (1), and a new `middle` entry (0.95 +- 0.005, the reader's line). In the real grader (`numGrade`) 0.9, 0.90, 9/10 and 90% pass; 0.95 lands on `middle`; 0.85, 0.91 and 0.92 get the generic line. Both methods agree the key is 0.9, and L falls from 0.9 to 1 (script).
2. Fixed. `unit: "%"` on `p-currency-vol` parts 1 to 4 and `p-three-month-fund` parts 1 and 3. The key, its `tol` and every `wrong` value and `tol` are divided by 100 (0.0025, 0.010874, 0.078414, 0.0196; 0.020817, 0.016997). The field supports `unit` for numeric parts, so the percent-sign `wrong` line was not needed. Tested in the real grader: each key, typed as 0.25 and as 0.25%, passes, and each `wrong` value lands on its own line with and without the % sign (`probe-fix.mjs`, 210 checks, 0 failures).
3. Fixed. `p-three-month-fund` part 4 `feedback.correct`: "$1.70 / 2.08 \approx 0.817$. From the unrounded values it is $\sqrt{2 / 3} \approx 0.816$." Script: 0.8165 rounds to 0.817 from the rounded SEs and to 0.816 from the exact ratio.
4. Fixed. `p-tank-sensor` part 1 `middle-two` is now `last-two`, "That averages the last two readings, 55 and 50. Use all four." Script: the last two readings average 52.5, the middle two (50 and 52) average the key 51.
5. Fixed. `p-currency-vol` part 3: `times-52` 0.5661 +- 0.0008, `trading-days` 0.1728 +- 0.0003, `carried` 0.0838 +- 0.0002, `variance` 0.616 +- 0.002 (all in the fraction scale of finding 2, that is 56.61 +- 0.08, 17.28 +- 0.03, 8.38 +- 0.02, 61.6 +- 0.2 per cent). Each band takes the slip worked from the exact figure and from the 1.09 (or 1.16) that part 2 hands over, and is clear of the key (script and grader). `p-three-month-fund` part 4: `inverted` and `squared` `tol` 0.0015 (take 2.08 / 1.70 = 1.224 and (1.70 / 2.08)^2 = 0.668 as well as 1.2247 and 0.6667; the key and `same` stay clear). `p-ticket-bot` part 4: `no-root` `tol` 0.05 (takes 27.6 and 27.62). Four wrong-band follow-on edits are in finding 7.
6. Fixed. `p-currency-vol` part 5 `round-down` (122, tol 0; 7.84 / sqrt(244) = 0.502 > 0.5, 7.84 / sqrt(246) = 0.4999) with the reader's line. `p-routing-test` part 3 `no-sign` (0.1035 +- 0.01; 1.96 x 0.461 = 0.904 > 0.8) with the reader's line.
7. Fixed. "Give a whole number." added to `p-ping-latency` part 1, `p-reference-mass` part 1 (rewritten, finding 10) and `p-tank-sensor` part 1. Placeholders "whole number" on `p-reference-mass` parts 2 and 3 and `p-ticket-bot` part 3. Follow-on: the validator then flagged four slip bands narrower than the whole-number rounding, so `by-four` 387.5 became 387.75 +- 0.25, `by-four` 2.5 became 2.75 +- 0.25, `sizes` 8.4 became 8.2 +- 0.2 and `last-two` 52.5 became 52.75 +- 0.25 (each still takes the exact slip and its rounding, and is clear of the key). The script's integer-key check now requires the sentence and a non-decimal placeholder on every such part.
8. Fixed, both parts re-authored as the reader proposed. `p-ping-latency` part 4: "at most 2 microseconds", key 28 (root 27.5; 28 pings give 1.98, 27 give 2.02), `carried` 22, `no-square` 55, `unsquared` 5.5 +- 0.5 (takes 5.24), `round-down` 27; the old `from-se` entry went (22 is now `carried`). Question shortened to "Using $s^2 = 110$ again, how many pings bring the standard error down to at most 2 microseconds? Give a whole number." `p-reference-mass` part 5: "how many standard errors of a five-reading mean is 2 mg? Give your answer to 2 decimal places", key 0.513 +- 0.005 (exact 0.51299, also from the raw readings), `carried-90` 0.471, `carried-72` 0.527, `no-root` 0.132, `sd-not-se` 0.229, `inverted` 1.949, each +- 0.005; the old `unsquared` slip went. Stale checks: the old key 19 and 110, "1 microsecond" and "readings must the lab average" are gone.
9. Decisions (I list each; no change where the last part is new, as the reader says). `p-route-delays` parts 1 to 3 (halved estimator, l4 screens 1 to 3 and `r-half-shrink`): left, part 4 (the cut-off) is new and the reader asks for no change. `p-ticket-bot` (l12 screen 11 with bots for traders; exam `s-beta-posterior` uses Beta(12, 8)): left, part 4 (the gap in standard errors) is new and the prior Beta(8, 12) already differs from the exam's. `p-currency-vol` part 4 (l10 screen 11 and `r-vol-se`): left, part 5 is new. `p-ride-waits` parts 1 and 2 (exam `s-gap-mle`): left, parts 3 and 4, the censored rider, are new. Fresh-check on the changed sets: 0 hits.
10. Fixed. `p-reference-mass` part 1 now asks "Here $\mu = 0$ mg above 50 g. What is the sampling error $\bar x - \mu$ of the five readings' mean, in mg? Give a whole number." Key 2 unchanged; `correct`, `generic` and `explain` rewritten for it. l1 is now tested by a graded part.
11. Fixed. `p-tank-sensor` part 4 opens "Part 3 found the readings 3.08 times as likely at 51 as at 48." (script: e^1.125 = 3.08).

### B. Regression

12. Fixed. `p-stopping-distances` part 1: `reverse` line "That is $S_{xx}/S_{xy}$, the slope turned upside down. The slope of distance on speed is $S_{xy}/S_{xx}$." with `tol` 0.004, and a new `other-way` (0.6481 +- 0.004, the reader's line). Basis, a computation: statsmodels' least squares slope of speed on distance is 0.64813 = $S_{xy}/S_{yy}$ = 1,520 / 2,345.2 (both in the script), while $S_{xx}/S_{xy}$ = 0.65789 is the reciprocal of the slope of distance on speed. The two bands (0.6579 +- 0.004 and 0.6481 +- 0.004) do not meet; in the grader 0.65 and 0.648 land on `other-way`, 0.66 and 0.658 on `reverse`.
13. Fixed. `p-stopping-distances` part 5 `outlier` `why`: "It is about the size of the misses at the ends, 3.0 and 3.2 m. All five residuals follow one smooth arch." Script: |-3.4| exceeds 3.0 and 3.2 by under 0.5.
14. Fixed. `p-overlap-signal` part 4 explain now reads "... an honest $t$ of about 1.90. HAC errors go only part of the way: in simulation they still reject a true zero about one time in ten." Basis, a simulation I ran (2,000 runs, 503 days, next-5-day return on a past-5-day signal, no true effect; route 1 statsmodels `cov_type="HAC"` for 200 runs, route 2 a hand-coded Newey-West sandwich with Bartlett weights for all 2,000; the two agree to 1e-9): the naive $t$ has sd 1.88 (the factor is 1.844); the HAC $t$ has sd 1.23, 1.19 and 1.20 at 4, 8 and 20 lags and rejects |t| > 1.96 in 12%, 11% and 11% of runs. So HAC turns a naive 3.5 into about 2.2, not 1.90, which is the course's own l11 screen 10 ("cut that to 12%, still above 5%"). The sentence "would give much the same" is gone. The numbers script asserts the simulation ranges, so a reversion fails it.
15. Fixed. `p-overlap-signal` prose gains "Each signal is a 5-day rolling average, so it shares 4 days with its neighbour." and part 4 opens "The returns and the signals both overlap by 4 days in 5. The naive $t$ is then too big by a factor of about ...". Basis, the same simulation: an independent daily signal gives a naive $t$ with sd 1.00, so the factor needs the overlapping signal. `p-bond-fund-weeks` part 5 `cautious` `why`: "With residuals and predictors that both echo, the usual errors are too small: 8 echoing weeks hold less news than 8 independent ones." Basis, a simulation (3,000 runs, n = 200, AR(1) errors with rho 0.9, true slope 0): the true sd of the slope over the mean usual SE is 1.01 for an independent predictor and 3.01 for a predictor with rho 0.9 (the textbook factor $\sqrt{(1 + \rho_e\rho_x)/(1 - \rho_e\rho_x)}$ = 3.09).
16. Fixed with the course's term. l3 defines SSR as the explained sum $\sum(\hat y_i - \bar y)^2$ and l7 uses ESS on one screen, so `p-freight-summary` part 1 now reads "$F = \mathrm{SSR}/s^2$, where SSR is the explained sum of squares and $s^2 = \mathrm{SSE}/(n - 2)$", and its `correct`, `generic` and `explain` say SSR. Script: statsmodels `ess` over `ssr / 40` equals `fvalue`, and no "ESS" is left in the item.
17. Fixed. `p-bond-fund-weeks` part 4 explain now carries the 0.73. Script: $\sum e_te_{t-1}/\sum e_t^2$ = 0.728 by hand and by statsmodels `acf`; the end terms $(e_1^2 + e_8^2)/\sum e_t^2$ = 0.321.
18. Fixed. New dropped-sign lines: `p-stopping-distances` part 2 `no-sign` (21.4 +- 0.05), `p-solar-output` part 2 `no-sign` (0.5 +- 0.005), `p-bond-fund-weeks` part 1 `no-sign` (0.006 +- 0.00005, the fraction scale of its % unit), `p-raw-intercept` part 4 `extra` (105, tol 0), `p-overlap-signal` part 4 `root-h` (1.5652 +- 0.005). Moot: `p-car-prices` part 4 `no-sign` (the part is re-authored, finding 19) and `p-power-price` part 4 `extra` (re-authored, finding 20). All are clear of their keys and of the entries already there (script and grader).
19. Fixed as proposed. `p-car-prices` part 4 now asks for the corrected line's price at 9 years: key 7850 (14,000 - 1,230 x 5; also a `polyfit` of the corrected prices), `old-slope` 6600, `raw-x` 2930, `wrong-way` 5350, `old-mean` 7517 +- 1. Stale checks: "corrected slope?", -1430 and -1030 are gone.
20. Decisions. `p-power-price` part 4 re-authored (the reader judges it the same question as `homework-3` `h-vif-n`): "The two-predictor fit reports a standard error of 0.05 for the gas slope. Using VIF = 1.5625, what would it be with uncorrelated predictors, the same spreads and the same noise? Give your answer to 3 decimal places." Key 0.04 (0.05 / 1.25; method 2 divides 0.05 by the ratio of the gas slope's standard errors from the correlated and uncorrelated synthetic fits), +- 0.0005; `by-vif` 0.032, `times` 0.0625, `times-vif` 0.0781, `carried` 0.0439 (a VIF of 1.2994 from part 3's slip), each +- 0.0005. Stale checks: 313, 312, 250, 500, 260, "days" and the "1/n" sentence are gone. `p-overlap-signal` parts 2 to 4: no further change, finding 15's prose separates it from `h-overlap10`. `p-bond-fund-weeks` parts 3 and 4, `p-sunny-cones` part 4, `p-raw-intercept` part 4: accepted as the reader advises (the chain before each is new). Fresh-check on the changed sets: 0 hits and only shared-formula advisories.

Engine (deferred, already raised in the inbox): units typed in full after a number stop the field; a plus sign before a positive number is not read; `\ell(\lambda) =` before an expression is not dropped as a label.

### Every graded answer, band or item that changed

- Graded answers (keys) changed: `p-ping-latency` part 4 (110 to 28); `p-reference-mass` part 5 (19 to 0.513); `p-car-prices` part 4 (-1230 to 7850); `p-power-price` part 4 (313 to 0.04). Graded questions reworded with the key unchanged: `p-reference-mass` part 1 (2, now the sampling error); `p-freight-summary` part 1 (10, ESS to SSR); `p-robot-deliveries` part 3 (0.9, now to 2 places).
- Key rescaled to a `unit: "%"` field (the typed value in per cent is unchanged, and a typed % sign is now accepted): `p-currency-vol` parts 1 to 4, `p-three-month-fund` parts 1 and 3, each with its band and all its `wrong` values.
- Bands changed: `p-robot-deliveries` part 3 key 0.05 to 0.005, `unrestricted` 0.05 to 0.005, `top` 0.04 to 0.005; `p-currency-vol` part 3 four slip bands (finding 5); `p-three-month-fund` part 4 `inverted` and `squared` 0.0005 to 0.0015; `p-ticket-bot` part 4 `no-root` 0.005 to 0.05; `p-stopping-distances` part 1 `reverse` 0.005 to 0.004; `p-ping-latency` part 1 `by-four`, `p-reference-mass` part 1 `by-four` and `sizes`, `p-tank-sensor` part 1 `last-two` (finding 7).
- New `wrong` entries: `p-robot-deliveries` part 3 `middle`; `p-currency-vol` part 5 `round-down`; `p-routing-test` part 3 `no-sign`; `p-stopping-distances` part 1 `other-way`, part 2 `no-sign`; `p-raw-intercept` part 4 `extra`; `p-solar-output` part 2 `no-sign`; `p-bond-fund-weeks` part 1 `no-sign`; `p-overlap-signal` part 4 `root-h`. Renamed: `p-tank-sensor` part 1 `middle-two` to `last-two`. New `wrong` sets with the re-authored parts: `p-ping-latency` part 4, `p-reference-mass` part 5, `p-car-prices` part 4, `p-power-price` part 4.
- Text only (no key or band change): `p-three-month-fund` part 4 `correct`; `p-stopping-distances` part 1 `reverse` line, part 5 `outlier` `why`; `p-overlap-signal` prose, part 4 question and explain; `p-bond-fund-weeks` part 4 explain, part 5 `cautious` `why`; `p-tank-sensor` part 4 question; placeholders on `p-reference-mass` parts 2 and 3 and `p-ticket-bot` part 3.

### Gates

- Number scripts, scratchpad venv: `problems-estimation-numbers.py` 1,080 checks, 0 failures, exit 0; `problems-regression-numbers.py` 1,202 checks, 0 failures, exit 0.
- Reader's scripts rerun: `mine.py` keeps its table of the old keys, so its 61 FAIL lines are exactly the changed parts (the `%` rescales, the re-authored parts, and each new `wrong` entry "not in my table"), and its six CLAIM lines now describe text that is gone (findings 3, 4, 12, 13, 14, 17); `proposed.py` 89 checks, its only 8 failures are each new entry meeting itself, and its listings of missing form sentences and "decimal" placeholders on whole-number parts are empty; `grade-probe.mjs` 26 failures, all rows for old keys of the re-authored parts, and its 19 findings are the three engine items. A new probe of every changed part in the engine's own `numGrade`, `probe-fix.mjs` in the scratchpad, 210 checks, 0 failures.
- Validator: 0 errors; no new warning on these files (three `O2-long-sentence` advisories remain, all in untouched questions, one fewer than before); `manifest.json` unchanged.
- Voice scan 35: estimation 0 and 0, regression 0 and 0.
- Playthrough `--problems --local-cdn`, all six sets, desktop and `--mobile`: all passed.
- `fresh-check.mjs --file` on the changed sets: 0 hits.
