# Delta read: fix passes of problems 1.3 c, 0.2 a, 0.3 a and 0.2 b

Scope: only what the four fix passes changed, read at commit fc8c221. `changed.py` lists 42 items and 95 parts in 17 files, and confirms no file has changed since its fix pass.

- Fix pass 1.3 c (e9f5825): `limits/problems-4` and `-5`, `integrals/problems-4`, `multivar/problems-4`. 11 items, 25 parts. Record: `review-problems-1.3-c.md`, "Fix pass".
- Fix pass 0.2 a (7e7560d): `equations/problems-2` and `-3`, `functions/problems-1` to `-3`. 12 items, 30 parts. Record: `review-problems-0.2-a.md`.
- Fix pass 0.3 a (418c8ae, 6313ee2, 8513198): `counting/problems-1` to `-3`, `functions/problems-4`. 11 items, 21 parts. Record: `review-problems-0.3-a.md`.
- Fix pass 0.2 b (cbb69dc, fda93b7, 53224ff): `quadratics/problems-1` to `-3`, `equations/problems-4`. 8 items, 19 parts (the four parts of `p-cliff-stone` are story only). Record: `review-problems-0.2-b.md`.

Method. Each of the 42 changed items was read whole as it now stands (`dump.py`). The re-authored items (`p-corner-sprinkler` part 1, `p-drone-landing`, `p-path-and-pipe`, `p-sledge-cyclist` parts 1 and 2, `p-track-cubic`, the ice-cream item, `p-cinema-block`, `p-allotment-plots`, `p-bus-chase` parts 3 and 4) were solved from the text before the key was read. `recompute.py` then recomputes every changed answer, band and `wrong` value twice: exactly (sympy, fractions) and by a second route (quadrature and a Cartesian double integral for the sprinkler and the drone, a root-finder for the 90% radius, the crossing times and $\sqrt{40}$, a second difference for $V''(0)$, a grid search for the foot of the pipe and the cubic's roots, turning points and level line, a search over whole pence, and enumeration of every cup, cone, purchase, line-up, seat and whole-number pair). The same script checks, on all 187 single-value numeric parts of the 17 files, that no two bands of a part meet and that every `wrong` id has its `byKey` line. `grade.mjs` runs the engine's own graders (`grade.js` with the local Compute Engine, the shape check of `expression.js`) on every answer, `accept` form and `wrong` entry of the 42 items and on 641 typed strings (`typed.mjs`): each printed value, the sensible roundings, each slip as typed, the old keys, and the forms the fixers reported as refused. `stale.py` searches each re-authored item for numbers and words of its old version. `fresh.py` searches all 2,297 content files for the new numbers, formulae and story words; I then read the lessons, reviews, homework and exams it pointed at. Authors' scripts, the validator, the voice scan, `fresh-check` and the playthrough were run.

Scripts: `docs/reviews/delta-problems-aa-2-scripts/`, run from the repo root: `changed.py [--dump]`; `dump.py <file> [item ...]`; `recompute.py` (scratchpad venv Python); `grade.mjs --local-cdn <pkgs> [--show]` with `typed.mjs`; `stale.py`; `fresh.py [--all]`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways; `minor` = otherwise.

## Tool results

- `recompute.py`: 2,202 checks, 0 failures; 2 FINDING rows (findings 1 and 3).
- `grade.mjs`: 2,443 checks, 0 failures; 7 FINDING rows (findings 1, 5, 6 and 7). Every answer and `accept` form grades correct, every `wrong` entry lands on its own key, every old key is refused.
- `stale.py`: 9 hits, one of them stale (finding 3). `fresh.py`: 135 hits, judged under findings 2, 4 and 8 and in "Verified clean".
- Authors' scripts, all 0 failures: limits 1,269 checks, integrals 1,087, multivar 731, equations 1,154, functions 787, functions-4 444, counting 1,759, quadratics 646.
- `node tools/validate.mjs`: 0 errors. On the 17 files: three `[wrong-band]` warnings (below) and three `[O2-long-sentence]` advisories on restated questions of counting 1 and 3.
- `voice-scan.py 35` on the seven course folders: 0 and 0. `fresh-check.mjs --file` on the 17 sets: 0 hits each.
- `playthrough --problems` on all 17 sets, with and without `--mobile`: all passed.
- No changed answer, band or `wrong` value is wrong. No two bands meet.

## Rulings asked for

1. `p-car-park` part 2, $\tfrac{5t-4}{2}$: a learner is marked wrongly. The question asks only for "as simply as possible", the fraction is true and has nothing left to collect, and the line it gets ("open the bracket and collect the numbers into one") names work already done. An `accept` entry cannot fix it: the shape check runs on what was typed, after the match, so the fraction is still refused with it listed (`grade.mjs`, last block). The fix is a reworded question and `form` line: finding 5.
2. `p-salt-solutions` part 1, `0.15x+0.4y=0.25(x+y)`: no learner is marked wrongly. The question now asks for the salt in the 500 g batch "as one number", so a right-hand side in $x$ and $y$ is not what was asked. Its line is true and gives the cure. `15x+40y=25(x+y)`, $\tfrac{x+y}{4}$ on the right and `2x=3y` get the same line; `0.25(500)`, `(0.25)(500)`, `500(0.25)`, $\tfrac{500}{4}$ and either order of the left side are accepted. No edit.
3. `p-sprinkler-bank` part 1, `\frac{5x}{2}-\frac{x^2}{2}`: as now worded, no learner is marked wrongly. The question prints $0.5x^2$ and says "Keep the decimals, as in $1.5x$", so turning the given decimals into fractions is not a reasonable thing to type, and the line repeats the instruction. A small fault in the line remains: finding 7.

## Findings: fix pass 1.3 c (limits 4 and 5, integrals 4, multivar 4)

1. `minor` | `integrals/problems-4.json` | `p-dish-and-spindle` | part 3, `accept` line.
   "accepted as $0.141 \pm 0.001$" prints a band about the rounded figure. The engine's band sits about the key 0.14076, from 0.13976 to 0.14176, so the printed end 0.142 is refused. No working I could build lands on 0.142 (the 4-place route gives 0.1404, the exact one 0.1408), so no learner is marked wrongly. Same class as finding 1 of `review-delta-problems-1.3-ab.md`. The ten lines of review finding 7 have refused ends with more places than their parts ask for; `p-level-annuity` part 5 is exact.
   Fix: "$\\pi\\left(\\tfrac{5}{3} + 4\\ln\\tfrac{2}{3}\\right) \\approx 0.141$ (0.140 is accepted too)".

2. `minor` | `multivar/problems-4.json` | `p-drone-landing` | part 4, freshness against the topic exam.
   `exams/topic-1.3.json` item `c-gauss-disc`: "Their joint density is $\tfrac{1}{2\pi}e^{-(x^2 + y^2)/2}$. What is $P(X^2 + Y^2 \le 1)$? Give 4 decimal places." Key 0.3935, and its explanation ends "only about 39% of the time". Part 4 here is the same disc of one $\sigma$ with the same key and the same 4 places, and part 5 prints "from 39% to 90%". The fix pass did not bring this in (the old part, 2 m with $\sigma = 2$, had the key too), and `fresh-check` does not see it. The exponent 32, $\sqrt{32\pi}$, $\tfrac{1}{32\pi}$ and 8.58 are in no multivar file or exam; $\tfrac{1}{4\sqrt{2\pi}}$ is only a distractor of l16 screen 9.
   Fix proposed (numbers in `recompute.py`, "proposed"): part 4 asks for "within 6 m". Answer 0.6753 ($1 - e^{-9/8}$, radial integral $16(1 - e^{-9/8})$), `tol` unchanged. `r-not-squared` 0.1710 ($1 - e^{-6/32}$; "at $r = 6$ it is $-\tfrac{36}{32}$"), `no-2pi` 0.1075, `outside` 0.3247 ("Within 6 m it is $1 - 0.3247$"). Part 5: "which is 0.6753 at $a = 6$", and the explanation ends "The radius grows by under a half to go from 68% to 90%" ($8.58 / 6 = 1.43$). None of the four values is in multivar or the exam. Or rule that it stands: the density, the scale and parts 1 to 3 and 5 are new. For the main session; the edit changes graded values of one part.

## Findings: fix pass 0.2 a (equations 2 and 3, functions 1 to 3)

3. `wrong` | `functions/problems-3.json` | `p-track-cubic` | part 2, `byKey` `count`.
   "The track meets the floor at two places: one from the factor $x$ and one from $(x - 3)^2$." The line survives from the old curve. The track is now $x(x - 6)^2$, printed in the question above it, and 3 is not a root. A learner who types one value is sent to a factor that is not there. Every other string of the item was changed (`stale.py`); the author's script and the playthrough do not read `count` lines.
   Fix: "The track meets the floor at two places: one from the factor $x$ and one from $(x - 6)^2$. Give both, separated by a comma."

4. `minor` | `functions/problems-2.json` | `p-path-and-pipe` | freshness.
   Neither new line ($4x + 9$, $-0.25x + 26$), nor B, D or the meeting point $(4, 25)$, is in the course or the 0.2 exam. The point $A(-2, 1)$ is the first point of `review-2` item 4, "Find the line through $(-2, 1)$ and $(2, 9)$". So parts 1 and 2 share that item's two steps on A: a run that subtracts $-2$, and $c = 1 + 2m$. The review's line is $y = 2x + 5$.
   Ruling proposed: stands, no edit. One point is shared; gradient, intercept, the second point and parts 3 to 5 are new, and moving A re-authors all five parts again. For the main session to confirm.

## Findings: fix pass 0.3 a (counting 1 to 3, functions 4)

5. `wrong` | `functions/problems-4.json` | `p-car-park` | part 2, `form` (ruling 1).
   $\tfrac{5t-4}{2}$ and `(5t-4)/2` are refused with "That is equal, but open the bracket and collect the numbers into one." There is no bracket and one number. The shape test is also uneven: `\frac{5t}{2}-\frac{4}{2}` and `2.5(t-0.8)` pass, `0.5(5t-4)` and `2(1.25t-1)` do not. The case is rare, since the prose is in decimals. Without the `form`, the unworked `3+2.5(t-2)` passes again, so the `form` stays.
   Fix (text only; key, `accept`, `wrong` and `form` unchanged): question "On the piece for $t > 2$, open the bracket and collect the numbers. Write the charge as $C(t) = at + b$, with $a$ and $b$ as decimals or whole numbers. Type only what comes after the $=$ sign." `byKey` `form`: "That is equal, but write it as one $t$ term and one number, as in $0.8t + 1.5$. Open any bracket and collect the numbers." The single fraction is then outside the stated form, and its line is true of it. The engine bullet in the inbox stands.

6. `minor` | `counting/problems-3.json` | `p-sail-ring` | part 3, `form`.
   Review finding 4 is fixed for the line it named: `\frac{2}{3}(\frac{1}{2}r+\frac{1}{2}s)` now returns `form`. The same unworked line typed as `\frac{2}{3}\cdot\frac{1}{2}(r+s)` still passes, as does `\frac{2}{6}r+\frac{2}{6}s`: the engine multiplies bare numbers before the size test. The key, both `accept` forms, $\tfrac{r+s}{3}$, $\tfrac{r}{3} + \tfrac{s}{3}$ and either order pass, so no right answer is refused.
   Fix: none in content. One line for the inbox under `Raised later (review problems 0.3 a)`: form "simplified" does not see an unmultiplied product of two numbers.

## Findings: fix pass 0.2 b (quadratics 1 to 3, equations 4)

7. `minor` | `quadratics/problems-3.json` | `p-sprinkler-bank` | part 1, `byKey` `form` (ruling 3).
   `\frac{5x}{2}-\frac{x^2}{2}` and `2.5x-\frac{x^2}{2}` get "That is equal, but collect the $x$ terms into one and keep the decimals, as in $1.5x$." Its first half is untrue of them: the $x$ terms are collected. The acceptance is uneven too ($\tfrac{5}{2}x - \tfrac{1}{2}x^2$, `\frac{5x}{2}-0.5x^2`, $\tfrac{5x - x^2}{2}$ and `0.5x(5-x)` pass), which is the engine row already in the inbox.
   Fix: `form` line "That is equal, but type it with decimals, as in $1.5x$, and with the $x$ terms collected into one." It is then true of the fraction typings and of the unworked `3x-0.5x-0.5x^2`.

8. `minor` | `quadratics/problems-1.json` | `p-cinema-block` | parts 2 and 4, freshness.
   Review finding 1 had two halves. The product is fixed: $x^2 + 15x + 44$, $x^2 + 15x + 36$ and $(x + 3)(x + 12)$ are in no 0.2 file. The other half, a list of pairs the level already prints, moved from 18 to 36. `l2-product-and-sum` quiz item 3 is "Factorise $x^2 - 12x + 36$", with options $(x - 6)^2$ and $(x - 4)(x - 9)$ and the line "$-4$ and $-9$ multiply to 36 but add to $-13$". Part 2's two slips are its mirrors: `sum-thirteen` $(x + 4)(x + 9)$ and `square` $(x + 6)^2$. `homework-1` item 6 keys "$(x + 6)^2 = x^2 + 12x + 36$", the `why` of part 4's option `six`.
   Ruling proposed: stands, no edit. The quadratic and its answer pair (3 and 12) are new. From 44 only three removals leave whole factors with sum 15 (14, 26 and 36), and 36 alone gives a search of more than two pairs. For the main session to confirm.

## The three `[wrong-band]` warnings

All three are narrow bands the reviews asked for, each on a decimal slip under a whole-number question; none needs an edit.

- `limits/problems-5` `p-impact-curve` part 4 `not-inverted` (0.0031, band 0.0005) and `integrals/problems-4` `p-dish-and-spindle` part 4 `inverse` (0.0687, band 0.005). Rounded as the question asks, each slip is 0, and a band wide enough for 0 was the fault the reviews found: it told 0.4, 0.141 and 0 something untrue. The bands take 0.003, 0.00308 and 0.0031; 0.069 and 0.07.
- `functions/problems-3` `p-sledge-cyclist` part 3 `lost-t` (2.449, band 0.05). Rounded, the slip is 2, which now gets the generic line ("Both sides have a factor $t$. Divide it out"), the cure. The band takes 2.4, 2.45 and 2.449 and refuses 2.5, which is now part 2's answer.

## Verified clean

- Each original finding was really fixed. 1.3 c: 1 to 11, with 12 in the inbox. 0.2 a: 1, 2 and 4 to 20, bar the one line of finding 14 that finding 3 here names; its finding 3 is in the inbox. 0.3 a: 1 to 15, with the residues of its findings 13 and 4 in findings 5 and 6 here. 0.2 b: 1, 2 and 5 to 11, with the half of finding 1 noted in finding 8; 3 and 4 are in the inbox.
- `p-corner-sprinkler` part 1: $x = r\cos\theta$, $y = r\sin\theta$ give $d = 9 - r^2$. The engine takes `-r^2+9`, `3^2-r^2` and `(3-r)(3+r)`, gives `9-r` and `9r-r^3` (and `r(9-r^2)`) their keys, and refuses the retyped `9-(x^2+y^2)` and the old key. The chain runs 1 to 5: $9r - r^3$, 20.25, $\tfrac{81\pi}{8} = 31.81$ (also by a Cartesian double integral).
- `p-drone-landing`: $\int e^{-x^2/32}\,dx = 4\sqrt{2\pi} = 10.0265$ (sympy and quadrature); plane $32\pi$ (double quadrature); $c = \tfrac{1}{32\pi} \approx 0.0099$; within 4 m $1 - e^{-1/2} = 0.3935$ (closed form and a double integral over the disc); $a = \sqrt{32\ln 10} = 8.58$ (bisection), and $8.58 / 4 = 2.15$. Slips: 1.7725, 0.3133, 14.1796; 0.1175, 0.0626, 0.6065; 73.68, 1.84, 5.66. `4\sqrt{2\pi}` and `8\sqrt{2\pi}` go to `not-squared` and `doubled`; every old key is refused. No stale 8, $\sigma = 2$ or 2 m is left.
- `p-level-annuity` part 5 takes 9.0634, 9.0635, 9.0636 and the printed 9.06345, and refuses 9.0633, 9.0637 and the 4-place 9.065. `p-barbell-hedge` part 4: £43 and 42.81 accepted, 45 to `second-order` ($\tfrac12 \times 900 \times 0.0001$ thousand, by sympy and a second difference), 47 to `wrong-way`, 44 and 46 to no key. `p-dish-and-spindle` part 3 takes 0.140, 0.1404, 0.141; part 4 takes 14.5 to 15.
- `p-path-and-pipe`: gradient 4, $c = 9$, pipe $-0.25$, $c = 26$, meeting at $(4, 25)$ between A and B (line through two points by sympy; the foot by a grid search). Slips 0.25, 9.333; `4x+1`, `4x-7`, `0.25x+1.5`; 0.25, $-4$, 4; `-0.25x+23`, `-0.25x+20`, `0.25x+20`; 25, 4.533, 8.235. The engine takes `28/7`, `-1/4`, `\frac{104-x}{4}` and `-0.25(x-12)+23`.
- `p-sledge-cyclist`: 12.5 m, 2.5 m/s (below the cyclist's 3); slips 2.5, 6.25, 25; 62.5, 12.5. Fresh: the functions course has no $0.5t^2$, no distance of 12.5 m and no average over 5 seconds (l12 and `homework-3` keep $t^2$ at 4 seconds).
- `p-track-cubic`: $x(x - 6)^2$, $h(4) = 16$, roots 0 and 6, turning points $(2, 32)$ and $(6, 0)$, falling only on $2 < x < 6$, $h = 32$ at 2 and 8 with $h - 32 = (x - 2)^2(x - 8)$ (sympy and a grid of 801 points). Slips 400, $-36$. Fresh: no such cubic, height or turning point in functions or the exam (the exam's cubic is $x^3 - 3x$).
- `p-bakery-trays`: part 4 is the choice keyed `left`, part 5 the profit 80 (vertex and grid), and part 5 restates part 4. `p-climbing-wall` part 4: 728 is the best whole-pence price by search; 728 goes to `pence`, £7.28 is accepted. `p-interest-split`: `12,000-s` is still refused, and both questions now say so.
- Ice-cream item: 364 cups, 2,184 cones, 2,548 items and 12,740 purchases, each by formula and by listing every one; all ten slips recomputed. No 11, 165, 990, 1,155 or 5,775 is left, and "orders" no longer means purchases. Fresh: 14 flavours, $\binom{14}{3}$, 2184, 2548 and 12740 are in no other content file, and "flavours" and "scoops" in no 0.3 course or exam; 364 appears only as $\tfrac{364}{365}$ and in unrelated sums. Team line-up: 720 and 192 by listing all $7!$ orders; no "photo" is left.
- `p-ticket-bonus` part 2: `5n-100`, `-100+5n`, `5(n-20)` pass; `0.2(25n-500)`, $\tfrac{25n - 500}{5}$ and $\tfrac{1}{5}(25n - 500)$ return `form`, whose line is true of each.
- `p-cinema-block`: 3 and 12 are the only pair of 36 with sum 15; 286 by rows of seats, $294 - 8$ and $13 \times 22$; slips 294, 266, 256; no whole $k$ has $2k = 15$; options `six` (8 seats out) and `five` (19 seats out) are right in their `why` lines.
- `p-allotment-plots`: $(x + 5)(x + 6)$, $(x + 5)(2x + 9)$ (9 and 10 the only pair of 90 with sum 19), $3(x + 5)^2$, 300 at $x = 5$ as $110 + 190$. `(x+5)(3x+15)` and the expanded form return `form`. Fresh: neither quadratic is in a 0.2 file; $(x + 5)^2$ is l2's perfect square, here only inside a new total.
- `p-bus-chase` part 3: $(t - 3)^2 - 3$, roots $3 \pm \sqrt{3}$ (formula, bisection); 1.27 and 1.268 accepted, 1.26, 1.28 and the old 1.59 refused; slips 4.73205, $-0.4641$, 0. Part 4 takes 6.32, 6.325, 6.33 ($6.32^2 < 40 < 6.33^2$) and refuses 6.31 and 6.34. Fresh: $t^2 - 6t + 6$ is in no 0.2 file. It shares the step $\sqrt{12} = 2\sqrt{3}$ with l7's first quiz item ($x^2 + 2x - 2$, roots $-1 \pm \sqrt{3}$): one surd, another equation, so it stands.
- `p-cliff-stone` is now the flare: no "stone", "cliff", "throw" or "beach" is left, the numbers are unchanged and right, and "flare", "deck" and "ship" are in no 0.2 course or exam (`fresh.py`; elsewhere a ship sails in counting l9 and a deck is a deck of cards).
- `p-canal-arch` part 3: the three listed forms and $20 - \tfrac{(x-10)^2}{5}$ pass; `y=...` is still refused, and the question now says to leave it out. `p-remote-cars`: $49 + 32 = 81$, 9 s, 18 m.
- Wording only, read and true: `p-signal-decay` part 3, `p-app-adoption` part 5, the ten `accept` lines and the `unit-rule` line of integrals 4, `p-climbing-wall` parts 1 and 3, `p-cottage-share` part 1, `p-bakery-stock` part 1, `p-fridge-temperature` part 4, `p-stone-throw` parts 2, 4 and 5, `p-two-savers` part 4, `p-two-cultures` parts 3 and 4 ($2^{3.3} = 9.849$, $2^{3.4} = 10.556$), the restated values of counting 2 and 3, `p-photo-mount` parts 2 and 3.
- Outside the delta, noted in passing: `p-bus-chase` parts 1 and 2 (unchanged) use $t^2 - 6t + 10$, discriminant $36 - 40 = -4$, square form $(t - 3)^2 + 1$. `l8-how-many-solutions` quiz item 1 is $x^2 + 6x + 10$ with "$36 - 40 = -4$" and "$(x + 3)^2 + 1$". Not raised by the first read; for the main session.

## Counts

| tag | 1.3 c | 0.2 a | 0.3 a | 0.2 b | total |
|---|---|---|---|---|---|
| `wrong` | 0 | 1 | 1 | 0 | 2 |
| `unclear` | 0 | 0 | 0 | 0 | 0 |
| `minor` | 2 | 1 | 1 | 2 | 6 |

Findings 1, 3, 5 and 7 are text edits with no graded value changed; a fix pass on Sonnet covers them without a further delta read. Finding 6 is one inbox line. Findings 2, 4 and 8 need a ruling: 4 and 8 are proposed to stand, and 2 carries a proposed edit that changes the graded values of one part.
