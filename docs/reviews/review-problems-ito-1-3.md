# Problem sets 3.2, ito levels 1 to 3: second-reader findings

Scope: `app/content/courses/ito/problems-1.json`, `-2`, `-3`: 9 problems, 36 parts (32 numeric, 2 `expression`, 2 choice), 93 `wrong` entries. Rules: `docs/briefs/wave-c-reader-ag.md`, `docs/briefs/chained-prompts.md`, `docs/briefs/chained.md`. Pattern: `review-problems-analysis-1-3.md`.

## Verdict per problem

| problem | closest lesson screen | quiz | review | homework | other set | exam | verdict |
|---|---|---|---|---|---|---|---|
| p-maker-tally | l1 S7 (biased coin, drift of the mean path) | l1 q-fine-walk | r-var-horizon (sd by $\sqrt t$) | **h-drift-below** ($X_t = 0.5t + W_t$, chance of being down) | none | e-qv-drift | `reuse`: finding 1 |
| p-quarter-rally | l4 S3, S4 (mean, $P(S_1 < 100)$); l2 S3 (independent increments) | l4 q-median then q-mean, the same share in a row | r-gbm-above | none conditions on an earlier price | p-results-vol parts 3 and 4 (median, loss chance) | s2-gbm-median | `clean`, the closest call: parts 2 to 4 are q-median, q-mean and l4 S4 in order, but restarted at $t = 0.25$, which no item does |
| p-realised-then-risk | l3 S11 (126 days, $\sum r^2 = 0.02036$) | l3 q-qv-var | r-qv-sd | **h-realised-vol** (63 days, $\sum r^2 = 0.0144$) | p-quarter-rally part 4 | none (r-dig110 of review-4 holds $\ln(60/64)$, a call struck at 64 from 60) | `reuse`: finding 2 |
| p-cable-inverse | l6 S4 and S5 ($d(S^2)$, then $dm = (2\mu + \sigma^2)m\,dt$) | l6 q-ln-s, l8 q-exp-mean | r-dlns, r-disc | h-moment-order ($E[S^p]$ for all $p$; parts 1 and 2 are $p = -1$), h-discount | none | e-pick-martingales | `clean` as a chain (the product $e^{\sigma^2T}$ and the drift solved for are new); one retold line, finding 8, and a weak last part, finding 6 |
| p-cube-path | l5 S4 (square the path step by step, telescope); l8 S3 table ($W^3$ drifts at $3W$) | l5 q-left-small | r-left-sum | h-iso-w2 | none | e-pick-martingales (option $W_t^3 - 3\int W\,ds$) | `reuse`: findings 5 and 7 |
| p-results-vol | l7 S8 ($\sigma(t) = 0.1 + 0.2t$) | l5 q-det | r-iso-det | none | p-quarter-rally | s2-gbm-median (slip line, finding 3) | `clean`; band, finding 4 |
| p-touch-note | l9 S5 (forward checked in the equation); l16 S5 (power claim, $S_0 = 80$, $r = 4\%$, $\sigma = 25\%$) | l9 q-vt, q-hedge ("How many shares does it hold") | r-pde-vt | h-pde-check | none | e-cubed-claim part 2 (the power with no time decay, $m = -2r/\sigma^2$) | `clean` as a chain; shared parameter set, finding 10 |
| p-digital-measures | l10 S2 ($\theta$); l11 S8 (digital); **l11 S5 (a junior, real drift, discounted at $r$)**; l16 S3 (digital put) | l10 q-theta, l11 q-digital | r-digital, r-dig110 | h-girsanov-ratio ($P$ and $Q$ scores 0.24 apart) | none | none | `re-author`: finding 11 |
| p-one-touch | **l12 S1 (reflection), S8 (parity), S3 and S9 (shift)** | l12 q-touch, q-shift | r-touch, r-parity, r-digital | h-touch-shift | none | **e-daily-touch**, s3-touch | `re-author`: finding 12 |

