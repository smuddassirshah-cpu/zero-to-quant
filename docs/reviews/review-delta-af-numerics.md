# Delta read AF, numerics: the two re-authored problems and the parts the two fix passes changed

Counts: `wrong` 1, `misleading` 3, `reuse` 1, `re-author` 0, `continuity` 1, `voice` 0, `other` 0. Neither new problem is a retelling. Four of the six findings sit in the new problem `p-implicit-newton-step` or in a part of `p-float32-overnight` the fix pass edited but did not recompute; one is in the first reader's own replacement text.

Scope, at commit 3229dbb7 (sets last changed by 0cbca46b, 3c1c67d4, eefe7c40 and 90088234):

- `problems-2` `p-vol-curve-extension` and `problems-3` `p-implicit-newton-step`, whole;
- `problems-1` `p-float32-overnight` prose and parts 2 and 3 (findings 1, 4, 5, N3), `p-moment-recurrence` part 2 explain (N2);
- `problems-2` `p-survival-crossing` parts 1, 3, 5 (findings 6 to 9), `p-project-irr` part 4 explain (finding 10);
- `problems-3` `p-normal-cdf-quadrature` part 2 explain (finding 11);
- `problems-4` `p-hand-implicit-put` part 1, `p-pilot-control` parts 2 and 4, `p-grid-node-budget` part 3, `p-digital-pairs` part 4 (findings 1 to 7 of the level 4 read).

Finding 12 of the first read (`p-rate-path-euler` part 5) is an accepted exception and was not read again.

Method. Each part in scope was solved from its text before its key was read. No browser, no content or engine edit.

- `docs/reports/delta-review-delta-af-numerics-numbers.py` imports no earlier script: exact fractions for the cubic pieces, the Newton iterates and the quadratic through three points; mpmath for the roots, the exact path and its ODE (differentiated, and against a Taylor solve); NumPy float32 for the gap; a brute search for each whole-number key; a seeded simulation for the pair correlation. Each band is rebuilt with the engine's rule and fed what a learner types from the rounded numbers the part prints.
- The engine's `numGrade` was read (`app/js/engine/grade.js`, `parseNum`, `numValue`, `within`: a bare number is divided by 100 when `unit` is "%", a typed % sign does the same once, and every absolute band has $10^{-9}$ of slack) and run on 113 typed strings over the parts in scope; 112 came out as expected and the other is finding 4.
- Reuse. Read in full against the two new problems: l5, l8 and l12 (every screen, hint, option line, summary), `review-2` `r2-spline-global`, `r2-forward`, `review-3` `r3-ring`, `r3-euler-limit`, `homework-2` `h2-spline-row`, `h2-spline-m`, `homework-3` `h3-implicit-factor`, `h3-step-update`, `h3-stiff-longform`, and the exam items `e-natural-spline`, `e-stiff-implicit`, `e-newton-minimise` (`topic-2.5`), `c-newton-yield` (`stage-2`). The course folder was searched for each key number, each closing sentence of the new problems and of the replaced lines of set 4, and `app/content` for the numbers of both new problems. `mock-superday-strats` holds no Newton, spline or implicit-step item.

## Tool results

| check | result |
|---|---|
| author's script | `problems-numerics-numbers.py` 1,087 of 1,087, exit 0 |
| readers' scripts | `problems-numerics-numbers-read.py` 436 checks, 0 FINDING; `problems-numerics-4-numbers-read.py` 507 of 507, 0 FINDING |
| this read's script | 265 checks, 0 failed, 6 FINDING rows, exit 0 (a row prints `resolved` once fixed) |
| validator | 0 errors; one warning on the four sets (20-word sentence, `problems-2` `items[2].parts[0].explain`); `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file` | 0 hits on each of the four sets; advisories as before ($u = 2^{-53}$, $e_{k+1} \approx Ce_k^2$, 95 and 1.96) |
| `grade-all.mjs --file` | 13, 15, 14, 18 widgets, 0 failures |
| same checks with every fix below applied | fresh-check 0, 0, 0 hits; grade-all 0 failures; voice 0 and 0; validator 0 errors and no warning on the sets; this script 265 checks, 6 rows `resolved`; files restored with `git checkout` |

