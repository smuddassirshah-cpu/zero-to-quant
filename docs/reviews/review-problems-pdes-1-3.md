# Problem sets 3.2, pdes levels 1 to 3: second-reader findings

Scope: `app/content/courses/pdes/problems-1.json`, `-2`, `-3`: 10 problems, 43 parts (all numeric), 87 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Reader, Author rules, Session AE additions), `docs/briefs/wave-c-author-ag.md` rules 1 to 6, `docs/briefs/wave-c-reader-ag.md`. Pattern: `review-problems-analysis-1-3.md`.

## Verdict per problem

Reuse scope read: lessons l1 to l12 (every screen and quiz item), `review-1` to `-3`, `homework-1` to `-3`, the other sets, and the ten `pe-` items of `exams/topic-3.2.json` (no other exam file carries a `pe-` skill), including `e-heat-grid-steps` (two parts) and `e-fk-reverting`.

| Set | Problem | Closest lesson screen | Closest quiz item | Closest review item | Closest homework item | Closest other set problem | Closest exam item | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `p-tick-spread` | l2 s3 and s4 ($D$, then variance at $t = 2$) | l2 `q-d-small` | `r-d-walk`, `r-sd-time` (items 2, 3) | `h-colleague` | `p-drift-walk` | `e-kernel-peak` | clean |
| 1 | `p-two-level-bar` | l3 s3 (unit step, $u(1, 0.5)$) | l3 `q-step-d` | `r-step-neg` | `h-gauss-general` | `p-grid-rod` p4 (steady line) | `e-slab-heat` | clean |
| 1 | `p-grid-rod` | l4 s8 (explicit step), l4 s0 (steady line) | l12 `q-steps` | `r-insulated-avg` | `h-unstable` | `p-grid-modes` | `e-heat-grid-steps` p2 | clean (finding 10) |
| 1 | `p-drift-walk` | l2 s7 ($c$ for $q = 0.55$), l1 s3 | l1 `q-residual` | `r-decay-rate` | `h-drift`, `h-derive-lazy-walk` | `p-tick-spread` | `e-kernel-peak` | clean (finding 5) |
| 2 | `p-tent-rod` | l8 s0 (centre reaches 50, one term) | l8 `q-centre`, l5 `q-lambda2` | `r-lambda-len4`, `r-linearity` | `h-centre-nonzero` | `p-grid-modes` | `e-rod-centre` | clean |
| 2 | `p-exp-series` | l7 s7 ($f = x$ at $x = \pi$), l7 s2 | l6 `q-x-b3`, `q-leibniz` | `r-coefficient-decay` | `h-gibbs-true` | none | `e-jump-gibbs` p1 | clean (findings 3, 11) |
| 2 | `p-grid-modes` | l8 s4, s5 (mode factor) | l8 `q-dt` | `r-stable-step`, `r-decay-ratio` | `h-explicit` | `p-grid-rod` | `e-explicit-code` | reuse (finding 9; finding 2) |
| 3 | `p-call-heat` | l10 s2 and s4 | l9 `q-tau`, l10 `q-arg` | `r-k` | `h-chain` | none | `e-heat-grid-steps` p1, `e-heat-change` | **re-author** (finding 6) |
| 3 | `p-fk-claim` | l9 s1, l11 s7 | l10 `q-width` | `r-se`, `r-sd` | `h-vasicek` | none | `e-fk-reverting`, `e-fk-square` | **re-author** (finding 7) |
| 3 | `p-grid-no-formula` | l12 s4 (Richardson), l12 s3 | l12 `q-order` | `r-rich`, `r-put` (items 7, 3) | `h-sequence` | none | `e-heat-grid-steps` | **re-author**, the borderline one (finding 8) |

Both texts for each ruling are under "Reuse" below. Three of ten are ruled re-author, all in level 3, whose four lessons are one route: each part of those problems has a twin in the course, in the lesson's own order.