Two of nine are ruled `re-author` (`p-digital-measures`, `p-one-touch`), three `reuse` with exact fixes, four `clean`.

Method. The author's script was run first. I then read each set part by part and worked every part by hand from its text. `docs/reports/problems-ito-numbers-read.py` rebuilds every key, every `wrong` value and the printed working, importing nothing from the author's script: $\Phi$ from `erfc` and again by Simpson's rule, the 625 trades by their exact binomial law, lognormal chances also by seeded simulation, both Itô coefficients by sympy, the path sums in exact fractions, the note's exponent by the first-passage transform, the touch chances by a fine-grid and a daily simulation. It uses no root finder. It also checks each band: the stated rounding and the rounded route are taken, each `wrong` value is refused by the key and no two bands meet, and a part that names a table takes the reading at $z$ to 2 places. For reuse I read the learner-facing text of l1 to l17, `review-1` to `-4`, `homework-1` to `-4` and the 13 exam items carrying an `it-` skill (`topic-3.2`, `mock-superday-strats`), searched them for each problem's numbers, nouns and letters, and ran a 5-word run comparison of every line of the sets against them (scratch `read-ito/ngram.py`), reading each hit.

## Tool results

| check | result |
|---|---|
| author's script | `problems-ito-numbers.py` 956 of 956, exit 0 |
| reader's script | `problems-ito-numbers-read.py` 420 checks, exit 0, 4 `FINDING` lines (findings 1, 4, 9, 5) |
| validator | 0 errors, 4,561 warnings; **2 on these files**, both `[table-source]` (findings 4 and 9). The author's report says none. `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 (8,553 sentences) |
| `fresh-check.mjs --files` three sets, `--pairs` | 0 hits, 4 advisories, as the author lists |
| `grade-all.mjs --file`, three sets | 12 widgets each, 0 failures |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 32 numeric keys, both expression keys and both choice keys agree with mine, as do all 93 `wrong` values and every number in a feedback or explanation line. No learner who works as told with software is marked wrongly: no `wrong`-tagged finding. Two parts name a normal table and refuse its reading (findings 4, 9). One part can be read off its own question (finding 5). Every claim holds: the fixed sum of squares, $2T\Delta t$, the reflection principle for a driftless log price, the general solution $AS + BS^{-1.28}$, the shift $\theta\sqrt T$ between the $P$ and $Q$ scores, parity of the two notes paid at expiry. Each definition matches its lesson's wording. Each later part restates its value, except `p-one-touch` part 4 (noted in finding 12). The percentage parts carry unit "%". The main faults are reuse.

Severities: `wrong`, `misleading`, `reuse`, `voice`, `continuity`.

## A. `problems-1`

