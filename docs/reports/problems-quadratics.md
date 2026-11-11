# Problem sets: quadratics (brief `docs/briefs/chained.md`)

Files: `app/content/courses/quadratics/problems-1.json` to `problems-4.json`. Numbers: `docs/reports/problems-quadratics-numbers.py` (exits 0, 857 checks with level 4; 634 for levels 1 to 3).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-cinema-block | 4 (3 / 1) | l1, l2 | 3 |
| problems-1 | p-allotment-plots | 4 (4 / 0) | l2, l3 | 4 |
| problems-1 | p-steel-plates | 5 (5 / 0) | l1, l3, l4 | 5 |
| problems-2 | p-cliff-stone (flare) | 4 (4 / 0) | l5, l6 | 3 |
| problems-2 | p-bus-chase | 4 (4 / 0) | l6, l7, l8 | 5 |
| problems-2 | p-can-stack | 4 (4 / 0) | l5, l7, l8 | 4 |
| problems-3 | p-canal-arch | 4 (4 / 0) | l9, l10, l11, l12 | 4 |
| problems-3 | p-bike-hire | 5 (4 / 1) | l10, l11, l12, l13 | 5 |
| problems-3 | p-sprinkler-bank | 4 (4 / 0) | l10, l11, l12 | 3 |

Typed parts: level 1 12 of 13, level 2 12 of 12, level 3 12 of 13. Every lesson of a level appears in at least one problem and every problem draws on at least two. The two choice parts are judgements: whether any square block can be left (the middle term $2kx$), and whether the profit band lies inside or outside the roots.

Level 1 (expressions only; nothing is solved). Cinema: expand $(x + 4)(x + 11)$, take out 8 seats and factorise, evaluate, then the judgement. Allotments: two factorisations (product and sum; split the middle term), the shared bracket joined into $3(x + 5)^2$ (plots $x^2 + 11x + 30$ and $2x^2 + 19x + 45$) fully factorised, then evaluated. Steel plates: $36x^2 - 9$, fully factorised as $9(2x + 1)(2x - 1)$, a wider plate expanded and factorised by splitting (or as a difference of squares), then evaluated.

Level 2. Flare fired from a ship's deck (was a stone from a cliff; story changed in the second-read fix): completed square gives the greatest height, the landing time from it, the deck-level times by factorising (the lost root $t = 0$ has its own `count` line), then two times to 2 places. Bus: discriminant negative, the smallest gap from the square, a second runner's catch time (Sam starts 6 m behind: $3 \pm \sqrt{3}$, 1.27 s), then the slowest speed for one root. Cans: 120 cans factorised, 100 cans by discriminant and formula, then the cans left over.