## Rulings asked for

- **Finding 7 of the first read (the fixer's dispute).** The fixer is right. From the restated 3.5333, $p = 0.98 - 0.03 \times 2.5333 - 0.0025 \times 2.5333 \times 0.5333 = 0.90062348$, so 0.9006235 to 7 places and 0.900623 to 6: the reader's 0.900624 rounds the wrong way. $p'(3.5333) = -0.0376665$ and the step is $0.00062348/0.0376665 = 0.016553$; the reader's $0.000624/0.037667$ is 0.016566 and would land at 3.5499 only by luck (3.549866). As printed, $0.0006235/0.037667 = 0.016553$ and $3.5333 + 0.016553 = 3.549853$, typed 3.5499, taken. The text stays as the fixer wrote it.
- **The percentage part (`p-float32-overnight` part 2).** Sound. Key $2^{-24}/10^{-4} = 5.9605 \times 10^{-4}$ as a fraction, `unit` "%", band $\pm 5 \times 10^{-6}$. Taken: "0.060", "0.060%", "0.06", "0.06%", "0.0596", "0.0596%", "0.060 %", "0.060 per cent". Refused: "0.059", "0.061" with or without the sign, "0.000596", "5.96e-4", "0.6". Routed: "0.030", "0.030%", "0.0298%", "0.03" to `one-factor`; "0.119", "0.119%", "0.1192" to `eps`. No tie (0.059605% at 3 places).
- **The Newton iterates.** `p-vol-curve-extension`: $q'(0.75) = 0.0375$, $q''(0.75) = -2.7$, step 0.013889, $t = 2.763889$, peak $3 - \sqrt5 = 0.763932$, gap $4.3 \times 10^{-5}$: all as printed. `p-implicit-newton-step`: $G(0.05) = 0.125$, $G' = 4$, $v = 0.01875$; $G(0.01875) = 5/512 = 0.0097656$, $G' = 3.375$, step 0.0028935, $v = 137/8640 = 0.0158565$; root $(-3 + \sqrt{11})/20 = 0.0158312$; errors $2.9 \times 10^{-3}$ and $2.5 \times 10^{-5}$; constant $G''/2G' = 3.02$; $x(0.05) = 0.005564$; local error 0.0102672; ratio 406. Every printed digit holds. The fault is in the form asked of part 2 (finding 4).
- **Does `p-implicit-newton-step` walk l12, `r3-ring`, `h3-stiff-longform` or `e-stiff-implicit`?** No. It forms no factor $\tfrac{1}{1 - h\lambda}$, no step limit, no trapezoidal factor, no power of a factor and no ringing; its chain (Newton iterate, second iterate, exact root, local error, ratio of the two errors) is in none of them. Likenesses, none a finding: the step $h = 0.05$ is also the failing Euler step of l12 screen 1 and of `h3-stiff-longform` (one number, with $h\lambda = -3$ against $-2.5$); the slips `explicit` and `no-one` of part 1 are the same two natural slips as `explicit` and `inverse-z` of `e-stiff-implicit` part 1, on a Newton step where the exam has a factor, in other words ("You left the 1 out of $G'(v) = 1 - hf'(v)$, so you divided by 3, not 4." against "You dropped the 1. The factor is $\tfrac{1}{1 + h\lambda} = \tfrac19$."); "stable and positive, but first order" echoes l12 screen 3's "first-order accurate and stable at six times Euler's limit".

## Verdict per item

| item | part | numbers | reuse | chain |
|---|---|---|---|---|
| `p-float32-overnight` | prose, part 2 | clean | clean | holds |
| | part 3 | wrong (finding 1), misleading (finding 2) | clean | restated values miss the key |
| `p-moment-recurrence` | part 2 explain | clean | clean | holds |
| `p-project-irr` | part 4 explain | clean ($10^{-12}/3.4 \times 10^{-14} = 29$; real third error $3.2 \times 10^{-14}$) | clean | holds |
| `p-vol-curve-extension` | all | clean | clean | holds |
| `p-survival-crossing` | part 1 | misleading claim (finding 3) | clean | holds |
| | parts 3, 5 | clean | clean | holds |
| `p-normal-cdf-quadrature` | part 2 explain | clean (weights $\tfrac16$, $\tfrac46$, $\tfrac16$; errors 0.0127, 0.00046) | clean | holds |
| `p-implicit-newton-step` | part 1 | clean | reuse, one line (finding 6) | holds |
| | part 2 | misleading, key on a tie (finding 4) | continuity, one term (finding 5) | holds |
| | parts 3 to 5 | clean | clean | holds |
| `p-hand-implicit-put` | part 1 | clean ($0.5 \times 2.29 = 1.145$) | clean | as the first read's N1 |
| `p-pilot-control` | parts 2, 4 | clean (45,235 by search; $64/4.71 = 13.58811$, band takes 13.59 and 13.588, refuses 13.58 and 13.60) | clean | holds |
| `p-grid-node-budget` | part 3 | clean ($k = 4$ by search; $k = 3.31$ gives $M = 229$ with the strike off a node) | clean | holds |
| `p-digital-pairs` | part 4 | clean ($\rho = -0.25$ exactly and by simulation; three pair means have variance $s^2/8$) | clean | holds |

All seven fixes of the level 4 read and findings 1, 4 to 6, 8, 10, 11 and notes N2, N3 of the first read are applied as given. Finding 7 is applied with the fixer's two figures, which are right. Finding 9 is applied as given, and its text carries finding 3 below.

## Findings

1. `numerics/problems-1.json` | `items[0].parts[2]` (`p-float32-overnight` part 3): `widget.tol`, `widget.wrong[0].tol`, `feedback.correct` | wrong | The part hands over 0.0596% and $3.16 \times 10^{-8}$ and asks for the nearest whole number. Those give 18,861, which is refused. | $5.96 \times 10^{-4}/3.16 \times 10^{-8} = 18{,}860.76$; the band is $18{,}850 \pm 2$, and "18861" gets the generic line. The feedback, edited by the fix pass, still prints "$5.96 \times 10^{-4} \div 3.16 \times 10^{-8} \approx 18{,}850$", which is false. 18,850 needs the unrounded $2^{-24}/10^{-4}$ over $2^{-25}/0.9425$. The first reader's script allowed a gap of 15 here. The slip `one-input` has the same fault: $2.98 \times 10^{-4}/3.16 \times 10^{-8} = 9{,}430$ misses $9{,}425 \pm 2$. | `widget`: `"tol": {"abs": 12}`; `wrong` `one-input` `"tol": {"abs": 8}` (value stays 9425). `feedback.correct`: "$5.96 \\times 10^{-4} \\div 3.16 \\times 10^{-8} \\approx 18{,}861$, or $18{,}850$ before any rounding. Compare $\\tfrac{P_0 + P_1}{P_0 - P_1} = 18{,}849$, the condition number of the subtraction." Engine: 18861, 18860, 18850, 18849 pass; 18837 and 18863 are refused; 9425 and 9430 route to `one-input`. The explain stays (it derives 18,850 from the powers of two). Both earlier scripts need the tolerances.

2. `numerics/problems-1.json` | `items[0].parts[2].widget.wrong[1]` (`per-cent`) | misleading | The entry's value is not the slip its line names, so the line is never shown. | Line: "You divided the percentage itself. As a decimal 0.0596% is $5.96 \times 10^{-4}$." Dividing the percentage itself gives $0.0596/3.16 \times 10^{-8} = 1{,}886{,}076$ (1,885,000 unrounded). The entry is 188.5, which is $5.96 \times 10^{-6}/3.16 \times 10^{-8}$: the percentage divided by 100 twice. | `"value": 1885000, "tol": {"abs": 1500}`. Engine: 1886076, 1885035 and "1,885,000" route to `per-cent`. The line stays. Both earlier scripts need the value.

3. `numerics/problems-2.json` | `items[2].parts[0].explain.text` (`p-survival-crossing` part 1) | misleading | The first reader's replacement says the slopes "change by $\tfrac{-0.04 + 0.03}{4} = -0.0025$ a year". They do not. | The slope of $p$ changes by $p'' = -0.005$ a year (the chord slopes $-0.03$ and $-0.04$ sit at 2 and 4 years). $-0.0025$ is the coefficient of $(t - 1)(t - 3)$, half of $p''$. | Whole text: "The slopes between neighbouring points are $-0.03$ and $-0.04$ a year. Their difference, spread over the 4 years between the outer dates, is $\\tfrac{-0.04 + 0.03}{4} = -0.0025$, the coefficient of $(t - 1)(t - 3)$. So $p(t) = 0.98 - 0.03(t - 1) - 0.0025(t - 1)(t - 3)$, which fits all three dates, and $p(4) = 0.98 - 0.09 - 0.0075 = 0.8825$." Checker 0 hits; the validator's 20-word warning goes too.

4. `numerics/problems-3.json` | `items[1].parts[1]` (`p-implicit-newton-step` part 2): `question`, `widget` | misleading | The key sits on a rounding tie at the 6 places asked. | The iterate is $137/8640 = 0.0158564815$, $1.9 \times 10^{-8}$ below the tie 0.0158565. The part's own feedback prints "$0.01875 - 0.0028935 = 0.0158565$"; a learner who works to those 7 places and rounds half up types 0.015857, which the band ($0.015856 \pm 6 \times 10^{-7}$) refuses with the generic line. | Ask for the 7 places the later parts restate. `question`: "Using $v = 0.01875$ from part 1, take a second Newton iterate. Give 7 decimal places." `widget`: `"answer": 0.0158565`, `"tol": {"abs": 6e-08}`; `frozen` `"value": 0.0163086, "tol": {"abs": 6e-08}`; `sign` `"value": 0.0216435, "tol": {"abs": 6e-08}`. At 7 places the value is $3 \times 10^{-8}$ from the nearest tie and the rounded intermediates ($0.0097656/3.375$, or the step 0.0028935) give the same 0.0158565; the slips from the printed values give 0.0163086 and 0.0216435. Engine: 0.0158565 passes; 0.0158564 and 0.0158566 are refused; the two slips route. Feedback and explain stay. Part 3's `stopped` (0.0158565) already matches. The author's script needs the key and the two values.

5. `numerics/problems-3.json` | `items[1].parts[1].feedback.byKey.frozen` | continuity | "That simplified Newton converges only linearly" uses a name and a word the course does not teach. | Search of the course: "simplified Newton" and "linearly" appear in this line only; l5 says "order 1" and "drops to order 1". The claim itself is right (the error ratio is $1 - G'(r)/4 = 0.17$). | "You kept $G' = 4$ from the start. A slope held fixed gives only order 1, so recompute $G'(0.01875) = 3.375$." Checker: 0 hits.

6. `numerics/problems-3.json` | `items[1].parts[0].feedback.byKey.sign` (`p-implicit-newton-step` part 1) | reuse | The slip line is the one of the numerics exam item `c-newton-yield` (`exams/stage-2.json`), which the checker does not read. | Exam: "You added $f/f'$. Newton subtracts it, and here $f' < 0$, so $y$ rises." Problem: "You added the correction. Newton subtracts $\tfrac{G}{G'}$, and $G(0.05) > 0$." | "That moves $v$ up. $G(0.05)$ and $G'(0.05)$ are both positive, so the root lies below 0.05." Checker: 0 hits. Part 2's `sign` line ("You added the correction. $G(0.01875) > 0$ and $G' > 0$, so $v$ falls.") no longer pairs with it and may stay.

## Reuse verdict, the two new problems

| problem | closest material | verdict | texts |
|---|---|---|---|
| `p-vol-curve-extension` | l8 screen 2 ("Value, slope and curvature match at every quote ... zero at the two ends, which is what natural means"); l8 screens 3, 4, 7 (a row's right side, a row check, the piece formula); l8 screen 8 code explain (three points, $4M_2 = 6(-1 - 1)$); `h2-spline-row`, `h2-spline-m`; `r2-spline-global`; exam `e-natural-spline`; exam `e-newton-minimise` (convex item, Newton on $f'$); set problem `p-survival-crossing` part 3 | clean | No row, no system, no piece formula: the three matching conditions fix three coefficients and the quote the fourth, which no item does. Part 4 is one Newton step on a derivative, the task of `e-newton-minimise` part 1 asked once on its own cubic: "Newton for a minimum is the root finder applied to $f'(x) = e^x - 3$" against "To find a peak, Newton solves $q'(u) = 0$, so $q''$ plays the part of the slope." One echo, left: "The piece bends down as the quotes level off" against `h2-spline-m` "The curve bends down at the middle knot, as a rise then a flat stretch should." The set now has a Newton step in each of its three problems (root, peak, level crossing), each on another function. |
| `p-implicit-newton-step` | l12 screens 1 to 6 and 7 ("One linear solve per step makes the method implicit"); l11 screen 2 (local error); l5 screens 5 and 6 ($e_{k+1} \approx Ce_k^2$); `r3-ring`, `r3-euler-limit`; `h3-implicit-factor`, `h3-stiff-longform`; exams `e-stiff-implicit`, `c-newton-yield`; set problem `p-project-irr` part 4 | clean but for finding 6 | See the ruling above. The nonlinear step solved by Newton, the exact root as the limit of the iterates, and the local error set against Newton's error are in no lesson, review, homework or exam item. |

## Claims checked, no finding

- `p-vol-curve-extension`: $p''(1) = 0$; $q$ matches $p$ in value, slope and curvature at 2 years and passes 20.4; $q'(1) = -0.6 < 0$, so the peak is before 3 years; a natural spline through the three quotes has $M = -4.2 \ne -3.6$, so it changes $p$, and it rises on all of $[1, 3]$; the height at the Newton point and at the exact peak agree to $3 \times 10^{-9}$ ("costs only its square"). Part 5 from the restated 2.7639: $19.6 + 1.83336 - 1.05038 + 0.08915 = 20.47214$, rise 0.0721, with `start` 0.0719 and `sign` 0.0711 each on its own line.
- `p-implicit-newton-step`: $f'(0.05) = -60$, $h\lambda = -3$; $G(v) = 10v^2 + 3v - 0.05$ and $G' = 3 + 20v$ identically; the exact path starts at 0.05 and satisfies the ODE; parts 4 and 5 give their keys from the restated values (0.01027; $0.01027/2.53 \times 10^{-5} = 405.9$); `first` takes 3.52, 3.54, 3 and 4.
- `p-survival-crossing` part 5: $2.033 \times 10^{-4}/0.03775 = 0.0053854$, times 365 is 1.9657, typed 1.97; the `sign` slip of part 3 takes 3.5167 and 3.5168.
- `p-pilot-control` part 2: with the exact normal point the count would be 45,234, so stating 1.96 was needed and is there.
- Skills are the course's; set 2 still draws on l5 to l8 and set 3 on l9 to l12.

## Engine

- No rule warns when a numeric key lies within a few per cent of a rounding unit from a tie at the places its question asks for (finding 4: $1.9 \times 10^{-8}$ from the tie at 6 places).
- No rule holds a part's printed sum against its band: `feedback.correct` prints a quotient of two restated values whose result (18,861) lies outside $18{,}850 \pm 2$ (finding 1).
- The same-course checker reads no exam, so a slip line of `exams/stage-2.json` `c-newton-yield` passed (finding 6); the same gap as the convex bullets.
- Bullets added to `docs/BACKLOG-INBOX.md` under `Raised later (delta read AF numerics):`.