1. `reuse` | `ito/problems-1.json` | `p-maker-tally` | `items[0]`, prose and parts 1 to 4 | the model is a homework item's process in other units.
   `homework-1` `h-drift-below`: "A strategy's cumulative P&L, in £ thousand, is modelled as Brownian motion with drift: $X_t = 0.5t + W_t$ ... What is $P(X_4 < 0)$, the chance the strategy is down after four months?" Its explanation ends "the chance of being down falls as the horizon grows: $\Phi(-0.5\sqrt t)$". Parts 1 and 2 here build $X_t = 500t + 1000W_t$ in pounds, which is that process times 1,000, and part 4 asks the chance of being down at $t = 5$: the homework's printed rule gives the key, $\Phi(-0.5\sqrt5) = 0.1318$. The slips match too: 0.3085 and 0.5 are `wrong` values of both. One slip line is the l1 quiz line with the number changed (l1 S10 `linear`, and `r-var-horizon`: "Independent days add variances, so the sd grows by $\sqrt{10}$ only").
   Fix (numbers under `PROPOSED finding 1` in my script): win chance 0.507, so the drift over $\sigma$ is 0.35.
   - Prose: "... gaining with chance 0.507, independently of the others ..."
   - Part 1: `answer` 350. `wrong`: `wins-only` 12675, `half-edge` 175, `per-trade-count` 8.75. `correct`: "Each trade has mean $40(0.507 - 0.493) = 0.56$ pounds, so 625 trades expect $625 \times 0.56 = 350$." `wins-only`: "... The 49.3% of losing trades each hand £40 back." `half-edge`: "The edge per trade is the gap between the two chances, 0.014, not half of it." `per-trade-count`: "That is the edge counted in trades, $625 \times 0.014$. Each trade is worth £40, so multiply by 40 as well." `explain`: "A trade's mean is $40 \times 0.507 - 40 \times 0.493 = 0.56$ pounds. Means add across independent trades. The day's mean is $625 \times 0.56 = 350$."
   - Part 2: `wrong` `variance` 999804; its line: "That is the day's variance, $625(1600 - 0.56^2)$. ..."
   - Part 3: question "Model the P&L as $X_t = 350t + \sigma W_t$ ..."; `explain` "The drift $350t$ is fixed ...". `sd-times-t` line: "You multiplied the sd by 5. The variance is what grows fivefold; its root grows by $\sqrt5$."
   - Part 4: question "The week's mean is $5 \times 350 = 1{,}750$. Using the sd 2,236.07 from part 3, what is the chance the week ends down? Take $\Phi$ from software and give 4 decimal places." `answer` 0.216924. `wrong`: `sd-times-t` 0.3632, `no-drift` 0.5, `ends-up` 0.7831, `one-day` 0.0401. `correct`: "A loss is $X_5 < 0$: $z = -1750/2236.07 = -0.7826$, and $\Phi(-0.7826) \approx 0.2169$." Replace $-1.1180$ by $-0.7826$ in `sd-times-t` and `ends-up`, and £2,500 by £1,750 in `no-drift`. `explain`: "The week's P&L is normal with mean 1,750 and sd 2,236.07. Zero sits $1750/2236.07 = 0.7826$ sds below the mean. The lower tail is $\Phi(-0.7826) \approx 0.2169$."
   The table is dropped from part 4 because its reading at $z = -0.78$ (0.2177) would miss the band. None of 0.2169, 0.7831, 0.0401, 12675 or 999804 occurs in the course or the exams; 0.3632 occurs only among path values of l3, l5, l6 and l9, which the fixer should confirm.

2. `reuse` | `ito/problems-1.json` | `p-realised-then-risk` | `items[2].prose`, `items[2].parts[0].question` | the stem retells a homework stem sentence for sentence.
   `homework-1` `h-realised-vol`: "Over one quarter, 63 trading days or $T = 0.25$ years, a share's squared daily log returns add to $\sum r^2 = 0.0144$." and "Estimate its annual volatility $\sigma$ from the quadratic variation. Give 2 decimal places." Here: "Over the last 84 trading days, a third of a year, a share's squared daily log returns add to 0.0147." and "Estimate the annual volatility $\sigma$ from the quadratic variation. Give a decimal to 2 places." l3 S11 asks the same of 126 days. Only the numbers differ. The task may stay (it feeds parts 2 to 4, which no item runs); the sentences may not.
   Fix, prose: "A risk system keeps 84 daily log returns of a share, a third of a trading year. Their squares sum to 0.0147. The share trades at £64, and you take its drift as $\mu = 9\%$ a year. You want the chance that it is below £60 in a year, under GBM."
   Fix, part 1 question: "What annual volatility $\sigma$ does that sum of squares imply? Give a decimal to 2 places."
   No number changes. Advisory only: `review-4` `r-dig110` holds the same $\ln(60/64)$ (a digital struck at 64 from 60).