Method. The author's script was run first. Every part was then solved from its text in `docs/reports/problems-pdes-numbers-read.py`, which imports nothing from the author's script and uses `math` and `numpy` only (no SciPy solver). Route 1 is the closed form with exact inputs. Route 2 is another method: the kernel integral by quadrature (the two-level bar, the call price by lesson 10's route), the grid run step by step and to its limit (the rod, 5,000 steps), a finite-difference residual, the exact binomial walk, the tent and $e^x$ coefficients by quadrature, the series $\sum 1/(1 + k^2)$ summed to two million terms with its tail, the eigenvalues and the 50th power of the explicit step matrix, $V = e^{x + b(T - t)}$ put into the Feynman-Kac equation, and a dense-matrix Crank-Nicolson solve of the lesson 12 scheme. Route 3 is the part's own printed working with its rounded inputs. Each key band is tested against all three at the asked rounding. Every `wrong` value is rebuilt from the slip its line names, tested in its own band at the asked rounding, against the key band and against the other slip bands. Entries on band edges went through the engine's `numGrade` in node (`SCRATCH/read-pdes/probe.mjs`, 44 rows). Each claim was read against the lesson that teaches it.

## Tool results

| check | result |
|---|---|
| author's script | `problems-pdes-numbers.py` 571 checks, 0 failures, exit 0 |
| reader's script | `problems-pdes-numbers-read.py` 977 checks, 7 `FINDING` lines (findings 1, 2, 3, 4, 5), exit 0 |
| validator | 0 errors, 4567 warnings; three on these files, all `[O2-long-sentence]` (20 words, under the gate of 35); none of the pass-8 rules; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --files` (three sets) `--pairs` | 0 hits, 12 advisory, read: the taught formulas the author lists. It does not see the retold exam sentence of finding 7 (Engine 1) |
| `grade-all.mjs --file`, three sets | 17, 13 and 13 widgets, 0 failures |
| engine grader probe | 44 rows; 1 fault (`1.3` refused in finding 2); `0.5436` is taken in finding 4 by a float margin of $5 \times 10^{-17}$ |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 43 keys agree with mine by two routes, and so do all 87 `wrong` values but one, stored 0.000015 off inside its band (finding 1). No key or slip sits on a rounding tie that refuses an asked rounding; every band takes its printed working. The percentage part carries unit "%" with the key as a fraction; each tail and quantile value is given in the question. No part can be passed by working backwards from a printed target. One printed number is false (finding 1). One restated value contradicts the working the part before it prescribes, and refuses the learner who carries his own (finding 2). Two printed divisions round the other way (findings 3, 4). One model sentence claims more than the course's own homework allows (finding 5).

## A. Numbers and claims

1. `problems-3.json` | `items[2].parts[3]` `feedback.correct`, `explain.text`, `widget.wrong[1].value` | wrong | `p-grid-no-formula` part 4 prints $Ke^{-rT} = 50e^{-0.015} = 49.255582$. | $50e^{-0.015} = 49.2555970$. The key 2.99678 was computed with the right value ($3.741181 - 50 + 49.255597 = 2.996778$), so the line's own sum does not hold: $3.741181 - 50 + 49.255582 = 2.996763$. The slip `v400` is stored as 2.996422; the slip gives $3.7408399 - 50 + 49.255597 = 2.996437$ (still inside its band). The author's script checks the string, not the value. | In both lines replace `49.255582` by `49.255597`. `wrong[1].value` 2.996437. (Moot if finding 8 is applied.)

2. `problems-2.json` | `items[2].parts[3].question`, `widget.answer`, `widget.tol` | misleading | `p-grid-modes` part 4 says "Using 0.2200 from part 3". | Part 3 tells the learner to use the factor 0.9702, and $0.9702^{50} = 0.22032$: 0.220 to the 3 places asked, but 0.2203 to 4, not 0.2200 (that is the unrounded $0.970171^{50} = 0.21999$). A learner who carries his own 0.2203 gets $(0.2231 - 0.2203) \div 0.2231 = 1.26\%$, types 1.3 and is refused on the generic line (probe). | If finding 9 is applied, its bands cure this. If finding 9 is waived: question "... Using 0.220 from part 3, by what percentage ..."; `answer` 0.0133, `tol.abs` 0.0009 (takes 1.26, 1.3, 1.39, 1.4 and the exact 1.41; refuses 1.2 and 1.5); `feedback.correct` "$(0.2231 - 0.220) \div 0.2231 \approx 0.014$, so the grid is about 1.4% low."; in `byKey.absolute` and `explain.text` replace `0.2200` by `0.220`.

3. `problems-2.json` | `items[1].parts[1]` `feedback.correct`, `explain.text` | misleading | `p-exp-series` part 2 prints "$\tfrac{6}{10} \times 3.6761 \approx 2.2056$" and "$0.6 \times 3.6761 \approx 2.2056$". | $0.6 \times 3.6761 = 2.20566$, which is 2.2057 to 4 places. 2.2056 comes from the unrounded $b_1$ ($0.6 \times 3.676078 = 2.205647$). The band takes both (probe), so no learner is refused; the line contradicts the learner who did as told. | `feedback.correct`: "$b_3 = (+1) \times \tfrac{6}{10} \times 3.6761 \approx 2.2057$. The unrounded $b_1$ gives 2.2056, which is also accepted." `explain.text` last sentence: "So $b_3 = 0.6 \times 3.6761 \approx 2.2057$."

4. `problems-3.json` | `items[0].parts[2].explain.text`, `widget.tol` | misleading | `p-call-heat` part 3 explains "$\sqrt{2\tau} = 0.2236$ ... $0.12154 \div 0.2236 \approx 0.5435$". | $0.12154 \div 0.2236 = 0.54356$, 0.5436 to 4 places. It lies 0.00006 from the key 0.54354 with `tol.abs` 0.00006, and is taken only because the float difference is $5.99999999999 \times 10^{-5}$. | `tol.abs` 0.0001 (slips at 0.25491 and 0.31993 stay clear). `explain.text`: "... and $\sqrt{2\tau} = 0.22361$ is the kernel's spread. With $x = 0.06454$ the argument is $0.12154 \div 0.22361 \approx 0.5435$, which is $d_1$." (Moot if finding 6 is applied.)

5. `problems-1.json` | `items[3].prose` | misleading | `p-drift-walk`: "Its density obeys $u_t + c\,u_x = D\,u_{xx}$". | The walk's own variance is $4q(1 - q)\Delta x^2 t/\Delta t = 2.4t$, not $2Dt = 2.5t$. The course says so itself: `homework-1` `h-derive-lazy-walk` rubric, "its variance 1.975 is $c^2\Delta t\,t = 0.025$ below $2Dt = 2$". Here $c^2\Delta t = 0.1$, a 4% gap: the walk is below 2 at $t = 0.32$ with chance 0.0855, where part 3's key is 0.0899. The equation is the model, not the walk's law. | Prose second sentence: "We model its density by $u_t + c\,u_x = D\,u_{xx}$, with $D = \Delta x^2/(2\Delta t) = 1.25$ and drift speed $c = (2q - 1)\Delta x/\Delta t$." Part 3 question, first sentence: "From a point start the model's density is a normal kernel that moves with the drift: at time $t$ it has mean $ct$ and variance $2Dt$." No key changes.

## B. Reuse

6. `problems-3.json` | `items[0]` (all four parts) | reuse, **re-author** | `p-call-heat` walks four course items in the lesson's order with other numbers. |
   - Part 1 "What is the heat time $\tau$ today? Give 3 decimal places." against l9 `q-tau` "We transform with $\tau = \tfrac12\sigma^2(T - t)$. What is $\tau$ today, at $t = 0$? Give 3 decimal places." and exam `e-heat-grid-steps` part 1 "What is the heat time $\tau$ today, with the whole 0.6 years left?". The slips `no-half` and `unsquared` are the exam's `no-half` and `sigma-unsquared`.
   - Part 2 "the scaled equation is $v_\tau = v_{xx} + (k - 1)v_x - kv$. What is $k$?" against `review-3` `r-k` "An option has $r = 4\%$, $\sigma = 30\%$ ... becomes $v_\tau = v_{xx} + (k - 1)v_x - kv$. What is $k = 2r/\sigma^2$?" (the same $r$), l9 s3 and l9 `q-coeff`.
   - Part 3 "gives $\Phi$ of $\dfrac{x + 2a\tau}{\sqrt{2\tau}}$. What is that argument today?" against l10 `q-arg` "The argument of $\Phi$ is $\dfrac{x + 2a\tau}{\sqrt{2\tau}}$. What is the argument?" and l10 s2.
   - Part 4 "Using $d_1$ ... and $d_2$ ... Take $\Phi(d_1) = 0.70662$ and $\Phi(d_2) = 0.62549$. What is the call worth, in £? Give 2 decimal places." against l10 s4 "The arguments are $d_1 = 0.8266$ and $d_2 = 0.6266$, with $\Phi(0.8266) = 0.7958$ ... Also $Ke^{-rT} = 95.1229$. What is the call worth at $S = 110$? Give 2 decimal places."
   | Not to walk: l9 `q-tau`; l9 s3, l9 `q-coeff`, `review-3` `r-k`; l10 `q-arg`, l10 s2; l10 s4; `e-heat-grid-steps` part 1; `e-heat-change` ($\sigma = 25\%$). A new chain on `pe-bs` and `pe-heat` should not open with $\tau$ then $k$, nor end on the formula with given $\Phi$ values.

7. `problems-3.json` | `items[1]` (prose and parts 1, 3, 4, 5) | reuse, **re-author** | `p-fk-claim` retells an exam item's prose and a lesson screen, and each part has a course twin. |
   - Prose "a value $V(t, x)$ solves $V_t - 0.1V_x + 0.18V_{xx} - 0.05V = 0$, with $V(T, x) = e^x$. Today $x = 0$ and two years remain." against exam `e-fk-reverting` "A value $V(t, x)$ solves $V_t + 0.3(3 - x)V_x + 0.08V_{xx} - 0.04V = 0$, with $V(T, x) = x$. Today $x = 1$ and two years remain." The same two sentences and horizon; `e-fk-square` also has "2 years to go".
   - Part 1 "Put $\tau = c(T - t)$, with $c$ chosen so that the $V_{xx}$ term has coefficient 1. What is $\tau$ today?", feedback "$V_t = -cV_\tau$", against l9 s1 "Put $\tau = c(T - t)$, so $V_t = -cV_\tau$ ... Choose $c$ so that this coefficient is 1. What is $\tau$?".
   - Part 2 (variance $2\tau$) against l10 `q-width` "The variance is $2\tau = 0.16$" and `review-3` `r-sd`. It is one doubling of part 1.
   - Parts 3 and 4 ($E[e^{X_T}]$, then the discount) are `e-fk-square` and `e-fk-reverting` cut in two: "$X_T \sim N(3, 2.88)$, so $E[X_T^2] = 11.88$, and $V = e^{-0.2} \cdot 11.88$"; the slip `no-disc` is their `no-discounting` and `no-discount`.
   - Part 5 "how many standard errors above $V$ is the estimate?" against l11 s7 "How many standard errors below the closed form is the no-noise price 0.789215?", l11 s4 and `review-3` `r-se`.
   | Not to walk: `e-fk-reverting` (its prose and its read-the-process, mean, discount chain); `e-fk-square`; l9 s1; l10 `q-width`, `r-sd`; l11 s7, l11 s4, `r-se`. The exponential payoff and the link $2\tau = \sigma^2(T - t)$ are new to the course and may be kept as ideas.

8. `problems-3.json` | `items[2]` (prose, parts 3 and 4) | reuse, **re-author** (borderline: parts 1 and 2 are new) | `p-grid-no-formula` ends on two review items in a row, on their option's $r$, $T$ and moneyness. |
   - Prose "$S = K = \text{£}50$, $r = 3\%$, $\sigma = 24\%$ and $T = 0.5$ ... with $n_t = n_x/5$" against `review-3` `r-rich` and `r-put` "$S = K = 100$, $r = 3\%$, $\sigma = 25\%$, $T = 0.5$" and `homework-3` `h-sequence` (the same option). The discount factor is the same $e^{-0.015}$: $Ke^{-rT} = 49.2556$ here is half of `r-put`'s 98.5112.
   - Part 3 (Richardson on 200 and 400) against `r-rich` "Crank-Nicolson gives £7.7576434 on 200 intervals and £7.7596032 on 400. What does Richardson extrapolation give?". Its explain "$V_{400} + (V_{400} - V_{200})/3$ cancels the $ch^2$ term" paraphrases l12 s4 "$V_h + \dfrac{V_h - V_{2h}}{3}$ cancels $c\,h^2$ (Richardson)". Part 3 is also only part 2 added to a printed price.
   - Part 4 "Using the extrapolated call price ... and put-call parity, what is the put worth, in £? Give 4 decimal places." against `r-put` "What is the put, by parity $P = C - S + Ke^{-rT}$? Give 4 decimal places.", l10 s7 and l10 `q-put`.
   - Part 1 against l12 `q-order` (order from two errors): different enough, since it uses differences and no formula. Part 2 gives its answer "times $10^6$", the form of l12 s3 and l12 `q-boundary`.
   | Not to walk: `r-rich` then `r-put`; l12 s4; l10 s7, l10 `q-put`; no at-the-money option with $r = 3\%$ and $T = 0.5$. Keep the opening idea (the order and the shortfall from differences alone, no formula), which no course item has, and build the later parts on it. If the main session prefers the smaller change, finding 1 still applies.

9. `problems-2.json` | `items[2]` (prose, parts 1, 3, 4) | reuse | `p-grid-modes` shares its rod and a key number with the course. | Prose "A grid on a rod of length $\pi$ ... and $D = 0.5$ cuts it into 12 intervals" against `review-2` `r-stable-step` "A rod of length $\pi$ with $D = 0.5$ is cut into $N = 20$ intervals", `r-decay-ratio` "On a rod of length $\pi$ with $D = 0.5$" and l5 `q-fade`. Part 4 "$e^{-1.5} = 0.2231$" against l5 s10 "$e^{-1.5} = 0.2231$: the sharp feature has faded fastest" (also a rod of length $\pi$). | Renumber with $D = 0.75$, $\Delta t = 0.04$, 40 steps to $t = 1.6$ ($D\Delta t = 0.03$ as before, so $\lambda = 0.437708$ and the factor 0.970171 stand; none of "D = 0.75", $e^{-1.2}$, 0.3012 or 0.298 occurs in the course or its exam items):
   - Prose: "... with both ends held at 0 and $D = 0.75$ cuts it ...".
   - Part 1: question "The run uses $\Delta t = 0.04$. ..."; `feedback.correct` "$\lambda = 0.75 \times 0.04 \div (\pi/12)^2 = 0.03 \div 0.068539 \approx 0.4377$."; `wrong` `no-d` 0.58361 ($0.04 \div 0.068539$), line "You left out $D = 0.75$: $\lambda = D\Delta t/\Delta x^2$, three quarters of $\Delta t/\Delta x^2$ here."; `unsquared` stays 0.114592. Part 2 unchanged.
   - Part 3: question "... how large is the $k = 1$ mode after 40 steps, at $t = 1.6$, if it starts at 1? Give 3 decimal places." `answer` 0.298, `tol.abs` 0.0005 ($0.970171^{40} = 0.29780$, $0.9702^{40} = 0.29816$). `wrong`: `exact` 0.30119, `power-t` 0.95275 ($0.9702^{1.6}$). `correct`: "Forty steps multiply by the factor forty times: $0.9702^{40} \approx 0.298$." `exact`: "That is the exact $e^{-Dt} = e^{-1.2}$. The grid multiplies by 0.9702 forty times." `power-t`: "You raised the factor to the power 1.6, the time. It applies once per step, 40 times." `explain`: "The grid applies its factor once per step, and $t = 1.6$ takes $1.6 \div 0.04 = 40$ steps. So the mode is $0.9702^{40} \approx 0.298$."
   - Part 4: question "Separation gives the exact mode $e^{-Dk^2t}$, which is $e^{-1.2} = 0.3012$ at $t = 1.6$. Using 0.298 from part 3, by what percentage is the grid's mode below the exact one? Give 1 decimal place." `answer` 0.0106, `tol.abs` 0.0008, unit "%" (takes 1.06 from 0.298, 1.00 from a carried 0.2982, the exact 1.13, and so 1.0 and 1.1; refuses 0.9 and 1.2). `wrong`: `absolute` 0.0032, `tol.abs` 0.0005; `ratio` 0.9895, `tol.abs` 0.0012 (98.9 or 99.0 typed). `correct`: "$(0.3012 - 0.298) \div 0.3012 \approx 0.011$, so the grid is about 1.1% low." `absolute`: "That is the gap $0.3012 - 0.298$ itself. As a percentage it is measured against the exact 0.3012." `explain`: "The grid's factor 0.9702 is a little below $e^{-0.03} = 0.9704$, and the gap compounds over 40 steps. The result is $(0.3012 - 0.298) \div 0.3012 \approx 0.011$ below, or 1.1%."
   The fixer adds these values to both number scripts and checks `[wide-wrong-tol]` on the `ratio` band.

## C. Continuity

10. `problems-1.json` | `items[2].parts[3]` | continuity | `p-grid-rod` part 4 restates 24.375 but its answer does not use it. | The steady value 20 follows from the prose alone. (`p-two-level-bar` part 5 is as loose: 0.879 is restated and unused. No change proposed there: the contrast with the long bar's 60 is the point of the part.) | Question: "The grid value at $x = 0.1$ was 24.375 after three steps, as part 3 found. As the steps go on, the grid settles on the rod's steady state. How far above its steady value is 24.375? Give 3 decimal places." `answer` 4.375, `tol.abs` 0.0005. `wrong`: `steady` 20; `mean-ends` $-20.625$; `left-end` 9.375; each `tol.abs` 0.0005. `correct`: "The steady state is the line from 15 to 75, which rises 50 a unit, so it is 20 at $x = 0.1$. The grid is still $24.375 - 20 = 4.375$ above it." `generic`: "Not quite. The steady state solves $u_{xx} = 0$ with the two end values. Subtract it from 24.375." `steady`: "20 is the steady value itself. The question asks how far 24.375 sits above it." `mean-ends`: "You took 45, the mean of the end values, as the steady value. Near the cold end the line gives 20." `left-end`: "You measured from the end's 15. The steady line has risen to 20 by $x = 0.1$." `explain`: "A steady state solves $u_{xx} = 0$ with the end values, so it is a straight line. Its slope is $60 \div 1.2 = 50$, which gives 20 at $x = 0.1$. After three steps the grid is still 4.375 above it."

11. `problems-2.json` | `items[1].parts[4].question` | continuity | `p-exp-series` part 5 restates $\cosh\pi$ but not $\sinh\pi = 11.5487$, which it also needs from part 1. | A learner who slipped in part 1 has no value to carry. | Last sentence of the question: "Using $\sinh\pi = 11.5487$ from part 1 and $\cosh\pi = 11.5920$ from part 4, what is $\sum_{k\ge1}\frac{1}{1 + k^2}$? Give 4 decimal places." ($(\pi \times 11.5920 \div 11.5487 - 1) \div 2 = 1.07669$, in the band.)

## Verified

- Level 1: $D = 0.8$, $\sqrt{96}$, the two-sided tail 0.1258 (the exact 600-step walk gives 0.1308, the same tail on its lattice of 0.8 pence), 360 s; the two-level profile by the kernel integral, the level 75 at $x = 0.2133$ and $t = 0.8792$, and $u(0.4, t)$ does fall through 75 towards 60; 75 steps, 27.5, 24.375, and the $\lambda = \tfrac12$ grid does settle on the line (all 11 mode factors are $\cos(k\pi/12)$, below 1 in size); $c = 10$, the residual vanishes only at $a = 5$, 0.0899, 0.1353.
- Level 2: $48/\pi^2$ and $b_3 = -0.5404$ by quadrature, $b_2 = 0$; the $k = 5$ term is $2 \times 10^{-5}$ at $t = 1.5$ and the $k = 3$ term is below $10^{-6}$ at $t = 6.41$; $b_k = (-1)^{k+1}\tfrac{2k}{1+k^2}b_1$ and $a_k\cos k\pi = \tfrac{2\sinh\pi}{\pi(1+k^2)}$ by quadrature for $k = 2, 3, 7$, so the series at $x = \pi$ is as printed; $\sum 1/(1+k^2) = 1.076674$ by direct sum; the grid factor is the top eigenvalue of the step matrix and every mode is bounded.
- Level 3: $d_1$ by the heat form and by the usual form; the call £11.0953 by the kernel integral; $V = e^{0.06}$ by the expectation and by the equation; the sample sd 1.0904 is plausible (true 1.0903); my dense Crank-Nicolson gives 3.7357101, 3.7398157, 3.7408399 and lesson 12's 10.4486123; Richardson 3.7411813 is within $2 \times 10^{-6}$ of the formula.
- Definitions against the lessons: width $\sqrt{2Dt}$ (l3 s2), $D = \Delta x^2/(2\Delta t)$ (l2 s9), $\lambda_k = (k\pi/L)^2$ (l5 s9), midpoint at a jump for a piecewise smooth function (l7 s9), slope $-1$ for a jump (l7 s2), the lemma argument (l10 s1), Feynman-Kac (l11 s3). `sinh`, `cosh` and `coth` appear nowhere else in the course; the values are printed, so no finding.
- Shape: every lesson of each level is drawn on, as the author's table says; skills are carried by the level's lessons; each set has a difficulty 5.

## Counts

| severity | count | findings |
|---|---|---|
| wrong | 1 | 1 |
| misleading | 4 | 2, 3, 4, 5 |
| reuse | 4 | 6, 7, 8 (re-author), 9 (renumber) |
| voice | 0 | |
| continuity | 2 | 10, 11 |

## Engine

1. `fresh-check.mjs` reports nothing for `p-fk-claim` against `e-fk-reverting`, though the prose is the same two sentences with other coefficients. With the maths dropped, too few signal words are left for the `retold` test.
2. No validator rule compares a value a part restates ("Using 0.2200 from part 3") with the value the earlier part's printed working gives ($0.9702^{50} = 0.2203$), nor recomputes a printed division or product at the asked places (findings 3, 4). `[working-band]` reads only the part's own line.
3. Author scripts' `says()` checks a printed figure as a string, so a false figure passes (finding 1).

Inbox bullets are under `Raised later (review problems pdes):` in `docs/BACKLOG-INBOX.md`.

## Fix pass

Session AF, one agent re-authoring and fixing (`docs/briefs/reauthor-fix-af.md`). Every number below was recomputed at full precision before it was written, then rounded.

1. Moot: `p-grid-no-formula` is re-authored (finding 8). The new problem prints no discount factor; level 3 printed products and quotients are now checked by value with `shown()` in the author's script, not as strings.
2. Fixed through finding 9: part 4 now restates "0.298 from part 3", which is part 3's own working ($0.9702^{40} = 0.29816$) at the 3 places part 3 asks; a carried 0.2982 gives 1.00% and is taken.
3. Fixed as written: both lines print 2.2057, `feedback.correct` adds that the unrounded $b_1$ gives 2.2056 ($0.6 \times 3.6761 = 2.20566$; $0.6 \times 3.676078 = 2.205647$; the band takes both).
4. Moot: `p-call-heat` is re-authored (finding 6).
5. Fixed as written (prose "We model its density by ..."; part 3 "the model's density ... it has mean $ct$ and variance $2Dt$"). Extended under the main session's rule that no sentence may claim the walk follows a model whose variance it does not match: part 3 now asks "what chance does the model give of being below 2 at $t = 0.32$?" in place of "the chance the walker is below 2". No key changes.
6. Re-authored as `p-straddle-vol` (difficulty 4, l9 and l10): an $r = 0$ straddle at £9.60 read back to its implied volatility. The argument $\sqrt{\tau/2}$ as an expression, $\Phi = 0.53$, $\tau = 0.01133$ by $\Phi^{-1}(0.53) = 0.07527$, $\sigma = 17.38\%$. It opens with neither $\tau$ nor $k$ and ends on no formula with given $\Phi$ values.
7. Re-authored as `p-log-contract` (difficulty 5, l9 and l11): a claim paying £1,000 $\ln(S_T/K)$. A trial solution of the scaled equation gives $c = k - 1$; the value $-$£27.95 in one step; the break-even rise 2.92%; Feynman-Kac in heat time gives the chance 0.4665 of a positive payoff. It has no read-mean-discount chain of `e-fk-reverting` or `e-fk-square`, no $\tau = c(T - t)$ step, no variance part and no standard error. The exponential payoff and the link $2\tau = \sigma^2(T - t)$ were not reused; $2\tau = 0.1176$ is printed, not asked.
8. Re-authored as `p-grid-budget` (difficulty 4, l12 and l11). Parts 1 and 2 keep the order and shortfall from differences on a new option ($S = K = 120$, $r = 4.5\%$, $\sigma = 18\%$, $T = 1.25$; order 2.0, shortfall $557.6 \times 10^{-6}$). Parts 3 and 4 are new: the shortfall on 16 times the work ($34.85 \times 10^{-6}$) and the 256 times the paths a simulation needs for the same cut. No Richardson price, no parity, no at-the-money option with $r = 3\%$ and $T = 0.5$. A first draft of part 3 asked the paths for a standard error equal to the shortfall, which walks the numerics exam item `topic-2.5` `e-error-budget`; it was dropped (inbox bullet).
9. Fixed as written: $D = 0.75$, $\Delta t = 0.04$, 40 steps to $t = 1.6$. Recomputed: $\lambda = 0.437708$; `no-d` $0.04 \div 0.068539 = 0.583610$; factor 0.970171; $0.970171^{40} = 0.297804$, $0.9702^{40} = 0.298161$, key 0.298 $\pm$ 0.0005; `exact` $e^{-1.2} = 0.301194$; `power-t` $0.9702^{1.6} = 0.952748$; part 4 $(0.3012 - 0.298) \div 0.3012 = 0.010624$, exact 0.011255, key 0.0106 $\pm$ 0.0008 (takes 1.0, 1.06, 1.1, 1.13 and a carried 0.2982's 1.00; refuses 0.9 and 1.2); `absolute` 0.0032 $\pm$ 0.0005; `ratio` $0.298 \div 0.3012 = 0.989376$, 0.9895 $\pm$ 0.0012, which takes 98.9 and 99.0 and is no wider than those roundings need (checked in both scripts). $e^{-0.03} = 0.970446$ prints as 0.9704.
10. Fixed as written: key 4.375 $\pm$ 0.0005; `steady` 20, `mean-ends` $-20.625$, `left-end` 9.375.
11. Fixed as written: $(\pi \times 11.5920 \div 11.5487 - 1) \div 2 = 1.076686$, in the band of 1.0767.

Engine 1 to 3: left to the engine queue (bullets already in the inbox). Engine 3 is worked around in this course's script by `shown()`, which compares the full-precision value with the printed figure at its places.

Keys changed: problems-1 `p-grid-rod` p4 (20 to 4.375, new slips); problems-2 `p-grid-modes` p1 `no-d` (0.875415 to 0.58361), p3 (0.220 to 0.298, slips 0.30119 and 0.95275), p4 (0.01405 to 0.0106, slips 0.0032 and 0.9895); problems-3 all 12 keys new.

Level 3 shape after the re-authoring: l9 in `p-straddle-vol` and `p-log-contract`, l10 in `p-straddle-vol`, l11 in `p-log-contract` and `p-grid-budget`, l12 in `p-grid-budget`. No lesson is in all three problems; one difficulty 5 (`p-log-contract`).

Gates:

| set | validator | voice 35 | fresh-check `--file` | number scripts | grade-all | playthrough | `--mobile --why` |
|---|---|---|---|---|---|---|---|
| problems-1 | 0 errors | 0 and 0 | 0 errors, 4 advisory | author 637 checks 0 failures; reader 716 checks 0 `FINDING` | 0 failures (17) | green | green |
| problems-2 | 0 errors | 0 and 0 | 0 errors, 2 advisory | as above | 0 failures (13) | green | green, 28 slips routed |
| problems-3 | 0 errors, no warnings | 0 and 0 | 0 errors, 6 advisory | as above | 0 failures (12: 2 expression, 10 numeric) | green | green, 30 slips routed |

The reader's script: checks of the three replaced problems removed (findings 1 and 4 go with them), its dense solver retargeted to the three `p-grid-budget` prices, the `p-grid-rod` and `p-grid-modes` checks moved to the new numbers, the `p-drift-walk` claim check now reads the wording, and the shape check accepts "expression" or "in terms of" as the stated form of an `expression` part. Screenshots at 440 px of the new set read: no overflow.
