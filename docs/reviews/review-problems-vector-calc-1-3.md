# Problem sets 1.13, vector-calc levels 1 to 3: second-reader findings

Scope: `app/content/courses/vector-calc/problems-1.json`, `-2`, `-3`: 12 problems, 54 parts (34 numeric, 19 `expression`, 1 choice), 113 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Author rules, Reader). Pattern: `review-problems-analysis-1-3.md`.

Method. The author's script was run first. Every part was then solved by hand from its text and again in `docs/reports/problems-vector-calc-numbers-read.py`, which imports nothing from the author's script and types every field, curve, region and surface from the prose. Each line, surface and flux integral is done twice, exactly, in sympy: directly (parametrise and integrate) and through the theorem the problem uses, or a second boundary form. The pairs are: the bead's work against Green on the closed half disc; the cubic loop against $\iint (1 - x)\,dA$; the potential's work on a straight and a bent path; the ellipse work for $k = 1$ and for a general $k$ with the whole field against curl times area; the rectangle's four edges against Green; the cycloid's area by $-\oint y\,dx$ and by $\oint x\,dy$, its moment by $\oint -\tfrac{y^2}{2}\,dx$ and by $\oint xy\,dy$; the triangle's three edge fluxes against the divergence; the plot's edges by the formula and by parametrising, its area by two triangles, its flux and circulation edge by edge; the roof's area in polar form and by rings, its flux directly and by closing it with a wall and a floor ($\nabla \cdot \mathbf F = 0$); the tank's six faces against the triple integral; the slanted ellipse by Stokes and by the line integral round $C$, also with $c$ as a letter; the can's side by parametrising it, by the closed surface, and by Stokes on side plus lid. Orientation was read at each use: which way each boundary runs, which normal each surface carries, and the sign each reversed path takes. Each "conservative" claim was checked by its curl and its domain (polynomial fields on the whole plane, no hole), each potential by differentiation. Every `wrong` value was rebuilt from the slip its line names, and every number after an "approx" sign was recomputed. Every typed part then went through the engine's own graders in node (`review-problems-vector-calc-1-3-scripts/grade-probe.mjs`: the key, one more place, a letter and `=`, a true minus sign, each `accept` form, each `wrong` entry on its own key, and 329 strings of my own: fraction against decimal, the rounding asked for and the next coarser one, other forms of each expression, exact multiples of $\pi$). `proposed.py` computes the numbers of the fixes of findings 1 to 4, each twice. Reuse was read by eye after `fresh.py` (formulas, numbers and nouns of each problem, normalised, across `app/content`), `find.py` (the learner text of the screen or item behind a hit) and `fresh-check.mjs --file`, with and without `--cross-numbers`. Scratch: `<scratchpad>/read-vector-calc/`.

Severities as the Reader brief names them: `wrong`, `misleading`, `reuse`, `voice`, `continuity`.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-vector-calc-numbers.py` 748 of 748, exit 0 |
| `problems-vector-calc-numbers-read.py` (reader's own keys, slips, printed numbers, set shape) | 818 checks, 0 failed, exit 0 |
| `grade-probe.mjs` (engine graders, 53 typed parts) | 698 checks, 329 reader rows, 0 failures, exit 0; 3 rows held to be faults (finding 6, Engine note 1); 13 NOTE rows (Engine note 2) |
| `proposed.py` (numbers of the fixes of findings 1 to 4) | 7 of 7, exit 0 |
| `grade-all.mjs --file`, three sets | 19, 17 and 18 widgets, 0 failures |
| validator | 0 errors, 4531 warnings, none on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file`, three sets | 0 hits each; with `--cross-numbers` 0 hits and 0, 15, 0 advisories (small whole numbers of the plot, other courses, as the author says). It lists none of findings 1, 2, 3, 4 or 7 |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 53 typed keys and the choice key agree with mine, by both routes. So does every one of the 113 `wrong` values, every accepted form and every printed number. Every orientation and sign is right: the cubic loop is anticlockwise (A below B), the cycloid boundary is anticlockwise with the arch run backwards, the triangle and plot corners are anticlockwise, the slanted ellipse carries the upward normal $(1, 0, 1)$, and the can's base takes $(0, 0, -1)$. Each conservative claim holds on the whole plane and each potential differentiates back to its field. No band overlaps another, and each rounding the part asks for is taken while the next coarser one is refused. No learner is marked wrongly: no `wrong` finding. The findings are reuse (five, of which four need new numbers), one term never taught, one part with more than one right answer, and three wording points.