3. `reuse` | `ito/problems-1.json` and `-2.json` | two slip lines built from course lines.
   - `p-quarter-rally` `items[1].parts[0].feedback.byKey.variance`: "That is the variance, $0.35^2 \times 0.75$. The sd is its square root." l1 S4, l3 S6 and `r-qv-sd` each end a `var` line "... is the variance. The sd is its square root." Fix: "$0.35^2 \times 0.75 = 0.0919$ is a variance. Take its root for the sd."
   - `p-results-vol` `items[2].parts[2].feedback.byKey.full-variance`: "You took off the whole variance. The drag is half of it, $0.0284375$." `mock-superday-strats` `s2-gbm-median`: "You took off the whole variance, $\sigma^2$, not half of it."; l4 `q-median` `fullv`: "You subtracted the whole $\sigma^2$. The drag is half of it." Fix: "$72e^{0.06 - 0.056875}$ subtracts all of the integrated variance. Only half, $0.0284375$, comes off the log mean."

## B. `problems-2`

4. `misleading` | `ito/problems-2.json` | `p-results-vol` | `items[2].parts[3].widget.tol` | the part names a table and refuses its reading.
   "A normal table or software gives $\Phi$". A table at $z = -0.13$ gives 0.4483; the band is $0.447355 \pm 0.0005$, so a learner who does as told gets the generic line. The validator reports it (`[table-source]`).
   Fix: `tol.abs` 0.001 (takes 0.4483 and 0.4474; the nearest `wrong`, 0.4301, stays 0.017 away).

5. `misleading` | `ito/problems-2.json` | `p-cube-path` | `items[1].parts[3].question` | passable from the printed target.
   The question opens "The limit in part 3 says $W_1^3 = 3\int_0^1 W^2\,dW + 3\int_0^1 W\,dt$" and then asks for the $dt$ coefficient of $d(W_t^3)$. The answer $3w$ is the integrand printed one line above; no derivative is needed. (l8 S3 also states that $W^3$ drifts at $3W$.)
   Fix, question: "Check the limit of part 3 with Itô's lemma. For $f = x^3$, $a = 0$ and $b = 1$, $d(W_t^3) = 3W_t^2\,dW_t + (\ldots)\,dt$. Writing $w$ for $W_t$, enter the $dt$ coefficient."
   Fix, `feedback.correct`: "$f_{xx} = 6x$, so $\tfrac12 f_{xx} = 3w$. Integrated, $W_1^3 = 3\int_0^1 W^2\,dW + 3\int_0^1 W\,dt$, as the path gave."

6. `continuity` | `ito/problems-2.json` | `p-cable-inverse` | `items[0].parts[3].question` | the last part hands over its own idea.
   "From part 1, $Y$ has zero drift when $\sigma^2 - \mu = 0$. Which $\mu$ makes $Y$ a martingale?" The step being tested is that a martingale needs zero drift; the question states it and leaves only $0.12^2$.
   Fix: "Using the drift rate $\sigma^2 - \mu$ from part 1, which $\mu$ makes $Y$ a martingale? Give it as a percentage."

7. `reuse` | `ito/problems-2.json` | `p-cube-path` | `items[1].parts[1].explain.text`, `items[1].parts[2].widget.options[1].why` | two lines retold from l5 and l3.
   l5 S4 ("Square the path step by step"): "the left side telescopes to $W_1^2 - W_0^2 = W_1^2$". Here: "The left side telescopes to $W_1^3 - W_0^3 = 0.216$." The problem runs that screen's chain (expand a step, telescope, replace $(\Delta W)^2$) one power higher, which is fair transfer; the line should be its own. l3 S7 `zero`: "You treated $(\Delta W)^2$ as negligible, as in ordinary calculus." Here: "You treated $(\Delta W)^2$ as negligible."
   Fix, `explain.text` sentence 1: "Step by step the cubes cancel in pairs, leaving $W_1^3 - W_0^3 = 0.216$."
   Fix, `why`: "You let $(\Delta W)^2$ vanish in the limit. It is of size $\Delta t$, so the terms add up like $W_k\,\Delta t$."

