# Problem sets 1.3 (b): second-reader findings

Read at commit be3049d. A full second read of six sets. Pattern: `review-problems-1.3-a.md` and section A of `review-problems-1.5-c.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible rounding in the stated form; `minor` = weak part, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: taylor and multivar, sets 1 to 3

Scope: `app/content/courses/taylor/problems-1.json` to `problems-3.json` and `app/content/courses/multivar/problems-1.json` to `problems-3.json`: 21 problems, 101 parts (57 taylor, 44 multivar; 79 numeric, 15 expression, 7 choice).

Method. Both authors' scripts run first: `problems-taylor-numbers.py` 900 checks, 0 failures; `problems-multivar-numbers.py` 420 of 420. Every part was then solved from its text before its answer was read, by hand, and again in `problems-1.3-b-scripts/mine.py`: sympy for the exact value (rationals, `diff`, `solve`, `limit`), then a second route (mpmath at 30 digits, a Newton loop, `findroot` on the true price curve, a grid search, a brute-force count of descent steps). Every numeric `wrong` value was re-derived from the slip its feedback line names and compared inside that entry's own band. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `matchWrong` in listed order with each entry's own band, `numSetGrade`, `exprEqual`, the `expanded` shape, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry, and 191 typed strings of my own (fractions, roundings in the stated form, MathLive's `\left( \right)` pairs, other correct forms, near misses, slips typed in the wrong units). The lessons of each level were searched and the passages read for each idea a set leans on (`taught.py`): the $\tfrac12 f''(a)h^2$ rule and which side of its tangent a curve lies (taylor l2), DV01 and modified duration (l4), $c_k = f^{(k)}(a)/k!$ about a centre (l6), where the standard series work (l7), comparison, the ratio test and $\sum \tfrac{1}{n^2}$ (l9), endpoints (l10), the first-left-out rule and Lagrange with $M$ (l11); along a contour $\tfrac{df}{dt} = 0$ (multivar l4), $|\nabla f|\cos\theta$ (l6), the error of a tangent plane going with the square of the step (l7), the factors $1 - ks$ of descent (l8), $\lambda$ as the gain per unit of limit (l11), $\lambda = 2\sigma_p^2$ (l12).

Tool results.

| check | result |
|---|---|
| authors' number scripts | 900 and 420 checks, 0 failures |
| `mine.py` (reader's own answers, slips and prose claims) | 78 numeric parts, 752 checks, 2 failures: both are content faults and stay failing (finding 6) |
| `grade-check.mjs` (engine graders) | 780 checks, 0 failures, 9 rows the reader holds to be content faults (findings 3, 4, 5) |
| `proposed.py` (numbers of the fixes below) | 91 checks, all hold |
| validator | 0 errors; 0 warnings on the six files |
| playthrough `--problems`, six sets, `--local-cdn` | green |
| the same with `--mobile` | green |
| voice scan 35, both course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| the same at `--min-run 8 --min-share 0` | taylor 9, 25, 3; multivar 1, 1, 5: form sentences and stock phrases, bar the `homework-3` hit judged in finding 9 |

Result. Every `answer` and `accept` value agrees with my own, and every numeric `wrong` value is the value its named slip gives. Two feedback claims are false (findings 1 and 2); the rest of the 101 parts state nothing untrue. No expression answer carries a plain-text function name: the 15 are polynomials, pairs and one quotient in LaTeX, and each answer and `accept` form grades correct while every `wrong[].tex` grades to its own key. Pairs take `(18,6)`, `\left(18,6\right)`, `18,6` and fractions; `form: "expanded"` on `p-min-variance-pair` part 1 takes the terms in any order and fractions for decimals, and returns the form line for the unexpanded sum.

The parts answered in units of $10^{-k}$ (taylor set 3: `p-two-months` 2, 4, 5 and `p-tail-bound` 4). Each answer is right in its units ($17.07$, $4.86$, $21.93$, $11.594$) and each band takes the rounding the question asks for (17.1, 4.86, 21.9, 11.59). Each scaled slip is right ($8.53$, $51.2$, $320$; $4.17$, $14.58$, $2.08$; $12.21$, $21.24$; $10.67$, $11.85$, $16.0$). Three faults sit here: a band that refuses a value the item's own figures give (finding 3), a weaker case of the same (finding 4), and the four `unscaled` entries, whose bands swallow every small number (finding 5).

Claims checked beyond the keys: $\sqrt[3]{27.81} = 3.02970$; Newton's errors 0.037, 0.00087, 0.0000005 and the root 1.213412; $x_2 = \tfrac{17}{14}$, $f(x_2) = \tfrac{13}{2744}$, $f'(x_2) = \tfrac{1063}{196}$; the true loss at 35.3 bp (£49,600), the true limit (35.6 bp) and £1.25 a lot on 35 bp; $V(0.05403) = 10{,}000.41$, $V'(0.05403) = -18{,}642.89$ and the loan rate 0.054052; $4.4^{3/2} = 9.22952$; $f^{(k)}(0) = (k + 1)!$ for $(1 - x)^{-2}$; the modified duration 3.3502 and the true price £98.36 at 8.5%; $\ln 2.1 = 0.74194$; the true errors $16.10$, $4.33$ and $11.8 \times 10^{-5}$; $e^{0.4} = 1.49182$ inside $[1.49173, 1.49183]$ and the true tail $11.58 \times 10^{-4}$; $\ln 1.4$, $\ln 2.8$; $f_x(2, 1.1) = 10.78$; the true half-step error 0.0029; $0.8^{23}$, $0.8^{24}$; the exact best 51.875 at $(5.25, 1.25)$, by solving and by a grid; $0.03375 \times 1.0404$.

### Findings

1. `wrong` | `taylor/problems-3.json` | `p-two-months` | part 5.
   The part asks "what is the most this total can be out" and keys $17.07 + 4.86 = 21.93$. The item itself fixes the sign of each error: part 2's series alternates, so the first estimate is too low (true error $+16.10 \times 10^{-5}$); part 4 says every term is negative, so the second is too high ($-4.33 \times 10^{-5}$). The errors must cancel in part, and the most the total can be out is the larger bound, 17.07. A learner who reasons so types 17.1 and is told "The second month's error adds to it", which is false. The `subtracted` line, "The two errors could have the same sign", is false too. The explanation's own figure, 11.8, is $16.10 - 4.33$.
   Fix: keep the answer and ask for the bound without the signs.
   - `question`: "Log returns add, so the two-month estimate is $0.0768 - 0.05125 = 0.02555$. Use only the sizes of the bounds, $17.07 \times 10^{-5}$ and $4.86 \times 10^{-5}$, not the signs of the errors. What is the most this total can be out? Answer in units of $10^{-5}$, to 1 decimal place."
   - `byKey.subtracted`: "You took one bound from the other. A bound gives a size, not a sign, so the safe total is the sum."
   - `byKey.first-only`: "That is the first month's bound alone. With the signs left out, the second month's 4.86 adds to it."
   - `generic`: "Not quite. Each estimate is out by at most its bound, and with the signs unknown the two can add."
   - `explain`: "With the signs left out, the sum is out by at most the sum of the bounds, $(17.07 + 4.86) \times 10^{-5} \approx 21.9 \times 10^{-5}$. The true two-month log return is $\ln(1.08 \times 0.95) = 0.025668$, $11.8 \times 10^{-5}$ above 0.02555. The two errors had opposite signs, $+16.10$ and $-4.33$, so they partly cancelled."

2. `wrong` | `taylor/problems-1.json` | `p-newton-cubic` | part 3, option `below`, `why`.
   "Newton's steps overshoot only when the curve bends the other way." False, and the item shows it: with $f'' > 0$ the first step went from $x_0 = 1$, below the root 1.2134, to $x_1 = 1.25$, above it. On a rising curve that bends up a step from the left crosses the root and a step from the right cannot. The key (`above`) and the explanation are right.
   Fix: `why` "The step from $x_0 = 1$ did cross the root, but a step from $x_1$ cannot. With $f'' > 0$ the tangent lies under the curve, so it reaches 0 before the curve does."

3. `unclear` | `taylor/problems-3.json` | `p-tail-bound` | part 4.
   `tol` 0.005 on 11.594, in units of $10^{-4}$ to 2 places. The part's own `first-term` entry gives $a_4$ as 10.67, and part 2's explanation prints $a_4 \approx 0.001067$. Either gives $10.67 / 0.92 = 11.598$, which rounds to 11.60 and is refused. The same class as findings 2 to 4 of batch a.
   Fix: answer `tol` `{ "abs": 0.008 }`; `accept` "11.59, from $\\tfrac{10.667 \\times 10^{-4}}{0.92}$ (11.60 is accepted too)". The band 11.586 to 11.602 still refuses the true error 11.58, `first-term` 10.67, `over-four` 11.85 and `lagrange` 16.

4. `minor` | `taylor/problems-3.json` | `p-two-months` | part 4.
   (a) `tol` 0.005 on 4.86. With $M$ kept as 2.33 the bound is $2.33 \times \tfrac{0.000125}{6} = 4.854 \times 10^{-5}$, typed 4.85 and refused. The feedback's own $M = 2.3327$ is accepted, so this is the weaker case of finding 3. (b) The part never says what to find: it reads "Use Lagrange ... Answer in units of $10^{-5}$".
   Fix: answer `tol` `{ "abs": 0.01 }` (`wrong-end` 4.17 stays far outside). `question`: "At $r = -0.05$ every term is negative, so the first-left-out rule does not apply. Use Lagrange, $|R_2| \le \tfrac{M |r|^3}{3!}$, with $f'''(x) = \tfrac{2}{(1 + x)^3}$ for $x$ between $-0.05$ and 0. What bound does it give on the error of $-0.05125$? Answer in units of $10^{-5}$, to 2 decimal places."

5. `minor` | `taylor/problems-3.json`, `problems-1.json` | five loose `wrong` bands.
   The four `unscaled` entries carry the answer's own `tol` (0.05 or 0.005) on a value near 0.0002, so each catches every number from about $-0.05$ to 0.05. A learner who makes another slip and also forgets the units is told "That is the bound itself ... so type 17.1": untrue of their value, and it hands over the answer. `grade-check.mjs` shows it for 0.0000853 (the $3!$ slip), 0.000512, 0.0032, 0.0000417 (the $M = 2$ slip), 0.0001221, 0.0016 and 0.0010667.
   Fix (bands checked in `proposed.py`; each takes the value typed to 2 or 3 figures and refuses every other slip unscaled):
   - `p-two-months` part 2 `unscaled`: `tol` `{ "abs": 0.000001 }`
   - `p-two-months` part 4 `unscaled`: `tol` `{ "abs": 0.0000005 }`
   - `p-two-months` part 5 `unscaled`: `tol` `{ "abs": 0.000001 }`
   - `p-tail-bound` part 4 `unscaled`: `tol` `{ "abs": 0.000005 }`
   - `taylor/problems-1.json` `p-loss-limit` part 3 `one-lot` (0.0354, `tol` 0.5, so 0.35 and 0.14 are told "That is the DV01 of one £100 lot"): `tol` `{ "abs": 0.005 }`

6. `minor` | `taylor/problems-1.json` | `p-loss-limit` part 2, `p-loan-rate` part 2 | two printed terms.
   $4 \times 103 / 1.04^5 = 338.63397$, printed as 338.6338 in `feedback.correct` and in `explain`; $3 / 1.05^4 = 2.4681074$, printed as 2.468108 in `explain`. The sums and the answers are right. These are the two failing checks of `mine.py`.
   Fix: 338.6338 becomes 338.6340 (both places; $2.7737 + 5.3340 + 7.6932 + 338.6340 = 354.4349$); 2.468108 becomes 2.468107 ($0.907029 + 1.727675 + 2.468107 = 5.102811$).

7. `minor` | `taylor/problems-1.json` | `p-newton-cubic` | part 3.
   The correct option is 74 characters against 53, 43 and 38, and the only one with two clauses of reasoning. Advisory rule 586.
   Fix: correct option text "Above: the tangent at $x_1$ reaches 0 before the curve does" (59 characters).

8. `minor` | `taylor/problems-1.json` | `p-cube-root-27` | freshness.
   Lesson l1 quiz item 2 is the same function and the same step: "The cube root $f(x) = x^{1/3}$ has $f(8) = 2$ and $f'(x) = \tfrac13 x^{-2/3}$. Use the tangent at $a = 8$ to estimate $\sqrt[3]{8.06}$." Only the base point differs, and l3's quiz finds $\sqrt[3]{9}$ as well. Parts 3 and 4 are l2's rule on that function. The tool does not see it. The brief bars a setup from a quiz of the course.
   Ruling: change the function; the chain stands. Fix (all in `proposed.py`): the fourth root about 16, which no lesson, review, homework or exam of the course uses.
   - `prose`: "You want $\sqrt[4]{16.32}$ without a calculator. Take $f(x) = x^{1/4}$, where $f(16) = 2$ exactly and $f'(x) = \tfrac14 x^{-3/4}$."
   - Part 1: $16^{-3/4} = \tfrac18$, slope $\tfrac{1}{32}$. Answer `2+\frac{x-16}{32}`; `accept` `2+(x-16)/32`, `2+\frac{1}{32}(x-16)`, `\frac{3}{2}+\frac{x}{32}`, `1.5+x/32`. `wrong`: `slope-eighth` `2+\frac{x-16}{8}` ("You left out the $\tfrac14$ in front. The slope is $\tfrac14 \times \tfrac18 = \tfrac{1}{32}$."), `slope-quarter` `2+\frac{x-16}{4}` ("You kept only the $\tfrac14$ in front. The factor $16^{-3/4} = \tfrac18$ is part of the slope too."), `at-x` `x^{1/4}+\frac{1}{4}x^{-3/4}(x-16)`.
   - Part 2: $h = 0.32$, $L(16.32) = 2 + \tfrac{0.32}{32} = 2.01$, to 4 places. `eighth` 2.04, `quarter` 2.08, `whole-x` 2.51.
   - Part 3: $f''(x) = -\tfrac{3}{16} x^{-7/4}$, $16^{-7/4} = \tfrac{1}{128}$, $f''(16) = -\tfrac{3}{2048}$, $h^2 = 0.1024$. Error $\tfrac12 \times (-\tfrac{3}{2048}) \times 0.1024 = -0.000075$ exactly; "Give a decimal to 6 places", `tol` `{ "abs": 0.0000005 }`. `no-half` $-0.00015$, `h-not-squared` $-0.000234$, `sign` 0.000075.
   - Part 4: $2.01 - 0.000075 = 2.009925$, to 6 places, `tol` `{ "abs": 0.0000005 }`. `sign` 2.010075, `no-half` 2.00985, `eighth-carried` 2.039925. The true $\sqrt[4]{16.32}$ is 2.009926 to 6 places, so the corrected estimate matches it to 5 places.

9. `minor` | `multivar/problems-3.json` | `p-min-variance-pair` | freshness, and part 4's wording.
   `homework-3` item 9 (`items[8]`) opens "Asset A has volatility 30% and asset B 20%, with correlation 0.4" and asks for the minimum variance weights by Lagrange, the check by substitution, the volatility and $\lambda = 2\sigma_p^2$. This problem is the same two assets and the same route with the correlation changed to 0.25, which is the correlation of the topic exam's item 24. Also, part 4 says "treat the weights $w_1 = 0.25$ and $w_2 = 0.75$ as free": numbers cannot be free.
   Ruling: change the assets; the chain stands. Fix (all in `proposed.py`): volatility 40% and 25%, correlation 0.3, a pair the course and its exams do not use.
   - `prose`: "Asset A has volatility 40% and asset B 25%, with correlation 0.3. A portfolio holds the share $w$ in A and $1 - w$ in B, so $\sigma_p^2 = 0.16w^2 + 0.0625(1 - w)^2 + 0.06w(1 - w)$."
   - Part 1: answer `0.1625w^2-0.065w+0.0625`; `accept` `\frac{13w^2}{80}-\frac{13w}{200}+\frac{1}{16}`. `no-cross` `0.2225w^2-0.125w+0.0625`; `half-cross` `0.1925w^2-0.095w+0.0625` (the cross term is $2 \times 0.3 \times 0.4 \times 0.25 = 0.06$). Working: $w^2$ terms $0.16 + 0.0625 - 0.06 = 0.1625$; $w$ terms $-0.125 + 0.06 = -0.065$; constant 0.0625.
   - Part 2: $0.325w - 0.065 = 0$, $w = 0.2$: 20% in A, 80% in B. `no-two` 0.4, `gave-b` 0.8, `carried` 0.2809.
   - Part 3: variance $0.0065 - 0.013 + 0.0625 = 0.056$; $\sigma_p = 0.2366$, below B's 25%. `variance` 0.056, `weighted` 0.28, `carried-half` 0.25 (the volatility at $w = 0.4$).
   - Part 4: `question` "Now treat both weights as free, $w_1$ in A and $w_2$ in B, with the budget $w_1 + w_2 = 1$. The minimum is at $w_1 = 0.2$, $w_2 = 0.8$. Here $\frac{\partial \sigma_p^2}{\partial w_1} = 0.32w_1 + 0.06w_2$, and at the minimum this equals $\lambda$. What is $\lambda$? Give the exact decimal." Answer $0.064 + 0.048 = 0.112 = 2 \times 0.056$; the other partial is $0.125w_2 + 0.06w_1 = 0.1 + 0.012$. `variance` 0.056, `no-cross` 0.064.
   - Part 5: $0.056 + 0.112 \times 0.02 = 0.05824$; the exact value is $0.056 \times 1.0404 = 0.05826$. Answer 0.05824, `tol` `{ "abs": 0.0001 }`, `accept` "0.0582 (the exact value, 0.0583, is accepted too)". `sigma-lambda` 0.05712, `no-change` 0.056, `whole-lambda` 0.168.

10. `minor` | `taylor/problems-3.json` `p-tail-bound`, `taylor/problems-2.json` `p-three-halves` | freshness.
    `review-3` item 5 is "$e^{0.2} \approx T_3(0.2) = 1.221333$. For $0 < c < 0.2$, $e^c < 2$", the Lagrange bound of parts 1 and 2 at another point. Lesson l2 screen 5 predicts the error of $\sqrt{4.4}$ about 4 with $h = 0.4$; `p-three-halves` builds $4.4^{3/2}$ about 4.
    Ruling: both stand. `p-tail-bound` shares one step, and its geometric bound on the tail and its two-sided bracket (parts 3 to 5) appear nowhere else. `p-three-halves` shares a base point and a step with l2, not the function: no number of it repeats. No edit.

11. `minor` | `multivar/problems-2.json` | `p-two-book-risk` | part 5.
    "Using the error 0.0118 from part 4 and the square rule". No lesson calls it that: l7 says the error "shrinks with the square of the step".
    Fix: "Halve the move: $x = 3.1$ and $y = 3.85$. The error 0.0118 from part 4 shrinks with the square of the step. Predict the new error. Give 4 decimal places."

12. `minor` | tooling, `app/tools/fresh-check.mjs` and `validate.mjs`.
    (a) Findings 8 and 9 are a function and a pair of assets taken from a quiz and a homework with one number changed. Batch a found the same class twice (its findings 7 and 8); the word-run tool saw none of the four, so the class has now been seen four times (protocol 6). (b) Finding 5: a `wrong` band wide enough to hold other entries' values at another scale.
    Fix (engine items, not content): (a) for `--file` on a problems set, an advisory when an item's prose shares a displayed formula of three or more tokens (`x^{1/3}`, `9 - x^2`) or two or more of its stated parameters with one lesson screen, quiz, review or homework item of its course; `fresh-grep.py` here is the hand version. (b) an advisory `[wide-wrong-band]` when a `wrong` entry's `tol.abs` is more than half its own `|value|`.

### Per problem

- Chains. Every problem has a real chain and its last part asks for the result the problem is about. Parts that use no earlier answer and feed a later one: `p-loss-limit` 2, `p-loan-rate` 2, `p-eight-coupon` 2, `p-log-two` 3, `p-two-months` 3, `p-tail-bound` 3, `p-doubling-coefficients` 4 (a side result, used by no later part; acceptable as the l9 half of the item), `p-mixed-both-ways` 3, `p-dollar-holding` 2, `p-two-level-points` 2. All acceptable. `p-two-level-points` part 5 is a plain evaluation; its explanation earns it (the pit is local, since $2x^3$ falls without limit).
- Later parts restate what they need: yes, in every item. The rounded hand-offs each give an answer inside the part's band: £1,417.72 into the loss limit (35.3 from £1,418 too), $V$ and $V'$ to the penny into the Newton step, $x_2 = \tfrac{17}{14}$ with its exact $f$ and $f'$, 0.68854 into $\ln 2.1$ (0.73733 from the unrounded 0.6885417 too), 0.0118 into the square of the step (0.0029, 0.00295 and 0.0030 all taken).
- Answer form. Every numeric part with a non-whole answer names its form. 17 parts with a whole-number answer do not say "whole number"; none refuses a sensible entry.
- `wrong` entries: 255 (220 numeric, 35 `tex`). Every one differs from its answer, none is caught first by a neighbour, and every one is the value its named slip gives. Carried slips are present where a learner would carry one (the slope $\tfrac19$, the DV01 of £141,772, $c_3 = 24$, the four-term $\ln 2$, the ratio 0.1, the gradient $(-4, 2)$, the plane $6x + 8y - 45$, the quadratic without its cross term). The loose bands are finding 5.
- `p-square-geometric` part 3 takes $\tfrac{(k + 1)!}{k!}$ as correct. It is equal, and the feedback then shows the cancelling. No edit.
- `p-dollar-holding` part 4 refuses a lower-case $x$. The question says "an expression in $X$". No edit.
- `p-capital-limit` part 5 and `p-two-book-risk` part 5 take the exact value beside the estimate (51.875; 0.0029), as their `accept` lines promise.

Clean problems (14 of 21): taylor set 1 `p-loan-rate` (bar one printed digit, finding 6); set 2 all four; set 3 `p-doubling-coefficients`, `p-big-gain`; multivar set 1 all three; set 2 `p-slopes-around`, `p-fit-descent`; set 3 `p-two-level-points`, `p-capital-limit`.

### Per set

- Lessons. Every lesson of each level is drawn on (taylor l1 to l4, l5 to l8, l9 to l12; multivar l1 to l4, l5 to l8, l9 to l12), and each problem draws on at least two. The thinnest is `p-eight-coupon`: it is l8 throughout, with l5 only as the idea of a second-order term. Nothing is used before its level. Taylor level 1 uses no Taylor polynomial beyond the tangent and its $\tfrac12 f''h^2$ error; `p-newton-cubic` part 3 joins l2 (which side of its tangent) to l3, a join neither lesson makes. Level 2 hands over the interval $-1 < x \le 1$ and asks for no radius or test; `p-square-geometric` part 4 leans on l7's "works only for $-1 < x < 1$". Multivar level 1 has no gradient; `p-dollar-holding` part 5 applies l4's chain rule to $V_P$ with l3's second partials. Level 2 has no stationary point test. Level 3's `p-min-variance-pair` part 5 uses $\lambda$ as l11 teaches it.
- Difficulty. One 5 in each set (`p-loan-rate`, `p-log-two`, `p-tail-bound`, `p-dollar-holding`, `p-fit-descent`, `p-min-variance-pair`), and each earns it. Typed parts 94 of 101 (taylor 16 of 18, 18 of 20, 18 of 19; multivar 14 of 14, 15 of 15, 13 of 15). Each of the 7 choice parts is a judgement.
- Skills. All from `course.json`. `p-fit-descent` carries `mv-optimise`, a skill l8 and `review-2` also use.
- Voice. British spelling, no exclamation marks, no em-dashes, £ for money, explanations of at most three sentences (my own count in `forms.py` and `voice-scan.py 35`: 0 and 0). No option, `why` or feedback line names an option by place.

### Counts

| tag | taylor | multivar | tooling | total |
|---|---|---|---|---|
| `wrong` | 2 | 0 | 0 | 2 |
| `unclear` | 1 | 0 | 0 | 1 |
| `minor` | 6 | 2 | 1 | 9 |

### Verdict by set

| set | verdict |
|---|---|
| taylor `problems-1` | sound; findings 2, 5 (one band), 6, 7, 8 (new function for `p-cube-root-27`) |
| taylor `problems-2` | clean; no edit (finding 10 stands) |
| taylor `problems-3` | sound after finding 1; findings 3, 4, 5; finding 10 stands |
| multivar `problems-1` | clean; no edit |
| multivar `problems-2` | sound; finding 11 |
| multivar `problems-3` | sound; finding 9 (new assets for `p-min-variance-pair`) |

One fix pass on Sonnet covers all of it. Findings 8 and 9 change graded answers, so a delta reader should recompute those two items after the pass; finding 1 changes a question and three feedback lines; the rest change bands, digits and text only.

### Scripts (`docs/reviews/problems-1.3-b-scripts/`)

| file | what it does | run |
|---|---|---|
| `mine.py` | the reader's own answer and named-slip value for every numeric part, two routes, and every number in prose and feedback | `<venv>/bin/python`, exit 1: 2 failures, both finding 6 |
| `grade-check.mjs` | the engine's graders on every answer, `accept`, `wrong` and 191 typed strings; `--probe` prints 10 forms the reader was unsure of | `node ... --local-cdn <pkgs>`, exit 0, 9 FINDING rows |
| `proposed.py` | the numbers of every fix above, twice | `<venv>/bin/python`, exit 0 |
| `taught.py` | per lesson, counts of each idea a set leans on; `--show` prints the passages | `python3` |
| `forms.py` | form sentences, explanation length, voice, typed share, option length | `python3` |
| `fresh-grep.py` | each setup's formula and nouns across the course and the exams; `--show` prints the hits | `python3` |
| `dump.py`, `exprs.py` | compact dumps for reading | `python3` |

All run from the repo root.

## Fix pass

Applied by targeted edits to `taylor/problems-1.json`, `-3.json`, `multivar/problems-2.json`, `-3.json`; the two number scripts updated and exit 0 (`problems-taylor-numbers.py` 937 checks, `problems-multivar-numbers.py` 727 of 727, run with the scratchpad venv). `multivar/problems-4` and `-5` untouched. Item ids kept (`p-cube-root-27` now holds the fourth-root problem).

1. `p-two-months` part 5: fixed. Basis (my own): the item fixes the signs, with true errors $+16.10$ and $-4.33$ (in $10^{-5}$) from $\ln 1.08 - 0.0768$ and $\ln 0.95 + 0.05125$, so the real total error is their sum, 11.8, below the larger bound; a bound on a size ignores sign, so $17.07 + 4.86 = 21.93$ stays right for a question that says to ignore signs. Question, `subtracted`, `first-only`, `generic` and `explain` reworded as proposed; the whole item reads true (parts 2 and 4 explains state only true errors). The script now checks the signs and the total.
2. `p-newton-cubic` part 3 `below` `why`: fixed. Basis: for $f' > 0$ and $f'' > 0$ the tangent lies under the curve, so its zero sits at or above the root from either side; from $x_0 = 1$ the step gave 1.25 > 1.2134 (crossed), from $x_1$ it cannot cross. New `why` says so.
3. `p-tail-bound` part 4: fixed. `tol` 0.008; $10.67 / 0.92 = 11.598$ and $10.667 / 0.92 = 11.594$ both accepted, 11.58, 10.67, 11.85 and 16 refused (script).
4. `p-two-months` part 4: fixed. `tol` 0.01 ($2.33 \times 0.000125 / 6 = 4.854$ accepted, 4.17 refused); question now says what bound to find.
5. Five loose bands: fixed. `unscaled` `tol.abs` 0.000001 (part 2), 0.0000005 (part 4), 0.000001 (part 5), 0.000005 (`p-tail-bound` part 4); `one-lot` 0.005. The script checks that each holds its own value and refuses every other slip and nine unrelated small numbers. The validator now warns `[wrong-band]` on these five (a heuristic that ignores the units); raised in `docs/BACKLOG-INBOX.md`.
6. Printed terms: fixed. $4 \times 103 / 1.04^5 = 338.63397$ gives 338.6340 (two places; sum 354.4349); $3 / 1.05^4 = 2.4681074$ gives 2.468107 (sum of printed terms 5.102811, true sum 5.1028121, printed "5.10281" stands). Both recomputed twice in the script.
7. `p-newton-cubic` part 3 correct option: fixed, "Above: the tangent at $x_1$ reaches 0 before the curve does".
8. `p-cube-root-27`: fixed as proposed, the fourth root about 16 (my recompute: slope $\tfrac14 \cdot \tfrac18 = \tfrac1{32}$; $L(16.32) = 2.01$; $f''(16) = -\tfrac{3}{16} \cdot \tfrac{1}{128} = -\tfrac{3}{2048}$; error exactly $-0.000075$; corrected 2.009925 against the true 2.0099259). Part 4 `explain` says "within $0.000001$" instead of the reader's "matches to 5 places", which rounds either way.
9. `p-min-variance-pair`: fixed as proposed (40%, 25%, correlation 0.3; checked by sympy, a polynomial fit, a grid search and a line search; $w = 0.2$, $\sigma_p^2 = 0.056$, $\sigma_p = 0.2366$, $\lambda = 0.112$, estimate 0.05824 against exact 0.0582624). Part 4 no longer says "free" for numbers. Part 5 asks for 5 places, since the answer has five.
10. Freshness of `p-tail-bound` and `p-three-halves`: no edit, as ruled.
11. `p-two-book-risk` part 5: fixed, "shrinks with the square of the step".
12. Tooling: reader had no bullet in the inbox for it, so added under `Raised later (review problems 1.3 b):` in `docs/BACKLOG-INBOX.md` (freshness formula advisory, wide-band advisory, plus the `[wrong-band]` false positive on `unscaled` entries). No engine file edited.

Counts: 11 fixed, 0 disputed, 1 deferred to the engine (12), 1 no-edit by ruling (10).

### Graded answers, bands and `wrong` values changed (for the delta reader)

Taylor `problems-1`, `p-cube-root-27` (all four parts new; ids `slope-ninth`, `slope-third`, `ninth`, `third`, `ninth-carried` renamed `slope-eighth`, `slope-quarter`, `eighth`, `quarter`, `eighth-carried`):
- part 1 answer `3+\frac{x-27}{27}` to `2+\frac{x-16}{32}`; accept now `2+(x-16)/32`, `2+\frac{1}{32}(x-16)`, `\frac{3}{2}+\frac{x}{32}`, `1.5+x/32`; wrong `3+\frac{x-27}{9}`, `3+\frac{x-27}{3}`, `x^{1/3}+...` to `2+\frac{x-16}{8}`, `2+\frac{x-16}{4}`, `x^{1/4}+\frac{1}{4}x^{-3/4}(x-16)`.
- part 2 answer 3.03 to 2.01 (tol 5e-5); wrong 3.09, 3.27, 4.03 to 2.04, 2.08, 2.51.
- part 3 answer -0.0003 to -0.000075 (tol 5e-6 to 5e-7); wrong -0.0006, -0.00037, 0.0003 to -0.00015, -0.000234, 0.000075 (tol 5e-7).
- part 4 answer 3.0297 to 2.009925 (tol 5e-7); wrong 3.0303, 3.0294, 3.0897 to 2.010075, 2.00985, 2.039925 (tol 5e-7).
- `p-loss-limit` part 3 `one-lot`: 0.0354 unchanged, tol 0.5 to 0.005. Printed digits 338.6338 to 338.6340 (parts 2 feedback and explain), `p-loan-rate` part 2 explain 2.468108 to 2.468107 (no value changed).
- `p-newton-cubic` part 3: option text and `below` `why` only.

Taylor `problems-3`:
- `p-two-months` part 2 `unscaled` (0.0001707) tol 0.05 to 0.000001; part 4 answer 4.86 tol 0.005 to 0.01, `unscaled` (4.86e-05) tol 0.005 to 0.0000005; part 5 answer 21.93 unchanged (question and feedback only), `unscaled` (0.0002193) tol 0.05 to 0.000001.
- `p-tail-bound` part 4 answer 11.594 tol 0.005 to 0.008; `unscaled` (0.0011594) tol 0.005 to 0.000005.

Multivar `problems-3`, `p-min-variance-pair` (all five parts new):
- part 1 answer `0.1w^2-0.05w+0.04` to `0.1625w^2-0.065w+0.0625`; accept `\frac{w^2}{10}-\frac{w}{20}+\frac{1}{25}` to `\frac{13w^2}{80}-\frac{13w}{200}+\frac{1}{16}`; wrong `no-cross` `0.13w^2-0.08w+0.04` to `0.2225w^2-0.125w+0.0625`, `half-cross` `0.115w^2-0.065w+0.04` to `0.1925w^2-0.095w+0.0625`.
- part 2 answer 0.25 to 0.2; wrong 0.5, 0.75, 0.3077 to 0.4, 0.8, 0.2809.
- part 3 answer 0.1837 to 0.2366; wrong 0.03375, 0.225, 0.2 to 0.056, 0.28, 0.25.
- part 4 answer 0.0675 to 0.112; wrong 0.03375, 0.045 to 0.056, 0.064.
- part 5 answer 0.0351 (tol 5e-5) to 0.05824 (tol 0.0001); wrong 0.0344, 0.03375, 0.10125 to 0.05712 (tol 0.0001), 0.056 (tol 0.0001), 0.168 (tol 6e-5); `accept` added.

Multivar `problems-2` `p-two-book-risk` part 5: wording only.

### Gates

Validator 0 errors. `fresh-check.mjs --file` 0 hits on all four changed sets. `playthrough --problems` with `--local-cdn`, with and without `--mobile`: taylor 1, taylor 3, multivar 2, multivar 3 all passed. Voice scan 35: taylor 0 and 0, multivar 0 and 0. Number scripts: exit 0 both.