| severity | count | findings |
|---|---|---|
| wrong | 0 | |
| misleading | 2 | 6, 8 |
| reuse | 5 | 1, 2, 3, 4, 7 |
| voice | 0 | |
| continuity | 3 | 5, 9, 10 |

## A. `problems-1`

1. `vector-calc/problems-1.json` | `items[0]` (`p-bead-semicircle`): `prose`, `parts[2]` to `parts[4]` | `reuse` | the work half of the problem is `review-1` `r4-clockwise` with the sign changed.
   Evidence: `review-1` `items[3]`: "the circle of radius 3 about the origin ... $\mathbf r(t) = (3\cos t, -3\sin t)$ ... the work of $\mathbf F = (-y, x)$ ... The integrand is $-9$, so $W = -18\pi$." Here $\mathbf F = (2x - y, x + 2y) = 2(x, y) + (-y, x)$, and the radial part does no work on a circle. So part 4 is the same circle, the same field in effect and the same integrand, 9, and part 5 its integral, $9\pi$. The author moved the can of `problems-3` off $x^2 + y^2 = 9$ for the bead's sake; the review's circle was missed.
   Fix (values in `proposed.py`): radius 6. No file of the course has $x^2 + y^2 = 36$ or $6\cos t$.
   - `prose`: "... along the upper half of the circle $x^2 + y^2 = 36$. The bead runs from $(6, 0)$ to $(-6, 0)$ along $\mathbf r(t) = (6\cos t, 6\sin t)$, $0 \le t \le \pi$. ..."
   - `parts[2]`: question "... $|\mathbf F| = 6\sqrt5$ on the circle ..."; `answer` 252.8933 ($36\sqrt5\,\pi$), `tol` 0.006; `wrong`: `no-speed` 42.1489, `squared` 3392.92 (`tol` 0.01), `full-circle` 505.7867. `correct`: "$\int_0^\pi 6\sqrt5 \cdot 6\,dt = 36\sqrt5\,\pi \approx 252.89$." `no-speed`: "... $|\mathbf r'(t)| = 6$. Here $ds = 6\,dt$, so the answer is six times yours." `squared`: "You integrated $|\mathbf F|^2 = 180$ instead of $|\mathbf F| = 6\sqrt5$." `explain`: "On the circle $x^2 + y^2 = 36$, so $|\mathbf F| = \sqrt{180} = 6\sqrt5$. The speed is $|\mathbf r'(t)| = 6$, so $\int_0^\pi 6\sqrt5 \cdot 6\,dt = 36\sqrt5\,\pi \approx 252.89$."
   - `parts[3]`: question with $(6\cos t, 6\sin t)$; `answer` 36; `wrong`: `position` 72, `magnitude` 180. `correct`: "$(12\cos t - 6\sin t)(-6\sin t) + (6\cos t + 12\sin t)(6\cos t) = 36\sin^2 t + 36\cos^2 t = 36$." `position`: "... which gives 72. Work uses the velocity $\mathbf r'(t) = (-6\sin t, 6\cos t)$." `explain`: "$\mathbf F(\mathbf r(t)) = (12\cos t - 6\sin t,\ 6\cos t + 12\sin t)$ and $\mathbf r'(t) = (-6\sin t, 6\cos t)$. The $\sin t\cos t$ terms cancel and $36\sin^2 t + 36\cos^2 t = 36$."
   - `parts[4]`: question "Using $\mathbf F \cdot \mathbf r' = 36$ from part 4, the work is $W = \int_0^\pi 36\,dt$. What fraction of $\int_C |\mathbf F|\,ds = 36\sqrt5\,\pi$ from part 3 ..."; `answer` and the three `wrong` values do not change (0.4472; 2.2361, 0.1424, 0.8944). `correct`: "$W = 36\pi$, and $\tfrac{36\pi}{36\sqrt5\,\pi} = \tfrac{1}{\sqrt5} \approx 0.447$." `generic`: "... integrating 36 over $0 \le t \le \pi$, then divide by $36\sqrt5\,\pi$." `no-integral`: "You divided 36 by $36\sqrt5\,\pi$. Integrate first: $W = 36\pi$." `full-circle`: "... the work is $36\pi$." `explain`: "The work is $36\pi \approx 113.10$. Divided by $36\sqrt5\,\pi$ it is ..." (rest as now).
   Parts 1 and 2 stand. $36\pi$ occurs in l7, l11 and homework-3 as a lone multiple of $\pi$ in other settings (an area, two fluxes); that is not a shared set.

