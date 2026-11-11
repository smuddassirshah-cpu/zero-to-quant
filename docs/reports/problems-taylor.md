# Problem sets: taylor (brief `docs/briefs/chained.md`)

Files: `app/content/courses/taylor/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-taylor-numbers.py` (exits 0, 900 checks).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-cube-root-27 | 4 (4 / 0) | l1, l2 | 3 |
| problems-1 | p-newton-cubic | 4 (3 / 1) | l3, l1, l2 | 4 |
| problems-1 | p-loss-limit | 5 (4 / 1) | l4, l1, l2 | 4 |
| problems-1 | p-loan-rate | 5 (5 / 0) | l3, l4, l1 | 5 |
| problems-2 | p-three-halves | 5 (5 / 0) | l5, l6 | 3 |
| problems-2 | p-square-geometric | 5 (4 / 1) | l6, l7 | 4 |
| problems-2 | p-eight-coupon | 5 (5 / 0) | l8, l5 | 4 |
| problems-2 | p-log-two | 5 (4 / 1) | l7, l6, l5 | 5 |
| problems-3 | p-doubling-coefficients | 5 (4 / 1) | l9, l10 | 3 |
| problems-3 | p-two-months | 5 (5 / 0) | l11, l12 | 4 |
| problems-3 | p-tail-bound | 5 (5 / 0) | l9, l11 | 5 |
| problems-3 | p-big-gain | 4 (4 / 0) | l9, l10, l11, l12 | 4 |

Typed parts: level 1 16 of 18, level 2 18 of 20, level 3 18 of 19. Expression parts: p-cube-root-27 part 1 ($L(x)$), p-square-geometric part 3 ($c_k = k + 1$). Every lesson of each level appears in at least one problem, and every problem draws on at least two lessons of its level. Each set has one item at difficulty 5.

Chains. Level 1: the tangent to $\sqrt[3]{x}$ at 27, its estimate, the predicted $\tfrac12 f''h^2$ error, then the corrected value. Newton on $x^3 + x - 3$ for three steps, with the side of the root read from the sign of $f''$. A bond's price, slope and position DV01, then the yield rise that hits a £50,000 loss limit and why the true loss is smaller. A loan's value, slope and duration, then two Newton steps to its rate (duration and Newton use the same tangent). Level 2: $x^{3/2}$ about 4 coefficient by coefficient to $P_3(4.4)$; $(1 - x)^{-2}$ by matching derivatives, where it fails, and $\tfrac{1}{0.81}$; a bond's bend, convexity, then duration and duration plus convexity prices; $\ln 2$ from the log series at $x = -\tfrac12$ carried into a cubic for $\ln 2.1$. Level 3: ratio, limit, radius, comparison at 0.4 and the closed interval; two monthly log returns, the alternating bound, a case where it fails and Lagrange holds, and the bound on the sum; $T_3$ for $e^{0.4}$, Lagrange against a geometric tail bound, and bounds on both sides; the log series diverging at $r = 1.8$, then $\ln 2.8 = \ln 2 + \ln 1.4$ with its error bound.

Every later part restates the value it needs. Every numeric part names its form ("Give a decimal to 4 places", "to the nearest pound", "in units of $10^{-5}$, to 1 decimal place"), and the script checks that the value at those places is accepted and that the number printed last in `feedback.correct` lies inside the band. Parts asked in units of $10^{-k}$ carry an `unscaled` wrong entry for a learner who types the raw value.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (900 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (18 parts) | green (20 parts) | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The validator's `[shown-arithmetic]`, `[wrong-band]`, `[key-length]` and `O2-long-sentence` warnings fired on drafts; every one was fixed, not silenced.

## Fresh-check

Gate (`node tools/fresh-check.mjs --file ...`): 0 hits on each set. Loosened (`--min-run 8 --min-share 0`), judged:

- problems-1: 7 hits, all stock phrasing: "pays a # coupon at the end of each year" (series l5, l13), "at the end of each of the next # years" (markets l4, review-1, homework-1; series l13), and a form sentence shared with conditional problems-1. Two first drafts were replaced after reading the homework by hand, not because of a hit: a price, slope, duration, tangent and sign item and a Newton-for-yield item matched `homework-1` `h-long-bond` (a)-(e) and (g) in story. They became the loss-limit item and the loan-rate item.
- problems-2: 24 hits; 22 are the form sentence "Give an exact fraction, or a decimal to # places" shared with other sets, one is `homework-1` `h-long-bond` ("a # year bond pays a # coupon each year and # face"), one is problems-1 of this course. A first draft of the convexity item used a 3-year bond at 6%, the setting of `homework-2` `h2-par-convexity`; it was moved to a 4-year 8% bond at 7%.
- problems-3: 3 hits; "series alternates and its terms shrink, what is the most the error" (l11 quiz, review-3) is the stated condition of the alternating bound, kept because the part needs it. `p-big-gain` shares the idea of l10's transfer (a big gain makes the log series diverge) but asks for the remedy, splitting $2.8 = 2 \times 1.4$, which no screen does.

## Notes for the second reader

- `p-loan-rate` applies modified duration to a loan's repayments ("treat the loan as a bond the lender holds"). l4 defines $D = -P'/P$ for any price of cash flows, so no new idea is used.
- `p-two-months` part 4 shows that the first-left-out rule fails for $r = -0.05$ (every term is negative): the true error $4.33 \times 10^{-5}$ exceeds $\tfrac{0.05^3}{3} = 4.17 \times 10^{-5}$, and Lagrange gives $4.86 \times 10^{-5}$. The script checks all three numbers.
- `p-doubling-coefficients` part 5 tests the ends by the sizes $\tfrac{1}{n^2}$, the reasoning of l10's quiz `q-basel-ends` on a different series.
- l12's volatility drag result is not used in level 3, so no part needs a standard deviation.