Level 3. Arch: line of symmetry from the roots, the top, the completed square form, then the width above a barge's height. Bike hire: zero-demand price, best price halfway, most revenue, the best price with a unit cost (half the cost added), then the band where profit is at least £525. Sprinkler: the gap between water and bank, where they meet, the landing height, then the greatest gap at the gap's own vertex.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (634 checks for the three sets) | same | same |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (13 parts) | green (12 parts) | green (13 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

Besides the script, every answer, accept form and wrong form, and 85 typed strings, went through the engine's own graders in node (`grade.js` with the local Compute Engine and the form checks of `expression.js`): 248 checks, 0 failures. The typed strings include the equal-but-unshaped forms ($(x + 4)(3x + 12)$, $(6x + 3)(6x - 3)$, $9(4x^2 - 1)$, $-0.2x(x - 20)$ all return `form`), sets in either order, `1 ± 0.63`, and roundings at the stated places.

## Review 1.3 faults avoided

- Bands take the printed working. Each 2-place part has `tol` 0.005 on the unrounded key, which takes the 2-place value and the 3-place figure the feedback prints (1.268, 13.651, 6.32; 0.37 and 1.63). The slowest-speed part has `tol` 0.006, so 6.32, 6.325 and 6.33 are all taken ($6.32^2 < 40 < 6.33^2$, so a careful learner rounds up). The 3.125 part takes 3.13 and 3.12.
- Every numeric `accept` is a plain number the field reads; none promises a surd or a form.
- No `%` units in these sets. Integer answers need no form; every other numeric part names one ("to 2 decimal places", "as a decimal").
- Slips from the part before carry their own `wrong` where a learner would carry them ($q = 10$ into the landing time; a discriminant of 401 into the root; $(x + 3)(x + 6)$ into the seat count; $36x^2 - 5$ into the plate area).
- No `wrong` value is close to the key or broad: the widest band is 0.02, on 2.414.

## Fresh-check

All three sets: 0 hits at the gate and 0 at `--min-run 8 --min-share 0`.

Read by hand against the course's lessons, quizzes, reviews, homework and `topic-0.2`: the course uses desks, firms, subscriptions, data feeds, bonds, portfolios, rectangles by perimeter and a trading floor. These sets use a cinema, allotments, steel plates, a stone off a cliff, a bus chase, a can stack, a canal arch, bike hire and a sprinkler. Shapes that recur, judged acceptable: a unit cost moving the best price by half (bike hire part 4) is l13's trap and `review-3` `r3-profit-price`, with demand $150 - 5p$ and a cost of £8 (theirs $500 - 10p$ with £4, $60 - 4p$ with £2, $300 - 15p$ with £6); a common factor before a difference of squares (plates part 2) is the skill of l4's $3x^2 - 48$ and `homework-1` `h-eighteen`, here $36x^2 - 9$; a constant chosen for one root (bus part 4) is l8's $k$ ladder, here a speed.

## Engine limits

One bullet to `docs/BACKLOG-INBOX.md` under "Raised later (problems quadratics)": `form: "expanded"` takes an uncollected expansion, the second course to want an expanded-and-simplified form.

## Level 4

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-park-pond | 5 (5 / 0) | l14, l18, l19 | 5 |
| problems-4 | p-windy-ride | 5 (5 / 0) | l15, l16 | 4 |
| problems-4 | p-storage-crate | 5 (5 / 0) | l15, l17 | 4 |

Typed parts: 15 of 15. Every lesson of the level appears in at least one problem and every problem draws on at least two. Skills: `quad-rational` (l14 to l17), `quad-solve` and `quad-graph` (l16, l18, l19).

Park pond: the radius from the centre $(-2, 3)$ to a lamp post at $(4, 11)$ (10 m), the circle's equation, where the path $y = x + 7$ crosses (a numeric set, 4 and $-10$), the path's length in the pond as $a\sqrt{2}$ (14), then the $c > 0$ for which $y = x + c$ is a tangent, from the discriminant ($5 + 10\sqrt{2} \approx 19.14$). Windy ride: 16 km out at $v$ and 9 km home at $v - 2$; the top over $v(v - 2)$ ($25v - 32$), both roots of the 3.5-hour equation (8 and $\tfrac{8}{7}$, to 2 dp), the speed out once $\tfrac{8}{7}$ is rejected, the time home over the time out as one fraction ($\tfrac{9v}{16(v - 2)}$), then its value at $v = 8$ (0.75). Storage crate: $V(-2) = 0$ for $V(x) = x^3 + 4x^2 + x - 6$, the quotient by $(x + 2)$, the full factorisation, the height $\tfrac{V(x)}{x^2 + 5x + 6} = x - 1$, then the volume at a height of 2.5 m (89.375).

Each later part restates what it uses ("Using $(x + 2)^2 + (y - 3)^2 = 100$", "Using $v = 8$ or $v = \tfrac{8}{7}$", "Using $V(x) = (x + 2)(x + 3)(x - 1)$"), and carries a `wrong` for the answer that follows from the commonest slip before it: the crossing points from the centre's signs flipped ($-0.26$ and $-7.74$), the roots from the top $25v - 18$ (8.54 and 0.60), and the ratio at the rejected root ($-0.75$).

### Checks

| check | problems-4 |
|---|---|
| numbers script | 0 failures (223 new checks; 857 for the four sets). Two methods each part: sympy against a whole-number search, the grid of the circle, the rational search $\tfrac{k}{7}$ for the roots, the distance $\tfrac{c - 5}{\sqrt{2}} = 10$ for the tangent, the remainder by long division, floats for the volume; the circle part is checked as an equation (ratio of the two sides a non-zero constant) |
| validator | 0 errors, no warning on the file (4,664 in all, as before) |
| playthrough `--local-cdn` | green (15 parts) |
| playthrough `--mobile` | green; 440 px shots of every part read, no fault |
| voice scan 35 (course folder) | 0 and 0 |
| grader probe | 27 typed strings through `grade.js` `exprGrade` with the local Compute Engine (scratch script, not committed): the circle in either order and expanded passes, each named slip routes to its key, and the unexpanded top, the factorised quotient, the unfinished factorisation and both uncancelled heights return `form`. The one gap: the division typed back in windy ride part 4 passes (inbox) |

### Review 4 faults avoided

- No rule stated without its reason: the tangent comes from the discriminant (l19), the root rejected because the speed home would be negative, the cancelling from factorising the base.
- Each 2 dp part has `tol` 0.005 on the unrounded key, which takes the printed 19.14 and 1.14; the expression parts accept the expanded circle and reordered forms, and `form` refuses an unfinished factorisation or an uncancelled height.

### Fresh-check

0 hits at the gate and at `--min-run 8 --min-share 0`. One advisory: the formula $x^2 + 5x + 6$ also opens l15 (`screens[1]`), as the top of the hook fraction; here it is the crate's base, the product $(x + 2)(x + 3)$ of two factors of $V$. A stock quadratic, judged acceptable. Read by hand: l18 measures from $(1, 2)$ to $(4, 6)$, so the pond uses $(-2, 3)$ to $(4, 11)$; l19 meets $x^2 + y^2 = 25$ with $y = x + 1$ ($x^2 + x - 12$), here $x^2 + 6x - 40$; l16 has a share bought with equal sums of money, here a ride; l17's cubics have roots $\{1, -2, 3\}$ and $\{1, 2, -3\}$, the crate $\{1, -2, -3\}$.

### Engine limits

One bullet to `docs/BACKLOG-INBOX.md` under "Raised later (fluency and problems quadratics 4)": a part that asks for a ratio of two algebraic fractions in simplest form (windy ride part 4) also accepts the division typed back unsimplified.