8. `reuse` | `ito/problems-2.json` | `p-cable-inverse` | `items[0].parts[1]` `feedback.correct`, `feedback.generic`, `explain.text` | the step line of l6 S5 and `h-moment-order`.
   l6 S5: "The $dW$ term has mean zero, so $m(t) = E[S_t^2]$ obeys $dm = (2\mu + \sigma^2)m\,dt$, with $m(0) = 10{,}000$." `h-moment-order`: "The $dW$ term has mean zero, so $m(t) = E[S_t^p]$ obeys $m' = cm$". Here: "The $dW$ term has mean 0, so $E[Y_t]$ grows at ..." and "Taking expectations, $m(t) = E[Y_t]$ obeys $dm = (\sigma^2 - \mu)m\,dt$ with $m(0) = 0.8$."
   Fix, `correct`: "Averaging removes the noise, so $E[Y_t]$ grows at $\sigma^2 - \mu = -0.0056$ a year: $0.8e^{-0.0168} \approx 0.7867$."
   Fix, `generic`: "Not quite. The mean of $Y$ grows at the drift rate $\sigma^2 - \mu$, starting from $Y_0 = 0.8$."
   Fix, `explain.text`: "The mean of $Y$ grows at the drift rate, $-0.0056$ a year, from 0.8. Over three years that is $0.8e^{3(0.0144 - 0.02)}$. So $E[Y_3] = 0.8e^{-0.0168} \approx 0.7867$."

## C. `problems-3`

9. `misleading` | `ito/problems-3.json` | `p-one-touch` | `items[2].parts[1].widget.tol` | the part names a table and refuses its reading.
   "with $\Phi$ from a normal table". At $z = 0.88$ a table gives $2 \times 0.1894 = 0.3788$; the band is $0.380381 \pm 0.0005$. Doubling doubles the table's error. The validator reports it (`[table-source]`).
   Fix if the part survives finding 12: `tol.abs` 0.002 (takes 0.3788; the nearest `wrong`, 0.3359, stays 0.044 away).

10. `reuse` | `ito/problems-3.json` | `p-touch-note` | `items[0].prose` and the numbers that follow | a parameter set shared with a power-claim screen. Minor; the main session may waive it.
   l16 S5 prices the power claim $S_T^2$ "with $S_0 = 80$, $r = 4\%$, $\sigma = 25\%$". The note is a power of $S$ with barrier 80, $r = 4\%$, $\sigma = 25\%$. `e-cubed-claim` part 2 asks for the same root, $m = -2r/\sigma^2$, by another route (judged fine: one part, other numbers).
   Fix (numbers under `PROPOSED finding 10`): barrier £75; the roots and part 1 stand.
   - Prose: "... the first time a share falls to £75 ...".
   - Part 2: "worth £1 at $S = 75$"; options $(S/75)^{-1.28}$, $S/75$, $\tfrac12(S/75) + \tfrac12(S/75)^{-1.28}$; "a fall to £75"; `correct` "... it equals $(75/75)^{-1.28} = 1$ at the barrier."; `generic` "... at $S = 75$ ...".
   - Part 3: "Using $V = (S/75)^{-1.28}$ from part 2 ..."; `answer` 0.691956; `wrong`: `sign` 1.4452, `no-half` 0.8318, `root-one` 1.3333. `correct`: "$(100/75)^{-1.28} = e^{-1.28\ln(4/3)} \approx 0.6920$." `generic`: "Not quite. Put $S = 100$ into $(S/75)^{-1.28}$." `sign`: "That is $(4/3)^{1.28}$, above £1. ..." `root-one`: unchanged. `explain`: "The share must fall 25% before the note pays ... The value is $(4/3)^{-1.28} \approx 0.6920$."
   - Part 4: "Using $V = 0.6920$ at $S = 100$ from part 3 ..."; `answer` $-88.5704$; `wrong`: `sign` 88.6, `no-power` $-69.20$. `correct`: "$V_S = -1.28V/S = -1.28(0.6920)/100 = -0.00886$ a note, so the desk holds $10000V_S \approx -88.6$ shares." `explain`: "... With $V = (S/75)^{-1.28}$, $V_S = -1.28V/S$. So $\Delta = -1.28 \times 0.6920 \times 100 \approx -88.6$."