2. `vector-calc/problems-1.json` | `items[1]` (`p-two-routes-cubic`): `prose`, `parts[1]` to `parts[4]` | `reuse` | the frame of `homework-1` `h1-two-paths`.
   Evidence: `homework-1` `items[0]`: "Take $\mathbf F = (y^2, x)$ from $(0, 0)$ to $(1, 1)$", the work along the curve $(t, t^2)$, the work along "the line $\mathbf r(t) = (t, t)$", then a choice "What do the two answers show?" with the options "no potential" and "$\mathbf F$ has a potential, but the paths differ in length". The problem has the same end points, the same second route $(t, t)$, the same closing choice and the same distractor ("may still be conservative: the two routes have different lengths"). l3 screens 2 to 4 also run $(0, 0)$ to $(1, 1)$ with $y = x$ as the second path. Field, first route and numbers are new; the setting is not.
   Fix (values in `proposed.py`): new end point and second route, and a loop work that comes out negative.
   - `prose`: "A field $\mathbf F(x, y) = (xy,\ x + y)$ moves a particle from $(0, 0)$ to $(2, 8)$. Route A is the cubic $\mathbf r(t) = (t, t^3)$ and route B the segment $\mathbf r(t) = (t, 4t)$, each for $0 \le t \le 2$."
   - `parts[0]`: unchanged (the integrand does not depend on the end point).
   - `parts[1]`: "... Give an exact fraction or a decimal to 1 place." `answer` 50.4 ($\tfrac{252}{5}$), `tol` 0.001; `wrong`: `no-dot` 12.4, `no-chain` 21.0667 ($\tfrac{316}{15}$). `correct`: "$\tfrac{32}{5} + 12 + 32 = \tfrac{252}{5} = 50.4$." `no-dot`: "That is $\int_0^2 (t^4 + t^3 + t)\,dt$, ..." `no-chain`: "That is $\int_0^2 (t^4 + t^3 + t^5)\,dt$, ..." `generic`: "Not quite. Integrate each power of $t$ from 0 to 2." `explain`: "$\int_0^2 t^4\,dt = \tfrac{32}{5}$, $\int_0^2 3t^3\,dt = 12$ and $\int_0^2 3t^5\,dt = 32$. They add to $\tfrac{252}{5} = 50.4$."
   - `parts[2]`: "Now route B, the segment $\mathbf r(t) = (t, 4t)$. ... Give an exact fraction or a decimal to 3 places." `answer` 50.66667 ($\tfrac{152}{3}$), `tol` 0.0005; `wrong`: `ds` 208.904 ($\times \sqrt{17}$, `tol` 0.001), `p-only` 10.6667, `q-only` 40, and a new `no-four` 20.6667 ($\mathbf r' = (1, 1)$: $\int_0^2 (4t^2 + 5t)\,dt = \tfrac{62}{3}$). `correct`: "$\mathbf F(t, 4t) = (4t^2, 5t)$ and $\mathbf r' = (1, 4)$, so $W = \int_0^2 (4t^2 + 20t)\,dt = \tfrac{152}{3} \approx 50.667$." `generic`: "Not quite. Put $x = t$ and $y = 4t$ into $\mathbf F$ and dot with $(1, 4)$." `ds`: "You multiplied by the length factor $\sqrt{17}$. ..." `p-only`: "You kept only $P\,dx = 4t^2\,dt$. The $Q\,dy = 20t\,dt$ term counts too." `q-only`: "You kept only $Q\,dy = 20t\,dt$. The $P\,dx = 4t^2\,dt$ term counts too." `no-four`: "You dotted with $(1, 1)$. On this segment $\mathbf r' = (1, 4)$." `explain`: "On the segment $\mathbf F = (4t^2,\ 5t)$ and $\mathbf r' = (1, 4)$. The integrand is $4t^2 + 20t$, and $\int_0^2 (4t^2 + 20t)\,dt = \tfrac{32}{3} + 40 = \tfrac{152}{3}$."
   - `parts[3]`: "... Using $\tfrac{252}{5}$ from part 2 and $\tfrac{152}{3}$ from part 3 ... Give an exact fraction or a decimal to 4 places." `answer` $-0.266667$ ($-\tfrac{4}{15}$), `tol` 6e-05; `wrong`: `added` 101.0667 ($\tfrac{1516}{15}$), `sign` 0.266667. `correct`: "$\tfrac{252}{5} - \tfrac{152}{3} = \tfrac{756 - 760}{15} = -\tfrac{4}{15} \approx -0.2667$." `sign`: "You did B minus A. Out along A is $+\tfrac{252}{5}$ and back along B is $-\tfrac{152}{3}$." `explain`: "Out along A the work is $\tfrac{252}{5}$. Back along B, reversed, it is $-\tfrac{152}{3}$. The loop total is $-\tfrac{4}{15} \approx -0.2667$." Green agrees: A lies below B, the loop is anticlockwise, and $\iint (1 - x)\,dA = -\tfrac{4}{15}$.
   - `parts[4]`: "Using the loop work $-\tfrac{4}{15}$ from part 4, ..."; option `b`: "$\mathbf F$ may still be conservative: the loop work is small beside the work on each route.", `why` "Small is not zero. A potential forces the loop work to be exactly 0."; `explain`: "... Here it is $-\tfrac{4}{15}$, so no potential exists. ..." Option `d` ("the work along each route is positive") still reads true of the numbers.
   None of $\tfrac{252}{5}$, $\tfrac{152}{3}$, $\tfrac{4}{15}$ or $(t, 4t)$ occurs in `vector-calc`, `multivar` or `integrals`.

3. `vector-calc/problems-1.json` | `items[2]` (`p-cubic-potential`), whole item | `reuse` (other course; a ruling is wanted) | the potential is the function of `multivar/review-1` `r1-partial-y` less its last term.
   Evidence: `multivar/review-1` `items[2]`: "Take $f(x, y) = x^3 + xy^2 + y$. Find $\partial f / \partial y$", key `2xy+1`, `wrong` `f-x` = `3x^2+y^2`. Here $\mathbf F = (3x^2 + y^2, 2xy)$ and part 3's key is $x^3 + xy^2$: the first component is that item's $f_x$ and the potential is its $f$ without the $+ y$. `multivar` is a prerequisite course. The author's report lists the hit and judges it "another course, another function". By the app-wide rule (DECISIONS session AB) a function is not shared; session AC let a common fraction stand, not a function. `multivar/l8` also uses $f = 3x^2 + y^2$.
   Fix if ruled reuse (values in `proposed.py`): $\mathbf F(x, y) = (4x^3 + 3y^2,\ 6xy)$, potential $f = x^4 + 3xy^2$. Neither occurs in `app/content`.
   - `parts[0]`: `answer` `(16, 12)`, `accept` `(16,12)`; `wrong` `y-not-squared` `(10, 12)`, `swap` `(12, 16)`. "$P = 4 + 12 = 16$ and $Q = 6 \times 1 \times 2 = 12$".
   - `parts[1]`: `answer` `6y`; `wrong` `px` `12x^2`, `qy` `6x`. "With $x$ fixed, $4x^3$ is a constant and $3y^2$ gives $6y$. So $P_y = 6y$, which matches $Q_x = 6y$ on the whole plane."
   - `parts[2]`: `answer` `x^4+3xy^2`, `accept` `3xy^2+x^4`; `wrong` `double` `x^4+6xy^2`, `wrong-var` `x^4+3x^2y`. "$\int P\,dx = x^4 + 3xy^2 + g(y)$, and $f_y = 6xy + g'(y) = Q$ forces $g$ constant".
   - `parts[3]`: `answer` 69 ($f(2, 3) = 16 + 54 = 70$, $f(1, 0) = 1$); `wrong` `end-only` 70, `double` 123 ($16 + 108 - 1$).
   If the item is kept as it is, the report should record the pairing as ruled, not as "another function".

## B. `problems-2`

4. `vector-calc/problems-2.json` | `items[2]` (`p-triangle-flux`): `prose`, all four parts | `reuse` | the region is the triangle of `multivar/problems-5` and the shadow of `homework-3`.
   Evidence: `multivar/problems-5` `items[2]`: "A triangular field has corners $(0, 0)$, $(4, 0)$ and $(0, 2)$", with a double integral over it and "the slanted edge $x = 4 - 2y$". Here: "the triangle $T$ with corners $(0, 0)$, $(4, 0)$ and $(0, 2)$", a double integral over it and the same long edge. `vector-calc/homework-3` `items[1]`: "The plane $x + 2y + z = 4$ meets the axes at $A = (4, 0, 0)$, $B = (0, 2, 0)$ ...", whose shadow in the $xy$-plane is this triangle. The report says the triangle was moved here from $(0, 0), (2, 0), (0, 2)$ (homework-2 h9); it landed on another used region. Part 2's key $\tfrac{64}{3} \approx 21.33$ is also the printed answer of `integrals/l8` screen 5.
   Fix (values in `proposed.py`): corners $(0, 0)$, $(3, 0)$ and $(0, 6)$; no file of `vector-calc`, `multivar` or `integrals` pairs them. Every answer becomes a whole number.
   - `prose`: "... over the triangle $T$ with corners $(0, 0)$, $(3, 0)$ and $(0, 6)$. ..."
   - `parts[0]`: unchanged.
   - `parts[1]`: "... Give a whole number." `answer` 36, `tol` 0; `wrong`: `curl` 27, `rectangle` 108, `only-p` 18 (all `tol` 0). `correct`: "$\int_0^3 4x(6 - 2x)\,dx = 108 - 72 = 36$." `generic`: "... with $y$ from 0 to $6 - 2x$." `rectangle`: "You integrated over the rectangle $[0, 3] \times [0, 6]$. In $T$, $y$ runs from 0 up to $6 - 2x$." `explain`: "... For each $x$, $y$ runs from 0 to $6 - 2x$, so the integral is $\int_0^3 (24x - 8x^2)\,dx = 108 - 72 = 36$."
   - `parts[2]`: "... the left edge, from $(0, 6)$ down to $(0, 0)$ ..." `answer` $-18$; `wrong`: `sign` 18, `tangent` 0. `correct`: "... $\int_0^6 (-y)\,dy = -18$." `generic`: "... integrate over $0 \le y \le 6$." `explain`: "... and $\int_0^6 (-y)\,dy = -18$: fluid flows in there."
   - `parts[3]`: "... The total is 36 from part 2, and the left edge gives $-18$ from part 3. Find the outward flux across the long edge from $(3, 0)$ to $(0, 6)$. Give a whole number." `answer` 54, `tol` 0; `wrong`: `add-edge` 18, `all-out` 36. `correct`: "$36 - 0 - (-18) = 54$." `add-edge`: "You added $-18$ to the total. The three edges add up to 36, so the long edge is $36 - (-18)$." `explain`: "The edges add to 36, so the long edge carries $36 + 18 = 54$. A direct check with $\mathbf r(t) = (3 - 3t, 6t)$ and $\int (P\,dy - Q\,dx)$ gives the same."

5. `vector-calc/problems-2.json` | `items[1]` (`p-cycloid-arch`): `prose`, `parts[2].question`, `parts[4]` | `continuity` | "centroid" is taught nowhere.
   Evidence: neither "centroid" nor "centre of mass" occurs in any file of `app/content` outside this problem. Part 5 asks for "the height $\bar y$ of the centroid" with no formula; a learner who has not met the word can only guess, then read it in the `generic` line. The idea itself is taught under another name: l10 "Mean height of a dome" (an integral divided by an area), `multivar` l13 "average height".
   Fix: name it as the course does.
   - `prose`: "... We find its area and the mean height of its points, $\bar y = \tfrac{1}{A}\iint_D y\,dA$, from the boundary alone."
   - `parts[2].question`: "For the mean height we need $\iint_D y\,dA$ as a boundary integral. ..." (see finding 6 for the rest).
   - `parts[4].question`: "Using the area $3\pi$ from part 2 and $\iint_D y\,dA = \tfrac{5\pi}{2}$ from part 4, find the mean height $\bar y$ of $D$. Give an exact fraction or a decimal to 3 places."
   - `parts[4].feedback.generic`: "Not quite. The mean height is $\iint_D y\,dA$ divided by the area."
   - `parts[4].explain.text`: "... The arch is 2 high, so the mean height sits below half way: most of the area is low down." (True: 62% of the area lies below $y = 1$, checked in the reader's script.)

6. `vector-calc/problems-2.json` | `items[1].parts[2]` (`p-cycloid-arch`, part 3) | `misleading` | the question has more than one right answer and takes one.
   Evidence: "Find $P(x, y)$, with $Q = 0$, so that Green's theorem gives $\oint P\,dx = \iint_D y\,dA$." Any $P = -\tfrac{y^2}{2} + g(x)$ does this, since only $P_y$ enters. `grade-probe.mjs`: `-\frac{y^2}{2}+x` and `-\frac{y^2}{2}+1` are refused on the generic line "Choose $P$ so that $-P_y = y$", which they satisfy. Writing $P(x, y)$ invites an $x$ term.
   Fix, question (with finding 5): "For the mean height we need $\iint_D y\,dA$ as a boundary integral. Find $P$, a function of $y$ alone with $P = 0$ on the axis $y = 0$, so that Green's theorem with $Q = 0$ gives $\oint P\,dx = \iint_D y\,dA$." The key, forms and slips stand. Part 4's explanation already says "On the axis $P = 0$".

## C. `problems-3`

7. `vector-calc/problems-3.json` | `items[0]` (`p-saddle-roof`): `prose`, `parts[2].question`, `parts[3].question` and four feedback strings | `reuse` | the story is l10's opening.
   Evidence: l10 screens 1 and 2, "Rain on a roof": "A roof $z = ax$ covers the unit square", its normal $(-a, 0, 1)$, its area $\sqrt{1 + a^2}$ against its shadow, and the flux of the rain through it, upward positive. The problem is a roof, its normal, its area against the flat disc ("The saddle is tilted") and the upward flux through it. Surface, field and numbers are new; the story and its order are the lesson's.
   Fix: a canopy and wind ("canopy" is in no file of `app/content`). `prose`: "A canopy has the shape of the saddle $z = xy$ over the disc $x^2 + y^2 \le 3$, written $\mathbf r(x, y) = (x, y, xy)$. We find its normal, its area, then the upward flux of the wind $\mathbf F = (y, x, 5)$ through it." `parts[2].question`: "... find the area of the canopy. ..." `parts[3].question`: "... up through the canopy. ..." No other string names the roof. The item id may stay.
   Not raised: the surface $z = xy$ is also `multivar/l13`'s first example (a volume over a rectangle). It is the standard saddle, on another region with another task.

8. `vector-calc/problems-3.json` | `items[1]` (`p-open-tank`): `prose`, `parts[3]` | `misleading` | "five walls".
   Evidence: "the flux out through the five walls of the open tank". A tank has four walls and a floor. The explanation then lists "the wall $x = 4$", "the wall $y = 1$" and "the rest", so the floor $z = 0$ is counted as a wall without being named. A learner may take "walls" as the four sides; the answer is the same only because the floor gives 0.
   Fix: `prose`: "... We find the flux out of the closed box, then the flux out through the four walls and the floor of the open tank." `parts[3].question`: "... Find the flux out through the four walls and the floor of the open tank. Give a whole number." `generic`: "Not quite. The walls, the floor and the lid make the closed box." `added`: "You added the lid. The walls, the floor and the lid together give 40, so take the lid away." `explain`: "The closed box gives 40 and the lid 24, so the walls and floor give $40 - 24 = 16$. As a check, the wall $x = 4$ has $\mathbf F \cdot \mathbf n = 4z$, giving 8, the wall $y = 1$ has $y^2 = 1$ over area 8, and the rest, floor included, give 0."

## D. All three sets

9. `problems-1.json` `items[3].prose`; `problems-2.json` `items[0].prose`, `items[0].parts[1].feedback.byKey.reversed`, `items[0].parts[3].feedback.byKey.direction`, `items[1].parts[1].question`, `items[3].prose`, `items[3].parts[3].question`; `problems-3.json` `items[2].prose`, `items[2].parts[1].feedback.byKey.down`, `items[3].parts[2].question` | `continuity` | the sets say "anticlockwise"; the course says "counterclockwise".
   Evidence: the lessons, reviews and homework of `vector-calc` use "counterclockwise" 112 times and "anticlockwise" never (l6 23, l7 22, l12 14: it is the word in the statements of Green's and Stokes' theorems). The three sets use "anticlockwise" 10 times and "counterclockwise" never. The orientation word is the one a learner must match to the theorem.
   Fix: replace "anticlockwise" by "counterclockwise" in the ten strings ("clockwise" in `reversed` stays). If the main session prefers the British word, the change belongs in the lessons, as a separate item; the sets and the lessons should not differ.

10. `vector-calc/problems-2.json` | `items[2].parts[1].explain.text`, `items[3].parts[2].explain.text` | `continuity` | "The flux form of Green's theorem" is not the course's name.
   Evidence: l8 names it "Green in normal form" (screen title) and "the normal form" (five more times); "flux form" occurs in no lesson.
   Fix: "The normal form of Green's theorem gives ..." in both strings.

## Notes, no fix asked

- Chain shape. `p-saddle-roof` part 4 (flux) uses part 1, not part 3 (area); `p-quadrilateral-plot` parts 3 and 4 both use part 2; `p-can-curl` part 3 uses part 1. Each is a tree, not a line, and each last part is the result the prose names. Every part that uses a value restates it.
- Coverage. Every lesson of each level is drawn on, as the report's tables say. Nothing beyond the level is needed once finding 5 is fixed. Skills are those of the level's lessons.
- Judged, not raised (other courses, one component of a field): `exams/stage-1` `a-directional` has $f = xy^2 + 2x$, the $Q$ of `p-rectangle-edges`; `complex/problems-2` `items[1]` has $u = 2xy + 3x$, the $Q$ of `p-ellipse-family`, and integrates $2y + 3$ to $y^2 + 3y$ as part 2 here does. Neither is the object the problem is about. If the main session rules these reuse, `p-rectangle-edges` moves with $Q = xy^2 + 5x$ (curl $9 - 2y^2$, total 25, right edge 16, top edge 9); I have not costed the ellipse family.
- `p-cycloid-arch` part 5 explain read "well below half way" for $\tfrac56$ against 1; finding 5's text drops "well".

## Engine

1. `expression` has no "expanded" form. `p-bead-semicircle` part 2 asks for $|\mathbf F|^2$ "with no brackets" and takes `(2x-y)^2+(x+2y)^2`, the definition retyped (`grade-probe.mjs`, 1 row). Part 3 hands over the result, so little is lost here.
2. A `numeric` field cannot read $\pi$ or a surd: `20\pi`, `3\pi`, `-16\pi`, `\frac{14\pi}{3}`, `9\sqrt5\pi` and `1/\sqrt5` do not parse (13 NOTE rows). Thirteen parts of these sets have such a value as their natural answer and ask for decimals, which each question says. The course's own lessons take `16\pi` in `expression` fields, so the habit is there.
3. `fresh-check.mjs --file` gives no line for findings 1, 2, 4 or 7: a shared curve with a shared integrand under a different field, a shared pair of end points with a shared second route, a shared polygon given by its corners (across courses and against a plane's intercepts), a shared story noun in a lesson title.

Inbox bullets: `docs/BACKLOG-INBOX.md`, `Raised later (review problems vector-calc):`.

## Fix pass

Each corrected number was recomputed here twice (sympy exact, scipy quad on the field itself) in `docs/reports/problems-vector-calc-numbers.py`, and again by the reader's script. Before pasting, `app/content/` was grepped for the new region, integrand, curve, field, potential and key numbers: no hit outside the problem itself (the `(0, 6)`, `6 - 2x` and `36\pi` hits are other settings: a normal distribution, a slope line, a Jacobian, lone multiples of pi in l7, l11, homework-3 and `eigen`).

1. fixed: `p-bead-semicircle` on the circle of radius 6, `r(t) = (6 cos t, 6 sin t)`. Keys: part 3 252.8933 (`36 sqrt5 pi`), part 4 36, part 5 unchanged 0.4472. Slips: no-speed 42.1489, squared 3392.92, full-circle 505.7867, position 72, magnitude 180. Also checked by Green on the closed half disc (curl 2, area 18 pi, diameter 0) and the whole circle 72 pi.
2. fixed: `p-two-routes-cubic` from (0, 0) to (2, 8), A `(t, t^3)`, B `(t, 4t)`, `0 <= t <= 2`. Keys: 252/5 = 50.4 (asked to 1 place), 152/3 = 50.66667, loop -4/15 = -0.266667 (also by Green, A below B). Slips: no-dot 12.4, no-chain 21.0667, ds 208.904, p-only 10.6667, q-only 40, new no-four 20.6667, added 101.0667, sign 0.266667. The choice keeps option a; option b now reads "the loop work is small beside the work on each route".
3. fixed (ruling: reuse is app-wide): `p-cubic-potential` with `F = (4x^3 + 3y^2, 6xy)`, potential `x^4 + 3xy^2`. Keys: (16, 12), 6y, the potential, work 69 (f(2, 3) = 70, f(1, 0) = 1; also on a straight and a bent path). Slips: (10, 12), (12, 16), 12x^2, 6x, x^4 + 6xy^2, x^4 + 3x^2 y, 70, 123.
4. fixed: `p-triangle-flux` on the triangle (0, 0), (3, 0), (0, 6). Keys: 36 (whole number), -18, 54. Slips: curl 27, rectangle 108, only-p 18, sign 18, tangent 0, add-edge 18, all-out 36. Edges 0, 54, -18 add to 36; the long edge was also checked by parametrising `(3 - 3t, 6t)`.
5. fixed (ruling: wording the course teaches): "centroid" is gone; the prose defines the mean height as `(1/A) iint_D y dA` and parts 3 and 5 say "mean height". Explanation: "sits below half way" (62% of the area lies below y = 1, as the reader checked).
6. fixed (ruling: make P unique): part 3 asks for "P, a function of y alone with P = 0 on the axis y = 0". Key and forms unchanged. `-y^2/2 + x` and `-y^2/2 + 1` satisfy `-P_y = y` but break the stated conditions, so they are two new `wrong` entries (`x-term`, `constant`) with their own lines. Real grader (`review-problems-vector-calc-1-3-scripts/grade-probe.mjs`, rows updated): both refused on their own line, `-y^2/2`, `-y^2/2` in the accepted spellings still graded correct, 703 checks and 0 failures.
7. fixed: `p-saddle-roof` is a canopy in the wind (prose, parts 3 and 4, the "tilted" line in `flat`). No "canopy" elsewhere in `app/content`.
8. fixed: `p-open-tank` says "the four walls and the floor" in prose, part 4 question, its three feedback lines and the explanation (now two sentences, so the `O2` warning does not appear).
9. deferred: main session ruling. The sets keep "anticlockwise" (British; 40 files of the app use it); the vector-calc lessons get their own pass.
10. fixed: "The normal form of Green's theorem" in `p-triangle-flux` part 2 and `p-quadrilateral-plot` part 3.

Changed keys: `problems-1` p-bead-semicircle parts 3 and 4; p-two-routes-cubic parts 2, 3 and 4; p-cubic-potential parts 1 to 4. `problems-2` p-triangle-flux parts 2 to 4. Fixed counts: 9 fixed, 0 disputed, 1 deferred. Graded answers changed: 12 (and 2 `wrong` entries added in p-cycloid-arch part 3, 1 in p-two-routes-cubic part 3).

Gates (worktree):
- `problems-vector-calc-numbers.py`: 782 of 782, exit 0. `problems-vector-calc-numbers-read.py`: 826 checks, 0 failed. Both fail on the old values (keys, slips, wording checks).
- `grade-probe.mjs`: 703 checks, 0 failures, 1 row held (Engine note 1).
- validator: 0 errors; voice scan 35: 0 and 0; `manifest.json` restored.
- `grade-all.mjs --file`: 19, 17 and 18 widgets, 0 failures.
- `playthrough.mjs --problems vector-calc/problems-1`, `-2`, `-3`, with and without `--mobile`: All passed.