11. `reuse`, ruled `re-author` | `ito/problems-3.json` | `p-digital-measures` | `items[1]`, whole item | walks four course items in a row.
   - Part 1 is l10 `q-theta` with other numbers ("A share has $\mu = 8\%$, $r = 3\%$ and $\sigma = 25\%$. What is the market price of risk $\theta$?"), and its `excess` line ("Divide it by $\sigma$ to put it per unit of noise") is that item's `no-sigma` line ("Divide it by $\sigma$ to get the price of risk").
   - Part 2 is l11 S8 and l16 S3 ("Now the digital put, which pays £1 if $S_T < 100$ ... Its chance under $Q$ is $\Phi(-d_2)$").
   - Part 3 is l11 `q-digital` and `r-digital` ("The risk-neutral chance of that is 0.42, with $r = 2\%$ and $T = 1$. What does the digital cost?"); `review-4` `r-dig110` runs parts 2 and 3 as one item.
   - Part 4 retells l11 S5: "A junior simulates the same call with the real drift ... but discounts at $r = 5\%$." Here: "A junior prices the same digital with the real drift, $P(S_{0.5} < 36)$, discounted at $r$". The shift between the two scores is in `h-girsanov-ratio` ($\Phi(0.1462)$ under $P$, $\Phi(0.3862)$ under $Q$, a gap of $\theta\sqrt T = 0.24$).
   Not to walk: l10 S2 and `q-theta`; l11 S5, S8 and `q-digital`; l16 S3 and S10 (the junior's digital pair); `r-weight`, `r-digital`, `r-dig110`; `h-girsanov-ratio`. No story of a junior pricing under $P$. The keys and bands of the present text are right.

12. `reuse`, ruled `re-author` | `ito/problems-3.json` | `p-one-touch` | `items[2]`, whole item | retells l12 S1, S8 and S3 with a one-touch for the knock-in, and the exam item.
   - Part 2 is l12 S1 (driftless path, "By reflection, a path that touches 1 and falls back matches a path that ends above 1"; slip "Paths that touch and fall back are as many again"). Here: "Paths that touch and fall back count too, which doubles it."
   - Part 3 is l12 S8 with other nouns: "Every path either touches the barrier or does not. So a knock-out and its knock-in add to the vanilla". Here: "Every path either touches £120 or does not, so the two notes add to a sure £1 at expiry." The discounting is `r-digital`.
   - Part 4 is l12 S3, `q-shift`, `r-touch`, `h-touch-shift` and above all `e-daily-touch`: "A log price is driftless Brownian motion with $\sigma = 25\%$ ... checked on 126 days ... The barrier sits 0.06 above the start, in log terms ... shifted by $0.5826\sigma\sqrt{\Delta t}$"; its line "Daily checks miss some touches, so the shifted barrier is higher." Here: "$\ln S$ is driftless Brownian motion with volatility 24%", "The barrier is $\ln 1.2 = 0.1823$ above the start in log terms", "Daily closes miss some touches, so the barrier acts further away" (also l12 S5 and `r-parity`: "Daily closes miss some touches, so fewer paths ...").
   - Part 1 only sets $r = \tfrac12\sigma^2$ to make the log driftless, the exam item's setting. `review-1` `r-gbm-above` holds the same $\ln 1.2 = 0.1823$ from £100 to £120.
   - Part 4 also restates no value: it needs 0.1823, 0.2078 and the factor 0.978632 from parts 2 and 3 and says only "Using the method of part 3".
   Not to walk: l12 S1, S3, S5, S8 and S9, `q-touch`, `q-shift`, `q-parity`; `r-touch`, `r-parity`, `r-shift`, `r-digital`; `h-touch-shift`; `e-daily-touch`, `s3-touch`. No driftless log price touched by reflection and then shifted for daily closes; no in-out parity retold as touch against no-touch. The keys of the present text are right; its part 2 band is finding 9.

## Notes, no change asked

- `p-maker-tally` part 3 takes $\sigma^2$ from the sum of squares, 1,000,000; the day's variance is 999,600. The question says which to use, and l3 reads $\sigma^2$ off the squares, so the key stands.
- `p-realised-then-risk` part 4 prints "$0.09 - 0.02885 = 0.06115$"; the drag is 0.028855, a tie at the fifth place. The arithmetic as printed is consistent and the key is unaffected.
- `p-maker-tally` part 4 names a table and takes its reading (0.1314 at $z = -1.12$, 0.0004 from the key); so does `p-realised-then-risk` part 3 (0.2643).
- `p-touch-note` part 4 asks "how many shares does it hold", the wording of l9 `q-hedge` ("A desk is short 500 of our calls ... How many shares does it hold to be delta-hedged?"). The delta is derived here and given there; judged fine.

## Engine

- `fresh-check` passed `p-maker-tally` although its process is `h-drift-below`'s in other units ($500t + 1000W$ against $0.5t + W$ in thousands). A drift-to-volatility ratio shared with a same-course item that asks the same chance would catch it.
- `retold` passed a stem that keeps a homework sentence with the numbers and the opening clause changed ("a share's squared daily log returns add to", finding 2) and a story kept with one noun changed ("A junior ... the same ... with the real drift ... discounts at $r$", finding 11).
- The chain rule of `retold` did not see `p-one-touch` walk l12 S1, S8 and S3 in order, nor its three lines shared with `e-daily-touch`.

## Fix pass

Session AF, `docs/briefs/reauthor-fix-af.md`, one agent as author and fixer. Every replacement number recomputed in `docs/reports/problems-ito-numbers.py` before writing.

1. fixed: win chance 0.507; keys 350 and 0.216924, every `wrong` value and line as written; the table dropped from part 4. 0.3632 occurs in the course only as path values and as l9's put delta $-0.3632$ (also $\Phi(-0.35)$, another context); kept as a slip.
2. fixed: prose and part 1 question as written; no number changes.
3. fixed: both slip lines as written ($0.35^2 \times 0.75 = 0.0919$ checked).
4. fixed: `tol.abs` 0.001; the table reading 0.4483 is taken, the nearest `wrong` stays outside.
5. fixed: question and `feedback.correct` as written.
6. fixed: question as written.
7. fixed: `explain` sentence 1 and the `zero` option's `why` as written.
8. fixed: `correct`, `generic` and `explain` as written.
9. superseded: `p-one-touch` re-authored (finding 12).
10. fixed (applied by ruling; barrier £75 collides with no course material): keys 0.691956 and $-88.5704$, `wrong` values 1.4452, 0.8318, 1.3333, 88.6, $-69.20$, every line as written.
11. re-authored as `p-twin-shares` (l9, l10, l11): hedge one share with another, the noiseless book fixes $\mu_B$, the drift rate of $S_B/S_A$ under $P$ and then $Q$, a note on the ratio. No $\theta$ question, no digital, no junior.
12. re-authored as `p-bridge-closes` (l10, l11, l12): a daily-simulated up-and-out call; why the drift drops out between two known closes, the reflection touch chance between closes, survival over four gaps, the path's corrected payoff. No touch chance from the start, no shift, no parity.

Reader's script: `p-maker-tally` and `p-touch-note` checks retargeted to the applied values (the maker reuse check now reads the drift from the set); `p-digital-measures` and `p-one-touch` checks removed (re-authored); the PROPOSED block replaced by a band check. 320 checks, 0 FINDING lines.

Gates: validator 0 errors, no warning on the three sets; voice scan 35, 0 and 0; `fresh-check --files` 0 hits (advisories in the report); author script 988 of 988, exit 0; `grade-all --file` 0 failures on each set; playthrough `--problems ito/problems-<n>` green with and without `--mobile` for n = 1, 2, 3.
